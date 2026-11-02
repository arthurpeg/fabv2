# Or (GC) : les affirmations de Fattinger-Ziegler testées sur nos données

*2026-11-02. Exploratoire, non pré-enregistré, demandé en séance. Compteur global : 1 577 → 1 631 (54 tests). Code : [run_gc_fattinger.py](../run_gc_fattinger.py). Sorties : `results/gc_fattinger/` (run.log, hypotheses.csv, periods.csv, unbiasedness.csv, intervals.csv). Papier : « Risk and Return around the Clock », SSRN 2606706, échantillon 2010-2013 ; résumé dans [[resumes_papiers_overnight_recolte1]] (entrée [20]).*

## Ce qui est mesuré

GC 1 minute Databento, 2016-01-05 → 2026-08-28 (holdout non touché). Nos données d'or commencent en 2016 : c'est une réplication **hors échantillon dans le temps** du papier, avec sa méthode :

- jour = clôture 17:00 NY de la veille → 17:00 NY ; 277 rendements logarithmiques par jour (gap de l'arrêt 17:00 → 18:00, puis 276 intervalles de 5 minutes), prix ajustés en ratio aux roulements ;
- jours où l'écart New York / Europe centrale n'est pas de 6 h supprimés, comme dans le papier ; séances courtes et fériés supprimés. Il reste **2 329 jours** ;
- heures données en NY (CET = NY + 6 h sur tous les jours gardés) ;
- IC et p : bootstrap par blocs de 10 jours ; écarts-types de White pour les pentes ; Holm dans chaque famille.

## Résultats

| Code | Affirmation du papier pour l'or | Nos données (2016-2026) | p Holm famille | Verdict |
|---|---|---|---|---|
| H1 | Contribution au prix quasi nulle avant l'ouverture européenne (17:00 → 3:00 NY) | **26,5 %** du prix du jour [23,3 ; 29,7], pour 25,1 % de la variance ; 24 / 19 / 33 % par sous-période | 0,005 | ❌ **contredit** |
| H2 (×8) | Prix et variance arrivent ensemble | Écart prix − variance entre −1,1 et +1,5 point dans les 8 périodes, aucun significatif | 1,00 | ✅ confirmé |
| H3 | Prix bruité (pente b < 1) les 2 à 5 premières heures de Globex | b = 0,68 à 19:00 (p 0,06 ; 0,86 winsorisé), 0,89 à 20:00, puis **> 1** dès 21:00 | ≥ 0,97 | ❌ non confirmé |
| H3 | b ≈ 1 en séance US | b = 1,00 à 1,05 de 9:00 à 16:00 ; b > 1 de 4:00 à 8:00 (1,13 à 5:00, Holm 0,02) et à 15:00 (1,02, Holm 0,02) | — | ✅ en séance US, ⚠️ continuation le matin européen |
| H4 | L'efficience chute entre clôture asiatique (1:00) et ouverture européenne (3:00) | Δ augmente de +0,025 [−0,008 ; +0,058] | 1,00 | ❌ non confirmé |
| H5.1 | Pic à l'ouverture de Tokyo | × 2,0 [1,7 ; 2,3] | 0,005 | ✅ |
| H5.2 | Montée de la volatilité pendant l'Asie | 2:00-3:00 contre 20:00-21:00 : × 0,83 (test mal spécifié, voir plus bas) | 0,055 | ❌ tel que défini |
| H5.3 | Hausse à l'ouverture européenne | 3:00-4:00 contre 2:00-3:00 : × 1,22 [1,14 ; 1,30] | 0,005 | ✅ |
| H5.4 | Pic à 8:20 (ancienne ouverture de la corbeille) | × 1,9 | 0,005 | ✅ (persiste sans corbeille) |
| H5.5 | Pic à 8:30 (macro US) | **× 4,8** [4,0 ; 5,7] ; intervalle le plus volatil de la journée (18,2 bp RMS) | 0,005 | ✅ |
| H5.6 | Pic à 10:00 (macro US) | × 1,9 | 0,005 | ✅ |
| H5.7 | Pic à 13:30 (règlement, ancienne clôture de la corbeille) | × 1,36 [1,07 ; 1,75] | 0,03 | ✅ |
| H5.8 | Pic à 14:00 les jours FOMC | × 7,3 [5,0 ; 9,7] (145 jours) | 0,005 | ✅ |
| H5.9 | Pic à 16:00 (clôture des actions US) | × 1,12 [0,96 ; 1,29] | 0,15 | ❌ |
| H6 | Pas de U en séance COMEX | Bords/milieu = 0,89 [0,83 ; 0,96] : début × 1,23, fin × 0,55 ; profil décroissant, pas de U | — | ✅ |
| H7 | Sauts = 5 à 13 % de la variance | **9,0 %** [7,8 ; 10,2] ; 11,8 / 8,5 / 8,0 % par sous-période ; 0,6 saut détecté par jour | — | ✅ |
| H8 | Le plus gros saut est à 8:30 | Rang 1 dans 100 % des tirages ; **2,0 %** de la variance totale [1,5 ; 2,6] (papier : 1,22 %) ; puis 10:00 (0,50 %) et 14:00 (0,32 %) | < 0,001 | ✅ |
| H9 | Métaux : sauts de 10:00 > sauts de la Fed | 0,50 % contre 0,52 %, écart nul | 0,97 | ❌ |
| H10 | Le saut de 8:30 vient des annonces | 91 % de la variance de saut de 8:30 tombe les jours d'annonce (23 % des jours) | 0,001 | ✅ |
| H11 | Hors séance COMEX, volume < volatilité | Hors 8:20-13:30 : 51 % du volume pour 66 % de la volatilité (+15,5 points) | 0,004 | ✅ |
| H12-H13 | Aux annonces et aux ouvertures/clôtures, le volume monte plus que la volatilité | Vrai à 8:30, 10:00, 8:20, 13:30 et 9:30 (excès +0,04 à +0,52 point) | 0,004 | ✅ |
| H14 | Plus de prix par contrat la nuit | Nuit 18:00 → 3:00 : 26,5 % du prix pour 20,6 % du volume, soit **× 1,29** [1,14 ; 1,43] | 0,004 | ✅ |

## Lecture

**Ce qui se reproduit** (sur une période différente, sans corbeille depuis 2015) : la mécanique de microstructure. Les pics de volatilité tombent aux annonces US (8:30 domine tout, puis 10:00 et la Fed), à l'ouverture de Tokyo, à l'ouverture européenne, et aux anciennes heures de corbeille (8:20, 13:30), qui restent des points focaux. Pas de U en séance COMEX. Les sauts pèsent environ 9 % de la variance, concentrés à 8:30 les jours d'annonce. La nuit, peu de volume et beaucoup de mouvement : chaque contrat y déplace davantage le prix.

**Ce qui ne se reproduit pas** :
- **L'or fait aujourd'hui un quart de son prix avant l'Europe** (H1), exactement sa part de variance. L'affirmation du papier (« contribution quasi nulle jusqu'à l'ouverture européenne ») ne tient pas en 2016-2026, et l'écart se creuse en 2023-2026 (33 %). C'est cohérent avec le lot du 2026-11-02 (découverte du prix partiellement en Asie depuis 2014) et avec notre reprise du soir ([[reports/gc_sessions_report]]).
- **Le début de Globex n'est pas significativement bruité** (H3, H4). La pente est sous 1 à 19:00 dans les trois sous-périodes (0,67 / 0,44 / 0,76), donc le mouvement 17:00 → 19:00 tend à se défaire, mais c'est porté par les queues (0,86 winsorisé) et non significatif après Holm. Un fade du début de Globex sur l'or n'est pas justifié par ces données.

**Ce qui est nouveau (à ne pas sur-interpréter)** : de 4:00 à 8:00 NY la pente dépasse 1 (1,13 à 5:00, Holm 0,02). Le mouvement 17:00 → 5:00 se **prolonge** en moyenne le reste de la journée (b − 1 = 0,13 : pour un mouvement de nuit d'un écart-type, environ 58 bp, la suite fait en moyenne +7 bp dans le même sens). Mais c'est **entièrement 2023-2026** (b(5:00) = 0,97 / 1,07 / 1,21 ; t +4,1 sur 2023-2026), une période de forte tendance de l'or, et c'est trouvé parmi 23 coupures. Candidat au holdout tout au plus, pas un résultat.

**Limites** :
- H5.2 était mal spécifié : la fenêtre de comparaison 20:00-21:00 contient les ouvertures de Tokyo (en été) et de Shanghai. Le profil horaire (descriptif) montre bien un creux à 23:00-0:00 (3,8 à 4,0 bp RMS) puis une remontée jusqu'à 3:00 (5,8 bp), ce qui va dans le sens du papier, mais ce n'est pas le test prévu.
- La contribution au prix au sens du papier (moyenne de r_période / r_jour) est instable : P2 vaut 22 % brut contre 11 % winsorisé. Le verdict s'appuie sur la contribution pondérée (Barclay-Warner), robuste.
- Pas d'argent ni de cuivre dans nos données : les comparaisons entre métaux du papier ne sont pas testées.
- Annonces de 8:30 : les inscriptions au chômage (hebdomadaires) ne sont pas dans `config/calendrier_macro_us.csv` ; certains jours « sans annonce » en ont une.

## Conclusion

Sur 54 tests, la partie microstructure du papier se reproduit sur l'or en 2016-2026 (pics, sauts, volume). Les deux affirmations qui auraient pu donner une idée de trading ne se reproduisent pas : la découverte du prix ne se fait pas seulement en Europe et aux US (un quart se fait avant 3:00 NY), et le début de Globex n'est pas significativement bruité. Rien ici n'est une règle. La continuation 5:00 → 17:00 de 2023-2026 n'est qu'un candidat au holdout postérieur au 2026-08-28.
