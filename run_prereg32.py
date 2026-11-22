"""Pré-enregistrement n° 32 : forward de BB sur NQ. À LANCER SEULEMENT AUX DATES DE LECTURE (2028-02-29, 2029-08-31,
2031-08-29), après avoir mis à jour les données Databento et supprimé cache/NQ_adj.parquet (voir PREREGISTRATION_32.md).

uv run python run_prereg32.py --lecture 2028-02-29
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from fab.core import ASSETS
from fab.protocole import nw_t
from fab.replications import sgrid
from run_bb_sltp import prepare, simulate
from run_m2_vwap import m2

DEBUT = pd.Timestamp("2026-11-04")
LECTURES = {"2028-02-29": "L1", "2029-08-31": "L2", "2031-08-29": "L3"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lecture", required=True, choices=list(LECTURES))
    lec = pd.Timestamp(ap.parse_args().lecture)
    if pd.Timestamp(date.today()) < lec:
        raise SystemExit(f"Interdit avant le {lec.date()} (PREREGISTRATION_32).")
    out = Path("results/prereg32")
    out.mkdir(parents=True, exist_ok=True)
    a = ASSETS["NQ"]
    g = sgrid(a)
    dates = g.dates[(g.dates >= DEBUT) & (g.dates <= lec)]
    # H1 : BB de référence, P&L journalier en points (0 sans trade)
    t1 = m2(a, g, True)
    t1 = t1[(pd.to_datetime(t1.date) >= DEBUT) & (pd.to_datetime(t1.date) <= lec)]
    pts = (t1.p_out - t1.p_in) * t1.dir / t1.f_in - a.rt_cost
    d1 = pd.Series(pts.values, index=pd.to_datetime(t1.date)).groupby(level=0).sum().reindex(dates).fillna(0.0)
    # H2 : version prop firm, premier trade de la séance, R net
    P = prepare()
    t2 = simulate(P, "A", 0.25, 2).sort_values(["date", "m_in"]).groupby("date", as_index=False).first()
    t2 = t2[(pd.to_datetime(t2.date) >= DEBUT) & (pd.to_datetime(t2.date) <= lec)]
    r2 = t2.net_pts / (0.25 * P[8].reindex(pd.to_datetime(t2.date)).values)
    res = []
    for h, x in [("H1 BB référence (pts/jour)", d1.values), ("H2 BB prop firm (R/trade)", r2.values)]:
        z = nw_t(x)
        res.append({"hypothese": h, "n": len(x), "moyenne": float(np.mean(x)), "z": z, "p": float(stats.norm.sf(z))})
    tab = pd.DataFrame(res)
    tab.to_csv(out / f"lecture_{LECTURES[str(lec.date())]}.csv", index=False)
    print(f"Lecture {LECTURES[str(lec.date())]} ({DEBUT.date()} → {lec.date()}) :\n{tab.to_string(index=False)}")
    print("Règle : L1 et L2 succès seulement si z ≥ 3,0 ; L3 : Holm sur les hypothèses non décidées, p ≤ 0,05.")


if __name__ == "__main__":
    main()
