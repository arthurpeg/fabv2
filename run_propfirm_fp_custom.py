"""Exploratoire : gestion du risque sur mesure pour FundingPips 1 Step Flex 100k (option Swing), règle NQ de nuit.

uv run python run_propfirm_fp_custom.py  → results/propfirm_fp_custom/ (run.log, grid.csv)

Critère : un compte racheté à chaque échec pendant 3 ans (756 nuits), départs toutes les 5 nuits ; on choisit sur
les départs 2011-07 → 2018-12 (médiane du gain net), on vérifie sur 2019-01 → 2023-08. Règles : run_propfirm_multi
(objectif +12 %, perte max 12 % fixe, perte du jour 3 %, levier 1:20 en éval et 1:5 en financé (supposé), retraits
remis à zéro). Chaîne vectorisée (tous les départs avancent ensemble) : éval → financé (la nuit suivante) → perte →
nouvelle éval la nuit suivante.
Grille :
- éval : risque 1 / 1,5 / 2 / 2,5 / 3 % du capital, objectif 0,75 … 3 R ramené au reste à faire ;
- financé : risque 0,5 / 0,75 / 1 / 1,25 %, objectif 1 … 3 R ; protection : risque divisé par 2 dès que le profit du
  cycle dépasse 2 % ou 4 % (ou jamais) ;
- retraits : « toutes les 2 semaines » (80 %, min 1 %) ou « à la demande » (100 %, meilleur jour ≤ 35 % du profit du
  cycle, 7 jours à ≥ 0,5 %), deux formules affichées sur fundingpips.com (prix d'une éventuelle option non lu).
Sensibilité : levier 1:20 en financé (si l'hypothèse 1:5 est fausse).
"""

from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.generic import CFD_COST, _trade
from propfirm.nights import build

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_fp_custom")
OUT.mkdir(parents=True, exist_ok=True)
LOG = None
L = build()
CAL = (L.dates - L.dates[0]).days.to_numpy()
SIZE, FEE, TARGET, DD, DLL = 100e3, 732.6, 12e3, 12e3, 3e3
H3, STEP = 756, 5
STARTS = np.arange(0, L.n - H3, STEP)
IS = L.dates[STARTS] < pd.Timestamp("2019-01-01")
E_R, E_RR = (0.01, 0.015, 0.02, 0.025, 0.03), (0.75, 1.0, 1.5, 2.0, 2.5, 3.0)
F_R, F_RR, F_PROT = (0.005, 0.0075, 0.01, 0.0125), (1.0, 1.5, 2.0, 2.5, 3.0), (None, 0.02, 0.04)
MODES = ("2 semaines", "à la demande")


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def chain(re_, rre, rf, rrf, prot, mode, f_lev=5.0):
    n = len(STARTS)
    t = np.zeros(n, int)
    ph = np.zeros(n, int)                      # 0 éval, 1 financé
    P = np.zeros(n); best = np.zeros(n)
    cpnl = np.zeros(n); cwin = np.zeros(n, int); last = CAL[STARTS].astype(float)
    cash = -np.full(n, FEE); low = cash.copy(); evals = np.ones(n, int); npay = np.zeros(n, int)
    paid = np.zeros(n); passes = np.zeros(n, int)
    side_all = np.where(L.dir > 0, 0, 1)
    for step in range(H3):
        i = STARTS + step
        e = ph == 0
        room = P + DD
        risk = np.where(e, np.minimum(re_ * SIZE, room), np.minimum(rf * SIZE, room))
        if prot is not None:
            risk = np.where(~e & (cpnl >= prot * SIZE), risk * 0.5, risk)
        risk = np.minimum(risk, DLL * 0.999)
        lev = np.where(e, 20.0, f_lev) * SIZE
        side = side_all[i]
        need = np.maximum(TARGET - P, 1.0)
        _, _, _, perR, cost = _trade(L, "cfd", i, side, 0, risk, np.full(n, 1.0), None, lev)
        tp = np.where(e, np.minimum(rre, (need + cost) / np.maximum(perR, 1e-9)), rrf)
        pnl, _, _, _, _ = _trade(L, "cfd", i, side, 0, risk, tp, None, lev)
        P += pnl
        dead = (P <= -DD + 1e-6) | (pnl <= -DLL + 1e-6) | (risk < 50)
        # éval validée → financé dès la nuit suivante
        ok = e & ~dead & (P >= TARGET)
        passes += ok
        # financé : retrait
        f = ~e & ~dead
        cpnl = np.where(f, cpnl + pnl, cpnl); best = np.where(f, np.maximum(best, pnl), best)
        cwin = np.where(f & (pnl >= 500), cwin + 1, cwin)
        now = CAL[i]
        if mode == "2 semaines":
            due = f & (now - last >= 14) & (P >= 1000)
            sp = 0.8
        else:
            due = f & (cwin >= 7) & (cpnl > 0) & (best <= 0.35 * cpnl) & (P >= 1000)
            sp = 1.0
        paid += np.where(due, sp * P, 0); cash += np.where(due, sp * P, 0); npay += due
        last = np.where(due, now, last)
        P = np.where(due, 0.0, P); cpnl = np.where(due, 0.0, cpnl); best = np.where(due, 0.0, best)
        cwin = np.where(due, 0, cwin)
        # transitions
        new_eval = dead
        cash -= np.where(new_eval, FEE, 0); evals += new_eval
        low = np.minimum(low, cash)
        start_f = ok
        ph = np.where(new_eval, 0, np.where(start_f, 1, ph))
        P = np.where(new_eval | start_f, 0.0, P)
        best = np.where(new_eval | start_f, 0.0, best); cpnl = np.where(new_eval | start_f, 0.0, cpnl)
        cwin = np.where(new_eval | start_f, 0, cwin)
        last = np.where(start_f, now, last)
    return dict(net=cash, mise=-np.minimum(low, 0), evals=evals, npay=npay, passes=passes)


