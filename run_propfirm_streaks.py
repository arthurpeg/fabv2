"""Exploratoire (non pré-enregistré) : pires séries d'évals ratées et plus longues périodes sans reward,
règle NQ de nuit sur FTMO 1-Step (réglage principal de l'avenant C du n° 18).

uv run python run_propfirm_streaks.py [TP_FINANCÉ]  → results/propfirm_streaks[_tp<TP>]/ (run.log, starts_*.csv, events_2011.csv)

TP_FINANCÉ (ATR) : en financé, trades de la règle avec cet objectif (cache/propfirm/nq_nuit_tp<TP>.parquet,
build_nq_nuit_tp.py) ; par défaut, mêmes trades qu'en éval (TP 5 ATR).

Un emplacement suit l'historique réel sans bouclage : achat d'une éval, validation ou échec, 3 nuits de
vérification, compte financé jusqu'à la perte max, rachat le lendemain. Éval 2 % de risque, financé 1 %,
spread 1,5 point, reward au 10e trade du compte, RAZ de la perte max (règles vérifiées sur ftmo.com).
On le lance depuis chaque nuit de départ possible (tous les 5 trades) jusqu'à la fin des données
(2026-08-28), et on mesure pour chaque départ :
- la plus longue série d'évals ratées d'affilée (nombre, frais perdus, nuits écoulées) ;
- la plus longue période sans reward (entre deux rewards, ou du départ au premier reward) ;
- le creux maximal de la trésorerie cumulée (frais payés − rewards reçus), en $ et en durée.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.ftmo import DAILY, EUR, MAXLOSS, PRICES_EUR, SPLIT, TARGET

sys.stdout.reconfigure(encoding="utf-8")
TP_F = sys.argv[1] if len(sys.argv) > 1 else None
OUT = Path("results/propfirm_streaks" + (f"_tp{TP_F}" if TP_F else ""))
R_EVAL, R_FUND, CYCLE, REVIEW = 2.0, 1.0, 10, 3
COST = 1.5 / 25_684.0
TOL = 1e-3  # % du capital (0,10 $ sur 10k) : tolérance sur tous les seuils (perte max, objectif, meilleur jour)
STEP = 5
MIN_NIGHTS = 504  # au moins 2 ans d'historique après le départ

t = pd.read_csv("results/couts_reels_nq_nuit/trades.csv", parse_dates=["night"]).sort_values("entry_idx")
R = t.R_brut.to_numpy()
C = COST / t.risk.fillna(t.risk.median()).to_numpy()
NIGHT = t.night.dt.date.to_numpy()
NT = len(R)
RF, CF = R, C  # trades du compte financé
if TP_F:
    f = pd.read_parquet(f"cache/propfirm/nq_nuit_tp{TP_F}.parquet").sort_values("entry_idx")
    assert (f.entry_idx.to_numpy() == t.entry_idx.to_numpy()).all()
    RF = f.R_brut.to_numpy()
    CF = COST / f.risk.fillna(f.risk.median()).to_numpy()
LOG = None


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def trace(start: int) -> list[tuple[str, int, float]]:
    """Événements (type, indice de nuit, % du capital) d'un emplacement de `start` à la fin des données."""
    ev = []
    i = start
    while i < NT:
        ev.append(("achat", i, 0.0))
        P = hi = best = 0.0
        passed = False
        while i < NT:
            floor = hi - MAXLOSS
            risk = min(R_EVAL, P - floor)
            if risk < 0.05:  # marge épuisée : éval abandonnée, comme propfirm.ftmo.run_eval (MIN_RISK)
                break
            pnl = risk * (R[i] - C[i]) / (1 + C[i])
            P += pnl; i += 1
            if P <= floor + TOL or pnl <= -DAILY:
                break
            best = max(best, pnl); hi = max(hi, P)
            if P >= TARGET - TOL and best <= 0.5 * P + TOL:
                passed = True
                break
        ev.append(("validée" if passed else "ratée", i - 1, 0.0))
        if not passed:
            continue
        i += REVIEW
        P = hi = best = 0.0
        cyc = 0
        while i < NT:
            floor = hi - MAXLOSS
            risk = min(R_FUND, P - floor)
            if risk < 0.05:
                break
            pnl = risk * (RF[i] - CF[i]) / (1 + CF[i])
            P += pnl; i += 1; cyc += 1
            if P <= floor + TOL or pnl <= -DAILY:
                break
            best = max(best, pnl); hi = max(hi, P)
            if cyc >= CYCLE and P > TOL and best <= 0.5 * P + TOL:
                ev.append(("reward", i - 1, SPLIT * P))
                P = hi = best = 0.0; cyc = 0
        ev.append(("financé perdu", i - 1, 0.0))
        i += 1
    return ev


