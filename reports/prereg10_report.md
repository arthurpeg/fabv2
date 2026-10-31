# Pré-enregistrement n° 10 — résultat : ÉCHEC

*2026-10-30. Règle et critères : [PREREGISTRATION_10.md](../PREREGISTRATION_10.md). Code : [run_prereg10.py](../run_prereg10.py). Données : [results/prereg10/](../results/prereg10/). Compteur global d'essais : 1 455.*

Règle figée : momentum 12-1 de l'actif (long ou short pour le mois), entrée 20:00 ET, SL 2 ATR / TP 5 ATR (ATR 14 sur M15), sortie à 9:30 ET, coût 1 tick + 5 $. Sur NQ, où elle a été choisie : +0,084 R/trade [+0,033 ; +0,134].

## Tests principaux (compte 20:00)

| Marché | Trades | R/trade net [IC 95 %] | p unilatéral | p Holm | 2017–2020 | 2021–2026 | R/an 2017–2025 | Max DD | Critères |
|---|---|---|---|---|---|---|---|---|---|
| ES | 2 419 | +0,029 [−0,021 ; +0,081] | 0,13 | 0,25 | +0,048 | +0,016 | +6,7 | −44 R | ✘ (p) |
| YM | 2 416 | +0,016 [−0,039 ; +0,067] | 0,27 | 0,27 | +0,108 | **−0,049** | +0,1 | −129 R | ✘ (p, signe 2021–26) |

Aucun des deux marchés ne remplit le critère 1 (p Holm < 0,05) ; YM échoue aussi au critère 2 (négatif sur 2021–2026). **Verdict pré-enregistré : échec.**

## Tests secondaires (bloc 19:00 + 20:00 + 21:00, R par nuit)

| Marché | R/nuit [IC 95 %] | p unilatéral | R/an 2017–2025 | Max DD |
|---|---|---|---|---|
| ES | +0,093 [−0,048 ; +0,232] | 0,09 | +20,4 | −119 R |
| YM | +0,049 [−0,098 ; +0,196] | 0,27 | −0,8 | −362 R |

## R par année (compte 20:00)

| | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (→ août) |
|---|---|---|---|---|---|---|---|---|---|---|
| ES | +22,8 | +3,5 | +2,9 | +18,6 | −17,6 | −8,0 | +10,6 | +28,0 | −0,4 | +10,7 |
| YM | +58,3 | +7,2 | +31,7 | +10,6 | −39,5 | −31,5 | −10,2 | −12,0 | −13,9 | +37,1 |

## Lecture

- Le signe reste positif sur ES et YM, mais l'effet est 3 à 5 fois plus faible que sur NQ et indiscernable de zéro. C'est l'écart attendu quand une configuration a été retenue parce qu'elle était la meilleure sur un seul marché.
- Sur 2021–2026, la règle perd sur YM et est presque nulle sur ES : l'effet, s'il existe, est concentré sur 2017–2020, comme la prime de nuit des indices dans la récolte 1.
- Interdit par le pré-enregistrement et non fait : changer d'heure, de multiples d'ATR, ajouter un filtre ou exclure des années pour « sauver » le résultat.
