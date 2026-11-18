# Zhang (2018) : sessions intraday du FX sur les 7 majeures

*2026-11-19. Pré-enregistrement [[PREREGISTRATION_27]] (commit `fd5b243`, avant tout calcul). Code : [run_zhang.py](../run_zhang.py) (`uv run --with arch --with statsmodels python run_zhang.py`). Sorties : `results/zhang/` (`tests.csv`, `sessions_summary.csv`, `halves_O.csv`, `by_year.csv`, `garch.csv`, `costs.csv`, `sans_weekend.csv`, une série de sessions par devise et par période). Compteur 1 742 → 1 784 (42 essais). Rien après le 2026-08-28.*

Papier : Zhang (2018), Finance Research Letters 27, SSRN 3138756. Sessions : domestique = 08-16 heure locale, LDN-NY = 08-11 New York, US = 11-17 New York, non-US = le reste. Prix en dollars par unité de devise : un rendement négatif veut dire que la devise baisse.

## Verdict

1. **La réplication sur la période du papier (2010-05 → 2015) marche.** Nos moyennes tombent presque au centième de point de base sur la Table 1 pour EUR, GBP, JPY, CAD et NZD. Sur les 9 cases que le papier marque ** ou *** (pour nos 7 devises), 7 se retrouvent avec le même signe et p < 0,05. Les 2 échecs sont tous les deux sur CHF : ils viennent du 15 janvier 2015 (voir plus bas).
2. **Hors échantillon (2016 → 2026-08), les deux thèses centrales du papier ne tiennent plus.**
   - H1 (la devise baisse pendant ses heures domestiques) et H2 (elle monte pendant la session US) : **aucun des 14 tests ne passe Holm**. Ni H2 sur EUR et GBP, qui passaient sur la période du papier, ni H1 sur NZD.
   - La hausse d'EUR et de GBP en session US existe encore en 2016-2020 (+0,9 bp chacune), puis disparaît pour EUR (+0,06 bp en 2021-2026) et faiblit pour GBP (+0,8 bp, t 1,4).
3. **H3 (la relation négative avec la volatilité réalisée en session domestique) n'est confirmée nulle part, même sur la période du papier.** Les coefficients φ ont la même taille que ceux de la Table 2 : EUR −0,029 contre −0,031, NZD −0,112 contre −0,126, CAD −0,081 contre −0,092, CHF +0,61 contre +0,33. Mais ils ne sont pas significatifs (meilleur t −1,75 sous GARCH, contre *** dans le papier). La significativité du papier semble surestimée. De toute façon, l'équation est contemporaine : elle ne permet aucune prévision.
4. **Une observation du papier tient très bien : le yen baisse pendant la session US.** Ce n'était pas une hypothèse à verdict, mais c'est une case *** de la Table 1.
   - JPY, 11:00-17:00 NY : −2,03 bp sur 2010-2015, puis **−1,72 bp sur 2016-2026** (t Newey-West −4,28, p bilatéral 2 × 10⁻⁵, Holm sur les 28 cases de O ≈ 5 × 10⁻⁴).
   - Le signe tient dans les deux moitiés (−1,14 puis −2,24 bp) et l'effet est négatif 16 années sur 17, la seule exception étant 2015 à 0,0.
   - Il entre dans [[wiki/phenomenes]]. Ce n'est pas une stratégie : c'est la jambe 6J de la saisonnalité des fixings déjà au [[wiki/Failed Ideas/ledger|registre]] (R5b). Il fait 1,7 bp, contre 0,57 bp pour un tick et environ 1,1 bp au coût standard du dépôt (1,8 à 2 ticks).

## Réplication (période R, 2010-05-03 → 2015-12-31, spot Dukascopy mid)

Moyennes de session en bp. Les étoiles viennent du t simple, comme dans le papier : * p < 0,10, ** p < 0,05, *** p < 0,01.

| Devise | Domestique | | LDN-NY | | US | | Non-US | |
|---|---|---|---|---|---|---|---|---|
| | nous | papier | nous | papier | nous | papier | nous | papier |
| EUR | −2,17* | −2,10* | −0,65 | −0,63 | **+2,20***** | +2,21*** | −0,57 | −0,67 |
| GBP | −1,46 | −1,48 | −0,50 | −0,44 | **+1,65***** | +1,66*** | −0,27 | −0,39 |
| JPY | +0,88 | +0,95 | +0,76 | +0,90 | **−2,03***** | −2,12*** | −0,65* | −1,36* |
| CHF | +1,51 | +3,74** | +0,70 | +2,70** | +1,51 | +1,34 | −2,19*** | −4,12*** |
| AUD | −1,89* | −1,65 | −1,16 | −1,61* | +1,25 | +0,71 | +0,21 | +1,85* |
| CAD | −1,62 | −1,69 | **−2,40***** | −2,50*** | +0,83 | +0,80 | −0,55 | −0,41 |
| NZD | **−2,56**** | −2,60** | −1,45 | −1,85* | +2,02** | −0,47 | **+2,44**** | +3,10*** |

