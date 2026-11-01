"""Exploratoire : gestion du risque sur mesure pour FTMO 1-Step 100k, règle NQ de nuit (pendant de run_propfirm_fp_custom).

uv run python run_propfirm_ftmo_custom.py  → results/propfirm_ftmo_custom/ (run.log, grid.csv)

Critère : un compte racheté à chaque échec pendant 3 ans (756 nuits), départs toutes les 5 nuits ; choix sur les
départs 2011-07 → 2018-12 (médiane du gain net), vérification sur 2019-01 → 2023-08. Règles comme
run_propfirm_multi : objectif +10 %, perte max 10 % suiveuse (sous le plus haut solde de clôture), perte du jour 3 %,
meilleur jour ≤ 50 % du profit pour valider ; financé 3 nuits après la validation ; reward après ≥ 10 jours tradés
dans le cycle avec meilleur jour ≤ 50 % du profit du cycle, 90 %, puis solde et perte max remis à zéro. Pas de plafond
de levier (comme dans les simulations FTMO précédentes). Financé : règle FTMO des annonces (aucune exécution, stop et
objectif compris, 2 min autour du NFP, du CPI, du PIB avancé…) respectée en fermant la position à 8:19 ET les jours
d'annonce 8:30 (propfirm.nights, variante 1 : tous les jours d'annonce 8:30 du calendrier, liste plus large que celle
de FTMO, donc prudent). L'éval n'est pas concernée.
Grille (limites de l'utilisateur : éval ≤ 2,5 %, financé ≤ 1 %) : éval risque 1 / 1,5 / 2 / 2,5 %, objectif 0,75 … 3 R ramené au reste à faire (cible et consistance) ;
financé risque 0,5 / 0,75 / 1 %, objectif 1 … 3 R ; protection : risque divisé par 2 dès que
le profit du cycle dépasse 2 % ou 4 % (ou jamais).
"""

from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.generic import _trade
from propfirm.nights import build

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_ftmo_custom")
OUT.mkdir(parents=True, exist_ok=True)
LOG = None
L = build()
SIZE, FEE, TARGET, DD, DLL, CONS, REVIEW, CYCLE, SPLIT = 100e3, 549.0, 10e3, 10e3, 3e3, 0.5, 3, 10, 0.9
H3, STEP = 756, 5
STARTS = np.arange(0, L.n - H3, STEP)
IS = L.dates[STARTS] < pd.Timestamp("2019-01-01")
E_R, E_RR = (0.01, 0.015, 0.02, 0.025), (0.75, 1.0, 1.5, 2.0, 2.5, 3.0)
F_R, F_RR, F_PROT = (0.005, 0.0075, 0.01), (1.0, 1.5, 2.0, 2.5, 3.0), (None, 0.02, 0.04)


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def chain(re_, rre, rf, rrf, prot, cap_tp=True):
    n = len(STARTS)
    ph = np.zeros(n, int)                      # 0 éval, 1 financé
    wait = np.zeros(n, int)                    # nuits d'attente avant le financé
    P = np.zeros(n); hi = np.zeros(n); best = np.zeros(n); cdays = np.zeros(n, int)
    cash = -np.full(n, FEE); low = cash.copy(); evals = np.ones(n, int); npay = np.zeros(n, int)
    side_all = np.where(L.dir > 0, 0, 1)
    for step in range(H3):
        i = STARTS + step
        e = ph == 0
        act = wait == 0
        floor = hi - DD
        room = P - floor
        risk = np.where(e, np.minimum(re_ * SIZE, room), np.minimum(rf * SIZE, room))
        if prot is not None:
            risk = np.where(~e & (P >= prot * SIZE), risk * 0.5, risk)
        risk = np.minimum(risk, DLL * 0.999)
        side = side_all[i]
        need = np.maximum(np.maximum(TARGET - P, best / CONS - P), 1.0)
        _, _, _, perR, cost = _trade(L, "cfd", i, side, 0, risk, np.full(n, 1.0), None, None)
        tp_e = np.minimum(rre, (need + cost) / np.maximum(perR, 1e-9)) if cap_tp else np.full(n, rre)
        tp = np.where(e, tp_e, rrf)
        pnl, _, _, _, _ = _trade(L, "cfd", i, side, np.where(e, 0, 1), risk, tp, None, None)  # financé : à plat avant 8:30
        pnl = np.where(act, pnl, 0.0)
        wait = np.maximum(wait - 1, 0)
        P += pnl
        dead = act & ((P <= floor + 1e-6) | (pnl <= -DLL + 1e-6) | (risk < 50))
        best = np.where(act & ~dead, np.maximum(best, pnl), best)
        hi = np.where(act & ~dead, np.maximum(hi, P), hi)
        cdays += act & ~dead & ~e
        ok = e & act & ~dead & (P >= TARGET - 1e-6) & (best <= CONS * P + 1e-6)
        due = ~e & act & ~dead & (cdays >= CYCLE) & (P > 1.0) & (best <= CONS * P + 1e-6)
        cash += np.where(due, SPLIT * P, 0); npay += due
        reset = due | dead | ok
        cash -= np.where(dead, FEE, 0); evals += dead
        low = np.minimum(low, cash)
        ph = np.where(dead, 0, np.where(ok, 1, ph))
        wait = np.where(ok, REVIEW, wait)
        P = np.where(reset, 0.0, P); hi = np.where(reset, 0.0, hi); best = np.where(reset, 0.0, best)
        cdays = np.where(reset, 0, cdays)
    return dict(net=cash, mise=-np.minimum(low, 0), evals=evals, npay=npay)


