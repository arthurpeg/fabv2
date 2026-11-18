# Suivi P&L des books FTMO (démo), au 17/11/2026 20:57 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : -511.49 $ de trading** sur 6 trades (2 × 10 000 $ → 19,488.51 $) ; résultat FTMO virtuel -173.80 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-16 | -249.55 | +0.00 | -249.55 |
| 2026-11-17 | -254.84 | +497.24 | +242.40 |
| 2026-11-18 | -255.33 | -249.01 | -504.34 |

## Book A (mom)

- **P&L cumulé, tous essais : -759.72 $** (-7.60 %) sur 3 trades, du 15/11/2026 au 17/11/2026
- Compte continu : 9,240.28 $ ; plus gros creux -759.72 $ (-7.60 %)
- Trades gagnants 0 % ; R net moyen -1.03 ; sorties : SL 3

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 3 | -759.72 | -1.03 | 1.95 | 1.95 (1.95) | -2.53 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 511480419 | 3 | -759.72 | 15/11 → 17/11 |

- **Compte FTMO virtuel** : éval, cycle -7.60 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)

## Book B (3n + M2)

- **P&L cumulé, tous essais : +248.23 $** (+2.48 %) sur 3 trades, du 17/11/2026 au 17/11/2026
- Compte continu : 10,248.23 $ ; plus gros creux -249.01 $ (-2.37 %)
- Trades gagnants 67 % ; R net moyen +0.43 ; sorties : heure 1, TP 1, SL 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 2 | -176.49 | -0.36 | 1.95 | 1.95 (1.95) | -0.25 |
| M2 | 1 | +424.72 | +2.01 | 1.45 | 1.45 (1.45) | -0.50 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 541521340 | 3 | +248.23 | 17/11 → 17/11 |

- **Compte FTMO virtuel** : éval, cycle +2.48 % (meilleur jour +4.97 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
