# Règle NQ de nuit : stop au bord du range du soir (17:00 → 20:00) au lieu de 2 ATR

*2026-11-01. Exploratoire, non pré-enregistré, demandé en séance. Compteur global : 1 485 → 1 493 (8 variantes : TP 1 à 2,5 R par pas de 0,25, plus sans TP). Code : [run_nq_nuit_sl_range.py](../run_nq_nuit_sl_range.py). Sorties : `results/nq_nuit_sl_range/` (run.log, summary.csv, trades.csv, by_year.csv).*

## Règle testée

Tout est identique à la règle de référence (momentum 12-1, entrée 20:00 ET, sortie 9:30 ET, NQ 2011-07-01 → 2026-08-28, holdout non touché), sauf le stop :

- **Range du soir** = barres 1 min de 17:00 ET (clôture CME ; en pratique la reprise de 18:00) jusqu'à la barre d'entrée comprise, soit ~2 h.
- **SL** = plus bas du range si long, plus haut si short. 1 R = distance entrée → SL.
- **TP** = 1 ; 1,25 ; 1,5 ; 1,75 ; 2 ; 2,25 ; 2,5 R, et une variante sans TP (sortie 9:30).
- Nuits où la distance au SL est < 2 ticks : écartées (136 sur 3 787).
- Moteur, coûts et référence identiques à [[reports/nq_nuit_heures_report]] (vectorbt sur barres 1 min, net = 1 tick + 5 $ aller-retour). La référence SL 2 / TP 5 ATR redonne +0,088 R net.

## Le stop obtenu est beaucoup plus serré

Distance au SL : médiane **8,2 points NQ** (p10 1,5 ; p90 46,8), soit **0,86 ATR M15** en médiane (p10 0,26 ; p90 2,06), contre 2 ATR pour la référence. Le prix de 20:00 est en général près d'un bord du range de 2 h, et le stop se retrouve dans le bruit de la nuit.

## Résultats (net)

| Variante | R/trade net [IC 95 %] | 2011-15 | 2016-26 | R/an | Max DD R | Sharpe (1×) | Gagnants | PF | TP / SL / 9:30 | R/trade brut |
|---|---|---|---|---|---|---|---|---|---|---|
| TP 1 R | −0,098 [−0,130 ; −0,064] | −0,203 | −0,057 | −23,6 | −360 | 0,12 | 51 % | 0,82 | 50 / 47 / 3 % | +0,030 |
| TP 1,25 R | −0,100 [−0,133 ; −0,063] | −0,222 | −0,052 | −24,0 | −366 | 0,13 | 46 % | 0,84 | 44 / 53 / 4 % | +0,028 |
| TP 1,5 R | −0,076 [−0,113 ; −0,036] | −0,183 | −0,034 | −18,4 | −289 | 0,22 | 43 % | 0,88 | 39 / 55 / 5 % | +0,051 |
| TP 1,75 R | −0,065 [−0,104 ; −0,023] | −0,163 | −0,027 | −15,7 | −258 | 0,32 | 40 % | 0,90 | 35 / 58 / 7 % | +0,063 |
| TP 2 R | −0,046 [−0,089 ; 0,000] | −0,130 | −0,013 | −11,1 | −191 | 0,42 | 38 % | 0,93 | 32 / 60 / 8 % | +0,082 |
| TP 2,25 R | −0,047 [−0,091 ; 0,000] | −0,111 | −0,022 | −11,3 | −202 | 0,36 | 36 % | 0,93 | 29 / 62 / 10 % | +0,081 |
| TP 2,5 R | −0,033 [−0,080 ; +0,018] | −0,093 | −0,009 | −7,8 | −157 | 0,40 | 35 % | 0,96 | 26 / 63 / 11 % | +0,095 |
| sans TP | +0,009 [−0,104 ; +0,136] | +0,030 | +0,001 | +2,2 | −188 | 0,47 | 24 % | 1,01 | 0 / 74 / 26 % | +0,137 |
| **Réf. SL 2 / TP 5 ATR** | **+0,088 [+0,045 ; +0,133]** | +0,115 | +0,077 | **+22,0** | **−25** | **1,00** | 43 % | 1,16 | 16 / 52 / 32 % | +0,125 |

Source : `results/nq_nuit_sl_range/summary.csv` et `run.log`.

## Lecture

1. **Toutes les variantes TP 1 à 2,5 R perdent en net**, et l'IC 95 % est sous 0 ou touche 0. Le meilleur TP (2,5 R) fait −0,03 R/trade contre +0,09 R pour la référence.
2. **Ce sont les coûts qui tuent** : en brut, TP 2 à 2,5 R font +0,08 à +0,10 R, proche de la référence (+0,125). Mais avec un R médian de ~8 points, le coût fixe (~0,5 point aller-retour) pèse en moyenne 0,13 R par trade (écart brut − net, tiré par les stops de quelques points), contre 0,04 R avec 2 ATR.
3. **Le stop est trop proche** : 60 % des trades touchent le SL (TP 2 R) contre 52 % pour la référence, alors que le stop de référence est plus de 2 fois plus large. La nuit balaie souvent le bord du range du soir avant de partir dans le sens de la prime.
4. **Le drawdown en R explose** (−150 à −370 R contre −25) : à risque fixe par trade, les nuits à stop minuscule ont autant de poids que les autres et accumulent les pertes pleines.
5. **Par largeur de stop** (terciles en ATR, `run.log`) : le tiers serré perd −0,19 à −0,30 R/trade ; les tiers moyen et large sont à +0,02 à +0,06 R (TP 2 R : +0,05 / +0,06), sous la référence. Un plancher de distance serait un réglage choisi après coup sur ces données (même piège que le plancher de R du n° 19, [[reports/prereg19_report]]) : non retenu ici.
6. En Sharpe à 1× notionnel (sans normaliser par R), la variante range fait 0,1 à 0,5 contre 1,0.

## Conclusion

Stop au bord du range 17:00 → 20:00 : **rejeté**. Il remplace un stop de 2 ATR par un stop médian de 0,86 ATR, logé dans le bruit de la nuit, et les coûts transforment un edge brut à peine plus faible en perte nette, pour tous les TP de 1 à 2,5 R. La référence SL 2 / TP 5 ATR reste. Ligne ajoutée à [[wiki/Failed Ideas/ledger]].
