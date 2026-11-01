# Or (GC) : quelle session de la journée rapporte, et est-ce significatif ?

*2026-11-01. Exploratoire, non pré-enregistré, demandé en séance. Compteur global : 1 520 → 1 553 (7 sessions + 23 heures + 3 fenêtres a posteriori autour de l'arrêt quotidien). Code : [run_gc_sessions.py](../run_gc_sessions.py). Sorties : `results/gc_sessions/` (run.log, sessions.csv, summary.csv, by_period.csv, by_year.csv, hours.csv, posthoc_halt.txt).*

## Ce qui est mesuré

GC 1 minute Databento, 2016-01-04 → 2026-08-28 (holdout non touché), prix ajustés en ratio aux roulements G J M Q V Z (`recolte1.engine.load`). Un jour GC va de la clôture 17:00 NY du jour ouvré précédent à 17:00 NY : la première session contient donc l'arrêt 17:00 → 18:00 et le gap de réouverture (et le week-end pour le lundi). 2 510 jours ont les 8 bornes ; la décomposition est contrôlée (produit des sessions = rendement 17:00 → 17:00).

| Session | Bornes (heure locale) | Durée de cotation moyenne |
|---|---|---|
| reprise | 17:00 NY veille → 9:00 Shanghai (ouverture SGE) | 2,7 h |
| asie | 9:00 Shanghai → 8:00 Londres | 6,4 h |
| ldn_am | 8:00 → 10:30 Londres (fixing LBMA AM) | 2,5 h |
| ldn_mid | 10:30 Londres → 8:20 NY (ouverture COMEX) | 2,8 h |
| comex_am | 8:20 NY → 15:00 Londres (fixing LBMA PM) | 1,7 h |
| comex_pm | 15:00 Londres → 13:30 NY (règlement COMEX) | 3,4 h |
| post | 13:30 → 17:00 NY | 3,5 h |

Pour chaque session, position longue : rendement brut et net (1 tick + 5 $ aller-retour) par vectorbt, t de Newey-West (5 retards), IC 95 % bootstrap par blocs, correction de Holm sur 7 sessions. Comme l'or a fortement monté (+4,0 bp par jour en moyenne), on teste aussi l'**excès sur la dérive proportionnelle** : la session fait-elle mieux que sa part de durée × la dérive journalière ?

## Résultats par session (2016-2026)

| Session | Moy. brute (bp) | IC 95 % | t NW | p Holm | Net (bp) | Sharpe net | Part durée | Excès (bp, t) | p Holm excès |
|---|---|---|---|---|---|---|---|---|---|
| **reprise** | **+1,98** | [+0,94 ; +3,07] | **+3,54** | **0,003** | +1,11 | +0,60 | 12 % | +1,52 (+2,71) | 0,047 |
| asie | +0,27 | [−1,32 ; +1,86] | +0,33 | 1,00 | −0,59 | −0,21 | 28 % | −0,84 (−1,00) | 1,00 |
| ldn_am | +0,41 | [−0,73 ; +1,57] | +0,69 | 1,00 | −0,46 | −0,24 | 11 % | −0,03 (−0,04) | 1,00 |
| ldn_mid | +1,01 | [−0,13 ; +2,14] | +1,70 | 0,44 | +0,14 | +0,07 | 12 % | +0,53 (+0,89) | 1,00 |
| comex_am | −0,86 | [−2,69 ; +0,92] | −0,89 | 1,00 | −1,72 | −0,58 | 8 % | −1,16 (−1,21) | 1,00 |
| comex_pm | −0,19 | [−1,99 ; +1,63] | −0,19 | 1,00 | −1,05 | −0,35 | 15 % | −0,78 (−0,81) | 1,00 |
| post | +1,33 | [−0,03 ; +2,71] | +1,92 | 0,33 | +0,47 | +0,22 | 15 % | +0,73 (+1,05) | 1,00 |
| séance entière | +3,99 | [+0,21 ; +7,85] | +1,94 | — | — | — | 100 % | — | — |

- **Une seule session est significative : la reprise** (17:00 NY → 9:00 Shanghai), +2,0 bp brut, t 3,5, Holm 0,003, et positive dans les 3 sous-périodes (+1,6 / +1,3 / +3,0 bp ; t 2,6 / 1,2 / 2,5), 7 années positives sur 11. Elle fait la moitié de la dérive de l'or en 12 % des heures de cotation ; l'excès sur la dérive proportionnelle passe tout juste Holm (0,047).
- **Net, elle ne passe plus** : +1,1 bp, t 2,0, Sharpe 0,60. Le coût (≈ 0,9 bp aller-retour) mange plus de la moitié.
- **Les sessions de Londres et du COMEX sont nulles.** Le COMEX du matin (8:20 → fix PM) est même négatif dans 2 sous-périodes sur 3 et 8 années sur 11, mais sans significativité (t −0,9).
- **Le post-règlement (13:30 → 17:00)** est positif 9 années sur 11 et monte en 2023-2026 (+2,9 bp, t 1,9), mais n'est pas significatif sur la période (Holm 0,33). Tout vient de la dernière heure (voir ci-dessous).

## Heure par heure (23 heures NY, Benjamini-Hochberg)

Seules 3 heures ont une moyenne brute avec IC hors de 0, et toutes encadrent l'arrêt quotidien :

| Heure NY | Moy. brute (bp) | t NW | q BH | 2016-19 / 2020-22 / 2023-26 |
|---|---|---|---|---|
| 16:00 → 17:00 (dernière heure avant l'arrêt) | +0,67 | +2,75 | 0,05 | −0,02 / +1,04 / +1,12 |
| 17:00 veille → 19:00 (arrêt + gap + 1re heure) | +1,56 | +3,43 | 0,01 | +1,28 / +1,09 / +2,25 |
| 19:00 → 20:00 | +0,78 | +2,73 | 0,05 | +0,64 / +0,93 / +0,82 |

Les 20 autres heures sont nulles (q BH ≥ 0,60). Somme de ces trois heures : ≈ 3 bp, soit les trois quarts de la dérive journalière (+4,0 bp).

## Contrôle a posteriori : la fenêtre 16:00 → 19:00 NY

Fenêtre choisie **après** avoir lu le tableau horaire (3 essais de plus au compteur), donc purement descriptive :

| Fenêtre | Brut (bp, t) | Net (bp, IC, t) | Sharpe net | Net par sous-période |
|---|---|---|---|---|
| 16:00 → 19:00 | +2,23 (t 4,3) | +1,37 [+0,34 ; +2,41] (t 2,7) | +0,79 | +0,05 / +1,52 / +2,68 |
| 17:00 → 19:00 | +1,56 (t 3,4) | +0,69 [−0,24 ; +1,62] (t 1,5) | +0,45 | +0,12 / +0,25 / +1,69 |
| 16:00 → 17:00 | +0,67 (t 2,8) | −0,19 (t −0,8) | −0,25 | −1,18 / +0,20 / +0,57 |

Net, 16:00 → 19:00 garde un IC hors de 0. Mais c'est une sélection après coup parmi 33 essais : avec Bonferroni sur ces 33 essais, p ≈ 0,26. C'est nul en 2016-2019 net, et tout vient de 2020-2026, une période de forte hausse de l'or. Rien ici n'est validé.

## Conclusion

- **Significatif** : seule la reprise du soir (clôture 17:00 → ouverture de Shanghai), en brut, est robuste aux tests multiples et stable dans les sous-périodes. Plus précisément, c'est la fenêtre 16:00 → 20:00 NY autour de l'arrêt quotidien qui porte l'essentiel de la hausse de l'or 2016-2026. C'est la même famille que la [[wiki/concepts/prime-de-nuit|prime de nuit]], mais concentrée sur quelques heures au lieu d'être étalée sur l'Asie.
- **Non significatif** : Asie (séance SGE), Londres (avant et après le fix AM), COMEX (avant et après le fix PM), post-règlement hors dernière heure.
- **Tradable ?** Non démontré : net, la reprise ne vaut que +1,1 bp (t 2,0) ; la fenêtre 16:00 → 19:00 (+1,4 bp net) a été choisie après coup et ne marche pas en 2016-2019. Elle est candidate à un pré-enregistrement sur le holdout postérieur au 2026-08-28, avec un contrôle de régime (long de l'or seul sur la même durée, pour séparer l'effet d'heure de la tendance).
- Cohérent avec les résultats déjà obtenus sur GC : [[reports/recolte1_report]] (nuit longue GC +3,7 à +4,0 bp net ; session US de GC nulle ; Asie de Wei nulle) et le registre (close-to-open GC avec stops ATR négatif net).

## Anatomie de la reprise (suite, même jour)

*Compteur 1 559 → 1 577 (4 jambes, 5 jours de semaine, 7 états conditionnels, roulements, queues). Code : [run_gc_reprise.py](../run_gc_reprise.py). Sorties : `results/gc_reprise/`. 2 486 jours complets.*

| Jambe | Brut (bp) | t NW | 2016-19 / 2020-22 / 2023-26 |
|---|---|---|---|
| Gap 17:00 → 18:05 (arrêt + 5 premières minutes) | +1,22 | +3,6 | +0,8 / +2,3 / +0,8 |
| 18:05 → 19:00 | +0,25 | +0,8 | +0,4 / −1,1 / +1,2 |
| 19:00 → 20:00 (ouverture de Tokyo en hiver) | +0,97 | +3,2 | +0,8 / +1,0 / +1,2 |
| 20:00 → 9:00 Shanghai (0 h en hiver, 1 h en été) | −0,42 | −1,4 | — |
| Reprise entière | +2,01 | +3,5 | +1,6 / +1,2 / +3,1 |

- **Deux moments portent tout** : le gap de l'arrêt (le cours de 18:05 au-dessus de la clôture de 17:00) et l'heure 19:00 → 20:00 NY. Les deux sont positifs dans les trois sous-périodes.
- **Pas le lundi** : lundi (week-end inclus) +0,1 bp, σ 48 bp ; mardi +2,5, mercredi +2,6, jeudi +3,5 (t 3,5), vendredi +1,1. Hors lundis : +2,5 bp, t 4,1 (lecture a posteriori).
- **Pas un artefact de roulement** : les roulements tombent à 00:00 UTC, dans la session, mais seuls 22 jours de séance sont concernés ; sans les jours de roulement (± 1 j) : +2,05 bp, t 3,6.
- **Pas seulement les queues** : médiane +0,7 bp, moyenne tronquée à 5 % +1,3 bp, sans les 1 % de chaque queue +1,9 bp (t 4,3). Mais les 20 meilleurs jours font 62 % de la somme, et les plus gros mouvements datent de 2026 (±200 à 300 bp).
- **Pas de conditionnement utile** : séance précédente > 0 : +2,7 bp contre +1,3 (écart t 1,1) ; tendance 20 j : aucun écart (t 0,1) ; vol haute +2,9 contre +1,5 à +1,7 (IC larges).
- **Liquidité faible** : 46 contrats/minute vers 18-20 h NY contre 288 en séance COMEX (8-13 h) et 39 à 16 h. Le coût standard (1 tick) est probablement optimiste le soir ; aucune donnée bid/ask GC dans `cache/databento_bbo/` pour le vérifier.
- **Lecture** : c'est une prime de nuit « de reprise » sur l'or, concentrée sur la réouverture et l'heure suivante, pas un effet asiatique (la séance SGE elle-même est nulle). Net du coût standard, elle reste sous 1,5 bp et dépend de l'hypothèse de coût. À pré-enregistrer sur le holdout seulement, idéalement avec des données bid/ask du soir.
