# 3n SL + M2 + stop, au plus un trade par jour (priorité à la nuit)

*2026-11-03. **Descriptif, hors compteur** : aucune règle nouvelle, on assemble des trades existants, recalculés avec le code figé. Les deux règles ont échoué hors échantillon (n° 24 et n° 25). Une combinaison ne servira qu'après un pré-enregistrement. Script : [run_combo_3n_m2.py](../run_combo_3n_m2.py). Sorties : `results/combo_3n_m2/` (`run.log`, `stats.csv`, `annees.csv`, trades).*

**Règle testée.** 3n SL est long de 20:05 à 03:00 ET. M2 + stop 4 × ATR M15 trade de 9:35 à 15:55. Si la nuit qui se termine le matin du jour J a un trade 3n, on ne prend pas M2 le jour J. C'est le seul ordre possible sans regarder l'avenir : le signal M2 n'est connu qu'à 9:30, après la nuit. Le coût est de 15 $ par aller-retour. 1 R = la distance du stop de chaque règle, donc chaque trade risque la même chose.

## Résultats en R

| Période | | 3n SL seul | M2 + stop seul | Les deux, tous les trades | **Max 1 / jour** |
|---|---|---|---|---|---|
| **2010-06 → 2015-12** (hors échantillon des deux règles) | R/an | 1,6 | 7,4 | 9,0 | **2,2** |
| | Sharpe | 0,20 | 0,57 | 0,58 | **0,17** |
| | Max DD (R) | −18,8 | −15,6 | −20,7 | **−26,2** |
| **2016-2024** (période de sélection) | R/an | 13,5 | 19,5 | 33,0 | **24,9** |
| | Sharpe | 1,31 | 1,29 | 1,80 | **1,59** |
| | Max DD (R) | −19,9 | −18,5 | −18,0 | **−18,0** |
| | t NW | 4,19 | 4,06 | 5,69 | 5,08 |
| **2025-08/2026** | R/an | 15,5 | 23,9 | 39,3 | **22,3** |
| | Sharpe | 1,45 | 1,79 | 2,35 | **1,63** |
| | Max DD (R) | −6,3 | −12,5 | −16,1 | **−12,7** |
| **Holdout vu, 2026-08-31 → 11-03** (46 séances) | R total | +8,7 | +1,9 | +10,6 | **+11,8** |

Pire journée : −2,1 R quand on prend les deux trades, contre −1,2 à −1,5 R avec la règle d'un trade par jour.

## Lecture

1. **La règle d'un trade par jour coûte cher.** Les jours où les deux signaux tombent, le M2 qu'on saute est un M2 normal : +0,20 R en moyenne sur 2016-2024 (+74,9 R laissés sur 367 jours), +0,21 R sur 2010-2015 (+38,7 R sur 184 jours). On perd donc environ un tiers du rendement (25 contre 33 R par an sur 2016-2024) et le Sharpe baisse (1,59 contre 1,80). Le drawdown, lui, ne baisse pas (−18,0 R dans les deux cas).
2. **Ce qu'elle apporte : la pire journée** passe de −2,1 R à environ −1,2 R. C'est utile seulement si une limite de perte par jour l'impose, comme les 3 % de FTMO : avec 1 % par trade, deux pertes le même jour ne font que −2 %.
3. **Les deux règles sont décorrélées** (corrélation journalière ≈ 0 sur toutes les périodes). Les additionner améliore donc le Sharpe sans augmenter le drawdown : 1,80 contre environ 1,30 pour chacune seule sur 2016-2024.
4. **Hors échantillon (2010-2015), la combinaison reste faible.** En prenant les deux, Sharpe 0,58 et 9 R par an ; avec un trade par jour, 0,17. Tout le rendement de cette période vient de M2 ; 3n n'y fait presque rien.
5. **Les 46 séances du holdout déjà vues** sont trop courtes pour conclure. La règle d'un trade par jour y a fait mieux par hasard : les 5 M2 sautés étaient perdants.
