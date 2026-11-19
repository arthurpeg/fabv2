# N° 24 : la stratégie transmise 3n hors échantillon, NQ 2010-2015

*2026-11-03. Règles et critères : [[PREREGISTRATION_24]] (commit 90085fb, avant calcul). Compteur global : 1 719 → 1 726 (7 essais). Code : [run_prereg24.py](../run_prereg24.py). Sorties : `results/prereg24/` (`run.log`, `tests.csv`, trades).*

## Verdict : ÉCHEC

| Critère | Résultat | Seuil |
|---|---|---|
| P1 : E[R] net de 3n SL > 0 | **+0,016 R**/trade, t 0,47, p 0,32 | p < 0,05 ❌ |
| P2 : nuits prises − nuits sautées (long avec stop) | +0,042 R, t 0,87, p 0,19 | p < 0,05 ❌ |
| E[R] > 0 sur les deux sous-périodes | 2010-06 → 2012-12 : **−0,031** ; 2013 → 2015 : +0,061 | toutes deux > 0 ❌ |

Sur NQ 2010-2015 (567 trades, 15 $ l'aller-retour), 3n SL fait +689 $/an, avec un Sharpe de 0,42 et un max DD de 2 218 $. Sur 2016-2024, il faisait +12 100 $/an et un Sharpe de 1,36. Les contrôles sont propres : aucun roulement pendant un trade (plus grand saut 13,7 bps), et vectorbt donne les mêmes sorties que la boucle à la main sur tous les trades.

## Tests secondaires (ne changent pas le verdict)

| | E[R] net | t | p | Sharpe ($) |
|---|---|---|---|---|
| NQ long toutes les nuits, sans stop | +0,006 | 0,22 | 0,41 | 0,38 |
| NQ long toutes les nuits, avec stop | −0,009 | −0,38 | 0,65 | 0,37 |
| NQ 3n sans stop | +0,041 | 1,15 | 0,13 | 0,42 |
| NQ 3n SL, sortie 08:00 | +0,085 | 1,65 | 0,0495 | 0,77 |
| ES 3n SL | +0,022 | 0,64 | 0,26 | 0,52 |
| YM 3n SL | +0,061 | 1,57 | 0,058 | 0,78 |

Aucun ne passe une correction pour 5 tests. 3n 08h (p 0,0495) et YM (p 0,058) sont à la limite, sans plus. Au coût du dépôt (10 $ sur NQ), 3n SL ferait +0,054 R par trade, ce qui ne change pas le verdict, puisque le coût était fixé à l'avance.

## Pourquoi : le coût et le filtre (diagnostic, après coup)

- **Le coût pèse lourd en R sur 2010-2015.** Le NQ cotait autour de 2 000 à 4 500 points, et le stop moyen n'était que de 8 points. Les 15 $ coûtent donc **0,11 R par trade**, contre environ 0,03 R sur 2016-2026.
- **En brut, il y a bien quelque chose :** 3n SL fait **+0,128 R par trade (t 3,6)**, et c'est pareil sur ES (+0,113, t 3,3) et YM (+0,176, t 4,5).
- **Mais ce brut vient surtout du long de nuit, pas du filtre.** Les nuits que 3n saute font elles aussi **+0,092 R brut (t 3,05)**, contre +0,128 pour les nuits prises. La [[wiki/concepts/prime-de-nuit|prime de nuit]] existe en 2010-2015. Le filtre 3 nuits y ajoute environ +0,04 R, ce qui n'est pas significatif (P2).
- **Ce que le filtre faisait sur 2016-2021 ne se retrouve pas.** Il y apportait environ +0,15 R, mais cet écart ne réapparaît pas sur des années jamais vues. Cela concorde avec [[reports/nq_nuit_r3_pente_report]] : la nuit brute après r3 ≤ 0 n'y valait que 1,6 bps de plus qu'après r3 > 0.

## Lecture

1. **Ce test ne valide pas le filtre 3 nuits.** Sur 2010-2015, la stratégie se ramène à « long NQ de nuit avec un petit avantage non significatif ». Son Sharpe de 1,36 sur 2016-2024 dépend en grande partie de la période où le filtre a été choisi. Les résultats FTMO de 3n ([[reports/propfirm_3n_vs_mom_report]]) sont donc à lire comme optimistes.
2. **Le décile le plus bas de r3 reste positif** dans les 6 échantillons, et reste « à surveiller ». Ce rebond après forte baisse est un effet plus étroit que 3n, et il n'est pas testé ici.
3. **Pour comparaison, notre règle de nuit (mom) avait passé son test hors échantillon** sur 2011-2015 (n° 11 : +0,116 R par trade, p 0,0015, coût 1 tick + 5 $).
