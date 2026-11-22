# FTMO : ajouter BB au plan retenu (compte A = mom + BB, ou troisième compte C = BB)

*2026-11-22. Demande de l'utilisateur. Script [run_ftmo_bb_options.py](../run_ftmo_bb_options.py) (branche `propfirm-ftmo`), **exploratoire, hors compteur** : simulation de contrat sur des trades existants. BB n'est pas validé hors échantillon (forward [PREREGISTRATION_32](../PREREGISTRATION_32.md), 1re lecture le 2028-02-29) ; tous ses chiffres viennent de 2016-2026, données déjà explorées. Le bot n'est pas modifié. Sorties : `results/ftmo_bb_options/` (`run.log`, `departs.csv`, `bb_trades.csv`).*

## Ce qui est simulé

- **Moteur** : celui du plan retenu ([run_ftmo_deux_comptes.py](../run_ftmo_deux_comptes.py)) : FTMO 1-Step 10k, objectif +10 %, perte max 10 %, perte du jour 3 % (règle relue le 2026-11-13 ; ce n'est pas 5 %), meilleur jour ≤ 50 %, reward après 10 jours de bourse, 90 % versés ; éval 2,5 % de risque, financé 1 %, objectif 2 R ramené au reste à faire en éval ; règle des annonces et politique « cible + attente » ; coût CFD 1,5 pt ; compte racheté après chaque échec (86,90 $).
- **BB** : version prop firm du n° 32 (VWAP exigé à l'entrée, stop suiveur gardé, SL 0,25 × ATR14, TP 2R, premier trade de la séance) : 1 545 trades, R brut moyen +0,140, MFE médian 0,75 R.
- **Plan actuel** : A = mom (nuit), B = 3n (nuit) + M2 EMA 9:30 (séance).
- **Option 1** : A = mom + BB. Si mom touche son SL ou son TP, pas de BB ; sinon (sortie à 9:30 ou pas de mom), BB avec une taille qui garde la journée entre −r et +2 r (même règle que le compte B). Mom sort au plus tard à 9:30, BB n'entre pas avant 10:00.
- **Option 2** : plan actuel + un compte C avec BB seul (mêmes réglages).
- **Anti-hedging** : pas de BB un jour où le M2 du compte B est de sens opposé (162 jours retirés sur 1 545). **Annonces** : en financé, pas de BB les jours de Fed.
- **Départs** : un tous les 5 jours de bourse de 2016-01 à 2025-08 (494 départs), 12 mois de trading chacun.

## Résultats (net sur 12 mois, en $, comptes 10k)

| | Total : moyenne / médiane / 10e centile | P(total < 0) | Pire creux de trésorerie | Compte A | Compte B | Compte C |
|---|---|---|---|---|---|---|
| **Plan actuel** | +3 502 / +3 331 / +2 075 | 0 % | −695 $ | +1 796 (4,1 évals, 6,3 rewards par an) | +1 705 (5,7 rewards) | — |
| **Option 1 : A = mom + BB** | **+3 749 / +3 539 / +2 267** | 0 % | −782 $ | **+2 044** (3,7 évals, 6,9 rewards) | +1 705 | — |
| **Option 2 : + compte C = BB** | **+4 971 / +4 930 / +3 485** | 0 % | −1 043 $ | +1 796 | +1 705 | **+1 469** (1,9 évals, 4,7 rewards) |

Net total moyen selon l'année de départ ($) :

| Année de départ | Plan actuel | Option 1 | Option 2 |
|---|---|---|---|
| 2016 | 3 284 | 3 027 | 3 771 |
| 2017 | 4 761 | 5 447 | 6 500 |
| 2018 | 2 353 | 2 694 | 4 077 |
| 2019 | 4 180 | 3 966 | 5 463 |
| 2020 | 3 536 | 3 729 | 5 049 |
| 2021 | 2 615 | 3 049 | 4 138 |
| 2022 | 2 932 | 3 350 | 4 815 |
| 2023 | 2 351 | 2 594 | 4 336 |
| 2024 | 4 320 | 4 655 | 6 025 |
| 2025 | 5 342 | 5 647 | 5 827 |

## Lecture

1. **Option 1 (A = mom + BB)** : +247 $ par an (+7 %), sans compte supplémentaire. Le compte A gagne +248 $ et rachète moins d'évals (3,7 contre 4,1 par an), parce que BB complète les journées où mom sort à 9:30. Mais le gain est faible et pas systématique : moins bon que le plan pour les départs de 2016 et 2019.
2. **Option 2 (compte C = BB)** : +1 469 $ par an (+42 %) pour une éval de plus au départ. Meilleure que le plan pour toutes les années de départ, et le compte C seul rapporte à peu près autant qu'un compte du plan (A +1 796, B +1 705). Le creux de trésorerie s'aggrave un peu (pire −1 043 $ contre −695 $), car il faut financer une éval de plus.
3. **Par emplacement de compte, BB vaut à peu près mom ou 3n + M2**, comme le montrait déjà la simulation à un seul compte. Le gain de l'option 2 vient surtout de la **diversification** : un compte de plus, sur une stratégie de séance, peu liée aux stratégies de nuit.

## Réserves

- **Les chiffres de BB sont en échantillon** (2016-2026, version choisie parmi 72 réglages), et les autres sont aussi des trades historiques : mom a été **validé hors échantillon** sur NQ 2011-2015 (n° 11 : +0,116 R par trade, p 0,0015 ; en fait « long NQ la nuit », tous les trades hors échantillon étaient longs ; échec sur ES et YM au n° 10), alors que 3n et M2 (EMA 9:30) ont échoué hors échantillon (n° 24, 25) *(corrigé le 2026-11-22 : une version antérieure de ce rapport disait à tort que mom avait échoué)*. Aucune n'a encore été confirmée sur des données postérieures au 2026-08-28 (holdout n° 26).
- **FTMO** : l'exposition cumulée sur des comptes liés (deux comptes longs NQ au même moment) attend toujours la réponse du support ; l'option 2 l'augmente.
- Glissement sur les stops serrés de BB, refus de reward et délais FTMO non modélisés ; anti-hedging appliqué contre le M2 de B mais pas contre d'éventuels trades manuels.
