---
type: experiment
updated: 2026-10-31
status: paper-trading
verdict: candidat (dépend du régime)
prereg: [2]
trials: 96
---

# Fade de gap sur indices (|z| > 1, régime post-0DTE)

**Une phrase** : depuis 2022, les gaps d'ouverture de ES/NQ/YM se retournent dans la séance (+8,8 pb/trade depuis 2023, contre −5,6 pb avant), ce qui coïncide avec la généralisation des options 0DTE (Ladia 2026).

## Tests
| Test | Résultat | Critère |
|---|---|---|
| A1 jours jamais tradés, 1 < \|z\| ≤ 2 | Sharpe OOS +0,54 | ✅ |
| A2 rupture 2023 | Welch t = 2,89, p = 0,002 | ✅ |
| A3 dose-réponse | +5,5 / +6,4 / +18,3 pb | ✅ monotone |

## Réserves
- Perdante sur 2016–2021 : c'est un pari sur la durée du régime 0DTE.
- L'idée est venue de l'OOS du premier lot ; la validation reste sur 2023–2026 et sur des indices corrélés.
- Corrélation avec [[wiki/experiments/m2-bande-bruit-nq|M2 sur NQ]] : 0,01.

## Usage prévu
Paper trading avec interrupteur de régime (couper si le Sharpe glissant 12 mois redevient négatif).

## Sources brutes
[[PREREGISTRATION_2]] · [[RESULTS]] (« Piste A ») · [followup.py](../../followup.py) · `results/followup.log`
