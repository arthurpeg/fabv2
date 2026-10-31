---
type: experiment
updated: 2026-10-31
status: done
verdict: EV positive sans edge (si les rewards sont versés)
prereg: [18]
trials: 0
---

# Prop firm comme option : FTMO 1-Step avec des trades au hasard

**Une phrase** : la perte d'une tentative est plafonnée au prix de l'éval alors que le compte financé paie sans plafond ; avec des trades NQ au sens tiré au hasard et un stop à 1 ATR M15 (avenant A), l'EV vaut ≈ +71 $ par éval 10k et ≈ +1 035 $ par éval 100k (36 % de passage, financé 4,35 % du capital) ; avec un stop à 0,5 % du prix, ≈ +178 $ / +2 100 $.

## Résultat
- Stop 1 ATR M15 (≈ 0,12 % du prix à 9:30) : le spread (1 pb) coûte 0,083 R par trade et divise l'EV par ~2 ; sans coût, ce stop ferait +3 000 $ sur 100k (diagnostic exploratoire). **Le spread réel FTMO US100 est l'hypothèse décisive.**
- Vraies trajectoires NQ ≈ pile ou face binaire : la convexité ne dépend que du rapport perte max / objectif (10 % / 10 %).
- Le stop en % du prix fixe la durée (0,5 % → ~15 jours par éval ; 1 % → ~35 jours et moins de passage).
- Hypothèse la plus lourde : remise à zéro de la perte max après un reward (sinon EV −34 %).
- Risque non modélisé : refus de reward / bannissement (account rolling interdit chez FTMO). Seuil de refus qui annule l'EV : 45 % (10k), 65 % (100k) avec le stop ATR.
- Branche git `propfirm-ftmo`. Hors compteur d'essais (évaluation d'un contrat, pas d'une règle de marché).

## Sources brutes
[[PREREGISTRATION_18]] · [[reports/prereg18_report]] · [run_propfirm_ftmo.py](../../run_propfirm_ftmo.py) · [propfirm/](../../propfirm/) · `results/propfirm/` · session « Hedge sim discussion » (scripts `ftmo_sim.py`, `ftmo_funded_cmp.py`, hors dépôt)
