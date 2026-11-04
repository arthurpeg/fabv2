"""Performances de la règle NQ de nuit (mom, compte 20:00, momentum 12-1, SL 2 / TP 5 ATR M15, sortie 9:30 ET,
coût 1 tick + 5 $) du 2011-07 au 2026-11-03. DESCRIPTIF, hors compteur.

uv run python run_mom_perf.py → results/mom_perf/ (run.log, periodes.csv, annees.csv)

Trades vectorbt déjà calculés avec le code figé (run_recolte1_atr.simulate) :
  - 2011-07-01 → 2026-08-28 : results/nq_nuit_heures/trades.csv (run_nq_nuit_heures.py, colonne 20:00, net) ;
  - 2026-08-31 → 2026-11-03 : results/holdout_anticipe/trades_H1_mom.csv (fenêtre déjà vue, avenant A du n° 26).
Les données à partir du 2026-11-04 (holdout officiel du n° 26) ne sont pas utilisées.
R = rendement net / (2 x ATR M15 / prix) ; Sharpe sur le R par nuit (nuits sans trade à 0), x racine(252).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from run_nq_nuit_3n_vbt import nw_t

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/mom_perf")
PERIODES = {"2011-07 → 2015-12 (hors échantillon, n° 11)": ("2011-07-01", "2015-12-31"),
            "2016-2024": ("2016-01-01", "2024-12-31"), "2025 → 2026-08-28": ("2025-01-01", "2026-08-28"),
            "2026-08-31 → 2026-11-03 (fenêtre vue)": ("2026-08-31", "2026-11-03"),
            "2011-07 → 2026-11-03 (tout)": ("2011-07-01", "2026-11-03")}


def stats(t: pd.DataFrame) -> dict:
    r = t.R.values
    eq = np.r_[0.0, np.cumsum(r)]
    ans = (t.night.max() - t.night.min()).days / 365.25
    return {"Nuits": len(r), "Longs %": 100 * (t.dir > 0).mean(), "Win %": 100 * (r > 0).mean(),
            "TP %": 100 * (t.reason == "TP").mean(), "SL %": 100 * (t.reason == "SL").mean(),
            "E[R] net": r.mean(), "R/an": r.sum() / ans, "Total R": r.sum(),
            "Sharpe (R)": r.mean() / r.std() * np.sqrt(252), "Max DD (R)": (eq - np.maximum.accumulate(eq)).min(),
            "Pire nuit (R)": r.min(), "t NW": nw_t(r) if len(r) > 10 else np.nan,
            "Rendement net (bps/nuit)": 1e4 * t.ret.mean(), "Rendement net / an (%)": 100 * t.ret.sum() / ans}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    h = pd.read_csv("results/nq_nuit_heures/trades.csv", parse_dates=["night"])
    h = h[(h.clock == "20:00") & (h.cost == "net")]
    w = pd.read_csv("results/holdout_anticipe/trades_H1_mom.csv", parse_dates=["night"])
    cols = [c for c in h.columns if c in w.columns]
    t = pd.concat([h[cols], w[cols]], ignore_index=True).sort_values("night")
    assert t.night.max() <= pd.Timestamp("2026-11-03")
    tab = {p: stats(t[(t.night >= a) & (t.night <= z)]) for p, (a, z) in PERIODES.items()}
    tab = pd.DataFrame(tab)
    tab.to_csv(OUT / "periodes.csv")
    yr = t.groupby(t.night.dt.year).agg(nuits=("R", "size"), R=("R", "sum"), E_R=("R", "mean"),
                                        rendement_pct=("ret", lambda x: 100 * x.sum()),
                                        win_pct=("R", lambda x: 100 * (x > 0).mean()))
    yr.to_csv(OUT / "annees.csv")
    txt = (f"Règle NQ de nuit (mom), vectorbt, 2011-07-01 → {t.night.max():%Y-%m-%d}\n\n{tab.round(3).to_string()}\n\n"
           f"Par année :\n{yr.round(2).to_string()}")
    print(txt)
    (OUT / "run.log").write_text(txt, encoding="utf-8")


if __name__ == "__main__":
    main()
