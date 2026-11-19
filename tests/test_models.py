"""Modèles sur DONNÉES SYNTHÉTIQUES (générées ici, bonne réponse connue)."""

import numpy as np
import pytest

from gap.features import FPCA, normalize, subperiod_returns
from gap.models import NPFDA, OLS, kernel, pairwise

RNG = np.random.default_rng(0)


def test_kernel():
    assert kernel(np.array([0.0, 0.5, 1.0, 2.0])).tolist() == [1.5, 1.125, 0.0, 0.0]


def test_pairwise_matches_naive():
    A, B = RNG.normal(size=(5, 3)), RNG.normal(size=(4, 3))
    naive = np.sqrt(((A[:, None] - B[None]) ** 2).sum(-1))
    assert np.allclose(pairwise(A, B), naive)


def test_ols_recovers_coefficients():
    X = RNG.normal(size=(500, 2))
    y = 0.1 + X @ [2.0, -1.0]
    assert np.allclose(OLS().fit(X, y).coef_, [0.1, 2.0, -1.0])


def test_npfda_mean_tracks_smooth_function():
    z = RNG.uniform(-1, 1, size=(800, 1))
    y = np.sin(3 * z[:, 0]) + RNG.normal(0, 0.05, 800)
    m = NPFDA().fit(z, y)
    q = np.array([[-0.5], [0.0], [0.5]])
    assert np.allclose(m.predict(q).mean, np.sin(3 * q[:, 0]), atol=0.1)


def test_npfda_uniform_weights_give_sample_statistics():
    # bimodal : 70 % autour de +1, 30 % autour de −1 → moyenne ≈ 0,4, mode ≈ +1
    z = RNG.normal(size=(1000, 2))
    y = np.where(RNG.uniform(size=1000) < 0.7, 1.0, -1.0) + RNG.normal(0, 0.05, 1000)
    m = NPFDA().fit(z, y)
    m.h_ = 1e9  # poids uniformes
    f = m.predict(np.zeros((1, 2)))
    assert f.mean[0] == pytest.approx(y.mean(), abs=1e-9)
    assert f.median[0] == pytest.approx(np.quantile(np.sort(y), 0.5, method="inverted_cdf"), abs=1e-9)
    assert f.mode[0] == pytest.approx(1.0, abs=0.1)
    assert f.p_up[0] == pytest.approx((y > 0).mean(), abs=1e-9)
    assert f.lo[0] == pytest.approx(np.quantile(y, 0.05, method="inverted_cdf"), abs=1e-9)
    assert f.hi[0] == pytest.approx(np.quantile(y, 0.95, method="inverted_cdf"), abs=1e-9)


def test_npfda_no_neighbour_means_no_signal():
    z = RNG.normal(size=(200, 2))
    m = NPFDA().fit(z, RNG.normal(size=200))
    f = m.predict(np.full((1, 2), 1e6))
    assert f.no_signal[0] and f.mean[0] == 0 and f.mode[0] == 0 and f.p_up[0] == 0.5 and np.isnan(f.lo[0])


def test_cv_bandwidth_small_with_structure_large_without():
    z = RNG.uniform(-1, 1, size=(600, 1))
    structured = NPFDA().fit(z, np.sign(z[:, 0]) + RNG.normal(0, 0.1, 600))
    noise = NPFDA().fit(z, RNG.normal(size=600))
    assert structured.h_ < noise.h_


def test_cpi_coverage_on_iid_data():
    z = RNG.normal(size=(600, 2))
    m = NPFDA().fit(z, RNG.normal(size=600))
    zt, yt = RNG.normal(size=(3000, 2)), RNG.normal(size=3000)
    f = m.predict(zt)
    ok = ~f.no_signal
    cov = ((f.lo <= yt) & (yt <= f.hi))[ok].mean()
    assert 0.85 < cov < 0.95


def test_fpca_fit_only_on_train():
    X = RNG.normal(size=(100, 20)).cumsum(axis=1)
    p = FPCA(5).fit(X[:60])
    comp = p.components_.copy()
    p.transform(X[60:])
    assert np.allclose(p.components_, comp)
    assert np.allclose(comp @ comp.T, np.eye(5), atol=1e-10)
    assert np.allclose(p.transform(X[:60]).mean(axis=0), 0, atol=1e-10)


def test_normalize_and_subperiods():
    C = np.array([[100.0] * 12 + [110.0] * 15 + [121.0] * 12])  # 39 points : 3 h 10 en pas de 5 min
    assert normalize(C)[0, 0] == 100.0 and normalize(C * 2)[0, -1] == pytest.approx(121.0)
    r = subperiod_returns(C)
    assert r[0, 0] == pytest.approx(0.1) and r[0, 2] == pytest.approx(0.1)
