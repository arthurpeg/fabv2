"""Descriptif (non pré-enregistré, hors compteur : heures d'entrée déjà comptées aux n° 10-12) : la règle NQ de
nuit avec entrée à 19:00, 20:00 ou 21:00 ET, tout le reste identique, puis corrélation des trois variantes.

uv run python run_nq_nuit_heures.py  → results/nq_nuit_heures/ (run.log, trades.csv, nights.csv, by_year.csv, corr.csv)

Règle : momentum 12-1 (signe du mois), SL 2 ATR / TP 5 ATR (ATR 14 en M15), sortie 9:30 ET, 2011-07 → 2026-08.
Trades calculés par vectorbt (run_recolte1_atr.simulate = Portfolio.from_signals sur barres 1 min).
Coût « net » = convention du dépôt (1 tick + 5 $ aller-retour). R = rendement / (2 ATR / prix).
Attention : importer run_prereg12 réécrit results/prereg12/run.log (vide de toute façon).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_prereg12 as Q  # historique 2010-2015 actif
import run_prereg10 as P
import run_recolte1_atr as A
from recolte1.engine import NY, ci_mean, ci_sharpe
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/nq_nuit_heures")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
HOURS = ("19:00", "20:00", "21:00")


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def main() -> None:
    A.VARIANTS = [("SL 2 ATR / TP 5 ATR", 2.0, 5.0)]
    trades = []
    for h in HOURS:
        e = Q.table(at(Q.D, h, NY, -1), Q.B["t_open"], Q.MOM, h)
        T = A.simulate("NQ", e)
        for cost in ("gross", "net"):
            t = T[T["cost"] == cost].copy()
            t["R"] = P.r_multiples("NQ", e, t).values
            t["hour"] = h
            trades.append(t)
    T = pd.concat(trades, ignore_index=True)
    T["night"] = pd.to_datetime(T["night"])
    T.to_csv(OUT / "trades.csv", index=False)

    say("Règle NQ de nuit, entrée 19:00 / 20:00 / 21:00 ET, momentum 12-1, SL 2 ATR / TP 5 ATR, sortie 9:30 ET ; vectorbt")
    rows, nightly = [], {}
    for h in HOURS:
        for cost in ("gross", "net"):
            t = T[(T.hour == h) & (T.cost == cost)]
            r = t.groupby("night")["ret"].sum().reindex(Q.NIGHTS).fillna(0.0)
            R = t["R"].to_numpy()
            mR, loR, hiR = ci_mean(R[np.isfinite(R)])
            sh, slo, shi = ci_sharpe(r.values)
            cumR = t.set_index("night")["R"].cumsum()
            ddR = (cumR - cumR.cummax()).min()
            eq = (1 + r).cumprod()
            rows.append(dict(heure=h, coût=cost, trades=len(t), R_par_trade=mR, R_lo=loR, R_hi=hiR,
                             pb_par_nuit=r.mean() * 1e4, ann_pct=r.mean() * 252 * 100, sharpe=sh, sharpe_lo=slo, sharpe_hi=shi,
                             R_par_an=t["R"].sum() / ((Q.NIGHTS[-1] - Q.NIGHTS[0]).days / 365.25),
                             max_dd_R=ddR, max_dd_pct=float((eq / eq.cummax() - 1).min() * 100),
                             gagnants=(t["R"] > 0).mean(), part_TP=(t["reason"] == "TP").mean(),
                             part_SL=(t["reason"] == "SL").mean(), longs=(t["dir"] > 0).mean()))
            if cost == "net":
                nightly[h] = pd.DataFrame({"ret": r, "R": t.groupby("night")["R"].sum().reindex(Q.NIGHTS)})
    S = pd.DataFrame(rows)
    S.to_csv(OUT / "summary.csv", index=False)
    say(f"\n{len(Q.NIGHTS)} nuits ouvrées du {Q.NIGHTS[0].date()} au {Q.NIGHTS[-1].date()}")
    say(f"{'heure':<6} {'coût':<6} {'trades':>6} {'R/trade [IC 95 %]':>24} {'pb/nuit':>8} {'%/an':>6} {'Sharpe [IC 95 %]':>22} "
        f"{'R/an':>6} {'DD R':>7} {'DD %':>7} {'gagn.':>6} {'TP':>5} {'SL':>5} {'longs':>6}")
    for x in S.itertuples():
        say(f"{x.heure:<6} {x.coût:<6} {x.trades:>6} {x.R_par_trade:>+8.3f} [{x.R_lo:+.3f} ; {x.R_hi:+.3f}] {x.pb_par_nuit:>8.2f} "
            f"{x.ann_pct:>6.1f} {x.sharpe:>6.2f} [{x.sharpe_lo:+.2f} ; {x.sharpe_hi:+.2f}] {x.R_par_an:>6.1f} {x.max_dd_R:>7.1f} "
            f"{x.max_dd_pct:>7.1f} {x.gagnants:>6.1%} {x.part_TP:>5.1%} {x.part_SL:>5.1%} {x.longs:>6.1%}")

    # par année (net, R)
    Y = pd.DataFrame({h: nightly[h]["R"].groupby(nightly[h].index.year).sum() for h in HOURS})
    Y.to_csv(OUT / "by_year.csv")
    say("\nR nets par année :")
    say(Y.round(1).to_string())

    # corrélations (net)
    N = pd.concat({h: nightly[h]["ret"] for h in HOURS}, axis=1)
    N.to_csv(OUT / "nights.csv")
    both = pd.concat({h: nightly[h]["R"] for h in HOURS}, axis=1).dropna()
    say(f"\nCorrélations des rendements nets par nuit ({len(N)} nuits, 0 les nuits sans trade) :")
    say("  Pearson :\n" + N.corr().round(3).to_string())
    say("  Spearman :\n" + N.corr(method="spearman").round(3).to_string())
    say(f"\nCorrélation des R par nuit, nuits tradées par les trois ({len(both)} nuits) :")
    say(both.corr().round(3).to_string())
    say("\nCorrélation des R annuels :")
    say(Y.corr().round(3).to_string())
    M = N.groupby(N.index.to_period("M")).sum()
    say("\nCorrélation des rendements mensuels :")
    say(M.corr().round(3).to_string())
    pd.concat({"nuit_pearson": N.corr(), "nuit_spearman": N.corr(method="spearman"), "mois": M.corr(), "année_R": Y.corr()}).to_csv(OUT / "corr.csv")
    same = {f"{a}/{b}": float((np.sign(both[a]) == np.sign(both[b])).mean()) for a, b in (("19:00", "20:00"), ("20:00", "21:00"), ("19:00", "21:00"))}
    say("\nMême signe de R la même nuit : " + ", ".join(f"{k} {v:.1%}" for k, v in same.items()))
    eq = N.mean(axis=1)
    say(f"Panier égal des trois heures (net) : {eq.mean() * 1e4:.2f} pb/nuit, Sharpe {eq.mean() / eq.std() * np.sqrt(252):.2f}, "
        f"max DD {((1 + eq).cumprod() / (1 + eq).cumprod().cummax() - 1).min() * 100:.1f} %")


if __name__ == "__main__":
    main()
