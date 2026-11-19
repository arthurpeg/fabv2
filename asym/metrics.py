"""Jeu complet de métriques d'une règle : portefeuille (rendements journaliers vectorbt) et
par trade (rendements nets arithmétiques), par fenêtre."""

from __future__ import annotations

import numpy as np
import pandas as pd


def full_metrics(r: pd.Series, net: np.ndarray, dates: pd.Series, windows: dict) -> list[dict]:
    """r : rendements journaliers (calendrier des séances) ; net, dates : par trade."""
    rows = []
    dates = pd.to_datetime(pd.Series(dates).values)
    for w, (a, b) in windows.items():
        rw = r[(r.index >= a) & (r.index <= b)]
        m = (dates >= pd.Timestamp(a)) & (dates <= pd.Timestamp(b))
        xn = np.asarray(net)[m]
        if len(rw) == 0:
            continue
        eq = (1 + rw).cumprod()
        dd = eq / eq.cummax() - 1
        yrs = len(rw) / 252
        cagr = eq.iloc[-1] ** (1 / yrs) - 1
        down = np.sqrt((np.minimum(rw, 0) ** 2).mean())
        under = (dd < 0).astype(int)
        longest = int(under.groupby((under == 0).cumsum()).sum().max())
        yr = rw.groupby(rw.index.year).apply(lambda s: (1 + s).prod() - 1)
        wins, losses = xn[xn > 0], xn[xn < 0]
        act = rw[rw != 0]
        rows.append({
            "window": w, "trades": len(xn), "expo_pct": 100 * len(xn) / len(rw),
            "total_pct": 100 * (eq.iloc[-1] - 1), "cagr_pct": 100 * cagr,
            "vol_pct": 100 * rw.std() * np.sqrt(252),
            "sharpe": rw.mean() / rw.std() * np.sqrt(252) if rw.std() > 0 else np.nan,
            "sortino": rw.mean() / down * np.sqrt(252) if down > 0 else np.nan,
            "maxdd_pct": 100 * dd.min(), "calmar": cagr / abs(dd.min()) if dd.min() < 0 else np.nan,
            "longest_dd_days": longest,
            "win_pct": 100 * (xn > 0).mean() if len(xn) else np.nan,
            "avg_bp": 1e4 * xn.mean() if len(xn) else np.nan,
            "avg_win_bp": 1e4 * wins.mean() if len(wins) else np.nan,
            "avg_loss_bp": 1e4 * losses.mean() if len(losses) else np.nan,
            "payoff": wins.mean() / -losses.mean() if len(wins) and len(losses) else np.nan,
            "pf": wins.sum() / -losses.sum() if len(losses) else np.nan,
            "best_bp": 1e4 * xn.max() if len(xn) else np.nan, "worst_bp": 1e4 * xn.min() if len(xn) else np.nan,
            "skew": act.skew(), "kurt": act.kurt(),
            "pos_years": f"{int((yr > 0).sum())}/{len(yr)}",
            "best_year_pct": 100 * yr.max(), "worst_year_pct": 100 * yr.min(),
        })
    return rows
