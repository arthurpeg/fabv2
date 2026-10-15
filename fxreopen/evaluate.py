"""Coûts, métriques par trade et par portefeuille journalier, tests (bootstrap
stationnaire, permutations du sens, DSR, Reality Check) et spread effectif."""

from __future__ import annotations

import numpy as np
import pandas as pd

from fxreopen.data import NY, PAIRS
from lab.optimize import deflated_sharpe, expected_max_sharpe

N_PAIRS = len(PAIRS)


def with_cost(t: pd.DataFrame, cost) -> pd.DataFrame:
    """cost : pips aller-retour (nombre) ou "std" (1 tick + 5 $, converti par trade)."""
    t = t.copy()
    if isinstance(cost, str):
        c = np.empty(len(t))
        for pair, g in t.groupby("pair"):
            c[g.index] = PAIRS[pair].std_cost_pips(g["p_in"].values)
    else:
        c = np.full(len(t), float(cost))
    t["cost"] = c
    t["net"] = t["gross"] - c
    pip = t["pair"].map({k: p.pip for k, p in PAIRS.items()}).values
    t["ret"] = t["net"] * pip / t["p_in"]
    return t


def trade_stats(t: pd.DataFrame) -> dict:
    n = len(t)
    if n == 0:
        return {"n": 0}
    x = t["net"].values
    win, loss = x[x > 0].sum(), -x[x < 0].sum()
    years = (t["date"].max() - t["date"].min()).days / 365.25 or np.nan
    yr = t.groupby(t["date"].dt.year)["net"].sum()
    return {
        "n": n,
        "pf": win / loss if loss > 0 else np.inf,
        "win_%": 100 * (x > 0).mean(),
        "mean_net": x.mean(),
        "mean_gross": t["gross"].mean(),
        "sd": x.std(ddof=1),
        "sharpe_paper": x.mean() / x.std(ddof=1) * np.sqrt(n / years) if n > 1 else np.nan,
        "losing_years": f"{int((yr < 0).sum())}/{len(yr)}",
    }


def daily(t: pd.DataFrame, calendar: pd.DatetimeIndex) -> pd.Series:
    """Rendement journalier du portefeuille : 1/4 du capital par paire, trades d'une
    même paire successifs, 0 les jours sans trade."""
    return (t.groupby("date")["ret"].sum() / N_PAIRS).reindex(calendar, fill_value=0.0)


def sharpe(r: pd.Series) -> float:
    s = r.std()
    return float(r.mean() / s * np.sqrt(252)) if s > 0 else np.nan


def stationary_idx(rng, n: int, mean_block: float, reps: int) -> np.ndarray:
    p = 1 / mean_block
    idx = np.empty((reps, n), dtype=np.int64)
    idx[:, 0] = rng.integers(0, n, reps)
    new = rng.random((reps, n)) < p
    rnd = rng.integers(0, n, (reps, n))
    for k in range(1, n):
        idx[:, k] = np.where(new[:, k], rnd[:, k], (idx[:, k - 1] + 1) % n)
    return idx


def bootstrap_p(r: pd.Series, reps: int = 10_000, block: float = 10, seed: int = 0) -> float:
    """p unilatéral de H0 : moyenne ≤ 0, bootstrap stationnaire de la série centrée."""
    rng = np.random.default_rng(seed)
    x = r.values
    mu = x.mean()
    xc = x - mu
    means = np.empty(reps)
    for i in range(0, reps, 500):
        idx = stationary_idx(rng, len(x), block, min(500, reps - i))
        means[i:i + len(idx)] = xc[idx].mean(1)
    return float((means >= mu).mean())


def permutation_p(t: pd.DataFrame, reps: int = 10_000, seed: int = 0) -> float:
    """Permute le sens (±1) entre les événements, paire par paire ; statistique = gain
    moyen net par trade. H0 : le fade ne fait pas mieux qu'un sens aléatoire."""
    rng = np.random.default_rng(seed)
    obs = t["net"].mean()
    tot = np.zeros(reps)
    for _, g in t.groupby("pair"):
        move = (g["gross"] * g["dir"]).values  # mouvement de prix en pips (sens long)
        d = g["dir"].values
        chunk = max(1, 5_000_000 // len(d))
        for i in range(0, reps, chunk):
            k = min(chunk, reps - i)
            perm = rng.permuted(np.tile(d, (k, 1)), axis=1)
            tot[i:i + k] += perm @ move
        tot -= g["cost"].sum()
    return float(((tot / len(t)) >= obs).mean())


def dsr(D: pd.DataFrame, col: str, n_trials: int) -> tuple[float, float]:
    sr = D.mean() / D.std()
    sr0 = expected_max_sharpe(float(sr.var()), n_trials)
    return deflated_sharpe(D[col], sr0), sr0 * np.sqrt(252)


def reality_check(D: pd.DataFrame, reps: int = 5000, block: float = 10, seed: int = 1) -> tuple[float, str, float]:
    """Reality Check de White (t-stats studentisées, bootstrap stationnaire)."""
    rng = np.random.default_rng(seed)
    M = D.values
    T = len(M)
    mu, sd = M.mean(0), M.std(0, ddof=1)
    sd[sd == 0] = np.inf
    stat = np.max(np.sqrt(T) * mu / sd)
    maxes = []
    for i in range(0, reps, 250):
        for row in stationary_idx(rng, T, block, 250):
            maxes.append(np.max(np.sqrt(T) * (M[row].mean(0) - mu) / sd))
    return float(np.mean(np.array(maxes) >= stat)), D.columns[int(np.argmax(mu / sd))], float(stat)


def abdi_ranaldo(df: pd.DataFrame, pip: float, windows: dict[str, tuple[int, int]]) -> pd.DataFrame:
    """Spread effectif d'Abdi & Ranaldo (2017) sur barres 1 minute consécutives :
    s² = 4 (c_t − η_t)(c_t − η_{t+1}), η = moyenne des log high/low. Moyenné par
    fenêtre ET [début, fin) en minutes et par année, puis s = √max(s², 0), en pips."""
    lc, eta = np.log(df["close"].values), (np.log(df["high"].values) + np.log(df["low"].values)) / 2
    consec = np.r_[np.diff(df.index.as_unit("ns").asi8) == 60_000_000_000, False]
    s2 = np.full(len(df), np.nan)
    s2[:-1] = 4 * (lc[:-1] - eta[:-1]) * (lc[:-1] - eta[1:])
    s2[~consec] = np.nan
    et = df.index.tz_convert(NY)
    mins = et.hour * 60 + et.minute
    rows = []
    for name, (a, b) in windows.items():
        m = (mins >= a) & (mins < b) & np.isfinite(s2)
        g = pd.DataFrame({"y": et.year[m], "s2": s2[m], "px": df["close"].values[m]}).groupby("y")
        for y, x in g:
            rows.append({"window": name, "year": y,
                         "spread_pips": np.sqrt(max(x["s2"].mean(), 0)) * x["px"].mean() / pip})
    return pd.DataFrame(rows)
