"""Exploratoire : plan « 2 coups » sur LucidFlex 50K (DLL désactivée, consistance 50 %), règle NQ de nuit en MNQ.

uv run python run_propfirm_lucid_plan.py  → results/propfirm_lucid_plan/ (run.log, attempts.csv, cycles.csv)

Plan demandé par l'utilisateur (2026-10-31) :
- éval : risque 2 000 $, objectif 1 500 $ par nuit (deux gains = 3 000 $, meilleur jour 50 %) ;
- financé, 1er trade : risque 2 000 $, objectif 3 400 $ (un stop = compte perdu) ;
- puis une position chaque nuit, risque 150 $ et objectif 150 $ (RR 1), jusqu'à 5 jours à ≥ 150 $ dans le cycle
  (le 1er trade compte pour un) ; payout = 50 % du profit, plafonné à 2 000 $ (4 × 150 $ gagnés → 3 400 + 600 = 4 000 $).
Règles LucidFlex 50K relues le 2026-10-31 sur support.lucidtrading.com (Customization, Evaluation, Funded, Payouts,
Consistency, Scaling Plan, Drawdown) : objectif 3 000 $, MLL 2 000 $ en fin de séance sous le plus haut solde de
clôture, bloquée à +100 $ dès que la clôture dépasse +2 100 $ et ramenée à +100 $ au premier payout ; consistance
50 % (option ; petite marge non modélisée) en éval seulement ; 4 minis / 40 micros en éval ; financé : 20 / 30 / 40
micros sous 1 000 / 2 000 / au-delà de profit (mis à jour en fin de séance) ; payout : 5 jours à ≥ 150 $ dans le
cycle et profit net du cycle > 0, montant 50 % du profit plafonné à 2 000 $, minimum 500 $, 90 % au trader, 5 payouts
puis passage en réel (non valorisé). Avec 2 000 $ de risque, la DLL (1 200 $, « soft breach ») doit être désactivée :
c'est la version la plus chère, dont le prix ne s'affiche qu'au paiement ; 130 $ selon l'utilisateur (EV aussi
donnée à 150, 200 et 250 $).

Marché : chaque nuit de la règle NQ de nuit (momentum 12-1, entrée à la clôture de la barre de 20:00 ET, sortie au
plus tard à la clôture de la barre de 9:29, comme run_propfirm_vbt.nights), barres 1 min. Distances converties en
points au niveau actuel du NQ (25 684, convention « prix actuels » de l'avenant D) ; MNQ à 2 $ le point ; coût réel par
MNQ et par aller-retour (demi-spreads bbo-1m + 1,50 $, cache/propfirm/lucid_trades.parquet).
- Gros trades (éval et 1er trade du financé) : stop 2 ATR M15 de la règle ; n = plancher(risque / perte d'un MNQ au
  stop, coût compris), plafonné par la taille max ; objectif placé pour gagner exactement le montant visé, coût déduit.
- Trades à 150 $ : 1 MNQ, stop et objectif placés pour perdre ou gagner exactement 150 $ coût compris.
- Ordre d'exécution : objectif touché strictement avant le stop (même barre = stop) ; stop rempli au pire du stop et de
  l'ouverture de la barre ; sinon sortie à 9:30.
- Si la nuit sort à 9:30 sans toucher l'un ou l'autre, on recommence la nuit suivante avec le montant qui reste
  (objectif = reste à faire, risque = min(2 000 $, marge avant la MLL)). En éval, l'objectif tient aussi compte de la
  consistance (reste = max(3 000 − P, 2 × meilleur jour − P)).
Après le 1er payout, deux lectures : (a) on s'arrête là (un seul payout) ; (b) on recommence le même cycle (gros trade
vers 3 400 $ de profit avec le risque que permet la marge, puis trades à 150 $) jusqu'au 5e payout ou à la perte.
Contrôle sans edge : sens tiré à pile ou face (10 tirages).
Une tentative par nuit de départ, 2011-07 → 2025-08 (au moins un an de données après le départ).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_propfirm_vbt as V

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_lucid_plan")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
CACHE = Path("cache/propfirm/nq_nuit_paths.npz")
P_REF, MNQ_PT = 25_684.0, 2.0
TARGET, MLL, LOCK_AT, LOCK_FLOOR, CONSIST, EVAL_MAX = 3000.0, 2000.0, 2100.0, 100.0, 0.5, 40
DAY_MIN, DAYS_NEEDED, PAY_FRAC, PAY_CAP, PAY_MIN, MAX_PAYOUTS, SPLIT = 150.0, 5, 0.5, 2000.0, 500.0, 5, 0.9
BIG_RISK, EVAL_TP, FUND_GOAL, SMALL = 2000.0, 1500.0, 3400.0, 150.0
FEES = (130, 150, 200, 250)
TAIL = 252  # nuits de données exigées après le départ


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def paths():
    """Par nuit : maxima cumulés de la hausse et de la baisse depuis l'entrée (fractions du prix), mouvement à
    l'ouverture de chaque barre, mouvement final ; sens de la règle, stop 2 ATR, coût par MNQ."""
    if CACHE.exists():
        z = np.load(CACHE, allow_pickle=True)
        return {k: z[k] for k in z.files}
    from recolte1.engine import load

    df = load("NQ").copy()
    df.attrs = {}
    e, _ = V.nights("20:00", df)
    O, Hh, L, C = (df[c].to_numpy() for c in ("open", "high", "low", "close"))
    off, up, dn, oup, odn, end = [0], [], [], [], [], []
    for a, b in zip(e.p_in.to_numpy(), e.p_out.to_numpy()):
        x = C[a]
        sl = slice(a + 1, b + 1)
        up.append(np.maximum.accumulate((Hh[sl] - x) / x)); dn.append(np.maximum.accumulate((x - L[sl]) / x))
        oup.append((O[sl] - x) / x); odn.append((x - O[sl]) / x)
        end.append((C[b] - x) / x)
        off.append(off[-1] + b - a)
    cost = pd.read_parquet("cache/propfirm/lucid_trades.parquet").set_index("night")["cost"]
    out = dict(night=e.night.to_numpy(), dir=e.dir.to_numpy(), stop=2 * e.atr_frac.to_numpy(),
               cost=cost.reindex(e.night.values).fillna(2.0).to_numpy(), off=np.array(off),
               up=np.concatenate(up), dn=np.concatenate(dn), oup=np.concatenate(oup), odn=np.concatenate(odn),
               end=np.array(end))
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez(CACHE, **out)
    return out


