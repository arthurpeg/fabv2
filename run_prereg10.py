"""Pré-enregistrement n° 10 : momentum 12-1 de nuit, entrée 20:00 ET, SL 2 ATR / TP 5 ATR M15, sur ES et YM.

uv run python run_prereg10.py   → results/prereg10/ (trades.csv, results.csv, by_year.csv, run.log)

Règle figée dans PREREGISTRATION_10.md ; simulation reprise de run_recolte1_atr.py sans changement.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_recolte1_atr as A
from recolte1.engine import _block_index, ci_mean, load
from recolte1.rules import base, monthly, next_month_sign, sessions

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg10")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
CLOCKS = ["19:00", "20:00", "21:00"]
A.VARIANTS = [("SL 2 ATR / TP 5 ATR", 2.0, 5.0)]


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def entries(asset: str) -> pd.DataFrame:
    b = sessions()
    bb = base(asset)
    s = next_month_sign(bb, monthly(bb, "cc").shift(1).rolling(11, min_periods=11).sum())
    w = pd.DataFrame({"t_start": b["t_prev"], "t_end": b["t_open"], "dir": s.reindex(b.index).fillna(0.0)})
    A.windows = lambda rule: (asset, w)  # même construction que la règle NQ, sur l'actif lui-même
    _, e = A.entries_table("prereg10")
    return e[e["clock"].isin(CLOCKS)]


def r_multiples(asset: str, e: pd.DataFrame, T: pd.DataFrame) -> pd.Series:
    df = load(asset).copy()
    df.attrs = {}
    idx = df.index.as_unit("ns")
    e = e.copy()
    e["p_in"] = A.bar_pos(idx, e["t_in"])
    e = e[e["p_in"] >= 0].drop_duplicates("p_in")
    atr = A.atr_m15(df).reindex(pd.DatetimeIndex(e["t_in"]).as_unit("ns"), method="ffill")
    frac = pd.Series(atr.values / df["close"].values[e["p_in"].values], index=e["p_in"].values)
    return T["ret"] / (2 * frac.reindex(T["entry_idx"].values).values)


def p_one_sided(x: np.ndarray) -> float:
    """Part des moyennes bootstrap (blocs de 10) ≤ 0, après recentrage sous H0 (moyenne nulle)."""
    x = x[np.isfinite(x)]
    m = (x - x.mean())[_block_index(len(x))].mean(axis=1)
    return float((m >= x.mean()).mean())


def main():
    rows, years, alltr = [], [], []
    for asset in ["ES", "YM"]:
        e = entries(asset)
        T = A.simulate(asset, e)
        T = T[T["cost"] == "net"].copy()
        T["R"] = r_multiples(asset, e, T).values
        T["asset"] = asset
        T["year"] = pd.to_datetime(T["night"]).dt.year
        alltr.append(T)
        for lab, t in [("20:00", T[T["clock"] == "20:00"]), ("bloc 19-21", T)]:
            x = t.groupby("night")["R"].sum().values if lab == "bloc 19-21" else t["R"].values
            m, lo, hi = ci_mean(x)
            y = t.groupby("year")["R"].sum()
            cum = t.sort_values("entry_idx")["R"].cumsum()
            h1 = t[t["year"] <= 2020]["R"].mean()
            h2 = t[t["year"] >= 2021]["R"].mean()
            rows.append({
                "asset": asset, "test": lab, "principal": lab == "20:00", "n_trades": len(t),
                "unité": "R/trade" if lab == "20:00" else "R/nuit", "moyenne": m, "ic_lo": lo, "ic_hi": hi,
                "p_unilatéral": p_one_sided(x), "R_2017_2020_par_trade": h1, "R_2021_2026_par_trade": h2,
                "R_par_an_2017_2025": y.loc[2017:2025].mean(), "annees_pos_2017_2025": int((y.loc[2017:2025] > 0).sum()),
                "max_dd_R": float((cum - cum.cummax()).min()),
                "TP_%": (t["reason"] == "TP").mean() * 100, "SL_%": (t["reason"] == "SL").mean() * 100,
                "sortie_9h30_%": (t["reason"] == "fin fenêtre").mean() * 100,
                "pct_long": (t["dir"] > 0).mean() * 100,
            })
            years.append(y.rename(f"{asset} {lab}"))
    R = pd.DataFrame(rows)
    # Holm sur les 2 tests principaux
    prim = R[R["principal"]].sort_values("p_unilatéral")
    adj = np.maximum.accumulate(prim["p_unilatéral"].values * np.array([2, 1]))
    R.loc[prim.index, "p_holm"] = np.minimum(adj, 1)
    R.to_csv(OUT / "results.csv", index=False)
    pd.concat(years, axis=1).to_csv(OUT / "by_year.csv")
    pd.concat(alltr).to_csv(OUT / "trades.csv", index=False)
    pd.set_option("display.width", 250)
    log(R.round(4).T.to_string())
    log(pd.concat(years, axis=1).round(1).to_string())
    ok = {a: bool(r["p_holm"] < 0.05 and r["R_2017_2020_par_trade"] > 0 and r["R_2021_2026_par_trade"] > 0)
          for a, r in R[R["principal"]].set_index("asset").iterrows()}
    verdict = "SUCCÈS" if all(ok.values()) else ("SUCCÈS PARTIEL" if any(ok.values()) else "ÉCHEC")
    log(f"critères principaux par marché : {ok} → {verdict}")


if __name__ == "__main__":
    main()
