"""Règles Smart Trader Funds « 1 Phase » (challenge en une étape), lues sur smartraderfunds.com le 2026-10-31.

Sources : configurateur de la page d'accueil, /challenges/ (comparatif), /help/ (Trading Rules, Payouts, Billing),
/terms-of-use/ (§ 14 et § 18), page de paiement (prix). Tout est en % du capital initial.

Éval (phase unique) : objectif +9 %, perte max 6 % fixe depuis le solde initial, perte du jour 4 % (solde de début
de journée, latent compris, remise à zéro à minuit GMT), au moins 5 jours avec un trade, aucun jour > 45 % du profit
total, aucune ouverture / modification / clôture de position 5 min avant ou après une annonce 3 étoiles (10 min une
fois financé), pas de trade les jours fériés, pas de position le week-end, levier 1:50. Durée illimitée.
Financé : mêmes limites (4 % / 6 % fixe, 45 %, 5 jours) ; premier retrait 30 jours après l'ouverture du financé,
ensuite tous les 14 jours, minimum 100 $ ; part du trader 80 %, 90 % après 3 retraits réussis ; frais d'éval
remboursés avec le 2e retrait (page d'aide ; /challenges/ dit « le premier », on prend le plus prudent).
Le retrait vide le profit : le solde revient au capital initial et le plancher reste à −6 % de ce capital.

Comme run_propfirm_vbt.replay : une seule position par nuit, P&L de la nuit en % du capital donné par `pnl_of`.
Une nuit sans trade (pnl NaN ou nuit interdite) ne compte pas comme jour de trading.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

DAILY, MAXLOSS, TARGET, CONSIST, MIN_DAYS = 4.0, 6.0, 9.0, 0.45, 5
FIRST_PAY, NEXT_PAY, MIN_PAY_USD, REFUND_AT = 30, 14, 100.0, 2
REVIEW = 1  # « instant funding on target » : le financé commence la nuit suivante
TOL = 1e-3
# Prix en dollars, plateforme TradeLocker (Platform 5 / MT5 : 153 / 252 / 428 / 659 / 1 297 / 1 813 $)
PRICES_USD = {10_000: 139, 25_000: 229, 50_000: 389, 100_000: 599, 200_000: 1179, 300_000: 1649}
MAX_BUYING_POWER = 800_000  # total de tous les comptes d'un même profil


def split(k: int) -> float:
    """Part du trader pour le retrait n° k (1, 2, ...)."""
    return 0.8 if k <= 3 else 0.9


def replay(pnl_of, dates: pd.DatetimeIndex, nt: int, start: int, size: int, r_eval: float, r_fund: float,
           viol_e: np.ndarray, viol_f: np.ndarray, once: bool = False):
    """Règles STF 1 Phase sur un emplacement depuis la nuit `start`, rachat le lendemain de chaque échec.
    pnl_of(i, phase, risk_pct) → P&L en % du capital, NaN si pas de trade. viol_e / viol_f[i] : la nuit i clôt
    sa position dans une fenêtre d'annonce interdite (éval / financé) → compte perdu.
    Renvoie des événements (type, nuit, ...) : achat, validée / ratée (+ cause), reward (% versé, frais remboursés ?),
    financé perdu (+ cause)."""
    ev = []
    i = start
    min_pay = MIN_PAY_USD / size * 100
    while i < nt:
        ev.append(("achat", i))
        P = best = 0.0
        n = 0
        passed, why = False, "fin des données"
        while i < nt:
            risk = min(r_eval, P + MAXLOSS)
            if risk < 0.05:
                why = "marge épuisée"
                break
            pnl = pnl_of(i, "éval", risk)
            i += 1
            if np.isnan(pnl):
                continue
            if viol_e[i - 1]:
                why = "annonce"
                break
            P += pnl; n += 1
            if P <= -MAXLOSS + TOL:
                why = "perte max"
                break
            if pnl <= -DAILY:
                why = "perte du jour"
                break
            best = max(best, pnl)
            if P >= TARGET - TOL and best <= CONSIST * P + TOL and n >= MIN_DAYS:
                passed = True
                break
        ev.append(("validée", max(i - 1, start)) if passed else ("ratée", max(i - 1, start), why))
        if not passed:
            if once:
                break
            continue
        i += REVIEW
        if i >= nt:
            break
        d0, last, k = dates[i], None, 0
        P = best = 0.0
        n = 0
        why = "fin des données"
        while i < nt:
            risk = min(r_fund, P + MAXLOSS)
            if risk < 0.05:
                why = "marge épuisée"
                break
            pnl = pnl_of(i, "financé", risk)
            i += 1
            if np.isnan(pnl):
                continue
            if viol_f[i - 1]:
                why = "annonce"
                break
            P += pnl; n += 1
            if P <= -MAXLOSS + TOL:
                why = "perte max"
                break
            if pnl <= -DAILY:
                why = "perte du jour"
                break
            best = max(best, pnl)
            d = dates[i - 1]
            due = (d - d0).days >= FIRST_PAY if last is None else (d - last).days >= NEXT_PAY
            if due and n >= MIN_DAYS and P >= min_pay and best <= CONSIST * P + TOL:
                k += 1
                ev.append(("reward", i - 1, split(k) * P, k == REFUND_AT))
                P = best = 0.0
                n = 0
                last = d
        ev.append(("financé perdu", min(i - 1, nt - 1), why))
        i += 1
        if once:
            break
    return ev
