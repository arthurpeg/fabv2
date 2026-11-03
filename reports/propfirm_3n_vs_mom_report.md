# FTMO 1-Step : stratégie 3n contre notre règle de nuit (mom)

Date : 2026-11-03. **Exploratoire, hors compteur.** On rejoue des trades existants dans le moteur du n° 18 ([propfirm/ftmo.py](../propfirm/ftmo.py)), avec les mêmes réglages que l'avenant C ([[reports/prereg18_report]]). Script : [run_propfirm_3n_vs_mom.py](../run_propfirm_3n_vs_mom.py). Sorties : `results/propfirm_3n_vs_mom/` (`run.log`, `eval.csv`, `funded.csv`, `ev.csv`). 20 000 comptes par réglage, graine 1818.

## Réglages

Ce sont les réglages de l'avenant C :
- éval à 10 %, 2 % de risque par trade ; compte financé à 1 % de risque par trade ;
- limite de perte de 3 % par jour et de 10 % au total ;
- règle des 50 % sur le meilleur jour ;
- reward tous les 10 trades, partagé à 90 % ;
- spread CFD de 1,5 point au niveau actuel du NQ (3 points en contrôle) ;
- RAZ de la perte max après chaque reward (hypothèse principale de l'avenant C) ;
- un trade = un jour FTMO ; chaque compte part d'un trade tiré au hasard et enchaîne les suivants dans l'ordre historique.

Les deux bibliothèques de trades :
- **mom** : `results/couts_reels_nq_nuit/trades.csv`, 20:00 → 9:30, SL 2 / TP 5 ATR, environ 250 trades par an.
- **3n** : trades vectorbt de [[reports/nq_nuit_3n_vbt_report]], 20:05 → 03:00, stop 2 ATR M15, sans TP, environ 109 trades par an. Les nuits à plat ne comptent pas comme des jours.

Pour comparer à durée égale, on calcule une **EV par mois d'emplacement** : EV par tentative / (durée moyenne d'une éval + P(passage) × vie moyenne du compte financé), avec chaque durée convertie en mois selon la fréquence de trades de la règle.

## Résultats (éval 2 %, financé 1 %, 1,5 pt, RAZ)

| Bibliothèque | R brut moyen | Passage | Durée de l'éval si validée | Valeur du financé | P(≥ 1 reward) | Vie du financé | **EV / tentative 10k** | **EV / tentative 100k** | **EV par mois d'emplacement, 100k** |
|---|---|---|---|---|---|---|---|---|---|
| mom 2011-2026 (avenant C) | +0,125 | 50,8 % | 13 nuits ≈ 0,6 mois | 18,5 % | 80 % | 120 nuits ≈ 6 mois | +853 $ | +8 849 $ | **+2 481 $** |
| mom 2016-2026 | +0,099 | 47,5 % | 0,6 mois | 11,7 % | 76 % | 4 mois | +468 $ | +5 000 $ | +1 814 $ |
| mom 2016-2026, sans edge | 0 | 33,0 % | 0,6 mois | 5,0 % | 57 % | 3 mois | +79 $ | +1 110 $ | +675 $ |
| **3n 03h SL 2016-2026** | +0,160 | **62,7 %** | 22 trades ≈ 2,4 mois | **41,2 %** | 87 % | 275 trades ≈ 30 mois | **+2 499 $** | **+25 307 $** | +1 164 $ |
| 3n 03h SL, sans edge | 0 | 30,6 % | 2,8 mois | 5,6 % | 60 % | 12 mois | +85 $ | +1 174 $ | +182 $ |
| 3n 03h SL, spread 3 pt | | 58,6 % | 2,6 mois | 35,2 % | | 30 mois | +1 976 $ | +20 080 $ | +978 $ |
| 3n 08h SL 2016-2026 | +0,191 | 56,4 % | 1,8 mois | 42,0 % | 84 % | 23 mois | +2 279 $ | +23 113 $ | +1 530 $ |
| 3n 03h SL 2025-2026 seul (OOS) ⚠️ | +0,154 | 83,4 % | 3,1 mois | 59,3 % | 100 % | ≥ 55 mois (plafond) | +4 859 $ | +48 907 $ | +1 009 $ |

