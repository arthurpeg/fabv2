# NQ : règle de la 1ʳᵉ bougie de 5 minutes (Zarattini-Aziz) avec d'autres sorties

*2026-11-22. Étape 1 (exploration) de [[wiki/experiments/nq-orb-bougie-sorties]]. Grille figée et commitée dans l'en-tête de [run_nq_orb_bougie.py](../run_nq_orb_bougie.py) avant tout calcul (commit `a49ca1a`). Données : NQ Databento 1 min, 2010-06-08 → 2021-09-30 seulement ; la réserve de la question « sortie » (2021-10-01 → 2026-08-28) n'a pas été lue. Compteur global : 1 965 (1 940 + 25 essais). Sorties : `results/nq_orb_bougie/` (`grille.csv`, `trades_V0.csv`, `trades_choisie.csv`, `summary.txt`).*

## Règle

- Entrée : sens de la bougie 9:30-9:35 ET (pas de trade si doji, corps ≤ 1 tick), à l'open de 9:35, 1 contrat.
- Sorties testées : **V0** (aucun stop ni objectif, sortie à 16:00) et **24 variantes** stop = k × ATR14 (moyenne des amplitudes 9:30-16:00 des 14 séances précédentes), objectif = RR × stop, k ∈ {0,05 ; 0,10 ; 0,25 ; 0,50}, RR ∈ {1, 2, 3, 5, 10, clôture}.
- Coût standard 0,50 pt aller-retour (1 tick + 5 $). Stop prioritaire si stop et objectif tombent dans la même minute.
- 2 671 trades (233 jours sans trade : doji ou données manquantes). ATR14 moyen 75,6 pts (27 en 2010, 178 en 2021).
- Contrôle : V0 et la règle choisie repassées dans le moteur vectorbt de `fab.core`, corrélation journalière 1,0000.

## Résultats (points nets par trade)

| Variante | Net | t NW | Sharpe | Gagnants | Stoppés | Réf. « toujours long » | t écart réf. | 2010-06 → 2015 | 2016 → 2021-09 |
|---|---|---|---|---|---|---|---|---|---|
| **V0 sans stop ni objectif** | **+2,83** | 2,48 | 0,72 | 52 % | — | +0,91 | 1,27 | +1,00 | +4,49 |
| k 0,05, RR 1 | −0,14 | −1,51 | −0,44 | 54 % | 46 % | −0,54 | 3,31 | −0,34 | +0,04 |
| k 0,05, RR 2 | +0,10 | 0,72 | 0,21 | 40 % | 60 % | −0,35 | 2,80 | −0,16 | +0,33 |
| k 0,05, RR 3 | +0,22 | 1,24 | 0,38 | 31 % | 69 % | −0,24 | 2,45 | −0,08 | +0,49 |
| k 0,05, RR 5 | +0,49 | 2,10 | 0,64 | 21 % | 79 % | −0,09 | 2,39 | −0,10 | +1,02 |
| k 0,05, RR 10 | +0,91 | 2,70 | 0,83 | 13 % | 86 % | +0,24 | 2,12 | +0,16 | +1,59 |
| **k 0,05, clôture** (choisie) | **+1,52** | **3,16** | **1,00** | 10 % | 90 % | +0,71 | 1,78 | +0,23 | +2,69 |
| k 0,10, RR 1 | +0,19 | 1,09 | 0,30 | 55 % | 45 % | −0,48 | 2,44 | −0,22 | +0,56 |
| k 0,10, RR 2 | +0,37 | 1,38 | 0,41 | 37 % | 62 % | −0,28 | 2,02 | −0,13 | +0,83 |
| k 0,10, RR 3 | +0,80 | 2,43 | 0,70 | 29 % | 71 % | −0,17 | 2,64 | −0,13 | +1,65 |
| k 0,10, RR 5 | +0,81 | 1,92 | 0,56 | 21 % | 79 % | −0,00 | 1,90 | +0,16 | +1,41 |
| k 0,10, RR 10 | +1,79 | 3,10 | 0,92 | 17 % | 83 % | +0,53 | 2,09 | +0,15 | +3,28 |
| k 0,10, clôture | +1,68 | 2,92 | 0,85 | 16 % | 83 % | +0,58 | 1,88 | +0,18 | +3,04 |
| k 0,25, RR 1 | +0,29 | 0,67 | 0,19 | 52 % | 47 % | −0,20 | 0,84 | −0,10 | +0,66 |
| k 0,25, RR 2 | +0,38 | 0,62 | 0,18 | 38 % | 59 % | −0,30 | 0,98 | +0,26 | +0,48 |
| k 0,25, RR 3 | +1,18 | 1,67 | 0,48 | 34 % | 63 % | +0,08 | 1,38 | +0,33 | +1,94 |
| k 0,25, RR 5 | +1,32 | 1,70 | 0,50 | 32 % | 64 % | +0,54 | 0,94 | +0,28 | +2,27 |
| k 0,25, RR 10 | +1,23 | 1,56 | 0,45 | 32 % | 64 % | +0,33 | 1,07 | +0,29 | +2,09 |
| k 0,25, clôture | +1,17 | 1,49 | 0,43 | 32 % | 64 % | +0,31 | 1,02 | +0,27 | +1,98 |
| k 0,50, RR 1 | +1,42 | 1,69 | 0,52 | 53 % | 33 % | −0,31 | 1,66 | +0,90 | +1,90 |
| k 0,50, RR 2 | +2,23 | 2,17 | 0,69 | 47 % | 36 % | +0,56 | 1,37 | +0,96 | +3,38 |
| k 0,50, RR 3 | +1,83 | 1,77 | 0,56 | 47 % | 36 % | +0,31 | 1,32 | +0,88 | +2,70 |
| k 0,50, RR 5 | +1,98 | 1,91 | 0,59 | 46 % | 37 % | +0,26 | 1,47 | +0,85 | +3,00 |
| k 0,50, RR 10 | +1,92 | 1,86 | 0,57 | 47 % | 37 % | +0,24 | 1,44 | +0,82 | +2,91 |
| k 0,50, clôture | +1,91 | 1,85 | 0,57 | 47 % | 37 % | +0,24 | 1,43 | +0,82 | +2,90 |
| *R4, papier (référence, non comptée)* | +1,32 | 1,89 | 0,54 | 23 % | 76 % | — | — | −0,11 | +2,62 |

