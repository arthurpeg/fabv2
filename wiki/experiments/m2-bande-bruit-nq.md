---
type: experiment
updated: 2026-11-22
status: paper-trading
verdict: rejeté (DSR), surveillé
prereg: [1, 2, 3, 19]
trials: 2091
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

**N° 19 (hors échantillon 2010–2015, pré-enregistré)** : échec. +0,030 R/trade, p = 0,15 ; Sharpe $ 0,57 contre 0,55 sans stop. Voir [[reports/prereg19_report]].

## Sources brutes
[[PREREGISTRATION]] · [[PREREGISTRATION_2]] · [[PREREGISTRATION_3]] · [[PREREGISTRATION_19]] · [[reports/prereg19_report]] · [[RESULTS]] · `results/m2_*`

## Lectures du 2026-11-22 (textes intégraux, aucun calcul)

Papiers lus : *Beat the Market* version du 22/09/2025 avec FAQ (SSRN 4824172), Chuk (7609644), Paz (7290621), Delgado (7323419), Maróy (5095349). Fiches : [[papiers_ssrn_orb_2026-11-22]] ([5], [6]) et [[recherche_causalite_intraday]].
- **Écart de fidélité de notre M2** : `fab/strategies.py::m2_noise` utilise bien le VWAP au prix typique, mais **n'exige pas le VWAP à l'entrée** (entrée si clôture > bande seulement). Le code publié par les auteurs l'exige (Delgado : principale cause d'écart entre le texte et le code ; Chuk et Paz l'appliquent aussi). Nos chiffres M2 portent donc sur une version qui prend plus de signaux que l'originale. À corriger avant tout nouveau test ; aucune validation historique possible sur NQ (données explorées ou consommées), seulement le forward.
- **La période ancienne est faible partout** : SPY 2000-2007 Sharpe 0,53 (Delgado), NQ 2014-2019 « plat » (Chuk), notre NQ 2010-2015 ≈ 0,55. L'effet est concentré sur 2018-2024.
- **Après la publication** : bon jusqu'en août 2025 (Sharpe 1,06-1,28), puis SPY −8,1 % de septembre 2025 à août 2026 (Delgado) ; Paz : 0,39 sur mai 2024 → mars 2026, sans écart significatif des moyennes. Chuk sur NQ : 2025 faible (+3,38 $/jour) mais 2026 bon.
- **Autres actifs (FAQ Q13, 33 futures, 2007-2024)** : Sharpe moyen 0,60 ; Nasdaq 1,23, S&P 500 1,32, MidCap 0,80, Russell 0,45 ; 21 matières premières anonymisées, de −0,30 à 1,11 (la plupart 0,2-0,6). QQQ 0,99, IWM 0,45 (Delgado).
- **Variantes jugées utiles par les auteurs ou les répliques** : lookback 90 j (Sharpe 1,50 contre 1,35, FAQ Q6) ; multiplicateur 1,3-1,5 ; jambe courte plus faible (0,56 contre 0,90) ; taille continue selon le volume relatif cumulé (Delgado, seule modification qui améliore les quatre fenêtres). Maróy (Sharpe > 3) = optimisation de 7-11 paramètres sans hors échantillon : à ignorer.


## Vérification de fidélité : VWAP à l'entrée (2026-11-22)

Demande de l'utilisateur : voir si exiger le VWAP à l'entrée (code des auteurs) améliore M2, **sans rien publier vers le bot du VPS**. Script séparé [run_m2_vwap.py](../../run_m2_vwap.py) (copie de `m2_noise`, rien de modifié dans `fab/strategies.py`), grille commitée avant calcul : NQ, ES, YM × {1×, volatilité cible}, 6 essais, compteur 2 085 → 2 091. Ce n'est pas une réouverture : données 2016-2026 déjà explorées, aucun verdict B1.

**Résultat** ([[reports/m2_vwap_report]]) : exiger le VWAP à l'entrée améliore un peu M2, surtout sur NQ à taille fixe : Sharpe net 1,16 → **1,23** sur 2016-2026 (IS 1,26, OOS 1,19), +0,7 pt par trade, 4 % de trades en moins, écart journalier +0,24 bp (t 2,27) ; ES 0,60 → 0,65 ; YM et volatilité cible dans le bruit. NQ corrigé = exactement le Sharpe des auteurs pour le future Nasdaq (1,23, FAQ Q13). Vérification de fidélité, pas une validation ; rien changé dans `fab/strategies.py` ni dans le bot. Compteur 2 085 → 2 091.

