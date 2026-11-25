"""Contrôle du carry du future 6J : la baisse du yen en session US se voit-elle aussi au comptant 2016-2025 ?

uv run python run_jpy_spot_carry.py

Question d'un relecteur du papier FX (2026-11-25) : le future 6J intègre le différentiel de taux, et l'effet est
plus fort en 2022-2026, quand ce différentiel a grandi. Si le comptant montre la même baisse, le carry n'en est pas
la cause. Contrôle de robustesse d'un effet existant, pas une nouvelle règle : hors compteur.

Données : USD/JPY comptant Dukascopy M15 (bid), 2013-01 → 2025-06 (tranche explorée, wiki/reserves.md) ;
trades du future 6J 11:00 → 16:55 (results/jpy_us/trades_6J.csv). Fenêtre comptant 11:00 → 16:45 NY (dernière
borne M15 avant la reprise de 17:00). Rien après le 2026-08-28.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SPOT = Path("C:/Users/arthu/strategie trading/data_m15/USDJPY_m15.parquet")
OUT = Path("results/jpy_spot_carry")


def nw_t(x: np.ndarray, lags: int = 5) -> float:
    xc = x - x.mean()
    n = len(x)
    v = xc @ xc / n
    for k in range(1, lags + 1):
        v += 2 * (1 - k / (lags + 1)) * (xc[k:] @ xc[:-k]) / n
    return x.mean() / np.sqrt(v / n)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    s = pd.read_parquet(SPOT)["Close"].tz_convert("America/New_York")
    # barre M15 horodatée au début : le prix à T est la clôture de la barre qui commence à T − 15 min
    end = s.copy()
    end.index = end.index + pd.Timedelta(minutes=15)
    d = pd.DataFrame({"t": end.index.strftime("%H:%M"), "px": end.values}, index=end.index)
    p11 = d[d.t == "11:00"].px
    p1645 = d[d.t == "16:45"].px
    p11.index, p1645.index = p11.index.normalize().tz_localize(None), p1645.index.normalize().tz_localize(None)
    spot = (np.log(p1645 / p11) * 1e4).dropna().rename("spot_bp")  # > 0 : le yen baisse
    spot = spot[spot.index.dayofweek < 5]
    fut = pd.read_csv("results/jpy_us/trades_6J.csv", parse_dates=["date"]).set_index("date").gross_bp.rename("fut_bp")
    both = pd.concat([spot, fut], axis=1, join="inner").dropna()
    both = both[(both.index >= "2016-01-01")]
    rows = []
    for y, g in both.groupby(both.index.year):
        rows.append((y, len(g), g.spot_bp.mean(), g.fut_bp.mean(), (g.fut_bp - g.spot_bp).mean()))
    by = pd.DataFrame(rows, columns=["year", "days", "spot_bp", "fut_bp", "fut_minus_spot_bp"])
    by.to_csv(OUT / "by_year.csv", index=False)
    lines = [
        f"Jours communs : {len(both)} ({both.index.min().date()} → {both.index.max().date()})",
        f"Comptant 11:00-16:45 : {both.spot_bp.mean():+.2f} bp (t NW {nw_t(both.spot_bp.values):.2f})",
        f"Future 11:00-16:55   : {both.fut_bp.mean():+.2f} bp (t NW {nw_t(both.fut_bp.values):.2f})",
        f"Écart future − comptant : {(both.fut_bp - both.spot_bp).mean():+.2f} bp (t NW {nw_t((both.fut_bp - both.spot_bp).values):.2f})",
        f"Corrélation journalière : {both.spot_bp.corr(both.fut_bp):.3f}",
    ]
    for a, b in [("2016", "2021"), ("2022", "2025")]:
        g = both.loc[a:b]
        lines.append(f"{a}-{b} : comptant {g.spot_bp.mean():+.2f} (t {nw_t(g.spot_bp.values):.2f}), "
                     f"future {g.fut_bp.mean():+.2f}, écart {(g.fut_bp - g.spot_bp).mean():+.2f}")
    txt = "\n".join(lines) + "\n\n" + by.round(2).to_string(index=False)
    (OUT / "summary.txt").write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
