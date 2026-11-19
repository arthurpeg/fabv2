"""Exploratoire (non pré-enregistré, compteur +7) : règle NQ de nuit avec stop au bord du range du soir au lieu de l'ATR.

uv run python run_nq_nuit_sl_range.py  → results/nq_nuit_sl_range/ (run.log, summary.csv, trades.csv, by_year.csv)

Règle : momentum 12-1 (signe du mois), entrée 20:00 ET, sortie 9:30 ET, 2011-07 → 2026-08 (holdout non touché).
Range du soir = barres 1 min de 17:00 ET (clôture CME ; en pratique reprise 18:00) jusqu'à la barre d'entrée comprise.
SL = plus bas du range si long, plus haut si short ; 1 R = distance entrée → SL. TP = k R, k = 1 ; 1,25 ; … ; 2,5,
plus « sans TP » (sortie 9:30). Référence : SL 2 ATR / TP 5 ATR (ATR 14 en M15), même moteur.
Trades vectorbt (Portfolio.from_signals sur barres 1 min, entrée à la clôture de 19:59, stops sur high/low suivants).
Net = 1 tick + 5 $ aller-retour. Nuits où la distance au SL < 2 ticks : écartées (stop dans le bruit, R indéfini).
Attention : importer run_prereg12 réécrit results/prereg12/run.log (vide de toute façon).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

import run_prereg12 as Q  # historique 2010-2015 actif
import run_recolte1_atr as A
from recolte1.engine import NY, SPECS, ci_mean, ci_sharpe, load
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/nq_nuit_sl_range")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
TPS = (1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, np.nan)
MIN_TICKS = 2
TICK = 0.25


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def run(df, e, sl_frac, tp_frac, label) -> pd.DataFrame:
    """Une colonne vectorbt, stops en fraction du prix d'entrée (par trade)."""
    N = len(df)
    op, hi, lo, cl = (df[c].values for c in ["open", "high", "low", "close"])
    fee_net = SPECS["NQ"].rt_cost / 2 / (cl / df["factor"].values)
    ent_l = np.zeros(N, bool); ent_s = np.zeros(N, bool); ex = np.zeros(N, bool)
    ent_l[e.loc[e["dir"] > 0, "p_in"].values] = True
    ent_s[e.loc[e["dir"] < 0, "p_in"].values] = True
    ex[e["p_out"].values] = True
    sl = np.full(N, np.nan); tp = np.full(N, np.nan)
    sl[e["p_in"].values] = sl_frac
    tp[e["p_in"].values] = tp_frac
    pf = vbt.Portfolio.from_signals(close=cl, open=op, high=hi, low=lo, entries=ent_l, exits=ex,
                                    short_entries=ent_s, short_exits=ex, sl_stop=sl, tp_stop=tp,
                                    fees=fee_net, size=1.0, size_type="percent", init_cash=1_000_000.0, freq="1min")
    rec = pf.trades.records
    rec = rec[rec["status"] == 1]
    m = e.set_index("p_in").reindex(rec["entry_idx"])
    reason = np.where(rec["exit_idx"] == m["p_out"].values, "9:30", np.where(rec["pnl"] > 0, "TP", "SL"))
    gross = (rec["pnl"] + rec["entry_fees"] + rec["exit_fees"]) / (rec["size"] * rec["entry_price"])
    out = []
    for cost, ret in (("gross", gross), ("net", rec["return"])):
        out.append(pd.DataFrame({"variant": label, "cost": cost, "night": m["night"].values,
                                 "dir": np.where(rec["direction"] == 0, 1, -1), "ret": np.asarray(ret),
                                 "R": np.asarray(ret) / m["risk_frac"].values, "reason": reason,
                                 "dist_atr": m["dist_atr"].values}))
    return pd.concat(out, ignore_index=True)


