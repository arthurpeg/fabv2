"""Montée en taille FTMO 1-Step avec les deux stratégies (A = mom, B = 3n + M2), règle des annonces + cible + attente
(demande du 2026-11-04). EXPLORATOIRE, hors compteur.

uv run python run_ftmo_scaling.py [N] → results/ftmo_scaling/ (run.log, historique_evenements.csv, glissants.csv,
mc_<scénario>.csv)

Paliers, pour chaque stratégie (un compte A et un compte B par « paire ») :
  1 : 1 x 10k   2 : 2 x 10k   3 : 3 x 10k
  4 : 1 x 100k (les comptes 10k continuent mais ne sont plus rachetés quand ils sautent)
  5 : 2 x 100k (les comptes 10k restants sont abandonnés : 4 x 100k = 400k, plafond FTMO hors plan de scaling)
Cagnotte = dépôt de départ + rewards - frais d'éval. On passe au palier suivant dès que la cagnotte couvre la réserve du
palier suivant. Réserve = 10 évals par paire de comptes A + B de même taille (niveau à 99 % de la paire dans le
Monte-Carlo, reports/ftmo_monte_carlo_report.md et run_ftmo_reserve_par_compte.py) : les comptes d'une même stratégie
tradent les mêmes trades et sautent ensemble, la réserve s'additionne donc d'une paire à l'autre. Une première version
(10 évals par compte, réserve double) est dans results/ftmo_scaling/run_reserve_20evals.log. Prix : 10k 79 € (86,90 $), 100k 499 € (548,90 $). Réserves : palier 1 869 $,
2 1 738 $, 3 2 607 $, 4 5 489 $, 5 10 978 $. Dépôt de départ = réserve du palier 1 (869 $).
Un compte perdu est racheté le jour suivant si la cagnotte paie l'éval (sinon l'emplacement attend). Rien n'est retiré ;
« excédent » = cagnotte - réserve du palier atteint (ce qu'on pourrait retirer).
Règles et trades : run_ftmo_deux_comptes.py (Compte, jambes_A, jambes_B), reward au 14e jour calendaire dans le rejeu
historique, après 10 séances dans les tirages ; un nouveau compte trade dès le jour suivant son achat.
Simulations : (1) le vrai chemin 2011-07-01 → 2026-11-03 ; (2) un départ toutes les 20 séances de 2011-07 à 2021-08,
5 ans chacun ; (3) Monte-Carlo par blocs (run_ftmo_monte_carlo), 5 ans, scénarios « historique » et « edge / 2 ».
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as M
import run_ftmo_monte_carlo as MC
from propfirm.ftmo import EUR, PRICES_EUR

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000
OUT = Path("results/ftmo_scaling")
PRIX = {10_000: PRICES_EUR[10_000] * EUR, 100_000: PRICES_EUR[100_000] * EUR}
PALIERS = [{10_000: 1, 100_000: 0}, {10_000: 2, 100_000: 0}, {10_000: 3, 100_000: 0},
           {10_000: 0, 100_000: 1}, {10_000: 0, 100_000: 2}]
EVALS_RESERVE = 10
H5 = 1260
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def reserve(k: int) -> float:
    return sum(n * EVALS_RESERVE * PRIX[t] for t, n in PALIERS[k].items())  # 10 évals par paire (A + B) de comptes


DEPOT = reserve(0)


class Gestion:
    def __init__(self, calendaire: bool):
        self.cal, self.palier, self.slots, self.morts = calendaire, 0, [], []
        self.cagnotte, self.dates, self.idle, self.events = DEPOT, {}, 0, []
        for strat in ("A", "B"):
            self._ajoute(strat, 10_000, None)

    def _ajoute(self, strat, taille, d):
        c = M.Compte(f"{strat} {taille // 1000}k", self.cal, True, "cible+attente", taille, PRIX[taille], False)
        self.cagnotte -= PRIX[taille]
        self.slots.append(dict(strat=strat, taille=taille, compte=c, rachat=True))

    def jour(self, t: int, d, row):
        for s in self.slots:
            c = s["compte"]
            if c is None or c.mort:
                continue
            avant = c.cash
            c.jour(d, M.jambes_A(row) if s["strat"] == "A" else M.jambes_B(row))
            self.cagnotte += c.cash - avant
        for s in self.slots:  # rachats
            c = s["compte"]
            if c is not None and c.mort:
                self.events.append((d, f"{c.nom} perdu"))
                s["compte"] = None
            if s["compte"] is None and s["rachat"]:
                if self.cagnotte >= PRIX[s["taille"]]:
                    self.cagnotte -= PRIX[s["taille"]]
                    s["compte"] = M.Compte(f"{s['strat']} {s['taille'] // 1000}k", self.cal, True, "cible+attente",
                                           s["taille"], PRIX[s["taille"]], False)
                else:
                    self.idle += 1
        self.slots = [s for s in self.slots if s["compte"] is not None or s["rachat"]]
        if self.palier < len(PALIERS) - 1 and self.cagnotte >= reserve(self.palier + 1):
            self._monte(t, d)

    def _monte(self, t, d):
        k = self.palier + 1
        cible, actuel = PALIERS[k], PALIERS[self.palier]
        if k == 3:  # 1 x 100k : les 10k ne sont plus rachetés
            for s in self.slots:
                s["rachat"] = False
        if k == 4:  # 2 x 100k : les 10k restants sont abandonnés
            self.slots = [s for s in self.slots if s["taille"] == 100_000]
        for strat in ("A", "B"):
            for taille, n in cible.items():
                deja = actuel[taille] if k not in (3, 4) or taille == 100_000 else 0
                for _ in range(n - deja):
                    self._ajoute(strat, taille, d)
        self.palier = k
        self.dates[k + 1] = t
        self.events.append((d, f"palier {k + 1} : {cible[10_000]} x 10k + {cible[100_000]} x 100k par stratégie, "
                               f"cagnotte {self.cagnotte:,.0f} $"))

    def excedent(self):
        return self.cagnotte - reserve(self.palier)


def joue(jours, idx, calendaire=False):
    g = Gestion(calendaire)
    traj = np.empty(len(idx))
    for t, i in enumerate(idx):
        d, row = jours[i]
        g.jour(t, d, row)
        traj[t] = g.cagnotte
    return g, traj


def resume(nom: str, rows: list[dict], horizon: int):
    D = pd.DataFrame(rows)
    D.to_csv(OUT / f"{nom}.csv", index=False)
    say(f"\n===== {nom} : {len(D)} chemins de {horizon} séances (≈ {horizon / 252:.0f} ans) =====")
    for k in range(2, 6):
        s = D[f"palier_{k}"]
        ok = s.notna()
        say(f"  palier {k} atteint dans {100 * ok.mean():.0f} % des chemins ; délai médian "
            f"{(s[ok].median() / 21 if ok.any() else np.nan):.1f} mois (10e c. {s[ok].quantile(.1) / 21 if ok.any() else np.nan:.1f}, "
            f"90e c. {s[ok].quantile(.9) / 21 if ok.any() else np.nan:.1f})")
    for col, lab in (("cagnotte_1an", "cagnotte à 1 an"), ("cagnotte_fin", "cagnotte à la fin"),
                     ("excedent_fin", "excédent retirable à la fin")):
        s = D[col]
        say(f"  {lab:<28}: médiane {s.median():+,.0f} $ ; 10e c. {s.quantile(.1):+,.0f} $ ; 90e c. {s.quantile(.9):+,.0f} $ ; "
            f"5e c. {s.quantile(.05):+,.0f} $")
    say(f"  plus bas de la cagnotte : médiane {D.min_cagnotte.median():,.0f} $ ; 5e c. {D.min_cagnotte.quantile(.05):,.0f} $ ; "
        f"pire {D.min_cagnotte.min():,.0f} $ ; jours-emplacement sans argent pour racheter : médiane {D.idle.median():.0f}, "
        f"P(> 0) {100 * (D.idle > 0).mean():.0f} %")


def ligne(g, traj):
    r = {f"palier_{k}": g.dates.get(k) for k in range(2, 6)}
    r |= dict(cagnotte_1an=traj[min(251, len(traj) - 1)], cagnotte_fin=traj[-1], excedent_fin=g.excedent(),
              min_cagnotte=traj.min(), idle=g.idle, palier_fin=g.palier + 1)
    return r


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lib = M.bibliotheque()
    jours = M.tableau(lib)
    dates = pd.DatetimeIndex([d for d, _ in jours])
    say(f"Scaling FTMO, A = mom et B = 3n + M2, règle des annonces + cible + attente ; dépôt {DEPOT:,.0f} $ ; réserves par "
        f"palier : " + ", ".join(f"{k + 1} : {reserve(k):,.0f} $" for k in range(5)))

    # 1. vrai chemin
    g, traj = joue(jours, np.arange(len(jours)), calendaire=True)
    ev = pd.DataFrame(g.events, columns=["date", "événement"])
    ev.to_csv(OUT / "historique_evenements.csv", index=False)
    say(f"\n===== Vrai chemin {dates[0]:%Y-%m-%d} → {dates[-1]:%Y-%m-%d} =====")
    for d, e in g.events:
        if e.startswith("palier"):
            say(f"  {d:%Y-%m-%d} {e}")
    cag = pd.Series(traj, index=dates)
    an = cag.resample("YE").last()
    say(f"  cagnotte fin d'année ($) : " + ", ".join(f"{y.year} {v:,.0f}" for y, v in an.items()))
    say(f"  à la fin : palier {g.palier + 1}, cagnotte {g.cagnotte:,.0f} $, excédent retirable {g.excedent():,.0f} $ ; "
        f"plus bas {traj.min():,.0f} $ ; jours-emplacement sans argent {g.idle}")

    # 2. départs glissants, 5 ans
    rows = []
    fin = int(np.searchsorted(dates, pd.Timestamp("2026-08-29")))
    for i0 in range(0, fin - H5, 20):
        g, traj = joue(jours, np.arange(i0, i0 + H5))
        rows.append(dict(départ=dates[i0].date(), **ligne(g, traj)))
    resume("glissants", rows, H5)

    # 3. Monte-Carlo
    for nom, src in (("mc_historique", jours), ("mc_edge_2", M.tableau(MC.decale(lib, 0.5)))):
        rng = np.random.default_rng(MC.SEED)
        rows = []
        for _ in range(N):
            MC.H = H5
            g, traj = joue(src, MC.indices(len(src), rng))
            rows.append(ligne(g, traj))
        resume(nom, rows, H5)
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
