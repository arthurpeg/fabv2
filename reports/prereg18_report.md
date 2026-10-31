# Rapport n° 18 : espérance d'une éval FTMO 1-Step avec des trades au hasard

*2026-10-31. Protocole : [[PREREGISTRATION_18]]. Code : [run_propfirm_ftmo.py](../run_propfirm_ftmo.py), [propfirm/](../propfirm/). Sorties : `results/propfirm/` (run.log, eval.csv, funded.csv, ev.csv). Compteur d'essais inchangé (1 482) : on évalue un contrat, pas une règle de marché.*

## Avenant B : entrée 9:50 ET, spread 1 à 1,5 point (résultat principal actuel)

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

10k : principal +178 $, sans remise à zéro +107 $, pire case de la grille sans RAZ +93 $. **Aucune case de la grille n'a une EV négative.** L'hypothèse la plus lourde est la remise à zéro de la perte max après un reward (−34 % d'EV si elle est fausse) : à vérifier chez FTMO.

## Écart au protocole

Le pré-enregistrement dit « risque = r % du capital » sans préciser brut ou net. Un premier passage (2 000 comptes) a compté le coût en plus du risque : à r = 2,9 %, un stop coûtait 3,02 % et violait la perte journalière de 3 % dès le premier stop (passage 7-14 %). Le risque est maintenant **net de coût**, comme dans la session précédente (la taille est choisie pour qu'un stop coûte r, spread compris). La variante sans remise à zéro a aussi été corrigée : le plancher reste au même niveau en dollars après le retrait (définition de la session précédente). Ni l'une ni l'autre ne change le résultat principal du binaire contrôlé.

## Limites

- **Le vrai risque n'est pas modélisé** : FTMO interdit l'« account rolling » et le trading assimilé à du jeu, et relit les comptes avant chaque reward. L'EV reste positive tant que moins de 67 % (10k) à 79 % (100k) des rewards sont refusés, mais un bannissement coupe toute la suite.
- Règles FTMO relevées en octobre 2026 dans la session précédente, pas revérifiées ici.
- Un seul actif (NQ), séance US uniquement, un trade par jour ; 1 € = 1,10 $.
