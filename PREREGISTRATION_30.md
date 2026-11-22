# Pré-enregistrement n° 30 : règle de la 1ʳᵉ bougie NQ, stop 0,5 ATR et objectif 2R, sur la réserve « sortie »

*2026-11-22, écrit et commité avant tout calcul sur la réserve. Protocole : [PROTOCOLE.md](PROTOCOLE.md), étape 2 → 3. Parcours : stratégie.*

> **Écart au protocole, assumé et demandé par l'utilisateur.** La règle n'a **pas** franchi la barrière B1 (DSR de la famille complète ≈ 0,02), et elle a été désignée après coup, à l'œil, parmi 81 variantes de sortie, et non par le critère fixé d'avance (meilleur Sharpe). Le PROTOCOLE n'autorise pas l'ouverture de la réserve dans ce cas. L'utilisateur l'a demandée en connaissance de cause (2026-11-22), après qu'on lui a exposé la puissance faible et le coût (réserve consommée). Le verdict de ce test doit être lu avec cette réserve : une confirmation resterait fragile, un échec enterre la règle.

## Origine et fiche d'idée (étape 0)

- Source : Zarattini et Aziz, *Can Day Trading Really Be Profitable?* (SSRN 4416622, 2023 ; QQQ 2016-2023). Entrée du papier conservée, sortie remplacée.
- Registre des échecs : ligne ORB du 2026-10-12 (sans condition de réouverture), puis lignes du 2026-11-22 (sorties NQ, ES/YM, filtres). La réouverture repose sur la demande de l'utilisateur, pas sur une condition remplie.
- Registre des phénomènes : rien de proche.
- Mécanisme : non démontré (déséquilibre d'ordres accumulé avant l'ouverture, résumé par la 1ʳᵉ bougie).
- Taille attendue face au coût : +2,73 pts bruts par trade en exploration, contre 0,50 pt de coût (rapport 5,5).

Fiche : [wiki/experiments/nq-orb-bougie-sorties](wiki/experiments/nq-orb-bougie-sorties.md).

## Déjà vu

- Tranches explorées pour cette question : NQ 2010-06 → 2021-09-30 ([run_nq_orb_bougie.py](run_nq_orb_bougie.py), [run_orb_bougie_indices.py](run_orb_bougie_indices.py), [run_orb_bougie_filtres.py](run_orb_bougie_filtres.py)) ; ES et YM sur la même période.
- **Sur la réserve, la règle de base R4 (même entrée, stop à l'extrême de la bougie, 10R, levier du papier) a déjà été vue** : Sharpe net +0,17 sur 2023-01 → 2026-08 ([PREREGISTRATION_3](PREREGISTRATION_3.md), `results/replications.csv`). C'est pourquoi C2 compare la règle à R4 sur les mêmes jours.
- Exploration de la règle (NQ, 2010-06 → 2021-09, 1 contrat) : n 2 671, brut +2,73, net **+2,23 pts/trade**, Sharpe 0,69, t NW 2,17, 47,4 % de gagnants, pire creux −2 060 pts ; R4 mêmes jours +1,32 ; « toujours long » mêmes sorties +0,56 (t de l'écart 1,37). DSR : 0,64 (famille NQ de 28) ; ≈ 0,02 avec la famille complète de 81 variantes sur trois indices. Rapports : [[reports/nq_orb_bougie_report]], [[reports/orb_bougie_indices_report]], [[reports/orb_bougie_filtres_report]].
- Barrière B1 : t NW 2,17 ✅ ; DSR ❌ ; référence triviale t 1,37 ✅ ; deux moitiés > 0 ✅ ; sans la meilleure année > 0 ✅ ; 1 tick de plus > 0 ✅. **B1 ❌ (DSR).**

## Règle (figée)

- Actif, données : NQ, Databento 1 min (`fab.core.load("NQ")`), prix ajustés des roulements ramenés en prix bruts par le facteur (aucune position ne traverse un roulement). Heures de New York, jours ouvrés.
- Entrée : bougie 9:30-9:35 ET ; O1 = open de la 1ʳᵉ barre dans [9:30, 9:35), C1 = dernière clôture de 9:30 à 9:34. Pas de trade si |C1 − O1| ≤ 1 tick. Sens = +1 si C1 > O1, −1 sinon. Entrée à l'open de la barre de 9:35 (pas de trade si elle manque).
- Sortie : stop à 0,5 × ATR14 du prix d'entrée, objectif à 2 × cette distance. ATR14 = moyenne des amplitudes (plus haut − plus bas) des séances 9:30-16:00 des 14 séances précédentes. Surveillance sur les barres 1 min dès 9:35 incluse ; stop prioritaire si les deux niveaux tombent dans la même minute ; sortie à l'open si une barre ouvre au-delà ; sinon sortie à l'open de la 1ʳᵉ barre dans [16:00, 16:05).
- Sens, taille : 1 contrat, achat ou vente.
- Coût : coût standard 1 tick + 5 $ = 0,50 pt aller-retour.
- Code figé : [run_prereg30.py](run_prereg30.py), qui réutilise `simule` et `first_open` de `run_nq_orb_bougie.py` (commit `a49ca1a`). Rien d'autre ne change que les dates.

## Référence (fixée avant calcul)

- **C2** : R4 à 1 contrat sur les mêmes jours (même entrée ; stop à l'extrême de la 1ʳᵉ bougie, objectif 10R, sinon 16:00), comme annoncé dans la fiche pour une couche « sortie ».
- Rapportée sans être un critère : « toujours long » avec les mêmes sorties.

## Données de confirmation

- Réserve : NQ **2021-10-01 → 2026-08-28** (« réservée », question « sortie » seulement, depuis le 2026-11-22, [wiki/reserves.md](wiki/reserves.md)). Les séances de septembre 2021 servent seulement à amorcer l'ATR14 (données déjà explorées) ; aucun trade avant le 2021-10-01.
- Puissance de C1 (test unilatéral à 5 %, environ 1 150 trades) : **≈ 43 %** à l'effet de l'exploration (Sharpe par trade 0,043), **≈ 18 %** à la moitié de cet effet.

## Critères (PROTOCOLE.md, étape 3 ; tous requis)

- **C1** : net moyen > 0, p unilatéral NW (5 retards) ≤ 0,05.
- **C2** : net > R4 sur les mêmes jours (écart moyen > 0).
- **C3** : net > 0 sans la meilleure année de la réserve.
- **C4** : net > 0 avec 1 tick de coût en plus.

**Puissance < 50 %**. Verdict prévu :
- C1-C4 remplis : « confirmée hors protocole » (B1 non franchie). Étape 4 obligatoire avant tout argent réel : paper trading d'au moins 6 mois et 60 trades.
- Sinon : **rejet** (l'utilisateur ne veut pas d'étape 4 longue). Ligne au registre.

## Hypothèses et compteur

1 essai ; compteur 2 024 → 2 025.

## Interdit après calcul

On ne change ni la règle, ni le coût, ni la réserve, ni les critères, ni la référence. On n'ajoute aucun filtre (F3 compris). La réserve NQ « sortie » passe en « consommée » quel que soit le résultat ; celle d'ES et YM reste réservée.
