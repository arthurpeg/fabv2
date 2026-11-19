"""Fix de 16h Londres : heure d'été britannique, fin de mois, sens des règles A et B,
roulements et clôtures d'indices, sur des barres construites à la main."""

import numpy as np
import pandas as pd

from fxfix.rules import LDN, daily_closes, fix_days, flow_trades, month_to_date, reversal_trades, wall

U = lambda s: pd.Timestamp(s, tz="UTC")  # noqa: E731


def bars(spec: dict) -> pd.DataFrame:
    idx = pd.DatetimeIndex([U(k) if isinstance(k, str) else k for k in spec])
    v = np.array(list(spec.values()), float)
    df = pd.DataFrame({"open": v, "high": v, "low": v, "close": v, "volume": 1.0}, index=idx)
    return df.sort_index()


def ldn(day: str, hhmm: str) -> pd.Timestamp:
    return pd.Timestamp(f"{day} {hhmm}").tz_localize(LDN).tz_convert("UTC")


def fix_session(day: str, p15: float, p16: float, p_in: float, next_day: str, p_noon: float) -> dict:
    return {ldn(day, "15:00"): p15, ldn(day, "16:00"): p16, ldn(day, "16:01"): p16,
            ldn(day, "16:05"): p_in, ldn(next_day, "12:00"): p_noon}


def test_fix_is_1600_london_in_bst_and_gmt():
    assert pd.Timestamp(wall(pd.DatetimeIndex(["2025-01-15"]), "16:00", LDN)[0], tz="UTC") == U("2025-01-15 16:00")
    assert pd.Timestamp(wall(pd.DatetimeIndex(["2025-07-15"]), "16:00", LDN)[0], tz="UTC") == U("2025-07-15 15:00")
    # 2026-03-10 : États-Unis à l'heure d'été, pas le Royaume-Uni → 16:00 UTC
    assert pd.Timestamp(wall(pd.DatetimeIndex(["2026-03-10"]), "16:00", LDN)[0], tz="UTC") == U("2026-03-10 16:00")


def test_month_end_is_last_fix_day_of_month():
    df = bars({**fix_session("2025-07-30", 1, 1, 1, "2025-07-31", 1),
               **fix_session("2025-07-31", 1, 1, 1, "2025-08-01", 1),
               **fix_session("2025-08-01", 1, 1, 1, "2025-08-04", 1)})
    fd = fix_days(df).set_index("date")
    assert list(fd["eom"]) == [False, True, False]  # août est le dernier mois des données : incomplet
    assert fd.loc["2025-08-01", "next"] == pd.Timestamp("2025-08-04")


def test_reversal_direction_entries_and_exit():
    # +10 pips de 15:00 à 16:00 → vente ; E5 vend à 1.1008, sortie à midi le lendemain à 1.1001
    df = bars({**fix_session("2025-07-31", 1.1000, 1.1010, 1.1008, "2025-08-01", 1.1001),
               ldn("2025-08-01", "16:00"): 1.1001})  # août présent → juillet complet
    t5 = reversal_trades("6E", df, 5)
    t5 = t5[t5["date"] == "2025-07-31"]
    assert len(t5) == 1 and t5["dir"].iloc[0] == -1 and np.isclose(t5["m"].iloc[0], 10)
    assert np.isclose(t5["gross"].iloc[0], 7.0)
    t0 = reversal_trades("6E", df, 0).iloc[:1]
    assert np.isclose(t0["p_in"].iloc[0], 1.1010) and np.isclose(t0["gross"].iloc[0], 9.0)
    assert bool(t5["eom"].iloc[0])


def test_reversal_skips_roll_window_crossing():
    # fix le 2025-03-13, sortie le 14 à midi : traverse 00:00 UTC du 14 mars (fenêtre 8-21)
    s = fix_session("2025-03-13", 1.1, 1.101, 1.1008, "2025-03-14", 1.1)
    s[U("2025-03-14 00:00")] = 1.1
    assert reversal_trades("6E", bars(s), 5).empty
    # même chose le 31 mars → 1er avril : hors fenêtre, gardé
    s = fix_session("2025-03-31", 1.1, 1.101, 1.1008, "2025-04-01", 1.1)
    s[U("2025-04-01 00:00")] = 1.1
    assert len(reversal_trades("6E", bars(s), 5)) == 1


def test_daily_close_takes_last_bar_before_local_close():
    eq = pd.DataFrame({"close": [100.0, 101.0, 999.0]},
                      index=pd.DatetimeIndex([U("2025-07-15 15:25"), U("2025-07-15 15:29"), U("2025-07-15 15:31")]))
    c = daily_closes(eq, "Europe/Berlin", "17:30")  # 17:30 Berlin (été) = 15:30 UTC
    assert c.iloc[0] == 101.0


def test_month_to_date_uses_previous_month_end_and_day_before():
    closes = pd.Series([100.0, 110.0, 121.0, 500.0],
                       index=pd.DatetimeIndex([U("2025-06-30 20:00"), U("2025-07-15 20:00"),
                                               U("2025-07-30 20:00"), U("2025-07-31 20:00")]))
    r = month_to_date(closes, pd.DatetimeIndex(["2025-07-31"]), wall(pd.DatetimeIndex(["2025-07-31"]), "00:00", LDN))
    assert np.isclose(r[0], 0.21)  # 100 → 121, la clôture du jour J (500) est ignorée


def _flow_setup(cty_ret: float, us_ret: float):
    df = bars({ldn("2025-07-31", "13:00"): 1.1000, ldn("2025-07-31", "16:00"): 1.0990,
               ldn("2025-07-31", "15:00"): 1.0995})
    t = lambda d: U(d + " 20:00")  # noqa: E731
    us = pd.Series([100.0, 100 * (1 + us_ret)], index=pd.DatetimeIndex([t("2025-06-30"), t("2025-07-30")]))
    cty = pd.Series([100.0, 100 * (1 + cty_ret)], index=pd.DatetimeIndex([t("2025-06-30"), t("2025-07-30")]))
    return df, us, cty


def test_flow_sells_currency_of_outperforming_market():
    df, us, cty = _flow_setup(0.05, 0.01)  # actions du pays devant → vendre la devise (XXXUSD court)
    t = flow_trades("6E", df, "16:00", us, cty)
    assert t["dir"].iloc[0] == -1 and np.isclose(t["gross"].iloc[0], 10.0)
    tj = flow_trades("6J", df, "16:00", us, cty)  # USDJPY : le Japon devant → acheter USDJPY
    assert tj["dir"].iloc[0] == 1


def test_flow_excluded_month_for_6e():
    df = bars({ldn("2023-12-29", "13:00"): 1.1, ldn("2023-12-29", "16:00"): 1.1})
    us = pd.Series([100.0, 101.0], index=pd.DatetimeIndex([U("2023-11-30 21:00"), U("2023-12-28 21:00")]))
    assert flow_trades("6E", df, "16:00", us, us * 2).empty
