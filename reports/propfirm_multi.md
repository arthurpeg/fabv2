# La règle NQ de nuit chez 10 prop firms, avec plusieurs gestions du risque

*2026-10-31. Exploratoire, hors compteur d'essais (évaluation de contrats). Chiffres : [run_propfirm_multi.py](../run_propfirm_multi.py) → `results/propfirm_multi/run.log` (et `summary.csv`, `eval_grid.csv`, `funded_grid.csv`). Moteur : [propfirm/generic.py](../propfirm/generic.py) ; nuits : [propfirm/nights.py](../propfirm/nights.py). Stratégie unique : règle NQ de nuit (momentum 12-1, entrée 20:00 ET, stop 2 ATR M15, sortie 9:30 ET au plus tard). Chiffres **optimistes** : la règle a été choisie sur 2016-2026, il n'y a qu'un historique, et les spreads réels des CFD ne sont pas connus (1,5 point supposé).*

## Règles relevées sur les sites (2026-10-31)

Taille retenue : 100k pour les CFD (20k chez The5ers, maximum de départ 40k), 50K pour les futures. « Fixe » = sous le capital initial ; « EOD » = suit le plus haut solde de clôture ; « séance » = suit le plus haut latent.

| Prop firm (programme) | Prix | Éval | Financé | Retraits |
|---|---|---|---|---|
| **FTMO** 1-Step 100k | 549 $ (499 €) | +10 %, perte max 10 % suiveuse, jour 3 %, meilleur jour ≤ 50 % | idem | cycle de 10 jours tradés, meilleur jour ≤ 50 %, 90 %, perte max remise à zéro |
| **Smart Trader Funds** 1 Phase 100k | 599 $ | +9 %, 6 % fixe, jour 4 %, 45 %, 5 jours, annonces ±5 min | annonces ±10 min | 1er à 30 j puis 14 j, 80 % puis 90 %, frais rendus au 2e |
| **FundedNext** Stellar 1-Step 100k | 569,99 $ | +10 %, 6 % fixe, jour 3 %, 2 jours | risque ≤ 3 % à tout moment, profits ±5 min d'une annonce comptés à 40 % | tous les 5 jours ouvrés, 80 %, frais rendus au 3e |
| **FundingPips** 1 Step Flex 100k | 666 $ + 10 % (option Swing, obligatoire pour garder la nuit en financé) | +12 %, 12 % fixe, jour 3 % (option ; 2 % de base), levier indices 1:20 | levier 1:5 (compte Swing), pas de consistance | toutes les 2 semaines, min 1 %, 80 % |
| **The5ers** Pro Growth 20k | 189 $ | +10 %, 6 % fixe, jour 3 %, 3 jours gagnants, levier 1:30 | idem à chaque palier | à chaque +10 % : profit versé (75 %), puis compte agrandi (20k → 25k → 30k → 40k → … → 300k, 80 % au-delà) |
| **Topstep** 50K Standard | 49 $ / mois + 149 $ d'activation | +3 000 $, 2 000 $ EOD bloqué au capital, meilleur jour ≤ 55 % de l'objectif, 5 minis | 2 000 $ EOD bloqué à 0 ; 2 / 3 / 5 minis sous 1 500 / 2 000 $ / au-delà | 5 jours ≥ 150 $, 50 % du solde plafonné à 2 000 $, 90 %, plancher à 0 après le 1er |
| **Apex** 50K EOD sans activation | 119 $ (coupon permanent ; 1 190 $ affiché) | +3 000 $, 2 000 $ EOD, jour 1 000 $ souple, 6 minis, **30 jours max** | 2 000 $ EOD bloqué à +100 $ ; paliers 2 / 3 / 4 / 4 minis et jour 1 000 / 1 000 / 2 000 / 3 000 $ | 5 jours ≥ 250 $, meilleur jour < 50 %, garder 2 100 $, plafonds 1 500 / 1 500 / 2 000 / 2 500 / 2 500 / 3 000 $, 100 %, 6 retraits |
| **MyFundedFutures** Rapid 50K | 125 $ (promo ; 209 $) | +3 000 $, 2 000 $ EOD bloqué à +100 $, 50 %, 2 jours, 5 minis | 2 000 $ **en séance** bloqué à +100 $, à plat ±2 min des annonces Tier 1 | quotidien, coussin 2 100 $, min 500 $, 90 % |
| **Tradeify** Growth 50K | 145 $ (reset 95 $) | +3 000 $, 2 000 $ EOD, jour 1 250 $ souple, 4 minis | idem (blocage à +100 $ et jour supposés) | profit ≥ 3 000 $, 5 jours > 150 $, meilleur jour ≤ 35 %, plafonds 1 500 / 2 000 / 2 500 / 3 000 $, 90 % |
| **Lucid** LucidFlex 50K (jour désactivé, 50 %) | 130 $ | +3 000 $, 2 000 $ EOD bloqué à +100 $, 50 %, 4 minis | 2 / 3 / 4 minis sous 1 000 / 2 000 $ / au-delà | 5 jours ≥ 150 $, 50 % du profit plafonné à 2 000 $, 90 %, 5 retraits |

