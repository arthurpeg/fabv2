"""Évals FTMO 1-Step plus rapides avec mom, 3n et M2 : grille de plans et de risques choisie sur 2011-07 → 2018-12,
vérifiée sans changement sur 2019-01 → 2026-08 (demande du 2026-11-04).

EXPLORATOIRE, hors compteur (réglage d'un contrat sur des trades existants). La sélection est faite sur la première
période seulement ; la seconde ne sert qu'à vérifier. 3n et M2 ont été choisis par leurs auteurs sur 2013-2024 et ont
échoué hors échantillon (n° 24, 25) ; mom a passé le sien (n° 11).

uv run python run_propfirm_eval_rapide.py → results/propfirm_eval_rapide/ (run.log, grille.csv, retenus.csv)

Trades (objectif à 2 R) : 3n et M2 de results/propfirm_combo/trades_tp2.csv, mom de cache/propfirm/nq_nuit_tp4.parquet.
Calendrier : toutes les séances où au moins une des trois règles a une donnée ; un jour sans trade fait avancer
l'horloge (durée en séances calendaires, ≈ 21 par mois).
Plans (risque de chaque trade en % du capital initial ; la somme du jour ne dépasse jamais 2,5 %) :
  A « 3n prioritaire » : nuit 3n -> 3n à r3 ; sinon mom à rm, puis M2 à r2 s'il y a un setup ;
  B « mom toujours »   : mom à rm chaque nuit, puis M2 à r2 (3n ignoré) ;
  C « 3n + mom »       : nuit 3n -> 3n à r3 et mom à rm ; sinon mom à rm ; M2 à r2 les jours sans 3n.
Moteur : celui du n° 18 (propfirm/ftmo.py) à plusieurs trades par jour : risque de chaque trade = r x min(1, marge
jusqu'au plancher / risque total du jour), plancher et perte du jour (3 %) vérifiés après chaque trade, objectif +10 %,
règle du meilleur jour 50 %. Coût CFD 1,5 point au niveau actuel du NQ, par trade. Depuis la correction du 2026-11-04,
l'objectif de chaque trade d'éval est ramené au reste à faire (MFE_R) ; ancienne version : *_objectif_fixe.* .
Choix : parmi les réglages qui passent au moins 60 % des évals sur 2011-2018 (5 000 comptes), le plus court en durée
moyenne d'une éval validée ; on rapporte aussi le front « passage / durée ».
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.ftmo import DAILY, MAXLOSS, MIN_RISK, TARGET

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_eval_rapide")
SEED = 1828
COST = 1.5 / 25_684.0
CHOIX, VERIF = ("2011-07-01", "2018-12-31"), ("2019-01-01", "2026-08-28")
NIVEAUX = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]
CAP_JOUR, P_MIN = 2.5, 0.60
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def trades() -> pd.DataFrame:
    t = pd.read_csv("results/propfirm_combo/trades_tp2.csv", parse_dates=["date"])[["date", "strat", "R_brut", "s", "MFE_R"]]
    m = pd.read_parquet("cache/propfirm/nq_nuit_tp4_mfe.parquet")  # build_mfe_mom.py
    m = pd.DataFrame({"date": pd.to_datetime(m.night), "strat": "mom", "R_brut": m.R_brut,
                      "s": m.risk.fillna(m.risk.median()), "MFE_R": m.MFE_R})
    return pd.concat([t, m], ignore_index=True)


def matrices(t: pd.DataFrame, a: str, z: str) -> dict:
    """Pour chaque séance : R brut, coût en R et présence de chaque règle (3n, mom, M2)."""
    t = t[(t.date >= a) & (t.date <= z)]
    jours = pd.DatetimeIndex(sorted(set(t.date)))
    out = {"n": len(jours)}
    for s in ("3n", "mom", "M2"):
        x = t[t.strat == s].set_index("date").reindex(jours)
        out[s] = (x.R_brut.fillna(0.0).to_numpy(), (COST / x.s).fillna(0.0).to_numpy(), x.R_brut.notna().to_numpy(),
                  x.MFE_R.fillna(0.0).to_numpy())
    return out


def plan(M: dict, nom: str, r3: float, rm: float, r2: float):
    """(R, c, risque, MFE) de forme (séances, 3) ; None si un jour peut perdre plus que CAP_JOUR."""
    h3, hm, h2 = M["3n"][2], M["mom"][2], M["M2"][2]
    w = np.zeros((M["n"], 3))
    if nom == "A":
        w[:, 0] = np.where(h3, r3, 0)
        w[:, 1] = np.where(~h3 & hm, rm, 0)
        w[:, 2] = np.where(~h3 & h2, r2, 0)
    elif nom == "B":
        w[:, 1] = np.where(hm, rm, 0)
        w[:, 2] = np.where(h2, r2, 0)
    elif nom == "C":
        w[:, 0] = np.where(h3, r3, 0)
        w[:, 1] = np.where(hm, rm, 0)
        w[:, 2] = np.where(~h3 & h2, r2, 0)
    if w.sum(axis=1).max() > CAP_JOUR + 1e-9:
        return None
    R = np.column_stack([M[s][0] for s in ("3n", "mom", "M2")])
    c = np.column_stack([M[s][1] for s in ("3n", "mom", "M2")])
    mfe = np.column_stack([M[s][3] for s in ("3n", "mom", "M2")])
    return R, c, w, mfe


def run_eval(R, c, w, mfe, n: int, rng, max_days: int = 3000, reste: bool = True):
    nd = len(R)
    tot = w.sum(axis=1)
    P, hi, best = np.zeros(n), np.zeros(n), np.zeros(n)
    days, st = np.zeros(n, int), np.zeros(n, int)
    start = rng.integers(0, nd, n)
    for _ in range(max_days):
        a = np.flatnonzero(st == 0)
        if not len(a):
            break
        marge = P[a] - (hi[a] - MAXLOSS)
        dead = marge < MIN_RISK
        st[a[dead]] = -1
        a, marge = a[~dead], marge[~dead]
        day = (start[a] + days[a]) % nd
        scale = np.minimum(1.0, marge / np.maximum(tot[day], 1e-12))
        pnl = np.zeros(len(a))
        fail = np.zeros(len(a), bool)
        for k in (1, 0, 2):  # ordre horaire : mom 20:00 et 3n 20:05 (nuit), puis M2 9:35
            risk = w[day, k] * scale
            Rk, ck = R[day, k], c[day, k]
            if reste:  # objectif ramené au reste à faire (cible et meilleur jour), atteint si le MFE le dépasse
                need = np.maximum(np.maximum(TARGET - P[a], 2 * np.maximum(best[a], pnl) - P[a]), 0.01)
                obj = need * (1 + ck) / np.maximum(risk, 1e-12) + ck
                Rk = np.where((risk > 0) & (obj < 2.0) & (mfe[day, k] >= obj), obj, Rk)
            leg = np.where((risk > 0) & ~fail, risk * (Rk - ck) / (1 + ck), 0.0)
            P[a] += leg
            pnl += leg
            fail |= (P[a] <= hi[a] - MAXLOSS + 1e-9) | (pnl <= -DAILY)
        days[a] += 1
        st[a[fail]] = -1
        best[a] = np.maximum(best[a], pnl)
        hi[a] = np.maximum(hi[a], P[a])
        ok = ~fail & (P[a] >= TARGET - 1e-9) & (best[a] <= 0.5 * P[a] + 1e-9)
        st[a[ok]] = 1
    ok = st == 1
    return ok.mean(), days[ok].mean() if ok.any() else np.nan, np.median(days[ok]) if ok.any() else np.nan, \
        np.percentile(days[ok], 90) if ok.any() else np.nan, days.mean()


def grille(M: dict, n: int, rng) -> pd.DataFrame:
    rows = []
    for nom in ("A", "B", "C"):
        for r3, rm, r2 in itertools.product(NIVEAUX if nom != "B" else [0.0], NIVEAUX, [0.0] + NIVEAUX):
            p = plan(M, nom, r3, rm, r2)
            if p is None:
                continue
            pp, moy, med, p90, tent = run_eval(*p, n, rng)
            rows.append(dict(plan=nom, r3=r3, rm=rm, r2=r2, passage=pp, jours_moy=moy, jours_med=med, jours_p90=p90,
                             jours_tentative=tent))
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = trades()
    MC, MV = matrices(t, *CHOIX), matrices(t, *VERIF)
    say(f"Choix sur {CHOIX[0]} → {CHOIX[1]} ({MC['n']} séances), vérification sur {VERIF[0]} → {VERIF[1]} "
        f"({MV['n']} séances) ; perte max du jour ≤ {CAP_JOUR} % ; passage ≥ {P_MIN:.0%}")
    rng = np.random.default_rng(SEED)
    G = grille(MC, 5_000, rng)
    G.to_csv(OUT / "grille.csv", index=False)
    say(f"{len(G)} réglages testés")
    ok = G[G.passage >= P_MIN].sort_values("jours_moy")
    front = G.sort_values("jours_moy")
    front = front[front.passage >= front.passage.cummax()]  # front passage / durée
    say(f"\nFront passage / durée (2011-2018, 5 000 comptes) :\n{front.round(3).to_string(index=False)}")
    say(f"\n10 plus rapides avec passage ≥ {P_MIN:.0%} :\n{ok.head(10).round(3).to_string(index=False)}")

    refs = pd.DataFrame([dict(plan="B", r3=0.0, rm=2.5, r2=0.0, ref="mom seul 2,5 %"),
                         dict(plan="A", r3=2.5, rm=1.25, r2=1.25, ref="trio demandé (3n 2,5 ; mom 1,25 ; M2 1,25)")])
    pick = ok.head(5).assign(ref="choisi sur 2011-2018")
    rows = []
    for _, x in pd.concat([refs, pick[refs.columns]]).iterrows():
        for lab, M in (("2011-2018 (choix)", MC), ("2019-2026 (vérification)", MV)):
            pp, moy, med, p90, tent = run_eval(*plan(M, x.plan, x.r3, x.rm, x.r2), 20_000, rng)
            rows.append(dict(ref=x.ref, plan=x.plan, r3=x.r3, rm=x.rm, r2=x.r2, période=lab, passage=pp,
                             jours_moy=moy, jours_med=med, jours_p90=p90, jours_tentative=tent))
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "retenus.csv", index=False)
    say(f"\nRetenus et références (20 000 comptes ; jours = séances calendaires, ≈ 21 par mois) :\n"
        f"{R.round(3).to_string(index=False)}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
