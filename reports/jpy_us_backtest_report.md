# Short du yen pendant la session US : backtest historique et pistes d'explication

*2026-11-19. Exploratoire, sur données **déjà vues** (≤ 2026-08-28). Aucun verdict : la preuve est le [[PREREGISTRATION_28]], sur des données nouvelles. Rien après le 2026-08-28 n'a été chargé. Le compteur est inchangé : c'est la même règle, et les variantes de coût sont seulement rapportées. Code : [run_jpy_us_backtest.py](../run_jpy_us_backtest.py). Sorties : `results/jpy_us/` (`summary.txt`, `trades_6J.csv`, `trades_spot.csv`, `equity.png`).*

Règle : short 6J (le yen baisse = long USDJPY) de 11:00 à 16:55 ET, 1 contrat de 12,5 M JPY, soit environ 85 à 110 k$.

## Futures 6J, 2016-01 → 2026-08-28 (portefeuille vectorbt)

| Coût | bp/trade | Gagnants | Sharpe annuel | P&L, 1 contrat |
|---|---|---|---|---|
| Sans coût | +2,03 | 54,6 % | 1,37 | +52 600 $ |
| **1 tick + 5 $ (standard)** | **+0,90** | 52,7 % | **0,61** | **+22 300 $** |
| 2 ticks + 5 $ | +0,28 | 51,4 % | 0,19 | +5 500 $ |

- Au coût standard, le résultat est +0,90 bp. Le moteur de R5b donnait +0,92 bp : deux calculs indépendants concordent.
- **Années :** 7 sur 11 sont positives au net. 2017, 2019, 2020 et 2021 sont légèrement négatives. Les meilleures sont 2022 (+2,2 bp), 2023 (+1,8) et 2025 (+3,1).
- **Risque :** l'écart type d'un jour vaut 240 $, le pire jour −1 681 $. Le pire creux atteint −7 100 $ (2020-2022), et le plus long creux dure 636 trades, environ 2,5 ans.
- **Sensibilité au coût :** très forte. Un tick de plus divise le résultat par trois. Toute la stratégie se joue sur l'exécution.
- **Jour de semaine** (rapporté seulement, ce n'est pas un filtre) : le vendredi est négatif (−0,9 bp), les autres jours sont entre +0,8 et +1,8 bp.

## Spot USDJPY Dukascopy, 2012-01 → 2015-12 (avant la période des futures)

| Coût | bp/trade | Sharpe annuel |
|---|---|---|
| Mid, sans coût | +2,34 | 1,52 |
| Spread réel bid/ask (médiane 0,67 bp) | +1,55 | 1,01 |
| Spread réel + 0,5 bp de commission | +1,05 | 0,68 |

## Pourquoi le yen baisse-t-il pendant la session US ? (même fenêtre, 2016-2026)

Zhang n'explique pas ce cas : pour son hypothèse (une devise s'apprécie pendant les heures étrangères), JPY est un contre-exemple. Ce que nos données permettent d'exclure, et ce qui reste :

1. **Ce n'est pas un artefact des futures** (portage, roulement). Le spot montre le même effet : −2,0 bp sur 2010-2015 (n° 27), +2,3 bp pour la règle sur 2012-2015. Le swap spot est payé à 17:00 NY, en dehors de la fenêtre.
2. **Ce n'est pas une hausse générale du dollar.** Dans la même fenêtre, l'euro monte contre le dollar (+0,41 bp). Si l'on régresse le yen sur l'euro et sur ES, il reste une constante de **−2,05 bp (t −5,7)**. C'est donc une faiblesse propre au yen.
3. **Ce n'est pas, en moyenne, le « risk-on » des actions US.**
   - Le yen baisse bien davantage les jours où ES monte (−3,6 bp, contre 0,0 les jours où ES baisse), ce qui va avec son rôle de monnaie de financement du carry trade.
   - Mais ES n'explique que −0,23 bp de la moyenne (corrélation −0,15). La constante reste.
4. **Ce n'est pas seulement la tendance du yen.**
   - En 2016-2020, le yen a **monté** sur 24 h (+0,86 bp/jour) tout en baissant dans la fenêtre US (−1,17). Il montait donc de +2,04 bp pendant le reste de la journée. C'est une rotation intraday : hausse hors des heures US, baisse pendant les heures US.
   - En 2021-2026, le yen baisse de −3,58 bp/jour, dont −2,65 dans la fenêtre US, soit 74 % de la baisse.

**Ce qui reste, ce sont des hypothèses que nos données ne permettent pas de trancher :**
- **(a) Flux de portefeuille ou de stocks des intermédiaires** : des achats nets de dollars contre yens concentrés dans les heures US, à l'inverse du schéma « devise domestique » de Breedon-Ranaldo. Pour le vérifier, il faudrait des données de flux (CLS, flux clients).
- **(b) Carry trade** : des positions financées en yen ouvertes ou reconstituées pendant les heures US. C'est compatible avec l'asymétrie des jours de hausse d'ES.
- **(c) Taux US** : USDJPY suit les rendements des Treasuries. Si ceux-ci montent en moyenne pendant les heures US, le yen baisse mécaniquement. Ce n'est pas testable sans futures de taux (ZN), que nous n'avons pas.