Sources : help.fundednext.com (article Stellar 1-Step), fundingpips.com (/trading-objectives, /1-step-flex), the5ers.com (/hyper-growth, onglets Pro Growth), help.topstep.com (paramètres, retraits, MLL, scaling, prix), apextraderfunding.com (help-center EOD), help.myfundedfutures.com et /plans/rapid, help.tradeify.co (Growth, retraits, prix), support.lucidtrading.com ; FTMO et STF : rapports précédents ([[reports/prereg18_report]], [[reports/propfirm_stf_1phase]]).

Points supposés (non écrits sur le site) : Tradeify, blocage de la perte max à +100 $ et perte du jour en financé ; MyFundedFutures et Tradeify, on ne retire que le profit au-delà de 2 100 $ ; FundingPips, levier 1:5 en financé avec l'option Swing ; The5ers, profit versé à chaque palier. Non retenus : E8 Markets, Alpha Capital, Take Profit Trader (pas relevés).

## Méthode

- **Gestion du risque** : risque par trade = k × perte max du compte (borné par la marge restante et par la perte du jour), objectif à rr R. En éval, l'objectif est ramené au reste à faire (cible et consistance). Grille : éval k ∈ {0,1 ; 0,2 ; 0,33 ; 0,5 ; 1}, rr ∈ {0,75 ; 1 ; 1,5 ; 2 ; 2,5 ; 3} ; financé k ∈ {0,1 ; 0,2 ; 0,33 ; 0,5}, rr ∈ {1 ; 1,5 ; 2 ; 2,5 ; 3}.
- **Valeur** : P(passage) × (retraits reçus sur 2 ans par le financé − activation) − coût moyen de l'éval. Éval et financé sont simulés séparément depuis chaque nuit de départ.
- **Choix du réglage** sur les départs 2011-07 → 2018-12, mesure sur 2019-01 → 2025-08 (hors échantillon).
- **Contrôles** :
  - FTMO avec les réglages du plan : passage 51,2 %, EV +11 095 $ (+10 408 $ dans run_propfirm_rr2) ;
  - STF, trajectoire reproduite au dollar près sur un même départ ;
  - les issues de chaque nuit sont identiques à celles de vectorbt (corrélation 1,00).

## Résultats

| Prop firm | Prix | EV avec les réglages du plan FTMO | Réglage choisi sur 2011-2018 (éval k / rr ; financé k / rr) | **EV hors échantillon 2019-2025** | EV sur 2011-2018 | Sans edge |
|---|---|---|---|---|---|---|
| **FundingPips** 1 Step Flex 100k | 733 $ | +17 579 $ | 0,1 / 1,5 ; 0,1 / 2 | **+12 053 $** (×16,5) | +33 709 $ | +3 413 $ |
| **FTMO** 1-Step 100k | 549 $ | +11 095 $ | 0,1 / 2 ; 0,1 / 1 | **+7 633 $** (×13,9) | +24 970 $ | +1 712 $ |
| Smart Trader Funds 1 Phase 100k | 599 $ | +9 011 $ | 0,1 / 1,5 ; 0,1 / 2 | +6 941 $ (×11,6) | +18 739 $ | +1 116 $ |
| FundedNext Stellar 1-Step 100k | 570 $ | +7 516 $ | 0,1 / 1,5 ; 0,1 / 2 | +6 134 $ (×10,8) | +15 409 $ | +1 058 $ |
| The5ers Pro Growth 20k | 189 $ | +2 413 $ | 0,1 / 1,5 ; 0,2 / 1 | +896 $ (×4,7) | +5 377 $ | +48 $ |
| Tradeify Growth 50K | 145 $ | +980 $ | 0,1 / 2 ; 0,2 / 2,5 | +462 $ (×3,2) | +2 925 $ | +4 $ |
| MyFundedFutures Rapid 50K | 125 $ | +807 $ | 0,1 / 2 ; 0,1 / 2 | +380 $ (×3,0) | +1 857 $ | −23 $ |
| Apex 50K EOD | 119 $ | +251 $ | 0,33 / 2 ; 0,2 / 2,5 | +344 $ (×2,9) | +1 206 $ | +81 $ |
| Lucid LucidFlex 50K | 130 $ | +205 $ | 0,1 / 2 ; 0,5 / 2 | +206 $ (×1,6) | +684 $ | +21 $ |
| Topstep 50K | 49 $/mois + 149 $ | +93 $ | 0,1 / 2 ; 0,5 / 2,5 | **−53 $** | +1 956 $ | −156 $ |