Z = paths()
NT = len(Z["night"])


KIND = {}  # issue du dernier appel à move() : "objectif", "stop" ou "9:30"


def move(i: int, d: int, s: float, t: float) -> float:
    """Mouvement réalisé (fraction du prix, signé dans le sens du trade) avec stop s et objectif t."""
    a, b = Z["off"][i], Z["off"][i + 1]
    fav, adv, aop = (Z["up"], Z["dn"], Z["odn"]) if d > 0 else (Z["dn"], Z["up"], Z["oup"])
    js = np.searchsorted(adv[a:b], s - 1e-12)
    jt = np.searchsorted(fav[a:b], t - 1e-12)
    m = b - a
    if jt < m and jt < js:
        KIND["k"] = "objectif"
        return t
    if js < m:
        KIND["k"] = "stop"
        return -max(s, aop[a + js])
    KIND["k"] = "9:30"
    return d * Z["end"][i]


def big_trade(i: int, d: int, risk: float, goal: float, cap: int) -> float:
    """P&L net en $ d'un trade au stop 2 ATR : n MNQ pour perdre au plus `risk`, objectif à +`goal` net."""
    c = Z["cost"][i]
    per = Z["stop"][i] * P_REF * MNQ_PT + c
    n = min(int(risk // per), cap)
    if n < 1:
        return np.nan
    t = (goal + n * c) / (n * MNQ_PT * P_REF)
    return n * (MNQ_PT * P_REF * move(i, d, Z["stop"][i], t) - c)


def small_trade(i: int, d: int) -> float:
    """1 MNQ, perte ou gain de 150 $ net (coût compris)."""
    c = Z["cost"][i]
    s, t = (SMALL - c) / (MNQ_PT * P_REF), (SMALL + c) / (MNQ_PT * P_REF)
    return MNQ_PT * P_REF * move(i, d, s, t) - c


def floor_of(hi: float, locked: bool) -> float:
    return LOCK_FLOOR if locked or hi >= LOCK_AT else hi - MLL


def run_eval(s0: int, dirs: np.ndarray):
    """→ (validée, nuit de fin, nuits tradées, cause)."""
    P = hi = best = 0.0
    i, n = s0, 0
    while i < NT:
        fl = floor_of(hi, False)
        room = P - fl
        need = max(TARGET - P, 2 * best - P)
        pnl = big_trade(i, dirs[i], min(BIG_RISK, room), min(EVAL_TP, need), EVAL_MAX)
        i += 1
        if np.isnan(pnl):
            if room < Z["stop"][i - 1] * P_REF * MNQ_PT + Z["cost"][i - 1]:
                return False, i - 1, n, "marge épuisée"
            continue
        n += 1
        P += pnl
        if P <= fl + 1e-9:
            return False, i - 1, n, "MLL"
        best = max(best, pnl); hi = max(hi, P)
        if P >= TARGET and best <= CONSIST * P + 1e-9:
            return True, i - 1, n, ""
    return False, NT - 1, n, "fin des données"


def scaling(P: float) -> int:
    return 40 if P >= 2000 else 30 if P >= 1000 else 20


def run_funded(s0: int, dirs: np.ndarray, repeat: bool):
    """Financé ouvert la nuit s0. → (payouts bruts [$], nuits de vie, nuit du 1er payout ou -1, cause de fin)."""
    P = hi = 0.0
    locked = False
    pays, first = [], -1
    i = s0
    while i < NT:
        cyc_pnl, cyc_days, phase = 0.0, 0, "gros"
        while i < NT:
            fl = floor_of(hi, locked)
            room = P - fl
            if phase == "gros" and P >= FUND_GOAL:
                phase = "150"
            if phase == "gros":
                pnl = big_trade(i, dirs[i], min(BIG_RISK, room), FUND_GOAL - P, scaling(P))
            else:
                pnl = small_trade(i, dirs[i]) if room > SMALL + 1e-9 else np.nan
            i += 1
            if np.isnan(pnl):
                if room < SMALL:
                    return pays, i - s0, first, "marge épuisée"
                continue
            P += pnl; cyc_pnl += pnl; cyc_days += pnl >= DAY_MIN
            if P <= fl + 1e-9:
                return pays, i - s0, first, "MLL" + (" (gros trade)" if phase == "gros" else " (trades à 150 $)")
            hi = max(hi, P); locked |= hi >= LOCK_AT
            amt = min(PAY_FRAC * P, PAY_CAP)
            if cyc_days >= DAYS_NEEDED and cyc_pnl > 0 and amt >= PAY_MIN:
                pays.append(amt); P -= amt; locked = True
                first = i - 1 - s0 if first < 0 else first
                break
        else:
            break
        if not repeat or len(pays) >= MAX_PAYOUTS:
            return pays, i - s0, first, "arrêt volontaire" if not repeat else "5 payouts (réel)"
    return pays, i - s0, first, "fin des données"


def attempts(dirs: np.ndarray, repeat: bool) -> pd.DataFrame:
    rows = []
    for s0 in range(0, NT - TAIL):
        ok, j, n, why = run_eval(s0, dirs)
        r = dict(start=s0, ok=ok, nuits_eval=j - s0 + 1, trades_eval=n, cause_eval=why, paid=0.0, npay=0,
                 vie=0, premier=-1, fin="")
        if ok:
            pays, vie, first, fin = run_funded(j + 1, dirs, repeat)
            r.update(paid=SPLIT * sum(pays), npay=len(pays), vie=vie, premier=first, fin=fin,
                     pay1=pays[0] if pays else 0.0)
        rows.append(r)
    return pd.DataFrame(rows)


def summary(A: pd.DataFrame, lab: str) -> dict:
    F = A[A.ok]
    v = F.paid.mean()
    p = A.ok.mean()
    se = A.paid.std() / np.sqrt(len(A)) * np.sqrt(10)  # départs chevauchants : erreur-type grossière
    say(f"  {lab} : passage {p:.1%} (nuits par éval : {A.nuits_eval.median():.0f} médiane, validées {F.nuits_eval.median():.0f}) ; "
        f"financé : P(≥ 1 payout) {(F.npay > 0).mean():.0%}, {F.npay.mean():.2f} payouts, valeur {v:_.0f} $ (90 %) ; "
        f"valeur par éval {p * v:_.0f} $ ± {1.96 * se:_.0f} → EV ".replace("_", " ")
        + ", ".join(f"{p * v - f:+_.0f} $ à {f} $".replace("_", " ") for f in FEES)
        + f" ; prix d'équilibre {p * v:_.0f} $".replace("_", " "))
    return dict(p=p, v=v, ev0=p * v)


def main() -> None:
    say(f"Plan « 2 coups » LucidFlex 50K (DLL OFF, consistance 50 %), règle NQ de nuit en MNQ ; {NT} nuits "
        f"{pd.Timestamp(Z['night'][0]).date()} → {pd.Timestamp(Z['night'][-1]).date()} ; {NT - TAIL} départs")
    per = Z["stop"] * P_REF * MNQ_PT + Z["cost"]
    n_big = np.minimum(BIG_RISK // per, EVAL_MAX)
    say(f"  stop 2 ATR au niveau actuel : médiane {np.median(Z['stop'] * P_REF):.0f} points ({np.median(per):.0f} $ par MNQ) ; "
        f"risque 2 000 $ → {np.median(n_big):.0f} MNQ en médiane, plafond 40 atteint {np.mean(BIG_RISK // per > EVAL_MAX):.1%} "
        f"des nuits, 20 (financé sous 1 000 $) {np.mean(BIG_RISK // per > 20):.1%} ; risque réel médian {np.median(n_big * per):.0f} $")
    say(f"  objectif 1 500 $ ≈ {np.median(EVAL_TP / (n_big * per)):.2f} R, 3 400 $ ≈ {np.median(FUND_GOAL / (np.minimum(BIG_RISK // per, 20) * per)):.2f} R "
        f"(médianes) ; trade à 150 $ : stop et objectif ≈ {np.median((SMALL - Z['cost']) / MNQ_PT):.0f} points")

    rule = Z["dir"].astype(int)
    say("\n1. Un trade isolé (chaque nuit, toutes les nuits) :")
    for lab, f in (("éval 2 000 $ → +1 500 $", lambda i: big_trade(i, rule[i], BIG_RISK, EVAL_TP, EVAL_MAX)),
                   ("financé 2 000 $ → +3 400 $ (20 MNQ max)", lambda i: big_trade(i, rule[i], BIG_RISK, FUND_GOAL, 20)),
                   ("150 $ → +150 $", lambda i: small_trade(i, rule[i]))):
        x, k = [], []
        for i in range(NT):
            v = f(i)
            if not np.isnan(v):
                x.append(v); k.append(KIND["k"])
        x, k = np.array(x), pd.Series(k)
        say(f"  {lab} : " + ", ".join(f"{q} {v:.1%}" for q, v in k.value_counts(normalize=True).items())
            + f" ; P&L moyen {x.mean():+.0f} $ (sorties à 9:30 : {x[(k == '9:30').to_numpy()].mean():+.0f} $), pire {x.min():+.0f} $")

    say("\n2. Une tentative par nuit de départ")
    res = {}
    for repeat in (False, True):
        A = attempts(rule, repeat)
        A.to_csv(OUT / f"attempts_{'repete' if repeat else 'un_payout'}.csv", index=False)
        lab = "(b) cycle répété jusqu'à 5 payouts" if repeat else "(a) un seul payout"
        res[repeat] = summary(A, f"règle, {lab}")
        F = A[A.ok]
        say(f"    éval ratée : " + ", ".join(f"{k} {v:.0%}" for k, v in A[~A.ok].cause_eval.value_counts(normalize=True).items())
            + " ; fin du financé : " + ", ".join(f"{k} {v:.0%}" for k, v in F.fin.value_counts(normalize=True).items()))
        g = F[F.npay > 0]
        say(f"    1er payout : {g.pay1.mean():_.0f} $ brut en moyenne (2 000 $ dans {(g.pay1 >= PAY_CAP - 1e-6).mean():.0%} des cas), "
            f"{g.premier.median():.0f} nuits après l'ouverture du financé (75e centile {g.premier.quantile(0.75):.0f}) ; "
            f"payouts : ".replace("_", " ") + ", ".join(f"{k} : {v:.0%}" for k, v in F.npay.value_counts(normalize=True).sort_index().items()))
    rng = np.random.default_rng(2026)
    for repeat in (False, True):
        S = []
        for _ in range(10):
            d = np.where(rng.random(NT) < 0.5, 1, -1)
            A = attempts(d, repeat)
            S.append((A.ok.mean(), A[A.ok].paid.mean()))
        p, v = np.mean([s[0] for s in S]), np.mean([s[1] for s in S])
        say(f"  sans edge (sens au hasard, 10 tirages), {'(b)' if repeat else '(a)'} : passage {p:.1%}, valeur du financé {v:_.0f} $, "
            f"valeur par éval {p * v:_.0f} $ → EV {p * v - FEES[0]:+_.0f} $ à {FEES[0]} $".replace("_", " "))

    say("\n3. Un seul compte racheté à chaque échec, plan (a), départs toutes les 5 nuits, horizon 1 an (252 nuits)")
    rows = []
    for s0 in range(0, NT - TAIL - 252, 5):
        i, cash, low, nev, run, worst = s0, 0.0, 0.0, 0, 0, 0
        while i < s0 + 252:
            cash -= FEES[0]; low = min(low, cash); nev += 1
            ok, j, _, _ = run_eval(i, rule)
            if not ok:
                run += 1; worst = max(worst, run); i = j + 1
                continue
            run = 0
            pays, vie, _, _ = run_funded(j + 1, rule, False)
            cash += SPLIT * sum(pays)
            i = j + 1 + vie
        rows.append(dict(start=s0, net=cash, mise=-low, evals=nev, pire_serie=worst))
    Rr = pd.DataFrame(rows)
    Rr.to_csv(OUT / "rachat_1an.csv", index=False)
    say(f"  à {FEES[0]} $ l'éval : gain net sur 1 an médiane {Rr.net.median():+_.0f} $, 5e centile {Rr.net.quantile(0.05):+_.0f} $, "
        f"pire {Rr.net.min():+_.0f} $ ; argent sorti avant remboursement médiane {Rr.mise.median():_.0f} $, 95e centile "
        f"{Rr.mise.quantile(0.95):_.0f} $, pire {Rr.mise.max():_.0f} $ ; {Rr.evals.median():.0f} évals par an ; pire série "
        f"d'évals ratées {Rr.pire_serie.max()}".replace("_", " "))


if __name__ == "__main__":
    main()
