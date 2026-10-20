"""Exécution vectorbt d'une règle ouverture → clôture : une colonne, cible ±100 % du capital
à l'ouverture de t+1, 0 à la clôture ; frais = demi-coût aller-retour par ordre."""

from __future__ import annotations

import numpy as np
import pandas as pd
import vectorbt as vbt

INIT_CASH = 1_000_000.0


def cost_frac(T: pd.DataFrame, cost) -> np.ndarray:
    """Coût aller-retour en fraction du prix : nombre = points de base ; ("pts", x) = points."""
    if isinstance(cost, tuple):
        return cost[1] / T["p_in"].values
    return np.full(len(T), cost / 1e4)


def simulate(T: pd.DataFrame, cost) -> vbt.Portfolio:
    half = cost_frac(T, cost) / 2
    ent = pd.DataFrame({"ts": T["t_in"].values, "price": T["p_in"].values, "target": T["dir"].values, "fee": half})
    ext = pd.DataFrame({"ts": T["t_out"].values, "price": T["p_out"].values, "target": 0.0, "fee": half})
    ev = pd.concat([ent, ext]).sort_values("ts")
    if ev["ts"].duplicated().any():
        raise ValueError("ordres au même instant")
    idx = pd.to_datetime(ev["ts"].values, utc=True)
    return vbt.Portfolio.from_orders(
        close=pd.Series(ev["price"].values, index=idx), size=pd.Series(ev["target"].values, index=idx),
        size_type="targetpercent", direction="both", fees=pd.Series(ev["fee"].values, index=idx),
        init_cash=INIT_CASH, freq="1min",
    )


def daily_returns(pf: vbt.Portfolio, T: pd.DataFrame, calendar: pd.DatetimeIndex) -> pd.Series:
    """Rendement par séance : valeur après la sortie de chaque trade, 0 les jours sans trade."""
    v = pf.value()
    after = v.reindex(pd.to_datetime(T["t_out"].values, utc=True)).values
    s = pd.Series(after, index=pd.DatetimeIndex(T["date"])).sort_index()
    prev = s.shift(1, fill_value=INIT_CASH)
    r = s / prev - 1
    return r.reindex(calendar, fill_value=0.0)


def net_returns(T: pd.DataFrame, cost) -> np.ndarray:
    """Rendement net par trade (arithmétique, 1×) : sens × (p_out/p_in − 1) − coût."""
    return T["gross"].values - cost_frac(T, cost)
