"""Pré-enregistrement n° 20 : matinée US 9:30 → 11:30 (|z| > 1) → position jusqu'à 16:00, sur ES et YM.

uv run python run_prereg20.py   → results/prereg20/ (run.log, results.csv, by_year.csv, trades.csv)

Règle, critères et interdits : PREREGISTRATION_20.md (commité avant calcul).
"""

from __future__ import annotations

from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd

import recolte1.engine as E

E.USE_2010 = True

import run_nq_sessions_corr as S  # noqa: E402

OUT = Path("results/prereg20")
NY = "America/New_York"
END = "2026-08-28"


def p_one_sided(x: np.ndarray) -> float:
    """Comme run_prereg10 (non importé : son import réécrit results/prereg10/run.log)."""
    x = x[np.isfinite(x)]
    m = (x - x.mean())[E._block_index(len(x))].mean(axis=1)
    return float((m >= x.mean()).mean())


def bounds(name: str) -> pd.DataFrame:
    df = E.load(name)
    sched = xc.get_calendar("XNYS").schedule.loc[str(df.index[0].date()):END]
    d = pd.DatetimeIndex(sched.index)
    b = pd.DataFrame(index=d)
    b["t_open"] = sched["open"]
    b["t_mid"] = E.at(d, "11:30", NY)
    b["t_close"] = sched["close"]
    b = b[b["t_close"].dt.tz_convert(NY).dt.hour == 16]  # demi-séances exclues
    for k in ["open", "mid", "close"]:
        b[f"p_{k}"], b[f"f_{k}"] = E.price_at(name, b[f"t_{k}"])
    return b


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log = S.log
    rows, years, trades = [], [], []
    for name in ["ES", "YM"]:
        b = bounds(name)
        cost = E.SPECS[name].rt_cost
        x = S.ret(b, "open", "mid")
        z = x / x.rolling(20).std().shift(1)
        log(f"{name} : {len(b)} séances pleines, {b.index[0].date()} → {b.index[-1].date()}, coût {cost} point A/R")
        st, net = S.follow(b[z.abs() > 1], ("open", "mid"), ("mid", "close"), cost_pts=cost, series=True)
        st_all = S.follow(b, ("open", "mid"), ("mid", "close"), cost_pts=cost)
        d = S.describe(x, S.ret(b, "mid", "close"))
        bp = net.values * 1e4
        m, lo, hi = E.ci_mean(bp)
        y = net.groupby(net.index.year).sum() * 1e4
        tpy = len(net) / ((net.index[-1] - net.index[0]).days / 365.25)
        cum = net.cumsum()
        rows.append({
            "actif": name, "n_trades": len(net), "trades_par_an": tpy,
            "net_bp": m, "ic_lo": lo, "ic_hi": hi, "p_unilatéral": p_one_sided(bp),
            "net_2010_2017_bp": net[net.index.year <= 2017].mean() * 1e4,
            "net_2018_2026_bp": net[net.index.year >= 2018].mean() * 1e4,
            "brut_bp": st["gross_bp"], "sharpe_reel": net.mean() / net.std() * np.sqrt(tpy),
            "bp_par_an": y.loc[2011:2025].mean(), "annees_pos_2011_2025": int((y.loc[2011:2025] > 0).sum()),
            "max_dd_bp": float((cum - cum.cummax()).min() * 1e4),
            "sans_seuil_net_bp": st_all["net_bp"], "sans_seuil_t": st_all["t_net"],
            "pearson_X_Y": d["pearson"], "t_pente_HC": d["t_beta_hc"],
        })
        years.append(y.rename(name))
        trades.append(pd.DataFrame({"actif": name, "jour": net.index, "net_bp": bp}))
    R = pd.DataFrame(rows)
    o = R.sort_values("p_unilatéral")
    adj = np.minimum(np.maximum.accumulate(o["p_unilatéral"].values * np.array([2, 1])), 1)
    R.loc[o.index, "p_holm"] = adj
    R["critère"] = (R["p_holm"] < 0.05) & (R["net_2010_2017_bp"] > 0) & (R["net_2018_2026_bp"] > 0)
    n_ok = int(R["critère"].sum())
    verdict = {2: "SUCCÈS", 1: "SUCCÈS PARTIEL", 0: "ÉCHEC"}[n_ok]

    pd.set_option("display.width", 250)
    log("\n" + R.round(4).T.to_string())
    log("\nbp nets par année (somme des trades)")
    log(pd.concat(years, axis=1).round(1).to_string())
    log(f"\nVerdict pré-enregistré : {verdict} ({n_ok} marché(s) sur 2 remplissent les critères 1 et 2)")
    R.to_csv(OUT / "results.csv", index=False)
    pd.concat(years, axis=1).to_csv(OUT / "by_year.csv")
    pd.concat(trades).to_csv(OUT / "trades.csv", index=False)
    (OUT / "run.log").write_text("\n".join(S.LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
