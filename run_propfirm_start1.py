"""Exploratoire : démarrer FTMO 1-Step avec un seul compte 10k (règle NQ de nuit), puis monter en taille.

uv run python run_propfirm_start1.py  → results/propfirm_start1/ (run.log, reserve.csv, paths.csv)

Rendements de chaque nuit : results/propfirm_farm_heures/returns.csv (vectorbt). Règles FTMO : run_propfirm_vbt.replay
(éval 2 % TP 5, financé 1 % TP 4, rachat le lendemain d'un compte raté ou perdu, 3 nuits de vérification).

1. Réserve pour un seul compte 10k racheté à chaque échec : pour chaque départ (toutes les 5 nuits, 2011-07 →
   2023-08), argent sorti de la poche avant que les rewards le remboursent (−minimum de la trésorerie cumulée),
   délai jusqu'au premier reward, plus longue série d'évals ratées. Pour chacune des trois heures.
2. Chemins sur 3 ans depuis un seul compte 10k (signal 20:00), départ avec la réserve R0 trouvée en 1. Chaque palier
   n'est franchi que quand les gains nets couvrent 2 évals par compte à la nouvelle configuration (un rachat d'avance) :
   - A « 1 × 10k → 1 × 100k → trio 100k » : le compte passe en 100k à 1 098 $ de gains (2 × 549 $), le 2e compte
     (19:00, 100k) s'ajoute à 2 196 $, le 3e (21:00, 100k) à 3 293 $ ;
   - B « 1 × 10k → trio 10k → trio 100k » : 2e compte 10k (19:00) à 348 $ (2 comptes × 2 évals × 87 $), 3e (21:00)
     à 522 $, puis toutes les évals suivantes en 100k à 3 293 $ ;
   - C « 1 × 10k → trio 100k » : à 3 293 $ de gains, le compte passe en 100k et les deux autres s'ajoutent en 100k.
   Un compte ajouté commence la nuit suivante. Les financés 10k déjà ouverts continuent jusqu'à leur perte.
   Un achat se fait toujours : si la trésorerie ne suffit pas, c'est un apport personnel, mesuré.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_propfirm_vbt as V
from propfirm.ftmo import EUR, PRICES_EUR

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_start1")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
H, STEP = 756, 5
F10, F100 = PRICES_EUR[10_000] * EUR, PRICES_EUR[100_000] * EUR

R = pd.read_csv("results/propfirm_farm_heures/returns.csv", index_col=0, parse_dates=True)
NT = len(R)


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def events(hour: str, start: int, end: int):
    r5, r4, s = R[f"ret_{hour}_tp5"].to_numpy(), R[f"ret_{hour}_tp4"].to_numpy(), R[f"stop_{hour}"].to_numpy()

    def pnl(i, ph, risk):
        x = (r5 if ph == "éval" else r4)[i]
        return 0.0 if np.isnan(x) else risk * x / (s[i] + V.COST)

    ev, _ = V.replay(pnl, end, start)
    return ev


def reserve(starts) -> pd.DataFrame:
    rows = []
    for h in ("19:00", "20:00", "21:00"):
        for s0 in starts:
            ev = events(h, s0, s0 + H)
            cash, low, first, run, worst = 0.0, 0.0, None, 0, 0
            for k, j, *x in ev:
                if k == "achat":
                    cash -= F10
                    low = min(low, cash)
                elif k == "reward":
                    cash += x[0] / 100 * 10_000
                    first = j - s0 if first is None else first
                elif k == "ratée":
                    run += 1; worst = max(worst, run)
                elif k == "validée":
                    run = 0
            rows.append(dict(heure=h, start=R.index[s0].date(), mise=-low, premier_reward=first, ratées=worst, net_3ans=cash))
    return pd.DataFrame(rows)


def worst_mise(config: list[tuple[str, int]], starts) -> float:
    """Pire argent sorti avant remboursement (−min de la trésorerie cumulée) pour des comptes (heure, taille)
    démarrés le même soir, rachetés à chaque échec, sur 3 ans, tous départs confondus."""
    worst = 0.0
    for s0 in starts:
        cash = np.zeros(H)
        for h, size in config:
            fee = PRICES_EUR[size] * EUR
            for k, j, *x in events(h, s0, s0 + H):
                if k == "achat":
                    cash[j - s0] -= fee
                elif k == "reward":
                    cash[j - s0] += x[0] / 100 * size
        worst = max(worst, -np.cumsum(cash).min())
    return worst


THR: dict[str, float] = {}  # pires chemins, remplis dans main()


def path(policy: str, s0: int, cash0: float) -> dict:
    end = s0 + H
    plan = {"A": [("20:00", 0), ("19:00", 2 * 2 * F100), ("21:00", 3 * 2 * F100)],
            "B": [("20:00", 0), ("19:00", 2 * 2 * F10), ("21:00", 3 * 2 * F10)],
            "C": [("20:00", 0), ("19:00", 3 * 2 * F100), ("21:00", 3 * 2 * F100)],
            "A2": [("20:00", 0), ("19:00", THR.get("2x100k", 0)), ("21:00", THR.get("3x100k", 0))],
            "B2": [("20:00", 0), ("19:00", THR.get("3x10k", 0)), ("21:00", THR.get("3x10k", 0))],
            "C2": [("20:00", 0), ("19:00", THR.get("3x100k", 0)), ("21:00", THR.get("3x100k", 0))]}[policy]
    to100 = {"A": 2 * F100, "B": 3 * 2 * F100, "C": 3 * 2 * F100,
             "A2": THR.get("1x100k", 0), "B2": THR.get("3x100k", 0), "C2": THR.get("3x100k", 0)}[policy]
    big = {"A": {"19:00", "21:00"}, "B": set(), "C": {"19:00", "21:00"},
           "A2": {"19:00", "21:00"}, "B2": set(), "C2": {"19:00", "21:00"}}[policy]  # comptes ajoutés directement en 100k
    cash, low, fees = cash0, cash0, 0.0
    active, cur, ptr, evs = {}, {}, {}, {}
    switched, t_switch, t_trio = False, None, None
    marks = {252: None, 504: None}

    def add(h, j):
        evs[h] = events(h, j, end); ptr[h] = 0; active[h] = True

    add(plan[0][0], s0)
    for j in range(s0, end):
        for m in marks:
            if marks[m] is None and j - s0 >= m:
                marks[m] = cash - cash0
        todo = []
        for h in list(evs):
            while ptr[h] < len(evs[h]) and evs[h][ptr[h]][1] == j:
                todo.append((0 if evs[h][ptr[h]][0] == "reward" else 1, h, evs[h][ptr[h]]))
                ptr[h] += 1
        for _, h, (k, _, *x) in sorted(todo, key=lambda z: z[0]):
            if k == "reward":
                cash += x[0] / 100 * cur[h]
            elif k == "achat":
                if not switched and cash - cash0 >= to100:
                    switched, t_switch = True, j - s0
                size = 100_000 if (switched and (policy[0] != "A" or h == "20:00")) or h in big else 10_000
                if policy[0] == "A" and h == "20:00":
                    size = 100_000 if switched else 10_000
                cur[h] = size
                fee = F100 if size == 100_000 else F10
                cash -= fee; fees += fee
                low = min(low, cash)
        gain = cash - cash0
        for h, thr in plan[1:]:
            if h not in evs and gain >= thr:
                add(h, j + 1)
        if t_trio is None and len(cur) == 3 and all(v == 100_000 for v in cur.values()):
            t_trio = j - s0
    return dict(politique=policy, start=R.index[s0].date(), bascule=t_switch, trio_100k=t_trio,
                net_1an=marks[252], net_2ans=marks[504], net_3ans=cash - cash0, apport=max(0.0, -low), frais=fees)


def main() -> None:
    starts = np.arange(0, NT - H, STEP)
    say(f"Démarrage avec un seul compte FTMO 10k (éval {F10:.0f} $), règle NQ de nuit, {len(starts)} départs de "
        f"{R.index[starts[0]].date()} à {R.index[starts[-1]].date()}, horizon 3 ans")
    Rs = reserve(starts)
    Rs.to_csv(OUT / "reserve.csv", index=False)
    say("\n1. Argent à sortir avant que les rewards remboursent (un compte 10k, rachat à chaque échec) :")
    for h, g in Rs.groupby("heure"):
        say(f"  {h} : médiane {g.mise.median():.0f} $, 90e centile {g.mise.quantile(0.9):.0f} $, 95e {g.mise.quantile(0.95):.0f} $, "
            f"pire {g.mise.max():.0f} $ ({g.mise.max() / F10:.0f} évals) ; 1er reward médiane {g.premier_reward.median():.0f} nuits "
            f"(~{g.premier_reward.median() / 21:.1f} mois), 90e centile {g.premier_reward.quantile(0.9):.0f}, pire {g.premier_reward.max():.0f} ; "
            f"pire série d'évals ratées {g.ratées.max()} ; net à 3 ans médiane {g.net_3ans.median():+,.0f} $".replace(",", " "))
    cash0 = float(np.ceil(Rs[Rs.heure == "20:00"].mise.max() / 50) * 50)
    say(f"\n2. Chemins depuis un seul compte 10k (20:00), départ avec {cash0:.0f} $ (pire mise historique du compte 20:00, arrondie)")
    P = pd.DataFrame([path(p, s0, cash0) for s0 in starts for p in ("A", "B", "C")])
    P.to_csv(OUT / "paths.csv", index=False)
    names = {"A": "1 × 10k → 1 × 100k → trio 100k", "B": "1 × 10k → trio 10k → trio 100k", "C": "1 × 10k → trio 100k"}
    for p, g in P.groupby("politique"):
        say(f"\n=== {p}. {names[p]} ===")
        say(f"  premier passage en 100k : médiane {g.bascule.median():.0f} nuits (~{g.bascule.median() / 21:.0f} mois), "
            f"75e centile {g.bascule.quantile(0.75):.0f}, atteint dans {g.bascule.notna().mean():.0%} des départs")
        say(f"  trio en 100k : médiane {g.trio_100k.median():.0f} nuits (~{g.trio_100k.median() / 21:.0f} mois), "
            f"75e centile {g.trio_100k.quantile(0.75):.0f}, atteint en 3 ans dans {g.trio_100k.notna().mean():.0%} des départs")
        for c, lab in (("net_1an", "gain net à 1 an"), ("net_2ans", "à 2 ans"), ("net_3ans", "à 3 ans")):
            say(f"  {lab:<16} : médiane {g[c].median():+,.0f} $, 5e centile {g[c].quantile(0.05):+,.0f} $, pire {g[c].min():+,.0f} $".replace(",", " "))
        say(f"  apport en plus des {cash0:.0f} $ : nul dans {(g.apport == 0).mean():.0%} des départs, 95e centile "
            f"{g.apport.quantile(0.95):,.0f} $, pire {g.apport.max():,.0f} $".replace(",", " "))
    W = P.pivot(index="start", columns="politique", values="net_3ans")
    say(f"\nMême départ, gain à 3 ans : A > B dans {(W.A > W.B).mean():.0%}, A > C dans {(W.A > W.C).mean():.0%}, C > B dans {(W.C > W.B).mean():.0%} des cas")

    # 3. Seuils = pire chemin historique de la configuration suivante, payé par les rewards déjà reçus
    configs = {"1x10k": [("20:00", 10_000)], "1x100k": [("20:00", 100_000)],
               "2x100k": [("20:00", 100_000), ("19:00", 100_000)],
               "3x100k": [(h, 100_000) for h in ("19:00", "20:00", "21:00")],
               "3x10k": [(h, 10_000) for h in ("19:00", "20:00", "21:00")]}
    say("\n3. Pire chemin historique (argent sorti avant remboursement, 3 ans, tous départs) par configuration :")
    for k, cfg in configs.items():
        THR[k] = worst_mise(cfg, starts)
        say(f"  {k:<7} : {THR[k]:,.0f} $".replace(",", " "))
    cash0 = float(np.ceil(THR["1x10k"] / 50) * 50)
    say(f"  départ avec {cash0:.0f} $ ; un palier ne se franchit que quand les gains nets (trésorerie − {cash0:.0f} $) "
        f"couvrent le pire chemin de la configuration suivante")
    names2 = {"A2": f"1 × 10k → 1 × 100k (à {THR['1x100k']:,.0f} $) → 2 × 100k (à {THR['2x100k']:,.0f} $) → trio 100k (à {THR['3x100k']:,.0f} $)",
              "B2": f"1 × 10k → trio 10k (à {THR['3x10k']:,.0f} $) → trio 100k (à {THR['3x100k']:,.0f} $)",
              "C2": f"1 × 10k → trio 100k (à {THR['3x100k']:,.0f} $)"}
    P2 = pd.DataFrame([path(p, s0, cash0) for s0 in starts for p in ("A2", "B2", "C2")])
    P2.to_csv(OUT / "paths_pire_chemin.csv", index=False)
    for p, g in P2.groupby("politique"):
        say(f"\n=== {p}. {names2[p]} ===".replace(",", " "))
        say(f"  premier passage en 100k : médiane {g.bascule.median():.0f} nuits (~{g.bascule.median() / 21:.0f} mois), "
            f"75e centile {g.bascule.quantile(0.75):.0f}, atteint en 3 ans dans {g.bascule.notna().mean():.0%} des départs")
        say(f"  trio en 100k : médiane {g.trio_100k.median():.0f} nuits (~{g.trio_100k.median() / 21:.0f} mois), "
            f"75e centile {g.trio_100k.quantile(0.75):.0f}, atteint en 3 ans dans {g.trio_100k.notna().mean():.0%} des départs")
        for c, lab in (("net_1an", "gain net à 1 an"), ("net_2ans", "à 2 ans"), ("net_3ans", "à 3 ans")):
            say(f"  {lab:<16} : médiane {g[c].median():+,.0f} $, 5e centile {g[c].quantile(0.05):+,.0f} $, pire {g[c].min():+,.0f} $".replace(",", " "))
        say(f"  apport en plus des {cash0:.0f} $ : nul dans {(g.apport == 0).mean():.0%} des départs, 95e centile "
            f"{g.apport.quantile(0.95):,.0f} $, pire {g.apport.max():,.0f} $".replace(",", " "))
    W2 = P2.pivot(index="start", columns="politique", values="net_3ans")
    say(f"\nMême départ, gain à 3 ans : A2 > B2 dans {(W2.A2 > W2.B2).mean():.0%}, A2 > C2 dans {(W2.A2 > W2.C2).mean():.0%}, "
        f"B2 > C2 dans {(W2.B2 > W2.C2).mean():.0%} des cas")


if __name__ == "__main__":
    main()
