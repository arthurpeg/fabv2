# Short du yen en session US avec SL / TP en ATR (RR 2)

*2026-11-19. Exploratoire, sur données **déjà vues** (6J 2016-01 → 2026-08-28) ; rien après le 2026-08-28, qui est le holdout du [[PREREGISTRATION_28]]. La grille de 12 combinaisons a été figée et commitée dans l'en-tête de [run_jpy_us_sltp.py](../run_jpy_us_sltp.py) avant le calcul. Compteur global : 1 798 (1 786 + 12). Sorties : `results/jpy_us_sltp/` (`grid.csv`, `summary.txt`, `trades_<ATR>_k<k>.parquet`).*

## Règle

- Short 6J à l'open de la barre de 11:00 ET.
- Sortie au premier de trois événements : SL = k × ATR, TP = 2 × SL, ou 16:55 ET.
- L'ATR est l'ATR de Wilder sur 14 bougies M5, M15 ou H1, calculé sur la dernière bougie terminée à 11:00. On teste k = 1, 2, 3 et 4.
- La simulation se fait sur des barres de 1 minute :
  - si une barre ouvre déjà au-delà d'un niveau, la sortie se fait à son open ;
  - si SL et TP sont touchés dans la même minute, on retient le SL.
- Le coût est le coût standard (1 tick + 5 $). La colonne « avec glissement » ajoute 1 tick sur chaque sortie au SL.

## Résultats (2 694 trades)

| Combinaison | Risque médian (bp) | % SL / TP / temps | Brut (bp) | Net (bp) | Net avec glissement | Sharpe net | P&L 1 contrat | Pire creux | Net 2016-20 / 2021-26 |
|---|---|---|---|---|---|---|---|---|---|
| **Sans SL/TP (règle du n° 28)** | — | 0 / 0 / 100 | +2,00 | **+0,88** | +0,88 | **0,59** | +22 300 $ | −7 100 $ | +0,32 / +1,36 |
| SL 1 / TP 2 ATR M5 | 5,3 | 64 / 34 / 2 | +0,34 | −0,79 | −1,19 | −1,35 | −22 200 $ | −23 400 $ | −0,92 / −0,67 |
| SL 2 / TP 4 ATR M5 | 10,6 | 50 / 20 / 30 | +0,82 | −0,31 | −0,62 | −0,31 | −9 100 $ | −16 100 $ | −0,42 / −0,21 |
| SL 3 / TP 6 ATR M5 | 15,9 | 35 / 8 / 57 | +0,96 | −0,16 | −0,38 | −0,14 | −6 300 $ | −18 700 $ | −0,58 / +0,20 |
| SL 4 / TP 8 ATR M5 | 21,1 | 23 / 4 / 73 | +1,25 | +0,13 | −0,01 | 0,10 | +1 200 $ | −15 800 $ | −0,50 / +0,68 |
| SL 1 / TP 2 ATR M15 | 8,3 | 58 / 28 / 15 | +0,76 | −0,37 | −0,72 | −0,43 | −10 700 $ | −18 100 $ | −0,50 / −0,25 |
| SL 2 / TP 4 ATR M15 | 16,5 | 33 / 8 / 60 | +1,08 | −0,05 | −0,25 | −0,04 | −2 900 $ | −17 400 $ | −0,42 / +0,27 |
| SL 3 / TP 6 ATR M15 | 24,8 | 18 / 3 / 80 | +1,43 | +0,30 | +0,19 | 0,23 | +5 600 $ | −14 100 $ | −0,46 / +0,96 |
| SL 4 / TP 8 ATR M15 | 33,1 | 9 / 1 / 90 | +1,82 | +0,69 | +0,64 | 0,51 | +16 900 $ | −7 500 $ | +0,05 / +1,26 |
| SL 1 / TP 2 ATR H1 | 14,8 | 38 / 10 / 52 | +0,92 | −0,20 | −0,44 | −0,17 | −7 000 $ | −17 500 $ | −0,57 / +0,12 |
| SL 2 / TP 4 ATR H1 | 29,5 | 12 / 2 / 86 | +1,68 | +0,56 | +0,49 | 0,41 | +13 000 $ | −9 200 $ | −0,19 / +1,21 |
| SL 3 / TP 6 ATR H1 | 44,3 | 5 / 0,3 / 95 | +1,93 | +0,81 | +0,78 | 0,57 | +19 800 $ | −7 400 $ | +0,13 / +1,40 |
| SL 4 / TP 8 ATR H1 | 59,0 | 2 / 0,2 / 97 | +1,94 | +0,81 | +0,80 | 0,57 | +20 400 $ | −7 100 $ | +0,25 / +1,30 |

## Lecture

1. **Aucune combinaison ne bat la règle sans SL/TP.** Plus le stop est serré, plus le résultat est mauvais. Les stops les plus larges (4 ATR M15, 3 à 4 ATR H1) ne font que rejoindre la référence : ils ne se déclenchent presque jamais (90 à 97 % des sorties se font à 16:55).
2. **Pourquoi.** L'effet est une dérive moyenne de 2 bp sur 6 heures, noyée dans un bruit dont l'écart type vaut environ 24 bp. Ce n'est pas un mouvement directionnel avec une grosse queue à droite.
   - Un TP à 2 × SL demande un mouvement de 10 à 60 bp dans la fenêtre, qui arrive rarement : 0,2 à 34 % des trades.
   - Un SL serré coupe les trades avant que la dérive ne s'accumule. Avec le SL 1 ATR M5, le brut tombe de +2,0 à +0,3 bp, alors que le coût reste le même.
3. **Le glissement aggrave les stops serrés** (−0,4 bp pour le SL 1 ATR M5) et ne change presque rien aux stops larges.
4. **En R** (le rendement divisé par le risque du SL), l'espérance vaut au mieux +0,01 à +0,02 R par trade. Aucune combinaison ne serait utile avec le dimensionnement en risque d'une prop firm.
5. **Biais de sélection.** Le meilleur des 12 est mécaniquement flatté. Ici, il ne dépasse même pas la référence : on ne garde rien.
6. **La règle du n° 28 ne change pas** : pas de SL ni de TP, comme le pré-enregistrement le fixe.

## Contrôle vectorbt

Sur SL 2 ATR M15, `Portfolio.from_signals` (stops sur OHLC) donne le même brut moyen : +1,07 bp contre +1,08. Il y a pourtant des écarts trade par trade, sur 36 % des trades, presque tous des sorties au SL ou au TP. Par défaut, vectorbt calcule le stop à partir de la **clôture** de la barre d'entrée (`stop_entry_price`), et non du prix d'entrée à l'open. Notre simulation utilise le prix d'entrée réel.
