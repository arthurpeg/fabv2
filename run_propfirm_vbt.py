"""Contrôle vectorbt de la trace FTMO 1-Step (avenant E du n° 18) : éval 2 % (TP 5 ATR), financé 1 % (TP 4 ATR).

uv run python run_propfirm_vbt.py  → results/propfirm_vbt/ (run.log, nights.csv, events_python.csv, events_vbt.csv)

vectorbt n'a pas de règles de prop firm. Partage du travail :
1. Python (règles FTMO, comme run_propfirm_streaks.py) : un emplacement 10k depuis le 2011-07-01, achat
   d'éval, validation ou échec, 3 nuits de vérification, financé jusqu'à la perte max, rachat. Il fixe pour
   chaque nuit tradée la phase (éval ou financé), le TP (5 ou 4 ATR) et la taille en dollars.
2. vectorbt (Portfolio.from_signals sur les barres 1 minute NQ) exécute TOUS ces trades avec ces tailles :
   entrée 20:00 ET, sortie 9:30 ET, sl_stop 2 ATR, tp_stop 5 ou 4 ATR, spread de 1,5 point en frais
   (moitié à l'entrée, moitié à la sortie). Il rend le P&L en dollars de chaque trade.
3. Les règles FTMO sont rejouées avec les P&L de vectorbt, en gardant les décisions de taille de l'étape 1 ;
   on compare les événements (validations, échecs, rewards, comptes perdus) aux événements de l'étape 1.
Taille : notionnel = risque $ / (stop + coût), où stop = 2 ATR / prix et coût = 1,5 / 25 684 (fraction du prix) :
un stop sans glissement coûte exactement le risque, spread compris (même convention que propfirm.ftmo).
Attention : importer run_prereg12 réécrit results/prereg12/run.log (vide de toute façon).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

import run_prereg12 as Q  # historique 2010-2015 actif
import run_recolte1_atr as A
from propfirm.ftmo import DAILY, MAXLOSS, SPLIT, TARGET
from recolte1.engine import NY, load
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_vbt")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
SIZE = 10_000.0
R_EVAL, R_FUND, CYCLE, REVIEW = 2.0, 1.0, 10, 3
COST = 1.5 / 25_684.0
TOL = 1e-3  # % du capital (0,10 $ sur 10k) : tolérance sur tous les seuils (perte max, objectif, meilleur jour)
A0, Z0 = "2011-07-01", "2026-08-28"


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def nights() -> pd.DataFrame:
    """Une ligne par nuit tradée de la règle : barre d'entrée, de sortie, sens, ATR / prix (comme A.simulate)."""
    e = Q.table(at(Q.D, "20:00", NY, -1), Q.B["t_open"], Q.MOM, "R0")
    df = load("NQ").copy()
    df.attrs = {}
    idx = df.index.as_unit("ns")
    e = e.copy()
    e["p_in"] = A.bar_pos(idx, e["t_in"])
    e["p_out"] = A.bar_pos(idx, e["t_out"])
    e = e[(e["p_in"] >= 0) & (e["p_out"] > e["p_in"])]
    a = A.atr_m15(df).reindex(pd.DatetimeIndex(e["t_in"]).as_unit("ns"), method="ffill")
    e["atr_frac"] = a.values / df["close"].values[e["p_in"].values]
    e = e.dropna(subset=["atr_frac"])
    e["night"] = pd.to_datetime(e["night"])
    e = e[(e["night"] >= A0) & (e["night"] <= Z0)].sort_values("p_in").reset_index(drop=True)
    return e, df


