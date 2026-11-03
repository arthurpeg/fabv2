# Filtre 3 nuits : sortie à 08:00 au lieu de 03:00, et comparaison avec notre règle de nuit

Date : 2026-11-03. **Exploratoire, hors compteur** : la variante 08h figurait déjà dans le rapport d'origine. Script : [run_nq_nuit_3n_8h_vbt.py](../run_nq_nuit_3n_8h_vbt.py). Sorties : `results/nq_nuit_3n_8h/` (`run.log`, `nuits_R.csv`, `annees.csv`, trades).

**Règles.** Elles sont identiques à [[reports/nq_nuit_3n_vbt_report]] (version corrigée), sauf la sortie, qui se fait à l'open de 08:00 ET. Le stop 2 × ATR M15 est surveillé jusqu'à la barre de 07:55. Le signal 3n ne change pas : il reste la somme des 3 nuits 20:05 → 03:00. Les 03h et 08h sont comparés sur les mêmes 2 750 nuits. vectorbt donne les mêmes sorties que la boucle à la main sur tous les trades.

## 1. Les chiffres d'origine sont retrouvés

Pour 3n 08h et 3n 08h SL, sur les 4 périodes, l'écart avec le rapport d'origine est ≤ 0,02 de Sharpe et ≤ 0,2 de t NW, sauf sur l'OOS 3n 08h sans stop (1,28 contre 1,38). La différence vient des nuits du changement d'heure, corrigées ici.

## 2. 03h contre 08h (1 NQ, 15 $ l'aller-retour)

| Période | 3n 03h SL : Sharpe | 3n 08h SL : Sharpe | 03h SL : Net $/an | 08h SL : Net $/an | 03h SL : Max DD $ | 08h SL : Max DD $ | 03h SL : % stoppés | 08h SL : % stoppés |
|---|---|---|---|---|---|---|---|---|
| 2016-2024 (IS) | **1,36** | 1,24 | 12 104 | **14 747** | **12 418** | 19 109 | 26 % | 44 % |
| 2016-2021 | **1,67** | 1,65 | 13 396 | **16 777** | **4 870** | 6 444 | 26 % | 43 % |
| 2022-2024 | **0,91** | 0,73 | 9 524 | **10 696** | **12 418** | 19 109 | 26 % | 48 % |
| 2025-08/2026 (OOS) | 1,59 | **1,82** | 31 245 | **46 096** | **8 301** | 13 928 | 30 % | 42 % |

Sans stop, la sortie à 08:00 est moins bonne : Sharpe 1,14 contre 1,33 sur l'IS, 1,28 contre 1,44 sur l'OOS, et le drawdown IS passe de 20 510 $ à 30 180 $.

**La tranche 03:00 → 08:00 seule n'a pas d'avantage.** Brut, elle fait +1,30 bps les nuits « 3n long » (t 0,89) et +0,03 bps les autres nuits sur l'IS. Sur l'OOS, c'est +1,42 bps (t 0,41) contre +1,90 bps. Rester jusqu'à 08:00 ajoute 5 heures d'exposition pour un gain non significatif, et le filtre 3n ne prédit pas cette tranche.

## 3. Comparaison avec notre règle (mom, 20:00 → 9:30), même coût (1 tick + 5 $), en R

| Période | mom | 3n 03h SL | 3n 08h SL | mom + 3n 03h SL | mom + 3n 08h SL |
|---|---|---|---|---|---|
| 2016-2026 · Sharpe (R) | 0,90 | **1,42** | 1,36 | 1,29 | 1,28 |
| 2016-2026 · R/an | 19,3 | 14,8 | 18,5 | 34,1 | **37,8** |
| 2016-2026 · Max DD R | −25,4 | **−21,0** | −25,7 | −27,8 | −34,5 |
| 2022-2024 · Sharpe (R) | 0,83 | 0,48 | 0,35 | **0,91** | 0,81 |
| 2025-08/2026 · Sharpe (R) | 1,20 | 1,39 | 1,32 | **1,48** | 1,43 |
| Corrélation par nuit avec mom (2016-2026) | — | +0,29 | **+0,39** | — | — |

Par année, 3n 08h SL perd en 2018, 2022 et 2023 ; mom ne perd qu'en 2022 (`annees.csv`).

## Lecture

1. **La sortie à 08:00 rapporte plus de dollars, mais pas un meilleur rapport rendement/risque.** Elle gagne environ +3,7 R/an et une E[R] plus haute (0,173 contre 0,138). En échange, le Sharpe baisse sur 2016-2024 et 2022-2024, le drawdown augmente de 22 % en R (54 % en $ sur l'IS), et 44 % des trades sont stoppés au lieu de 26 %. Le gain vient de la dérive normale de la prime de nuit sur 5 heures de plus, pas du signal (section 2).
2. **Le seul point en faveur de 08h est l'OOS** (Sharpe 1,82 contre 1,59, 1 NQ), soit 182 trades sur 20 mois, avec des intervalles de confiance très larges. Ça ne suffit pas pour préférer 08h.
3. **Face à mom, la variante 08h est moins complémentaire.** La corrélation passe de +0,29 à +0,39, parce que la fenêtre recouvre davantage celle de notre règle (jusqu'à 9:30). La combinaison avec 08h a un drawdown plus profond (−34,5 R contre −27,8) pour le même Sharpe. Si une combinaison est un jour pré-enregistrée, c'est 3n 03h SL qu'il faut tester avec mom, pas 08h.
