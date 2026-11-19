# Plan « 2 coups » sur LucidFlex 50K

*2026-10-31. Exploratoire, hors compteur d'essais (évaluation d'un contrat). Plan proposé par l'utilisateur. Chiffres : [run_propfirm_lucid_plan.py](../run_propfirm_lucid_plan.py) → `results/propfirm_lucid_plan/run.log` (et `attempts_*.csv`, `rachat_1an.csv`). Même stratégie que les autres plans prop firm : règle NQ de nuit (momentum 12-1, entrée 20:00 ET, stop 2 ATR M15, sortie 9:30 ET au plus tard), ici en MNQ, distances au niveau actuel du NQ (25 684), coût réel par MNQ (~2 $ aller-retour). Chiffres **optimistes** : règle choisie sur 2016-2026, un seul historique.*

## Le plan

- **Éval** : risque 2 000 $, objectif +1 500 $ par nuit. Deux gains d'affilée font 3 000 $ avec un meilleur jour à 50 %.
- **Financé, 1er trade** : risque 2 000 $, objectif +3 400 $. Un stop fait perdre le compte.
- **Ensuite** : une position par nuit, 1 MNQ, risque 150 $ et objectif 150 $ (RR 1, ~74 points). On continue jusqu'à 5 jours à ≥ 150 $ dans le cycle, le gros trade comptant pour un. Payout = 50 % du profit, plafonné à 2 000 $ (3 400 $ + 4 × 150 $ = 4 000 $).
- Une nuit qui sort à 9:30 sans toucher le stop ni l'objectif est suivie d'un nouveau trade, avec le reste à faire comme objectif.

## Règles LucidFlex 50K relues le 2026-10-31 (support.lucidtrading.com)

- **Éval** : objectif 3 000 $, 4 minis ou 40 micros, pas de limite de temps, consistance 40 % (50 % en option, « passer en 2 jours », avec une petite marge non modélisée).
- **MLL** : 2 000 $ en fin de séance sous le plus haut solde de clôture ; bloquée à +100 $ dès que la clôture dépasse +2 100 $, et ramenée à +100 $ au premier payout.
- **Financé** : pas de consistance. Scaling : 20 / 30 / 40 micros sous 1 000 $ / de 1 000 à 1 999 $ / à partir de 2 000 $ de profit.
- **Payout** : 5 jours à ≥ 150 $ et profit net du cycle > 0 ; montant 50 % du profit, plafonné à 2 000 $, minimum 500 $ ; 90 % au trader ; 5 payouts, puis passage en réel (non valorisé).
- **Limite journalière** : avec 2 000 $ de risque, la DLL (1 200 $, « soft breach ») couperait le trade, donc il faut la version **DLL désactivée + consistance 50 %**. C'est la plus chère ; son prix ne s'affiche qu'au paiement, **130 $ selon l'utilisateur**.
- Max 5 comptes financés par foyer.

## Résultats (une tentative par nuit de départ, 3 535 départs, 2011-07 → 2025-08)

Un trade isolé, toutes les nuits :

| Trade | Objectif | Stop | Sortie 9:30 | P&L moyen |
|---|---|---|---|---|
| 2 000 $ → +1 500 $ (≈ 0,77 R, ~15 MNQ) | 58,0 % | 39,5 % | 2,6 % | +111 $ |
| 2 000 $ → +3 400 $ (≈ 1,8 R, 20 MNQ max) | 26,4 % | 51,0 % | 22,6 % | +185 $ |
| 150 $ → +150 $ (1 MNQ) | 44,7 % | 40,0 % | 15,3 % | +9 $ |

Contrat complet, à 130 $ l'éval :

| | Passage | P(≥ 1 payout) si financé | Valeur du financé (90 %) | **EV par éval** | Prix d'équilibre |
|---|---|---|---|---|---|
| (a) un seul payout puis arrêt | 34,5 % | 36 % | 569 $ | **+66 $** (± 54) | 196 $ |
| (b) même cycle répété jusqu'au 5e payout | 34,5 % | 36 % | 1 057 $ | **+234 $** (± 121) | 364 $ |
| Sans edge, sens au hasard (a) / (b) | 30,8 % / 30,3 % | — | 525 $ / 915 $ | +32 $ / +147 $ | 162 $ / 277 $ |

- **L'éval se joue en 2 nuits** : passer revient à 2 objectifs d'affilée (0,58² ≈ 34 %). Presque toutes les évals ratées le sont sur un stop, qui laisse ~60 $ de marge, trop peu pour 1 MNQ.
- **Le financé se joue sur le gros trade** : 64 % des financés meurent sur ce stop ; ceux qui le passent touchent presque toujours le payout. Le 1er payout vaut en moyenne 1 740 $ bruts (2 000 $ dans 5 % des cas seulement, car les jours perdants à 150 $ rognent le profit) et arrive ~8 nuits après l'ouverture du financé.
- **Hors le gros trade, l'edge compte peu.** Sans edge, le plan garde la moitié de sa valeur ((b) : +147 $ contre +234 $). La convexité du contrat (perte plafonnée au prix de l'éval) fait le reste. Le gain de l'edge (+34 $ en (a), +87 $ en (b)) reste dans l'erreur-type.
- **Prix** : à 130 $, (a) n'a qu'une petite marge (EV ≈ 0 vers 196 $) ; (b) tient jusqu'à ~360 $.
- Comparaison avec l'avenant D (règle sans changement, éval 400 $, financé 200 $, DLL ON 40 %, 115 $) : **+157 $** par éval. Le plan « 2 coups » fait moins si l'on s'arrête au 1er payout, plus si l'on recommence le cycle.

**Un compte racheté à chaque échec** (plan (a), 130 $, horizon 1 an, départs toutes les 5 nuits) : gain net médian **+3 738 $**, 5e centile −2 538 $, pire −5 208 $. Il faut sortir 988 $ de sa poche en médiane avant que les payouts remboursent (95e centile 3 918 $, pire 5 208 $). Environ **60 évals par an** (une éval dure ~2 nuits) ; pire série de 23 évals ratées d'affilée.

## Limites

- Prix de la version DLL OFF + 50 % non lu sur le site (130 $ donné par l'utilisateur).
- Les gros trades risquent ~15 MNQ (jusqu'à 40) sur une seule position : rien n'a été vérifié dans les règles Lucid sur les comportements jugés « de jeu » ou sur la revue des payouts.
- La marge de consistance (≈ 52 %) n'est pas utilisée ; la limite de 5 comptes financés par foyer n'est pas modélisée.
- Le compte réel après 5 payouts n'est pas valorisé (prudent).
- Erreurs-types grossières : les départs se chevauchent.
