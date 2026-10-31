"""Bibliothèque de journées NQ pour un trade intraday au hasard (PREREGISTRATION_18).

Pour chaque séance NYSE : entrée à l'open de la première barre >= 9:35 ET, sortie au plus
tard à la clôture de la dernière barre démarrant <= 15:54 ET (13:00 en demi-séance).
Pour chaque sens et chaque distance de stop s (fraction du prix) on garde, en minutes
depuis l'entrée : la barre où le stop est touché, la barre où chaque niveau d'objectif
k * s est touché (k = 0,05, 0,10, … en R), le R réellement perdu au stop (pire de stop
et open de la barre) et le R de sortie en fin de journée.

Pas d'ajustement de roulement : tout se passe dans la séance et les roulements .v.0
tombent à 00:00 UTC.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd

DATA = Path("D:/quant-data/Cotations/indices")
NY = "America/New_York"
END = pd.Timestamp("2026-08-28")  # holdout après cette date
K_STEP = 0.05
K_N = 120  # niveaux d'objectif jusqu'à 6 R
NEVER = np.iinfo(np.int16).max


@dataclass
class DayLib:
    """Issues d'un trade par jour ; tableaux indexés [jour, sens (0 long, 1 short), ...]."""
    dates: pd.DatetimeIndex
    s: float
    tp_bar: np.ndarray    # [jour, sens, K_N] int16, NEVER si jamais touché
    stop_bar: np.ndarray  # [jour, sens] int16
    stop_R: np.ndarray    # [jour, sens] R perdu au stop (>= 1)
    eod_R: np.ndarray     # [jour, sens] R à la clôture de sortie

    @property
    def n(self) -> int:
        return len(self.dates)


def session_bars(name: str = "NQ") -> dict[pd.Timestamp, pd.DataFrame]:
    """Barres 1 min de chaque séance NYSE, de 9:35 ET à la dernière barre <= clôture - 6 min."""
    df = pd.read_parquet(DATA / f"{name}_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    loc = df.index.tz_convert(NY)
    sched = xc.get_calendar("XNYS").schedule.loc["2016-01-04":END.strftime("%Y-%m-%d")]
    out = {}
    day = loc.normalize().tz_localize(None)
    groups = pd.Series(np.arange(len(df)), index=day).groupby(level=0)
    for d, row in sched.iterrows():
        d = pd.Timestamp(d)
        if d not in groups.groups:
            continue
        ix = groups.get_group(d).to_numpy()
        t0 = pd.Timestamp(d.strftime("%Y-%m-%d") + " 09:35", tz=NY)
        t1 = row["close"].tz_convert(NY) - pd.Timedelta(minutes=6)
        sel = ix[(loc[ix] >= t0) & (loc[ix] <= t1)]
        if len(sel) < 60 or loc[sel[0]] > t0 + pd.Timedelta(minutes=5):
            continue  # trou de données
        out[d] = df.iloc[sel][["open", "high", "low", "close"]]
    return out


def _one_side(e: float, O, H, L, C, s: float, sign: int, levels: np.ndarray):
    if sign > 0:
        fav, adv, fill_adv, end = (H - e) / e, (e - L) / e, (e - O) / e, (C[-1] - e) / e
    else:
        fav, adv, fill_adv, end = (e - L) / e, (H - e) / e, (O - e) / e, (e - C[-1]) / e
    hit = np.flatnonzero(adv >= s)
    if len(hit):
        j = int(hit[0])
        stop_bar, stop_R = j, max(1.0, fill_adv[j] / s)
    else:
        stop_bar, stop_R = NEVER, 1.0
    tp = np.searchsorted(np.maximum.accumulate(fav), levels * s, side="left")
    tp = np.where(tp >= len(fav), NEVER, tp)
    return tp.astype(np.int16), stop_bar, stop_R, end / s


def build(bars: dict[pd.Timestamp, pd.DataFrame], s: float) -> DayLib:
    levels = K_STEP * np.arange(1, K_N + 1)
    dates = sorted(bars)
    n = len(dates)
    tp = np.empty((n, 2, K_N), np.int16)
    sb = np.empty((n, 2), np.int16)
    sr = np.empty((n, 2))
    er = np.empty((n, 2))
    for i, d in enumerate(dates):
        b = bars[d]
        O, H, L, C = (b[c].to_numpy() for c in ("open", "high", "low", "close"))
        e = O[0]
        for k, sign in enumerate((1, -1)):
            tp[i, k], sb[i, k], sr[i, k], er[i, k] = _one_side(e, O, H, L, C, s, sign, levels)
    return DayLib(pd.DatetimeIndex(dates), s, tp, sb, sr, er)
