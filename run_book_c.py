"""Book C hypothétique SANS edge chez FundingPips (1 Step Flex 10k), en plus des comptes FTMO A (mom) et B (3n + M2)
— demande du 2026-11-05. EXPLORATOIRE, hors compteur.

uv run python run_book_c.py [N] → results/book_c/ (run.log, glissants.csv, mc.csv)

Book C : un trade chaque nuit aux heures de mom (entrée 20:00 ET, SL 2 ATR M15, objectif 2 R, sortie 9:30), mais sens
tiré à pile ou face (aucun edge). Issues des deux sens de chaque nuit : propfirm.nights (variante 0 : FundingPips n'a pas
de règle des annonces dans nos relevés). Coût CFD 1,5 point au niveau actuel du NQ, comme A et B.
Règles FundingPips 1 Step Flex (relevées le 2026-10-31, reports/propfirm_multi.md ; le site refuse les requêtes le
2026-11-05, rien de nouveau vérifié) : objectif +12 %, perte max 12 % fixe sous le capital, perte du jour 3 % (option),
levier 1:20 en éval et 1:5 en financé (option Swing, obligatoire pour garder la nuit), pas de consistance, retrait toutes
les 2 semaines (min 1 % de profit, 80 % versés), le solde revient au capital après un retrait.
Prix SUPPOSÉ du 10k : 100k à 733 $ (option Swing comprise) x 87 / 549 (rapport 10k / 100k de FTMO) ≈ 116 $.
Gestion, calquée sur le plan FTMO : éval 2,5 % de risque, objectif 2 R ramené au reste à faire ; financé 1 % à 2 R ;
compte racheté après chaque échec.
Simulations, les trois books en même temps (A et B : Compte de run_ftmo_deux_comptes avec annonces, cible + attente et
anti-hedging ; le hedging ne compte qu'à l'intérieur d'une même prop firm) :
  (1) vrai chemin 2011-07-01 → 2026-08-28, C rejoué avec N tirages des sens ;
  (2) départs glissants tous les 5 jours, 12 mois ;
  (3) Monte-Carlo par blocs (run_ftmo_monte_carlo.indices), 3 ans, N chemins (sens de C retirés à chaque chemin).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as M
import run_ftmo_monte_carlo as MC
from propfirm.nights import K_N, K_STEP, NEVER, build

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000
OUT = Path("results/book_c")
FEE_C, SIZE_C = 733.0 * 86.9 / 548.9, 10_000
TARGET_C, DD_C, DAILY_C, SPLIT_C, PAY_MIN = 12.0, 12.0, 3.0, 0.8, 1.0
R_EVAL, R_FUND, TP = 2.5, 1.0, 2.0
COST = 1.5 / 25_684.0
LOG: list[str] = []
L = build()
POS = {d: i for i, d in enumerate(L.dates.normalize())}


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def issue(i: int, side: int, k: float) -> float:
    """R brut d'un trade de la nuit i, sens side (0 long, 1 short), objectif k R."""
    kidx = min(max(int(np.ceil(k / K_STEP - 1e-9)) - 1, 0), K_N - 1)
    tpb, sb = L.tp_bar[0, i, side, kidx], L.stop_bar[0, i, side]
    if tpb < sb:
        return K_STEP * (kidx + 1)
    return -float(L.stop_R[0, i, side]) if sb != NEVER else float(L.eod_R[0, i, side])


class CompteFP:
    def __init__(self):
        self.cash, self.evals, self.payouts, self.valides = -FEE_C, 1, 0, 0
        self._nouveau("éval", None)

    def _nouveau(self, phase, d):
        self.phase, self.P, self.debut = phase, 0.0, d

    def jour(self, d, side):
        i = POS.get(d)
        if self.phase == "financé" and self.debut is not None and (d - self.debut).days >= 14 and self.P >= PAY_MIN:
            self.cash += SPLIT_C * self.P / 100 * SIZE_C
            self.payouts += 1
            self._nouveau("financé", d)
        if i is None:
            return
        c = COST / L.s[i]
        r = R_EVAL if self.phase == "éval" else R_FUND
        risk = min(r, self.P + DD_C)
        k = TP
        if self.phase == "éval":
            need = TARGET_C - self.P
            k = min(TP, need * (1 + c) / risk + c)
        R = issue(i, side, k)
        pnl = risk * (R - c) / (1 + c)
        self.P += pnl
        if self.phase == "financé" and self.debut is None:
            self.debut = d
        if self.P <= -DD_C + 1e-9 or pnl <= -DAILY_C:
            self.evals += 1
            self.cash -= FEE_C
            self._nouveau("éval", None)
        elif self.phase == "éval" and self.P >= TARGET_C - 1e-9:
            self.valides += 1
            self._nouveau("financé", None)


