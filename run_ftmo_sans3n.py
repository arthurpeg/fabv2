"""FTMO 1-Step : remplacer 3n par BB (demande de l'utilisateur, 2026-11-22 : « mom et 3n sont très corrélées »).
EXPLORATOIRE, hors compteur. Même moteur, mêmes trades et mêmes réglages que run_ftmo_4comptes.py (éval 2,5 %, financé
1 %, objectif 2 R, règle des annonces, cible + attente, 10k, 494 départs 2016-01 → 2025-08, 12 mois). Bot non modifié.

uv run python run_ftmo_sans3n.py → results/ftmo_sans3n/ (run.log, departs.csv)

1. Corrélation mom / 3n : R des nuits où les deux tradent, et nets des comptes.
2. Configurations :
   plan        : A = mom, B = 3n + M2 ;
   option 2    : A, B, C = BB ;
   R1          : A = mom, B = M2 puis BB (un trade par jour sur B : M2 s'il a un signal, sinon BB) ;
   R2          : A = mom, B = M2 seul, C = BB (3 comptes, sans 3n) ;
   R3          : A = mom, C = BB (2 comptes, sans 3n ni M2).
Anti-hedging : mom short → pas de 3n long ; pas de BB un jour où M2 a un signal de sens opposé.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as D
from run_ftmo_4comptes import jambes_seule
from run_ftmo_bb_options import _bb_leg, jambes_C, jours_bb, trades_bb

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/ftmo_sans3n")
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def jambes_M2_puis_BB(row):
    def f(base, r):
        x = row.get("M2")
        return [(*x, base)] if x is not None else _bb_leg(row, base, r)
    return f


CONFIGS = {
    "plan : A mom, B 3n + M2": {"A": D.jambes_A, "B": D.jambes_B},
    "option 2 : A, B, C = BB": {"A": D.jambes_A, "B": D.jambes_B, "C": jambes_C},
    "R1 : A mom, B = M2 puis BB": {"A": D.jambes_A, "B": jambes_M2_puis_BB},
    "R2 : A mom, B = M2, C = BB": {"A": D.jambes_A, "B": jambes_seule("M2"), "C": jambes_C},
    "R3 : A mom, C = BB": {"A": D.jambes_A, "C": jambes_C},
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    bb = trades_bb()
    lib = D.bibliotheque()
    lib = lib[lib.date <= "2026-08-28"]
    # 1. corrélation mom / 3n (2016-01 → 2026-08)
    l = lib[lib.date >= "2016-01-01"]
    m, n3, m2 = (l[l.strat == s].groupby("date").R.first() for s in ("mom", "3n", "M2"))
    b = bb.set_index("date").R
    for nom, x in [("3n", n3), ("M2", m2), ("BB", b)]:
        j = pd.concat([m, x], axis=1, join="inner").dropna()
        say(f"mom et {nom} : {len(j)} jours communs, corrélation des R {j.iloc[:, 0].corr(j.iloc[:, 1]):+.2f}")
    j = pd.concat([n3, b], axis=1, join="inner").dropna()
    say(f"3n et BB : {len(j)} jours communs, corrélation des R {j.iloc[:, 0].corr(j.iloc[:, 1]):+.2f}")
    mm = m.reindex(n3.index)
    say(f"Nuits 3n : mom trade aussi {100 * mm.notna().mean():.0f} % de ces nuits ; même sens (mom long) "
        f"{100 * (l[(l.strat == 'mom') & l.date.isin(n3.index)].dir > 0).mean():.0f} %")

    jours = jours_bb(lib, bb)
    dates = pd.DatetimeIndex([d for d, _ in jours])
    H = 252
    i0s = range(int(np.searchsorted(dates, pd.Timestamp("2016-01-04"))),
                int(np.searchsorted(dates, pd.Timestamp("2026-08-29"))) - H, 5)
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
    say(f"\n{R.départ.nunique()} départs (2016-01 → 2025-08), 12 mois, comptes 10k")
    for nom, g in R.groupby("config", sort=False):
        say(f"\n  {nom} ({len(CONFIGS[nom])} comptes)")
        say(f"    total : moy. {g.net_total.mean():+,.0f} $, méd. {g.net_total.median():+,.0f} $, 10e c. "
            f"{g.net_total.quantile(.1):+,.0f} $, pire départ {g.net_total.min():+,.0f} $, P(< 0) {100 * (g.net_total < 0).mean():.1f} % ; "
            f"évals/an {g.évals.mean():.1f}, rewards/an {g.rewards.mean():.1f} ; pire creux {g.creux.min():,.0f} $ ; "
            f"par compte {g.net_total.mean() / len(CONFIGS[nom]):+,.0f} $")
        for k in CONFIGS[nom]:
            s = g[f"net_{k}"]
            say(f"    {k}: moy. {s.mean():+,.0f} $, 10e c. {s.quantile(.1):+,.0f} $, P(< 0) {100 * (s < 0).mean():.0f} %, "
                f"évals/an {g[f'évals_{k}'].mean():.1f}, rewards/an {g[f'rewards_{k}'].mean():.1f}")
        nets = g[[f"net_{k}" for k in CONFIGS[nom]]]
        say("    corrélations des nets : " + ", ".join(f"{a[4:]}/{b[4:]} {nets[a].corr(nets[b]):+.2f}"
                                                   for i, a in enumerate(nets) for b in list(nets)[i + 1:]))
    par = R.assign(année=pd.to_datetime(R.départ).dt.year).pivot_table(index="année", columns="config", values="net_total",
                                                                        aggfunc="mean").round(0)[list(CONFIGS)]
    say(f"\nNet total moyen selon l'année de départ ($) :\n{par.to_string()}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
