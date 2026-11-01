"""Exploratoire : la règle NQ de nuit chez 10 prop firms, avec une grille de gestion du risque et de ratios gain / risque.

uv run python run_propfirm_multi.py  → results/propfirm_multi/ (run.log, eval_grid.csv, funded_grid.csv, summary.csv)

Règles relevées sur les sites le 2026-10-31 (détail et sources : reports/propfirm_multi.md). Moteur : propfirm.generic
(éval en une étape + financé, une position par nuit), nuits : propfirm.nights.
Gestion du risque : risque par trade = k × perte max du compte (borné par la marge restante et la perte du jour),
objectif rr R (stop 2 ATR M15), en éval ramené au reste à faire. Grille : éval k ∈ {0,1 ; 0,2 ; 0,33 ; 0,5 ; 1},
rr ∈ {0,75 ; 1 ; 1,5 ; 2 ; 2,5 ; 3} ; financé k ∈ {0,1 ; 0,2 ; 0,33 ; 0,5}, rr ∈ {1 ; 1,5 ; 2 ; 2,5 ; 3}.
Éval et financé sont simulés séparément depuis chaque nuit de départ (financé : retraits reçus sur 2 ans, 504 nuits) ; EV par éval = P(passage) × (valeur du
financé − activation) − coût moyen de l'éval. Choix du réglage sur les départs 2011-07 → 2018-12, évaluation hors
échantillon sur 2019-01 → 2025-08 (la règle de nuit elle-même a été choisie sur 2016-2026 : tout reste optimiste).
Contrôles : réglage du plan FTMO (éval 0,2 / 2,5 R, financé 0,1 / 2 R, sans ramener l'objectif) chez FTMO et STF,
à comparer à run_propfirm_rr2 (+10 408 $ / 100k) et run_propfirm_stf (+4 512 $) ; sens au hasard (sans edge).
"""

from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.generic import Firm, run_eval, run_funded
from propfirm.nights import build

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_multi")
OUT.mkdir(parents=True, exist_ok=True)
LOG = None  # ouvert dans main() : le module peut être importé sans écraser run.log
INF = -1e18
SPLIT_DATE = pd.Timestamp("2019-01-01")
E_K, E_RR = (0.1, 0.2, 0.33, 0.5, 1.0), (0.75, 1.0, 1.5, 2.0, 2.5, 3.0)
F_K, F_RR = (0.1, 0.2, 0.33, 0.5), (1.0, 1.5, 2.0, 2.5, 3.0)
FIVE_LADDER = (20e3, 25e3, 30e3, 40e3, 50e3, 60e3, 70e3, 80e3, 100e3, 125e3, 150e3, 175e3, 200e3, 250e3, 300e3,
               350e3, 400e3, 450e3, 500e3)

