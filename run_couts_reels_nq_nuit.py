"""Règle NQ de nuit avec les spreads réels (bbo-1m Databento) au lieu du coût fixe de 1 tick.

uv run python run_couts_reels_nq_nuit.py   → results/couts_reels_nq_nuit/ (trades.csv, summary.csv, by_year.csv, run.log)

Coût d'un trade = demi-spread à l'entrée + demi-spread à la sortie (meilleur bid/ask relevé à la fin
de la minute d'exécution) + commission. Spreads nuls, négatifs (carnet croisé) ou absents → 1 tick.
Mêmes trades que les n° 11-17 (compte 20:00, momentum 12-1, SL 2 / TP 5 ATR, sortie 9:30).
NQ : commission 5 $ aller-retour (convention du dépôt). MNQ (2019-05+) : mêmes prix et mêmes trades,
spreads MNQ, commissions de 0,50 à 2,50 $ aller-retour (hypothèses, le dépôt n'en fixe pas).
Re-estimation de coût, pas une sélection : le compteur d'essais ne bouge pas.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_prereg12 as Q  # historique 2010-2015 actif
import run_prereg10 as P
import run_recolte1_atr as A
from recolte1.engine import NY, ci_mean, ci_sharpe, load
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/couts_reels_nq_nuit")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
TICK = 0.25
A0, Z0 = "2011-07-01", "2026-08-28"


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def spread_at(name: str, ts: pd.DatetimeIndex) -> np.ndarray:
    b = pd.read_parquet(f"cache/databento_bbo/{name}_v0_bbo1m.parquet", columns=["bid_px_00", "ask_px_00"])
    sp = (b["ask_px_00"] - b["bid_px_00"]).rename("sp").sort_index()
    sp = sp.where(sp > 0)
    q = pd.DataFrame({"t": ts}).reset_index().sort_values("t")
    m = pd.merge_asof(q, sp.rename_axis("ts").reset_index(), left_on="t", right_on="ts",
                      direction="backward", tolerance=pd.Timedelta(minutes=2))
    out = np.full(len(ts), np.nan)
    out[m["index"].values] = m["sp"].values
    return out


def main():
    e = Q.table(at(Q.D, "20:00", NY, -1), Q.B["t_open"], Q.MOM, "R0")
    A.VARIANTS = Q.STOP
    T = A.simulate("NQ", e)
    g = T[T["cost"] == "gross"].copy()
    g["R_brut"] = P.r_multiples("NQ", e, g).values
    g["risk"] = g["ret"] / g["R_brut"]
    old = T[T["cost"] == "net"].set_index("entry_idx")["ret"]
    g["ret_net_1tick"] = old.reindex(g["entry_idx"]).values
    g["night"] = pd.to_datetime(g["night"])
    g = g[(g["night"] >= A0) & (g["night"] <= Z0)].reset_index(drop=True)
    df = load("NQ")
    t_in = df.index[g["entry_idx"].values] + pd.Timedelta(minutes=1)  # fin de la minute d'exécution
    t_out = df.index[g["exit_idx"].values] + pd.Timedelta(minutes=1)
    raw = (df["close"] / df["factor"]).values[g["entry_idx"].values]
    rows = []
    for name, comms, start in [("NQ", [5.0], A0), ("MNQ", [0.5, 1.24, 2.5], "2019-05-06")]:
        pv = 20.0 if name == "NQ" else 2.0
        s_in, s_out = spread_at(name, t_in), spread_at(name, t_out)
        miss = np.isnan(s_in) | np.isnan(s_out)
        s_in, s_out = np.where(np.isnan(s_in), TICK, s_in), np.where(np.isnan(s_out), TICK, s_out)
        g[f"spread_in_{name}"], g[f"spread_out_{name}"] = s_in / TICK, s_out / TICK
        sel = (g["night"] >= start).values
        for c in comms:
            cost_pts = (s_in + s_out) / 2 + c / pv
            net = g["ret"] - cost_pts / raw
            R = net / g["risk"]
            col = f"R_{name}_{c}$"
            g[col] = R
            x = R[sel]
            old_R = (g["ret_net_1tick"] / g["risk"])[sel]
            m, lo, hi = ci_mean(x.values)
            daily = x.groupby(g["night"][sel]).sum()
            cum = daily.cumsum()
            years = (g["night"][sel].max() - g["night"][sel].min()).days / 365.25
            rows.append({"contrat": name, "commission_AR_$": c, "période": f"{start[:4]} → 2026-08", "trades": int(sel.sum()),
                         "spread_entrée_ticks_moy": float(np.mean(s_in[sel]) / TICK), "spread_sortie_ticks_moy": float(np.mean(s_out[sel]) / TICK),
                         "coût_ticks_AR_moy": float(np.mean(cost_pts[sel]) / TICK), "spreads_manquants_%": float(miss[sel].mean() * 100),
                         "R_trade_brut": float(g["R_brut"][sel].mean()), "R_trade_1tick": float(old_R.mean()),
                         "R_trade_réel": m, "lo": lo, "hi": hi, "R_an": float(x.sum() / years),
                         "max_dd_R": float((cum - cum.cummax()).min()), "sharpe_jour": ci_sharpe(daily.reindex(Q.NIGHTS[(Q.NIGHTS >= start)]).fillna(0).values)[0]})
    S = pd.DataFrame(rows)
    S.to_csv(OUT / "summary.csv", index=False)
    g.to_csv(OUT / "trades.csv", index=False)
    yr = g.groupby(g["night"].dt.year).agg(spread_entree=("spread_in_NQ", "mean"), spread_sortie=("spread_out_NQ", "mean"),
                                         R_1tick=("ret_net_1tick", lambda s: (s / g.loc[s.index, "risk"]).sum()),
                                         R_reel=("R_NQ_5.0$", "sum"))
    yr.to_csv(OUT / "by_year.csv")
    pd.set_option("display.width", 250)
    log(S.round(3).to_string(index=False))
    log(yr.round(2).to_string())
    log(g.groupby("reason")[["spread_in_NQ", "spread_out_NQ"]].mean().round(2).to_string())


if __name__ == "__main__":
    main()