Net moyen par année (pts/trade) : V0 2010 +1,17 · 2011 +1,27 · 2012 +0,06 · 2013 +1,50 · 2014 +3,73 · 2015 −1,56 · 2016 +3,24 · 2017 +2,01 · 2018 +10,03 · 2019 −0,43 · **2020 +8,67** · 2021 (jusqu'en septembre) +2,89. Règle choisie : −0,73, −0,07, −0,21, +0,31, +1,68, −0,02, +2,80, −0,16, +2,85, +2,99, +1,44, +7,18.

## Fiche de la règle choisie (meilleur Sharpe net : stop 0,05 × ATR14, sortie à la clôture)

n 2 671 · brut +2,02 · net +1,52 pt (médiane −2,71) · écart-type 24,0 · Sharpe 1,00 · t NW 3,16 · 10 % de gagnants · pire creux −610 pts · 7 années positives sur 12 · moitiés +0,41 / +2,63 · sans la meilleure année +1,09 · avec 1 tick de plus +1,27 · référence « toujours long » +0,71 (écart +0,81, t 1,78) · **DSR (N = 26) 0,948**.

**B1 : ❌ ratée de justesse** : DSR 0,948 < 0,95. Les cinq autres critères passent.

## Lecture

1. **Avant 2016, la règle ne gagne presque rien.** Sur 2010-06 → 2015, toutes les variantes à stop serré sont entre −0,3 et +0,3 pt par trade, et R4 (la règle du papier) est à −0,11. Ce qu'on voit sur 2016-2021 est cohérent avec Zarattini-Aziz, mais la période antérieure, jamais vue, ne le confirme pas.
2. **Les objectifs fixes coûtent.** À stop égal, RR 1 à 3 font toujours moins bien que RR 10 ou « clôture » : la règle ne gagne que par quelques grosses journées, que l'objectif coupe. C'est le « let profits run » du papier.
3. **V0 (sans rien) a le plus gros gain par trade (+2,83 pts)**, mais aussi la plus forte dispersion (creux de −2 200 pts). Une partie de son gain est la dérive haussière : « toujours long » fait +0,91 sur les mêmes jours, et l'écart n'est qu'à t 1,27. **Elle doit beaucoup à 2018 et 2020** (+10,0 et +8,7 pts/trade).
4. **La règle choisie est fragile à l'exécution.** Un stop à 0,05 × ATR vaut environ 1,4 pt (5 à 6 ticks) en 2010 et environ 9 pts en 2021. 90 % des trades sont stoppés. Le modèle suppose un remplissage au prix du stop, avec un seul tick de glissement compris dans le coût. Le papier fait la même mise en garde pour TQQQ.
5. **Contre R4, sur les mêmes jours** : la règle choisie fait +0,20 pt/trade de mieux, V0 +1,51.

## Suite

B1 ratée : idée **abandonnée** au sens du protocole (ligne au registre). La réserve de la question « sortie » (2021-10-01 → 2026-08-28) reste **réservée** et n'a pas été lue ; elle ne pourrait de toute façon pas trancher seule (puissance estimée 15 à 30 %, voir la fiche).
