"""ORB 30 minutes NQ, lundi à jeudi, objectif 2R : régime de gamma approché par le RSI 5 jours (Zarattini, Aziz,
Barbon 2024, section 4.5). Étape 1, suite.

Fiche : wiki/experiments/orb30-jours-semaine.md (section « Lundi-jeudi : RSI 5 jours »). Grille figée ici et commitée
AVANT tout calcul. Idée : RSI bas (marché en baisse récente) → teneurs de marché probablement en gamma négatif →
tendances prolongées → suivre la cassure ; RSI haut → gamma positif → cassures qui échouent → jouer la réintégration
(demande de l'utilisateur, 2026-11-22).

DONNÉES : NQ Databento 1 min, exploration 2016-01-01 → 2026-08-28 seulement (réserve 2010-06 → 2015-12 non lue).
Trades du 2016-06-01 au 2026-08-28, lundi à jeudi.

RSI 5 JOURS : RSI de Wilder, période 5, sur les clôtures de 16:00 ET (dernière barre avant 16:00) des séances
précédentes ; la valeur utilisée un jour J est celle de la clôture de J−1. Seuil fixé : 50.

RÈGLES (range 9:30-9:59 : ORhi, ORlo, W ; 1 contrat ; coût 0,50 pt ; objectif 2 × distance au stop ; sinon sortie
à l'open de la 1ʳᵉ barre dans [16:00, 16:05) ; stop et objectif surveillés dès la barre d'entrée, stop prioritaire)
- CASSURE (ORB de Subhani) : première barre dès 10:00 qui dépasse ORhi (achat) ou passe sous ORlo (vente) ; si les
  deux dans la même barre, la clôture tranche ; entrée par ordre stop sur la borne (gap : à l'open) ; stop à 1 W.
- RÉINTÉGRATION (les deux côtés) : pour chaque borne, après une barre qui la dépasse, la première barre qui clôture de
  nouveau à l'intérieur arme un ordre LIMITE sur cette borne à partir de la barre suivante, dans le sens du retour
  (borne haute → vente, borne basse → achat). Rempli si le prix dépasse la borne d'au moins 1 tick (au prix de la borne,
  ou à l'open si la barre ouvre au-delà). Premier ordre rempli = trade du jour. Stop à 1 W de l'entrée.

GRILLE (2 essais)
- V1 filtre : RSI5(J−1) < 50 → CASSURE ; RSI5(J−1) ≥ 50 → pas de trade.
- V2 filtre + réintégration : RSI5(J−1) < 50 → CASSURE ; RSI5(J−1) ≥ 50 → RÉINTÉGRATION.
Rapporté aussi (décomposition de V2, non compté) : RÉINTÉGRATION les jours RSI ≥ 50 ; CASSURE les jours RSI ≥ 50.

RÉFÉRENCE (non comptée) : CASSURE tous les lundis-jeudis (ORB objectif 2R), mêmes jours.
- V1 : jours pris contre jours exclus (t de Welch, en R).
- V2 : écart par jour en points nets avec la référence (0 si pas de trade), t de Newey-West.
CHOIX ET BARRIÈRE : meilleur Sharpe net par trade (R) parmi V1, V2 ; n_famille = 75 (73 + 2) ; variance des Sharpe :
les 46 cases déjà calculées + les 2. Fiche et B1 : fab.protocole.

Compteur global : 2 071 → 2 073 (2 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from fab.protocole import barriere_exploration, fiche, imprimer, nw_t
from run_orb30_jours import FERME, FIN_RANGE, OPEN, matrices

DEBUT_TRADES = pd.Timestamp("2016-06-01")
OUT = Path("results/orb30_rsi")
TICK, COUT, TP, SEUIL = 0.25, 0.50, 2.0, 50.0
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def rsi_wilder(close: pd.Series, n: int = 5) -> pd.Series:
    d = close.diff()
    up, dn = d.clip(lower=0), (-d).clip(lower=0)
    au, ad = up.ewm(alpha=1 / n, adjust=False).mean(), dn.ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + au / ad)


def sortie(hh, ll, oo, j0, side, pe, dist, pe_end):
    st, tg = pe - side * dist, pe + side * TP * dist
    H_, L_, O_ = hh[j0:], ll[j0:], oo[j0:]
    if side == 1:
        s_hit, t_hit = np.nan_to_num(L_, nan=np.inf) <= st, np.nan_to_num(H_, nan=-np.inf) >= tg
    else:
        s_hit, t_hit = np.nan_to_num(H_, nan=-np.inf) >= st, np.nan_to_num(L_, nan=np.inf) <= tg
    ks, kt = np.flatnonzero(s_hit), np.flatnonzero(t_hit)
    js = ks[0] if ks.size else 10**9
    jt = kt[0] if kt.size else 10**9
    if js == 10**9 and jt == 10**9:
        return pe_end, "clôture"
    if js <= jt:
        g = js > 0 and np.isfinite(O_[js]) and ((O_[js] < st) if side == 1 else (O_[js] > st))
        return (O_[js] if g else st), "stop"
    g = jt > 0 and np.isfinite(O_[jt]) and ((O_[jt] > tg) if side == 1 else (O_[jt] < tg))
    return (O_[jt] if g else tg), "objectif"


def cassure(hh, ll, oo, cc, h0, l0):
    up = np.nan_to_num(hh, nan=-np.inf) > h0
    dn = np.nan_to_num(ll, nan=np.inf) < l0
    k = np.flatnonzero(up | dn)
    if not k.size:
        return None
    j = k[0]
    side = ((1 if (np.isfinite(cc[j]) and cc[j] >= (h0 + l0) / 2) else -1) if (up[j] and dn[j]) else (1 if up[j] else -1))
    o_j = oo[j] if np.isfinite(oo[j]) else (h0 if side == 1 else l0)
    return j, side, (max(h0, o_j) if side == 1 else min(l0, o_j))


def reintegration(hh, ll, oo, cc, h0, l0):
    broke = {1: False, -1: False}   # 1 = borne haute, -1 = borne basse
    armed = {1: False, -1: False}
    for j in range(len(hh)):
        if not np.isfinite(hh[j]):
            continue
        # ordres armés aux barres précédentes : vente limite à ORhi, achat limite à ORlo
        if armed[1] and hh[j] >= h0 + TICK:
            o_j = oo[j] if np.isfinite(oo[j]) else h0
            return j, -1, max(h0, o_j)
        if armed[-1] and ll[j] <= l0 - TICK:
            o_j = oo[j] if np.isfinite(oo[j]) else l0
            return j, 1, min(l0, o_j)
        if hh[j] > h0:
            broke[1] = True
        if ll[j] < l0:
            broke[-1] = True
        if np.isfinite(cc[j]):
            if broke[1] and not armed[1] and cc[j] < h0:
                armed[1] = True
            if broke[-1] and not armed[-1] and cc[j] > l0:
                armed[-1] = True
    return None


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    M = matrices("NQ")
    O, H, L, C = M["open"], M["high"], M["low"], M["close"]
    sess = list(range(OPEN, FERME))
    close16 = C[sess].ffill(axis=1).iloc[:, -1]
    rsi_prev = rsi_wilder(close16.dropna()).reindex(O.index).shift(1)
    rng = list(range(OPEN, FIN_RANGE))
    hi, lo = H[rng].max(axis=1), L[rng].min(axis=1)
    end = O[list(range(FERME, FERME + 5))].bfill(axis=1).iloc[:, 0]
    post = list(range(FIN_RANGE, FERME))
    Hp, Lp, Op, Cp = H[post].values, L[post].values, O[post].values, C[post].values
    rows = []
    for i, d in enumerate(O.index):
        if d < DEBUT_TRADES or d.dayofweek > 3 or not np.isfinite(rsi_prev.iat[i]):
            continue
        h0, l0, pe_end = hi.iat[i], lo.iat[i], end.iat[i]
        if not (np.isfinite(h0) and np.isfinite(l0) and np.isfinite(pe_end)) or h0 - l0 <= 0:
            continue
        W = h0 - l0
        for typ, fn in (("cassure", cassure), ("réintégration", reintegration)):
            e = fn(Hp[i], Lp[i], Op[i], Cp[i], h0, l0)
            if e is None:
                continue
            j, side, pe = e
            px, so = sortie(Hp[i], Lp[i], Op[i], j, side, pe, W, pe_end)
            net = side * (px - pe) - COUT
            rows.append({"date": d, "jour": d.dayofweek, "rsi": rsi_prev.iat[i], "type": typ, "side": side, "W": W,
                         "minute": FIN_RANGE + j, "p_in": pe, "p_out": px, "sortie": so, "net_pts": net, "net_R": net / W})
    T = pd.DataFrame(rows).set_index("date")
    cas, rei = T[T.type == "cassure"], T[T.type == "réintégration"]
    bas = cas.rsi < SEUIL
    v1 = cas[bas]
    v2 = pd.concat([cas[bas], rei[rei.rsi >= SEUIL]]).sort_index()
    jours = O.index[(O.index >= DEBUT_TRADES) & (O.index.dayofweek <= 3) & rsi_prev.notna().values]
    base_d = cas.net_pts.reindex(jours).fillna(0.0)
    g1 = pd.read_csv("results/orb30_jours/grille.csv")
    g2 = pd.read_csv("results/orb30_tp/grille.csv")
    g3 = pd.read_csv("results/orb30_filtres/conditions.csv")
    g4 = pd.read_csv("results/orb30_biais/grille.csv")
    fam = list(g1.sharpe_an / np.sqrt(252)) + list(g2.sharpe_an / np.sqrt(252)) + list(g3.sharpe_trade) + list(g4.sharpe_trade)
    fam += [v1.net_R.mean() / v1.net_R.std(), v2.net_R.mean() / v2.net_R.std()]
    say(f"Jours lun-jeu avec RSI : {len(jours)} ; RSI < 50 : {int((rsi_prev.reindex(jours) < SEUIL).sum())} ; "
        f"référence (cassure tous les jours) : {len(cas)} trades, {cas.net_R.mean():+.3f} R, {base_d.mean():+.2f} pts par jour ; "
        f"famille {len(fam)} Sharpe, N = 75")
    fiches = {}
    f1 = fiche(v1.net_R, None, None, n_famille=75, sharpes_famille=fam, tick_bp=TICK / v1.W)
    w = stats.ttest_ind(v1.net_R, cas.net_R[~bas], equal_var=False)
    f1["ref_net_moy"], f1["ecart_ref"], f1["t_ecart_ref"] = float(cas.net_R[~bas].mean()), float(v1.net_R.mean() - cas.net_R[~bas].mean()), float(w.statistic)
    fiches["V1 filtre RSI < 50"] = f1
    f2 = fiche(v2.net_R, None, None, n_famille=75, sharpes_famille=fam, tick_bp=TICK / v2.W)
    diff = v2.net_pts.reindex(jours).fillna(0.0) - base_d
    f2["ref_net_moy"], f2["ecart_ref"], f2["t_ecart_ref"] = float(base_d.mean()), float(diff.mean()), nw_t(diff.values)
    fiches["V2 cassure si RSI < 50, réintégration sinon"] = f2
    rows = []
    for nom, x, f in [("V1 filtre RSI < 50", v1, f1), ("V2 cassure si RSI < 50, réintégration sinon", v2, f2)]:
        y = x.index.year
        rows.append({"variante": nom, "n": len(x), "net_R": x.net_R.mean(), "t_nw": f["t_nw"],
                     "sharpe_trade": x.net_R.mean() / x.net_R.std(), "gagnants_%": f["gagnants_%"], "net_pts": x.net_pts.mean(),
                     "ref": f["ref_net_moy"], "ecart_ref": f["ecart_ref"], "t_ecart_ref": f["t_ecart_ref"],
                     "objectif_%": 100 * (x.sortie == "objectif").mean(), "2016-22": x.net_R[y <= 2022].mean(),
                     "2023-26": x.net_R[y >= 2023].mean(), "annees_pos": f["annees_pos"], "dsr_75": f["dsr_famille"]})
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "grille.csv", index=False)
    say("\n===== RSI 5 jours (NQ, lundi-jeudi, objectif 2R) =====")
    say(tab.round(3).to_string(index=False))
    say("\nDécomposition (non comptée), R net par trade :")
    for nom, x in [("cassure, RSI < 50", cas[bas]), ("cassure, RSI ≥ 50", cas[~bas]),
                   ("réintégration, RSI < 50", rei[rei.rsi < SEUIL]), ("réintégration, RSI ≥ 50", rei[rei.rsi >= SEUIL])]:
        say(f"  {nom:26s} n {len(x):4d}  {x.net_R.mean():+.3f} R  t {x.net_R.mean() / x.net_R.std() * np.sqrt(len(x)):+.2f}  "
            f"({x.net_pts.mean():+.2f} pts)")
    q = pd.qcut(cas.rsi, 5)
    say("\nCassure par quintile de RSI5 (R net) :\n" + cas.groupby(q, observed=True).net_R.agg(["count", "mean"]).round(3).to_string())
    best = tab.sort_values("sharpe_trade", ascending=False).iloc[0].variante
    say("\n" + imprimer(fiches[best], f"Règle choisie (meilleur Sharpe net) : {best}"))
    okb, raisons = barriere_exploration(fiches[best])
    say("B1 : " + ("✅ franchie" if okb else "❌ ratée"))
    for r in raisons:
        say("  " + r)
    T.to_csv(OUT / "trades.csv")
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
