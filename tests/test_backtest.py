"""Moteur vectorbt et règles de trading, sur DONNÉES SYNTHÉTIQUES."""

import numpy as np
import pandas as pd

from gap.backtest import arithmetic, diebold_mariano, permutation_test, simulate, trading_metrics
from gap.signals import npfda_positions, ols_positions

RNG = np.random.default_rng(2)


def synthetic_days(n=50):
    days = pd.bdate_range("2025-01-06", periods=n)
    entry = (days + pd.Timedelta(hours=7, minutes=55)).tz_localize("UTC")
    exit_ = entry + pd.Timedelta(minutes=20)
    pe = 20000 * np.exp(RNG.normal(0, 0.01, n).cumsum())
    px = pe * (1 + RNG.normal(0, 0.003, n))
    return days, entry, exit_, pe, px


def test_vectorbt_matches_arithmetic_pnl():
    days, entry, exit_, pe, px = synthetic_days()
    w = RNG.choice([-1.0, -0.4, 0.0, 0.3, 1.0], size=len(days))
    W = pd.DataFrame({"s": w, "flat": 0.0}, index=days)
    r = simulate(entry, exit_, pe, px, W, cost_rt_pts=0.7)
    assert np.allclose(r["s"].values, arithmetic(w, pe, px, 0.7), atol=2e-6)
    assert (r["flat"] == 0).all()


def test_no_leverage_and_costs_hurt():
    days, entry, exit_, pe, px = synthetic_days()
    w = np.ones(len(days))
    gross = simulate(entry, exit_, pe, px, pd.DataFrame({"x": w}, index=days), 0.0)["x"]
    net = simulate(entry, exit_, pe, px, pd.DataFrame({"x": w}, index=days), 5.0)["x"]
    assert (net < gross).all()
    assert np.allclose(gross.values, px / pe - 1, atol=2e-6)  # 1× exactement


def test_trading_metrics_counts():
    r = pd.Series([0.01, 0.0, -0.005, 0.002])
    m = trading_metrics(r, np.array([1.0, 0.0, -0.5, 0.2]))
    assert m["n_trades"] == 3 and m["exposure_%"] == 75 and round(m["hit_%"], 6) == round(200 / 3, 6)


def test_permutation_detects_real_signal_and_not_noise():
    n = 600
    pe = np.full(n, 20000.0)
    move = RNG.normal(0, 0.003, n)
    px = pe * (1 + move)
    p_signal, _ = permutation_test(np.sign(move), pe, px, 0.0, 300, 0)
    p_noise, _ = permutation_test(RNG.choice([-1.0, 1.0], n), pe, px, 0.0, 300, 0)
    assert p_signal < 0.01 and p_noise > 0.01


def test_diebold_mariano_direction():
    y = RNG.normal(size=1000)
    good, bad = y + RNG.normal(0, 0.1, 1000), y + RNG.normal(0, 1, 1000)
    assert diebold_mariano(y - bad, y - good)[1] < 0.01
    assert diebold_mariano(y - good, y - bad)[1] > 0.99


def test_signal_filters():
    p = pd.DataFrame({
        "np_mode": [0.002, 0.002, -0.002, 0.002, 0.0], "np_mean": [0.001, 0.001, -0.004, 0.00001, 0.001],
        "np_median": [0.001] * 5, "p_up": [0.7, 0.5, 0.2, 0.9, 0.9], "m_ref": [0.002] * 5,
        "ols": [0.001, 0.001, 0.001, 0.001, 0.001], "no_signal": [False, False, False, False, True],
    })
    sig = {"direction": "mode", "p_min": 0.55, "cost_mult": 1.0, "agreement": False}
    w = npfda_positions(p, np.full(5, 0.00003), sig)
    assert w.tolist() == [0.5, 0.0, -1.0, 0.0, 0.0]  # confiance, taille plafonnée, coûts, pas de signal
    assert npfda_positions(p, np.full(5, 0.00003), {**sig, "agreement": True})[2] == 0.0
    assert ols_positions(p, np.full(5, 0.002), sig).tolist() == [0.0] * 5
