"""FTMO 1-Step avec les deux stratégies transmises combinées, au plus un trade par jour (priorité à la nuit) :
3n (long 20:05 -> 03:00 ET si somme des 3 nuits <= 0, stop 2 x ATR M15) et M2 (close 9:30 contre EMA12, 9:35 -> 15:55,
force > 2,2 ATR ou retournement < -60 bps, stop 4 x ATR M15), toutes deux avec un objectif à 2 R.

EXPLORATOIRE, hors compteur : évaluation d'un contrat sur des trades existants. Les deux règles ont échoué hors
échantillon (n° 24, n° 25) ; les chiffres 2016-2026 sont ceux de leur période de sélection.

uv run python run_propfirm_combo.py [N] → results/propfirm_combo/ (run.log, trades_tp2.csv, ftmo.csv)

1. Trades avec TP à 2 R (TP = 2 x distance du stop : 4 ATR M15 pour 3n, 8 ATR M15 pour M2), recalculés avec vectorbt
   (from_signals, sl_stop + tp_stop, même code de séances que run_nq_nuit_3n_vbt.py / run_nq_ema930_vbt.py). Contrôle :
   boucle à la main, stop prioritaire si stop et objectif tombent dans la même barre, fill à l'open en cas de gap.
   La boucle donne aussi MFE_R (mouvement favorable maximal avant la sortie, barre du stop exclue).
2. Un trade par jour : si la nuit qui se termine le matin du jour J a un trade 3n, pas de M2 le jour J.
3. Moteur propfirm.ftmo (n° 18) : un trade = une journée FTMO, R brut historique, coût CFD 1,5 point au niveau actuel
   du NQ (25 684). Éval : 2,5 % risqués par trade ; financé : 1 % ; perte max 10 %, perte du jour 3 %, règle du meilleur
   jour 50 %, reward tous les 10 trades, partage 90 %, remise à zéro de la perte max après reward (règle du 1-Step).
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

import run_nq_ema930_vbt as E
import run_nq_nuit_3n_vbt as B
from propfirm.ftmo import PRICES_EUR, Market, TradeLib, ev, refusal_breakeven, run_eval, run_funded

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/propfirm_combo")
SEED = 1826
P_REF = 25_684.0
COST = 1.5 / P_REF
R_EVAL, R_FUND, TP_R = 2.5, 1.0, 2.0
SOURCES = {
    "2010-06 → 2015-12": ("cache/databento_2010/NQ_v0_1m_2010.parquet", "2010-06-08", "2015-12-31", "2016-01-01"),
    "2016-01 → 2026-08": ("D:/quant-data/Cotations/indices/NQ_v0_1m.parquet", "2016-01-01", "2026-08-28", "2026-08-29"),
}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def simule(b5: pd.DataFrame, pin: np.ndarray, pout: np.ndarray, side: np.ndarray, dist: np.ndarray,
           sortie_open: bool) -> tuple[pd.DataFrame, int]:
    """Trades vectorbt avec stop à dist et objectif à TP_R x dist ; sortie à l'open (3n) ou au close (M2) de pout."""
    a, z = pin.min(), pout.max() + 1
    sub = b5.iloc[a:z]
    e, x = pin - a, pout - a
    o, h, l, c = (sub[k].values.copy() for k in ("open", "high", "low", "close"))
    price = c.copy()
    price[e] = o[e]
    if sortie_open:  # la barre de sortie ne sert qu'à son open (voir run_nq_nuit_3n_vbt.portefeuille)
        price[x], h[x], l[x] = o[x], o[x], o[x]
    le, se, ex = (np.zeros(len(sub), bool) for _ in range(3))
    le[e[side > 0]], se[e[side < 0]], ex[x] = True, True, True
    entry = o[e]
    sl, tp = np.full(len(sub), np.nan), np.full(len(sub), np.nan)
    sl[e], tp[e] = dist / entry, TP_R * dist / entry
    pf = vbt.Portfolio.from_signals(close=c, open=o, high=h, low=l, price=price, entries=le, exits=ex,
                                    short_entries=se, short_exits=ex, sl_stop=sl, tp_stop=tp,
                                    stop_entry_price="price", size=1.0, init_cash=1e9, freq="5min")
    rec = pf.trades.records_readable
    assert len(rec) == len(pin)
    px_vbt = rec["Avg Exit Price"].values
    # contrôle : boucle à la main (3n : barres pin..pout-1 ; M2 : barres pin..pout)
    # MFE_R : plus grand mouvement favorable avant la sortie, en R ; la barre du stop est exclue (on ne sait pas si le
    # haut est venu avant le bas dans ces 5 minutes) ; sert à ramener l'objectif d'éval FTMO au reste à faire
    px = np.where(sortie_open, o[x], c[x]).astype(float)
    mfe = np.zeros(len(e))
    for i, (ei, xi, s, en, d) in enumerate(zip(e, x, side, entry, dist)):
        stop, obj = en - s * d, en + s * TP_R * d
        last = xi - 1 if sortie_open else xi
        for k in range(ei, last + 1):
            if (s > 0 and l[k] <= stop) or (s < 0 and h[k] >= stop):
                px[i] = min(stop, o[k]) if s > 0 else max(stop, o[k])
                last = k - 1
                break
            if (s > 0 and h[k] >= obj) or (s < 0 and l[k] <= obj):
                px[i] = max(obj, o[k]) if s > 0 else min(obj, o[k])
                last = k
                break
        if last >= ei:
            mfe[i] = ((h[ei:last + 1].max() - en) if s > 0 else (en - l[ei:last + 1].min())) / d
    ecart = int((np.abs(px_vbt - px) > 1e-9).sum())
    R = side * (px_vbt - entry) / dist
    return pd.DataFrame({"entry_px": entry, "exit_px": px_vbt, "side": side, "dist": dist, "R_brut": R,
                         "MFE_R": np.maximum(mfe, 0.0)}), ecart