- **Les écarts sur CHF viennent du 15 janvier 2015**, le jour où la BNS a abandonné le plancher. Ce jour-là, la session domestique vaut +1 410 bp, LDN-NY −395, US +801 et non-US −436. Cela pèse environ 1 bp par session sur la moyenne de 1 430 jours. La façon dont ce choc se répartit entre les heures dépend de la source (cotations Dukascopy chaotiques ce jour-là, Datastream de son côté). C'est un problème de données, pas un désaccord de fond.
- **NZD en session US** : nous trouvons +2,02** et le papier −0,47. Nous n'avons pas d'explication. La différence de source est probable.
- Le GARCH(1,1) de l'équation (2) (`garch.csv`) donne les mêmes signes, comme dans le papier. Le F de Welch est significatif pour 6 devises sur 7 (pour AUD, p = 0,07).
- Les tests à verdict sur R, Holm sur 21 : seuls **H2 EUR** (p_Holm 0,029) et **H2 GBP** (0,031) passent.

## Hors échantillon (période O, 2016-01-01 → 2026-08-28)

EUR, GBP, JPY et AUD viennent des futures 6E, 6B, 6J et 6A (42 roulements chacun, ajustés). CHF, CAD et NZD viennent du spot Dukascopy.

| Devise | Domestique | LDN-NY | US | Non-US | t NW (dom / ldn / us / non-US) |
|---|---|---|---|---|---|
| EUR | −0,78 | +0,70 | +0,44 | +0,22 | −1,1 / 1,3 / 1,1 / 0,6 |
| GBP | +0,06 | +0,59 | +0,85 | −1,49 | 0,1 / 1,0 / 1,7 / **−2,6** |
| JPY | −0,07 | +0,60 | **−1,72** | −0,42 | −0,1 / 1,0 / **−4,3** / −1,7 |
| CHF | +0,34 | +1,48 | −0,06 | +0,33 | 0,5 / **2,8** / −0,1 / 1,0 |
| AUD | −0,07 | +0,74 | −0,16 | −0,35 | −0,1 / 1,2 / −0,3 / −0,9 |
| CAD | +0,76 | +0,43 | +0,66 | −1,10 | 1,2 / 0,9 / 1,7 / **−2,4** |
| NZD | −0,06 | +0,89 | −0,06 | −0,89 | −0,1 / 1,4 / −0,1 / −1,3 |

- **Tests à verdict** (Holm sur 21) : aucun ne passe. Le meilleur p brut est celui de H2 sur CAD (0,048) et GBP (0,046) ; après Holm, p = 0,97.
- **H1 est mort partout** : aucune devise ne baisse significativement pendant ses heures. Le motif « domestique négatif » du papier a disparu après 2015.
- **À surveiller** (significatif en brut, pas après Holm sur 28 cases, signe stable sur les deux moitiés) :
  - GBP non-US −1,5 bp (moitiés −1,9 et −1,1) ;
  - CAD non-US −1,1 bp (−0,7 et −1,4) ;
  - CHF LDN-NY +1,5 bp (+1,5 et +1,4).
- Variante sans le rendement du week-end (`sans_weekend.csv`) : aucune conclusion ne change. Pour JPY en domestique sur R, l'effet passe de +0,88 à +1,63 bp, car le week-end tombe dans les heures de Tokyo.

## Coûts (information, sans verdict)

- **Futures** : un tick aller-retour vaut 0,44 bp (6E), 0,77 (6B), 0,57 (6J) et 1,42 (6A). Le coût standard du dépôt (1,8 à 2 ticks) fait environ le double.
- **Spot sur O** : demi-spread d'entrée plus de sortie, en médiane. Il va de 0,8 à 1,2 bp (sessions qui commencent ou finissent en journée) à 1,6 à 4,2 bp (sessions qui touchent 17:00 NY : CHF 2,9, NZD 4,2).
- **Conclusion** : à part JPY en session US, aucun mouvement hors échantillon ne dépasse le coût.

## Ce qui change dans le wiki

- [[wiki/phenomenes]] : JPY en baisse pendant la session US passe en confirmé ; GBP non-US, CAD non-US et CHF LDN-NY vont dans « À surveiller ».
- [[wiki/Failed Ideas/ledger|Registre]] : H1/H2 de Zhang sur les majeures après 2015 (❌, effet disparu).
