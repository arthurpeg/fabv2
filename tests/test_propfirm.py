import numpy as np
import pandas as pd

from propfirm.days import NEVER, build
from propfirm.ftmo import Market, run_eval, run_funded


def _day(prices):
    o = np.array(prices[:-1], float)
    c = np.array(prices[1:], float)
    return pd.DataFrame({"open": o, "high": np.maximum(o, c), "low": np.minimum(o, c), "close": c})


def test_day_library_long_short():
    # +1 % puis −2 % : long touche +1 R (s = 1 %) avant le stop ; short touche son stop d'abord
    bars = {pd.Timestamp("2020-01-02"): _day([100, 101, 99, 98])}
    lib = build(bars, 0.01)
    assert lib.tp_bar[0, 0, 19] == 0          # niveau 1,0 R long : barre 0
    assert lib.stop_bar[0, 1] == 0            # stop short (101) : barre 0
    assert lib.stop_bar[0, 0] == 1 and lib.stop_R[0, 0] == 1.0  # stop long (99) : barre 1
    assert np.isclose(lib.eod_R[0, 0], -2.0)


def test_stop_slippage_on_gap():
    bars = {pd.Timestamp("2020-01-02"): pd.DataFrame(
        {"open": [100, 97], "high": [100.2, 97], "low": [99.5, 96], "close": [99.6, 96]})}
    lib = build(bars, 0.01)
    assert lib.stop_bar[0, 0] == 1 and np.isclose(lib.stop_R[0, 0], 3.0)  # rempli à l'open 97
    assert lib.tp_bar[0, 1, 0] == 0 or lib.tp_bar[0, 1, 0] == NEVER


def test_binary_eval_near_gamblers_ruin():
    # Sans coût ni suiveuse, P(+10 avant −10) = 50 % ; la suiveuse et la règle des 50 % font baisser
    m = Market(None, 1e9)  # coût en R ≈ 0
    ok, _ = run_eval(m, 2.0, 2.0, 20_000, np.random.default_rng(0))
    assert 0.30 < ok.mean() < 0.50


def test_funded_pays_only_after_cycle():
    m = Market(None, 1e9)
    paid, n, days, first = run_funded(m, 1.0, 1.0, 5_000, np.random.default_rng(1), cycle=10)
    assert (first[first > 0] >= 10).all()
    assert (paid >= 0).all() and paid.mean() > 0