Sans RAZ, les EV sur 10k sont : mom 2016-2026 +235 $, 3n +710 $, 3n 08h +450 $. Le détail de toutes les grilles de risque est dans `run.log`. En prenant le meilleur réglage de la grille, 3n atteint +4 358 $ par tentative sur 10k (éval 0,5 %, 100 % de passage), mais l'éval dure alors **17 mois**.

## Lecture

1. **Par tentative, 3n vaut 3 à 5 fois mom.** Il fait +2 499 $ contre +468 $ sur la même période 2016-2026, et contre +853 $ pour mom sur 2011-2026. Ses trades sont meilleurs (R brut +0,16 contre +0,10) et sa série est plus régulière en R (Sharpe 1,42 contre 0,90, voir [[reports/nq_nuit_3n_vs_mom_report]]). Le compte financé vit donc bien plus longtemps : 30 mois en moyenne, 9 rewards. L'avantage reste au spread de 3 points (+1 976 $). Sans edge, 3n vaut à peine mieux que mom sans edge (+85 $ contre +79 $). **L'écart vient bien du signal, pas de la structure des trades.**
2. **Par mois d'emplacement, c'est l'inverse.** 3n ne trade que 109 nuits par an, si bien que l'éval prend 2,4 mois au lieu de 0,6 et que l'argent arrive lentement. Sur un même compte occupé en continu (100k), mom rapporte +1 814 $ par mois (2016-2026) ou +2 481 $ (2011-2026), contre **+1 164 $** pour 3n. Une fois retirée la valeur de l'option sans edge, l'apport du signal est du même ordre : +1 139 $ par mois pour mom, +982 $ pour 3n.
3. **Les deux se cumulent plutôt qu'ils ne s'excluent.** Ce sont deux comptes, et 3n laisse 58 % des nuits libres. Si le nombre de comptes est limité, mom remplit mieux un emplacement. Si c'est le nombre d'évals qui est limité (frais, refus de rewards), 3n rentabilise mieux chaque éval. Avant de faire tourner les deux en même temps, il faut tenir compte de leur corrélation par nuit (+0,35) : les mauvaises périodes peuvent tomber ensemble (2023 pour 3n, 2022 pour mom).
4. **La règle FTMO des annonces avantage 3n.** En compte financé, FTMO interdit toute exécution, stop et objectif compris, dans les 2 minutes autour du NFP, du CPI, etc. ([[wiki/experiments/propfirm-ftmo-option]]). 3n est à plat dès 03:00, donc **il n'est jamais concerné**. mom, elle, garde la position jusqu'à 9:30 ; ses chiffres FTMO, ici comme à l'avenant C, ignorent cette règle et sont environ 10 % trop optimistes.
5. **3n 08h**, avec la sortie à 08:00, fait un peu moins par tentative que 03h (+2 279 $), mais plus par mois (+1 530 $). Ses trades rapportent plus de R, et ses comptes perdus libèrent l'emplacement plus vite.

## Limites

- **3n est entièrement dans son échantillon de sélection.** Son filtre a été choisi sur 2016-2024, alors que mom a été validée sur 2011-2015. La ligne OOS 2025-2026 ⚠️ n'est **pas fiable** : le moteur rejoue en boucle 182 trades d'une période favorable (100 % de comptes avec reward, vie bloquée au plafond).
- **Le moteur arrête un compte financé à 500 trades.** C'est environ 4,6 ans pour 3n contre 2 ans pour mom, et ce plafond tronque une partie des comptes 3n. La valeur de 3n est donc un peu sous-estimée.
- **Hypothèses reprises de l'avenant C :** RAZ de la perte max après chaque reward, et rewards versés sans refus. Le spread réel de nuit du CFD n'est pas vérifié.
- **Trading de nuit :** 3n entre à 20:05 et sort à 03:00 ET. Il faut s'assurer que le compte FTMO autorise la position à ces heures et que les frais de swap éventuels ne sont pas comptés ici.
