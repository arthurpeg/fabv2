"""Corrélation entre sessions successives sur NQ (Asie → Europe → US), 1 minute Databento.

uv run python run_nq_sessions_corr.py   → results/nq_sessions_corr/ (run.log, pairs.csv,
by_period.csv, quintiles.csv, follow.csv, sessions.csv)

Exploratoire, non pré-enregistré, demandé en séance. Question : quand une session finit en
hausse, la suivante a-t-elle tendance à monter aussi ?

Bornes (heures murales, heure d'été gérée par fuseau ; jour = séance NYSE, calendrier XNYS) :
  prev     clôture NYSE de la veille (16:00 NY)
  eu_open  08:00 Londres (ouverture des actions européennes)
  hk_close 16:00 Hong Kong (clôture HKEX = 08:00 UTC, dernière grande clôture asiatique)
  us_open  09:30 NY
  eu_close 16:30 Londres (clôture cash européenne, 17:30 Paris/Francfort ≈ 11:30 NY)
  us_close 16:00 NY

Deux façons de couper chaque session :
  variante A (« la session s'arrête quand la suivante ouvre ») :
    Asie = prev → eu_open ; Europe = eu_open → us_open ; US = us_open → us_close
  variante B (« on attend la vraie clôture ») :
    Asie = prev → hk_close, puis on regarde le reste de l'Europe hk_close → us_open
      (en hiver hk_close = eu_open : B = A ; l'écart n'existe qu'en heure d'été, 1 h)
    Europe = eu_open → eu_close, puis on regarde le reste de l'US eu_close → us_close
Demi-séances NYSE (clôture 13:00, avant eu_close) exclues. Données arrêtées au 2026-08-28
(holdout non touché).

Prix à un instant = clôture ajustée (ratio aux roulements, recolte1.engine.load avec
l'historique 2010) de la dernière barre démarrant dans [T-5 min, T-1 min].

Mesures pour chaque paire X → Y : corrélation de Pearson et de Spearman, pente de Y sur X
avec t robuste (White), P(Y > 0 | X > 0) contre P(Y > 0 | X < 0), moyenne de Y selon le signe
et le quintile de X, par sous-période. Contrôle tradable : position Y = signe(X), backtest
vectorbt (entrée/sortie aux bornes de Y), net = 1 tick + 5 $ aller-retour, comparé au long
seul sur la même fenêtre.
"""

from __future__ import annotations

from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd
import vectorbt as vbt
from scipy import stats as st

import recolte1.engine as E

E.USE_2010 = True

OUT = Path("results/nq_sessions_corr")
NY, LDN, HK = "America/New_York", "Europe/London", "Asia/Hong_Kong"
END = "2026-08-28"
COST_PTS = E.SPECS["NQ"].rt_cost  # 0,25 + 5 / 20 = 0,5 point aller-retour
PERIODS = [("2010-2015", "2010", "2015"), ("2016-2019", "2016", "2019"),
           ("2020-2022", "2020", "2022"), ("2023-2026", "2023", "2026")]

# (étiquette, variante, X = (début, fin), Y = (début, fin))
PAIRS = [
    ("Asie → Europe", "A", ("prev", "eu_open"), ("eu_open", "us_open")),
    ("Asie → US", "A", ("prev", "eu_open"), ("us_open", "us_close")),
    ("Asie → Europe+US", "A", ("prev", "eu_open"), ("eu_open", "us_close")),
    ("Asie (clôture HK) → reste Europe", "B", ("prev", "hk_close"), ("hk_close", "us_open")),
    ("Asie (clôture HK) → US", "B", ("prev", "hk_close"), ("us_open", "us_close")),
    ("Europe → US", "A", ("eu_open", "us_open"), ("us_open", "us_close")),
    ("Europe (clôture 16:30 Ldn) → reste US", "B", ("eu_open", "eu_close"), ("eu_close", "us_close")),
    ("Nuit (Asie+Europe) → US", "A", ("prev", "us_open"), ("us_open", "us_close")),
]

LINES: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


def bounds() -> pd.DataFrame:
    df = E.load("NQ")
    sched = xc.get_calendar("XNYS").schedule.loc[str(df.index[0].date()):END]
    d = pd.DatetimeIndex(sched.index)
    b = pd.DataFrame(index=d)
    b["t_prev"] = sched["close"].shift(1)
    b["t_eu_open"] = E.at(d, "08:00", LDN)
    b["t_hk_close"] = E.at(d, "16:00", HK)
    b["t_us_open"] = sched["open"]
    b["t_eu_close"] = E.at(d, "16:30", LDN)
    b["t_us_close"] = sched["close"]
    b = b.iloc[1:]
    b = b[b["t_us_close"].dt.tz_convert(NY).dt.hour == 16]  # demi-séances exclues
    for k in ["prev", "eu_open", "hk_close", "us_open", "eu_close", "us_close"]:
        b[f"p_{k}"], b[f"f_{k}"] = E.price_at("NQ", b[f"t_{k}"])
    return b


