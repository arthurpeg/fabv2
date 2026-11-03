# NQ intraday « close de 9:30 contre EMA12 » (stratégie transmise) : backtest refait avec vectorbt

Date : 2026-11-03. **Exploratoire, hors compteur** : on refait un backtest externe sans rien choisir. Script : [run_nq_ema930_vbt.py](../run_nq_ema930_vbt.py). Sorties : `results/nq_ema930/` (`run.log`, `seances.csv`, `stats.csv`, trades). Données : NQ.v.0 Databento 1 min non ajusté, 2016-01-04 → 2026-08-28. Le holdout n'est pas touché.

Source : `scripts_strategies_NQ.zip`, scripts `bt_ema930.py`, `explore_c_ema930.py` et `bt_m2_ema930.py`. Le zip ne contient pas de stratégie ORB ; celle-ci est la deuxième stratégie du zip. Comparaison avec le rapport d'origine : **à faire quand ses chiffres seront transmis**.

## Règles (reprises telles quelles)

- **Sens.** Close de la barre 5 min de 9:30 ET comparé à l'EMA(12) des closes 5 min, Globex compris : au-dessus, long ; en dessous, short.
- **Exécution.** Entrée à l'open de 9:35, sortie au close de 15:55 (ou au close de la dernière barre les jours écourtés). 15 $ l'aller-retour par NQ.
- **C** : toutes les séances, sans stop. **D** : toujours long (référence).
- **M2** : on ne trade que si l'une des deux conditions est remplie :
  - force = |close 9:30 − EMA12| / ATR(14) M5 > 2,2 ;
  - retournement < −60 bps : le rendement 9:35 → 15:55 de la veille, signé dans le sens du jour, est inférieur à −60 bps.
- **Version retenue par l'original : M2 + taille / σ 20 j.** Le nombre de contrats vaut 1 / σ, divisé par la moyenne de 1 / σ sur les jours M2 de 2016-2024, arrondi à 0,1 (MNQ). σ est l'écart-type du mouvement 9:35 → 15:55, en points, sur les 20 séances précédentes. Variante possible : un stop fixe à 4 × ATR M15.

## Contrôles

- **Séances.** On trouve 2 747 séances et 1 067 jours M2. Par année, le nombre de trades M2 est identique à celui du post d'origine, sauf 2020 (123 contre 125) et 2026, où le post s'arrête plus tôt.
- **Sorties sans stop.** Les sorties vectorbt sont identiques à celles de la boucle à la main sur tous les trades.
- **Sorties avec stop.** 2 trades sur 1 067 diffèrent (2018-09-19 et 2021-10-25) : le stop est touché dans la barre d'entrée de 9:35. La boucle d'origine sort au stop dans cette barre. vectorbt ne teste le stop qu'à partir de la barre suivante et sort à l'open de 9:40, 4,5 et 16 points plus bas. L'écart est négligeable, mais c'est un comportement de vectorbt à connaître.
- **Roulements.** Aucun roulement pendant un trade (ils ont lieu à 00:00 UTC) ; le plus grand saut entre deux barres pendant un trade est de 42 bps.

## Résultats

| Variante | Période | Trades | Net $/an | bps/trade par NQ | Win % | PF | **Sharpe** | Max DD $ | t NW |
|---|---|---|---|---|---|---|---|---|---|
| D toujours long | IS 2016-2024 | 2 320 | 6 312 | 1,7 | 54,4 | 1,03 | 0,16 | 73 300 | 0,54 |
| C (signal, tous les jours) | IS | 2 320 | 23 873 | 5,8 | 51,2 | 1,12 | 0,62 | 87 665 | 1,96 |
| M2 | IS | 899 | 32 648 | 15,1 | 53,5 | 1,44 | 1,22 | 34 585 | 3,99 |
| **M2 + taille (retenue)** | **IS** | 899 | 19 806 | 15,1 | 53,5 | 1,43 | **1,28** | 19 253 | 4,05 |
| M2 + stop 4 ATR M15 + taille | IS | 899 | 16 735 | 12,1 | 42,8 | 1,41 | 1,31 | 15 421 | 4,17 |
| M2 + taille | 2016-2021 | 580 | 19 107 | 16,4 | 52,8 | 1,42 | 1,25 | 18 566 | 3,29 |
| M2 + taille | 2022-2024 | 319 | 21 203 | 12,8 | 54,9 | 1,44 | 1,34 | 19 253 | 2,37 |
| C | OOS 2025-08/2026 | 427 | 122 205 | 9,7 | 57,6 | 1,34 | 1,57 | 55 260 | 2,24 |
| M2 | OOS | 168 | 86 931 | 19,7 | 63,1 | 1,76 | 1,79 | 24 775 | 2,78 |
| **M2 + taille (retenue)** | **OOS** | 168 | 26 429 | 19,7 | 63,1 | 1,71 | **1,86** | 6 996 | 2,74 |

**Taille moyenne de la version retenue** : 1,30 NQ sur 2016-2021, 0,44 sur 2022-2024, 0,35 en 2025-2026. Le NQ bouge plus en points, donc la taille baisse. Les dollars ne se comparent pas d'une période à l'autre ; les bps par NQ et le Sharpe, si.

## Lecture (à confirmer avec les chiffres d'origine)

- **Le filtre M2 fait l'essentiel.** C seul a un Sharpe de 0,62 sur 2016-2024 (t 1,96) et son max DD de 88 k$ dépasse 3 ans de gain. Avec M2, on passe à 15 bps par trade, Sharpe 1,22, t 4,0. La taille inverse à la volatilité et le stop servent surtout à réduire le drawdown, pas à augmenter l'espérance.
- **Les gains sont concentrés.** Les 10 meilleurs trades font 32 % du net sur l'IS, mais 70 à 80 % sur 2022-2024 et 2025-2026. Les meilleures années, 2020, 2024 et 2025, portent l'essentiel.
- **M2 est positif dans toutes les sous-périodes** (Sharpe 1,25 / 1,34 / 1,86), contrairement à 3n, nul sur 2022-2024. Mais le hors échantillon 2025-2026 n'en est pas vraiment un. Les seuils 2,2 ATR et −60 bps viennent du post, et l'original compare ses nombres de trades à ceux du post **jusqu'en 2026**. Les seuils ont donc pu être réglés en voyant ces années. L'original a aussi exploré une grille de seuils.
- **Ce que disent nos échecs passés.**
  - Le registre contient le momentum intraday de Gao (nul depuis 2016) et « suivre la matinée US » (n° 20, ES et YM négatifs, 2010-2017 perdant).
  - Il contient aussi « le signe de la nuit prédit la séance US » (r = 0,000).
  - C (signe du close de 9:30 contre l'EMA, toutes séances) ressemble à ces idées, et son résultat faible est cohérent avec elles.
  - M2 est un filtre sur des journées extrêmes (gros écart à l'EMA, ou grosse perte de la veille dans le sens du jour) qui n'a pas d'équivalent dans le registre.
- **Le vrai test reste à faire** : le même protocole que le n° 24 (3n), sur NQ 2010-2015, jamais vu par cette stratégie, avec ES et YM en secondaire.
