"""ORB 30 minutes de Subhani, objectif 2R, NQ, lundi à jeudi : trois conditions C1-C3. Étape 1, suite.

Fiche : wiki/experiments/orb30-jours-semaine.md (section « Lundi-jeudi : conditions C1-C3 »). Grille figée ici et
commitée AVANT tout calcul. Règle et données identiques à run_orb30_tp.py (commit 4d51084), objectif 2R.

DONNÉES : NQ, exploration 2016-01-01 → 2026-08-28 seulement (réserve 2010-06 → 2015-12 non lue).

BASE (B) : range 9:30-9:59 (1 R = W), entrée à la première cassure dès 10:00, stop fixe à 1 W, objectif 2 W, sinon
16:00 ; 1 contrat, coût 0,50 pt ; jours = lundi, mardi, mercredi, jeudi regroupés.

CONDITIONS (3 essais, seuils fixés ici)
- C1 range étroit : W < 0,5 × ATR14, ATR14 = moyenne des amplitudes 9:30-16:00 des 14 séances précédentes.
- C2 veille comprimée (NR7, Crabel) : l'amplitude 9:30-16:00 de la séance précédente est ≤ à celle de chacune des
  6 séances qui la précèdent (plus petite des 7 dernières séances).
- C3 annonce pendant la séance : jour présent dans config/calendrier_macro_us.csv avec une annonce à 10:00 ou 14:00
  (ISM, JOLTS, FOMC décision, FOMC minutes) ; on ne trade QUE ces jours.

MESURE ET BARRIÈRE
- Pour chaque condition : fiche des jours pris (R net). Référence = jours exclus de B (écart, t de Welch).
- Rapporté aussi en points nets (C1 a W au dénominateur : effet mécanique possible sur le R).
- Choix : meilleur Sharpe net par trade parmi C1-C3 ; n_famille = 60 (57 + 3) ; variance des Sharpe : 30 cases déjà
  calculées (results/orb30_jours, results/orb30_tp) + les 3.

Compteur global : 2 055 → 2 058 (3 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from fab.protocole import barriere_exploration, fiche, imprimer
from run_orb30_jours import FERME, OPEN, matrices
from run_orb30_tp import trades

OUT = Path("results/orb30_filtres")
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    M = matrices("NQ")
    H, L = M["high"], M["low"]
    sess = list(range(OPEN, FERME))
    amp = H[sess].max(axis=1) - L[sess].min(axis=1)
    atr = amp.rolling(14, min_periods=14).mean().shift(1)
    prev = amp.shift(1)
    nr7 = prev <= amp.shift(2).rolling(6, min_periods=6).min()
    t = trades("NQ", M, 2.0)
    t = t[t.jour <= 3].copy()
    t["atr"], t["nr7"] = atr.reindex(t.index), nr7.reindex(t.index)
    t = t[t.atr.notna() & prev.reindex(t.index).notna()]
    cal = pd.read_csv("config/calendrier_macro_us.csv")
    ann = set(pd.to_datetime(cal[cal.heure_ET.isin(["10:00", "14:00"])].date))
    conds = {
        "C1 range étroit (W < 0,5 ATR14)": (t.W < 0.5 * t.atr).values,
        "C2 veille NR7": t.nr7.astype(bool).values,
        "C3 annonce à 10:00 ou 14:00": t.index.isin(ann),
    }
    g1 = pd.read_csv("results/orb30_jours/grille.csv")
    g2 = pd.read_csv("results/orb30_tp/grille.csv")
    fam = list(g1.sharpe_an / np.sqrt(252)) + list(g2.sharpe_an / np.sqrt(252))
    sh3 = [t.net_R[m].mean() / t.net_R[m].std() for m in conds.values()]
    fam += sh3
    say(f"Base B (NQ, lun-jeu, objectif 2R) : {len(t)} trades, net {t.net_R.mean():+.3f} R ({t.net_pts.mean():+.2f} pts), "
        f"t {t.net_R.mean() / t.net_R.std() * np.sqrt(len(t)):.2f} ; famille {len(fam)} Sharpe, N = 60")
    rows, fiches = [], {}
    for nom, m in conds.items():
        m = np.asarray(m)
        x, r = t.net_R[m], t.net_R[~m]
        f = fiche(x, None, None, n_famille=60, sharpes_famille=fam, tick_bp=0.25 / t.W[m])
        w = stats.ttest_ind(x, r, equal_var=False)
        wp = stats.ttest_ind(t.net_pts[m], t.net_pts[~m], equal_var=False)
        f["ref_net_moy"], f["ecart_ref"], f["t_ecart_ref"] = float(r.mean()), float(x.mean() - r.mean()), float(w.statistic)
        fiches[nom] = f
        y = x.index.year
        rows.append({"condition": nom, "pris": len(x), "exclus": len(r), "net_R_pris": x.mean(), "net_R_exclus": r.mean(),
                     "t_ecart_R": w.statistic, "t_nw_pris": f["t_nw"], "sharpe_trade": x.mean() / x.std(),
                     "pts_pris": t.net_pts[m].mean(), "pts_exclus": t.net_pts[~m].mean(), "t_ecart_pts": wp.statistic,
                     "objectif_%": 100 * (t.sortie[m] == "objectif").mean(), "2016-22": x[y <= 2022].mean(),
                     "2023-26": x[y >= 2023].mean(), "annees_pos": f["annees_pos"], "dsr_60": f["dsr_famille"]})
        say(f"\n{nom} — par jour (R net pris / exclus) :")
        say(pd.DataFrame({"pris": x.groupby(x.index.dayofweek).mean(), "exclus": r.groupby(r.index.dayofweek).mean(),
                          "n_pris": x.groupby(x.index.dayofweek).size()}).rename(index={0: "lun", 1: "mar", 2: "mer", 3: "jeu"})
            .round(3).to_string())
        say("par année (R net pris) : " + " · ".join(f"{a} {v:+.2f}" for a, v in x.groupby(y).mean().items()))
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "conditions.csv", index=False)
    say("\n===== Conditions (NQ, lundi-jeudi, objectif 2R) =====")
    say(tab.round(3).to_string(index=False))
    best = tab.sort_values("sharpe_trade", ascending=False).iloc[0].condition
    f = fiches[best]
    say("\n" + imprimer(f, f"Condition choisie (meilleur Sharpe net) : {best}"))
    okb, raisons = barriere_exploration(f)
    say("B1 : " + ("✅ franchie" if okb else "❌ ratée"))
    for r in raisons:
        say("  " + r)
    out = t[["jour", "W", "atr", "net_R", "net_pts", "sortie"]].copy()
    for k, v in conds.items():
        out[k.split(" ")[0]] = np.asarray(v)
    out.to_csv(OUT / "trades.csv")
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
