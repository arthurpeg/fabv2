# Pré-enregistrement n° 12 : la règle NQ de nuit est-elle plus que du bêta, et plus qu'une exposition de nuit quelconque ?

*2026-10-30, avant calcul. Suite des n° 10 et 11. Ces tests portent sur 2011-07 → 2026-08, des années déjà utilisées (2016+) ou déjà testées (2011–2015) : ce sont des **comparaisons descriptives**, pas un nouveau test hors échantillon. Leur but est de dire ce que la règle apporte, pas de la re-valider.*

## Règle évaluée (inchangée)

NQ, momentum 12-1, entrée 20:00 ET, SL 2 ATR / TP 5 ATR (ATR 14 sur M15), sortie 9:30 ET, coût 1 tick + 5 $, exécution vectorbt `from_signals` 1 min (`run_recolte1_atr.simulate`). Données 2010-06 → 2026-08 raboutées (`recolte1.engine.USE_2010`). Nuits du 2011-07-01 au 2026-08-28.

## Étape 1 — bêta et alpha face à l'achat-conservation de NQ

- Série de la règle : rendement net de la nuit (fraction du capital, 0 les nuits sans trade), indexé par la séance NYSE qui suit.
- Référence : rendement close-to-close NQ de la même séance (16:00 ET veille → 16:00 ET), qui contient la nuit.
- Régression MCO r_règle = α + β · r_NQ. α annualisé (× 252). IC 95 % de α par bootstrap par blocs (blocs de 10 jours, 2 000 tirages) sur α + résidus.
- Rapportés : β, corrélation, α annualisé, Sharpe de la règle, Sharpe de NQ, Sharpe de β · NQ.
- **Conclusion prévue** : « plus que du bêta » si l'IC 95 % de α est entièrement > 0 ; sinon « pas distinguable d'une exposition au Nasdaq ».

## Étape 2 — références de nuit (toutes nettes du même coût)

| # | Référence | Sens |
|---|---|---|
| R0 | **la règle** (20:00, SL 2 / TP 5, momentum) | momentum |
| R1 | 20:00 → 9:30 sans stop, momentum | momentum |
| R2 | 20:00 → 9:30 sans stop, toujours long | long |
| R3 | 18:01 → 9:30 sans stop, toujours long (première minute de la journée CME) | long |
| R4 | 00:00 → 3:00 ET sans stop, toujours long | long |
| R5 | 16:00 → 9:30, toujours long (**non intraday CME**, rapporté pour comparaison seulement) | long |
| R6 | entrée à une minute tirée au hasard entre 18:01 et 3:00 ET, SL 2 / TP 5 ATR, momentum, sortie 9:30 ; **40 tirages** (graines 0 à 39), une entrée par nuit | momentum |

Mesures : rendement moyen net par nuit en bp [IC 95 %], Sharpe annualisé [IC 95 %], et R moyen par trade pour R0 et R6.

**Conclusions prévues :**
- « L'heure de 20:00 apporte quelque chose » si le R moyen de R0 dépasse le 95e centile des 40 moyennes de R6.
- « Les stops apportent quelque chose » si le Sharpe de R0 dépasse celui de R1 avec un IC de la différence entièrement > 0 (bootstrap apparié par blocs) ; sinon non.
- R2 à R5 sont descriptifs : ils situent la règle parmi les façons simples d'être long la nuit.

Compteur global : 1 459 → **1 467** (étape 1 : 1 ; étape 2 : R1 à R6, R6 compté une fois, + la comparaison des stops = 7).
