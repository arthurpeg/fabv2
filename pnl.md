# Suivi P&L des books FTMO (démo), au 09/11/2026 02:38 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : +214.32 $ de trading** sur 4 trades (2 × 10 000 $ → 20,214.32 $) ; résultat FTMO virtuel -173.80 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-05 | -252.65 | +499.36 | +246.71 |
| 2026-11-06 | +215.96 | +0.00 | +215.96 |
| 2026-11-09 | -248.35 | +0.00 | -248.35 |

## Book A (mom)

- **P&L cumulé, tous essais : -285.04 $** (-2.85 %) sur 3 trades, du 04/11/2026 au 09/11/2026
- Compte continu : 9,714.96 $ ; plus gros creux -285.04 $ (-2.85 %)
- Trades gagnants 33 % ; R net moyen -0.39 ; sorties : SL 2, heure 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 3 | -285.04 | -0.39 | 1.95 | 1.95 (1.95) | +2.47 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 1515190763 | 3 | -285.04 | 04/11 → 09/11 |

- **Compte FTMO virtuel** : éval, cycle -2.85 % (meilleur jour +2.16 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)

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

- **Compte FTMO virtuel** : éval, cycle +4.99 % (meilleur jour +4.99 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
