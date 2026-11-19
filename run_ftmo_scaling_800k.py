"""Montée en taille FTMO prolongée jusqu'à 800k (4 x 100k par stratégie) — simulation hypothétique demandée le
2026-11-05 (FTMO plafonne aujourd'hui à 400k hors plan de scaling). EXPLORATOIRE, hors compteur.

uv run python run_ftmo_scaling_800k.py [N] → results/ftmo_scaling_800k/ (run.log, metriques_<simulation>.csv)

Mêmes règles que run_ftmo_scaling.py (A = mom, B = 3n + M2, annonces + cible + attente, anti-hedging ; réserve de
10 évals par paire A + B) avec deux paliers de plus :
  6 : 3 x 100k par stratégie (600k, réserve 16 467 $)    7 : 4 x 100k par stratégie (800k, réserve 21 956 $)
Mesures : délai de chaque palier, cagnotte, revenu mensuel une fois à 400k (palier 5) et à 800k (palier 7), plus bas
et max DD de la cagnotte, ruine (cagnotte qui ne paie plus une éval 10k). Mois = 21 séances.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as M
import run_ftmo_monte_carlo as MC
import run_ftmo_scaling as S
import run_ftmo_scaling_metrics as SM

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000
OUT = Path("results/ftmo_scaling_800k")
S.PALIERS = S.PALIERS + [{10_000: 0, 100_000: 3}, {10_000: 0, 100_000: 4}]
H = 1260
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def revenus(traj, t0):
    if t0 is None or len(traj) - t0 < 42:
        return {}
    seg = traj[t0:]
    f = np.diff(seg[::21])
    return dict(moy=f.mean(), med=np.median(f), neg=100 * (f < 0).mean(), pire=f.min())


def metriques(g, traj):
    Hh = len(traj)
    r = {f"palier_{k}_mois": (g.dates[k] / 21 if k in g.dates else np.nan) for k in range(2, 8)}
    for m in (12, 24, 36, 60):
        r[f"cagnotte_{m}m"] = traj[min(21 * m, Hh) - 1]
    x = np.r_[S.DEPOT, traj]
    r |= dict(min_cagnotte=traj.min(), max_dd=float((x - np.maximum.accumulate(x)).min()),
              ruine=bool(traj.min() < S.PRIX[10_000]), excedent_fin=g.excedent(),
              frais=g.st["frais_10k"] + g.st["frais_100k"], finances_perdus_100k=g.st["finances_perdus_100k"],
              evals_100k=g.st["evals_100k"])
    for k, nom in ((5, "400k"), (7, "800k")):
        for a, v in revenus(traj, g.dates.get(k)).items():
            r[f"rev_{nom}_{a}"] = v
    return r


def resume(nom, rows):
    D = pd.DataFrame(rows)
    D.to_csv(OUT / f"metriques_{nom}.csv", index=False)
    say(f"\n===== {nom} : {len(D)} chemins de {H} séances (5 ans) =====")
    for k, lab in ((5, "400k"), (6, "600k"), (7, "800k")):
        s = D[f"palier_{k}_mois"]
        say(f"  {lab} atteint dans {100 * s.notna().mean():.1f} % des chemins ; délai médian {s.median():.1f} mois "
            f"(10e c. {s.quantile(.1):.1f}, 90e c. {s.quantile(.9):.1f})")
    for m in (12, 24, 36, 60):
        s = D[f"cagnotte_{m}m"]
        say(f"  cagnotte à {m} mois : médiane {s.median():+,.0f} $ ; 10e c. {s.quantile(.1):+,.0f} $ ; "
            f"90e c. {s.quantile(.9):+,.0f} $")
    for lab in ("400k", "800k"):
        c = f"rev_{lab}_moy"
        if c in D:
            s = D[c].dropna()
            say(f"  revenu mensuel moyen une fois à {lab} : médiane {s.median():,.0f} $ (10e c. {s.quantile(.1):,.0f}, "
                f"90e c. {s.quantile(.9):,.0f}) ; mois négatifs {D[f'rev_{lab}_neg'].median():.0f} % ; "
                f"pire mois (médiane des chemins) {D[f'rev_{lab}_pire'].median():,.0f} $")
    say(f"  max DD de cagnotte : médiane {D.max_dd.median():,.0f} $, 10e c. {D.max_dd.quantile(.1):,.0f} $, "
        f"pire {D.max_dd.min():,.0f} $ ; ruine {100 * D.ruine.mean():.1f} % ; comptes 100k financés perdus sur 5 ans "
        f"(médiane) {D.finances_perdus_100k.median():.0f} ; évals 100k achetées {D.evals_100k.median():.0f}")
    return D


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    say("Réserves par palier : " + ", ".join(f"{k + 1} : {S.reserve(k):,.0f} $" for k in range(len(S.PALIERS))))
    lib = M.bibliotheque()
    jours = M.tableau(lib)
    dates = pd.DatetimeIndex([d for d, _ in jours])
    g, traj = SM.joue(jours, np.arange(len(jours)), calendaire=True)
    say(f"\n===== Vrai chemin {dates[0]:%Y-%m-%d} → {dates[-1]:%Y-%m-%d} =====")
    for d, e in g.events:
        if e.startswith("palier"):
            say(f"  {d:%Y-%m-%d} {e}")
    cag = pd.Series(traj, index=dates)
    an = cag.resample("YE").last()
    say("  cagnotte fin d'année ($) : " + ", ".join(f"{y.year} {v:,.0f}" for y, v in an.items()))
    t7 = g.dates.get(7)
    if t7 is not None:
        fl = cag.resample("ME").last().diff().dropna()
        fl = fl[fl.index >= dates[t7]]
        say(f"  revenu mensuel une fois à 800k : moyenne {fl.mean():,.0f} $, médiane {fl.median():,.0f} $, "
            f"mois négatifs {100 * (fl < 0).mean():.0f} %, pire {fl.min():,.0f} $ ({fl.idxmin():%Y-%m})")
    rows = []
    fin = int(np.searchsorted(dates, pd.Timestamp("2026-08-29")))
    for i0 in range(0, fin - H, 20):
        rows.append(dict(départ=dates[i0].date(), **metriques(*SM.joue(jours, np.arange(i0, i0 + H)))))
    resume("glissants", rows)
    for nom, src in (("mc_historique", jours), ("mc_edge_2", M.tableau(MC.decale(lib, 0.5)))):
        rng = np.random.default_rng(MC.SEED)
        MC.H = H
        resume(nom, [metriques(*SM.joue(src, MC.indices(len(src), rng))) for _ in range(N)])
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