def stats(r, m):
    x = r["net"][m]
    return dict(med=np.median(x), p5=np.quantile(x, 0.05), pire=x.min(), mise_med=np.median(r["mise"][m]),
                mise_max=r["mise"][m].max(), evals=np.median(r["evals"][m]), retraits=np.median(r["npay"][m]))


def main() -> None:
    global LOG
    LOG = open(OUT / "run.log", "w", encoding="utf-8")
    say(f"FundingPips 1 Step Flex 100k (+Swing), règles sur mesure ; {len(STARTS)} départs de 3 ans "
        f"({IS.sum()} en 2011-2018, {(~IS).sum()} en 2019-2023)")
    base = chain(0.024, 2.5, 0.012, 2.0, None, "2 semaines")
    for lab, m in (("2011-2018", IS), ("2019-2023", ~IS), ("tout", slice(None))):
        s = stats(base, m)
        say(f"  référence plan FTMO (2,4 % à 2,5 R ; 1,2 % à 2 R ; 2 semaines), {lab} : médiane {s['med']:+_.0f} $, "
            f"5e c. {s['p5']:+_.0f} $, pire {s['pire']:+_.0f} $".replace("_", " "))
    rows = []
    for re_, rre, rf, rrf, prot, mode in product(E_R, E_RR, F_R, F_RR, F_PROT, MODES):
        r = chain(re_, rre, rf, rrf, prot, mode)
        a, b = stats(r, IS), stats(r, ~IS)
        rows.append(dict(e_risk=re_, e_rr=rre, f_risk=rf, f_rr=rrf, protection=prot, retraits=mode,
                         **{f"is_{k}": v for k, v in a.items()}, **{f"oos_{k}": v for k, v in b.items()}))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / "grid.csv", index=False)
    say(f"\nGrille : {len(G)} réglages. 10 meilleurs en médiane 2011-2018 :")
    top = G.sort_values("is_med", ascending=False).head(10)
    for _, x in top.iterrows():
        say(f"  éval {x.e_risk:.1%} à {x.e_rr:g} R ; financé {x.f_risk:.2%} à {x.f_rr:g} R, protection "
            f"{'—' if pd.isna(x.protection) else f'{x.protection:.0%}'}, retraits {x.retraits} : IS médiane {x.is_med:+_.0f} $ "
            f"(pire {x.is_pire:+_.0f}) | OOS médiane {x.oos_med:+_.0f} $, 5e c. {x.oos_p5:+_.0f} $, pire {x.oos_pire:+_.0f} $, "
            f"mise max {x.oos_mise_max:_.0f} $".replace("_", " "))
    best = top.iloc[0]
    say("\nEffet de chaque choix (médiane OOS du meilleur réglage quand on ne fait varier que ce paramètre) :")
    keys = ["e_risk", "e_rr", "f_risk", "f_rr", "protection", "retraits"]
    for k in keys:
        m = np.ones(len(G), bool)
        for o in keys:
            if o != k:
                m &= (G[o].isna() & pd.isna(best[o])) | (G[o] == best[o])
        sub = G[m].sort_values(k, key=lambda s: s.astype(str))
        say(f"  {k} : " + " ; ".join(f"{v} → IS {a:+_.0f} / OOS {b:+_.0f}".replace("_", " ")
                                     for v, a, b in zip(sub[k], sub.is_med, sub.oos_med)))
    r20 = chain(best.e_risk, best.e_rr, best.f_risk, best.f_rr, None if pd.isna(best.protection) else best.protection,
                best.retraits, f_lev=20.0)
    s = stats(r20, ~IS)
    say(f"\nSensibilité, même réglage avec levier 1:20 en financé : OOS médiane {s['med']:+_.0f} $, pire {s['pire']:+_.0f} $".replace("_", " "))


if __name__ == "__main__":
    main()