def trades(src: str, a: str, z: str, fin: str) -> pd.DataFrame:
    B.SRC, B.END = Path(src), pd.Timestamp(fin, tz="America/New_York")
    b5, b15 = B.bars()
    n = B.nuits(b5, b15)
    n = n[(n.session >= a) & (n.session <= z) & n.sig3n].reset_index(drop=True)
    t3, e3 = simule(b5, n.pos_in.values, n.pos_out.values, np.ones(len(n), int), n.dist.values, True)
    t3.insert(0, "date", pd.to_datetime(n.session))
    t3.insert(1, "strat", "3n")
    d = E.seances(b5, b15)
    d = d[(pd.to_datetime(d.date) >= a) & (pd.to_datetime(d.date) <= z) & d.m2].reset_index(drop=True)
    tm, em = simule(b5, d.e.values, d.z.values, d.side.values, E.K_SL * d.atr15.values, False)
    tm.insert(0, "date", pd.to_datetime(d.date))
    tm.insert(1, "strat", "M2")
    say(f"  {a} → {z} : 3n {len(t3)} trades (≠ boucle : {e3}), M2 {len(tm)} trades (≠ boucle : {em}, "
        f"stop ou objectif dans la barre d'entrée)")
    t = pd.concat([t3, tm], ignore_index=True)
    t["s"] = t.dist / t.entry_px
    return t