def replay(pnl_of, nt: int):
    """Règles FTMO sur un emplacement 10k depuis la nuit 0. pnl_of(i, phase, risk_pct) → P&L en % du capital.
    Renvoie (événements, plan des nuits tradées : i → (phase, risque %))."""
    ev, plan = [], {}
    i = 0
    while i < nt:
        ev.append(("achat", i))
        P = hi = best = 0.0
        passed = False
        while i < nt:
            floor = hi - MAXLOSS
            risk = min(R_EVAL, P - floor)
            if risk < 0.05:  # marge épuisée : éval abandonnée, comme propfirm.ftmo.run_eval (MIN_RISK)
                break
            plan[i] = ("éval", risk)
            pnl = pnl_of(i, "éval", risk)
            P += pnl; i += 1
            if P <= floor + TOL or pnl <= -DAILY:
                break
            best = max(best, pnl); hi = max(hi, P)
            if P >= TARGET - TOL and best <= 0.5 * P + TOL:
                passed = True
                break
        ev.append(("validée" if passed else "ratée", i - 1))
        if not passed:
            continue
        i += REVIEW
        P = hi = best = 0.0
        cyc = 0
        while i < nt:
            floor = hi - MAXLOSS
            risk = min(R_FUND, P - floor)
            if risk < 0.05:
                break
            plan[i] = ("financé", risk)
            pnl = pnl_of(i, "financé", risk)
            P += pnl; i += 1; cyc += 1
            if P <= floor + TOL or pnl <= -DAILY:
                break
            best = max(best, pnl); hi = max(hi, P)
            if cyc >= CYCLE and P > TOL and best <= 0.5 * P + TOL:
                ev.append(("reward", i - 1, round(SPLIT * P, 6)))
                P = hi = best = 0.0; cyc = 0
        ev.append(("financé perdu", i - 1))
        i += 1
    return ev, plan


