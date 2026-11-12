# Suivi P&L des books FTMO (démo), au 12/11/2026 08:09 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : +927.05 $ de trading** sur 11 trades (2 × 10 000 $ → 20,927.05 $) ; résultat FTMO virtuel -173.80 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-05 | -252.65 | +499.36 | +246.71 |
| 2026-11-06 | +215.96 | +0.00 | +215.96 |
| 2026-11-09 | -248.35 | +492.54 | +244.19 |
| 2026-11-10 | -249.62 | +17.05 | -232.57 |
| 2026-11-11 | +489.85 | +195.53 | +685.38 |
| 2026-11-12 | -251.42 | +18.80 | -232.62 |

## Book A (mom)

- **P&L cumulé, tous essais : -296.23 $** (-2.96 %) sur 6 trades, du 04/11/2026 au 12/11/2026
- Compte continu : 9,703.77 $ ; plus gros creux -534.66 $ (-5.35 %)
- Trades gagnants 33 % ; R net moyen -0.20 ; sorties : SL 4, heure 1, TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 6 | -296.23 | -0.20 | 1.85 | 1.88 (1.95) | +1.53 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 1515190763 | 6 | -296.23 | 04/11 → 12/11 |

- **Compte FTMO virtuel** : éval, cycle -2.96 % (meilleur jour +4.90 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)

## Book B (3n + M2)

- **P&L cumulé, tous essais : +1,223.28 $** (+12.23 %) sur 5 trades, du 05/11/2026 au 12/11/2026
- Compte continu : 11,223.28 $ ; plus gros creux 0.00 $ (0.00 %)
- Trades gagnants 100 % ; R net moyen +1.25 ; sorties : TP 4, heure 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 3 | +231.38 | +0.75 | 1.95 | 1.85 (1.95) | -1.33 |
| M2 | 2 | +991.90 | +2.00 | 1.45 | 1.45 (1.45) | +0.40 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 1515191583 | 3 | +1,008.95 | 05/11 → 09/11 |
| 1515245887 | 2 | +214.33 | 10/11 → 12/11 |

- **Compte FTMO virtuel** : financé, cycle +2.14 % (meilleur jour +1.96 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
  - 2026-11-10 éval n° 1 validée → financé
