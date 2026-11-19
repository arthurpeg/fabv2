"""Pré-enregistrement n° 11 : la règle NQ de nuit (n° 10) hors échantillon, nuits 2011-07 → 2015-12.

uv run python run_prereg11.py   → results/prereg11/ (results.csv, by_year.csv, trades.csv, run.log)

Même code que run_prereg10.py ; seules changent les données (historique 2010-2015 rabouté) et
la période de test fixée dans PREREGISTRATION_11.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import recolte1.engine as E
import recolte1.rules as RU

E.USE_2010 = True
RU.START = "2010-06-08"

import run_prereg10 as P  # noqa: E402
from recolte1.engine import ci_mean  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg11")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
T0, T1 = "2011-07-01", "2015-12-31"
H1_END = "2013-12-31"


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def main():
    rows, years, alltr = [], [], []
    for asset in ["NQ", "ES", "YM"]:
        r = E.load(asset).attrs["rolls"]
        r = r[(r.index >= "2010-06-01") & (r.index < "2016-01-04")]
        log(f"{asset} : {len(r)} roulements 2010-2015, |écart| médian {r.abs().median() * 1e4:.1f} bp")
        e = P.entries(asset)
        T = P.A.simulate(asset, e)
        T["R"] = np.nan
        for c in ["gross", "net"]:
            m = T["cost"] == c
            T.loc[m, "R"] = P.r_multiples(asset, e, T[m]).values
        nt = pd.to_datetime(T["night"])
        T = T[(nt >= T0) & (nt <= T1)].copy()
        T["year"] = pd.to_datetime(T["night"]).dt.year
        T["asset"] = asset
        alltr.append(T)
        tests = [("20:00", "net"), ("20:00", "gross")] + ([("bloc 19-21", "net")] if asset == "NQ" else [])
        for lab, cost in tests:
            t = T[T["cost"] == cost]
            if lab == "20:00":
                t = t[t["clock"] == "20:00"]
            x = t.groupby("night")["R"].sum().values if lab != "20:00" else t["R"].values
            m, lo, hi = ci_mean(x)
            nt = pd.to_datetime(t["night"])
            y = t.groupby("year")["R"].sum()
            cum = t.sort_values("entry_idx")["R"].cumsum()
            rows.append({
                "asset": asset, "test": lab, "cost": cost, "principal": asset == "NQ" and lab == "20:00" and cost == "net",
                "n_trades": len(t), "moyenne": m, "ic_lo": lo, "ic_hi": hi,
                "p_unilatéral": P.p_one_sided(x) if cost == "net" else np.nan,
                "R_2011_2013": t[nt <= H1_END]["R"].mean(), "R_2014_2015": t[nt > H1_END]["R"].mean(),
                "R_par_an": y.loc[2012:2015].mean(), "max_dd_R": float((cum - cum.cummax()).min()),
                "TP_%": (t["reason"] == "TP").mean() * 100, "SL_%": (t["reason"] == "SL").mean() * 100,
                "pct_long": (t["dir"] > 0).mean() * 100,
            })
            if cost == "net":
                years.append(y.rename(f"{asset} {lab}"))
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "results.csv", index=False)
    pd.concat(years, axis=1).to_csv(OUT / "by_year.csv")
    pd.concat(alltr).to_csv(OUT / "trades.csv", index=False)
    pd.set_option("display.width", 250)
    log(R.round(4).T.to_string())
    log(pd.concat(years, axis=1).round(1).to_string())
    p = R[R["principal"]].iloc[0]
    ok = p["moyenne"] > 0 and p["p_unilatéral"] < 0.05 and p["R_2011_2013"] > 0 and p["R_2014_2015"] > 0
    log(f"verdict pré-enregistré : {'SUCCÈS' if ok else 'ÉCHEC'}")


if __name__ == "__main__":
    main()
