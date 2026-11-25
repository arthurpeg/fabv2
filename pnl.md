# Suivi P&L des books FTMO (démo), au 24/11/2026 21:55 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : -1,500.56 $ de trading** sur 14 trades (2 × 10 000 $ → 18,499.44 $) ; résultat FTMO virtuel -260.70 $.

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

## Book A (mom)

- **P&L cumulé, tous essais : -1,281.67 $** (-12.82 %) sur 8 trades, du 15/11/2026 au 24/11/2026
- Compte continu : 8,718.33 $ ; plus gros creux -1,281.67 $ (-12.82 %)
- Trades gagnants 12 % ; R net moyen -0.66 ; sorties : SL 7, TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 8 | -1,281.67 | -0.66 | 1.95 | 1.95 (1.95) | -0.98 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 511480419 | 4 | -1,001.26 | 15/11 → 18/11 |
| 531542597 | 4 | -280.41 | 20/11 → 24/11 |

- **Compte FTMO virtuel** : éval, cycle -2.80 % (meilleur jour +4.96 %), évals achetées 2, rewards 0 (0.00 $) → **résultat FTMO virtuel -173.80 $** (rewards − frais d'éval)
  - 2026-11-19 éval perdu (-10.01 %) → nouvelle éval virtuelle (79 €)

## Book B (3n + M2)

- **P&L cumulé, tous essais : -218.89 $** (-2.19 %) sur 6 trades, du 17/11/2026 au 24/11/2026
- Compte continu : 9,781.11 $ ; plus gros creux -716.13 $ (-6.82 %)
- Trades gagnants 50 % ; R net moyen -0.10 ; sorties : SL 3, heure 2, TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 4 | -674.50 | -0.68 | 1.95 | 1.95 (1.95) | -0.40 |
| M2 | 2 | +455.61 | +1.07 | 1.45 | 1.45 (1.45) | -2.40 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 541521340 | 6 | -218.89 | 17/11 → 24/11 |

- **Compte FTMO virtuel** : éval, cycle -2.19 % (meilleur jour +4.97 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
