# N° 25 : la stratégie transmise EMA 9:30 / M2 hors échantillon, NQ 2010-06 → 2012-12

*2026-11-03. Règles et critères : [[PREREGISTRATION_25]] (commit f130eeb, avant calcul). Compteur global : 1 726 → 1 734 (8 essais). Code : [run_prereg25.py](../run_prereg25.py). Sorties : `results/prereg25/` (`run.log`, `tests.csv`, trades).*

## Verdict : ÉCHEC

| Critère | Résultat | Seuil |
|---|---|---|
| P1 : P&L net moyen de M2 > 0 (NQ, 1 contrat, sans stop) | +20,7 $/trade (5,2 bps), t 0,89, **p 0,19** | p < 0,05 ❌ |
| P2 : jours M2 − jours exclus (signal C) | +4,2 $/trade, t 0,12, **p 0,45** | p < 0,05 ❌ |
| Positif sur les deux moitiés | 2010-06 → 2011-09 : +17,1 $ ; 2011-10 → 2012-12 : +24,6 $ | ✅ |

Il y a 661 séances, dont 230 jours M2 (environ 88 par an, contre environ 100 sur 2016-2026). Les contrôles sont propres : vectorbt donne les mêmes sorties que la boucle à la main sur toutes les variantes, et le plus grand saut pendant un trade est de 9 bps (aucun roulement).

## Toutes les variantes, NQ (15 $ l'aller-retour)

| | C | D toujours long | M2 | M2 + taille (retenue) | M2 + stop 4 ATR M15 | M2 + stop + taille |
|---|---|---|---|---|---|---|
| Trades | 661 | 661 | 230 | 230 | 230 | 230 |
| bps/trade par NQ | 4,0 | −1,2 | 5,2 | 5,2 | 6,3 | 6,3 |
| $/trade | 17,9 | −7,9 | 20,7 | 6,7 | 28,3 | 24,9 |
| Win % | 52,0 | 51,9 | 53,0 | 53,0 | 44,8 | 44,8 |
| PF | 1,12 | 0,95 | 1,12 | 1,05 | 1,20 | 1,21 |
| **Sharpe** | 0,68 | −0,30 | 0,42 | 0,16 | 0,68 | 0,74 |
| Max DD $ | 7 940 | 10 625 | 3 835 | 3 382 | 2 856 | 1 870 |
| t NW (p unilatéral) | 1,18 (0,12) | −0,49 | 0,89 (0,19) | 0,31 (0,38) | 1,45 (0,074) | 1,41 (0,080) |

**M2 + stop en R** (1 R = 4 ATR M15) : E[R] +0,066 (t 0,91), 5,8 R par an, 45 % de gagnants, max DD −9,5 R, 45 % de trades stoppés. Sur 2016-2024, on avait +0,200 R, 19,6 R par an et t 4,06.

**ES et YM, M2** (secondaires) : ES +11,7 bps/trade, Sharpe 0,90, p 0,039 ; YM +7,7 bps, Sharpe 0,83, p 0,054. Avec 6 tests secondaires, aucun ne reste significatif après correction (Holm : ES 0,23).

P&L net de M2 par année : 2010 −150 $, 2011 +5 480 $, 2012 −575 $.

## Lecture

1. **M2 ne se retrouve pas sur des années jamais vues.** Son avantage tombe à 5 bps par trade, contre 15 bps sur 2016-2024 et 20 bps sur 2025-2026. Le résultat est positif, mais il ne se distingue pas du hasard. Le Sharpe de 1,22 à 1,28 sur 2016-2024 tient en grande partie au choix des seuils sur ces années.
2. **Le filtre M2 n'apporte rien sur 2010-2012.** Les jours M2 font +20,7 $ par trade, et les jours qu'il exclut font presque autant (+16,4 $). C'est le même constat que sur 2025-2026 dans le rapport d'origine, où le choix des jours n'avait que p 0,098. Sur deux échantillons sur trois, la force et le retournement ne choisissent pas de meilleurs jours.
3. **Il reste une trace faible du sens du signal.** C (tous les jours) est positif sur les deux moitiés, mais avec t 1,18. ES et YM vont dans le même sens, à p 0,04-0,05 avant correction. Ce n'est pas assez pour une stratégie ; c'est cohérent avec le momentum intraday faible déjà noté au registre (Gao, n° 20).
4. **Le stop améliore un peu le résultat** (Sharpe 0,68 contre 0,42 pour M2 seul) sans le rendre significatif (p 0,074). Ce n'était pas un critère, et on ne change pas le verdict après coup.
5. **Les deux stratégies du zip sont désormais testées hors échantillon, et aucune ne passe.** 3n (n° 24) n'y garde que la prime de nuit. M2 (n° 25) n'y garde qu'un signal de sens faible. Notre règle de nuit (mom) reste la seule à avoir passé ce type de test (n° 11).

## Diagnostic après coup : niveau de prix, coût et volatilité

Question posée : le NQ valait environ 2 300 points en 2010-2012, contre 11 000 sur 2016-2024. Faut-il normaliser ? Ce calcul est fait sur les jours M2, sans stop, et ne change pas le verdict.

