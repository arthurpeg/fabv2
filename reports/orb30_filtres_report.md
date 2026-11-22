# ORB 30 minutes NQ, lundi à jeudi, objectif 2R : conditions C1-C3

*2026-11-22. Suite de l'étape 1 de [[wiki/experiments/orb30-jours-semaine]] (précédents : [[reports/orb30_jours_report]], [[reports/orb30_tp_report]]). Grille figée et commitée dans l'en-tête de [run_orb30_filtres.py](../run_orb30_filtres.py) avant tout calcul (commit `d04655c`). NQ, exploration 2016-01 → 2026-08 ; réserve 2010-06 → 2015-12 non lue. Compteur global : 2 058 (2 055 + 3 essais). Sorties : `results/orb30_filtres/` (`conditions.csv`, `trades.csv`, `summary.txt`).*

## Règle de base

ORB 30 min de Subhani (range 9:30-9:59, 1 R = W, entrée à la cassure dès 10:00, stop 1 W), **objectif 2R** (demande prop firm), NQ, 1 contrat, coût 0,50 pt, **lundi à jeudi regroupés** : 2 106 trades, **+0,011 R** par trade (+0,76 pt), t 0,46.

## Résultats

| Condition | Trades pris | R net pris | R net exclus | t écart (R) | Points pris / exclus | t NW (pris) | Années + | DSR (N 60) |
|---|---|---|---|---|---|---|---|---|
| C1 range étroit (W < 0,5 ATR14) | 1 434 | +0,003 | +0,026 | −0,50 | −0,13 / +2,64 | 0,12 | 5/11 | 0,000 |
| **C2 veille NR7** (choisie) | 340 | **+0,044** | +0,004 | 0,62 | +0,34 / +0,84 | 0,76 | 6/11 | 0,077 |
| C3 annonce à 10:00 / 14:00 | 458 | −0,021 | +0,019 | −0,71 | +1,02 / +0,69 | −0,43 | 4/11 | 0,002 |

**B1 : ❌** pour la meilleure (C2) : t 0,76, DSR 0,08, écart avec les jours exclus à t 0,62. Seuls les critères « deux moitiés », « sans la meilleure année » et « 1 tick de plus » passent, sur un gain proche de zéro.

## Lecture

1. **Aucune condition ne crée d'avantage du lundi au jeudi.** La base est à +0,011 R ; les trois conditions restent entre −0,02 et +0,04 R, sans écart significatif avec les jours exclus.
2. **C1 (range étroit)** ne reproduit pas le tableau 9 de Subhani hors vendredi : ici les ranges étroits font +0,003 R, moins que les larges (+0,026 R). En points, ils perdent (−0,13 pt contre +2,64).
3. **C2 (NR7)** : légèrement positif, mais 340 trades seulement, et les jours vont dans tous les sens (mercredi +0,17, jeudi −0,10).
4. **C3 (annonces)** : négatif, porté par les jeudis d'annonce (−0,32 R, 52 trades).
5. Conclusion pour l'ORB 30 min sur NQ : **le seul effet est le vendredi**. Les autres jours, ni la règle ni ces trois conditions ne donnent rien.

Ligne au registre des échecs. La règle de référence reste NQ vendredi (sans objectif : +0,190 R ; objectif 2R : +0,164 R).
