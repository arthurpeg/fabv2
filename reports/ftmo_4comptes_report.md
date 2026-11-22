# FTMO : compte B séparé en deux (3n, M2) et compte C = BB, jusqu'à 4 comptes

*2026-11-22. Demande de l'utilisateur. Script [run_ftmo_4comptes.py](../run_ftmo_4comptes.py) (branche `propfirm-ftmo`), **exploratoire, hors compteur**. Même moteur, mêmes trades et mêmes réglages que [[reports/ftmo_bb_options_report]] : FTMO 1-Step 10k, éval 2,5 %, financé 1 %, objectif 2 R (réduit au reste à faire en éval), règle des annonces, cible + attente, coût CFD 1,5 pt ; 494 départs de 2016-01 à 2025-08, 12 mois. BB n'est pas validé hors échantillon (n° 32) ; mom a été **validé hors échantillon** sur NQ 2011-2015 (n° 11 : +0,116 R par trade, p 0,0015 ; en fait « long NQ la nuit », tous les trades hors échantillon étaient longs ; échec sur ES et YM au n° 10), alors que 3n et M2 (EMA 9:30) ont échoué hors échantillon (n° 24, 25) *(corrigé le 2026-11-22)*. Le bot n'est pas modifié. Sorties : `results/ftmo_4comptes/`.*

## Anti-hedging modélisé

FTMO interdit des positions opposées sur deux comptes. Les fenêtres de trading : mom 20:00 → 9:30, 3n 20:05 → 03:00, M2 9:35 → 15:55, BB à partir de 10:00.
- **mom et 3n** (seul chevauchement de nuit) : une nuit où mom est short, pas de 3n long (règle existante, appliquée dès que le signal de mom est short).
- **M2 et BB** (seul chevauchement de séance) : pas de BB un jour où M2 a un signal de sens opposé, que M2 soit pris ou non (162 jours sur 1 545 retirés).
- Aucun autre couple ne se chevauche dans le temps.
- **Non modélisé** : l'exposition cumulée de même sens (deux comptes longs NQ au même moment), dont la règle FTMO est floue (question posée au support) ; un conflit possible si un trade dépasse sa fenêtre (glissement d'exécution).

## Résultats (net sur 12 mois, en $)

| Configuration | Total : moyenne / médiane / 10e c. / pire départ | Évals / rewards par an | Pire creux de trésorerie |
|---|---|---|---|
| **2 comptes : A mom, B 3n + M2 (plan)** | +3 502 / +3 331 / +2 075 / +803 | 6,3 / 12,1 | −695 |
| **3 comptes : A, B, C = BB (option 2)** | **+4 971 / +4 930 / +3 485 / +1 661** | 8,2 / 16,8 | −1 043 |
| 3 comptes : A, B1 = 3n, B2 = M2 | +3 659 / +3 534 / +1 955 / +457 | 8,1 / 13,2 | −1 043 |
| **4 comptes : A, B1 = 3n, B2 = M2, C = BB** | **+5 129 / +5 010 / +3 474 / +1 511** | 9,9 / 17,9 | −1 130 |

Par compte (moyenne sur 12 mois ; part des départs où le compte perd ; évals et rewards par an) :

| Compte | Net | 10e c. | P(< 0) | Évals | Rewards |
|---|---|---|---|---|---|
| A = mom | +1 796 | +629 | 0 % | 4,1 | 6,3 |
| B = 3n + M2 | +1 705 | +725 | 0 % | 2,3 | 5,7 |
| B1 = 3n seul | +643 | −174 | **21 %** | 1,7 | 2,8 |
| B2 = M2 seul | +1 220 | +280 | 2 % | 2,3 | 4,1 |
| C = BB | +1 469 | +446 | 0 % | 1,9 | 4,7 |

Corrélations des nets entre départs : **C et A −0,43**, C et B +0,13, B1 et B2 −0,26.

Net total moyen selon l'année de départ : option 2 meilleure que le plan pour les 10 années ; 4 comptes meilleur que l'option 2 pour 8 années sur 10 (pas en 2022 ni 2023).

## Lecture

1. **Séparer B en deux comptes n'apporte presque rien** : B1 + B2 = +1 863 $ contre +1 705 $ pour B, soit +158 $ pour un emplacement de plus, et le 10e centile baisse (+1 955 contre +2 075 $). 3n seul est faible (+643 $, perdant dans 21 % des départs) : sur un compte commun, M2 complète les journées où 3n ne trade pas ou sort à 3:00.
2. **Le compte C = BB est l'ajout utile** : +1 469 $ pour un emplacement, sans départ perdant sur 12 mois, et une **corrélation négative avec A (−0,43)** : les années faibles de mom sont plutôt de bonnes années pour BB, ce qui lisse le total (10e centile +3 485 $, pire départ +1 661 $).
3. **4 comptes** fait un peu mieux que l'option 2 (+158 $ par an en moyenne), mais demande un compte de plus, des évals en plus (9,9 contre 8,2 par an) et ne gagne rien sur le 10e centile. **L'option 2 est le meilleur compromis.**

## Réserves

- Tous les chiffres sont historiques et en échantillon pour BB ; aucune des quatre stratégies n'est validée sur des données neuves.
- Exposition cumulée de même sens non limitée (règle FTMO floue) : avec plus de comptes, le risque de requalification est plus grand.
- Glissement sur les stops serrés de BB, refus de reward et délais FTMO non modélisés.
