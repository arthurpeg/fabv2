"""ORB 30 minutes de Subhani (2026), stop à une largeur de range, par jour de la semaine, sur NQ, ES, YM. Étape 1.

Fiche : wiki/experiments/orb30-jours-semaine.md. Grille figée ici et commitée AVANT tout calcul.

DONNÉES
- NQ, ES, YM Databento 1 min (fab.core.load, prix ajustés ramenés en prix bruts par le facteur ; aucune position ne
  traverse un roulement). Heures de New York, jours ouvrés.
- Exploration : 2016-01-01 → 2026-08-28 seulement. La réserve 2010-06-08 → 2015-12-31 (wiki/reserves.md) n'est PAS
  lue : ce script n'ouvre pas cache/databento_2010 et coupe toute date antérieure au 2016-01-01.

RÈGLE (Subhani 2026, tableau 1, transposée aux futures)
- Range : plus haut ORhi et plus bas ORlo des barres 9:30 → 9:59 ; W = ORhi − ORlo (pas de trade si W ≤ 0).
- Entrée : première barre à partir de 10:00 dont le plus haut dépasse ORhi (achat) ou le plus bas passe sous ORlo
  (vente). Si une même barre dépasse les deux bornes, sa clôture tranche : moitié haute du range → achat.
  Ordre stop posé sur la borne : prix d'entrée = max(ORhi, open de la barre) à l'achat, min(ORlo, open) à la vente.
- Stop fixe à une largeur de range : achat stop = entrée − W, vente stop = entrée + W. Surveillé dès la barre d'entrée
  incluse (prudent) ; sortie au stop, ou à l'open si une barre ouvre au-delà.
- Pas d'objectif. Sinon sortie à l'open de la première barre dans [16:00, 16:05).
- Un trade au plus par jour. 1 contrat. Coût standard 1 tick + 5 $ (NQ 0,50 pt, ES 0,35 pt, YM 2 pts).
- Mesure : R net = (points nets) / W ; aussi en points et en $.

GRILLE (18 essais) : 3 actifs × 6 calendriers {lundi, mardi, mercredi, jeudi, vendredi, tous les jours}.

RÉFÉRENCES (non comptées)
- Pour un jour J : les autres jours, même règle (écart J − autres jours, t de Welch) = référence triviale du filtre.
- Pour « tous les jours » : même entrée et mêmes sorties, mais toujours à l'achat (ce qui retire la direction).

RÉPLICATION : vendredi sur NQ et ES, du 2018-05-01 au 2026-06-12 (période du papier), à comparer à QQQ +0,199 R
(t 3,05) et SPY (t 1,88). Rapportée, pas un critère.

CHOIX ET BARRIÈRE : règle choisie = meilleur Sharpe net par trade (en R) parmi les 18 ; n_famille = 45 (18 + les 27
ORB de M3 déjà vus) ; variance des Sharpe : les 18. Fiche et B1 : fab.protocole.

Compteur global : 2 025 → 2 043 (18 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from fab.core import ASSETS, NY, load
from fab.protocole import barriere_exploration, fiche, imprimer

DEBUT, FIN = pd.Timestamp("2016-01-01"), pd.Timestamp("2026-08-28")
OUT = Path("results/orb30_jours")
OPEN, FIN_RANGE, FERME = 570, 600, 960
JOURS = {0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi", 4: "vendredi"}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def matrices(name: str) -> dict[str, pd.DataFrame]:
    b = load(name)
    b = b[(b.index >= pd.Timestamp(DEBUT, tz="UTC")) & (b.index < pd.Timestamp(FIN + pd.Timedelta(days=2), tz="UTC"))]
    df = b[["open", "high", "low", "close"]].div(b["factor"], axis=0)
    loc = df.tz_convert(NY)
    m = loc.index.hour * 60 + loc.index.minute
    keep = (m >= OPEN) & (m < FERME + 5) & (loc.index.dayofweek < 5)
    loc = loc[keep]
    loc = loc.assign(d=loc.index.tz_localize(None).normalize(), m=m[keep])
    loc = loc[(loc.d >= DEBUT) & (loc.d <= FIN)]  # garde-fou : rien dans la réserve, rien après le 2026-08-28
    cols = range(OPEN, FERME + 5)
    return {c: loc.pivot(index="d", columns="m", values=c).reindex(columns=cols) for c in ["open", "high", "low", "close"]}


def trades(name: str) -> pd.DataFrame:
    M = matrices(name)
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
            continue  # le prix n'est jamais sorti du range
        j = k[0]
        if up[j] and dn[j]:
            side = 1 if (np.isfinite(cc[j]) and cc[j] >= (h0 + l0) / 2) else -1
        else:
            side = 1 if up[j] else -1
        o_j = oo[j] if np.isfinite(oo[j]) else (h0 if side == 1 else l0)
        pe = max(h0, o_j) if side == 1 else min(l0, o_j)
        st = pe - side * W
        hit = (np.nan_to_num(ll[j:], nan=np.inf) <= st) if side == 1 else (np.nan_to_num(hh[j:], nan=-np.inf) >= st)
        ks = np.flatnonzero(hit)
        if ks.size:
            jj = j + ks[0]
            gap = jj > j and np.isfinite(oo[jj]) and ((oo[jj] < st) if side == 1 else (oo[jj] > st))
            px, sortie = (oo[jj] if gap else st), "stop"
        else:
            px, sortie = pe_end, "clôture"
        rows.append({"date": d, "jour": d.dayofweek, "side": side, "W": W, "p_in": pe, "p_out": px, "sortie": sortie,
                     "m_in": FIN_RANGE + j, "brut_pts": side * (px - pe), "long_pts": px - pe})
    t = pd.DataFrame(rows).set_index("date")
    a = ASSETS[name]
    t["net_pts"] = t.brut_pts - a.rt_cost
    t["net_R"] = t.net_pts / t.W
    t["brut_R"] = t.brut_pts / t.W
    t["long_R"] = (t.long_pts - a.rt_cost) / t.W
    t["net_usd"] = t.net_pts * a.point_value
    return t


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    T = {n: trades(n) for n in ["NQ", "ES", "YM"]}
    cal = {**{v: [k] for k, v in JOURS.items()}, "tous": list(JOURS)}
    sharpes = []
    for n, t in T.items():
        for c, js in cal.items():
            x = t.net_R[t.jour.isin(js)]
            sharpes.append(x.mean() / x.std())
    rows, fiches = [], {}
    for n, t in T.items():
        say(f"\n######## {n} : {len(t)} trades ({t.index[0].date()} → {t.index[-1].date()}), W médian {t.W.median():.1f} pts, "
            f"coût médian {(ASSETS[n].rt_cost / t.W).median():.4f} R, sorties stop {100 * (t.sortie == 'stop').mean():.1f} %")
        for c, js in cal.items():
            m = t.jour.isin(js)
            x = t.net_R[m]
            ref = None if c == "tous" else t.net_R[~m]
            f = fiche(x, t.brut_R[m], t.long_R[m] if c == "tous" else None, n_famille=45, sharpes_famille=sharpes,
                      tick_bp=(ASSETS[n].tick / t.W[m]))
            if ref is not None:
                w = stats.ttest_ind(x, ref, equal_var=False)
                f["ref_net_moy"], f["ecart_ref"], f["t_ecart_ref"] = float(ref.mean()), float(x.mean() - ref.mean()), float(w.statistic)
            fiches[(n, c)] = f
            y = x.index.year
            pap = x[(x.index >= "2018-05-01") & (x.index <= "2026-06-12")]
            rows.append({"actif": n, "calendrier": c, "n": f["n"], "net_R": f["net_moy"], "t_nw": f["t_nw"],
                         "sharpe_an": f["sharpe_an"], "gagnants_%": f["gagnants_%"], "net_pts": t.net_pts[m].mean(),
                         "net_$": t.net_usd[m].mean(), "ref_R": f.get("ref_net_moy", np.nan),
                         "t_ecart_ref": f.get("t_ecart_ref", np.nan), "2016-22": x[y <= 2022].mean(),
                         "2023-26": x[y >= 2023].mean(), "2020": x[y == 2020].mean(), "periode_papier": pap.mean(),
                         "t_papier": (pap.mean() / pap.std() * np.sqrt(len(pap))) if len(pap) > 2 else np.nan,
                         "annees_pos": f["annees_pos"], "dsr_45": f["dsr_famille"]})
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "grille.csv", index=False)
    say("\n===== Grille (R net par trade, 1 R = largeur du range 9:30-10:00) =====")
    say(tab.round(3).to_string(index=False))
    best = tab.sort_values("sharpe_an", ascending=False).iloc[0]
    f = fiches[(best.actif, best.calendrier)]
    say("\n" + imprimer(f, f"Règle choisie (meilleur Sharpe net) : {best.actif}, {best.calendrier}"))
    okb, raisons = barriere_exploration(f)
    say("B1 : " + ("✅ franchie" if okb else "❌ ratée"))
    for r in raisons:
        say("  " + r)
    for n, t in T.items():
        say(f"\n{n} — R net moyen par année et par jour :")
        say(t.pivot_table(index=t.index.year, columns=t.jour.map(JOURS), values="net_R", aggfunc="mean")
            [list(JOURS.values())].round(3).to_string())
        t.to_csv(OUT / f"trades_{n}.csv")
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
