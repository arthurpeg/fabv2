# Suivi P&L des books FTMO (démo), au 17/11/2026 03:00 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : -177.03 $ de trading** sur 2 trades (2 × 10 000 $ → 19,822.97 $) ; résultat FTMO virtuel -173.80 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-16 | -249.55 | +0.00 | -249.55 |
| 2026-11-17 | +0.00 | +72.52 | +72.52 |

## Book A (mom)

- **P&L cumulé, tous essais : -249.55 $** (-2.50 %) sur 1 trades, du 15/11/2026 au 15/11/2026
- Compte continu : 9,750.45 $ ; plus gros creux -249.55 $ (-2.50 %)
- Trades gagnants 0 % ; R net moyen -1.02 ; sorties : SL 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 1 | -249.55 | -1.02 | 1.95 | 1.95 (1.95) | -0.90 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 511480419 | 1 | -249.55 | 15/11 → 15/11 |

- **Compte FTMO virtuel** : éval, cycle -2.50 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)

## Book B (3n + M2)

- **P&L cumulé, tous essais : +72.52 $** (+0.73 %) sur 1 trades, du 17/11/2026 au 17/11/2026
- Compte continu : 10,072.52 $ ; plus gros creux 0.00 $ (0.00 %)
- Trades gagnants 100 % ; R net moyen +0.29 ; sorties : heure 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 1 | +72.52 | +0.29 | 1.95 | 1.95 (1.95) | +0.00 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 541521340 | 1 | +72.52 | 17/11 → 17/11 |

- **Compte FTMO virtuel** : éval, cycle +0.73 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
