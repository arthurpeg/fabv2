"""Stratégie NQ overnight long 20:05 -> 03:00 ET avec filtre 3 nuits (scripts_strategies_NQ.zip, transmis le
2026-11-03, bt_overnight_long.py / sl_atr_overnight_long.py / sl2atr15_overnight_long.py) refaite avec vectorbt.

EXPLORATOIRE, hors compteur : on refait un backtest externe déjà fait, sans rien choisir. Le filtre (3 nuits,
seuil 0 bps) a été choisi par l'auteur d'origine parmi plusieurs essais (ATR, range, nuit précédente, rendement
de la journée) : les t ci-dessous ne sont pas corrigés pour cette sélection. S'arrête au 2026-08-28 (holdout intact).

uv run python run_nq_nuit_3n_vbt.py [--replique] → results/nq_nuit_3n/[replique/] (run.log, nuits.csv, trades_<variante>.csv, comparaison.csv)

Règles (docstrings d'origine) :
  - NQ.v.0 Databento 1 min, NON ajusté (points réels), regroupé en barres 5 et 15 min horodatées au début, heure NY ;
    séance CME : une barre à partir de 18:00 appartient à la séance du lendemain.
  - Entrée à l'open de la 1re barre 5 min de 20:05 à 20:30 ; sortie à l'open de la 1re barre de 03:00 à 03:30 de la
    même séance. Les roulements .v.0 tombent à 00:00 UTC (19:00 ou 20:00 NY), avant l'entrée : contrôlé par le plus
    grand saut open / close précédent pendant un trade.
  - REF : long chaque nuit. 3n : long seulement si la somme des rendements (bps) des 3 nuits précédentes <= 0.
  - SL : stop à 2 x ATR(14) de Wilder sur barres 15 min, dernière barre terminée à l'entrée (19:45-20:00),
    vérifié sur les plus bas 5 min de la barre d'entrée à la barre avant 03:00 ; fill au stop ou à l'open si gap.
  - 1 NQ = 20 $ / point, 7,50 $ par ordre (15 $ l'aller-retour). 1 R = 2 x ATR M15 x 20 $ pour toutes les variantes.
  - Sharpe en $ : P&L net par jour de sortie, jours sans trade à 0 $ (jours = dates de sortie de toutes les nuits de
    la période), x racine(252). t Newey-West : moyenne par trade, 5 retards (Bartlett).

vectorbt : Portfolio.from_signals sur les barres 5 min (OHLC réels), prix d'exécution = open, size = 20 (un point de
prix vaut 20 $), sl_stop = distance / prix d'entrée avec stop_entry_price = prix d'exécution ; haut et bas de la
barre de 03:00 ramenés à son open (vectorbt testerait sinon le stop sur toute la barre avant la sortie à l'open). Le compte fait
1e7 $ pour que vectorbt n'ait jamais de manque de liquidités ; les stats « compte de 100 000 $ » ramènent la valeur
à 100 000 $ + P&L cumulé. Contrôle : une boucle à la main (copie de la règle d'origine) donne les mêmes sorties,
trade par trade.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt
import warnings

warnings.filterwarnings("ignore", message="Metric .* requires benchmark_rets")

sys.stdout.reconfigure(encoding="utf-8")
SRC = Path("D:/quant-data/Cotations/indices/NQ_v0_1m.parquet")
OUT = Path("results/nq_nuit_3n")
NY = "America/New_York"
PV, FEE, K_SL, NW_LAGS = 20.0, 7.5, 2.0, 5
CASH, ACCOUNT = 1e7, 1e5
END = pd.Timestamp("2026-08-29", tz=NY)
PERIODS = {"2016-2024 (IS)": (2016, 2024), "2016-2021": (2016, 2021), "2022-2024": (2022, 2024),
           "2025-08/2026 (OOS)": (2025, 2026)}
VARIANTES = {"REF 03h": ("all", False), "REF 03h SL": ("all", True), "3n 03h": ("3n", False), "3n 03h SL": ("3n", True)}
LOG: list[str] = []
# --replique : séances calculées comme dans l'original (lundis après le passage à l'heure d'hiver perdus), pour
# vérifier qu'on retrouve ses chiffres ; sinon séances corrigées
REPLIQUE = "--replique" in sys.argv
if REPLIQUE:
    OUT = OUT / "replique"


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def bars() -> tuple[pd.DataFrame, pd.DataFrame]:
    m = pd.read_parquet(SRC)
    m = m[~m.index.duplicated()].sort_index()
    agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    b5, b15 = (m.resample(f).agg(agg).dropna(subset=["open"]) for f in ("5min", "15min"))
    for b in (b5, b15):
        b.index = b.index.tz_convert(NY)
    b5 = b5[b5.index < END]
    # date locale naïve + 1 jour : le « normalize() + 1 jour » de l'original, en heure tz-aware, tombe à 23:00 du
    # dimanche du passage à l'heure d'hiver (nuit perdue) ; voir REPLIQUE
    d = b5.index.tz_localize(None).normalize() + pd.to_timedelta((b5.index.hour >= 18).astype(int), unit="D")
    b5["session"] = d
    if REPLIQUE:
        orig = (b5.index.normalize() + pd.to_timedelta((b5.index.hour >= 18).astype(int), unit="D")).tz_localize(None)
        b5["session"] = orig.normalize()
    return b5, b15


def atr_wilder(b: pd.DataFrame, n: int = 14) -> pd.Series:
    pc = b.close.shift()
    tr = pd.concat([b.high - b.low, (b.high - pc).abs(), (b.low - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def nuits(b5: pd.DataFrame, b15: pd.DataFrame) -> pd.DataFrame:
    t = b5.index.hour * 60 + b5.index.minute
    pos = pd.DataFrame({"pos": np.arange(len(b5)), "session": b5.session.values})
    ent = pos[(t >= 20 * 60 + 5) & (t <= 20 * 60 + 30)].groupby("session").head(1)
    ext = pos[(t >= 3 * 60) & (t <= 3 * 60 + 30)].groupby("session").head(1)
    n = ent.merge(ext, on="session", suffixes=("_in", "_out"))
    n["entry_time"], n["exit_time"] = b5.index[n.pos_in], b5.index[n.pos_out]
    o = b5.open.values
    n["entry_px"], n["exit_px"] = o[n.pos_in], o[n.pos_out]
    gap = np.abs(o[1:] / b5.close.values[:-1] - 1)
    n["max_gap_bps"] = [gap[a:z].max() * 1e4 for a, z in zip(n.pos_in, n.pos_out)]
    n["ret_bps"] = (n.exit_px / n.entry_px - 1) * 1e4
    n["r3_bps"] = n.ret_bps.shift(1).rolling(3).sum()
    n["sig3n"] = n.r3_bps <= 0
    # ATR M15 de la dernière barre terminée à l'entrée (fin de barre = début + 15 min)
    a = atr_wilder(b15)
    a.index = a.index + pd.Timedelta(minutes=15)
    n["dist"] = K_SL * a.reindex(n.entry_time, method="ffill").values
    n["year"] = n.exit_time.dt.year
    return n


def stops_main(b5: pd.DataFrame, n: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Contrôle : la règle de stop d'origine écrite à la main (plus bas de la barre d'entrée à la barre avant 03:00)."""
    lo, op = b5.low.values, b5.open.values
    px, hit = n.exit_px.values.copy(), np.zeros(len(n), bool)
    for i, (a, z, e, d) in enumerate(zip(n.pos_in, n.pos_out, n.entry_px, n.dist)):
        j = np.flatnonzero(lo[a:z] <= e - d)
        if len(j):
            px[i], hit[i] = min(e - d, op[a + j[0]]), True
    return px, hit


