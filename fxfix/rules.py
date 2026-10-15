"""Événements du fix de 16h (heure de Londres) et trades des résultats A et B.

Mêmes conventions que `fxreopen` : prix à l'instant T = open de la première barre dans
[T, T + 5 min) ; trades avec paire, date (date de Londres du jour du fix), horodatages et
prix d'entrée et de sortie, sens, P&L brut en pips. Les coûts s'appliquent ensuite
(`fxreopen.evaluate.with_cost`). Voir PREREGISTRATION_7.md.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from fxreopen.data import PAIRS, crosses_roll, last_close_before, price_at

LDN = "Europe/London"
MIN = pd.Timedelta(minutes=1).value
ROLL_FIRST_DAY, ROLL_LAST_DAY = 8, 21
HISTDATA = Path("cache/histdata")
ES_FILE = Path("cache/ES_adj.parquet")  # ES continu ajusté des roulements (rendements mensuels propres)


def wall(dates: pd.DatetimeIndex, hhmm: str, tz: str) -> np.ndarray:
    """Heure murale `hhmm` du fuseau `tz` aux dates (naïves) → UTC ns."""
    h, m = map(int, hhmm.split(":"))
    w = pd.DatetimeIndex(dates).normalize() + pd.Timedelta(hours=h, minutes=m)
    return w.tz_localize(tz, ambiguous="raise", nonexistent="raise").tz_convert("UTC").as_unit("ns").asi8


def roll_midnights(df: pd.DataFrame) -> np.ndarray:
    """Barres de 00:00 UTC du 8 au 21 des mois trimestriels (fenêtre du n° 7)."""
    idx = df.index
    m = ((idx.hour == 0) & (idx.minute == 0) & np.isin(idx.month, (3, 6, 9, 12))
         & (idx.day >= ROLL_FIRST_DAY) & (idx.day <= ROLL_LAST_DAY))
    return idx[m].as_unit("ns").asi8


def london_days(df: pd.DataFrame, hhmm: str) -> pd.DatetimeIndex:
    """Dates de Londres où le future a une barre dans [hhmm, hhmm + 5 min) heure de Londres."""
    loc = df.index.tz_convert(LDN)
    h, m = map(int, hhmm.split(":"))
    mins = loc.hour * 60 + loc.minute
    sel = (mins >= h * 60 + m) & (mins < h * 60 + m + 5)
    return pd.DatetimeIndex(np.unique(loc[sel].tz_localize(None).normalize()))


def fix_days(df: pd.DataFrame) -> pd.DataFrame:
    """Jours de fix (barre à 16:00 Londres), avec l'indicateur de fin de mois (dernier jour
    de fix du mois civil) et le jour suivant ayant une barre à 12:00 Londres."""
    d = london_days(df, "16:00")
    s = pd.Series(d, index=d)
    eom = s.groupby([d.year, d.month]).transform("max").values == d.values
    eom &= d.to_period("M") < d.max().to_period("M")  # mois final des données : fin de mois inconnue
    noon = london_days(df, "12:00")
    pos = np.searchsorted(noon.values, d.values, side="right")
    nxt = pd.Series(pd.NaT, index=range(len(d)), dtype="datetime64[ns]")
    ok = pos < len(noon)
    nxt[ok] = noon.values[pos[ok]]
    return pd.DataFrame({"date": d, "eom": eom, "next": nxt.values})


def _trades(pair: str, df: pd.DataFrame, dates, t_sig, t_in, p_in, t_out, p_out, sign, extra) -> pd.DataFrame:
    pip = PAIRS[pair].pip
    out = pd.DataFrame({"pair": pair, "date": pd.DatetimeIndex(dates), "t_prev": t_sig, "t_in": t_in,
                        "t_out": t_out, "p_in": p_in, "p_out": p_out, "dir": np.sign(sign), **extra})
    ok = (np.isfinite(p_in) & np.isfinite(p_out) & (t_in > 0) & (t_out > t_in) & (out["dir"] != 0)
          & ~crosses_roll(t_sig, t_out, roll_midnights(df)))
    out = out[ok.values].reset_index(drop=True)
    out["gross"] = out["dir"] * (out["p_out"] - out["p_in"]) / pip
    return out


def reversal_trades(pair: str, df: pd.DataFrame, entry_min: int) -> pd.DataFrame:
    """Résultat A, tous les jours de fix : m = open(16:00) − open(15:00) (pips) ; sens = −signe(m) ;
    entrée à l'open de 16:00 + entry_min ; sortie à l'open de 12:00 Londres du jour suivant."""
    fd = fix_days(df).dropna(subset=["next"])
    d = pd.DatetimeIndex(fd["date"])
    p15, t15 = price_at(df, wall(d, "15:00", LDN))
    p16, _ = price_at(df, wall(d, "16:00", LDN))
    T_in = wall(d, "16:00", LDN) + entry_min * MIN
    p_in, t_in = price_at(df, T_in)
    p_out, t_out = price_at(df, wall(pd.DatetimeIndex(fd["next"]), "12:00", LDN))
    m = (p16 - p15) / PAIRS[pair].pip
    ok = np.isfinite(m) & (t15 > 0)
    out = _trades(pair, df, d, np.where(ok, t15, -1), t_in, np.where(ok, p_in, np.nan), t_out, p_out,
                  -np.nan_to_num(m), {"m": np.round(m, 6), "eom": fd["eom"].values})
    return out


# ------------------------------------------------------------------ actions (résultat B)

EQUITY = {  # paire → (indice du pays, fuseau, heure de clôture locale [, à partir de date, nouvelle heure])
    "6E": ("GRXEUR", "Europe/Berlin", "17:30", None),
    "6A": ("AUXAUD", "Australia/Sydney", "16:00", None),
    "6J": ("JPXJPY", "Asia/Tokyo", "15:00", ("2024-11-05", "15:30")),
}
EXCLUDED_MONTHS = {"6E": {(2020, 6), (2023, 12)}}
CLOSE_SLACK = pd.Timedelta(minutes=10).value


def load_equity(name: str) -> pd.DataFrame:
    if name == "ES":
        df = pd.read_parquet(ES_FILE)
        df = df[~df.index.duplicated()].sort_index()
        return df[["close"]]
    return pd.read_parquet(HISTDATA / f"{name}.parquet")[["close"]]


def daily_closes(eq: pd.DataFrame, tz: str, hhmm: str, switch=None) -> pd.Series:
    """Clôture au comptant locale : dernier close 1 minute dont la barre commence dans
    [heure de clôture − 10 min, heure de clôture). Une valeur par date locale de bourse."""
    loc_dates = pd.DatetimeIndex(np.unique(eq.index.tz_convert(tz).tz_localize(None).normalize()))
    t = wall(loc_dates, hhmm, tz)
    if switch is not None:
        later = loc_dates >= pd.Timestamp(switch[0])
        t[later] = wall(loc_dates[later], switch[1], tz)
    idx = eq.index.as_unit("ns").asi8
    pos = np.searchsorted(idx, t, side="left") - 1
    okp = pos >= 0
    pc = np.maximum(pos, 0)
    ok = okp & (idx[pc] >= t - CLOSE_SLACK)
    return pd.Series(eq["close"].values[pc][ok], index=pd.DatetimeIndex(t[ok], tz="UTC"))


def month_to_date(closes: pd.Series, fix_dates: pd.DatetimeIndex, cutoff_ns: np.ndarray) -> np.ndarray:
    """Rendement de la dernière clôture du mois précédent à la dernière clôture strictement
    antérieure au jour du fix (instant de clôture < cutoff_ns, minuit de Londres du jour J)."""
    t = closes.index.as_unit("ns").asi8
    v = closes.values
    out = np.full(len(fix_dates), np.nan)
    month_start = wall(pd.DatetimeIndex(fix_dates).to_period("M").to_timestamp(), "00:00", LDN)
    for i, (a, b) in enumerate(zip(month_start, cutoff_ns)):
        i0 = np.searchsorted(t, a, side="left") - 1  # dernière clôture avant le mois
        i1 = np.searchsorted(t, b, side="left") - 1  # dernière clôture avant le jour J
        if i0 >= 0 and i1 > i0 and t[i0] >= a - 10 * 86_400 * 10**9:
            out[i] = v[i1] / v[i0] - 1
    return out


def flow_trades(pair: str, df: pd.DataFrame, exit_hhmm: str, eq_us: pd.Series, eq_cty: pd.Series) -> pd.DataFrame:
    """Résultat B, tous les jours de fix : x = r_actions(pays) − r_actions(US) depuis le début du
    mois jusqu'à la veille ; position dans le sens de la dépréciation de la devise dont les
    actions ont surperformé ; entrée 13:00 Londres, sortie `exit_hhmm` Londres."""
    fd = fix_days(df)
    d = pd.DatetimeIndex(fd["date"])
    cutoff = wall(d, "00:00", LDN)
    x = month_to_date(eq_cty, d, cutoff) - month_to_date(eq_us, d, cutoff)
    bad = np.array([(y, mo) in EXCLUDED_MONTHS.get(pair, set()) for y, mo in zip(d.year, d.month)], bool)
    x[bad] = np.nan
    sign = np.sign(x) if PAIRS[pair].inverted else -np.sign(x)
    p_in, t_in = price_at(df, wall(d, "13:00", LDN))
    p_out, t_out = price_at(df, wall(d, exit_hhmm, LDN))
    ok = np.isfinite(x)
    return _trades(pair, df, d, np.where(ok, t_in, -1), t_in, np.where(ok, p_in, np.nan), t_out, p_out,
                   np.nan_to_num(sign), {"x": x, "eom": fd["eom"].values})