def joue(jours, idx, rng, calendaire):
    """Les trois books sur la suite de séances idx ; renvoie les trajectoires de trésorerie et les comptes."""
    A = M.Compte("A", calendaire, True, "cible+attente")
    B = M.Compte("B", calendaire, True, "cible+attente")
    C = CompteFP()
    tr = np.empty((len(idx), 3))
    for t, j in enumerate(idx):
        d, row = jours[j]
        A.jour(d, M.jambes_A(row))
        B.jour(d, M.jambes_B(row))
        C.jour(d, int(rng.integers(2)))
        tr[t] = A.cash, B.cash, C.cash
    return tr, (A, B, C)


def dd(x):
    x = np.r_[0.0, x]
    return float((x - np.maximum.accumulate(x)).min())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    say(f"Book C : FundingPips 1 Step Flex 10k, prix supposé {FEE_C:,.0f} $, sens au hasard, éval 2,5 % / financé 1 %, "
        f"objectif 2 R")
    lib = M.bibliotheque()
    jours = [j for j in M.tableau(lib) if j[0] <= pd.Timestamp("2026-08-28")]
    dates = pd.DatetimeIndex([d for d, _ in jours])

    # (1) vrai chemin, N tirages des sens de C
    rows, flux = [], None
    for s in range(min(N, 200)):
        tr, (A, B, C) = joue(jours, np.arange(len(jours)), np.random.default_rng(s), True)
        mois = pd.DataFrame(tr, index=dates, columns=list("ABC")).resample("ME").last().diff().dropna()
        tot = mois.sum(axis=1)
        rows.append(dict(A=tr[-1, 0], B=tr[-1, 1], C=tr[-1, 2], total=tr[-1].sum(), evals_C=C.evals,
                         valides_C=C.valides, payouts_C=C.payouts, dd_C=dd(tr[:, 2]), dd_AB=dd(tr[:, :2].sum(1)),
                         dd_ABC=dd(tr.sum(1)), neg_AB=100 * (mois[["A", "B"]].sum(1) < 0).mean(),
                         neg_ABC=100 * (tot < 0).mean(), corr_AC=mois.A.corr(mois.C), corr_BC=mois.B.corr(mois.C)))
    D = pd.DataFrame(rows)
    D.to_csv(OUT / "vrai_chemin.csv", index=False)
    an = len(jours) / 252
    q = lambda c: f"médiane {D[c].median():+,.0f} $ (10e c. {D[c].quantile(.1):+,.0f}, 90e c. {D[c].quantile(.9):+,.0f}, P<0 {100 * (D[c] < 0).mean():.1f} %)"
    say(f"\n===== Vrai chemin {dates[0]:%Y-%m-%d} → {dates[-1]:%Y-%m-%d} ({an:.1f} ans), {len(D)} tirages des sens de C =====")
    say(f"  A mom : {D.A.iloc[0]:+,.0f} $ ; B 3n + M2 : {D.B.iloc[0]:+,.0f} $ ; A + B : {D.A.iloc[0] + D.B.iloc[0]:+,.0f} $")
    say(f"  C (sans edge) : {q('C')} ; par an {D.C.median() / an:+,.0f} $")
    say(f"  C : évals achetées {D.evals_C.median():.0f} (frais {D.evals_C.median() * FEE_C:,.0f} $), validées "
        f"{D.valides_C.median():.0f}, retraits {D.payouts_C.median():.0f}")
    say(f"  A + B + C : {q('total')}")
    say(f"  max DD de trésorerie : C {D.dd_C.median():,.0f} $ (pire {D.dd_C.min():,.0f}) ; A + B {D.dd_AB.iloc[0]:,.0f} $ ; "
        f"A + B + C {D.dd_ABC.median():,.0f} $ (pire {D.dd_ABC.min():,.0f})")
    say(f"  mois négatifs : A + B {D.neg_AB.iloc[0]:.0f} % ; A + B + C {D.neg_ABC.median():.0f} % ; corrélation des flux "
        f"mensuels C / A {D.corr_AC.median():+.2f}, C / B {D.corr_BC.median():+.2f}")

    # (2) départs glissants, 12 mois
    rng = np.random.default_rng(7)
    g = []
    for i0 in range(0, len(jours) - 252, 5):
        tr, (A, B, C) = joue(jours, np.arange(i0, i0 + 252), rng, False)
        g.append(dict(départ=dates[i0].date(), A=tr[-1, 0], B=tr[-1, 1], C=tr[-1, 2], AB=tr[-1, :2].sum(),
                      ABC=tr[-1].sum(), dd_AB=dd(tr[:, :2].sum(1)), dd_ABC=dd(tr.sum(1)), dd_C=dd(tr[:, 2])))
    G = pd.DataFrame(g)
    G.to_csv(OUT / "glissants.csv", index=False)
    say(f"\n===== {len(G)} départs glissants, 12 mois =====")
    for c in ("A", "B", "C", "AB", "ABC"):
        s = G[c]
        say(f"  {c:<4}: moyenne {s.mean():+,.0f} $ ; médiane {s.median():+,.0f} $ ; 10e c. {s.quantile(.1):+,.0f} $ ; "
            f"pire {s.min():+,.0f} $ ; P(< 0) {100 * (s < 0).mean():.1f} %")
    say(f"  max DD de trésorerie (médiane / pire) : C {G.dd_C.median():,.0f} / {G.dd_C.min():,.0f} $ ; A + B "
        f"{G.dd_AB.median():,.0f} / {G.dd_AB.min():,.0f} $ ; A + B + C {G.dd_ABC.median():,.0f} / {G.dd_ABC.min():,.0f} $")

    # (3) Monte-Carlo par blocs, 3 ans
    rng = np.random.default_rng(MC.SEED)
    MC.H = 756
    m = []
    for _ in range(N):
        tr, _c = joue(jours, MC.indices(len(jours), rng), rng, False)
        m.append(dict(A=tr[-1, 0], B=tr[-1, 1], C=tr[-1, 2], AB=tr[-1, :2].sum(), ABC=tr[-1].sum(),
                      C_1an=tr[251, 2], ABC_1an=tr[251].sum(), AB_1an=tr[251, :2].sum(),
                      dd_AB=dd(tr[:, :2].sum(1)), dd_ABC=dd(tr.sum(1)), dd_C=dd(tr[:, 2])))
    Q = pd.DataFrame(m)
    Q.to_csv(OUT / "mc.csv", index=False)
    say(f"\n===== Monte-Carlo, {N} chemins de 3 ans =====")
    for c in ("C_1an", "AB_1an", "ABC_1an", "C", "AB", "ABC"):
        s = Q[c]
        say(f"  {c:<7}: moyenne {s.mean():+,.0f} $ ; médiane {s.median():+,.0f} $ ; 5e c. {s.quantile(.05):+,.0f} $ ; "
            f"1er c. {s.quantile(.01):+,.0f} $ ; P(< 0) {100 * (s < 0).mean():.1f} %")
    say(f"  max DD de trésorerie (médiane / 99e c.) : C {Q.dd_C.median():,.0f} / {Q.dd_C.quantile(.01):,.0f} $ ; A + B "
        f"{Q.dd_AB.median():,.0f} / {Q.dd_AB.quantile(.01):,.0f} $ ; A + B + C {Q.dd_ABC.median():,.0f} / "
        f"{Q.dd_ABC.quantile(.01):,.0f} $ ; corrélation des nets à 3 ans C / A + B {Q.C.corr(Q.AB):+.2f}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
