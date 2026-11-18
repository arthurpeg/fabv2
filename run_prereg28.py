"""Pré-enregistrement n° 28 : short du yen pendant la session US (short 6J de 11:00 à 16:55 ET).

uv run python run_prereg28.py --hist             → référence historique 2016-01 → 2026-08-28 (déjà vue)
uv run python run_prereg28.py --lecture AAAA-MM-JJ → lecture du n° 28 : trades du 2026-08-29 à la date donnée

Moteur figé : fab/replications.py (run_legs / window, celui de R5b), coût 1 tick + 5 $ aller-retour
(≈ 1,8 tick sur 6J), entrée à l'ouverture de la barre de 11:00 ET, sortie à 16:55 ET.
6J = dollars par yen : short 6J = le yen baisse = long USDJPY.

Tests (voir PREREGISTRATION_28.md) : H1 rendement brut moyen > 0, H2 rendement net moyen > 0,
t de Newey-West (5 retards), unilatéral, Holm sur 2. Aux lectures intermédiaires : succès si z ≥ 3,0.
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from scipy.stats import norm

from fab.replications import ASSETS, NY, et_dates, run_legs, window

sys.stdout.reconfigure(encoding="utf-8")
HOLDOUT_START = pd.Timestamp("2026-08-29")


def nw(x: pd.Series, lags: int = 5) -> float:
    """t de la moyenne, variance de Newey-West (noyau de Bartlett)."""
    e = x.values - x.values.mean()
    T = len(e)
    v = e @ e / T
    for k in range(1, lags + 1):
        v += 2 * (1 - k / (lags + 1)) * (e[k:] @ e[:-k]) / T
    return float(x.mean() / np.sqrt(v / T))


def daily() -> tuple[pd.Series, pd.Series]:
    r = run_legs("P28", ASSETS["6J"], [(window("6J", NY, "11:00", "16:55", -1), NY)], NY, et_dates("6J"))
    traded = r.daily_gross != 0
    return r.daily_gross[traded] * 1e4, r.daily_net[traded] * 1e4  # bp


def describe(g: pd.Series, n: pd.Series, label: str) -> None:
    print(f"\n== {label} : {len(n)} trades, {n.index.min().date()} → {n.index.max().date()}")
    for name, x in [("brut", g), ("net", n)]:
        print(f"  {name} : {x.mean():+.2f} bp/trade, écart type {x.std():.1f} bp, "
              f"Sharpe annuel {x.mean() / x.std() * np.sqrt(252):+.2f}, t NW {nw(x):+.2f}")


def main() -> None:
    g, n = daily()
    if "--hist" in sys.argv:
        g, n = g[g.index < HOLDOUT_START], n[n.index < HOLDOUT_START]
        describe(g, n, "Référence historique (déjà vue)")
        for a, b in [("2016", "2021"), ("2021", "2026-08-29")]:
            describe(g[(g.index >= a) & (g.index < b)], n[(n.index >= a) & (n.index < b)], f"{a} → {b}")
        return
    i = sys.argv.index("--lecture")
    end = pd.Timestamp(sys.argv[i + 1])
    final = end >= pd.Timestamp("2031-08-29")
    m = (g.index >= HOLDOUT_START) & (g.index <= end)
    g, n = g[m], n[m]
    describe(g, n, f"Lecture au {end.date()} ({'finale' if final else 'intermédiaire'})")
    z = {"H1 brut > 0": nw(g), "H2 net > 0": nw(n)}
    p = {k: norm.sf(v) for k, v in z.items()}
    order = sorted(p, key=p.get)
    holm = {k: min(1.0, max(p[j] * (2 - order.index(j)) for j in order[: order.index(k) + 1])) for k in p}
    for k in z:
        verdict = (holm[k] <= 0.05) if final else (z[k] >= 3.0)
        print(f"  {k} : z {z[k]:+.2f}, p {p[k]:.4f}, p Holm {holm[k]:.4f} → "
              f"{'SUCCÈS' if verdict else ('échec' if final else 'on continue')}")


if __name__ == "__main__":
    main()
