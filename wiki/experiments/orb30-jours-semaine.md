---
type: experiment
updated: 2026-11-22
status: active
verdict: en cours (étape 1)
prereg: []
trials: 2025
---

# ORB 30 minutes, stop à une largeur de range, par jour de la semaine (Subhani 2026) sur NQ, ES, YM

**Une phrase** : cassure du range 9:30-10:00 ET, stop fixe à une largeur de range de l'entrée, sortie à la clôture ; Subhani (SSRN 7589980, texte intégral lu le 2026-11-22) ne la trouve rentable que le **vendredi** sur QQQ (2018-2026). On la teste sur les futures NQ, ES et YM, pour chaque jour de la semaine et pour tous les jours. Demandé par l'utilisateur le 2026-11-22.

## Étape 0 : fiche d'idée (2026-11-22, aucun calcul)

### 1. Déjà vu ?

- **Registre des échecs** : « Opening range breakout (30 min, 5 min, filtre volume ; ORB de Zarattini) » (2026-10-12, sans condition de réouverture) ; règle de la 1ʳᵉ bougie (2026-11-22, plusieurs lignes). **Réouverture** : demande explicite de l'utilisateur, et couche nouvelle jamais calculée chez nous (le jour de la semaine), tirée d'un papier qui publie son registre d'essais.
- **Déjà vu sur la tranche d'exploration** : M3a ([[PREREGISTRATION]]) est presque la même règle **tous jours confondus** (range 30 min, entrée à la cassure, stop à l'autre borne, sortie à la clôture ; différences : M3a ne trade pas si une barre casse les deux bornes, et son stop est l'autre borne et non « entrée − W », ce qui est identique sauf en cas de gap). Sharpe net, 1 contrat avec la taille de M3 : NQ +0,06 (2016-2022) / +0,95 (2023-2026) ; ES −0,27 / +0,12 ; YM −0,19 / −0,09 (`results/summary.csv`). La variante « tous les jours » de cette fiche n'est donc pas nouvelle ; le découpage par jour l'est.
- **Phénomènes** : aucun effet « jour de la semaine » au registre.

### 2. Mécanisme supposé

Inconnu. Subhani écarte l'échéance mensuelle des options, l'effet week-end et la compression de volatilité ; il cite les options 0DTE comme piste non testée. Sans mécanisme : noté. Le risque principal est un **effet calendaire trouvé après coup** (Sullivan, Timmermann et White 2001).

### 3. Taille attendue face au coût

Papier (QQQ, 2018-2026) : +0,199 R par trade le vendredi, 1 R = largeur du range ; coût du papier ≈ 0,035 R. Sur NQ, un range de 30 min vaut typiquement 0,4 à 1 % du prix, soit environ 60 à 150 pts en 2024 : le coût standard (0,50 pt) pèse moins de 0,01 R. Parcours **stratégie** ouvert.

### 4. Découpage des données

- Idée tirée d'un papier : la période du papier (2018-2026) est explorable. Il n'existe pas de données postérieures non consommées (après le 2026-08-28 : holdout du n° 26).
- On prend donc une **tranche plus ancienne** comme réserve : **NQ, ES, YM 2010-06-08 → 2015-12-31** (5,6 ans), jamais vue par une règle ORB (M3 portait sur 2016-2026). Elle a servi de réserve à d'autres règles (n° 11, 12, 19, 24, 25), mais jamais pour cette question. Déclarée dans [[wiki/reserves]] avant tout calcul.
- **Exploration** : 2016-01-01 → 2026-08-28. Elle contient la période du papier, d'où une vérification de réplication (signe et ordre de grandeur du vendredi sur NQ face à QQQ).

### 5. Puissance (avant calcul)

Vendredi, réserve : environ 280 trades. Effet du papier 0,2 R, écart-type ≈ 1,3 R : t attendu ≈ 2,5, **puissance ≈ 80 %** ; à la moitié de l'effet, ≈ 35 %.

**B0** : ✅ (réouverture sur demande, couche nouvelle, découpage écrit, puissance connue).

## Étape 1 : exploration

Grille figée dans l'en-tête de [run_orb30_jours.py](../../run_orb30_jours.py), commitée avant tout calcul. Résultats : [[reports/orb30_jours_report]].
