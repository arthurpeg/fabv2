# Pré-enregistrement n° 30 : règle de la 1ʳᵉ bougie NQ, stop 0,5 ATR / objectif 2R, sur la réserve

*2026-11-22. Confirmation (étape 3) de [PREREGISTRATION_30](../PREREGISTRATION_30.md), commité avant tout calcul (commit `bade69c`), **hors protocole** : la règle n'avait pas franchi B1 ; test demandé par l'utilisateur. Code : [run_prereg30.py](../run_prereg30.py), une seule exécution. Réserve NQ 2021-10-01 → 2026-08-28, désormais **consommée**. Compteur global : 2 025 (2 024 + 1 essai). Sorties : `results/prereg30/` (`trades.csv`, `run.log`).*

## Règle

NQ, sens de la bougie 9:30-9:35 ET (pas de trade si doji), entrée à 9:35, stop 0,5 × ATR14, objectif 2R, sinon sortie à 16:00. 1 contrat, coût 0,50 pt aller-retour.

## Résultat (1 216 trades, 2021-10-01 → 2026-08-28)

| | Exploration 2010-06 → 2021-09 | **Réserve 2021-10 → 2026-08** |
|---|---|---|
| Net par trade | +2,23 pts | **+2,57 pts (+51 $)** |
| Médiane | −2,75 | −30 |
| Écart-type | 51 | 156 |
| Sharpe annuel | 0,69 | **0,26** |
| t NW / p unilatéral | 2,17 / 0,015 | **0,58 / 0,28** |
| Gagnants | 47,4 % | 46,1 % |
| Résultat en R (stop ≈ 0,5 ATR) | +0,064 R | ≈ +0,018 R |
| Pire creux (1 contrat) | −41 207 $ | **−67 253 $** |
| R4, mêmes jours | +1,32 | +2,05 |
| « Toujours long », mêmes sorties | +0,56 | **+2,61** |

L'ATR14 moyen est passé de 76 à 283 pts : les montants en points ne se comparent pas directement d'une période à l'autre. En unités de risque, l'avantage est environ 3,5 fois plus faible sur la réserve.

Sorties : stop 41 %, objectif 11 %, 16:00 48 %. Achats +2,76 (n 609), ventes +2,38 (n 607).

Par année (pts/trade, règle / R4 / toujours long) : 2021 (oct.-déc.) −21,7 / −6,3 / +21,0 · 2022 +3,7 / +9,0 / +1,3 · 2023 −1,1 / +0,3 / +9,7 · 2024 +1,8 / +6,4 / +2,2 · 2025 +6,6 / +2,6 / −3,8 · 2026 (jusqu'en août) +10,7 / −10,1 / −2,8. Moitiés : −2,16 puis +7,30.

## Critères

- **C1** net > 0, p ≤ 0,05 : ❌ (p 0,28)
- C2 net > R4 sur les mêmes jours : ✅ (+0,53 pt, mais t de l'écart 0,15)
- C3 net > 0 sans la meilleure année : ✅ (+1,31)
- C4 net > 0 avec 1 tick de plus : ✅ (+2,32)

**Verdict : REJET**, comme prévu par le pré-enregistrement en cas d'échec (puissance annoncée ≈ 43 %).

## Lecture

1. Le net reste positif, mais il est indiscernable de zéro et de la simple dérive : « toujours long » avec les mêmes sorties fait **mieux** (+2,61), et l'écart avec R4 n'est qu'à t 0,15.
2. Le Sharpe tombe de 0,69 à 0,26 et le creux s'aggrave (−67 000 $ par contrat). Le gain total (+62 500 $) est fait en 2025-2026, après une première moitié négative.
3. Cohérent avec R4 sur la même période (Sharpe +0,17 avec le levier du papier) : l'entrée « sens de la 1ʳᵉ bougie » ne porte presque plus d'information sur NQ depuis 2022.

La réserve NQ « sortie » est consommée. Celle d'ES et YM (2021-10 → 2026-08) reste réservée. Ligne au registre des échecs.
