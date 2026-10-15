"""Reprise CME de 18:00 ET, heure d'été, roulements, inversion de 6J et règles de
fade, sur des barres construites à la main."""

import numpy as np
import pandas as pd

from fxreopen.data import PAIRS, crosses_roll, prepare, roll_midnights
from fxreopen.evaluate import permutation_p, with_cost
from fxreopen.rules import intraday_trades, reopen_events, reopen_trades

U = lambda s: pd.Timestamp(s, tz="UTC")  # noqa: E731


def bars(spec: dict[str, float]) -> pd.DataFrame:
    """{horodatage UTC: prix} → barres plates (open = high = low = close)."""
    idx = pd.DatetimeIndex([U(k) for k in spec])
    v = np.array(list(spec.values()))
    return pd.DataFrame({"open": v, "high": v, "low": v, "close": v, "volume": 1.0}, index=idx)


def session(day_utc: str, offset_h: int, prev: float, reopen: float, path: dict[int, float]) -> dict:
    """Clôture 16:59 ET, reprise 18:00 ET, puis minutes `path` (minutes après 18:00).
    offset_h = 4 en heure d'été américaine, 5 en hiver."""
    d = pd.Timestamp(day_utc, tz="UTC")
    t1659 = d + pd.Timedelta(hours=16 + offset_h, minutes=59)
    t1800 = d + pd.Timedelta(hours=18 + offset_h)
    out = {str(t1659): prev, str(t1800): reopen}
    for k, px in path.items():
        out[str(t1800 + pd.Timedelta(minutes=k))] = px
    return out


def test_reopen_is_1800_et_in_summer_and_winter():
    df = bars({**session("2025-07-15", 4, 1.1000, 1.1010, {1: 1.1008}),
               **session("2025-01-15", 5, 1.0300, 1.0290, {1: 1.0292})})
    ev = reopen_events(df.sort_index())
    got = pd.to_datetime(ev["t_reopen"], utc=True).dt.strftime("%m-%d %H:%M").tolist()
    assert got == ["01-15 23:00", "07-15 22:00"]  # 18:00 ET = 23:00 UTC l'hiver, 22:00 l'été


def test_us_dst_week_not_european():
    # 2026-03-10 : États-Unis passés à l'heure d'été le 8 mars, pas l'Europe → reprise 22:00 UTC
    df = bars(session("2026-03-10", 4, 1.0, 1.0, {}))
    ev = reopen_events(df)
    assert pd.Timestamp(ev["t_reopen"].iloc[0], tz="UTC") == U("2026-03-10 22:00")


def test_bar_at_1800_without_halt_is_not_a_reopen():
    df = bars({"2025-07-15 21:58": 1.0, "2025-07-15 21:59": 1.0, "2025-07-15 22:00": 1.001})
    assert reopen_events(df).empty


def test_fade_direction_and_entries():
    # gap haussier de +10 pips, puis retour : E0 vend à 1.1010, E1 vend à l'open de 18:01
    path = {1: 1.1008, 5: 1.1006, 15: 1.1004, 60: 1.1001, 61: 1.1000, 65: 1.0999, 75: 1.0998}
    df = bars(session("2025-07-15", 4, 1.1000, 1.1010, path))
    t0 = reopen_trades("6E", df, 0)
    assert t0["gap"].iloc[0] == 10 and t0["dir"].iloc[0] == -1
    assert np.isclose(t0["gross"].iloc[0], 9.0)  # 1.1010 → 1.1001 (open de 19:00)
    t1 = reopen_trades("6E", df, 1)
    assert np.isclose(t1["p_in"].iloc[0], 1.1008) and np.isclose(t1["gross"].iloc[0], 8.0)
    t15 = reopen_trades("6E", df, 15)
    assert np.isclose(t15["gross"].iloc[0], 6.0)  # 1.1004 → 1.0998 (19:15)


