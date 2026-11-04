"""Réserve de trésorerie d'un compte FTMO 10k seul contre la paire (A = mom, B = 3n + M2), mêmes chemins Monte-Carlo
que run_ftmo_monte_carlo.py (bootstrap stationnaire, blocs de 20 séances, 3 ans, même graine). EXPLORATOIRE, hors compteur.

uv run python run_ftmo_reserve_par_compte.py [N] → results/ftmo_monte_carlo/reserve_par_compte.csv
Réserve = plus grande baisse du cumul (rewards - frais) depuis 0 ou depuis un plus haut, frais de la 1re éval compris.
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as M
import run_ftmo_monte_carlo as MC

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000


def dd(x: np.ndarray) -> float:
    x = np.r_[0.0, x]
    return float((x - np.maximum.accumulate(x)).min())


def main() -> None:
    lib = M.bibliotheque()
    rows = []
    for nom, jours in (("historique", M.tableau(lib)), ("récent", M.tableau(lib[lib.date >= "2019-01-01"])),
                       ("edge / 2", M.tableau(MC.decale(lib, 0.5)))):
        rng = np.random.default_rng(MC.SEED)
        for _ in range(N):
            idx = MC.indices(len(jours), rng)
            A = M.Compte("A", False, True, "cible+attente")
            B = M.Compte("B", False, True, "cible+attente")
            ca, cb = np.empty(MC.H), np.empty(MC.H)
            for t, i in enumerate(idx):
                d, row = jours[i]
                A.jour(d, M.jambes_A(row))
                B.jour(d, M.jambes_B(row))
                ca[t], cb[t] = A.cash, B.cash
            rows.append(dict(scénario=nom, dd_A=dd(ca), dd_B=dd(cb), dd_paire=dd(ca + cb)))
    D = pd.DataFrame(rows)
    D.to_csv("results/ftmo_monte_carlo/reserve_par_compte.csv", index=False)
    fee = M.FEE
    for nom, g in D.groupby("scénario", sort=False):
        print(f"\n{nom} ({len(g)} chemins de 3 ans) : réserve en $ (en nombre d'évals de {fee:.0f} $)")
        for c, lab in (("dd_A", "A seul (mom)"), ("dd_B", "B seul (3n + M2)"), ("dd_paire", "les deux")):
            s = -g[c]
            print(f"  {lab:<17}: médiane {s.median():,.0f} $ ({s.median() / fee:.0f}) ; 95e c. {s.quantile(.95):,.0f} $ "
                  f"({s.quantile(.95) / fee:.0f}) ; 99e c. {s.quantile(.99):,.0f} $ ({s.quantile(.99) / fee:.0f}) ; "
                  f"pire {s.max():,.0f} $ ({s.max() / fee:.0f})")


if __name__ == "__main__":
    main()
