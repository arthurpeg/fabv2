"""Réplications fidèles (PREREGISTRATION_3.md, règles tirées de PAPER_SPECS.md)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .core import ASSETS, LDN, NY, Asset, Grid, Result, backtest, grid, hm, simple_trades, trades_frame
from .strategies import TOKYO, _GRIDS, m2_noise, session_grid

SYDNEY = "Australia/Sydney"
GMT3 = "Etc/GMT-3"  # GMT+3 fixe
FX = ["6E", "6J", "6B", "6A"]
IDX = ["ES", "NQ", "YM"]


def sgrid(a: Asset) -> Grid:
    if a.name not in _GRIDS:
        _GRIDS[a.name] = session_grid(a)
    return _GRIDS[a.name]


def to_tz(t: pd.DataFrame, src: str, dst: str) -> pd.DataFrame:
    """Réexprime des trades (date, minutes locales) d'un fuseau dans un autre."""
    t = t.copy()
    for col in ["m_in", "m_out"]:
        wall = pd.to_datetime(t["date"]) + pd.to_timedelta(t[col], unit="min")
        ts = wall.dt.tz_localize(src, ambiguous="NaT", nonexistent="NaT").dt.tz_convert(dst).dt.tz_localize(None)
        t[col + "_ts"] = ts
    t = t.dropna(subset=["m_in_ts", "m_out_ts"])
    t["date"] = t["m_in_ts"].dt.normalize()
    t["m_in"] = (t["m_in_ts"] - t["date"]).dt.total_seconds() / 60
    t["m_out"] = (t["m_out_ts"] - t["date"]).dt.total_seconds() / 60
    return t.drop(columns=["m_in_ts", "m_out_ts"])


def run_legs(name: str, a: Asset, legs: list[tuple[pd.DataFrame, str]], tz: str, dates: pd.Index) -> Result:
    t = pd.concat([to_tz(x, src, tz) for x, src in legs]).sort_values("m_in", kind="stable")
    t = t.sort_values(["date", "m_in"]).reset_index(drop=True)
    return backtest(name, a, trades_frame(t), tz, dates)


def scaled(res: Result, lev: pd.Series) -> Result:
    L = lev.reindex(res.daily_net.index).fillna(0.0)
    return Result(res.name, res.asset, res.trades, res.daily_net * L, res.daily_gross * L)


# --------------------------------------------------------------------------- R1 / R2


def intraday_mom(a: Asset, g: Grid, o: int, c: int, mode: str) -> pd.DataFrame:
    prev = g.price_at(c)[0].shift(1)
    onfh = g.price_at(o + 30)[0] / prev - 1
    rod = g.price_at(c - 30)[0] / prev - 1
    if mode == "gao_joint":  # η(r1, r12)
        r12 = g.price_at(c - 30)[0] / g.price_at(c - 60)[0] - 1
        sig = pd.Series(np.where((onfh > 0) & (r12 > 0), 1, np.where((onfh <= 0) & (r12 <= 0), -1, 0)), index=g.dates)
        sig = sig.where(onfh.notna() & r12.notna(), 0)
    elif mode == "rod":
        sig = np.where(rod > 0, 1, -1)
        sig = pd.Series(sig, index=g.dates).where(rod.notna(), 0)
    elif mode == "onfh":
        sig = pd.Series(np.where(onfh > 0, 1, -1), index=g.dates).where(onfh.notna(), 0)
    elif mode == "joint":
        sig = pd.Series(np.where((onfh > 0) & (rod > 0), 1, np.where((onfh <= 0) & (rod <= 0), -1, 0)), index=g.dates)
        sig = sig.where(onfh.notna() & rod.notna(), 0)
    return simple_trades(g, sig, c - 30, c)


FX_O, FX_C = hm("08:20"), hm("15:00")


def fx_grid(n: str) -> Grid:
    key = n + "_fxET"
    if key not in _GRIDS:
        _GRIDS[key] = grid(n, NY, FX_O, FX_C + 5)
    return _GRIDS[key]


# --------------------------------------------------------------------------- R3


def vol_target_lev(a: Asset, g: Grid) -> pd.Series:
    close = g.price_at(a.close_min)[0]
    ret = close.pct_change()
    sd = ret.shift(1).rolling(14, min_periods=14).std()
    return np.minimum(4.0, 0.02 / sd)


# --------------------------------------------------------------------------- R4


