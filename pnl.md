# Suivi P&L des books FTMO (démo), au 18/11/2026 20:25 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : -1,002.86 $ de trading** sur 8 trades (2 × 10 000 $ → 18,997.14 $) ; résultat FTMO virtuel -260.70 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-16 | -249.55 | +0.00 | -249.55 |
| 2026-11-17 | -254.84 | +497.24 | +242.40 |
| 2026-11-18 | -255.33 | -249.01 | -504.34 |
| 2026-11-19 | -241.54 | -249.83 | -491.37 |

## Book A (mom)

- **P&L cumulé, tous essais : -1,001.26 $** (-10.01 %) sur 4 trades, du 15/11/2026 au 18/11/2026
- Compte continu : 8,998.74 $ ; plus gros creux -1,001.26 $ (-10.01 %)
- Trades gagnants 0 % ; R net moyen -1.03 ; sorties : SL 4

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 4 | -1,001.26 | -1.03 | 1.95 | 1.95 (1.95) | -2.40 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 511480419 | 4 | -1,001.26 | 15/11 → 18/11 |

- **Compte FTMO virtuel** : éval, cycle +0.00 % (meilleur jour +0.00 %), évals achetées 2, rewards 0 (0.00 $) → **résultat FTMO virtuel -173.80 $** (rewards − frais d'éval)
  - 2026-11-19 éval perdu (-10.01 %) → nouvelle éval virtuelle (79 €)

## Book B (3n + M2)

- **P&L cumulé, tous essais : -1.60 $** (-0.02 %) sur 4 trades, du 17/11/2026 au 18/11/2026
- Compte continu : 9,998.40 $ ; plus gros creux -498.84 $ (-4.75 %)
- Trades gagnants 50 % ; R net moyen +0.07 ; sorties : SL 2, heure 1, TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 3 | -426.32 | -0.58 | 1.95 | 1.95 (1.95) | +0.00 |
| M2 | 1 | +424.72 | +2.01 | 1.45 | 1.45 (1.45) | -0.50 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 541521340 | 4 | -1.60 | 17/11 → 18/11 |

- **Compte FTMO virtuel** : éval, cycle -0.02 % (meilleur jour +4.97 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
