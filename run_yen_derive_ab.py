"""Dérive du yen en session US, grille A + B (étape 1 de PROTOCOLE.md) — fiche : wiki/experiments/yen-derive-concentree.md.

uv run python -X utf8 run_yen_derive_ab.py   → results/yen_derive_ab/ (tranches.csv, fenetres.csv, deciles.csv, seuils.csv, summary.txt)

Données : 6J.v.0 Databento 1 min, du 2016-01-04 au 2023-06-30 SEULEMENT (exploration). Le 2023-07-01 → 2026-08-28 est
la réserve par question (wiki/reserves.md) : le fichier est coupé AVANT tout calcul, y compris les fenêtres glissantes.
Rendement : short 6J (positif = le yen baisse), en bp. Entrée à l'open de la première minute dans [t, t + 5 min),
sortie à l'open de la première minute dans [t_fin, t_fin + 5 min) ; 16:55 pour la dernière tranche. Pas de stop.
Coût standard 1 tick + 5 $ par aller-retour. Jours du lundi au vendredi.
R4 : rendement 6J des 3 journées précédentes (16:55 J−4 → 16:55 J−1) > 0, yen en hausse (même définition que le n° 29).

Grille figée avant tout calcul (2026-11-21). Compteur 1 839 → 1 937 (98 variantes calculées) :
  A1. 18 tranches de 30 min de 08:00 à 16:55 ET (la dernière est 16:30 → 16:55) × {tous les jours, jours R4} = 36 cellules
      descriptives : brut moyen, écart type, t NW, part de la dérive de la fenêtre 08:00 → 16:55.
  A2. 24 fenêtres candidates × {tous, R4} = 48 règles : départ à chaque heure pleine de 08:00 à 16:00, durée 1 h, 2 h ou
      3 h (fin ≤ 16:55 ; une fin à 17:00 devient 16:55). Référence triviale : 11:00 → 16:55 sur les mêmes jours.
  B1. Déciles de la hausse du yen sur 3 journées (seuils = déciles de l'échantillon d'exploration, descriptif seulement,
      10 cellules), sur la fenêtre 11:00 → 16:55.
  B2. 4 règles ex ante sur 11:00 → 16:55 : trader seulement si la hausse du yen sur 3 journées dépasse son quantile
      glissant sur 250 jours (connu la veille), q ∈ {0,5 ; 0,7 ; 0,8 ; 0,9}. Références : R4 et tous les jours.
Mesure de choix (figée) : rapport gain / bruit par trade = net moyen / écart type du trade. Seuil d'intérêt 0,15.
Choix : la meilleure fenêtre A2 et le meilleur seuil B2 selon ce rapport, puis barrière B1 (fab.protocole) avec
n_famille = 98 + 42 (essais antérieurs sur le yen pris en compte dans le DSR : N = 140).
La combinaison fenêtre × seuil (C) et le stop viendront dans une grille séparée, figée après lecture de A + B.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from fab.protocole import barriere_exploration, fiche, nw_t

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/yen_derive_ab")
NY = "America/New_York"
FIN_EXPLO = pd.Timestamp("2023-07-01", tz=NY)
MULT, TICK, FEE = 12_500_000, 0.0000005, 5.0
N_FAMILLE = 140
LINES: list[str] = []


def say(s=""):
    print(s)
    LINES.append(str(s))


def prix(df: pd.DataFrame, hhmm: str) -> pd.Series:
    h, m = map(int, hhmm.split(":"))
    mins = df.index.hour * 60 + df.index.minute
    sel = df[(mins >= h * 60 + m) & (mins < h * 60 + m + 5)]
    first = sel.groupby(sel.index.date).head(1)
    s = pd.Series(first.open.values, index=pd.to_datetime(first.index.date))
    return s[s.index.dayofweek < 5]


def hhmm(x: float) -> str:
    return f"{int(x):02d}:{int(round((x % 1) * 60)):02d}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("D:/quant-data/Cotations/forex/6J_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    df.index = df.index.tz_convert(NY)
    df = df[df.index < FIN_EXPLO]  # réserve coupée avant tout calcul
    cache: dict[str, pd.Series] = {}

    def p(t):
        if t not in cache:
            cache[t] = prix(df, t)
        return cache[t]

    def trade(t0, t1):
        a, b = p(t0), p(t1)
        d = pd.concat([a, b], axis=1, join="inner").dropna()
        brut = -1e4 * np.log(d.iloc[:, 1] / d.iloc[:, 0])
        cout = 1e4 * (TICK * MULT + FEE) / (MULT * d.iloc[:, 0])
        return brut, brut - cout, 1e4 * TICK / d.iloc[:, 0]

    p1655 = p("16:55")
    jour = 1e4 * np.log(p1655 / p1655.shift(1))  # rendement 6J 16:55 → 16:55
    h3 = jour.shift(1).rolling(3).sum()  # hausse du yen sur les 3 journées précédentes (connue la veille 16:55)
    r4 = h3 > 0
    say(f"Exploration : {df.index.min().date()} → {df.index.max().date()}")

    # A1 : tranches de 30 min
    bornes = [8 + 0.5 * i for i in range(18)] + [16 + 55 / 60]
    rows = []
    for lab, mask in (("tous", None), ("R4", r4)):
        tot = trade("08:00", "16:55")[0]
        if mask is not None:
            tot = tot[mask.reindex(tot.index).fillna(False)]
        for a, b in zip(bornes[:-1], bornes[1:]):
            g, n, _ = trade(hhmm(a), hhmm(b))
            if mask is not None:
                g = g[mask.reindex(g.index).fillna(False)]
            rows.append({"jours": lab, "tranche": f"{hhmm(a)}-{hhmm(b)}", "n": len(g), "brut": g.mean(), "ecart_type": g.std(),
                         "t_nw": nw_t(g), "part_derive_%": 100 * g.mean() / tot.mean()})
    A1 = pd.DataFrame(rows)
    A1.to_csv(OUT / "tranches.csv", index=False)
    say("\n== A1. Tranches de 30 min (brut, bp)")
    say(A1.round(2).to_string(index=False))

    # A2 : fenêtres
    rows = []
    for lab, mask in (("tous", None), ("R4", r4)):
        rb, rn, _ = trade("11:00", "16:55")
        for dep in range(8, 17):
            for dur in (1, 2, 3):
                fin = min(dep + dur, 16 + 55 / 60)
                if dep + dur > 17 or (dur > 1 and dep + dur - 1 >= 17):
                    continue
                g, n, tk = trade(hhmm(dep), hhmm(fin))
                if mask is not None:
                    keep = mask.reindex(g.index).fillna(False)
                    g, n, tk = g[keep], n[keep], tk[keep]
                ref = rn.reindex(n.index)
                rows.append({"jours": lab, "fenetre": f"{hhmm(dep)}-{hhmm(fin)}", "n": len(n), "brut": g.mean(), "net": n.mean(),
                             "ecart_type": n.std(), "gain_bruit": n.mean() / n.std(), "t_nw": nw_t(n),
                             "ref_11_1655_net": ref.mean(), "t_ecart_ref": nw_t((n - ref).dropna()),
                             "_n": n, "_g": g, "_tk": tk, "_ref": ref})
    A2 = pd.DataFrame(rows)
    A2.drop(columns=[c for c in A2 if c.startswith("_")]).to_csv(OUT / "fenetres.csv", index=False)
    say(f"\n== A2. Fenêtres ({len(A2)} règles), triées par gain / bruit")
    say(A2.drop(columns=[c for c in A2 if c.startswith("_")]).sort_values("gain_bruit", ascending=False).round(3).to_string(index=False))

    # B1 : déciles de la hausse sur 3 journées
    rb, rn, rtk = trade("11:00", "16:55")
    d = pd.concat([rb.rename("brut"), rn.rename("net"), h3.rename("h3")], axis=1).dropna()
    d["dec"] = pd.qcut(d.h3, 10, labels=[f"D{i}" for i in range(1, 11)])
    B1 = d.groupby("dec", observed=True).agg(n=("net", "size"), h3_moy=("h3", "mean"), brut=("brut", "mean"), net=("net", "mean"),
                                              ecart_type=("net", "std"))
    B1["gain_bruit"] = B1.net / B1.ecart_type
    B1["t_nw"] = d.groupby("dec", observed=True).net.apply(nw_t)
    B1.to_csv(OUT / "deciles.csv")
    say("\n== B1. Déciles de la hausse du yen sur 3 journées (D1 = forte baisse, D10 = forte hausse), fenêtre 11:00 → 16:55")
    say(B1.round(3).to_string())

    # B2 : seuils glissants
    rows = []
    allnet = rn
    for q in (0.5, 0.7, 0.8, 0.9):
        seuil = h3.rolling(250).quantile(q)
        cond = (h3 > seuil) & seuil.notna()
        keep = cond.reindex(rn.index).fillna(False)
        n, g = rn[keep], rb[keep]
        rows.append({"regle": f"h3 > q{q:g} glissant 250 j", "n": len(n), "jours_%": 100 * keep.mean(), "brut": g.mean(), "net": n.mean(),
                     "ecart_type": n.std(), "gain_bruit": n.mean() / n.std(), "t_nw": nw_t(n),
                     "_n": n, "_g": g, "_tk": rtk[keep]})
    for nom, keep in (("R4 (h3 > 0)", r4.reindex(rn.index).fillna(False)), ("tous les jours", pd.Series(True, index=rn.index))):
        n = rn[keep]
        rows.append({"regle": nom, "n": len(n), "jours_%": 100 * keep.mean(), "brut": rb[keep].mean(), "net": n.mean(),
                     "ecart_type": n.std(), "gain_bruit": n.mean() / n.std(), "t_nw": nw_t(n)})
    B2 = pd.DataFrame(rows)
    B2.drop(columns=[c for c in B2 if c.startswith("_")]).to_csv(OUT / "seuils.csv", index=False)
    say("\n== B2. Seuils ex ante sur la hausse du yen (fenêtre 11:00 → 16:55)")
    say(B2.drop(columns=[c for c in B2 if c.startswith("_")]).round(3).to_string(index=False))

    # choix et barrière
    say(f"\n== Choix (gain / bruit max) et barrière B1, N = {N_FAMILLE}")
    bestA = A2.loc[A2.gain_bruit.idxmax()]
    fA = fiche(bestA._n, bestA._g, bestA._ref, n_famille=N_FAMILLE, tick_bp=bestA._tk)
    okA, rA = barriere_exploration(fA)
    say(f"A : {bestA.jours} {bestA.fenetre} : gain / bruit {bestA.gain_bruit:.3f} (seuil 0,15 : {'✅' if bestA.gain_bruit >= 0.15 else '❌'}), "
        f"net {fA['net_moy']:+.2f} bp, t NW {fA['t_nw']:.2f}, DSR {fA['dsr_famille']:.3f}, moitiés {fA['net_moitie1']:+.2f} / {fA['net_moitie2']:+.2f}")
    say("   " + " ; ".join(rA))
    b2 = B2[B2.regle.str.startswith("h3 >")]
    bestB = b2.loc[b2.gain_bruit.idxmax()]
    refB = allnet.reindex(bestB._n.index)
    fB = fiche(bestB._n, bestB._g, None, n_famille=N_FAMILLE, tick_bp=bestB._tk)
    sk = ~allnet.index.isin(bestB._n.index)
    fB["t_ecart_ref"] = float((bestB._n.mean() - allnet[sk].mean()) / np.sqrt(bestB._n.var() / len(bestB._n) + allnet[sk].var() / sk.sum()))
    okB, rB = barriere_exploration(fB)
    say(f"B : {bestB.regle} : gain / bruit {bestB.gain_bruit:.3f} (seuil 0,15 : {'✅' if bestB.gain_bruit >= 0.15 else '❌'}), "
        f"net {fB['net_moy']:+.2f} bp, t NW {fB['t_nw']:.2f}, DSR {fB['dsr_famille']:.3f}, moitiés {fB['net_moitie1']:+.2f} / {fB['net_moitie2']:+.2f}, "
        f"t pris − sautés {fB['t_ecart_ref']:.2f}")
    say("   " + " ; ".join(rB))
    (OUT / "summary.txt").write_text("\n".join(LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
