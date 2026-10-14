"""Cassure de canal de Donchian (turtle) : entrée sur plus haut/bas de `n` barres,
sortie sur le canal opposé de `exit_n` barres."""

import pandas as pd

from lab.engine import Signals


def donchian(b: pd.DataFrame, n: int = 55, exit_n: int = 20, short: bool = True) -> Signals:
    hi = b["high"].rolling(n).max().shift(1)
    lo = b["low"].rolling(n).min().shift(1)
    xhi = b["high"].rolling(exit_n).max().shift(1)
    xlo = b["low"].rolling(exit_n).min().shift(1)
    c = b["close"]
    return Signals(
        long_entries=c > hi,
        long_exits=c < xlo,
        short_entries=(c < lo) if short else None,
        short_exits=(c > xhi) if short else None,
    )
