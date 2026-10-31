---
type: experiment
updated: 2026-10-31
status: active
verdict: candidat
prereg: [10, 11, 12, 13, 14]
trials: 1474
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

## Ce qu'on sait
- Hors échantillon temporel (n° 11), **100 % des trades étaient longs** : c'est « long NQ la nuit » qui est validé, pas le filtre momentum.
- Le filtre momentum coupe la perte de 2022 (DD −10,7 % contre −25,8 % toujours long), mais sur 422 nuits seulement : cohérent, pas démontré.
- Les stops ne changent pas le Sharpe, mais réduisent à 1 le nombre de nuits sous −2 % (32 sans stop).

## Ouvert
- Concentration : ~40 % des R de 2016–2026 viennent des nuits NFP/CPI (9 % des nuits) ; « prime d'annonce » à tester seulement sur le holdout (n° 14).
- Lisser le drawdown par la taille de position ou la diversification, pas par un filtre (n° 13).
- Hypothèse non validée : F2 (après une nuit baissière) améliore le R par trade sur 2016–2026 et 2011–2015 ; à pré-enregistrer séparément sur le holdout.
- Comportement en marché baissier prolongé (seule vraie phase : 2022).
- Holdout unique : données postérieures au 2026-08-28.

## Sources brutes
[[PREREGISTRATION_10]] · [[PREREGISTRATION_11]] · [[PREREGISTRATION_12]] · [run_prereg10.py](../../run_prereg10.py) · [run_prereg11.py](../../run_prereg11.py) · [run_prereg12.py](../../run_prereg12.py) · [run_robust13.py](../../run_robust13.py) · `results/prereg1{0,1,2}/`, `results/robust13/`
