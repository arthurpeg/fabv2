"""Règles de trading (variante B) : prévisions → position signée w ∈ [−1, 1].

- sens : signe du prédicteur choisi (mode par défaut, ou moyenne, médiane) ;
- taille : min(1, |moyenne conditionnelle| / m_ref), m_ref = médiane de |y| à l'entraînement ;
- filtre de confiance : P̂(y > 0) > p_min pour acheter, < 1 − p_min pour vendre ;
- filtre de coûts : |moyenne conditionnelle| > c × coût aller-retour (en rendement) ;
- filtre d'accord (optionnel) : même signe que le MCO.
Pour le MCO tradé : sens et taille tirés de ŷ, filtre de coûts seulement.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def npfda_positions(p: pd.DataFrame, cost_rt: np.ndarray, sig: dict) -> np.ndarray:
    d = np.sign(p[f"np_{sig['direction']}"].values)
    mean = p["np_mean"].values
    size = np.minimum(1.0, np.abs(mean) / p["m_ref"].values)
    conf = ((d > 0) & (p["p_up"].values > sig["p_min"])) | ((d < 0) & (p["p_up"].values < 1 - sig["p_min"]))
    cost_ok = np.abs(mean) > sig["cost_mult"] * cost_rt
    agree = np.sign(p["ols"].values) == d if sig.get("agreement") else True
    return np.where(conf & cost_ok & agree & ~p["no_signal"].values.astype(bool), d * size, 0.0)


def ols_positions(p: pd.DataFrame, cost_rt: np.ndarray, sig: dict) -> np.ndarray:
    yhat = p["ols"].values
    size = np.minimum(1.0, np.abs(yhat) / p["m_ref"].values)
    return np.where(np.abs(yhat) > sig["cost_mult"] * cost_rt, np.sign(yhat) * size, 0.0)
