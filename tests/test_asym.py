"""Asymétrie de Valenti : séances, signaux du jour t, trades de t+1, exclusions, vectorbt."""

import numpy as np
import pandas as pd

from asym.backtest import daily_returns, net_returns, simulate
from asym.rules import ES, next_day_frame, sessions, signals, trades


def day(d: str, o: float, h: float, low: float, c: float, tz="America/New_York", a="09:30", b="15:59",
        mid="12:00") -> dict:
    t = lambda hm: pd.Timestamp(f"{d} {hm}").tz_localize(tz).tz_convert("UTC")  # noqa: E731
    rows = {t(a): (o, o, o, o), t("09:31"): (o, o, o, o), t(mid): (o, h, low, o), t(b): (c, c, c, c)}
    return rows


def frame(*days: dict) -> pd.DataFrame:
    rows = {k: v for dd in days for k, v in dd.items()}
    idx = pd.DatetimeIndex(sorted(rows))
    return pd.DataFrame([rows[i] for i in idx], index=idx, columns=["open", "high", "low", "close"])


def test_session_ohlc_and_asym_sign():
    df = frame(day("2025-07-14", 100, 103, 99, 102), day("2025-07-15", 102, 103, 101, 101))
    S = sessions(df, ES)
    assert list(S.columns[:6]) == ["full", "O", "H", "L", "C", "t_open"] and S["full"].all()
    sig = signals(S)
    assert np.isclose(sig["asym"].iloc[0], np.log(1.03) + np.log(0.99))  # > 0 : hausse dominante
    assert np.isclose(sig["asym_prevC"].iloc[1], np.log(103 / 102) + np.log(101 / 102))


def test_trade_uses_next_day_open_to_close_and_contrarian_sign():
    df = frame(day("2025-07-14", 100, 103, 99, 102), day("2025-07-15", 102, 103, 101, 101))
    F = next_day_frame(sessions(df, ES), ES, df)
    T = trades(F, "asym")
    assert len(T) == 1 and T["dir"].iloc[0] == -1  # asym > 0 → short le 15
    assert T["date"].iloc[0] == pd.Timestamp("2025-07-15")
    assert np.isclose(T["gross"].iloc[0], -(101 / 102 - 1))
    assert trades(F, "asym_long").empty and len(trades(F, "asym_short")) == 1


def test_half_day_excluded_as_signal_and_trade_day():
    half = day("2025-07-03", 100, 101, 99, 100, b="12:59")  # pas de barre à 15:59
    df = frame(day("2025-07-02", 100, 102, 98, 101), half, day("2025-07-07", 100, 102, 98, 101))
    F = next_day_frame(sessions(df, ES), ES, df)
    assert F.empty


def test_vectorbt_matches_arithmetic_per_trade():
    df = frame(day("2025-07-14", 100, 103, 99, 102), day("2025-07-15", 102, 103, 101, 101),
               day("2025-07-16", 101, 101.5, 98, 99), day("2025-07-17", 99, 100, 98, 100))
    F = next_day_frame(sessions(df, ES), ES, df)
    T = trades(F, "asym")
    pf = simulate(T, 2.0)
    cal = pd.DatetimeIndex(T["date"])
    r = daily_returns(pf, T, cal)
    # écart de l'ordre de coût × rendement : vbt prélève le demi-coût de sortie sur la valeur de sortie
    assert np.allclose(r.values, net_returns(T, 2.0), atol=1e-5)
