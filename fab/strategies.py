"""Les 93 tests pré-enregistrés (PREREGISTRATION.md). Chaque fonction renvoie un
DataFrame de trades ; le moteur vectorbt (core.backtest) fait le reste."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .core import ASSETS, LDN, Asset, Grid, grid, hm, past_median, past_std, simple_trades, trades_frame

TOKYO, SYDNEY, NY = "Asia/Tokyo", "Australia/Sydney", "America/New_York"


def session_grid(a: Asset) -> Grid:
    return grid(a.name, a.tz, a.open_min, a.close_min + 5)


# --------------------------------------------------------------------------- M1


def _prev_close(g: Grid, a: Asset) -> pd.Series:
    return g.price_at(a.close_min)[0].shift(1)


def m1(a: Asset, g: Grid, variant: str) -> pd.DataFrame:
    prev = _prev_close(g, a)
    last = a.close_min - 30
    if variant == "a":
        pred = g.price_at(a.open_min + 30)[0] / prev - 1
    else:
        pred = g.price_at(last)[0] / prev - 1
    sig = np.sign(pred)
    if variant == "c":
        z = pred / past_std(pred)
        cols = [m for m in g.H.columns if a.open_min <= m < last]
        rng = (g.H[cols].max(axis=1) - g.L[cols].min(axis=1)) / g.price_at(a.open_min)[0]
        sig = sig.where((z.abs() > 1) & (rng > past_median(rng)), 0)
    return simple_trades(g, sig, last, a.close_min)


def m1d_eia(a: Asset, g: Grid) -> pd.DataFrame:
    prev = _prev_close(g, a)
    gao = g.price_at(a.open_min + 30)[0] / prev - 1
    eia = g.price_at(hm("11:00"))[0] / g.price_at(hm("10:30"))[0] - 1
    is_wed = pd.Series(g.dates.dayofweek == 2, index=g.dates)
    pred = eia.where(is_wed, gao)
    return simple_trades(g, np.sign(pred), a.close_min - 30, a.close_min)


# --------------------------------------------------------------------------- M2


def m2_noise(a: Asset, g: Grid) -> pd.DataFrame:
    o, c = a.open_min, a.close_min
    day_open = g.price_at(o)[0]
    prev = _prev_close(g, a)
    cols = list(range(o, c))
    C = g.C[cols].ffill(axis=1)
    move = C.div(day_open, axis=0).sub(1).abs()
    sigma = move.shift(1).rolling(14, min_periods=10).mean()
    tp = (g.H[cols] + g.L[cols] + g.C[cols]) / 3
    V = g.V[cols].fillna(0)
    vwap = (tp.fillna(0) * V).cumsum(axis=1) / V.cumsum(axis=1).replace(0, np.nan)
    up_base = np.maximum(day_open, prev)
    lo_base = np.minimum(day_open, prev)
    checks = list(range(o + 30, c, 30))
    exec_px = {m: g.price_at(m) for m in checks + [c]}
    rows = []
    for d in g.dates:
        if not (np.isfinite(up_base[d]) and np.isfinite(lo_base[d])):
            continue
        pos, entry = 0, None
        for m in checks:
            x, s, v = C.at[d, m - 1], sigma.at[d, m - 1], vwap.at[d, m - 1]
            if not (np.isfinite(x) and np.isfinite(s)):
                continue
            ub, lb = up_base[d] * (1 + s), lo_base[d] * (1 - s)
            v = v if np.isfinite(v) else x
            new = pos
            if pos == 1 and x < max(ub, v):
                new = 0
            elif pos == -1 and x > min(lb, v):
                new = 0
            if new == 0:
                new = 1 if x > ub else (-1 if x < lb else 0)
                if pos != 0 and new == pos:  # pas de ré-entrée dans le sens qu'on vient de stopper
                    new = 0
            if new != pos:
                px, mm = exec_px[m][0][d], exec_px[m][1][d]
                if not np.isfinite(px):
                    continue
                if pos != 0:
                    rows.append({**entry, "m_out": mm, "p_out": px})
                entry = {"date": d, "m_in": mm, "p_in": px, "dir": new, "f_in": 1.0} if new else None
                pos = new
        if pos != 0:
            px, mm = exec_px[c][0][d], exec_px[c][1][d]
            rows.append({**entry, "m_out": mm, "p_out": px})
    t = trades_frame(rows)
    t["f_in"] = g.factor_at(o).reindex(t["date"]).values
    return t


# --------------------------------------------------------------------------- M3


def m3_orb(a: Asset, g: Grid, minutes: int, rvol_filter: bool = False) -> pd.DataFrame:
    o, c = a.open_min, a.close_min
    rcols = list(range(o, o + minutes))
    orh, orl = g.H[rcols].max(axis=1), g.L[rcols].min(axis=1)
    allowed = pd.Series(True, index=g.dates)
    if rvol_filter:
        vol = g.V[rcols].sum(axis=1, min_count=1)
        allowed = vol > 1.5 * vol.shift(1).rolling(14, min_periods=10).mean()
    tcols = list(range(o + minutes, c))
    H, L, O = g.H[tcols].values, g.L[tcols].values, g.O[tcols].values
    exit_px, exit_m = g.price_at(c)
    fac = g.factor_at(o)
    rows = []
    for i, d in enumerate(g.dates):
        hi, lo = orh.iat[i], orl.iat[i]
        if not (allowed.iat[i] and np.isfinite(hi) and np.isfinite(lo) and hi > lo):
            continue
        h, l, op = H[i], L[i], O[i]
        up = np.nan_to_num(h, nan=-np.inf) >= hi
        dn = np.nan_to_num(l, nan=np.inf) <= lo
        hit = np.flatnonzero(up | dn)
        if hit.size == 0:
            continue
        j = hit[0]
        if up[j] and dn[j]:
            continue
        side = 1 if up[j] else -1
        level = hi if side == 1 else lo
        p_in = max(op[j], level) if side == 1 else min(op[j], level)
        if not np.isfinite(p_in):
            p_in = level
        stop = lo if side == 1 else hi
        # stop vérifié dès la barre d'entrée (hypothèse prudente)
        stop_hit = (np.nan_to_num(l[j:], nan=np.inf) <= stop) if side == 1 else (np.nan_to_num(h[j:], nan=-np.inf) >= stop)
        k = np.flatnonzero(stop_hit)
        if k.size:
            jj = j + k[0]
            p_out = stop if jj == j or not np.isfinite(op[jj]) else (min(op[jj], stop) if side == 1 else max(op[jj], stop))
            m_out = tcols[jj] + 1 if jj == j else tcols[jj]
            # une sortie dans la même minute que l'entrée est décalée d'une minute pour l'horodatage
        else:
            p_out, m_out = exit_px.iat[i], exit_m.iat[i]
        rows.append({"date": d, "m_in": tcols[j], "p_in": p_in, "m_out": m_out, "p_out": p_out, "dir": side, "f_in": fac.iat[i]})
    return trades_frame(rows)


# --------------------------------------------------------------------------- M4


def m4a_open_move(a: Asset, g: Grid) -> pd.DataFrame:
    r = g.price_at(a.open_min + 30)[0] / g.price_at(a.open_min)[0] - 1
    z = r / past_std(r)
    sign = -1 if a.kind == "index" else 1
    sig = (np.sign(z) * sign).where(z.abs() > 2, 0)
    return simple_trades(g, sig, a.open_min + 30, a.close_min)


def gap_z(a: Asset, g: Grid) -> pd.Series:
    gap = g.price_at(a.open_min)[0] / _prev_close(g, a) - 1
    return gap / past_std(gap)


def m4b_gap_fade(a: Asset, g: Grid, zmin: float = 2, zmax: float = np.inf) -> pd.DataFrame:
    z = gap_z(a, g)
    sig = (-np.sign(z)).where((z.abs() > zmin) & (z.abs() <= zmax), 0)
    return simple_trades(g, sig, a.open_min + 1, a.close_min)


def m4c_next_day(a: Asset, g: Grid) -> pd.DataFrame:
    close = g.price_at(a.close_min)[0]
    r = close / close.shift(1) - 1
    z = r / past_std(r)
    sign = -1 if a.kind == "gold" else 1
    sig = (np.sign(z) * sign).where(z.abs() > 2, 0).shift(1)  # signal d'hier → trade aujourd'hui
    return simple_trades(g, sig, a.open_min, a.close_min)


# --------------------------------------------------------------------------- M5


def clock(name: str, tz: str, start: str, end: str, direction: int) -> tuple[pd.DataFrame, Grid]:
    s, e = hm(start), hm(end)
    g = grid(name, tz, s, e + 5)
    sig = pd.Series(direction, index=g.dates)
    return simple_trades(g, sig, s, e), g


# --------------------------------------------------------------------------- registre


def registry():
    """Itère sur (nom, actif, fabrique) ; la fabrique renvoie (trades, tz, dates)."""
    tests = []
    for a in ASSETS.values():
        for v in "abc":
            tests.append((f"M1{v}", a, lambda a=a, v=v: _with_session(a, lambda g: m1(a, g, v))))
    cl = ASSETS["CL"]
    tests.append(("M1d_EIA", cl, lambda: _with_session(cl, lambda g: m1d_eia(cl, g))))
    for n in ["ES", "NQ", "YM"]:
        a = ASSETS[n]
        tests.append(("M2_noise", a, lambda a=a: _with_session(a, lambda g: m2_noise(a, g))))
    for a in ASSETS.values():
        tests.append(("M3a_ORB30", a, lambda a=a: _with_session(a, lambda g: m3_orb(a, g, 30))))
        tests.append(("M3b_ORB5", a, lambda a=a: _with_session(a, lambda g: m3_orb(a, g, 5))))
        tests.append(("M3c_ORB30_rvol", a, lambda a=a: _with_session(a, lambda g: m3_orb(a, g, 30, True))))
        tests.append(("M4a_open_move", a, lambda a=a: _with_session(a, lambda g: m4a_open_move(a, g))))
    for n in ["ES", "NQ", "YM"]:
        a = ASSETS[n]
        tests.append(("M4b_gap_fade", a, lambda a=a: _with_session(a, lambda g: m4b_gap_fade(a, g))))
    for n in ["GC", "CL"]:
        a = ASSETS[n]
        tests.append(("M4c_next_day", a, lambda a=a: _with_session(a, lambda g: m4c_next_day(a, g))))
    es = ASSETS["ES"]
    tests.append(("M5a_EU_open_long", es, lambda: _clock("ES", NY, "01:00", "05:00", 1)))
    for n in ["6E", "6B", "6J", "6A"]:
        a = ASSETS[n]
        # future = devise/USD : long USD = short future
        tests.append(("M5b_LDNfix_pre", a, lambda n=n: _clock(n, LDN, "15:00", "16:00", -1)))
        tests.append(("M5b_LDNfix_post", a, lambda n=n: _clock(n, LDN, "16:00", "17:00", 1)))
        tests.append(("M5c_TKYfix_pre", a, lambda n=n: _clock(n, TOKYO, "08:55", "09:55", -1)))
        tests.append(("M5c_TKYfix_post", a, lambda n=n: _clock(n, TOKYO, "09:55", "10:55", 1)))
    for n, tz, s, e in [("6E", LDN, "08:00", "12:00"), ("6B", LDN, "08:00", "12:00"),
                        ("6J", TOKYO, "09:00", "15:00"), ("6A", SYDNEY, "10:00", "16:00")]:
        tests.append(("M5d_home_hours_short", ASSETS[n], lambda n=n, tz=tz, s=s, e=e: _clock(n, tz, s, e, -1)))
    return tests


_GRIDS: dict[str, Grid] = {}


def _with_session(a: Asset, fn):
    if a.name not in _GRIDS:
        _GRIDS[a.name] = session_grid(a)
    g = _GRIDS[a.name]
    return fn(g), a.tz, g.dates


def _clock(name, tz, s, e, direction):
    t, g = clock(name, tz, s, e, direction)
    return t, tz, g.dates
