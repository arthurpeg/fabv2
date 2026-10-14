"""Barres rééchantillonnées + moteur vectorbt `from_signals`.

Conventions :
- un signal calculé sur la barre t (clôture connue) s'exécute à l'open de t+1 ;
- coût = `Asset.rt_cost / 2` par côté (1 tick + 5 $ aller-retour), converti en
  fraction du prix brut (prix ajusté / facteur de roulement) ;
- exposition 100 % du capital, long et/ou short, sans levier ;
- IS jusqu'au 2022-12-31, OOS ensuite (même coupure que `fab/`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from typing import Callable

import numpy as np
import pandas as pd
import vectorbt as vbt

from fab.core import ASSETS, IS_END, load

NY = "America/New_York"


@lru_cache(maxsize=None)
def bars(name: str, tf: str = "1h") -> pd.DataFrame:
    """OHLCV rééchantillonné. `tf` = règle pandas ("5min", "1h", "4h", "1D").

    "1D" = session CME (18:00 → 17:00 ET), étiquetée par la date de clôture.
    Les barres intraday sont en UTC, étiquetées à gauche ; les barres vides sont retirées.
    """
    df = load(name)
    agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum", "factor": "last"}
    if tf.upper() in ("1D", "D"):
        loc = df.tz_convert(NY)
        # 18:00 ET → minuit le lendemain : la session prend la date de sa clôture
        key = (loc.index + pd.Timedelta(hours=6)).tz_localize(None).normalize()
        out = loc.groupby(key).agg(agg)
        out = out[out.index.dayofweek < 5]
    else:
        out = df.resample(tf, label="left", closed="left").agg(agg)
    return out.dropna(subset=["open", "close"])


# --------------------------------------------------------------------------- signaux


@dataclass
class Signals:
    """Booléens alignés sur l'index des barres, évalués à la clôture."""

    long_entries: pd.Series
    long_exits: pd.Series
    short_entries: pd.Series | None = None
    short_exits: pd.Series | None = None


Strategy = Callable[..., Signals]


@dataclass
class Run:
    name: str
    asset: str
    tf: str
    params: dict
    pf: vbt.Portfolio
    bars: pd.DataFrame = field(repr=False)


def _shift(s: pd.Series | None, idx: pd.Index) -> pd.Series:
    if s is None:
        return pd.Series(False, index=idx)
    return s.reindex(idx).fillna(False).astype(bool).shift(1, fill_value=False)


def run(strategy: Strategy, asset: str, tf: str = "1h", start: str | None = None, **params) -> Run:
    b = bars(asset, tf)
    if start:
        b = b[b.index >= pd.Timestamp(start, tz=b.index.tz)]
    sig = strategy(b, **params)
    a = ASSETS[asset]
    raw_open = b["open"] / b["factor"]
    fees = (a.rt_cost / 2) / raw_open
    freq = "1D" if tf.upper() in ("1D", "D") else tf
    pf = vbt.Portfolio.from_signals(
        close=b["close"],
        price=b["open"],  # exécution à l'open de la barre suivant le signal
        entries=_shift(sig.long_entries, b.index),
        exits=_shift(sig.long_exits, b.index),
        short_entries=_shift(sig.short_entries, b.index),
        short_exits=_shift(sig.short_exits, b.index),
        fees=fees,
        init_cash=1_000_000.0,
        freq=freq,
    )
    name = getattr(strategy, "__name__", "strategy")
    return Run(name, asset, tf, params, pf, b)


# --------------------------------------------------------------------------- métriques


def _daily(r: Run) -> pd.Series:
    val = r.pf.value()
    idx = val.index.tz_localize(None) if val.index.tz is not None else val.index
    d = pd.Series(val.values, index=idx.normalize()).groupby(level=0).last()
    return d.pct_change().dropna()


def _sharpe(x: pd.Series) -> float:
    sd = x.std()
    return float(x.mean() / sd * np.sqrt(252)) if sd > 0 else np.nan


def report(r: Run) -> dict:
    d = _daily(r)
    tr = r.pf.trades.records_readable
    row = {"strategy": r.name, "asset": r.asset, "tf": r.tf, **{f"p_{k}": v for k, v in r.params.items()}}
    row["n_trades"] = len(tr)
    for lab, m in [("IS", d.index <= IS_END), ("OOS", d.index > IS_END)]:
        row[f"sharpe_{lab}"] = _sharpe(d[m])
        row[f"ret_{lab}_%"] = float((1 + d[m]).prod() - 1) * 100
    row["max_dd_%"] = float(r.pf.max_drawdown()) * 100
    row["win_rate_%"] = float((tr["PnL"] > 0).mean() * 100) if len(tr) else np.nan
    row["exposure_%"] = float((r.pf.position_mask()).mean() * 100)
    return row
