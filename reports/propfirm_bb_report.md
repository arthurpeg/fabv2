# BB (bande de bruit) en prop firm : un trade par jour, éval à risque élevé

*2026-11-22. Demande de l'utilisateur : exploiter BB dans l'approche par convexité (risque élevé en éval pour valider ou échouer vite), avec un trade par jour. Deux étapes, toutes deux **exploratoires** sur NQ 2016-01 → 2026-08 (données déjà vues ; BB est au registre des échecs, réouverture seulement sur des données après le 2026-08-28) :*
1. *[run_bb_1j.py](../run_bb_1j.py) (branche `strategies-vbt`, grille commitée avant calcul, commit `e1f932a`) : BB, VWAP exigé à l'entrée, SL = k × ATR14, TP = RR × SL, modes A (stop suiveur gardé) et B (remplacé), **premier trade de la séance seulement** ; 18 essais. Compteur global : 2 127 (2 109 + 18).*
2. *[run_propfirm_bb.py](../run_propfirm_bb.py) (branche `propfirm-ftmo`, hors compteur comme les autres simulations de contrat) : moteur FTMO 1-Step du n° 18 (un trade = une journée, objectif +10 %, perte max 10 %, perte du jour 3 %, meilleur jour ≤ 50 %, reward tous les 10 trades, partage 90 %, coût CFD 1,5 pt), 10 000 comptes par réglage ; éval à 1 / 2 / 2,5 / 2,9 % de risque (sous la limite journalière de 3 %), financé 1 %.*

## 1. BB à un trade par jour (1 contrat, net de 0,50 pt ; 1 R = k × ATR14)

| Version | Trades/an | R net/trade (t) | Gagnants | R/an | Pire creux | Pertes de suite | $/an |
|---|---|---|---|---|---|---|---|
| A, SL 0,25, TP 1R | 142 | +0,075 (3,5) | 49 % | 10,7 | −15,5 R | 9 | 11 500 |
| **A, SL 0,25, TP 2R** | 142 | **+0,124 (4,2)** | 40 % | **17,6** | **−14,7 R** | 12 | 19 800 |
| **A, SL 0,25, TP 3R** | 141 | **+0,148 (4,4)** | 37 % | **21,0** | **−14,1 R** | 12 | 22 200 |
| A, SL 0,5, TP 1-3R | 141 | +0,06-0,07 | 39-42 % | 9-10 | −8 à −11 R | 12 | 18 700-21 100 |
| A, SL 1, TP 1-3R | 141 | +0,035 | 39 % | 5 | −6 R | 12 | 20 000-21 700 |
| B, SL 0,25, TP 2R / 3R | 141 | +0,124 / +0,148 | 43 / 41 % | 17,5 / 21,0 | −19 / −21 R | 12 | 20 400 / 23 400 |
| B, SL 1, TP 1R | 141 | +0,038 | 55 % | 5,3 | −15,6 R | 7 | 34 100 |

Avec la limite d'un trade par jour, le R par trade s'améliore nettement (A, SL 0,25, TP 3R : +0,148 R contre +0,119 R sans limite) et le pire creux est presque divisé par deux (−14 R contre −25 à −26 R) : les ré-entrées de la journée étaient les plus mauvaises. Résultat stable entre 2016-2022 et 2023-2026 (A, SL 0,25, TP 2R : +0,124 puis +0,125 R). Tableau complet : `results/bb_1j/grille.csv`.

## 2. FTMO 1-Step (éval au risque indiqué, financé 1 %)

| Réglage | Risque éval | Passage | Trades médians (validée / ratée) | EV par tentative 10k / 100k | EV par mois d'emplacement 100k |
|---|---|---|---|---|---|
| A, SL 0,25, TP 2R | 1 % | 74 % | 50 / 62 | +2 078 / +21 101 $ | +1 162 $ |
| A, SL 0,25, TP 2R | **2,5 %** | 56 % | **10 / 13** | +1 583 / +16 154 $ | **+1 453 $** |
| A, SL 0,25, TP 3R | 1 % | 85 % | 43 / 52 | +2 818 / +28 497 $ | +1 422 $ |
| A, SL 0,25, TP 3R | **2 %** | 56 % | **15 / 18** | +1 820 / +18 522 $ | **+1 554 $** |
| A, SL 0,25, TP 3R | 2,5 % | 47 % | 13 / 13 | +1 542 / +15 738 $ | +1 557 $ |
| B, SL 0,25, TP 3R | 2 % | 51 % | 12 / 11 | +849 / +8 806 $ | +1 561 $ (meilleur de la grille) |
| B, SL 0,25, TP 2R | 2,5 % | 53 % | 9 / 8 | +895 / +9 273 $ | +1 525 $ |
| A, SL 0,5, TP 3R | 1 % | 100 % | 134 / — | +2 879 / +29 106 $ | +535 $ |
| Témoin sans edge (B, SL 0,25, TP 3R, 2 %) | 2 % | 31 % | — | +70 / +1 019 $ | +406 $ |
| *Plan : 3n + M2 (EMA 9:30) combinés* | *2,5 %* | *60 %* | *13 (moyenne)* | *+2 123 / +21 546 $* | *+1 477 $* |
| *Plan : mom seul* | *2,5 %* | *44 %* | *9 (moyenne)* | *+626 / +6 583 $* | *+1 989 $* |

Tableau complet (72 réglages) : `results/propfirm_bb/ftmo.csv`. Un trade toutes les 1,8 séances environ : 10 trades ≈ 3 à 4 semaines.

## Lecture

1. **La convexité fonctionne avec BB comme avec les autres stratégies** : en montant le risque d'éval de 1 % à 2-2,5 %, l'éval se joue en 10 à 15 trades au lieu de 40 à 130, le passage baisse (de 74-85 % à 47-56 %), et l'**EV par mois d'emplacement augmente** (A, SL 0,25, TP 2R : +1 162 → +1 453 $ par mois en 100k). Au-delà de 2,5 %, plus rien ne s'améliore.
2. **La bonne version pour la prop firm est le SL serré (0,25 ATR) avec TP 2R ou 3R.** Les SL plus larges donnent un meilleur taux de passage à 1 % mais une éval très longue (100 à 290 trades) : l'EV par mois s'effondre (+300 à +640 $).
3. **BB vaut à peu près le plan actuel** (3n + M2 : +1 477 $ par mois en 100k), moins que mom seul (+1 989 $). Il ne le domine pas.
4. **Le témoin sans edge fait +406 $ par mois** : une partie du gain vient de la structure du contrat (perte plafonnée au prix de l'éval), le reste (≈ +1 150 $ par mois) de l'avantage historique de BB.
5. **Mode A plutôt que B** : même EV par mois, mais en mode A un compte financé vit deux fois plus longtemps (≈ 18 contre ≈ 9 mois) et verse plus (≈ 30-35 % du capital contre ≈ 18 %).

## Réserves

- Tout est sur des données déjà explorées, et le réglage est choisi parmi 18 versions × 4 risques : ces EV sont optimistes. BB a eu un DSR de 0,03, et sa période ancienne est faible (≈ 0,55 de Sharpe sur 2010-2015).
- BB trade en séance US comme le M2 (EMA 9:30) du book B : sur des comptes FTMO différents, il faudrait respecter la règle anti-hedging (pas de positions opposées sur le même produit), non modélisée ici.
- Glissement sur les stops serrés (Chuk : 1 pt ≈ −22 % de l'avantage), refus de reward et délais FTMO non modélisés.
