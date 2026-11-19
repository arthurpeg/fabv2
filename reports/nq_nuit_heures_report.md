# Règle NQ de nuit : entrée à 19:00, 20:00 ou 21:00 ET, et corrélation des trois

*2026-10-31. Descriptif, non pré-enregistré, **hors compteur** : les heures d'entrée ont déjà été testées et comptées (n° 10 à 12, [[reports/recolte1_atr_report]]) ; le registre des échecs garde « affiner l'heure d'entrée » comme abandonné, ce calcul ne le rouvre pas. Code : [run_nq_nuit_heures.py](../run_nq_nuit_heures.py). Sorties : `results/nq_nuit_heures/` (run.log, summary.csv, trades.csv, nights.csv, by_year.csv, corr.csv).*

Seule l'heure d'entrée change : momentum 12-1, SL 2 ATR / TP 5 ATR (ATR 14 en M15), sortie 9:30 ET, NQ 2011-07-01 → 2026-08-28 (3 812 nuits ouvrées). Trades calculés par vectorbt (`run_recolte1_atr.simulate`, `Portfolio.from_signals` sur barres 1 minute). Net = 1 tick + 5 $ aller-retour. Contrôle : 20:00 redonne +0,125 R brut et +0,088 R net, les chiffres de [[reports/couts_reels_nq_nuit_report]].

## Rendements

| Entrée | Trades | R/trade net [IC 95 %] | R/trade brut | pb/nuit net | %/an net (1×) | Sharpe net [IC 95 %] | R/an net | Max DD | Gagnants | TP / SL |
|---|---|---|---|---|---|---|---|---|---|---|
| 19:00 | 3 769 | +0,076 [+0,040 ; +0,113] | +0,107 | 3,00 | 7,5 | 0,91 [0,45 ; 1,36] | 18,8 | −25,7 R / −12,5 % | 44,7 % | 11,5 % / 48,6 % |
| **20:00** | 3 787 | **+0,088 [+0,044 ; +0,131]** | +0,125 | 3,10 | 7,8 | **1,00 [0,54 ; 1,46]** | 22,0 | −25,4 R / −9,5 % | 42,8 % | 15,6 % / 52,1 % |
| 21:00 | 3 791 | +0,083 [+0,039 ; +0,126] | +0,124 | 2,58 | 6,5 | 0,87 [0,40 ; 1,32] | 20,7 | −34,2 R / −10,4 % | 41,1 % | 17,4 % / 54,3 % |

Les trois sont positives avec un IC entièrement au-dessus de 0. Les IC se recouvrent largement : rien ne départage les heures (conclusion déjà tirée au n° 12). Une entrée plus tardive touche plus souvent le TP (stop plus serré : l'ATR du soir baisse) mais aussi plus souvent le SL. Longs : ~89 % des trades pour les trois (le signe du momentum ne dépend pas de l'heure).

R nets par année (`by_year.csv`) : les années se contredisent souvent d'une heure à l'autre (2011 : +15 / −1 / −7 ; 2018 : +17 / +7 / −6 ; 2021 : +21 / +29 / −1 ; 2022 : +1 / −2 / +22 ; 2025 : +18 / +24 / +48).

## Corrélations (net)

| | 19:00 / 20:00 | 20:00 / 21:00 | 19:00 / 21:00 |
|---|---|---|---|
| Rendements par nuit, Pearson | **0,85** | **0,78** | **0,70** |
| Rendements par nuit, Spearman | 0,84 | 0,79 | 0,71 |
| R par nuit (nuits tradées par les trois, 3 766) | 0,85 | 0,79 | 0,71 |
| Rendements mensuels | 0,77 | 0,74 | 0,61 |
| R annuels | 0,77 | 0,61 | 0,37 |
| Même signe de R la même nuit | 90,1 % | 86,8 % | 83,4 % |

Les trois variantes sont **fortement corrélées** : elles tiennent la même position, dans le même sens, sur un intervalle commun (de 21:00 à 9:30 pour toutes) ; seule la première ou les deux premières heures diffèrent, et les stops se déclenchent à des moments différents. La corrélation baisse avec l'écart d'heure (0,85 à une heure, 0,70 à deux heures).

Un panier égal des trois heures fait 2,89 pb/nuit, Sharpe 1,01 et max DD −8,1 % : même Sharpe que 20:00 seul (1,00), drawdown un peu plus faible (−8,1 % contre −9,5 %). Combiner les heures ne diversifie presque pas ; pour des comptes de prop firm, trois comptes sur trois heures différentes resteraient très liés (voir l'exploratoire « comptes décalés » de [[reports/prereg18_report]] : la corrélation y était de 0,97 avec la même heure).
