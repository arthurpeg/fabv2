# Pré-enregistrement n° 28 : short du yen pendant la session US, sur données nouvelles seulement

*2026-11-19, écrit et commité avant tout calcul sur le yen (6J, USDJPY) après le 2026-08-28. À cette date, aucune donnée de yen postérieure au 2026-08-28 n'a été téléchargée : les fichiers 6J Databento et le spot Dukascopy s'arrêtent au 2026-08-28.*

## Origine et ce qui est déjà vu

- **Zhang (2018), Table 1** : le yen baisse contre le dollar pendant la session US, de 11:00 à 17:00 NY (−2,12 bp/jour, ***, 2010-2015).
- **Notre n° 27** ([[reports/zhang_fx_report]]) l'a retrouvé sur 2010-2015 (−2,03 bp). Il tient aussi hors échantillon 2016-2026-08 : −1,72 bp, t −4,3, négatif 16 années sur 17. Il est entré dans [[wiki/phenomenes]].
- **R5b** ([[PREREGISTRATION_3]], `results/replications.csv`) pariait l'inverse sur 6J : long du future 11:00 → 16:55, couplé à un short 02:00 → 08:15. Il a perdu −0,88 tick brut par trade en moyenne sur les deux jambes. Le sens short n'a jamais été testé comme règle.
- **Référence historique de la règle exacte ci-dessous**, calculée le 2026-11-19 avant ce texte (`uv run python run_prereg28.py --hist`) sur des données déjà vues :

| Période | Trades | Brut (bp/trade) | Net (bp/trade) | Sharpe net annuel | t NW net |
|---|---|---|---|---|---|
| 2016-01 → 2026-08-28 | 2 635 | +2,04 | +0,92 | +0,61 | 2,19 |
| 2016-2020 | 1 234 | +1,32 | +0,34 | +0,22 | 0,55 |
| 2021-2026-08 | 1 401 | +2,68 | +1,44 | +0,97 | 2,51 |

Toute l'histoire jusqu'au 2026-08-28 est donc vue. **Seules des données postérieures au 2026-08-28 peuvent servir de preuve.**

## Rapport au registre des échecs

La ligne « Saisonnalité des fixings comme stratégie autonome » (2026-10-12) ne se rouvre « que comme timing d'exécution ». **Cette condition n'est pas remplie** : H2 ci-dessous teste une stratégie. On la rouvre quand même, à la demande de l'utilisateur (2026-11-19), pour trois raisons :

1. Le sens testé (short du yen) est l'opposé de la jambe 6J rejetée.
2. L'effet brut (≈ 3,6 ticks) est au-dessus de la fourchette du registre (1 à 2,5 ticks pour 1,8 à 2 ticks de coût).
3. Le test ne porte que sur des données nouvelles.

Un succès de H2 ne vaut pas, à lui seul, autorisation de trader. Il faudrait aussi un passage en paper trading et une décision de l'utilisateur.

## Règle (figée)

- **Short 6J** (= le yen baisse = long USDJPY), chaque jour de séance CME : entrée à l'ouverture de la barre 1 min de 11:00 ET, sortie à 16:55 ET (juste avant la pause du CME de 17:00).
- **1 contrat, coût 1 tick + 5 $ l'aller-retour** (≈ 1,8 tick), comme R5b et toutes nos réplications FX.
- **Code figé** : [run_prereg28.py](run_prereg28.py), qui appelle le moteur de R5b (`fab/replications.py`, `run_legs` / `window`, commit `9bf1b68`). Seuls les fichiers d'entrée changent à chaque lecture.

## Hypothèses (2 essais ; compteur 1 784 → 1 786)

Les données vont du 2026-08-29 à la date de lecture.

- **H1 (phénomène)** : rendement brut moyen par trade > 0, soit « le yen baisse en session US ».
- **H2 (stratégie)** : rendement net moyen par trade > 0.

Pour les deux : t de Newey-West (5 retards), unilatéral, correction de Holm sur les 2 hypothèses.

## Puissance (effet de la référence historique, test unilatéral à 5 %)

| Hypothèse | Effet supposé | à 1,5 an | à 3 ans | à 5 ans |
|---|---|---|---|---|
| H1 brut | +2,04 bp (σ 23,8) | 51 % | 76 % | 92 % |
| H1 brut, effet divisé par 2 | +1,0 bp | 20 % | 31 % | 44 % |
| H2 net | +0,88 bp (σ 23,6) | 18 % | 27 % | 37 % |

Il faut le dire d'emblée : **H2 a peu de chances de conclure avant 5 ans**, même si l'effet est réel. H1 est le vrai test.

## Dates de lecture

Ce sont les mêmes que pour le n° 26.

| Lecture | Données jusqu'au | Règle de décision |
|---|---|---|
| L1 | **2028-02-29** | Succès seulement si z ≥ 3,0 (Haybittle-Peto), sinon on continue |
| L2 | **2029-08-31** | Succès si z ≥ 3,0. Arrêt pour futilité (non contraignant) si z < 0 |
| L3 (finale) | **2031-08-29** | p unilatéral, Holm sur les hypothèses non encore décidées, seuil 0,05 |

**Entre deux lectures, il est interdit** de calculer un prix, un rendement, un signal ou un P&L du yen (6J, USDJPY, et toute paire contre le yen) sur des données postérieures au 2026-08-28. Le paper trading de cette règle est interdit aussi, car il revient à regarder. On peut seulement télécharger les données et vérifier leur couverture. Toute ouverture anticipée invalide ce pré-enregistrement et doit être notée au journal.

## Données

- **Source principale : Databento `GLBX.MDP3`, `ohlcv-1m`, `6J.v.0`**, achetée à chaque date de lecture pour la période du 2026-08-29 à cette date, et raboutée au fichier `D:/quant-data/Cotations/forex/6J_v0_1m.parquet`. La fenêtre 11:00 → 16:55 ET ne contient jamais le roulement (00:00 UTC).
- **Source de repli : spot Dukascopy USDJPY** (`fetch_dukascopy.py`), mid, signe inversé, avec le même coût exprimé en bp (le coût moyen de la référence historique est 1,12 bp). Elle ne sert que si Databento n'est plus disponible.
- **Rapporté sans verdict** : la même règle sur le spot Dukascopy, au bid / ask réel plus 0,5 bp de commission (ordre de grandeur d'un compte ECN ou d'une prop firm).

## Interdit après calcul

On ne change ni la fenêtre, ni le sens, ni le coût, ni les dates, ni les seuils, ni la source (sauf indisponibilité). On n'ajoute aucun filtre (jour de semaine, régime, volatilité). On ne prolonge pas la date finale pour une hypothèse en échec.
