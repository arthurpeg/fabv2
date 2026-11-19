"""Exploratoire : variantes de montée en taille FTMO 1-Step depuis un seul compte 10k (règle NQ de nuit), avec des
seuils au 95e centile de l'argent sorti avant remboursement par la configuration visée.

uv run python run_propfirm_variants.py  → results/propfirm_variants/ (run.log, thresholds.csv, paths.csv)

Rendements de chaque nuit : results/propfirm_farm_heures/returns.csv (vectorbt). Règles FTMO : run_propfirm_vbt.replay
(éval 2 % TP 5, financé 1 % TP 4, rachat le lendemain d'un compte raté ou perdu, 3 nuits de vérification).

Une configuration = des comptes (heure → taille), affectés dans l'ordre 20:00, 19:00, 21:00. Seuil d'une
configuration = 95e centile, sur 612 départs et 3 ans, de l'argent sorti avant remboursement (−minimum de la
trésorerie cumulée) quand ces comptes démarrent le même soir et sont rachetés à chaque échec.
Chemin : départ avec le seuil de 1 × 10k arrondi à 50 $ ; on passe à la configuration suivante dès que les gains
nets (trésorerie − départ) couvrent son seuil. À chaque achat, un compte prend la taille de la configuration en cours ;
un compte absent de la configuration en cours n'est plus racheté (son compte ouvert finit sa vie) ; un compte ajouté
démarre la nuit suivante. Un achat se fait toujours (apport personnel mesuré si la trésorerie ne suffit pas).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_propfirm_vbt as V
from propfirm.ftmo import EUR, PRICES_EUR

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_variants")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
H, STEP, Q = 756, 5, 0.95
ORDER = ("20:00", "19:00", "21:00")
FEE = {s: PRICES_EUR[s] * EUR for s in (10_000, 100_000)}

R = pd.read_csv("results/propfirm_farm_heures/returns.csv", index_col=0, parse_dates=True)
NT = len(R)
_cache: dict = {}


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def events(hour: str, start: int, end: int):
    key = (hour, start, end)
    if key not in _cache:
        r5, r4, s = R[f"ret_{hour}_tp5"].to_numpy(), R[f"ret_{hour}_tp4"].to_numpy(), R[f"stop_{hour}"].to_numpy()

        def pnl(i, ph, risk):
            x = (r5 if ph == "éval" else r4)[i]
            return 0.0 if np.isnan(x) else risk * x / (s[i] + V.COST)

        _cache[key] = V.replay(pnl, end, start)[0]
    return _cache[key]


def cfg(n100: int, n10: int) -> dict:
    """n100 comptes 100k puis n10 comptes 10k, heures dans l'ordre 20:00, 19:00, 21:00."""
    sizes = [100_000] * n100 + [10_000] * n10
    return dict(zip(ORDER, sizes))


def label(c: dict) -> str:
    n100 = sum(v == 100_000 for v in c.values()); n10 = len(c) - n100
    return " + ".join(x for x in (f"{n100}×100k" if n100 else "", f"{n10}×10k" if n10 else "") if x)


def threshold(c: dict, starts) -> float:
    out = []
    for s0 in starts:
        cash = np.zeros(H)
        for h, size in c.items():
            for k, j, *x in events(h, s0, s0 + H):
                if k == "achat":
                    cash[j - s0] -= FEE[size]
                elif k == "reward":
                    cash[j - s0] += x[0] / 100 * size
        out.append(max(0.0, -np.cumsum(cash).min()))
    return float(np.quantile(out, Q))


def path(seq: list[dict], thr: list[float], s0: int, cash0: float) -> dict:
    end = s0 + H
    cash, low, k = cash0, cash0, 0
    slots: dict = {}
    t_final, t100, marks = None, None, {252: None, 504: None}

    def add(h, j):
        slots[h] = dict(evs=events(h, j, end), ptr=0, size=None, alive=True)

    for h in seq[0]:
        add(h, s0)
    for j in range(s0, end):
        for m in marks:
            if marks[m] is None and j - s0 >= m:
                marks[m] = cash - cash0
        todo = []
        for h, sl in slots.items():
            while sl["alive"] and sl["ptr"] < len(sl["evs"]) and sl["evs"][sl["ptr"]][1] == j:
                todo.append((0 if sl["evs"][sl["ptr"]][0] == "reward" else 1, h, sl["evs"][sl["ptr"]]))
                sl["ptr"] += 1
        for _, h, (kind, _, *x) in sorted(todo, key=lambda z: z[0]):
            sl = slots[h]
            if not sl["alive"]:
                continue
            if kind == "reward":
                cash += x[0] / 100 * sl["size"]
            elif kind == "achat":
                target = seq[k].get(h)
                if target is None:
                    sl["alive"] = False  # plus dans la configuration : pas de rachat
                    continue
                sl["size"] = target
                if target == 100_000 and t100 is None:
                    t100 = j - s0
                cash -= FEE[target]
                low = min(low, cash)
        while k + 1 < len(seq) and cash - cash0 >= thr[k + 1]:
            k += 1
        for h in seq[k]:
            if h not in slots or not slots[h]["alive"]:
                add(h, j + 1)
        if t_final is None and k == len(seq) - 1 and all(
                h in slots and slots[h]["alive"] and slots[h]["size"] == v for h, v in seq[-1].items()):
            t_final = j - s0
    return dict(premier_100k=t100, final=t_final, net_1an=marks[252], net_2ans=marks[504], net_3ans=cash - cash0, apport=max(0.0, -low))


