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
