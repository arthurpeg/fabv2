---
type: experiment
updated: 2026-10-31
status: done
verdict: utile (exécution, pas alpha)
prereg: [4]
trials: 138
---

# Timing d'exécution FX (règle X3, Baltussen)

**Une phrase** : pour un ordre FX nécessaire de toute façon, exécuter tout de suite si le mouvement du jour va contre soi, sinon attendre 15:00 ET ; gain ≈ 0,2 pb (un demi-tick) par ordre.

## Résultat
- X3 est la seule règle stable : positive en IS et OOS sur 6E, 6J, 6B ; seul 6E passe Bonferroni (12 tests).
- Krohn sur Tokyo : 0,5 à 1 pb avant 2023, ne subsiste que sur 6A.
- Ordre de grandeur : ~20 $ par million exécuté. Optimisation d'exécution, pas source de rendement.

## Sources brutes
[[PREREGISTRATION_4]] · [[RESULTS]] (« Timing d'exécution FX ») · [execution_timing.py](../../execution_timing.py) · `results/execution_timing*.csv`
