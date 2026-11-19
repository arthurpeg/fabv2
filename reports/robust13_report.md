# Robustesse de la règle NQ de nuit — régimes et pertes extrêmes (2011-07 → 2026-08)

*2026-10-30. Code : [run_robust13.py](../run_robust13.py). Résultats : [results/robust13/](../results/robust13/). Descriptif : aucun paramètre cherché, découpage par variables connues avant l'entrée. Les écarts entre niveaux ne sont pas des tests ; ce ne sont pas des filtres à ajouter.*

Séries nettes par nuit : **R0** = la règle (20:00, SL 2 / TP 5 ATR, momentum) ; **R1** = 20:00 → 9:30 sans stop, momentum ; **R2** = 20:00 → 9:30 sans stop, toujours long.

## Par régime (bp nets par nuit)

| Variable (connue avant l'entrée) | Niveau | Nuits | R0 [IC 95 %] | Sharpe R0 | R1 | R2 |
|---|---|---|---|---|---|---|
| Volatilité 20 j (terciles historiques) | basse | 1 121 | +2,9 [+1,3 ; +4,4] | 1,65 | +2,8 | +2,0 |
| | moyenne | 1 206 | +1,3 [−0,8 ; +3,3] | 0,57 | +1,0 | +1,1 |
| | haute | 1 485 | +4,8 [+1,7 ; +8,1] | 1,11 | +6,3 | +5,0 |
| Tendance (clôture vs MM200) | NQ > MM200 | 2 865 | +2,7 [+1,3 ; +4,2] | 1,07 | +2,8 | +2,4 |
| | NQ < MM200 | 947 | +4,2 [+0,4 ; +8,3] | 0,97 | +5,9 | +4,4 |
| Momentum 12-1 | positif | 3 390 | +3,2 [+1,6 ; +4,8] | 1,05 | +3,7 | +3,7 |
| | négatif | 422 | +2,2 [−2,5 ; +7,0] | 0,64 | +2,5 | **−3,7** |

- La prime ne disparaît dans aucun régime : positive par volatilité basse et haute, au-dessus et en dessous de la MM200. Le tercile de volatilité moyenne est le plus faible (IC qui touche 0).
- Quand le momentum est négatif, être toujours long perd (−3,7 bp/nuit) alors que suivre le momentum (short) gagne (+2,2 à +2,5). C'est l'effet du filtre, mais sur 422 nuits seulement, avec un IC très large.

## Par année (bp nets par nuit)

| | 2011* | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R0 | −0,7 | +3,7 | +1,6 | +3,7 | +8,0 | −0,2 | +2,2 | +1,3 | +1,7 | +7,1 | +4,0 | −0,3 | +4,0 | +4,6 | +3,3 | +4,1 |
| R2 (toujours long) | +6,7 | +3,4 | +3,5 | +3,4 | +4,9 | −3,0 | +4,5 | +0,4 | +5,9 | +11,3 | +2,5 | **−6,6** | 0,0 | +5,3 | +3,4 | +2,4 |
| NQ sur l'année | −1,7 % | +17,7 % | +36,0 % | +20,9 % | +9,4 % | +6,7 % | +30,9 % | −2,4 % | +36,0 % | +47,8 % | +27,1 % | **−33,8 %** | +47,1 % | +18,4 % | +15,2 % | +13,7 % |

*2011 : juillet → décembre ; 2026 : janvier → août.

R0 est positif 13 années sur 16. Les trois exceptions (2011 partiel, 2016, 2022) sont proches de zéro. En 2022, la seule vraie année baissière, toujours long perd −6,6 bp/nuit et la règle fait −0,3.

## Pertes extrêmes (nuits tradées)

| Série | Pire nuit | 1er centile | Nuits < −1 % | < −2 % | < −3 % | Asymétrie |
|---|---|---|---|---|---|---|
| **R0 (avec SL/TP)** | **−2,7 %** | −0,8 % | **22** | **1** | **0** | **+1,7** |
| R1 (sans stop, momentum) | −4,5 % | −1,9 % | 193 | 32 | 7 | 0,0 |
| R2 (sans stop, toujours long) | −3,8 % | −1,9 % | 190 | 33 | 9 | 0,0 |

Pires nuits sans stop : 5 août 2024 (débouclage du carry yen, −3,8 %), 8 septembre 2020, 6 mars 2020, 15 janvier 2016, 28 février 2020. La règle avec stops ne perd que −0,5 à −1,4 % ces nuits-là.

Dans les barres 1 minute, aucun stop n'a glissé au-delà de −1,3 R (moyenne des SL : −1,04 R coût compris). C'est logique : l'entrée à 20:00 évite le trou de réouverture du dimanche. Les données 1 minute ne montrent pas les sauts à l'intérieur d'une minute ; un krach éclair peut glisser plus loin en réel.

## Ce qu'on en retient

1. **La prime de nuit de NQ est robuste aux régimes** : elle ne dépend ni du niveau de volatilité, ni de la tendance, et la règle est positive presque toutes les années.
2. **Le vrai apport des stops est sur la queue de distribution, pas sur le Sharpe** : avec les stops, 1 nuit sous −2 % contre 32 à 33 sans, et une distribution asymétrique vers le haut. Le n° 12 ne montrait pas de gain de Sharpe démontrable ; ici, les stops changent fortement le profil de risque, ce qui compte pour dimensionner la position.
3. **Le filtre momentum protège dans la seule vraie année baissière (2022)**, mais repose sur peu de nuits : c'est cohérent, pas démontré.
4. Le résultat par jour de semaine (lundi le plus fort) est dans `regimes.csv` ; il n'est pas interprété : c'est du découpage sans hypothèse préalable.
