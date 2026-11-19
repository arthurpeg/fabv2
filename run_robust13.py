"""Robustesse descriptive de la règle NQ de nuit (n° 10-12), 2011-07 → 2026-08 : régimes et pertes extrêmes.

uv run python run_robust13.py   → results/robust13/ (nights.csv, regimes.csv, years.csv, worst.csv, tails.csv, run.log)

Aucun paramètre n'est cherché : on découpe des résultats existants par des variables connues
avant l'entrée (volatilité réalisée, tendance), pour savoir quand la prime de nuit disparaît.
Séries : R0 = la règle (20:00, SL 2 / TP 5 ATR, momentum) ; R1 = 20:00 → 9:30 sans stop, momentum ;
R2 = 20:00 → 9:30 sans stop, toujours long. Définitions identiques à run_prereg12.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_prereg12 as Q  # active l'historique 2010-2015
import run_prereg10 as P
from recolte1.engine import NY, ci_mean
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/robust13")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def main():
    t20, t930 = at(Q.D, "20:00", NY, -1), Q.B["t_open"]
    long1 = pd.Series(1.0, index=Q.D)
    S, R0_trades = {}, None
    for key, dr, var in [("R0", Q.MOM, Q.STOP), ("R1", Q.MOM, Q.NOSTOP), ("R2", long1, Q.NOSTOP)]:
        e = Q.table(t20, t930, dr, key)
        T = Q.sim(e, var)
        S[key] = Q.per_night(T)
        if key == "R0":
            t = T[T["cost"] == "net"].copy()
            t["R"] = P.r_multiples("NQ", e, t).values
            R0_trades = t
    N = pd.DataFrame(S)

    # variables connues avant l'entrée de la nuit d (fin de la séance d-1)
    cc = Q.BB["cc"]
    close = Q.BB["p_close"]
    vol20 = (cc.rolling(20, min_periods=15).std() * np.sqrt(252)).shift(1)
    vt = vol20.expanding(min_periods=250).quantile(1 / 3).shift(1), vol20.expanding(min_periods=250).quantile(2 / 3).shift(1)
    N["vol20_%"] = (vol20 * 100).reindex(N.index)
    N["vol"] = np.select([vol20 <= vt[0], vol20 <= vt[1]], ["basse", "moyenne"], "haute")[Q.D.get_indexer(N.index)]
    N.loc[vol20.reindex(N.index).isna() | vt[0].reindex(N.index).isna(), "vol"] = np.nan
    ma200 = close.rolling(200, min_periods=200).mean()
    N["tendance"] = np.where((close > ma200).shift(1).reindex(N.index), "NQ > MM200", "NQ < MM200")
    N["momentum"] = np.where(Q.MOM.reindex(N.index) > 0, "momentum +", "momentum −")
    N["jour"] = N.index.day_name()
    N["annee"] = N.index.year
    N.to_csv(OUT / "nights.csv")

    rows = []
    for var in ["vol", "tendance", "momentum", "jour"]:
        for lev, g in N.dropna(subset=[var]).groupby(var):
            for k in ["R0", "R1", "R2"]:
                m, lo, hi = ci_mean(g[k].values * 1e4)
                rows.append({"variable": var, "niveau": lev, "série": k, "nuits": len(g),
                             "bp_par_nuit": m, "lo": lo, "hi": hi,
                             "sharpe": g[k].mean() / g[k].std() * np.sqrt(252) if g[k].std() > 0 else np.nan})
    Rg = pd.DataFrame(rows)
    Rg.to_csv(OUT / "regimes.csv", index=False)
    Y = N.groupby("annee")[["R0", "R1", "R2"]].agg(lambda x: x.mean() * 1e4)
    Y["NQ_cc_%"] = cc.reindex(N.index).groupby(N["annee"]).apply(lambda x: (np.prod(1 + x) - 1) * 100)
    Y.to_csv(OUT / "years.csv")

    # pertes extrêmes
    tails = []
    for k in ["R0", "R1", "R2"]:
        x = N[k][N[k] != 0]
        tails.append({"série": k, "nuits_tradées": len(x), "pire_%": x.min() * 100, "q01_%": x.quantile(0.01) * 100,
                      "q05_%": x.quantile(0.05) * 100, "nuits_<-1%": int((x < -0.01).sum()),
                      "nuits_<-2%": int((x < -0.02).sum()), "nuits_<-3%": int((x < -0.03).sum()),
                      "part_perte_10_pires_%": float(x.nsmallest(10).sum() / x[x < 0].sum() * 100),
                      "skew": float(x.skew()), "kurtosis": float(x.kurt())})
    TL = pd.DataFrame(tails)
    TL.to_csv(OUT / "tails.csv", index=False)
    W = N.nsmallest(12, "R2")[["R0", "R1", "R2", "vol20_%", "tendance", "momentum", "jour"]].copy()
    W[["R0", "R1", "R2"]] *= 100
    W.to_csv(OUT / "worst.csv")
    # glissement au-delà du stop : trades sortis SL à moins de -1 R
    sl = R0_trades[R0_trades["reason"] == "SL"]
    gap = {"trades_SL": len(sl), "R_moyen_SL": sl["R"].mean(), "SL_pire_R": sl["R"].min(),
           "SL_au-delà_de_-1.5R": int((sl["R"] < -1.5).sum()), "SL_au-delà_de_-2R": int((sl["R"] < -2).sum())}
    worstR = R0_trades.nsmallest(8, "R")[["night", "R", "ret", "reason"]]

    pd.set_option("display.width", 250)
    log(Rg.pivot_table(index=["variable", "niveau"], columns="série", values="bp_par_nuit").round(2).to_string())
    log(Rg[Rg["série"] == "R0"][["variable", "niveau", "nuits", "bp_par_nuit", "lo", "hi", "sharpe"]].round(2).to_string(index=False))
    log(Y.round(2).to_string())
    log(TL.round(2).to_string(index=False))
    log(W.round(2).to_string())
    log(gap)
    log(worstR.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
