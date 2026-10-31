# Plan prop firm refait chez Smart Trader Funds, challenge « 1 Phase »

*2026-10-31. Exploratoire, hors compteur d'essais (évaluation d'un contrat, pas d'une règle de marché). Chiffres : [run_propfirm_stf.py](../run_propfirm_stf.py) → `results/propfirm_stf/run.log` (et `grid.csv`, `reserve.csv`, `paths_*.csv`, `exits.csv`). Règles codées dans [propfirm/stf.py](../propfirm/stf.py). Même stratégie que le plan FTMO : règle NQ de nuit (momentum 12-1, entrée 20:00 ET, stop 2 ATR M15, sortie 9:30 ET au plus tard), rendements de chaque nuit par vectorbt (`results/propfirm_farm_heures/returns.csv`), spread 1,5 point. Chiffres **optimistes** pour les mêmes raisons qu'avec FTMO : règle choisie sur 2016-2026, un seul historique.*

## Règles relevées sur smartraderfunds.com (2026-10-31)

Sources : configurateur de la page d'accueil, `/challenges/` (comparatif), `/help/`, `/terms-of-use/` (§ 14, § 18, § 19), page de paiement.

| Règle | 1 Phase (éval) | 1 Phase (financé) |
|---|---|---|
| Objectif | +9 % | — |
| Perte du jour | 4 % du solde de début de journée, latent compris, remise à zéro à minuit GMT | idem |
| Perte max | 6 %, **fixe** depuis le solde initial (pas suiveuse) | idem |
| Jours minimum | 5 jours avec au moins un trade | 5 jours |
| Consistance | aucun jour > 45 % du profit total | idem, « pendant toute la durée du financement » |
| Annonces 3 étoiles | aucune ouverture, modification ni clôture **5 min** avant / après | **10 min** avant / après |
| Week-end | interdit de garder une position | interdit |
| Jours fériés | aucun trade un jour marqué « Holiday » au calendrier économique | idem |
| Levier | 1:50 max | 1:50 max |
| Durée | illimitée ; compte désactivé après 20 jours calendaires sans trade | idem |
| Retraits | — | 1er retrait 30 jours après l'ouverture du financé, puis tous les 14 jours ; minimum 100 $ ; frais de retrait jusqu'à 3 % |
| Part du trader | — | 80 %, 90 % après 3 retraits réussis (95 % avec option payante +20 %) |
| Remboursement des frais | — | avec le **2e** retrait selon `/help/`, le **1er** selon `/challenges/` (contradiction ; on prend le 2e) |
| Taille | 10k à 300k au départ ; 800 k$ de capital cumulé max par profil (plusieurs comptes autorisés) | |

Prix (TradeLocker ; Platform 5 un peu plus cher) : 10k **139 $**, 25k 229 $, 50k 389 $, 100k **599 $**, 200k 1 179 $, 300k 1 649 $. Options : 95 % de part (+20 %), sans jours minimum (+25 %), retrait à 14 jours (+15 %). Pour comparer, FTMO 1-Step : 87 $ / 549 $, perte max 10 % suiveuse, objectif 10 %, consistance 50 %, pas de règle des annonces.

Interdits des CGU (§ 14.1) qui touchent ce plan : « Gap Trading », comptes liés tradés ensemble (« Group Trading »), positions beaucoup plus grosses que les autres du compte, « Account Rolling », copie de trades sans accord. Chaque position doit avoir un stop dès l'ouverture (§ 18.1.10). Rien de cela n'est modélisé ; un trio de comptes sur le même signal est le cas le plus exposé.

## Hypothèses de modélisation

