"""Exploratoire : toutes les métriques de FTMO 1-Step 100k et FundingPips 1 Step Flex 100k (règle NQ de nuit).

uv run python run_propfirm_metrics.py  → results/propfirm_multi/metrics.log, metrics_chain.csv

Mêmes règles, nuits et moteur que run_propfirm_multi.py (propfirm.generic). Deux réglages par prop firm : celui
choisi sur 2011-2018 par run_propfirm_multi, et celui du plan FTMO (éval 0,2 × perte max à 2,5 R, financé 0,1 à 2 R,
sans ramener l'objectif). Sections :
1. Trade : risque en $, part des nuits où l'objectif est touché avant le stop, R moyen.
2. Éval : passage, nuits et jours jusqu'à la validation, causes d'échec, coût moyen d'un financé (prix / passage).
3. Financé (2 ans) : retraits, montants, délai du premier, durée de vie, fin.
4. EV par éval : toute la période, 2011-2018, 2019-2025, sans edge.
5. Un compte racheté à chaque échec pendant 3 ans (départs toutes les 5 nuits) : gain net, argent sorti avant
   remboursement, évals achetées, pire série d'évals ratées, plus longue période sans retrait.
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

import run_propfirm_multi as M
from propfirm.generic import CFD_COST, run_eval, run_funded
from propfirm.nights import K_STEP, NEVER

sys.stdout.reconfigure(encoding="utf-8")
LOG = open(M.OUT / "metrics.log", "w", encoding="utf-8")
L = M.L
CAL = (L.dates - L.dates[0]).days.to_numpy()
SETS = {"FTMO 1-Step 100k": {"choisi (2011-2018)": (0.1, 2.0, 0.1, 1.0, True), "plan FTMO": (0.2, 2.5, 0.1, 2.0, False)},
        "FundingPips 1 Step Flex 100k (+Swing)": {"choisi (2011-2018)": (0.1, 1.5, 0.1, 2.0, True),
                                                  "plan FTMO": (0.2, 2.5, 0.1, 2.0, False)}}
H3 = 756


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def q(x, ps=(0.5, 0.75, 0.9)):
    x = np.asarray(x, float)
    return " / ".join(f"{np.quantile(x, p):_.0f}" for p in ps).replace("_", " ") if len(x) else "—"


def chain(f, ke, rre, kf, rrf, cap, s0):
    """Un compte racheté à chaque échec depuis la nuit s0, pendant H3 nuits."""
    end = s0 + H3
    i, cash, low, nev, run, worst, pays, gaps = s0, 0.0, 0.0, 0, 0, 0, [], []
    last_pay = CAL[s0]
    while i < end:
        cash -= f.fee; low = min(low, cash); nev += 1
        r = run_eval(f, L, np.array([i]), ke, rre, cap_tp=cap, max_steps=end - i)
        j = int(r["fin"][0])
        if not r["ok"][0]:
            run += 1; worst = max(worst, run); i = j + 1
            continue
        run = 0
        st = j + f.review
        if st >= end:
            break
        g = run_funded(f, L, np.array([st]), kf, rrf, max_steps=end - st)
        # dates des retraits : on ne les a pas une par une ; on prend le total versé à la fin de vie du financé
        paid = g["paid"][0]
        vie = int(g["vie"][0])
        if g["npay"][0] > 0:
            t1 = st + int(g["premier"][0]) - 1
            gaps.append(CAL[min(t1, L.n - 1)] - last_pay)
            last_pay = CAL[min(st + vie - 1, L.n - 1)]
        cash += paid; pays.append(int(g["npay"][0]))
        i = st + vie + 1
    gaps.append(CAL[min(end, L.n - 1)] - last_pay)
    return dict(start=L.dates[s0].date(), net=cash, mise=-low, evals=nev, pire_serie=worst, retraits=sum(pays),
                max_sans_retrait_j=max(gaps))


def main() -> None:
    say(f"Métriques FTMO et FundingPips, règle NQ de nuit ; départs d'éval {M.NE}, de financé {M.NF} (2 ans) ; "
        f"IS < {M.SPLIT_DATE.date()} ≤ OOS")
    firms = {f.name: f for f in M.FIRMS}
    rows = []
    for name, sets in SETS.items():
        f = firms[name]
        for lab, (ke, rre, kf, rrf, cap) in sets.items():
            say(f"\n=== {name} — {lab} : éval risque {ke:g} × {f.dd:_.0f} $ = {ke * f.dd:_.0f} $ à {rre:g} R"
                f"{' (objectif ramené au reste à faire)' if cap else ''} ; financé {kf * f.dd:_.0f} $ à {rrf:g} R ===".replace("_", " "))
            # 1. trade
            side = np.where(L.dir > 0, 0, 1); i = np.arange(L.n)
            for ph, rr in (("éval", rre), ("financé", rrf)):
                k = int(np.ceil(rr / K_STEP - 1e-9)) - 1
                win = L.tp_bar[0, i, side, k] < L.stop_bar[0, i, side]
                lost = ~win & (L.stop_bar[0, i, side] != NEVER)
                R = np.where(win, K_STEP * (k + 1), np.where(lost, -L.stop_R[0, i, side], L.eod_R[0, i, side]))
                c = CFD_COST / L.s
                say(f"  trade {ph} ({rr:g} R) : objectif {win.mean():.1%}, stop {lost.mean():.1%}, sortie 9:30 "
                    f"{1 - win.mean() - lost.mean():.1%} ; R net moyen {np.mean((R - c) / (1 + c)):+.3f} ; "
                    f"pire série de stops {max(len(x) for x in ''.join('1' if v else '0' for v in lost).split('0'))}")
            # 2. éval
            re = run_eval(f, L, M.SE, ke, rre, cap_tp=cap)
            ok = re["ok"]
            ce = pd.Series(re["cause"][~ok]).map({1: "plancher", 2: "perte du jour", 3: "marge épuisée", 4: "délai", 5: "fin des données"})
            say(f"  éval : passage {ok.mean():.1%} (2011-2018 {ok[M.ISE].mean():.1%}, 2019-2025 {ok[~M.ISE].mean():.1%}) ; "
                f"nuits pour valider médiane / 75e / 90e : {q(re['nuits'][ok])} ; jours calendaires {q(re['jours'][ok])} ; "
                f"nuits d'une éval ratée {q(re['nuits'][~ok])}")
            say("    échecs : " + ", ".join(f"{a} {b:.0%}" for a, b in ce.value_counts(normalize=True).items())
                + f" ; évals achetées par financé en moyenne {1 / ok.mean():.2f} → {f.fee / ok.mean():_.0f} $".replace("_", " "))
            # 3. financé
            rf = run_funded(f, L, M.SF, kf, rrf, max_steps=M.H_F)
            pd_, npay = rf["paid"], rf["npay"]
            cf = pd.Series(rf["cause"]).map({0: "encore en vie à 2 ans", 1: "plancher", 2: "perte du jour", 3: "marge épuisée", 5: "fin des données", 6: "retraits max"})
            pos = npay > 0
            say(f"  financé (2 ans) : P(≥ 1 retrait) {pos.mean():.0%} ; retraits {npay.mean():.2f} en moyenne (médiane {np.median(npay):.0f}, "
                f"90e {np.quantile(npay, 0.9):.0f}) ; versé {pd_.mean():_.0f} $ en moyenne, médiane / 75e / 90e {q(pd_)} $, "
                f"10e centile {np.quantile(pd_, 0.1):_.0f} $ ; P(versé > prix de l'éval) {(pd_ > f.fee).mean():.0%}".replace("_", " "))
            say(f"    montant moyen d'un retrait {pd_[pos].sum() / npay[pos].sum():_.0f} $ ; 1er retrait après {q(rf['premier'][pos])} nuits ; "
                f"vie {q(rf['vie'])} nuits ; versé 2011-2018 {pd_[M.ISF].mean():_.0f} $, 2019-2025 {pd_[~M.ISF].mean():_.0f} $".replace("_", " "))
            say("    fin : " + ", ".join(f"{a} {b:.0%}" for a, b in cf.value_counts(normalize=True).items()))
            # 4. EV
            ea, pa, va = M.ev(f, re, rf); ei, _, _ = M.ev(f, re, rf, M.ISE, M.ISF); eo, _, _ = M.ev(f, re, rf, ~M.ISE, ~M.ISF)
            rng = np.random.default_rng(31)
            ne, _, _ = M.ev(f, run_eval(f, L, M.SE, ke, rre, cap_tp=cap, rng=rng), run_funded(f, L, M.SF, kf, rrf, rng=rng, max_steps=M.H_F))
            say(f"  EV par éval : toute la période {ea:+_.0f} $ (×{ea / f.fee:.1f} le prix), 2011-2018 {ei:+_.0f} $, "
                f"2019-2025 {eo:+_.0f} $ (×{eo / f.fee:.1f}), sans edge {ne:+_.0f} $ ; refus de retraits tolérés {1 - f.fee / (pa * va):.0%}".replace("_", " "))
            # 5. chaîne
            C = pd.DataFrame([chain(f, ke, rre, kf, rrf, cap, s0) for s0 in range(0, L.n - H3, 5)])
            C.insert(0, "réglage", lab); C.insert(0, "firm", name)
            rows.append(C)
            say(f"  un compte racheté à chaque échec, 3 ans ({len(C)} départs) : gain net médiane {C.net.median():+_.0f} $, "
                f"5e centile {C.net.quantile(0.05):+_.0f} $, pire {C.net.min():+_.0f} $, meilleur {C.net.max():+_.0f} $ ; "
                f"argent sorti avant remboursement médiane {C.mise.median():_.0f} $, 95e {C.mise.quantile(0.95):_.0f} $, "
                f"pire {C.mise.max():_.0f} $".replace("_", " "))
            say(f"    évals achetées {C.evals.median():.0f} médiane (max {C.evals.max()}), pire série d'évals ratées {C.pire_serie.max()} ; "
                f"retraits en 3 ans {C.retraits.median():.0f} médiane ; plus longue période sans retrait médiane "
                f"{C.max_sans_retrait_j.median():.0f} jours, pire {C.max_sans_retrait_j.max():.0f} jours")
    pd.concat(rows).to_csv(M.OUT / "metrics_chain.csv", index=False)


if __name__ == "__main__":
    main()
