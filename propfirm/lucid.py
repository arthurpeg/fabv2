"""Moteur LucidFlex 50K : éval et compte financé, un trade par séance, en MNQ (PREREGISTRATION_18, avenant D).

Tout est en dollars de profit par rapport au solde initial. Les comptes avancent en parallèle ;
chaque compte part d'un trade tiré au hasard et enchaîne les suivants (bouclage).

Un trade : n MNQ, P&L = n × (stop_pts × 2 $ × R − coût par contrat). n = plancher(risque visé /
(stop_pts × 2 $)), plafonné par la taille max et par la marge avant la MLL ; 0 → nuit sautée. Compte abandonné quand la
marge tombe sous la perte d'un MNQ au stop un soir médian.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

TARGET, MLL, LOCK_AT, LOCK_FLOOR = 3000.0, 2000.0, 2100.0, 100.0
MNQ_PT = 2.0
EVAL_MAX = 40
DAY_MIN, DAYS_NEEDED, PAY_FRAC, PAY_CAP, PAY_MIN, MAX_PAYOUTS, SPLIT = 150.0, 5, 0.5, 2000.0, 500.0, 5, 0.9


@dataclass
class Trades:
    R: np.ndarray         # R brut
    stop_pts: np.ndarray  # distance du stop en points NQ
    cost: np.ndarray      # coût par MNQ aller-retour en $

    @property
    def n(self) -> int:
        return len(self.R)

    @property
    def min_room(self) -> float:
        """Perte d'un MNQ au stop un soir médian : en dessous, le compte ne peut plus trader."""
        return float(np.median(self.stop_pts * MNQ_PT + self.cost))


def _size(tr: Trades, j: np.ndarray, risk: float, cap: np.ndarray, room: np.ndarray) -> np.ndarray:
    per = tr.stop_pts[j] * MNQ_PT + tr.cost[j]  # perte d'un contrat au stop
    n = np.floor(risk / (tr.stop_pts[j] * MNQ_PT))
    return np.clip(np.minimum(np.minimum(n, cap), np.floor(room / per)), 0, None)


def _floor(hi: np.ndarray) -> np.ndarray:
    return np.where(hi >= LOCK_AT, LOCK_FLOOR, hi - MLL)


def scaling(P: np.ndarray) -> np.ndarray:
    return np.where(P >= 2000, 40, np.where(P >= 1000, 30, 20))


def run_eval(tr: Trades, risk: float, n: int, rng: np.random.Generator, consistency: float = 0.4,
             max_days: int = 3000):
    """Renvoie (validé [bool n], séances [int n])."""
    P = np.zeros(n); hi = np.zeros(n); best = np.zeros(n)
    days = np.zeros(n, int); st = np.zeros(n, int)
    start = rng.integers(0, tr.n, n)
    for _ in range(max_days):
        a = np.flatnonzero(st == 0)
        if not len(a):
            break
        j = (start[a] + days[a]) % tr.n
        floor = _floor(hi[a])
        k = _size(tr, j, risk, np.full(len(a), EVAL_MAX), P[a] - floor)
        stuck = (P[a] - floor) < tr.min_room  # plus assez de marge pour 1 MNQ un soir ordinaire : abandon
        st[a[stuck]] = -1
        k[stuck] = 0
        pnl = k * (tr.stop_pts[j] * MNQ_PT * tr.R[j] - tr.cost[j])
        days[a] += 1
        P[a] += pnl
        fail = P[a] <= floor + 1e-9
        st[a[fail & ~stuck]] = -1
        best[a] = np.maximum(best[a], pnl)
        hi[a] = np.maximum(hi[a], P[a])
        ok = ~fail & ~stuck & (P[a] >= TARGET) & (best[a] <= consistency * P[a] + 1e-9)
        st[a[ok]] = 1
    return st == 1, days


def run_funded(tr: Trades, risk: float, n: int, rng: np.random.Generator, max_days: int = 500):
    """Renvoie (payouts reçus en $, nb de payouts, séances de vie, séance du 1er payout ou -1)."""
    P = np.zeros(n); hi = np.zeros(n); locked = np.zeros(n, bool)
    cyc_pnl = np.zeros(n); cyc_days = np.zeros(n, int)
    days = np.zeros(n, int); alive = np.ones(n, bool)
    paid = np.zeros(n); npay = np.zeros(n, int); first = np.full(n, -1)
    start = rng.integers(0, tr.n, n)
    for _ in range(max_days):
        a = np.flatnonzero(alive)
        if not len(a):
            break
        j = (start[a] + days[a]) % tr.n
        floor = np.where(locked[a], LOCK_FLOOR, _floor(hi[a]))
        room = P[a] - floor
        k = _size(tr, j, risk, scaling(P[a]), room)
        stuck = room < tr.min_room
        alive[a[stuck]] = False
        k[stuck] = 0
        pnl = k * (tr.stop_pts[j] * MNQ_PT * tr.R[j] - tr.cost[j])
        days[a] += 1
        P[a] += pnl
        fail = P[a] <= floor + 1e-9
        alive[a[fail]] = False
        hi[a] = np.maximum(hi[a], P[a])
        locked[a] |= hi[a] >= LOCK_AT
        cyc_pnl[a] += pnl
        cyc_days[a] += pnl >= DAY_MIN
        amt = np.minimum(PAY_FRAC * P[a], PAY_CAP)
        pay = ~fail & ~stuck & (cyc_days[a] >= DAYS_NEEDED) & (cyc_pnl[a] > 0) & (amt >= PAY_MIN)
        b, amt = a[pay], amt[pay]
        paid[b] += SPLIT * amt; npay[b] += 1
        first[b] = np.where(first[b] < 0, days[b], first[b])
        P[b] -= amt; locked[b] = True
        cyc_pnl[b] = 0.0; cyc_days[b] = 0
        alive[b[npay[b] >= MAX_PAYOUTS]] = False  # passage en réel, non valorisé
    return paid, npay, days, first
