# FTMO 1-Step : un plan pour l'éval, un autre pour le financé (mom seul / trio)

*2026-11-04. **Exploratoire, hors compteur.** Script : [run_propfirm_mix.py](../run_propfirm_mix.py). Sorties : `results/propfirm_mix/` (`run.log`, `mix.csv`). Le moteur et les trades sont ceux de [[reports/propfirm_trio_report]] (objectif à 2 R, coût CFD 1,5 point). 20 000 comptes, graine 1829.*

Plans :
- **Éval à 2,5 %** : « mom » = mom seul à 2,5 % ; « trio » = 3n à 2,5 % si signal, sinon mom 1,25 % + M2 1,25 %.
- **Financé à 1 %** : « mom » = mom seul à 1 % ; « trio » = 3n à 1 %, sinon mom 0,5 % + M2 0,5 %.

| Période | Éval → financé | Passage | Durée de l'éval | Valeur du financé | Vie | **EV 10k** | **EV 100k** | **EV / mois 100k** |
|---|---|---|---|---|---|---|---|---|
| 2016-2026 | mom → mom | 43,8 % | 0,4 mois | 16,1 % | 6 mois | +617 $ | +6 495 $ | **+1 978 $** |
| | **mom → trio** | 43,8 % | 0,4 mois | 35,1 % | 21 mois | **+1 451 $** | **+14 831 $** | +1 518 $ |
| | trio → mom | 60,5 % | 1,1 mois | 16,1 % | 6 mois | +886 $ | +9 177 $ | +1 815 $ |
| | trio → trio | 60,5 % | 1,1 mois | 35,1 % | 21 mois | **+2 037 $** | **+20 687 $** | +1 476 $ |
| 2011-2015 | mom → mom | 55,9 % | 0,5 mois | 33,7 % | 9 mois | +1 793 $ | +18 250 $ | **+3 393 $** |
| | **mom → trio** | 55,9 % | 0,5 mois | 48,7 % | 28 mois | +2 632 $ | +26 644 $ | +1 648 $ |
| | trio → trio | 71,1 % | 1,1 mois | 48,7 % | 28 mois | **+3 376 $** | **+34 085 $** | +1 617 $ |
| 2019-2026 | mom → mom | 43,0 % | 0,4 mois | 13,5 % | 6 mois | +494 $ | +5 258 $ | **+1 834 $** |
| | **mom → trio** | 43,0 % | 0,4 mois | 35,5 % | 23 mois | +1 443 $ | +14 746 $ | +1 409 $ |
| | trio → trio | 56,2 % | 1,0 mois | 35,5 % | 23 mois | **+1 911 $** | **+19 430 $** | +1 372 $ |

## Lecture

1. **mom en éval puis trio en financé est un compromis, mais il ne domine sur aucun critère.**
   - L'éval passe en environ 2 semaines au lieu d'un mois.
   - **Par tentative**, on perd environ 30 % face à trio → trio (+1 451 $ contre +2 037 $ sur 10k, 2016-2026), parce que l'éval mom passe moins souvent (44 % contre 60 %).
   - **Par mois d'emplacement**, c'est à peine mieux que trio → trio (+1 518 $ contre +1 476 $), et nettement sous mom → mom (+1 978 $).
2. **Le choix du plan financé compte plus que celui de l'éval.** Un compte financé trio vaut environ 2 fois plus qu'un compte financé mom (35 % du capital contre 16 %), car il vit 3 à 4 fois plus longtemps.
3. **mom → mom reste le meilleur par mois.** Il rapporte vite, mais il saute vite : environ 6 mois de vie, et une éval à racheter environ tous les 3 mois et demi par emplacement.
4. **Résumé du choix :**
   - beaucoup d'emplacements, et des évals bon marché à racheter sans problème : **mom → mom** ;
   - peu de comptes, ou envie de garder longtemps un compte financé sans racheter : **trio → trio** ;
   - **mom → trio** ne vaut que si la durée de l'éval compte en elle-même, par exemple pour accéder plus vite à un compte financé.
5. **Réserves** : ce sont les mêmes que pour le trio. La règle FTMO des annonces n'est pas modélisée (mom traverse 8:30, M2 traverse 10:00 et 14:00). 3n et M2 ont échoué hors échantillon. Les rewards sont supposés versés sans refus.

> **Correction du 2026-11-04** : en éval, l'objectif de chaque trade est désormais ramené au reste à faire. Les chiffres ci-dessus sont ceux de l'objectif fixe ; les chiffres corrigés sont dans [[reports/propfirm_correction_reste_report]] (passage +1 à +7 points, mêmes classements).