def stats(ev, start: int, size: int) -> dict:
    fee = PRICES_EUR[size] * EUR
    # séries d'évals ratées
    best_run, run, run_start, worst = 0, 0, None, (0, start, start)
    for k, j, _ in ev:
        if k == "ratée":
            if run == 0:
                run_start = j
            run += 1
            if run > best_run:
                best_run, worst = run, (run, run_start, j)
        elif k == "validée":
            run = 0
    # périodes sans reward
    pays = [j for k, j, _ in ev if k == "reward"]
    marks = [start] + pays
    gaps = np.diff(marks + [NT - 1]) if marks else np.array([NT - start])
    g = int(np.argmax(gaps))
    # trésorerie cumulée
    cash = np.zeros(NT - start)
    for k, j, x in ev:
        if k == "achat":
            cash[j - start] -= fee
        elif k == "reward":
            cash[j - start] += x / 100 * size
    cum = np.cumsum(cash)
    peak = np.maximum.accumulate(np.concatenate([[0.0], cum]))[1:]
    dd = cum - peak
    jd = int(np.argmin(dd))
    under = 0; longest_under = 0
    for x in dd:
        under = under + 1 if x < 0 else 0
        longest_under = max(longest_under, under)
    return dict(start=NIGHT[start], fails_max=best_run, fails_fees=best_run * fee,
                fails_from=NIGHT[worst[1]], fails_to=NIGHT[worst[2]], fails_nights=worst[2] - worst[1],
                nopay_nights=int(gaps[g]), nopay_from=NIGHT[marks[g]], nopay_to=NIGHT[min(marks[g] + gaps[g], NT - 1)],
                nopay_open=g == len(marks) - 1, cash_dd=dd[jd], cash_dd_at=NIGHT[start + jd],
                underwater_nights=longest_under, evals=sum(k == "achat" for k, _, _ in ev),
                rewards=len(pays), net=cum[-1])


def main() -> None:
    global LOG
    OUT.mkdir(parents=True, exist_ok=True)
    LOG = open(OUT / "run.log", "w", encoding="utf-8")
    say(f"financé : TP {TP_F or 5} ATR")
    say("Exploratoire — règle NQ de nuit sur FTMO 1-Step (éval 2 %, financé 1 %, 1,5 pt) ; séries sur l'historique réel")
    starts = np.arange(0, NT - MIN_NIGHTS, STEP)
    for size in (10_000, 100_000):
        S = pd.DataFrame([stats(trace(s), s, size) for s in starts])
        S.to_csv(OUT / f"starts_{size // 1000}k.csv", index=False)
        say(f"\n=== {size // 1000}k (éval {PRICES_EUR[size] * EUR:.0f} $) : {len(S)} départs de {S.start.min()} à {S.start.max()} ===")
        for col, lab, unit in [("fails_max", "évals ratées d'affilée", ""), ("fails_fees", "frais perdus dans cette série", " $"),
                               ("fails_nights", "durée de cette série (nuits)", ""),
                               ("nopay_nights", "plus longue période sans reward (nuits)", ""),
                               ("cash_dd", "creux de trésorerie cumulée", " $"),
                               ("underwater_nights", "plus longue durée sous le pic de trésorerie (nuits)", "")]:
            x = S[col]
            say(f"  {lab:<52} médiane {x.median():>9,.0f}{unit}   95e centile {x.quantile(0.95 if col != 'cash_dd' else 0.05):>9,.0f}{unit}"
                f"   pire {x.max() if col != 'cash_dd' else x.min():>9,.0f}{unit}".replace(",", " "))
        w = S.loc[S.fails_max.idxmax()]
        say(f"  pire série d'échecs : {w.fails_max} évals ratées du {w.fails_from} au {w.fails_to} ({w.fails_nights} nuits, {w.fails_fees:,.0f} $)".replace(",", " "))
        w = S.loc[S.nopay_nights.idxmax()]
        say(f"  plus longue période sans reward : {w.nopay_nights} nuits (~{w.nopay_nights / 21:.0f} mois), du {w.nopay_from} au {w.nopay_to}"
            + (" (encore ouverte à la fin des données)" if w.nopay_open else ""))
        w = S.loc[S.cash_dd.idxmin()]
        say(f"  pire creux de trésorerie : {w.cash_dd:,.0f} $ atteint le {w.cash_dd_at} (départ {w.start})".replace(",", " "))
        say(f"  par départ : {S.evals.median():.0f} évals achetées et {S.rewards.median():.0f} rewards (médianes), "
            f"gain net médian {S.net.median():,.0f} $".replace(",", " "))
        # épisodes datés : où tombent les pires périodes sans reward
        top = S.sort_values("nopay_nights", ascending=False).drop_duplicates("nopay_from").head(5)
        say("  5 plus longues périodes sans reward (dates distinctes) : " + " ; ".join(
            f"{r.nopay_from} → {r.nopay_to} ({r.nopay_nights} n.)" for r in top.itertuples()))
        top = S.sort_values("fails_max", ascending=False).drop_duplicates("fails_from").head(5)
        say("  5 pires séries d'échecs (dates distinctes) : " + " ; ".join(
            f"{r.fails_from} → {r.fails_to} ({r.fails_max} évals)" for r in top.itertuples()))
    ev = trace(0)
    pd.DataFrame([(k, NIGHT[j], x) for k, j, x in ev], columns=["event", "night", "pct"]).to_csv(OUT / "events_2011.csv", index=False)


if __name__ == "__main__":
    main()
