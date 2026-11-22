"""FTMO 1-Step : plan retenu avec le compte B séparé en deux (B1 = 3n seul, B2 = M2 EMA 9:30 seul), avec et sans un
compte C = BB. EXPLORATOIRE, hors compteur, comme run_ftmo_bb_options.py (même moteur, mêmes trades, mêmes réglages :
éval 2,5 %, financé 1 %, objectif 2 R, règle des annonces, cible + attente, 10k, 494 départs 2016-01 → 2025-08, 12 mois).
Demande de l'utilisateur (2026-11-22). Le bot n'est pas modifié.

uv run python run_ftmo_4comptes.py → results/ftmo_4comptes/ (run.log, departs.csv)

Configurations :
  2 comptes : A = mom, B = 3n + M2 (plan actuel ; M2 seulement si 3n n'a touché ni SL ni TP, journée bornée −r / +2 r) ;
  3 comptes : A, B, C = BB (option 2) ;
  3 comptes séparés : A, B1 = 3n seul, B2 = M2 seul (M2 tous ses jours de signal, taille pleine) ;
  4 comptes : A, B1, B2, C = BB.
Anti-hedging (FTMO interdit des positions opposées sur deux comptes) :
  - mom (A) short une nuit → pas de 3n long (B ou B1) : règle existante ;
  - BB (C) : pas de BB un jour où le M2 a un signal de sens opposé (que M2 soit pris ou non) : règle de run_ftmo_bb_options ;
  - pas de chevauchement dans le temps entre mom (20:00 → 9:30), 3n (20:05 → 03:00), M2 (9:35 → 15:55) et BB (≥ 10:00),
    sauf M2 / BB, couvert ci-dessus. L'exposition cumulée de même sens (deux comptes longs NQ au même moment) n'est pas
    limitée : la règle FTMO est floue (question posée au support).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as D
from run_ftmo_bb_options import jambes_C, jours_bb, trades_bb

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/ftmo_4comptes")
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def jambes_seule(strat):
    def g(row):
        def f(base, r):
            x = row.get(strat)
            return [] if x is None else [(*x, base)]
        return f
    return g


CONFIGS = {
    "2 comptes : A mom, B 3n + M2 (plan)": {"A": D.jambes_A, "B": D.jambes_B},
    "3 comptes : A, B, C = BB (option 2)": {"A": D.jambes_A, "B": D.jambes_B, "C": jambes_C},
    "3 comptes : A, B1 = 3n, B2 = M2": {"A": D.jambes_A, "B1": jambes_seule("3n"), "B2": jambes_seule("M2")},
    "4 comptes : A, B1 = 3n, B2 = M2, C = BB": {"A": D.jambes_A, "B1": jambes_seule("3n"), "B2": jambes_seule("M2"),
                                                "C": jambes_C},
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    bb = trades_bb()
    lib = D.bibliotheque()
    lib = lib[lib.date <= "2026-08-28"]
    jours = jours_bb(lib, bb)
    dates = pd.DatetimeIndex([d for d, _ in jours])
    H = 252
    i0s = range(int(np.searchsorted(dates, pd.Timestamp("2016-01-04"))), int(np.searchsorted(dates, pd.Timestamp("2026-08-29"))) - H, 5)
    rows = []
    for nom, cfg in CONFIGS.items():
        for i0 in i0s:
            C = {k: D.Compte(k, False, True, "cible+attente") for k in cfg}
            tot = []
            for d, row in jours[i0:i0 + H]:
                for k, f in cfg.items():
                    C[k].jour(d, f(row))
                tot.append(sum(c.cash for c in C.values()))
            tot = np.array(tot)
            r = dict(config=nom, départ=dates[i0].date(), net_total=tot[-1], creux=min(0.0, tot.min()),
                     évals=sum(c.evals for c in C.values()), rewards=sum(c.rewards for c in C.values()))
            for k, c in C.items():
                r[f"net_{k}"], r[f"évals_{k}"], r[f"rewards_{k}"] = c.cash, c.evals, c.rewards
            rows.append(r)
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "departs.csv", index=False)
    say(f"{R.départ.nunique()} départs (2016-01 → 2025-08), 12 mois, comptes 10k, règle des annonces + cible + attente")
    for nom, g in R.groupby("config", sort=False):
        say(f"\n  {nom}")
        say(f"    total : moy. {g.net_total.mean():+,.0f} $, méd. {g.net_total.median():+,.0f} $, 10e c. {g.net_total.quantile(.1):+,.0f} $, "
            f"pire départ {g.net_total.min():+,.0f} $ ; évals/an {g.évals.mean():.1f}, rewards/an {g.rewards.mean():.1f} ; "
            f"pire creux de trésorerie méd. {g.creux.median():,.0f} $, pire {g.creux.min():,.0f} $")
        for k in CONFIGS[nom]:
            s = g[f"net_{k}"]
            say(f"    {k:<3}: moy. {s.mean():+,.0f} $, 10e c. {s.quantile(.1):+,.0f} $, P(< 0) {100 * (s < 0).mean():.0f} %, "
                f"évals/an {g[f'évals_{k}'].mean():.1f}, rewards/an {g[f'rewards_{k}'].mean():.1f}")
        nets = g[[f"net_{k}" for k in CONFIGS[nom]]]
        if nets.shape[1] > 1:
            say("    corrélations des nets entre départs :\n" + nets.corr().round(2).to_string())
    par = R.assign(année=pd.to_datetime(R.départ).dt.year).pivot_table(index="année", columns="config", values="net_total",
                                                                        aggfunc="mean").round(0)[list(CONFIGS)]
    say(f"\nNet total moyen sur 12 mois selon l'année de départ ($) :\n{par.to_string()}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