FIRMS = [
    Firm("FTMO 1-Step 100k", "cfd", 100e3, 549.0, target=10e3, dd=10e3, dd_type="eod", dll=3e3, consist=0.5,
         review=3, news_f=True, pay_min_days=10, f_consist=0.5, split=(0.9,), after="reset"),
    Firm("Smart Trader Funds 1 Phase 100k", "cfd", 100e3, 599.0, target=9e3, dd=6e3, dd_type="static", dll=4e3,
         consist=0.45, min_days=5, news_e=True, news_f=True, pay_first_days=30, pay_every_days=14, pay_min_days=5,
         f_consist=0.45, pay_min=100, split=(0.8, 0.8, 0.8, 0.9), refund_at=2, after="reset"),
    Firm("FundedNext Stellar 1-Step 100k", "cfd", 100e3, 569.99, target=10e3, dd=6e3, dd_type="static", dll=3e3,
         min_days=2, news_f=True, pay_first_days=7, pay_every_days=7, split=(0.8,), refund_at=3, f_risk_cap=3e3,
         after="reset"),
    Firm("FundingPips 1 Step Flex 100k (+Swing)", "cfd", 100e3, 732.6, target=12e3, dd=12e3, dd_type="static",
         dll=3e3, lev=20, f_lev=5, pay_first_days=14, pay_every_days=14, pay_min=1e3, split=(0.8,), after="reset"),
    Firm("The5ers Pro Growth 20k", "cfd", 20e3, 189.0, target=2e3, dd=1.2e3, dd_type="static", dll=600,
         min_win_days=3, lev=30, milestone=0.10, ladder=FIVE_LADDER, split=(0.75,) * 15 + (0.8,), after="reset"),
    Firm("Topstep 50K (Standard)", "fut", 50e3, 49.0, target=3e3, dd=2e3, dd_type="eod", lock_at=2e3, lock_floor=0.0,
         consist=0.55, min_days=2, max_micros=50, monthly=True, activation=149.0,
         f_dd=2e3, f_dd_type="eod", f_lock_at=2e3, f_lock_floor=0.0,
         f_tiers=[(INF, 20, None), (1500, 30, None), (2000, 50, None)], win_days=5, win_min=150, pay_frac=0.5,
         pay_caps=(2000,), pay_min=125, split=(0.9,), after="keep", lock_after_pay=0.0),
    Firm("Apex 50K EOD (sans activation)", "fut", 50e3, 119.0, target=3e3, dd=2e3, dd_type="eod", dll=1e3,
         dll_soft=True, max_micros=60, max_cal_days=30,
         f_dd=2e3, f_dd_type="eod", f_lock_at=2.1e3, f_lock_floor=100.0, f_dll=1e3, f_dll_soft=True,
         f_tiers=[(INF, 20, 1000), (1500, 30, 1000), (3000, 40, 2000), (6000, 40, 3000)], win_days=5, win_min=250,
         f_consist=0.5, pay_keep=2.1e3, pay_caps=(1500, 1500, 2000, 2500, 2500, 3000), pay_min=500, split=(1.0,),
         after="keep", lock_after_pay=100.0, max_payouts=6),
    Firm("MyFundedFutures Rapid 50K", "fut", 50e3, 125.0, target=3e3, dd=2e3, dd_type="eod", lock_at=2.1e3,
         lock_floor=100.0, consist=0.5, min_days=2, max_micros=50,
         f_dd=2e3, f_dd_type="intraday", f_lock_at=2.1e3, f_lock_floor=100.0, f_max_micros=50, news_f=True,
         pay_keep=2.1e3, pay_min=500, split=(0.9,), after="keep", lock_after_pay=100.0),
    Firm("Tradeify Growth 50K", "fut", 50e3, 145.0, target=3e3, dd=2e3, dd_type="eod", lock_at=2.1e3,
         lock_floor=100.0, dll=1250, dll_soft=True, max_micros=40,
         f_dd=2e3, f_dd_type="eod", f_lock_at=2.1e3, f_lock_floor=100.0, f_dll=1250, f_dll_soft=True,
         f_max_micros=40, win_days=5, win_min=150, f_consist=0.35, pay_balance=3e3, pay_keep=2.1e3,
         pay_caps=(1500, 2000, 2500, 3000), pay_min=500, split=(0.9,), after="keep", lock_after_pay=100.0),
    Firm("LucidFlex 50K (DLL OFF, 50 %)", "fut", 50e3, 130.0, target=3e3, dd=2e3, dd_type="eod", lock_at=2.1e3,
         lock_floor=100.0, consist=0.5, max_micros=40,
         f_dd=2e3, f_dd_type="eod", f_lock_at=2.1e3, f_lock_floor=100.0,
         f_tiers=[(INF, 20, None), (1000, 30, None), (2000, 40, None)], win_days=5, win_min=150, pay_frac=0.5,
         pay_caps=(2000,), pay_min=500, split=(0.9,), after="keep", lock_after_pay=100.0, max_payouts=5),
]


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


L = build()
NE = L.n - 252           # départs d'éval (un an de données au moins pour la finir)
H_F = 504                # financé : retraits sur 2 ans (même horizon pour tous les départs)
NF = L.n - H_F           # départs de financé
SE, SF = np.arange(NE), np.arange(NF)
ISE, ISF = L.dates[SE] < SPLIT_DATE, L.dates[SF] < SPLIT_DATE


