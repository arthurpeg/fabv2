"""Anti-fuite, sur DONNÉES SYNTHÉTIQUES (générées ici, jamais des cotations)."""

import numpy as np
import pandas as pd
import pytest

from gap.data import Sample, curves, open_at
from gap.walkforward import LeakError, walk_forward

RNG = np.random.default_rng(1)


def synthetic_bars(start="2025-01-06 00:00", minutes=600) -> pd.DataFrame:
    """Barres 1 min synthétiques : close = numéro de minute, open = close − 0,5."""
    idx = pd.date_range(start, periods=minutes, freq="1min", tz="UTC")
    c = np.arange(minutes, dtype=float) + 1000
    return pd.DataFrame({"open": c - 0.5, "close": c}, index=idx)


def test_curve_points_only_use_finished_bars():
    px = synthetic_bars()
    start = pd.DatetimeIndex([pd.Timestamp("2025-01-06 01:00", tz="UTC")])
    end = start + pd.Timedelta(minutes=30)
    C, missing, last_end = curves(px, start, end, step_min=5)
    # point à 01:05 = close de la barre 01:04 (finie à 01:05), pas de la barre 01:05
    assert C[0, 1] == 1000 + 64
    assert C[0, 0] == 1000 + 60 - 0.5  # open de la première barre de la fenêtre
    assert last_end[0] == end[0]  # dernière barre utilisée finie exactement à la fin
    assert missing[0] == 0


def test_curve_ignores_bars_before_window_and_stale_prices():
    px = synthetic_bars().iloc[:30]  # rien après 00:30
    start = pd.DatetimeIndex([pd.Timestamp("2025-01-06 03:00", tz="UTC")])
    C, missing, _ = curves(px, start, start + pd.Timedelta(minutes=20), step_min=5)
    assert missing[0] == 1.0


def test_open_at_slack():
    px = synthetic_bars().drop(pd.Timestamp("2025-01-06 02:00", tz="UTC"))
    p, ts = open_at(px, pd.DatetimeIndex([pd.Timestamp("2025-01-06 02:00", tz="UTC")]))
    assert p[0] == 1000 + 121 - 0.5 and pd.Timestamp(ts[0]) == pd.Timestamp("2025-01-06 02:01")
    p, _ = open_at(px.iloc[:100], pd.DatetimeIndex([pd.Timestamp("2025-01-06 05:00", tz="UTC")]))
    assert np.isnan(p[0])


def synthetic_sample(n=160, G=13) -> Sample:
    days = pd.bdate_range("2024-01-01", periods=n)
    t_dec = (days + pd.Timedelta(hours=7, minutes=55)).tz_localize("UTC")
    curves_ = {m: 100 + RNG.normal(size=(n, G)).cumsum(axis=1) for m in ["A", "B"]}
    last = {m: t_dec - pd.Timedelta(minutes=5) for m in curves_}
    z = np.zeros(n)
    return Sample(days, t_dec, curves_, last, RNG.normal(0, 0.01, n), {15: RNG.normal(0, 0.003, n)},
                  t_dec, z + 100, {15: t_dec}, {15: z + 100}, z * np.nan, {15: z * np.nan},
                  np.zeros(n, bool), z, z, z)


CFG = {"walkforward": {"initial_train": 60, "refit_every": 20, "scheme": "expanding"},
       "npfda": {"h_quantiles": [0.1, 0.5, 0.9], "mode_grid": 50, "cpi_level": 0.9},
       "features": {"n_pc": 3}}


def test_walk_forward_trains_strictly_before_each_prediction():
    s = synthetic_sample()
    out = walk_forward(s, ["A", "B"], {"A": s.y_a, "B15": s.y_b[15]}, CFG)
    for p in out.values():
        assert len(p) == len(s) - 60
        assert (p["train_end"] < p.index).all()
        assert (p["last_feature_end"] <= p["t_decision"]).all()
        assert (p["n_train"] >= 60).all()


def test_rolling_window_has_fixed_length():
    s = synthetic_sample()
    cfg = {**CFG, "walkforward": {**CFG["walkforward"], "scheme": "rolling", "rolling_train": 50}}
    p = walk_forward(s, ["A"], {"A": s.y_a}, cfg)["A"]
    assert (p["n_train"] == 50).all()


def test_leak_is_detected():
    s = synthetic_sample()
    s.last_end["B"] = s.last_end["B"].copy()
    bad = s.last_end["B"].to_numpy().copy()
    bad[100] = s.t_decision[100] + pd.Timedelta(minutes=1)
    s.last_end["B"] = pd.DatetimeIndex(bad)
    with pytest.raises(LeakError):
        walk_forward(s, ["A", "B"], {"A": s.y_a}, CFG)


def test_feature_peeking_at_target_would_be_caught():
    """Contrôle de bon sens : si une variable contenait la cible, NP-FDA la
    retrouverait. Le pipeline réel n'y a pas accès (audit ci-dessus)."""
    s = synthetic_sample()
    s.curves["A"][:, -1] = s.curves["A"][:, 0] * (1 + 50 * s.y_a)  # fuite délibérée
    p = walk_forward(s, ["A"], {"A": s.y_a}, CFG)["A"]
    assert np.corrcoef(p["np_mean"], p["y"])[0, 1] > 0.5
