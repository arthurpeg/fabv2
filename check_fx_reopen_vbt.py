"""Contrôle croisé du pré-enregistrement n° 6 : rejoue les 18 règles dans
`vbt.Portfolio.from_orders` (même convention que `fab/core.py` : une sortie et une
entrée au même instant fusionnent en un seul ordre, `targetpercent`, frais = demi-coût
aller-retour / prix à chaque ordre) et compare au P&L arithmétique de `fxreopen`.

uv run python check_fx_reopen_vbt.py   → results/fx_reopen/vbt_check.csv, vbt_check.log
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

from fxreopen.data import NY, PAIRS
from fxreopen.evaluate import daily, sharpe, trade_stats, with_cost

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/fx_reopen")
LOG = open(OUT / "vbt_check.log", "w", encoding="utf-8")
MAIN_COST = 3


def say(s: str = "") -> None:
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def session_date(ts: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Date de séance CME (date ET de la reprise de 18:00) ; la sortie de 17:00 ET
    appartient encore à la séance de la veille."""
    et = ts.tz_convert(NY).tz_localize(None)
    return (et - pd.Timedelta(hours=18)).normalize()


def run_pair(t: pd.DataFrame, pip: float) -> tuple[pd.Series, np.ndarray]:
    """Rendement par séance (variation de valeur) et rendement de chaque trade (vbt)."""
    half = t["cost"].values / 2 * pip
    ent = pd.DataFrame({"ts": t["t_in"].values, "price": t["p_in"].values, "target": t["dir"].values,
                        "fee_pts": half, "o": 1})
    ext = pd.DataFrame({"ts": t["t_out"].values, "price": t["p_out"].values, "target": 0.0,
                        "fee_pts": half, "o": 0})
    ev = pd.concat([ent, ext]).sort_values(["ts", "o"])
    g = ev.groupby("ts")
    # sortie puis entrée au même instant (même open) : cible finale, frais des deux côtés
    ev = pd.DataFrame({"price": g["price"].last(), "target": g["target"].last(), "fee_pts": g["fee_pts"].sum()})
    idx = pd.to_datetime(ev.index.values, utc=True)
    n_flip = int((g.size() > 1).sum())
    # frais en fraction de la valeur échangée ; un retournement échange 2× la taille
    traded = np.abs(np.diff(np.r_[0.0, ev["target"].values]))
    fees = ev["fee_pts"].values / ev["price"].values / np.where(traded > 0, traded, 1.0)
    pf = vbt.Portfolio.from_orders(
        close=pd.Series(ev["price"].values, index=idx),
        size=pd.Series(ev["target"].values, index=idx),
        size_type="targetpercent", direction="both", fees=pd.Series(fees, index=idx),
        init_cash=1_000_000.0, freq="1min",
    )
    val = pf.value()
    sess = session_date(val.index)
    day_val = val.groupby(sess).last()
    r = day_val / day_val.shift(1, fill_value=1_000_000.0) - 1
    tr = pf.trades.records_readable.sort_values("Entry Timestamp")
    return r, tr["Return"].values, n_flip


def main() -> None:
    base = {k: pd.read_parquet(OUT / f"trades_{k}.parquet") for k in ("E0", "E1", "E5", "E15", "close", "intra")}
    for t in base.values():
        t["date"] = pd.to_datetime(t["date"])
    rules = {}
    for s in (1, 2, 5):
        for e in (0, 1, 5, 15):
            rules[f"reopen_s{s}_E{e}"] = (base[f"E{e}"], s, MAIN_COST)
    for s in (1, 2, 5):
        rules[f"intra_s{s}"] = (base["intra"], s, "std")
    for s in (1, 2, 5):
        rules[f"close_s{s}_E0"] = (base["close"], s, MAIN_COST)

    D = pd.read_parquet(OUT / "daily_net.parquet")
    cal = D.index
    rows, Dv = [], {}
    say("# Contrôle croisé vectorbt — pré-enregistrement n° 6\n")
    for name, (t0, s, c) in rules.items():
        t = with_cost(t0[t0["gap"].abs() >= s].reset_index(drop=True), c)
        per_pair, max_dtrade, flips, merged = [], 0.0, 0, 0
        for pair, g in t.groupby("pair"):
            g = g.sort_values("t_in")
            r, tr_ret, nf = run_pair(g, PAIRS[pair].pip)
            flips += nf
            if len(tr_ret) == len(g):
                max_dtrade = max(max_dtrade, float(np.abs(tr_ret - g["ret"].values).max()))
            else:  # sortie et entrée de même sens au même instant : vbt garde la position
                assert name.startswith("intra"), (name, pair, len(tr_ret), len(g))
                max_dtrade = np.nan
                merged += len(g) - len(tr_ret)
            per_pair.append(r.reindex(cal, fill_value=0.0))
        dv = sum(per_pair) / len(PAIRS)
        Dv[name] = dv
        diff = (dv - D[name]).abs()
        rows.append({"rule": name, "n": len(t), "flips_merged": flips, "same_side_merged": merged, "max_abs_trade_ret_diff": max_dtrade,
                     "max_abs_daily_diff": float(diff.max()), "corr_daily": float(np.corrcoef(dv, D[name])[0, 1]),
                     "sharpe_arith": sharpe(D[name]), "sharpe_vbt": sharpe(dv),
                     "total_ret_arith_%": float(D[name].sum() * 100), "total_ret_vbt_%": float(dv.sum() * 100)})
        say(f"{name:<15} n={len(t):>5} retournements={flips:>4} continuations={merged:>5} écart max/trade={max_dtrade:.2e} "
            f"écart max/jour={diff.max():.2e} corr={rows[-1]['corr_daily']:.6f} "
            f"SRj arith={rows[-1]['sharpe_arith']:+.3f} vbt={rows[-1]['sharpe_vbt']:+.3f}")
    pd.DataFrame(rows).to_csv(OUT / "vbt_check.csv", index=False)
    pd.DataFrame(Dv).to_parquet(OUT / "daily_net_vbt.parquet")

    # configuration principale, recalculée à partir des trades vbt
    t = with_cost(base["E1"][base["E1"]["gap"].abs() >= 5].reset_index(drop=True), MAIN_COST)
    say(f"\nConfiguration principale (vbt) : SRj={sharpe(Dv['reopen_s5_E1']):+.2f}, "
        f"arith : {trade_stats(t)['mean_net']:+.2f} pips/trade, SRj={sharpe(daily(t, cal)):+.2f}")
    say("fin.")


if __name__ == "__main__":
    main()
