"""Pré-enregistrement n° 27 : Zhang (2018, SSRN 3138756), sessions intraday du FX sur les 7 majeures.

uv run --with arch --with statsmodels python run_zhang.py   → results/zhang/ (*.csv) + résumé à l'écran

Grille horaire 00:00-23:00 GMT du lundi au vendredi (comme Datastream). Prix en dollars par unité
de devise étrangère. Sessions : domestique 08-16 locales, LDN-NY 08-11 NY, US 11-17 NY, non-US = le
reste ; les sessions peuvent se recouvrir, sauf non-US (voir PREREGISTRATION_27.md).
Période R (réplication) 2010-05-03 → 2015-12-31 : spot Dukascopy. Période O 2016-01-01 → 2026-08-28 :
futures 6E/6B/6J/6A (roulements : règle de run_sessions.py) et spot Dukascopy pour CHF, CAD, NZD.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats as st
from statsmodels.stats.oneway import anova_oneway

sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")
OUT = Path("results/zhang")
FX = Path("D:/quant-data/Cotations/forex")
NY = "America/New_York"
# devise → (place domestique, fichier spot, signe pour avoir USD par devise, future)
CUR = {
    "EUR": ("Europe/Berlin", "EURUSD", 1, "6E"),
    "GBP": ("Europe/London", "GBPUSD", 1, "6B"),
    "JPY": ("Asia/Tokyo", "USDJPY", -1, "6J"),
    "CHF": ("Europe/Zurich", "USDCHF", -1, None),
    "AUD": ("Australia/Sydney", "AUDUSD", 1, "6A"),
    "CAD": ("America/Toronto", "USDCAD", -1, None),
    "NZD": ("Pacific/Auckland", "NZDUSD", 1, None),
}
TICK = {"6E": 0.00005, "6B": 0.0001, "6J": 0.0000005, "6A": 0.0001}
PERIODS = {"R": ("2010-05-03", "2016-01-01"), "O": ("2016-01-01", "2026-08-29")}
SESS = ["dom", "ldn", "us", "nonus"]
# Table 1 du papier (moyennes en %, étoiles) pour la comparaison
PAPER = {
    "AUD": ("-0.0165", "-0.0161*", "0.0071", "0.0185*"),
    "JPY": ("0.0095", "0.0090", "-0.0212***", "-0.0136*"),
    "NZD": ("-0.0260**", "-0.0185*", "-0.0047", "0.0310***"),
    "CHF": ("0.0374**", "0.0270**", "0.0134", "-0.0412***"),
    "EUR": ("-0.0210*", "-0.0063", "0.0221***", "-0.0067"),
    "GBP": ("-0.0148", "-0.0044", "0.0166***", "-0.0039"),
    "CAD": ("-0.0169", "-0.0250***", "0.0080", "-0.0041"),
}


def load_future(code: str) -> pd.Series:
    """Clôtures 1 min .v.0 ajustées en ratio (règle de run_sessions.py::load)."""
    df = pd.read_parquet(FX / f"{code}_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    gap = df["open"] / df["close"].shift() - 1
    ix = df.index
    prev = pd.Series(ix, index=ix).shift()
    cand = (ix.hour == 0) & (ix.minute == 0) & ((ix - prev) <= pd.Timedelta(minutes=60)).values
    cand &= ix.month.isin([3, 6, 9, 12]) & (ix.day >= 7) & (ix.day <= 22)
    g = gap[cand]
    rolls = pd.DatetimeIndex(g.abs().groupby([g.index.year, g.index.month]).idxmax().tolist())
    step = pd.Series(1.0, index=ix)
    step.loc[rolls] = 1 + gap.loc[rolls]
    factor = step[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
    print(f"  {code} : {len(rolls)} roulements, |écart| médian {gap.loc[rolls].abs().median() * 1e4:.1f} bp")
    s = df["close"] * factor
    s.attrs["raw"] = df["close"]
    return s


def hourly_grid(close: pd.Series, a: str, b: str) -> pd.Series:
    """Prix à chaque heure pleine H (lun-ven, 00-23 GMT) = dernière clôture d'une barre commencée avant H."""
    p = close.resample("1h", label="right", closed="left").last().dropna()
    grid = pd.date_range(pd.Timestamp(a, tz="UTC") - pd.Timedelta(days=7), pd.Timestamp(b, tz="UTC"),
                         freq="1h", inclusive="left")
    grid = grid[grid.dayofweek < 5]
    return p.reindex(p.index.union(grid)).ffill().reindex(grid)


