"""Pré-enregistrement n° 14 : nuits d'annonce NFP/CPI (8:30 ET) dans la règle NQ de nuit.

uv run python run_prereg14.py   → results/prereg14/ (results.csv, trades.csv, run.log)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_prereg12 as Q  # historique 2010-2015 actif, nuits 2011-07 → 2026-08
import run_prereg10 as P
from recolte1.engine import NY, ci_mean
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg14")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
PERIODS = {"sélection 2016-2026": ("2016-01-01", "2026-08-28"), "confirmation 2011-2015": ("2011-07-01", "2015-12-31")}
N_RANDOM = 500


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def night_R(t_out) -> pd.Series:
    e = Q.table(at(Q.D, "20:00", NY, -1), t_out, Q.MOM, "x")
    T = Q.sim(e, Q.STOP)
    t = T[T["cost"] == "net"].copy()
    t["R"] = P.r_multiples("NQ", e, t).values
    return t.groupby(pd.to_datetime(t["night"]))["R"].sum()


def dd(R: pd.Series) -> float:
    c = R.cumsum()
    return float((c - c.cummax()).min())


def main():
    cal = pd.read_csv("config/calendrier_macro_bls.csv", parse_dates=["date"])
    events = pd.DatetimeIndex(cal["date"].unique())
    base = night_R(Q.B["t_open"])
    early = night_R(at(Q.D, "08:25", NY)).reindex(base.index)
    df = pd.DataFrame({"base": base, "early": early})
    df["event"] = df.index.isin(events)
    df.to_csv(OUT / "trades.csv")
    rows = []
    for pname, (a, z) in PERIODS.items():
        d = df[(df.index >= a) & (df.index <= z)].copy()
        d["early"] = d["early"].fillna(d["base"])  # sortie 8:25 indisponible → base
        years = (d.index.max() - d.index.min()).days / 365.25
        b_dd, b_ran = dd(d["base"]), d["base"].sum() / years
        ev, non = d["event"].values, np.flatnonzero(~d["event"].values)
        k = int(ev.sum())
        worst10 = d["base"].nsmallest(10)
        log(f"{pname} : {len(d)} nuits, {k} d'annonce ; R/trade annonce {d.loc[ev, 'base'].mean():+.3f} "
            f"contre {d.loc[~ev, 'base'].mean():+.3f} ailleurs ; {int(d.loc[worst10.index, 'event'].sum())}/10 des pires nuits sont des nuits d'annonce")
        rows.append({"période": pname, "variante": "base", "nuits": len(d), "R_par_an": b_ran, "max_dd_R": b_dd})
        for vname in ["V1 pas de trade", "V2 sortie 8:25"]:
            def apply(mask):
                s = d["base"].copy()
                if vname.startswith("V1"):
                    return s[~mask]
                s[mask] = d.loc[mask, "early"]
                return s
            s = apply(ev)
            red = 1 - dd(s) / b_dd
            reds = []
            for i in range(N_RANDOM):
                m = np.zeros(len(d), bool)
                m[np.random.default_rng(i).choice(non, size=k, replace=False)] = True
                reds.append(1 - dd(apply(m)) / b_dd)
            reds = np.array(reds)
            mm, lo, hi = ci_mean(d.loc[ev, "base"].values - d.loc[ev, "early"].values) if vname.startswith("V2") else (np.nan,) * 3
            rows.append({"période": pname, "variante": vname, "nuits": len(s), "R_par_an": s.sum() / years,
                         "R_an_vs_base_%": s.sum() / years / b_ran * 100, "max_dd_R": dd(s), "reduction_dd_%": red * 100,
                         "aleatoire_p95_%": np.percentile(reds, 95) * 100, "rang_vs_aleatoire_%": (reds < red).mean() * 100,
                         "gain_9h30_vs_8h25_R": mm, "gain_lo": lo, "gain_hi": hi,
                         "c1": red >= 0.30, "c2": s.sum() / years >= 0.8 * b_ran, "c3": red > np.percentile(reds, 95)})
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "results.csv", index=False)
    pd.set_option("display.width", 250)
    log(R.round(3).to_string(index=False))
    sel = R[(R["période"].str.startswith("sélection")) & R["c1"].fillna(False) & R["c2"].fillna(False) & R["c3"].fillna(False)]["variante"].tolist()
    conf = R[(R["période"].str.startswith("confirmation")) & R["variante"].isin(sel) & R["c1"].fillna(False) & R["c2"].fillna(False)]["variante"].tolist()
    log(f"retenues : {sel or 'aucune'} ; confirmées : {conf or 'aucune'}")


if __name__ == "__main__":
    main()
