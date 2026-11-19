"""Variables explicatives : rendements, courbes normalisées, ACP fonctionnelle.

Tout ce qui s'ajuste (moyenne, composantes, échelle) est ajusté par `fit` sur
la fenêtre d'entraînement seulement ; `transform` n'apprend rien.
"""

from __future__ import annotations

import numpy as np

from gap.data import Sample


def normalize(C: np.ndarray) -> np.ndarray:
    """x(t) / x(1) × 100."""
    return C / C[:, :1] * 100.0


def subperiod_returns(C: np.ndarray, step_min: int = 5) -> np.ndarray:
    """Rendements première heure, milieu de séance, dernière heure (n × 3)."""
    h = 60 // step_min
    return np.column_stack([C[:, h] / C[:, 0] - 1, C[:, -1 - h] / C[:, h] - 1, C[:, -1] / C[:, -1 - h] - 1])


class FPCA:
    """ACP sur courbes discrétisées. Les scores sont divisés par la racine de la
    variance totale d'entraînement, pour que chaque marché pèse autant."""

    def __init__(self, n_pc: int = 5):
        self.n_pc = n_pc

    def fit(self, X: np.ndarray) -> "FPCA":
        self.mean_ = X.mean(axis=0)
        Xc = X - self.mean_
        _, _, vt = np.linalg.svd(Xc, full_matrices=False)
        self.components_ = vt[: self.n_pc]
        self.scale_ = np.sqrt(max((Xc**2).sum(axis=1).mean(), 1e-12))
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        return (X - self.mean_) @ self.components_.T / self.scale_


class FeatureBuilder:
    """Scores ACP concaténés des marchés d'une spécification."""

    def __init__(self, markets: list[str], n_pc: int = 5):
        self.markets, self.n_pc = markets, n_pc

    def fit(self, s: Sample, idx: np.ndarray) -> "FeatureBuilder":
        self.pca_ = {m: FPCA(self.n_pc).fit(normalize(s.curves[m][idx])) for m in self.markets}
        return self

    def scores(self, s: Sample, idx: np.ndarray) -> np.ndarray:
        return np.hstack([self.pca_[m].transform(normalize(s.curves[m][idx])) for m in self.markets])

    def linear(self, s: Sample, idx: np.ndarray) -> np.ndarray:
        return s.window_returns(self.markets)[idx]

    def subperiods(self, s: Sample, idx: np.ndarray) -> np.ndarray:
        return np.hstack([subperiod_returns(s.curves[m][idx]) for m in self.markets])
