# Pré-enregistrement n° 31 : ORB 30 minutes de Subhani le vendredi sur NQ, réserve 2010-06 → 2015-12

*2026-11-22, écrit et commité avant tout calcul sur la réserve. Protocole : [PROTOCOLE.md](PROTOCOLE.md), étape 2 → 3. Parcours : stratégie.*

> **Écart au protocole, assumé et demandé par l'utilisateur (2026-11-22).** La règle n'a pas franchi B1 : DSR 0,846 avec N = 45 au moment du choix (la famille compte 81 essais aujourd'hui, en comptant les variantes lundi-jeudi testées depuis). Les cinq autres critères de B1 étaient remplis. Argument retenu pour ouvrir quand même la réserve : **l'hypothèse « vendredi » a été fixée par le papier (Subhani 2026), pas choisie par nous**, et la règle réplique le papier sur sa période (NQ +0,219 R, t 3,34 contre QQQ +0,199 R, t 3,05).

## Origine et fiche d'idée (étape 0)

- Source : Subhani, *Opening-range breakouts on Fridays* (SSRN 7589980, version du 15/11/2026, texte intégral lu ; QQQ 2018-05 → 2026-06).
- Registre des échecs : ligne ORB du 2026-10-12, rouverte sur demande ; lignes du 2026-11-22 sur l'ORB 30 min (vendredi : B1 ratée sur le DSR seul ; lundi-jeudi : six séries d'essais sans effet).
- Registre des phénomènes : « À surveiller » du 2026-11-22 (ORB 30 min le vendredi sur NQ).
- Mécanisme : inconnu (le papier écarte l'échéance mensuelle, le week-end et la compression de volatilité ; options 0DTE citées sans test).
- Taille attendue face au coût : +0,201 R brut par trade en exploration, coût médian 0,007 R sur NQ.

Fiche : [wiki/experiments/orb30-jours-semaine](wiki/experiments/orb30-jours-semaine.md).

## Déjà vu

- Tranche explorée pour cette question : NQ, ES, YM 2016-01-01 → 2026-08-28 ([run_orb30_jours.py](run_orb30_jours.py) et suites). La réserve 2010-06-08 → 2015-12-31 n'a jamais été lue par une règle ORB ; elle a servi à d'autres règles (n° 11, 12, 19, 24, 25, règle de la 1ʳᵉ bougie).
- Exploration, NQ, R net par trade (1 R = largeur du range) : **vendredi +0,190 R, t NW 3,50, n 527, 10/11 années positives** ; lundi −0,032, mardi +0,103 (t 1,75), mercredi +0,003, jeudi −0,003. Vendredi avec objectif 2R : +0,164 R, t 3,67. Rapports : [[reports/orb30_jours_report]], [[reports/orb30_tp_report]].
- Barrière B1 (vendredi, sans objectif) : t 3,50 ✅ ; DSR 0,846 ❌ ; autres jours (t écart 2,75) ✅ ; deux moitiés ✅ ; sans la meilleure année ✅ ; 1 tick de plus ✅.

## Règles (figées)

Code figé : [run_orb30_jours.py](run_orb30_jours.py) (fonction `trades`, commit `f40b125`) et [run_orb30_tp.py](run_orb30_tp.py) (fonction `trades`, commit `4d51084`), appelés par [run_prereg31.py](run_prereg31.py) avec les données de la réserve à la place de celles de l'exploration. Rien d'autre ne change.

- Actif, données : NQ, Databento 1 min, `cache/databento_2010/NQ_v0_1m_2010.parquet` (prix bruts ; aucune position ne traverse un roulement). Heures de New York, jours ouvrés.
- Range : plus haut ORhi et plus bas ORlo des barres 9:30 → 9:59 ; W = ORhi − ORlo ; 1 R = W.
- Entrée : première barre à partir de 10:00 qui dépasse ORhi (achat) ou passe sous ORlo (vente) ; les deux dans la même barre : la clôture tranche. Ordre stop sur la borne : prix = max(ORhi, open) à l'achat, min(ORlo, open) à la vente.
- Stop fixe à 1 W de l'entrée, surveillé dès la barre d'entrée.
- **Règle A (principale)** : pas d'objectif ; sortie à l'open de la première barre dans [16:00, 16:05).
- **Règle B** : objectif à 2 W de l'entrée (2R), stop prioritaire dans la même minute ; sinon 16:00.
- Vendredis seulement ; 1 contrat ; coût standard 1 tick + 5 $ = 0,50 pt aller-retour.

## Référence (fixée avant calcul)

Même règle (A ou B) les lundis, mardis, mercredis et jeudis de la réserve : C2 demande vendredi > moyenne des autres jours.

**Contrôle placebo** (rapporté, sans verdict) : règle A chaque jour du lundi au jeudi. Prédiction si le vendredi est spécial : ≈ 0 R pour chacun.

## Données de confirmation

- Réserve : NQ **2010-06-08 → 2015-12-31** (statut « réservée », question « ORB 30 min par jour de la semaine », depuis le 2026-11-22, [wiki/reserves.md](wiki/reserves.md)). Environ 280 vendredis.
- Puissance de C1 à l'effet de l'exploration (0,19 R, écart-type 1,29 R) : t attendu ≈ 2,45, **≈ 79 %** au seuil unilatéral de 5 %, ≈ 69 % au seuil de Holm le plus strict (2,5 %) ; à la moitié de l'effet, ≈ 34 %.

## Critères (PROTOCOLE.md, étape 3 ; tous requis, pour chaque règle)

- **C1** : net moyen > 0, p unilatéral NW (5 retards) ≤ 0,05 **après Holm sur les 2 règles (A, B)**.
- **C2** : net du vendredi > net moyen des lundis-jeudis (même règle, réserve).
- **C3** : net > 0 sans la meilleure année de la réserve.
- **C4** : net > 0 avec 1 tick de coût en plus.

Verdict :
- A et/ou B remplissent C1-C4 : « confirmée » (hors protocole : B1 non franchie). Étape 4 obligatoire avant tout argent réel (paper trading ≥ 6 mois et 60 trades).
- Sinon : rejet de la règle concernée ; ligne au registre.

## Hypothèses et compteur

2 règles jugées + 4 lectures placebo ; compteur 2 079 → 2 085.

## Interdit après calcul

On ne change ni les règles, ni le coût, ni la réserve, ni les critères, ni la référence. On n'ajoute aucun filtre ni objectif. Toute la réserve « ORB 30 min » (ES, NQ, YM 2010-06 → 2015-12) passe en « consommée » quel que soit le résultat (seul NQ est lu ; ES et YM sont déclarés consommés pour cette famille, par prudence).
