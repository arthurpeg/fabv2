# Pré-enregistrement n° 22 : lecture de niveaux sur NQ (measured move, règle des 80 %)

*2026-11-02. Règles et critères : [[PREREGISTRATION_22]] (commit 40404f4, avant calcul). Compteur global : 1 689 → 1 695 (6 essais : 2 règles × NQ, ES, YM ; le n° 21 est compté bien que pas encore lancé). Code : [run_prereg22.py](../run_prereg22.py). Sorties : `results/prereg22/` (run.log, results.csv, by_year.csv, trades.csv).*

## Origine

Captures TradingView « αλλο research » (NQ et QQQ, 26-30 octobre 2026) transmises en séance : indicateur « AVP Zones » (profil de volume ancré, HVN / LVN), niveaux GexSuite, rectangles de range et flèches de projection, total affiché « 2 438 points pour la semaine, 487 par jour ». Lecture faite en séance : rien ne relève de l'orderflow. Chaque flèche mesure la hauteur du rectangle d'à côté et a été tracée après coup ; aucune entrée, sortie ni stop n'est montrée. Les deux idées sous-jacentes ont été figées en règles exécutables :

- **R1** : cassure du plus haut / plus bas de la séance US de la veille, stop au milieu du range, cible = une hauteur de range au-delà (measured move).
- **R2** : règle des 80 % du Market Profile. Ouverture hors de la zone de valeur (70 % du volume) de la veille, acceptation pendant deux périodes de 30 min, cible au bord opposé, stop à l'extrême de la séance.

Les deux règles sont exécutées avec vectorbt sur barres 1 min, de 2010-06 au 2026-08-28, nettes d'1 tick + 5 $, sortie à 16:00 au plus tard.

## Résultats (R net par trade)

| | NQ R1 | NQ R2 | ES R1 | ES R2 | YM R1 | YM R2 |
|---|---|---|---|---|---|---|
| Trades (par an) | 1 900 (117) | 894 (55) | 1 805 (111) | 851 (53) | 1 820 (112) | 834 (51) |
| R net [IC 95 %] | +0,018 [−0,025 ; +0,061] | −0,014 [−0,052 ; +0,025] | −0,048 | +0,004 | −0,056 | −0,035 |
| p unilatéral / p Holm (NQ) | 0,21 / 0,43 | 0,77 / 0,77 | 0,98 | 0,42 | 1,00 | 0,94 |
| 2010-2017 / 2018-2026 | −0,028 / +0,058 | −0,012 / −0,017 | −0,103 / −0,003 | +0,003 / +0,004 | −0,084 / −0,033 | −0,061 / −0,012 |
| R brut | +0,035 | +0,003 | −0,016 | +0,040 | −0,034 | −0,011 |
| Cible atteinte / p0 marche au hasard | 11,7 % / 35,9 % | **45,3 %** / 65,6 % | 11,6 % / 36,1 % | 50,4 % / 64,7 % | 10,3 % / 36,0 % | 49,0 % / 65,7 % |
| Stop / sortie 16:00 | 31,7 % / 56,6 % | 17,8 % / 36,9 % | 33,9 % / 54,5 % | 19,5 % / 30,1 % | 32,6 % / 57,1 % | 20,6 % / 30,3 % |
| Sharpe (vrai nombre de trades) | 0,20 | −0,16 | −0,54 | 0,04 | −0,65 | −0,39 |
| Max DD (R) | −34 | −28 | −106 | −13 | −105 | −38 |
| Années positives 2011-2025 | 9 / 15 | 5 / 15 | 5 / 15 | 6 / 15 | 3 / 15 | 5 / 15 |
| Stop médian (points) | 40,6 | 43,3 | 13,5 | 12,5 | 111,5 | 113 |

p0 = d_stop / (d_stop + d_cible), probabilité d'atteindre la cible avant le stop sous une marche au hasard **sans limite de temps**. Avec la sortie forcée à 16:00, le taux observé ne se compare pas directement à p0. La mesure qui tranche est le R net (≈ 0 sous la marche au hasard, moins le coût).

## Verdict pré-enregistré

- **R1 : ÉCHEC.** +0,018 R/trade sur NQ, p Holm 0,43, négatif sur 2010-2017. ES et YM négatifs, même en brut. Le +0,058 R de NQ sur 2018-2026 n'est pas significatif ; sur toute la période, longs et shorts font pareil (+0,020 / +0,015 R).
- **R2 : ÉCHEC.** −0,014 R/trade sur NQ, p 0,77. La « règle des 80 % » atteint sa cible dans **45 %** des cas sur NQ, 49 à 50 % sur ES et YM, et non dans 80 %. Elle échoue aussi en brut (+0,003 R).

## Ce que ça dit des captures

- L'amplitude moyenne de la séance US de NQ en 2026 (jusqu'au 28 août) est de **415 points**, contre 487 dans le « total de la semaine ». Additionner les hauteurs de ranges revient à mesurer la volatilité du marché, pas un gain.
- Mises en règles fixées à l'avance, les deux lectures de niveaux qu'on devine derrière les captures ne font pas mieux que le hasard après coûts sur 16 ans et trois indices.

## Limites

- Une seule traduction de chaque idée. Les ranges de l'auteur sont tracés à la main (consolidations, sessions Globex), et ses zones AVP sont ancrées sur des périodes que la capture ne précise pas. Ce test ne réfute pas toutes les lectures de niveaux possibles. Il montre que les deux formulations standard et objectivables n'ont pas d'avantage.
- Profil de volume reconstruit à partir de barres 1 min (volume réparti uniformément entre le plus bas et le plus haut), et non tick par tick. C'est l'approximation habituelle des plateformes sur les historiques longs.
- Ce n'est pas un test d'orderflow : le volume n'est pas signé. Voir la ligne « pression vendeuse de fin de séance » du registre pour le coût d'un vrai volume signé.
