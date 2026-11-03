# N° 26, avenant A : lecture anticipée du holdout, 2026-08-31 → 2026-11-03 (exploratoire, sans verdict)

*2026-11-03. Cadre : [[PREREGISTRATION_26]], avenant A (commit 9f87d69, avant calcul). Cette fenêtre est désormais **vue**. Le holdout officiel du n° 26 commence le 2026-11-04, et les lectures L1, L2 et L3 ne changent pas. Compteur global : 1 738 → 1 742 (4 essais exploratoires). Code : [run_holdout_anticipe.py](../run_holdout_anticipe.py). Sorties : `results/holdout_anticipe/` ; données raboutées dans `cache/holdout_anticipe/`.*

## Données

- **Sources.** Databento NQ.v.0 jusqu'au 2026-08-28, puis London Strategic Edge (`NASDAQ100`). À la jonction, l'écart est de +0,1 bp (29 509,50 contre 29 509,75) : c'est le même contrat.
- **Roulement LSE.** La règle de l'avenant A ne détecte **aucun roulement** en septembre. Dans toute la série LSE, le plus gros saut de septembre fait 17 bps, à la réouverture du dimanche 27/09. Pourtant le contrat de septembre a expiré le 18/09. Or LSE montrait bien des sauts de roulement en mars (+93 bps le 18/03) et en juin (+173 bps le 14/06). Pour la lecture : aucune fenêtre de trade ne contient de saut artificiel. Mais ce point est **à vérifier avec Databento à la lecture L1**.
- **Trous.** RTH du 2026-10-12 (86 barres) et 2026-10-16 de 9:30 à 9:58 : M2 saute ces séances, comme prévu par la règle.

## Résultats (4 hypothèses, code figé)

| Hypothèse | n | Moyenne | t | p unilatéral |
|---|---|---|---|---|
| H1 mom (R net par nuit) | 44 nuits, toutes longues | **−0,023 R** (total −1,0 R) | −0,14 | 0,55 |
| H2 M2 ($ net par trade, 1 NQ) | **9 trades** (4 longs) | +716 $ (+11,7 bps) ; net +6 440 $ | 3,25 | 0,0006 |
| H3 3n SL (R net par trade) | 23 trades | +0,379 R ; net +13 237 $ | 1,36 | 0,087 |
| H4 rebond (r3 ≤ −50 bps, moins les autres nuits) | 11 nuits contre 35 | +15,0 contre −4,9 bps net (écart +19,8) | 1,19 | 0,13 |

Détails :
- **H1** : le signe du momentum 12-1 est positif chaque mois (septembre à novembre), donc la règle est longue chaque nuit. Sorties : 28 stops, 10 TP, 6 en fin de fenêtre.
- **H2** : le signal C, tous les jours, fait +625 $ par trade sur la même fenêtre.

## Lecture

- **Rien ne peut être conclu**, et c'était prévu par l'avenant. Les intervalles couvrent presque tout. Pour H2, le t de 3,25 porte sur **9 trades**, et l'erreur Newey-West est peu fiable à cette taille. Ce sont des chiffres d'humeur, pas des preuves.
- **Comme sur 2025-2026, la période est favorable au suivi de la séance US.** C gagne autant que M2 par trade (+625 contre +716 $). C'est l'environnement de forte volatilité déjà noté dans le rapport d'origine.
- **mom est plat sur ces deux mois** (−1 R), avec beaucoup de stops. C'est dans sa variance normale : sur 2016-2026, son max DD est de −25 R.
- **3n et le rebond vont dans le sens attendu**, sans être significatifs. Leurs tests hors échantillon sur 2010-2015 avaient échoué (n° 24) ou n'avaient pas été faits (rebond, « à surveiller »).
- **Ces deux mois ne comptent pas** pour le verdict du n° 26, qui portera sur les données à partir du 2026-11-04 (lectures 2028-02-29, 2029-08-31 et 2031-08-29).
