"""Moteur vectorbt : un portefeuille `from_orders` à 4 colonnes (une par paire,
1/4 du capital chacune, sans partage de cash), regroupé en un seul portefeuille.

Convention de `fab/core.py` : ordres `targetpercent` (cible = sens, 0 à la sortie) ;
une sortie et une entrée au même instant fusionnent en un seul ordre (la cible finale
gagne). Si les deux ont le même sens, vbt garde la position, sans payer d'aller-retour.
Frais à chaque ordre = demi-coût aller-retour en pips / prix.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import vectorbt as vbt

from fxreopen.data import NY, PAIRS

INIT_CASH = 1_000_000.0


def _orders(t: pd.DataFrame) -> pd.DataFrame:
    """Trades d'une paire (avec colonne `cost`) → ordres (ts, prix, cible, frais en points)."""
    pip = PAIRS[t["pair"].iloc[0]].pip
    half = t["cost"].values / 2 * pip
    ent = pd.DataFrame({"ts": t["t_in"].values, "price": t["p_in"].values, "target": t["dir"].values,
                        "fee_pts": half, "o": 1})
    ext = pd.DataFrame({"ts": t["t_out"].values, "price": t["p_out"].values, "target": 0.0,
                        "fee_pts": half, "o": 0})
    g = pd.concat([ent, ext]).sort_values(["ts", "o"]).groupby("ts")
    ev = pd.DataFrame({"price": g["price"].last(), "target": g["target"].last(), "fee_pts": g["fee_pts"].sum()})
    traded = np.abs(np.diff(np.r_[0.0, ev["target"].values]))
    ev["fee"] = ev["fee_pts"] / ev["price"] / np.where(traded > 0, traded, 1.0)
    return ev


def simulate(t: pd.DataFrame) -> vbt.Portfolio:
    """`t` : trades de toutes les paires, avec `cost` (voir `evaluate.with_cost`)."""
    per = {p: _orders(g.sort_values("t_in")) for p, g in t.groupby("pair")}
    for p in PAIRS:  # paire sans trade : colonne vide
        per.setdefault(p, pd.DataFrame(columns=["price", "target", "fee"], dtype=float))
    idx = pd.Index(sorted(set().union(*[set(e.index) for e in per.values()])))
    cols = list(PAIRS)
    price = pd.DataFrame({p: per[p]["price"].reindex(idx) for p in cols})
    size = pd.DataFrame({p: per[p]["target"].reindex(idx) for p in cols})
    fees = pd.DataFrame({p: per[p]["fee"].reindex(idx) for p in cols}).fillna(0.0)
    price = price.ffill().bfill()  # valorisation entre deux ordres (à plat de toute façon)
    ts = pd.to_datetime(idx.values, utc=True)
    for df in (price, size, fees):
        df.index = ts
    return vbt.Portfolio.from_orders(
        close=price, size=size, size_type="targetpercent", direction="both", fees=fees,
        init_cash=INIT_CASH / len(cols), cash_sharing=False, group_by=True, freq="1min",
    )


def session_returns(pf: vbt.Portfolio, calendar: pd.DatetimeIndex) -> pd.Series:
    """Rendement par séance CME (date ET de la reprise de 18:00) du portefeuille regroupé."""
    val = pf.value()
    sess = (val.index.tz_convert(NY).tz_localize(None) - pd.Timedelta(hours=18)).normalize()
    v = val.groupby(sess).last()
    v = v.reindex(calendar.union(v.index)).ffill().fillna(INIT_CASH)
    return (v / v.shift(1, fill_value=INIT_CASH) - 1).reindex(calendar).fillna(0.0)


def trade_table(pf: vbt.Portfolio) -> pd.DataFrame:
    """Trades vbt (toutes colonnes) avec date de séance, P&L et rendement."""
    r = pf.trades.records_readable
    ts = pd.to_datetime(r["Entry Timestamp"], utc=True)
    r["date"] = (ts.dt.tz_convert(NY).dt.tz_localize(None) - pd.Timedelta(hours=18)).dt.normalize()
    return r


def max_drawdown(r: pd.Series) -> float:
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())
