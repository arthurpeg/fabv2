# Pré-enregistrement n° 31 : ORB 30 minutes de Subhani le vendredi sur NQ, réserve 2010-06 → 2015-12

*2026-11-22. Confirmation (étape 3) de [PREREGISTRATION_31](../PREREGISTRATION_31.md), commité avant tout calcul (commit `c7fb825`), **hors protocole** (B1 non franchie : DSR 0,846) ; demandé par l'utilisateur. Code : [run_prereg31.py](../run_prereg31.py), une seule exécution, fonctions de trading figées de `run_orb30_jours.py` et `run_orb30_tp.py`. Réserve ES, NQ, YM 2010-06-08 → 2015-12-31 désormais **consommée** (seul NQ lu). Compteur global : 2 085 (2 079 + 6). Sorties : `results/prereg31/`.*

## Règles

NQ, vendredis, range 9:30-9:59 (1 R = W), entrée à la cassure par ordre stop dès 10:00, stop fixe à 1 W. **A** : sortie à 16:00. **B** : objectif 2R. 1 contrat, coût 0,50 pt. Sur la réserve, le range médian ne vaut que 14,25 pts : le coût médian monte à 0,035 R (0,007 R en exploration).

## Résultats (271 vendredis)

| | Exploration 2016-2026 | **Réserve 2010-06 → 2015-12** |
|---|---|---|
| A sans objectif | +0,190 R, t 3,50 | **+0,041 R, t 0,52**, p 0,30 (Holm 0,59) |
| B objectif 2R | +0,164 R, t 3,67 | **+0,038 R, t 0,54**, p 0,30 (Holm 0,59) |
| Lundis-jeudis, règle A | ≈ +0,02 R | −0,062 R |

| Critère | A | B |
|---|---|---|
| C1 net > 0, p de Holm ≤ 0,05 | ❌ (0,59) | ❌ (0,59) |
| C2 vendredi > lundi-jeudi | ✅ (+0,104 R) | ✅ (+0,082 R) |
| C3 net > 0 sans la meilleure année | ❌ (−0,000) | ❌ (−0,005) |
| C4 net > 0 avec 1 tick de plus | ✅ | ✅ |

**Verdict : REJET pour A et pour B.**

Règle A en dollars : +0,79 pt (+16 $) par trade, 38,7 % de sorties au stop. Par année, vendredi / lundi-jeudi : 2010 −0,24 / −0,04 · 2011 +0,06 / −0,01 · 2012 **+0,23** / −0,03 · 2013 −0,06 / −0,08 · 2014 −0,00 / −0,04 · 2015 +0,13 / −0,16. Trois années positives sur six ; sans 2012, le gain est nul.

## Contrôle placebo (règle A, réserve)

| Jour | Trades | R net | t |
|---|---|---|---|
| Lundi | 260 | −0,048 | −0,68 |
| Mardi | 285 | −0,176 | −2,66 |
| Mercredi | 283 | −0,068 | −0,95 |
| Jeudi | 275 | +0,048 | 0,65 |
| Vendredi | 271 | +0,041 | 0,59 |

Sur la réserve, le vendredi n'est plus à part : il est à peu près au niveau du jeudi. Le mardi, deuxième meilleur jour en exploration (+0,10 R), est ici le pire (−0,18 R, t −2,66).

## Lecture

1. **L'effet vendredi ne se retrouve pas avant 2016** : +0,04 R au lieu de +0,19 R, non significatif, et porté par une seule année (2012).
2. Le classement des jours change d'une période à l'autre (mardi : +0,10 R puis −0,18 R). C'est le comportement attendu d'un **effet calendaire de hasard** (Sullivan, Timmermann et White 2001), ou d'un effet propre à 2016-2026.
3. **Le papier ne couvre que 2018-2026** et l'auteur écrivait lui-même que l'existence de l'effet avant 2018 n'était pas testée. Ce résultat va dans le sens de sa réserve : si l'effet existe, il est récent (régime des options courtes, 0DTE), et rien ne permet aujourd'hui de le distinguer d'un hasard sur 8 à 10 ans.
4. La puissance annoncée était d'environ 79 % à l'effet de l'exploration : un effet de cette taille aurait probablement été vu.

Ligne au registre des échecs ; la ligne « À surveiller » des phénomènes est annotée « contredit ».
