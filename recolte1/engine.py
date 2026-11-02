"""Données, exécution vectorbt et intervalles de confiance.

Conventions :
- barres 1 minute Databento `.v.0`, horodatées au début de la barre (UTC) ;
- prix à l'instant T = clôture de la dernière barre démarrant dans [T - slack, T - 1 min]
  (comme run_sessions.py) ; sinon le point manque et le trade est écarté ;
- prix ajustés en ratio aux roulements, une détection par cycle d'échéance (la règle de
  fab.core.load manque des roulements, voir run_sessions.py) ;
- coût aller-retour = 1 tick + 5 $ de commission (fab.core.Asset.rt_cost), réparti par côté.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

DATA = Path("D:/quant-data/Cotations")
HIST_2010 = Path("cache/databento_2010")  # 2010-06 → 2015-12, achat Databento (PREREGISTRATION_11)
USE_2010 = False  # à activer avant le premier load() pour rabouter l'historique 2010-2015
NY, LDN, CET = "America/New_York", "Europe/London", "Europe/Berlin"


@dataclass(frozen=True)
class Spec:
    folder: str
    tick: float
    point_value: float
    roll: str  # "quarterly" (mars, juin, sept., déc.) | "gold" (G J M Q V Z) | "silver" (H K N U Z, série LSE)

    @property
    def rt_cost(self) -> float:
        return self.tick + 5.0 / self.point_value


SPECS = {
    "NQ": Spec("indices", 0.25, 20, "quarterly"),
    "ES": Spec("indices", 0.25, 50, "quarterly"),
    "YM": Spec("indices", 1.0, 5, "quarterly"),
    "GC": Spec("metaux", 0.10, 100, "gold"),
    "6E": Spec("forex", 0.00005, 125_000, "quarterly"),
    "6B": Spec("forex", 0.0001, 62_500, "quarterly"),
    "6J": Spec("forex", 0.0000005, 12_500_000, "quarterly"),
    "6A": Spec("forex", 0.00005, 100_000, "quarterly"),
    # argent : London Strategic Edge (fetch_lse.py), 2017-04 → 2026-08, front non ajusté
    "SI": Spec("lse", 0.005, 5_000, "silver"),
}
LSE = Path("cache/lse")
UNIVERSE = list(SPECS)


@lru_cache(maxsize=None)
def load(name: str) -> pd.DataFrame:
    """Barres ajustées en ratio. Un roulement par cycle = le plus grand |écart| à 00:00 UTC
    (barre précédente à moins de 60 min) dans la fenêtre du cycle :
    trimestriels → jours 7 à 22 de mars, juin, sept., déc. (règle de run_sessions.py) ;
    or → du 20 d'un mois impair au 5 du mois suivant (bascule de volume avant G J M Q V Z)."""
    s = SPECS[name]
    if s.folder == "lse":
        return _load_lse(name)
    df = pd.read_parquet(DATA / s.folder / f"{name}_v0_1m.parquet")
    old = HIST_2010 / f"{name}_v0_1m_2010.parquet"
    if USE_2010 and old.exists():
        o = pd.read_parquet(old)
        o = o[o.index < df.index.min()]
        df = pd.concat([o[df.columns].astype(df.dtypes.to_dict()), df])
    df = df[~df.index.duplicated()].sort_index()
    gap = df["open"] / df["close"].shift() - 1
    ix = df.index
    prev = pd.Series(ix, index=ix).shift()
    cand = (ix.hour == 0) & (ix.minute == 0) & ((ix - prev) <= pd.Timedelta(minutes=60)).values
    if s.roll == "quarterly":
        cand &= ix.month.isin([3, 6, 9, 12]) & (ix.day >= 7) & (ix.day <= 22)
        key = ix.year * 100 + ix.month
    else:
        late = (ix.month % 2 == 1) & (ix.day >= 20)
        early = (ix.month % 2 == 0) & (ix.day <= 5)
        cand &= late | early
        cyc = ix.month - early.astype(int)  # mois impair du cycle
        key = ix.year * 100 + cyc
    g = gap[cand]
    k = pd.Series(key[cand], index=g.index)
    rolls = pd.DatetimeIndex(g.abs().groupby(k.values).idxmax().tolist())
    step = pd.Series(1.0, index=ix)
    step.loc[rolls] = 1 + gap.loc[rolls]
    factor = step[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
    out = df[["open", "high", "low", "close"]].mul(factor, axis=0)
    out["volume"] = df["volume"]
    out["factor"] = factor
    out.attrs["rolls"] = gap.loc[rolls]
    return out


def lse_sessions(df: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par séance 18:00 → 17:00 NY : première barre, volume, écart d'ouverture."""
    ix = df.index
    sess = (ix.tz_convert(NY).tz_localize(None) + pd.Timedelta(hours=6)).normalize()
    gap = df["open"] / df["close"].shift() - 1
    g = pd.DataFrame({"t0": ix, "vol": df["volume"].values, "gap": gap.values}).groupby(sess.values)
    out = g.agg(t0=("t0", "min"), vol=("vol", "sum"), gap=("gap", "first"))
    out["med"] = out["vol"].rolling(20, min_periods=5).median().shift(1)
    out["thin"] = out["vol"] < 0.4 * out["med"]
    return out


def lse_rolls(df: pd.DataFrame) -> pd.DataFrame:
    """Roulements de la série LSE (contrat « front » qui reste sur l'échéance jusqu'au mois de
    livraison H K N U Z, puis change à une réouverture de 18:00 NY dont la date varie de ± 3 séances).
    Dans la fenêtre [1er du mois − 10 j, 1er du mois + 5 j] : première séance de volume normal, à
    partir du 1er du mois − 4 j, qui suit une séance mince (< 40 % de la médiane des 20 séances
    précédentes) ; à défaut, séance au plus grand |écart d'ouverture|. Vérifié à la main le 2026-11-02."""
    s = lse_sessions(df)
    rows = []
    for y in range(s.index[0].year, s.index[-1].year + 1):
        for m in (3, 5, 7, 9, 12):
            m0 = pd.Timestamp(y, m, 1)
            w = s[(s.index >= m0 - pd.Timedelta(days=10)) & (s.index <= m0 + pd.Timedelta(days=5))]
            if len(w) < 5:
                continue
            # les séances minces de jours fériés (Thanksgiving, Presidents Day…) ne comptent pas :
            # le roulement suit une séance mince et tombe à moins de 4 jours du 1er du mois
            after_thin = w["thin"].shift(1, fill_value=False) & ~w["thin"] & (w.index >= m0 - pd.Timedelta(days=4))
            if after_thin.any() and w["thin"].any():
                day, how = after_thin[after_thin].index[0], "volume"
            else:
                day, how = w["gap"].abs().idxmax(), "écart"
            rows.append({"séance": day, "t": s.loc[day, "t0"], "gap": s.loc[day, "gap"], "méthode": how})
    return pd.DataFrame(rows)


def _load_lse(name: str) -> pd.DataFrame:
    """Série LSE ajustée en ratio aux roulements de lse_rolls (l'écart retenu absorbe aussi le gap
    de l'arrêt ce jour-là : écarter la séance de roulement des études intraday). Les séances minces
    avant chaque roulement sont sur le contrat qui expire : les filtrer par le volume."""
    df = pd.read_parquet(LSE / f"{name}_lse_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    ix = df.index
    rl = lse_rolls(df)
    rolls = pd.DatetimeIndex(rl["t"])
    gap = df["open"] / df["close"].shift() - 1
    step = pd.Series(1.0, index=ix)
    step.loc[rolls] = 1 + gap.loc[rolls]
    factor = step[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
    out = df[["open", "high", "low", "close"]].mul(factor, axis=0)
    out["volume"] = df["volume"]
    out["factor"] = factor
    out.attrs["rolls"] = gap.loc[rolls]
    out.attrs["roll_table"] = rl
    return out


def price_at(name: str, when: pd.Series, slack_min: int = 5) -> tuple[pd.Series, pd.Series]:
    """(prix ajusté, facteur) à chaque instant UTC de `when`."""
    df = load(name)
    bars = df[["close", "factor"]].rename_axis("bar").reset_index()
    bars["bar"] = bars["bar"].dt.as_unit("ns")
    w = pd.DatetimeIndex(pd.to_datetime(when)).as_unit("ns")
    q = pd.DataFrame({"T": w, "key": w - pd.Timedelta(minutes=1), "i": np.arange(len(w))})
    q = q.dropna(subset=["key"]).sort_values("key")
    m = pd.merge_asof(q, bars, left_on="key", right_on="bar", direction="backward")
    bad = m["bar"] < m["T"] - pd.Timedelta(minutes=slack_min)
    m.loc[bad, ["close", "factor"]] = np.nan
    px = pd.Series(np.nan, index=range(len(w)))
    fa = pd.Series(np.nan, index=range(len(w)))
    px[m["i"].values] = m["close"].values
    fa[m["i"].values] = m["factor"].values
    return pd.Series(px.values, index=when.index), pd.Series(fa.values, index=when.index)


def at(dates: pd.Index, hhmm: str, tz: str, day_offset: int = 0) -> pd.Series:
    """Instant UTC de l'heure murale `hhmm` (fuseau `tz`) pour chaque date."""
    h, m = map(int, hhmm.split(":"))
    wall = pd.DatetimeIndex(dates) + pd.Timedelta(days=day_offset, hours=h, minutes=m)
    loc = wall.tz_localize(tz, ambiguous="NaT", nonexistent="NaT")
    return pd.Series(loc.tz_convert("UTC"), index=dates)


# --------------------------------------------------------------------------- exécution


def non_overlapping(tr: pd.DataFrame) -> pd.DataFrame:
    """Garde les trades dans l'ordre d'entrée, en sautant ceux qui commencent avant la sortie
    du précédent (positions de plusieurs jours)."""
    tr = tr.sort_values("t_in")
    keep, last_out = [], pd.Timestamp.min.tz_localize("UTC")
    for i, (a, b) in zip(tr.index, zip(tr["t_in"], tr["t_out"])):
        if a >= last_out:
            keep.append(i)
            last_out = b
    return tr.loc[keep]


def run(name: str, tr: pd.DataFrame, slack_min: int = 5) -> dict[str, pd.DataFrame]:
    """Exécute `tr` (colonnes t_in, t_out UTC, w = poids signé, day = étiquette) dans vectorbt,
    sans frais ("gross") et avec le coût aller-retour ("net"). Retourne, pour chacun,
    les trades (rendement par trade lu dans pf.trades) et les rendements journaliers."""
    tr = tr.dropna(subset=["t_in", "t_out", "w"])
    tr = tr[(tr["w"] != 0) & (tr["t_out"] > tr["t_in"])]
    if tr.empty:
        return {}
    tr = non_overlapping(tr)
    p_in, f_in = price_at(name, tr["t_in"], slack_min)
    p_out, f_out = price_at(name, tr["t_out"], slack_min)
    ok = p_in.notna() & p_out.notna()
    tr = tr[ok]
    if tr.empty:
        return {}
    ent = pd.DataFrame({"ts": pd.DatetimeIndex(tr["t_in"]), "price": p_in[ok].values, "f": f_in[ok].values,
                        "target": tr["w"].values, "o": 1})
    ext = pd.DataFrame({"ts": pd.DatetimeIndex(tr["t_out"]), "price": p_out[ok].values, "f": f_out[ok].values,
                        "target": 0.0, "o": 0})
    day_of = pd.Series(tr["day"].values, index=pd.DatetimeIndex(tr["t_in"]))
    # trades alternés dans deux portefeuilles : une sortie et l'entrée suivante au même instant
    # ne fusionnent jamais, chaque trade est un aller-retour complet (coût compris)
    par = np.arange(len(tr)) % 2
    out = {}
    for label, cost in [("gross", 0.0), ("net", SPECS[name].rt_cost / 2)]:
        trades, vals = [], []
        for k in (0, 1):
            ev = pd.concat([ent[par == k], ext[par == k]]).sort_values(["ts", "o"]).groupby("ts").last()
            if ev.empty:
                continue
            fees = cost / (ev["price"].values / ev["f"].values)  # coût en points bruts → fraction
            pf = vbt.Portfolio.from_orders(
                close=ev["price"], size=ev["target"], size_type="targetpercent", direction="both",
                fees=fees, init_cash=1_000_000.0, freq="1min",
            )
            rec = pf.trades.records_readable
            raw = pf.trades.records
            closed = (rec["Status"] == "Closed").values
            rec = rec[closed]
            t_ent = ev.index[raw["entry_idx"][closed]]  # horodatage d'entrée, fuseau conservé
            trades.append(pd.DataFrame({
                "day": day_of.reindex(t_ent).values,
                "dir": np.where(rec["Direction"].values == "Long", 1, -1),
                "ret": rec["Return"].values,
            }))
            val = pf.value()
            nyday = val.index.tz_convert(NY).tz_localize(None).normalize()
            dv = val.groupby(nyday).last()
            vals.append(dv / dv.shift(1, fill_value=1_000_000.0) - 1)
        daily = pd.concat(vals, axis=1).fillna(0.0).sum(axis=1)  # positions disjointes dans le temps
        out[label] = {"trades": pd.concat(trades, ignore_index=True), "daily": daily}
    return out


# --------------------------------------------------------------------------- intervalles de confiance

B = 2000
BLOCK = 10
RNG = np.random.default_rng(20261030)


@lru_cache(maxsize=None)
def _block_index(n: int) -> np.ndarray:
    """Indices d'un bootstrap par blocs mobiles circulaires (B tirages, blocs de BLOCK)."""
    nb = int(np.ceil(n / BLOCK))
    starts = RNG.integers(0, n, size=(B, nb))
    idx = (starts[:, :, None] + np.arange(BLOCK)[None, None, :]) % n
    return idx.reshape(B, -1)[:, :n]


def ci_mean(x: np.ndarray) -> tuple[float, float, float]:
    """Moyenne et IC 95 % (bootstrap par blocs, percentile)."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return np.nan, np.nan, np.nan
    if len(x) < 30:  # trop peu de trades pour un bootstrap par blocs de 10
        return float(x.mean()), np.nan, np.nan
    m = x[_block_index(len(x))].mean(axis=1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def ci_sharpe(r: np.ndarray, ann: float = 252.0) -> tuple[float, float, float]:
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    if len(r) < 20 or r.std() == 0:
        return np.nan, np.nan, np.nan
    s = r[_block_index(len(r))]
    sd = s.std(axis=1)
    sr = np.where(sd > 0, s.mean(axis=1) / np.where(sd > 0, sd, 1) * np.sqrt(ann), np.nan)
    return float(r.mean() / r.std() * np.sqrt(ann)), float(np.nanpercentile(sr, 2.5)), float(np.nanpercentile(sr, 97.5))


def ci_corr(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = np.asarray(x)[ok], np.asarray(y)[ok]
    if len(x) < 20:
        return np.nan, np.nan, np.nan
    idx = _block_index(len(x))
    xs, ys = x[idx], y[idx]
    xs = xs - xs.mean(axis=1, keepdims=True)
    ys = ys - ys.mean(axis=1, keepdims=True)
    c = (xs * ys).sum(axis=1) / np.sqrt((xs ** 2).sum(axis=1) * (ys ** 2).sum(axis=1))
    return float(np.corrcoef(x, y)[0, 1]), float(np.percentile(c, 2.5)), float(np.percentile(c, 97.5))
