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
