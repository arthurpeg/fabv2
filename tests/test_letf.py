"""Momentum de fin de séance (n° 9) : signal depuis la clôture de la veille, seuil, sens,
demi-séances, coût sur le prix réel."""

import numpy as np
import pandas as pd

from asym.backtest import cost_frac
from letf.rules import days, trades


def bars(spec: dict, factor: float = 1.0) -> pd.DataFrame:
    idx = pd.DatetimeIndex([pd.Timestamp(k).tz_localize("America/New_York").tz_convert("UTC") for k in spec])
    v = np.array(list(spec.values()), float)
    df = pd.DataFrame({"open": v, "high": v, "low": v, "close": v, "volume": 1.0, "factor": factor}, index=idx)
    return df.sort_index()


def session(d: str, o: float, p1430: float, c: float, close_bar="15:59") -> dict:
    return {f"{d} 09:30": o, f"{d} 14:30": p1430, f"{d} {close_bar}": c}


def test_follow_large_move_from_prior_close():
    df = bars({**session("2025-04-02", 100, 100, 100), **session("2025-04-03", 99, 97.5, 96.0)})
    T = trades(days(df, ("14:30",)), "14:30", 0.02)
    assert len(T) == 1 and T["dir"].iloc[0] == -1  # −2,5 % à 14:30 → short
    assert np.isclose(T["gross"].iloc[0], -(96.0 / 97.5 - 1))
    assert trades(days(df, ("14:30",)), "14:30", 0.03).empty  # sous le seuil de 3 %


def test_half_day_breaks_prior_close():
    df = bars({**session("2025-11-26", 100, 100, 100), **session("2025-11-28", 100, 100, 100, close_bar="12:59"),
               **session("2025-12-01", 97, 97, 96)})
    T = trades(days(df, ("14:30",)), "14:30", 0.02)
    assert T.empty  # la veille du 1er décembre est la demi-séance du 28 : pas de C_{t−1}


def test_cost_uses_real_price_when_adjusted():
    df = bars({**session("2025-04-02", 100, 100, 100), **session("2025-04-03", 99, 97.5, 96.0)}, factor=1.25)
    T = trades(days(df, ("14:30",)), "14:30", 0.02)
    assert np.isclose(cost_frac(T, ("pts", 0.35))[0], 0.35 / (97.5 / 1.25))
