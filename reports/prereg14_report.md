# Pré-enregistrement n° 14 — éviter les annonces NFP/CPI de 8:30 : ÉCHEC, et hypothèse inversée

*2026-10-31. Protocole : [PREREGISTRATION_14.md](../PREREGISTRATION_14.md). Calendrier : [config/calendrier_macro_bls.csv](../config/calendrier_macro_bls.csv) (388 dates BLS). Code : [run_prereg14.py](../run_prereg14.py). Résultats : [results/prereg14/](../results/prereg14/). Compteur global : 1 473.*

## Résultats

| Période | Variante | R/an (vs base) | Max DD (R) | Réduction DD | Aléatoire p95 | Critères |
|---|---|---|---|---|---|---|
| 2016–2026 | **base** | **+19,3** | **−25,4** | — | — | — |
| | V1 pas de trade les nuits d'annonce | +12,3 (64 %) | −33,2 | **−31 %** (pire) | 14 % | ✘ ✘ ✘ |
| | V2 sortie 8:25 les nuits d'annonce | +14,3 (74 %) | −26,9 | −6 % (pire) | 2 % | ✘ ✘ ✘ |
| 2011–2015 | **base** | **+28,6** | **−22,4** | — | — | — |
| | V1 | +24,1 (84 %) | −20,4 | 9 % | 17 % | ✘ ✔ ✘ |
| | V2 | +27,9 (97 %) | −21,2 | 5 % | 5 % | ✘ ✔ ✔ |

**Verdict pré-enregistré : aucune variante retenue. La règle reste inchangée : on garde la position pendant les annonces.**

## L'hypothèse était fausse, dans le sens inverse

| Période | Nuits d'annonce | R/trade nuits d'annonce | R/trade autres nuits | Pires nuits qui sont des nuits d'annonce |
|---|---|---|---|---|
| 2016–2026 | 249 (9 %) | **+0,299** | +0,054 | **0 / 10** |
| 2011–2015 | 106 (10 %) | **+0,191** | +0,108 | **0 / 10** |

- Les nuits NFP/CPI sont les **meilleures** nuits de la règle, pas les pires. Aucune des 10 pires nuits n'en fait partie, sur aucune des deux périodes.
- Tenir jusqu'à 9:30 plutôt que sortir à 8:25 rapporte +0,21 R par nuit d'annonce [+0,13 ; +0,30] sur 2016–2026 ; +0,03 [−0,11 ; +0,16] sur 2011–2015.
- Sur 2016–2026, ces 9 % de nuits fournissent environ **40 % des R** de la règle (249 × 0,299 ≈ 74 R sur ≈ 186 R).
- C'est cohérent avec la « prime d'annonce macro » documentée dans la littérature (rendements moyens plus élevés les jours d'annonce, Savor-Wilson), mais ce n'est **pas validé ici** : c'est une observation faite après coup.

## Conséquences

1. Couper les nuits d'annonce retire une grosse partie du gain : la règle doit les garder.
2. La règle est plus concentrée qu'on ne le pensait : une part importante de son rendement vient de ~24 nuits par an.
3. « Ne trader que les nuits d'annonce » ou « surpondérer ces nuits » est une hypothèse nouvelle, formée sur ces données : elle ne peut être testée honnêtement que sur des données jamais vues (holdout post-2026-08-28 : environ 2 annonces par mois, donc plusieurs années avant d'avoir un échantillon utile).
