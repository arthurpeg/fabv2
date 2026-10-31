"""Avenant E du n° 18 refait avec vectorbt : FTMO 1-Step, éval 2 % (TP 5 ATR), financé 1 % (TP 4 ATR).

uv run python run_propfirm_vbt.py [N]  → results/propfirm_vbt/ (run.log, returns.csv, metrics.csv,
    streaks_vbt.csv, streaks_python.csv, events_vbt.csv, events_python.csv, sized_check.csv)

vectorbt n'a pas de règles de prop firm. Partage du travail :
1. vectorbt (Portfolio.from_signals sur les barres 1 minute NQ) calcule le rendement net de CHAQUE nuit de la
   règle, pour TP 5 ATR et pour TP 4 ATR : entrée 20:00 ET, sortie 9:30 ET, sl_stop 2 ATR, tp_stop, spread de
   1,5 point (au niveau actuel du NQ, 25 684) en frais, moitié à l'entrée et moitié à la sortie. Le rendement
   par dollar de notionnel ne dépend pas de la taille.
2. Règles FTMO (Python) sur ces rendements : P&L = notionnel × rendement vectorbt, notionnel = risque / (stop
   + coût), stop = 2 ATR / prix, coût = 1,5 / 25 684. Trace historique depuis 2011-07-01, pires séries (départs
   tous les 5 trades) et Monte-Carlo (propfirm.ftmo) ; mêmes calculs sur les R du moteur maison, pour comparer.
3. Contrôle : vectorbt rejoue la trace historique avec les vraies tailles en dollars ; on compare son P&L par
   trade à celui de l'étape 2.
Seuils FTMO avec une tolérance de 0,001 % du capital (0,10 $ sur 10k) ; éval abandonnée sous 0,05 % de marge
(comme propfirm.ftmo.run_eval). Attention : importer run_prereg12 réécrit results/prereg12/run.log (vide).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

import run_prereg12 as Q  # historique 2010-2015 actif
import run_recolte1_atr as A
from propfirm.ftmo import DAILY, EUR, MAXLOSS, PRICES_EUR, SPLIT, TARGET, Market, TradeLib, run_eval, run_funded
from recolte1.engine import NY, load
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_vbt")
OUT.mkdir(parents=True, exist_ok=True)
LOG = None  # ouvert dans main() : le module peut être importé sans écraser run.log
N_MC = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
SEED = 1820
SIZE = 10_000.0
R_EVAL, R_FUND, CYCLE, REVIEW = 2.0, 1.0, 10, 3
COST = 1.5 / 25_684.0
TOL = 1e-3
STEP, MIN_NIGHTS = 5, 504
A0, Z0 = "2011-07-01", "2026-08-28"


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def nights(hour: str = "20:00", df=None):
    """Une ligne par nuit tradée de la règle : barre d'entrée, de sortie, sens, ATR / prix (comme A.simulate)."""
    e = Q.table(at(Q.D, hour, NY, -1), Q.B["t_open"], Q.MOM, "R0")
    df = load("NQ").copy() if df is None else df
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


def replay(pnl_of, nt: int, start: int = 0):
    """Règles FTMO sur un emplacement 10k depuis la nuit `start`. pnl_of(i, phase, risk_pct) → P&L en % du capital.
    Renvoie (événements, plan des nuits tradées : i → (phase, risque %))."""
    ev, plan = [], {}
    i = start
    while i < nt:
        ev.append(("achat", i))
        P = hi = best = 0.0
        passed = False
        while i < nt:
            floor = hi - MAXLOSS
            risk = min(R_EVAL, P - floor)
            if risk < 0.05:
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
        ev.append(("validée" if passed else "ratée", max(i - 1, start)))
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
                ev.append(("reward", i - 1, SPLIT * P))
                P = hi = best = 0.0; cyc = 0
        ev.append(("financé perdu", min(i - 1, nt - 1)))
        i += 1
    return ev, plan


