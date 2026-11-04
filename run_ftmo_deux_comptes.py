"""Deux comptes FTMO 1-Step 10k tradés en même temps (demande du 2026-11-04) : compte A = mom, compte B = 3n + M2.
EXPLORATOIRE, hors compteur.

uv run python run_ftmo_deux_comptes.py → results/ftmo_deux_comptes/ (run.log, departs.csv, septembre_<compte>.csv)

Règles de trading (objectif 2 R partout ; éval 2,5 % de risque par trade, financé 1 %) :
  A : mom chaque nuit (20:00 → 9:30, SL 2 ATR / TP 4 ATR M15) ;
  B : nuit 3n (20:05 → 03:00, SL 2 ATR / TP 4 ATR M15) si signal ; si 3n est sorti au stop ou au TP, pas de M2 ce
      jour-là ; si 3n est sorti à 03:00 (ni stop ni TP) ou s'il n'y a pas de 3n, M2 (9:35 → 15:55, SL 4 ATR / TP 8 ATR
      M15) avec une taille qui garde la journée entre -r et +2 r : rho = min(r + x, (2 r - x) / 2), x = résultat de 3n
      la nuit (0 sans 3n), r = 2,5 % en éval, 1 % en financé (borné par la marge jusqu'au plancher).
Règles FTMO (relues le 2026-11-04) : objectif +10 %, perte max 10 % sous le plus haut solde (remise à zéro après un
reward), perte du jour 3 %, meilleur jour ≤ 50 % du gain net (comptes commandés depuis le 12/10/2026), reward possible
à partir du 14e jour après le 1er trade du compte (ici 10 jours de bourse, tradés ou non ; calendaire dans le rejeu de
septembre),
demandé dès qu'il est permis, 90 % versés, nouveau compte gratuit ensuite. En éval, l'objectif de chaque trade est ramené
au reste à faire s'il est sous 2 R (atteint si le mouvement favorable maximal du trade le dépasse). Une éval ratée ou un
compte perdu est racheté le jour suivant (79 € = 86,90 $). Coût CFD 1,5 point par trade au niveau actuel du NQ.
Données : trades avec objectif 2 R et MFE (cache/propfirm/nq_nuit_tp4_mfe.parquet, results/propfirm_combo/trades_tp2.csv),
2011-07 → 2026-08-28 ; rejeu de septembre sur la fenêtre déjà vue du holdout (avenant A du n° 26), jusqu'au 2026-11-03.
Simulation : un départ tous les 5 jours de bourse entre 2011-07 et 2025-08, 12 mois de trading à partir de chaque départ.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_septembre as S
from propfirm.ftmo import DAILY, EUR, MAXLOSS, MIN_RISK, PRICES_EUR, SPLIT, TARGET

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/ftmo_deux_comptes")
COST = 1.5 / 25_684.0
R_EVAL, R_FUND, TP_R, CYCLE = 2.5, 1.0, 2.0, 10
FEE = PRICES_EUR[10_000] * EUR
SIZE = 10_000
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def bibliotheque() -> pd.DataFrame:
    """Une ligne par trade : date (séance), strat, R brut, s (stop en fraction du prix), MFE en R."""
    m = pd.read_parquet("cache/propfirm/nq_nuit_tp4_mfe.parquet")
    m = pd.DataFrame({"date": pd.to_datetime(m.night), "strat": "mom", "R": m.R_brut,
                      "s": m.risk.fillna(m.risk.median()), "MFE": m.MFE_R})
    t = pd.read_csv("results/propfirm_combo/trades_tp2.csv", parse_dates=["date"])
    t = t.rename(columns={"R_brut": "R", "MFE_R": "MFE"})[["date", "strat", "R", "s", "MFE"]]
    hist = pd.concat([m, t], ignore_index=True)
    hist = hist[(hist.date >= "2011-07-01") & (hist.date <= "2026-08-28")]
    # fenêtre déjà vue (2026-08-31 → 2026-11-03), mêmes règles et même code
    import run_propfirm_combo as C
    w = C.trades("cache/holdout_anticipe/brut/NQ_v0_1m.parquet", "2026-08-31", "2026-11-03", "2026-11-04")
    w = w.rename(columns={"R_brut": "R", "MFE_R": "MFE"})[["date", "strat", "R", "s", "MFE"]]
    mw = S.trades().rename(columns={"night": "date", "MFE_R": "MFE"})[["date", "R", "s", "MFE"]].assign(strat="mom")
    lib = pd.concat([hist, w, mw], ignore_index=True).sort_values("date").reset_index(drop=True)
    # règle des annonces en financé (build_news_trades.py) : trades mom coupés à 8:19, M2 coupés à 13:55
    news = pd.read_parquet("cache/propfirm/news_trades.parquet")[["date", "strat", "R_news", "MFE_news"]]
    lib = lib.merge(news, on=["date", "strat"], how="left")
    lib["R_news"] = lib.R_news.fillna(lib.R)
    lib["MFE_news"] = lib.MFE_news.fillna(lib.MFE)
    return lib


class Compte:
    """Un emplacement FTMO : éval puis financé, racheté après chaque échec."""

    def __init__(self, nom: str, calendaire: bool = False, annonces: bool = False, politique: str = "actuel"):
        self.nom, self.calendaire, self.annonces, self.politique = nom, calendaire, annonces, politique
        self.evals, self.cash, self.rewards, self.events = 1, -FEE, 0, []
        self._nouveau("éval")

    def _nouveau(self, phase: str):
        self.phase, self.P, self.hi, self.best, self.cyc, self.f0 = phase, 0.0, 0.0, 0.0, 0, None

    def _regle_ok(self):
        return self.P > 0 and self.best <= 0.5 * self.P + 1e-9

    def jour(self, d: pd.Timestamp, legs) -> float:
        """`legs` : fonction (risque de base, pnl déjà fait ce jour) -> liste de (R, c, MFE, risque) jouée en ordre.
        Renvoie le P&L du jour (% du capital)."""
        if self.phase == "financé" and self.f0 is not None:  # reward demandé avant de trader ce jour
            date_ok = (d - self.f0).days >= 13 if self.calendaire else self.cyc >= CYCLE
            if date_ok and self._regle_ok():
                self.cash += SPLIT * self.P / 100 * SIZE
                self.rewards += 1
                self.events.append((d, f"reward {SPLIT * self.P:.2f} % ({SPLIT * self.P / 100 * SIZE:,.0f} $)"))
                self._nouveau("financé")
        r = R_EVAL if self.phase == "éval" else R_FUND
        floor = self.hi - MAXLOSS
        base = min(r, self.P - floor)
        if base < MIN_RISK:
            return self._echec(d)
        pnl, traded = 0.0, False
        fin = self.phase == "financé"
        for R, c, mfe, Rn, mfen, risk in legs(base, r):
            if fin and self.annonces:  # règle des annonces : trade coupé avant la fenêtre interdite
                R, mfe = Rn, mfen
            if fin and "attente" in self.politique and self.f0 is not None and self.P > 0 and                     max(self.best, pnl) <= 0.5 * self.P + 1e-9:
                break  # règle des 50 % respectée : on attend la date du reward
            risk = min(risk, self.P - floor)
            if risk < MIN_RISK:
                continue
            traded = True
            if self.phase == "éval":  # objectif ramené au reste à faire
                need = max(TARGET - self.P, 2 * max(self.best, pnl) - self.P, 0.01)
                k = need * (1 + c) / risk + c
                if k < TP_R and mfe >= k:
                    R = k
            elif "cible" in self.politique and self.P > 0:  # viser juste ce qui manque pour la règle des 50 %
                b = max(self.best, pnl)
                need = 2 * b - self.P + 0.01
                if b > 0.5 * self.P and need <= b + 1e-9:
                    k = need * (1 + c) / risk + c
                    if k < TP_R and mfe >= k:
                        R = k
            leg = risk * (R - c) / (1 + c)
            self.P += leg
            pnl += leg
            if self.P <= floor + 1e-9 or pnl <= -DAILY:
                return self._echec(d)
        if not traded:  # jour sans trade (attente, ou pas de signal) : l'horloge du reward avance quand même
            if self.f0 is not None:
                self.cyc += 1
            return 0.0
        self.f0 = d if self.f0 is None else self.f0
        self.cyc += 1
        self.best, self.hi = max(self.best, pnl), max(self.hi, self.P)
        if self.phase == "éval" and self.P >= TARGET - 1e-9 and self._regle_ok():
            self.events.append((d, f"éval n° {self.evals} validée"))
            self._nouveau("financé")
        return pnl

    def _echec(self, d):
        self.events.append((d, f"{self.phase} perdu ({self.P:+.2f} %) → nouvelle éval"))
        self.evals += 1
        self.cash -= FEE
        self._nouveau("éval")
        return np.nan


def jambes_A(row):
    def f(base, r):
        x = row.get("mom")
        return [] if x is None else [(*x, base)]
    return f


def jambes_B(row):
    def f(base, r):
        out = []
        n3, m2 = row.get("3n"), row.get("M2")
        x = 0.0
        if n3 is not None:
            out.append((*n3, base))
            sortie_temps = -0.999 < n3[0] < TP_R - 1e-3
            if not sortie_temps:
                return out
            x = base * (n3[0] - n3[1]) / (1 + n3[1])  # résultat de la nuit 3n (sans réduction d'objectif)
        if m2 is not None:
            rho = max(0.0, min(base + x, (2 * base - x) / 2))
            if rho > 0:
                out.append((*m2, rho))
        return out
    return f


def tableau(lib: pd.DataFrame) -> list[tuple[pd.Timestamp, dict]]:
    jours = []
    for d, g in lib.groupby("date"):
        row = {s: (float(x.R), COST / float(x.s), float(x.MFE), float(x.R_news), float(x.MFE_news))
               for s, x in g.set_index("strat").iterrows()}
        jours.append((d, row))
    return jours


def simule(jours, i0: int, n: int, calendaire: bool = False, annonces: bool = False, politique: str = "actuel"):
    A, B = Compte("A mom", calendaire, annonces, politique), Compte("B 3n + M2", calendaire, annonces, politique)
    ca, cb = [], []
    for d, row in jours[i0:i0 + n]:
        A.jour(d, jambes_A(row))
        B.jour(d, jambes_B(row))
        ca.append(A.cash)
        cb.append(B.cash)
    return A, B, np.array(ca), np.array(cb)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lib = bibliotheque()
    jours = tableau(lib)
    dates = pd.DatetimeIndex([d for d, _ in jours])
    say(f"Calendrier : {len(jours)} séances du {dates[0]:%Y-%m-%d} au {dates[-1]:%Y-%m-%d} ; "
        f"compte B : 3n {int((lib.strat == '3n').sum())} nuits, M2 {int((lib.strat == 'M2').sum())} setups")

    CONFIGS = {"sans règle des annonces, politique actuelle": (False, "actuel"),
               "règle des annonces, politique actuelle": (True, "actuel"),
               "règle des annonces, cible + attente": (True, "cible+attente")}
    for nom_c, (ann, pol) in CONFIGS.items():
      suffixe = {False: "", True: "_annonces"}[ann] + ("_cible_attente" if pol != "actuel" else "")
      say(f"\n#################### {nom_c} ####################")
      # 1. tous les départs, 12 mois
      H = 252
      rows = []
      hist_end = np.searchsorted(dates, pd.Timestamp("2026-08-29"))
      for i0 in range(0, hist_end - H, 5):
          A, B, ca, cb = simule(jours, i0, H, False, ann, pol)
          tot = ca + cb
          rows.append(dict(départ=dates[i0].date(), année=dates[i0].year,
                           net_A=A.cash, net_B=B.cash, net_total=A.cash + B.cash,
                           évals_A=A.evals, évals_B=B.evals, rewards_A=A.rewards, rewards_B=B.rewards,
                           creux_total=min(0.0, tot.min()), creux_A=min(0.0, ca.min()), creux_B=min(0.0, cb.min())))
      D = pd.DataFrame(rows)
      D.to_csv(OUT / f"departs{suffixe}.csv", index=False)
      q = lambda s: f"médiane {s.median():+,.0f} $, 10e c. {s.quantile(0.1):+,.0f} $, 90e c. {s.quantile(0.9):+,.0f} $, " \
                    f"P(< 0) {100 * (s < 0).mean():.0f} %"
      say(f"\n12 mois à partir de chaque départ ({len(D)} départs, 2011-07 → 2025-08), deux comptes 10k :")
      for k in ("A", "B", "total"):
          say(f"  net {k:<5} : moyenne {D[f'net_{k}'].mean():+,.0f} $ ; {q(D[f'net_{k}'])}")
      say(f"  évals achetées par an : A {D.évals_A.mean():.1f}, B {D.évals_B.mean():.1f} ; rewards : A {D.rewards_A.mean():.1f}, "
          f"B {D.rewards_B.mean():.1f}")
      say(f"  pire creux de trésorerie sur 12 mois (frais payés avant les rewards) : total médiane {D.creux_total.median():,.0f} $, "
          f"pire {D.creux_total.min():,.0f} $ ; A pire {D.creux_A.min():,.0f} $, B pire {D.creux_B.min():,.0f} $")
      say(f"  corrélation des nets A / B entre départs : {D.net_A.corr(D.net_B):+.2f}")
      par = D.groupby("année")[["net_A", "net_B", "net_total"]].mean().round(0)
      say(f"\nNet moyen sur 12 mois selon l'année de départ ($) :\n{par.to_string()}")

      # 2. départ réel le 1er septembre 2026
      i0 = int(np.searchsorted(dates, pd.Timestamp("2026-09-01")))
      A, B, ca, cb = simule(jours, i0, len(jours) - i0, True, ann, pol)
      say(f"\nDépart réel le 01/09/2026 (jusqu'au 03/11, reward au 14e jour calendaire) :")
      for C_ in (A, B):
          say(f"  {C_.nom} : évals {C_.evals}, rewards {C_.rewards}, net {C_.cash:+,.0f} $ ; phase au 03/11 {C_.phase}, "
              f"solde {C_.P:+.2f} %")
          for d, e in C_.events:
              say(f"    {d:%d/%m} {e}")
      say(f"  total des deux comptes : {A.cash + B.cash:+,.0f} $")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
