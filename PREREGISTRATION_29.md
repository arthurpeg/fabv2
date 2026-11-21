# Pré-enregistrement n° 29 : short du yen en session US après une hausse du yen (R4), avec stop

*2026-11-21, écrit et commité avant tout téléchargement et tout calcul sur USDJPY avant 2010, et avant toute donnée yen postérieure au 2026-08-28. Protocole : [PROTOCOLE.md](PROTOCOLE.md), étape 2 → 3 (comptant 2003-2009), puis étape 4 (forward 6J, dates du n° 28). Parcours : stratégie (H2) et phénomène (H1).*

## Origine et fiche d'idée (étape 0)

- **Source** : exploration à nous, sur l'effet confirmé du n° 27 (le yen baisse en session US). Elle rejoint Piccotti (SSRN 2446584) : retournement des rendements 24 h de l'USD/JPY pendant la séance de New York.
- **Registre des échecs** :
  - La ligne Piccotti (2026-11-19) avait pour condition de réouverture « une mesure montrant que le retournement se concentre dans une fenêtre intraday ». [[reports/jpy_us_filtres_report]] est cette mesure : la condition est remplie.
  - La ligne « stops sur le short yen » (2026-11-21) disait de ne rouvrir les stops que si l'effet changeait de forme. On les rouvre ici parce qu'un stop est **obligatoire en prop firm** : c'est une contrainte d'exécution, pas une recherche d'amélioration. Et le stop est choisi pour la règle filtrée R4, qui est nouvelle.
- **Registre des phénomènes** : même effet que « le yen baisse en session US », concentré sur certains jours. Ce n'est pas un nouvel effet, on ne le compte pas deux fois. Il est noté « À surveiller » depuis le 2026-11-21.
- **Mécanisme supposé** : après une hausse du yen (risk-off, rapatriement), la séance américaine en défait une partie. Non testé.
- **Taille attendue face au coût** : sur les jours R4, brut environ +3,2 bp (6J 2017-2026) contre environ 1,1 bp de coût standard sur 6J, soit un rapport de 2,9. Sur le comptant 2003-2009, le spread de l'époque est inconnu : il est mesuré au contrôle de qualité.

## Déjà vu

- **Tranches explorées** : 6J 2016-01 → 2026-08-28 en entier (n° 27, n° 28, backtests, distribution, SL/TP, trailing, filtres, stops sur R4) et USDJPY au comptant 2010-2015 (n° 27, règle 2012-2015). Voir `wiki/reserves.md`.
- **Exploration du filtre** ([[reports/jpy_us_filtres_report]], 8 essais) : R4 sur 6J 2017-01-30 → 2026-08-28.
  - 1 109 jours pris (46 %), net +2,09 bp, t NW 3,50.
  - Jours sautés −0,11 bp ; t de l'écart pris − sautés 2,43.
  - Sharpe quotidien 1,00 contre 0,64 pour la règle tous les jours.
  - DSR 0,99 à N = 8 et 0,98 à N = 42.
- **Barrière B1 de R4** : les 6 critères sont remplis. Le critère de choix entre R1 et R4 n'avait pas été écrit d'avance : R4 a été retenue parce qu'elle est la meilleure sur toutes les mesures.
- **Exploration du stop** ([run_jpy_us_r4_stops.py](run_jpy_us_r4_stops.py), 8 essais, `results/jpy_us_r4_stops/`). Le critère figé était le plus grand R net moyen ; il donne **S7, SL 2 ATR H1 avec TP 3R**.

| Variante | Risque médian | % SL | R net moyen | t NW (bp) | Pire creux |
|---|---|---|---|---|---|
| S7 (retenue) | 29,6 bp | 10,8 % | +0,041 | 2,73 | −13,3 R |
| SL 2 ATR H1 sans TP | | | +0,040 | | |
| SL 3 ATR H1 | | | +0,032 | | |
| SL 4 ATR H1 | | | +0,027 | | |
| SL 1,5 σ20 | | | +0,034 | | |

  Le TP de S7 n'est touché que dans 0,3 % des cas : en pratique, c'est le SL 2 ATR H1 sans TP.
- **Contrôle du code figé** (`run_prereg29.py --controle`, sur 6J déjà vu) : R +0,042, 1 110 trades. Il redonne S7, ce qui valide le code avant toute donnée nouvelle.

## Règle (figée)

