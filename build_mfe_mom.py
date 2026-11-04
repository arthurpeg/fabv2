"""Ajoute à la bibliothèque mom TP 4 ATR (cache/propfirm/nq_nuit_tp4.parquet) le mouvement favorable maximal de chaque
trade avant sa sortie, en R (MFE_R), pour ramener l'objectif d'éval FTMO au reste à faire.

uv run python build_mfe_mom.py → cache/propfirm/nq_nuit_tp4_mfe.parquet

Mêmes barres 1 min que build_nq_nuit_tp.py (recolte1.engine.load("NQ") avec l'historique 2010-2015 raccordé,
USE_2010 = True comme run_prereg12) : entrée au close de la barre entry_idx ; MFE sur les barres entry_idx + 1 →
exit_idx, sauf la barre de sortie d'un stop (on ne sait pas si le haut est venu avant le bas dans la minute).
Contrôle : un trade sorti au TP doit avoir MFE_R >= 2.
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

import recolte1.engine as eng

sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    eng.USE_2010 = True
    eng.load.cache_clear()
    df = eng.load("NQ")
    hi, lo, cl = df.high.values, df.low.values, df.close.values
    t = pd.read_parquet("cache/propfirm/nq_nuit_tp4.parquet")
    risk = t.risk.fillna(t.risk.median()).values
    mfe = np.zeros(len(t))
    for i, (e, x, d, why) in enumerate(zip(t.entry_idx, t.exit_idx, t.dir, t.reason)):
        last = x - 1 if why == "SL" else x
        if last > e:
            en = cl[e]
            m = (hi[e + 1:last + 1].max() - en) if d > 0 else (en - lo[e + 1:last + 1].min())
            mfe[i] = max(m / (risk[i] * en), 0.0)
    t["MFE_R"] = mfe
    tp = t.reason == "TP"
    print(f"{len(t)} trades ; MFE médian {np.median(mfe):.2f} R ; TP avec MFE ≥ 1,98 R : "
          f"{(t.MFE_R[tp] >= 1.98).mean():.1%} ; SL avec MFE ≥ 0,5 R : {(t.MFE_R[t.reason == 'SL'] >= 0.5).mean():.1%}")
    t.to_parquet("cache/propfirm/nq_nuit_tp4_mfe.parquet")


if __name__ == "__main__":
    main()