| | 2010-06 → 2012-12 | 2016-2024 | 2025-08/2026 |
|---|---|---|---|
| Prix moyen du NQ | 2 332 | 10 990 | 24 255 |
| Gain brut (bps) | **8,5** | 15,9 | 20,0 |
| Coût de 15 $ (bps) | **3,3** | 0,8 | 0,3 |
| Gain net (bps) | 5,2 | 15,1 | 19,7 |
| Volatilité du jour : σ 20 j (bps) | 90 | 100 | 97 |
| Gain brut / σ 20 j | **0,061** (t 0,93) | 0,165 (t 4,4) | 0,202 (t 2,8) |
| E[R] brut (1 R = 4 ATR M15) | **0,057** (t 0,60) | 0,245 (t 4,0) | 0,321 (t 3,2) |

- **Les bps sont déjà un rendement en % du prix.** Ils ne dépendent pas du niveau du NQ, seuls les $ en dépendent. Ce qui dépend du prix, c'est le **coût** : 15 $ font 3,3 bps à 2 300 points, contre 0,8 à 11 000. Cela explique environ 2,5 des 10 bps d'écart.
- **En brut, l'avantage est quand même divisé par deux** (8,5 bps contre 15,9), alors que la volatilité du jour en % était la même (σ 90 contre 100 bps).
- **Normalisé par la volatilité, l'écart est le même ou plus grand.** En σ, on passe de 0,165 à 0,061 ; en R, de 0,245 à 0,057. Aucun de ces deux chiffres n'est significatif sur 2010-2012.
- **P2 (le choix des jours) compare des jours de la même période**, donc il ne dépend ni du prix ni du coût. Il échoue de toute façon (p 0,45).

## Prolongement descriptif : 2013-2015 et 2010-06 → 2015-12

[run_ema930_2013_2015.py](../run_ema930_2013_2015.py), sorties dans `results/prereg25/suite_2013_2015/`. **Ce n'est pas un test** : le post a choisi ses seuils en regardant 2013-2024, donc 2013-2015 a déjà été vu. C'est hors compteur, et cela ne change pas le verdict. Mêmes règles et même code que plus haut. vectorbt donne les mêmes sorties que la boucle, sauf 3 stops touchés dans la barre d'entrée.

| NQ, M2 | 2010-06 → 2012-12 (n° 25) | **2013-2015** | **2010-06 → 2015-12** | 2016-2024 | 2025-08/2026 |
|---|---|---|---|---|---|
| Trades | 230 | 227 | 457 | 899 | 168 |
| Net bps/trade | 5,2 | 7,6 | 6,4 | 15,1 | 19,7 |
| Coût (bps) | 3,3 | 2,0 | 2,6 | 0,8 | 0,3 |
| Sharpe M2 | 0,42 | 0,83 | 0,65 | 1,22 | 1,79 |
| Sharpe M2 + taille | 0,16 | 1,09 | 0,69 | 1,28 | 1,86 |
| Sharpe M2 + stop | 0,68 | 0,27 | 0,44 | 1,27 | 1,52 |
| t NW M2 | 0,89 | 1,34 | 1,59 | 3,99 | 2,78 |
| Brut / σ 20 j | 0,061 (t 0,93) | 0,160 (t 2,14) | 0,111 (t 2,22) | 0,165 (t 4,4) | 0,202 (t 2,8) |
| C jours M2 − jours exclus | +4 $ (p 0,45) | +69 $ (p 0,07) | +38 $ (p 0,10) | — | (p 0,098) |
| ES M2 : Sharpe (t) | 0,90 (1,77) | 0,70 (1,23) | 0,79 (2,02) | | |
| YM M2 : Sharpe (t) | 0,83 (1,61) | 0,34 (0,72) | 0,54 (1,56) | | |

P&L net de M2 sur NQ par année : 2010 −150 $, 2011 +5 480 $, 2012 −575 $, 2013 +3 060 $, 2014 +3 905 $, 2015 +6 185 $.

**Lecture.**
- **2013-2015 est meilleur que 2010-2012**, sans être significatif (t 1,34). Avant coût et normalisé par la volatilité (0,160 σ), il est proche de 2016-2024 ; le coût, à 2 bps, mange une part plus grande. Le choix des jours y redevient presque significatif (p 0,07).
- **Sur les 5,5 ans de 2010-2015, M2 est positif mais faible** : 6,4 bps par trade, Sharpe 0,65, t 1,59. Avant coût, normalisé par σ, on obtient t 2,2, et ES va dans le même sens (t 2,0). Il y a probablement un petit effet, mais il fait environ deux fois moins que sur 2016-2024, et sur 2013-2015 il est obtenu sur des années que le post avait vues.
- **Le stop 4 ATR M15 change de sens d'une période à l'autre** : il aide sur 2010-2012 et sur 2022-2024, mais il nuit sur 2013-2015 (Sharpe 0,27 contre 0,83). Il n'est pas robuste.

