"""Retour à la moyenne RSI : long sous `low`, short au-dessus de `high`, sortie à 50."""

import pandas as pd
import vectorbt as vbt

from lab.engine import Signals


def rsi_reversion(b: pd.DataFrame, n: int = 14, low: float = 30, high: float = 70, short: bool = True) -> Signals:
    rsi = vbt.RSI.run(b["close"], n).rsi
    return Signals(
        long_entries=rsi < low,
        long_exits=rsi > 50,
        short_entries=(rsi > high) if short else None,
        short_exits=(rsi < 50) if short else None,
    )
