import numpy as np
import pandas as pd

from fab.protocole import barriere_exploration, dsr, fiche, holm, nw_t, verdict_confirmation


def _serie(mu, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2016-01-01", periods=n)
    return pd.Series(rng.normal(mu, 1.0, n), index=idx)


def test_nw_t_egal_t_iid_sans_autocorrelation():
    x = _serie(0.1).values
    t_iid = x.mean() / x.std(ddof=1) * np.sqrt(len(x))
    assert abs(nw_t(x, lags=0) - t_iid) / t_iid < 0.01


def test_holm():
    adj = holm([0.01, 0.04, 0.03])
    assert np.allclose(adj, [0.03, 0.06, 0.06])


def test_dsr_baisse_avec_n():
    x = _serie(0.05).values
    assert dsr(x, 1) > dsr(x, 100) > dsr(x, 10_000)


def test_fiche_et_barrieres():
    fort = _serie(0.15)
    ref = _serie(0.0, seed=1)
    f = fiche(fort, fort + 0.1, ref, n_famille=1, tick_bp=0.05)
    ok, raisons = barriere_exploration(f)
    assert ok, raisons
    assert verdict_confirmation(f)[0]
    nul = _serie(0.0, seed=2)
    f0 = fiche(nul, None, ref, n_famille=12, tick_bp=0.05)
    assert not barriere_exploration(f0)[0]
    assert not verdict_confirmation(f0)[0]