- Une nuit tradée = un jour de trading ; l'entrée (00:00 ou 01:00 GMT) et la sortie tombent le même jour GMT, donc la perte du jour ne compte qu'un trade (≤ 2 % ici).
- **Annonces** : seules les annonces US de 8:30 ET du calendrier `config/calendrier_macro_us.csv` (NFP, CPI, PPI, ventes au détail, PCE, PIB) sont prises en compte ; une sortie par stop ou objectif à moins de 5 min (éval) ou 10 min (financé) de 8:30 = compte perdu. Les annonces non US et les « 3 étoiles » absentes de ce calendrier ne sont pas comptées (optimiste).
- Variante **à plat** : les jours d'annonce 8:30, la position est fermée à 8:19 ET (dans la règle, avant les deux fenêtres). vectorbt rejoue ces nuits avec cette sortie. Ce n'est pas un filtre de rendement (le n° 14 l'a rejeté comme tel, voir le registre) : c'est la seule manière de garder la règle conforme.
- Jours fériés : une nuit dont l'entrée tombe un jour de semaine sans séance NYSE n'est pas tradée (~110 nuits sur 3 800).
- Week-end : la règle n'ouvre rien le vendredi soir ; levier à 2 % de risque : médiane 7,7, max 39,9 (sous 50).
- Financé : un retrait vide le profit, le solde revient au capital initial, le plancher reste à −6 % de ce capital. On retire dès que c'est permis (30 / 14 jours, ≥ 5 jours tradés dans le cycle, ≥ 100 $, meilleur jour ≤ 45 % du profit du cycle). Frais de retrait de 3 % non déduits.
- Financé ouvert la nuit qui suit la validation (« instant funding »).

## Résultats (signal 20:00, une tentative par nuit de départ, 2011-07 → 2024-08)

| Réglage | Passage | P(≥ 1 retrait) | EV / éval 10k | EV / éval 100k |
|---|---|---|---|---|
| Réglage FTMO (éval 2 % TP 5, financé 1 % TP 4), position gardée pendant les annonces | 30,6 % | 31 % | **−62 $** | +148 $ (± 390) |
| idem, règle des annonces ignorée | 46,9 % | 71 % | +339 $ | +4 001 $ |
| idem, **à plat à 8:19 les jours d'annonce** | 44,8 % | 71 % | **+390 $** (± 167) | **+4 512 $** (± 1 632) |
| à plat, signal 19:00 | 46,8 % | 69 % | +615 $ | +6 748 $ |
| à plat, signal 21:00 | 41,4 % | 63 % | +334 $ | +3 989 $ |
| à plat, risques × 0,6 (6 % / 10 % de perte max, fixé avant de voir les chiffres) : éval 1,2 %, financé 0,6 % | 60,5 % | 88 % | +678 $ | +7 209 $ |
| à plat, meilleur des 36 réglages de la grille (éval 1 % TP 4, financé 0,5 % TP 4 ; choisi après coup) | 72,8 % | — | +1 179 $ | +12 118 $ |

Les ± sont des IC 95 % grossiers (départs chevauchants).

- **La règle des annonces est le point décisif.** Sans précaution, 2,5 % des nuits sortent par stop ou objectif dans la fenêtre interdite (la volatilité de 8:30 déclenche les ordres) : c'est 36 % des évals ratées et 58 % des financés perdus, et l'EV du 10k devient négative. Fermer à 8:19 ces jours-là coûte un peu de rendement sur les nuits concernées (~380, R moyen +0,79 → +0,68 en unités de stop) mais rétablit tout.
- Avec les mêmes réglages qu'au plan FTMO, STF rapporte **environ 2,5 fois moins par éval** (FTMO : +1 009 $ / +10 408 $, avenant E). Causes : perte max 6 % fixe au lieu de 10 % suiveuse (3 stops à 2 % suffisent à perdre le compte), objectif 9 % avec consistance 45 % (un TP de +5 % exige ≥ 11,1 % de profit avant de valider), éval plus chère en 10k, premier retrait à 30 jours.
- Des risques plus petits conviennent mieux à une perte max de 6 % : les 36 réglages de la grille ont une EV 100k positive (pire +3 925 $), les meilleurs sont à 1 % en éval et 0,5 % en financé. Le réglage × 0,6, fixé par la seule règle de proportion, double l'EV (+678 $ / +7 209 $) ; les meilleurs de la grille sont optimistes (choisis sur les mêmes données).

## Plan de montée (variante à plat, réglage FTMO, 612 départs de 3 ans, 2011-07 → 2023-08)

**Un seul 10k racheté à chaque échec** (20:00) : mise médiane 316 $, 95e centile 973 $, pire 1 668 $ (12 évals ; FTMO : 650 $, 7 évals) ; premier retrait après 67 nuits en médiane, au pire 312 ; pire série de 7 évals ratées ; gain net à 3 ans **+3 173 $** en médiane (5e centile +1 370 $).

**Configurations fixes dès le départ** (rachat à chaque échec) :

| Configuration | Argent sorti avant remboursement : médiane / 95e c. / pire | Gain net à 3 ans : médiane / 5e c. / pire |
|---|---|---|
| 1 × 10k | 316 / 973 / 1 668 $ | +3 173 / +1 370 / +665 $ |
| 3 × 10k (19:00, 20:00, 21:00) | 1 108 / 2 919 / 4 309 $ | +10 821 / +4 242 / +2 135 $ |
| 1 × 100k | 1 198 / 4 193 / 7 188 $ | +44 663 / +26 654 / +16 929 $ |
| 2 × 100k | 2 396 / 8 386 / 12 579 $ | +100 930 / +45 399 / +32 948 $ |
| 3 × 100k | 3 866 / 11 183 / 18 569 $ | +141 837 / +86 129 / +69 605 $ |

**Chemins depuis un seul 10k**, palier franchi quand les gains couvrent l'argent sorti de la configuration suivante (comme `run_propfirm_start1.py`) :
- seuils au 95e centile (départ 1 000 $ ; 1 × 100k à 4 193 $, trio 10k à 2 919 $, trio 100k à 11 183 $) : A2 (1 × 10k → 1 × 100k → 2 × 100k → trio) atteint le 100k dans 41 % des départs seulement, en ~24 mois médians ; gain à 3 ans **+2,8 k$** en médiane. B2 +3,5 k$, C2 jamais de 100k en 3 ans. FTMO, même règle : A2 +54,9 k$.
- seuils au pire chemin (départ 1 700 $) : presque jamais de 100k en 3 ans (14 % des départs pour A2).

Le 10k STF rapporte trop peu (≈ 1 175 $ par an pour un compte) pour financer la montée : la règle « les gains paient le palier suivant » bloque le plan au 10k. Le chiffre qui compte est le 100k : sa réserve au 95e centile (4 193 $ pour un compte, 11 183 $ pour trois) est sortie de sa poche, mais le gain net à 3 ans est positif dans **tous** les départs historiques (pire +16,9 k$ pour un 100k, +69,6 k$ pour trois).

## Limites

- Annonces : calendrier US 8:30 seulement ; le comportement exact de STF quand un stop serveur est touché pendant la fenêtre (échec, ou seulement trade annulé) n'est pas écrit sur le site. La ligne « annonces ignorées » donne la borne haute.
- Spread US100 chez STF inconnu (1,5 point supposé, comme FTMO). Plateformes TradeLocker / Platform 5, pas de commissions annoncées.
- Remboursement des frais : 1er ou 2e retrait selon la page ; frais de retrait jusqu'à 3 % non déduits.
- Risques non modélisés : refus de retrait au titre du § 14 (gap trading, comptes liés, tailles anormales), désactivation, faillite de la prop firm.
- Chiffres optimistes : règle choisie sur 2016-2026, un seul historique, grille de risques choisie sur les mêmes données.
