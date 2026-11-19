# Montée en taille FTMO avec deux stratégies (A = mom, B = 3n + M2), de 2 × 10k à 4 × 100k

*2026-11-04. **Exploratoire, hors compteur.** Script : [run_ftmo_scaling.py](../run_ftmo_scaling.py). Sorties : `results/ftmo_scaling/` (`run.log`, `historique_evenements.csv`, `glissants.csv`, `mc_historique.csv`, `mc_edge_2.csv`).*

## Règles (demande de l'utilisateur)

| Palier | Comptes par stratégie (A et B) | Capital FTMO | Réserve requise (10 évals par paire A + B) |
|---|---|---|---|
| 1 (départ) | 1 × 10k | 20k | 869 $ (= dépôt de départ) |
| 2 | 2 × 10k | 40k | 1 738 $ |
| 3 | 3 × 10k | 60k | 2 607 $ |
| 4 | 1 × 100k (les 10k ne sont plus rachetés quand ils sautent) | 200k (+ les 10k restants) | 5 489 $ |
| 5 | 2 × 100k (les 10k restants sont abandonnés) | **400k = plafond FTMO** | 10 978 $ |

- **Cagnotte** = dépôt + rewards − frais d'éval. On passe au palier suivant dès que la cagnotte couvre la réserve de ce palier. Rien n'est retiré ; l'« excédent » est ce qu'on pourrait retirer au-delà de la réserve.
- **Évals** : 10k à 79 € (86,90 $), 100k à 499 € (548,90 $). Un compte perdu est racheté le lendemain si la cagnotte le permet.
- **Réserve.** Les comptes d'une même stratégie tradent les mêmes trades et sautent ensemble : la réserve s'additionne paire par paire. Le niveau de 10 évals par paire est celui à 99 % du Monte-Carlo.
- **Trading** : règle des annonces et politique cible + attente, comme dans [[reports/ftmo_deux_comptes_historique_report]].

## Vrai chemin (2011-07-01 → 2026-11-03)

| Date | Événement | Cagnotte |
|---|---|---|
| 01/07/2011 | départ : 1 × 10k A + 1 × 10k B | 869 $ déposés |
| 07/11/2011 | palier 2 (2 × 10k chacun) | 1 683 $ |
| 24/01/2012 | palier 3 (3 × 10k chacun) | 2 484 $ |
| 15/03/2012 | palier 4 (1 × 100k chacun) | 4 439 $ |
| **25/04/2012** | **palier 5 (2 × 100k chacun, 400k)**, environ 10 mois après le départ | 10 354 $ |

Cagnotte en fin d'année : 2012 72 626 $, 2013 160 863 $, 2014 279 115 $, 2015 372 894 $, 2016 440 805 $, 2018 626 280 $, 2020 802 029 $, 2022 952 530 $, 2024 1 092 742 $, 2026 (au 03/11) **1 308 914 $**. Le plus bas de la cagnotte est 695 $, et aucun rachat n'a jamais manqué d'argent. Au palier 5, le rythme est d'environ 90 000 $ par an.

## Distribution sur 5 ans

| | Départs glissants (130, 2011-2021) | Monte-Carlo historique (1 000) | **Monte-Carlo edge / 2 (1 000)** |
|---|---|---|---|
| Palier 2 : atteint / délai médian | 100 % / 4,0 mois | 100 % / 3,9 mois | 98 % / 5,7 mois |
| Palier 3 | 100 % / 6,0 mois | 100 % / 6,1 mois | 98 % / 9,0 mois |
| Palier 4 (100k) | 100 % / 9,4 mois | 100 % / 9,5 mois | 98 % / 14,1 mois |
| **Palier 5 (400k)** : atteint / délai médian (10e-90e centile) | 100 % / 11,9 mois (9,0-15,4) | 100 % / 12,0 mois (8,4-17,3) | 96 % / **17,7 mois** (11,7-27,0) |
| Cagnotte à 1 an : médiane (10e centile) | +10 022 $ (+3 796 $) | +9 642 $ (+3 091 $) | +3 447 $ (+1 260 $) |
| **Cagnotte à 5 ans : médiane (5e centile)** | +345 622 $ (+290 924 $) | +375 371 $ (+272 349 $) | **+212 428 $ (+96 317 $)** |
| Plus bas de la cagnotte : médiane / 5e centile / pire | 608 / 435 / 261 $ | 608 / 347 / 0 $ | 521 / 60 / 0 $ |
| Chemins où un rachat a dû attendre faute d'argent | 0 % | 1 % | 6 % |

