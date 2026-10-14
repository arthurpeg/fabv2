"""Sessions, jours fériés et instants de décision, en UTC.

Les écarts horaires entre places bougent deux fois par an, et pas aux mêmes
dates (États-Unis, Europe, Australie). On ne manipule donc jamais d'écart fixe :
toute heure locale est convertie en UTC date par date via `tz_localize`.
"""

from __future__ import annotations

from functools import lru_cache

import exchange_calendars as xc
import numpy as np
import pandas as pd


@lru_cache(maxsize=None)
def schedule(cal: str, start: str, end: str) -> pd.DataFrame:
    """Séances (index = date de séance, naïf) avec open/close en UTC."""
    return xc.get_calendar(cal, start=start, end=end).schedule


def wall_to_utc(dates: pd.DatetimeIndex, hhmm: str, tz: str) -> pd.DatetimeIndex:
    """Heure murale `hhmm` du fuseau `tz` à chaque date → instant UTC."""
    h, m = map(int, hhmm.split(":"))
    wall = pd.DatetimeIndex(dates).normalize() + pd.Timedelta(hours=h, minutes=m)
    return wall.tz_localize(tz, ambiguous="raise", nonexistent="raise").tz_convert("UTC")


def utc_on(dates: pd.DatetimeIndex, hhmm: str) -> pd.DatetimeIndex:
    """Heure UTC fixe `hhmm` à chaque date."""
    return wall_to_utc(dates, hhmm, "UTC")


def target_days(cfg: dict) -> pd.DataFrame:
    """Jours cibles D (séances XETR) avec la séance Xetra précédente et t_decision.

    Colonnes : `prev` (date Xetra précédente), `t_decision` (UTC).
    """
    d, t = cfg["data"], cfg["timing"]
    pad_start = (pd.Timestamp(d["start"]) - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    xetr = schedule("XETR", pad_start, d["end"]).index
    prev = pd.Series(xetr, index=xetr).shift(1)
    days = xetr[(xetr >= d["start"]) & (xetr <= d["end"])]
    out = pd.DataFrame({"prev": prev.reindex(days).values}, index=days)
    out["t_decision"] = wall_to_utc(days, t["decision"], t["target_tz"])
    return out.dropna(subset=["prev"])


def market_window(cfg: dict, name: str, days: pd.DataFrame) -> pd.DataFrame:
    """Fenêtre de la courbe d'un marché pour chaque jour cible.

    Colonnes : `session` (date de séance du marché), `start`, `end` (UTC),
    `ok` (séance ouverte, non écourtée avant la fin de la fenêtre).
    """
    m = cfg["markets"][name]
    d = cfg["data"]
    session = pd.DatetimeIndex(days["prev"] if m.get("previous_day") else days.index)
    pad = (pd.Timestamp(d["start"]) - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    sch = schedule(m["calendar"], pad, d["end"])
    start = wall_to_utc(session, m["start"], m["tz"])
    end = utc_on(session, m["end_utc"]) if "end_utc" in m else wall_to_utc(session, m["end"], m["tz"])
    is_sess = session.isin(sch.index)
    close = sch["close"].reindex(session)
    # séance écourtée : la clôture officielle tombe avant la fin de notre fenêtre
    ok = is_sess & ~(close.values < end.values)
    return pd.DataFrame({"session": session, "start": start, "end": end, "ok": ok}, index=days.index)


def third_fridays(start: str, end: str, months=(3, 6, 9, 12)) -> pd.DatetimeIndex:
    """3e vendredi des mois d'échéance : jour de bascule du FDAX continu `.v.0`."""
    m = pd.date_range(start, end, freq="MS")
    m = m[m.month.isin(months)]
    first_fri = m + pd.to_timedelta((4 - m.dayofweek) % 7, unit="D")
    return pd.DatetimeIndex(first_fri + pd.Timedelta(days=14))