def stats(r, m):
    x = r["net"][m]
    return dict(med=np.median(x), p5=np.quantile(x, 0.05), pire=x.min(), mise_med=np.median(r["mise"][m]),
                mise_max=r["mise"][m].max(), evals=np.median(r["evals"][m]), retraits=np.median(r["npay"][m]))


def main() -> None:
    global LOG
    LOG = open(OUT / "run.log", "w", encoding="utf-8")
    say(f"FTMO 1-Step 100k, règles sur mesure ; {len(STARTS)} départs de 3 ans ({IS.sum()} en 2011-2018, "
        f"{(~IS).sum()} en 2019-2023)")
    for lab, args in (("plan FTMO (2 % à 2,5 R, objectif fixe ; 1 % à 2 R)", (0.02, 2.5, 0.01, 2.0, None, False)),
                      ("réglage 0,1 × perte max (1 % à 2 R ; 1 % à 1 R)", (0.01, 2.0, 0.01, 1.0, None, True))):
        r = chain(*args)
        for per, m in (("2011-2018", IS), ("2019-2023", ~IS), ("tout", slice(None))):
            s = stats(r, m)
            say(f"  référence {lab}, {per} : médiane {s['med']:+_.0f} $, 5e c. {s['p5']:+_.0f} $, pire {s['pire']:+_.0f} $, "
                f"argent sorti max {s['mise_max']:_.0f} $, évals {s['evals']:.0f}, rewards {s['retraits']:.0f}".replace("_", " "))
    rows = []
    for re_, rre, rf, rrf, prot in product(E_R, E_RR, F_R, F_RR, F_PROT):
        r = chain(re_, rre, rf, rrf, prot)
        a, b = stats(r, IS), stats(r, ~IS)
        rows.append(dict(e_risk=re_, e_rr=rre, f_risk=rf, f_rr=rrf, protection=prot,
                         **{f"is_{k}": v for k, v in a.items()}, **{f"oos_{k}": v for k, v in b.items()}))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / "grid.csv", index=False)
    say(f"\nGrille : {len(G)} réglages. 10 meilleurs en médiane 2011-2018 :")
    top = G.sort_values("is_med", ascending=False).head(10)
    for _, x in top.iterrows():
        say(f"  éval {x.e_risk:.1%} à {x.e_rr:g} R ; financé {x.f_risk:.2%} à {x.f_rr:g} R, protection "
            f"{'—' if pd.isna(x.protection) else f'{x.protection:.0%}'} : IS médiane {x.is_med:+_.0f} $ (pire {x.is_pire:+_.0f}) | "
            f"OOS médiane {x.oos_med:+_.0f} $, 5e c. {x.oos_p5:+_.0f} $, pire {x.oos_pire:+_.0f} $, argent sorti max "
            f"{x.oos_mise_max:_.0f} $, évals {x.oos_evals:.0f}, rewards {x.oos_retraits:.0f}".replace("_", " "))
    best = top.iloc[0]
    say("\nEffet de chaque choix autour du réglage retenu (médianes IS / OOS) :")
    keys = ["e_risk", "e_rr", "f_risk", "f_rr", "protection"]
    for k in keys:
        m = np.ones(len(G), bool)
        for o in keys:
            if o != k:
                m &= (G[o].isna() & pd.isna(best[o])) | (G[o] == best[o])
        sub = G[m].sort_values(k, key=lambda s: s.astype(str))
        say(f"  {k} : " + " ; ".join(f"{v} → IS {a:+_.0f} / OOS {b:+_.0f}".replace("_", " ")
                                     for v, a, b in zip(sub[k], sub.is_med, sub.oos_med)))
    say(f"\nMeilleur réglage hors échantillon (pour mémoire, choisi après coup) : "
        + G.sort_values("oos_med", ascending=False).head(1)[["e_risk", "e_rr", "f_risk", "f_rr", "protection", "oos_med"]].to_string(index=False))


if __name__ == "__main__":
    main()
