"""Les 4 règles de nuit retenues de la récolte 1, rejouées en entrées horaires avec SL/TP en ATR M15.

uv run python run_recolte1_atr.py   → results/recolte1_atr/ (trades.parquet, by_hour.csv, summary.csv, run.log)

Pour chaque nuit d'une règle, une entrée à chaque heure pleine après le début de la fenêtre
(clôture + 1 h, + 2 h, ...) tant que l'heure précède la fin de la fenêtre, dans le sens de la
règle. Chaque heure d'horloge est une colonne vectorbt indépendante (au plus un trade par nuit).
Sortie : SL, TP, fin de la fenêtre de la règle, ou 17:00 ET (fin de la journée de trading CME,
18:00 → 17:00) si elle arrive avant : aucun trade ne passe d'une journée de trading à l'autre.
ATR = ATR de Wilder 14 périodes sur bougies de 15 min, dernière bougie terminée à l'entrée.
SL/TP en multiples d'ATR (RR 2.5) ; variante sans SL/TP comme référence.
Exécution vectorbt from_signals sur barres 1 min : entrée à la clôture de la barre qui finit à
l'heure d'entrée, stops testés sur high/low des barres suivantes (remplis au prix du stop,
ou à l'ouverture si elle le dépasse). Coût net = 1 tick + 5 $ par aller-retour.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

from recolte1.engine import NY, SPECS, ci_mean, ci_sharpe, load
from recolte1.rules import at, base, monthly, next_month_sign, sessions

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/recolte1_atr")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
VARIANTS = [("SL 2 ATR / TP 5 ATR", 2.0, 5.0), ("SL 1 ATR / TP 2.5 ATR", 1.0, 2.5),
            ("SL 1.5 ATR / TP 3.75 ATR", 1.5, 3.75), ("SL 3 ATR / TP 7.5 ATR", 3.0, 7.5),
            ("sans SL/TP (sortie fin de fenêtre)", np.nan, np.nan)]


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def windows(rule: str) -> tuple[str, pd.DataFrame]:
    """(actif, une ligne par nuit : t_start, t_end UTC, dir)."""
    b = sessions()
    d = b.index
    if rule == "[19] momentum 12-1 sur la nuit (NQ)":
        bb = base("NQ")
        m = monthly(bb, "cc")
        s = next_month_sign(bb, m.shift(1).rolling(11, min_periods=11).sum())
        return "NQ", pd.DataFrame({"t_start": b["t_prev"], "t_end": b["t_open"], "dir": s.reindex(d).fillna(0.0)})
    if rule == "[7] nuit séance propre 13:30→8:20 (GC)":
        return "GC", pd.DataFrame({"t_start": at(d, "13:30", NY).shift(1), "t_end": at(d, "08:20", NY), "dir": 1.0})
    if rule == "[7]/[15] nuit 16:00→9:30 (GC)":
        return "GC", pd.DataFrame({"t_start": b["t_prev"], "t_end": b["t_open"], "dir": 1.0})
    if rule == "[1] CTO 16:15→8:30 (GC)":
        return "GC", pd.DataFrame({"t_start": at(d, "16:15", NY).shift(1), "t_end": at(d, "08:30", NY), "dir": 1.0})
    raise KeyError(rule)


RULES = ["[19] momentum 12-1 sur la nuit (NQ)", "[7] nuit séance propre 13:30→8:20 (GC)",
         "[7]/[15] nuit 16:00→9:30 (GC)", "[1] CTO 16:15→8:30 (GC)"]


def bar_pos(idx: pd.DatetimeIndex, t: pd.Series, slack_min: int = 5) -> np.ndarray:
    """Position de la dernière barre démarrant dans [T - slack, T - 1 min] ; -1 sinon."""
    key = pd.DatetimeIndex(t).as_unit("ns") - pd.Timedelta(minutes=1)
    p = idx.searchsorted(key, side="right") - 1
    ok = (p >= 0) & (idx[np.clip(p, 0, None)] >= key - pd.Timedelta(minutes=slack_min - 1))
    return np.where(ok & pd.notna(t).values, p, -1)


def atr_m15(df: pd.DataFrame, n: int = 14) -> pd.Series:
    """ATR de Wilder sur bougies 15 min, indexé par l'instant de fin de bougie."""
    o = df[["open", "high", "low", "close"]].resample("15min", label="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    pc = o["close"].shift(1)
    tr = pd.concat([o["high"] - o["low"], (o["high"] - pc).abs(), (o["low"] - pc).abs()], axis=1).max(axis=1)
    a = tr.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    a.index = a.index + pd.Timedelta(minutes=15)
    return a


def entries_table(rule: str) -> tuple[str, pd.DataFrame]:
    asset, w = windows(rule)
    w = w.dropna(subset=["t_start", "t_end"])
    w = w[w["dir"] != 0]
    rows = []
    for day, r in w.iterrows():
        t = r["t_start"] + pd.Timedelta(hours=1)
        while t < r["t_end"] - pd.Timedelta(minutes=1):
            rows.append((day, t, r["t_end"], r["dir"]))
            t += pd.Timedelta(hours=1)
    e = pd.DataFrame(rows, columns=["night", "t_in", "t_out", "dir"])
    # intraday : sortie au plus tard à 17:00 ET, fin de la journée de trading CME (18:00 → 17:00)
    loc = e["t_in"].dt.tz_convert(NY)
    eod = loc.dt.normalize() + pd.Timedelta(hours=17)
    eod = eod.where(loc < eod, eod + pd.Timedelta(days=1))
    eod = pd.DatetimeIndex([x.tz_localize(None) for x in eod]).tz_localize(NY).tz_convert("UTC")
    eod = pd.Series(eod, index=e.index)
    e["forced_eod"] = eod < e["t_out"]
    e["t_out"] = e["t_out"].where(~e["forced_eod"], eod)
    e["clock"] = e["t_in"].dt.tz_convert(NY).dt.strftime("%H:%M")
    # 17:00-17:59 ET = pause CME : le prix d'entrée serait celui de 16:59 (journée précédente)
    e = e[~e["clock"].str.startswith("17:")]
    return asset, e


def simulate(asset: str, e: pd.DataFrame) -> pd.DataFrame:
    df = load(asset).copy()
    df.attrs = {}  # load() y range les roulements (Series), ce qui casse resample
    idx = df.index.as_unit("ns")
    e = e.copy()
    e["p_in"] = bar_pos(idx, e["t_in"])
    e["p_out"] = bar_pos(idx, e["t_out"])
    e = e[(e["p_in"] >= 0) & (e["p_out"] > e["p_in"])]
    atr = atr_m15(df)
    a = atr.reindex(pd.DatetimeIndex(e["t_in"]).as_unit("ns"), method="ffill")  # dernière bougie terminée
    e["atr_frac"] = a.values / df["close"].values[e["p_in"].values]
    e = e.dropna(subset=["atr_frac"])
    N = len(df)
    op, hi, lo, cl = (df[c].values for c in ["open", "high", "low", "close"])
    half = SPECS[asset].rt_cost / 2
    fee_net = half / (cl / df["factor"].values)
    out = []
    for clock, g in e.groupby("clock"):
        ent_l = np.zeros(N, bool); ent_s = np.zeros(N, bool); ex = np.zeros(N, bool)
        ent_l[g.loc[g["dir"] > 0, "p_in"].values] = True
        ent_s[g.loc[g["dir"] < 0, "p_in"].values] = True
        ex[g["p_out"].values] = True
        for vname, ksl, ktp in VARIANTS:
            sl = np.full(N, np.nan); tp = np.full(N, np.nan)
            if np.isfinite(ksl):
                sl[g["p_in"].values] = ksl * g["atr_frac"].values
                tp[g["p_in"].values] = ktp * g["atr_frac"].values
            pf = vbt.Portfolio.from_signals(
                close=cl, open=op, high=hi, low=lo,
                entries=ent_l, exits=ex, short_entries=ent_s, short_exits=ex,
                sl_stop=sl, tp_stop=tp, fees=fee_net, size=1.0, size_type="percent",
                init_cash=1_000_000.0, freq="1min",
            )
            rec = pf.trades.records
            rec = rec[rec["status"] == 1]  # fermés
            p_in = rec["entry_idx"]
            m = g.set_index("p_in").reindex(p_in)
            reason = np.where(rec["exit_idx"] == m["p_out"].values,
                              np.where(m["forced_eod"].values, "17:00", "fin fenêtre"),
                              np.where(rec["pnl"] > 0, "TP", "SL"))
            gross = (rec["pnl"] + rec["entry_fees"] + rec["exit_fees"]) / (rec["size"] * rec["entry_price"])
            for label, ret in [("gross", gross), ("net", rec["return"])]:
                out.append(pd.DataFrame({
                    "asset": asset, "clock": clock, "variant": vname, "cost": label,
                    "night": m["night"].values, "dir": np.where(rec["direction"] == 0, 1, -1),
                    "ret": ret, "reason": reason, "entry_idx": p_in,
                }))
    return pd.concat(out, ignore_index=True)


def stats(t: pd.DataFrame, nights: pd.Index) -> dict:
    m, lo, hi = ci_mean(t["ret"].values * 1e4)
    daily = t.groupby("night")["ret"].sum().reindex(nights).fillna(0.0)
    s, slo, shi = ci_sharpe(daily.values)
    return {"n": len(t), "bp": m, "bp_lo": lo, "bp_hi": hi, "win_%": (t["ret"] > 0).mean() * 100,
            "TP_%": (t["reason"] == "TP").mean() * 100, "SL_%": (t["reason"] == "SL").mean() * 100,
            "fin_fenetre_%": (t["reason"] == "fin fenêtre").mean() * 100,
            "sortie_17h_%": (t["reason"] == "17:00").mean() * 100,
            "sharpe": s, "sharpe_lo": slo, "sharpe_hi": shi, "ret_total_%": (np.prod(1 + daily.values) - 1) * 100}


def summarize(T: pd.DataFrame):
    nights = sessions().index
    rows = []
    for (rule, var, cost, clock), g in T.groupby(["rule", "variant", "cost", "clock"]):
        rows.append({"rule": rule, "variant": var, "cost": cost, "clock": clock} | stats(g, nights))
    pd.DataFrame(rows).to_csv(OUT / "by_hour.csv", index=False)
    # toutes heures : capital réparti également entre les heures d'horloge de la règle
    rows = []
    # heures d'horloge régulières seulement (≥ 200 trades) : les autres n'existent que les
    # nuits de jours fériés et diluent le capital
    cnt = T.groupby(["rule", "clock"]).size() / T.groupby(["rule", "clock"])[["variant", "cost"]].apply(
        lambda x: len(x.drop_duplicates()))
    keep = cnt[cnt >= 200].index
    T = T[pd.MultiIndex.from_frame(T[["rule", "clock"]]).isin(keep)]
    for (rule, var, cost), g in T.groupby(["rule", "variant", "cost"]):
        k = g["clock"].nunique()
        st = stats(g.assign(ret=g["ret"] / k), nights)
        m, lo, hi = ci_mean(g["ret"].values * 1e4)
        st |= {"bp_par_trade": m, "bp_par_trade_lo": lo, "bp_par_trade_hi": hi, "heures": k}
        rows.append({"rule": rule, "variant": var, "cost": cost} | st)
    S = pd.DataFrame(rows)
    S.to_csv(OUT / "summary.csv", index=False)
    return S


def main():
    t0 = time.time()
    allt = []
    for rule in RULES:
        asset, e = entries_table(rule)
        log(f"{rule} : {len(e)} entrées prévues, {e['clock'].nunique()} heures d'horloge")
        tr = simulate(asset, e).assign(rule=rule)
        allt.append(tr)
        log(f"  simulé ({time.time() - t0:.0f} s)")
    T = pd.concat(allt, ignore_index=True)
    T.to_parquet(OUT / "trades.parquet")
    S = summarize(T)
    log(S[S["cost"] == "net"][["rule", "variant", "n", "bp_par_trade", "bp_par_trade_lo", "bp_par_trade_hi",
                               "win_%", "TP_%", "SL_%", "sharpe", "sharpe_lo", "sharpe_hi", "ret_total_%"]]
        .round(2).to_string())
    log(f"terminé {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
