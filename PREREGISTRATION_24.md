# Pré-enregistrement n° 24 : la stratégie transmise 3n hors échantillon dans le temps, NQ 2010-2015

*2026-11-03, écrit et commité avant de lancer 3n sur ces données. Données : Databento `GLBX.MDP3`, `ohlcv-1m`, `NQ.v.0` (et `ES.v.0`, `YM.v.0`), 2010-06-07 → 2015-12-31, non ajustées, `cache/databento_2010/` (achat du n° 11).*

## Pourquoi

La stratégie 3n (scripts transmis le 2026-11-03, refaite dans [[reports/nq_nuit_3n_vbt_report]]) a son filtre choisi par son auteur sur NQ 2016-2024, parmi plusieurs candidats. Son seul hors échantillon est 2025 → 08/2026 (182 trades). Les années 2010-2015 n'ont jamais servi à construire cette stratégie : c'est un vrai test dans le temps, avec 5,5 ans de données.

## Ce qui est déjà connu de ces données (à déclarer)

[[reports/nq_nuit_r3_pente_report]] (exploratoire, même jour) a déjà calculé sur NQ, ES et YM 2010-2015 la nuit brute 20:05 → 03:00 selon r3 :
- NQ : +3,96 bps quand r3 ≤ 0, contre +2,33 bps quand r3 > 0 ;
- le décile le plus bas de r3 donne +6,8 bps (t 2,0).

Ces chiffres sont bruts, sans stop et sans coût. On sait donc déjà que l'écart brut entre nuits prises et nuits sautées est faible sur NQ. Cela rend le critère 2 ci-dessous **plus dur** à remplir, pas plus facile. Aucun trade avec stop, aucun R et aucun résultat en $ n'a été calculé sur 2010-2015.

## Règle (version retenue par l'original, rien ne change)

- **Entrée.** Long 1 contrat à l'open de la 1re barre 5 min entre 20:05 et 20:30 ET.
- **Sortie.** Open de la 1re barre entre 03:00 et 03:30 de la même séance CME. La séance est datée par la date locale naïve + 1 jour pour les barres à partir de 18:00, soit la version corrigée de [run_nq_nuit_3n_vbt.py](run_nq_nuit_3n_vbt.py).
- **Filtre 3n.** On n'entre que si la somme des rendements (bps) des 3 nuits 20:05 → 03:00 précédentes est ≤ 0.
- **Stop.** 2 × ATR(14) de Wilder sur barres 15 min, calculé sur la dernière barre terminée à l'entrée. Il est vérifié sur les plus bas 5 min ; le fill se fait au stop, ou à l'open en cas de gap.
- **Exécution.** vectorbt `Portfolio.from_signals`, avec le code de `run_nq_nuit_3n_vbt.py` inchangé, y compris la neutralisation du haut et du bas de la barre de sortie. Une boucle à la main sert de contrôle.
- **Coût.** **15 $ l'aller-retour** (le coût de l'original). 1 R = 2 ATR M15 × valeur du point. R net = (P&L en points × valeur du point − 15 $) / (2 ATR × valeur du point).
- **Données.** Série non ajustée. On contrôle que le plus grand saut open / close pendant un trade reste sous 30 bps, pour s'assurer qu'aucun roulement ne tombe pendant un trade. Si un trade dépasse ce seuil, il est rapporté, puis gardé.
- **Période.** Toutes les nuits du 2010-06-07 au 2015-12-31, sauf les 3 premières, qui n'ont pas de signal.

## Tests (7 essais ; compteur 1 719 → 1 726)

**Principaux (2), sur NQ :**
- **P1.** Le R net moyen par trade de 3n SL est > 0. On utilise un t HAC Newey-West (5 retards), en test unilatéral.
- **P2.** Le filtre apporte quelque chose. On mesure le R net moyen d'un long avec stop sur les nuits prises par 3n, moins celui des nuits qu'il saute, avec un t de Welch unilatéral.

**Secondaires (5) :**
- NQ 3n sans stop ;
- NQ long toutes les nuits avec stop ;
- NQ 3n SL avec sortie à 08:00 ;
- ES 3n SL et YM 3n SL (15 $ l'aller-retour, valeur du point de chaque contrat).

On rapporte aussi les stats en $, le Sharpe, le max DD et le résultat au coût du dépôt (10 $ sur NQ).

## Critères, fixés à l'avance

1. **Succès** si les trois conditions suivantes sont remplies :
   - P1 a p < 0,05 ;
   - P2 a p < 0,05 ;
   - le R net moyen de 3n SL est positif sur chacune des deux sous-périodes, 2010-06 → 2012-12 et 2013 → 2015.
2. **Succès partiel** (« prime de nuit seulement ») si P1 réussit mais que P2 échoue. Le gain viendrait alors du long de nuit, pas du filtre.
3. **Échec** sinon.

Les tests secondaires sont rapportés tels quels et ne changent pas le verdict.

## Interdit après calcul

Après le calcul, on ne change ni les heures, ni le nombre de nuits, ni le seuil, ni le multiple ou le type d'ATR, ni le coût, ni la période, ni les sous-périodes. On n'ajoute aucun filtre et on n'exclut aucune année.
