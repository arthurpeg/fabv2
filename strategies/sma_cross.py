"""Croisement de moyennes mobiles : long si SMA rapide > lente, short sinon."""

import pandas as pd
import vectorbt as vbt

from lab.engine import Signals


def sma_cross(b: pd.DataFrame, fast: int = 20, slow: int = 100, short: bool = True) -> Signals:
    f = vbt.MA.run(b["close"], fast).ma
    s = vbt.MA.run(b["close"], slow).ma
    up, down = f > s, f < s
    return Signals(up, down, down if short else None, up if short else None)
