"""Backtest exploratoire (données déjà vues, ≤ 2026-08-28) de la règle du n° 28 : short du yen de 11:00 à 16:55 ET.

uv run python run_jpy_us_backtest.py   → results/jpy_us/ (trades_6J.csv, trades_spot.csv, equity.png, summary.txt)

Ce n'est pas une preuve : toute cette histoire est vue (PREREGISTRATION_28.md, référence historique).
Rien après le 2026-08-28 n'est chargé (interdit par le n° 28 entre les lectures).

A. Futures 6J 2016-01 → 2026-08-28 (Databento 1 min, non ajustés : la fenêtre ne contient pas le
   roulement de 00:00 UTC). Entrée = open de la barre 11:00 ET, sortie = open de la barre 16:55 ET
   (première barre disponible dans les 5 min). 1 contrat (12,5 M JPY), short. Portefeuille vectorbt.
   Coûts : 0, 1 tick + 5 $ (standard), 2 ticks + 5 $.
B. Spot USDJPY Dukascopy 1 min 2012-01-11 → 2015-12-31 : achat à l'ask, vente au bid (spread réel),
   + 0 ou 0,5 bp de commission. Période antérieure aux futures du dépôt, mais déjà vue en moyenne (n° 27).
C. Pistes d'explication : même fenêtre sur ES (actions US) et 6E (dollar contre euro) ; régression du
   rendement 6J sur ES et 6E ; part du rendement du jour entier réalisée dans la fenêtre.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import vectorbt as vbt

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/jpy_us")
NY = "America/New_York"
END = pd.Timestamp("2026-08-29", tz=NY)
MULT, TICK = 12_500_000, 0.0000005


def window_prices(df: pd.DataFrame, col_in: str = "open", col_out: str = "open",
                  t_in: str = "11:00", t_out: str = "16:55") -> pd.DataFrame:
    """Prix d'entrée / sortie par date ET : open de la première barre dans [t, t + 5 min)."""
    d = df.copy()
    d.index = d.index.tz_convert(NY)
    d = d[d.index < END]
    rows = {}
    for t, col, name in [(t_in, col_in, "p_in"), (t_out, col_out, "p_out")]:
        h, m = map(int, t.split(":"))
        mins = d.index.hour * 60 + d.index.minute
        sel = d[(mins >= h * 60 + m) & (mins < h * 60 + m + 5)]
        first = sel.groupby(sel.index.date).head(1)
        s = first[col]
        s.index = pd.Index(first.index.date, name="date")
        rows[name] = s
        rows[name + "_ts"] = pd.Series(first.index, index=s.index)
    w = pd.DataFrame(rows).dropna()
    w = w[pd.to_datetime(w.index).dayofweek < 5]
    return w


def vbt_short(w: pd.DataFrame, fee_usd: float) -> vbt.Portfolio:
    """Short 1 contrat 6J par jour : vente à p_in, rachat à p_out ; frais fixes par ordre."""
    ts = pd.concat([w.p_in_ts, w.p_out_ts]).sort_values()
    price = pd.concat([pd.Series(w.p_in.values, index=w.p_in_ts.values),
                       pd.Series(w.p_out.values, index=w.p_out_ts.values)]).sort_index()
    size = pd.concat([pd.Series(-MULT, index=w.p_in_ts.values),
                      pd.Series(MULT, index=w.p_out_ts.values)]).sort_index()
    assert len(ts) == len(price)
    return vbt.Portfolio.from_orders(price, size, fixed_fees=fee_usd / 2, init_cash=100_000, freq="1min")


