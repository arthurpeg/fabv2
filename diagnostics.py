"""Diagnostics POST-HOC des survivants (aucun paramètre modifié) :
Sharpe par année, avant/après publication, coûts ×2, long vs short, fenêtre Delgado 2026."""

import dataclasses

import numpy as np
import pandas as pd

from fab.core import ASSETS, backtest, sharpe
from fab.strategies import _with_session, m2_noise

PERIODS = {
    "2016-2022 (IS)": ("2016-01-01", "2022-12-31"),
    "2023-2026 (OOS)": ("2023-01-01", "2026-08-31"),
    "pré-publication (→ 2024-05)": ("2016-01-01", "2024-05-15"),
    "post-publication (2024-05 →)": ("2024-05-16", "2026-08-31"),
    "fenêtre Delgado (2025-09 → 2026-08)": ("2025-09-01", "2026-08-31"),
}


def run(name):
    a = ASSETS[name]
    t, tz, dates = _with_session(a, lambda g: m2_noise(a, g))
    base = backtest("M2", a, t, tz, dates)
    a2 = dataclasses.replace(a, tick=a.tick * 2, point_value=a.point_value / 2)  # coût ×2 en points
    x2 = backtest("M2x2", a2, t, tz, dates)
    longs = backtest("M2L", a, t[t.dir > 0], tz, dates)
    shorts = backtest("M2S", a, t[t.dir < 0], tz, dates)
    rows = []
    for lab, (s, e) in PERIODS.items():
        m = (dates >= s) & (dates <= e)
        rows.append({
            "actif": name, "période": lab,
            "SR net": sharpe(base.daily_net[m]), "SR brut": sharpe(base.daily_gross[m]),
            "SR net coûts×2": sharpe(x2.daily_net[m]),
            "SR long": sharpe(longs.daily_net[m]), "SR short": sharpe(shorts.daily_net[m]),
            "rendement net %": float((1 + base.daily_net[m]).prod() - 1) * 100,
        })
    yearly = base.daily_net.groupby(base.daily_net.index.year).apply(sharpe).rename(name)
    eq = (1 + base.daily_net).cumprod().rename(name)
    dd = float((eq / eq.cummax() - 1).min() * 100)
    return pd.DataFrame(rows), yearly, eq, dd


if __name__ == "__main__":
    tabs, years, eqs = [], [], []
    for n in ["ES", "NQ"]:
        tab, yr, eq, dd = run(n)
        print(f"{n}: drawdown max net = {dd:.1f} %")
        tabs.append(tab), years.append(yr), eqs.append(eq)
    tab = pd.concat(tabs)
    yr = pd.concat(years, axis=1)
    pd.set_option("display.width", 200)
    print(tab.round(2).to_string(index=False))
    print(yr.round(2).to_string())
    tab.to_csv("results/m2_diagnostics.csv", index=False, float_format="%.3f")
    yr.to_csv("results/m2_yearly_sharpe.csv", float_format="%.3f")
    pd.concat(eqs, axis=1).to_csv("results/m2_equity.csv", float_format="%.5f")
