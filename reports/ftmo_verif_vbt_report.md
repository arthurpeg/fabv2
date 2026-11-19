# Contrôle du moteur FTMO Python par vectorbt (compte A, mom, 2011-07 → 2026-08)

*2026-11-04. **Exploratoire, hors compteur.** Script : [run_ftmo_verif_vbt.py](../run_ftmo_verif_vbt.py). Sorties : `results/ftmo_verif_vbt/` (`run.log`, `trades.csv`).*

## Méthode

Le moteur Python ([run_ftmo_deux_comptes.py](../run_ftmo_deux_comptes.py), `Compte`) joue le compte A du chemin historique avec la règle des annonces, la politique cible + attente et l'objectif d'éval ramené au reste à faire. Il journalise chaque trade : date, phase, risque, objectif utilisé, coupe d'annonce, R et P&L.

Chaque trade est ensuite rejoué dans vectorbt (`Portfolio.from_signals`) sur les barres 1 min de la même série :
- **entrée** au close de la barre d'entrée, dans le sens du trade ;
- **stop** à la distance du trade ;
- **objectif** à la valeur choisie par le moteur (2 R, ou réduite) ;
- **sortie** à 9:30, ou à 8:19 les jours d'annonce quand le compte est financé ;
- **taille** = risque en $ / (distance du stop + coût CFD) ;
- **coût** de l'aller-retour en frais fixes.

Ce rejeu contrôle donc l'arithmétique du moteur, les tailles, l'objectif réduit, les coupes d'annonce et les sorties.

## Résultat

| | Moteur Python | vectorbt |
|---|---|---|
| Trades | 3 646 | 3 646 |
| P&L total de trading | +32 724,48 $ | +32 745,69 $ |
| **Trades identiques au centime près** | | **3 639 / 3 646 (99,81 %)** |
| Écart absolu maximal sur un trade | | 6,18 $ |
| Écart cumulé maximal sur le solde | | 21,22 $ (0,06 %) |

Les 7 trades qui diffèrent ont tous un **objectif réduit** (cible + attente en financé). Le prix a ouvert une barre au-delà de l'objectif. vectorbt exécute alors au prix d'ouverture, plus favorable, alors que le moteur compte l'objectif exact. L'écart va de +0,74 à +6,18 $ par trade, toujours en faveur de vectorbt : **le moteur est légèrement prudent.** Les 308 trades à objectif réduit et les 146 coupes d'annonce sont, sinon, identiques.

## Lecture

- **Le moteur Python est validé pour le compte A.** Les règles FTMO (plancher suiveur, règle des 50 %, rewards, rachats) ne font que décider la taille et l'objectif de chaque trade. Une fois ces décisions données, vectorbt retrouve le même P&L.
- **Le compte B (3n + M2) n'est pas rejoué.** Ses trades viennent des mêmes calculs vectorbt (`run_propfirm_combo.simule`), et leur P&L passe par la même formule du moteur. Son rejeu demanderait les barres 5 min des trois séries (2010-2015, 2016-2026, fenêtre déjà vue).