(×n = EV hors échantillon divisée par le prix de l'éval et de l'activation.)

**EV selon l'agressivité en éval** (toute la période, meilleur rr pour chaque k, meilleur financé) et nuits médianes pour valider (`results/propfirm_multi/agressif.txt`) :

| Prop firm | k = 0,1 | 0,2 | 0,33 | 0,5 | 1 (tout ou presque) |
|---|---|---|---|---|---|
| FTMO 100k | +16 801 $ (43 nuits) | +12 041 $ (10) | +10 188 $ (6) | = 0,33 (plafond : perte du jour 3 %) | = 0,33 |
| FundingPips 100k | +24 863 $ (60) | +19 760 $ (14) | +17 040 $ (9) | = | = |
| STF 100k | +13 151 $ (114) | +9 852 $ (66) | +7 971 $ (24) | +6 963 $ (10) | +6 179 $ (6) |
| FundedNext 100k | +11 053 $ (129) | +8 264 $ (29) | +6 386 $ (28) | +5 325 $ (4) | = |
| Tradeify 50K | +1 871 $ (118) | +1 432 $ (26) | +1 084 $ (8) | +1 103 $ (3) | +1 148 $ (2) |
| Apex 50K | −114 $ (19, délai de 30 j) | +438 $ (13) | +783 $ (7) | +832 $ (3) | +832 $ |
| Lucid 50K | +510 $ (118) | +371 $ | +260 $ | +234 $ | +202 $ (3) |

## Lecture

- **Les CFD à 100k dominent largement les futures à 50K**, même rapporté au prix (×11 à ×16 contre ×2 à ×3 hors échantillon). La raison tient au contrat, pas au marché : chez les CFD, un retrait remet le solde au capital initial et la perte max repart de zéro. Chez les prop firms de futures, le plancher se bloque à +100 $ (ou 0) au premier retrait, les retraits sont plafonnés (1 500 à 3 000 $) et souvent limités en nombre. Le compte financé futures vit donc peu : 29 à 65 % touchent au moins un retrait, contre 87 à 95 % chez les CFD.
- **FundingPips 1 Step Flex sort premier**, devant FTMO, grâce à une perte max fixe de 12 % pour un objectif de 12 %. Mais deux points ne sont pas vérifiés : le levier 1:5 du compte Swing (supposé ; il plafonne déjà le risque à ~1,3 %), et le prix exact de l'option perte du jour 3 %.
- **Être agressif ne paie pas en espérance.** Le risque le plus bas de la grille (k = 0,1, soit 1 % chez FTMO) gagne partout sauf chez Apex, où la limite de 30 jours l'interdit. Ce choix est en bord de grille : un risque encore plus bas pourrait faire mieux. Le prix à payer, c'est le temps : chez FTMO, 43 nuits médianes pour valider à 1 %, contre 10 nuits à 2 % et 6 à 3 % (EV −29 % et −39 %). En futures, k = 0,1 ne fait qu'un MNQ et l'éval dure ~6 mois.
- **Ratio gain / risque** : en éval, l'objectif ramené au reste à faire avec rr 1,5 à 2 est le meilleur chez les CFD, et 2 à 3 chez les futures. En financé, rr 2 est presque partout le meilleur ; Topstep, Tradeify, Apex et Lucid préfèrent un risque financé plus élevé (0,2 à 0,5) avec rr 2,5, pour atteindre vite un retrait plafonné.
- **La période 2019-2025 rapporte 2 à 4 fois moins que 2011-2018** chez tout le monde, avec le même réglage. L'hors échantillon est le chiffre à retenir. Topstep y devient négatif.
- **Sans edge** (sens au hasard), seules les prop firms CFD restent nettement positives (+1 000 à +3 400 $), par pure convexité du contrat. Les futures tombent vers zéro ou en dessous.

