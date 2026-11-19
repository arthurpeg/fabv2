"""Backtest vectorbt du pré-enregistrement n° 6 (Tolušić 2026, futures CME).

Mêmes trades que `run_fx_reopen.py` (lus dans results/fx_reopen/trades_*.parquet),
exécutés dans `vbt.Portfolio.from_orders` : 4 paires, 1/4 du capital chacune.

uv run python run_fx_reopen_vbt.py   → results/fx_reopen/vbt_*.csv, vbt_run.log, vbt_equity.png
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from fxreopen.backtest import max_drawdown, session_returns, simulate, trade_table  # noqa: E402
from fxreopen.evaluate import bootstrap_p, dsr, sharpe, with_cost  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/fx_reopen")
LOG = open(OUT / "vbt_run.log", "w", encoding="utf-8")
COSTS = (0, 2, 3, 5, 8)
MAIN_COST = 3
PRIMARY = "reopen_s5_E1"
WINDOWS = {
    "2016-2018": ("2016-01-01", "2018-12-31"),
    "2019-2026-01": ("2019-01-01", "2026-01-31"),
    "2026-02+": ("2026-02-01", "2026-12-31"),
    "tout": ("2016-01-01", "2026-12-31"),
}


def say(s: str = "") -> None:
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def rules() -> dict[str, tuple[pd.DataFrame, object]]:
    base = {k: pd.read_parquet(OUT / f"trades_{k}.parquet") for k in ("E0", "E1", "E5", "E15", "close", "intra")}
    out = {}
    for s in (1, 2, 5):
        for e in (0, 1, 5, 15):
            t = base[f"E{e}"]
            out[f"reopen_s{s}_E{e}"] = (t[t["gap"].abs() >= s].reset_index(drop=True), MAIN_COST)
    for s in (1, 2, 5):
        t = base["intra"]
        out[f"intra_s{s}"] = (t[t["gap"].abs() >= s].reset_index(drop=True), "std")
    for s in (1, 2, 5):
        t = base["close"]
        out[f"close_s{s}_E0"] = (t[t["gap"].abs() >= s].reset_index(drop=True), MAIN_COST)
    return out


def window_stats(r: pd.Series, tr: pd.DataFrame, w: str) -> dict:
    a, b = WINDOWS[w]
    rw = r[(r.index >= a) & (r.index <= b)]
    tw = tr[(tr["date"] >= a) & (tr["date"] <= b)]
    pnl = tw["PnL"]
    loss = -pnl[pnl < 0].sum()
    return {
        "window": w, "trades": len(tw),
        "total_ret_%": 100 * float((1 + rw).prod() - 1),
        "ann_ret_%": 100 * float(rw.mean() * 252),
        "sharpe": sharpe(rw), "max_dd_%": 100 * max_drawdown(rw),
        "win_%": 100 * float((pnl > 0).mean()) if len(tw) else np.nan,
        "pf": float(pnl[pnl > 0].sum() / loss) if loss > 0 else np.nan,
        "mean_trade_bp": 1e4 * float(tw["Return"].mean()) if len(tw) else np.nan,
    }


def main() -> None:
    R = rules()
    cal = pd.read_parquet(OUT / "daily_net.parquet").index
    say("# Backtest vectorbt — pré-enregistrement n° 6 (futures CME 6E/6B/6A/6J, 1/4 du capital par paire)\n")
    rows, D, curves = [], {}, {}
    for name, (t0, c_main) in R.items():
        costs = ["std", 0] if c_main == "std" else COSTS
        for c in costs:
            pf = simulate(with_cost(t0, c))
            r = session_returns(pf, cal)
            tr = trade_table(pf)
            if c == c_main:
                D[name] = r
                if name == PRIMARY:
                    # stats natives vbt au coût principal ; on garde celles qui portent sur les
                    # trades et la valeur : l'index est fait des instants d'ordre (freq fictive
                    # de 1 min), donc Sharpe, durées et Calmar natifs n'ont pas de sens ici
                    keep = ["Start Value", "End Value", "Total Return [%]", "Max Drawdown [%]",
                            "Total Fees Paid", "Total Trades", "Win Rate [%]", "Best Trade [%]",
                            "Worst Trade [%]", "Avg Winning Trade [%]", "Avg Losing Trade [%]",
                            "Profit Factor", "Expectancy"]
                    native = pf.stats()[keep].to_string()
            if name in (PRIMARY, "reopen_s5_E0", "reopen_s5_E15") and c in (0, MAIN_COST):
                curves[f"{name} coût {c}"] = (1 + r).cumprod()
            for w in WINDOWS:
                rows.append({"rule": name, "cost": c, **window_stats(r, tr, w)})
            st = rows[-1]
            say(f"{name:<15} coût {str(c):>3} | trades={st['trades']:>5} rendement total={st['total_ret_%']:+7.2f}% "
                f"annuel={st['ann_ret_%']:+6.2f}% Sharpe={st['sharpe']:+5.2f} DDmax={st['max_dd_%']:+6.2f}% "
                f"gagnants={st['win_%']:5.1f}% PF={st['pf']:.2f} moyen={st['mean_trade_bp']:+.2f} pb")
        if name == PRIMARY:
            say(f"\npf.stats() vbt, {PRIMARY} à {MAIN_COST} pips :\n" + native + "\n")
    S = pd.DataFrame(rows)
    S.to_csv(OUT / "vbt_summary.csv", index=False)
    D = pd.DataFrame(D)
    D.to_parquet(OUT / "vbt_daily_net.parquet")

    say(f"\n## Configuration principale {PRIMARY}, par fenêtre (vbt)")
    sub = S[(S["rule"] == PRIMARY) & S["cost"].isin([0, 3, 5])]
    say(sub.drop(columns="rule").round(2).to_string(index=False))

    say("\n## Tests sur les rendements vbt au coût principal")
    for k in D:
        d18, sr0 = dsr(D, k, 18)
        say(f"{k:<15} Sharpe={sharpe(D[k]):+5.2f} p_boot={bootstrap_p(D[k], reps=2000):.4f} "
            f"DSR18={d18:.3f} DSR192={dsr(D, k, 192)[0]:.3f}")

    fig, ax = plt.subplots(figsize=(10, 5))
    for k, v in curves.items():
        ax.plot(v.index, v.values, label=k, lw=1)
    ax.axhline(1, color="grey", lw=0.5)
    ax.set_yscale("log")
    ax.set_title("Fade de la reprise FX (futures CME, 4 paires) — vectorbt")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "vbt_equity.png", dpi=120)
    say("\nfin.")


if __name__ == "__main__":
    main()
