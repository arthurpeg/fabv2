# Short du yen filtré R4 avec stop obligatoire (prop firm)

*2026-11-21. Exploratoire, sur données **déjà vues** (6J du 2017-01-30 au 2026-08-28), avec les mêmes jours R4 que [[reports/jpy_us_filtres_report]]. La grille de 8 essais et le critère de choix ont été figés et commités dans l'en-tête de [run_jpy_us_r4_stops.py](../run_jpy_us_r4_stops.py) avant le calcul. Compteur global : 1 822 (1 814 + 8). Sorties : `results/jpy_us_r4_stops/`.*

## Résultats (1 109 trades)

| Variante | Risque médian (bp) | % SL | % TP | Net (bp) | t NW | Sharpe net | R net moyen | R avec glissement | Moitiés (R) | Pire série de pertes | Pire creux (R) | Années + |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R4 sans stop | — | 0 | 0 | +2,09 | 3,50 | 1,48 | — | — | — | — | — | 9/10 |
| SL 2 ATR H1 | 29,6 | 10,8 | 0 | +1,55 | 2,73 | 1,12 | +0,040 | +0,038 | +0,031 / +0,049 | 7 | −13,3 | 9/10 |
| SL 3 ATR H1 | 44,4 | 4,1 | 0 | +1,85 | 3,19 | 1,32 | +0,032 | +0,031 | +0,027 / +0,038 | 7 | −7,9 | 9/10 |
| SL 4 ATR H1 | 59,2 | 1,5 | 0 | +2,02 | 3,51 | 1,45 | +0,027 | +0,027 | +0,024 / +0,030 | 7 | −5,7 | 9/10 |
| SL 1 σ20 | 17,2 | 30,6 | 0 | +0,52 | 0,99 | 0,42 | +0,008 | −0,005 | +0,001 / +0,014 | 9 | −41,5 | 6/10 |
| SL 1,5 σ20 | 25,8 | 16,0 | 0 | +1,21 | 2,19 | 0,91 | +0,034 | +0,030 | +0,037 / +0,032 | 7 | −22,9 | 7/10 |
| SL 2 σ20 | 34,4 | 8,7 | 0 | +1,49 | 2,65 | 1,10 | +0,033 | +0,031 | +0,027 / +0,039 | 7 | −16,6 | 8/10 |
| **SL 2 ATR H1, TP 3R** (retenue) | 29,6 | 10,8 | 0,3 | +1,56 | 2,73 | 1,12 | **+0,041** | +0,039 | +0,031 / +0,051 | 7 | −13,3 | 9/10 |
| SL 3 ATR H1, TP 3R | 44,4 | 4,1 | 0 | +1,85 | 3,19 | 1,32 | +0,032 | +0,031 | +0,027 / +0,038 | 7 | −7,9 | 9/10 |

## Lecture

1. **Avec le filtre R4, un stop large ne coûte presque rien.** Le SL 4 ATR H1 garde +2,02 bp sur +2,09, contre −0,79 bp avec les stops serrés de la règle non filtrée.
2. **Le R par trade a un optimum.** Un stop plus serré augmente le R tant qu'il ne coupe pas trop de trades : on passe de +0,027 R à 4 ATR à +0,040 R à 2 ATR. En dessous (1 σ20, environ 17 bp), il s'effondre : +0,008 R.
3. **Le critère figé retient SL 2 ATR H1 + TP 3R** (+0,041 R). Le TP n'est touché que dans 0,3 % des trades : en pratique, c'est un **seul SL d'environ 30 bp, sans TP**, comme tu le proposais.
4. **Ordre de grandeur en prop firm**, sur données vues :
   - +0,04 R par trade, environ 115 trades par an, donc environ +4,6 R par an ;
   - pire creux de −13 R, et jusqu'à 7 pertes de suite.
   - À 1 % de risque par trade, cela fait environ +4,6 % par an pour un creux d'environ −13 %. C'est trop faible pour une éval seule, mais utilisable en complément de mom / 3n, à condition que ce ne soit pas le même risque. Corrélation à vérifier avant toute combinaison (règle 3).
5. **Bougies dollar : non testées.**
   - La règle est définie dans le temps (11:00 → 16:55), et le stop doit tenir face au bruit de cette fenêtre. Une ATR en temps (H1) mesure exactement ce bruit, alors qu'une ATR en bougies dollar le mesure par volume échangé.
   - Le comptant Dukascopy de la confirmation n'a pas de vrai volume, ce qui rendrait la règle impossible à tester de la même façon.
   - Pour 8 essais de plus, le gain attendu est nul.

