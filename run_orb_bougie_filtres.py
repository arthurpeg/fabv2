"""NQ, règle de la 1ʳᵉ bougie (Zarattini-Aziz) avec stop 0,5 × ATR14 et objectif 2R : trois filtres. Étape 1, suite.

Fiche : wiki/experiments/nq-orb-bougie-sorties.md (section « Filtres F1-F3 »). Grille figée ici et commitée AVANT tout
calcul. Règle de base, données et conventions identiques à run_orb_bougie_indices.py (commit 40cfcc9).

DONNÉES : NQ Databento 1 min, 2010-06 → 2021-09-30 (rien dans la réserve 2021-10-01 → 2026-08-28).

RÈGLE DE BASE (B) : sens de la bougie 9:30-9:35 ET (doji si corps ≤ 1 tick : pas de trade), entrée à l'open de 9:35,
stop 0,5 × ATR14 (amplitude moyenne 9:30-16:00 des 14 séances précédentes), objectif 2 × stop, sinon sortie à 16:00.
1 contrat, coût 0,50 pt aller-retour.

FILTRES (3 essais, un seuil chacun, fixé ici)
- F1 « pas d'annonce pendant le trade » : on saute les jours où config/calendrier_macro_us.csv contient une annonce à
  10:00 ou 14:00 ET (ISM manufacturier, ISM services, JOLTS, FOMC décision, FOMC minutes). Les annonces de 8:30 sont
  gardées (elles tombent avant la bougie). Dates ISM approximées par règle dans le calendrier.
- F2 « volume anormal » : volume 9:30-9:34 > 1,5 × médiane de ce même volume sur les 20 séances précédentes.
- F3 « bougie franche » : |C1 − O1| > 0,05 × ATR14.

MESURE ET BARRIÈRE (PROTOCOLE.md, filtre sur une règle connue)
- Pour chaque filtre : fiche (fab.protocole.fiche) des jours pris.
- Référence d'un filtre = les jours sautés : écart moyen jours pris − jours sautés, t de Welch. Ce t remplace le
  critère 3 de B1 (« bat la référence triviale, t ≥ 1 »).
- n_famille = 85 (81 variantes de sortie déjà calculées sur ES, YM, NQ + R4 + 3 filtres) ; variance des Sharpe :
  les 81 de results/orb_bougie_indices/grille.csv + les 3 filtres.
- Choix : meilleur Sharpe net par trade parmi F1, F2, F3. Rapporté aussi : 2010-2015, 2016-2021, 2020.

Compteur global : 2 021 → 2 024 (3 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from fab.core import NY, load
from fab.protocole import barriere_exploration, fiche, imprimer
from run_nq_orb_bougie import first_open, simule

FIN_EXPLO = pd.Timestamp("2021-09-30")
OUT = Path("results/orb_bougie_filtres")
OPEN, ENTREE, FERME = 570, 575, 960
TICK, COUT, K, RR = 0.25, 0.50, 0.50, 2.0
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def matrices() -> dict[str, pd.DataFrame]:
    a = pd.read_parquet("cache/databento_2010/NQ_v0_1m_2010.parquet")
    a = a[a.index < pd.Timestamp("2016-01-01", tz="UTC")]
    b = load("NQ")
    b = b[b.index >= pd.Timestamp("2016-01-01", tz="UTC")]
    px = b[["open", "high", "low", "close"]].div(b["factor"], axis=0)
    b = px.assign(volume=b["volume"])
    df = pd.concat([a[["open", "high", "low", "close", "volume"]], b]).sort_index()
    df = df[~df.index.duplicated()]
    loc = df.tz_convert(NY)
    m = loc.index.hour * 60 + loc.index.minute
    keep = (m >= OPEN) & (m < FERME + 5) & (loc.index.dayofweek < 5)
    loc = loc[keep]
    loc = loc.assign(d=loc.index.tz_localize(None).normalize(), m=m[keep])
    loc = loc[loc.d <= FIN_EXPLO]  # garde-fou : rien dans la réserve
    cols = range(OPEN, FERME + 5)
    return {c: loc.pivot(index="d", columns="m", values=c).reindex(columns=cols)
            for c in ["open", "high", "low", "close", "volume"]}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    M = matrices()
    O, H, L, C, V = M["open"], M["high"], M["low"], M["close"], M["volume"]
    sess, rc = list(range(OPEN, FERME)), list(range(OPEN, ENTREE))
    atr = (H[sess].max(axis=1) - L[sess].min(axis=1)).rolling(14, min_periods=14).mean().shift(1)
    vol1 = V[rc].sum(axis=1, min_count=1)
    vmed = vol1.rolling(20, min_periods=20).median().shift(1)
    o1, c1 = first_open(O, OPEN), C[rc].ffill(axis=1).iloc[:, -1]
    p_in, p_end = O[ENTREE], first_open(O, FERME)
    ok = o1.notna() & c1.notna() & p_in.notna() & p_end.notna() & atr.notna() & vmed.notna() & ((c1 - o1).abs() > TICK)
    d = pd.DataFrame({"o1": o1, "c1": c1, "p_in": p_in, "p_end": p_end, "atr": atr, "vol1": vol1, "vmed": vmed})[ok]
    d["side"] = np.where(d.c1 > d.o1, 1, -1)
    idx = d.index
    tc = list(range(ENTREE, FERME))
    sd = K * d.atr.values
    po, kd = simule(d.side.values, d.p_in.values, sd, RR * sd, H.loc[idx, tc].values, L.loc[idx, tc].values,
                    O.loc[idx, tc].values, d.p_end.values)
    net = pd.Series(d.side.values * (po - d.p_in.values) - COUT, idx)

    cal = pd.read_csv("config/calendrier_macro_us.csv")
    jours_annonce = set(pd.to_datetime(cal[cal.heure_ET.isin(["10:00", "14:00"])].date))
    filtres = {
        "F1 pas d'annonce 10:00/14:00": ~idx.isin(jours_annonce),
        "F2 volume 1re bougie > 1,5 × médiane 20 j": (d.vol1 > 1.5 * d.vmed).values,
        "F3 corps > 0,05 × ATR14": ((d.c1 - d.o1).abs() > 0.05 * d.atr).values,
    }
    g = pd.read_csv("results/orb_bougie_indices/grille.csv")
    sh81 = list((g[~g.variante.str.startswith("R4")].sharpe_an / np.sqrt(252)).values)
    sh3 = [net[m].mean() / net[m].std() for m in filtres.values()]
    famille = sh81 + sh3
    say(f"Base B (stop 0,5 ATR, objectif 2R) : {len(net)} trades, net {net.mean():+.3f} pt, "
        f"Sharpe {net.mean() / net.std() * np.sqrt(252):.3f} (famille : {len(famille)} Sharpe, N = 85)")
    rows, fiches = [], {}
    for nom, m in filtres.items():
        m = np.asarray(m)
        pris, saute = net[m], net[~m]
        f = fiche(pris, pris + COUT, None, n_famille=85, sharpes_famille=famille, tick_bp=TICK)
        w = stats.ttest_ind(pris, saute, equal_var=False)
        f["ref_net_moy"], f["ecart_ref"], f["t_ecart_ref"] = float(saute.mean()), float(pris.mean() - saute.mean()), float(w.statistic)
        fiches[nom] = f
        y = pris.index.year
        rows.append({"filtre": nom, "pris": len(pris), "sautes": len(saute), "net_pris": pris.mean(), "net_sautes": saute.mean(),
                     "t_ecart": w.statistic, "t_nw_pris": f["t_nw"], "sharpe_pris": f["sharpe_an"], "dsr_85": f["dsr_famille"],
                     "2010-15": pris[y <= 2015].mean(), "2016-21": pris[y >= 2016].mean(), "2020": pris[y == 2020].mean(),
                     "annees_pos": f["annees_pos"]})
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "filtres.csv", index=False)
    pd.set_option("display.width", 250)
    say(tab.round(3).to_string(index=False))
    best = tab.sort_values("sharpe_pris", ascending=False).iloc[0].filtre
    f = fiches[best]
    say("\n" + imprimer(f, f"Filtre choisi (meilleur Sharpe net) : {best}"))
    okb, raisons = barriere_exploration(f)
    say("B1 : " + ("✅ franchie" if okb else "❌ ratée"))
    for r in raisons:
        say("  " + r)
    for nom, m in filtres.items():
        m = np.asarray(m)
        say(f"\n{nom} — net par année, jours pris / sautés (pts/trade) :")
        yy = net.index.year
        say(pd.DataFrame({"pris": net[m].groupby(yy[m]).mean(), "sautes": net[~m].groupby(yy[~m]).mean(),
                          "n_pris": net[m].groupby(yy[m]).size()}).round(2).to_string())
    pd.DataFrame({"net": net, **{k: np.asarray(v) for k, v in filtres.items()}}).to_csv(OUT / "trades.csv")
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