def sessions(r: pd.Series, place: str) -> pd.DataFrame:
    """Rendements de session (bp) à partir des rendements horaires r indexés par la fin de l'heure."""
    start = r.index - pd.Timedelta(hours=1)
    loc = start.tz_convert(place).hour
    ny = start.tz_convert(NY).hour
    us_hours = (ny >= 8) & (ny < 17)
    masks = {
        "dom": (loc >= 8) & (loc < 16),
        "ldn": (ny >= 8) & (ny < 11),
        "us": (ny >= 11) & (ny < 17),
        "nonus": ~((loc >= 8) & (loc < 16)) & ~us_hours,
    }
    rows = []
    for name, m in masks.items():
        m = pd.Series(m, index=r.index)
        run = (m != m.shift()).cumsum()
        g = pd.DataFrame({"r": r, "run": run})[m.values]
        agg = g.groupby("run").agg(ret=("r", "sum"), rv=("r", lambda x: np.sqrt((x ** 2).sum())), n=("r", "size"))
        t = g.reset_index().groupby("run")["index"].agg(["min", "max"])
        agg["start"] = t["min"] - pd.Timedelta(hours=1)
        agg["end"] = t["max"]
        agg = agg.iloc[1:-1]  # sessions coupées aux bords
        agg["sess"] = name
        rows.append(agg)
    out = pd.concat(rows, ignore_index=True)
    out[["ret", "rv"]] *= 1e4
    return out.sort_values("start").reset_index(drop=True)


def nw_t(x: pd.Series, lags: int = 5) -> float:
    res = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return float(res.tvalues[0])


def eq4(s: pd.DataFrame, garch: bool = False):
    X = pd.DataFrame({"const": 1.0, "rv": s.rv})
    for j in ["ldn", "us", "nonus"]:
        X[f"rv_{j}"] = s.rv * (s.sess == j)
    if not garch:
        res = sm.OLS(s.ret.values, X.values).fit(cov_type="HC1")
        return dict(zip(X.columns, res.params)), dict(zip(X.columns, res.tvalues)), res.rsquared_adj
    from arch import arch_model
    res = arch_model(s.ret.values, x=X.drop(columns="const").values, mean="LS", vol="GARCH", p=1, q=1).fit(disp="off")
    names = ["const"] + list(X.columns[1:])
    return dict(zip(names, res.params.values[:5])), dict(zip(names, res.tvalues.values[:5])), np.nan


def eq2_garch(s: pd.DataFrame) -> dict:
    """Équation (2) : AR(k, BIC ≤ 5) + 4 indicatrices de session, erreurs GARCH(1,1)."""
    from arch import arch_model
    y = s.ret.reset_index(drop=True)
    D = pd.get_dummies(s.sess.reset_index(drop=True)).reindex(columns=SESS).astype(float)
    best = None
    for k in range(6):
        X = pd.concat([D] + [y.shift(i).rename(f"l{i}") for i in range(1, k + 1)], axis=1).iloc[5:]
        bic = sm.OLS(y.iloc[5:].values, X.values).fit().bic
        if best is None or bic < best[0]:
            best = (bic, k, X)
    _, k, X = best
    from arch.univariate import LS, GARCH  # sans constante : les 4 indicatrices la remplacent
    m = LS(y.iloc[5:].values, x=X.values, constant=False)
    m.volatility = GARCH(1, 0, 1)
    r2 = m.fit(disp="off")
    p = pd.Series(r2.params.values[:4], index=SESS)
    t = pd.Series(r2.tvalues.values[:4], index=SESS)
    return {"k": k, **{f"b_{j}": p[j] for j in SESS}, **{f"tb_{j}": t[j] for j in SESS}}


def holm(p: pd.Series) -> pd.Series:
    o = p.sort_values()
    adj = (o * np.arange(len(o), 0, -1)).cummax().clip(upper=1)
    return adj.reindex(p.index)


