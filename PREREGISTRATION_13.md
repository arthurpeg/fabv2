# Pré-enregistrement n° 13 : filtres « à plat » pour réduire le drawdown de la règle NQ de nuit

*2026-10-31, avant tout calcul. Suite des n° 10 à 12 ([[wiki/experiments/nq-nuit-momentum]]). Le rapport descriptif `robust13` n'est pas un pré-enregistrement : ce document est le n° 13.*

## Objectif

La règle est longue 86 % du temps et subit des séries de pertes. On cherche un filtre qui met la position **à plat** certaines nuits, sans jamais en ajouter ni la retourner, pour réduire le drawdown maximal sans détruire le rendement. Le côté short n'est pas renforcé : il rapporte +0,013 R/trade contre +0,068 R en long (n° 12).

## Règle de base (inchangée)

NQ, compte 20:00 ET, momentum 12-1 (long si > 0, short si < 0), SL 2 ATR / TP 5 ATR (ATR 14 sur M15), sortie 9:30 ET, coût 1 tick + 5 $, exécution `run_recolte1_atr.simulate`. Mesure en R (1 R = 2 ATR / prix d'entrée), un trade par nuit. Un filtre ne fait que retirer des trades de cette liste : les trades restants sont identiques.

## Les 4 filtres (tous tirés de papiers de la récolte 1, connus avant 20:00 ET de la veille de la séance d)

Notations : séance NYSE d−1 = celle qui se termine avant l'entrée de 20:00 ET.

| # | Papier | On trade la nuit seulement si… |
|---|---|---|
| F1 | Jones-Pyun-Wang [4] (asymétrie) | NQ a monté entre 9:45 et 15:00 ET pendant la séance d−1 (demi-séances : pas de trade) |
| F2 | Abdi [8] (rebond après une nuit baissière) | la nuit précédente (clôture d−2 → ouverture d−1) a été négative |
| F3 | Berkman et al. [2] (attention) | le rendement close-to-close de d−1 au carré est dans le tercile haut de son historique passé (fenêtre expansive, ≥ 60 obs) |
| F4 | Vojtko-Hanicová [15] (tendance) | la clôture de d−1 est au-dessus de sa moyenne mobile 20 séances |

Les filtres s'appliquent quelle que soit la direction du momentum (porte ouverte ou fermée).

## Contrôle aléatoire

Retirer des nuits au hasard réduit aussi le drawdown, mécaniquement. Pour chaque filtre de taux de participation p (part des nuits gardées), on tire **500 sous-ensembles aléatoires** de même taille (graines 0 à 499) et on calcule la même réduction de drawdown.

## Critères (fixés à l'avance)

Mesures sur le compte 20:00, en R : R par an, drawdown maximal (somme cumulée chronologique des R), ratio R/an ÷ |DD|.

Un filtre est **retenu** s'il remplit, **sur la période de sélection 2016-01 → 2026-08** (trades 2017 → 2026) :
1. drawdown maximal réduit d'au moins **30 %** par rapport à la règle de base ;
2. R par an au moins égal à **80 %** de celui de la base ;
3. réduction de drawdown supérieure au **95e centile** des 500 filtres aléatoires de même participation.

Un filtre retenu est **confirmé** s'il remplit à nouveau 1 et 2 sur **2011-07 → 2015-12**, période où aucun filtre n'a été regardé. Le critère 3 y est rapporté sans être exigé.

Si aucun filtre n'est retenu, ou si aucun n'est confirmé, la règle reste sans filtre. On ne combine pas les filtres entre eux dans ce test.

## Compteur

1 467 → **1 471** (4 filtres ; la confirmation porte sur des filtres déjà comptés).

## Interdit après calcul

Changer les seuils (tercile, MM20, fenêtre 9:45–15:00), combiner des filtres, ajouter un filtre, changer les critères ou les périodes.
