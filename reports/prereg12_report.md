# Pré-enregistrement n° 12 — la règle NQ de nuit face au bêta et aux références simples (2011-07 → 2026-08)

*2026-10-30. Protocole : [PREREGISTRATION_12.md](../PREREGISTRATION_12.md). Code : [run_prereg12.py](../run_prereg12.py). Résultats : [results/prereg12/](../results/prereg12/). Comparaisons descriptives sur des années déjà utilisées : ce n'est pas un nouveau test hors échantillon. Compteur global : 1 467.*

## Étape 1 — bêta et alpha face à l'achat-conservation de NQ

| | Valeur |
|---|---|
| Bêta de la règle sur le rendement journalier de NQ | **0,09** |
| Corrélation | 0,24 |
| Alpha annualisé [IC 95 %] | **+6,2 % [+2,5 ; +9,7]** |
| Rendement annualisé de la règle | +7,8 % (NQ : +18,1 %) |
| Part du rendement expliquée par le bêta | 21 % |
| Sharpe : règle / NQ / bêta × NQ | **1,00** / 0,86 / 0,86 |

Conclusion prévue : l'IC de α est entièrement > 0 → **plus que du bêta**. La règle n'est presque pas exposée au mouvement du Nasdaq sur la journée (β = 0,09), et 79 % de son rendement ne s'explique pas par cette exposition. C'est l'anomalie de nuit elle-même : la nuit rapporte plus que sa part du risque.

## Étape 2 — références (net, par nuit, 2011-07 → 2026-08)

| Référence | bp/nuit [IC 95 %] | Sharpe [IC 95 %] | Rendement/an | Max DD |
|---|---|---|---|---|
| **R0 règle : 20:00, SL 2 / TP 5, momentum** | **+3,1 [+1,6 ; +4,7]** | **1,00 [0,54 ; 1,47]** | +7,8 % | **−9,5 %** |
| R1 20:00 → 9:30 sans stop, momentum | +3,6 [+1,8 ; +5,4] | 0,86 [0,43 ; 1,31] | +9,0 % | −10,7 % |
| R2 20:00 → 9:30 sans stop, toujours long | +2,9 [+1,1 ; +4,8] | 0,70 [0,26 ; 1,15] | +7,3 % | −25,8 % |
| R3 18:01 → 9:30 sans stop, toujours long | +3,7 [+1,8 ; +5,6] | 0,85 [0,41 ; 1,30] | +9,3 % | −27,7 % |
| R4 00:00 → 3:00 sans stop, toujours long | +1,4 [+0,4 ; +2,4] | 0,78 [0,27 ; 1,25] | +3,5 % | −13,3 % |
| R5 16:00 → 9:30 toujours long (non intraday) | +4,3 [+2,2 ; +6,5] | 0,92 [0,47 ; 1,37] | +10,9 % | −30,5 % |
| R6 entrée aléatoire 18:01–3:00, SL 2 / TP 5, momentum (40 tirages) | +1,8 | 0,64 | +4,5 % | −12,9 % |

- **Heure d'entrée** : R0 fait +0,088 R/trade contre +0,046 en moyenne pour les entrées aléatoires (95e centile +0,063) ; R0 bat les 40 tirages. Critère prévu rempli. Mais les entrées aléatoires arrivent en moyenne vers 22:30, donc plus tard : l'écart reflète surtout la durée d'exposition (R3, entré à 18:01, fait mieux que R2, entré à 20:00), pas une vertu propre à 20:00.
- **Stops** : Sharpe R0 − R1 = +0,14 [−0,22 ; +0,50]. Critère prévu non rempli : les SL/TP ne font pas mieux que de tenir jusqu'à 9:30 de façon démontrable. Ils baissent un peu le rendement (+3,1 contre +3,6 bp) pour une volatilité un peu plus basse.
- **Filtre momentum** : ce n'est pas un test pré-enregistré, mais c'est l'écart le plus net du tableau. Sur le drawdown maximal, R1 (momentum) fait −10,7 % contre −25,8 % pour R2 (toujours long), aux mêmes heures, et le Sharpe passe de 0,70 à 0,86. Le filtre ne sert à rien en 2011–2015, puisqu'il était toujours long, mais il coupe la grosse perte de 2022.

## Ce qu'on en retient

1. **Ce n'est pas du bêta Nasdaq** : α ≈ +6 %/an, IC loin de zéro, bêta 0,09.
2. **La configuration exacte apporte peu** : toute façon d'être long NQ du début de soirée à 9:30 donne +3 à +4 bp par nuit. Les stops ATR n'apportent rien de démontrable, et l'avantage de 20:00 sur une heure aléatoire vient de la durée d'exposition.
3. **Ce qui compte vraiment** : être long tôt dans la nuit (la durée), et le filtre momentum pour le drawdown. Ce dernier point reste à confirmer sur d'autres phases baissières.