def portefeuille(b5: pd.DataFrame, n: pd.DataFrame) -> vbt.Portfolio:
    """Un portefeuille vectorbt par variante (colonnes) sur la fenêtre couverte par les nuits n."""
    a, z = n.pos_in.min(), n.pos_out.max() + 1
    sub = b5.iloc[a:z]
    pin, pout = n.pos_in.values - a, n.pos_out.values - a
    cols = list(VARIANTES)
    e = pd.DataFrame(False, index=sub.index, columns=cols)
    x, sl = e.copy(), pd.DataFrame(np.nan, index=sub.index, columns=cols)
    for c, (filt, stop) in VARIANTES.items():
        m = n.sig3n.values if filt == "3n" else np.ones(len(n), bool)
        e.iloc[pin[m], cols.index(c)] = True
        x.iloc[pout[m], cols.index(c)] = True
        if stop:
            sl.iloc[pin[m], cols.index(c)] = (n.dist / n.entry_px).values[m]
    # la barre de 03:00 ne sert qu'à son open : sinon vectorbt teste le stop sur tout son range AVANT la sortie à l'open
    hi, lo = sub.high.copy(), sub.low.copy()
    hi.iloc[pout], lo.iloc[pout] = sub.open.values[pout], sub.open.values[pout]
    bc = lambda s: pd.DataFrame({c: s.values for c in cols}, index=sub.index)
    return vbt.Portfolio.from_signals(
        close=bc(sub.close), open=bc(sub.open), high=bc(hi), low=bc(lo), price=bc(sub.open),
        entries=e, exits=x, sl_stop=sl, stop_entry_price="price", size=PV, size_type="amount", fixed_fees=FEE,
        init_cash=CASH, direction="longonly", accumulate=False, freq="5min")


