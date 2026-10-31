"""Trades de la règle NQ de nuit avec un autre objectif (TP en ATR), même chaîne que run_couts_reels_nq_nuit.py.

uv run python build_nq_nuit_tp.py [TP_ATR]  → cache/propfirm/nq_nuit_tp<TP>.parquet (night, entry_idx, dir, reason, R_brut, risk)

Compte 20:00 ET, momentum 12-1, SL 2 ATR, TP `TP_ATR` ATR (défaut 4 = 2 R), sortie 9:30 ET, 2011-07 → 2026-08.
Contrôle : avec TP 5, les R doivent être identiques à results/couts_reels_nq_nuit/trades.csv.
Attention : importer run_prereg12 réécrit results/prereg12/run.log (vide de toute façon).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_prereg12 as Q  # historique 2010-2015 actif
import run_prereg10 as P
import run_recolte1_atr as A
from recolte1.engine import NY
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
A0, Z0 = "2011-07-01", "2026-08-28"


def build(tp: float) -> pd.DataFrame:
    e = Q.table(at(Q.D, "20:00", NY, -1), Q.B["t_open"], Q.MOM, "R0")
    A.VARIANTS = [(f"SL 2 ATR / TP {tp:g} ATR", 2.0, tp)]
    T = A.simulate("NQ", e)
    g = T[T["cost"] == "gross"].copy()
    g["R_brut"] = P.r_multiples("NQ", e, g).values
    g["risk"] = g["ret"] / g["R_brut"]
    g["night"] = pd.to_datetime(g["night"])
    g = g[(g["night"] >= A0) & (g["night"] <= Z0)].reset_index(drop=True)
    return g[["night", "entry_idx", "exit_idx", "dir", "reason", "R_brut", "risk"]]


if __name__ == "__main__":
    tp = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    out = Path(f"cache/propfirm/nq_nuit_tp{tp:g}.parquet")
    out.parent.mkdir(parents=True, exist_ok=True)
    g = build(tp)
    g.to_parquet(out)
    print(f"TP {tp:g} ATR : {len(g)} trades, R brut moyen {g.R_brut.mean():+.4f}, "
          f"sorties {g.reason.value_counts().to_dict()} → {out}")
    if tp == 5.0:
        ref = pd.read_csv("results/couts_reels_nq_nuit/trades.csv")
        m = g.merge(ref[["entry_idx", "R_brut"]], on="entry_idx", suffixes=("", "_ref"))
        print(f"contrôle TP 5 : {len(m)}/{len(ref)} trades appariés, écart max de R {np.nanmax(np.abs(m.R_brut - m.R_brut_ref)):.2e}")
