# Pré-enregistrement n° 15 — filtres VIX et taille selon la volatilité : ÉCHEC des trois essais

*2026-10-31. Protocole : [PREREGISTRATION_15.md](../PREREGISTRATION_15.md). Données VIX/VIX3M : CBOE ([config/cboe_VIX_history.csv](../config/cboe_VIX_history.csv), [config/cboe_VIX3M_history.csv](../config/cboe_VIX3M_history.csv)). Code : [run_prereg15.py](../run_prereg15.py). Résultats : [results/prereg15/](../results/prereg15/). Compteur global : 1 478.*

Base : règle de nuit 20:00 (momentum 12-1, SL 2 / TP 5 ATR, sortie 9:30), en R.

## Sélection : NQ 2016-01 → 2026-08

| Essai | Nuits gardées | R/an (vs base) | Max DD (R) | Réduction DD | R/an ÷ DD | Critères |
|---|---|---|---|---|---|---|
| **Base** | 100 % | **+19,3** | **−25,4** | — | **0,76** | — |
| F5 Donninger : VIX/VIX3M > 0,87 | 53 % | +7,7 (40 %) | −25,0 | 2 % (aléatoire p95 : 29 %) | 0,31 | ✘ ✘ ✘ |
| F6 Vojtko : VIX < MM20 | 59 % | +10,3 (54 %) | −30,1 | −18 % (pire) | 0,34 | ✘ ✘ ✘ |
| T1 taille réduite si σ20 > médiane (taille moyenne 0,80) | 100 % | +16,5 (86 %) | −25,2 | 1 % | 0,66 | ✘ ✘ |

**Verdict pré-enregistré : aucun essai retenu, donc aucun confirmé.**

## Confirmations (rapportées pour information)

| Marché / période | Base R/an, DD | F5 | F6 | T1 |
|---|---|---|---|---|
| NQ 2011–2015 | +28,6 / −22,4 | +25,6 / −14,8 (DD −34 %) | +12,6 / −20,9 | +27,0 / −22,1 |
| ES 2011–2026 | +2,2 / −61,8 | +5,1 / −44,4 | −0,6 / −75,0 | −0,2 / −59,7 |
| YM 2011–2026 | +6,5 / −129,1 | +5,0 / −69,9 | +4,1 / −66,3 | +5,5 / −115,4 |

F5 aide sur NQ 2011–2015 et réduit le drawdown sur ES et YM, mais il échoue nettement sur l'échantillon de sélection, NQ 2016–2026 : il garde 40 % des R pour le même drawdown. Le critère de sélection étant fixé à l'avance, le résultat partiel des confirmations ne change rien.

## Ce qu'on en retient

1. Les deux règles VIX des papiers ne filtrent pas les nuits perdantes de la règle NQ de nuit. Le filtre de Vojtko aggrave même le drawdown.
2. La réduction de taille selon la volatilité ne change presque rien au drawdown en R (−1 %) : la règle est déjà normalisée par le risque (le stop vaut 2 ATR M15, donc 1 R s'adapte déjà à la volatilité du moment).
3. Avec les n° 13, 14 et 15, ce sont maintenant 9 filtres (prix, annonces, VIX, taille) qui ne réduisent pas le drawdown mieux que le hasard. Le drawdown de la règle est la variance normale d'un avantage faible (≈ 0,08 R par nuit), pas une catégorie de nuits repérable avec ces informations.
