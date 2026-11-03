"""Stratégie transmise NQ intraday « close de la barre de 9:30 contre EMA(12) » (scripts_strategies_NQ.zip, 2026-11-03 :
bt_ema930.py, explore_c_ema930.py, bt_m2_ema930.py) refaite avec vectorbt.

EXPLORATOIRE, hors compteur : on refait un backtest externe sans rien choisir (seuils et réglages de l'original).
S'arrête au 2026-08-28 (holdout intact).

uv run python run_nq_ema930_vbt.py → results/nq_ema930/ (run.log, seances.csv, trades_<variante>.csv, stats.csv)

Règles (docstrings d'origine) :
  - NQ.v.0 Databento 1 min non ajusté, barres 5 min horodatées au début, heure NY. EMA(12) des closes et ATR(14) de
    Wilder (M5) sur toutes les barres, Globex compris. Séance = date calendaire des barres 9:30-15:55 ; on garde les
    séances qui ont une barre de 9:30 et une barre de 9:35.
  - Sens : close de la barre de 9:30 (9:30-9:35) > EMA12 -> long, < -> short. Entrée à l'open de 9:35, sortie au close
    de la dernière barre RTH (15:55, ou plus tôt les jours écourtés).
  - C : toutes les séances, sans stop. D : toujours long, sans stop.
  - M2 : seulement si force = |close 9:30 - EMA12| / ATR M5 > 2,2, ou retournement < -60 bps (rendement 9:35 -> 15:55
    de la séance précédente du tableau, signé dans le sens du jour).
  - Stop (variante) : fixe à 4 x ATR(14) M15 de la barre 9:15-9:30, vérifié sur les plus bas / hauts 5 min de la barre
    d'entrée à la barre de sortie ; fill au stop, ou à l'open si gap.
  - Taille / sigma 20 j : contrats = (1 / sigma) / moyenne de (1 / sigma) sur les jours M2 de 2016-2024, arrondi à 0,1
    (MNQ), au moins 0,1 ; sigma = écart-type du mouvement 9:35 -> 15:55 (points) des 20 séances précédentes ; 1 NQ
    tant que sigma manque. Coût 15 $ l'aller-retour par NQ équivalent (7,50 $ x taille par ordre).
vectorbt : Portfolio.from_signals, longs et shorts dans la même colonne (entries / short_entries), prix d'exécution
= open à l'entrée et close à la sortie, size = taille x 20, sl_stop = distance / prix d'entrée (stop_entry_price =
prix d'exécution). Contrôle : boucle à la main recopiée de stop_exit (explore_c_ema930.py).
Stats en $ comme l'original : P&L par séance, séances sans trade à 0 $, Sharpe x racine(252), max DD sur le cumul
journalier, t Newey-West 5 retards par trade.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

import run_nq_nuit_3n_vbt as B

warnings.filterwarnings("ignore", message="Metric .* requires benchmark_rets")
sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/nq_ema930")
PV, FEE, CASH = 20.0, 7.5, 1e7
STR_T, REV_T, K_SL = 2.2, -60.0, 4.0
PERIODS = {"2016-2024 (IS)": (2016, 2024), "2016-2021": (2016, 2021), "2022-2024": (2022, 2024),
           "2025-08/2026 (OOS)": (2025, 2026)}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def seances(b5: pd.DataFrame, b15: pd.DataFrame) -> pd.DataFrame:
    ema = b5.close.ewm(span=12, adjust=False).mean().values
    atr5 = B.atr_wilder(b5).values
    hm = b5.index.hour * 60 + b5.index.minute
    r = pd.DataFrame({"pos": np.arange(len(b5)), "hm": hm, "date": b5.index.date})
    r = r[(hm >= 9 * 60 + 30) & (hm <= 15 * 60 + 55)]
    g = r.groupby("date")
    d = pd.DataFrame({"first_hm": g.hm.first(), "sig": g.pos.first(), "z": g.pos.last()})
    d = d[(d.first_hm == 9 * 60 + 30) & (d.z > d.sig)]
    d["e"] = d.sig + 1
    d = d[hm[d.e.values] == 9 * 60 + 35].reset_index()
    c, o = b5.close.values, b5.open.values
    d["side"] = np.sign(c[d.sig] - ema[d.sig]).astype(int)
    d = d[d.side != 0].reset_index(drop=True)
    d["atr"] = atr5[d.sig]
    d["entry_px"], d["exit_px"] = o[d.e], c[d.z]
    d["entry_time"] = b5.index[d.e]
    d["year"] = pd.DatetimeIndex(pd.to_datetime(d.date)).year
    d["strength"] = np.abs(c[d.sig] - ema[d.sig]) / d.atr
    ret = (d.exit_px / d.entry_px - 1) * 1e4
    d["reversal"] = ret.shift(1) * d.side
    d["m2"] = (d.strength > STR_T) | (d.reversal < REV_T)
    a15 = B.atr_wilder(b15)
    a15.index = a15.index + pd.Timedelta(minutes=15)
    d["atr15"] = a15.reindex(d.entry_time, method="ffill").values
    d["sigma20"] = (d.exit_px - d.entry_px).shift(1).rolling(20).std()
    raw = 1 / d.sigma20.values
    ism = d.year.between(2016, 2024).values & d.m2.values
    size = np.round(raw / np.nanmean(raw[ism]), 1).clip(0.1, None)
    d["size"] = np.where(np.isnan(size), 1.0, size)
    return d


def stop_main(b5: pd.DataFrame, d: pd.DataFrame, dist: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Contrôle : stop_exit d'origine (plus bas / hauts de la barre d'entrée à la barre de sortie incluse)."""
    o, h, lo = b5.open.values, b5.high.values, b5.low.values
    px, hit = d.exit_px.values.astype(float).copy(), np.zeros(len(d), bool)
    for i, (e, z, en, s, ds) in enumerate(zip(d.e, d.z, d.entry_px, d.side, dist)):
        stop = en - s * ds
        j = np.flatnonzero(lo[e:z + 1] <= stop) if s > 0 else np.flatnonzero(h[e:z + 1] >= stop)
        if len(j):
            k = e + j[0]
            px[i], hit[i] = (min(stop, o[k]) if s > 0 else max(stop, o[k])), True
    return px, hit


