# Filtre ML binaire (taille fixe 1 R) sur mom, jugé sur le passage d'un challenge prop firm

*2026-11-19, branche `ml`, étape 1 (exploration). Script et grille figée avant calcul (commit 2c9dcd6) : [ml_propfirm_filter.py](../experiments/ml_propfirm_filter/ml_propfirm_filter.py). Sorties : `experiments/ml_propfirm_filter/results/` (run.log, qualite.csv, monte_carlo.csv, aleatoires_p95.csv, monte_carlo_blocs20.csv, stabilite.csv, importances.csv, verdict.csv, oof.csv). 9 filtres comptés : **compteur 1 798 → 1 807**.*

## Verdict

**❌ Ne pas utiliser le ML.** Aucun des 6 filtres ML ne remplit un seul des critères de significativité figés : E[R] non significatif contre le hasard (p brut ≥ 0,18, Holm 1,0), P(réussite) jamais au-dessus du 95e centile des filtres aléatoires, toujours moins bon que la règle Abdi seule au même taux. Les AUC hors bloc valent 0,498 (logit), 0,507 (LightGBM) et 0,512 (Abdi seule) : aucun pouvoir de classement. La règle Abdi seule n'est pas significative non plus (meilleur p 0,057 à 70 %), et tous les filtres perdent de l'E[R] sur 2023 → 2026-08. **Le holdout n'a pas été lu.**

## Données et cadre

Règle mom : compte 20:00 ET, momentum 12-1, SL 2 ATR M15, TP 4 ATR (2 R), sortie 9:30 ET. 3 787 nuits du 2011-07-01 au 2026-08-28, données déjà explorées ([[wiki/reserves]]) ; rien de la fenêtre de l'avenant A ni du holdout n° 26. R net d'un coût CFD de 1,5 point. Baseline : E[R] +0,099, win 44,2 %.

Variables (corrélations deux à deux toutes ≤ 0,03 en valeur absolue) : `mom` (valeur continue du 12-1), `abdi` (sens × nuit d−1 / ATR), `blw` (sens × (clôture 16:15 − VWAP 15:15-16:15) / ATR, définition du n° 16), `annonce` (NFP ou CPI à 8:30 le matin). Purged K-Fold, 5 blocs chronologiques, embargo de 5 nuits.

## Qualité du signal (hors bloc)

| Filtre | Trades | Win % | E[R] | Série de pertes max | R/an | Max DD (R) | p vs hasard |
|---|---|---|---|---|---|---|---|
| Baseline 100 % | 3 787 | 44,2 | +0,099 | 15 | 24,7 | −26,6 | — |
| Logit 70 % | 2 651 | 44,6 | +0,112 | 11 | 19,5 | −24,9 | 0,18 |
| Logit 50 % | 1 894 | 43,7 | +0,085 | 11 | 10,6 | −28,1 | 0,75 |
| Logit 35 % | 1 326 | 43,8 | +0,092 | 11 | 8,0 | −24,0 | 0,60 |
| LightGBM 70 % | 2 654 | 44,4 | +0,098 | 12 | 17,2 | −36,4 | 0,50 |
| LightGBM 50 % | 1 901 | 45,2 | +0,109 | 10 | 13,7 | −31,9 | 0,31 |
| LightGBM 35 % | 1 351 | 45,1 | +0,110 | 12 | 9,8 | −22,8 | 0,34 |
| Abdi seule 70 % | 2 651 | 45,2 | +0,119 | 13 | 20,9 | −19,6 | 0,057 |
| Abdi seule 50 % | 1 894 | 45,1 | +0,115 | 11 | 14,3 | −18,6 | 0,23 |
| Abdi seule 35 % | 1 326 | 45,4 | +0,137 | 10 | 12,0 | −22,5 | 0,09 |

Contre Abdi au même taux, chaque filtre ML a un E[R] plus faible (−0,006 à −0,045 R). Les séries de pertes plus courtes des filtres viennent surtout du nombre de trades plus faible.

## Monte Carlo prop firm (10 000 chemins i.i.d. ; une nuit filtrée vaut 0 et compte comme un jour)