def main() -> None:
    e, df = nights()
    nt = len(e)
    t5 = pd.read_csv("results/couts_reels_nq_nuit/trades.csv").sort_values("entry_idx")
    t4 = pd.read_parquet("cache/propfirm/nq_nuit_tp4.parquet").sort_values("entry_idx")
    assert (t5.entry_idx.to_numpy() == e.p_in.to_numpy()).all() and (t4.entry_idx.to_numpy() == e.p_in.to_numpy()).all()
    s = 2 * e["atr_frac"].to_numpy()  # stop en fraction du prix
    R = {"éval": t5.R_brut.to_numpy(), "financé": t4.R_brut.to_numpy()}
    c = COST / s
    say(f"Contrôle vectorbt de la trace FTMO (éval 2 % TP 5 ATR, financé 1 % TP 4 ATR, 10k, 1,5 pt) : {nt} nuits "
        f"{e.night.iloc[0].date()} → {e.night.iloc[-1].date()}, {len(df):,} barres 1 min".replace(",", " "))

    # 1. Python : trace et plan de taille
    ev_py, plan = replay(lambda i, ph, r: r * (R[ph][i] - c[i]) / (1 + c[i]), nt)
    say(f"Étape 1 (Python) : {len(plan)} nuits tradées, {sum(k == 'achat' for k, *_ in ev_py)} évals, "
        f"{sum(k == 'reward' for k, *_ in ev_py)} rewards")

    # 2. vectorbt : tous les trades du plan, tailles en dollars
    N = len(df)
    op, hi_, lo, cl = (df[x].values for x in ["open", "high", "low", "close"])
    ent_l = np.zeros(N, bool); ent_s = np.zeros(N, bool); ex = np.zeros(N, bool)
    sl = np.full(N, np.nan); tp = np.full(N, np.nan); size = np.full(N, np.nan)
    rows = []
    for i, (ph, risk) in plan.items():
        p_in, p_out, d = int(e.p_in[i]), int(e.p_out[i]), e.dir[i]
        (ent_l if d > 0 else ent_s)[p_in] = True
        ex[p_out] = True
        sl[p_in] = s[i]
        tp[p_in] = (5.0 if ph == "éval" else 4.0) * e.atr_frac[i]
        size[p_in] = risk / 100 * SIZE / (s[i] + COST)
        rows.append((i, p_in, ph, risk, size[p_in]))
    pf = vbt.Portfolio.from_signals(
        close=cl, open=op, high=hi_, low=lo,
        entries=ent_l, exits=ex, short_entries=ent_s, short_exits=ex,
        sl_stop=sl, tp_stop=tp, size=size, size_type="value", fees=COST / 2,
        init_cash=1e12, freq="1min",
    )
    rec = pd.DataFrame(pf.trades.records)
    rec = rec[rec["status"] == 1]
    plan_df = pd.DataFrame(rows, columns=["i", "p_in", "phase", "risk_pct", "notional"]).merge(
        rec[["entry_idx", "exit_idx", "pnl", "entry_price", "exit_price", "size"]], left_on="p_in", right_on="entry_idx", how="left")
    miss = plan_df.pnl.isna().sum()
    say(f"Étape 2 (vectorbt) : {len(rec)} trades fermés pour {len(plan_df)} prévus ; manquants {miss}")
    plan_df["pnl_vbt_pct"] = plan_df.pnl / SIZE * 100
    plan_df["pnl_py_pct"] = [r * (R[ph][i] - c[i]) / (1 + c[i]) for i, ph, r in zip(plan_df.i, plan_df.phase, plan_df.risk_pct)]
    diff = (plan_df.pnl_vbt_pct - plan_df.pnl_py_pct).abs()
    say(f"  écart de P&L vectorbt − Python par trade : max {diff.max() * 100:.4f} $ ... "
        f"en $ sur 10k : max {diff.max() / 100 * SIZE:.4f} $, moyen {diff.mean() / 100 * SIZE:.4f} $")
    plan_df["night"] = e.night.values[plan_df.i]
    plan_df.to_csv(OUT / "nights.csv", index=False)

    # 3. règles FTMO rejouées avec les P&L de vectorbt (décisions de taille de l'étape 1)
    vb = dict(zip(plan_df.i, plan_df.pnl_vbt_pct))
    ev_vb, plan_vb = replay(lambda i, ph, r: vb[i] * (r / plan[i][1]) if plan[i][1] else 0.0, nt)
    same_plan = plan_vb.keys() == plan.keys()
    k_py = [x[:2] for x in ev_py]; k_vb = [x[:2] for x in ev_vb]
    say(f"Étape 3 : événements Python {len(ev_py)}, vectorbt {len(ev_vb)} ; identiques (type et nuit) : {k_py == k_vb} ; "
        f"mêmes nuits tradées : {same_plan}")
    pay_py = np.array([x[2] for x in ev_py if x[0] == "reward"]); pay_vb = np.array([x[2] for x in ev_vb if x[0] == "reward"])
    if len(pay_py) == len(pay_vb):
        say(f"  rewards : {len(pay_vb)}, total versé Python {pay_py.sum() / 100 * SIZE:,.2f} $, vectorbt {pay_vb.sum() / 100 * SIZE:,.2f} $, "
            f"écart max par reward {np.abs(pay_py - pay_vb).max() / 100 * SIZE:.4f} $".replace(",", " "))
    for name, ev in (("python", ev_py), ("vbt", ev_vb)):
        pd.DataFrame([(k, e.night.iloc[j].date(), x[0] if x else np.nan) for k, j, *x in ev],
                     columns=["event", "night", "pct"]).to_csv(OUT / f"events_{name}.csv", index=False)

    # 4. séries sur la trace vectorbt
    evd = pd.read_csv(OUT / "events_vbt.csv", parse_dates=["night"])
    pos = {d: k for k, d in enumerate(e.night)}
    evd["i"] = evd.night.map(pos)
    pay = evd[evd.event == "reward"]
    marks = [(0, e.night.iloc[0])] + list(zip(pay.i, pay.night))
    gaps = sorted(((b - a, an.date(), bn.date()) for (a, an), (b, bn) in zip(marks, marks[1:])), reverse=True)
    runs, cur = [], []
    for r in evd.itertuples():
        if r.event == "ratée":
            cur.append(r.night.date())
        elif r.event == "validée" and cur:
            runs.append((len(cur), cur[0], cur[-1])); cur = []
    runs.sort(reverse=True)
    fee = 79 * 1.10
    say(f"\nTrace vectorbt depuis le {e.night.iloc[0].date()} : {(evd.event == 'achat').sum()} évals, "
        f"{(evd.event == 'validée').sum()} validées, {len(pay)} rewards, "
        f"rewards {pay.pct.sum() / 100 * SIZE:,.0f} $ − frais {(evd.event == 'achat').sum() * fee:,.0f} $".replace(",", " "))
    say("  plus longues périodes sans reward : " + " ; ".join(f"{a} → {b} ({n} nuits)" for n, a, b in gaps[:5]))
    say("  pires séries d'évals ratées : " + " ; ".join(f"{n} ({a} → {b})" for n, a, b in runs[:4]))
    say(f"  rewards par an : {pay.night.dt.year.value_counts().sort_index().to_dict()}")
    st = pf.stats()
    say(f"\nvectorbt Portfolio.stats() sur l'ensemble des trades (P&L en $, capital fictif 1e12 pour ne jamais limiter) :")
    say(f"  trades {int(st['Total Trades'])}, taux de réussite {st['Win Rate [%]']:.1f} %, "
        f"meilleur trade {st['Best Trade [%]']:.3f} %, pire {st['Worst Trade [%]']:.3f} % (en % du notionnel), "
        f"profit factor {st['Profit Factor']:.2f}, P&L total {pf.total_profit():,.0f} $".replace(",", " "))


if __name__ == "__main__":
    main()
