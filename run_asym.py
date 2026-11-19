"""Pré-enregistrement n° 8 : asymétrie intraday ancrée sur l'ouverture (Valenti 2026), ES et DAX.

uv run python run_asym.py   → results/asym/ (run.log, CSV, parquet, equity.png)
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

from asym.backtest import daily_returns, net_returns, simulate  # noqa: E402
from asym.rules import DAX, ES, load, next_day_frame, sessions, trades  # noqa: E402
from fxreopen.evaluate import bootstrap_p, dsr, reality_check, sharpe  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/asym")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")

ES_STD = ("pts", 0.25 + 5.0 / 50)  # 1 tick + 5 $ aller-retour
GRID = (0, 1, 2, 5)
PRIMARY = "ES_asym"
N_PREREG, N_GLOBAL = 7, 208
WINDOWS = {"2016-2020": ("2016-01-01", "2020-12-31"), "2021-2026-08": ("2021-01-01", "2026-12-31"),
           "2026": ("2026-01-01", "2026-12-31"), "tout": ("2016-01-01", "2026-12-31")}


def say(s: str = "") -> None:
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def permutation_p(T: pd.DataFrame, cost, reps: int = 10_000, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    move = (T["p_out"] / T["p_in"] - 1).values
    c = net_returns(T, cost) - T["gross"].values  # −coût
    obs = (T["dir"].values * move + c).mean()
    d = T["dir"].values
    perm = rng.permuted(np.tile(d, (reps, 1)), axis=1)
    return float((((perm @ move) + c.sum()) / len(d) >= obs).mean())


def newey_west_ols(y: np.ndarray, X: np.ndarray, lags: int = 5):
    X = np.column_stack([np.ones(len(y)), X])
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    u = y - X @ b
    Z = X * u[:, None]
    S = Z.T @ Z
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1)
        G = Z[k:].T @ Z[:-k]
        S += w * (G + G.T)
    se = np.sqrt(np.diag(XtX_inv @ S @ XtX_inv))
    return b, b / se


def stats(T: pd.DataFrame, cost, w: str) -> dict:
    a, b = WINDOWS[w]
    m = (T["date"] >= a) & (T["date"] <= b)
    x = net_returns(T, cost)[m.values]
    if len(x) == 0:
        return {"n": 0}
    yrs = T.loc[m, "date"].dt.year
    yr = pd.Series(x).groupby(yrs.values).sum()
    win, loss = x[x > 0].sum(), -x[x < 0].sum()
    return {"n": len(x), "mean_bp": 1e4 * x.mean(), "win_%": 100 * (x > 0).mean(),
            "pf": win / loss if loss > 0 else np.inf, "losing_years": f"{int((yr < 0).sum())}/{len(yr)}",
            "active_ann_%": 100 * 252 * x.mean(), "active_vol_%": 100 * np.sqrt(252) * x.std(ddof=1)}


def fmt(d: dict) -> str:
    if d.get("n", 0) == 0:
        return "n=0"
    return (f"n={d['n']:>5} moy={d['mean_bp']:+6.2f}pb win={d['win_%']:4.1f}% PF={d['pf']:.2f} "
            f"années<0={d['losing_years']} [jours actifs : {d['active_ann_%']:+5.1f}%/an, vol {d['active_vol_%']:4.1f}%]")


def main() -> None:
    say("# Pré-enregistrement n° 8 — asymétrie ancrée sur l'ouverture (Valenti 2026)\n")
    frames, cals = {}, {}
    for m in (ES, DAX):
        df = load(m)
        S = sessions(df, m)
        F = next_day_frame(S, m, df)
        frames[m.name] = F
        cals[m.name] = pd.DatetimeIndex(S.index[S["full"]])
        say(f"{m.name}: séances={len(S)} complètes={int(S['full'].sum())} couples (t, t+1)={len(F)} "
            f"[{F['date'].min().date()} → {F['date'].max().date()}] part asym<0={100 * (F['asym'] < 0).mean():.1f}%")
    F = frames["ES"]
    say(f"Corrélation des signaux ES (jour t) : asym/roc={F['asym'].corr(F['roc']):.3f}, "
        f"asym/asym_C={F['asym'].corr(F['asym_C']):.3f}, "
        f"concordance de signe asym/roc={100 * (np.sign(F['asym']) == np.sign(F['roc'])).mean():.1f}%")

    rules = {f"ES_{r}": (trades(frames["ES"], r), ES_STD) for r in
             ("asym", "asym_prevC", "asym_C", "roc", "asym_long", "asym_short")}
    rules["DAX_asym"] = (trades(frames["DAX"], "asym"), 2.0)

    say("\n## Par trade, coût principal (ES : 1 tick + 5 $ ; DAX : 2 pb)")
    for k, (T, c) in rules.items():
        T.to_parquet(OUT / f"trades_{k}.parquet")
        for w in ("2016-2020", "2021-2026-08", "2026", "tout"):
            say(f"{k:<14} {w:<12} {fmt(stats(T, c, w))}")
    Tl = trades(frames["ES"], "asym", entry="open1")
    say(f"\nExécutabilité (sans essai) : ES_asym entrée 09:31 : {fmt(stats(Tl, ES_STD, 'tout'))}")
    allday = pd.DataFrame({"date": F["date"], "gross": F["p_out"] / F["p_in"] - 1, "p_in": F["p_in"]})
    say(f"Référence : long inconditionnel ouverture → clôture (brut) : {100 * 252 * allday['gross'].mean():+.1f}%/an "
        f"(papier : 4,1 %)")

    say("\n## Régression d'apport : r_{t+1} = a + b·Asym_O + c·ln(C/O), Newey-West 5 retards (ES, 2016-2026)")
    y = (F["p_out"] / F["p_in"] - 1).values
    b, t = newey_west_ols(y, F[["asym", "roc"]].values)
    p_b = norm.cdf(t[1])  # unilatéral, H1 : b < 0
    say(f"b(Asym)={b[1]:+.4f} t={t[1]:+.2f} p_unilatéral={p_b:.4f} | c(roc)={b[2]:+.4f} t={t[2]:+.2f}")
    b1, t1 = newey_west_ols(y, F[["asym"]].values)
    b2, t2 = newey_west_ols(y, F[["roc"]].values)
    say(f"Seuls : b(Asym)={b1[1]:+.4f} (t={t1[1]:+.2f}) ; c(roc)={b2[1]:+.4f} (t={t2[1]:+.2f})")

    say("\n## Backtest vectorbt (1×, cible ±100 %)")
    rows, D, curves = [], {}, {}
    for k, (T, c) in rules.items():
        cal = cals["DAX" if k.startswith("DAX") else "ES"]
        for cc in (c, *GRID):
            pf = simulate(T, cc)
            r = daily_returns(pf, T, cal)
            if cc == c:
                D[k] = r
                curves[k] = (1 + r).cumprod()
            for w in WINDOWS:
                a, bb = WINDOWS[w]
                rw = r[(r.index >= a) & (r.index <= bb)]
                eq = (1 + rw).cumprod()
                rows.append({"rule": k, "cost": str(cc), "window": w, "total_%": 100 * (eq.iloc[-1] - 1) if len(eq) else np.nan,
                             "ann_%": 100 * 252 * rw.mean(), "sharpe": sharpe(rw),
                             "max_dd_%": 100 * float((eq / eq.cummax() - 1).min()) if len(eq) else np.nan})
            st = rows[-1]
            lab = "std" if isinstance(cc, tuple) else f"{cc}pb"
            say(f"{k:<14} coût {lab:>4} | total={st['total_%']:+8.1f}% annuel={st['ann_%']:+6.2f}% "
                f"Sharpe={st['sharpe']:+5.2f} DDmax={st['max_dd_%']:+6.1f}%")
    pd.DataFrame(rows).to_csv(OUT / "vbt_summary.csv", index=False)
    D = pd.DataFrame(D)  # calendriers ES et DAX différents : NaN hors calendrier
    D.to_parquet(OUT / "vbt_daily_net.parquet")

    say("\n## Tests au coût principal")
    Des = D[[k for k in D if k.startswith("ES")]].dropna()
    Dall = D.fillna(0.0)
    res = {}
    for k, (T, c) in rules.items():
        r = D[k].dropna()
        d7, sr0 = dsr(Dall, k, N_PREREG)
        res[k] = {"p_boot": bootstrap_p(r), "p_perm": permutation_p(T, c), "dsr7": d7,
                  "dsr208": dsr(Dall, k, N_GLOBAL)[0], "sharpe": sharpe(r)}
        say(f"{k:<14} Sharpe={res[k]['sharpe']:+5.2f} p_boot={res[k]['p_boot']:.4f} p_perm={res[k]['p_perm']:.4f} "
            f"DSR7={d7:.3f} DSR208={res[k]['dsr208']:.3f}")
    p_rc, best, st = reality_check(Dall)
    say(f"Reality Check (7 règles) : p={p_rc:.4f}, meilleure={best}, t={st:.2f}")
    _ = Des

    say("\n## Critères de ES_asym")
    T, c = rules[PRIMARY]
    h = [stats(T, c, w) for w in ("2016-2020", "2021-2026-08")]
    c1 = all(x["mean_bp"] > 0 and x["pf"] > 1 for x in h)
    c2, c3, c4 = res[PRIMARY]["p_boot"] < 0.05, res[PRIMARY]["p_perm"] < 0.05, res[PRIMARY]["dsr7"] > 0.95
    c5 = (b[1] < 0) and (p_b < 0.05)
    say(f"(1) deux moitiés={c1} (2) bootstrap={c2} (3) permutation={c3} (4) DSR={c4} (5) apport vs roc={c5} "
        f"→ {'SURVIT' if all((c1, c2, c3, c4, c5)) else 'REJETÉ'}")
    T, c = rules["DAX_asym"]
    hd = [stats(T, c, w) for w in ("2016-2020", "2021-2026-08")]
    say(f"DAX (réplication, critères 1-3) : deux moitiés={all(x['mean_bp'] > 0 and x['pf'] > 1 for x in hd)} "
        f"bootstrap={res['DAX_asym']['p_boot'] < 0.05} permutation={res['DAX_asym']['p_perm'] < 0.05}")
    g = {k: stats(*rules[k], "tout")["mean_bp"] for k in rules}
    say(f"Prédictions du papier : long > short : {g['ES_asym_long'] > g['ES_asym_short']} "
        f"({g['ES_asym_long']:+.2f} vs {g['ES_asym_short']:+.2f} pb) ; ancrage clôture du jour perdant : "
        f"{g['ES_asym_C'] < 0} ({g['ES_asym_C']:+.2f}) ; clôture de la veille < ouverture : "
        f"{g['ES_asym_prevC'] < g['ES_asym']} ({g['ES_asym_prevC']:+.2f} vs {g['ES_asym']:+.2f})")

    fig, ax = plt.subplots(figsize=(10, 5))
    for k, v in curves.items():
        ax.plot(v.index, v.values, label=k, lw=1)
    ax.axhline(1, color="grey", lw=0.5)
    ax.set_yscale("log")
    ax.set_title("Asymétrie ancrée sur l'ouverture (Valenti 2026) — vectorbt, coût principal")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "equity.png", dpi=120)
    say("\nfin.")


if __name__ == "__main__":
    main()
