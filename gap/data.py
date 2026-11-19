"""Chargement, courbes intrajournalières 5 min et cibles A′ / B.

Conventions (PREREGISTRATION_5.md) :
- tout est en UTC ; une barre 1 min étiquetée `s` (début) n'est connue qu'à `s + 1 min` ;
- un point de courbe à l'instant g vaut la clôture de la dernière barre terminée
  au plus tard à g (et commencée dans la fenêtre) ; le premier point vaut l'open
  de la première barre dans [début, début + 5 min) ;
- un prix d'exécution à l'instant t vaut l'open de la première barre dans
  [t, t + 5 min), sinon le jour est exclu (convention de `fab/core.py`).
"""

from __future__ import annotations

import glob
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from fab.core import CACHE_DIR, DATA_DIR, load
from gap import ROOT
from gap.calendar import market_window, target_days, third_fridays, wall_to_utc

MIN = pd.Timedelta(minutes=1)
# Horodatages HistData : heure brute + 7 h = heure d'Athènes (règles d'été
# européennes), contrairement à la FAQ (« EST sans heure d'été »). Mesuré sur
# les ouvertures de Hong Kong, Sydney et Xetra, 2016-2026 ; voir cache/histdata/README.md.
HISTDATA_SHIFT = pd.Timedelta(hours=7)
HISTDATA_TZ = "Europe/Athens"


# --------------------------------------------------------------------------- sources


def histdata_to_utc(raw: pd.Series) -> pd.DatetimeIndex:
    """Chaînes `AAAAMMJJ HHMMSS` HistData → instants UTC. Les heures inexistantes
    ou ambiguës (nuit du changement d'heure, toujours un dimanche) deviennent NaT."""
    wall = pd.to_datetime(raw, format="%Y%m%d %H%M%S") + HISTDATA_SHIFT
    loc = pd.DatetimeIndex(wall).tz_localize(HISTDATA_TZ, ambiguous="NaT", nonexistent="NaT")
    return loc.tz_convert("UTC")


@lru_cache(maxsize=None)
def load_histdata(pair: str, src_dir: str) -> pd.DataFrame:
    """Barres 1 min HistData (open, close), index UTC = début de barre. Cache parquet."""
    cached = CACHE_DIR / "histdata" / f"{pair}.parquet"
    if cached.exists():
        return pd.read_parquet(cached)
    files = sorted(glob.glob(str(Path(src_dir) / f"DAT_ASCII_{pair}_M1_*.csv")))
    if not files:
        raise FileNotFoundError(f"aucun fichier HistData pour {pair} dans {src_dir}")
    cols = ["ts", "open", "high", "low", "close", "volume"]
    df = pd.concat(pd.read_csv(f, sep=";", header=None, names=cols, dtype={"ts": str}) for f in files)
    idx = histdata_to_utc(df["ts"])
    out = pd.DataFrame({"open": df["open"].values, "close": df["close"].values}, index=idx)
    out = out[out.index.notna()].sort_index()
    out = out[~out.index.duplicated()]
    out.index.name = "ts"
    out.to_parquet(cached)
    return out


@lru_cache(maxsize=None)
def load_fdax() -> pd.DataFrame:
    """FDAX `.v.0` Databento brut (pas dans `fab.core.ASSETS` : les scripts du
    labo prennent tout le registre par défaut)."""
    df = pd.read_parquet(DATA_DIR / "indices" / "FDAX_v0_1m.parquet")
    return df[~df.index.duplicated()].sort_index()[["open", "close"]]


def load_source(source: str, cfg: dict) -> pd.DataFrame:
    kind, name = source.split(":")
    if kind == "histdata":
        return load_histdata(name, str(ROOT / cfg["data"]["histdata_dir"]))
    if name == "FDAX":
        return load_fdax()
    return load(name)[["open", "close"]]


# --------------------------------------------------------------------------- extraction


def utc_ns(x) -> np.ndarray:
    """DatetimeIndex (UTC ou naïf UTC) ou tableau → datetime64[ns] naïf UTC."""
    if isinstance(x, pd.DatetimeIndex) and x.tz is not None:
        x = x.tz_convert("UTC").tz_localize(None)
    return np.asarray(x, dtype="datetime64[ns]")


def to_index(a: np.ndarray) -> pd.DatetimeIndex:
    return pd.DatetimeIndex(a).tz_localize("UTC")


