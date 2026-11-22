"""ORB 30 minutes NQ, lundi à jeudi, objectif 2R : forme de la cassure (clôture au-delà de la borne), heure de la
cassure, et ordres limite sur les bords du range. Étape 1, suite.

Fiche : wiki/experiments/orb30-jours-semaine.md (section « Lundi-jeudi : forme et heure de la cassure, ordres limite »).
Demande de l'utilisateur (2026-11-22). Grille figée ici et commitée AVANT tout calcul.

DONNÉES : NQ Databento 1 min, exploration 2016-01-01 → 2026-08-28 seulement (réserve 2010-06 → 2015-12 non lue).
Trades du 2016-06-01 au 2026-08-28, lundi à jeudi.

COMMUN : range 9:30-9:59 (ORhi, ORlo, W). Stop fixe à 1 W de l'entrée, objectif 2 × W (2R), sinon sortie à l'open de
la 1ʳᵉ barre dans [16:00, 16:05). Stop et objectif surveillés dès la barre d'entrée, stop prioritaire. Un trade par
jour. 1 contrat, coût 0,50 pt. R = résultat net / W.

GRILLE (6 essais)
- K1 « clôture 1 min » : première barre 1 min, dès 10:00, qui CLÔTURE au-dessus de ORhi (achat) ou sous ORlo
  (vente) ; entrée à l'open de la barre suivante (convention du dépôt : décision à la clôture, exécution à l'open qui
  suit).
- K5 « clôture 5 min » : bougies 5 min 10:00-10:05, 10:05-10:10, … construites sur les barres 1 min ; première bougie
  dont la clôture est au-delà d'une borne ; entrée à l'open de la barre 1 min qui suit la fin de cette bougie.
- H1, H2, H3 « heure de la cassure » : ORB de Subhani (ordre stop sur la borne, première barre qui la dépasse, la
  clôture tranche si les deux) ; on ne garde le trade que si la barre d'entrée commence dans [10:00, 11:00) pour H1,
  [11:00, 13:00) pour H2, [13:00, 16:00) pour H3.
- L « ordres limite sur les bords » : dès 10:00, vente limite à ORhi (remplie si le plus haut ≥ ORhi + 1 tick) et achat
  limite à ORlo (rempli si le plus bas ≤ ORlo − 1 tick) ; prix = la borne, ou l'open si la barre ouvre au-delà ; le
  premier rempli gagne ; si les deux le sont dans la même barre, pas de trade.

RÉFÉRENCE (non comptée) : ORB de Subhani objectif 2R, lundi-jeudi, toutes heures (+0,015 R au calcul précédent).
- H1-H3 : trades de la tranche contre les autres trades de l'ORB (t de Welch, en R).
- K1, K5, L : écart par jour en points nets avec la référence (0 si pas de trade), t de Newey-West.
CHOIX ET BARRIÈRE : meilleur Sharpe net par trade (R) parmi les 6 ; n_famille = 81 (75 + 6) ; variance des Sharpe :
les 48 cases déjà calculées + les 6. Fiche et B1 : fab.protocole.

Compteur global : 2 073 → 2 079 (6 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from fab.protocole import barriere_exploration, fiche, imprimer, nw_t
from run_orb30_jours import FERME, FIN_RANGE, OPEN, matrices
from run_orb30_rsi import cassure, sortie

DEBUT_TRADES = pd.Timestamp("2016-06-01")
OUT = Path("results/orb30_forme")
TICK, COUT = 0.25, 0.50
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def cloture(hh, ll, oo, cc, h0, l0, k):
    """Première bougie de k minutes (dès 10:00) clôturant au-delà d'une borne ; entrée à l'open de la barre suivante."""
    n = len(cc)
    for s in range(0, n - k, k):
        c = cc[s:s + k]
        c = c[np.isfinite(c)]
        if not c.size:
            continue
        last = c[-1]
        side = 1 if last > h0 else (-1 if last < l0 else 0)
        if side:
            j = s + k
            while j < n and not np.isfinite(oo[j]):
                j += 1
            if j >= n:
                return None
            return j, side, oo[j]
    return None


def limites(hh, ll, oo, h0, l0):
    for j in range(len(hh)):
        if not np.isfinite(hh[j]):
            continue
        a, b = hh[j] >= h0 + TICK, ll[j] <= l0 - TICK
        if a and b:
            return None
        if a:
            o_j = oo[j] if np.isfinite(oo[j]) else h0
            return j, -1, max(h0, o_j)
        if b:
            o_j = oo[j] if np.isfinite(oo[j]) else l0
            return j, 1, min(l0, o_j)
    return None


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    M = matrices("NQ")
    O, H, L, C = M["open"], M["high"], M["low"], M["close"]
    rng = list(range(OPEN, FIN_RANGE))
    hi, lo = H[rng].max(axis=1), L[rng].min(axis=1)
    end = O[list(range(FERME, FERME + 5))].bfill(axis=1).iloc[:, 0]
    post = list(range(FIN_RANGE, FERME))
    Hp, Lp, Op, Cp = H[post].values, L[post].values, O[post].values, C[post].values
    regles = {"ORB": lambda i, h0, l0: cassure(Hp[i], Lp[i], Op[i], Cp[i], h0, l0),
              "K1": lambda i, h0, l0: cloture(Hp[i], Lp[i], Op[i], Cp[i], h0, l0, 1),
              "K5": lambda i, h0, l0: cloture(Hp[i], Lp[i], Op[i], Cp[i], h0, l0, 5),
              "L": lambda i, h0, l0: limites(Hp[i], Lp[i], Op[i], h0, l0)}
    rows = []
    jours = []
    for i, d in enumerate(O.index):
        if d < DEBUT_TRADES or d.dayofweek > 3:
            continue
        h0, l0, pe_end = hi.iat[i], lo.iat[i], end.iat[i]
        if not (np.isfinite(h0) and np.isfinite(l0) and np.isfinite(pe_end)) or h0 - l0 <= 0:
            continue
        jours.append(d)
        W = h0 - l0
        for nom, fn in regles.items():
            e = fn(i, h0, l0)
            if e is None:
                continue
            j, side, pe = e
            px, so = sortie(Hp[i], Lp[i], Op[i], j, side, pe, W, pe_end)
            net = side * (px - pe) - COUT
            rows.append({"date": d, "regle": nom, "side": side, "W": W, "minute": FIN_RANGE + j, "p_in": pe, "p_out": px,
                         "sortie": so, "net_pts": net, "net_R": net / W})
    T = pd.DataFrame(rows).set_index("date")
    jours = pd.DatetimeIndex(jours)
    orb = T[T.regle == "ORB"]
    base_d = orb.net_pts.reindex(jours).fillna(0.0)
    tranches = {"H1": (600, 660), "H2": (660, 780), "H3": (780, 960)}
    X = {"K1": T[T.regle == "K1"], "K5": T[T.regle == "K5"], "L": T[T.regle == "L"]}
    for h, (a, b) in tranches.items():
        X[h] = orb[(orb.minute >= a) & (orb.minute < b)]
    g = [pd.read_csv(f) for f in ["results/orb30_jours/grille.csv", "results/orb30_tp/grille.csv"]]
    fam = list(g[0].sharpe_an / np.sqrt(252)) + list(g[1].sharpe_an / np.sqrt(252))
    fam += list(pd.read_csv("results/orb30_filtres/conditions.csv").sharpe_trade)
    fam += list(pd.read_csv("results/orb30_biais/grille.csv").sharpe_trade)
    fam += list(pd.read_csv("results/orb30_rsi/grille.csv").sharpe_trade)
    fam += [x.net_R.mean() / x.net_R.std() for x in X.values()]
    say(f"Lundis-jeudis : {len(jours)} ; référence ORB objectif 2R : {len(orb)} trades, {orb.net_R.mean():+.3f} R, "
        f"{base_d.mean():+.2f} pts par jour ; famille {len(fam)} Sharpe, N = 81")
    rows, fiches = [], {}
    for nom, x in X.items():
        f = fiche(x.net_R, None, None, n_famille=81, sharpes_famille=fam, tick_bp=TICK / x.W)
        if nom.startswith("H"):
            autre = orb.net_R[~orb.index.isin(x.index)]
            w = stats.ttest_ind(x.net_R, autre, equal_var=False)
            f["ref_net_moy"], f["ecart_ref"], f["t_ecart_ref"] = float(autre.mean()), float(x.net_R.mean() - autre.mean()), float(w.statistic)
        else:
            diff = x.net_pts.reindex(jours).fillna(0.0) - base_d
            f["ref_net_moy"], f["ecart_ref"], f["t_ecart_ref"] = float(base_d.mean()), float(diff.mean()), nw_t(diff.values)
        fiches[nom] = f
        y = x.index.year
        rows.append({"regle": nom, "n": len(x), "net_R": x.net_R.mean(), "t_nw": f["t_nw"], "sharpe_trade": x.net_R.mean() / x.net_R.std(),
                     "gagnants_%": f["gagnants_%"], "net_pts": x.net_pts.mean(), "ref": f["ref_net_moy"], "ecart_ref": f["ecart_ref"],
                     "t_ecart_ref": f["t_ecart_ref"], "stop_%": 100 * (x.sortie == "stop").mean(),
                     "objectif_%": 100 * (x.sortie == "objectif").mean(), "2016-22": x.net_R[y <= 2022].mean(),
                     "2023-26": x.net_R[y >= 2023].mean(), "annees_pos": f["annees_pos"], "dsr_81": f["dsr_famille"]})
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "grille.csv", index=False)
    say("\n===== Forme, heure de la cassure, ordres limite (NQ, lundi-jeudi, objectif 2R) =====")
    say(tab.round(3).to_string(index=False))
    say("\nPar jour (R net) :\n" + T.assign(j=T.index.dayofweek).pivot_table(index="regle", columns="j", values="net_R", aggfunc="mean")
        .rename(columns={0: "lun", 1: "mar", 2: "mer", 3: "jeu"}).round(3).to_string())
    best = tab.sort_values("sharpe_trade", ascending=False).iloc[0].regle
    say("\n" + imprimer(fiches[best], f"Règle choisie (meilleur Sharpe net) : {best}"))
    okb, raisons = barriere_exploration(fiches[best])
    say("B1 : " + ("✅ franchie" if okb else "❌ ratée"))
    for r in raisons:
        say("  " + r)
    T.to_csv(OUT / "trades.csv")
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
