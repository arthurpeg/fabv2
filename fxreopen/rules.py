"""Événements de reprise (18:00 ET), gaps intrajournaliers et trades de fade.

Tout trade porte : paire, date de séance (date ET du début de séance, 18:00),
horodatages d'entrée et de sortie, prix, gap (pips), sens (= −signe du gap) et
P&L brut en pips. Les coûts s'appliquent ensuite (`fxreopen.evaluate`).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from fxreopen.data import NY, PAIRS, crosses_roll, last_close_before, ny_wall, price_at, roll_midnights

MIN = pd.Timedelta(minutes=1).value
HALT = pd.Timedelta(minutes=61).value  # dernière barre 16:59 → reprise 18:00


def reopen_events(df: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par reprise : première barre dans [18:00, 18:05) ET après une pause
    d'au moins 60 minutes (week-end et fermetures anticipées inclus)."""
    idx = df.index.as_unit("ns").asi8
    et = df.index.tz_convert(NY)
    mins = et.hour * 60 + et.minute
    dt = np.r_[np.iinfo(np.int64).max, np.diff(idx)]
    m = (dt >= HALT) & (mins >= 18 * 60) & (mins < 18 * 60 + 5)
    pos = np.flatnonzero(m)
    return pd.DataFrame({
        "date": et[pos].tz_localize(None).normalize(),
        "t_prev": idx[pos - 1],
        "t_reopen": idx[pos],
        "p_prev": df["close"].values[pos - 1],
        "p_reopen": df["open"].values[pos],
    })


def _finish(pair: str, ev: pd.DataFrame, t_in, p_in, t_out, p_out, mids) -> pd.DataFrame:
    pip = PAIRS[pair].pip
    gap = (ev["p_reopen"].values - ev["p_prev"].values) / pip if "p_reopen" in ev else ev["gap"].values
    out = pd.DataFrame({
        "pair": pair, "date": ev["date"].values, "t_prev": ev["t_prev"].values,
        "t_in": t_in, "t_out": t_out, "p_in": p_in, "p_out": p_out, "gap": np.round(gap, 6),
    })
    out["dir"] = -np.sign(out["gap"])
    ok = (np.isfinite(p_in) & np.isfinite(p_out) & (t_in > 0) & (t_out > t_in) & (out["dir"] != 0)
          & ~crosses_roll(out["t_prev"].values, t_out, mids))
    out = out[ok].reset_index(drop=True)
    out["gross"] = out["dir"] * (out["p_out"] - out["p_in"]) / pip
    return out


def reopen_trades(pair: str, df: pd.DataFrame, entry_min: int, hold: str = "1h") -> pd.DataFrame:
    """Fade de chaque reprise (sans seuil : le seuil se filtre sur |gap| ensuite).
    entry_min = 0 : entrée à l'open de la barre de reprise. Sinon : open de la première
    barre dans [18:00 + entry_min, +5 min), jamais la barre de reprise elle-même.
    hold = "1h" : sortie à l'open de la première barre dans [entrée nominale + 60 min, +5) ;
    hold = "close" : close de la dernière barre dans [16:55, 17:00) ET le lendemain."""
    ev = reopen_events(df)
    dates = pd.DatetimeIndex(ev["date"])
    mids = roll_midnights(df)
    if entry_min == 0:
        T_in = ev["t_reopen"].values
        t_in, p_in = T_in, ev["p_reopen"].values
    else:
        T_in = ny_wall(dates, "18:00") + entry_min * MIN
        T_in = np.maximum(T_in, ev["t_reopen"].values + MIN)
        p_in, t_in = price_at(df, T_in)
    if hold == "1h":
        T_nom = np.maximum(ny_wall(dates, "18:00") + entry_min * MIN, T_in)
        p_out, t_out = price_at(df, T_nom + 60 * MIN)
    elif hold == "close":
        p_out, t_out = last_close_before(df, ny_wall(dates, "17:00", day_offset=1))
        t_out = np.where(t_out > 0, t_out + MIN, -1)  # close de la barre = fin de minute
    else:
        raise ValueError(hold)
    return _finish(pair, ev, t_in, p_in, t_out, p_out, mids)


def intraday_trades(pair: str, df: pd.DataFrame) -> pd.DataFrame:
    """Fade à chaque frontière HH:00 ET hors 17:00 (pause) et 18:00 (reprise) : barre à
    HH:00 exactement, barre précédente au plus 5 minutes avant. Sortie à l'open de
    HH+1:00 (première barre dans 5 min), ou au close de la dernière barre avant 17:00
    pour la frontière de 16:00."""
    idx = df.index.as_unit("ns").asi8
    et = df.index.tz_convert(NY)
    dt = np.r_[np.iinfo(np.int64).max, np.diff(idx)]
    m = (et.minute == 0) & ~np.isin(et.hour, (17, 18)) & (dt <= 5 * MIN)
    pos = np.flatnonzero(m)
    hours = et.hour[pos]
    local = et[pos].tz_localize(None)
    sess = local.normalize() - pd.to_timedelta(np.where(hours < 18, 1, 0), unit="D")
    pip = PAIRS[pair].pip
    ev = pd.DataFrame({
        "date": sess, "t_prev": idx[pos - 1],
        "gap": (df["open"].values[pos] - df["close"].values[pos - 1]) / pip,
        "hour": hours,
    })
    t_in, p_in = idx[pos], df["open"].values[pos]
    p_out, t_out = price_at(df, t_in + 60 * MIN)
    last16 = hours == 16
    if last16.any():
        T17 = ny_wall(pd.DatetimeIndex(local[last16]).normalize(), "17:00")
        pc, tc = last_close_before(df, T17)
        p_out[last16], t_out[last16] = pc, np.where(tc > 0, tc + MIN, -1)
    out = _finish(pair, ev, t_in, p_in, t_out, p_out, roll_midnights(df))
    return out
