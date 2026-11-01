"""Exploratoire (non pré-enregistré, demandé en séance) : règle matinée US sur NQ avec SL/TP en ATR M15.

uv run python run_nq_matin_sltp.py  → results/nq_matin_sltp/ (run.log, summary.csv, trades.csv, by_year.csv)

Règle de [[reports/nq_matin_aprem_report]] / [[PREREGISTRATION_20]] (échec sur ES et YM, au registre) :
matinée X = 9:30 → 11:30 NY ; si |X| > 1 écart-type des 20 séances précédentes, position dans le sens
de X, entrée 11:30 (clôture de la barre 11:29), sortie 16:00 (clôture de la barre 15:59) sauf stop.
Variantes de stops (ATR de Wilder 14 sur bougies 15 min, dernière bougie terminée avant 11:30) :
  SL 1 / TP 1 ATR (RR 1) ; SL 2 / TP 2 ATR ; référence sans stop (sortie 16:00).
Chacune avec le filtre |z| > 1 et sans filtre (tous les jours).
vectorbt Portfolio.from_signals sur barres 1 min, stops sur high/low (SL prioritaire si les deux dans la
même minute), net 1 tick + 5 $ aller-retour. NQ 2010-06 → 2026-08-28 (holdout non touché).
R = rendement / distance du SL (1 ATR pour la référence sans stop).
"""

from __future__ import annotations

import sys
from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd
import vectorbt as vbt

import recolte1.engine as E

E.USE_2010 = True

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/nq_matin_sltp")
NY = "America/New_York"
END = "2026-08-28"
VARIANTS = [("SL 1 / TP 1 ATR", 1.0, 1.0), ("SL 2 / TP 2 ATR", 2.0, 2.0), ("sans stop (16:00)", np.nan, np.nan)]
LINES: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LINES.append(s)


def bar_pos(idx: pd.DatetimeIndex, t: pd.Series, slack_min: int = 5) -> np.ndarray:
    """Comme run_recolte1_atr.bar_pos (non importé : son import réécrit results/recolte1_atr/run.log)."""
    key = pd.DatetimeIndex(t).as_unit("ns") - pd.Timedelta(minutes=1)
    p = idx.searchsorted(key, side="right") - 1
    ok = (p >= 0) & (idx[np.clip(p, 0, None)] >= key - pd.Timedelta(minutes=slack_min - 1))
    return np.where(ok & pd.notna(t).values, p, -1)


