"""Short du yen en session US filtré R4 (yen en hausse sur les 3 journées précédentes) avec stop obligatoire
(contrainte prop firm) — exploratoire, données déjà vues (6J 2017-01-30 → 2026-08-28, même échantillon que
run_jpy_us_filtres.py ; rien après le 2026-08-28 : holdout du n° 28).

uv run python -X utf8 run_jpy_us_r4_stops.py   → results/jpy_us_r4_stops/ (grid.csv, summary.txt, trades_<id>.parquet)

Pas de réserve possible sur 6J pour cette question : l'effet des stops a déjà été calculé sur toutes les années
(12 SL/TP et 8 trailings sur tous les jours, dont les jours R4). La confirmation se fera sur USDJPY au comptant
2003-2009 (n° 29) puis sur le holdout du n° 28.

Grille figée avant tout calcul (2026-11-21) — 8 essais, compteur 1 814 → 1 822. Jours : R4 seulement.
Entrée short 6J à l'open de la barre 11:00 ET, sortie au stop, au TP éventuel ou à 16:55 ET (open).
  S1-S3 : SL = k × ATR de Wilder 14 H1 à 11:00, k ∈ {2, 3, 4}, pas de TP ;
  S4-S6 : SL = k × σ20, σ20 = écart type des 20 fenêtres 11:00 → 16:55 précédentes (tous les jours), k ∈ {1 ; 1,5 ; 2},
          pas de TP ;
  S7    : SL = 2 ATR H1, TP = 3 × SL ;
  S8    : SL = 3 ATR H1, TP = 3 × SL.
Exécution 1 min : open au-delà d'un niveau → sortie à l'open ; SL et TP dans la même minute → SL.
Coût standard 1 tick + 5 $ ; variante avec 1 tick de glissement au SL.
Critère de choix (figé) : le plus grand R net moyen par trade (net / distance du SL), car en prop firm la taille
est fixée par le risque ; à égalité à 0,005 R près, le stop le plus large. Référence : R4 sans stop.
Mesures : R moyen, t NW, % SL / TP / temps, Sharpe net, pire série de pertes, pire creux en R, moitiés.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from fab.protocole import nw_t
from run_jpy_us_sltp import END, FEE_USD, MULT, NY, TICK, atr, build_days

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/jpy_us_r4_stops")
DEBUT = pd.Timestamp("2017-01-30")


def simulate(d: dict, sl: float, tp: float | None) -> tuple[str, float]:
    p0 = d["p_in"]
    s, t = p0 + sl, (p0 - tp if tp is not None else -np.inf)
    o, h, l = d["o"], d["h"], d["l"]
    hit = (h >= s) | (o >= s) | (l <= t) | (o <= t)
    if not hit.any():
        return "temps", d["p_out"]
    i = int(np.argmax(hit))
    if o[i] >= s:
        return "SL", o[i]
    if o[i] <= t:
        return "TP", o[i]
    if h[i] >= s:
        return "SL", s
    return "TP", t


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("D:/quant-data/Cotations/forex/6J_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    df.index = df.index.tz_convert(NY)
    df = df[df.index < END]
    days = build_days(df)
    idx = pd.to_datetime([d["date"] for d in days])
    p_in = pd.Series([d["p_in"] for d in days], index=idx)
    p_out = pd.Series([d["p_out"] for d in days], index=idx)
    brut_all = -1e4 * (p_out / p_in - 1)
    r6j_day = 1e4 * np.log(p_out / p_out.shift(1))
    r4 = r6j_day.shift(1).rolling(3).sum() > 0
    sig20 = brut_all.rolling(20).std().shift(1)  # bp
    a = atr(df, "1h")
    at = a.reindex(pd.DatetimeIndex([d["t_in"] for d in days]).floor("min").map(lambda x: x.replace(minute=0, second=0)),
                   method="ffill").values
    atr_bp = pd.Series(1e4 * at / p_in.values, index=idx)
    keep = r4 & (idx >= DEBUT) & sig20.notna()
    grid = {"S0 sans stop": (None, None)}
    for k in (2, 3, 4):
        grid[f"S{k - 1} SL {k} ATR H1"] = (atr_bp * k, None)
    for j, k in enumerate((1.0, 1.5, 2.0)):
        grid[f"S{4 + j} SL {k:g} σ20"] = (sig20 * k, None)
    grid["S7 SL 2 ATR H1, TP 3R"] = (atr_bp * 2, 3.0)
    grid["S8 SL 3 ATR H1, TP 3R"] = (atr_bp * 3, 3.0)

    rows = []
    for nom, (sl_bp, rr) in grid.items():
        out = []
        for j, d in enumerate(days):
            dt = idx[j]
            if not keep.iat[j]:
                continue
            if sl_bp is None:
                how, px, risk = "temps", d["p_out"], np.nan
            else:
                risk = sl_bp.iat[j]
                sl = risk * d["p_in"] / 1e4
                how, px = simulate(d, sl, rr * sl if rr else None)
            out.append({"date": dt, "p_in": d["p_in"], "p_out": px, "exit": how, "risk_bp": risk})
        t = pd.DataFrame(out).set_index("date")
        t["brut"] = -1e4 * (t.p_out / t.p_in - 1)
        t["net"] = t.brut - 1e4 * (TICK * MULT + FEE_USD) / (MULT * t.p_in)
        t["net_gl"] = t.net - np.where(t.exit == "SL", 1e4 * TICK / t.p_in, 0.0)
        t.to_parquet(OUT / f"trades_{nom.split()[0]}.parquet")
        R = t.net / t.risk_bp
        Rg = t.net_gl / t.risk_bp
        half = len(t) // 2
        streak = (R < 0).astype(int).groupby((R >= 0).cumsum()).sum().max() if R.notna().all() else np.nan
        eqR = R.cumsum()
        rows.append({
            "variante": nom, "n": len(t), "risque_med_bp": t.risk_bp.median(), "SL_%": 100 * (t.exit == "SL").mean(),
            "TP_%": 100 * (t.exit == "TP").mean(), "brut_bp": t.brut.mean(), "net_bp": t.net.mean(),
            "sharpe_net": t.net.mean() / t.net.std() * np.sqrt(252), "t_nw": nw_t(t.net),
            "R_net": R.mean(), "R_net_gliss": Rg.mean(), "R_moitie1": R.iloc[:half].mean(), "R_moitie2": R.iloc[half:].mean(),
            "gagnants_%": 100 * (t.net > 0).mean(), "pire_serie": streak,
            "pire_creux_R": (eqR - eqR.cummax()).min() if R.notna().all() else np.nan,
            "annees_pos": f"{int((t.net.groupby(t.index.year).mean() > 0).sum())}/{t.index.year.nunique()}",
        })
    g = pd.DataFrame(rows)
    g.to_csv(OUT / "grid.csv", index=False)
    cand = g[g.variante != "S0 sans stop"].copy()
    top = cand.R_net.max()
    choix = cand[cand.R_net >= top - 0.005].sort_values("risque_med_bp").iloc[-1].variante
    pd.set_option("display.width", 320)
    s = g.round(3).to_string(index=False) + f"\n\nCritère figé (R net max, à 0,005 R près le stop le plus large) : {choix}"
    print(s)
    (OUT / "summary.txt").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    main()
