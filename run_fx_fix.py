"""Pré-enregistrement n° 7 : fix de Londres à 16h en fin de mois (Melvin et Prins), futures CME.

Trades construits par `fxfix.rules`, exécutés dans vectorbt (`fxreopen.backtest.simulate`,
1/4 du capital par paire), tests de `fxreopen.evaluate`.

uv run python run_fx_fix.py   → results/fx_fix/ (run.log, CSV, parquet, equity.png)
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import norm  # noqa: E402

from fxfix.rules import EQUITY, daily_closes, flow_trades, load_equity, reversal_trades  # noqa: E402
from fxreopen.backtest import max_drawdown, session_returns, simulate, trade_table  # noqa: E402
from fxreopen.data import NY, PAIRS, load  # noqa: E402
from fxreopen.evaluate import (bootstrap_p, dsr, permutation_p, reality_check, sharpe,  # noqa: E402
                               trade_stats, with_cost)

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/fx_fix")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")

COSTS = ("std", 0, 1, 2, 3)
MAIN_COST = "std"
PRIMARIES = ("A_eom_E5", "B_eom_16:00")
N_PREREG, N_GLOBAL = 9, 201
ALPHA = 0.025
WINDOWS = {"2016-2020": ("2016-01-01", "2020-12-31"), "2021-2026-08": ("2021-01-01", "2026-12-31"),
           "tout": ("2016-01-01", "2026-12-31")}


def say(s: str = "") -> None:
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def window(t: pd.DataFrame, w: str) -> pd.DataFrame:
    a, b = WINDOWS[w]
    return t[(t["date"] >= a) & (t["date"] <= b)]


def fmt(d: dict) -> str:
    if d.get("n", 0) == 0:
        return "n=0"
    return (f"n={d['n']:>5} PF={d['pf']:5.2f} win={d['win_%']:5.1f}% net={d['mean_net']:+7.2f} "
            f"brut={d['mean_gross']:+7.2f} sd={d['sd']:6.1f} années<0={d['losing_years']}")


def build() -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame], pd.DatetimeIndex]:
    data = {f: load(f) for f in PAIRS}
    rev = {e: pd.concat([reversal_trades(f, df, e) for f, df in data.items()], ignore_index=True)
           for e in (0, 1, 5)}
    us = daily_closes(load_equity("ES"), NY, "16:00")
    cty = {f: daily_closes(load_equity(name), tz, hhmm, sw) for f, (name, tz, hhmm, sw) in EQUITY.items()}
    flow = {x: pd.concat([flow_trades(f, data[f], x, us, cty[f]) for f in EQUITY], ignore_index=True)
            for x in ("16:00", "16:05")}
    idx = data["6E"].index.tz_convert(NY).tz_localize(None)
    cal = pd.DatetimeIndex(np.unique((idx - pd.Timedelta(hours=18)).normalize()))
    rules = {}
    for e in (0, 1, 5):
        t = rev[e]
        rules[f"A_eom_E{e}"] = t[t["eom"]].reset_index(drop=True)
        rules[f"A_noneom_E{e}"] = t[~t["eom"]].reset_index(drop=True)
    for x in ("16:00", "16:05"):
        t = flow[x]
        rules[f"B_eom_{x}"] = t[t["eom"]].reset_index(drop=True)
    t = flow["16:00"]
    rules["B_noneom_16:00"] = t[~t["eom"]].reset_index(drop=True)
    return rules, {"rev_E0": rev[0], "flow_16": flow["16:00"]}, cal


def ols(y: np.ndarray, X: np.ndarray, groups: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """MCO avec constante, erreurs types groupées (un groupe par observation = HC0).
    Retourne (coefficients, p bilatéraux normaux, R²)."""
    X = np.column_stack([np.ones(len(y)), X])
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    u = y - X @ b
    S = pd.DataFrame(X * u[:, None]).groupby(groups).sum().values
    V = XtX_inv @ (S.T @ S) @ XtX_inv
    p = 2 * norm.sf(np.abs(b / np.sqrt(np.diag(V))))
    return b, p, 1 - u.var() / y.var()


def vbt_window(r: pd.Series, tr: pd.DataFrame, w: str) -> dict:
    a, b = WINDOWS[w]
    rw = r[(r.index >= a) & (r.index <= b)]
    tw = tr[(tr["date"] >= a) & (tr["date"] <= b)]
    pnl = tw["PnL"]
    loss = -pnl[pnl < 0].sum()
    return {"window": w, "trades": len(tw), "total_ret_%": 100 * float((1 + rw).prod() - 1),
            "ann_ret_%": 100 * float(rw.mean() * 252), "sharpe": sharpe(rw), "max_dd_%": 100 * max_drawdown(rw),
            "pf": float(pnl[pnl > 0].sum() / loss) if loss > 0 else np.nan}


def main() -> None:
    say("# Pré-enregistrement n° 7 — fix de Londres à 16h (Melvin et Prins), futures CME\n")
    rules, raw, cal = build()
    for k, t in rules.items():
        t.to_parquet(OUT / f"trades_{k.replace(':', '')}.parquet")

    say("## Anatomie : |m| = |open 16:00 − open 15:00| (pips), jours de fin de mois (FDM) et autres")
    t0 = raw["rev_E0"]
    for f in PAIRS:
        g = t0[t0["pair"] == f]
        say(f"{f}: FDM n={int(g['eom'].sum())} |m| moyen={g.loc[g['eom'], 'm'].abs().mean():.1f} | "
            f"autres n={int((~g['eom']).sum())} |m| moyen={g.loc[~g['eom'], 'm'].abs().mean():.1f}")
    fl = raw["flow_16"]
    say(f"B : jours FDM avec signal actions = {int(fl['eom'].sum())} (6E/6A/6J), "
        f"|x| moyen = {100 * fl.loc[fl['eom'], 'x'].abs().mean():.2f} %")

    say("\n## Réplication des régressions du papier (lecture secondaire)")
    pip = t0["pair"].map({k: p.pip for k, p in PAIRS.items()})
    ya = (t0["p_out"] - t0["p_in"]) / pip  # mouvement 16:00 → 12:00 J+1, en pips, sens long
    Xa = np.column_stack([t0["m"].values, (t0["m"] * t0["eom"]).values])
    b, p, r2 = ols(ya.values, Xa, t0["date"].factorize()[0])
    say(f"A : r(16→12 J+1) = a + b·m + c·m·FDM, n={len(t0)} : b={b[1]:+.3f} (p={p[1]:.3f}), "
        f"c={b[2]:+.3f} (p={p[2]:.3f}), R²={100 * r2:.2f} % | papier : b=−0,178, c=−0,518")
    fe = fl[fl["eom"]].reset_index(drop=True)
    sgn = np.where([PAIRS[q].inverted for q in fe["pair"]], -1.0, 1.0)
    strength = sgn * (fe["p_out"] / fe["p_in"] - 1).values
    b, p, r2 = ols(strength, fe["x"].values[:, None], np.arange(len(fe)))
    say(f"B : r_devise(13→16) = a + b·x, FDM, n={len(fe)} : b={b[1]:+.4f} (p={p[1]:.3f}), "
        f"R²={100 * r2:.2f} % | papier : b < 0, R² = 2 %")

    say("\n## Par trade, coût principal (1 tick + 5 $), pips")
    for k, t in rules.items():
        tc = with_cost(t, MAIN_COST)
        say(f"{k:<16} " + " | ".join(f"{w}: {fmt(trade_stats(window(tc, w)))}" for w in ("2016-2020", "2021-2026-08")))
        say(f"{'':<16} tout: {fmt(trade_stats(tc))} | point mort = {t['gross'].mean():+.2f} pips")
    for k in PRIMARIES:
        t = with_cost(rules[k], MAIN_COST)
        say(f"\n{k} par paire (tout) :")
        for f, g in t.groupby("pair"):
            say(f"  {f}: {fmt(trade_stats(g.reset_index(drop=True)))}")
    tq = with_cost(rules["A_eom_E5"], MAIN_COST)
    q = tq[tq["date"].dt.month.isin([3, 6, 9, 12])]
    say(f"\nDescriptif : A_eom_E5, fins de trimestre seulement : {fmt(trade_stats(q.reset_index(drop=True)))}")
    e0, e5 = rules["A_eom_E0"], rules["A_eom_E5"]
    say(f"Exécutabilité A (FDM) : brut moyen E0={e0['gross'].mean():+.2f}, E1={rules['A_eom_E1']['gross'].mean():+.2f}, "
        f"E5={e5['gross'].mean():+.2f} pips")

    say("\n## Backtest vectorbt (1/4 du capital par paire, sans levier)")
    rows, D, curves = [], {}, {}
    for k, t in rules.items():
        for c in COSTS:
            pf = simulate(with_cost(t, c))
            r = session_returns(pf, cal)
            tr = trade_table(pf)
            if c == MAIN_COST:
                D[k] = r
                if k in PRIMARIES:
                    curves[k] = (1 + r).cumprod()
            for w in WINDOWS:
                rows.append({"rule": k, "cost": c, **vbt_window(r, tr, w)})
            st = rows[-1]
            say(f"{k:<16} coût {str(c):>3} | trades={st['trades']:>5} total={st['total_ret_%']:+7.2f}% "
                f"annuel={st['ann_ret_%']:+6.2f}% Sharpe={st['sharpe']:+5.2f} DDmax={st['max_dd_%']:+6.2f}% "
                f"PF={st['pf']:.2f}")
    S = pd.DataFrame(rows)
    S.to_csv(OUT / "vbt_summary.csv", index=False)
    D = pd.DataFrame(D)
    D.to_parquet(OUT / "vbt_daily_net.parquet")

    say(f"\n## Tests au coût principal (seuil α = {ALPHA} par configuration principale)")
    res = {}
    for k in D:
        d9, sr0 = dsr(D, k, N_PREREG)
        res[k] = {"sharpe": sharpe(D[k]), "p_boot": bootstrap_p(D[k]), "p_perm": permutation_p(with_cost(rules[k], MAIN_COST)),
                  "dsr9": d9, "dsr201": dsr(D, k, N_GLOBAL)[0]}
        say(f"{k:<16} Sharpe={res[k]['sharpe']:+5.2f} p_boot={res[k]['p_boot']:.4f} p_perm={res[k]['p_perm']:.4f} "
            f"DSR9={d9:.3f} DSR201={res[k]['dsr201']:.3f} (SR0 annualisé={sr0:.2f})")
    p_rc, best, stat = reality_check(D)
    say(f"Reality Check (9 règles) : p={p_rc:.4f}, meilleure={best}, t={stat:.2f}")

    say("\n## Critères des configurations principales")
    for k in PRIMARIES:
        tc = with_cost(rules[k], MAIN_COST)
        halves = [trade_stats(window(tc, w)) for w in ("2016-2020", "2021-2026-08")]
        c1 = all(h.get("n", 0) > 0 and h["mean_net"] > 0 and h["pf"] > 1 for h in halves)
        c2, c3, c4 = res[k]["p_boot"] < ALPHA, res[k]["p_perm"] < ALPHA, res[k]["dsr9"] > 0.95
        say(f"{k}: (1) deux moitiés positives={c1} (2) bootstrap={c2} (3) permutation={c3} (4) DSR={c4} "
            f"→ {'SURVIT' if all((c1, c2, c3, c4)) else 'REJETÉ'}")
    say("\nContrôles :")
    say(f"A non-FDM vs FDM (E5, brut) : {rules['A_noneom_E5']['gross'].mean():+.2f} vs {rules['A_eom_E5']['gross'].mean():+.2f} pips")
    say(f"B non-FDM vs FDM (16:00, brut) : {rules['B_noneom_16:00']['gross'].mean():+.2f} vs "
        f"{rules['B_eom_16:00']['gross'].mean():+.2f} pips")

    fig, ax = plt.subplots(figsize=(10, 5))
    for k, v in curves.items():
        ax.plot(v.index, v.values, label=f"{k} (coût standard)", lw=1)
    ax.axhline(1, color="grey", lw=0.5)
    ax.set_title("Fix de Londres en fin de mois (futures CME) — vectorbt")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "equity.png", dpi=120)
    say("\nfin.")


if __name__ == "__main__":
    main()
