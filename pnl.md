# Suivi P&L des books FTMO (démo), au 05/11/2026 09:56 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : +246.71 $ de trading** sur 2 trades (2 × 10 000 $ → 20,246.71 $) ; résultat FTMO virtuel -173.80 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-05 | -252.65 | +499.36 | +246.71 |

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

- **P&L cumulé, tous essais : +499.36 $** (+4.99 %) sur 1 trades, du 05/11/2026 au 05/11/2026
- Compte continu : 10,499.36 $ ; plus gros creux 0.00 $ (0.00 %)
- Trades gagnants 100 % ; R net moyen +2.01 ; sorties : TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| M2 | 1 | +499.36 | +2.01 | 1.45 | 1.45 (1.45) | -1.00 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 1515191583 | 1 | +499.36 | 05/11 → 05/11 |

- **Compte FTMO virtuel** : éval, cycle +4.99 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
