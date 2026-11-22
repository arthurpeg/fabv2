---
type: experiment
updated: 2026-11-22
status: abandoned
verdict: ❌ B1 sur NQ, ES, YM (DSR famille complète 0,02 ; ≈ 0 avant 2016)
prereg: []
trials: 2021
---

# NQ : règle de la 1ʳᵉ bougie de 5 minutes (Zarattini-Aziz) avec d'autres sorties

**Une phrase** : on prend position à 9:35 ET dans le sens de la bougie 9:30-9:35, comme Zarattini et Aziz (SSRN 4416622). On remplace leur sortie (stop à l'extrême de la bougie, objectif 10R) par (a) aucune sortie avant 16:00, ou (b) un stop à k × ATR et un objectif à RR × stop. Demandé par l'utilisateur le 2026-11-22.

## Étape 0 : fiche d'idée (2026-11-22, aucun calcul)

### 1. Déjà vu ?

- **Registre des échecs** : « Opening range breakout (30 min, 5 min, filtre volume ; ORB de Zarattini) » (2026-10-12, ❌, sans condition de réouverture). La règle de base (R4, [[PREREGISTRATION_3]]) est connue : NQ Sharpe net **+0,96 sur 2016-2022, +0,17 sur 2023-08/2026**, 24 % de réussite, environ 7,7 ticks nets par trade ([[RESULTS]], `results/replications.csv`).
- **Pourquoi la rouvrir** : demande explicite de l'utilisateur, et la question est une **couche nouvelle** (la gestion de sortie) qui n'a jamais été calculée sur NQ. Le papier lui-même (section « A Further Investigation ») trouve son meilleur résultat avec un stop à 5 % de l'ATR sur 14 jours et une sortie à la clôture, mais il choisit cette case sur tout l'échantillon, sans test hors échantillon et sans slippage ([[papiers_ssrn_orb_2026-11-22]], fiche [14]).
- **Phénomènes** : aucun phénomène « 1ʳᵉ bougie » au registre.

### 2. Mécanisme supposé

Le papier n'en propose pas de formel. L'hypothèse implicite : le déséquilibre d'ordres accumulé hors séance se résorbe à l'ouverture du cash et donne la direction de la journée ; la 1ʳᵉ bougie en est un indicateur bruité. Sans mécanisme démontré : noté.

### 3. Taille attendue face au coût

R4 sur NQ : environ 9,7 ticks bruts par trade sur 2016-2026, pour un coût standard de 2 ticks (1 tick + 5 $). La taille dépasse 1,5 × le coût, le parcours **stratégie** est donc ouvert. Mais l'effet est concentré sur 2016-2022.

### 4. Découpage des données

- Tranche : NQ, Databento 1 min, **2010-06-08 → 2026-08-28**, déjà explorée pour l'effet de base.
- **Réserve de la question « sortie »** : les 30 % les plus récents, soit **2021-10-01 → 2026-08-28** (4,9 ans), déclarée dans [[wiki/reserves]] avant tout calcul. Sur cette réserve, C1 n'est **pas informatif** seul, puisque R4 y a déjà été vu. Le verdict reposerait sur l'écart entre la règle choisie et R4 sur les mêmes jours.
- **Exploration** : 2010-06-08 → 2021-09-30. La partie 2010-2015 n'a jamais été vue par cette règle (ni par R4).
- Rien après le 2026-08-28 (holdout du n° 26).

### 5. Puissance (ordre de grandeur, avant calcul)

Écart attendu entre deux sorties : quelques points par trade. L'écart-type d'un trade 9:35 → 16:00 sur NQ est de l'ordre de 50 à 100 points. Avec environ 1 150 trades sur la réserve, un écart de 2 points donne un t d'environ 0,7 à 1,4 : **puissance d'environ 15 à 30 %**, sous 50 %. La réserve ne pourra probablement pas trancher seule ; il faudrait une étape 4 longue.

**B0** : ✅ (rouverte sur demande, couche nouvelle, découpage écrit, puissance connue et faible).

## Étape 1 : exploration

Grille figée dans l'en-tête de [run_nq_orb_bougie.py](../../run_nq_orb_bougie.py), commitée avant tout calcul. Résultats : [[reports/nq_orb_bougie_report]].

**Résultat (2026-11-22)** : ❌ **B1 ratée de justesse**. La meilleure variante (stop 0,05 × ATR14, sortie à la clôture) fait +1,52 pt net par trade (t NW 3,16, Sharpe 1,00) sur 2010-06 → 2021-09, mais son DSR avec N = 26 vaut 0,948. Les cinq autres critères passent.
- Avant 2016 (jamais vu par cette règle), presque rien : +0,23 pt/trade pour la règle choisie, −0,11 pour R4.
- V0 (sans stop ni objectif) : +2,83 pts/trade, t 2,48, mais seulement t 1,27 contre « toujours long », et porté par 2018 et 2020.
- Les objectifs fixes (RR 1 à 3) font toujours moins bien que RR 10 ou la clôture.
- Le stop de la règle choisie ne fait que 5 à 6 ticks en 2010 : le résultat dépend d'un remplissage au prix du stop.

La réserve 2021-10-01 → 2026-08-28 reste réservée, non lue. Compteur 1 940 → 1 965.

## Suite : ES, YM et stop 1 ATR (2026-11-22)

Demande de l'utilisateur : même grille sur ES et YM, détail de stop 0,5 ATR / objectif 2R et 3R, et stop 1 ATR / objectif 2 ou 3 ATR (2R, 3R) sur les trois indices. Réserve « sortie » 2021-10-01 → 2026-08-28 déclarée aussi pour ES et YM dans [[wiki/reserves]] avant calcul. Grille figée dans l'en-tête de [run_orb_bougie_indices.py](../../run_orb_bougie_indices.py), commitée avant calcul : 56 essais (ES 27, YM 27, NQ 2), compteur 1 965 → 2 021. Puissance sur ES et YM : même ordre que NQ (faible). Résultats : [[reports/orb_bougie_indices_report]].

**Résultat de la suite** : ❌ **B1 sur les trois indices**.
- ES : meilleure variante V0 (+0,68 pt/trade, t 2,11), pas mieux que « toujours long » (t 1,24), DSR 0,002. Les stops serrés y perdent tous.
- YM : rien (meilleur t 0,39).
- NQ : stop 1 ATR et objectif 2 ou 3 ATR, +2,02 et +2,17 pts (t 1,75 et 1,87). C'est presque V0, car l'objectif n'est atteint que 0,2 à 1,3 % du temps. Stop 0,5 ATR / 2R : +2,23 pts (t 2,17), la plus régulière avant 2016 (+0,96).
- Le DSR de la règle NQ passe à 0,953 avec la famille de 28 propre à NQ, mais ce n'est qu'un effet de la dispersion de la famille. Avec la famille complète (81 variantes sur trois indices), il vaut **0,02**, et c'est ce chiffre qui fait foi.
- Compteur 1 965 → 2 021. Réserve non lue.


## Filtres F1-F3 sur la variante NQ stop 0,5 ATR / objectif 2R (2026-11-22)

Demande de l'utilisateur, après la proposition de filtres justifiés par un mécanisme : F1 « pas d'annonce à 10:00 ou 14:00 » (Subhani), F2 « volume de la 1ʳᵉ bougie > 1,5 × médiane 20 j » (stocks in play ; voisin du filtre M3c déjà raté sur une cassure), F3 « corps de la bougie > 0,05 × ATR14 ». F4 (sens du gap) écarté : double comptage avec le fade de gap post-0DTE. Grille figée dans l'en-tête de [run_orb_bougie_filtres.py](../../run_orb_bougie_filtres.py), commitée avant calcul ; référence d'un filtre = jours sautés ; n_famille = 85 ; compteur 2 021 → 2 024. Barre attendue : il faut à peu près doubler le Sharpe (≈ 1,5 par an) pour un DSR ≥ 0,95.