def main() -> None:
    df = load("NQ").copy()
    df.attrs = {}
    idx = df.index.as_unit("ns")
    e = Q.table(at(Q.D, "20:00", NY, -1), Q.B["t_open"], Q.MOM, "20:00")
    e["p_in"] = A.bar_pos(idx, e["t_in"])
    e["p_out"] = A.bar_pos(idx, e["t_out"])
    e = e[(e["p_in"] >= 0) & (e["p_out"] > e["p_in"])].copy()
    p17 = idx.searchsorted(pd.DatetimeIndex(e["t_in"]).as_unit("ns") - pd.Timedelta(hours=3), side="left")
    hi, lo, cl = df["high"].values, df["low"].values, df["close"].values
    e["r_hi"] = [hi[a:b + 1].max() for a, b in zip(p17, e["p_in"].values)]
    e["r_lo"] = [lo[a:b + 1].min() for a, b in zip(p17, e["p_in"].values)]
    e["px"] = cl[e["p_in"].values]
    e["range_min"] = (e["p_in"].values - p17 + 1)
    dist = np.where(e["dir"] > 0, e["px"] - e["r_lo"], e["r_hi"] - e["px"])
    # tick en prix ajusté : on ramène à des points réels avec le facteur de roulement
    dist_pts = dist / df["factor"].values[e["p_in"].values]
    atr = A.atr_m15(df).reindex(pd.DatetimeIndex(e["t_in"]).as_unit("ns"), method="ffill").values
    e["atr_frac"] = atr / e["px"].values
    e["sl_frac"] = dist / e["px"].values
    e["dist_pts"] = dist_pts
    e["dist_atr"] = dist / atr
    n_all = len(e)
    e = e.dropna(subset=["atr_frac"])
    small = e["dist_pts"] < MIN_TICKS * TICK
    say("Règle NQ de nuit, entrée 20:00 ET, momentum 12-1, sortie 9:30 ET ; SL au bord du range 17:00→20:00 ; vectorbt")
    say(f"{n_all} nuits avec entrée ; {int(small.sum())} écartées (distance au SL < {MIN_TICKS} ticks)")
    say(f"Distance au SL (points NQ réels) : médiane {e.loc[~small, 'dist_pts'].median():.1f}, "
        f"p10 {e.loc[~small, 'dist_pts'].quantile(.1):.1f}, p90 {e.loc[~small, 'dist_pts'].quantile(.9):.1f} ; "
        f"en ATR M15 : médiane {e.loc[~small, 'dist_atr'].median():.2f}, p10 {e.loc[~small, 'dist_atr'].quantile(.1):.2f}, "
        f"p90 {e.loc[~small, 'dist_atr'].quantile(.9):.2f} (référence : 2 ATR)")
    say(f"Durée du range (min de barres) : médiane {e['range_min'].median():.0f}")
    er = e[~small].copy()
    er["risk_frac"] = er["sl_frac"]
    trades = [run(df, er, er["sl_frac"].values, k * er["sl_frac"].values if np.isfinite(k) else np.nan,
                  f"range, TP {k:g} R" if np.isfinite(k) else "range, sans TP") for k in TPS]
    # référence ATR, sur toutes les nuits et sur les mêmes nuits que la variante range
    ea = e.copy()
    ea["risk_frac"] = 2 * ea["atr_frac"]
    trades.append(run(df, ea, 2 * ea["atr_frac"].values, 5 * ea["atr_frac"].values, "réf. SL 2 / TP 5 ATR"))
    T = pd.concat(trades, ignore_index=True)
    T["night"] = pd.to_datetime(T["night"])
    T.to_csv(OUT / "trades.csv", index=False)

    years = (Q.NIGHTS[-1] - Q.NIGHTS[0]).days / 365.25
    rows = []
    for (v, cost), t in T.groupby(["variant", "cost"], sort=False):
        r = t.groupby("night")["ret"].sum().reindex(Q.NIGHTS).fillna(0.0)
        R = t["R"].to_numpy()
        mR, loR, hiR = ci_mean(R)
        sh, slo, shi = ci_sharpe(r.values)
        cumR = t.sort_values("night")["R"].cumsum()
        a, b = t[t.night < "2016-01-01"]["R"].mean(), t[t.night >= "2016-01-01"]["R"].mean()
        win, loss = R[R > 0], R[R <= 0]
        rows.append(dict(variante=v, coût=cost, trades=len(t), R_par_trade=mR, R_lo=loR, R_hi=hiR,
                         R_2011_15=a, R_2016_26=b, R_par_an=R.sum() / years,
                         max_dd_R=float((cumR - cumR.cummax()).min()), pb_par_nuit=r.mean() * 1e4,
                         sharpe=sh, sharpe_lo=slo, sharpe_hi=shi, gagnants=(R > 0).mean(),
                         PF=win.sum() / -loss.sum() if loss.sum() < 0 else np.nan,
                         TP=(t["reason"] == "TP").mean(), SL=(t["reason"] == "SL").mean(), sortie_930=(t["reason"] == "9:30").mean()))
    S = pd.DataFrame(rows)
    S.to_csv(OUT / "summary.csv", index=False)
    for cost in ("net", "gross"):
        say(f"\n== {cost} ==")
        say(f"{'variante':<22} {'trades':>6} {'R/trade [IC 95 %]':>25} {'11-15':>7} {'16-26':>7} {'R/an':>6} {'DD R':>7} "
            f"{'pb/nuit':>7} {'Sharpe [IC 95 %]':>22} {'gagn.':>6} {'PF':>5} {'TP':>6} {'SL':>6} {'9:30':>6}")
        for x in S[S["coût"] == cost].itertuples():
            say(f"{x.variante:<22} {x.trades:>6} {x.R_par_trade:>+8.3f} [{x.R_lo:+.3f} ; {x.R_hi:+.3f}] {x.R_2011_15:>+7.3f} "
                f"{x.R_2016_26:>+7.3f} {x.R_par_an:>6.1f} {x.max_dd_R:>7.1f} {x.pb_par_nuit:>7.2f} "
                f"{x.sharpe:>6.2f} [{x.sharpe_lo:+.2f} ; {x.sharpe_hi:+.2f}] {x.gagnants:>6.1%} {x.PF:>5.2f} "
                f"{x.TP:>6.1%} {x.SL:>6.1%} {x.sortie_930:>6.1%}")

    net = T[T.cost == "net"]
    Y = net.pivot_table(index=net.night.dt.year, columns="variant", values="R", aggfunc="sum", sort=False)
    Y.to_csv(OUT / "by_year.csv")
    say("\nR nets par année :")
    say(Y.round(1).to_string())

    # selon la largeur du stop (terciles de distance en ATR), TP 2 R et sans TP, net
    say("\nR net par trade selon la distance au SL (terciles en ATR M15) :")
    q = net[net.variant.str.startswith("range")].copy()
    q["tercile"] = pd.qcut(q["dist_atr"], 3, labels=["serré", "moyen", "large"])
    say(q.pivot_table(index="variant", columns="tercile", values="R", aggfunc="mean", observed=True, sort=False).round(3).to_string())


if __name__ == "__main__":
    main()