VARIANTES = {  # nom : (jours, sens, stop, taille)
    "C": ("tous", "signal", False, False),
    "D (toujours long)": ("tous", "long", False, False),
    "M2": ("m2", "signal", False, False),
    "M2 + taille / σ 20 j (retenue)": ("m2", "signal", False, True),
    "M2 + stop 4×ATR M15": ("m2", "signal", True, False),
    "M2 + stop + taille": ("m2", "signal", True, True),
}


def portefeuille(b5: pd.DataFrame, d: pd.DataFrame) -> dict[str, pd.DataFrame]:
    a, z = d.e.min(), d.z.max() + 1
    sub = b5.iloc[a:z]
    e, x = d.e.values - a, d.z.values - a
    cols = list(VARIANTES)
    shape = (len(sub), len(cols))
    le, se, lx, sx = (np.zeros(shape, bool) for _ in range(4))
    sl, size, ff = np.full(shape, np.nan), np.full(shape, np.nan), np.zeros(shape)
    price = np.repeat(sub.close.values[:, None], len(cols), axis=1)
    price[e, :] = sub.open.values[e, None]
    masks = {}
    for j, (c, (jours, sens, stop, taille)) in enumerate(VARIANTES.items()):
        m = d.m2.values if jours == "m2" else np.ones(len(d), bool)
        side = d.side.values if sens == "signal" else np.ones(len(d), int)
        q = d["size"].values if taille else np.ones(len(d))
        masks[c] = (m, side, q)
        le[e[m & (side > 0)], j], se[e[m & (side < 0)], j] = True, True
        lx[x[m & (side > 0)], j], sx[x[m & (side < 0)], j] = True, True
        size[e[m], j] = q[m] * PV
        ff[e[m], j], ff[x[m], j] = FEE * q[m], FEE * q[m]
        if stop:
            sl[e[m], j] = K_SL * d.atr15.values[m] / d.entry_px.values[m]
    df = lambda v: pd.DataFrame(v, index=sub.index, columns=cols)
    bc = lambda s: df(np.repeat(s.values[:, None], len(cols), axis=1))
    pf = vbt.Portfolio.from_signals(
        close=bc(sub.close), open=bc(sub.open), high=bc(sub.high), low=bc(sub.low), price=df(price),
        entries=df(le), exits=df(lx), short_entries=df(se), short_exits=df(sx), sl_stop=df(sl),
        stop_entry_price="price", size=df(size), size_type="amount", fixed_fees=df(ff), init_cash=CASH,
        accumulate=False, freq="5min")
    out = {}
    for c, (m, side, q) in masks.items():
        sel = d[m].reset_index(drop=True)
        rec = pf[c].trades.records_readable
        assert len(rec) == len(sel), (c, len(rec), len(sel))
        out[c] = pd.DataFrame({"date": sel.date, "year": sel.year, "side": side[m], "size": q[m],
                               "entry_px": rec["Avg Entry Price"].values, "exit_px": rec["Avg Exit Price"].values,
                               "pnl": rec["PnL"].values, "exit_time": rec["Exit Timestamp"].values})
        assert (out[c].entry_px.values == sel.entry_px.values).all()
    return out


