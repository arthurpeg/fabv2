# Suivi P&L des books FTMO (démo), au 26/11/2026 10:48 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : -1,419.99 $ de trading** sur 16 trades (2 × 10 000 $ → 18,580.01 $) ; résultat FTMO virtuel -260.70 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-16 | -249.55 | +0.00 | -249.55 |
| 2026-11-17 | -254.84 | +497.24 | +242.40 |
| 2026-11-18 | -255.33 | -249.01 | -504.34 |
| 2026-11-19 | -241.54 | -249.83 | -491.37 |
| 2026-11-20 | -248.66 | +0.00 | -248.66 |
| 2026-11-23 | +495.97 | +30.89 | +526.86 |
| 2026-11-24 | -256.35 | +0.00 | -256.35 |
| 2026-11-25 | -271.37 | -248.18 | -519.55 |
| 2026-11-26 | +0.00 | -12.67 | -12.67 |
| 2026-11-27 | +93.24 | +0.00 | +93.24 |

## Book A (mom)

- **P&L cumulé, tous essais : -1,188.43 $** (-11.88 %) sur 9 trades, du 15/11/2026 au 26/11/2026
- Compte continu : 8,811.57 $ ; plus gros creux -1,281.67 $ (-12.82 %)
- Trades gagnants 22 % ; R net moyen -0.54 ; sorties : SL 7, TP 1, heure 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 9 | -1,188.43 | -0.54 | 1.95 | 1.89 (1.95) | -0.76 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 511480419 | 4 | -1,001.26 | 15/11 → 18/11 |
| 531542597 | 5 | -187.17 | 20/11 → 26/11 |

- **Compte FTMO virtuel** : éval, cycle -1.87 % (meilleur jour +4.96 %), évals achetées 2, rewards 0 (0.00 $) → **résultat FTMO virtuel -173.80 $** (rewards − frais d'éval)
  - 2026-11-19 éval perdu (-10.01 %) → nouvelle éval virtuelle (79 €)

## Book B (3n + M2)

- **P&L cumulé, tous essais : -231.56 $** (-2.32 %) sur 7 trades, du 17/11/2026 au 26/11/2026
- Compte continu : 9,768.44 $ ; plus gros creux -728.80 $ (-6.94 %)
- Trades gagnants 43 % ; R net moyen -0.09 ; sorties : heure 3, SL 3, TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 5 | -687.17 | -0.56 | 1.95 | 1.95 (1.95) | -0.56 |
| M2 | 2 | +455.61 | +1.07 | 1.45 | 1.45 (1.45) | -2.40 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 541521340 | 7 | -231.56 | 17/11 → 26/11 |

- **Compte FTMO virtuel** : éval, cycle -2.32 % (meilleur jour +4.97 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
