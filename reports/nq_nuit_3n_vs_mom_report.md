# Filtre 3 nuits (stratégie transmise) contre notre règle NQ de nuit

Date : 2026-11-03. **Descriptif, hors compteur.** Aucun nouveau signal : on compare deux séries de trades qui existaient déjà. Script : [run_nq_nuit_3n_vs_mom.py](../run_nq_nuit_3n_vs_mom.py). Sorties : `results/nq_nuit_3n_vs_mom/` (`run.log`, `nuits.csv`, `annees.csv`).

| | **3n SL** (transmise, [[reports/nq_nuit_3n_vbt_report]]) | **mom** (la nôtre, [[wiki/experiments/nq-nuit-momentum]]) |
|---|---|---|
| Fenêtre | 20:05 → 03:00 ET | 20:00 → 9:30 ET |
| Signal | long si la somme des 3 nuits précédentes ≤ 0, sinon à plat | signe du momentum 12-1 : long (89 % des nuits) ou short |
| Sortie | stop 2 × ATR M15, sinon 03:00 | SL 2 / TP 5 ATR M15, sinon 9:30 |
| En position | 42 % des nuits | ≈ 100 % des nuits |
| Origine | filtre choisi par l'auteur sur 2016-2024 (IS) | choisie sur 2016-2026, validée hors échantillon sur 2011-2015 |

**Conventions.** Les deux règles ont le même coût, celui du dépôt : 1 tick + 5 $ l'aller-retour (3n est donc compté à 10 $, pas 15 $). Il y a 2 677 nuits communes, du 2016-01-04 au 2026-08-28 ; une nuit sans trade compte 0. Pour les deux règles, **toute la période 2016-2024 est dans l'échantillon.** Le seul « hors échantillon » de 3n est 2025 → 08/2026, et ce n'en est pas un pour mom.

## 1. Performances, en R (1 R = 2 ATR M15 dans les deux règles, donc même risque par trade)

| Période | mom E[R] | mom R/an | **mom Sharpe** | mom DD R | 3n SL E[R] | 3n SL R/an | **3n SL Sharpe** | 3n SL DD R | **Les deux, Sharpe** | Les deux, R/an |
|---|---|---|---|---|---|---|---|---|---|---|
| 2016-2026 | 0,077 | 19,3 | 0,90 [0,31 ; 1,45] | −25,4 | 0,138 | 14,8 | **1,42** [0,89 ; 1,96] | −21,0 | 1,29 | 34,0 |
| 2016-2021 | 0,073 | 18,3 | 0,86 | −21,9 | 0,189 | 19,8 | **1,87** | −12,1 | 1,41 | 38,1 |
| 2022-2024 | 0,071 | 17,9 | **0,83** | −25,4 | 0,043 | 4,7 | 0,48 | −21,0 | 0,91 | 22,6 |
| 2025-08/2026 | 0,100 | 25,3 | 1,20 | −24,4 | 0,136 | 14,9 | 1,39 | −6,8 | **1,48** | 40,2 |

Les intervalles sont des IC 95 % par bootstrap par blocs.

## 2. En % du notionnel d'un contrat (sans normaliser le risque)

| 2016-2026 | mom | 3n SL | 3n sans stop | long 03h toutes les nuits | mom + 3n SL (même vol) |
|---|---|---|---|---|---|
| % / an | 7,2 | 6,5 | 7,6 | 4,7 | 9,9 |
| Vol % / an | 8,3 | 4,3 | 4,8 | 7,1 | 6,8 |
| Sharpe | 0,87 | **1,52** | 1,58 | 0,66 | 1,45 |
| Max DD % | −9,7 | −4,6 | −7,6 | −7,0 | −4,7 |
| Nuits < −2 % | 1 | 1 | 1 | 8 | 1 |

Dans la colonne « même vol », le poids de 3n SL (× 1,93) est fixé sur 2016-2024 pour égaliser les volatilités. Par année, mom perd en 2016 et 2022 ; 3n SL perd en 2023 (−1,5 %). Aucune année n'est négative pour les deux à la fois (`annees.csv`).

## 3. Les deux règles ne sont pas indépendantes

- **Corrélation par nuit : +0,35** [+0,25 ; +0,44] sur 2016-2026, et +0,49 les nuits où 3n est en position, ce qui est logique : 3n est long 20:05 → 03:00, et mom est long sur la même fenêtre 89 % du temps. La corrélation tombe à +0,09 sur 2022-2024 et vaut +0,25 sur 2025-2026.
- **Notre règle gagne surtout les nuits où 3n dit « long ».** Sur 2016-2024, mom fait **+7,5 bps/nuit** quand la somme des 3 nuits est ≤ 0, contre **−0,8 bps** sinon : écart +8,3 bps, t de Welch 3,6. C'est le même retour à la moyenne qui se lit dans notre règle. Le n° 13 l'avait déjà vu avec F2 (nuit précédente < 0 : +0,131 R/trade), rejeté parce qu'il ne coupait pas le drawdown. **En 2025-2026, c'est l'inverse :** −3,4 bps, t −0,7 ; mom gagne alors surtout les nuits où 3n est à plat.

## Lecture

1. **Par trade et sur 2016-2026, 3n SL est meilleur** : Sharpe 1,42 contre 0,90 en R, drawdown plus faible, une nuit sur deux à plat. Mais son filtre a été choisi sur ces années-là. Notre règle a été validée sur 2011-2015 ; 3n ne l'a été que sur 20 mois (Sharpe 1,39, IC [−0,13 ; +2,83]).
2. **mom est plus régulière** : Sharpe 0,83 à 1,20 dans toutes les sous-périodes. 3n tombe à 0,48 sur 2022-2024. Les deux règles se complètent par année (2022-2023), d'où une combinaison meilleure que chaque règle seule sur 2022-2024 et 2025-2026, mais moins bonne que 3n seul sur 2016-2021.
3. **Ce n'est pas un deuxième effet indépendant.** Une bonne part du rendement de mom en 2016-2024 vient des nuits qui suivent des nuits baissières. Combiner les deux revient en partie à surpondérer ces nuits-là. Le registre des phénomènes demande de vérifier ce double comptage avant toute combinaison.
4. **Pour aller plus loin, il faut un pré-enregistrement sur le holdout postérieur au 2026-08-28.** Hypothèses possibles : (a) 3n SL seul ; (b) mom en surpondérant les nuits « 3n long », la piste F2 déjà notée « ouverte » dans la page de la règle de nuit. Rien de cela n'est fait ici.