def ret(b: pd.DataFrame, s: str, e: str) -> pd.Series:
    return b[f"p_{e}"] / b[f"p_{s}"] - 1


def white_t(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Pente MCO de y sur x et t robuste à l'hétéroscédasticité (HC1)."""
    xc_ = x - x.mean()
    beta = (xc_ * (y - y.mean())).sum() / (xc_ ** 2).sum()
    u = y - y.mean() - beta * xc_
    n = len(x)
    var = n / (n - 2) * (xc_ ** 2 * u ** 2).sum() / (xc_ ** 2).sum() ** 2
    return beta, beta / np.sqrt(var)


def describe(x: pd.Series, y: pd.Series) -> dict:
    ok = x.notna() & y.notna() & (x != 0)
    x, y = x[ok], y[ok]
    up, dn = y[x > 0], y[x < 0]
    beta, tb = white_t(x.values, y.values)
    tw = st.ttest_ind(up, dn, equal_var=False)
    # test de proportions P(Y>0 | X>0) - P(Y>0 | X<0)
    p1, p2 = (up > 0).mean(), (dn > 0).mean()
    pp = ((up > 0).sum() + (dn > 0).sum()) / (len(up) + len(dn))
    z = (p1 - p2) / np.sqrt(pp * (1 - pp) * (1 / len(up) + 1 / len(dn)))
    return {
        "n": len(x),
        "pearson": x.corr(y),
        "spearman": x.corr(y, method="spearman"),
        "beta": beta, "t_beta_hc": tb,
        "P(Y>0)": (y > 0).mean() * 100,
        "P(Y>0|X>0)": p1 * 100, "P(Y>0|X<0)": p2 * 100, "z_prop": z,
        "Y_bp|X>0": up.mean() * 1e4, "Y_bp|X<0": dn.mean() * 1e4,
        "diff_bp": (up.mean() - dn.mean()) * 1e4, "t_diff": tw.statistic,
        "n_up": len(up), "n_dn": len(dn),
    }


def follow(b: pd.DataFrame, xs: tuple, ys: tuple) -> dict:
    """Position sur Y = signe de X ; backtest vectorbt aux bornes de Y, net du coût standard."""
    x = ret(b, *xs)
    s = b[(x != 0) & x.notna() & b[[f"p_{ys[0]}", f"p_{ys[1]}"]].notna().all(axis=1)]
    side = np.sign(x.loc[s.index])
    ev = pd.concat([
        pd.DataFrame({"ts": s[f"t_{ys[0]}"].values, "price": s[f"p_{ys[0]}"].values,
                      "size": side.values, "day": s.index}),
        pd.DataFrame({"ts": s[f"t_{ys[1]}"].values, "price": s[f"p_{ys[1]}"].values,
                      "size": 0.0, "day": s.index}),
    ]).sort_values(["ts", "size"]).set_index("ts")
    assert ev.index.is_unique
    pf = vbt.Portfolio.from_orders(
        close=ev["price"], size=ev["size"], size_type="targetpercent", direction="both",
        fees=0.0, init_cash=1_000_000.0, freq="1min",
    )
    tr = pf.trades.records_readable
    assert len(tr) == len(s) and (tr["Status"] == "Closed").all()
    gross = pd.Series(tr["Return"].values, index=ev.loc[tr["Entry Timestamp"], "day"].values).sort_index()
    # coût en points rapporté au prix réel du contrat (prix ajusté / facteur)
    raw_px = (s[f"p_{ys[0]}"] / s[f"f_{ys[0]}"]).reindex(gross.index)
    net = gross - COST_PTS / raw_px
    long_net = ret(s, *ys) - COST_PTS / raw_px
    # contrôle indépendant de vectorbt
    assert np.allclose(gross.values, (side * ret(s, *ys)).reindex(gross.index).values, atol=1e-9)

    def sh(r):
        return r.mean() / r.std() * np.sqrt(252)

    return {
        "n": len(net), "gross_bp": gross.mean() * 1e4, "net_bp": net.mean() * 1e4,
        "t_net": net.mean() / net.std() * np.sqrt(len(net)),
        "sharpe_net": sh(net), "long_net_bp": long_net.mean() * 1e4, "sharpe_long_net": sh(long_net),
        "net_2016_26_bp": net[net.index >= "2016"].mean() * 1e4,
        "net_2023_26_bp": net[net.index >= "2023"].mean() * 1e4,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    b = bounds()
    log(f"NQ, {len(b)} séances NYSE pleines, {b.index[0].date()} → {b.index[-1].date()}")
    summer = (b["t_hk_close"] != b["t_eu_open"]).mean() * 100
    log(f"Clôture HK ≠ ouverture Europe : {summer:.0f} % des jours (heure d'été britannique)")
    eu_ny = b["t_eu_close"].dt.tz_convert(NY).dt.strftime("%H:%M").value_counts()
    log(f"Clôture Europe 16:30 Londres en heure NY : {eu_ny.to_dict()}")

    # contrôle de décomposition : Asie·Europe·US = close-to-close
    c2c = ret(b, "prev", "us_close")
    comp = (1 + ret(b, "prev", "eu_open")) * (1 + ret(b, "eu_open", "us_open")) * (1 + ret(b, "us_open", "us_close")) - 1
    ok = c2c.notna() & comp.notna()
    assert np.allclose(c2c[ok], comp[ok], atol=1e-10)

    sess = pd.DataFrame({
        "asia_A": ret(b, "prev", "eu_open"), "asia_B": ret(b, "prev", "hk_close"),
        "eu_A": ret(b, "eu_open", "us_open"), "eu_rest_B": ret(b, "hk_close", "us_open"),
        "eu_B": ret(b, "eu_open", "eu_close"), "us": ret(b, "us_open", "us_close"),
        "us_overlap": ret(b, "us_open", "eu_close"), "us_rest_B": ret(b, "eu_close", "us_close"),
    })
    sess.mul(1e4).round(3).to_csv(OUT / "sessions.csv")
    log("\nSessions (bp) : moyenne, écart-type, % positifs")
    for c in sess:
        r = sess[c].dropna()
        log(f"  {c:11s} n {len(r):5d}  moy {r.mean()*1e4:+6.2f}  σ {r.std()*1e4:6.1f}  pos {(r>0).mean()*100:4.1f} %")

    rows, per, quint, fol = [], [], [], []
    for lab, var, xs, ys in PAIRS:
        x, y = ret(b, *xs), ret(b, *ys)
        d = describe(x, y)
        rows.append({"paire": lab, "variante": var, **d})
        for pn, a, z in PERIODS:
            m = (x.index >= a) & (x.index <= f"{z}-12-31")
            per.append({"paire": lab, "période": pn, **describe(x[m], y[m])})
        ok = x.notna() & y.notna()
        q = pd.qcut(x[ok], 5, labels=[f"Q{i}" for i in range(1, 6)])
        g = y[ok].groupby(q, observed=True)
        quint.append({"paire": lab, **{k: v * 1e4 for k, v in g.mean().items()},
                      **{f"{k}_pos%": v * 100 for k, v in g.apply(lambda s: (s > 0).mean()).items()}})
        fol.append({"paire": lab, **follow(b, xs, ys)})

    pairs = pd.DataFrame(rows)
    by_p = pd.DataFrame(per)
    qt = pd.DataFrame(quint)
    fo = pd.DataFrame(fol)
    for df_, f in [(pairs, "pairs"), (by_p, "by_period"), (qt, "quintiles"), (fo, "follow")]:
        df_.round(4).to_csv(OUT / f"{f}.csv", index=False)

    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    log("\n=== Paires (toute la période) ===")
    log(pairs.drop(columns=["n_up", "n_dn"]).round(3).to_string(index=False))
    log("\n=== Par sous-période : Pearson, P(Y>0|X>0) - P(Y>0|X<0), écart de moyenne ===")
    v = by_p.assign(dP=by_p["P(Y>0|X>0)"] - by_p["P(Y>0|X<0)"])
    log(v.pivot(index="paire", columns="période", values="pearson").round(3).to_string())
    log(v.pivot(index="paire", columns="période", values="dP").round(1).to_string())
    log(v.pivot(index="paire", columns="période", values="diff_bp").round(1).to_string())
    log(v.pivot(index="paire", columns="période", values="t_beta_hc").round(2).to_string())
    log("\n=== Moyenne de Y (bp) par quintile de X ===")
    log(qt.round(1).to_string(index=False))
    log("\n=== Suivre le signe de X sur Y (vectorbt, net 1 tick + 5 $) ===")
    log(fo.round(2).to_string(index=False))

    # la variante B de l'Europe (08:00 → 16:30 Ldn) contient le début de l'US (09:30 → 11:30 NY) :
    # quelle partie prédit le reste de l'US ?
    log("\n=== Décomposition : reste US (16:30 Ldn → 16:00 NY) sur Europe pré-US et début US ===")
    d = sess[["eu_A", "us_overlap", "us_rest_B", "asia_A"]].dropna()
    for cols in [["eu_A"], ["us_overlap"], ["eu_A", "us_overlap"], ["asia_A", "eu_A", "us_overlap"]]:
        X = np.column_stack([np.ones(len(d))] + [d[c].values for c in cols])
        y = d["us_rest_B"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        u = y - X @ beta
        n, k = X.shape
        XtXi = np.linalg.inv(X.T @ X)
        V = n / (n - k) * XtXi @ (X.T * u ** 2) @ X @ XtXi
        t = beta / np.sqrt(np.diag(V))
        log("  " + " ; ".join(f"{c} β {beta[i+1]:+.3f} t {t[i+1]:+.2f}" for i, c in enumerate(cols)))
    for pn, a, z in PERIODS:
        m = (d.index >= a) & (d.index <= f"{z}-12-31")
        log(f"  {pn} : r(eu_A, reste US) {d['eu_A'][m].corr(d['us_rest_B'][m]):+.3f} ; "
            f"r(début US, reste US) {d['us_overlap'][m].corr(d['us_rest_B'][m]):+.3f}")
    (OUT / "run.log").write_text("\n".join(LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
