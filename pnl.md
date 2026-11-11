# Suivi P&L des books FTMO (démo), au 10/11/2026 23:27 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : +669.82 $ de trading** sur 8 trades (2 × 10 000 $ → 20,669.82 $) ; résultat FTMO virtuel -173.80 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-05 | -252.65 | +499.36 | +246.71 |
| 2026-11-06 | +215.96 | +0.00 | +215.96 |
| 2026-11-09 | -248.35 | +492.54 | +244.19 |
| 2026-11-10 | -249.62 | +17.05 | -232.57 |
| 2026-11-11 | +0.00 | +195.53 | +195.53 |

## Book A (mom)

- **P&L cumulé, tous essais : -534.66 $** (-5.35 %) sur 4 trades, du 04/11/2026 au 09/11/2026
- Compte continu : 9,465.34 $ ; plus gros creux -534.66 $ (-5.35 %)
- Trades gagnants 25 % ; R net moyen -0.55 ; sorties : SL 3, heure 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 4 | -534.66 | -0.55 | 1.90 | 1.95 (1.95) | +2.07 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 1515190763 | 4 | -534.66 | 04/11 → 09/11 |

- **Compte FTMO virtuel** : éval, cycle -5.35 % (meilleur jour +2.16 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)

## Book B (3n + M2)

- **P&L cumulé, tous essais : +1,204.48 $** (+12.04 %) sur 4 trades, du 05/11/2026 au 10/11/2026
- Compte continu : 11,204.48 $ ; plus gros creux 0.00 $ (0.00 %)
- Trades gagnants 100 % ; R net moyen +1.52 ; sorties : TP 4

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 2 | +212.58 | +1.03 | 1.95 | 1.80 (1.95) | -1.20 |
| M2 | 2 | +991.90 | +2.00 | 1.45 | 1.45 (1.45) | +0.40 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 1515191583 | 3 | +1,008.95 | 05/11 → 09/11 |
| 1515245887 | 1 | +195.53 | 10/11 → 10/11 |

- **Compte FTMO virtuel** : financé, cycle +1.96 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
  - 2026-11-10 éval n° 1 validée → financé