def stats_line(r_bp: pd.Series, label: str) -> str:
    sh = r_bp.mean() / r_bp.std() * np.sqrt(252)
    return (f"{label:<38} n {len(r_bp):5d} | moy {r_bp.mean():+5.2f} bp | méd {r_bp.median():+5.2f} | "
            f"gagnants {100 * (r_bp > 0).mean():4.1f} % | Sharpe an. {sh:+.2f} | t {sh / np.sqrt(252) * np.sqrt(len(r_bp)):+.2f}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = []

    def say(s=""):
        print(s)
        lines.append(s)

    # ---------------- A. futures 6J
    j = pd.read_parquet("D:/quant-data/Cotations/forex/6J_v0_1m.parquet")
    w = window_prices(j)
    w["gross_bp"] = -1e4 * np.log(w.p_out / w.p_in)  # short 6J
    w["tick_bp"] = 1e4 * TICK / w.p_in
    w["usd_per_bp"] = MULT * w.p_in / 1e4
    say("== A. Futures 6J, short 11:00 → 16:55 ET, 2016-01 → 2026-08-28")
    costs = {"sans coût": 0, "1 tick + 5 $ (standard)": 1, "2 ticks + 5 $": 2}
    pfs = {}
    for lab, k in costs.items():
        fee = 0.0 if k == 0 else k * TICK * MULT + 5.0
        net = w.gross_bp - fee / w.usd_per_bp
        w[f"net_{k}"] = net
        say(stats_line(net, lab))
        pf = vbt_short(w, fee)
        pfs[lab] = pf
        say(f"   vectorbt : P&L total {pf.total_profit():+,.0f} $ sur 1 contrat, drawdown max {pf.max_drawdown():.1%} "
            f"(sur 100 k$), {pf.trades.count()} trades".replace(",", " "))
    net = w["net_1"]
    say("\nPar année (net standard, bp/trade ; $ pour 1 contrat) :")
    y = pd.to_datetime(w.index).year
    pnl_usd = net * w.usd_per_bp
    for yr in sorted(set(y)):
        m = y == yr
        say(f"  {yr} : {net[m].mean():+5.2f} bp, {pnl_usd[m].sum():+8,.0f} $, gagnants {100 * (net[m] > 0).mean():.0f} %".replace(",", " "))
    eq = pnl_usd.cumsum()
    dd = eq - eq.cummax()
    say(f"\nP&L cumulé net (1 contrat) : {eq.iloc[-1]:+,.0f} $ ; pire creux {dd.min():+,.0f} $ ; "
        f"durée du plus long creux {int((dd < 0).astype(int).groupby((dd == 0).cumsum()).sum().max())} trades".replace(",", " "))
    say(f"Pire jour {pnl_usd.min():+,.0f} $, meilleur {pnl_usd.max():+,.0f} $ ; écart type d'un jour {pnl_usd.std():,.0f} $".replace(",", " "))
    say("Par jour de semaine (net bp, rapporté seulement, pas un filtre) : " + ", ".join(
        f"{d} {net[pd.to_datetime(w.index).dayofweek == i].mean():+.2f}" for i, d in enumerate(["lun", "mar", "mer", "jeu", "ven"])))
    w.to_csv(OUT / "trades_6J.csv")

    # ---------------- B. spot 2012-2015
    s = pd.read_parquet("cache/dukascopy/USDJPY_1m.parquet")
    s = s[s.index < pd.Timestamp("2016-01-01", tz="UTC")]
    ws = window_prices(s, "ask_open", "open")  # achat USDJPY à l'ask, vente au bid
    mid = window_prices(s.assign(mid_open=(s.open + s.ask_open) / 2), "mid_open", "mid_open")
    ws["gross_bp"] = 1e4 * np.log(mid.p_out / mid.p_in).reindex(ws.index)
    ws["net_spread_bp"] = 1e4 * np.log(ws.p_out / ws.p_in)
    ws["net_spread_comm_bp"] = ws.net_spread_bp - 0.5
    say("\n== B. Spot USDJPY Dukascopy 2012-01-11 → 2015-12-31 (long USDJPY = short yen)")
    say(stats_line(ws.gross_bp.dropna(), "mid, sans coût"))
    say(stats_line(ws.net_spread_bp, "spread réel bid/ask"))
    say(stats_line(ws.net_spread_comm_bp, "spread réel + 0,5 bp de commission"))
    say(f"   coût médian du spread : {(ws.gross_bp - ws.net_spread_bp).median():.2f} bp")
    ws.to_csv(OUT / "trades_spot.csv")

    # ---------------- C. explications
    say("\n== C. Pistes d'explication (même fenêtre 11:00 → 16:55 ET, 2016-2026-08)")
    es = window_prices(pd.read_parquet("D:/quant-data/Cotations/indices/ES_v0_1m.parquet"))
    e6 = window_prices(pd.read_parquet("D:/quant-data/Cotations/forex/6E_v0_1m.parquet"))
    X = pd.DataFrame({
        "yen": -w.gross_bp,  # rendement du yen (6J long)
        "es": 1e4 * np.log(es.p_out / es.p_in),
        "eur": 1e4 * np.log(e6.p_out / e6.p_in),
    }).dropna()
    say(f"  moyennes (bp) : yen {X.yen.mean():+.2f}, ES {X.es.mean():+.2f}, euro {X.eur.mean():+.2f} ; n {len(X)}")
    say(f"  corrélations : yen-ES {X.yen.corr(X.es):+.2f}, yen-euro {X.yen.corr(X.eur):+.2f}, ES-euro {X.es.corr(X.eur):+.2f}")
    A = np.column_stack([np.ones(len(X)), X.es, X.eur])
    beta, *_ = np.linalg.lstsq(A, X.yen.values, rcond=None)
    res = X.yen.values - A @ beta
    se = np.sqrt(np.diag(np.linalg.inv(A.T @ A)) * res.var(ddof=3))
    say(f"  yen = {beta[0]:+.2f} bp (t {beta[0] / se[0]:+.2f}) + {beta[1]:+.3f}·ES (t {beta[1] / se[1]:+.1f}) "
        f"+ {beta[2]:+.3f}·euro (t {beta[2] / se[2]:+.1f})")
    say(f"  part expliquée par ES : {beta[1] * X.es.mean():+.2f} bp ; par l'euro : {beta[2] * X.eur.mean():+.2f} bp")
    for lab, m in [("ES en hausse", X.es > 0), ("ES en baisse", X.es <= 0)]:
        say(f"  jours {lab} : yen {X.yen[m].mean():+.2f} bp (n {m.sum()})")
    # part de la baisse du yen sur 24 h faite dans la fenêtre
    jd = j.copy()
    jd.index = jd.index.tz_convert(NY)
    jd = jd[jd.index < END]
    close17 = jd.close[(jd.index.hour == 16) & (jd.index.minute >= 50)].groupby(jd.index[(jd.index.hour == 16) & (jd.index.minute >= 50)].date).last()
    day = 1e4 * np.log(close17).diff()
    day.index = pd.Index(day.index, name="date")
    both = pd.DataFrame({"day": day, "win": -w.gross_bp}).dropna()
    both = both[both.day.abs() < 300]  # écarte les sauts de roulement (série non ajustée)
    for a, b in [("2016", "2021"), ("2021", "2027")]:
        m = (pd.to_datetime(both.index) >= a) & (pd.to_datetime(both.index) < b)
        say(f"  {a}-{int(b) - 1} : yen sur 24 h {both.day[m].mean():+.2f} bp/jour, dont fenêtre US {both.win[m].mean():+.2f}, "
            f"reste de la journée {(both.day - both.win)[m].mean():+.2f}")

    # ---------------- graphique
    fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    for k, lab in [(0, "sans coût"), (1, "1 tick + 5 $"), (2, "2 ticks + 5 $")]:
        ax[0].plot(pd.to_datetime(w.index), (w[f"net_{k}"] * w.usd_per_bp).cumsum(), label=lab)
    ax[0].set_ylabel("P&L cumulé, 1 contrat ($)")
    ax[0].legend()
    ax[0].set_title("Short 6J 11:00 → 16:55 ET (données déjà vues)")
    ax[1].fill_between(pd.to_datetime(w.index), dd, 0, color="tab:red", alpha=0.4)
    ax[1].set_ylabel("Creux, net standard ($)")
    fig.tight_layout()
    fig.savefig(OUT / "equity.png", dpi=110)
    (OUT / "summary.txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
