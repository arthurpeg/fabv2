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

## Variante exploratoire S1 + stop dur 1R (2026-10-31, hors compteur)
Fichier `S1_R_stop.py` transmis (30 séances, bande 1,2 σ, filtre VWAP, stop dur à 1R, R ≥ plancher × prix), refait dans [run_s1_r_stop_vbt.py](../../run_s1_r_stop_vbt.py) ; résultats dans `results/s1_r_stop/run.log`. vectorbt et la boucle d'origine donnent les mêmes trades. Le stop et le plancher changent peu le P&L en dollars (Sharpe $ 1,03 → 1,12 avec 1 MNQ). Le meilleur chiffre en R vient surtout de la normalisation par le plancher, qui a été **choisi après avoir vu les résultats**. Cela ne rouvre pas la piste : condition du [[wiki/Failed Ideas/ledger|registre]] = holdout post-2026-08-28 seulement.

## Sources brutes
[[PREREGISTRATION]] · [[PREREGISTRATION_2]] · [[PREREGISTRATION_3]] · [[RESULTS]] · `results/m2_*`