def stats(t: pd.DataFrame, jours: pd.Series) -> dict:
    daily = t.groupby("date").pnl.sum().reindex(jours, fill_value=0.0).values
    eq = np.cumsum(daily)
    p = t.pnl.values
    w, l = p[p > 0], p[p <= 0]
    ans = len(jours) / 252
    return {"Trades": len(p), "Taille moy. (NQ)": t["size"].mean(), "% stoppés": 100 * t.hit.mean(),
            "Net $": p.sum(), "Net $/an": p.sum() / ans, "$/trade": p.mean(),
            "bps/trade (par NQ)": (p / t["size"] / (t.entry_px * PV)).mean() * 1e4, "Win %": 100 * (p > 0).mean(),
            "PF": w.sum() / -l.sum(), "Sharpe": daily.mean() / daily.std() * np.sqrt(252),
            "Max DD $": -(eq - np.maximum.accumulate(eq)).min(), "Pire trade $": p.min(),
            "Part des 10 meilleurs %": 100 * np.sort(p)[-10:].sum() / p.sum() if p.sum() > 0 else np.nan,
            "t NW": B.nw_t(p), "Longs": int((t.side > 0).sum()), "Shorts": int((t.side < 0).sum())}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    b5, b15 = B.bars()
    d = seances(b5, b15)
    d.to_csv(OUT / "seances.csv", index=False)
    gap = max(np.abs(b5.open.values[e + 1:z + 1] / b5.close.values[e:z] - 1).max() for e, z in zip(d.e, d.z)) * 1e4
    say(f"Séances : {len(d)} ({d.date.iloc[0]} -> {d.date.iloc[-1]}) ; M2 : {int(d.m2.sum())} ; "
        f"plus grand saut entre deux barres pendant un trade : {gap:.1f} bps")
    say("Trades M2 par année : " + ", ".join(f"{y} {n}" for y, n in d[d.m2].groupby("year").size().items()))

    tr = portefeuille(b5, d)
    ctrl_px, ctrl_hit = stop_main(b5, d, K_SL * d.atr15.values)
    for c, (jours, sens, stop, taille) in VARIANTES.items():
        m = d.m2.values if jours == "m2" else np.ones(len(d), bool)
        ref = ctrl_px[m] if stop else d.exit_px.values[m]
        t = tr[c]
        t["hit"] = ctrl_hit[m] if stop else False
        ecart = np.abs(t.exit_px.values - ref)
        say(f"Contrôle {c:32s} : {len(t)} trades, sorties différentes de la boucle : {int((ecart > 1e-9).sum())} "
            f"(écart max {ecart.max():.2f} pt)")
        t.to_csv(OUT / f"trades_{c.split(' (')[0].replace(' ', '_').replace('/', '').replace('×', 'x')}.csv", index=False)

    rows = []
    for p, (a, z) in PERIODS.items():
        jours = d.date[d.year.between(a, z)]
        tab = {c: stats(t[t.year.between(a, z)], jours) for c, t in tr.items()}
        rows += [{"période": p, "variante": c, **s} for c, s in tab.items()]
        say(f"\n===== {p} (vectorbt, 15 $ l'aller-retour par NQ) =====\n"
            f"{pd.DataFrame(tab).round(2).to_string()}")
    pd.DataFrame(rows).to_csv(OUT / "stats.csv", index=False)
    yr = pd.DataFrame({c: t.groupby("year").pnl.sum() for c, t in tr.items()})
    say(f"\n===== P&L net par année ($) =====\n{yr.round(0).to_string()}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
