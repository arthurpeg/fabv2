# Pré-enregistrement n° 16 — clôture sous le VWAP de la dernière heure (pression vendeuse) : ÉCHEC

*2026-10-31. Protocole : [PREREGISTRATION_16.md](../PREREGISTRATION_16.md). Code : [run_prereg16.py](../run_prereg16.py). Résultats : [results/prereg16/](../results/prereg16/). Compteur global : 1 480.*

Signal S : clôture de 16:15 ET sous le VWAP (prix typique) de 15:15–16:15 ET, séance précédant la nuit. Base : règle de nuit 20:00 (momentum 12-1, SL 2 / TP 5 ATR, sortie 9:30), en R, nuits 2011-07 → 2026-08.

## Hypothèse H : les nuits S rapportent plus

| Marché (rôle) | Nuits S | R/trade nuits S [IC 95 %] | R/trade autres nuits | Écart | p unilatéral |
|---|---|---|---|---|---|
| ES (sélection) | 46 % | +0,023 [−0,04 ; +0,08] | −0,003 | +0,025 | 0,30 |
| YM (sélection) | 47 % | +0,012 [−0,05 ; +0,08] | +0,039 | **−0,027** | 0,72 |
| NQ (confirmation) | 47 % | +0,115 [+0,06 ; +0,18] | +0,065 | +0,051 | 0,11 |

## Filtre V1 : ne trader que les nuits S

| Marché | Base R/an, DD | V1 R/an (vs base), DD | Réduction DD | Aléatoire p95 | Critères |
|---|---|---|---|---|---|
| ES | +2,2 / −61,8 | +2,6 (115 %) / −36,4 | 41 % | 50 % | ✔ ✔ ✘ |
| YM | +6,5 / −129,1 | +1,4 (21 %) / −70,6 | 45 % | 69 % | ✔ ✘ ✘ |
| NQ | +22,0 / −25,4 | +13,4 (61 %) / −20,2 | 20 % | 25 % | ✘ ✘ ✘ |

## Verdict pré-enregistré

**H rejetée (p = 0,30 sur ES, écart de signe contraire sur YM), V1 rejeté (ne bat le hasard sur aucun marché).**

- Sur NQ, le sens est celui du papier (+0,051 R par trade les nuits de pression vendeuse) mais pas significatif (p = 0,11), et ES/YM ne le confirment pas.
- Le VWAP de la dernière heure n'est pas une approximation suffisante du déséquilibre de clôture mesuré par Boyarchenko-Larsen-Whelan (volume signé), ou l'effet est trop faible sur ces marchés à l'horizon 20:00 → 9:30. Tester le vrai RSV demanderait les trades tick par tick (environ 1 275 $ pour NQ).