def open_at(px: pd.DataFrame, t, slack_min: int = 5) -> tuple[np.ndarray, np.ndarray]:
    """Open de la première barre commencée dans [t, t + slack). Retourne (prix, début de barre)."""
    idx, t = utc_ns(px.index), utc_ns(t)
    pos = np.searchsorted(idx, t, side="left")
    pos_c = np.minimum(pos, len(idx) - 1)
    ok = (pos < len(idx)) & (idx[pos_c] < t + np.timedelta64(slack_min, "m"))
    price = np.where(ok, px["open"].values[pos_c], np.nan)
    ts = np.where(ok, idx[pos_c], np.datetime64("NaT", "ns"))
    return price, ts


def curves(px: pd.DataFrame, start: pd.DatetimeIndex, end: pd.DatetimeIndex, step_min: int = 5,
           tolerance_min: int = 90) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Courbes de prix sur une grille fixe de `step_min` minutes, une ligne par jour.

    Retourne (C, missing, last_end) :
    - C : n × G, NaN là où aucune barre terminée récente (≤ `tolerance_min`) n'existe ;
    - missing : fraction de points manquants par jour ;
    - last_end : instant de fin (UTC) de la dernière barre utilisée, par jour.
    Toutes les fenêtres doivent avoir la même longueur.
    """
    span = (end - start).unique()
    if len(span) != 1:
        raise ValueError(f"fenêtres de longueurs différentes : {span}")
    G = int(span[0] / pd.Timedelta(minutes=step_min)) + 1
    offs = np.arange(G) * np.timedelta64(step_min, "m")
    st = utc_ns(start)
    grid = st[:, None] + offs[None, :]  # n × G
    # clôtures indexées par l'instant où elles sont connues (fin de barre)
    idx = utc_ns(px.index)
    ends = idx + np.timedelta64(1, "m")
    flat = grid.ravel()
    pos = np.searchsorted(ends, flat, side="right") - 1
    pos_c = np.maximum(pos, 0)
    row_start = np.repeat(st, G)
    ok = (pos >= 0) & (idx[pos_c] >= row_start) & (flat - ends[pos_c] <= np.timedelta64(tolerance_min, "m"))
    C = np.where(ok, px["close"].values[pos_c], np.nan).reshape(-1, G)
    used = np.where(ok, ends[pos_c], np.datetime64("NaT", "ns")).reshape(-1, G)
    # premier point = open de la première barre de la fenêtre (connu à son début)
    C[:, 0], used[:, 0] = open_at(px, st)
    missing = np.isnan(C).mean(axis=1)
    as_int = np.where(np.isnat(used), np.iinfo(np.int64).min, used.view("int64"))
    last_end = as_int.max(axis=1).view("datetime64[ns]")  # NaT si rien d'utilisé
    # lissage des trous restants : dernier prix connu, puis premier prix pour le début
    C = pd.DataFrame(C).ffill(axis=1).bfill(axis=1).values
    return C, missing, to_index(last_end)


# --------------------------------------------------------------------------- échantillon


@dataclass
class Sample:
    """Tout ce qu'il faut pour un jour cible, aligné sur `days`."""

    days: pd.DatetimeIndex
    t_decision: pd.DatetimeIndex
    curves: dict[str, np.ndarray]
    last_end: dict[str, pd.DatetimeIndex]  # fin de la dernière barre utilisée, par marché
    y_a: np.ndarray  # A′ : CFD 09:00 / CFD 17:30 la veille − 1
    y_b: dict[int, np.ndarray]  # B : CFD 09:00+k / CFD 08:55 − 1
    entry_ts: pd.DatetimeIndex
    entry_px: np.ndarray
    exit_ts: dict[int, pd.DatetimeIndex]
    exit_px: dict[int, np.ndarray]
    fdax_entry_px: np.ndarray  # NaN avant 2025-03
    fdax_exit_px: dict[int, np.ndarray]
    roll_night: np.ndarray  # nuit de bascule du FDAX continu (exclue de A′ sur le future)
    overnight: np.ndarray  # CFD 17:30 la veille → 08:55 (référence)
    us_ret: np.ndarray  # rendement ES de la séance US de la veille (référence)
    vol20: np.ndarray  # écart-type des 20 derniers rendements 17:30 → 17:30, connu la veille
    excluded: dict[str, int] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.days)

    def window_returns(self, markets: list[str]) -> np.ndarray:
        return np.column_stack([self.curves[m][:, -1] / self.curves[m][:, 0] - 1 for m in markets])

    def last_feature_end(self, markets: list[str]) -> pd.DatetimeIndex:
        v = np.column_stack([utc_ns(self.last_end[m]) for m in markets])
        return to_index(v.max(axis=1))


