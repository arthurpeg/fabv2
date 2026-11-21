# Short du yen en session US avec trailing stop en ATR

*2026-11-21. Exploratoire, sur données **déjà vues** (6J 2016-01 → 2026-08-28) ; rien après le 2026-08-28, qui est le holdout du [[PREREGISTRATION_28]]. La grille de 8 essais a été figée et commitée dans l'en-tête de [run_jpy_us_trailing.py](../run_jpy_us_trailing.py) avant le calcul. Compteur global : 1 806 (1 798 + 8). Sorties : `results/jpy_us_trailing/` (`grid.csv`, `summary.txt`, `trades_<ATR>_k<k>.parquet`).*

## Règle

- Short 6J à l'open de la barre de 11:00 ET, sans TP.
- Le trailing stop est placé à d = k × ATR au-dessus du plus bas atteint depuis l'entrée. L'ATR est l'ATR de Wilder 14 sur M15 ou H1, calculé sur la dernière bougie terminée à 11:00. On teste k = 1, 2, 3 et 4.
- Sortie au stop ou à 16:55 ET.
- La simulation se fait sur des barres de 1 minute. Le high d'une minute est comparé au stop des minutes précédentes, puis le plus bas est mis à jour (choix prudent). Si l'open d'une minute franchit déjà le stop, la sortie se fait à cet open.
- Le coût est le coût standard (1 tick + 5 $). La colonne « avec glissement » ajoute 1 tick à chaque sortie au stop.

## Résultats (2 694 trades)

| Variante | Distance médiane (bp) | % stoppés | Brut (bp) | Net (bp) | Net avec glissement | Sharpe net | P&L 1 contrat | Pire creux | Stoppés : % gagnants, brut moyen |
|---|---|---|---|---|---|---|---|---|---|
| **Sans stop (n° 28)** | — | 0 | +2,00 | **+0,88** | +0,88 | **0,59** | +22 300 $ | −7 100 $ | — |
| Trailing 1 ATR M15 | 8,3 | 97 | +0,33 | −0,79 | −1,40 | −1,18 | −21 700 $ | −24 500 $ | 36 %, −0,3 |
| Trailing 2 ATR M15 | 16,5 | 62 | +0,65 | −0,47 | −0,85 | −0,44 | −13 900 $ | −20 100 $ | 21 %, −6,6 |
| Trailing 3 ATR M15 | 24,8 | 32 | +1,27 | +0,14 | −0,05 | 0,11 | +2 100 $ | −17 200 $ | 11 %, −14,5 |
| Trailing 4 ATR M15 | 33,1 | 17 | +1,61 | +0,49 | +0,39 | 0,36 | +11 700 $ | −9 400 $ | 9 %, −21,1 |
| Trailing 1 ATR H1 | 14,8 | 70 | +0,84 | −0,29 | −0,71 | −0,28 | −8 600 $ | −16 600 $ | 24 %, −4,7 |
| Trailing 2 ATR H1 | 29,5 | 23 | +1,37 | +0,24 | +0,10 | 0,18 | +4 600 $ | −15 100 $ | 9 %, −18,7 |
| Trailing 3 ATR H1 | 44,3 | 8 | +1,85 | +0,73 | +0,68 | 0,52 | +17 600 $ | −7 800 $ | 6 %, −31,4 |
| Trailing 4 ATR H1 | 59,0 | 4 | +2,00 | +0,87 | +0,85 | 0,62 | +22 000 $ | −7 100 $ | 6 %, −41,6 |

## Lecture

1. **Aucune variante ne bat la règle sans stop.** C'est la même gradation qu'avec SL/TP : plus le trailing est serré, plus le résultat est mauvais. Les plus larges (3 à 4 ATR H1) ne font que rejoindre la référence, parce qu'ils ne se déclenchent presque jamais (4 à 8 % des trades). Le Sharpe de 0,62 du trailing 4 ATR H1 contre 0,59 est du bruit : il porte sur 4 % des trades, et c'est le meilleur des 8.
2. **Pourquoi.** Un trailing stop ne gagne que si les gains viennent de mouvements longs et directionnels, qu'il laisse courir pendant qu'il coupe le reste. Ici, l'effet est une dérive de 2 bp noyée dans environ 24 bp de bruit, qui se répartit uniformément sur toute la distribution ([[reports/jpy_us_distribution_report]]). Le trailing coupe donc la plupart des séances bien avant 16:55, et le brut tombe avec le temps d'exposition : de +2,00 à +0,33 bp avec 1 ATR M15, alors que le coût reste entier.
3. **Il ne protège même pas le gain.** Les trades stoppés ont un brut moyen négatif dans toutes les variantes. Avec 1 ATR M15, 36 % seulement sortent gagnants, pour −0,3 bp en moyenne.
4. **Le glissement aggrave les trailings serrés** : −0,6 bp de plus avec 1 ATR M15.
5. **La règle du n° 28 ne change pas** : pas de stop.