def nw_t(x: np.ndarray, lags: int = NW_LAGS) -> float:
    x = np.asarray(x, float)
    u, T = x - x.mean(), len(x)
    s = u @ u / T + 2 * sum((1 - k / (lags + 1)) * (u[k:] @ u[:-k]) / T for k in range(1, lags + 1))
    return x.mean() / np.sqrt(s / T)


def stats_dollars(tr: pd.DataFrame, days: list) -> dict:
    """tr : trades vectorbt d'une variante sur une période (pnl $ net, R, exit_time, hit)."""
    pnl = tr.pnl.values
    daily = tr.groupby(tr.exit_time.dt.date).pnl.sum().reindex(days, fill_value=0.0)
    eq = np.concatenate([[0.0], pnl.cumsum()])
    w, l = pnl[pnl > 0], pnl[pnl <= 0]
    ans = len(days) / 252
    return {
        "Trades": len(pnl), "Trades/an": len(pnl) / ans, "% stoppés": 100 * tr.hit.mean(),
        "Net $": pnl.sum(), "Net $/an": pnl.sum() / ans, "Espérance $/trade": pnl.mean(),
        "Rendement net (bps/trade)": tr.ret_net_bps.mean(),
        "Taux de réussite %": 100 * len(w) / len(pnl), "RR": w.mean() / -l.mean(), "Profit factor": w.sum() / -l.sum(),
        "Sharpe": daily.mean() / daily.std() * np.sqrt(252),
        "Sortino": daily.mean() / np.sqrt((daily.clip(upper=0) ** 2).mean()) * np.sqrt(252),
        "Max DD $": -(eq - np.maximum.accumulate(eq)).min(), "Pire trade $": pnl.min(),
        "t NW": nw_t(pnl), "E[R]": tr.R.mean(), "R/an": tr.R.sum() / ans,
        "Max DD R": -(np.r_[0, tr.R.cumsum()] - np.maximum.accumulate(np.r_[0, tr.R.cumsum()])).min(),
    }