- **Actif** : USDJPY. Short yen = long USDJPY. Pour 6J, les prix sont inversés.
- **Jours** : du lundi au vendredi, avec R4 vrai. R4 : le rendement USDJPY des 3 journées précédentes, de 16:55 ET à J−4 jusqu'à 16:55 ET à J−1, calculé sur le prix de sortie mid, est **négatif**. Autrement dit, le yen a monté.
- **Entrée** : open de la première minute dans [11:00, 11:05) ET. Au comptant, achat à l'ask.
- **Stop** :
  - SL = 2 × ATR de Wilder 14 sur bougies H1 (bid au comptant), dernière bougie terminée à 11:00 ET ;
  - TP = 3 × SL ;
  - les niveaux sont testés sur le bid ;
  - si une minute ouvre au-delà d'un niveau, sortie à son open ; si SL et TP sont touchés dans la même minute, on retient le SL.
- **Sortie sinon** : open de la première minute dans [16:55, 17:00) ET, au bid.
- **Taille** : risque fixe par trade. Le résultat est mesuré en R, c'est-à-dire le net divisé par la distance du SL.
- **Coût** :
  - comptant : spread réel (achat ask, vente bid) + 0,5 bp de commission par aller-retour ;
  - 6J : 1 tick + 5 $.
- **Code figé** : `run_prereg29.py`, commité avec ce document. Seuls les fichiers d'entrée et les dates changent.

## Référence triviale (fixée avant calcul)

- **Pour H1** : les jours sautés (R4 faux), même position sans stop.
- **Pour H2 (C2)** : la même position tous les jours, sans stop, en net par trade.

## Données de confirmation

**Étape 3 : USDJPY au comptant Dukascopy, de la première donnée disponible (attendue en 2003) au 2009-12-31.**
- Tranche **vierge** jusqu'ici. Elle est déclarée « réservée » dans `wiki/reserves.md` par ce commit.
- La bibliothèque ne sert pas de bougies minute avant 2012. Les barres 1 min bid et ask sont donc reconstruites depuis les fichiers de ticks horaires du datafeed (même source que `fetch_dukascopy.py --ticks`), sur 24 h, pour l'ATR H1 et la fenêtre.
- **Contrôle de qualité permis avant le calcul**, sans aucune moyenne de rendement : nombre de barres par jour, trous, spread médian par année.
- **Règle de qualité figée** : une année est retirée si moins de 90 % de ses jours ouvrés ont à la fois une minute d'entrée et une minute de sortie. Aucun jour n'est retiré pour cause de spread.

**Étape 4 : 6J après le 2026-08-28 (Databento 6J.v.0), aux dates de lecture du n° 28.**
- Lectures L1 le 2028-02-29 et L2 le 2029-08-31, avec un seuil z ≥ 3,0. Lecture finale le 2031-08-29 à p ≤ 0,05, avec Holm sur H1 et H2.
- Rien n'est calculé entre deux lectures.

**Puissance de C1**, pour environ 1 600 jours dont 46 % pris, un écart type d'environ 24 bp et Holm sur 2 hypothèses (seuil 2,5 %) :

| Hypothèse | À l'effet de l'exploration | À la moitié de cet effet |
|---|---|---|
| H1 (écart 2,2 bp) | ≈ 44 % | ≈ 13 % |
| H2 (+0,04 R, écart type ≈ 0,8 R, ≈ 740 trades), avant le spread de l'époque | ≈ 30 % | ≈ 9 % |

**La puissance est sous 50 %.** Un échec sur le comptant sera donc déclaré « non concluant » si l'écart estimé est positif, et la décision passera à l'étape 4. Un écart estimé **négatif** (H1) sera un rejet.

## Hypothèses (Holm sur 2, par jeu de données)

- **H1 (phénomène)** : brut mid du short sans stop, jours R4 − jours non R4 > 0. Test t de Welch, unilatéral.
- **H2 (stratégie)** : R net moyen de la règle complète > 0. t de Newey-West (5 retards), unilatéral.

## Critères (tous requis pour « confirmée »)

**H1**
- **C1** : p de Holm ≤ 0,05 et écart > 0.
- **C3** : écart > 0 sans la meilleure année.

**H2**
- **C1** : p de Holm ≤ 0,05 et R > 0.
- **C2** : net en bp par trade > net de la référence tous les jours sans stop.
- **C3** : R > 0 sans la meilleure année.
- **C4** : R > 0 avec un coût de plus : 0,5 bp au comptant, 1 tick sur 6J.

**Rapporté sans verdict** : le brut du short tous les jours sur 2003-2009, c'est-à-dire l'effet de base du n° 27 avant 2010, et les sous-périodes 2003-2007 et 2008-2009.

## Hypothèses et compteur

4 essais : H1 et H2 sur le comptant, H1 et H2 en forward. Compteur global : 1 822 → 1 826.

## Interdit après calcul

On ne change ni la règle, ni le filtre, ni le stop, ni le coût, ni les dates, ni les critères, ni la référence triviale. On n'ajoute aucun filtre. La tranche au comptant 2003-2009 passe en « consommée » quel que soit le résultat.
