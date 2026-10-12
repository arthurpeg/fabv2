"""Timing d'exécution FX (PREREGISTRATION_4.md) : économie d'exécution contre un benchmark naïf."""

import numpy as np
import pandas as pd

from fab.core import ASSETS, IS_END, NY, grid, hm
from fab.replications import FX_C, fx_grid
from fab.strategies import TOKYO

rng = np.random.default_rng(42)


def boot_t(x: np.ndarray, block=10, reps=4000) -> float:
    n = len(x)
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n - block, (reps, nb))
    idx = (starts[:, :, None] + np.arange(block)).reshape(reps, -1)[:, :n]
    se = x[idx].mean(1).std()
    return float(x.mean() / se)


def twap(g, s, e):
    cols = [m for m in g.C.columns if s <= m < e]
    return g.C[cols].ffill(axis=1).mean(axis=1)


def rule_x1(n):
    g = grid(n, NY, hm("02:00"), hm("16:00") + 5)
    bench = twap(g, hm("02:00"), hm("16:00"))
    buy = g.price_at(hm("08:00"))[0]
    sell = g.price_at(hm("16:00"))[0]
    return (bench - buy) / bench, (sell - bench) / bench, g.factor_at(hm("08:00")) , bench


def rule_x2(n):
    g = grid(n, TOKYO, hm("08:00"), hm("15:00") + 5)
    bench = twap(g, hm("08:00"), hm("15:00"))
    buy = g.price_at(hm("09:55"))[0]
    sell = g.price_at(hm("15:00"))[0]
    return (bench - buy) / bench, (sell - bench) / bench, g.factor_at(hm("08:00")), bench


def rule_x3(n):
    g = fx_grid(n)
    prev = g.price_at(FX_C)[0].shift(1)
    p1430, p1500 = g.price_at(FX_C - 30)[0], g.price_at(FX_C)[0]
    rod = p1430 / prev - 1
    up = rod > 0
    buy_px = p1430.where(up, p1500)      # acheteur : agit tout de suite si la devise monte
    sell_px = p1500.where(up, p1430)     # vendeur : attend si la devise monte
    ok = rod.notna() & p1430.notna() & p1500.notna()
    buy = ((p1430 - buy_px) / p1430).where(ok)
    sell = ((sell_px - p1430) / p1430).where(ok)
    return buy, sell, g.factor_at(FX_C - 30), p1430


rows, series = [], {}
for rid, fn in [("X1_europe_8h_16h", rule_x1), ("X2_tokyo_fix", rule_x2), ("X3_baltussen_close", rule_x3)]:
    for n in ["6E", "6J", "6B", "6A"]:
        a = ASSETS[n]
        buy, sell, fac, px = fn(n)
        df = pd.DataFrame({"buy": buy, "sell": sell, "fac": fac, "px": px}).dropna()
        df["avg"] = (df["buy"] + df["sell"]) / 2
        series[f"{rid}|{n}"] = df["avg"]
        is_m = df.index <= IS_END
        raw_px = df["px"] / df["fac"]
        ticks = df["avg"] * raw_px / a.tick
        rows.append({
            "règle": rid, "actif": n, "jours": len(df),
            "pb_IS": df.loc[is_m, "avg"].mean() * 1e4, "pb_OOS": df.loc[~is_m, "avg"].mean() * 1e4,
            "pb_acheteur": df["buy"].mean() * 1e4, "pb_vendeur": df["sell"].mean() * 1e4,
            "ticks": ticks.mean(), "$_par_M": df["avg"].mean() * 1e6,
            "t_boot": boot_t(df["avg"].values),
        })

res = pd.DataFrame(rows)
res["utile"] = (res["pb_IS"] > 0) & (res["pb_OOS"] > 0) & (res["t_boot"] > 2)
pd.set_option("display.width", 200)
print(res.round(2).to_string(index=False))
print(f"\n{int(res['utile'].sum())} / {len(res)} règles utiles")
res.to_csv("results/execution_timing.csv", index=False, float_format="%.4f")

# profil par année pour les règles utiles
S = pd.DataFrame(series)
yearly = (S.groupby(S.index.year).mean() * 1e4).round(2)
print("\nÉconomie moyenne (pb) par année :")
print(yearly[[c for c in S.columns if res.set_index(res["règle"] + "|" + res["actif"]).loc[c, "utile"]]].to_string())
yearly.to_csv("results/execution_timing_yearly.csv")