def run_vbt(df, e, sel, tp_atr, size):
    """vectorbt sur les nuits `sel` (indices de e), objectif tp_atr ATR, taille en $ de notionnel par nuit."""
    N = len(df)
    ent_l = np.zeros(N, bool); ent_s = np.zeros(N, bool); ex = np.zeros(N, bool)
    sl = np.full(N, np.nan); tp = np.full(N, np.nan); sz = np.full(N, np.nan)
    p_in = e.p_in.to_numpy()[sel]; p_out = e.p_out.to_numpy()[sel]; d = e.dir.to_numpy()[sel]
    a = e.atr_frac.to_numpy()[sel]
    ent_l[p_in[d > 0]] = True; ent_s[p_in[d < 0]] = True; ex[p_out] = True
    sl[p_in] = 2 * a; tp[p_in] = tp_atr * a; sz[p_in] = size
    pf = vbt.Portfolio.from_signals(
        close=df["close"].values, open=df["open"].values, high=df["high"].values, low=df["low"].values,
        entries=ent_l, exits=ex, short_entries=ent_s, short_exits=ex,
        sl_stop=sl, tp_stop=tp, size=sz, size_type="value", fees=COST / 2, init_cash=1e12, freq="1min",
    )
    rec = pd.DataFrame(pf.trades.records)
    rec = rec[rec["status"] == 1].set_index("entry_idx")
    return pf, rec.reindex(p_in)


def streaks(pnl_of, nt: int, nights: pd.Series, size: int = 10_000) -> pd.DataFrame:
    fee = PRICES_EUR[size] * EUR
    rows = []
    for s0 in range(0, nt - MIN_NIGHTS, STEP):
        ev, _ = replay(pnl_of, nt, s0)
        run = best_run = 0
        run_from = w_from = w_to = s0
        for k, j, *_ in ev:
            if k == "ratée":
                run_from = j if run == 0 else run_from
                run += 1
                if run > best_run:
                    best_run, w_from, w_to = run, run_from, j
            elif k == "validée":
                run = 0
        marks = [s0] + [j for k, j, *_ in ev if k == "reward"]
        gaps = np.diff(marks + [nt - 1])
        g = int(np.argmax(gaps))
        cash = np.zeros(nt - s0)
        for k, j, *x in ev:
            if k == "achat":
                cash[j - s0] -= fee
            elif k == "reward":
                cash[j - s0] += x[0] / 100 * size
        cum = np.cumsum(cash)
        dd = cum - np.maximum.accumulate(np.concatenate([[0.0], cum]))[1:]
        rows.append(dict(start=nights[s0].date(), fails_max=best_run, fails_from=nights[w_from].date(),
                         fails_to=nights[w_to].date(), nopay_nights=int(gaps[g]), nopay_from=nights[marks[g]].date(),
                         nopay_to=nights[min(marks[g] + gaps[g], nt - 1)].date(), cash_dd=dd.min(),
                         evals=sum(k == "achat" for k, *_ in ev), rewards=len(marks) - 1, net=cum[-1]))
    return pd.DataFrame(rows)


