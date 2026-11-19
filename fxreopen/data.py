"""Futures FX CME 1 minute (Databento) : chargement, inversion de 6J, fenêtres de
roulement et prix à un instant donné. Voir PREREGISTRATION_6.md.

Conventions :
- index UTC ; les heures de règle sont en America/New_York (le CME suit l'heure
  d'été américaine : reprise à 18:00 ET toute l'année) ;
- prix à l'instant T = open de la première barre dans [T, T + 5 min) ;
- 6J (USD par JPY) est inversé pour travailler en USDJPY (high et low permutés).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path("D:/quant-data/Cotations/forex")
NY = "America/New_York"
SLACK = pd.Timedelta(minutes=5)
ROLL_MONTHS = (3, 6, 9, 12)
ROLL_LAST_DAY = 21


@dataclass(frozen=True)
class Pair:
    future: str
    name: str
    pip: float
    tick: float  # en unités du future (non inversé)
    point_value: float
    inverted: bool

    def std_cost_pips(self, px: np.ndarray) -> np.ndarray:
        """Coût standard du dépôt (1 tick + 5 $ aller-retour), en pips de la paire.
        `px` = prix de la paire (déjà inversé pour 6J)."""
        cost_fut = self.tick + 5.0 / self.point_value
        if self.inverted:  # d(1/p) = dp / p² ; p_fut = 1 / px
            return cost_fut * px**2 / self.pip
        return np.full(len(px), cost_fut / self.pip)


PAIRS = {
    p.future: p
    for p in [
        Pair("6E", "EURUSD", 0.0001, 0.00005, 125_000, False),
        Pair("6B", "GBPUSD", 0.0001, 0.0001, 62_500, False),
        Pair("6A", "AUDUSD", 0.0001, 0.00005, 100_000, False),
        Pair("6J", "USDJPY", 0.01, 0.0000005, 12_500_000, True),
    ]
}


def prepare(df: pd.DataFrame, inverted: bool) -> pd.DataFrame:
    df = df[~df.index.duplicated()].sort_index()[["open", "high", "low", "close", "volume"]]
    if inverted:
        df = pd.DataFrame(
            {"open": 1 / df["open"], "high": 1 / df["low"], "low": 1 / df["high"],
             "close": 1 / df["close"], "volume": df["volume"]},
            index=df.index,
        )
    return df


@lru_cache(maxsize=None)
def load(future: str) -> pd.DataFrame:
    """Barres 1 minute brutes (non ajustées), index UTC."""
    df = pd.read_parquet(DATA_DIR / f"{future}_v0_1m.parquet")
    return prepare(df, PAIRS[future].inverted)


def is_roll_window(ts_utc: pd.DatetimeIndex) -> np.ndarray:
    return np.isin(ts_utc.month, ROLL_MONTHS) & (ts_utc.day <= ROLL_LAST_DAY)


def roll_midnights(df: pd.DataFrame) -> np.ndarray:
    """Barres de 00:00 UTC des fenêtres de roulement (1er-21 des mois trimestriels) :
    instants où le contrat continu peut basculer. int64 ns, triés."""
    idx = df.index
    m = (idx.hour == 0) & (idx.minute == 0) & is_roll_window(idx)
    return idx[m].as_unit("ns").asi8


def crosses_roll(t_a: np.ndarray, t_b: np.ndarray, mids: np.ndarray) -> np.ndarray:
    """True si une barre de 00:00 UTC de roulement M vérifie t_a < M ≤ t_b (int64 ns)."""
    lo = np.searchsorted(mids, t_a, side="right")
    hi = np.searchsorted(mids, t_b, side="right")
    return hi > lo


def midnight_jumps(df: pd.DataFrame, thr: float = 0.0015) -> pd.DataFrame:
    """Sauts |open/close précédent − 1| > thr sur les barres de 00:00 UTC, avec
    l'indicateur « dans une fenêtre de roulement ». Sert au contrôle des roulements."""
    jump = df["open"] / df["close"].shift() - 1
    idx = df.index
    m = (idx.hour == 0) & (idx.minute == 0) & (jump.abs() > thr).values
    return pd.DataFrame({"jump": jump[m], "in_window": is_roll_window(idx[m])})


def price_at(df: pd.DataFrame, t_ns: np.ndarray, col: str = "open") -> tuple[np.ndarray, np.ndarray]:
    """Prix `col` de la première barre dans [T, T + 5 min). Retourne (prix, horodatage ns),
    NaN / -1 si aucune barre."""
    idx = df.index.as_unit("ns").asi8
    pos = np.searchsorted(idx, t_ns, side="left")
    ok = pos < len(idx)
    pos_c = np.minimum(pos, len(idx) - 1)
    ok &= idx[pos_c] < t_ns + SLACK.value
    px = np.where(ok, df[col].values[pos_c], np.nan)
    return px, np.where(ok, idx[pos_c], -1)


def last_close_before(df: pd.DataFrame, t_ns: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Close de la dernière barre commençant dans [T − 5 min, T). NaN / -1 sinon."""
    idx = df.index.as_unit("ns").asi8
    pos = np.searchsorted(idx, t_ns, side="left") - 1
    ok = pos >= 0
    pos_c = np.maximum(pos, 0)
    ok &= idx[pos_c] >= t_ns - SLACK.value
    px = np.where(ok, df["close"].values[pos_c], np.nan)
    return px, np.where(ok, idx[pos_c], -1)


def ny_wall(dates: pd.DatetimeIndex, hhmm: str, day_offset: int = 0) -> np.ndarray:
    """Heure murale de New York `hhmm` aux dates (naïves) + day_offset → UTC ns."""
    h, m = map(int, hhmm.split(":"))
    wall = dates.normalize() + pd.Timedelta(days=day_offset, hours=h, minutes=m)
    return wall.tz_localize(NY, ambiguous="raise", nonexistent="raise").tz_convert("UTC").as_unit("ns").asi8
