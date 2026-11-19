# Évals FTMO plus rapides avec mom, 3n et M2 : grille choisie sur 2011-2018, vérifiée sur 2019-2026

*2026-11-04. **Exploratoire, hors compteur** : réglage d'un contrat sur des trades existants. Script : [run_propfirm_eval_rapide.py](../run_propfirm_eval_rapide.py). Sorties : `results/propfirm_eval_rapide/` (`run.log`, `grille.csv`, `retenus.csv`).*

## Méthode

- **Trades.** Objectif à 2 R partout : 3n et M2 viennent de [[reports/propfirm_combo_report]], mom a son TP à 4 ATR.
- **Durée.** Elle est comptée en **séances calendaires**, environ 21 par mois : un jour sans trade fait aussi avancer l'horloge.
- **Plans.** Chaque trade a son risque en % du capital, et la somme du jour ne dépasse jamais 2,5 %.
  - **A** : 3n en priorité ; sinon mom, puis M2.
  - **B** : mom chaque nuit, puis M2 ; 3n ignoré.
  - **C** : 3n et mom ensemble les nuits 3n ; sinon mom ; M2 les jours sans 3n.
  - Niveaux de risque : 0,5 à 2,5 %, soit **384 réglages**.
- **Choix sur 2011-07 → 2018-12** (5 000 comptes) : parmi les réglages qui passent au moins 60 % des évals, on prend le plus court. **Vérification sur 2019-01 → 2026-08** sans rien changer (20 000 comptes).
- **Moteur.** Celui du n° 18, à plusieurs trades par jour, avec un coût CFD de 1,5 point.

## Le compromis : vitesse contre taux de passage (front 2011-2018)

| Plan (r3n / rmom / rM2) | Passage | Durée moyenne d'une éval validée | Médiane | 90e centile |
|---|---|---|---|---|
| B (– / 2,5 / –) = mom seul | 52 % | 9,4 séances | 8 | 17 |
| A (2,5 / 2,5 / –) | 54 % | 12,1 | 10 | 25 |
| C (0,5 / 2,0 / –) | 58 % | 13,1 | 11 | 25 |
| A (2,5 / 2,0 / 0,5) | 63 % | 16,6 | 14 | 33 |
| C (1,0 / 1,5 / 1,0) | 65 % | 18,4 | 16 | 34 |
| A (2,5 / 1,5 / 0,75) | 73 % | 23,0 | 20 | 42 |
| **A (2,5 / 1,25 / 1,25) = trio demandé** | **73 %** | **24,2** | 22 | 43 |
| C (1,0 / 0,75 / –) | 85 % | 44,5 | 39 | 78 |
| B (– / 0,5 / 0,75) | 100 % | 116 | 93 | 213 |

## Vérification 2019-2026 (rien changé)

| Réglage | Passage 2011-2018 → 2019-2026 | Durée moyenne (séances) 2011-2018 → 2019-2026 |
|---|---|---|
| **Choisi : A (2,5 / 2,0 / –)** | 61,5 % → **47,8 %** | 16,3 → **15,6** |
| Choisi : A (2,5 / 2,0 / 0,5) | 63,4 % → 47,4 % | 16,6 → 15,3 |
| Choisi : A (2,0 / 2,0 / –) | 62,5 % → 48,5 % | 17,8 → 19,4 |
| Choisi : C (1,0 / 1,5 / –) | 61,0 % → 57,9 % | 17,6 → 24,4 |
| Choisi : C (1,0 / 1,5 / 0,5) | 62,0 % → 56,9 % | 18,1 → 22,7 |
| **Trio demandé (2,5 / 1,25 / 1,25)** | 72,3 % → **58,2 %** | 24,5 → **21,2** |
| mom seul à 2,5 % | 51,1 % → 42,4 % | 9,5 → 9,5 |

## Lecture

1. **Il n'existe pas de plan qui soit à la fois plus rapide et aussi sûr que le trio.** Sur la période de vérification, les réglages plus rapides (environ 15 séances, 3 semaines) passent moins de 50 % des évals. Les réglages qui gardent environ 57 % de passage durent autant que le trio, voire plus (22 à 24 séances). **Le trio demandé est déjà sur le front.**
2. **La vitesse d'une éval vient surtout du risque, pas de l'edge.** Avec +0,1 à +0,15 R par trade, la dérive attendue est d'environ 0,2-0,3 % par jour, soit 30 à 50 jours pour atteindre +10 %. Une éval passe plus vite que ça parce qu'une série favorable l'y porte. Plus de risque donne des séries plus grandes dans les deux sens : on va plus vite, mais on échoue plus souvent.
3. **Le passage baisse de 3 à 15 points sur 2019-2026**, sur tous les réglages, mom seul compris. C'est la période où les nuits du NQ sont moins favorables, et c'est aussi le signe d'une part de sélection dans la grille.
4. **Pour aller plus vite sans perdre de passage, il faudrait changer le contrat**, pas le plan. Par exemple, un objectif de trade plus large en éval (2,5 à 3 R) ou une baisse du risque une fois proche des +10 %. Ces pistes ne sont pas testées ici : pour 3n et M2, les trades n'existent qu'avec un objectif à 2 R.

> **Correction du 2026-11-04** : en éval, l'objectif de chaque trade est désormais ramené au reste à faire. Les chiffres ci-dessus sont ceux de l'objectif fixe ; les chiffres corrigés sont dans [[reports/propfirm_correction_reste_report]] (passage +1 à +7 points, mêmes classements).
