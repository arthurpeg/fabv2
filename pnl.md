# Suivi P&L des books FTMO (démo), au 17/11/2026 10:51 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : -7.15 $ de trading** sur 4 trades (2 × 10 000 $ → 19,992.85 $) ; résultat FTMO virtuel -173.80 $.

### Dix dernières journées FTMO ($)

| Jour | A | B | total |
|---|---|---|---|
| 2026-11-16 | -249.55 | +0.00 | -249.55 |
| 2026-11-17 | -254.84 | +497.24 | +242.40 |

## Book A (mom)

- **P&L cumulé, tous essais : -504.39 $** (-5.04 %) sur 2 trades, du 15/11/2026 au 17/11/2026
- Compte continu : 9,495.61 $ ; plus gros creux -504.39 $ (-5.04 %)
- Trades gagnants 0 % ; R net moyen -1.02 ; sorties : SL 2

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| mom | 2 | -504.39 | -1.02 | 1.95 | 1.95 (1.95) | -0.05 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 511480419 | 2 | -504.39 | 15/11 → 17/11 |

- **Compte FTMO virtuel** : éval, cycle -5.04 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)

## Book B (3n + M2)

- **P&L cumulé, tous essais : +497.24 $** (+4.97 %) sur 2 trades, du 17/11/2026 au 17/11/2026
- Compte continu : 10,497.24 $ ; plus gros creux 0.00 $ (0.00 %)
- Trades gagnants 100 % ; R net moyen +1.15 ; sorties : heure 1, TP 1

| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) | Glissement entrée (pts) |
|---|---|---|---|---|---|---|
| 3n | 1 | +72.52 | +0.29 | 1.95 | 1.95 (1.95) | +0.00 |
| M2 | 1 | +424.72 | +2.01 | 1.45 | 1.45 (1.45) | -0.50 |

Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = exécuté plus cher que le prix affiché.

| Essai MT5 | Trades | P&L ($) | Période |
|---|---|---|---|
| 541521340 | 2 | +497.24 | 17/11 → 17/11 |

- **Compte FTMO virtuel** : éval, cycle +4.97 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
