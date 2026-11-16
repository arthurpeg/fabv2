# Suivi P&L des books FTMO (démo), au 15/11/2026 20:11 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : -249.55 $ de trading** sur 1 trades (2 × 10 000 $ → 19,750.45 $) ; résultat FTMO virtuel -173.80 $.

### Dix dernières journées FTMO ($)

| Jour | A | total |
|---|---|---|
| 2026-11-16 | -249.55 | -249.55 |

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

Aucun trade fermé pour l'instant.

- **Compte FTMO virtuel** : éval, cycle +0.00 % (meilleur jour +0.00 %), évals achetées 1, rewards 0 (0.00 $) → **résultat FTMO virtuel -86.90 $** (rewards − frais d'éval)
