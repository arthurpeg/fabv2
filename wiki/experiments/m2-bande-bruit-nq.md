---
type: experiment
updated: 2026-10-31
status: paper-trading
verdict: rejeté (DSR), surveillé
prereg: [1, 2, 3]
trials: 138
---

# Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ

**Une phrase** : Sharpe net +1,15 IS / +1,13 OOS sur ~2 300 trades, mais rejetée par le [[wiki/concepts/dsr|DSR]] (0,03) selon la règle fixée à l'avance.

## Tests
| Test | Résultat |
|---|---|
| DSR (N = 96) | 0,03 ❌ |
| [[wiki/concepts/reality-check|Reality Check]] (93 séries) | p = 0,018 ✅ |
| PBO | 0,05 |
| Sharpe 2024-09 → 2026-08 | 0,81, IC [−0,54 ; 1,78] |
| Réplication fidèle R3 (volatilité cible) | NQ +0,80 / +1,07 net, DSR ≈ 0 |

## Lecture
Le DSR échoue parce que les rendements sont très asymétriques (gains de crise, avril 2025) et que la dispersion des Sharpe entre essais est gonflée par les coûts. La barre n'est pas déplacée après coup : la piste est rejetée, gardée seulement en paper trading. Version ES abandonnée : voir [[wiki/Failed Ideas/ledger]].

## Sources brutes
[[PREREGISTRATION]] · [[PREREGISTRATION_2]] · [[PREREGISTRATION_3]] · [[RESULTS]] · `results/m2_*`