def atr_m15(df: pd.DataFrame, n: int = 14) -> pd.Series:
    """Comme run_recolte1_atr.atr_m15 : ATR de Wilder sur bougies 15 min, indexé par la fin de bougie."""
    o = df[["open", "high", "low", "close"]].resample("15min", label="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    pc = o["close"].shift(1)
    tr = pd.concat([o["high"] - o["low"], (o["high"] - pc).abs(), (o["low"] - pc).abs()], axis=1).max(axis=1)
    a = tr.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    a.index = a.index + pd.Timedelta(minutes=15)
    return a


def entries(df: pd.DataFrame) -> pd.DataFrame:
    sched = xc.get_calendar("XNYS").schedule.loc[str(df.index[0].date()):END]
    d = pd.DatetimeIndex(sched.index)
    e = pd.DataFrame(index=d)
    e["t_open"], e["t_in"], e["t_out"] = sched["open"], E.at(d, "11:30", NY), sched["close"]
    e = e[e["t_out"].dt.tz_convert(NY).dt.hour == 16]  # demi-séances exclues
    idx = df.index.as_unit("ns")
    for k in ["open", "in", "out"]:
        e[f"p_{k}"] = bar_pos(idx, e[f"t_{k}"])
    e = e[(e[["p_open", "p_in", "p_out"]] >= 0).all(axis=1)].copy()
    cl = df["close"].values
    e["x"] = cl[e["p_in"].values] / cl[e["p_open"].values] - 1
    e["z"] = e["x"] / e["x"].rolling(20).std().shift(1)
    e["dir"] = np.sign(e["x"])
    atr = atr_m15(df).reindex(pd.DatetimeIndex(e["t_in"]).as_unit("ns"), method="ffill").values
    e["atr_frac"] = atr / cl[e["p_in"].values]
    e["atr_pts"] = atr / df["factor"].values[e["p_in"].values]
    return e.dropna(subset=["z", "atr_frac"])[lambda t: t["dir"] != 0]


def run(df, e, k_sl, k_tp, label, filt) -> pd.DataFrame:
    N = len(df)
    op, hi, lo, cl = (df[c].values for c in ["open", "high", "low", "close"])
    fee = E.SPECS["NQ"].rt_cost / 2 / (cl / df["factor"].values)
    ent_l = np.zeros(N, bool); ent_s = np.zeros(N, bool); ex = np.zeros(N, bool)
    ent_l[e.loc[e["dir"] > 0, "p_in"].values] = True
    ent_s[e.loc[e["dir"] < 0, "p_in"].values] = True
    ex[e["p_out"].values] = True
    sl = np.full(N, np.nan); tp = np.full(N, np.nan)
    sl[e["p_in"].values] = k_sl * e["atr_frac"].values
    tp[e["p_in"].values] = k_tp * e["atr_frac"].values
    pf = vbt.Portfolio.from_signals(close=cl, open=op, high=hi, low=lo, entries=ent_l, exits=ex,
                                    short_entries=ent_s, short_exits=ex, sl_stop=sl, tp_stop=tp,
                                    fees=fee, size=1.0, size_type="percent", init_cash=1_000_000.0, freq="1min")
    rec = pf.trades.records
    rec = rec[rec["status"] == 1]
    assert len(rec) == len(e)
    m = e.reset_index(names="day").set_index("p_in").reindex(rec["entry_idx"])
    reason = np.where(rec["exit_idx"] == m["p_out"].values, "16:00", np.where(rec["pnl"] > 0, "TP", "SL"))
    gross = (rec["pnl"] + rec["entry_fees"] + rec["exit_fees"]) / (rec["size"] * rec["entry_price"])
    risk = (k_sl if np.isfinite(k_sl) else 1.0) * m["atr_frac"].values
    out = []
    for cost, r in (("brut", np.asarray(gross)), ("net", np.asarray(rec["return"]))):
        out.append(pd.DataFrame({"variante": label, "filtre": filt, "coût": cost, "jour": m["day"].values,
                                 "dir": np.where(rec["direction"] == 0, 1, -1), "ret": r, "R": r / risk,
                                 "sortie": reason, "atr_pts": m["atr_pts"].values}))
    return pd.concat(out, ignore_index=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = E.load("NQ").copy()
    df.attrs = {}
    e = entries(df)
    say(f"NQ, {len(e)} séances, {e.index[0].date()} → {e.index[-1].date()} ; |z| > 1 : {int((e['z'].abs() > 1).sum())} jours")
    say(f"ATR M15 à 11:30 (points NQ réels) : médiane {e['atr_pts'].median():.1f}, p10 {e['atr_pts'].quantile(.1):.1f}, "
        f"p90 {e['atr_pts'].quantile(.9):.1f} ; coût A/R {E.SPECS['NQ'].rt_cost} point")
    T = pd.concat([run(df, ee, s, t, lab, filt)
                   for filt, ee in [("|z| > 1", e[e["z"].abs() > 1]), ("aucun", e)]
                   for lab, s, t in VARIANTS], ignore_index=True)
    T.to_csv(OUT / "trades.csv", index=False)

    rows = []
    for (v, f, c), t in T.groupby(["variante", "filtre", "coût"], sort=False):
        t = t.sort_values("jour")
        bp = t["ret"].to_numpy() * 1e4
        m, lo, hi = E.ci_mean(bp)
        R = t["R"].to_numpy()
        yrs = (t["jour"].iloc[-1] - t["jour"].iloc[0]).days / 365.25
        cum = t["ret"].cumsum()
        win, loss = bp[bp > 0], bp[bp <= 0]
        rows.append(dict(variante=v, filtre=f, coût=c, trades=len(t), bp_trade=m, bp_lo=lo, bp_hi=hi,
                         t=bp.mean() / bp.std() * np.sqrt(len(bp)), R_trade=R.mean(),
                         bp_2010_17=bp[t["jour"].dt.year.values <= 2017].mean(),
                         bp_2018_26=bp[t["jour"].dt.year.values >= 2018].mean(),
                         bp_2023_26=bp[t["jour"].dt.year.values >= 2023].mean(),
                         sharpe=bp.mean() / bp.std() * np.sqrt(len(bp) / yrs),
                         max_dd_bp=float((cum - cum.cummax()).min() * 1e4), gagnants=(bp > 0).mean(),
                         PF=win.sum() / -loss.sum(), TP=(t["sortie"] == "TP").mean(),
                         SL=(t["sortie"] == "SL").mean(), fin=(t["sortie"] == "16:00").mean()))
    S = pd.DataFrame(rows)
    S.to_csv(OUT / "summary.csv", index=False)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    for c in ("net", "brut"):
        say(f"\n== {c} ==")
        say(S[S["coût"] == c].drop(columns="coût").round(3).to_string(index=False))
    net = T[(T["coût"] == "net")].copy()
    net["année"] = net["jour"].dt.year
    Y = net.pivot_table(index="année", columns=["filtre", "variante"], values="ret", aggfunc="sum", sort=False) * 1e4
    Y.to_csv(OUT / "by_year.csv")
    say("\nbp nets par année (somme des trades)")
    say(Y.round(0).to_string())
    (OUT / "run.log").write_text("\n".join(LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
