"""Fuseaux, changements d'heure et sessions. Aucune donnée de marché : seulement
des calendriers et des horodatages construits à la main."""

import numpy as np
import pandas as pd
import pytest

from gap import load_config
from gap.calendar import market_window, target_days, third_fridays, wall_to_utc
from gap.data import histdata_to_utc

CFG = load_config()
U = lambda s: pd.Timestamp(s, tz="UTC")  # noqa: E731


def test_histdata_follows_european_dst():
    # ouverture des futures de Hong Kong, 09:15 HKT = 01:15 UTC toute l'année ;
    # l'heure brute HistData passe de 20:15 à 21:15 aux dates européennes
    raw = pd.Series(["20250327 201500", "20250331 211500", "20251024 211500", "20251027 201500",
                     "20260310 201500"])  # 2026-03-10 : US déjà en heure d'été, pas l'Europe
    got = histdata_to_utc(raw)
    assert (got.strftime("%H:%M") == "01:15").all()


def test_histdata_naive_fixed_est_would_be_wrong_in_summer():
    raw = pd.Series(["20250701 211500"])
    naive = pd.to_datetime(raw) + pd.Timedelta(hours=5)  # lecture de la FAQ
    assert naive.dt.strftime("%H:%M").iloc[0] == "02:15"  # une heure trop tard
    assert histdata_to_utc(raw)[0] == U("2025-07-02 01:15")


@pytest.mark.parametrize("day,expected", [
    ("2025-01-15", "07:55"), ("2025-07-15", "06:55"),
    ("2026-03-27", "07:55"),  # vendredi avant le passage européen (29 mars)
    ("2026-03-30", "06:55"),  # lundi après
    ("2025-10-24", "06:55"), ("2025-10-27", "07:55"),
])
def test_t_decision_across_dst(day, expected):
    d = target_days(CFG)
    assert d.loc[day, "t_decision"].strftime("%H:%M") == expected


def test_us_close_moves_with_us_dst_not_european():
    d = target_days(CFG)
    w = market_window(CFG, "SP500", d)
    # cible 2026-03-13 : veille 03-12, États-Unis en heure d'été depuis le 8 mars, Europe pas encore
    assert w.loc["2026-03-13", "end"] == U("2026-03-12 20:00")
    assert w.loc["2026-02-13", "end"] == U("2026-02-12 21:00")
    # écart clôture US → décision : 11 h 55 cette semaine-là, 10 h 55 l'été, 10 h 55 l'hiver
    gap_mar = d.loc["2026-03-13", "t_decision"] - w.loc["2026-03-13", "end"]
    gap_feb = d.loc["2026-02-13", "t_decision"] - w.loc["2026-02-13", "end"]
    assert gap_mar - gap_feb == pd.Timedelta(hours=1)


def test_asx_window_follows_sydney_dst():
    d = target_days(CFG)
    w = market_window(CFG, "ASX", d)
    assert w.loc["2025-01-15", "start"] == U("2025-01-14 23:00")  # AEDT
    assert w.loc["2025-07-15", "start"] == U("2025-07-15 00:00")  # AEST


def test_all_curve_windows_end_before_decision():
    d = target_days(CFG)
    for m in CFG["markets"]:
        w = market_window(CFG, m, d)
        assert (w["end"] <= d["t_decision"]).all(), m


def test_holidays_and_early_closes_flagged():
    d = target_days(CFG)
    us = market_window(CFG, "SP500", d)
    assert not us.loc["2025-12-01", "ok"]  # veille = 2025-11-28, NYSE ferme à 13:00
    jp = market_window(CFG, "NIKKEI", d)
    assert not jp.loc["2025-01-02", "ok"]  # Tokyo fermé
    assert not jp.loc["2025-05-05", "ok"]  # Golden Week


def test_nikkei_window_fits_old_tse_hours():
    d = target_days(CFG)
    jp = market_window(CFG, "NIKKEI", d)
    assert jp.loc["2019-06-12", "ok"]  # avant 2024-11, la TSE fermait à 15:00


def test_wall_to_utc_rejects_nonexistent_time():
    with pytest.raises(Exception):
        wall_to_utc(pd.DatetimeIndex(["2025-03-30"]), "02:30", "Europe/Berlin")


def test_third_fridays():
    tf = third_fridays("2025-01-01", "2025-12-31")
    assert list(tf.strftime("%Y-%m-%d")) == ["2025-03-21", "2025-06-20", "2025-09-19", "2025-12-19"]
    assert (tf.dayofweek == 4).all()
