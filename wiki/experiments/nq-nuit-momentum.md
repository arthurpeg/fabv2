---
type: experiment
updated: 2026-11-01
status: active
verdict: candidat
prereg: [10, 11, 12, 13, 14, 15, 16, 17]
trials: 1482
---

# Règle NQ de nuit : momentum 12-1, entrée 20:00 ET

**Une phrase** : être long (ou short si le momentum 12-1 est négatif) sur NQ de 20:00 à 9:30 ET, avec SL 2 ATR / TP 5 ATR (ATR 14 en M15), capte la [[wiki/concepts/prime-de-nuit|prime de nuit]] avec α ≈ +6 %/an et un bêta de 0,09.

## Origine
Sélectionnée sur NQ parmi les règles de la [[wiki/research/recoltes-ssrn|récolte 1]] ([[reports/recolte1_atr_report]]), donc choisie après coup. Les tests suivants sont là pour corriger ce biais.

## Tests
| N° | Question | Verdict | Rapport |
|---|---|---|---|
| 10 | Tient-elle sur ES et YM ? | ❌ échec | [[reports/prereg10_report]] |
| 11 | Tient-elle sur 2011–2015, jamais vu ? | ✅ +0,116 R/trade, p = 0,0015 | [[reports/prereg11_report]] |
| 12 | Plus que du bêta ? Mieux que des références simples ? | ✅ α +6,2 % [+2,5 ; +9,7] ; config exacte apporte peu | [[reports/prereg12_report]] |
| 13 (descriptif) | Régimes, pertes extrêmes | robuste ; stops = gain sur la queue | [[reports/robust13_report]] |
| 13 (pré-enregistré) | Un filtre « à plat » (Jones, Abdi, Berkman, Vojtko) réduit-il le drawdown ? | ❌ aucun ne bat un filtre aléatoire de même taille | [[reports/prereg13_report]] |
| 14 | Éviter les annonces NFP/CPI de 8:30 ? | ❌ inversé : ce sont les meilleures nuits (+0,30 R contre +0,05) | [[reports/prereg14_report]] |
| 15 | Filtres VIX (Donninger, Vojtko) et taille selon la volatilité ? | ❌ aucun des 3 ; la taille ne change rien (1 R suit déjà l'ATR) | [[reports/prereg15_report]] |
| 16 | Clôture sous le VWAP 15:15–16:15 (pression vendeuse, BLW) ? | ❌ ES p = 0,30, YM inversé ; NQ +0,05 R p = 0,11 | [[reports/prereg16_report]] |
| 17 | Exécution au VWAP (entrée 20:00–21:00, sortie 9:00–9:30) ? | non retenue : entrée +0,005 R sur NQ (IC inclut 0), sortie nulle | [[reports/prereg17_report]] |
| coûts réels | Spreads bbo-1m au lieu de 1 tick fixe | ✅ reste positif : +0,076 R/trade [+0,033 ; +0,116], +19 R/an ; MNQ dépend de la commission | [[reports/couts_reels_nq_nuit_report]] |
| 18 avenant C | Sur un compte FTMO 1-Step (éval 2 %, financé 1 %, spread CFD 1,5 pt) ? | EV +853 $ / éval 10k, +8 849 $ / 100k (sans edge : +98 $ / +1 295 $) ; dépend de la RAZ de la perte max | [[reports/prereg18_report]] |
| 18 avenant D | Sur un compte LucidFlex 50K en MNQ (éval 400 $, financé 200 $) ? | EV +157 $ / éval au niveau de prix actuel (sans edge −55 $) ; 5 fois moins que FTMO | [[reports/prereg18_report]] |
| 18 avenant E | FTMO, financé en RR 2 (TP 4 ATR, 1 %) ? | EV +1 009 $ / 10k (+14 % contre TP 5) ; R moyen TP 4 = +0,126 ; pire : 11 mois sans reward en 2022 | [[reports/prereg18_report]] |
| heures (descriptif) | Entrée 19:00 / 20:00 / 21:00 recalculée avec vectorbt, corrélations | +0,076 / +0,088 / +0,083 R net, Sharpe 0,91 / 1,00 / 0,87 ; corrélation par nuit 0,85 (19/20), 0,78 (20/21), 0,70 (19/21) ; panier égal Sharpe 1,01 | [[reports/nq_nuit_heures_report]] |
| SL range du soir (exploratoire) | SL au plus bas / plus haut de 17:00→20:00, TP 1 à 2,5 R ? | ❌ net −0,10 à −0,03 R/trade (réf. +0,088) ; stop médian 0,86 ATR, coûts ≈ 0,13 R | [[reports/nq_nuit_sl_range_report]] |

## Ce qu'on sait
- Hors échantillon temporel (n° 11), **100 % des trades étaient longs** : c'est « long NQ la nuit » qui est validé, pas le filtre momentum.
- Le filtre momentum coupe la perte de 2022 (DD −10,7 % contre −25,8 % toujours long), mais sur 422 nuits seulement : cohérent, pas démontré.
- Les stops ne changent pas le Sharpe, mais réduisent à 1 le nombre de nuits sous −2 % (32 sans stop).

## Ouvert
- Concentration : ~40 % des R de 2016–2026 viennent des nuits NFP/CPI (9 % des nuits) ; « prime d'annonce » à tester seulement sur le holdout (n° 14).
- Lisser le drawdown par la taille de position ou la diversification, pas par un filtre (n° 13).
- Hypothèse non validée : F2 (après une nuit baissière) améliore le R par trade sur 2016–2026 et 2011–2015 ; à pré-enregistrer séparément sur le holdout. Même lecture avec le filtre 3 nuits de la stratégie transmise : +7,5 bps/nuit les nuits « 3n long » contre −0,8 sinon sur 2016-2024, mais inversé en 2025-26 ([[reports/nq_nuit_3n_vs_mom_report]]).
- Comportement en marché baissier prolongé (seule vraie phase : 2022).
- Holdout unique : données postérieures au 2026-08-28.

## Sources brutes
[[PREREGISTRATION_10]] · [[PREREGISTRATION_11]] · [[PREREGISTRATION_12]] · [run_prereg10.py](../../run_prereg10.py) · [run_prereg11.py](../../run_prereg11.py) · [run_prereg12.py](../../run_prereg12.py) · [run_robust13.py](../../run_robust13.py) · `results/prereg1{0,1,2}/`, `results/robust13/`