VARIANTS = {
    "A. 1×10k → 1×100k → 2×100k → 3×100k": [cfg(0, 1), cfg(1, 0), cfg(2, 0), cfg(3, 0)],
    "B. 1×10k → 3×10k → 3×100k": [cfg(0, 1), cfg(0, 3), cfg(3, 0)],
    "C. 1×10k → 2×10k → 1×100k → 3×100k": [cfg(0, 1), cfg(0, 2), cfg(1, 0), cfg(3, 0)],
    "D. 1×10k → 2×10k → 1×100k → 2×100k → 3×100k": [cfg(0, 1), cfg(0, 2), cfg(1, 0), cfg(2, 0), cfg(3, 0)],
    "E. 1×10k → 2×10k → 2×100k → 3×100k": [cfg(0, 1), cfg(0, 2), cfg(2, 0), cfg(3, 0)],
    "F. 1×10k → 2×10k → 3×10k → 1×100k → 2×100k → 3×100k": [cfg(0, 1), cfg(0, 2), cfg(0, 3), cfg(1, 0), cfg(2, 0), cfg(3, 0)],
    "G. 1×10k → 3×10k → 1×100k + 2×10k → 2×100k + 1×10k → 3×100k": [cfg(0, 1), cfg(0, 3), cfg(1, 2), cfg(2, 1), cfg(3, 0)],
    "H. 1×10k → 2×10k → 1×100k + 1×10k → 2×100k → 3×100k": [cfg(0, 1), cfg(0, 2), cfg(1, 1), cfg(2, 0), cfg(3, 0)],
    "I. 1×10k → 1×100k + 1×10k → 2×100k + 1×10k → 3×100k": [cfg(0, 1), cfg(1, 1), cfg(2, 1), cfg(3, 0)],
}


def main() -> None:
    starts = np.arange(0, NT - H, STEP)
    say(f"Variantes de montée en taille FTMO depuis 1 × 10k, seuils au {Q:.0%} centile ; {len(starts)} départs "
        f"{R.index[starts[0]].date()} → {R.index[starts[-1]].date()}, horizon 3 ans")
    configs = {label(c): c for seq in VARIANTS.values() for c in seq}
    thr = {k: threshold(c, starts) for k, c in configs.items()}
    pd.Series(thr).to_csv(OUT / "thresholds.csv")
    say("Seuils (95e centile de l'argent sorti avant remboursement) : " + " ; ".join(f"{k} {v:,.0f} $" for k, v in thr.items()).replace(",", " "))
    cash0 = float(np.ceil(thr["1×10k"] / 50) * 50)
    say(f"Départ avec {cash0:.0f} $")
    rows = []
    for name, seq in VARIANTS.items():
        t = [thr[label(c)] for c in seq]
        for s0 in starts:
            rows.append(dict(variante=name, start=R.index[s0].date(), **path(seq, t, s0, cash0)))
        g = pd.DataFrame([r for r in rows if r["variante"] == name])
        say(f"\n=== {name} ===  seuils " + " → ".join(f"{x:,.0f} $" for x in t[1:]).replace(",", " "))
        say(f"  premier achat d'une éval 100k : {g.premier_100k.notna().mean():.0%} des départs en 3 ans, moyenne "
            f"{g.premier_100k.mean():.0f} nuits (~{g.premier_100k.mean() / 21:.1f} mois), médiane {g.premier_100k.median():.0f}, "
            f"25e-75e centile {g.premier_100k.quantile(0.25):.0f}-{g.premier_100k.quantile(0.75):.0f}, 90e {g.premier_100k.quantile(0.9):.0f}, pire {g.premier_100k.max():.0f}")
        say(f"  3 × 100k en place : {g.final.notna().mean():.0%} des départs en 3 ans, médiane {g.final.median():.0f} nuits "
            f"(~{g.final.median() / 21:.0f} mois)")
        for c, lab in (("net_1an", "gain net à 1 an"), ("net_2ans", "à 2 ans"), ("net_3ans", "à 3 ans")):
            say(f"  {lab:<16} : médiane {g[c].median():+,.0f} $, 5e centile {g[c].quantile(0.05):+,.0f} $, pire {g[c].min():+,.0f} $".replace(",", " "))
        say(f"  apport en plus des {cash0:.0f} $ : nul dans {(g.apport == 0).mean():.0%} des départs, pire {g.apport.max():,.0f} $".replace(",", " "))
    P = pd.DataFrame(rows)
    P.to_csv(OUT / "paths.csv", index=False)
    S = P.groupby("variante", sort=False).agg(trio_pct=("final", lambda x: x.notna().mean()), trio_mois=("final", lambda x: x.median() / 21),
                                              net1=("net_1an", "median"), net2=("net_2ans", "median"), net3=("net_3ans", "median"),
                                              net3_p5=("net_3ans", lambda x: x.quantile(0.05)), net3_min=("net_3ans", "min"),
                                              apport_max=("apport", "max"))
    W = P.pivot(index="start", columns="variante", values="net_3ans")
    S["meilleure_à_3ans"] = (W.eq(W.max(axis=1), axis=0)).mean().reindex(S.index)
    say("\nRésumé (gains en $ ; « meilleure » = part des départs où la variante gagne le plus à 3 ans) :")
    say(S.round(2).to_string())


if __name__ == "__main__":
    main()
