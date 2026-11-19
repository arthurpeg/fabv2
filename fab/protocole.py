"""Outils communs du protocole de validation (PROTOCOLE.md) : mêmes statistiques, même fiche, pour toute idée.

Usage typique :
    from fab.protocole import fiche, barriere_exploration, verdict_confirmation, imprimer
    f = fiche(net_bp, brut_bp, ref_net_bp, n_famille=12, sharpes_famille=[...], tick_bp=0.57)
    imprimer(f)
    ok, raisons = barriere_exploration(f)      # étape 1 → droit de dépenser la réserve
    ok, raisons = verdict_confirmation(f)      # étape 3 → règle confirmée

Les séries sont des rendements par trade (ou par jour), indexées par date, dans l'unité choisie (bp, R, $).
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats

NW_LAGS = 5
EULER = 0.5772156649


def nw_t(x, lags: int = NW_LAGS) -> float:
    """t de la moyenne, erreur type de Newey-West (noyau de Bartlett)."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    e = x - x.mean()
    T = len(e)
    s = e @ e / T
    for k in range(1, lags + 1):
        s += 2 * (1 - k / (lags + 1)) * (e[k:] @ e[:-k]) / T
    return float(x.mean() / math.sqrt(s / T))


def holm(p) -> np.ndarray:
    """p-values ajustées de Holm (même ordre que l'entrée)."""
    p = np.asarray(p, float)
    o = np.argsort(p)
    adj = np.minimum(1, np.maximum.accumulate(p[o] * (len(p) - np.arange(len(p)))))
    out = np.empty_like(adj)
    out[o] = adj
    return out


def sr0(n: float, v: float) -> float:
    """Sharpe maximal attendu sous H0 parmi n essais de variance de Sharpe v (Bailey & López de Prado)."""
    if n <= 1:
        return 0.0
    return math.sqrt(v) * ((1 - EULER) * stats.norm.ppf(1 - 1 / n) + EULER * stats.norm.ppf(1 - 1 / (n * math.e)))


def dsr(x, n: float, sharpes_famille=None) -> float:
    """Deflated Sharpe Ratio (Sharpe par observation). V = variance des Sharpe de la famille si fournie
    (≥ 2 essais), sinon 1/(T−1) (dispersion d'échantillonnage seule)."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    T = len(x)
    sr = x.mean() / x.std(ddof=1)
    v = float(np.var(sharpes_famille, ddof=1)) if sharpes_famille is not None and len(sharpes_famille) >= 2 else 1 / (T - 1)
    sk, ku = stats.skew(x), stats.kurtosis(x, fisher=False)
    den = math.sqrt(max(1e-12, 1 - sk * sr + (ku - 1) / 4 * sr ** 2))
    return float(stats.norm.cdf((sr - sr0(n, v)) * math.sqrt(T - 1) / den))


def creux(x: pd.Series) -> float:
    eq = x.cumsum()
    return float((eq - eq.cummax()).min())


def fiche(net: pd.Series, brut: pd.Series | None = None, ref_net: pd.Series | None = None,
          n_famille: int = 1, sharpes_famille=None, tick_bp: float | None = None,
          par_an: int = 252) -> dict:
    """Fiche standard d'une règle. `ref_net` = référence triviale (même heures, autre règle simple), alignée par date.
    `tick_bp` = valeur d'un tick dans l'unité de `net` (pour le test « coût + 1 tick »)."""
    net = net.dropna()
    yrs = pd.DatetimeIndex(pd.to_datetime(net.index)).year
    by_year = net.groupby(yrs).sum()
    best = by_year.idxmax()
    half = len(net) // 2
    t = nw_t(net)
    f = {
        "n": len(net),
        "debut": str(pd.to_datetime(net.index).min().date()),
        "fin": str(pd.to_datetime(net.index).max().date()),
        "brut_moy": float(brut.dropna().mean()) if brut is not None else np.nan,
        "net_moy": float(net.mean()),
        "net_med": float(net.median()),
        "ecart_type": float(net.std()),
        "sharpe_an": float(net.mean() / net.std() * math.sqrt(par_an)),
        "t_nw": t,
        "p_unilateral": float(stats.norm.sf(t)),
        "gagnants_%": float(100 * (net > 0).mean()),
        "pire_creux": creux(net),
        "annees_pos": f"{int((by_year > 0).sum())}/{len(by_year)}",
        "net_moitie1": float(net.iloc[:half].mean()),
        "net_moitie2": float(net.iloc[half:].mean()),
        "net_sans_meilleure_annee": float(net[yrs != best].mean()),
        "net_cout_plus_1_tick": float(net.mean() - tick_bp.mean()) if isinstance(tick_bp, pd.Series)
        else (float(net.mean() - tick_bp) if tick_bp is not None else np.nan),
        "n_famille": n_famille,
        "dsr_famille": dsr(net.values, n_famille, sharpes_famille),
    }
    if ref_net is not None:
        d = pd.concat([net, ref_net], axis=1, join="inner").dropna()
        diff = d.iloc[:, 0] - d.iloc[:, 1]
        f["ref_net_moy"] = float(d.iloc[:, 1].mean())
        f["ecart_ref"] = float(diff.mean())
        f["t_ecart_ref"] = nw_t(diff)
    return f


def barriere_exploration(f: dict) -> tuple[bool, list[str]]:
    """Étape 1 → 2 : a-t-on le droit de dépenser une réserve ? (PROTOCOLE.md, barrière B1)"""
    tests = {
        "t NW net ≥ 2,0": f["t_nw"] >= 2.0,
        "DSR (N = famille) ≥ 0,95": f["dsr_famille"] >= 0.95,
        "bat la référence triviale (t écart ≥ 1,0)": f.get("t_ecart_ref", np.nan) >= 1.0,
        "net > 0 dans les deux moitiés": f["net_moitie1"] > 0 and f["net_moitie2"] > 0,
        "net > 0 sans la meilleure année": f["net_sans_meilleure_annee"] > 0,
        "net > 0 avec 1 tick de coût en plus": not (f["net_cout_plus_1_tick"] <= 0),
    }
    return all(tests.values()), [f"{'✅' if v else '❌'} {k}" for k, v in tests.items()]


def verdict_confirmation(f: dict, p_ajuste: float | None = None) -> tuple[bool, list[str]]:
    """Étape 3 : verdict sur la réserve (PROTOCOLE.md, critères C1-C4). `p_ajuste` = p de Holm si plusieurs règles."""
    p = f["p_unilateral"] if p_ajuste is None else p_ajuste
    tests = {
        "C1 net > 0, p unilatéral (Holm) ≤ 0,05": p <= 0.05 and f["net_moy"] > 0,
        "C2 net > référence triviale": f.get("ecart_ref", np.nan) > 0,
        "C3 net > 0 sans la meilleure année": f["net_sans_meilleure_annee"] > 0,
        "C4 net > 0 avec 1 tick de coût en plus": not (f["net_cout_plus_1_tick"] <= 0),
    }
    return all(tests.values()), [f"{'✅' if v else '❌'} {k}" for k, v in tests.items()]


def imprimer(f: dict, titre: str = "Fiche") -> str:
    lignes = [f"== {titre}"] + [f"  {k:<26} {v:.4g}" if isinstance(v, float) else f"  {k:<26} {v}" for k, v in f.items()]
    s = "\n".join(lignes)
    print(s)
    return s
