"""Short yen filtré R4 avec SL en ATR M15 (sans TP) — 4 essais exploratoires, données déjà vues
(6J 2017-01-30 → 2026-08-28), figés avant calcul le 2026-11-21, compteur 1 827 → 1 831.
SL = k × ATR de Wilder 14 sur bougies M15 (dernière bougie terminée à 11:00 ET), k ∈ {2, 3, 4, 5}.
Mêmes jours, même exécution et même coût que run_jpy_us_r4_stops.py (fonction simulate réutilisée).
Règle de décision figée : si une variante dépasse le R net de la règle du n° 29 (SL 2 ATR H1 + TP 3R, +0,041 R)
d'au moins 0,005 R, un avenant au n° 29 est écrit AVANT tout téléchargement ; sinon le n° 29 reste tel quel.

uv run python -X utf8 run_jpy_us_r4_m15.py   → results/jpy_us_r4_stops/grid_m15.csv
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from fab.protocole import nw_t
from run_jpy_us_r4_stops import DEBUT, OUT, simulate
from run_jpy_us_sltp import END, FEE_USD, MULT, NY, TICK, atr, build_days

sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    df = pd.read_parquet("D:/quant-data/Cotations/forex/6J_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    df.index = df.index.tz_convert(NY)
    df = df[df.index < END]
    days = build_days(df)
    idx = pd.to_datetime([d["date"] for d in days])
    p_in = pd.Series([d["p_in"] for d in days], index=idx)
    p_out = pd.Series([d["p_out"] for d in days], index=idx)
    brut_all = -1e4 * (p_out / p_in - 1)
    r4 = (1e4 * np.log(p_out / p_out.shift(1))).shift(1).rolling(3).sum() > 0
    keep = r4 & (idx >= DEBUT) & brut_all.rolling(20).std().shift(1).notna()  # mêmes jours que l'original
    a = atr(df, "15min")
    # dernière bougie M15 terminée au plus tard à l'heure pleine d'entrée (11:00), comme le script d'origine
    at = a.reindex(pd.DatetimeIndex([d["t_in"] for d in days]).floor("min").map(lambda x: x.replace(minute=0, second=0)),
                   method="ffill").values
    atr_bp = pd.Series(1e4 * at / p_in.values, index=idx)
    rows = []
    for k in (2, 3, 4, 5):
        out = []
        for j, d in enumerate(days):
            if not keep.iat[j]:
                continue
            risk = k * atr_bp.iat[j]
            how, px = simulate(d, risk * d["p_in"] / 1e4, None)
            out.append({"date": idx[j], "p_in": d["p_in"], "p_out": px, "exit": how, "risk_bp": risk})
        t = pd.DataFrame(out).set_index("date")
        t["net"] = -1e4 * (t.p_out / t.p_in - 1) - 1e4 * (TICK * MULT + FEE_USD) / (MULT * t.p_in)
        t["net_gl"] = t.net - np.where(t.exit == "SL", 1e4 * TICK / t.p_in, 0.0)
        R = t.net / t.risk_bp
        half = len(t) // 2
        eqR = R.cumsum()
        rows.append({
            "variante": f"SL {k} ATR M15", "n": len(t), "risque_med_bp": t.risk_bp.median(),
            "SL_%": 100 * (t.exit == "SL").mean(), "net_bp": t.net.mean(), "t_nw": nw_t(t.net),
            "sharpe_net": t.net.mean() / t.net.std() * np.sqrt(252), "R_net": R.mean(),
            "R_net_gliss": (t.net_gl / t.risk_bp).mean(), "R_moitie1": R.iloc[:half].mean(), "R_moitie2": R.iloc[half:].mean(),
            "pire_serie": int((R < 0).astype(int).groupby((R >= 0).cumsum()).sum().max()),
            "pire_creux_R": (eqR - eqR.cummax()).min(),
            "annees_pos": f"{int((t.net.groupby(t.index.year).mean() > 0).sum())}/{t.index.year.nunique()}",
        })
    g = pd.DataFrame(rows)
    g.to_csv(OUT / "grid_m15.csv", index=False)
    pd.set_option("display.width", 300)
    best = g.R_net.max()
    s = g.round(3).to_string(index=False) + f"\n\nMeilleur R M15 : {best:+.3f} ; seuil d'avenant : +0.046 → " + \
        ("AVENANT au n° 29" if best >= 0.041 + 0.005 else "n° 29 inchangé")
    print(s)
    (OUT / "summary_m15.txt").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    main()
