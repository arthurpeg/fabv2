"""Séances régulières (ES, DAX), signaux d'asymétrie et trades ouverture → clôture de t+1.
Voir PREREGISTRATION_8.md.

Une séance = une date locale avec une barre à l'heure d'ouverture. Elle est « complète »
si elle a aussi la barre de la dernière minute (15:59 ES, 17:29 DAX). O = open de la barre
d'ouverture, H / L = extrêmes des barres de la séance, C = close de la dernière minute.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ES_FILE = Path("D:/quant-data/Cotations/indices/ES_v0_1m.parquet")
DAX_FILE = Path("cache/histdata/GRXEUR.parquet")
DAX_SWITCHES = (pd.Timestamp("2020-06-15"), pd.Timestamp("2023-12-01"))


@dataclass(frozen=True)
class Market:
    name: str
    tz: str
    open_hhmm: str
    last_hhmm: str  # dernière barre de la séance


ES = Market("ES", "America/New_York", "09:30", "15:59")
DAX = Market("DAX", "Europe/Berlin", "09:00", "17:29")


def load(m: Market) -> pd.DataFrame:
    if m.name == "ES":
        df = pd.read_parquet(ES_FILE)
        df = df[~df.index.duplicated()].sort_index()[["open", "high", "low", "close"]]
    else:  # CFD HistData : open et close seulement → high / low = extrêmes des open et close
        df = pd.read_parquet(DAX_FILE)[["open", "close"]]
        df = df.assign(high=df[["open", "close"]].max(axis=1), low=df[["open", "close"]].min(axis=1))
    return df


def _mins(hhmm: str) -> int:
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m


def sessions(df: pd.DataFrame, m: Market) -> pd.DataFrame:
    """Une ligne par date locale ayant une barre d'ouverture : O, O1 (open de la minute
    suivante, NaN si absente), H, L, C, horodatages (ns) de l'ouverture et de la fin de la
    dernière minute, et l'indicateur de séance complète."""
    loc = df.index.tz_convert(m.tz)
    mins = loc.hour * 60 + loc.minute
    a, b = _mins(m.open_hhmm), _mins(m.last_hhmm)
    inside = (mins >= a) & (mins <= b)
    s = df[inside].copy()
    s["date"] = loc[inside].tz_localize(None).normalize()
    s["mins"] = mins[inside]
    s["ts"] = s.index.as_unit("ns").asi8
    g = s.groupby("date")
    first = g.first()
    out = pd.DataFrame({
        "has_open": g["mins"].min() == a,
        "full": (g["mins"].min() == a) & (g["mins"].max() == b),
        "O": first["open"], "H": g["high"].max(), "L": g["low"].min(), "C": g["close"].last(),
        "t_open": g["ts"].min(), "t_close": g["ts"].max() + 60 * 10**9,
    })
    o1 = s[s["mins"] == a + 1].set_index("date")
    out["O1"] = o1["open"].reindex(out.index)
    out["t_open1"] = o1["ts"].reindex(out.index)
    out = out[out["has_open"]].drop(columns="has_open")
    return out


def roll_between(t_a: np.ndarray, t_b: np.ndarray, df: pd.DataFrame) -> np.ndarray:
    """True si une barre de 00:00 UTC du 8 au 21 d'un mois trimestriel tombe dans (t_a, t_b]."""
    idx = df.index
    mk = ((idx.hour == 0) & (idx.minute == 0) & np.isin(idx.month, (3, 6, 9, 12))
          & (idx.day >= 8) & (idx.day <= 21))
    mids = idx[mk].as_unit("ns").asi8
    return np.searchsorted(mids, t_b, side="right") > np.searchsorted(mids, t_a, side="right")


def signals(S: pd.DataFrame) -> pd.DataFrame:
    """Signaux du jour t (indexés par la date t)."""
    prevC = S["C"].shift()
    return pd.DataFrame({
        "asym": np.log(S["H"] / S["O"]) + np.log(S["L"] / S["O"]),
        "asym_prevC": np.log(S["H"] / prevC) + np.log(S["L"] / prevC),
        "asym_C": np.log(S["H"] / S["C"]) + np.log(S["L"] / S["C"]),
        "roc": np.log(S["C"] / S["O"]),
    }, index=S.index)


def next_day_frame(S: pd.DataFrame, m: Market, df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Couples (t, t+1) de séances consécutives, toutes deux complètes. Contient les signaux
    de t et les prix de t+1. `prevC_ok` : C_{t−1} utilisable (t−1 complète, pas de roulement
    entre t−1 et t). Pour le DAX, on exclut les couples qui chevauchent une bascule d'indice."""
    sig = signals(S)
    nxt = S.shift(-1)
    F = pd.DataFrame({
        "date_sig": S.index,
        "ok": S["full"].values & nxt["full"].fillna(False).astype(bool).values,
        "t_in": nxt["t_open"].values, "p_in": nxt["O"].values,
        "t_in1": nxt["t_open1"].values, "p_in1": nxt["O1"].values,
        "t_out": nxt["t_close"].values, "p_out": nxt["C"].values,
        **{k: sig[k].values for k in sig},
    })
    F["date"] = pd.to_datetime(S.index.to_series().shift(-1).values)
    prev_full = S["full"].shift(fill_value=False).values
    F["prevC_ok"] = prev_full
    if df is not None and m.name == "ES":
        t_prev_close = S["t_close"].shift().values
        bad = roll_between(np.nan_to_num(t_prev_close, nan=0).astype(np.int64), S["t_open"].values, df)
        F["prevC_ok"] &= ~bad
    if m.name == "DAX":
        prev_date = pd.to_datetime(S.index.to_series().shift().values)
        for sw in DAX_SWITCHES:
            F.loc[(F["date_sig"] < sw) & (F["date"] >= sw), "ok"] = False
            F.loc[(prev_date < sw) & (F["date_sig"] >= sw), "prevC_ok"] = False
    return F[F["ok"] & F["date"].notna()].reset_index(drop=True)


def trades(F: pd.DataFrame, rule: str, entry: str = "open") -> pd.DataFrame:
    """Trades d'une règle : sens (+1 long, −1 short), prix, horodatages, rendement brut."""
    if rule in ("asym", "asym_prevC", "asym_C", "roc"):
        d = -np.sign(F[rule].values)
    elif rule == "asym_long":
        d = np.where(F["asym"].values < 0, 1.0, 0.0)
    elif rule == "asym_short":
        d = np.where(F["asym"].values > 0, -1.0, 0.0)
    else:
        raise ValueError(rule)
    ok = np.isfinite(F[rule if rule in F else "asym"].values) & (d != 0)
    if rule == "asym_prevC":
        ok &= F["prevC_ok"].values
    p_in = F["p_in1"].values if entry == "open1" else F["p_in"].values
    t_in = F["t_in1"].values if entry == "open1" else F["t_in"].values
    T = pd.DataFrame({"date": F["date"].values, "t_in": t_in, "t_out": F["t_out"].values,
                      "p_in": p_in, "p_out": F["p_out"].values, "dir": d})
    T = T[ok & np.isfinite(p_in)].reset_index(drop=True)
    T["t_in"] = T["t_in"].astype(np.int64)
    T["gross"] = T["dir"] * (T["p_out"] / T["p_in"] - 1)
    return T
