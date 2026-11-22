"""Pré-enregistrement n° 31 : ORB 30 minutes de Subhani le vendredi sur NQ, réserve 2010-06-08 → 2015-12-31.
Une seule exécution. Règles, référence, critères : PREREGISTRATION_31.md. Les fonctions de trading sont celles,
figées, de run_orb30_jours.py (règle A) et run_orb30_tp.py (règle B) ; seules les données changent.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import run_orb30_jours as RJ
from fab.core import NY
from fab.protocole import fiche, holm, imprimer, verdict_confirmation
from run_orb30_jours import FERME, OPEN
from run_orb30_tp import trades as trades_tp

DEBUT, FIN = pd.Timestamp("2010-06-08"), pd.Timestamp("2015-12-31")
OUT = Path("results/prereg31")
JOURS = {0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi", 4: "vendredi"}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def matrices_reserve(name: str) -> dict[str, pd.DataFrame]:
    df = pd.read_parquet(f"cache/databento_2010/{name}_v0_1m_2010.parquet")[["open", "high", "low", "close"]]
    df = df[~df.index.duplicated()].sort_index()
    loc = df.tz_convert(NY)
    m = loc.index.hour * 60 + loc.index.minute
    keep = (m >= OPEN) & (m < FERME + 5) & (loc.index.dayofweek < 5)
    loc = loc[keep]
    loc = loc.assign(d=loc.index.tz_localize(None).normalize(), m=m[keep])
    loc = loc[(loc.d >= DEBUT) & (loc.d <= FIN)]
    cols = range(OPEN, FERME + 5)
    return {c: loc.pivot(index="d", columns="m", values=c).reindex(columns=cols) for c in ["open", "high", "low", "close"]}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 220)
    RJ.matrices = matrices_reserve  # mêmes règles, données de la réserve
    A = RJ.trades("NQ")
    B = trades_tp("NQ", matrices_reserve("NQ"), 2.0)
    say(f"Réserve NQ : {A.index.min().date()} → {A.index.max().date()} ; trades A {len(A)}, B {len(B)} ; "
        f"vendredis A {int((A.jour == 4).sum())}, W médian {A.W.median():.2f} pts, coût médian {(0.5 / A.W).median():.4f} R")
    res = {}
    for nom, T in [("A sans objectif", A), ("B objectif 2R", B)]:
        v = T.net_R[T.jour == 4]
        autres = T.net_R[T.jour <= 3]
        f = fiche(v, None, None, n_famille=1, tick_bp=0.25 / T.W[T.jour == 4])
        f["ref_net_moy"], f["ecart_ref"] = float(autres.mean()), float(v.mean() - autres.mean())
        res[nom] = (f, T)
    p_holm = holm([res[k][0]["p_unilateral"] for k in res])
    for (nom, (f, T)), ph in zip(res.items(), p_holm):
        say("\n" + imprimer(f, f"Règle {nom}, vendredis de la réserve (référence C2 = lundis-jeudis, même règle)"))
        ok, raisons = verdict_confirmation(f, p_ajuste=float(ph))
        say(f"  p de Holm (2 règles) : {ph:.4f}")
        for r in raisons:
            say("  " + r)
        say(f"  VERDICT {nom} : {'CONFIRMÉE (hors protocole, B1 non franchie) → étape 4' if ok else 'REJET'}")
        v = T[T.jour == 4]
        say(f"  sorties : stop {100 * (v.sortie == 'stop').mean():.1f} %"
            + (f", objectif {100 * (v.sortie == 'objectif').mean():.1f} %" if "objectif" in set(v.sortie) else "")
            + f" ; net {v.net_pts.mean():+.2f} pts ({v.net_pts.mean() * 20:+.0f} $) par trade")
    say("\nContrôle placebo (règle A, R net par jour de la semaine) :")
    pl = A.groupby(A.jour).net_R.agg(["count", "mean", "std"])
    pl["t"] = pl["mean"] / pl["std"] * np.sqrt(pl["count"])
    say(pl.rename(index=JOURS).round(3).to_string())
    say("\nRègle A, R net par année (vendredi / lundi-jeudi) :")
    say(pd.DataFrame({"vendredi": A[A.jour == 4].groupby(A[A.jour == 4].index.year).net_R.mean(),
                      "lun-jeu": A[A.jour <= 3].groupby(A[A.jour <= 3].index.year).net_R.mean()}).round(3).to_string())
    A.to_csv(OUT / "trades_A.csv")
    B.to_csv(OUT / "trades_B.csv")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
