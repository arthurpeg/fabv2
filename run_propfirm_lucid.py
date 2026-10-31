"""Pré-enregistrement n° 18, avenant D : la règle NQ de nuit sur un compte LucidFlex 50K, en MNQ.

uv run python run_propfirm_lucid.py [N]  → results/propfirm_lucid/ (run.log, eval.csv, funded.csv, ev.csv)

Trades : results/couts_reels_nq_nuit/trades.csv (compte 20:00 ET, momentum 12-1, SL 2 ATR / TP 5 ATR,
sortie 9:30 ET). Stop en points = distance du stop × prix brut d'entrée (recolte1.engine.load, 2010
activé ; cache/propfirm/lucid_trades.parquet). Coût par MNQ : demi-spreads réels (bbo-1m, MNQ sinon NQ)
+ 1,50 $ de commission. Moteur : propfirm.lucid.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.lucid import Trades, run_eval, run_funded

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/propfirm_lucid")
OUT.mkdir(parents=True, exist_ok=True)
CACHE = Path("cache/propfirm/lucid_trades.parquet")
LOG = open(OUT / "run.log", "w", encoding="utf-8")
SEED = 1819

COMMISSION, TICK_MNQ = 1.50, 0.50
P_REF = 25_684.0  # médiane du NQ 2025-08-29 → 2026-08-28 (écart au protocole : stop ramené au niveau actuel)
FEES = {"40 %": (0.4, 115.0), "50 %": (0.5, 130.0)}
EVAL_RISK = (200, 400, 600, 800, 1000)
FUNDED_RISK = (200, 400, 600, 800, 1000)
MAIN = dict(lib="règle 2011-2026", cons="40 %", ev=400, fd=200)


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def trades() -> pd.DataFrame:
    if CACHE.exists():
        return pd.read_parquet(CACHE)
    import recolte1.engine as E

    E.USE_2010 = True
    df = E.load("NQ")
    t = pd.read_csv("results/couts_reels_nq_nuit/trades.csv", parse_dates=["night"]).sort_values("entry_idx")
    raw = (df["close"] / df["factor"]).to_numpy()[t.entry_idx.to_numpy()]
    risk = t.risk.fillna(t.risk.median()).to_numpy()  # 2 trades à R = 0 sans ATR
    si = t.spread_in_MNQ.fillna(t.spread_in_NQ).to_numpy()
    so = t.spread_out_MNQ.fillna(t.spread_out_NQ).to_numpy()
    out = pd.DataFrame({"night": t.night.values, "R": t.R_brut.to_numpy(), "price": raw,
                        "stop_pts": risk * raw, "cost": (si + so) / 2 * TICK_MNQ + COMMISSION})
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(CACHE)
    return out


def main() -> None:
    t = trades()
    full = Trades(t.R.to_numpy(), t.stop_pts.to_numpy(), t.cost.to_numpy())
    oos = t[t.night < "2016-01-01"]
    libs = {
        "règle 2011-2026": full,
        "sans edge (R − moyenne)": Trades(full.R - full.R.mean(), full.stop_pts, full.cost),
        "règle 2011-2015 (OOS)": Trades(oos.R.to_numpy(), oos.stop_pts.to_numpy(), oos.cost.to_numpy()),
    }
    # Écart au protocole (constaté sur un passage de 1 000 comptes) : en points historiques, le stop d'un MNQ
    # vaut 42 $ en médiane (14 $ en 2011-2015) et la commission pèse 5 à 14 % du risque ; au niveau actuel
    # du NQ il vaut ~127 $. On rapporte aussi les trades avec le stop ramené au niveau actuel.
    now = t.stop_pts.to_numpy() / t.price.to_numpy() * P_REF
    libs["règle, prix actuels"] = Trades(full.R, now, full.cost)
    libs["sans edge, prix actuels"] = Trades(full.R - full.R.mean(), now, full.cost)
    say(f"Avenant D — règle NQ de nuit sur LucidFlex 50K (MNQ) ; {N} comptes par réglage, graine {SEED}")
    for k, lib in libs.items():
        say(f"  {k} : {lib.n} trades, R brut moyen {lib.R.mean():+.3f}, stop médian {np.median(lib.stop_pts):.1f} pts "
            f"= {np.median(lib.stop_pts) * 2:.0f} $ par MNQ, coût médian {np.median(lib.cost):.2f} $ par MNQ "
            f"({np.median(lib.cost / (lib.stop_pts * 2)):.3f} R), abandon sous {lib.min_room:.0f} $ de marge")

    rng = np.random.default_rng(SEED)
    E, F = [], []
    for k, lib in libs.items():
        say(f"\n=== {k} ===")
        for cname, (cons, fee) in FEES.items():
            if cname != "40 %" and k not in (MAIN["lib"], "règle, prix actuels"):
                continue
            for r in EVAL_RISK:
                ok, d = run_eval(lib, r, N, rng, consistency=cons)
                p = ok.mean()
                E.append(dict(lib=k, cons=cname, fee=fee, risk=r, p_pass=p, se_p=np.sqrt(p * (1 - p) / N),
                              days_pass=d[ok].mean(), days_all=d.mean()))
                say(f"  éval consistance {cname}, {r:>5} $ : passage {p:.1%} ± {1.96 * E[-1]['se_p']:.1%}, "
                    f"{E[-1]['days_pass']:.1f} séances si validé, {d.mean():.1f} par tentative")
        for r in FUNDED_RISK:
            paid, npay, d, first = run_funded(lib, r, N, rng)
            F.append(dict(lib=k, risk=r, value=paid.mean(), se_v=paid.std() / np.sqrt(N), p_payout=(npay > 0).mean(),
                          n_payouts=npay.mean(), five=(npay >= 5).mean(), life=d.mean(),
                          first_med=np.median(first[first > 0]) if (first > 0).any() else np.nan))
            x = F[-1]
            say(f"  financé {r:>5} $ : valeur {x['value']:,.0f} $ ± {1.96 * x['se_v']:,.0f}, P(payout) {x['p_payout']:.0%}, "
                f"{x['n_payouts']:.2f} payouts, 5 payouts (passage en réel) {x['five']:.0%}, vie {x['life']:.0f} séances, "
                f"1er payout méd. {x['first_med']:.0f}".replace(",", " "))
    E, F = pd.DataFrame(E), pd.DataFrame(F)
    E.to_csv(OUT / "eval.csv", index=False)
    F.to_csv(OUT / "funded.csv", index=False)

    rows = []
    for (k, cname), e in E.groupby(["lib", "cons"], sort=False):
        f = F[F.lib == k]
        main = "principal" if (k, cname) == (MAIN["lib"], MAIN["cons"]) else "même réglage"
        picks = {main: (e[e.risk == MAIN["ev"]].iloc[0], f[f.risk == MAIN["fd"]].iloc[0]),
                 "meilleur de la grille": (e.loc[e.p_pass.idxmax()], f.loc[f.value.idxmax()])}
        for which, (ee, ff) in picks.items():
            x = ee.p_pass * ff.value - ee.fee
            ci = 1.96 * np.sqrt((ff.value * ee.se_p) ** 2 + (ee.p_pass * ff.se_v) ** 2)
            rows.append(dict(lib=k, cons=cname, choix=which, eval_risk=ee.risk, funded_risk=ff.risk, fee=ee.fee,
                             p_pass=ee.p_pass, value=ff.value, ev_usd=x, ci95=ci,
                             refus_max=1 - ee.fee / (ee.p_pass * ff.value)))
    V = pd.DataFrame(rows)
    V.to_csv(OUT / "ev.csv", index=False)
    say("\n=== Espérance par éval achetée ===")
    for _, x in V.iterrows():
        say(f"  {x.lib:<26} consistance {x.cons:<5} {x.choix:<22} éval {x.eval_risk:>5} $ financé {x.funded_risk:>5} $ "
            f"(prix {x.fee:.0f} $) : EV {x.ev_usd:+7_.0f} $ ± {x.ci95:_.0f} (passage {x.p_pass:.1%}, "
            f"financé {x.value:_.0f} $, refus max {x.refus_max:.0%})".replace("_", " "))


if __name__ == "__main__":
    main()