def orb_candle(a: Asset, g: Grid) -> tuple[pd.DataFrame, pd.Series]:
    o, c = a.open_min, a.close_min
    rc = list(range(o, o + 5))
    O1 = g.price_at(o)[0]
    C1 = g.C[rc].ffill(axis=1).iloc[:, -1]
    H1, L1 = g.H[rc].max(axis=1), g.L[rc].min(axis=1)
    tc = list(range(o + 5, c))
    H, L, Op = g.H[tc].values, g.L[tc].values, g.O[tc].values
    exit_px, exit_m = g.price_at(c)
    fac = g.factor_at(o)
    rows, lev = [], {}
    for i, d in enumerate(g.dates):
        o1, c1, h1, l1 = O1.iat[i], C1.iat[i], H1.iat[i], L1.iat[i]
        if not np.all(np.isfinite([o1, c1, h1, l1])) or abs(c1 - o1) <= a.tick * fac.iat[i]:
            continue
        side = 1 if c1 > o1 else -1
        p_in = Op[i, 0]
        if not np.isfinite(p_in):
            continue
        stop = l1 if side == 1 else h1
        R = (p_in - stop) * side
        if R <= 0:
            continue
        target = p_in + side * 10 * R
        hh, ll, oo = H[i], L[i], Op[i]
        st_hit = (np.nan_to_num(ll, nan=np.inf) <= stop) if side == 1 else (np.nan_to_num(hh, nan=-np.inf) >= stop)
        tg_hit = (np.nan_to_num(hh, nan=-np.inf) >= target) if side == 1 else (np.nan_to_num(ll, nan=np.inf) <= target)
        ks, kt = np.flatnonzero(st_hit), np.flatnonzero(tg_hit)
        js = ks[0] if ks.size else 10**9
        jt = kt[0] if kt.size else 10**9
        if js == 10**9 and jt == 10**9:
            p_out, m_out = exit_px.iat[i], exit_m.iat[i]
        elif js <= jt:  # stop prioritaire si même barre (prudent)
            j = js
            gap = np.isfinite(oo[j]) and ((oo[j] < stop) if side == 1 else (oo[j] > stop))
            p_out, m_out = (oo[j] if gap else stop), tc[j] + (1 if j == 0 else 0)
        else:
            j = jt
            gap = np.isfinite(oo[j]) and ((oo[j] > target) if side == 1 else (oo[j] < target))
            p_out, m_out = (oo[j] if gap else target), tc[j] + (1 if j == 0 else 0)
        rows.append({"date": d, "m_in": tc[0], "p_in": p_in, "m_out": m_out, "p_out": p_out, "dir": side, "f_in": fac.iat[i]})
        lev[d] = min(4.0, 0.01 / (R / p_in))
    return trades_frame(rows), pd.Series(lev)


# --------------------------------------------------------------------------- R5 / R6


def window(n: str, tz: str, s: str, e: str, direction: int) -> pd.DataFrame:
    si, ei = hm(s), hm(e)
    key = f"{n}|{tz}|{si}|{ei}"
    if key not in _GRIDS:
        _GRIDS[key] = grid(n, tz, si, ei + 5)
    g = _GRIDS[key]
    return simple_trades(g, pd.Series(direction, index=g.dates), si, ei)


def et_dates(n: str) -> pd.Index:
    return fx_grid(n).dates


# --------------------------------------------------------------------------- R7


def day_grid(n: str) -> Grid:
    key = n + "_gmt3"
    if key not in _GRIDS:
        _GRIDS[key] = grid(n, GMT3, 0, 1439)
    return _GRIDS[key]


def abnormal_inputs(g: Grid):
    p_open, m_open = g.price_at(0, slack=240)
    p_end, m_end = g.price_at(1435, slack=5)
    R = p_end / p_open - 1
    mu = R.shift(1).rolling(252, min_periods=150).mean()
    sd = R.shift(1).rolling(252, min_periods=150).std()
    return p_open, m_open, p_end, m_end, R, mu + 2 * sd, mu - 2 * sd


def caporale_s1(a: Asset) -> pd.DataFrame:
    g = day_grid(a.name)
    p_open, m_open, p_end, m_end, R, up, dn = abnormal_inputs(g)
    C = g.C.ffill(axis=1)
    rows = []
    for i, d in enumerate(g.dates):
        po, u, l = p_open.iat[i], up.iat[i], dn.iat[i]
        if not (np.isfinite(po) and np.isfinite(u) and np.isfinite(l)) or pd.isna(m_open.iat[i]):
            continue
        for h in range(1, 24):
            m = 60 * h
            if m <= m_open.iat[i]:
                continue
            x = C.iat[i, m - 1]  # close de la barre qui finit à h:00
            if not np.isfinite(x):
                continue
            cum = x / po - 1
            side = 1 if cum > u else (-1 if cum < l else 0)
            if side:
                px, mm = g.price_at(m)[0].iat[i], g.price_at(m)[1].iat[i]
                if np.isfinite(px) and np.isfinite(p_end.iat[i]) and m_end.iat[i] > mm:
                    rows.append({"date": d, "m_in": mm, "p_in": px, "m_out": m_end.iat[i], "p_out": p_end.iat[i],
                                 "dir": side, "f_in": g.F.iat[i, m]})
                break
    return trades_frame(rows)


