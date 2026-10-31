"""Pré-enregistrement n° 12 : la règle NQ de nuit face au bêta et à des références simples, 2011-07 → 2026-08.

uv run python run_prereg12.py   → results/prereg12/ (beta.csv, references.csv, random.csv, run.log)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import recolte1.engine as E
import recolte1.rules as RU

E.USE_2010 = True
RU.START = "2010-06-08"

import run_prereg10 as P  # noqa: E402
import run_recolte1_atr as A  # noqa: E402
from recolte1.engine import NY, _block_index, ci_mean, ci_sharpe  # noqa: E402
from recolte1.rules import at, base, monthly, next_month_sign, sessions  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg12")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
T0, T1 = "2011-07-01", "2026-08-28"
STOP = [("SL 2 ATR / TP 5 ATR", 2.0, 5.0)]
NOSTOP = [("sans stop", np.nan, np.nan)]


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


B = sessions()
D = B.index
BB = base("NQ")
MOM = next_month_sign(BB, monthly(BB, "cc").shift(1).rolling(11, min_periods=11).sum()).reindex(D).fillna(0.0)
NIGHTS = D[(D >= T0) & (D <= T1)]


def table(t_in, t_out, direction, label) -> pd.DataFrame:
    e = pd.DataFrame({"night": D, "t_in": pd.DatetimeIndex(t_in), "t_out": pd.DatetimeIndex(t_out),
                      "dir": np.asarray(direction, float), "clock": label, "forced_eod": False})
    e = e[(e["night"] >= T0) & (e["night"] <= T1) & (e["dir"] != 0)]
    return e.dropna(subset=["t_in", "t_out"])


def sim(e, variants):
    A.VARIANTS = variants
    T = A.simulate("NQ", e)
    return T


def per_night(T, cost="net"):
    return T[T["cost"] == cost].groupby("night")["ret"].sum().reindex(NIGHTS).fillna(0.0)


def describe(name, T, e=None):
    r = per_night(T)
    m, lo, hi = ci_mean(r.values * 1e4)
    s, slo, shi = ci_sharpe(r.values)
    row = {"référence": name, "trades": int((T["cost"] == "net").sum()), "bp_par_nuit": m, "bp_lo": lo, "bp_hi": hi,
           "sharpe": s, "sharpe_lo": slo, "sharpe_hi": shi, "ann_%": r.mean() * 252 * 100,
           "bp_brut_par_nuit": per_night(T, "gross").mean() * 1e4,
           "max_dd_%": float(((1 + r).cumprod() / (1 + r).cumprod().cummax() - 1).min() * 100)}
    if e is not None:
        t = T[T["cost"] == "net"]
        R = P.r_multiples("NQ", e, t).values
        row["R_par_trade"] = float(np.nanmean(R))
    return row, r


def main():
    long1 = pd.Series(1.0, index=D)
    t20, t930 = at(D, "20:00", NY, -1), B["t_open"]
    refs, series = [], {}
    cfg = [
        ("R0 règle : 20:00, SL 2 / TP 5, momentum", t20, t930, MOM, STOP, True),
        ("R1 20:00 → 9:30 sans stop, momentum", t20, t930, MOM, NOSTOP, False),
        ("R2 20:00 → 9:30 sans stop, toujours long", t20, t930, long1, NOSTOP, False),
        ("R3 18:01 → 9:30 sans stop, toujours long", at(D, "18:01", NY, -1), t930, long1, NOSTOP, False),
        ("R4 00:00 → 3:00 sans stop, toujours long", at(D, "00:00", NY), at(D, "03:00", NY), long1, NOSTOP, False),
        ("R5 16:00 → 9:30 toujours long (non intraday)", B["t_prev"], t930, long1, NOSTOP, False),
    ]
    for name, ti, to, dr, var, want_r in cfg:
        e = table(ti, to, dr, name[:2])
        T = sim(e, var)
        row, r = describe(name, T, e if want_r else None)
        refs.append(row)
        series[name[:2]] = r
        log(f"{name} : {row['bp_par_nuit']:+.2f} bp/nuit, Sharpe {row['sharpe']:.2f}")
    R = pd.DataFrame(refs)

    # R6 : entrée aléatoire entre 18:01 et 3:00 ET
    rnd = []
    base_t = at(D, "18:01", NY, -1)
    for seed in range(40):
        off = np.random.default_rng(seed).integers(0, 540, size=len(D))  # 18:01 + 0..539 min → 3:00
        ti = base_t + pd.to_timedelta(off, unit="min")
        e = table(ti, t930, MOM, "R6")
        T = sim(e, STOP)
        row, _ = describe(f"R6 seed {seed}", T, e)
        rnd.append(row)
        log(f"R6 seed {seed} : R {row['R_par_trade']:+.4f}, {row['bp_par_nuit']:+.2f} bp/nuit")
    RN = pd.DataFrame(rnd)
    RN.to_csv(OUT / "random.csv", index=False)
    r0 = R.loc[0, "R_par_trade"]
    pct = float((RN["R_par_trade"] < r0).mean() * 100)
    q95 = float(RN["R_par_trade"].quantile(0.95))
    log(f"R0 R/trade {r0:+.4f} ; aléatoire : moyenne {RN['R_par_trade'].mean():+.4f}, 95e centile {q95:+.4f} ; "
        f"R0 dépasse {pct:.0f} % des tirages → « l'heure apporte » : {r0 > q95}")
    R.loc[len(R)] = {"référence": "R6 aléatoire 18:01–3:00 (moyenne de 40 tirages)", "trades": RN["trades"].mean(),
                     "bp_par_nuit": RN["bp_par_nuit"].mean(), "sharpe": RN["sharpe"].mean(),
                     "ann_%": RN["ann_%"].mean(), "R_par_trade": RN["R_par_trade"].mean(),
                     "bp_brut_par_nuit": RN["bp_brut_par_nuit"].mean(), "max_dd_%": RN["max_dd_%"].mean()}

    # stops : Sharpe R0 − R1, bootstrap apparié par blocs
    a, b = series["R0"].values, series["R1"].values
    idx = _block_index(len(a))
    sa, sb = a[idx], b[idx]
    d = sa.mean(1) / sa.std(1) * np.sqrt(252) - sb.mean(1) / sb.std(1) * np.sqrt(252)
    dsr = (a.mean() / a.std() - b.mean() / b.std()) * np.sqrt(252)
    log(f"Sharpe R0 − R1 = {dsr:+.2f} [{np.percentile(d, 2.5):+.2f} ; {np.percentile(d, 97.5):+.2f}] "
        f"→ « les stops apportent » : {np.percentile(d, 2.5) > 0}")
    R.to_csv(OUT / "references.csv", index=False)

    # étape 1 : bêta / alpha face à NQ achat-conservation
    y = series["R0"]
    x = BB["cc"].reindex(NIGHTS)
    ok = x.notna()
    x, y = x[ok].values, y[ok].values
    beta = np.cov(x, y)[0, 1] / x.var()
    alpha = y.mean() - beta * x.mean()
    idx = _block_index(len(x))
    xs, ys = x[idx], y[idx]
    bs = ((xs - xs.mean(1, keepdims=True)) * (ys - ys.mean(1, keepdims=True))).sum(1) / ((xs - xs.mean(1, keepdims=True)) ** 2).sum(1)
    al = ys.mean(1) - bs * xs.mean(1)
    sh = lambda v: v.mean() / v.std() * np.sqrt(252)
    beta_out = pd.DataFrame([{
        "beta": beta, "corr": float(np.corrcoef(x, y)[0, 1]),
        "alpha_ann_%": alpha * 252 * 100, "alpha_lo_%": np.percentile(al, 2.5) * 252 * 100,
        "alpha_hi_%": np.percentile(al, 97.5) * 252 * 100,
        "ret_ann_regle_%": y.mean() * 252 * 100, "ret_ann_NQ_%": x.mean() * 252 * 100,
        "sharpe_regle": sh(y), "sharpe_NQ": sh(x), "sharpe_beta_NQ": sh(beta * x),
        "part_expliquee_par_beta_%": beta * x.mean() / y.mean() * 100,
    }])
    beta_out.to_csv(OUT / "beta.csv", index=False)
    pd.set_option("display.width", 250)
    log(beta_out.round(3).T.to_string())
    log(R.round(3).to_string())


if __name__ == "__main__":
    main()
