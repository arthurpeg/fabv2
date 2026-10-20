# Pré-enregistrement n° 9 : momentum de fin de séance après un grand mouvement (ETF à levier, Shum et al.)

*2026-10-20, avant tout calcul de rendement ou de P&L. Papier : Shum, Hejazi, Haryanto et Rodier, « Intraday Share Price Volatility and Leveraged ETF Rebalancing », SSRN 2161057, texte intégral : [papers/ssrn_2026-10-13/c/ssrn-2161057.txt](papers/ssrn_2026-10-13/c/ssrn-2161057.txt). Quatrième de la revue du 2026-10-13, après les n° 6 à 8, tous rejetés.*

## Ce que dit le papier

- **Mécanisme** : les contreparties des ETF à levier et inverses (2×, 3×, −1×, −2×, −3×) rééquilibrent vers la clôture, **toujours dans le sens du mouvement du jour**. Le montant est M = A_{t−1}·(x² − x)·r, où r est le rendement depuis la clôture de la veille. Le flux est donc proportionnel au mouvement du jour, et quadratique en levier.
- **Données** : 346 actions du S&P 500, 2006-07 → 2011-07, plus 52 ETF à levier.
- **Stratégie « prix »** : si le marché a bougé d'au moins 2 % (en valeur absolue) depuis la clôture de la veille à la fin de la fenêtre 19, 20 ou 21 (14:15, 14:30 ou 14:45 ET), on achète (ou on vend) le marché jusqu'à la clôture, en ordre au marché à la clôture.
- **Résultats** : exécutés sur SSO et SDS (2×), environ 127 jours déclencheurs sur 2007-2010 :
  - « ETF-20 » (signal pondéré par l'encours des ETF, 14:30) : +0,66 %/jour en moyenne, 45 jours perdants sur 127 ;
  - « prix-21 » (14:45) : +0,60 %/jour.
  - Sur un ETF 2×, cela fait environ 0,3 %/jour sur l'indice.
- **Ce qui ne marche pas, selon le papier** : déclencher plus tard (fenêtres 22 à 26, après 14:45), ou avec un mouvement de moins de 2 %. Le papier mesure les prix comme la **moyenne** de la fenêtre de 15 minutes : la réplication utilisera des prix exécutables.

## Lien avec ce qui a déjà été testé

Le momentum intraday inconditionnel (Gao ; Baltussen : signe du rendement du jour → dernière demi-heure) a déjà été réfuté sur les indices dans ce dépôt (M1, R1, R2c dans [RESULTS.md](RESULTS.md)). Le test ici est différent sur trois points :
- **conditionnel** à un grand mouvement (|r| ≥ 2 %), seul cas où le papier trouve un effet ;
- **plus tôt** (14:15-14:45 au lieu de 15:30) ;
- **2016-2026**, alors que l'encours des ETF à levier (TQQQ, SQQQ, UPRO, SPXL…) est bien plus grand qu'en 2006-2011.

Tout l'échantillon est hors échantillon par rapport au papier.

## Données

Futures CME 1 minute, Databento, **ajustés en ratio aux roulements** (`cache/{ES,NQ,YM}_adj.parquet`, colonne `factor`), 2016-01 → 2026-08.
- **ES** : marché principal (S&P 500 : SSO, UPRO, SDS, SPXU…).
- **NQ** : secondaire (Nasdaq-100 : QLD, TQQQ, SQQQ, le plus gros encours d'ETF à levier depuis 2016).

Heures en **America/New_York**. Prix à l'instant T = open de la première barre dans [T, T + 5 min). Clôture du jour = close de la barre de 15:59.
- **C_{t−1}** = close de la barre de 15:59 du jour de séance régulière précédent.
- Un jour n'est retenu que si la veille et le jour même ont une barre à 15:59. Les demi-séances sont exclues comme jour de trade et comme veille de référence.
- Les prix ajustés en ratio rendent les rendements de la veille au jour J corrects même à travers un roulement.
- Coût en fraction du prix réel : (1 tick + 5 $ / valeur du point) / (prix ajusté / factor).

## Règles testées (16 essais, le compteur global passe de 208 à 224)

**Signal** : r = P(T) / C_{t−1} − 1. Si |r| ≥ s, on prend une position de sens = signe(r) à l'open de T, et on sort au close de 15:59.

| Dimension | Valeurs |
|---|---|
| Marché | **ES**, NQ |
| Heure de décision T | 14:15, **14:30**, 14:45, 15:30 |
| Seuil s | **2 %** (papier), 1 % |

2 × 4 × 2 = 16 essais. L'heure de 15:30 est l'heure de début du rééquilibrement indiquée par le papier, testée ici parce qu'avec un encours plus gros l'effet pourrait se déplacer vers la fin.

**Configuration principale, désignée à l'avance : ES, T = 14:30, s = 2 %.** C'est la fenêtre 20, la meilleure du papier, à son seuil.

## Coûts

- **Coût principal = 1 tick + 5 $ aller-retour** : ES 0,35 point, NQ 0,35 point. Grille : 0, 1, 2 et 5 pb aller-retour.
- Mêmes positions : la grille ne compte pas comme des essais en plus.

## Backtest et mesures

- **vectorbt** (`asym.backtest.simulate`, `Portfolio.from_orders`) : une colonne par règle, cible ±100 % du capital (1×, sans levier), frais = demi-coût par ordre. Rendement nul les jours sans déclenchement.
- On produit le même jeu complet de métriques que pour le n° 8 :
  - portefeuille : total, CAGR, volatilité, Sharpe, Sortino, drawdown maximal, Calmar, plus long drawdown, exposition, années positives, meilleure et pire année ;
  - par trade : taux de réussite, moyenne, gain et perte moyens, ratio gain/perte, PF, meilleur et pire trade, asymétrie et kurtosis ;
  - le tout par fenêtre **2016-2020**, **2021-2026-08** et sur l'ensemble, plus le détail année par année de la configuration principale.
- Lecture par trade en pb, avec le **nombre de jours déclencheurs par an** (attendu : quelques-uns en année calme, des dizaines en 2020, 2022 et 2025).

## Critères de décision (fixés avant exécution)

La configuration principale survit si elle remplit **toutes** ces conditions, au coût principal :
1. rendement moyen net > 0 et PF > 1 sur **chacune** des deux moitiés (2016-2020 et 2021-2026-08) ;
2. p < 0,05 pour la moyenne du rendement journalier net vectorbt > 0, par bootstrap stationnaire (blocs de 10 jours, 10 000 tirages) ;
3. p de permutation < 0,05 : 10 000 permutations du sens (±1) entre les jours déclencheurs, statistique = rendement moyen net par trade. On teste ainsi si suivre le mouvement bat un sens aléatoire sur les mêmes jours ;
4. **DSR > 0,95** avec N = 16 (le DSR avec N = 224 est rapporté).

Lectures secondaires, fixées elles aussi à l'avance :
- **NQ, 14:30, 2 %** : critères 1 à 3 rapportés comme réplication.
- **Profil temporel** : le papier prédit que le gain moyen par trade baisse quand T recule de 14:15 vers 15:30. C'est vérifié si le gain à 15:30 est inférieur à celui à 14:30, pour ES et pour NQ au seuil de 2 %.
- **Seuil** : le papier prédit que le seuil de 1 % donne moins par trade que celui de 2 %.
- Reality Check de White sur les 16 règles au coût principal.
- Dépendance aux épisodes : on rapporte le gain hors 2020.

**Puissance (à lire avant les résultats).**
- Seuil de 2 % : on attend de l'ordre de 50 à 150 jours déclencheurs sur ES en 10,7 ans, concentrés sur 2020, 2022 et 2025.
- Avec un écart type d'environ 1 % sur environ 1 h 30, l'erreur type du gain moyen est d'environ 10 à 14 pb. L'effet du papier (environ 30 pb sur l'indice) serait donc détectable de justesse (t ≈ 2 à 3). Un effet de 10 pb ne le serait pas.
- Le test est peu puissant : un échec n'est pas une preuve d'absence.

**Garde-fou.** Un Sharpe journalier supérieur à 2 ou un taux de réussite supérieur à 70 % déclenche d'abord une recherche de fuite (prix de T réutilisé, fuseau, demi-séances, roulement).

## Rapport

[reports/letf_report.md](reports/letf_report.md) et une section dans [RESULTS.md](RESULTS.md) : nombre d'événements par an, tableaux complets des métriques (16 règles × 3 fenêtres, grille de coûts), critères, DSR, permutations, Reality Check, profil temporel, courbes de capital, verdict.
