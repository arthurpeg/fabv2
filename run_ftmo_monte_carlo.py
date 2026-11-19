"""Monte-Carlo des deux comptes FTMO 1-Step 10k tradés en même temps (A = mom, B = 3n + M2, règle des annonces,
cible + attente en financé) : historiques synthétiques tirés par blocs de séances (demande du 2026-11-04).
EXPLORATOIRE, hors compteur.

uv run python run_ftmo_monte_carlo.py [N] → results/ftmo_monte_carlo/ (run.log, chemins_<scénario>.csv)

Tirage : bootstrap stationnaire (Politis-Romano) des séances 2011-07 → 2026-11-03, blocs de longueur géométrique de
moyenne 20 séances ; une séance tirée garde ensemble ses trades mom, 3n et M2 (corrélation entre comptes conservée), un
bloc garde l'ordre des séances (séries et régimes conservés sur environ un mois). Horizon : 3 ans (756 séances).
Règles, moteur et trades : run_ftmo_deux_comptes.py (Compte, jambes_A, jambes_B), reward après 10 séances (≈ 14 jours
calendaires), séances sans trade comprises.
Scénarios :
  « historique »  : toutes les séances 2011-07 → 2026-11 ;
  « récent »      : séances 2019-01 → 2026-11 seulement (période plus difficile pour mom) ;
  « edge / 2 »    : toutes les séances, R (et MFE) de chaque stratégie diminués de la moitié de son R moyen
                    historique : espérance divisée par deux, même volatilité.
Mesures par chemin : net à 1 et 3 ans, max DD de trésorerie, pire série d'évals entre deux rewards (par compte),
plus longue période sans aucun reward (en séances), délai du premier reward.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as M

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000
OUT = Path("results/ftmo_monte_carlo")
SEED = 1831
H, BLOC = 756, 20
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def indices(n_src: int, rng) -> np.ndarray:
    idx = np.empty(H, int)
    i = rng.integers(n_src)
    for t in range(H):
        idx[t] = i
        i = rng.integers(n_src) if rng.random() < 1 / BLOC else (i + 1) % n_src
    return idx


def chemin(jours: list, idx: np.ndarray) -> dict:
    A = M.Compte("A", False, True, "cible+attente")
    B = M.Compte("B", False, True, "cible+attente")
    cash = np.empty(H)
    rew_t, streak = [], {"A": [1], "B": [1]}
    nA = nB = 0
    first = None
    for t, i in enumerate(idx):
        d, row = jours[i]
        ea, eb, ra, rb = A.evals, B.evals, A.rewards, B.rewards
        A.jour(d, M.jambes_A(row))
        B.jour(d, M.jambes_B(row))
        for C, k, e0, r0 in ((A, "A", ea, ra), (B, "B", eb, rb)):
            if C.evals > e0:
                streak[k][-1] += C.evals - e0
            if C.rewards > r0:
                streak[k].append(0)
                rew_t.append(t)
                first = t if first is None else first
        cash[t] = A.cash + B.cash
        if t == 251:
            nA, nB = A.cash, B.cash
    gaps = np.diff([0] + sorted(set(rew_t)) + [H - 1]) if rew_t else np.array([H])
    pic = np.maximum.accumulate(np.r_[0.0, cash])
    return dict(net_1an=cash[251], net_1an_A=nA, net_1an_B=nB, net_3ans=cash[-1], net_3ans_A=A.cash,
                net_3ans_B=B.cash, max_dd=float((np.r_[0.0, cash] - pic).min()), evals_A=A.evals, evals_B=B.evals,
                rewards=A.rewards + B.rewards, serie_A=max(streak["A"]), serie_B=max(streak["B"]),
                sans_reward=int(gaps.max()), premier_reward=first if first is not None else H)


def scenario(nom: str, jours: list, rng) -> pd.DataFrame:
    rows = [chemin(jours, indices(len(jours), rng)) for _ in range(N)]
    D = pd.DataFrame(rows)
    D.to_csv(OUT / f"chemins_{nom.replace(' ', '_').replace('/', '-')}.csv", index=False)
    q = lambda s, p: s.quantile(p)
    say(f"\n===== Scénario « {nom} » : {N} chemins de 3 ans ({len(jours)} séances sources) =====")
    for col, lab in (("net_1an", "net à 1 an"), ("net_3ans", "net à 3 ans")):
        s = D[col]
        say(f"  {lab:<12}: moyenne {s.mean():+,.0f} $ ; médiane {s.median():+,.0f} $ ; 5e c. {q(s, .05):+,.0f} $ ; "
            f"1er c. {q(s, .01):+,.0f} $ ; P(< 0) {100 * (s < 0).mean():.1f} %")
    say(f"  net à 3 ans par compte : A médiane {D.net_3ans_A.median():+,.0f} $ (P < 0 {100 * (D.net_3ans_A < 0).mean():.1f} %), "
        f"B médiane {D.net_3ans_B.median():+,.0f} $ (P < 0 {100 * (D.net_3ans_B < 0).mean():.1f} %) ; "
        f"corrélation des nets A / B {D.net_3ans_A.corr(D.net_3ans_B):+.2f}")
    s = D.max_dd
    say(f"  max DD de trésorerie : médiane {s.median():,.0f} $ ; 95e c. {q(s, .05):,.0f} $ ; 99e c. {q(s, .01):,.0f} $ ; "
        f"pire {s.min():,.0f} $")
    for k in ("A", "B"):
        s = D[f"serie_{k}"]
        say(f"  pire série d'évals sans reward, compte {k} : médiane {s.median():.0f} ; 95e c. {q(s, .95):.0f} ; "
            f"99e c. {q(s, .99):.0f} ; max {s.max()} ; P(≥ 6) {100 * (s >= 6).mean():.1f} %")
    s = D.sans_reward
    say(f"  plus longue période sans aucun reward (séances) : médiane {s.median():.0f} ; 95e c. {q(s, .95):.0f} ; "
        f"max {s.max()} ; premier reward : médiane {D.premier_reward.median():.0f} séances, 95e c. "
        f"{q(D.premier_reward, .95):.0f}")
    say(f"  évals sur 3 ans : A {D.evals_A.mean():.1f}, B {D.evals_B.mean():.1f} ; rewards sur 3 ans : {D.rewards.mean():.1f}")
    return D


def decale(lib: pd.DataFrame, h: float) -> pd.DataFrame:
    """R, R_news, MFE et MFE_news de chaque stratégie diminués de h x son R moyen."""
    lib = lib.copy()
    for s, g in lib.groupby("strat"):
        mu = g.R.mean()
        for c in ("R", "R_news", "MFE", "MFE_news"):
            lib.loc[g.index, c] = g[c] - h * mu
    lib["MFE"] = lib.MFE.clip(lower=0.0)
    lib["MFE_news"] = lib.MFE_news.clip(lower=0.0)
    return lib


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lib = M.bibliotheque()
    say(f"Monte-Carlo, deux comptes 10k (A mom, B 3n + M2), règle des annonces + cible + attente ; {N} chemins de "
        f"{H} séances, blocs de {BLOC} séances en moyenne, graine {SEED}")
    say("R moyen par stratégie sur l'historique : " + ", ".join(f"{s} {g.R.mean():+.3f}" for s, g in lib.groupby("strat")))
    rng = np.random.default_rng(SEED)
    scenario("historique", M.tableau(lib), rng)
    scenario("récent", M.tableau(lib[lib.date >= "2019-01-01"]), rng)
    scenario("edge / 2", M.tableau(decale(lib, 0.5)), rng)
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
