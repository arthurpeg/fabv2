---
type: experiment
updated: 2026-11-22
status: active
verdict: en cours (étape 1)
prereg: []
trials: 1940
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
