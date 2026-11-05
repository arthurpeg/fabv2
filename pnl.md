# Suivi P&L des books FTMO (démo), au 04/11/2026 20:16 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : -252.65 $ de trading** sur 1 trades (2 × 10 000 $ → 19,747.35 $) ; résultat FTMO virtuel -173.80 $.

### Dix derniers jours ($)

| Jour | A | total |
|---|---|---|
| 2026-11-04 | -252.65 | -252.65 |

## Book A (mom)

- **P&L cumulé, tous essais : -252.65 $** (-2.53 %) sur 1 trades, du 04/11/2026 au 04/11/2026
- Compte continu : 9,747.35 $ ; plus gros creux -252.65 $ (-2.53 %)
- Trades gagnants 0 % ; R net moyen -1.03 ; sorties : SL 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 1 | -252.65 | -1.03 | 1.95 | 1.95 (1.95) | +0.10 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 1515190763 | 1 | -252.65 | 04/11 → 04/11 |

- **Compte FTMO virtuel** : éval, cycle -2.53 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)

## Book B (3n + M2)

Aucun trade fermé pour l'instant.

- **Compte FTMO virtuel** : éval, cycle +0.00 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
