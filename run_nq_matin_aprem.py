"""Pouvoir prédictif de la matinée US sur l'après-midi US, NQ 1 minute Databento 2010-2026.

uv run python run_nq_matin_aprem.py   → results/nq_matin_aprem/ (run.log, grid.csv,
by_period.csv, by_year.csv, magnitude.csv, regime.csv, follow.csv)

Exploratoire, non pré-enregistré, demandé en séance, suite de [[reports/nq_sessions_corr_report]]
(Europe jusqu'à 16:30 Ldn → reste US : r +0,066, porté par 9:30 → 11:30 NY). Descriptif : le
momentum intraday sur indices est au registre des échecs (Gao, Baltussen) ; rien ici ne rouvre
une stratégie.

X = 9:30 → h (h = 10:00, 10:30, 11:00, 11:30, 12:00, 13:00 NY) ; Y = h → 16:00 (reste de la
séance) et 15:30 → 16:00 (dernière demi-heure, cible de Gao). Mesures de run_nq_sessions_corr :
Pearson, pente à t robuste, P(Y > 0) selon le signe de X, quintiles, sous-périodes, années.
Puis, pour X = 9:30 → 11:30 : taille du mouvement en unités de son écart-type des 20 séances
précédentes, régime de volatilité (terciles de la volatilité réalisée journalière des 20 séances
précédentes), et contrôle tradable vectorbt (signe de X sur Y, net 1 tick + 5 $), avec ou sans
seuil |X| > 1 σ.
"""

from __future__ import annotations

from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd

import recolte1.engine as E
import run_nq_sessions_corr as S

E.USE_2010 = True

OUT = Path("results/nq_matin_aprem")
NY = "America/New_York"
HOURS = ["10:00", "10:30", "11:00", "11:30", "12:00", "13:00"]
MAIN = "11:30"


def bounds() -> pd.DataFrame:
    df = E.load("NQ")
    sched = xc.get_calendar("XNYS").schedule.loc[str(df.index[0].date()):S.END]
    d = pd.DatetimeIndex(sched.index)
    b = pd.DataFrame(index=d)
    b["t_prev"] = sched["close"].shift(1)
    b["t_open"] = sched["open"]
    for h in HOURS + ["15:30"]:
        b[f"t_{h}"] = E.at(d, h, NY)
    b["t_close"] = sched["close"]
    b = b.iloc[1:]
    b = b[b["t_close"].dt.tz_convert(NY).dt.hour == 16]  # demi-séances exclues
    for k in ["prev", "open", *HOURS, "15:30", "close"]:
        b[f"p_{k}"], b[f"f_{k}"] = E.price_at("NQ", b[f"t_{k}"])
    return b


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log = S.log
    b = bounds()
    log(f"NQ, {len(b)} séances NYSE pleines, {b.index[0].date()} → {b.index[-1].date()}")

    # 1. grille : fin de matinée × cible
    grid, per = [], []
    for h in HOURS:
        x = S.ret(b, "open", h)
        for tgt, ys in [("reste", (h, "close")), ("dernière 1/2 h", ("15:30", "close"))]:
            y = S.ret(b, *ys)
            grid.append({"matin": f"9:30→{h}", "cible": tgt, **S.describe(x, y)})
            for pn, a, z in S.PERIODS:
                m = (x.index >= a) & (x.index <= f"{z}-12-31")
                per.append({"matin": f"9:30→{h}", "cible": tgt, "période": pn, **S.describe(x[m], y[m])})
    grid, per = pd.DataFrame(grid), pd.DataFrame(per)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    log("\n=== Grille (toute la période) ===")
    log(grid.drop(columns=["n_up", "n_dn", "spearman", "z_prop"]).round(3).to_string(index=False))
    log("\n=== Pearson par sous-période ===")
    log(per.pivot_table(index=["cible", "matin"], columns="période", values="pearson").round(3).to_string())
    log("\n=== t de la pente (HC) par sous-période ===")
    log(per.pivot_table(index=["cible", "matin"], columns="période", values="t_beta_hc").round(2).to_string())

    # 2. fenêtre principale 9:30 → 11:30 → 16:00
    x, y = S.ret(b, "open", MAIN), S.ret(b, MAIN, "close")
    d = pd.DataFrame({"x": x, "y": y}).dropna()
    yr = pd.DataFrame([{"année": a, **S.describe(g["x"], g["y"])} for a, g in d.groupby(d.index.year)])
    log(f"\n=== 9:30→{MAIN} → reste, par année ===")
    log(yr[["année", "n", "pearson", "t_beta_hc", "P(Y>0|X>0)", "P(Y>0|X<0)", "diff_bp"]].round(2).to_string(index=False))

    sig = d["x"].rolling(20).std().shift(1)  # écart-type de la matinée sur les 20 séances précédentes
    d["z"] = d["x"] / sig
    c2c = (b["p_close"] / b["p_close"].shift(1) - 1).reindex(d.index)
    d["vol20"] = c2c.rolling(20).std().shift(1)
    d = d.dropna()
    bins = [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf]
    d["zb"] = pd.cut(d["z"], bins)
    mag = d.groupby("zb", observed=True)["y"].agg(
        n="size", moy_bp=lambda s: s.mean() * 1e4, pos=lambda s: (s > 0).mean() * 100,
        t=lambda s: s.mean() / s.std() * np.sqrt(len(s)))
    log("\n=== Reste de séance selon la taille de la matinée (z = X / σ20) ===")
    log(mag.round(2).to_string())
    d["reg"] = pd.qcut(d["vol20"], 3, labels=["vol basse", "vol moyenne", "vol haute"])
    reg = pd.DataFrame([{"régime": r, **S.describe(g["x"], g["y"])} for r, g in d.groupby("reg", observed=True)])
    log("\n=== Par régime de volatilité (terciles de la vol. réalisée 20 j, toute la période) ===")
    log(reg[["régime", "n", "pearson", "t_beta_hc", "P(Y>0|X>0)", "P(Y>0|X<0)", "diff_bp"]].round(3).to_string(index=False))

    # 3. contrôle tradable (vectorbt), toutes les fins de matinée, avec et sans seuil 1 σ
    fol = []
    for h in HOURS:
        fol.append({"matin": f"9:30→{h}", "filtre": "aucun", **S.follow(b, ("open", h), (h, "close"))})
    zb = S.ret(b, "open", MAIN) / S.ret(b, "open", MAIN).rolling(20).std().shift(1)
    bb = b[zb.abs() > 1]
    fol.append({"matin": f"9:30→{MAIN}", "filtre": "|z| > 1", **S.follow(bb, ("open", MAIN), (MAIN, "close"))})
    fo = pd.DataFrame(fol)
    log("\n=== Suivre le signe de la matinée jusqu'à 16:00 (vectorbt, net 1 tick + 5 $) ===")
    log(fo.round(2).to_string(index=False))

    for df_, f in [(grid, "grid"), (per, "by_period"), (yr, "by_year"), (reg, "regime"), (fo, "follow")]:
        df_.round(4).to_csv(OUT / f"{f}.csv", index=False)
    mag.round(4).to_csv(OUT / "magnitude.csv")
    (OUT / "run.log").write_text("\n".join(S.LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