def star(p: float) -> str:
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("Chargement")
    spot = {c: pd.read_parquet(f"cache/dukascopy/{v[1]}_1h.parquet") for c, v in CUR.items()}
    fut = {c: load_future(v[3]) for c, v in CUR.items() if v[3]}
    tests, comp, garch_rows, yearly, costs, wk = [], [], [], [], [], []
    for per, (a, b) in PERIODS.items():
        print(f"\n===== Période {per} : {a} → {b}")
        for c, (place, pair, sgn, code) in CUR.items():
            use_fut = per == "O" and code is not None
            if use_fut:
                close = fut[c]
            else:
                d = spot[c]
                close = d["mid_close"] if sgn == 1 else 1 / d["mid_close"]
            P = hourly_grid(close, a, b)
            r = np.log(P).diff().dropna()
            s = sessions(r, place)
            s = s[(s.start >= pd.Timestamp(a, tz="UTC")) & (s.end <= pd.Timestamp(b, tz="UTC"))]
            s.assign(cur=c, period=per).to_csv(OUT / f"sessions_{per}_{c}.csv", index=False)
            g = {j: s.ret[s.sess == j] for j in SESS}
            # variante sans le rendement du week-end (heure qui finit le lundi 00:00 GMT)
            rw = r.where(~((r.index.dayofweek == 0) & (r.index.hour == 0)), 0.0)
            sw = sessions(rw, place)
            sw = sw[(sw.start >= pd.Timestamp(a, tz="UTC")) & (sw.end <= pd.Timestamp(b, tz="UTC"))]
            wk.append({"period": per, "cur": c, **{f"{j}_bp": sw.ret[sw.sess == j].mean() for j in SESS},
                       **{f"t_{j}": nw_t(sw.ret[sw.sess == j]) for j in SESS}})
            row = {"period": per, "cur": c, "src": code if use_fut else "spot"}
            for j in SESS:
                x = g[j]
                row[f"{j}_bp"] = x.mean()
                row[f"{j}_t"] = x.mean() / x.std() * np.sqrt(len(x))
                row[f"{j}_p2"] = 2 * st.t.sf(abs(row[f"{j}_t"]), len(x) - 1)
                row[f"{j}_nwt"] = nw_t(x)
                row[f"{j}_n"] = len(x)
            for j in ["ldn", "us", "nonus"]:
                tt = st.ttest_ind(g["dom"], g[j], equal_var=False)
                row[f"dom_vs_{j}_t"] = tt.statistic
                row[f"dom_vs_{j}_p"] = tt.pvalue
            wf = anova_oneway([g[j].values for j in SESS], use_var="unequal")
            row["welch_F"], row["welch_p"] = wf.statistic, wf.pvalue
            co, tv, r2 = eq4(s)
            row.update({f"eq4_{k}": v for k, v in co.items()}, **{f"eq4_t_{k}": v for k, v in tv.items()}, eq4_r2=r2)
            comp.append(row)
            # tests à verdict
            n_d, n_u = len(g["dom"]), len(g["us"])
            tests += [
                {"period": per, "cur": c, "hyp": "H1 dom<0", "stat": row["dom_nwt"], "p": st.norm.cdf(row["dom_nwt"])},
                {"period": per, "cur": c, "hyp": "H2 us>0", "stat": row["us_nwt"], "p": st.norm.sf(row["us_nwt"])},
                {"period": per, "cur": c, "hyp": "H3 phi<0", "stat": tv["rv"], "p": st.norm.cdf(tv["rv"])},
            ]
            # GARCH (rapporté)
            try:
                gr = {"period": per, "cur": c, **eq2_garch(s)}
                co_g, tv_g, _ = eq4(s.reset_index(drop=True), garch=True)
                gr.update({f"eq4g_{k}": v for k, v in co_g.items()}, **{f"eq4g_t_{k}": v for k, v in tv_g.items()})
            except Exception as e:  # noqa: BLE001
                gr = {"period": per, "cur": c, "err": str(e)}
            garch_rows.append(gr)
            # par année et moitiés de O
            for j in SESS:
                x = s[s.sess == j]
                for y, v in x.groupby(x.end.dt.year).ret:
                    yearly.append({"period": per, "cur": c, "sess": j, "year": y, "bp": v.mean(), "n": len(v)})
            # coût
            if use_fut:
                raw = fut[c].attrs["raw"]
                px = raw.resample("1D").last().dropna()
                cost = (TICK[code] / px * 1e4).median()
                costs.append({"period": per, "cur": c, "kind": "1 tick aller-retour", **{j: cost for j in SESS}})
            else:
                d = spot[c]
                spr = (1e4 * d["spread_close"] / d["mid_close"])
                spr.index = spr.index + pd.Timedelta(hours=1)  # écart à l'heure H = fin de la barre
                cc = {}
                for j in SESS:
                    x = s[s.sess == j]
                    s0 = spr.reindex(pd.DatetimeIndex(x.start)).values
                    s1 = spr.reindex(pd.DatetimeIndex(x.end)).values
                    cc[j] = np.nanmedian((s0 + s1) / 2)
                costs.append({"period": per, "cur": c, "kind": "demi-spread entrée + sortie (médiane)", **cc})
            print(f"  {c} ({row['src']:>4}) dom {row['dom_bp']:+6.2f} bp (t {row['dom_t']:+.2f}) | "
                  f"ldn {row['ldn_bp']:+6.2f} ({row['ldn_t']:+.2f}) | us {row['us_bp']:+6.2f} ({row['us_t']:+.2f}) | "
                  f"nonus {row['nonus_bp']:+6.2f} ({row['nonus_t']:+.2f}) | Welch F {row['welch_F']:.2f} p {row['welch_p']:.3f}"
                  f" | φ {co['rv']:+.3f} (t {tv['rv']:+.2f})")
    T = pd.DataFrame(tests)
    T["p_holm"] = T.groupby("period", group_keys=False).p.apply(holm)
    T["pass"] = T.p_holm <= 0.05
    C = pd.DataFrame(comp)
    Y = pd.DataFrame(yearly)
    for df, name in [(T, "tests"), (C, "sessions_summary"), (pd.DataFrame(garch_rows), "garch"), (Y, "by_year"),
                     (pd.DataFrame(costs), "costs"), (pd.DataFrame(wk), "sans_weekend")]:
        df.to_csv(OUT / f"{name}.csv", index=False)

    # moitiés de O (critère de stabilité)
    halves = []
    for c in CUR:
        s = pd.read_csv(OUT / f"sessions_O_{c}.csv", parse_dates=["start", "end"])
        for j in SESS:
            x = s[s.sess == j]
            h1 = x[x.end < pd.Timestamp("2021-01-01", tz="UTC")].ret
            h2 = x[x.end >= pd.Timestamp("2021-01-01", tz="UTC")].ret
            halves.append({"cur": c, "sess": j, "2016-2020_bp": h1.mean(), "t1": nw_t(h1),
                           "2021-2026_bp": h2.mean(), "t2": nw_t(h2)})
    H = pd.DataFrame(halves)
    H.to_csv(OUT / "halves_O.csv", index=False)

    print("\n===== Tests à verdict (Holm sur 21 par période)")
    print(T.round(4).to_string(index=False))
    print("\n===== Comparaison avec la Table 1 (période R, moyennes en bp, t simple)")
    for _, r in C[C.period == "R"].iterrows():
        pp = PAPER[r.cur]
        cells = []
        for j, ptxt in zip(SESS, pp):
            pm = float(ptxt.rstrip("*")) * 100
            cells.append(f"{j} {r[f'{j}_bp']:+5.2f}{star(r[f'{j}_p2']):3} (papier {pm:+5.2f}{ptxt.count('*') * '*':3})")
        print(f"  {r.cur} : " + " | ".join(cells))
    print("\n===== Moitiés de O")
    print(H.round(2).to_string(index=False))
    print("\n===== GARCH")
    print(pd.DataFrame(garch_rows).round(3).to_string(index=False))
    print("\n===== Coûts (bp)")
    print(pd.DataFrame(costs).round(2).to_string(index=False))
    print("\n===== Sans week-end (bp, t NW)")
    print(pd.DataFrame(wk).round(2).to_string(index=False))


if __name__ == "__main__":
    main()
