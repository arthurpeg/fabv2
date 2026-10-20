"""Pré-enregistrement n° 9 : momentum de fin de séance après un grand mouvement (Shum et al.), ES et NQ.

uv run python run_letf.py   → results/letf/ (run.log, metrics_full.csv, vbt_summary.csv, parquet, equity.png)
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from asym.backtest import daily_returns, net_returns, simulate  # noqa: E402
from asym.metrics import full_metrics  # noqa: E402
from fxreopen.evaluate import bootstrap_p, dsr, reality_check, sharpe  # noqa: E402
from letf.rules import days, load, trades  # noqa: E402
from run_asym import permutation_p  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/letf")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")

TIMES = ("14:15", "14:30", "14:45", "15:30")
THRESH = (0.02, 0.01)
STD = ("pts", 0.25 + 5.0 / 50)  # ES et NQ : 1 tick (0,25) + 5 $ / point (50 $ et 20 $)
COST = {"ES": ("pts", 0.25 + 5.0 / 50), "NQ": ("pts", 0.25 + 5.0 / 20)}
GRID = (0, 1, 2, 5)
PRIMARY = "ES_1430_s2"
N_PREREG, N_GLOBAL = 16, 224
WINDOWS = {"2016-2020": ("2016-01-01", "2020-12-31"), "2021-2026-08": ("2021-01-01", "2026-12-31"),
           "tout": ("2016-01-01", "2026-12-31")}


def say(s: str = "") -> None:
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def name(mkt: str, T: str, s: float) -> str:
    return f"{mkt}_{T.replace(':', '')}_s{int(s * 100)}"


def main() -> None:
    say("# Pré-enregistrement n° 9 — momentum de fin de séance après un grand mouvement (ETF à levier)\n")
    rules, cals = {}, {}
    for mkt in ("ES", "NQ"):
        D = days(load(mkt), TIMES)
        cals[mkt] = pd.DatetimeIndex(D.index)
        for T in TIMES:
            for s in THRESH:
                rules[name(mkt, T, s)] = (trades(D, T, s), COST[mkt], mkt)
    say(f"Séances complètes : ES {len(cals['ES'])}, NQ {len(cals['NQ'])}\n")

    say("## Jours déclencheurs par an (T = 14:30)")
    for k in ("ES_1430_s2", "NQ_1430_s2", "ES_1430_s1"):
        t = rules[k][0]
        say(f"{k}: " + ", ".join(f"{y}:{n}" for y, n in t.groupby(t['date'].dt.year).size().items())
            + f" | total={len(t)} | part long={100 * (t['dir'] > 0).mean():.0f}%")

    say("\n## Backtest vectorbt (1×) — coût principal 1 tick + 5 $ et grille")
    D, rows, vrows, curves = {}, [], [], {}
    for k, (t, c, mkt) in rules.items():
        t.to_parquet(OUT / f"trades_{k}.parquet")
        for cc in (c, *GRID):
            pf = simulate(t, cc)
            r = daily_returns(pf, t, cals[mkt])
            lab = "std" if isinstance(cc, tuple) else f"{cc}pb"
            for w, (a, b) in WINDOWS.items():
                rw = r[(r.index >= a) & (r.index <= b)]
                eq = (1 + rw).cumprod()
                vrows.append({"rule": k, "cost": lab, "window": w, "total_pct": 100 * (eq.iloc[-1] - 1),
                              "ann_pct": 100 * 252 * rw.mean(), "sharpe": sharpe(rw),
                              "maxdd_pct": 100 * float((eq / eq.cummax() - 1).min())})
            if cc == c:
                D[k] = r
                curves[k] = (1 + r).cumprod()
                for row in full_metrics(r, net_returns(t, c), t["date"], WINDOWS):
                    rows.append({"rule": k, **row})
            st = vrows[-1]
            say(f"{k:<12} coût {lab:>4} | n={len(t):>4} total={st['total_pct']:+7.1f}% annuel={st['ann_pct']:+6.2f}% "
                f"Sharpe={st['sharpe']:+5.2f} DDmax={st['maxdd_pct']:+6.1f}%")
    M = pd.DataFrame(rows)
    M.to_csv(OUT / "metrics_full.csv", index=False)
    pd.DataFrame(vrows).to_csv(OUT / "vbt_summary.csv", index=False)
    D = pd.DataFrame(D)
    D.to_parquet(OUT / "vbt_daily_net.parquet")

    say("\n## Métriques complètes, coût principal")
    pd.set_option("display.width", 260)
    pd.set_option("display.max_columns", 40)
    say(M.round(2).to_string(index=False))

    r = D[PRIMARY]
    yr = r.groupby(r.index.year).apply(lambda s: (1 + s).prod() - 1)
    say(f"\n{PRIMARY} par année (%) : " + ", ".join(f"{y}:{100 * v:+.1f}" for y, v in yr.items()))
    t = rules[PRIMARY][0]
    x = net_returns(t, rules[PRIMARY][1])
    ex20 = t["date"].dt.year != 2020
    say(f"{PRIMARY} hors 2020 : n={int(ex20.sum())} moyenne={1e4 * x[ex20.values].mean():+.1f} pb/trade")

    say("\n## Tests au coût principal")
    Dz = D.fillna(0.0)
    res = {}
    for k, (t, c, mkt) in rules.items():
        d16, _ = dsr(Dz, k, N_PREREG)
        res[k] = {"p_boot": bootstrap_p(D[k].dropna()), "p_perm": permutation_p(t, c) if len(t) else np.nan,
                  "dsr16": d16, "dsr224": dsr(Dz, k, N_GLOBAL)[0]}
        say(f"{k:<12} n={len(t):>4} Sharpe={sharpe(D[k]):+5.2f} p_boot={res[k]['p_boot']:.4f} "
            f"p_perm={res[k]['p_perm']:.4f} DSR16={d16:.3f} DSR224={res[k]['dsr224']:.3f}")
    p_rc, best, st = reality_check(Dz)
    say(f"Reality Check (16 règles) : p={p_rc:.4f}, meilleure={best}, t={st:.2f}")

    say("\n## Critères")
    for k, label in ((PRIMARY, "PRINCIPALE"), ("NQ_1430_s2", "réplication")):
        t, c, _ = rules[k]
        h = M[(M["rule"] == k) & M["window"].isin(["2016-2020", "2021-2026-08"])]
        c1 = bool(((h["avg_bp"] > 0) & (h["pf"] > 1)).all()) and len(h) == 2
        c2, c3, c4 = res[k]["p_boot"] < 0.05, res[k]["p_perm"] < 0.05, res[k]["dsr16"] > 0.95
        verdict = "SURVIT" if all((c1, c2, c3, c4)) else "REJETÉ"
        say(f"{k} ({label}) : (1) deux moitiés={c1} (2) bootstrap={c2} (3) permutation={c3} (4) DSR={c4} → {verdict}")
    for mkt in ("ES", "NQ"):
        g = {T: M[(M["rule"] == name(mkt, T, 0.02)) & (M["window"] == "tout")]["avg_bp"].iloc[0] for T in TIMES}
        g1 = M[(M["rule"] == name(mkt, "14:30", 0.01)) & (M["window"] == "tout")]["avg_bp"].iloc[0]
        say(f"Profil {mkt} (2 %, pb/trade) : " + ", ".join(f"{T}:{v:+.1f}" for T, v in g.items())
            + f" | 15:30 < 14:30 : {g['15:30'] < g['14:30']} | seuil 1 % (14:30) = {g1:+.1f} < 2 % : {g1 < g['14:30']}")

    fig, ax = plt.subplots(figsize=(10, 5))
    for k in ("ES_1415_s2", "ES_1430_s2", "ES_1445_s2", "ES_1530_s2", "NQ_1430_s2"):
        ax.plot(curves[k].index, curves[k].values, label=k, lw=1)
    ax.axhline(1, color="grey", lw=0.5)
    ax.set_title("Momentum de fin de séance après |r| ≥ 2 % (vectorbt, coût 1 tick + 5 $)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "equity.png", dpi=120)
    say("\nfin.")


if __name__ == "__main__":
    main()
