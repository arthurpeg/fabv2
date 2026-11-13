# Suivi P&L des books FTMO (démo), au 13/11/2026 10:10 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : +854.13 $ de trading** sur 13 trades (2 × 10 000 $ → 20,854.13 $) ; résultat FTMO virtuel -173.80 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-05 | -252.65 | +499.36 | +246.71 |
| 2026-11-06 | +215.96 | +0.00 | +215.96 |
| 2026-11-09 | -248.35 | +492.54 | +244.19 |
| 2026-11-10 | -249.62 | +17.05 | -232.57 |
| 2026-11-11 | +489.85 | +195.53 | +685.38 |
| 2026-11-12 | -251.42 | +18.80 | -232.62 |
| 2026-11-13 | -249.89 | +176.97 | -72.92 |

## Book A (mom)

- **P&L cumulé, tous essais : -546.12 $** (-5.46 %) sur 7 trades, du 04/11/2026 au 12/11/2026
- Compte continu : 9,453.88 $ ; plus gros creux -546.12 $ (-5.46 %)
- Trades gagnants 29 % ; R net moyen -0.32 ; sorties : SL 5, heure 1, TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 7 | -546.12 | -0.32 | 1.81 | 1.89 (1.95) | +1.44 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 1515190763 | 7 | -546.12 | 04/11 → 12/11 |

- **Compte FTMO virtuel** : éval, cycle -5.46 % (meilleur jour +4.90 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)

## Book B (3n + M2)

- **P&L cumulé, tous essais : +1,400.25 $** (+14.00 %) sur 6 trades, du 05/11/2026 au 13/11/2026
- Compte continu : 11,400.25 $ ; plus gros creux 0.00 $ (0.00 %)
- Trades gagnants 100 % ; R net moyen +1.34 ; sorties : TP 5, heure 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 3 | +231.38 | +0.75 | 1.95 | 1.85 (1.95) | -1.33 |
| M2 | 3 | +1,168.87 | +1.94 | 1.45 | 1.45 (1.45) | -0.03 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 1515191583 | 3 | +1,008.95 | 05/11 → 09/11 |
| 1515245887 | 3 | +391.30 | 10/11 → 13/11 |

- **Compte FTMO virtuel** : financé, cycle +3.91 % (meilleur jour +1.96 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
  - 2026-11-10 éval n° 1 validée → financé
