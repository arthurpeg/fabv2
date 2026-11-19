# FTMO 1-Step : plan à trois stratégies (3n, sinon mom r/2 + M2 r/2)

*2026-11-04. **Exploratoire, hors compteur** : évaluation d'un contrat sur des trades existants. Script : [run_propfirm_trio.py](../run_propfirm_trio.py). Sorties : `results/propfirm_trio/` (`run.log`, `jours.csv`, `ftmo.csv`). 20 000 comptes par ligne, graine 1827.*

## Plan journalier (demande de l'utilisateur)

Une journée FTMO va de minuit à minuit, heure de Paris : elle contient la nuit qui commence à 20:00 ET la veille, puis la matinée et la séance US du jour.

- **S'il y a un signal 3n** pour la nuit qui se termine le matin : 3n seul, à **plein risque r** (20:05 → 03:00, stop 2 ATR, objectif 4 ATR M15 = 2 R). Ni mom ni M2 ce jour-là.
- **Sinon** : mom à **r/2** (20:00 → 9:30, SL 2 / TP 4 ATR M15), puis **M2 à r/2** s'il y a un setup (9:35 → 15:55, SL 4 / TP 8 ATR M15). Deux pertes pleines font r = 2,5 %, sous la perte du jour FTMO de 3 %.
- **r = 2,5 % en éval, 1 % en financé.** Le même plan est appliqué aux deux phases.

**Moteur.** C'est celui du n° 18, recopié pour accepter deux trades par jour. Le risque de chaque trade vaut le poids × min(r, marge restante jusqu'au plancher). On vérifie le plancher et la perte du jour après chaque trade. La règle du meilleur jour et les rewards (tous les 10 jours tradés) portent sur le P&L de la journée. Le coût CFD est de 1,5 point par trade, au niveau actuel du NQ. Pour comparer à durée égale, les autres plans sont recalculés avec ce même moteur. Il arrête un compte financé à 1 000 jours (le moteur précédent s'arrêtait à 500), ce qui explique pourquoi « 3n + M2 » fait ici +2 618 $ contre +2 123 $ dans [[reports/propfirm_combo_report]].

## Résultats

| Période | Plan | Journées / an | Composition des journées | Passage | Valeur du financé | Vie | **EV 10k** | **EV 100k** | **EV / mois d'emplacement 100k** |
|---|---|---|---|---|---|---|---|---|---|
| **2016-2026** | **Trio** | 255 | 3n 43 %, mom seul 34 %, mom + M2 22 % | 59,8 % | 35,2 % | 21 mois | **+2 020 $** | **+20 519 $** | **+1 478 $** |
| | Trio, sans edge | 255 | idem | 25,6 % | 3,1 % | 6 mois | −6 $ | +256 $ | +97 $ |
| | 3n + M2 (1 / jour, plein risque) | 168 | 3n 65 %, M2 35 % | 60,0 % | 45,0 % | 29 mois | +2 618 $ | +26 500 $ | +1 446 $ |
| | mom seul (plein risque) | 251 | mom 100 % | 43,9 % | 16,2 % | 6 mois | +625 $ | +6 572 $ | **+1 989 $** |
| **2011-2015** | **Trio** | 252 | mom seul 42 %, 3n 39 %, mom + M2 18 % | 70,8 % | 48,7 % | 28 mois | **+3 362 $** | **+33 942 $** | **+1 616 $** |
| | Trio, sans edge | 252 | idem | 27,0 % | 2,1 % | 7 mois | −29 $ | +27 $ | +9 $ |
| | 3n + M2 (1 / jour) | 147 | 3n 67 %, M2 33 % | 54,8 % | 17,6 % | 15 mois | +879 $ | +9 113 $ | +948 $ |
| | mom seul | 248 | mom 100 % | 55,9 % | 33,5 % | 9 mois | +1 786 $ | +18 185 $ | **+3 397 $** |

L'éval dure entre 0,4 mois (mom seul) et 1,2 mois. 96-97 % des comptes financés du trio touchent au moins un reward, avec 9,6 rewards en moyenne sur 2016-2026 et 13,5 sur 2011-2015.

## Lecture

1. **Par tentative, le trio est entre les deux** sur 2016-2026 (+2 020 $ contre +2 618 $ pour 3n + M2 et +625 $ pour mom). Sur 2011-2015, c'est le meilleur plan (+3 362 $). C'est la seule période où aucune des trois règles n'a été choisie, mais mom y est forte (hors échantillon du n° 11) et 3n et M2 y sont faibles.
2. **Par mois d'emplacement, mom seul reste devant sur les deux périodes** (+1 989 $ et +3 397 $, contre +1 478 $ et +1 616 $ pour le trio). Le trio remplace les nuits mom les plus rentables par 3n. Sur 2016-2024, mom faisait +7,5 bps les nuits « 3n long » contre −0,8 bps les autres ([[reports/nq_nuit_3n_vs_mom_report]]). Le trio garde donc surtout les nuits faibles de mom, à demi-risque. Dans la ligne sans edge, le R moyen de mom sur les nuits restantes est négatif, ce qui donne −0,014 R par jour au lieu de 0.
3. **Le trio a une meilleure stabilité.** Il passe l'éval plus souvent (60 à 71 %), le compte financé vit 3 à 4 fois plus longtemps que pour mom seul (21 à 28 mois contre 6 à 9), et la pire journée reste bornée à 2,5 %.
4. **Le choix dépend de la contrainte.**
   - Si l'on veut **maximiser le gain par compte acheté**, avec peu d'évals, des refus de rewards possibles ou un account rolling à éviter, il faut prendre **le trio ou 3n + M2**.
   - Si l'on veut **maximiser le gain par mois** d'un emplacement qu'on rachète dès qu'il saute, il faut prendre **mom seul**. Mais mom seul enchaîne beaucoup d'évals : environ 20 par an sur un emplacement.
5. **Réserves :**
   - La **règle FTMO des annonces** n'est pas modélisée. mom traverse les annonces de 8:30 (NFP, CPI) jusqu'à 9:30, et M2 celles de 10:00 et de 14:00. Les chiffres de mom et du trio sont donc trop optimistes, d'environ 10 % pour mom (voir [[wiki/experiments/propfirm-ftmo-option]]). 3n n'est pas concerné.
   - 3n et M2 ont échoué hors échantillon (n° 24 et 25). Leurs lignes 2016-2026 sont dans leur période de sélection.
   - Rewards supposés versés sans refus, spread CFD non mesuré.

> **Correction du 2026-11-04** : en éval, l'objectif de chaque trade est désormais ramené au reste à faire. Les chiffres ci-dessus sont ceux de l'objectif fixe ; les chiffres corrigés sont dans [[reports/propfirm_correction_reste_report]] (passage +1 à +7 points, mêmes classements).