Une version plus prudente, avec 10 évals par compte (20 par paire, dépôt de 1 738 $), atteint le palier 5 en environ 19 mois (historique) ou 29 mois (edge / 2). Elle est dans `results/ftmo_scaling/run_reserve_20evals.log`.

## Lecture

1. **Avec ces règles, le chemin vers 400k est court** : environ 1 an en médiane, environ 18 mois si l'espérance est divisée par deux. Le seul argent sorti de la poche est le dépôt de 869 $. Tout le reste est financé par les rewards.
2. **Le moment risqué est le début.** Dans les 6 premiers mois, la cagnotte peut tomber à 0 (1 à 6 % des chemins), et un rachat doit alors attendre le reward suivant. Une fois le palier 4 atteint, la cagnotte dépasse largement les réserves.
3. **Les montants à 5 ans, de 200 000 à 375 000 $ en médiane, sont théoriques.** Ils reposent sur plusieurs hypothèses fortes.
   - **La stratégie** : son edge tiendrait sur 5 ans. Or 3n et M2 ont échoué hors échantillon.
   - **FTMO** paierait sans limite ni refus. Or un trader qui touche environ 7 000 $ par mois sur 4 comptes de 100k est examiné de près, et les mêmes trades sur plusieurs comptes doivent rester dans le plafond de 400k et dans les conditions générales.
   - **Les coûts réels** : le spread du CFD et le glissement sur 1 % de 100k (1 000 $ de risque par trade) sont ceux du backtest ; les délais d'examen et de fourniture des comptes ne sont pas modélisés.
   - **La fiscalité** n'est pas prise en compte.
4. **Calcul.** Les trades sont calculés avec vectorbt : mom avec `run_recolte1_atr.simulate`, 3n et M2 avec `run_propfirm_combo.simule`, contrôlés par une boucle à la main. Les règles FTMO (plancher suiveur, règle du meilleur jour, rewards, rachats, paliers) sont gérées en Python, comme dans tout le n° 18.

## Métriques complètes (2026-11-04)

Script : [run_ftmo_scaling_metrics.py](../run_ftmo_scaling_metrics.py). Sorties : `results/ftmo_scaling/metriques.log` et `metriques_<simulation>.csv`.

- Mêmes règles et mêmes chemins que plus haut, avec une gestion instrumentée.
- Les cases donnent la **médiane** et, entre parenthèses, le **5e centile** ou la fourchette **10e-90e centile**.
- Un mois vaut 21 séances. Le vrai chemin dure 15,3 ans ; les autres simulations, 5 ans.