## Limites

- Spread des CFD supposé à 1,5 point partout ; commissions futures ~2 $ par MNQ ; aucun glissement au-delà des barres 1 min.
- Règles supposées (voir plus haut) ; FTMO et STF sans la limite de taille ni les refus de retraits ; aucun risque de faillite ni de bannissement (« account rolling », positions anormalement grosses).
- Éval et financé simulés séparément : la corrélation entre le moment du passage et la suite est ignorée.
- Grille de 30 × 20 réglages choisie sur les mêmes données pour la colonne « toute la période » ; seul le chiffre hors échantillon échappe à ce biais de sélection, pas au choix de la règle sur 2016-2026.

## Métriques détaillées FTMO et FundingPips (2026-11-01)

Chiffres : [run_propfirm_metrics.py](../run_propfirm_metrics.py) → `results/propfirm_multi/metrics.log`, `metrics_chain.csv`. Deux réglages chacun : « choisi » (risque 0,1 × perte max, choisi sur 2011-2018) et « plan FTMO » (éval 0,2 × perte max à 2,5 R, financé 0,1 à 2 R).

| | FTMO choisi | FTMO plan | FundingPips choisi | FundingPips plan |
|---|---|---|---|---|
| Risque éval / financé | 1 000 $ à 2 R / 1 000 $ à 1 R | 2 000 $ à 2,5 R / 1 000 $ à 2 R | 1 200 $ à 1,5 R / 1 200 $ à 2 R | 2 400 $ à 2,5 R / 1 200 $ à 2 R |
| Passage (2011-2018 / 2019-2025) | 76 % (84 / 67) | 51 % (54 / 48) | 88 % (95 / 81) | 67 % (69 / 63) |
| Nuits pour valider (médiane / 90e) | 43 / 90 | 11 / 24 | 60 / 152 | 15 / 39 |
| Financé : P(≥ 1 retrait), retraits sur 2 ans | 92 %, 8,5 | 87 %, 5,2 | 94 %, 11,9 | 94 %, 11,9 |
| Versé sur 2 ans (moyenne / médiane / 10e c.) | 22,5 / 16,8 / 1,9 k$ | 22,7 / 15,8 / 0 k$ | 27,5 / 22,8 / 4,4 k$ | idem |
| 1er retrait (nuits, médiane) | 15 | 17 | 11 | 11 |
| EV par éval : tout / 2019-2025 / sans edge | +16,6 / +7,6 / +1,7 k$ | +11,1 / +6,2 / +2,0 k$ | +23,5 / +12,1 / +3,5 k$ | +17,6 / +9,3 / +3,5 k$ |
| **Un compte racheté 3 ans : gain net médiane / 5e c. / pire** | +31,2 / +20,4 / +14,7 k$ | **+73,1 / +51,5 / +43,7 k$** | +43,8 / +23,7 / +10,2 k$ | **+61,6 / +48,5 / +38,2 k$** |
| Argent sorti avant remboursement (médiane / pire) | 549 / 2 196 $ | 1 098 / 3 843 $ | 733 / 2 198 $ | 733 / 3 663 $ |
| Évals achetées en 3 ans (médiane), pire série ratée | 3, 2 | 9, 6 | 4, 2 | 4, 4 |

**Le meilleur réglage par éval n'est pas le meilleur dans le temps.** À 1 % de risque, l'EV par éval est plus haute, mais l'éval dure 2 à 3 mois et le financé paie lentement. Sur 3 ans avec un seul compte racheté à chaque échec, le réglage plus agressif du plan FTMO rapporte 2,3 fois plus chez FTMO (+73 k$ contre +31 k$) et 1,4 fois plus chez FundingPips. Pour un compte unique, c'est le gain par unité de temps qui compte, pas l'EV par éval. Ces chaînes couvrent 2011-2023 : en partie dans l'échantillon, et optimistes comme le reste.
