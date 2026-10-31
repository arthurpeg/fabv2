"""Exploratoire : chemin complet du plan de montée en taille FTMO, par paliers (10k → 25k → 50k → 100k) ou en
sautant directement de 10k à 100k. Règle NQ de nuit, trio de comptes 19:00 / 20:00 / 21:00.

uv run python run_propfirm_paths.py  → results/propfirm_paths/ (run.log, paths.csv)

Rendements de chaque nuit : results/propfirm_farm_heures/returns.csv (vectorbt). Règles FTMO : run_propfirm_vbt.replay
(éval 2 % TP 5, financé 1 % TP 4, rachat le lendemain d'un compte raté ou perdu). En % du capital, la vie d'un
compte ne dépend pas de sa taille : seule la taille choisie à l'achat change les frais et les rewards en dollars.

Trésorerie : départ 1 750 $ (réserve du palier 10k). À chaque achat d'éval, la taille est choisie selon la trésorerie
du moment, en passant les rewards avant les achats de la même nuit :
- paliers : la plus grande taille dont la réserve (pire creux historique du trio) est couverte :
  10k 0 $, 25k 4 378 $, 50k 7 018 $, 100k 10 978 $ (results/propfirm_scaling/sizes.csv) ;
- direct : 100k si la trésorerie couvre 10 978 $, sinon 10k ;
- direct agressif : 100k dès que la trésorerie couvre le prix d'une éval 100k (549 $), sinon 10k.
Un achat se fait même si la trésorerie ne le couvre pas : on mesure alors l'apport personnel nécessaire.
Départs tous les 5 nuits sur 2011-07 → 2023-08 (au moins 3 ans de données après).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_propfirm_vbt as V
from propfirm.ftmo import EUR, PRICES_EUR

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_paths")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
HOURS = ("19:00", "20:00", "21:00")
H, STEP, CASH0 = 756, 5, 1750.0
RESERVE = {10_000: 0.0, 25_000: 4378.0, 50_000: 7018.0, 100_000: 10978.0}
FEE = {k: PRICES_EUR[k] * EUR for k in RESERVE}

R = pd.read_csv("results/propfirm_farm_heures/returns.csv", index_col=0, parse_dates=True)
NT = len(R)


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def slot_events(hour: str, start: int):
    r5, r4, s = R[f"ret_{hour}_tp5"].to_numpy(), R[f"ret_{hour}_tp4"].to_numpy(), R[f"stop_{hour}"].to_numpy()

    def pnl(i, ph, risk):
        x = (r5 if ph == "éval" else r4)[i]
        return 0.0 if np.isnan(x) else risk * x / (s[i] + V.COST)

    ev, _ = V.replay(pnl, start + H, start)
    return ev


def size_for(policy: str, cash: float) -> int:
    if policy == "direct":
        return 100_000 if cash >= RESERVE[100_000] else 10_000
    if policy == "direct agressif":
        return 100_000 if cash >= FEE[100_000] else 10_000
    return max(k for k, v in RESERVE.items() if cash >= v)


def path(policy: str, evs: dict) -> dict:
    # (nuit, ordre, compte) : rewards (0) avant achats (1) la même nuit
    q = []
    for h, ev in evs.items():
        for k, j, *x in ev:
            if k == "achat":
                q.append((j, 1, h, "achat", 0.0))
            elif k == "reward":
                q.append((j, 0, h, "reward", x[0]))
    q.sort()
    cash, low, fees, cur = CASH0, CASH0, 0.0, {}
    t_full = None
    marks = {252: None, 504: None, 756: None}
    for j, _, h, k, x in q:
        for m in marks:
            if marks[m] is None and j - q[0][0] >= m:
                marks[m] = cash - CASH0
        if k == "reward":
            cash += x / 100 * cur[h]
        else:
            size = size_for(policy, cash)
            cur[h] = size
            cash -= FEE[size]; fees += FEE[size]
            low = min(low, cash)
            if t_full is None and len(cur) == 3 and all(v == 100_000 for v in cur.values()):
                t_full = j - q[0][0]
    for m in marks:
        marks[m] = cash - CASH0 if marks[m] is None else marks[m]
    return dict(nuits_jusqu_a_3x100k=t_full, net_1an=marks[252], net_2ans=marks[504], net_3ans=marks[756],
                apport_max=max(0.0, -low), frais=fees, tréso_min=low)


def main() -> None:
    starts = np.arange(0, NT - H, STEP)
    rows = []
    for s0 in starts:
        evs = {h: slot_events(h, s0) for h in HOURS}
        for policy in ("paliers", "direct", "direct agressif"):
            rows.append(dict(start=R.index[s0].date(), politique=policy, **path(policy, evs)))
    P = pd.DataFrame(rows)
    P.to_csv(OUT / "paths.csv", index=False)
    say(f"Chemin du plan FTMO (trio 19h/20h/21h), départ avec {CASH0:,.0f} $, {len(starts)} départs de {P.start.min()} à {P.start.max()}, horizon 3 ans".replace(",", " "))
    for policy, g in P.groupby("politique", sort=False):
        t = g.nuits_jusqu_a_3x100k
        reached = t.notna().mean()
        say(f"\n=== {policy} ===")
        say(f"  3 comptes en 100k atteints dans les 3 ans : {reached:.0%} des départs ; délai médian {t.median():.0f} nuits "
            f"(~{t.median() / 21:.0f} mois), 75e centile {t.quantile(0.75):.0f}, pire {t.max():.0f}")
        for c, lab in (("net_1an", "gain net à 1 an"), ("net_2ans", "à 2 ans"), ("net_3ans", "à 3 ans")):
            say(f"  {lab:<16} : médiane {g[c].median():+,.0f} $, 5e centile {g[c].quantile(0.05):+,.0f} $, pire {g[c].min():+,.0f} $".replace(",", " "))
        say(f"  apport personnel en plus des {CASH0:,.0f} $ : nul dans {(g.apport_max == 0).mean():.0%} des départs, "
            f"95e centile {g.apport_max.quantile(0.95):,.0f} $, pire {g.apport_max.max():,.0f} $ ; frais sur 3 ans médiane {g.frais.median():,.0f} $".replace(",", " "))
    W = P.pivot(index="start", columns="politique", values=["nuits_jusqu_a_3x100k", "net_3ans"])
    for pol in ("direct", "direct agressif"):
        t_d, t_p = W[("nuits_jusqu_a_3x100k", pol)], W[("nuits_jusqu_a_3x100k", "paliers")]
        faster = ((t_d < t_p) | (t_d.notna() & t_p.isna())).mean()
        richer = (W[("net_3ans", pol)] > W[("net_3ans", "paliers")]).mean()
        say(f"\nMême départ, {pol} contre paliers : 3 × 100k atteints plus tôt dans {faster:.0%} des cas ; "
            f"gain à 3 ans plus élevé dans {richer:.0%} des cas")


if __name__ == "__main__":
    main()
