"""Données, grilles intraday et moteur vectorbt communs à toutes les stratégies.

Conventions (voir PREREGISTRATION.md) :
- une décision prise à T n'utilise que les barres terminées à T ;
- elle s'exécute à l'open de la barre qui commence à T (ou de la première barre
  dans les 5 minutes qui suivent) ;
- toutes les stratégies sont à plat en fin de fenêtre.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

DATA_DIR = Path("D:/quant-data/Cotations")
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"

IS_END = pd.Timestamp("2022-12-31")


@dataclass(frozen=True)
class Asset:
    name: str
    folder: str
    tick: float
    point_value: float
    tz: str
    open_min: int  # minute de la journée locale
    close_min: int
    kind: str  # "index" | "oil" | "gold" | "fx"

    @property
    def rt_cost(self) -> float:
        """Coût aller-retour en points : 1 tick + 5 $ de commission."""
        return self.tick + 5.0 / self.point_value


def hm(s: str) -> int:
    h, m = s.split(":")
    return int(h) * 60 + int(m)


NY, LDN = "America/New_York", "Europe/London"
ASSETS = {
    a.name: a
    for a in [
        Asset("ES", "indices", 0.25, 50, NY, hm("09:30"), hm("16:00"), "index"),
        Asset("NQ", "indices", 0.25, 20, NY, hm("09:30"), hm("16:00"), "index"),
        Asset("YM", "indices", 1.0, 5, NY, hm("09:30"), hm("16:00"), "index"),
        Asset("CL", "energie", 0.01, 1000, NY, hm("09:00"), hm("14:30"), "oil"),
        Asset("GC", "metaux", 0.10, 100, NY, hm("08:20"), hm("13:30"), "gold"),
        Asset("6E", "forex", 0.00005, 125_000, LDN, hm("08:00"), hm("16:00"), "fx"),
        Asset("6J", "forex", 0.0000005, 12_500_000, LDN, hm("08:00"), hm("16:00"), "fx"),
        Asset("6B", "forex", 0.0001, 62_500, LDN, hm("08:00"), hm("16:00"), "fx"),
        Asset("6A", "forex", 0.00005, 100_000, LDN, hm("08:00"), hm("16:00"), "fx"),
    ]
}


# --------------------------------------------------------------------------- données


@lru_cache(maxsize=None)
def load(name: str) -> pd.DataFrame:
    """Barres 1 minute UTC, ajustées en ratio aux roulements ; colonne `factor`
    = prix ajusté / prix brut."""
    CACHE_DIR.mkdir(exist_ok=True)
    cached = CACHE_DIR / f"{name}_adj.parquet"
    if cached.exists():
        return pd.read_parquet(cached)
    a = ASSETS[name]
    df = pd.read_parquet(DATA_DIR / a.folder / f"{name}_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    gap = df["open"] / df["close"].shift() - 1
    med = df["close"].pct_change().abs().rolling(1440, min_periods=100).median()
    at_midnight = (df.index.hour == 0) & (df.index.minute == 0)
    roll = at_midnight & (gap.abs() > np.maximum(12 * med, 0.001))
    # facteur appliqué à toutes les barres strictement antérieures au roulement
    step = pd.Series(np.where(roll, 1 + gap, 1.0), index=df.index)
    factor = step[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
    out = df[["open", "high", "low", "close"]].mul(factor, axis=0)
    out["volume"] = df["volume"]
    out["factor"] = factor
    out.attrs["n_rolls"] = int(roll.sum())
    out.to_parquet(cached)
    return out


@dataclass
class Grid:
    """Matrices jours × minutes locales (colonnes = minute de la journée)."""

    tz: str
    O: pd.DataFrame
    H: pd.DataFrame
    L: pd.DataFrame
    C: pd.DataFrame
    V: pd.DataFrame
    F: pd.DataFrame  # facteur d'ajustement

    @property
    def dates(self) -> pd.Index:
        return self.O.index

    def price_at(self, minute: int, slack: int = 5) -> tuple[pd.Series, pd.Series]:
        """Open de la première barre dans [minute, minute+slack). Retourne (prix, minute réelle)."""
        cols = [m for m in range(minute, minute + slack) if m in self.O.columns]
        sub = self.O[cols]
        first = sub.notna().idxmax(axis=1).where(sub.notna().any(axis=1))
        px = pd.Series(
            [sub.at[d, m] if pd.notna(m) else np.nan for d, m in first.items()],
            index=sub.index,
        )
        return px, first

    def factor_at(self, minute: int) -> pd.Series:
        cols = [m for m in self.F.columns if m >= minute]
        return self.F[cols].bfill(axis=1).iloc[:, 0].fillna(self.F.ffill(axis=1).iloc[:, -1])


def grid(name: str, tz: str, start: int, end: int) -> Grid:
    """Fenêtre locale [start, end] (minutes) ; une ligne par date locale ouvrée."""
    df = load(name)
    loc = df.tz_convert(tz)
    mins = loc.index.hour * 60 + loc.index.minute
    keep = (mins >= start) & (mins <= end) & (loc.index.dayofweek < 5)
    sub = loc[keep]
    key_d = sub.index.tz_localize(None).normalize()
    key_m = mins[keep]
    piv = {}
    for col in ["open", "high", "low", "close", "volume", "factor"]:
        piv[col] = pd.DataFrame({"d": key_d, "m": key_m, "v": sub[col].values}).pivot(
            index="d", columns="m", values="v"
        )
    full_cols = range(start, end + 1)
    piv = {k: v.reindex(columns=full_cols) for k, v in piv.items()}
    return Grid(tz, piv["open"], piv["high"], piv["low"], piv["close"], piv["volume"], piv["factor"])


def past_std(s: pd.Series, n: int = 60) -> pd.Series:
    return s.shift(1).rolling(n, min_periods=int(n * 0.66)).std()


def past_median(s: pd.Series, n: int = 60) -> pd.Series:
    return s.shift(1).rolling(n, min_periods=int(n * 0.66)).median()


# --------------------------------------------------------------------------- trades


TRADE_COLS = ["date", "m_in", "p_in", "m_out", "p_out", "dir", "f_in"]


def trades_frame(rows: list[dict] | pd.DataFrame) -> pd.DataFrame:
    t = pd.DataFrame(rows, columns=TRADE_COLS) if isinstance(rows, list) else rows[TRADE_COLS]
    t = t.dropna(subset=["p_in", "p_out", "m_in", "m_out"])
    t = t[(t["dir"] != 0) & (t["m_out"] > t["m_in"])]
    return t.reset_index(drop=True)


def simple_trades(g: Grid, direction: pd.Series, m_in: int, m_out: int) -> pd.DataFrame:
    """Une position `direction` (±1, 0/NaN = rien) de m_in à m_out, chaque jour."""
    p_in, a_in = g.price_at(m_in)
    p_out, a_out = g.price_at(m_out)
    t = pd.DataFrame(
        {
            "date": g.dates,
            "m_in": a_in.values,
            "p_in": p_in.values,
            "m_out": a_out.values,
            "p_out": p_out.values,
            "dir": np.sign(direction.reindex(g.dates).fillna(0)).values,
            "f_in": g.factor_at(m_in).values,
        }
    )
    return trades_frame(t)


# --------------------------------------------------------------------------- moteur


@dataclass
class Result:
    name: str
    asset: str
    trades: pd.DataFrame
    daily_net: pd.Series
    daily_gross: pd.Series


def _events(trades: pd.DataFrame, tz: str) -> pd.DataFrame:
    """Trades → événements (horodatage UTC, prix, cible, facteur). Une sortie et une
    entrée au même instant fusionnent en un seul ordre (retournement)."""

    def ts(m):
        # minutes locales → heure murale → instant UTC (gère l'heure d'été)
        wall = pd.to_datetime(trades["date"]) + pd.to_timedelta(m, unit="min")
        return wall.dt.tz_localize(tz, ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")

    common = {"factor": trades["f_in"].values}
    ent = pd.DataFrame({"ts": ts(trades["m_in"]), "price": trades["p_in"], "target": trades["dir"], "o": 1, **common})
    ext = pd.DataFrame({"ts": ts(trades["m_out"]), "price": trades["p_out"], "target": 0.0, "o": 0, **common})
    ev = pd.concat([ent, ext]).dropna(subset=["ts"]).sort_values(["ts", "o"])
    return ev.groupby("ts").last()  # sortie puis entrée au même instant → la cible finale gagne


def backtest(name: str, asset: Asset, trades: pd.DataFrame, tz: str, all_dates: pd.Index) -> Result:
    """Exécute les trades dans vectorbt (net et brut) et renvoie les rendements journaliers."""
    ev = _events(trades, tz)
    out = {}
    for label, cost in [("net", asset.rt_cost / 2), ("gross", 0.0)]:
        if ev.empty:
            out[label] = pd.Series(0.0, index=all_dates)
            continue
        # coût par côté en points bruts → fraction du prix brut (= prix ajusté / facteur)
        fees = cost / (ev["price"].values / ev["factor"].values)
        pf = vbt.Portfolio.from_orders(
            close=ev["price"],
            size=ev["target"],
            size_type="targetpercent",
            direction="both",
            fees=fees,
            init_cash=1_000_000.0,
            freq="1min",
        )
        val = pf.value()
        local_day = val.index.tz_convert(tz).tz_localize(None).normalize()
        day_val = val.groupby(local_day).last()
        day_val = day_val.reindex(all_dates.union(day_val.index)).ffill().fillna(1_000_000.0)
        out[label] = (day_val / day_val.shift(1, fill_value=1_000_000.0) - 1).reindex(all_dates).fillna(0.0)
    return Result(name, asset.name, trades, out["net"], out["gross"])


# --------------------------------------------------------------------------- métriques


def sharpe(r: pd.Series) -> float:
    sd = r.std()
    return float(r.mean() / sd * np.sqrt(252)) if sd > 0 else np.nan


def summarize(res: Result) -> dict:
    a = ASSETS[res.asset]
    t = res.trades
    raw_move = (t["p_out"] - t["p_in"]) * t["dir"] / t["f_in"]  # points bruts
    net_pts = raw_move - a.rt_cost
    row = {"strategy": res.name, "asset": res.asset, "n_trades": len(t)}
    for lab, mask in [("IS", res.daily_net.index <= IS_END), ("OOS", res.daily_net.index > IS_END)]:
        tm = (pd.to_datetime(t["date"]) <= IS_END) if lab == "IS" else (pd.to_datetime(t["date"]) > IS_END)
        row[f"sharpe_net_{lab}"] = sharpe(res.daily_net[mask])
        row[f"sharpe_gross_{lab}"] = sharpe(res.daily_gross[mask])
        row[f"ret_net_{lab}_%"] = float((1 + res.daily_net[mask]).prod() - 1) * 100
        row[f"trades_{lab}"] = int(tm.sum())
        row[f"avg_ticks_gross_{lab}"] = float(raw_move[tm].mean() / a.tick) if tm.any() else np.nan
    row["avg_ticks_gross"] = float(raw_move.mean() / a.tick) if len(t) else np.nan
    row["cost_ticks"] = a.rt_cost / a.tick
    row["avg_ticks_net"] = float(net_pts.mean() / a.tick) if len(t) else np.nan
    row["hit_rate_net_%"] = float((net_pts > 0).mean() * 100) if len(t) else np.nan
    row["survives"] = bool(
        row["sharpe_net_IS"] > 0.5
        and row["sharpe_net_OOS"] > 0.3
        and row["avg_ticks_net"] > 0
    )
    return row
