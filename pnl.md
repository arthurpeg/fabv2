# Suivi P&L des books FTMO (démo), au 14/11/2026 13:38 ET

Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.

**Total A + B : +1,400.25 $ de trading** sur 6 trades (2 × 10 000 $ → 21,400.25 $) ; résultat FTMO virtuel -86.90 $.

### Dix dernières journées FTMO ($)

| Jour | B | total |
|---|---|---|
| 2026-11-05 | +499.36 | +499.36 |
| 2026-11-09 | +492.54 | +492.54 |
| 2026-11-10 | +17.05 | +17.05 |
| 2026-11-11 | +195.53 | +195.53 |
| 2026-11-12 | +18.80 | +18.80 |
| 2026-11-13 | +176.97 | +176.97 |

## Book A (mom)

Aucun trade fermé pour l'instant.

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
