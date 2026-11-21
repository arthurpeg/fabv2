"""Short du yen en session US (règle du n° 28) avec trailing stop en ATR — exploratoire, données déjà vues.

uv run python -X utf8 run_jpy_us_trailing.py   → results/jpy_us_trailing/ (grid.csv, trades_<combo>.parquet, summary.txt)

Grille figée avant tout calcul (2026-11-21) — 8 essais, compteur 1 798 → 1 806 :
  distance du trailing = k × ATR de Wilder 14 sur bougies M15 ou H1 (dernière bougie terminée à 11:00 ET),
  k ∈ {1, 2, 3, 4} ; pas de TP. Référence : sans stop (règle du n° 28).
Règle : short 6J à l'open de la barre 11:00 ET. Stop initial = entrée + d ; ensuite stop = plus bas atteint + d
(il ne fait que descendre). Sortie au stop ou à 16:55 ET (open).
Exécution sur barres 1 min : on compare le high de la minute au stop issu des minutes PRÉCÉDENTES, puis on met
à jour le plus bas avec la minute (prudent : pas de baisse puis rebond comptés dans la même minute) ; si l'open
franchit déjà le stop, sortie à l'open. Coût standard 1 tick + 5 $ ; variante avec 1 tick de glissement au stop.
Données : Databento 6J.v.0 1 min, 2016-01 → 2026-08-28 (rien après : holdout du n° 28).
Attendu (rapports SL/TP et distribution) : l'effet est une dérive lente de 2 bp sous 24 bp de bruit ; tout stop
raccourcit l'exposition. Le meilleur des 8 est biaisé vers le haut. La règle du n° 28 ne change pas.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from run_jpy_us_sltp import END, NY, TICK, MULT, FEE_USD, atr, build_days, summarize

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/jpy_us_trailing")
TFS = {"M15": "15min", "H1": "1h"}
KS = [1, 2, 3, 4]


def simulate(days: list[dict], atr_at: np.ndarray | None, k: float) -> pd.DataFrame:
    rows = []
    for j, d in enumerate(days):
        p0 = d["p_in"]
        how, px = "temps", d["p_out"]
        if atr_at is not None:
            dist = k * atr_at[j]
            best = p0
            o, h, l = d["o"], d["h"], d["l"]
            for i in range(len(o)):
                stop = best + dist
                if o[i] >= stop:
                    how, px = "SL", o[i]
                    break
                if h[i] >= stop:
                    how, px = "SL", stop
                    break
                best = min(best, l[i])
        rows.append({"date": d["date"], "p_in": p0, "p_out": px, "exit": how,
                     "risk_bp": np.nan if atr_at is None else 1e4 * k * atr_at[j] / p0})
    t = pd.DataFrame(rows).set_index("date")
    t["gross_bp"] = -1e4 * (t.p_out / t.p_in - 1)
    cost_bp = 1e4 * (TICK * MULT + FEE_USD) / (MULT * t.p_in)
    t["net_bp"] = t.gross_bp - cost_bp
    t["net_slip_bp"] = t.net_bp - np.where(t.exit == "SL", 1e4 * TICK / t.p_in, 0.0)
    t["usd"] = t.net_bp * MULT * t.p_in / 1e4
    return t


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("D:/quant-data/Cotations/forex/6J_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    df.index = df.index.tz_convert(NY)
    df = df[df.index < END]
    days = build_days(df)
    t_in = pd.DatetimeIndex([d["t_in"] for d in days]).floor("min")
    print(f"{len(days)} jours, {days[0]['date']} → {days[-1]['date']}")
    res = []
    t = simulate(days, None, 0)
    r = summarize(t, "sans stop (n° 28)")
    res.append(r)
    for tf, rule in TFS.items():
        a = atr(df, rule)
        at = a.reindex(t_in.map(lambda x: x.replace(minute=0, second=0)), method="ffill").values
        for k in KS:
            lab = f"trailing {k} ATR {tf}"
            t = simulate(days, at, k)
            t.to_parquet(OUT / f"trades_{tf}_k{k}.parquet")
            r = summarize(t, lab)
            stop = t[t.exit == "SL"]
            r["stop_gagnant_%"] = 100 * (stop.gross_bp > 0).mean() if len(stop) else np.nan
            r["brut_moy_stoppes"] = stop.gross_bp.mean() if len(stop) else np.nan
            res.append(r)
    g = pd.DataFrame(res).drop(columns=["TP_%"])
    g.to_csv(OUT / "grid.csv", index=False)
    pd.set_option("display.width", 300)
    s = g.round(2).to_string(index=False)
    print(s)
    (OUT / "summary.txt").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    main()
