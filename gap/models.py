"""MCO et régression fonctionnelle à noyau non paramétrique (NP-FDA).

NP-FDA (Ferraty & Vieu, repris par De Gooijer et al. 2009) :
- semi-métrique : distance euclidienne entre scores ACP concaténés ;
- noyau quadratique K(u) = 1,5 (1 − u²) sur [0, 1] ;
- poids W_s = K(d(x_s, x)/h) / Σ_r K(d(x_r, x)/h) ;
- F̂(y|x) = Σ_s W_s 1{y_s ≤ y}, d'où la moyenne, la médiane, le mode et le CPI ;
- h choisi par leave-one-out sur l'entraînement (erreur absolue de la médiane).
Si tous les poids sont nuls (aucun voisin à moins de h) : « pas de signal ».
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def kernel(u: np.ndarray) -> np.ndarray:
    return np.where(u < 1.0, 1.5 * (1.0 - u**2), 0.0)


def pairwise(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    d2 = (A**2).sum(1)[:, None] + (B**2).sum(1)[None, :] - 2.0 * A @ B.T
    return np.sqrt(np.maximum(d2, 0.0))


class OLS:
    def fit(self, X: np.ndarray, y: np.ndarray) -> "OLS":
        Z = np.column_stack([np.ones(len(X)), X])
        self.coef_, *_ = np.linalg.lstsq(Z, y, rcond=None)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.coef_[0] + X @ self.coef_[1:]


@dataclass
class NPForecast:
    mean: np.ndarray
    median: np.ndarray
    mode: np.ndarray
    p_up: np.ndarray  # P̂(y > 0)
    lo: np.ndarray  # CPI
    hi: np.ndarray
    no_signal: np.ndarray


def _weighted_quantiles(W: np.ndarray, y_sorted: np.ndarray, qs: list[float]) -> list[np.ndarray]:
    """Quantiles de F̂ pour chaque ligne ; W déjà ordonné comme y_sorted, lignes de somme 1."""
    cum = np.cumsum(W, axis=1)
    return [y_sorted[np.minimum((cum < q - 1e-12).sum(axis=1), len(y_sorted) - 1)] for q in qs]


class NPFDA:
    def __init__(self, h_quantiles=(0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
                 mode_grid: int = 200, cpi_level: float = 0.90):
        self.h_quantiles, self.mode_grid, self.cpi_level = tuple(h_quantiles), mode_grid, cpi_level

    def _weights(self, D: np.ndarray, h: float) -> tuple[np.ndarray, np.ndarray]:
        K = kernel(D / h)
        tot = K.sum(axis=1, keepdims=True)
        empty = tot[:, 0] <= 0
        return K / np.where(tot > 0, tot, 1.0), empty

    def fit(self, Z: np.ndarray, y: np.ndarray) -> "NPFDA":
        order = np.argsort(y, kind="stable")
        self.Z_, self.y_ = Z[order], y[order]
        D = pairwise(self.Z_, self.Z_)
        iu = np.triu_indices(len(y), 1)
        self.h_grid_ = np.quantile(D[iu], self.h_quantiles)
        np.fill_diagonal(D, np.inf)  # leave-one-out
        self.cv_mae_ = np.empty(len(self.h_grid_))
        for i, h in enumerate(self.h_grid_):
            W, empty = self._weights(D, h)
            (med,) = _weighted_quantiles(W, self.y_, [0.5])
            pred = np.where(empty, 0.0, med)
            self.cv_mae_[i] = np.abs(self.y_ - pred).mean()
        self.h_ = float(self.h_grid_[int(np.argmin(self.cv_mae_))])
        n, sd = len(y), y.std(ddof=1)
        self.h_y_ = 1.06 * sd * n ** (-1 / 5)
        self.grid_ = np.linspace(self.y_[0], self.y_[-1], self.mode_grid)
        self.Ky_ = kernel(np.abs(self.grid_[:, None] - self.y_[None, :]) / self.h_y_)  # G × n
        return self

    def predict(self, Z: np.ndarray) -> NPForecast:
        W, empty = self._weights(pairwise(Z, self.Z_), self.h_)
        a = (1 - self.cpi_level) / 2
        lo, med, hi = _weighted_quantiles(W, self.y_, [a, 0.5, 1 - a])
        mode = self.grid_[np.argmax(W @ self.Ky_.T, axis=1)]
        z = lambda v: np.where(empty, 0.0, v)  # noqa: E731
        return NPForecast(
            mean=z(W @ self.y_), median=z(med), mode=z(mode), p_up=np.where(empty, 0.5, W @ (self.y_ > 0)),
            lo=np.where(empty, np.nan, lo), hi=np.where(empty, np.nan, hi), no_signal=empty,
        )