def un_par_jour(t: pd.DataFrame) -> pd.DataFrame:
    nuit = set(t.date[t.strat == "3n"])
    return t[~((t.strat == "M2") & t.date.isin(nuit))].sort_values(["date", "strat"]).reset_index(drop=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    say(f"FTMO 1-Step, 3n + M2 avec objectif à {TP_R:g} R, un trade par jour ; éval {R_EVAL} %, financé {R_FUND} % ; "
        f"{N} comptes par réglage, graine {SEED}")
    T = {p: trades(*v) for p, v in SOURCES.items()}
    allt = pd.concat([t.assign(période=p) for p, t in T.items()])
    allt.to_csv(OUT / "trades_tp2.csv", index=False)
    libs = {}
    for p, t in T.items():
        an = (t.date.max() - t.date.min()).days / 365.25
        c = un_par_jour(t)
        libs[f"combiné {p}"] = (c, len(c) / an)
        libs[f"combiné {p}, sans edge"] = (c.assign(R_brut=c.R_brut - c.R_brut.mean()), len(c) / an)
        for s in ("3n", "M2"):
            x = t[t.strat == s]
            libs[f"{s} seul {p}"] = (x, len(x) / an)
    mom = pd.read_parquet("cache/propfirm/nq_nuit_tp4.parquet").sort_values("entry_idx")
    mom = mom[mom.night >= "2016-01-01"]
    libs["mom (TP 4 ATR = 2 R) 2016-01 → 2026-08"] = (
        pd.DataFrame({"R_brut": mom.R_brut.values, "s": mom.risk.fillna(mom.risk.median()).values,
                      "date": pd.to_datetime(mom.night.values)}), len(mom) / 10.65)

    say("\nBibliothèques (R brut, objectif à 2 R) :")
    for k, (t, f) in libs.items():
        r = t.R_brut.values
        say(f"  {k:<42} {len(r):>5} trades ({f:5.0f}/an), R brut moyen {r.mean():+.3f}, objectif atteint "
            f"{100 * (r >= TP_R - 1e-6).mean():4.1f} %, stop {100 * (r <= -1 + 1e-6).mean():4.1f} %, "
            f"coût CFD {np.median(COST / t.s.values):.3f} R")

    rng = np.random.default_rng(SEED)
    rows = []
    for k, (t, f) in libs.items():
        m = Market(TradeLib(t.date.values, t.s.to_numpy(), t.R_brut.to_numpy()), np.nan, COST)
        ok, d = run_eval(m, R_EVAL, 0.0, N, rng)
        p = ok.mean()
        paid, nr, life, first = run_funded(m, R_FUND, 0.0, N, rng, reset=True)
        row = dict(lib=k, trades_an=f, p_pass=p, trades_eval=d[ok].mean(), mois_eval=d[ok].mean() / f * 12,
                   mois_tentative=d.mean() / f * 12, v_pct=paid.mean(), p_reward=(nr > 0).mean(), n_rewards=nr.mean(),
                   vie_trades=life.mean(), vie_mois=life.mean() / f * 12,
                   premier_reward_mois=np.median(first[first > 0]) / f * 12 if (first > 0).any() else np.nan)
        for size in (10_000, 100_000):
            x, ci = ev(p, np.sqrt(p * (1 - p) / N), paid.mean(), paid.std() / np.sqrt(N), size)
            row[f"EV {size // 1000}k"] = x
            row[f"IC {size // 1000}k"] = ci
            row[f"EV/mois {size // 1000}k"] = x / (row["mois_tentative"] + p * row["vie_mois"])
            row[f"refus max {size // 1000}k"] = refusal_breakeven(p, paid.mean(), size)
        rows.append(row)
        say(f"\n{k} : passage {p:.1%} en {row['trades_eval']:.0f} trades (≈ {row['mois_eval']:.1f} mois) ; financé "
            f"{row['v_pct']:.1f} % du capital, P(reward) {row['p_reward']:.0%}, {row['n_rewards']:.1f} rewards, vie "
            f"{row['vie_mois']:.0f} mois, 1er reward ≈ {row['premier_reward_mois']:.1f} mois ; EV {row['EV 10k']:+,.0f} $ "
            f"(10k) / {row['EV 100k']:+,.0f} $ (100k) ; par mois d'emplacement {row['EV/mois 10k']:+,.0f} / "
            f"{row['EV/mois 100k']:+,.0f} $")
    pd.DataFrame(rows).to_csv(OUT / "ftmo.csv", index=False)
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