def caporale_s2(a: Asset) -> pd.DataFrame:
    g = day_grid(a.name)
    p_open, m_open, p_end, m_end, R, up, dn = abnormal_inputs(g)
    flag = pd.Series(np.where(R > up, 1, np.where(R < dn, -1, 0)), index=g.dates).shift(1).fillna(0)
    p6, m6 = g.price_at(hm("06:00"))
    fac = g.factor_at(0)
    rows = []
    for i, d in enumerate(g.dates):
        f = flag.iat[i]
        if f == 0 or not np.isfinite(p_open.iat[i]):
            continue
        if a.kind == "oil":
            side, po, mo = int(f), p_end.iat[i], m_end.iat[i]
        else:  # or : contrarien
            side = -int(f)
            po, mo = (p6.iat[i], m6.iat[i]) if f > 0 else (p_end.iat[i], m_end.iat[i])
        rows.append({"date": d, "m_in": m_open.iat[i], "p_in": p_open.iat[i], "m_out": mo, "p_out": po,
                     "dir": side, "f_in": fac.iat[i]})
    return trades_frame(rows)


# --------------------------------------------------------------------------- registre


def registry():
    """(id, actif, fabrique) ; la fabrique renvoie un Result."""
    T = []
    for n in IDX:
        a = ASSETS[n]
        T.append(("R1_gao_joint", a, lambda a=a: (lambda g: backtest("R1", a, intraday_mom(a, g, a.open_min, a.close_min, "gao_joint"), a.tz, g.dates))(sgrid(a))))
    for n in FX:
        a = ASSETS[n]
        for mode, rid in [("rod", "R2a_balt_ROD_fxET"), ("onfh", "R2b_balt_ONFH_fxET")]:
            T.append((rid, a, lambda a=a, mode=mode: (lambda g: backtest("R2", a, intraday_mom(a, g, FX_O, FX_C, mode), NY, g.dates))(fx_grid(a.name))))
    for a in ASSETS.values():
        if a.kind == "fx":
            T.append(("R2c_balt_joint", a, lambda a=a: (lambda g: backtest("R2c", a, intraday_mom(a, g, FX_O, FX_C, "joint"), NY, g.dates))(fx_grid(a.name))))
        else:
            T.append(("R2c_balt_joint", a, lambda a=a: (lambda g: backtest("R2c", a, intraday_mom(a, g, a.open_min, a.close_min, "joint"), a.tz, g.dates))(sgrid(a))))
    for n in IDX:
        a = ASSETS[n]
        T.append(("R3_noise_voltarget", a, lambda a=a: (lambda g: scaled(backtest("R3", a, m2_noise(a, g), a.tz, g.dates), vol_target_lev(a, g)))(sgrid(a))))
    for n in ["NQ", "ES", "YM"]:
        a = ASSETS[n]
        def r4(a=a):
            g = sgrid(a)
            t, lev = orb_candle(a, g)
            return scaled(backtest("R4", a, t, a.tz, g.dates), lev)
        T.append(("R4_orb5_candle_10R", a, r4))
    for n in FX:
        a = ASSETS[n]
        T.append(("R5a_krohn_tokyo", a, lambda n=n, a=a: run_legs("R5a", a, [
            (window(n, TOKYO, "08:00", "09:55", -1), TOKYO), (window(n, TOKYO, "09:55", "15:00", 1), TOKYO)], TOKYO,
            window_dates(n, TOKYO, "08:00", "15:00"))))
        T.append(("R5b_krohn_europe", a, lambda n=n, a=a: run_legs("R5b", a, [
            (window(n, NY, "02:00", "08:15", -1), NY), (window(n, NY, "11:00", "16:55", 1), NY)], NY, et_dates(n))))
    legs6 = {
        "6E": [((NY, "02:00", "08:00", -1)), ((NY, "08:00", "16:00", 1))],
        "6B": [((NY, "02:00", "08:00", -1)), ((NY, "08:00", "16:00", 1))],
        "6A": [((SYDNEY, "10:00", "16:00", -1)), ((NY, "08:00", "16:00", 1))],
        "6J": [((TOKYO, "08:00", "15:00", -1)), ((NY, "08:00", "16:00", 1))],
    }
    for n, legs in legs6.items():
        a = ASSETS[n]
        T.append(("R6_breedon_ranaldo", a, lambda n=n, a=a, legs=legs: run_legs("R6", a, [
            (window(n, tz, s, e, d), tz) for tz, s, e, d in legs], NY, et_dates(n))))
    for n in ["GC", "CL"]:
        a = ASSETS[n]
        T.append(("R7a_caporale_s1", a, lambda a=a: backtest("R7a", a, caporale_s1(a), GMT3, day_grid(a.name).dates)))
        T.append(("R7b_caporale_s2", a, lambda a=a: backtest("R7b", a, caporale_s2(a), GMT3, day_grid(a.name).dates)))
    return T


def window_dates(n, tz, s, e):
    window(n, tz, s, e, 1)
    return _GRIDS[f"{n}|{tz}|{hm(s)}|{hm(e)}"].dates
