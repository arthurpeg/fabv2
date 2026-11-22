# ORB 30 minutes de Subhani avec un objectif à 2R ou 3R (NQ, ES, YM)

*2026-11-22. Suite de l'étape 1 de [[wiki/experiments/orb30-jours-semaine]] (précédent : [[reports/orb30_jours_report]]). Grille figée et commitée dans l'en-tête de [run_orb30_tp.py](../run_orb30_tp.py) avant tout calcul (commit `4d51084`). Exploration 2016-01 → 2026-08 ; réserve 2010-06 → 2015-12 non lue. Compteur global : 2 055 (2 043 + 12 essais). Sorties : `results/orb30_tp/` (`grille.csv`, `summary.txt`).*

## Règle

Celle de Subhani (range 9:30-9:59, 1 R = largeur W, entrée à la cassure dès 10:00, stop fixe à 1 W), **plus un objectif à 2R ou 3R** ; sinon sortie à 16:00. Stop prioritaire si les deux niveaux tombent dans la même minute. Le papier n'a pas d'objectif et a rejeté +2R.

## Résultats (R net par trade ; référence = même case sans objectif, mêmes jours)

| Case | Sans objectif | **2R** | **3R** | Objectif atteint (2R / 3R) |
|---|---|---|---|---|
| **NQ vendredi** | **+0,190** (t 3,50) | +0,164 (t 3,67) | +0,164 (t 3,34) | 14 % / 5 % |
| NQ tous les jours | +0,053 | +0,040 | +0,048 | 12 % / 4 % |
| ES vendredi | +0,113 (t 2,02) | +0,102 (t 1,90) | **+0,146 (t 2,52)** | 20 % / 9 % |
| ES tous les jours | +0,034 | +0,013 | +0,045 | 18 % / 8 % |
| YM vendredi | +0,045 | +0,052 | +0,025 | 15 % / 4 % |
| YM tous les jours | +0,019 | +0,010 | +0,008 | 14 % / 5 % |

Écart avec la même case sans objectif : NQ vendredi −0,026 R (2R, t −0,99) et −0,025 R (3R, t −1,47) ; ES vendredi −0,011 (2R) et **+0,033 (3R, t 1,66)** ; ailleurs, entre −0,02 et +0,01.

**Sharpe** : la colonne `sharpe_an` de `grille.csv` annualise par √252 alors qu'un calendrier « vendredi » ne trade qu'environ 50 fois par an ; pour ces cases, il faut la multiplier par ≈ 0,45. NQ vendredi : ≈ 1,04 par an sans objectif, ≈ 1,06 avec 2R.

Par année, NQ vendredi (sans objectif / 2R / 3R) : 2016 +0,13 / +0,04 / +0,06 · 2017 −0,05 / −0,06 / −0,06 · 2018 +0,32 / +0,33 / +0,28 · 2019 +0,15 / +0,23 / +0,08 · 2020 +0,05 / +0,02 / +0,08 · 2021 +0,23 / +0,17 / +0,17 · 2022 +0,27 / +0,28 / +0,32 · 2023 +0,15 / +0,14 / +0,18 · 2024 +0,26 / +0,30 / +0,24 · **2025 +0,47 / +0,25 / +0,35** · 2026 +0,08 / +0,08 / +0,08.

## Fiche de la règle choisie (meilleur Sharpe : NQ vendredi, objectif 2R)

n 527 · net +0,164 R (médiane +0,036) · écart-type 1,09 R · t NW 3,67 · 51,8 % de gagnants · pire creux −13,3 R · 10/11 années positives · moitiés +0,096 / +0,232 · sans la meilleure année +0,147 · avec 1 tick de plus +0,159 · sans objectif +0,190 (écart −0,026, t −0,99) · **DSR (N = 57) 0,771**.

**B1 : ❌** : DSR sous 0,95, et l'objectif ne bat pas la règle sans objectif (critère 3).

## Lecture

1. **Un objectif fixe réduit un peu l'écart-type mais retire autant de gain** : sur NQ vendredi, le Sharpe par trade est presque inchangé (0,150 contre 0,147) et le gain moyen baisse. Le bénéfice de la règle vient en partie de rares grosses journées que l'objectif coupe (2025 : +0,47 sans objectif, +0,25 avec 2R).
2. C'est la conclusion du papier (objectif +2R rejeté) et celle de nos tests sur la règle de la 1ʳᵉ bougie.
3. **ES vendredi avec 3R** est le seul cas où l'objectif aide (+0,033 R, t 1,66), ce qui ne dépasse pas le bruit pour une case parmi douze.
4. Ajouter ces 12 essais fait baisser le DSR de la règle sans objectif : il faudra compter N = 57 si on va plus loin.

La règle de référence reste **NQ vendredi sans objectif**. Réserve 2010-2015 toujours non lue.
