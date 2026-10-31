# Pré-enregistrement n° 13 — filtres « à plat » contre le drawdown : ÉCHEC

*2026-10-31. Protocole : [PREREGISTRATION_13.md](../PREREGISTRATION_13.md). Code : [run_prereg13.py](../run_prereg13.py). Résultats : [results/prereg13/](../results/prereg13/). Compteur global : 1 471.*

Base : règle NQ de nuit (20:00 ET, momentum 12-1, SL 2 / TP 5 ATR, sortie 9:30), compte 20:00, en R. Un filtre met la position à plat certaines nuits ; il est retenu s'il réduit le max DD d'au moins 30 %, garde au moins 80 % des R/an et bat le 95e centile de 500 filtres aléatoires de même participation (sélection 2016–2026), puis confirmé sur 2011–2015.

## Sélection 2016-01 → 2026-08

| Filtre | Nuits gardées | R/an (vs base) | Max DD (R) | Réduction DD | Aléatoire p95 | R/trade [IC 95 %] | Critères |
|---|---|---|---|---|---|---|---|
| **Base** | 100 % | **+19,3** | **−25,4** | — | — | +0,077 | — |
| F1 jour 9:45→15:00 > 0 (Jones) | 55 % | +9,6 (50 %) | −24,0 | 6 % | 29 % | +0,069 [+0,009 ; +0,135] | ✘ ✘ ✘ |
| F2 nuit précédente < 0 (Abdi) | 43 % | +14,3 (74 %) | −20,8 | 18 % | 35 % | **+0,131 [+0,059 ; +0,202]** | ✘ ✘ ✘ |
| F3 VOL veille tercile haut (Berkman) | 40 % | +6,9 (36 %) | −21,4 | 16 % | 36 % | +0,069 [−0,005 ; +0,146] | ✘ ✘ ✘ |
| F4 clôture > MM20 (Vojtko) | 66 % | +13,2 (69 %) | −33,2 | **−31 %** (pire) | 23 % | +0,080 [+0,017 ; +0,141] | ✘ ✘ ✘ |

## Confirmation 2011-07 → 2015-12 (rapportée, aucun filtre n'étant retenu)

| Filtre | Nuits gardées | R/an (vs base) | Max DD (R) | Réduction DD | R/trade |
|---|---|---|---|---|---|
| **Base** | 100 % | **+28,6** | **−22,4** | — | +0,115 |
| F1 | 53 % | +15,3 (53 %) | −25,6 | −14 % | +0,116 |
| F2 | 42 % | +18,0 (63 %) | −15,5 | 31 % | **+0,173** |
| F3 | 32 % | +2,9 (10 %) | −25,2 | −13 % | +0,037 |
| F4 | 63 % | +15,4 (54 %) | −22,1 | 1 % | +0,098 |

## Verdict pré-enregistré

**Aucun filtre retenu, donc aucun confirmé : la règle reste sans filtre.**

- Aucun filtre ne réduit le drawdown plus qu'un filtre aléatoire de même taille (tous sous le 95e centile). Retirer des nuits réduit le drawdown à peu près autant qu'on perd de rendement : le ratio R/an ÷ DD de la base (0,76 sur 2016–2026, 1,28 sur 2011–2015) n'est battu par aucun filtre.
- F4 (tendance MM20) **aggrave** le drawdown sur 2016–2026.
- Observation, sans valeur de décision : F2 (après une nuit baissière, Abdi) améliore nettement le **R par trade** sur les deux périodes (+0,131 contre +0,077 ; +0,173 contre +0,115), mais il garde trop peu de nuits pour améliorer le drawdown ou les R par an. Ce n'est pas un résultat validé : à pré-enregistrer comme hypothèse séparée si on veut le tester sur le holdout post-2026-08-28.

## Ce qu'on en retient

Le drawdown de la règle vient de la variance des nuits elles-mêmes, pas d'une catégorie de nuits que ces filtres sauraient éviter. Pour le lisser, les leviers restants sont la **taille de position** (risque par trade, volatilité cible) et la **diversification** avec une stratégie peu corrélée, pas un filtre de plus.
