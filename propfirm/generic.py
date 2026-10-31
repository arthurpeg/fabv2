"""Moteur générique de prop firm (éval en une étape + compte financé), vectorisé sur les nuits de départ.

Un compte = une nuit de départ ; tous les comptes avancent en parallèle, un trade par nuit (propfirm.nights).
Tout est en dollars au capital nominal du compte (`Firm.size`). Deux façons d'exécuter un trade :
- CFD (FTMO, FundedNext, FundingPips, The5ers, STF) : taille continue, notionnel = risque / (stop + coût), coût
  = 1,5 point au niveau actuel du NQ (comme run_propfirm_vbt) ; plafond de levier éventuel (notionnel ≤ lev × capital) ;
- futures (Topstep, Apex, MyFundedFutures, Tradeify, Lucid) : n MNQ entiers, n = plancher(risque / perte d'un MNQ au
  stop, coût compris), distances au niveau actuel du NQ (25 684), plafond de contrats (scaling) ; nuit sautée si n = 0.
Gestion du risque : risque = k × perte max, borné par la marge avant le plancher et par la perte du jour ; objectif
en R (rr), ramené en éval au reste à faire (cible et consistance) si `cap_tp`.
Pertes max : « static » (fixe sous le capital initial), « eod » (suit le plus haut solde de clôture), « intraday »
(suit le plus haut latent : approximé par le plus haut R atteint pendant la nuit), avec blocage éventuel à
`lock_floor` dès que le plus haut dépasse `lock_at`. Perte du jour : dure (compte perdu) ou souple (perte coupée au
montant, compte gardé).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from propfirm.nights import K_N, K_STEP, NEVER, NightLib

P_REF, MNQ_PT, CFD_COST = 25_684.0, 2.0, 1.5 / 25_684.0


@dataclass
class Firm:
    name: str
    kind: str                      # "cfd" ou "fut"
    size: float
    fee: float                     # prix de l'éval (1re tentative)
    target: float
    dd: float
    dd_type: str = "static"
    lock_at: float | None = None
    lock_floor: float = 0.0
    dll: float | None = None
    dll_soft: bool = False
    consist: float | None = None   # meilleur jour ≤ consist × profit pour valider
    min_days: int = 0
    min_win_days: int = 0
    max_cal_days: int | None = None
    max_micros: int | None = None
    lev: float | None = None
    news_e: bool = False           # éval : à plat avant les annonces 8:30
    monthly: bool = False          # abonnement : `fee` par tranche de 30 jours d'éval
    activation: float = 0.0
    review: int = 1
    # financé
    f_dd: float | None = None
    f_dd_type: str | None = None
    f_lock_at: float | None = None
    f_lock_floor: float = 0.0
    f_dll: float | None = None
    f_dll_soft: bool = False
    f_tiers: list | None = None    # [(profit min, micros max, perte du jour)] du plus bas au plus haut
    f_max_micros: int | None = None
    f_lev: float | None = None
    f_risk_cap: float | None = None
    news_f: bool = False
    pay_first_days: int = 0        # jours calendaires depuis l'ouverture du financé
    pay_every_days: int = 0        # jours calendaires depuis le dernier retrait
    pay_min_days: int = 0          # jours tradés dans le cycle
    win_days: int = 0              # jours à ≥ win_min dans le cycle
    win_min: float = 0.0
    f_consist: float | None = None # meilleur jour ≤ f_consist × profit du cycle
    pay_frac: float = 1.0
    pay_keep: float = 0.0          # profit à laisser sur le compte
    pay_caps: tuple | None = None  # plafond par retrait (le dernier se répète)
    pay_min: float = 0.0
    pay_balance: float | None = None  # profit minimal pour demander
    split: tuple = (0.9,)          # part du trader par retrait (la dernière se répète)
    after: str = "reset"           # "reset" : le solde revient au capital ; "keep" : on retire le montant
    lock_after_pay: float | None = None
    max_payouts: int | None = None
    refund_at: int | None = None
    milestone: float | None = None # The5ers : retrait de tout le profit à +milestone, puis montée de taille
    ladder: tuple | None = None
    notes: str = ""
    extra: dict = field(default_factory=dict)

    def fund(self, k):
        v = getattr(self, "f_" + k)
        return getattr(self, k) if v is None else v


def _floor(hi, locked, dd, dd_type, lock_at, lock_floor):
    if dd_type == "static":
        fl = np.full(len(hi), -dd)
    else:
        fl = hi - dd
    if lock_at is not None:
        fl = np.where(locked | (hi >= lock_at), lock_floor, fl)
    return fl


def _trade(lib: NightLib, kind, i, side, v, risk, tp_R, cap, lev_cap):
    """→ (pnl $, plus haut latent $, tradé ?) pour un risque visé et un objectif en R."""
    s = lib.s[i]
    if kind == "fut":
        per = s * P_REF * MNQ_PT + lib.cost[i]
        n = np.floor(risk / per)
        if cap is not None:
            n = np.minimum(n, cap)
        perR, cost = n * s * P_REF * MNQ_PT, n * lib.cost[i]
    else:
        N = risk / (s + CFD_COST)
        if lev_cap is not None:
            N = np.minimum(N, lev_cap)
        perR, cost = N * s, N * CFD_COST
    traded = perR > 0
    kidx = np.clip(np.ceil(np.maximum(tp_R, K_STEP) / K_STEP - 1e-9).astype(int) - 1, 0, K_N - 1)
    tpb = lib.tp_bar[v, i, side, kidx]
    sb = lib.stop_bar[v, i, side]
    win = tpb < sb
    lost = ~win & (sb != NEVER)
    R = np.where(win, K_STEP * (kidx + 1), np.where(lost, -lib.stop_R[v, i, side], lib.eod_R[v, i, side]))
    pk = np.where(win, K_STEP * (kidx + 1), np.where(lost, lib.mfe_stop[v, i, side], lib.mfe_all[v, i, side]))
    return perR * R - cost, perR * pk, traded, perR, cost


def _side(lib, i, rng):
    if rng is None:
        return np.where(lib.dir[i] > 0, 0, 1)
    return rng.integers(0, 2, len(i))


def run_eval(f: Firm, lib: NightLib, starts, k, rr, cap_tp=True, rng=None, max_steps=3000):
    """→ dict(ok, nuits, jours calendaires, cause) ; causes : 1 plancher, 2 perte du jour, 3 marge, 4 délai, 5 données."""
    n0 = len(starts)
    P = np.zeros(n0); hi = np.zeros(n0); best = np.zeros(n0)
    days = np.zeros(n0, int); wins = np.zeros(n0, int); t = np.zeros(n0, int)
    st = np.zeros(n0, int); cause = np.zeros(n0, int)
    cal = (lib.dates - lib.dates[0]).days.to_numpy()
    v = 1 if f.news_e else 0
    lev_cap = f.lev * f.size if f.lev else None
    for _ in range(max_steps):
        a = np.flatnonzero(st == 0)
        if not len(a):
            break
        i = starts[a] + t[a]
        out = i >= lib.n
        st[a[out]] = -1; cause[a[out]] = 5
        a, i = a[~out], i[~out]
        if f.max_cal_days is not None:
            late = cal[i] - cal[starts[a]] >= f.max_cal_days
            st[a[late]] = -1; cause[a[late]] = 4
            a, i = a[~late], i[~late]
        fl = _floor(hi[a], np.zeros(len(a), bool), f.dd, f.dd_type, f.lock_at, f.lock_floor)
        room = P[a] - fl
        risk = np.minimum(k * f.dd, room)
        if f.dll is not None:
            risk = np.minimum(risk, f.dll * (0.999 if not f.dll_soft else 1.0))
        need = f.target - P[a]
        if f.consist:
            need = np.maximum(need, best[a] / f.consist - P[a])
        side = _side(lib, i, rng)
        # objectif : rr, ou le reste à faire s'il est plus petit (coût compris)
        pnl0, _, _, perR, cost = _trade(lib, f.kind, i, side, 0, risk, np.full(len(a), rr), f.max_micros, lev_cap)
        tpR = np.where(cap_tp & (perR > 0), np.minimum(rr, (np.maximum(need, 1.0) + cost) / np.where(perR > 0, perR, 1)), rr)
        pnl, pk, traded, perR, cost = _trade(lib, f.kind, i, side, v, risk, tpR, f.max_micros, lev_cap)
        stuck = ~traded & (room < np.median(lib.s) * P_REF * MNQ_PT + 2) if f.kind == "fut" else (risk < 5e-4 * f.size)
        st[a[stuck]] = -1; cause[a[stuck]] = 3
        if f.dll is not None and f.dll_soft:
            pnl = np.maximum(pnl, -f.dll)
        t[a] += 1
        ok_t = traded & ~stuck
        if f.dd_type == "intraday":
            hi_i = np.maximum(hi[a], P[a] + pk)
            fl = _floor(hi_i, np.zeros(len(a), bool), f.dd, f.dd_type, f.lock_at, f.lock_floor)
        newP = P[a] + np.where(ok_t, pnl, 0.0)
        breach = ok_t & (newP <= fl + 1e-6)
        dlb = ok_t & (f.dll is not None) & (not f.dll_soft) & (pnl <= -(f.dll or 0) + 1e-6)
        P[a] = newP
        days[a] += ok_t; wins[a] += ok_t & (pnl > 0)
        best[a] = np.maximum(best[a], np.where(ok_t, pnl, -np.inf))
        hi[a] = np.maximum(hi_i if f.dd_type == "intraday" else hi[a], P[a])
        bad = (breach | dlb) & ~stuck
        st[a[bad]] = -1; cause[a[bad]] = np.where(breach[bad], 1, 2)
        good = ~bad & ~stuck & (P[a] >= f.target) & (days[a] >= f.min_days) & (wins[a] >= f.min_win_days)
        if f.consist:
            good &= best[a] <= f.consist * P[a] + 1e-6
        st[a[good]] = 1
    end = np.minimum(starts + np.maximum(t - 1, 0), lib.n - 1)
    return dict(ok=st == 1, nuits=t, jours=cal[end] - cal[starts], fin=end, cause=cause)


def run_funded(f: Firm, lib: NightLib, starts, k, rr, rng=None, max_steps=1500):
    """→ dict(paid : part du trader + remboursement, npay, vie, premier, cause) ; causes : 1 plancher, 2 perte du
    jour, 3 marge, 6 nombre max de retraits, 5 fin des données."""
    n0 = len(starts)
    dd, dd_type = f.fund("dd"), f.fund("dd_type")
    lock_at = f.f_lock_at if f.f_dd is not None or f.f_lock_at is not None else f.lock_at
    lock_floor = f.f_lock_floor if f.f_dd is not None or f.f_lock_at is not None else f.lock_floor
    dll0 = f.fund("dll")
    soft = f.f_dll_soft if f.f_dll is not None else f.dll_soft
    v = 1 if f.news_f else 0
    cal = (lib.dates - lib.dates[0]).days.to_numpy()
    P = np.zeros(n0); hi = np.zeros(n0); best = np.zeros(n0); locked = np.zeros(n0, bool)
    cpnl = np.zeros(n0); cdays = np.zeros(n0, int); cwin = np.zeros(n0, int)
    t = np.zeros(n0, int); alive = np.ones(n0, bool); cause = np.zeros(n0, int)
    npay = np.zeros(n0, int); paid = np.zeros(n0); first = np.full(n0, -1)
    scale = np.ones(n0); rung = np.zeros(n0, int)
    last = cal[np.minimum(starts, lib.n - 1)].astype(float)
    t0 = last.copy()
    split = np.array(f.split); caps = np.array(f.pay_caps) if f.pay_caps else None
    for _ in range(max_steps):
        a = np.flatnonzero(alive)
        if not len(a):
            break
        i = starts[a] + t[a]
        out = i >= lib.n
        alive[a[out]] = False; cause[a[out]] = 5
        a, i = a[~out], i[~out]
        sc = scale[a]
        fl = _floor(hi[a], locked[a], dd * sc, dd_type, None if lock_at is None else lock_at * sc, lock_floor * sc)
        room = P[a] - fl
        cap, dll = f.fund("max_micros"), (None if dll0 is None else np.full(len(a), dll0 * sc))
        if f.f_tiers:
            th = np.array([x[0] for x in f.f_tiers]); j = np.searchsorted(th, P[a], side="right") - 1
            j = np.clip(j, 0, len(th) - 1)
            cap = np.array([x[1] for x in f.f_tiers])[j]
            if f.f_tiers[0][2] is not None:
                dll = np.array([x[2] for x in f.f_tiers], float)[j]
        risk = np.minimum(k * dd * sc, room)
        if dll is not None:
            risk = np.minimum(risk, dll * (1.0 if soft else 0.999))
        if f.f_risk_cap:
            risk = np.minimum(risk, f.f_risk_cap * sc)
        lev = f.fund("lev")
        side = _side(lib, i, rng)
        pnl, pk, traded, perR, cost = _trade(lib, f.kind, i, side, v, risk, np.full(len(a), rr), cap,
                                             None if lev is None else lev * f.size * sc)
        stuck = ~traded & (room < np.median(lib.s) * P_REF * MNQ_PT + 2) if f.kind == "fut" else (risk < 5e-4 * f.size * sc)
        alive[a[stuck]] = False; cause[a[stuck]] = 3
        if dll is not None and soft:
            pnl = np.maximum(pnl, -dll)
        t[a] += 1
        ok_t = traded & ~stuck
        if dd_type == "intraday":
            hi_i = np.maximum(hi[a], P[a] + pk)
            fl = _floor(hi_i, locked[a], dd * sc, dd_type, None if lock_at is None else lock_at * sc, lock_floor * sc)
        newP = P[a] + np.where(ok_t, pnl, 0.0)
        breach = ok_t & (newP <= fl + 1e-6)
        dlb = ok_t & (dll is not None) & (not soft) & (pnl <= -(dll if dll is not None else 0) + 1e-6)
        P[a] = newP
        cpnl[a] += np.where(ok_t, pnl, 0); cdays[a] += ok_t; cwin[a] += ok_t & (pnl >= f.win_min * sc) & (pnl > 0)
        best[a] = np.maximum(best[a], np.where(ok_t, pnl, -np.inf))
        hi[a] = np.maximum(hi_i if dd_type == "intraday" else hi[a], P[a])
        if lock_at is not None:
            locked[a] |= hi[a] >= lock_at * sc
        bad = (breach | dlb) & ~stuck
        alive[a[bad]] = False; cause[a[bad]] = np.where(breach[bad], 1, 2)
        # retrait
        b = a[~bad & ~stuck]
        if not len(b):
            continue
        now = cal[starts[b] + t[b] - 1]
        if f.milestone is not None:
            due = P[b] >= f.milestone * f.size * scale[b]
            amt = P[b].copy()
        else:
            due = np.where(npay[b] == 0, now - t0[b] >= f.pay_first_days, now - last[b] >= f.pay_every_days)
            due &= (cdays[b] >= f.pay_min_days) & (cwin[b] >= f.win_days) & (cpnl[b] > 0)
            if f.f_consist:
                due &= best[b] <= f.f_consist * cpnl[b] + 1e-6
            if f.pay_balance is not None:
                due &= P[b] >= f.pay_balance
            amt = np.minimum(f.pay_frac * P[b], P[b] - f.pay_keep)
            if caps is not None:
                amt = np.minimum(amt, caps[np.minimum(npay[b], len(caps) - 1)])
            due &= amt >= max(f.pay_min, 1e-9)
        c = b[due]
        if not len(c):
            continue
        amt = amt[due]
        sp = split[np.minimum(npay[c], len(split) - 1)]
        npay[c] += 1
        paid[c] += sp * amt + np.where(npay[c] == (f.refund_at or -1), f.fee, 0.0)
        first[c] = np.where(first[c] < 0, t[c], first[c])
        last[c] = cal[starts[c] + t[c] - 1]
        if f.after == "reset":
            P[c] = 0.0; hi[c] = 0.0
        else:
            P[c] -= amt
            if f.lock_after_pay is not None:
                locked[c] = True
        if f.milestone is not None and f.ladder:
            rung[c] = np.minimum(rung[c] + 1, len(f.ladder) - 1)
            scale[c] = np.array(f.ladder)[rung[c]] / f.size
        best[c] = 0.0; cpnl[c] = 0.0; cdays[c] = 0; cwin[c] = 0
        if f.max_payouts:
            done = c[npay[c] >= f.max_payouts]
            alive[done] = False; cause[done] = 6
    return dict(paid=paid, npay=npay, vie=t, premier=first, cause=cause)