La règle est figée au [[PREREGISTRATION_29]].

## Complément : SL en ATR M15 (2026-11-21)

4 essais, figés avant calcul dans [run_jpy_us_r4_m15.py](../run_jpy_us_r4_m15.py). Compteur global : 1 831 (1 827 + 4).

| Variante (sans TP) | Risque médian (bp) | % SL | Net (bp) | R net | R avec glissement | Moitiés (R) | Pire creux (R) | Années + |
|---|---|---|---|---|---|---|---|---|
| SL 2 ATR M15 | 16,5 | 31,6 | +0,76 | +0,024 | +0,011 | +0,008 / +0,040 | −33,7 | 6/10 |
| SL 3 ATR M15 | 24,8 | 16,1 | +1,35 | +0,036 | +0,032 | +0,020 / +0,052 | −18,9 | 7/10 |
| SL 4 ATR M15 | 33,0 | 8,7 | +1,61 | +0,038 | +0,036 | +0,031 / +0,045 | −11,5 | 8/10 |
| SL 5 ATR M15 | 41,3 | 5,1 | +1,79 | +0,034 | +0,033 | +0,028 / +0,040 | −8,8 | 9/10 |

**Lecture.** À distance égale, l'ATR M15 fait un peu moins bien que l'ATR H1 : +0,038 R pour 4 ATR M15 (33 bp) contre +0,041 R pour 2 ATR H1 (30 bp). Une ATR M15 mesure seulement les 3,5 dernières heures avant 11:00 : elle est plus bruitée et moins représentative de la fenêtre de 6 heures. La règle figée demandait +0,046 R pour écrire un avenant : le n° 29 reste inchangé.

## Complément : SL en ATR M15 avec TP 2R ou 3R (2026-11-21)

8 essais, figés avant calcul dans [run_jpy_us_r4_m15_tp.py](../run_jpy_us_r4_m15_tp.py). Compteur global : 1 839 (1 831 + 8).

| Variante | Risque médian (bp) | % SL | % TP | R net | R avec glissement | Moitiés (R) | % gagnants | Pire creux (R) | Années + |
|---|---|---|---|---|---|---|---|---|---|
| SL 2 ATR M15, TP 2R | 16,5 | 31,4 | 8,2 | +0,017 | +0,004 | −0,004 / +0,037 | 49,5 | −36,9 | 6/10 |
| SL 2 ATR M15, TP 3R | 16,5 | 31,6 | 2,7 | +0,019 | +0,007 | +0,001 / +0,038 | 49,1 | −36,3 | 6/10 |
| SL 3 ATR M15, TP 2R | 24,8 | 16,1 | 3,2 | +0,033 | +0,029 | +0,016 / +0,051 | 52,8 | −18,9 | 8/10 |
| SL 3 ATR M15, TP 3R | 24,8 | 16,1 | 0,8 | +0,038 | +0,034 | +0,021 / +0,055 | 52,8 | −18,9 | 7/10 |
| SL 4 ATR M15, TP 2R | 33,0 | 8,7 | 1,4 | +0,040 | +0,039 | +0,033 / +0,048 | 54,0 | −11,5 | 8/10 |
| SL 4 ATR M15, TP 3R | 33,0 | 8,7 | 0,3 | +0,039 | +0,037 | +0,031 / +0,046 | 54,0 | −11,5 | 8/10 |
| SL 5 ATR M15, TP 2R | 41,3 | 5,1 | 0,4 | +0,034 | +0,033 | +0,027 / +0,040 | 54,3 | −8,8 | 9/10 |
| SL 5 ATR M15, TP 3R | 41,3 | 5,1 | 0,3 | +0,036 | +0,035 | +0,030 / +0,042 | 54,3 | −8,8 | 9/10 |

**Lecture.**
- Le TP ne change presque rien : ±0,005 R au plus par rapport au même SL sans TP. Il n'est touché que dans 0,3 à 8 % des trades, et uniquement avec les stops serrés, où il coupe des gains.
- La meilleure variante, 4 ATR M15 avec TP 2R (+0,040 R), égale la règle du n° 29 (+0,041 R) sans la dépasser. Le seuil d'avenant (+0,046 R) n'est pas atteint : le n° 29 reste inchangé.
- Toutes les variantes de stops sur R4 testées (24 au total) se tiennent entre +0,03 et +0,04 R dès que la distance dépasse environ 25 bp. L'espérance vient de la dérive, pas de la gestion de la sortie.
