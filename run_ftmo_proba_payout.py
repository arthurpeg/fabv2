"""Probabilité de toucher un payout en démarrant le plan retenu avec deux comptes 10k (A = mom, B = 3n + M2, règle
des annonces + cible + attente) — demande du 2026-11-04. EXPLORATOIRE, hors compteur.

uv run python run_ftmo_proba_payout.py [N] → results/ftmo_proba_payout/ (run.log, departs_<scénario>.csv)

Pour chaque départ, chaque compte est joué avec rachat après chaque échec (Compte de run_ftmo_deux_comptes.py) jusqu'à
son premier reward, sur 2 ans au plus. On note le numéro de l'éval qui a donné le premier reward et la date. On en déduit :
  - P(la toute première éval achetée donne un reward), par compte et pour au moins un des deux ;
  - P(au moins un reward en achetant au plus k évals par compte) ;
  - le délai jusqu'au premier reward.
Départs : (1) historique, un départ à chaque séance de 2011-07-01 à 2024-11 (dates réelles, reward au 14e jour
calendaire) ; (2) Monte-Carlo par blocs (run_ftmo_monte_carlo.indices), scénarios « historique » et « edge / 2 ».
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as M
import run_ftmo_monte_carlo as MC

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000
OUT = Path("results/ftmo_proba_payout")
H = 504  # 2 ans
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def premier_reward(jours, idx, jambes, calendaire):
    """(numéro de l'éval du premier reward ou nan, séance du premier reward ou nan, jours calendaires)."""
    C = M.Compte("x", calendaire, True, "cible+attente")
    d0 = jours[idx[0]][0]
    passe = (np.nan, np.nan)  # (numéro de l'éval validée en premier, séance)
    for t, i in enumerate(idx):
        d, row = jours[i]
        ev = C.evals
        C.jour(d, jambes(row))
        if np.isnan(passe[0]) and C.phase == "financé" and C.evals == ev:
            passe = (ev, t)
        if C.rewards > 0:
            return ev, t, (d - d0).days, *passe
    return np.nan, np.nan, np.nan, *passe


def depart(jours, idx, calendaire):
    ea, ta, ja, pa, sa = premier_reward(jours, idx, M.jambes_A, calendaire)
    eb, tb, jb, pb, sb = premier_reward(jours, idx, M.jambes_B, calendaire)
    return dict(evals_A=ea, seance_A=ta, jours_A=ja, passe_A=pa, seance_passe_A=sa,
                evals_B=eb, seance_B=tb, jours_B=jb, passe_B=pb, seance_passe_B=sb)


def resume(nom, D):
    D.to_csv(OUT / f"departs_{nom}.csv", index=False)
    say(f"\n===== {nom} : {len(D)} départs, horizon {H} séances =====")
    ea, eb = D.evals_A.fillna(99), D.evals_B.fillna(99)
    for k in (1, 2, 3, 5, 10):
        pa, pb = (ea <= k).mean(), (eb <= k).mean()
        p1 = ((ea <= k) | (eb <= k)).mean()
        p2 = ((ea <= k) & (eb <= k)).mean()
        say(f"  ≤ {k:>2} éval(s) par compte ({2 * k * M.FEE:,.0f} $ au plus) : P(reward A) {100 * pa:5.1f} % ; "
            f"P(reward B) {100 * pb:5.1f} % ; P(au moins un) {100 * p1:5.1f} % ; P(les deux) {100 * p2:5.1f} %")
    qa, qb = D.passe_A.fillna(99), D.passe_B.fillna(99)
    for k in (1, 2, 3, 5):
        say(f"  validation ≤ {k} éval(s) par compte : A {100 * (qa <= k).mean():5.1f} % ; B {100 * (qb <= k).mean():5.1f} % ; "
            f"au moins un {100 * ((qa <= k) | (qb <= k)).mean():5.1f} % ; les deux {100 * ((qa <= k) & (qb <= k)).mean():5.1f} %")
    for k in ("A", "B"):
        f1 = D[f"passe_{k}"] == 1
        say(f"  {k} : 1re éval validée → reward sur ce financé {100 * (D.loc[f1, f'evals_{k}'] == 1).mean():.1f} % ; "
            f"durée de la 1re éval validée : médiane {D.loc[f1, f'seance_passe_{k}'].median():.0f} séances, "
            f"90e c. {D.loc[f1, f'seance_passe_{k}'].quantile(.9):.0f}")
    say(f"  jamais de reward en 2 ans : A {100 * D.evals_A.isna().mean():.1f} %, B {100 * D.evals_B.isna().mean():.1f} %")
    for k in ("A", "B"):
        s = D[f"seance_{k}"].dropna()
        s1 = D.loc[D[f"evals_{k}"] == 1, f"seance_{k}"]
        say(f"  délai du 1er reward {k} (séances) : médiane {s.median():.0f}, 75e c. {s.quantile(.75):.0f}, "
            f"90e c. {s.quantile(.9):.0f} ; si la 1re éval passe : médiane {s1.median():.0f}")
    t = np.fmin(D.seance_A.fillna(9e9), D.seance_B.fillna(9e9))
    t = t[t < 9e9]
    say(f"  délai du 1er reward, tous comptes (séances) : médiane {t.median():.0f}, 75e c. {t.quantile(.75):.0f}, "
        f"90e c. {t.quantile(.9):.0f} ; P(un reward en 3 mois) {100 * (t < 63).sum() / len(D):.1f} %, "
        f"6 mois {100 * (t < 126).sum() / len(D):.1f} %, 1 an {100 * (t < 252).sum() / len(D):.1f} %")
    say(f"  corrélation « 1re éval payée » A / B : "
        f"{(D.evals_A == 1).astype(float).corr((D.evals_B == 1).astype(float)):+.2f}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lib = M.bibliotheque()
    jours = M.tableau(lib)
    dates = pd.DatetimeIndex([d for d, _ in jours])
    fin = len(jours) - H
    rows = [dict(départ=dates[i0].date(), **depart(jours, np.arange(i0, i0 + H), True)) for i0 in range(fin)]
    resume("historique", pd.DataFrame(rows))
    for nom, src in (("mc_historique", jours), ("mc_edge_2", M.tableau(MC.decale(lib, 0.5)))):
        rng = np.random.default_rng(MC.SEED)
        MC.H = H
        resume(nom, pd.DataFrame([depart(src, MC.indices(len(src), rng), False) for _ in range(N)]))
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