# chiffres du rapport d'origine (artefact « Rapport NQ overnight », section 5 et 8), pour comparaison
ORIGINE = {
    ("REF 03h", "2016-2024 (IS)"): dict(Trades=2313, NetAn=9393, WR=52.75, PF=1.14, Sharpe=0.63, DD=19200, tNW=2.24, ER=0.04),
    ("REF 03h SL", "2016-2024 (IS)"): dict(Trades=2313, NetAn=6927, WR=48.94, PF=1.11, Sharpe=0.54, DD=12550, tNW=1.92, ER=0.03),
    ("3n 03h", "2016-2024 (IS)"): dict(Trades=982, NetAn=13594, WR=57.54, PF=1.53, Sharpe=1.29, DD=20165, tNW=3.74, ER=0.13),
    ("3n 03h SL", "2016-2024 (IS)"): dict(Trades=982, NetAn=12142, WR=53.26, PF=1.49, Sharpe=1.36, DD=12073, tNW=4.35, ER=0.12),
    ("3n 03h", "2016-2021"): dict(Trades=None, NetAn=16394, WR=60.31, PF=1.91, Sharpe=1.86, DD=8545, tNW=4.00, ER=0.19),
    ("3n 03h SL", "2016-2021"): dict(Trades=None, NetAn=13335, WR=55.16, PF=1.70, Sharpe=1.65, DD=4870, tNW=4.32, ER=0.16),
    ("3n 03h", "2022-2024"): dict(Trades=None, NetAn=8004, WR=52.34, PF=1.19, Sharpe=0.60, DD=20165, tNW=1.12, ER=0.02),
    ("3n 03h SL", "2022-2024"): dict(Trades=None, NetAn=9760, WR=49.71, PF=1.26, Sharpe=0.93, DD=12073, tNW=1.74, ER=0.05),
    ("REF 03h", "2025-08/2026 (OOS)"): dict(Trades=427, NetAn=13211, WR=55.74, PF=1.07, Sharpe=0.39, DD=33895, tNW=0.63, ER=0.01),
    ("REF 03h SL", "2025-08/2026 (OOS)"): dict(Trades=427, NetAn=26862, WR=51.99, PF=1.17, Sharpe=0.96, DD=16626, tNW=1.54, ER=0.05),
    ("3n 03h", "2025-08/2026 (OOS)"): dict(Trades=181, NetAn=34890, WR=62.43, PF=1.53, Sharpe=1.57, DD=10605, tNW=2.24, ER=0.17),
    ("3n 03h SL", "2025-08/2026 (OOS)"): dict(Trades=181, NetAn=32103, WR=55.80, PF=1.52, Sharpe=1.63, DD=8301, tNW=2.25, ER=0.15),
}
CLES = {"Trades": "Trades", "NetAn": "Net $/an", "WR": "Taux de réussite %", "PF": "Profit factor", "Sharpe": "Sharpe",
        "DD": "Max DD $", "tNW": "t NW", "ER": "E[R]"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    b5, b15 = bars()
    n = nuits(b5, b15)
    say(f"Données : {b5.index[0]} -> {b5.index[-1]} ({len(b5):,} barres 5 min)")
    say(f"Nuits : {len(n):,} | signal 3n : {int(n.sig3n.sum())} | à plat : {int((~n.sig3n & n.r3_bps.notna()).sum())} | "
        f"sans signal : {int(n.r3_bps.isna().sum())} | entrées décalées : "
        f"{int((n.entry_time.dt.hour * 60 + n.entry_time.dt.minute != 20 * 60 + 5).sum())}")
    say(f"Plus grand saut open/close précédent pendant un trade : {n.max_gap_bps.max():.1f} bps (pas de roulement)")
    n.to_csv(OUT / "nuits.csv", index=False)

    ctrl_px, ctrl_hit = stops_main(b5, n)
    rows, years, vbt_stats, trades_all = [], [], {}, {}
    for p, (y0, y1) in PERIODS.items():
        np_ = n[n.year.between(y0, y1)].reset_index(drop=True)
        days = sorted(set(np_.exit_time.dt.date))
        pf = portefeuille(b5, np_)
        for c, (filt, stop) in VARIANTES.items():
            m = np_.sig3n.values if filt == "3n" else np.ones(len(np_), bool)
            sel = np_[m].reset_index(drop=True)
            rec = pf[c].trades.records_readable
            assert len(rec) == len(sel), (p, c, len(rec), len(sel))
            tr = pd.DataFrame({"entry_time": sel.entry_time, "exit_time": rec["Exit Timestamp"].values,
                               "entry_px": rec["Avg Entry Price"].values, "exit_px": rec["Avg Exit Price"].values,
                               "pnl": rec["PnL"].values, "dist": sel.dist})
            assert (tr.entry_px.values == sel.entry_px.values).all()
            tr["hit"] = tr.exit_time.values != sel.exit_time.values
            tr["R"] = tr.pnl / (tr.dist * PV)
            tr["ret_net_bps"] = (tr.pnl / (PV * tr.entry_px)) * 1e4
            # contrôle : sorties vectorbt = boucle à la main (variantes SL) ou open de 03:00 (sans SL)
            idx = np.flatnonzero(n.year.between(y0, y1).values)[m]
            ref_px = ctrl_px[idx] if stop else n.exit_px.values[idx]
            ecart = np.abs(tr.exit_px.values - ref_px)
            if p == "2016-2024 (IS)" or p == "2025-08/2026 (OOS)":
                say(f"Contrôle {c:10s} {p:20s} : {len(tr)} trades, sorties différentes de la boucle : "
                    f"{int((ecart > 1e-9).sum())} (écart max {ecart.max():.2f} pt), stops vbt {int(tr.hit.sum())} / "
                    f"boucle {int(ctrl_hit[idx].sum()) if stop else 0}")
                trades_all[(c, p)] = tr
            rows.append({"variante": c, "période": p, **stats_dollars(tr, days)})
            if p in ("2016-2024 (IS)", "2025-08/2026 (OOS)"):
                # stats vectorbt d'un compte de 100 000 $ (même convention que l'original : rendements par jour)
                v = pf[c].value() - CASH + ACCOUNT
                v = v.resample("1D").last().dropna()
                r = v.pct_change().fillna(v.iloc[0] / ACCOUNT - 1)
                rs = r.vbt.returns(freq="1D", year_freq="252D").stats()
                ts = pf[c].trades.stats()
                vbt_stats[(c, p)] = pd.concat([ts[["Total Records", "Win Rate [%]", "Profit Factor", "Expectancy", "SQN"]],
                                               rs[["Total Return [%]", "Annualized Return [%]", "Annualized Volatility [%]",
                                                   "Max Drawdown [%]", "Sharpe Ratio", "Sortino Ratio", "Calmar Ratio"]]])
        if p == "2016-2024 (IS)" or p == "2025-08/2026 (OOS)":
            for c in VARIANTES:
                tr = trades_all[(c, p)]
                tr.to_csv(OUT / f"trades_{c.replace(' ', '_')}_{y0}-{y1}.csv", index=False)
                years.append(tr.groupby(tr.exit_time.dt.year).pnl.sum().rename(c))
    res = pd.DataFrame(rows)

    say("\n===== Toutes les variantes, par période (vectorbt, 1 NQ, 15 $ l'aller-retour) =====")
    for p in PERIODS:
        say(f"\n--- {p} ---\n{res[res['période'] == p].set_index('variante').drop(columns='période').T.round(2).to_string()}")

    say("\n===== vectorbt : Trades.stats() et Returns.stats() d'un compte de 100 000 $ =====")
    say(pd.DataFrame({f"{c} | {p[:9]}": s for (c, p), s in vbt_stats.items()}).round(2).to_string())

    yr = pd.concat(years, axis=1).groupby(level=0).sum()
    say(f"\n===== P&L net par année ($) =====\n{yr.round(0).to_string()}")

    comp = []
    for (c, p), o in ORIGINE.items():
        r = res[(res.variante == c) & (res["période"] == p)].iloc[0]
        for k, lab in CLES.items():
            if o[k] is not None:
                comp.append({"variante": c, "période": p, "métrique": lab, "origine": o[k], "vectorbt": r[lab],
                             "écart": r[lab] - o[k]})
    comp = pd.DataFrame(comp)
    comp.to_csv(OUT / "comparaison.csv", index=False)
    say("\n===== Comparaison avec le rapport d'origine =====")
    piv = comp.pivot_table(index=["variante", "période"], columns="métrique", values=["origine", "vectorbt"], sort=False)
    say(piv.swaplevel(axis=1).sort_index(axis=1, level=0, sort_remaining=False).round(2).to_string())
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
