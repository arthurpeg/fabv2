"""Figures des papiers publics (reports/*_paper.html) → reports/figures/*.svg.

uv run python make_paper_figures.py

Aucun nouveau test : les figures tracent des résultats déjà calculés (trades et moyennes annuelles
sauvegardés), sauf le profil horaire de NQ, statistique descriptive sur la tranche explorée
2016-01 → 2026-08-28 (rien dans le holdout).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import run_sessions as rs

OUT = Path("reports/figures")
END = pd.Timestamp("2026-08-28 23:59", tz="America/New_York")
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 10, "axes.linewidth": 0.7, "axes.spines.top": False, "axes.spines.right": False,
    "xtick.direction": "out", "ytick.direction": "out", "svg.fonttype": "none",
})


def nw(x: np.ndarray, lags: int = 5) -> float:
    """t de Newey-West (Bartlett) de la moyenne."""
    xc = x - x.mean()
    n = len(x)
    v = xc @ xc / n
    for k in range(1, lags + 1):
        v += 2 * (1 - k / (lags + 1)) * (xc[k:] @ xc[:-k]) / n
    return x.mean() / np.sqrt(v / n)


def mom_cumulative() -> None:
    t = pd.read_csv("results/nq_nuit_heures/trades.csv")
    t = t[(t.clock == "20:00") & (t.cost == "net")].copy()
    t["night"] = pd.to_datetime(t.night)
    t = t[t.night <= "2026-08-28"]
    c = t.set_index("night").R.cumsum()
    fig, ax = plt.subplots(figsize=(6.3, 2.8))
    ax.plot(c.index, c.values, color="black", lw=0.9)
    for x0, x1, lab in [("2011-07-01", "2015-12-31", "2011–2015\nout of sample\n(pre-registered)"),
                        ("2016-01-01", "2022-12-31", "2016–2022\nin sample"),
                        ("2023-01-01", "2026-08-28", "2023–2026\nout of sample")]:
        ax.axvline(pd.Timestamp(x0), color="0.6", lw=0.5, ls="--")
        ax.text(pd.Timestamp(x0) + pd.Timedelta(days=60), c.max() * 0.97, lab, va="top", fontsize=8, color="0.25")
    ax.set_ylabel("Cumulative net R")
    ax.axhline(0, color="0.4", lw=0.5)
    fig.tight_layout()
    fig.savefig(OUT / "overnight_mom_cumulative.svg")
    plt.close(fig)


def nq_hourly_profile() -> None:
    """Rendement moyen de NQ par demi-heure ET, de 16:00 à 9:30, 2016-01-04 → 2026-08-28."""
    close = rs.load("NQ")["close"]
    if close.index.tz is None:
        close = close.tz_localize("UTC")
    close = close.tz_convert("America/New_York")
    close = close[(close.index >= "2016-01-04") & (close.index <= END)]
    # dernier prix de chaque demi-heure (étiquette = fin) ; l'arrêt 17:00-18:00 est franchi par ffill,
    # le week-end et les jours fériés (plus de 2 tranches vides) ne le sont pas
    px = close.resample("30min", label="right", closed="right").last().ffill(limit=2)
    r = (np.log(px).diff() * 1e4).dropna()
    slots = [f"{h:02d}:{m:02d}" for h in list(range(16, 24)) + list(range(0, 10)) for m in (0, 30)]
    slots = slots[1:slots.index("09:30") + 1]          # fins de 16:30 à 09:30
    slots = [s for s in slots if s not in ("17:30", "18:00")]  # arrêt CME
    lab = r.index.strftime("%H:%M")
    rows = []
    for s in slots:
        x = r[lab == s]

        rows.append((s, x.mean(), nw(x.values), len(x)))
    prof = pd.DataFrame(rows, columns=["end", "mean_bp", "t_nw", "n"])
    prof.to_csv(OUT / "nq_hourly_profile.csv", index=False)
    fig, ax = plt.subplots(figsize=(6.3, 3.0))
    col = ["0.15" if abs(t) >= 1.96 else "0.65" for t in prof.t_nw]
    ax.bar(range(len(prof)), prof.mean_bp, color=col, width=0.75)
    ax.axhline(0, color="black", lw=0.6)
    ticks = [i for i, s in enumerate(prof.end) if s.endswith(":00") or s == "18:30"]
    ax.set_xticks(ticks, [prof.end[i] for i in ticks], rotation=60, fontsize=7.5)
    ax.set_xlabel("End of half-hour (ET)")
    ax.set_ylabel("Mean NQ return (bp)")
    top = ax.get_ylim()[1]
    for s, txt, ha in [("02:30", "Eurex core session 02:00 ", "right"), ("03:30", " London, Xetra 03:00", "left")]:
        i = list(prof.end).index(s) - 0.5
        ax.axvline(i, color="0.5", lw=0.5, ls="--")
        ax.text(i, top * 0.97, txt, ha=ha, va="top", fontsize=7.5, color="0.3")
    fig.tight_layout()
    fig.savefig(OUT / "nq_hourly_profile.svg")
    plt.close(fig)
    print(prof.round(3).to_string())


def yen_figures() -> None:
    y = pd.read_csv("results/zhang/by_year.csv")
    y = y[(y.cur == "JPY") & (y.sess == "us")].sort_values("year")
    t = pd.read_csv("results/jpy_us/trades_6J.csv", parse_dates=["date"])
    t = t[t.date <= "2026-08-28"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.5, 2.7), gridspec_kw={"width_ratios": [1.1, 1]})
    a1.bar(y.year, y.bp, color=["0.2" if p == "O" else "0.6" for p in y.period], width=0.7)
    a1.axhline(0, color="black", lw=0.6)
    a1.set_ylabel("Mean yen return, US session (bp/day)")
    a1.set_xticks([2010, 2014, 2018, 2022, 2026])
    a1.set_title("(a) By year: spot (light), futures (dark)", fontsize=9)
    a2.plot(t.date, t.gross_bp.cumsum(), color="black", lw=0.9, label="Gross")
    a2.plot(t.date, t.net_1.cumsum(), color="0.55", lw=0.9, label="Net, one tick")
    a2.axhline(0, color="0.4", lw=0.5)
    a2.set_ylabel("Cumulative bp, short 6J 11:00–16:55")
    a2.legend(frameon=False, fontsize=8)
    a2.set_title("(b) Short-yen rule, 2016–Aug. 2026", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "yen_us_session.svg")
    plt.close(fig)
    print(y[["period", "year", "bp"]].to_string(index=False))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    mom_cumulative()
    yen_figures()
    nq_hourly_profile()
