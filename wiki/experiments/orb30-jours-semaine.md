---
type: experiment
updated: 2026-11-22
status: active
verdict: NQ vendredi réplique le papier (+0,19 R, t 3,50) mais ❌ B1 (DSR) ; lundi-jeudi rien ; réserve 2010-2015 gardée en attente
prereg: []
trials: 2073
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

**Résultat (2026-11-22)** : la règle **réplique le papier** sur NQ (période du papier : vendredi +0,219 R, t 3,34, contre +0,199 R, t 3,05 sur QQQ). Sur 2016-2026, la meilleure case est NQ vendredi : +0,190 R (+244 $ par trade), t NW 3,50, 10 années positives sur 11, meilleure que les autres jours (écart t 2,75). ES vendredi +0,113 R (t 2,02), YM rien. **B1 ❌ sur le seul DSR (0,846, N = 45)** ; les cinq autres critères passent. Ligne « À surveiller » dans [[wiki/phenomenes]]. Réserve 2010-06 → 2015-12 non lue (puissance ≈ 80 %). Compteur 2 025 → 2 043.


## Objectifs 2R et 3R (2026-11-22)

La règle de Subhani n'a pas d'objectif (il a essayé +2R et l'a rejeté). Demande de l'utilisateur : ajouter un objectif à 2R ou 3R. Grille figée dans l'en-tête de [run_orb30_tp.py](../../run_orb30_tp.py), commitée avant calcul : 3 actifs × {vendredi, tous les jours} × {2R, 3R} = 12 essais ; référence = même case sans objectif ; n_famille = 57 ; compteur 2 043 → 2 055. Exploration 2016-2026 seulement.

**Résultat des objectifs** ([[reports/orb30_tp_report]]) : aucun gain. NQ vendredi : +0,164 R avec 2R ou 3R, contre +0,190 sans objectif (écart t −0,99 et −1,47). Seul ES vendredi 3R fait mieux que sans objectif (+0,033 R, t 1,66), dans le bruit. B1 ❌ pour la meilleure case (DSR 0,77 avec N = 57). La règle de référence reste NQ vendredi sans objectif. Correction : le « Sharpe 2,33 » du rapport précédent était annualisé par √252 ; avec ≈ 50 trades par an, c'est ≈ 1,04.


## Lundi-jeudi : conditions C1-C3 (2026-11-22)

Demande de l'utilisateur : garder un objectif (prop firms) et faire fonctionner l'ORB les autres jours. Pour limiter la recherche de données : NQ seul, lundi à jeudi regroupés, objectif 2R, trois conditions justifiées. C1 range d'ouverture étroit (W < 0,5 ATR14 ; tableau 9 de Subhani), C2 veille NR7 (Crabel), C3 jours d'annonce à 10:00 ou 14:00. Grille figée dans l'en-tête de [run_orb30_filtres.py](../../run_orb30_filtres.py), commitée avant calcul ; référence = jours exclus ; n_famille = 60 ; compteur 2 055 → 2 058.

**Résultat C1-C3** ([[reports/orb30_filtres_report]]) : ❌ B1. Base lundi-jeudi objectif 2R : +0,011 R (t 0,46). C1 range étroit +0,003 R, C2 veille NR7 +0,044 R (t 0,76, DSR 0,08), C3 annonces −0,021 R ; aucun écart significatif avec les jours exclus. Le seul effet ORB 30 min sur NQ reste le vendredi. Compteur 2 055 → 2 058.


## Lundi-jeudi : biais EMA et réintégration (2026-11-22)

Idée de l'utilisateur : biais de tendance par EMA 20/50 sur 15 min, 1 h, 4 h et jour (vote majoritaire) ; cassure dans le sens du biais (ordre stop), réintégration contre le biais (après une cassure contre le biais et une clôture de retour dans le range, ordre limite sur la borne cassée). Objectif 2R. Variantes choisies par l'utilisateur : stop de réintégration à 1 W ou au-delà de la mèche ; égalité 2-2 traitée de trois façons (pas de trade, ORB classique, le jour tranche) ; NQ seul. Décomposition : règle complète, cassure seule, réintégration seule. 13 essais ; grille figée dans l'en-tête de [run_orb30_biais.py](../../run_orb30_biais.py), commitée avant calcul ; n_famille = 73 ; compteur 2 058 → 2 071.

**Résultat biais EMA et réintégration** ([[reports/orb30_biais_report]]) : ❌ B1. Meilleure variante : réintégration seule, stop 1 W, pas de trade si égalité, +0,045 R (t 1,40, DSR 0,009) ; règle complète +0,037 R (t 1,44) ; référence sans biais +0,015 R ; écarts avec la référence à t ≤ 0,55. Stop sous la mèche négatif. Un bug de sens (réintégrations à l'envers) a été trouvé à la vérification manuelle et corrigé avant lecture des résultats ; grille inchangée. Compteur 2 058 → 2 071.

## Décision du 2026-11-22 : réserve gardée en attente

L'utilisateur choisit de **ne pas ouvrir tout de suite** la réserve 2010-06 → 2015-12 : d'autres papiers pourraient apporter une idée utile pour les autres jours de la semaine. Conséquences, fixées dès maintenant :
- la réserve reste **réservée** et ne sert qu'à cette famille d'idées (ORB 30 min et ses variantes par jour) ; aucune autre règle ne doit la lire ;
- toute nouvelle variante se teste d'abord sur l'exploration 2016-2026, grille commitée avant calcul, et **s'ajoute à la famille** (N = 73 au 2026-11-22) ;
- le jour où la réserve sera ouverte : un seul pré-enregistrement, avec toutes les règles retenues à la fois (Holm si plusieurs) et le N de la famille à cette date ;
- candidate actuelle : NQ vendredi, range 9:30-10:00, cassure, stop 1 W, objectif 2R (+0,164 R, t 3,67 en exploration) ou sans objectif (+0,190 R).


## Lundi-jeudi : RSI 5 jours, approximation du gamma (2026-11-22)

Source : Zarattini, Aziz, Barbon 2024 (*Beat the Market*, section 4.5) : RSI 5 jours bas → teneurs de marché probablement en gamma négatif → tendances prolongées. Demande de l'utilisateur : suivre la cassure quand le RSI est bas, et jouer la réintégration quand il est haut (gamma contre la cassure). V1 filtre (RSI5 de la veille < 50, sinon rien) et V2 (RSI < 50 cassure, RSI ≥ 50 réintégration des deux côtés, stop 1 W). Objectif 2R, NQ, lundi à jeudi. Grille figée dans l'en-tête de [run_orb30_rsi.py](../../run_orb30_rsi.py), commitée avant calcul ; n_famille = 75 ; compteur 2 071 → 2 073.

**Résultat RSI 5 jours** ([[reports/orb30_rsi_report]]) : ❌ B1. V1 (filtre RSI < 50) +0,018 R, t 0,48 ; V2 (cassure / réintégration) +0,006 R. Cassure +0,018 R sous 50 contre +0,013 au-dessus, aucune pente par quintile ; réintégration à RSI haut −0,000 R. Compteur 2 071 → 2 073. Famille N = 75.


## Lundi-jeudi : forme et heure de la cassure, ordres limite (2026-11-22)

Demande de l'utilisateur : entrée sur clôture au-delà de la borne (bougie 1 min et 5 min, exécution à l'open qui suit), heure de la cassure (10:00-11:00, 11:00-13:00, 13:00-16:00), et ordres limite sur les bords du range (vente au haut, achat au bas, dès 10:00). NQ, objectif 2R, stop 1 W. 6 essais ; grille figée dans l'en-tête de [run_orb30_forme.py](../../run_orb30_forme.py), commitée avant calcul ; n_famille = 81 ; compteur 2 073 → 2 079.
