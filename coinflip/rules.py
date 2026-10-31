"""Entrées, ATR M15 et premier contact stop / objectif, communs aux runners pile ou face.

- ATR : barres 15 min (frontières :00/:15/:30/:45) ou 1 h, ATR de Wilder sur 14
  barres, lu sur la dernière barre terminée à 01:00 Paris (00:45–01:00 en M15,
  00:00–01:00 en H1).
- Entrée : open de la première barre 1 min dans [01:00, 01:05) Paris, lundi–vendredi.
- Sortie : premier contact du stop ou de l'objectif, à partir de la barre suivante
  (convention vectorbt).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

TZ = "Europe/Paris"
ENTRY = (1, 0)  # 01:00 Paris
SLACK = 5
ATR_N = 14


def atr_tf(df: pd.DataFrame, freq: str = "15min") -> pd.Series:
    """ATR de Wilder sur barres `freq` (15min, 1h…), indexé par l'heure de FIN de barre."""
    b = df.resample(freq, label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    pc = b.close.shift()
    tr = pd.concat([b.high - b.low, (b.high - pc).abs(), (b.low - pc).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / ATR_N, adjust=False, min_periods=ATR_N).mean()
    atr.index = atr.index + pd.Timedelta(freq)
    return atr


def entry_bars(df: pd.DataFrame) -> np.ndarray:
    """Positions des barres d'entrée : première barre dans [01:00, 01:05) Paris, en semaine."""
    loc = df.index.tz_convert(TZ)
    mins = loc.hour * 60 + loc.minute
    t0 = ENTRY[0] * 60 + ENTRY[1]
    ok = (mins >= t0) & (mins < t0 + SLACK) & (loc.dayofweek < 5)
    pos = np.flatnonzero(ok)
    day = loc[pos].normalize()
    first = ~pd.Index(day).duplicated()
    return pos[first]


def entries_with_atr(df: pd.DataFrame, freq: str = "15min") -> tuple[np.ndarray, np.ndarray]:
    """Barres d'entrée et ATR `freq` de la dernière barre terminée à l'entrée
    (jours sans ATR retirés)."""
    pos = entry_bars(df)
    a = atr_tf(df, freq).reindex(df.index[pos].floor(freq), method="ffill").to_numpy()
    keep = ~np.isnan(a)
    return pos[keep], a[keep]


def first_touch(H: np.ndarray, L: np.ndarray, i0: int, up: float, dn: float) -> tuple[int, int]:
    """Première barre après i0 qui touche up ou dn. Retourne (barre, code) :
    code 1 = up seul, -1 = dn seul, 0 = les deux dans la même barre ; (-1, 0) si jamais."""
    i = i0 + 1
    n = len(H)
    step = 512
    while i < n:
        h, lo = H[i:i + step], L[i:i + step]
        hu, hd = h >= up, lo <= dn
        any_ = hu | hd
        if any_.any():
            k = int(np.argmax(any_))
            return i + k, (1 if not hd[k] else -1 if not hu[k] else 0)
        i += step
    return -1, 0
