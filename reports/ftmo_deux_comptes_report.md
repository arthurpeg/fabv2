# Deux comptes FTMO 1-Step 10k en même temps : A = mom, B = 3n + M2

*2026-11-04. **Exploratoire, hors compteur.** Script : [run_ftmo_deux_comptes.py](../run_ftmo_deux_comptes.py). Sorties : `results/ftmo_deux_comptes/` (`run.log`, `departs.csv`).*

## Règles (demande de l'utilisateur)

- **Compte A** : mom chaque nuit (20:00 → 9:30, SL 2 ATR, TP 4 ATR M15 = 2 R).
- **Compte B** : 3n la nuit s'il y a un signal (20:05 → 03:00, SL 2 ATR, TP 4 ATR = 2 R).
  - Si 3n sort au **stop ou au TP**, on ne prend **pas** M2 ce jour-là.
  - Si 3n sort à **03:00** (ni stop ni TP), ou s'il n'y a pas de 3n, on prend M2 (9:35 → 15:55, SL 4 ATR, TP 8 ATR = 2 R). Sa taille vaut ρ = min(r + x, (2r − x)/2), où x est le résultat de la nuit : la journée reste ainsi entre −r et +2r (−2,5 % et +5 % en éval).
- **Risque** : r = 2,5 % en éval, 1 % en financé. En éval, l'objectif est ramené au reste à faire (MFE de chaque trade).
- **Règles FTMO actuelles** : perte max 10 % sous le plus haut, remise à zéro après un reward ; perte du jour 3 % ; meilleur jour ≤ 50 % du gain net. Reward possible dès le 14e jour après le premier trade (10 jours de bourse dans la simulation, jours calendaires dans le rejeu de septembre), demandé dès qu'il est permis ; 90 % versés ; nouveau compte gratuit ensuite.
- **Rachat** : une éval ratée ou un compte perdu est rachetée le lendemain à 79 €, soit 86,90 $.
- **Coût CFD** : 1,5 point par trade.

## 1. Douze mois de trading, pour chaque départ possible (un tous les 5 jours de bourse, 2011-07 → 2025-08, 721 départs)

| Sur 12 mois | Compte A (mom) | Compte B (3n + M2) | **Les deux** |
|---|---|---|---|
| Net moyen (rewards − frais) | +2 469 $ | +1 591 $ | **+4 060 $** |
| Médiane | +2 333 $ | +1 533 $ | **+3 856 $** |
| 10e centile / 90e centile | +968 / +4 135 $ | +488 / +2 833 $ | **+2 096 / +6 197 $** |
| Départs perdants à 12 mois | 0 % | 0 % | **0 %** |
| Évals achetées par an | 3,9 | 2,1 | 6,0 (≈ 520 $) |
| Rewards par an | 6,3 | 4,1 | 10,4 |
| Pire creux de trésorerie (frais avancés avant les rewards) | −695 $ | −521 $ | **−782 $** (médiane −261 $) |

La corrélation des résultats A et B d'un départ à l'autre est de **+0,13** : les deux comptes ont rarement une mauvaise année ensemble.

Net moyen sur 12 mois selon l'année de départ :

| Départ | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 3 884 | 3 067 | 4 547 | 3 368 | 1 852 | 2 431 | 3 069 | 992 | 2 759 | 1 911 | 1 181 | 2 037 | 1 219 | 2 588 | 3 199 |
| B | 1 604 | 711 | 1 560 | 1 163 | 1 189 | 648 | 1 926 | 1 511 | 2 652 | 1 992 | 1 546 | 999 | 1 016 | 2 975 | 2 777 |
| **Total** | 5 488 | 3 778 | 6 107 | 4 531 | 3 041 | 3 079 | 4 995 | 2 503 | 5 412 | 3 902 | 2 727 | 3 036 | 2 235 | 5 563 | 5 975 |

## 2. Départ réel le 01/09/2026 (jusqu'au 03/11)

| Compte | Ce qui se passe | Net au 03/11 |
|---|---|---|
| A (mom) | éval validée le 14/09 ; compte financé perdu le 03/11 (−6,22 %), aucun reward ; 2e éval achetée | **−174 $** |
| B (3n + M2) | éval validée le **09/09** ; reward de **490 $ le 15/10**, puis reward de **368 $ le 29/10** ; compte n° 3 à −2,71 % le 03/11 | **+771 $** |
| **Total** | | **+598 $** |

## Lecture

1. **Les deux comptes ensemble lissent bien les résultats.** Ils sont peu corrélés : mom traverse la nuit jusqu'à 9:30 sur toutes les séances, alors que B est surtout tradé les nuits 3n et les jours M2. Sur l'historique, aucun départ ne perd d'argent sur 12 mois, et le 10e centile est à +2 100 $ pour les deux comptes.
2. **En septembre-octobre 2026, c'est B qui a compensé A** : deux rewards en octobre, alors que mom perdait −5,5 R sur le mois.
3. **Les frais à avancer restent faibles** : au pire 782 $ sur une année, avant que les rewards ne les couvrent.
4. **Réserves** :
   - **Les chiffres historiques sont optimistes.** 3n et M2 ont été choisis par leurs auteurs sur 2013-2024 et ont échoué hors échantillon (n° 24 et 25). Ici, la prime de nuit et le coût CFD actuel (0,02 R par trade, au lieu de 0,1 R au prix de 2010-2015) les rendent rentables même sur 2011-2015.
   - **La règle FTMO des annonces n'est pas modélisée** : mom traverse 8:30, M2 traverse 10:00 et 14:00.
   - Le compte financé démarre le lendemain de la validation ou du reward, alors que FTMO met 1 à 4 jours ouvrés.
   - Le refus de rewards et l'« account rolling » ne sont pas modélisés. Avec deux comptes sur des stratégies différentes, ce risque est faible.

