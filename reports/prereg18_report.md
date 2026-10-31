# Rapport n° 18 : espérance d'une éval FTMO 1-Step avec des trades au hasard

*2026-10-31. Protocole : [[PREREGISTRATION_18]]. Code : [run_propfirm_ftmo.py](../run_propfirm_ftmo.py), [propfirm/](../propfirm/). Sorties : `results/propfirm/` (run.log, eval.csv, funded.csv, ev.csv). Compteur d'essais inchangé (1 482) : on évalue un contrat, pas une règle de marché.*

## Avenant D : la règle NQ de nuit sur LucidFlex 50K (MNQ)

Code : [run_propfirm_lucid.py](../run_propfirm_lucid.py), [propfirm/lucid.py](../propfirm/lucid.py). Sorties : `results/propfirm_lucid/`. Règles relevées le 31 octobre sur lucidtrading.com et support.lucidtrading.com (voir l'avenant D). Mêmes 3 787 trades qu'à l'avenant C, exécutés en MNQ ; coût réel par MNQ ≈ 2,00 $ (demi-spreads bbo-1m + 1,50 $ de commission supposée).

**Écart au protocole.** Le protocole convertit le stop en points avec le prix historique. Sur un premier passage de 1 000 comptes, cela donne un stop médian de 21 points (42 $ par MNQ ; 7 points et 14 $ en 2011-2015), où la commission pèse 5 à 14 % du risque. Au niveau actuel du NQ (25 684), le même stop vaut ~65 points (131 $ par MNQ) et le coût 1,7 % du risque. Les deux sont rapportés ; **la version « prix actuels » est celle qui décrit un compte ouvert aujourd'hui** (même convention que le spread FTMO aux avenants B et C).

| Éval 400 $ de risque, financé 200 $, consistance 40 %, 115 $ | Passage | Séances par tentative | Valeur du financé | **EV par éval** | Refus tolérés |
|---|---|---|---|---|---|
| **Règle, prix actuels** | **39,5 %** | 26 | **690 $** (P(payout) 76 %, 1,2 payout, vie ~70 séances) | **+157 $ ± 6** | 58 % |
| Règle, prix historiques (résultat principal du protocole) | 29,8 % | 30 | 603 $ | +65 $ ± 5 | 36 % |
| Sans edge, prix actuels | 18,2 % | 22 | 330 $ | −55 $ | — |
| Sans edge, prix historiques | 13,1 % | 24 | 261 $ | −81 $ | — |
| Règle 2011-2015 seulement (prix historiques) | 30,7 % | 19 | 671 $ | +91 $ | 44 % |
| Consistance 50 % (130 $ supposés), prix actuels | 39,2 % | 26 | 690 $ | +140 $ | 52 % |

Meilleur de la grille (sélectionné, donc optimiste), prix actuels : éval 200 $ / financé 800 $ → passage 50,5 %, financé 1 039 $, **EV +410 $**, mais l'éval prend ~125 séances (~6 mois) à 200 $ de risque.

Lecture :
- **Lucid rapporte beaucoup moins que FTMO avec la même règle** : +157 $ par éval 50K contre +853 $ par éval FTMO 10k (prix comparables, 115 $ contre 87 $). Trois raisons : l'objectif (3 000 $) dépasse la perte max (2 000 $), alors que FTMO les égalise (10 % / 10 %) ; la consistance de 40 % bloque les gros jours (un TP à 2,5 R pèse lourd) ; surtout, **le financé Lucid meurt vite** : chaque payout ne rend que 50 % du profit (plafond 2 000 $) et ramène le plancher à +100 $, donc le coussin restant est mince, alors que FTMO remet la perte max à −10 % après chaque reward.
- **Sans edge, Lucid est négatif avec cette façon de trader** (−55 $ par éval), contrairement à FTMO (+98 $). Une règle à objectif fixe (2,5 R) ne s'adapte pas aux barrières du contrat ; la session précédente obtenait ~+58 $ sans edge chez Lucid grâce à un sizing taillé pour la marge (gros paris puis reliquat), pas avec une règle de marché.
- **L'edge fait toute la valeur ici** : de −55 $ à +157 $ par éval (prix actuels). Le passage en réel (5 payouts) n'arrive que dans 1 à 5 % des comptes, il n'est pas valorisé.
- Hypothèses : commission MNQ 1,50 $ (non publiée), prix de l'option 50 % (non lu), DLL de 1 200 $ jamais atteinte avec un trade par nuit (non simulée).

## Avenant C : la règle NQ de nuit sur FTMO 1-Step

Code : [run_propfirm_nq_nuit.py](../run_propfirm_nq_nuit.py). Sorties : `results/propfirm_nq_nuit/`. Trades : les 3 787 de [[reports/couts_reels_nq_nuit_report]] (compte 20:00 ET, momentum 12-1, SL 2 ATR / TP 5 ATR, sortie 9:30 ET ; 2011-07 → 2026-08), R brut moyen +0,125. Stop médian 0,254 % du prix : 1,5 point coûte 0,023 R par trade, 3 points 0,046 R. Un trade par nuit, du dimanche au jeudi, rien le week-end, pas de swap. Deux trades sans distance de stop (R = 0, 2014-05-28 et 2016-12-15) reçoivent le stop médian (seul leur coût en dépend).

**Résultat principal** (éval 2 % de risque par trade, financé 1 %, 1,5 point, remise à zéro de la perte max) :

| | Passage | Trades par éval | Valeur du financé | **EV 10k** | **EV 100k** | Refus tolérés (10k / 100k) |
|---|---|---|---|---|---|---|
| **Règle 2011-2026** | **50,8 % ± 0,7** | 13,5 | **18,5 %** (P(reward) 80 %, 3,4 rewards, vie ~120 trades) | **+853 $ ± 21** | **+8 849 $ ± 207** | 91 % / 94 % |
| Même chose à 3 points | 47,3 % | 13,8 | 15,3 % | +638 $ | +6 700 $ | 88 % / 92 % |
| Sans RAZ de la perte max | 50,8 % | 13,5 | 7,75 % | +307 $ | +3 390 $ | 78 % / 86 % |
| **Contrôle sans edge** (R − moyenne) | 34,5 % | 12,9 | 5,3 % | +98 $ | +1 295 $ | 53 % / 70 % |
| Règle 2011-2015 seulement (hors échantillon) | 60,7 % | 13,6 | 34,8 % | +2 023 $ | +20 551 $ | 96 % / 97 % |

Lecture :
- **L'edge multiplie l'EV par ~9** par rapport au même flux de trades sans edge (+853 $ contre +98 $ sur 10k) : le passage monte de 35 à 51 %, et surtout le compte financé vaut 3,5 fois plus (18,5 % contre 5,3 % du capital), parce qu'il encaisse ~0,12 R net par nuit pendant des mois.
- **Moins de risque, plus d'EV** : à 0,5 % de risque, le passage monte à 81 % et l'EV à +1 580 $ (10k) / +16 121 $ (100k), mais l'éval prend ~160 nuits (~8 mois) et le financé tourne jusqu'au plafond de 500 nuits (sélectionné dans la grille, donc optimiste ; valeur non actualisée). À 2 %, l'éval se décide en ~13 nuits.
- **La remise à zéro de la perte max pèse encore plus qu'avec des trades au hasard** (18,5 % → 7,75 %) : avec une edge, le compte monte, et sans remise à zéro chaque reward retiré rapproche le solde du plancher. **Vérifié le 31 octobre : sur le 1-Step, la remise à zéro est la règle** (voir « Règles FTMO vérifiées »), la ligne « sans RAZ » ne sert que de borne basse.
- **Biais** : 2016-2026 a servi à choisir la règle ; les chiffres complets sont donc optimistes. La période 2011-2015 (hors échantillon, n° 11) donne encore plus, mais c'est un marché haussier où la règle était longue à 100 %. Le DD historique de la règle (−26 R) dépasse 10 % du capital dès 0,4 % de risque par trade : une année comme 2022 tue le compte, ce que la simulation compte déjà.
- **Non modélisé** : spread de nuit réel du CFD FTMO (variante 3 points seulement), écart entre le CFD et le future à 20:00 et 9:30, et le risque de refus (bien moins probable ici : la règle est documentée et testée, ce n'est pas du pile ou face).

## Avenant E : financé FTMO en RR 2 (1 % risqué, 2 % visés)

Code : [build_nq_nuit_tp.py](../build_nq_nuit_tp.py) (trades TP 4 ATR ; contrôle TP 5 identique à 4e-16), [run_propfirm_rr2.py](../run_propfirm_rr2.py), séries : `run_propfirm_streaks.py 4`. Sorties : `results/propfirm_rr2/`, `results/propfirm_streaks_tp4/`. Éval inchangée (TP 5 ATR, 2 %) ; financé : SL 2 ATR, TP 4 ATR = 2 R, 1 % de risque ; spread 1,5 point ; RAZ de la perte max.

| Métrique (20 000 comptes) | **Financé RR 2** | Financé RR 2,5 (avenant C) | RR 2, spread 3 pt | RR 2 sans edge | RR 2, 2011-2015 |
|---|---|---|---|---|---|
| Passage de l'éval | 51,6 % | 51,6 % | 47,8 % | 34,6 % | 60,9 % |
| Nuits par tentative (si validée) | 13,3 (12,4) | 13,5 (12,7) | 13,8 (12,9) | 12,8 | 13,5 |
| **Valeur du financé** (% du capital) | **21,2 %** | 18,8 % | 16,7 % | 6,9 % | 33,3 % |
| P(≥ 1 reward) | **86 %** | 80 % | 82 % | 63 % | 90 % |
| Rewards par compte | 4,84 | 3,45 | 3,92 | 1,71 | 7,48 |
| Reward moyen | 4,39 % | 5,45 % | 4,26 % | 4,06 % | 4,45 % |
| Premier reward (médiane) | 17 nuits | 18 | 17 | 17 | 15 |
| Vie du compte (moy. / méd.) | 148 / 112 nuits | 121 / 84 | 134 / 101 | 89 / 57 | 178 / 124 |
| Gain par nuit de compte financé | 14,3 pb | 15,6 pb | 12,5 pb | 7,8 pb | 18,7 pb |
| **EV 10k** (refus tolérés) | **+1 009 $ ± 21** (92 %) | +883 $ (91 %) | +711 $ (89 %) | +153 $ (64 %) | +1 944 $ |
| **EV 100k** (refus tolérés) | **+10 408 $ ± 212** (95 %) | +9 152 $ (94 %) | +7 428 $ (93 %) | +1 855 $ (77 %) | +19 762 $ |

Le RR 2 en financé rapporte **+14 %** par rapport au RR 2,5 (+1 009 $ contre +883 $ sur 10k, même graine pour l'éval) : rewards un peu plus petits (4,4 % contre 5,5 %) mais plus nombreux (4,8 contre 3,5) et le compte vit plus longtemps. Un TP ne fait plus que +2 % en une nuit, donc la règle du meilleur jour exige +4 % (au lieu de +5 %) avant un reward. Par nuit de compte vivant, le RR 2,5 reste un peu plus rapide (15,6 pb contre 14,3).

**Pires séries sur l'historique réel** (657 départs, même méthode que l'exploratoire « pires séries ») :

| | Financé RR 2 | Financé RR 2,5 |
|---|---|---|
| Pire série d'évals ratées | **6** (2023-08-04 → 2023-11-07 ; 521 $ sur 10k, 3 293 $ sur 100k) | 6 (mêmes dates) |
| **Plus longue période sans reward** | **239 nuits ≈ 11 mois** (2022-01-11 → 2022-12-22) | 223 nuits (2018-03 → 2019-01) |
| Pire creux de trésorerie | −608 $ (10k) / −3 842 $ (100k) | idem |
| Plus longue durée sous le pic de trésorerie (pire) | 239 nuits | 223 nuits |
| Par départ (médiane) | 28 évals, 40 rewards, +16 100 $ (10k) | 36 évals, 37 rewards, +17 100 $ |

Trace qui démarre le 2011-07-01 (40 évals, 20 validées, 97 rewards) : sans reward 2023-05-18 → 2024-02-23 (192 nuits ; 5 évals dont 4 ratées), 2021-10-26 → 2022-07-05 (172), 2018-04-13 → 2018-11-13 (149), 2020-02 → 2020-09 (142) ; rewards par an de 2 (2022) à 11 (2012, 2014, 2017). Le RR 2 raccourcit l'épisode 2018 (de 200 à 149 nuits) mais pas 2022, la pire année de la règle (marché baissier). Le gain net médian par départ est un peu plus bas (16 100 $ contre 17 100 $) alors que l'EV Monte-Carlo est plus haute : sur l'unique historique, un emplacement reste plus longtemps sur chaque financé et achète moins d'évals ; les deux mesures ne répondent pas à la même question.

### Avenant E refait avec vectorbt

Code : [run_propfirm_vbt.py](../run_propfirm_vbt.py), sorties `results/propfirm_vbt/`. vectorbt n'a pas de règles de prop firm. Il calcule le marché : `Portfolio.from_signals` sur les 5 498 560 barres 1 minute du NQ, une position par nuit (entrée 20:00 ET, sortie 9:30 ET, `sl_stop` 2 ATR, `tp_stop` 5 ou 4 ATR), le spread de 1,5 point compté en frais, moitié à l'entrée et moitié à la sortie. Les règles FTMO tournent en Python sur les rendements nets que vectorbt rend pour chaque nuit. Les trades du moteur maison venaient déjà de vectorbt (`run_recolte1_atr.simulate`), mais avec un coût forfaitaire ajouté après coup ; ici, le coût est payé dans vectorbt.

| Contrôle | Résultat |
|---|---|
| Trades calculés par vectorbt | 3 787 nuits sur 3 787, pour TP 5 comme pour TP 4 ; R brut moyen +0,1253 (TP 5) et +0,1261 (TP 4) |
| Écart de R avec le moteur maison | au plus 7,4e-5 R par trade (le spread est payé sur le prix de sortie dans vectorbt) |
| vectorbt rejoue la trace avec les vraies tailles en $ | 3 708 trades sur 3 708, P&L identique à l'étape précédente à 3e-11 $ près ; 42 565,23 $ au total |
| Trace historique depuis 2011-07-01 | 40 évals, 20 validées, 97 rewards (43 506 $ reçus sur 10k), comme le moteur maison, **sauf un événement** : une éval de novembre 2023 a 0,0502 % de marge avec vectorbt et 0,0499 % avec le moteur maison ; elle continue avec un risque minuscule et rate le 2023-11-07 au lieu du 2023-11-01 |

Les résultats avec vectorbt :

| | vectorbt | moteur maison |
|---|---|---|
| Monte-Carlo (20 000 comptes, même graine) | passage 51,6 %, financé 21,24 %, P(≥ 1 reward) 86 %, 4,84 rewards de 4,39 %, 1er reward à 17 nuits, vie 148 nuits ; **EV +1 009 $ ± 21 (10k), +10 408 $ ± 212 (100k)** | identique à l'affichage |
| Pire série d'évals ratées | **6** (2023-08-04 → 2023-11-07), 521 $ sur 10k | 6 (2023-08-04 → 2023-11-01) |
| Plus longue période sans reward | **239 nuits ≈ 11,4 mois** (2022-01-11 → 2022-12-22) ; médiane 192 | 239 nuits, mêmes dates ; médiane 172 |
| Pire creux de trésorerie | −608 $ (10k) | −608 $ |
| Par départ (médianes) | 28 évals, 40 rewards, +16 081 $ | 28 évals, 41 rewards, +16 375 $ |

**Correction faite pendant ce contrôle** : les scripts de trace (`run_propfirm_streaks.py` et celui-ci) n'abandonnaient pas une éval sous 0,05 % de marge, alors que le moteur Monte-Carlo le fait, et comparaient les seuils sans tolérance ; des écarts d'un centime faisaient bifurquer la trace. Les deux appliquent maintenant la marge minimale de 0,05 % et une tolérance de 0,001 % du capital sur chaque seuil. Relancés, ils redonnent les mêmes pires valeurs qu'avant (6 évals ratées ; 223 nuits sans reward en TP 5, 239 en TP 4 ; −608 $). Seules changent la fin de la série d'échecs (2023-11-01 au lieu du 2023-11-07) et la médiane sans reward en TP 4 (172 nuits au lieu de 192).

## Exploratoire (non pré-enregistré) : pires séries sans validation et sans reward, FTMO + règle de nuit

Code : [run_propfirm_streaks.py](../run_propfirm_streaks.py), sorties `results/propfirm_streaks/` (starts_10k.csv, starts_100k.csv, events_2011.csv). Réglage de l'avenant C (éval 2 %, financé 1 %, 1,5 point), un seul emplacement qui rachète une éval dès qu'un compte saute, suivi sur l'historique réel sans bouclage depuis 657 nuits de départ (2011-07 → 2024-08).

**Les départs convergent** : quel que soit le jour de départ, l'emplacement finit sur le même enchaînement de comptes (même trade chaque nuit, mêmes barrières), donc la médiane et le 95e centile sont presque identiques. Ce sont les épisodes **datés** de l'unique historique qui comptent, et l'avenir peut faire pire.

| | 10k (éval 87 $) | 100k (éval 549 $) |
|---|---|---|
| Pire série d'évals ratées d'affilée | **6** (4 dans la trace 2011 ; 2023-08 → 2023-11, ~3 mois) | 6 |
| Frais perdus dans cette série | 521 $ | 3 293 $ |
| **Plus longue période sans reward** | **223 nuits ≈ 11 mois** (2018-03 → 2019-01-30) | idem |
| Pire creux de trésorerie (frais payés depuis le dernier pic) | −608 $ | −3 842 $ |
| Plus longue durée sous le pic de trésorerie | 223 nuits (~11 mois) | idem |
| Par départ (médiane) | 36 évals, 37 rewards, gain net +17 100 $ | +182 600 $ |

Épisodes distincts (trace qui démarre le 2011-07-01 ; 52 évals, 29 validées, 82 rewards) :

| Sans reward | Durée | Évals achetées / ratées |
|---|---|---|
| 2018-04-13 → 2019-01-30 | 200 nuits (~9,5 mois) | 2 / 0 |
| 2015-08-10 → 2016-04-05 | 163 nuits (~7,8 mois) | 1 / 0 |
| 2020-02-14 → 2020-10-09 | 159 nuits (~7,6 mois) | 1 / 0 |
| 2021-11-22 → 2022-07-12 | 158 nuits (~7,5 mois) | 3 / 1 |
| 2019-01-30 → 2019-08-27 | 144 nuits (~6,9 mois) | 2 / 1 |

Séries d'évals ratées : 4 (2025-04-02 → 2025-06-03), 4 (2023-09-21 → 2023-11-07), 3 (2019-10 → 2019-11), puis des séries de 2.

**Ce qui fait les longues attentes, ce ne sont pas les évals ratées** (frais faibles : quelques centaines de dollars sur 10k), **mais les comptes financés qui ne paient pas** : en 2018, un financé validé le 2018-06-05 saute le 2018-08-13 sans reward, le suivant met cinq mois à verser le premier (2019-01-30). La cause est la règle du meilleur jour : un TP de la règle fait +2,5 % du capital en une nuit (1 % de risque × 2,5 R), donc un reward exige au moins +5 % de profit sur le cycle. Rewards par an dans la trace : de 2 (2022) à 9 (2012, 2014). Prévoir de la trésorerie pour ~6 évals ratées et un an sans rentrée.

## Exploratoire (non pré-enregistré) : plusieurs comptes décalés dans le temps

Question : avoir plusieurs comptes à des moments différents de leur vie, tous sur la règle NQ de nuit, lisse-t-il la variance ? Code : [run_propfirm_farm.py](../run_propfirm_farm.py), sorties `results/propfirm_farm/`. Comptes 10k, éval 2 %, financé 1 %, 1,5 point, 3 nuits de vérification ; chaque emplacement rachète une éval le lendemain de la perte d'un compte. 758 fenêtres de 2 ans (504 nuits) sur l'historique réel ; un emplacement « décalé de k mois » a démarré k mois avant la fenêtre.

| 5 emplacements | Gain net moyen par emplacement (2 ans) | Écart-type | 5e centile | Pire fenêtre | Mois sans aucun reward (médiane) |
|---|---|---|---|---|---|
| 1 seul (référence) | +4 877 $ | 1 985 $ | +2 247 $ | +1 211 $ | 67 % |
| Synchrones | +4 877 $ | 1 985 $ | +2 247 $ | +1 211 $ | 67 % |
| Décalés de 1 mois | +5 179 $ | 2 023 $ | +2 455 $ | +1 754 $ | 62 % |
| Décalés de 3 mois | +5 202 $ | 2 037 $ | +2 475 $ | +1 751 $ | 62 % |
| Indépendants (histoires de marché différentes, borne théorique) | +4 886 $ | 873 $ | +3 576 $ | +2 809 $ | 12 % |

**Décaler les comptes ne lisse presque rien** : l'écart-type par emplacement reste ~2 000 $, contre ~870 $ si les comptes étaient vraiment indépendants. Les comptes prennent les mêmes trades les mêmes nuits ; un mauvais passage de la règle les fait sauter ensemble, ils rachètent leur éval le même jour et se resynchronisent : en moyenne **4,1 emplacements sur 5 rachètent la même nuit**, et leurs flux trimestriels sont corrélés à **0,97**. Le décalage ne sert qu'au début (un peu plus de rewards répartis, pire fenêtre +1 750 $ au lieu de +1 210 $). Pour lisser vraiment, il faut des flux différents (autre actif, autre règle, autre horizon), pas des dates différentes. Résultats sur 2011-2026, optimistes pour la même raison qu'à l'avenant C (aucune fenêtre de 2 ans n'est perdante).

## Avenant B : entrée 9:50 ET, spread 1 à 1,5 point (trades au hasard)

Stop 1 ATR M15 lu sur la barre 9:30-9:45 : **0,144 % du prix en médiane** (plus large qu'à 9:30, car l'ATR inclut le premier quart d'heure), stop touché 83 % des jours. Spread exprimé au niveau actuel du NQ (25 684) : 1,5 point = 0,58 pb = **0,041 R par trade** ; 1 point = 0,027 R (contre 0,083 R pour l'avenant A).

Éval 2 % / 4,9 %, financé 1 % / 2 %, remise à zéro de la perte max :

| Spread | Compte | Passage | Valeur du financé | **EV par tentative** | Refus tolérés | Sans RAZ |
|---|---|---|---|---|---|---|
| **1,5 pt** | 10k | 41,1 % ± 0,7 | 6,04 % ± 0,11 | **+161 $ ± 6** | 65 % | +93 $ |
| **1,5 pt** | 100k | 41,1 % | 6,04 % | **+1 933 $ ± 61** | 78 % | +1 246 $ |
| 1 pt | 10k | 41,9 % | 6,53 % | +187 $ ± 7 | 68 % | +104 $ |
| 1 pt | 100k | 41,9 % | 6,53 % | +2 187 $ ± 68 | 80 % | +1 364 $ |

Éval ~8,5 jours par tentative (7,9 si validée). Financé (1,5 pt) : P(≥ 1 reward) 57 %, 1,29 reward en moyenne, premier vers le 14e jour de bourse, vie ~52 jours. Meilleur de la grille (éval 1 / 4,9, financé 0,5 / 2 ; sélectionné, donc optimiste) : +206 $ / +2 376 $ à 1,5 pt.

Lecture : en attendant 9:50 et avec un spread de 1-1,5 point, le stop ATR retrouve à peu près l'espérance du stop à 0,5 % du prix (+178 $ / +2 098 $), avec des évals deux fois plus courtes (8,5 jours au lieu de 15). Le spread du CFD juste après 9:30 n'a pas pu être mesuré : le future NQ (bbo-1m) reste à 0,5 point médian de 9:20 à 10:30.

## Avenant A : stop à 1 ATR M15, entrée 9:35, coût 1 pb

Même réglage (éval 2 % / 4,9 %, financé 1 % / 2 %, RAZ), stop à 1 ATR M15 lu à 9:30 ET. Cet ATR vaut **0,12 % du prix en médiane** (~25 points à 20 000), 4 fois moins que 0,5 % : le stop est touché 86 % des jours et le coût de 1 pb pèse **0,083 R par trade** (contre 0,020 R).

| Compte | Passage | Valeur du financé | **EV par tentative** | Refus tolérés | Sans RAZ de la perte max |
|---|---|---|---|---|---|
| 10k | 36,4 % ± 0,7 | 4,35 % ± 0,09 | **+71 $ ± 4** | 45 % | +37 $ |
| 100k | 36,4 % | 4,35 % | **+1 035 $ ± 43** | 65 % | +688 $ |

Éval ~8,7 jours par tentative (8,1 si validée) ; financé : P(≥ 1 reward) 50 %, 0,95 reward en moyenne, vie ~46 jours. Meilleur de la grille (éval 1 / 4,9, financé 0,5 / 2 ; sélectionné, donc optimiste) : +95 $ (10k), +1 275 $ (100k). **Toutes les cases restent positives**, mais l'EV est environ divisée par deux par rapport au stop à 0,5 % du prix (+178 $ / +2 098 $).

**Pourquoi : c'est le spread, pas les trajectoires.** Diagnostic exploratoire (non pré-enregistré, même graine, 20 000 comptes) sur le réglage principal ATR :

| Coût par aller-retour | Passage | Financé | EV 10k | EV 100k |
|---|---|---|---|---|
| 1 pb (hypothèse du protocole) | 37,0 % | 4,41 % | +76 $ | +1 083 $ |
| 0 | 44,2 % | 8,08 % | +270 $ | +3 023 $ |

Avec un stop aussi serré, chaque trade paie ~8 % de son risque en spread, et un compte financé en fait des dizaines. Sans coût, le stop ATR serait au contraire le meilleur réglage. **L'hypothèse de coût devient donc décisive** : 1 pb ≈ 2 points sur US100 ; le spread réel FTMO en séance US est à mesurer (le spread du future NQ est de 2 à 4 ticks, soit 0,5 à 1 point, d'après les données bbo-1m achetées le 31 octobre).

## Réponse (stop en % du prix, protocole initial)

**Oui, l'espérance est positive sans aucune edge, à condition que FTMO verse les rewards.** Résultat principal du protocole initial (NQ réel, stop 0,5 % du prix, éval 2 % de risque / 4,9 % visés, financé 1 % / 2 %, perte max remise à −10 % après chaque reward) :

| Compte | Prix | Passage | Valeur du financé | **EV par tentative** | Refus de reward tolérés |
|---|---|---|---|---|---|
| 10k | 79 € ≈ 87 $ | 40,7 % ± 0,7 | 6,50 % ± 0,11 du capital | **+178 $ ± 6** (≈ 2 × le prix) | jusqu'à 67 % |
| 100k | 499 € ≈ 549 $ | 40,7 % | 6,50 % | **+2 098 $ ± 64** (≈ 3,8 × le prix) | jusqu'à 79 % |

Une éval dure ~15 jours de bourse (13,7 si validée). Le compte financé verse au moins un reward dans 61 % des cas (1,44 en moyenne, premier vers le 19e jour de bourse en médiane) et vit ~85 jours.

Mécanisme : sans edge, P(+10 % avant −10 %) ≈ 50 % ; la perte max qui suit le plus haut solde et la règle du meilleur jour la ramènent vers 41 %. Un financé vaut ~6,5 % du capital, soit ~12 fois le prix d'une éval 100k ; 0,41 × 6,5 % × 100k ≈ 2 650 $ contre 549 $ payés.

## Ce que les vraies trajectoires du NQ changent par rapport au pile ou face

- **Contrôle** : le mode binaire reproduit la session « Hedge sim discussion » (passage 40,9 % contre ~41 % ; financé 0,5/2 à 6,51 % contre 6,85 %, l'écart restant vient du cycle et des tirages).
- **Presque rien sur l'EV** : NQ réel +2 098 $ contre binaire +2 114 $ (100k, principal). La convexité du contrat ne dépend pas de la forme des rendements, seulement du rapport perte max / objectif.
- **La durée change** : avec un stop à 0,5 % du prix, la moitié des jours finissent sans toucher ni stop ni objectif (sortie à 15:54 ET), donc l'éval prend ~15 jours au lieu de ~8,5. Avec un stop à 1 %, il faut 35 jours et le passage tombe à 37 %. Un stop serré (0,25 %) va plus vite et passe autant.
- Glissement au stop : nul en barres 1 minute sur NQ (pas de gap intra-séance mesurable) ; le coût CFD (1 pb du prix) pèse 2 % du risque à s = 0,5 %.

## Sensibilités (100k)

| Variante | EV |
|---|---|
| Principal (s 0,5 %, RAZ) | +2 098 $ |
| s 0,25 % | +2 041 $ |
| s 1 % | +1 745 $ |
| **Sans remise à zéro de la perte max après un reward** | **+1 395 $** (financé 4,77 %) |
| Meilleur de la grille, s 0,25 % (éval 1/4,9, financé 0,5/2 ; sélectionné, donc optimiste) | +2 411 $ |

10k : principal +178 $, sans remise à zéro +107 $, pire case de la grille sans RAZ +93 $. **Aucune case de la grille n'a une EV négative.** L'hypothèse la plus lourde est la remise à zéro de la perte max après un reward (−34 % d'EV si elle était fausse) : vérifiée le 31 octobre, c'est bien la règle du 1-Step.

## Écart au protocole

Le pré-enregistrement dit « risque = r % du capital » sans préciser brut ou net. Un premier passage (2 000 comptes) a compté le coût en plus du risque : à r = 2,9 %, un stop coûtait 3,02 % et violait la perte journalière de 3 % dès le premier stop (passage 7-14 %). Le risque est maintenant **net de coût**, comme dans la session précédente (la taille est choisie pour qu'un stop coûte r, spread compris). La variante sans remise à zéro a aussi été corrigée : le plancher reste au même niveau en dollars après le retrait (définition de la session précédente). Ni l'une ni l'autre ne change le résultat principal du binaire contrôlé.

## Limites

- **Le vrai risque n'est pas modélisé** : FTMO interdit l'« account rolling » et le trading assimilé à du jeu, et relit les comptes avant chaque reward. L'EV reste positive tant que moins de 67 % (10k) à 79 % (100k) des rewards sont refusés, mais un bannissement coupe toute la suite.
- Règles FTMO revérifiées le 31 octobre 2026 : voir la section suivante.
- Un seul actif (NQ), séance US uniquement, un trade par jour ; 1 € = 1,10 $.

## Règles FTMO vérifiées (ftmo.com, 31 octobre 2026)

Relu sur [Trading Objectives](https://ftmo.com/en/trading-objectives/), [1-Step Challenge](https://ftmo.com/en/1-step-challenge/) et [How do I withdraw my reward?](https://ftmo.com/en/faq/how-do-i-withdraw-my-profits/) :

| Règle | Texte FTMO (1-Step) | Dans le simulateur |
|---|---|---|
| Perte max | 10 % du capital initial, « end-of-day trailing » sous le plus haut solde de 00:00 CE(S)T, « can only increase, but never decrease » | identique (plancher suiveur au solde de fin de journée, jamais bloqué) |
| **Après un reward** | « when a Reward is withdrawn and a new FTMO Account is provided, the Maximum Loss Limit fully resets, returning the first-day limit to 90% of the Initial Simulated Capital » | **identique (hypothèse RAZ = règle réelle)** |
| Perte journalière | solde de minuit CE(S)T − 3 % du capital initial | identique |
| Meilleur jour (comptes commandés depuis le 12/10/2026) | meilleur jour ≤ 50 % du profit total ; dépassement = pas une violation, il faut continuer à trader ; condition du reward sur le compte financé | identique |
| Reward | « on the 14th or any following day after the first trade is placed on the specific account », positions fermées, 90 % | 10 jours de bourse après le premier trade de chaque compte (un nouveau compte après chaque reward) |
| Objectif | +10 %, pas de limite de temps, pas de vérification | identique |

Le texte « Your Maximum Loss Limit does not reset when you withdraw a Reward » existe sur la même page, mais dans la section de l'**FTMO Instant Account**, pas du 1-Step. La variante « sans RAZ » ne correspond donc à aucune règle du 1-Step. Non vérifié : les prix (absents des pages lues) et une mention d'une limite de 30 % pour le meilleur jour, citée par un résumé de recherche mais introuvable sur les pages officielles lues.

## Exploratoire : 2026 avec une éval au départ et une éval de plus par reward (10k)

Code : [run_propfirm_2026.py](../run_propfirm_2026.py), sorties `results/propfirm_2026/` (journal daté de chaque compte). Rendements de chaque nuit calculés par vectorbt (`results/propfirm_vbt/returns.csv`), réglage de l'avenant E (éval 2 %, TP 5 ATR ; financé 1 %, TP 4 ATR ; spread 1,5 point), du 2026-01-02 au **2026-08-28, fin des données** (après : holdout, non chargé). Période dans l'échantillon qui a servi à choisir la règle.

| Politique | Évals achetées | Validées / ratées | Rewards | **Net** | Fin août |
|---|---|---|---|---|---|
| À la lettre : chaque reward paie une éval de plus ; un compte raté ou perdu n'est pas remplacé | 2 (174 $) | 1 / 1 | 1 (520 $, 2026-01-27) | **+346 $** | plus aucun compte : l'éval achetée avec le reward rate le 2026-03-02, le financé saute le 2026-03-11 |
| En plus, rachat après chaque échec ou compte perdu | 29 (2 520 $) | 15 / 14 | 7 (4 094 $) | **+1 574 $** | 8 financés validés le 2026-08-13, tous à −3,68 % (non compté) |

Avec rachat, flux nets par mois : janvier +346 $, mars −434 $, avril +1 674 $, mai +482 $, juin +549 $, juillet −1 043 $, août 0 $. Les comptes se synchronisent (même trade chaque nuit) : le 2026-07-28, six financés sautent la même nuit.