def main() -> None:
    global LOG
    LOG = open(OUT / "run.log", "w", encoding="utf-8")
    e, df = nights()
    nt = len(e)
    s = 2 * e["atr_frac"].to_numpy()
    say(f"Avenant E refait avec vectorbt (éval 2 % TP 5 ATR, financé 1 % TP 4 ATR, spread 1,5 pt) : {nt} nuits "
        f"{e.night.iloc[0].date()} → {e.night.iloc[-1].date()}, {len(df):_} barres 1 min".replace("_", " "))

    # 1. vectorbt : rendement net de chaque nuit, TP 5 et TP 4 (notionnel 10 000 $, le rendement n'en dépend pas)
    ret = {}
    for tp_atr in (5.0, 4.0):
        _, rec = run_vbt(df, e, np.arange(nt), tp_atr, 1e4)
        assert rec["pnl"].notna().all(), "nuit sans trade fermé"
        ret[tp_atr] = (rec["pnl"] / 1e4).to_numpy()
        say(f"  vectorbt TP {tp_atr:g} ATR : {rec['pnl'].notna().sum()} trades fermés sur {nt} nuits, rendement net moyen "
            f"{ret[tp_atr].mean() * 1e4:+.3f} pb du notionnel, soit {np.mean((ret[tp_atr] + COST) / s):+.4f} R brut, "
            f"gagnants {(ret[tp_atr] > 0).mean():.1%}")
    pd.DataFrame({"night": e.night.dt.date, "ret_tp5": ret[5.0], "ret_tp4": ret[4.0], "stop": s}).to_csv(OUT / "returns.csv", index=False)

    t5 = pd.read_csv("results/couts_reels_nq_nuit/trades.csv").sort_values("entry_idx")
    t4 = pd.read_parquet("cache/propfirm/nq_nuit_tp4.parquet").sort_values("entry_idx")
    assert (t5.entry_idx.to_numpy() == e.p_in.to_numpy()).all() and (t4.entry_idx.to_numpy() == e.p_in.to_numpy()).all()
    Rv = {k: (ret[k] + COST) / s for k in (5.0, 4.0)}  # R tel que P&L moteur = risque × ret / (s + coût)
    Rm = {5.0: t5.R_brut.to_numpy(), 4.0: t4.R_brut.to_numpy()}
    for k in (5.0, 4.0):
        d = np.abs(Rv[k] - Rm[k])
        say(f"  R vectorbt (spread 1,5 pt) − R moteur maison (brut + coût forfaitaire), TP {k:g} : écart max {d.max():.2e} R, moyen {d.mean():.2e} R")

    c = COST / s

    def pnl_vbt(i, ph, r):
        return r * ret[5.0 if ph == "éval" else 4.0][i] / (s[i] + COST)

    def pnl_py(i, ph, r):
        return r * (Rm[5.0 if ph == "éval" else 4.0][i] - c[i]) / (1 + c[i])

    # 2a. trace historique
    ev_v, plan_v = replay(pnl_vbt, nt)
    ev_p, _ = replay(pnl_py, nt)
    kv = [x[:2] for x in ev_v]
    kp = [x[:2] for x in ev_p]
    first = next((k for k, (a, b) in enumerate(zip(kv, kp)) if a != b), None)
    if kv == kp:
        say(f"\nTrace depuis le {e.night.iloc[0].date()} : {len(ev_v)} événements, identiques (type et nuit) entre vectorbt et le moteur maison")
    else:
        say(f"\nTrace depuis le {e.night.iloc[0].date()} : vectorbt {len(ev_v)} événements, moteur maison {len(ev_p)} ; premier écart "
            f"à l'événement {first} : vectorbt {kv[first][0]} le {e.night.iloc[kv[first][1]].date()}, maison {kp[first][0]} le "
            f"{e.night.iloc[kp[first][1]].date()}" if first is not None else " ; une trace est plus longue")
    for name, ev in (("vbt", ev_v), ("python", ev_p)):
        pd.DataFrame([(k, e.night.iloc[j].date(), x[0] if x else np.nan) for k, j, *x in ev],
                     columns=["event", "night", "pct"]).to_csv(OUT / f"events_{name}.csv", index=False)
    pay = [x for x in ev_v if x[0] == "reward"]
    yrs = pd.Series([e.night.iloc[j].year for _, j, _ in pay]).value_counts().sort_index().to_dict()
    say(f"  trace vectorbt : {sum(k == 'achat' for k, *_ in ev_v)} évals, {sum(k == 'validée' for k, *_ in ev_v)} validées, "
        f"{len(pay)} rewards ({sum(x for *_, x in pay) / 100 * SIZE:_.0f} $ reçus sur 10k), rewards par an {yrs}".replace("_", " "))

    # 3. contrôle : vectorbt rejoue la trace avec les vraies tailles en dollars
    idx = np.array(sorted(plan_v))
    ph = np.array([plan_v[i][0] for i in idx])
    rk = np.array([plan_v[i][1] for i in idx])
    notional = rk / 100 * SIZE / (s[idx] + COST)
    chk = []
    for k, tp_atr in (("éval", 5.0), ("financé", 4.0)):
        m = ph == k
        _, rec = run_vbt(df, e, idx[m], tp_atr, notional[m])
        chk.append(pd.DataFrame({"i": idx[m], "night": e.night.values[idx[m]], "phase": k, "risk_pct": rk[m],
                                 "notional": notional[m], "pnl_vbt_sized": rec["pnl"].to_numpy(),
                                 "pnl_step2": [pnl_vbt(i, k, r) / 100 * SIZE for i, r in zip(idx[m], rk[m])]}))
    chk = pd.concat(chk).sort_values("i")
    chk.to_csv(OUT / "sized_check.csv", index=False)
    gap = (chk.pnl_vbt_sized - chk.pnl_step2).abs()
    say(f"Contrôle tailles réelles : {chk.pnl_vbt_sized.notna().sum()} trades fermés par vectorbt sur {len(chk)} ; écart de P&L "
        f"avec l'étape 2 : max {gap.max():.2e} $ ; P&L total {chk.pnl_vbt_sized.sum():_.2f} $ contre {chk.pnl_step2.sum():_.2f} $".replace("_", " "))

    # 2b. pires séries
    for name, f in (("vectorbt", pnl_vbt), ("moteur maison", pnl_py)):
        S = streaks(f, nt, e.night)
        S.to_csv(OUT / f"streaks_{'vbt' if name == 'vectorbt' else 'python'}.csv", index=False)
        w1, w2, w3 = S.loc[S.fails_max.idxmax()], S.loc[S.nopay_nights.idxmax()], S.loc[S.cash_dd.idxmin()]
        say(f"\nPires séries ({name}, {len(S)} départs de {S.start.min()} à {S.start.max()}, compte 10k) :")
        say(f"  évals ratées d'affilée : médiane {S.fails_max.median():.0f}, pire {w1.fails_max} ({w1.fails_from} → {w1.fails_to}, "
            f"{w1.fails_max * PRICES_EUR[10_000] * EUR:.0f} $ de frais)")
        say(f"  plus longue période sans reward : médiane {S.nopay_nights.median():.0f} nuits, pire {w2.nopay_nights} nuits "
            f"(~{w2.nopay_nights / 21:.1f} mois, {w2.nopay_from} → {w2.nopay_to})")
        say(f"  creux de trésorerie : médiane {S.cash_dd.median():.0f} $, pire {w3.cash_dd:.0f} $ ; "
            f"par départ (médianes) {S.evals.median():.0f} évals, {S.rewards.median():.0f} rewards, gain net {S.net.median():_.0f} $".replace("_", " "))

    # 2c. Monte-Carlo (propfirm.ftmo), même graine pour les deux sources
    rows = []
    for name, R in (("vectorbt", Rv), ("moteur maison", Rm)):
        rng = np.random.default_rng(SEED)
        le, lf = TradeLib(e.night.values, s, R[5.0]), TradeLib(e.night.values, s, R[4.0])
        ok, d = run_eval(Market(le, np.nan, COST), R_EVAL, 0.0, N_MC, rng)
        paid, n, life, first_r = run_funded(Market(lf, np.nan, COST), R_FUND, 0.0, N_MC, rng)
        p, v = ok.mean(), paid.mean()
        se_p, se_v = np.sqrt(p * (1 - p) / N_MC), paid.std() / np.sqrt(N_MC)
        row = dict(source=name, passage=p, nuits_tentative=d.mean(), nuits_si_validée=d[ok].mean(), valeur_financé_pct=v,
                   p_reward=(n > 0).mean(), rewards=n.mean(), reward_moyen_pct=paid.sum() / max(n.sum(), 1),
                   premier_reward_méd=np.median(first_r[first_r > 0]), vie_moy=life.mean(), vie_méd=np.median(life))
        for size in (10_000, 100_000):
            fee = PRICES_EUR[size] * EUR
            row[f"EV_{size // 1000}k"] = p * v / 100 * size - fee
            row[f"IC_{size // 1000}k"] = 1.96 * size / 100 * np.sqrt((v * se_p) ** 2 + (p * se_v) ** 2)
            row[f"refus_max_{size // 1000}k"] = 1 - fee / (p * v / 100 * size)
        rows.append(row)
        say(f"\nMonte-Carlo ({name}, {N_MC} comptes, graine {SEED}) : passage {p:.1%} ± {1.96 * se_p:.1%}, "
            f"{d.mean():.1f} nuits par tentative ({d[ok].mean():.1f} si validée) ; financé {v:.2f} % ± {1.96 * se_v:.2f} du capital, "
            f"P(≥ 1 reward) {row['p_reward']:.0%}, {n.mean():.2f} rewards de {row['reward_moyen_pct']:.2f} % en moyenne, "
            f"1er reward méd. {row['premier_reward_méd']:.0f} nuits, vie {life.mean():.0f} nuits (méd. {np.median(life):.0f}) ; "
            f"EV 10k {row['EV_10k']:+.0f} $ ± {row['IC_10k']:.0f} (refus tolérés {row['refus_max_10k']:.0%}), "
            f"100k {row['EV_100k']:+.0f} $ ± {row['IC_100k']:.0f} ({row['refus_max_100k']:.0%})")
    pd.DataFrame(rows).to_csv(OUT / "metrics.csv", index=False)


if __name__ == "__main__":
    main()