## Ajout : règle des annonces et politique « cible + attente » (2026-11-04)

**Règle des annonces** ([build_news_trades.py](../build_news_trades.py) → `cache/propfirm/news_trades.parquet`). Sur le compte financé, FTMO n'exécute aucun ordre, stop ou objectif compris, 2 min avant et après une annonce restreinte. Pour l'US100, ce sont NFP, CPI, PIB avancé (8:30) et décision ou minutes de la Fed (14:00).
- mom est fermé à **8:19** les jours d'annonce de 8:30 (168 nuits coupées sur 2011-2026) ; M2 est fermé à **13:55** les jours de Fed (86 séances) ; 3n n'est pas concerné.
- Les dates de septembre-octobre 2026 sont relevées sur le BLS et sur federalreserve.gov : NFP 04/09 et 02/10, CPI 11/09 et 14/10, Fed 16/09 et 28/10, minutes 07/10. Le PIB avancé du 3e trimestre est **supposé** le 29/10 (date non trouvée sur bea.gov).

**Politique cible + attente** (voir [[reports/ftmo_payout_policy_report]]) : en financé, si seule la règle des 50 % bloque, le trade vise juste ce qui manque. Dès que la règle est respectée, on ne trade plus jusqu'à la date du reward.

**Correction du moteur.** L'horloge du reward compte maintenant chaque jour de bourse, tradé ou non. Avant, seuls les jours tradés comptaient : un compte en attente restait bloqué, et un compte B sans signal attendait plus que 14 jours calendaires. Les chiffres « sans règle des annonces » du haut de ce rapport ont donc légèrement bougé (total +4 082 $ au lieu de +4 060 $).

| 12 mois, 721 départs (2011-07 → 2025-08) | Sans règle des annonces | Règle des annonces | **Règle des annonces + cible + attente** |
|---|---|---|---|
| Net A (mom), moyenne | +2 472 $ | +2 213 $ | +2 232 $ |
| Net B (3n + M2), moyenne | +1 610 $ | +1 630 $ | +1 632 $ |
| **Net total, moyenne / médiane** | +4 082 / +3 903 $ | +3 843 / +3 714 $ | **+3 864 / +3 791 $** |
| 10e centile total | +2 097 $ | +2 108 $ | **+2 473 $** |
| 90e centile total | +6 237 $ | +5 741 $ | +5 525 $ |
| Départs perdants à 12 mois | 0 % | 0 % | 0 % |
| Rewards par an (A / B) | 6,3 / 4,2 | 5,9 / 4,3 | **7,5 / 5,4** |
| Évals par an (A / B) | 4,0 / 2,1 | 4,1 / 2,0 | 3,8 / 2,0 |
| Pire creux de frais | −782 $ | −782 $ | −695 $ |

Moyenne selon l'année de départ, règle des annonces avec ou sans cible + attente : 2011-2015 +4 354 → +4 404 $, 2016-2025 +3 609 → +3 615 $.

**Départ réel le 01/09/2026 (jusqu'au 03/11)** :

| | Sans règle des annonces | Règle des annonces | **Règle des annonces + cible + attente** |
|---|---|---|---|
| A (mom) | 0 reward, financé perdu le 03/11 → −174 $ | 0 reward ; le financé **survit** (−5,23 % au 03/11) grâce à la sortie à 8:19 du 14/10 (+0,71 R au lieu d'un stop avec gap à −1,68 R) → −87 $ | **reward de 353 $ le 28/09** ; nouveau compte à −7,95 % au 03/11 → **+266 $** |
| B (3n + M2) | rewards de 490 $ (15/10) et 368 $ (29/10) → +771 $ | identique → +771 $ | rewards de **210 $ (28/09)** et **352 $ (20/10)** ; compte à −1,56 % au 03/11 → +474 $ |
| **Total** | +598 $ | +685 $ | **+740 $** |

**Lecture.**
1. **La règle des annonces coûte environ 6 % sur un an** (−239 $ en moyenne), et tout vient de mom : les nuits d'annonce sont les meilleures de la règle (n° 14). B n'est presque pas touché, car M2 n'est coupé qu'environ 6 jours de Fed par an. En septembre-octobre 2026, la règle a même aidé A : la coupe à 8:19 du 14/10 a évité un stop avec gap.
2. **Cible + attente ne change pas le gain moyen sur un an** (+3 864 $ contre +3 843 $), mais **rend les rentrées plus régulières**. Il y a 12,9 rewards par an au lieu de 10,2, et le 10e centile monte de +2 108 à **+2 473 $**. En contrepartie, le 90e centile baisse : on renonce aux plus gros rewards. Sur septembre-octobre 2026, cette politique est la meilleure (+740 $).
3. **Version recommandée pour les deux comptes : règle des annonces respectée + cible + attente.** Elle donne environ +3 800 $ par an attendus pour deux comptes 10k et environ 6 évals par an. Aucun départ historique ne perd sur 12 mois, et il faut avancer au plus environ 700 $ de frais. Les réserves du haut de ce rapport restent valables (3n et M2 optimistes ; délais de FTMO non modélisés).

