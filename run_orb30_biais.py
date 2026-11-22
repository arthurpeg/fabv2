"""ORB 30 minutes NQ, lundi à jeudi : biais de tendance (EMA 20/50 sur 15 min, 1 h, 4 h, jour), cassure dans le sens du
biais et réintégration contre le biais. Objectif 2R. Étape 1, suite.

Fiche : wiki/experiments/orb30-jours-semaine.md (section « Lundi-jeudi : biais EMA et réintégration »). Idée de
l'utilisateur (2026-11-22). Grille figée ici et commitée AVANT tout calcul.

DONNÉES
- NQ Databento 1 min (fab.core.load). Exploration 2016-01-01 → 2026-08-28 seulement ; réserve 2010-06 → 2015-12 non lue.
- Les EMA sont amorcées sur les données à partir du 2016-01-01 ; aucun trade avant le 2016-06-01.
- Trades : lundi, mardi, mercredi, jeudi. Heures de New York.

BIAIS (fixé à 10:00, avec les seules bougies terminées à 10:00)
- Pour chaque unité de temps : tendance = +1 si EMA20 > EMA50 des clôtures, −1 si EMA20 < EMA50.
  * 15 min, 1 h, 4 h : bougies construites sur toutes les heures de cotation (nuit comprise), prix ajustés des
    roulements, découpage aligné sur minuit heure de New York ; dernière bougie terminée avant 10:00 (15 min : 9:45-10:00 ;
    1 h : 9:00-10:00 ; 4 h : 4:00-8:00).
  * Jour : clôtures de 16:00 ET des séances précédentes.
- Biais = signe de la somme des 4 votes. Égalité 2-2 (somme nulle) : trois traitements testés (voir la grille).

RÈGLE COMPLÈTE (range 9:30-9:59 : ORhi, ORlo, W = ORhi − ORlo ; 1 contrat ; coût 0,50 pt aller-retour)
- Ordre STOP côté biais, actif dès la barre de 10:00 : biais +1 → achat stop à ORhi ; biais −1 → vente stop à ORlo.
  Remplissage = max(ORhi, open) à l'achat, min(ORlo, open) à la vente (gap). Stop de protection à 1 W de l'entrée.
- Réintégration contre le biais : biais −1 et une barre dépasse ORhi (plus haut > ORhi) → on attend la première barre
  qui CLÔTURE sous ORhi ; à partir de la barre suivante, VENTE LIMITE à ORhi, remplie si le plus haut ≥ ORhi + 1 tick
  (au prix ORhi, ou à l'open si la barre ouvre au-dessus). Symétrique pour le biais +1 (achat limite à ORlo).
  Stop de protection : variante « W » = 1 W de l'entrée ; variante « mèche » = plus haut (plus bas) atteint entre la
  cassure et la barre précédant le remplissage, + 1 tick.
- Un seul trade par jour : le premier ordre rempli gagne ; si deux le sont dans la même barre, la cassure passe d'abord.
- Objectif à 2 × la distance d'entrée au stop (2R) ; sinon sortie à l'open de la 1ʳᵉ barre dans [16:00, 16:05).
  Stop et objectif surveillés dès la barre d'entrée incluse, stop prioritaire dans la même minute.
- R = résultat net / distance d'entrée au stop du trade.

ÉGALITÉ 2-2 : (a) pas de trade ; (b) ORB classique de Subhani dans les deux sens (cassure, stop 1 W, sans
réintégration) ; (c) le vote journalier tranche.

GRILLE (13 essais)
- Règle complète : stop de réintégration {W, mèche} × égalité {a, b, c} = 6.
- Cassure dans le sens du biais seule (pas de réintégration) : égalité {a, b, c} = 3.
- Réintégration seule (pas d'ordre stop côté biais) : stop {W, mèche} × égalité {a, c} = 4.

RÉFÉRENCE (non comptée) : ORB 30 min de Subhani, objectif 2R, lundi-jeudi, mêmes jours (run_orb30_filtres.py, base
+0,011 R). Écart par jour en POINTS nets (0 si pas de trade), t de Newey-West ; il remplace le critère 3 de B1.

CHOIX ET BARRIÈRE : meilleur Sharpe net par trade (en R) parmi les 13 ; n_famille = 73 (60 + 13) ; variance des Sharpe :
les 33 cases déjà calculées + les 13. Fiche et B1 : fab.protocole.

Compteur global : 2 058 → 2 071 (13 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from fab.core import NY, load
from fab.protocole import barriere_exploration, fiche, imprimer, nw_t
from run_orb30_jours import FERME, FIN_RANGE, OPEN, matrices

DEBUT_TRADES, FIN = pd.Timestamp("2016-06-01"), pd.Timestamp("2026-08-28")
OUT = Path("results/orb30_biais")
TICK, COUT, TP = 0.25, 0.50, 2.0
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def votes() -> pd.DataFrame:
    """Vote EMA20/50 de chaque unité de temps, connu à 10:00 de chaque date."""
    b = load("NQ")
    b = b[(b.index >= pd.Timestamp("2016-01-01", tz="UTC")) & (b.index < pd.Timestamp(FIN + pd.Timedelta(days=2), tz="UTC"))]
    c = b["close"].tz_convert(NY)
    out = {}
    for nom, freq in [("15min", "15min"), ("1h", "60min"), ("4h", "240min")]:
        cl = c.resample(freq, label="left", closed="left").last().dropna()
        e20, e50 = cl.ewm(span=20, adjust=False).mean(), cl.ewm(span=50, adjust=False).mean()
        v = pd.Series(np.sign(e20 - e50).values, index=cl.index + pd.Timedelta(freq))  # indexé à la FIN de la bougie
        out[nom] = v
    m = c.index.hour * 60 + c.index.minute
    rth = c[(m >= 570) & (m < 960) & (c.index.dayofweek < 5)]
    dcl = rth.groupby(rth.index.normalize()).last()
    e20, e50 = dcl.ewm(span=20, adjust=False).mean(), dcl.ewm(span=50, adjust=False).mean()
    out["D"] = pd.Series(np.sign(e20 - e50).values, index=dcl.index + pd.Timedelta(hours=16))
    return out


def bias_table(dates: pd.DatetimeIndex, v: dict) -> pd.DataFrame:
    t10 = dates.tz_localize(NY) + pd.Timedelta(hours=10)
    cols = {}
    for nom, s in v.items():
        s = s.sort_index()
        cols[nom] = s.reindex(s.index.union(t10)).ffill().reindex(t10).values  # dernière bougie terminée ≤ 10:00
    return pd.DataFrame(cols, index=dates)


def simulate(O, H, L, C, hi, lo, end, bias, mode, stop_rei, tie):
    """mode : 'complete' | 'cassure' | 'reint'. Retourne un DataFrame de trades (un par jour au plus)."""
    rows = []
    post = list(range(FIN_RANGE, FERME))
    Hp, Lp, Op, Cp = H[post].values, L[post].values, O[post].values, C[post].values
    for i, d in enumerate(O.index):
        if d < DEBUT_TRADES or d.dayofweek > 3:
            continue
        h0, l0, pe_end = hi.iat[i], lo.iat[i], end.iat[i]
        if not (np.isfinite(h0) and np.isfinite(l0) and np.isfinite(pe_end)) or h0 - l0 <= 0:
            continue
        W = h0 - l0
        bv = bias.loc[d]
        s = np.nansum(bv.values)
        if np.isnan(bv.values).any():
            continue
        b = int(np.sign(s))
        classic = False
        if b == 0:
            if tie == "a":
                continue
            if tie == "b":
                if mode == "reint":
                    continue
                classic = True
            if tie == "c":
                b = int(bv["D"])
        hh, ll, oo, cc = Hp[i], Lp[i], Op[i], Cp[i]
        n = len(hh)
        entry = None  # (j, side, prix, distance stop)
        broke, armed, wick = False, False, None
        for j in range(n):
            if not np.isfinite(hh[j]):
                continue
            # 1) ordres stop de cassure
            if classic:
                up, dn = hh[j] > h0, ll[j] < l0
                if up or dn:
                    side = (1 if (np.isfinite(cc[j]) and cc[j] >= (h0 + l0) / 2) else -1) if (up and dn) else (1 if up else -1)
                    o_j = oo[j] if np.isfinite(oo[j]) else (h0 if side == 1 else l0)
                    pe = max(h0, o_j) if side == 1 else min(l0, o_j)
                    entry = (j, side, pe, W, "classique")
                    break
                continue
            if mode in ("complete", "cassure"):
                if (b == 1 and hh[j] > h0) or (b == -1 and ll[j] < l0):
                    o_j = oo[j] if np.isfinite(oo[j]) else (h0 if b == 1 else l0)
                    pe = max(h0, o_j) if b == 1 else min(l0, o_j)
                    entry = (j, b, pe, W, "cassure")
                    break
            if mode in ("complete", "reint"):
                lvl = h0 if b == -1 else l0  # borne contre le biais
                if armed:
                    hit = (hh[j] >= lvl + TICK) if b == -1 else (ll[j] <= lvl - TICK)
                    if hit:
                        o_j = oo[j] if np.isfinite(oo[j]) else lvl
                        pe = max(lvl, o_j) if b == -1 else min(lvl, o_j)  # limite : au niveau ou mieux
                        if stop_rei == "W":
                            dist = W
                        else:
                            dist = (wick + TICK - pe) if b == -1 else (pe - (wick - TICK))
                        if dist > 0:
                            entry = (j, b, pe, dist, "réintégration")  # même sens que le biais (corrigé : -b inversait le trade)
                        break
                if b == -1:
                    if hh[j] > lvl:
                        broke = True
                        wick = hh[j] if wick is None else max(wick, hh[j])
                    if broke and not armed and np.isfinite(cc[j]) and cc[j] < lvl:
                        armed = True
                else:
                    if ll[j] < lvl:
                        broke = True
                        wick = ll[j] if wick is None else min(wick, ll[j])
                    if broke and not armed and np.isfinite(cc[j]) and cc[j] > lvl:
                        armed = True
        if entry is None:
            continue
        j0, side, pe, dist, typ = entry
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
            px, sortie = pe_end, "clôture"
        elif js <= jt:
            g = js > 0 and np.isfinite(O_[js]) and ((O_[js] < st) if side == 1 else (O_[js] > st))
            px, sortie = (O_[js] if g else st), "stop"
        else:
            g = jt > 0 and np.isfinite(O_[jt]) and ((O_[jt] > tg) if side == 1 else (O_[jt] < tg))
            px, sortie = (O_[jt] if g else tg), "objectif"
        # type fixé à l'entrée (voir entry)
        net = side * (px - pe) - COUT
        rows.append({"date": d, "jour": d.dayofweek, "biais": b, "type": typ, "side": side, "W": W, "dist": dist,
                     "net_pts": net, "net_R": net / dist, "sortie": sortie, "minute": FIN_RANGE + j0})
    return pd.DataFrame(rows).set_index("date") if rows else pd.DataFrame()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 260)
    M = matrices("NQ")
    O, H, L, C = M["open"], M["high"], M["low"], M["close"]
    rng = list(range(OPEN, FIN_RANGE))
    hi, lo = H[rng].max(axis=1), L[rng].min(axis=1)
    end = O[list(range(FERME, FERME + 5))].bfill(axis=1).iloc[:, 0]
    bias = bias_table(O.index, votes())
    lj = bias[(bias.index >= DEBUT_TRADES) & (bias.index.dayofweek <= 3)].dropna()
    s = lj.sum(axis=1)
    say(f"Biais lun-jeu : {len(lj)} jours ; haussier {int((s > 0).sum())}, baissier {int((s < 0).sum())}, égalité {int((s == 0).sum())} ; "
        f"accord des 4 votes {100 * (lj.abs().sum(axis=1) == lj.sum(axis=1).abs()).mean():.1f} %")
    grille = [("complete", r, t) for r in ("W", "meche") for t in ("a", "b", "c")]
    grille += [("cassure", "-", t) for t in ("a", "b", "c")]
    grille += [("reint", r, t) for r in ("W", "meche") for t in ("a", "c")]
    from run_orb30_tp import trades as base_trades
    base = base_trades("NQ", M, 2.0)
    base = base[(base.jour <= 3) & (base.index >= DEBUT_TRADES)]
    jours = O.index[(O.index >= DEBUT_TRADES) & (O.index.dayofweek <= 3)]
    base_d = base.net_pts.reindex(jours).fillna(0.0)
    res = {}
    for mode, r, t in grille:
        res[(mode, r, t)] = simulate(O, H, L, C, hi, lo, end, bias, mode, "W" if r == "-" else r, t)
    g1 = pd.read_csv("results/orb30_jours/grille.csv")
    g2 = pd.read_csv("results/orb30_tp/grille.csv")
    g3 = pd.read_csv("results/orb30_filtres/conditions.csv")
    fam = list(g1.sharpe_an / np.sqrt(252)) + list(g2.sharpe_an / np.sqrt(252)) + list(g3.sharpe_trade)
    fam += [x.net_R.mean() / x.net_R.std() for x in res.values()]
    rows, fiches = [], {}
    for k, x in res.items():
        f = fiche(x.net_R, None, None, n_famille=73, sharpes_famille=fam, tick_bp=TICK / x.dist)
        diff = x.net_pts.reindex(jours).fillna(0.0) - base_d
        f["ref_net_moy"], f["ecart_ref"], f["t_ecart_ref"] = float(base_d.mean()), float(diff.mean()), nw_t(diff.values)
        fiches[k] = f
        y = x.index.year
        rows.append({"mode": k[0], "stop_reint": k[1], "egalite": k[2], "n": len(x), "net_R": x.net_R.mean(),
                     "t_nw": f["t_nw"], "sharpe_trade": x.net_R.mean() / x.net_R.std(), "gagnants_%": f["gagnants_%"],
                     "net_pts": x.net_pts.mean(), "pts_par_jour_vs_base": f["ecart_ref"], "t_vs_base": f["t_ecart_ref"],
                     "%_reint": 100 * (x.type == "réintégration").mean(), "R_cassure": x.net_R[x.type == "cassure"].mean(),
                     "R_reint": x.net_R[x.type == "réintégration"].mean(), "objectif_%": 100 * (x.sortie == "objectif").mean(),
                     "2016-22": x.net_R[y <= 2022].mean(), "2023-26": x.net_R[y >= 2023].mean(),
                     "annees_pos": f["annees_pos"], "dsr_73": f["dsr_famille"]})
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "grille.csv", index=False)
    say(f"Référence (ORB 30 min objectif 2R, lun-jeu, mêmes jours) : {len(base)} trades, {base.net_R.mean():+.3f} R, "
        f"{base_d.mean():+.2f} pts par jour")
    say("\n===== Grille (NQ, lundi-jeudi, objectif 2R) =====")
    say(tab.round(3).to_string(index=False))
    best = tab.sort_values("sharpe_trade", ascending=False).iloc[0]
    k = (best["mode"], best.stop_reint, best.egalite)
    say("\n" + imprimer(fiches[k], f"Règle choisie (meilleur Sharpe net) : {k}"))
    okb, raisons = barriere_exploration(fiches[k])
    say("B1 : " + ("✅ franchie" if okb else "❌ ratée"))
    for r in raisons:
        say("  " + r)
    x = res[k]
    say("\nRègle choisie, R net par année et par type :")
    say(x.pivot_table(index=x.index.year, columns="type", values="net_R", aggfunc="mean").round(3).to_string())
    for kk, xx in res.items():
        xx.to_csv(OUT / f"trades_{kk[0]}_{kk[1]}_{kk[2]}.csv")
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
