"""Jours de séance (ES, NQ ajustés en ratio), signal r = P(T) / C_{t−1} − 1 et trades
« suivre le mouvement de T à la clôture ». Voir PREREGISTRATION_9.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

NY = "America/New_York"
CACHE = Path("cache")
SLACK = pd.Timedelta(minutes=5).value


def load(name: str) -> pd.DataFrame:
    return pd.read_parquet(CACHE / f"{name}_adj.parquet")


def days(df: pd.DataFrame, decision_times: tuple[str, ...]) -> pd.DataFrame:
    """Une ligne par date de New York ayant une barre à 15:59 : C (close de 15:59), fin de la
    barre de 15:59 (ns), et pour chaque heure T : prix (open de la première barre dans
    [T, T + 5 min)), horodatage et facteur d'ajustement."""
    loc = df.index.tz_convert(NY)
    date = loc.tz_localize(None).normalize()
    mins = loc.hour * 60 + loc.minute
    ts = df.index.as_unit("ns").asi8
    last = mins == 15 * 60 + 59
    D = pd.DataFrame({"C": df["close"].values[last], "t_close": ts[last] + 60 * 10**9},
                     index=pd.DatetimeIndex(date[last]))
    D = D[~D.index.duplicated()]
    trading = pd.DatetimeIndex(np.unique(date[mins == 9 * 60 + 30]))  # séances, demi-séances comprises
    pos = np.searchsorted(trading.values, D.index.values) - 1
    D["prev_trading"] = pd.DatetimeIndex(np.where(pos >= 0, trading.values[np.maximum(pos, 0)], np.datetime64("NaT")))
    for T in decision_times:
        h, m = map(int, T.split(":"))
        a = h * 60 + m
        sel = (mins >= a) & (mins < a + 5)
        first = pd.DataFrame({"date": date[sel], "p": df["open"].values[sel], "t": ts[sel],
                              "f": df["factor"].values[sel]}).groupby("date").first()
        D[f"p_{T}"] = first["p"].reindex(D.index)
        D[f"t_{T}"] = first["t"].reindex(D.index)
        D[f"f_{T}"] = first["f"].reindex(D.index)
    return D


def trades(D: pd.DataFrame, T: str, s: float) -> pd.DataFrame:
    """Jours où |P(T) / C_{t−1} − 1| ≥ s : position signe(r) de l'open de T au close de 15:59.
    La veille = jour précédent du tableau (séance complète avec une barre à 15:59)."""
    prev_date = pd.Series(D.index, index=D.index).shift()
    prevC = D["C"].shift().where(prev_date == D["prev_trading"])  # veille = séance complète
    r = D[f"p_{T}"] / prevC - 1
    ok = np.isfinite(r.values) & (r.abs().values >= s) & np.isfinite(D[f"t_{T}"].values)
    out = pd.DataFrame({
        "date": D.index[ok], "t_in": D[f"t_{T}"].values[ok].astype(np.int64), "t_out": D["t_close"].values[ok],
        "p_in": D[f"p_{T}"].values[ok], "p_out": D["C"].values[ok], "dir": np.sign(r.values[ok]),
        "r_sig": r.values[ok], "raw_in": D[f"p_{T}"].values[ok] / D[f"f_{T}"].values[ok],
    })
    out["gross"] = out["dir"] * (out["p_out"] / out["p_in"] - 1)
    return out.reset_index(drop=True)
