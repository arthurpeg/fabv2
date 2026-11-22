# FTMO : remplacer 3n par BB

*2026-11-22. Demande de l'utilisateur (« mom et 3n sont très corrélées »). Script [run_ftmo_sans3n.py](../run_ftmo_sans3n.py) (branche `propfirm-ftmo`), **exploratoire, hors compteur**. Même moteur, mêmes trades et mêmes réglages que [[reports/ftmo_4comptes_report]] : FTMO 1-Step 10k, éval 2,5 %, financé 1 %, objectif 2 R, règle des annonces, cible + attente ; 494 départs de 2016-01 à 2025-08, 12 mois. Anti-hedging : mom short → pas de 3n long ; pas de BB un jour où M2 a un signal opposé. BB n'est pas validé hors échantillon (n° 32) ; mom a été **validé hors échantillon** sur NQ 2011-2015 (n° 11 : +0,116 R par trade, p 0,0015 ; en fait « long NQ la nuit », tous les trades hors échantillon étaient longs ; échec sur ES et YM au n° 10), alors que 3n et M2 (EMA 9:30) ont échoué hors échantillon (n° 24, 25) *(corrigé le 2026-11-22)*. Bot non modifié. Sorties : `results/ftmo_sans3n/`.*

## Corrélations (2016-01 → 2026-08, R des trades les mêmes jours)

| Couple | Jours communs | Corrélation des R |
|---|---|---|
| **mom et 3n** | 1 135 | **+0,45** |
| mom et M2 | 1 041 | −0,06 |
| mom et BB | 1 538 | +0,06 |
| 3n et BB | 697 | +0,05 |

Oui, mom et 3n sont nettement corrélées : mom trade 97 % des nuits de 3n, et dans 83 % de ces nuits il est long comme 3n (mêmes heures, même sens). BB n'est corrélé à aucune des deux. Au niveau des comptes, la corrélation des nets A / B du plan reste faible (+0,01), parce que le compte B contient aussi M2 et que les trajectoires d'éval et de financé diluent le lien.

## Résultats (net sur 12 mois, en $)

| Configuration | Comptes | Moyenne | Médiane | 10e c. | Pire départ | Évals / rewards par an | Pire creux | Par compte |
|---|---|---|---|---|---|---|---|---|
| Plan : A mom, B 3n + M2 | 2 | +3 502 | +3 331 | +2 075 | +803 | 6,3 / 12,1 | −695 | +1 751 |
| **R1 : A mom, B = M2 puis BB** | **2** | **+3 894** | **+3 872** | **+2 480** | **+1 171** | 6,7 / 13,1 | −869 | **+1 947** |
| R3 : A mom, C = BB | 2 | +3 265 | +3 177 | +2 285 | +552 | 5,9 / 11,1 | −869 | +1 633 |
| **Option 2 : A, B 3n + M2, C = BB** | **3** | **+4 971** | **+4 930** | **+3 485** | **+1 661** | 8,2 / 16,8 | −1 043 | +1 657 |
| R2 : A mom, B = M2, C = BB | 3 | +4 486 | +4 443 | +2 867 | +1 086 | 8,2 / 15,1 | −956 | +1 495 |

R1 : sur le compte B, un trade par jour, M2 s'il a un signal (il entre à 9:35), sinon BB.

Corrélations des nets entre départs : R1 A / B −0,32 ; option 2 A / C −0,43.

Net total moyen selon l'année de départ : R1 bat le plan dans 6 années sur 10 (pas 2016, 2020, 2021, 2025) ; l'option 2 bat R2 dans 9 années sur 10.

## Lecture

1. **À deux comptes, remplacer 3n par BB sur le compte B (R1) est mieux que le plan** : +392 $ par an (+11 %), meilleur 10e centile (+2 480 contre +2 075 $) et meilleur pire départ (+1 171 contre +803 $), grâce à une corrélation négative entre les comptes (−0,32). Le gain n'est pas systématique (4 années de départ sur 10 plus faibles).
2. **À trois comptes, garder 3n reste meilleur** : l'option 2 (A, B 3n + M2, C = BB) fait +4 971 $ contre +4 486 $ pour R2 (A, B = M2, C = BB). Malgré sa corrélation avec mom, 3n apporte environ +485 $ par an sur le compte B (avec M2, il comble les nuits et sert de premier trade du jour).
3. **BB ne remplace pas M2** : sans M2 (R3), on fait moins bien que le plan.
4. Choix pratique : **avec 2 comptes, R1 ; avec 3 comptes, l'option 2.**

## Réserves

Mêmes que les rapports précédents : chiffres historiques, BB en échantillon (version choisie parmi 72 réglages), exposition cumulée de même sens non limitée (règle FTMO floue), glissement sur les stops de BB, refus de reward et délais FTMO non modélisés.
