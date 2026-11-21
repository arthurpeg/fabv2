"""Short yen filtré R4, SL k × ATR M15 avec TP 2R ou 3R — 8 essais exploratoires, données déjà vues
(6J 2017-01-30 → 2026-08-28), figés avant calcul le 2026-11-21, compteur 1 831 → 1 839.
k ∈ {2, 3, 4, 5} × TP ∈ {2R, 3R}. Mêmes jours, exécution et coût que run_jpy_us_r4_m15.py.
Règle de décision figée : avenant au n° 29 avant tout téléchargement seulement si une variante atteint
+0,046 R (règle du n° 29 + 0,005 R) ; sinon le n° 29 reste tel quel.

uv run python -X utf8 run_jpy_us_r4_m15_tp.py   → results/jpy_us_r4_stops/grid_m15_tp.csv
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
    keep = r4 & (idx >= DEBUT) & brut_all.rolling(20).std().shift(1).notna()
    a = atr(df, "15min")
    at = a.reindex(pd.DatetimeIndex([d["t_in"] for d in days]).floor("min").map(lambda x: x.replace(minute=0, second=0)),
                   method="ffill").values
    atr_bp = pd.Series(1e4 * at / p_in.values, index=idx)
    rows = []
    for k in (2, 3, 4, 5):
        for rr in (2.0, 3.0):
            out = []
            for j, d in enumerate(days):
                if not keep.iat[j]:
                    continue
                risk = k * atr_bp.iat[j]
                sl = risk * d["p_in"] / 1e4
                how, px = simulate(d, sl, rr * sl)
                out.append({"date": idx[j], "p_in": d["p_in"], "p_out": px, "exit": how, "risk_bp": risk})
            t = pd.DataFrame(out).set_index("date")
            t["net"] = -1e4 * (t.p_out / t.p_in - 1) - 1e4 * (TICK * MULT + FEE_USD) / (MULT * t.p_in)
            t["net_gl"] = t.net - np.where(t.exit == "SL", 1e4 * TICK / t.p_in, 0.0)
            R = t.net / t.risk_bp
            half = len(t) // 2
            eqR = R.cumsum()
            rows.append({
                "variante": f"SL {k} ATR M15, TP {rr:g}R", "risque_med_bp": t.risk_bp.median(),
                "SL_%": 100 * (t.exit == "SL").mean(), "TP_%": 100 * (t.exit == "TP").mean(),
                "net_bp": t.net.mean(), "t_nw": nw_t(t.net), "R_net": R.mean(), "R_net_gliss": (t.net_gl / t.risk_bp).mean(),
                "R_moitie1": R.iloc[:half].mean(), "R_moitie2": R.iloc[half:].mean(),
                "gagnants_%": 100 * (R > 0).mean(),
                "pire_serie": int((R < 0).astype(int).groupby((R >= 0).cumsum()).sum().max()),
                "pire_creux_R": (eqR - eqR.cummax()).min(),
                "annees_pos": f"{int((t.net.groupby(t.index.year).mean() > 0).sum())}/{t.index.year.nunique()}",
            })
    g = pd.DataFrame(rows)
    g.to_csv(OUT / "grid_m15_tp.csv", index=False)
    pd.set_option("display.width", 300)
    best = g.R_net.max()
    s = g.round(3).to_string(index=False) + f"\n\nMeilleur R : {best:+.3f} ; seuil d'avenant +0.046 → " + \
        ("AVENANT au n° 29" if best >= 0.046 else "n° 29 inchangé")
    print(s)
    (OUT / "summary_m15_tp.txt").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    main()
