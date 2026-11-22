"""BB (bande de bruit) sur NQ, UN trade par jour, avec SL et TP. Exploration, et bibliothèques de trades pour la prop firm.

Fiche : wiki/experiments/m2-bande-bruit-nq.md (section « BB un trade par jour »). Grille figée ici et commitée AVANT
tout calcul. Exploration sur données déjà vues (NQ 2016-01 → 2026-08-28) ; aucune réserve, aucun verdict.
Demande de l'utilisateur (2026-11-22) : approche prop firm par convexité (risque élevé en éval), un trade par jour.

RÈGLE : celle de run_bb_sltp.py (commit b217c32 ; BB avec VWAP exigé à l'entrée, SL = k × ATR14, TP = RR × SL,
modes A et B), en ne gardant que le PREMIER trade de chaque séance. C'est exactement « un trade par jour » : le premier
trade ne dépend pas des suivants (ils n'ont lieu qu'après sa sortie).

GRILLE (18 essais) : mode {A, B} × k {0,25 ; 0,5 ; 1,0} × RR {1, 2, 3}.
MESURES (1 contrat, coût standard 0,50 pt) : trades, R net (1 R = k × ATR14), gagnants, sorties, R par an, pire creux en
R, pertes consécutives, P&L $, Sharpe journalier ; 2016-2022 / 2023-2026. Référence (non comptée) : les mêmes cases sans
limite (run_bb_sltp.py).
SORTIE POUR LA PROP FIRM : results/bb_1j/trades_<mode>_<k>_<RR>.csv avec date, R_brut (sans coût), s = k × ATR14 /
prix d'entrée (taille du stop en fraction du prix), sortie. Le coût CFD est ajouté par le simulateur FTMO.

Compteur global : 2 109 → 2 127 (18 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from run_bb_sltp import prepare, simulate

OUT = Path("results/bb_1j")
KS, RRS = [0.25, 0.5, 1.0], [1, 2, 3]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def runs(x) -> int:
    m = c = 0
    for v in x:
        c = c + 1 if v <= 0 else 0
        m = max(m, c)
    return m


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    P = prepare()
    a, g, atr = P[0], P[1], P[8]
    dates = g.dates
    yrs = len(dates) / 252
    rows = []
    for mode in ("A", "B"):
        for k in KS:
            for rr in RRS:
                full = simulate(P, mode, k, rr)
                t = full.sort_values(["date", "m_in"]).groupby("date", as_index=False).first()
                dist = k * atr.reindex(pd.to_datetime(t.date)).values
                t["dist"] = dist
                t["R_brut"] = t.dir * (t.p_out - t.p_in) / dist
                t["R_net"] = t.net_pts / dist
                t["s"] = dist / t.p_in
                t[["date", "R_brut", "s", "sortie", "dir", "m_in"]].to_csv(OUT / f"trades_{mode}_{k}_{rr}.csv", index=False)
                d = t.set_index(pd.to_datetime(t.date)).net_pts.reindex(dates).fillna(0.0)
                dR = t.set_index(pd.to_datetime(t.date)).R_net.reindex(dates).fillna(0.0)
                eqR = dR.cumsum()
                y = dates.year
                rows.append({"mode": mode, "k_ATR": k, "RR": rr, "trades": len(t), "trades_an": len(t) / yrs,
                             "R_net_moyen": t.R_net.mean(), "t_R": t.R_net.mean() / t.R_net.std() * np.sqrt(len(t)),
                             "gagnants_%": 100 * (t.R_net > 0).mean(), "SL_%": 100 * (t.sortie == "SL").mean(),
                             "TP_%": 100 * (t.sortie == "TP").mean(), "suiveur_%": 100 * (t.sortie == "suiveur").mean(),
                             "R_par_an": t.R_net.sum() / yrs, "pire_creux_R": (eqR - eqR.cummax()).min(),
                             "pertes_consec": runs(t.R_net.values), "$_an": d.sum() * 20 / yrs,
                             "sharpe_jour": d.mean() / d.std() * np.sqrt(252),
                             "R_2016-22": t.R_net[pd.to_datetime(t.date).dt.year <= 2022].mean(),
                             "R_2023-26": t.R_net[pd.to_datetime(t.date).dt.year >= 2023].mean(),
                             "trades_sans_limite": len(full)})
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "grille.csv", index=False)
    say("===== BB NQ, un trade par jour, SL / TP (1 contrat, net de 0,50 pt ; 1 R = k × ATR14) =====")
    say(tab.round(3).to_string(index=False))
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