def build_sample(cfg: dict) -> Sample:
    t, d = cfg["timing"], cfg["data"]
    tz, slack = t["target_tz"], t["slack_min"]
    days = target_days(cfg)
    n0 = len(days)
    keep = np.ones(n0, bool)
    excluded: dict[str, int] = {}

    def drop(reason: str, mask: np.ndarray) -> None:
        new = mask & keep
        excluded[reason] = excluded.get(reason, 0) + int(new.sum())
        keep[new] = False

    # courbes de chaque marché
    cur, last, miss = {}, {}, {}
    for name, m in cfg["markets"].items():
        w = market_window(cfg, name, days)
        drop(f"séance absente ou écourtée : {name}", ~w["ok"].values)
        px = load_source(m["source"], cfg)
        C, missing, le = curves(px, pd.DatetimeIndex(w["start"]), pd.DatetimeIndex(w["end"]),
                                cfg["features"]["grid_min"])
        drop(f"données manquantes > {d['max_missing']:.0%} : {name}", ~(missing <= d["max_missing"]))
        cur[name], last[name], miss[name] = C, le, missing

    # cibles sur le CFD (et le FDAX pour la validation)
    D = days.index
    prev = pd.DatetimeIndex(days["prev"])
    t_entry = wall_to_utc(D, t["decision"], tz)
    t_open = wall_to_utc(D, t["cash_open"], tz)
    t_prev = wall_to_utc(prev, t["prev_close"], tz)
    cfd = load_source(d["target"], cfg)
    fdax = load_source(d["validation"], cfg)
    e_px, e_ts = open_at(cfd, t_entry, slack)
    o_px, _ = open_at(cfd, t_open, slack)
    c_px, _ = open_at(cfd, t_prev, slack)
    drop("prix CFD manquant (08:55, 09:00 ou 17:30 la veille)", np.isnan(e_px) | np.isnan(o_px) | np.isnan(c_px))
    bad = np.zeros(len(D), bool)
    for a, b in d.get("exclude", []):
        bad |= ((D >= a) & (D <= b)) | ((prev >= a) & (prev <= b))
    drop("source CFD invalide (amendement 3)", bad)
    floor = d.get("min_target_price", 0.0)
    drop("garde-fou : prix CFD sous le plancher", ~((e_px >= floor) & (o_px >= floor) & (c_px >= floor)))
    x_px, x_ts, fx_px = {}, {}, {}
    for k in t["exit_k"]:
        tk = t_open + pd.Timedelta(minutes=k)
        x_px[k], x_ts[k] = open_at(cfd, tk, slack)
        fx_px[k], _ = open_at(fdax, tk, slack)
        drop(f"prix CFD manquant à 09:00+{k}", np.isnan(x_px[k]))
    f_e, _ = open_at(fdax, t_entry, slack)

    # références
    es = cur["SP500"]
    us_ret = es[:, -1] / es[:, 0] - 1
    daily = pd.Series(c_px, index=D)  # CFD 17:30 de la veille, connu avant t_decision
    vol20 = np.log(daily).diff().rolling(20, min_periods=15).std().values
    rolls = third_fridays(d["start"], d["end"])

    k_ = keep
    return Sample(
        days=D[k_],
        t_decision=pd.DatetimeIndex(days["t_decision"])[k_],
        curves={m: c[k_] for m, c in cur.items()},
        last_end={m: le[k_] for m, le in last.items()},
        y_a=(o_px / c_px - 1)[k_],
        y_b={k: (x_px[k] / e_px - 1)[k_] for k in t["exit_k"]},
        entry_ts=to_index(e_ts[k_]),
        entry_px=e_px[k_],
        exit_ts={k: to_index(x_ts[k][k_]) for k in t["exit_k"]},
        exit_px={k: x_px[k][k_] for k in t["exit_k"]},
        fdax_entry_px=f_e[k_],
        fdax_exit_px={k: fx_px[k][k_] for k in t["exit_k"]},
        roll_night=D[k_].isin(rolls),
        overnight=(e_px / c_px - 1)[k_],
        us_ret=us_ret[k_],
        vol20=vol20[k_],
        excluded={"jours XETR": n0, **excluded, "retenus": int(k_.sum())},
    )
