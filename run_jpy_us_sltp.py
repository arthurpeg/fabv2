"""Short du yen en session US (règle du n° 28) avec SL / TP en ATR, RR 2 — exploratoire, données déjà vues.

uv run python run_jpy_us_sltp.py   → results/jpy_us_sltp/ (grid.csv, trades_<combo>.parquet, summary.txt)

Grille figée avant tout calcul (2026-11-19) — 12 essais, compteur 1 786 → 1 798 :
  ATR de Wilder 14 périodes sur bougies M5, M15 ou H1 (dernière bougie terminée à 11:00 ET),
  SL = k × ATR avec k ∈ {1, 2, 3, 4}, TP = 2 × SL (RR 2). Référence : sans SL/TP (règle du n° 28).
Règle : short 6J (le yen baisse) à l'open de la barre 11:00 ET ; sortie au premier de SL, TP ou 16:55 ET (open).
Exécution sur barres 1 min : si l'open d'une barre franchit déjà un niveau, sortie à l'open (gap) ;
si SL et TP sont touchés dans la même minute, on suppose le SL (prudent). Coût standard 1 tick + 5 $ ;
variante avec 1 tick de glissement supplémentaire sur chaque sortie au SL.
Données : Databento 6J.v.0 1 min, 2016-01 → 2026-08-28 (rien après : holdout du n° 28). La fenêtre
11:00-16:55 ET ne contient jamais le roulement (00:00 UTC) : prix non ajustés.
Ce n'est pas une preuve : toute la période est explorée, et le meilleur des 12 est biaisé vers le haut.
La règle du n° 28 (sans SL/TP) ne change pas.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/jpy_us_sltp")
NY = "America/New_York"
END = pd.Timestamp("2026-08-29", tz=NY)
MULT, TICK, FEE_USD = 12_500_000, 0.0000005, 5.0
TFS = {"M5": "5min", "M15": "15min", "H1": "1h"}
KS = [1, 2, 3, 4]
RR = 2.0


def atr(df: pd.DataFrame, rule: str, n: int = 14) -> pd.Series:
    """ATR de Wilder sur bougies `rule`, indexé par l'instant de FIN de bougie."""
    o = df.resample(rule, label="right", closed="left").agg({"high": "max", "low": "min", "close": "last"}).dropna()
    tr = pd.concat([o.high - o.low, (o.high - o.close.shift()).abs(), (o.low - o.close.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def build_days(df: pd.DataFrame) -> list[dict]:
    """Une entrée par jour : barres 1 min de l'entrée (11:00-11:04) jusqu'à la barre de sortie (16:55-16:59) exclue."""
    mins = df.index.hour * 60 + df.index.minute
    days = []
    for d, g in df[(mins >= 660) & (mins < 1020)].groupby(df.index[(mins >= 660) & (mins < 1020)].date):
        gm = g.index.hour * 60 + g.index.minute
        ein = np.flatnonzero((gm >= 660) & (gm < 665))
        eout = np.flatnonzero((gm >= 1015) & (gm < 1020))
        if not len(ein) or not len(eout) or pd.Timestamp(d).dayofweek > 4:
            continue
        i0, i1 = ein[0], eout[0]
        days.append({"date": d, "t_in": g.index[i0], "p_in": g.open.iat[i0], "p_out": g.open.iat[i1],
                     "o": g.open.values[i0:i1], "h": g.high.values[i0:i1], "l": g.low.values[i0:i1]})
    return days


def simulate(days: list[dict], atr_at: np.ndarray | None, k: float) -> pd.DataFrame:
    rows = []
    for j, d in enumerate(days):
        p0 = d["p_in"]
        how, px = "temps", d["p_out"]
        if atr_at is not None:
            sl, tp = p0 + k * atr_at[j], p0 - RR * k * atr_at[j]  # short : SL au-dessus, TP en dessous
            o, h, l = d["o"], d["h"], d["l"]
            hit_sl = (h >= sl) | (o >= sl)
            hit_tp = (l <= tp) | (o <= tp)
            hit = hit_sl | hit_tp
            if hit.any():
                i = int(np.argmax(hit))
                if o[i] >= sl:
                    how, px = "SL", o[i]
                elif o[i] <= tp:
                    how, px = "TP", o[i]
                elif hit_sl[i]:
                    how, px = "SL", sl
                else:
                    how, px = "TP", tp
        rows.append({"date": d["date"], "p_in": p0, "p_out": px, "exit": how,
                     "risk_bp": np.nan if atr_at is None else 1e4 * k * atr_at[j] / p0})
    t = pd.DataFrame(rows).set_index("date")
    t["gross_bp"] = -1e4 * (t.p_out / t.p_in - 1)
    cost_bp = 1e4 * (TICK * MULT + FEE_USD) / (MULT * t.p_in)
    t["net_bp"] = t.gross_bp - cost_bp
    t["net_slip_bp"] = t.net_bp - np.where(t.exit == "SL", 1e4 * TICK / t.p_in, 0.0)
    t["usd"] = t.net_bp * MULT * t.p_in / 1e4
    return t


def summarize(t: pd.DataFrame, label: str) -> dict:
    x = t.net_bp
    sh = x.mean() / x.std() * np.sqrt(252)
    eq = t.usd.cumsum()
    yrs = pd.to_datetime(t.index).year
    r = {
        "combo": label, "n": len(t), "brut_bp": t.gross_bp.mean(), "net_bp": x.mean(),
        "net_glisse_bp": t.net_slip_bp.mean(), "sharpe_net": sh, "t_net": sh / np.sqrt(252) * np.sqrt(len(x)),
        "gagnants_%": 100 * (x > 0).mean(), "SL_%": 100 * (t.exit == "SL").mean(), "TP_%": 100 * (t.exit == "TP").mean(),
        "temps_%": 100 * (t.exit == "temps").mean(), "risque_med_bp": t.risk_bp.median(),
        "R_moyen": (x / t.risk_bp).mean() if t.risk_bp.notna().all() else np.nan,
        "pnl_usd": eq.iloc[-1], "creux_usd": (eq - eq.cummax()).min(),
        "net_2016_2020": x[yrs <= 2020].mean(), "net_2021_2026": x[yrs >= 2021].mean(),
        "annees_pos": int((x.groupby(yrs).mean() > 0).sum()),
    }
    return r


def vbt_check(df: pd.DataFrame, days: list[dict], atr_at: np.ndarray, k: float) -> pd.Series:
    """Contrôle indépendant avec vectorbt (from_signals, stops sur OHLC) pour une combinaison."""
    mins = df.index.hour * 60 + df.index.minute
    w = df[(mins >= 660) & (mins < 1020)]
    entries = pd.Series(False, index=w.index)
    exits = pd.Series(False, index=w.index)
    slf = pd.Series(np.nan, index=w.index)
    for j, d in enumerate(days):
        entries.loc[d["t_in"]] = True
        slf.loc[d["t_in"]] = k * atr_at[j] / d["p_in"]
    wm = w.index.hour * 60 + w.index.minute
    first_out = pd.Series(w.index[(wm >= 1015)], index=w.index[(wm >= 1015)])
    exits.loc[first_out.groupby(first_out.index.date).first().tolist()] = True
    pf = vbt.Portfolio.from_signals(
        close=w.close, open=w.open, high=w.high, low=w.low, price=w.open,
        short_entries=entries, short_exits=exits, sl_stop=slf, tp_stop=RR * slf,
        size=1.0, init_cash=1e9, freq="1min")
    tr = pf.trades.records_readable
    ret = -1e4 * (tr["Avg Exit Price"] / tr["Avg Entry Price"] - 1)
    ret.index = pd.to_datetime(tr["Entry Timestamp"]).dt.date
    return ret


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("D:/quant-data/Cotations/forex/6J_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    df.index = df.index.tz_convert(NY)
    df = df[df.index < END]
    days = build_days(df)
    t_in = pd.DatetimeIndex([d["t_in"] for d in days]).floor("min")
    print(f"{len(days)} jours, {days[0]['date']} → {days[-1]['date']}")
    res, trades = [], {}
    t = simulate(days, None, 0)
    res.append(summarize(t, "sans SL/TP (n° 28)"))
    trades["ref"] = t
    for tf, rule in TFS.items():
        a = atr(df, rule)
        # dernière bougie terminée au plus tard à l'heure pleine d'entrée (11:00)
        at = a.reindex(t_in.floor("min").map(lambda x: x.replace(minute=0, second=0)), method="ffill").values
        for k in KS:
            lab = f"SL {k} ATR {tf} / TP {2 * k} ATR {tf}"
            t = simulate(days, at, k)
            trades[lab] = t
            t.to_parquet(OUT / f"trades_{tf}_k{k}.parquet")
            res.append(summarize(t, lab))
            if tf == "M15" and k == 2:
                v = vbt_check(df, days, at, k)
                both = pd.concat([t.gross_bp, v.rename("vb")], axis=1, join="inner")
                diff = (both.gross_bp - both.vb).abs()
                print(f"  contrôle vectorbt ({lab}) : {len(both)} trades communs, brut moyen {both.gross_bp.mean():+.2f} "
                      f"contre {both.vb.mean():+.2f} bp, écart > 0,5 bp sur {(diff > 0.5).sum()} trades")
    g = pd.DataFrame(res)
    g.to_csv(OUT / "grid.csv", index=False)
    pd.set_option("display.width", 250)
    s = g.round(2).to_string(index=False)
    print(s)
    (OUT / "summary.txt").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    main()
