# Pré-enregistrement n° 26 : le holdout NQ post-2026-08-28, dates de lecture fixées à l'avance

*2026-11-03, écrit et commité avant toute ouverture du holdout. À cette date, les données NQ 1 min postérieures au 2026-08-28 existent dans `cache/lse/NQ_lse_1m.parquet` (London Strategic Edge, symbole `NASDAQ100`). Seule leur couverture a été vérifiée : nombre de barres et trous. Aucun prix, rendement ou signal n'a été calculé dessus.*

## Pourquoi

Le holdout (données postérieures au 2026-08-28) ne s'ouvre qu'une fois ([[wiki/concepts/is-oos]]). Au 2026-11-03, il ne contient que 47 séances. Le calcul de puissance du jour (effets prudents, issus des hors-échantillon déjà faits ; test unilatéral à 5 %) donne :

| Règle | Effet supposé | Puissance à 1,5 an | à 3 ans | à 5 ans |
|---|---|---|---|---|
| H1 mom | +0,08 R/nuit (σ 1,36) | 31 % | 49 % | 67 % |
| H2 M2 | +0,10 σ/trade | 33 % | 52 % | 70 % |
| H3 3n SL | +0,05 R/trade (σ 0,84) | 18 % | 28 % | 39 % |
| H4 rebond | +0,15 σ/nuit | 23 % | 36 % | 51 % |

Une seule lecture rapide serait presque sans information. On fixe donc **trois dates de lecture**. Les deux premières ne peuvent conclure qu'à un succès net : seuil de Haybittle-Peto, z ≥ 3,0, qui laisse le risque global d'erreur proche de 5 %. Le verdict principal est rendu à la dernière date.

## Dates de lecture (données du 2026-08-29 au dernier jour inclus)

| Lecture | Données jusqu'au | Règle de décision |
|---|---|---|
| L1 (intermédiaire) | **2028-02-29** | Succès d'une hypothèse seulement si z ≥ 3,0 ; sinon on continue. Rien d'autre n'est conclu. |
| L2 (intermédiaire) | **2029-08-31** | Succès si z ≥ 3,0. Arrêt pour futilité (non contraignant) si z < 0. |
| L3 (finale) | **2031-08-29** | Verdict : p unilatéral, Holm sur les hypothèses non encore décidées, seuil 0,05. |

Entre deux lectures, il est **interdit** de calculer sur le holdout un prix, un rendement, un signal, un P&L ou du paper trading de ces quatre règles. On peut seulement télécharger les données chaque mois et vérifier leur couverture. Toute ouverture anticipée invalide ce pré-enregistrement, et elle doit être notée au journal.

## Hypothèses (4 essais ; compteur 1 734 → 1 738)

Chaque règle est figée telle qu'elle était à la date indiquée, avec le même code et le même coût.

- **H1 : règle NQ de nuit (mom).** Elle est figée au n° 11 (`run_prereg10.py` / `run_recolte1_atr.py`, compte 20:00) : signe du momentum 12-1, entrée 20:00 ET, SL 2 / TP 5 ATR M15, sortie 9:30 ET, coût 1 tick + 5 $. **Test : R net moyen par trade > 0.**
- **H2 : M2 (EMA 9:30).** Elle est figée au n° 25 (`run_nq_ema930_vbt.py`) : 1 contrat, sans stop, 15 $ l'aller-retour. **Test : P&L net moyen par trade > 0** (t HAC Newey-West, 5 retards).
- **H3 : 3n SL.** Elle est figée au n° 24 (`run_nq_nuit_3n_vbt.py`, version corrigée) : long 20:05 → 03:00 ET si la somme des 3 nuits précédentes est ≤ 0, stop 2 ATR M15, 15 $. **Test : R net moyen par trade > 0.**
- **H4 : rebond après forte baisse.** C'est la ligne « à surveiller » de [[reports/nq_nuit_r3_pente_report]]. Les nuits sont 20:05 → 03:00 ET (open à open), sans stop. On compare les nuits où r3 ≤ −50 bps (r3 = somme des rendements des 3 nuits précédentes) aux autres nuits. **Test : rendement net moyen (coût 1 tick + 5 $) des nuits r3 ≤ −50 bps, moins celui des autres nuits, > 0** (Welch unilatéral). Les nuits sont rapportées en bps.

Ce qui est seulement rapporté, sans verdict : les variantes (M2 + taille, M2 + stop, 3n sans stop), ES et YM, et les stats en $, Sharpe et drawdown.

## Données

- **Source principale : Databento `GLBX.MDP3`, `ohlcv-1m`, `NQ.v.0`**, achetée à chaque date de lecture pour la période du 2026-08-29 à la date de lecture. C'est la même source que tous les tests précédents.
- **Roulements.** Les nuits (H1, H3, H4) suivent la règle de `run_sessions.py`. Pour H2 (intraday), la série est non ajustée, comme dans le code figé.
- **Source de repli : London Strategic Edge** (`NASDAQ100`), si Databento n'est plus disponible. Ses roulements tombent à d'autres dates que Databento (vérifié sur 2026-01 → 08-28 : 2026-03-18, 2026-06-14 → 16). Avec cette source, on exclut tout trade dont la fenêtre contient un saut open / close précédent supérieur à 0,6 % à l'ouverture de Globex (18:00 ET), du 7 au 22 d'un mois de mars, juin, septembre ou décembre. Le nombre de trades exclus est rapporté.
- **Trous de données.** On applique les règles de chaque code figé : une séance sans barre de 9:30 ou de 9:35 est sautée (H2), et une nuit sans barre d'entrée ou de sortie est sautée.

## Interdit après calcul

On ne change ni les règles, ni les coûts, ni les seuils, ni les dates de lecture, ni la source de données, sauf si Databento est indisponible. On ne fixe pas de nouvelle date de lecture pour une hypothèse en échec, et on n'ajoute aucun filtre.
