"""Moteur FTMO 1-Step : éval et compte financé, un trade au hasard par jour (PREREGISTRATION_18).

Tout est en % du capital initial. Les comptes avancent en parallèle (tableaux numpy) ;
chaque compte part d'un jour tiré au hasard dans la bibliothèque et avance jour après jour.

Issue d'un trade, en R brut (1 R = distance du stop) :
- mode « NQ réel » (lib = DayLib) : objectif touché avant le stop (strictement) → +k ;
  stop touché → −stop_R (>= 1, glissement) ; sinon R de clôture en fin de journée ;
- mode binaire (lib = None) : +k avec probabilité 1 / (1 + k), sinon −1.
Le risque r est net : la taille est choisie pour qu'un stop sans glissement coûte r, coût
compris (comme dans la session précédente). P&L net = r × (R − c) / (1 + c), c = coût en R.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from propfirm.days import K_N, K_STEP, DayLib

DAILY, MAXLOSS, TARGET = 3.0, 10.0, 10.0
SPLIT = 0.9
EUR = 1.10
PRICES_EUR = {10_000: 79, 25_000: 199, 50_000: 319, 100_000: 499, 200_000: 999}
COST_FRAC = 1e-4  # 1 pb du prix par aller-retour
MIN_RISK = 0.05


@dataclass
class Market:
    lib: DayLib | None  # None = binaire
    s: float            # stop en fraction du prix (binaire ; en NQ réel : lib.s, propre à chaque jour)
    cost_frac: float = COST_FRAC  # coût aller-retour en fraction du prix

    def cost_R(self, day: np.ndarray) -> np.ndarray:
        s = self.s if self.lib is None else self.lib.s[day]
        return self.cost_frac / s * np.ones(len(day))

    @property
    def n_days(self) -> int:
        return self.lib.n if self.lib is not None else 1


def _k_index(k_gross: np.ndarray) -> np.ndarray:
    return np.clip(np.ceil(k_gross / K_STEP - 1e-9).astype(int) - 1, 0, K_N - 1)


def _outcome(m: Market, day: np.ndarray, kidx: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    k = K_STEP * (kidx + 1)
    if m.lib is None:
        return np.where(rng.random(len(k)) < 1 / (1 + k), k, -1.0)
    side = rng.integers(0, 2, len(k))
    lib = m.lib
    tpb = lib.tp_bar[day, side, kidx]
    sb = lib.stop_bar[day, side]
    win = tpb < sb
    lost = ~win & (sb != np.iinfo(np.int16).max)
    return np.where(win, k, np.where(lost, -lib.stop_R[day, side], lib.eod_R[day, side]))


def run_eval(m: Market, r: float, t: float, n: int, rng: np.random.Generator, max_days: int = 3000):
    """Renvoie (validé [bool n], jours [int n])."""
    P = np.zeros(n); hi = np.zeros(n); best = np.zeros(n)
    days = np.zeros(n, int); st = np.zeros(n, int)  # 0 en cours, 1 validé, -1 raté
    start = rng.integers(0, m.n_days, n)
    for _ in range(max_days):
        a = np.flatnonzero(st == 0)
        if not len(a):
            break
        floor = hi[a] - MAXLOSS
        risk = np.minimum(r, P[a] - floor)
        dead = risk < MIN_RISK
        st[a[dead]] = -1
        a, floor, risk = a[~dead], floor[~dead], risk[~dead]
        need = np.maximum(np.maximum(TARGET - P[a], 2 * best[a] - P[a]), 0.01)
        day = (start[a] + days[a]) % m.n_days
        c = m.cost_R(day)
        kidx = _k_index(np.minimum(t, need) / risk * (1 + c) + c)
        R = _outcome(m, day, kidx, rng)
        pnl = risk * (R - c) / (1 + c)
        days[a] += 1
        P[a] += pnl
        fail = (P[a] <= floor + 1e-9) | (pnl <= -DAILY)
        st[a[fail]] = -1
        best[a] = np.maximum(best[a], pnl)
        hi[a] = np.maximum(hi[a], P[a])
        ok = ~fail & (P[a] >= TARGET - 1e-9) & (best[a] <= 0.5 * P[a] + 1e-9)
        st[a[ok]] = 1
    return st == 1, days


def run_funded(m: Market, r: float, t: float, n: int, rng: np.random.Generator,
               cycle: int = 10, reset: bool = True, max_days: int = 500):
    """Renvoie (rewards reçus en % du capital, nb de rewards, jours de vie, jour du 1er reward ou -1)."""
    P = np.zeros(n); hi = np.zeros(n); best = np.zeros(n)
    cyc = np.zeros(n, int); days = np.zeros(n, int); alive = np.ones(n, bool)
    paid = np.zeros(n); nrew = np.zeros(n, int); first = np.full(n, -1)
    start = rng.integers(0, m.n_days, n)
    for _ in range(max_days):
        a = np.flatnonzero(alive)
        if not len(a):
            break
        floor = hi[a] - MAXLOSS
        risk = np.minimum(r, P[a] - floor)
        dead = risk < MIN_RISK
        alive[a[dead]] = False
        a, floor, risk = a[~dead], floor[~dead], risk[~dead]
        day = (start[a] + days[a]) % m.n_days
        c = m.cost_R(day)
        kidx = _k_index(t / risk * (1 + c) + c)
        R = _outcome(m, day, kidx, rng)
        pnl = risk * (R - c) / (1 + c)
        days[a] += 1; cyc[a] += 1
        P[a] += pnl
        fail = (P[a] <= floor + 1e-9) | (pnl <= -DAILY)
        alive[a[fail]] = False
        best[a] = np.maximum(best[a], pnl)
        hi[a] = np.maximum(hi[a], P[a])
        pay = ~fail & (cyc[a] >= cycle) & (P[a] > 0) & (best[a] <= 0.5 * P[a] + 1e-9)
        b = a[pay]
        paid[b] += SPLIT * P[b]; nrew[b] += 1
        first[b] = np.where(first[b] < 0, days[b], first[b])
        if reset:
            hi[b] = 0.0  # sinon le plancher reste au même niveau en $ alors que le solde revient au capital initial
        P[b] = 0.0; best[b] = 0.0; cyc[b] = 0
    return paid, nrew, days, first


def ev(p_pass: float, se_p: float, v_pct: float, se_v: float, size: int) -> tuple[float, float]:
    """EV par tentative en $ et demi-largeur d'IC 95 % (méthode delta)."""
    fee = PRICES_EUR[size] * EUR
    e = p_pass * v_pct / 100 * size - fee
    se = size / 100 * np.sqrt((v_pct * se_p) ** 2 + (p_pass * se_v) ** 2)
    return e, 1.96 * se


def refusal_breakeven(p_pass: float, v_pct: float, size: int) -> float:
    """Part de rewards refusés qui annule l'EV."""
    fee = PRICES_EUR[size] * EUR
    return 1 - fee / (p_pass * v_pct / 100 * size)