P(réussite) en %, puis jours de trading médians jusqu'à la réussite. S3 = FTMO 1-Step au risque du plan (2,5 % par trade) : +4 R avant −4 R sous le plus haut.

| Filtre | S1 +10/−10 | jours | S2 +8/−6 | jours | S3 FTMO | jours |
|---|---|---|---|---|---|---|
| Baseline 100 % | 80,2 | 48 | 65,7 | 29 | 50,0 | 8 |
| Logit 70 % | 81,3 | 67 | 67,7 | 41 | 50,6 | 12 |
| Logit 50 % | 75,5 | 96 | 61,5 | 59 | 47,5 | 15 |
| Logit 35 % | 76,8 | 138 | 63,7 | 83 | 48,6 | 23 |
| LightGBM 70 % | 79,7 | 69 | 66,6 | 42 | 49,7 | 12 |
| LightGBM 50 % | 81,7 | 94 | 68,2 | 59 | 51,5 | 16 |
| LightGBM 35 % | 81,6 | 134 | 68,5 | 83 | 52,1 | 23 |
| Abdi seule 70 % | 83,2 | 65 | 68,6 | 41 | 51,6 | 12 |
| Abdi seule 50 % | 82,7 | 93 | 68,6 | 58 | 52,3 | 16 |
| Abdi seule 35 % | 86,2 | 125 | 73,0 | 79 | 53,8 | 23 |
| *p95 filtres aléatoires 70 / 50 / 35 %* | *83,7 / 85,8 / 87,7* | | *69,9 / 72,0 / 74,5* | | *52,5 / 54,3 / 55,6* | |

Comme la taille est fixe, filtrer au hasard ne change pas la probabilité de réussite (une nuit à 0 ne bouge pas le solde) : seule la durée s'allonge, environ en 1/q. Un filtre ne peut donc améliorer le passage qu'en relevant l'E[R] par trade. Ici, au mieux, il gagne 1 à 2 points de P(réussite) (dans le bruit des filtres aléatoires) et il faut 1,4 à 2,9 fois plus de jours. En blocs de 20 nuits (sensibilité), les conclusions ne changent pas.

## Stabilité

- **Importances** : la logit n'a que des coefficients minuscules (|β| ≤ 0,06 en écart type). Seul le signe d'`abdi` est stable (négatif dans les 5 blocs, ce qui va dans le sens du retournement). LightGBM ne donne presque aucun poids à `annonce` (0 dans 4 blocs sur 5) et répartit le gain entre `mom`, `abdi` et `blw` sans hiérarchie stable.
- **Gain de E[R] par sous-période** (2011-13, 2014-16, 2017-19, 2020-22, 2023-26) : positif sur 5 / 5 seulement pour la logit 70 % (+0,003 à +0,063), qui n'est pourtant pas significative. Sur 2023 → 2026-08, **les 9 filtres sauf la logit 70 % retirent de l'E[R]** (−0,014 à −0,059).

## Réponse au critère strict

Aucun modèle ML ne bat significativement la baseline ni la règle Abdi seule, que ce soit sur la probabilité de passage Monte Carlo ou sur l'espérance par trade hors bloc. **Recommandation : ne pas utiliser de filtre ML sur mom.** Rien ne justifie d'ouvrir le holdout pour ces filtres. Abdi seule, la meilleure des neuf, reste elle aussi non significative (p 0,06-0,23) et négative sur 2023-2026. Elle s'ajoute aux filtres « nuit précédente » déjà rejetés au n° 13.

## Limites

- Le seuil de chaque filtre est un quantile des scores hors bloc de toute la période : il est connu après coup (seulement pour le taux, pas pour le classement des nuits).
- Le Monte Carlo i.i.d. ignore la persistance des régimes. La version en blocs de 20 nuits donne les mêmes classements.
- La perte du jour (3 %) et la règle du meilleur jour de FTMO ne mordent jamais à taille fixe 2,5 %. La réduction de l'objectif au reste à faire et le passage en financé ne sont pas modélisés.
- La règle mom traverse minuit, ce qui ne respecte pas la contrainte « intraday uniquement » énoncée le 2026-11-19. C'est pourtant la règle du compte A FTMO réel, testée ici à la demande de l'utilisateur.