def eval_cost(f: Firm, r) -> np.ndarray:
    return f.fee * (1 + r["jours"] // 30) if f.monthly else np.full(len(r["ok"]), f.fee)


def ev(f, re, rf, m_e=slice(None), m_f=slice(None)):
    p = re["ok"][m_e].mean()
    v = rf["paid"][m_f].mean()
    return p * (v - f.activation) - eval_cost(f, re)[m_e].mean(), p, v


def main() -> None:
    global LOG
    LOG = open(OUT / "run.log", "w", encoding="utf-8")
    say(f"10 prop firms, règle NQ de nuit ; {L.n} nuits {L.dates[0].date()} → {L.dates[-1].date()} ; départs d'éval {NE}, "
        f"de financé {NF} ; IS < {SPLIT_DATE.date()} ≤ OOS")
    rows_e, rows_f, summ = [], [], []
    rng = np.random.default_rng(31)
    for f in FIRMS:
        say(f"\n=== {f.name} (éval {f.fee:.0f} $" + (" par mois" if f.monthly else "") +
            (f", activation {f.activation:.0f} $" if f.activation else "") + ") ===")
        # contrôle / réglage de référence : plan FTMO
        re0 = run_eval(f, L, SE, 0.2, 2.5, cap_tp=False)
        rf0 = run_funded(f, L, SF, 0.1, 2.0, max_steps=H_F)
        e0, p0, v0 = ev(f, re0, rf0)
        say(f"  réglage du plan FTMO (éval 0,2 × perte max, 2,5 R ; financé 0,1, 2 R) : passage {p0:.1%}, financé "
            f"{v0:_.0f} $ ({rf0['npay'].mean():.2f} retraits), EV {e0:+_.0f} $".replace("_", " "))
        E, F = {}, {}
        for k, rr in product(E_K, E_RR):
            E[(k, rr)] = run_eval(f, L, SE, k, rr)
            r = E[(k, rr)]
            rows_e.append(dict(firm=f.name, k=k, rr=rr, p=r["ok"].mean(), p_is=r["ok"][ISE].mean(), p_oos=r["ok"][~ISE].mean(),
                               cost=eval_cost(f, r).mean(), nuits=np.median(r["nuits"][r["ok"]]) if r["ok"].any() else np.nan))
        for k, rr in product(F_K, F_RR):
            F[(k, rr)] = run_funded(f, L, SF, k, rr, max_steps=H_F)
            r = F[(k, rr)]
            rows_f.append(dict(firm=f.name, k=k, rr=rr, v=r["paid"].mean(), v_is=r["paid"][ISF].mean(),
                               v_oos=r["paid"][~ISF].mean(), npay=r["npay"].mean(), p_pay=(r["npay"] > 0).mean()))
        # choix sur IS, mesure sur OOS
        fbest = max(F, key=lambda x: F[x]["paid"][ISF].mean())
        vis = F[fbest]["paid"][ISF].mean()
        ebest = max(E, key=lambda x: E[x]["ok"][ISE].mean() * (vis - f.activation) - eval_cost(f, E[x])[ISE].mean())
        e_is, p_is, v_is = ev(f, E[ebest], F[fbest], ISE, ISF)
        e_oos, p_oos, v_oos = ev(f, E[ebest], F[fbest], ~ISE, ~ISF)
        e_all, p_all, v_all = ev(f, E[ebest], F[fbest])
        # sans edge, même réglage
        rr_e = run_eval(f, L, SE, *ebest, rng=rng)
        rr_f = run_funded(f, L, SF, *fbest, rng=rng, max_steps=H_F)
        e_ne, p_ne, v_ne = ev(f, rr_e, rr_f)
        # meilleur réglage choisi sur toute la période (optimiste)
        fb2 = max(F, key=lambda x: F[x]["paid"].mean())
        eb2 = max(E, key=lambda x: E[x]["ok"].mean() * (F[fb2]["paid"].mean() - f.activation) - eval_cost(f, E[x]).mean())
        e_best, _, _ = ev(f, E[eb2], F[fb2])
        r = F[fbest]
        say(f"  choisi sur IS : éval k {ebest[0]:g} rr {ebest[1]:g}, financé k {fbest[0]:g} rr {fbest[1]:g}")
        say(f"    IS : passage {p_is:.1%}, financé {v_is:_.0f} $, EV {e_is:+_.0f} $ | OOS : passage {p_oos:.1%}, financé "
            f"{v_oos:_.0f} $, EV {e_oos:+_.0f} $ | toute la période : EV {e_all:+_.0f} $ ({r['npay'].mean():.2f} retraits, "
            f"P(≥ 1) {(r['npay'] > 0).mean():.0%})".replace("_", " "))
        say(f"    sans edge (sens au hasard) : passage {p_ne:.1%}, financé {v_ne:_.0f} $, EV {e_ne:+_.0f} $ ; meilleur réglage "
            f"choisi sur toute la période : éval {eb2}, financé {fb2}, EV {e_best:+_.0f} $".replace("_", " "))
        ce = pd.Series(E[ebest]["cause"][~E[ebest]["ok"]]).map({1: "plancher", 2: "perte du jour", 3: "marge", 4: "délai", 5: "données"})
        cf = pd.Series(r["cause"]).map({0: "en vie", 1: "plancher", 2: "perte du jour", 3: "marge", 5: "fin des données", 6: "retraits max"})
        say("    échecs d'éval : " + ", ".join(f"{a} {b:.0%}" for a, b in ce.value_counts(normalize=True).items())
            + " ; fin du financé : " + ", ".join(f"{a} {b:.0%}" for a, b in cf.value_counts(normalize=True).items()))
        summ.append(dict(firm=f.name, fee=f.fee, monthly=f.monthly, activation=f.activation, ev_ftmo_plan=e0,
                         eval_k=ebest[0], eval_rr=ebest[1], fund_k=fbest[0], fund_rr=fbest[1], p_is=p_is, ev_is=e_is,
                         p_oos=p_oos, v_oos=v_oos, ev_oos=e_oos, ev_all=e_all, ev_no_edge=e_ne, ev_best_insample=e_best,
                         ratio_oos=e_oos / (f.fee + f.activation)))
    pd.DataFrame(rows_e).to_csv(OUT / "eval_grid.csv", index=False)
    pd.DataFrame(rows_f).to_csv(OUT / "funded_grid.csv", index=False)
    S = pd.DataFrame(summ).sort_values("ev_oos", ascending=False)
    S.to_csv(OUT / "summary.csv", index=False)
    say("\n=== Classement par EV hors échantillon (2019-2025), réglage choisi sur 2011-2018 ===")
    for _, x in S.iterrows():
        say(f"  {x.firm:<40} EV OOS {x.ev_oos:+8_.0f} $ (×{x.ratio_oos:.1f} le prix) ; IS {x.ev_is:+8_.0f} $ ; plan FTMO "
            f"{x.ev_ftmo_plan:+8_.0f} $ ; sans edge {x.ev_no_edge:+7_.0f} $".replace("_", " "))


if __name__ == "__main__":
    main()
