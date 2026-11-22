# BB (bande de bruit) sur NQ avec SL et TP

*2026-11-22. Exploration demandée par l'utilisateur ([[wiki/experiments/m2-bande-bruit-nq]]). Grille figée et commitée dans l'en-tête de [run_bb_sltp.py](../run_bb_sltp.py) avant tout calcul (commit `b217c32`). NQ 2016-01 → 2026-08-28, **données déjà explorées : aucune confirmation possible ici** ; BB reste au registre des échecs (réouverture seulement sur des données postérieures au 2026-08-28). Rien n'est modifié dans `fab/` ni dans le bot. Compteur global : 2 109 (2 091 + 18 essais). Sorties : `results/bb_sltp/`.*

## Règle

BB de référence : VWAP exigé à l'entrée, contrôles toutes les 30 min, stop suiveur sur max(bande, VWAP), sortie à 16:00, 1 contrat, coût 0,50 pt. On ajoute **SL = k × ATR14** et **TP = RR × SL**, surveillés à la minute (SL prioritaire dans la même minute ; sortie à l'open en cas de saut). Après un SL ou un TP, BB peut reprendre une position aux contrôles suivants.
- **Mode A** : stop suiveur de BB conservé, plus SL et TP.
- **Mode B** : stop suiveur supprimé ; sorties uniquement SL, TP ou 16:00.

Vérification manuelle : vente du 02/08/2016 à 11:00 (5 793,20), SL à +0,25 ATR = 5 802,86, touché à 11:23 ; vente du 03/11/2016, TP à 2R touché à 15:32. Conformes.

## Résultats (1 contrat NQ, 20 $/pt)

| | Trades | Pts nets/trade | Gagnants | $ par an | Sharpe jour | Pire creux | Sharpe 2016-22 / 2023-26 | Écart avec BB (pts/jour, t) |
|---|---|---|---|---|---|---|---|---|
| **BB sans SL/TP** | 2 247 | +7,11 | 39 % | 29 300 | 1,13 | −39 300 $ | 1,29 / 1,04 | — |
| A, SL 0,25 ATR, TP 1R | 4 359 | +3,54 | 50 % | 28 300 | 1,39 | −21 000 $ | 1,49 / 1,30 | −0,20 (−0,23) |
| **A, SL 0,25 ATR, TP 2R** | 3 202 | +5,50 | 40 % | **32 300** | **1,49** | **−27 300 $** | 1,68 / 1,27 | +0,59 (0,75) |
| A, SL 0,25 ATR, TP 3R | 2 783 | +6,52 | 38 % | 33 300 | 1,48 | −26 700 $ | 1,62 / 1,35 | +0,78 (1,19) |
| A, SL 0,5 ATR, TP 1R / 2R / 3R | 2 908 / 2 407 / 2 306 | +5,2 / +6,3 / +7,0 | 44 / 40 / 39 % | 27 900 / 27 700 / 29 700 | 1,18 / 1,16 / 1,16 | −33 600 / −38 900 / −37 600 $ | ≈ 1,4-1,5 / 0,8-0,9 | ≈ 0 |
| A, SL 1 ATR, TP 1R / 2R / 3R | ≈ 2 250-2 370 | +6,6 / +7,3 / +7,0 | ≈ 40 % | 28 400 / 30 200 / 29 000 | 1,13-1,15 | ≈ −37 500 à −41 900 $ | ≈ 1,3 / 1,0 | ≈ 0 |
| B, SL 0,25 ATR, TP 1R | 4 124 | +3,99 | 55 % | 30 100 | 1,40 | −20 200 $ | 1,53 / 1,27 | +0,16 (0,17) |
| B, SL 0,25 ATR, TP 2R | 2 867 | +6,48 | 44 % | 34 100 | 1,47 | −31 400 $ | 1,66 / 1,25 | +0,95 (1,04) |
| B, SL 0,25 ATR, TP 3R | 2 415 | +7,77 | 41 % | 34 400 | 1,43 | −30 800 $ | 1,60 / 1,25 | +1,01 (1,14) |
| B, SL 0,5 ATR, TP 1R / 2R / 3R | 2 384 / 1 828 / 1 713 | +6,6 / +8,3 / +9,6 | ≈ 51-54 % | 28 600 / 27 900 / 30 200 | 1,00-1,05 | −34 900 / −45 600 / −48 600 $ | ≈ 1,2 / 0,8 | ≈ 0 |
| B, SL 1 ATR, TP 1R / 2R / 3R | 1 718 / 1 598 / 1 585 | +11,2 / +12,4 / +12,1 | 54 % | 35 400 / 36 200 / 35 100 | 1,11-1,16 | −32 200 $ | ≈ 1,2 / 1,15 | +1,2 à +1,4 (≈ 1,1-1,3) |

Tableau complet : `results/bb_sltp/grille.csv`.

**Meilleure case (Sharpe journalier) : mode A, SL 0,25 ATR, TP 2R.** P&L par année : 2016 +0,9 k$ · 2017 +4,6 · 2018 +63,7 · 2019 −3,8 · 2020 +26,1 · 2021 +48,8 · 2022 +86,7 · 2023 +47,2 · 2024 +39,4 · 2025 +16,5 · 2026 (→ août) +21,9 (BB sans SL/TP : −4,7 · +6,7 · +51,4 · +0,9 · +38,0 · +27,4 · +66,2 · +47,7 · +38,9 · +35,0 · +12,0). 10 années positives sur 11. 31,6 % des trades sortent au SL : un point de glissement sur chaque SL coûterait environ 1 900 $ par an.

Le DSR calculé par le script (≈ 1,0) n'est **pas comparable** au DSR de 0,03 qui a fait rejeter BB : il n'utilise que la dispersion de ces 18 variantes très semblables. Il ne doit pas être lu comme une validation.

## Lecture

1. **Un SL serré (0,25 ATR) améliore surtout le risque** : Sharpe 1,13 → 1,4-1,5, pire creux −39 300 $ → −20 000 à −31 000 $, avec un gain annuel égal ou un peu supérieur. Il coupe les mauvais trades tôt, et BB reprend une position au contrôle suivant si la tendance repart (d'où 30 à 90 % de trades en plus).
2. **Le gain moyen par jour ne change pas significativement** (écart avec BB à t ≤ 1,3 dans toutes les cases) : l'amélioration est une baisse de la dispersion, pas un gain prouvé.
3. **SL de 0,5 ou 1 ATR** : proche de BB, voire pire en creux. Le stop suiveur de BB fait déjà ce travail.
4. **Mode B (sans stop suiveur)** avec SL 1 ATR : le plus gros gain par trade (+12 pts) et par an (≈ 36 000 $), mais Sharpe ≈ 1,1-1,2 et creux −32 000 $ : pas mieux que BB en risque.
5. **Pour une prop firm** (perte maximale bornée), le mode A avec SL 0,25 ATR et TP 2R ou 3R est la version la plus intéressante : creux réduit d'environ 30 %, résultat stable sur 2016-2022 et 2023-2026 (Sharpe 1,68 puis 1,27). Mais ce choix est fait sur des données explorées, parmi 18 variantes : seul le forward peut le confirmer.

Compteur global : 2 109.
