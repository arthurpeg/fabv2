# Règle NQ de nuit avec les spreads réels (bbo-1m Databento)

*2026-10-31. Code : [run_costs18.py](../run_costs18.py). Résultats : [results/costs18/](../results/costs18/). Données : bbo-1m NQ 2010–2026 et MNQ 2019–2026 (achat de 11,20 $). Re-estimation de coût sur les mêmes trades (compte 20:00, momentum 12-1, SL 2 / TP 5 ATR, sortie 9:30) : ce n'est pas une sélection, le compteur d'essais ne change pas.*

Coût d'un trade = demi-spread affiché à l'entrée + demi-spread à la sortie (meilleur bid/ask à la fin de la minute d'exécution) + commission. Spreads nuls, négatifs ou absents remplacés par 1 tick (aucun absent sur NQ, 0,06 % sur MNQ).

## Résultat

| Contrat | Commission A/R | Période | Coût moyen A/R | R/trade brut | R/trade au coût fixe (1 tick + 5 $) | **R/trade au coût réel [IC 95 %]** | R/an | Max DD | Sharpe |
|---|---|---|---|---|---|---|---|---|---|
| NQ | 5 $ | 2011-07 → 2026-08 | 3,4 ticks | +0,125 | +0,088 | **+0,076 [+0,033 ; +0,116]** | +18,9 | −26,0 R | 0,88 |
| MNQ | 0,50 $ | 2019-05 → 2026-08 | 3,2 ticks | +0,095 | +0,082 | +0,076 [+0,013 ; +0,135] | +19,0 | −25,7 R | 0,89 |
| MNQ | 1,24 $ | idem | 4,7 ticks | +0,095 | +0,082 | +0,067 [+0,004 ; +0,126] | +16,7 | −26,4 R | 0,78 |
| MNQ | 2,50 $ | idem | 7,2 ticks | +0,095 | +0,082 | +0,051 [−0,011 ; +0,110] | +12,8 | −27,4 R | 0,60 |

Spread moyen payé sur NQ : 2,45 ticks à l'entrée de 20:00, 2,29 à la sortie (1,9 aux sorties de 9:30, 2,5 aux SL et TP).

## Évolution par année (NQ, R totaux)

| | 2011* | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Spread à l'entrée (ticks) | 1,7 | 1,5 | 1,4 | 1,7 | 1,9 | 2,0 | 1,5 | 2,1 | 1,6 | 3,6 | 2,9 | 3,5 | 2,4 | 3,1 | 3,9 | 4,7 |
| R au coût fixe | −1,0 | +31,0 | +26,3 | +43,5 | +29,1 | +1,5 | +43,7 | +6,9 | +4,7 | +24,3 | +28,7 | −1,7 | +24,8 | +30,4 | +24,0 | +18,2 |
| R au coût réel | −3,2 | +26,5 | +22,8 | +39,2 | +24,4 | −3,1 | +41,1 | +4,6 | +2,8 | +21,4 | +25,8 | −4,2 | +22,4 | +28,0 | +21,5 | +16,5 |

## Ce qu'on en retient

1. **Le spread réel coûte environ 0,012 R de plus par trade** que le coût fixe : l'avantage passe de +0,088 à **+0,076 R par trade** (−14 %), et de +22 à +19 R par an. L'IC reste nettement positif.
2. Le spread en ticks a doublé depuis 2020 (de 1,5–2 à 3–5 ticks) parce que le prix de NQ a été multiplié par 4 ; mais le risque (2 ATR en points) a grossi dans la même proportion, si bien que le coût en R n'augmente pas autant.
3. **Sur MNQ**, la commission par contrat pèse 10 fois plus lourd par rapport à la valeur du point : à 1,24 $ aller-retour, l'avantage tombe à +0,067 R (IC tout juste > 0) ; au-delà de ~2,50 $, l'IC inclut zéro. Le choix du courtier compte.
4. Limites : seul le spread affiché est mesuré. Le glissement au-delà du meilleur prix sur un ordre stop dans un marché rapide, et l'impact d'une taille de plus de quelques contrats, ne sont pas couverts (il faudrait les trades tick par tick).
