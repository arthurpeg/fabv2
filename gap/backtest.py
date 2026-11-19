"""Exécution vectorbt, métriques de prévision et de trading, permutations, DSR.

Exécution (variante B) : chaque jour, un ordre `targetpercent` = w à l'instant
d'entrée (08:55 Berlin), puis 0 à la sortie (09:00 + k). Prix = open de la barre
1 min de l'instant. Frais = coût par côté (moitié de l'aller-retour, en points)
/ prix. |w| ≤ 1 : pas de levier. Le portefeuille est à plat entre deux jours ;
le rendement du jour est donc la variation de valeur entre deux sorties.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import vectorbt as vbt
from scipy import stats

from gap.data import to_index, utc_ns
from lab.optimize import deflated_sharpe, expected_max_sharpe


# --------------------------------------------------------------------------- exécution


def simulate(entry_ts: pd.DatetimeIndex, exit_ts: pd.DatetimeIndex, entry_px: np.ndarray, exit_px: np.ndarray,
             W: pd.DataFrame, cost_rt_pts: float) -> pd.DataFrame:
    """Rendements journaliers nets (jours × stratégies) via `vbt.Portfolio.from_orders`."""
    n = len(W)
    ts = np.concatenate([utc_ns(entry_ts), utc_ns(exit_ts)])
    px = np.concatenate([entry_px, exit_px])
    is_exit = np.r_[np.zeros(n), np.ones(n)]
    order = np.lexsort((is_exit, ts))
    if len(np.unique(ts)) != len(ts):
        raise ValueError("deux ordres au même instant")
    idx = to_index(ts[order])
    size = np.vstack([W.values, np.zeros_like(W.values)])[order]
    fees = (cost_rt_pts / 2) / px[order]
    pf = vbt.Portfolio.from_orders(
        close=pd.Series(px[order], index=idx),
        size=pd.DataFrame(size, index=idx, columns=W.columns),
        size_type="targetpercent",
        direction="both",
        fees=fees[:, None],
        init_cash=1_000_000.0,
        freq="1min",
    )
    val = pf.value()
    at_exit = val[is_exit[order] == 1]
    at_exit.index = W.index  # sorties dans l'ordre des jours
    return at_exit / at_exit.shift(1, fill_value=1_000_000.0) - 1


def arithmetic(w: np.ndarray, entry_px: np.ndarray, exit_px: np.ndarray, cost_rt_pts: float) -> np.ndarray:
    """Même P&L sans vectorbt (sert aux permutations et au contrôle croisé).
    Quantité = w × capital / prix d'entrée ; frais = coût en points × quantité."""
    return w * (exit_px / entry_px - 1) - np.abs(w) * cost_rt_pts / entry_px


# --------------------------------------------------------------------------- métriques


def sharpe(r: pd.Series | np.ndarray) -> float:
    r = np.asarray(r, float)
    sd = r.std(ddof=1)
    return float(r.mean() / sd * np.sqrt(252)) if sd > 0 else np.nan


def max_drawdown(r: pd.Series) -> float:
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def trading_metrics(r: pd.Series, w: np.ndarray) -> dict:
    traded = w != 0
    return {
        "ret_%": float((1 + r).prod() - 1) * 100,
        "sharpe": sharpe(r),
        "max_dd_%": max_drawdown(r) * 100,
        "hit_%": float((r[traded] > 0).mean() * 100) if traded.any() else np.nan,
        "n_trades": int(traded.sum()),
        "turnover": float(2 * np.abs(w).mean()),  # notionnel échangé / capital, par jour
        "exposure_%": float(traded.mean() * 100),
        "avg_|w|": float(np.abs(w[traded]).mean()) if traded.any() else 0.0,
        "n_days": len(r),
    }


def permutation_test(w: np.ndarray, entry_px, exit_px, cost_rt_pts: float, n: int, seed: int) -> tuple[float, np.ndarray]:
    """Mêmes positions réparties au hasard entre les jours : p = P(SR perm ≥ SR observé)."""
    rng = np.random.default_rng(seed)
    obs = sharpe(arithmetic(w, entry_px, exit_px, cost_rt_pts))
    perm = np.array([sharpe(arithmetic(rng.permutation(w), entry_px, exit_px, cost_rt_pts)) for _ in range(n)])
    perm = np.nan_to_num(perm, nan=0.0)
    return float((1 + (perm >= obs).sum()) / (n + 1)), perm


def newey_west_var(d: np.ndarray, lags: int | None = None) -> float:
    d = d - d.mean()
    n = len(d)
    lags = lags if lags is not None else int(np.floor(4 * (n / 100) ** (2 / 9)))
    v = d @ d / n
    for l in range(1, lags + 1):
        v += 2 * (1 - l / (lags + 1)) * (d[l:] @ d[:-l]) / n
    return v


def diebold_mariano(e_ref: np.ndarray, e_new: np.ndarray) -> tuple[float, float]:
    """H1 : le nouveau modèle a une perte quadratique plus faible. Retourne (stat, p unilatéral)."""
    d = e_ref**2 - e_new**2
    stat = d.mean() / np.sqrt(newey_west_var(d) / len(d))
    return float(stat), float(1 - stats.norm.cdf(stat))


def forecast_metrics(p: pd.DataFrame) -> dict:
    y = p["y"].values
    out = {"n": len(p), "mse_zero": float(np.mean(y**2))}
    for c in ["ols", "ols_sub", "np_mean", "np_median", "np_mode"]:
        f = p[c].values
        out[f"mse_{c}"] = float(np.mean((y - f) ** 2))
        m = (f != 0) & (y != 0)
        correct = int((np.sign(f[m]) == np.sign(y[m])).sum())
        out[f"sign_err_{c}_%"] = float(100 * (1 - correct / m.sum())) if m.any() else np.nan
        out[f"sign_n_{c}"] = int(m.sum())
        out[f"sign_p_{c}"] = float(stats.binomtest(correct, int(m.sum()), 0.5, alternative="greater").pvalue) if m.any() else np.nan
    ok = p["lo"].notna()
    out["cpi_coverage_%"] = float(100 * ((p["lo"] <= p["y"]) & (p["y"] <= p["hi"]))[ok].mean())
    out["no_signal_%"] = float(100 * p["no_signal"].mean())
    out["dm_stat"], out["dm_p"] = diebold_mariano(y - p["ols"].values, y - p["np_mean"].values)
    return out


def dsr(trials: pd.DataFrame, col: str, n_trials: int) -> tuple[float, float]:
    """DSR (Bailey & López de Prado) de la colonne `col`, avec la variance des
    Sharpe journaliers des essais et N = `n_trials`. Retourne (DSR, SR0 annualisé)."""
    sr = trials.mean() / trials.std()
    sr0 = expected_max_sharpe(float(sr.var()), n_trials)
    return deflated_sharpe(trials[col], sr0), sr0 * np.sqrt(252)
