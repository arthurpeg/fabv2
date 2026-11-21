"""Short du yen en session US (règle du n° 28) avec filtre de jour : volatilité ou retournement — exploratoire,
données déjà vues (6J 2016-01 → 2026-08-28 ; rien après : holdout du n° 28).

uv run python -X utf8 run_jpy_us_filtres.py   → results/jpy_us_filtres/ (grid.csv, summary.txt)

Grille figée avant tout calcul (2026-11-21) — 8 essais, compteur 1 806 → 1 814. Le trade est toujours le même
(short 6J open 11:00 → open 16:55 ET, 1 tick + 5 $) ; seul le choix des jours change, avec une information
connue avant 11:00 ET.
  V. Volatilité ex ante (trader seulement les jours agités) :
     V1 écart type des 20 fenêtres 11:00-16:55 précédentes > sa médiane glissante sur 250 jours ;
     V2 idem, > tercile haut (quantile 2/3 glissant 250 jours) ;
     V3 ATR de Wilder 14 sur H1 à 11:00 (en bp du prix) > sa médiane glissante sur 250 jours ;
     V4 idem, > tercile haut.
  R. Retournement (short seulement si le yen a MONTÉ récemment, c'est-à-dire si le short a perdu) :
     R1 rendement 6J de la fenêtre 11:00-16:55 de la veille > 0 ;
     R2 somme des rendements 6J des fenêtres des 3 séances précédentes > 0 ;
     R3 rendement 6J de la journée complète précédente (16:55 avant-veille → 16:55 veille) > 0 ;
     R4 somme sur les 3 journées complètes précédentes (16:55 J−4 → 16:55 J−1) > 0.
Référence triviale (fixée avant calcul) : la même position tous les jours (règle du n° 28), et les jours sautés.
Mesures par variante : fiche fab.protocole (net par trade) ; écart pris − sautés (t de Welch) ; Sharpe annuel de la
série quotidienne avec 0 les jours sans trade (comparable à la règle tous les jours) ; DSR à N = 8 et à N = 42
(ces 8 + les 34 coupes descriptives du 2026-11-19, dont les quintiles de volatilité ex ante déjà vus).
Barrière B1 (PROTOCOLE.md). Même si une variante passait, il n'y a plus de réserve sur le yen : étape 4 seulement.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from fab.protocole import barriere_exploration, dsr, fiche
from run_jpy_us_sltp import END, FEE_USD, MULT, NY, TICK, atr, build_days

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/jpy_us_filtres")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("D:/quant-data/Cotations/forex/6J_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    df.index = df.index.tz_convert(NY)
    df = df[df.index < END]
    days = build_days(df)
    t = pd.DataFrame({"p_in": [d["p_in"] for d in days], "p_out": [d["p_out"] for d in days],
                      "t_in": [d["t_in"] for d in days]}, index=pd.to_datetime([d["date"] for d in days]))
    t["brut"] = -1e4 * (t.p_out / t.p_in - 1)
    tick_bp = 1e4 * TICK / t.p_in
    t["net"] = t.brut - 1e4 * (TICK * MULT + FEE_USD) / (MULT * t.p_in)
    r6j_win = -t.brut  # rendement 6J (yen) dans la fenêtre
    r6j_day = 1e4 * np.log(t.p_out / t.p_out.shift(1))  # 16:55 veille → 16:55 jour (connu le lendemain)

    vol = t.brut.rolling(20).std().shift(1)
    a = atr(df, "1h")
    at = a.reindex(pd.DatetimeIndex(t.t_in).map(lambda x: x.replace(minute=0, second=0)), method="ffill").values
    atr_bp = pd.Series(1e4 * at / t.p_in.values, index=t.index)
    filtres = {
        "V1 vol 20 > médiane 250": vol > vol.rolling(250).median(),
        "V2 vol 20 > tercile haut 250": vol > vol.rolling(250).quantile(2 / 3),
        "V3 ATR H1 > médiane 250": atr_bp > atr_bp.rolling(250).median().shift(1),
        "V4 ATR H1 > tercile haut 250": atr_bp > atr_bp.rolling(250).quantile(2 / 3).shift(1),
        "R1 fenêtre veille yen ↑": r6j_win.shift(1) > 0,
        "R2 3 fenêtres yen ↑": r6j_win.shift(1).rolling(3).sum() > 0,
        "R3 journée veille yen ↑": r6j_day.shift(1) > 0,
        "R4 3 journées yen ↑": r6j_day.shift(1).rolling(3).sum() > 0,
    }
    # échantillon commun : jours où toutes les conditions sont définies
    ok = vol.rolling(250).quantile(2 / 3).notna() & atr_bp.rolling(250).quantile(2 / 3).shift(1).notna() \
        & r6j_day.shift(1).rolling(3).sum().notna()
    base = t[ok]
    lines = [f"Échantillon commun : {len(base)} jours, {base.index.min().date()} → {base.index.max().date()}"]
    sh_all = base.net.mean() / base.net.std() * np.sqrt(252)
    lines.append(f"Référence (tous les jours) : net {base.net.mean():+.2f} bp, brut {base.brut.mean():+.2f}, Sharpe {sh_all:.2f}, "
                 f"P&L {(base.net * MULT * base.p_in / 1e4).sum():+,.0f} $".replace(",", " "))
    sharpes = []
    rows = []
    for nom, f in filtres.items():
        f = f.reindex(base.index).fillna(False).astype(bool)
        pris, saut = base.net[f], base.net[~f]
        sharpes.append(pris.mean() / pris.std())
    for (nom, f), _ in zip(filtres.items(), sharpes):
        f = f.reindex(base.index).fillna(False).astype(bool)
        pris, saut = base.net[f], base.net[~f]
        fi = fiche(pris, base.brut[f], None, n_famille=8, sharpes_famille=sharpes, tick_bp=tick_bp[base.index][f])
        tw = stats.ttest_ind(pris, saut, equal_var=False).statistic
        fi["t_ecart_ref"] = tw  # filtre : écart pris − sautés
        quot = base.net.where(f, 0.0)
        ok1, raisons = barriere_exploration(fi)
        rows.append({
            "filtre": nom, "jours_%": 100 * f.mean(), "n": len(pris), "brut_pris": base.brut[f].mean(),
            "net_pris": pris.mean(), "net_sautes": saut.mean(), "t_pris_moins_sautes": tw, "t_nw_pris": fi["t_nw"],
            "sharpe_trade": fi["sharpe_an"], "sharpe_quotidien": quot.mean() / quot.std() * np.sqrt(252),
            "pnl_usd": (pris * MULT * base.p_in[f] / 1e4).sum(), "pire_creux_bp": fi["pire_creux"],
            "annees_pos": fi["annees_pos"], "moitie1": fi["net_moitie1"], "moitie2": fi["net_moitie2"],
            "dsr_8": fi["dsr_famille"], "dsr_42": dsr(pris.values, 42, sharpes), "B1": ok1,
        })
        lines.append(f"\n{nom} : " + " ; ".join(raisons))
    g = pd.DataFrame(rows)
    g.to_csv(OUT / "grid.csv", index=False)
    pd.set_option("display.width", 320)
    s = "\n".join(lines) + "\n\n" + g.round(2).to_string(index=False)
    print(s)
    (OUT / "summary.txt").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    main()