| | Vrai chemin 2011-2026 | Départs glissants (130) | Monte-Carlo historique (1 000) | Monte-Carlo edge / 2 (1 000) |
|---|---|---|---|---|
| **Palier 2 (2 × 10k chacun)**, mois | 4,3 | 4,0 | 3,9 | 5,7 |
| **Palier 3 (3 × 10k)** | 6,9 | 6,0 | 6,1 | 9,0 |
| **Palier 4 (1 × 100k)** | 8,6 | 9,4 | 9,5 | 14,1 |
| **Palier 5 (400k)** (10e-90e centile) | **10,0** | **11,9** (9,0-15,4) | **12,0** (8,4-17,3) | **17,7** (11,7-27,0) |
| 400k atteints en 5 ans | oui | 100 % | 99,8 % | 96,5 % |
| **Ruine** (dépôt de 869 $ perdu, cagnotte bloquée à 0) | non | 0 % | 0,2 % | 2,5 % |
| Cagnotte à 6 mois (5e centile) | 1 950 $ | 2 433 $ (1 225 $) | 2 355 $ (968 $) | 1 597 $ (340 $) |
| Cagnotte à 1 an | 20 311 $ | 10 022 $ (3 378 $) | 9 642 $ (2 413 $) | 3 447 $ (808 $) |
| Cagnotte à 2 ans | 98 397 $ | 90 042 $ (60 703 $) | 95 913 $ (33 344 $) | 34 539 $ (2 394 $) |
| Cagnotte à 3 ans | 209 745 $ | 175 007 $ (123 712 $) | 190 580 $ (112 986 $) | 94 911 $ (9 721 $) |
| **Cagnotte à 5 ans** | **399 122 $** | **345 622 $** (290 924 $) | **375 371 $** (272 349 $) | **212 428 $** (96 317 $) |
| **Revenu mensuel à 400k** (moyenne par chemin) | 7 380 $ | 6 916 $ (5 809 $) | 7 667 $ (5 685 $) | 4 961 $ (3 110 $) |
| Mois négatifs à 400k | 10 % | 9 % | 11 % | 22 % |
| Pire mois à 400k (5e centile) | −3 293 $ | −2 196 $ (−3 293 $) | −2 196 $ (−3 293 $) | −3 293 $ (−4 391 $) |
| **Max DD de la cagnotte** (5e centile) | −5 489 $ | −3 293 $ (−5 489 $) | −3 293 $ (−7 685 $) | −5 489 $ (−10 978 $) |
| Plus bas de la cagnotte (5e centile) | 695 $ | 608 $ (435 $) | 608 $ (348 $) | 521 $ (60 $) |
| **Plus longue attente d'un reward** (90e centile) | 3,3 mois | 3,3 mois (5,0) | 4,1 mois (6,0) | 5,6 mois (8,6) |
| Évals achetées, 10k / 100k | 11 / 100 (sur 15 ans) | 12 / 30,5 | 12 / 30,5 | 20 / 47 |
| Évals 100k ratées / comptes financés 100k perdus | 51 / 45 | 14,5 / 12 | 12 / 14 | 23 / 19 |
| **Frais d'éval totaux** | 55 846 $ (15 ans) | 17 624 $ | 17 944 $ | 28 117 $ |
| Rewards, nombre 10k / 100k | 26 / 403 | 27 / 103,5 | 27 / 115 | 28 / 71 |
| **Rewards encaissés** | 1 363 891 $ (15 ans) | 363 657 $ | 392 537 $ | 240 450 $ |

Vrai chemin, gain par année civile : 2012 +70 677 $, 2013 +88 237 $, 2014 +118 252 $, 2015 +93 780 $, 2016 +67 911 $, 2017 +97 154 $, 2018 +88 320 $, 2019 +87 143 $, 2020 +88 606 $, 2021 +90 562 $, 2022 +59 939 $, 2023 +61 848 $, 2024 +78 365 $, 2025 +96 233 $, 2026 (au 03/11) +119 939 $. À 400k, le revenu mensuel fait 7 404 $ en moyenne et 7 027 $ en médiane ; 13 % des mois sont négatifs ; le pire mois est −3 293 $ (mai 2025), le meilleur +28 116 $.

**Lecture des métriques :**
- **Ruine.** C'est le cas où le dépôt de 869 $ est perdu avant le premier reward et où la cagnotte reste bloquée à 0. Elle arrive dans 0 à 0,2 % des chemins avec l'edge historique, et dans 2,5 % avec l'espérance divisée par deux. Il suffit de réinjecter un ou deux prix d'éval pour en sortir.
- **Le max DD de la cagnotte vient presque toujours de séries d'évals 100k ratées** (3 293 $ = 6 évals, 5 489 $ = 10 évals). Une fois les 400k atteints, la cagnotte couvre déjà la réserve de 10 978 $ : ce DD n'interrompt jamais le trading.
- **Les comptes 100k sautent souvent** (12 à 19 comptes financés perdus et 12 à 23 évals ratées sur 5 ans). C'est normal avec ces règles : la politique rachète, et les rewards paient largement les rachats (frais ≈ 5 % des rewards dans les scénarios historiques, 12 % avec l'espérance divisée par deux).
