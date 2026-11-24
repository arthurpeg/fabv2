# Suivi P&L des books FTMO (démo), au 24/11/2026 03:55 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : -981.01 $ de trading** sur 12 trades (2 × 10 000 $ → 19,018.99 $) ; résultat FTMO virtuel -260.70 $.

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

## Book A (mom)

- **P&L cumulé, tous essais : -1,010.30 $** (-10.10 %) sur 7 trades, du 15/11/2026 au 24/11/2026
- Compte continu : 8,989.70 $ ; plus gros creux -1,249.92 $ (-12.50 %)
- Trades gagnants 14 % ; R net moyen -0.59 ; sorties : SL 6, TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 7 | -1,010.30 | -0.59 | 1.95 | 1.95 (1.95) | -1.11 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 511480419 | 4 | -1,001.26 | 15/11 → 18/11 |
| 531542597 | 3 | -9.04 | 20/11 → 24/11 |

- **Compte FTMO virtuel** : éval, cycle -0.09 % (meilleur jour +4.96 %), évals achetées 2, rewards 0 (0.00 $) → **résultat FTMO virtuel -173.80 $** (rewards − frais d'éval)
  - 2026-11-19 éval perdu (-10.01 %) → nouvelle éval virtuelle (79 €)

## Book B (3n + M2)

- **P&L cumulé, tous essais : +29.29 $** (+0.29 %) sur 5 trades, du 17/11/2026 au 23/11/2026
- Compte continu : 10,029.29 $ ; plus gros creux -498.84 $ (-4.75 %)
- Trades gagnants 60 % ; R net moyen +0.08 ; sorties : heure 2, SL 2, TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 3 | -426.32 | -0.58 | 1.95 | 1.95 (1.95) | +0.00 |
| M2 | 2 | +455.61 | +1.07 | 1.45 | 1.45 (1.45) | -2.40 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 541521340 | 5 | +29.29 | 17/11 → 23/11 |

- **Compte FTMO virtuel** : éval, cycle +0.29 % (meilleur jour +4.97 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
