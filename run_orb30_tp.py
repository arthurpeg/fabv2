"""ORB 30 minutes de Subhani avec un objectif à 2R ou 3R, sur NQ, ES, YM. Étape 1, suite.

Fiche : wiki/experiments/orb30-jours-semaine.md (section « Objectifs 2R et 3R »). Grille figée ici et commitée AVANT tout
calcul. Règle, données et conventions identiques à run_orb30_jours.py (commit f40b125), sauf l'objectif.

DONNÉES : exploration 2016-01-01 → 2026-08-28 seulement (même garde-fou ; réserve 2010-06 → 2015-12 non lue).

RÈGLE : range 9:30-9:59, 1 R = W ; entrée par ordre stop sur la borne à la première cassure dès 10:00 ; stop fixe à
une largeur de range de l'entrée ; NOUVEAU : objectif à entrée ± TP × W, TP ∈ {2, 3} ; sinon sortie à 16:00.
Stop et objectif surveillés dès la barre d'entrée incluse ; si les deux tombent dans la même minute, le stop passe en
premier (prudent) ; sortie à l'open si une barre (après celle d'entrée) ouvre au-delà du niveau.
1 contrat, coût standard 1 tick + 5 $.

GRILLE (12 essais) : 3 actifs × {vendredi, tous les jours} × TP {2R, 3R}.
RÉFÉRENCE : la même case sans objectif (run_orb30_jours.py), sur les mêmes jours (écart moyen, t apparié NW).
CHOIX ET BARRIÈRE : meilleur Sharpe net par trade parmi les 12 ; n_famille = 57 (45 + 12) ; variance des Sharpe :
les 18 cases sans objectif + les 12. Fiche et B1 : fab.protocole.

Compteur global : 2 043 → 2 055 (12 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from fab.core import ASSETS
from fab.protocole import barriere_exploration, fiche, imprimer, nw_t
from run_orb30_jours import FERME, FIN_RANGE, OPEN, matrices

OUT = Path("results/orb30_tp")
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def trades(name: str, M: dict, tp: float | None) -> pd.DataFrame:
    O, H, L, C = M["open"], M["high"], M["low"], M["close"]
    rng = list(range(OPEN, FIN_RANGE))
    hi, lo = H[rng].max(axis=1), L[rng].min(axis=1)
    post = list(range(FIN_RANGE, FERME))
    Hp, Lp, Op, Cp = H[post].values, L[post].values, O[post].values, C[post].values
    end = O[list(range(FERME, FERME + 5))].bfill(axis=1).iloc[:, 0]
    rows = []
    for i, d in enumerate(O.index):
        h0, l0, pe_end = hi.iat[i], lo.iat[i], end.iat[i]
        if not (np.isfinite(h0) and np.isfinite(l0) and np.isfinite(pe_end)) or h0 - l0 <= 0:
            continue
        W = h0 - l0
        hh, ll, oo, cc = Hp[i], Lp[i], Op[i], Cp[i]
        up = np.nan_to_num(hh, nan=-np.inf) > h0
        dn = np.nan_to_num(ll, nan=np.inf) < l0
        k = np.flatnonzero(up | dn)
        if not k.size:
            continue
        j = k[0]
        if up[j] and dn[j]:
            side = 1 if (np.isfinite(cc[j]) and cc[j] >= (h0 + l0) / 2) else -1
        else:
            side = 1 if up[j] else -1
        o_j = oo[j] if np.isfinite(oo[j]) else (h0 if side == 1 else l0)
        pe = max(h0, o_j) if side == 1 else min(l0, o_j)
        st = pe - side * W
        tg = np.inf * side if tp is None else pe + side * tp * W
        H_, L_, O_ = hh[j:], ll[j:], oo[j:]
        if side == 1:
            s_hit = np.nan_to_num(L_, nan=np.inf) <= st
            t_hit = np.nan_to_num(H_, nan=-np.inf) >= tg
        else:
            s_hit = np.nan_to_num(H_, nan=-np.inf) >= st
            t_hit = np.nan_to_num(L_, nan=np.inf) <= tg
        ks, kt = np.flatnonzero(s_hit), np.flatnonzero(t_hit)
        js = ks[0] if ks.size else 10**9
        jt = kt[0] if kt.size else 10**9
        if js == 10**9 and jt == 10**9:
            px, sortie = pe_end, "clôture"
        elif js <= jt:
            g = js > 0 and np.isfinite(O_[js]) and ((O_[js] < st) if side == 1 else (O_[js] > st))
            px, sortie = (O_[js] if g else st), "stop"
        else:
            g = jt > 0 and np.isfinite(O_[jt]) and ((O_[jt] > tg) if side == 1 else (O_[jt] < tg))
            px, sortie = (O_[jt] if g else tg), "objectif"
        rows.append({"date": d, "jour": d.dayofweek, "W": W, "net_pts": side * (px - pe) - ASSETS[name].rt_cost,
                     "sortie": sortie})
    t = pd.DataFrame(rows).set_index("date")
    t["net_R"] = t.net_pts / t.W
    return t


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    g0 = pd.read_csv("results/orb30_jours/grille.csv")
    sh18 = list((g0.sharpe_an / np.sqrt(252.0)).values)  # Sharpe par trade (fiche annualise par √252)
    res = {}
    for n in ["NQ", "ES", "YM"]:
        M = matrices(n)
        base = trades(n, M, None)
        for tp in (2.0, 3.0):
            res[(n, tp)] = (trades(n, M, tp), base)
    cal = {"vendredi": [4], "tous": [0, 1, 2, 3, 4]}
    sh12 = []
    for (n, tp), (t, b) in res.items():
        for c, js in cal.items():
            x = t.net_R[t.jour.isin(js)]
            sh12.append(x.mean() / x.std())
    rows, fiches = [], {}
    for (n, tp), (t, b) in res.items():
        for c, js in cal.items():
            m = t.jour.isin(js)
            x, x0 = t.net_R[m], b.net_R[b.jour.isin(js)]
            f = fiche(x, None, None, n_famille=57, sharpes_famille=sh18 + sh12, tick_bp=ASSETS[n].tick / t.W[m])
            diff = (x - x0.reindex(x.index)).dropna()
            f["ref_net_moy"], f["ecart_ref"], f["t_ecart_ref"] = float(x0.mean()), float(diff.mean()), nw_t(diff.values)
            fiches[(n, tp, c)] = f
            y = x.index.year
            rows.append({"actif": n, "TP": f"{tp:.0f}R", "calendrier": c, "n": f["n"], "net_R": f["net_moy"], "t_nw": f["t_nw"],
                         "sharpe_an": f["sharpe_an"], "gagnants_%": f["gagnants_%"],
                         "objectif_%": 100 * (t.sortie[m] == "objectif").mean(), "stop_%": 100 * (t.sortie[m] == "stop").mean(),
                         "sans_TP_R": x0.mean(), "ecart_vs_sans_TP": f["ecart_ref"], "t_ecart": f["t_ecart_ref"],
                         "2016-22": x[y <= 2022].mean(), "2023-26": x[y >= 2023].mean(), "annees_pos": f["annees_pos"],
                         "net_$": (t.net_pts[m] * ASSETS[n].point_value).mean(), "dsr_57": f["dsr_famille"]})
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "grille.csv", index=False)
    say("===== Objectifs 2R / 3R (R net par trade) ; référence = même case sans objectif =====")
    say(tab.round(3).to_string(index=False))
    best = tab.sort_values("sharpe_an", ascending=False).iloc[0]
    f = fiches[(best.actif, float(best.TP[:-1]), best.calendrier)]
    say("\n" + imprimer(f, f"Règle choisie (meilleur Sharpe net) : {best.actif}, {best.calendrier}, TP {best.TP}"))
    okb, raisons = barriere_exploration(f)
    say("B1 : " + ("✅ franchie" if okb else "❌ ratée"))
    for r in raisons:
        say("  " + r)
    t, b = res[("NQ", 2.0)]
    t3, _ = res[("NQ", 3.0)]
    v = lambda s: s[s.jour == 4].net_R
    say("\nNQ vendredi, R net par année : sans TP / TP 2R / TP 3R")
    say(pd.DataFrame({"sans_TP": v(b).groupby(v(b).index.year).mean(), "TP2R": v(t).groupby(v(t).index.year).mean(),
                      "TP3R": v(t3).groupby(v(t3).index.year).mean()}).round(3).to_string())
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