def test_delayed_entry_never_reuses_reopen_bar():
    # pas d'échange avant 18:02 : la reprise est à 18:02, E1 doit prendre la barre suivante
    d0 = U("2025-07-15 22:02")
    df = bars({"2025-07-15 20:59": 1.1000, str(d0): 1.1010, "2025-07-15 22:03": 1.1007,
               "2025-07-15 23:03": 1.1001})
    t1 = reopen_trades("6E", df, 1)
    assert pd.Timestamp(t1["t_in"].iloc[0], tz="UTC") == U("2025-07-15 22:03")


def test_hold_to_close_uses_next_day_1659():
    path = {60: 1.1001}
    s = session("2025-07-15", 4, 1.1000, 1.1010, path)
    s["2025-07-16 20:59"] = 1.0990  # 16:59 ET le lendemain
    t = reopen_trades("6E", bars(s), 0, hold="close")
    assert np.isclose(t["gross"].iloc[0], 20.0)


def test_roll_midnight_excludes_crossing_trades():
    # hiver : 18:15 ET = 23:15 UTC, sortie 19:15 ET = 00:15 UTC → traverse 00:00 UTC
    s = session("2025-12-15", 5, 1.1000, 1.1010, {15: 1.1004, 60: 1.1001, 75: 1.2000})
    s["2025-12-16 00:00"] = 1.2000  # bascule de contrat
    df = bars(s)
    # E0 sort à l'open de 00:00 UTC, c.-à-d. sur le nouveau contrat : exclu aussi
    assert reopen_trades("6E", df, 0).empty
    assert reopen_trades("6E", df, 15).empty
    mids = roll_midnights(df)
    assert crosses_roll(np.array([U("2025-12-15 23:59").value]), np.array([U("2025-12-16 00:00").value]), mids)[0]


def test_same_crossing_outside_roll_window_is_kept():
    s = session("2025-11-17", 5, 1.1000, 1.1010, {15: 1.1004, 75: 1.1000})
    s["2025-11-18 00:00"] = 1.1002
    assert len(reopen_trades("6E", bars(s), 15)) == 1


def test_6j_inversion_swaps_high_low():
    raw = pd.DataFrame({"open": [0.0067], "high": [0.0068], "low": [0.0066], "close": [0.00675], "volume": [1.0]},
                       index=pd.DatetimeIndex([U("2025-07-15 22:00")]))
    p = prepare(raw, inverted=True)
    assert p["high"].iloc[0] == 1 / 0.0066 and p["low"].iloc[0] == 1 / 0.0068
    # coût standard 6J ≈ 2 pips USDJPY à 149
    assert 1.9 < PAIRS["6J"].std_cost_pips(np.array([149.25]))[0] < 2.1


def test_intraday_skips_halt_and_reopen_hours():
    s = session("2025-07-15", 4, 1.1000, 1.1010, {59: 1.1011, 60: 1.1013, 119: 1.1012, 120: 1.1012})
    t = intraday_trades("6E", bars(s))
    # seule la frontière de 19:00 ET (23:00 UTC) est un événement ; 18:00 est la reprise
    assert len(t) == 1 and pd.Timestamp(t["t_in"].iloc[0], tz="UTC") == U("2025-07-15 23:00")
    assert t["gap"].iloc[0] == 2 and t["dir"].iloc[0] == -1


def test_permutation_detects_perfect_fade():
    rng = np.random.default_rng(0)
    n = 400
    move = rng.normal(0, 5, n)
    t = pd.DataFrame({"pair": "6E", "dir": np.sign(move), "gross": np.abs(move), "p_in": 1.1,
                      "date": pd.Timestamp("2020-01-01")})
    t = with_cost(t, 1.0)
    assert permutation_p(t, reps=500) < 0.01
    t["dir"] = rng.choice([-1.0, 1.0], n)
    t["gross"] = t["dir"] * move
    assert permutation_p(with_cost(t, 1.0), reps=500) > 0.01
