"""Recherche de paramètres vectorisée + Deflated Sharpe Ratio.

Protocole :
- toutes les combinaisons d'une grille sont simulées en un seul `from_signals`
  (une colonne par combinaison) ;
- le choix se fait sur l'IS seulement (Sharpe journalier max ≤ 2022-12-31) ;
- le DSR (Bailey & López de Prado, 2014) corrige ce Sharpe IS pour le nombre
  d'essais N et la dispersion des Sharpe entre essais ; même formule que
  `followup.py` ;
- l'OOS de la combinaison retenue est rapporté tel quel, jamais utilisé pour choisir.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np
import pandas as pd
from scipy import stats

from fab.core import IS_END
from lab.engine import Strategy, bars, daily_returns, portfolio

EULER = 0.5772156649


def combos(grid: dict[str, list], constraint=None) -> list[dict]:
    keys = list(grid)
    out = [dict(zip(keys, v)) for v in product(*grid.values())]
    return [c for c in out if constraint is None or constraint(c)]


def daily_sharpe(r: pd.DataFrame | pd.Series):
    """Sharpe journalier non annualisé (convention du DSR)."""
    return r.mean() / r.std()


def expected_max_sharpe(sr_var: float, n: int) -> float:
    """SR0 : espérance du max de n Sharpe nuls de variance `sr_var`."""
    if n < 2:
        return 0.0
    return float(np.sqrt(sr_var) * ((1 - EULER) * stats.norm.ppf(1 - 1 / n)
                                    + EULER * stats.norm.ppf(1 - 1 / (n * np.e))))


def deflated_sharpe(x: pd.Series, sr0: float) -> float:
    """P(vrai SR > SR0) compte tenu de la longueur, du skew et du kurtosis de x."""
    x = x.dropna()
    sr = x.mean() / x.std()
    sk, ku = stats.skew(x), stats.kurtosis(x, fisher=False)
    return float(stats.norm.cdf((sr - sr0) * np.sqrt(len(x) - 1)
                                / np.sqrt(1 - sk * sr + (ku - 1) / 4 * sr**2)))


@dataclass
class GridResult:
    strategy: str
    asset: str
    tf: str
    trials: pd.DataFrame  # une ligne par combinaison : params, SR IS/OOS annualisés
    best: dict  # paramètres retenus sur l'IS
    best_is: pd.Series  # rendements journaliers IS de la combinaison retenue
    best_oos: pd.Series


def grid_search(strategy: Strategy, asset: str, tf: str, grid: dict, constraint=None) -> GridResult:
    b = bars(asset, tf)
    cs = combos(grid, constraint)
    keys = list(grid)
    sigs = {tuple(c[k] for k in keys): strategy(b, **c) for c in cs}
    pf = portfolio(b, asset, tf, sigs)
    d = daily_returns(pf.value())
    d.columns = pd.MultiIndex.from_tuples(list(sigs), names=keys) if len(keys) > 1 else pd.Index([k[0] for k in sigs], name=keys[0])
    is_, oos = d[d.index <= IS_END], d[d.index > IS_END]
    trials = pd.DataFrame({
        "sr_daily_IS": daily_sharpe(is_),
        "sharpe_IS": daily_sharpe(is_) * np.sqrt(252),
        "sharpe_OOS": daily_sharpe(oos) * np.sqrt(252),
        "n_trades": pf.trades.count().values,
    }).reset_index()
    i = int(trials["sr_daily_IS"].fillna(-np.inf).values.argmax())
    col = d.columns[i]
    return GridResult(
        getattr(strategy, "__name__", "strategy"), asset, tf, trials,
        {k: trials[k].tolist()[i] for k in keys}, is_[col], oos[col],
    )


def summarize(results: list[GridResult], extra_trials: int = 0) -> pd.DataFrame:
    """DSR de chaque meilleure combinaison, à deux niveaux :
    - `dsr_grid` : N = taille de sa propre grille (optimiste) ;
    - `dsr_all`  : N = tous les essais de la session + `extra_trials` (à retenir).
    """
    all_sr = pd.concat([r.trials["sr_daily_IS"] for r in results]).dropna()
    n_all = len(all_sr) + extra_trials
    sr0_all = expected_max_sharpe(all_sr.var(), n_all)
    rows = []
    for r in results:
        t = r.trials["sr_daily_IS"].dropna()
        sr0_grid = expected_max_sharpe(t.var(), len(t))
        best = r.trials.loc[r.trials["sr_daily_IS"].idxmax()]
        rows.append({
            "strategy": r.strategy, "asset": r.asset, "tf": r.tf,
            "best": ", ".join(f"{k}={v}" for k, v in r.best.items()),
            "n_grid": len(t),
            "sharpe_IS": best["sharpe_IS"],
            "sharpe_OOS": best["sharpe_OOS"],
            "med_sharpe_OOS_grid": r.trials["sharpe_OOS"].median(),
            "sr0_grid_ann": sr0_grid * np.sqrt(252),
            "dsr_grid": deflated_sharpe(r.best_is, sr0_grid),
            "sr0_all_ann": sr0_all * np.sqrt(252),
            "dsr_all": deflated_sharpe(r.best_is, sr0_all),
            "n_trades": int(best["n_trades"]),
        })
    df = pd.DataFrame(rows)
    df.attrs["n_trials"] = n_all
    df["passes"] = (df["dsr_all"] > 0.95) & (df["sharpe_OOS"] > 0)
    return df
