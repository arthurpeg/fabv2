"""Pré-enregistrement n° 16 : clôture sous le VWAP de 15:15-16:15 ET (pression vendeuse) et règle de nuit 20:00.

uv run python run_prereg16.py   → results/prereg16/ (results.csv, nights.csv, run.log)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_prereg12 as Q  # historique 2010-2015 actif
from run_prereg15 import dd, nights_R
from recolte1.engine import NY, _block_index, ci_mean, load, price_at
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg16")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
A0, Z0 = "2011-07-01", "2026-08-28"
N_RANDOM = 500


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def selling_signal(asset: str) -> pd.Series:
    """S de la séance d-1, indexé par la nuit d."""
    df = load(asset)
    ny = df.index.tz_convert(NY)
    mins = ny.hour * 60 + ny.minute
    w = df[(mins >= 15 * 60 + 15) & (mins < 16 * 60 + 15)]
    day = w.index.tz_convert(NY).tz_localize(None).normalize()
    tp = (w["high"] + w["low"] + w["close"]) / 3
    vwap = (tp * w["volume"]).groupby(day).sum() / w["volume"].groupby(day).sum()
    close, _ = price_at(asset, at(Q.D, "16:15", NY))
    s = (close < vwap.reindex(Q.D)) & ~Q.B["half"] & vwap.reindex(Q.D).notna() & close.notna()
    return s.shift(1, fill_value=False).astype(bool)


def p_diff(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """Différence de moyennes a − b et p unilatéral (bootstrap par blocs indépendant pour chaque groupe, sous H0 recentrée)."""
    d = a.mean() - b.mean()
    ma = (a - a.mean())[_block_index(len(a))].mean(1)
    mb = (b - b.mean())[_block_index(len(b))].mean(1)
    return float(d), float(((ma - mb) >= d).mean())


def main():
    rows, store = [], {}
    for asset in ["ES", "YM", "NQ"]:
        R = nights_R(asset)
        R = R[(R.index >= A0) & (R.index <= Z0)]
        S = selling_signal(asset).reindex(R.index).values
        store[asset] = pd.DataFrame({"R": R, "S": S})
        years = (R.index.max() - R.index.min()).days / 365.25
        d, p = p_diff(R[S].values, R[~S].values)
        ms, los, his = ci_mean(R[S].values)
        mn, lon, hin = ci_mean(R[~S].values)
        b_dd, b_ran = dd(R), R.sum() / years
        x = R[S]
        red = 1 - dd(x) / b_dd
        reds = np.array([1 - dd(R.iloc[np.sort(np.random.default_rng(i).choice(len(R), int(S.sum()), replace=False))]) / b_dd
                         for i in range(N_RANDOM)])
        rows.append({
            "marché": asset, "rôle": "confirmation" if asset == "NQ" else "sélection", "nuits": len(R),
            "part_S_%": S.mean() * 100, "R_trade_S": ms, "S_lo": los, "S_hi": his, "R_trade_nonS": mn, "nonS_lo": lon, "nonS_hi": hin,
            "diff": d, "p_H": p, "H_ok": d > 0 and p < 0.05,
            "base_R_an": b_ran, "base_dd": b_dd, "V1_R_an": x.sum() / years, "V1_R_an_vs_base_%": x.sum() / years / b_ran * 100,
            "V1_dd": dd(x), "V1_reduction_dd_%": red * 100, "aleatoire_p95_%": np.percentile(reds, 95) * 100,
            "V1_c1": red >= 0.30, "V1_c2": x.sum() / years >= 0.8 * b_ran, "V1_c3": red > np.percentile(reds, 95),
        })
        log(f"{asset} fait")
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "results.csv", index=False)
    pd.concat({k: v for k, v in store.items()}).to_csv(OUT / "nights.csv")
    pd.set_option("display.width", 260)
    log(res.round(3).T.to_string())
    sel = res[res["rôle"] == "sélection"]
    h_sel = bool(sel["H_ok"].all())
    v_sel = bool((sel["V1_c1"] & sel["V1_c2"] & sel["V1_c3"]).all())
    nq = res[res["marché"] == "NQ"].iloc[0]
    log(f"H : sélection {h_sel} ; confirmée NQ {h_sel and bool(nq['H_ok'])}")
    log(f"V1 : sélection {v_sel} ; confirmée NQ {v_sel and bool(nq['V1_c1'] and nq['V1_c2'])}")


if __name__ == "__main__":
    main()
