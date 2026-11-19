"""Pré-enregistrement n° 17 : exécution au VWAP (entrée 20:00-21:00, sortie au temps 9:00-9:30) contre heure fixe.

uv run python run_prereg17.py   → results/prereg17/ (results.csv, trades.csv, run.log)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_prereg12 as Q  # historique 2010-2015 actif
import run_prereg10 as P
import run_recolte1_atr as A
from recolte1.engine import NY, ci_mean, load, price_at
from recolte1.rules import at, base, monthly, next_month_sign

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg17")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
A0, Z0 = "2011-07-01", "2026-08-28"


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def vwap_between(df: pd.DataFrame, t_a: pd.Series, t_z: pd.Series) -> np.ndarray:
    """VWAP (prix typique) des barres démarrant dans [t_a, t_z[ pour chaque ligne."""
    idx = df.index.as_unit("ns")
    tp = ((df["high"] + df["low"] + df["close"]) / 3).values
    v = df["volume"].values.astype(float)
    cpv = np.concatenate([[0.0], np.cumsum(tp * v)])
    cv = np.concatenate([[0.0], np.cumsum(v)])
    i = idx.searchsorted(pd.DatetimeIndex(t_a).as_unit("ns"))
    j = idx.searchsorted(pd.DatetimeIndex(t_z).as_unit("ns"))
    vol = cv[j] - cv[i]
    return np.where((j > i) & (vol > 0), (cpv[j] - cpv[i]) / np.where(vol > 0, vol, 1), np.nan)


def run(asset: str) -> pd.DataFrame:
    bb = base(asset)
    mom = next_month_sign(bb, monthly(bb, "cc").shift(1).rolling(11, min_periods=11).sum()).reindex(Q.D).fillna(0.0)
    t20 = at(Q.D, "20:00", NY, -1)
    e = Q.table(t20, Q.B["t_open"], mom, asset)
    A.VARIANTS = Q.STOP
    T = A.simulate(asset, e)
    t = T[T["cost"] == "net"].copy()
    t["R"] = P.r_multiples(asset, e, t).values
    t["risk"] = t["ret"] / t["R"]  # 2 ATR / prix d'entrée
    t["night"] = pd.to_datetime(t["night"])
    t = t[(t["night"] >= A0) & (t["night"] <= Z0)].reset_index(drop=True)
    df = load(asset)
    n = pd.DatetimeIndex(t["night"])
    ser = lambda hhmm, off=0: at(n, hhmm, NY, off).reset_index(drop=True)  # garde le fuseau UTC
    t20n, t21n, t900, t930 = ser("20:00", -1), ser("21:00", -1), ser("09:00"), ser("09:30")
    p20 = price_at(asset, t20n)[0].values
    p930 = price_at(asset, t930)[0].values
    vw_in = vwap_between(df, t20n, t21n)
    vw_out = vwap_between(df, t900, t930)
    t["gain_E1_R"] = t["dir"] * (p20 - vw_in) / p20 / t["risk"]
    t["gain_E2_R"] = np.where(t["reason"] == "fin fenêtre", t["dir"] * (vw_out - p930) / p20 / t["risk"], np.nan)
    t["asset"] = asset
    return t


def main():
    rows, all_t = [], []
    for asset in ["NQ", "ES", "YM"]:
        t = run(asset)
        all_t.append(t)
        for k in ["gain_E1_R", "gain_E2_R"]:
            x = t[k].dropna().values
            m, lo, hi = ci_mean(x)
            rows.append({"marché": asset, "test": k, "trades": len(x), "gain_moyen_R": m, "lo": lo, "hi": hi,
                         "R_base_par_trade": t["R"].mean(), "part_positifs_%": (x > 0).mean() * 100})
        log(f"{asset} fait")
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "results.csv", index=False)
    pd.concat(all_t).to_csv(OUT / "trades.csv", index=False)
    pd.set_option("display.width", 220)
    log(res.round(4).to_string(index=False))
    for k in ["gain_E1_R", "gain_E2_R"]:
        r = res[res["test"] == k].set_index("marché")
        ok = r.loc["NQ", "lo"] > 0 and (r.loc[["ES", "YM"], "gain_moyen_R"] > 0).all()
        log(f"{k} : exécution VWAP retenue = {bool(ok)}")


if __name__ == "__main__":
    main()
