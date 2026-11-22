# Règle de la 1ʳᵉ bougie (Zarattini-Aziz) sur ES, YM et NQ : autres sorties, stop 1 ATR

*2026-11-22. Suite de l'étape 1 de [[wiki/experiments/nq-orb-bougie-sorties]] (premier passage : [[reports/nq_orb_bougie_report]]). Grille figée et commitée dans l'en-tête de [run_orb_bougie_indices.py](../run_orb_bougie_indices.py) avant tout calcul (commit `40cfcc9`). Données Databento 1 min, 2010-06 → 2021-09-30 seulement ; la réserve « sortie » 2021-10-01 → 2026-08-28 (ES, YM, NQ) n'a pas été lue. Compteur global : 2 021 (1 965 + 56 essais : ES 27, YM 27, NQ 2). Sorties : `results/orb_bougie_indices/` (`grille.csv`, `trades_detail_<actif>.csv`, `summary.txt`).*

## Règle

Sens de la bougie 9:30-9:35 ET, entrée à 9:35, 1 contrat, pas de trade sur un doji (≤ 1 tick). Stop = k × ATR14 (amplitude moyenne 9:30-16:00 des 14 séances précédentes), objectif = RR × stop, sinon sortie à 16:00. Coût standard : ES 0,35 pt, YM 2 pts, NQ 0,50 pt. Grille : V0 (aucun stop ni objectif), k ∈ {0,05 ; 0,10 ; 0,25 ; 0,50} × RR ∈ {1, 2, 3, 5, 10, clôture}, et k = 1 × RR ∈ {2, 3} (stop 1 ATR, objectif 2 ou 3 ATR).

## Vue d'ensemble (points nets par trade, t de Newey-West)

| Variante | ES | YM | NQ |
|---|---|---|---|
| V0 sans stop ni objectif | **+0,68** (t 2,11) | +0,91 (t 0,33) | **+2,83** (t 2,48) |
| stop 0,05 ATR, clôture | −0,23 (t −2,03) | −0,94 (t −1,04) | +1,52 (t 3,16) |
| stop 0,10 ATR, RR 10 | +0,01 (t 0,06) | +0,06 (t 0,05) | +1,79 (t 3,10) |
| stop 0,25 ATR, clôture | +0,36 (t 1,42) | +0,33 (t 0,17) | +1,17 (t 1,49) |
| **stop 0,50 ATR, RR 2** | +0,50 (t 1,66) | +0,43 (t 0,18) | **+2,23** (t 2,17) |
| **stop 0,50 ATR, RR 3** | +0,38 (t 1,23) | +0,26 (t 0,10) | +1,83 (t 1,77) |
| **stop 1 ATR, RR 2 (objectif 2 ATR)** | +0,42 (t 1,20) | −1,48 (t −0,47) | +2,02 (t 1,75) |
| **stop 1 ATR, RR 3 (objectif 3 ATR)** | +0,42 (t 1,20) | −1,52 (t −0,48) | +2,17 (t 1,87) |
| R4, papier (référence) | +0,00 (t 0,01) | +0,88 (t 0,52) | +1,32 (t 1,89) |
| Trades | 2 414 | 2 639 | 2 671 |

Toutes les variantes : `results/orb_bougie_indices/grille.csv`.

- **ES** : les stops serrés perdent tous (k = 0,05 et 0,10 négatifs, jusqu'à t −7,9 pour RR 1). Seules les variantes larges (k ≥ 0,25) et V0 sont positives. Meilleur Sharpe : V0 (+0,68 pt, Sharpe 0,60, 2010-2015 +0,22, 2016-2021 +1,09, 2020 +3,58), qui ne bat « toujours long » qu'à t 1,24. DSR (N = 28) 0,002 : **B1 ❌**.
- **YM** : rien. Aucune variante n'atteint |t| = 0,6 du bon côté ; les ventes perdent (V0 : achats +3,02, ventes −1,22). Meilleure : stop 0,10 ATR, clôture, +0,54 pt, t 0,39. **B1 ❌** (cinq critères sur six ratés).
- **NQ** : les deux nouvelles variantes (stop 1 ATR) font +2,02 et +2,17 pts, t 1,75 et 1,87. La meilleure reste stop 0,05 ATR, clôture.

## B1 sur NQ : un passage qui n'en est pas un

Le script calcule le DSR avec une famille de 28 variantes propre à chaque actif, comme fixé dans l'en-tête. Sur NQ, cela donne **0,953**, donc B1 « franchie », alors que le premier passage donnait 0,948 avec la même règle. La seule différence : l'ajout des deux variantes « stop 1 ATR » a réduit la dispersion des Sharpe de la famille (variance 3,4 × 10⁻⁴ → 3,2 × 10⁻⁴), ce qui baisse le seuil du DSR.

Mais la règle NQ a aussi été choisie **parmi trois indices**, sur la même idée. Le protocole demande de compter dans `n_famille` toutes les variantes parmi lesquelles la règle a été choisie. Avec la famille complète (81 variantes sur ES, YM et NQ, plus R4), le DSR de la même règle vaut **0,02**. C'est ce chiffre qui fait foi. **Verdict : B1 ❌ sur les trois indices.**

## Détail : stop 0,5 ATR, objectif 2R

| | NQ | ES | YM |
|---|---|---|---|
| Net par trade | **+2,23 pts (+45 $)** | +0,50 pt (+25 $) | +0,43 pt (+2 $) |
| t NW / Sharpe | 2,17 / 0,69 | 1,66 / 0,55 | 0,18 / 0,06 |
| Médiane | −2,75 | −1,60 | −15,0 |
| Gagnants | 47,4 % | 45,4 % | 43,9 % |
| Gain moyen / perte moyenne | +38,5 / −30,5 pts | +12,3 / −9,3 | +98,9 / −76,7 |
| Sorties : stop / objectif / 16:00 | 36 % / 12 % / 52 % | 37 % / 13 % / 50 % | 38 % / 12 % / 51 % |
| Résultat moyen en R | +0,064 R | +0,030 R | −0,001 R |
| Stop moyen | 37,8 pts | 11,7 pts | 98,1 pts |
| Pire creux (1 contrat) | −2 060 pts (−41 207 $) | −504 pts (−25 202 $) | −4 619 pts (−23 097 $) |
| Achats / ventes | +2,64 / +1,80 | +0,61 / +0,40 | +0,69 / +0,17 |
| « Toujours long », mêmes sorties (t écart) | +0,56 (1,37) | −0,22 (2,14) | −0,79 (0,46) |
| 2010-2015 / 2016-2021 | +0,96 / +3,38 | +0,10 / +0,87 | +0,09 / +0,75 |

Par année sur NQ (pts/trade) : 2010 +1,77 · 2011 +1,93 · 2012 +0,10 · 2013 +1,64 · 2014 +3,18 · 2015 −2,37 · 2016 +1,59 · 2017 +2,34 · **2018 +8,23** · 2019 −0,33 · 2020 +0,51 · **2021 (jusqu'en septembre) +9,29**. 10 années positives sur 12. Les deux meilleures années pèsent 75 000 $ sur un total d'environ 119 000 $ (1 contrat, 11,3 ans).

Sur ES, les années positives sont 2014 et 2018-2021, toutes les autres sont légèrement négatives. Sur YM, les années alternent de −15 à +16 pts/trade, sans tendance.

**Lecture** : sur NQ, c'est la variante la plus régulière avant 2016 (+0,96 pt/trade sur 2010-2015, contre +0,23 pour la meilleure en Sharpe). Mais son avantage tient à t 2,2 sur 11 ans, elle ne bat « toujours long » qu'à t 1,37, et son creux (−41 000 $ par contrat) vaut près de 4 ans de gain moyen.

## Détail : stop 0,5 ATR, objectif 3R

Avec un objectif plus loin, on gagne moins sur les trois indices : NQ +1,83 pt (t 1,77), ES +0,38 (t 1,23), YM +0,26 (t 0,10). L'objectif n'est atteint que 3,7 à 3,9 % du temps ; 59 % des trades sortent à 16:00. Sur NQ, le creux s'aggrave (−2 975 pts, −59 499 $) et 2020 devient négatif (−0,97). Passer de 2R à 3R rend surtout les gains de milieu de journée que l'objectif 2R encaissait.

## Détail : stop 1 ATR, objectif 2 ATR ou 3 ATR

L'objectif est presque jamais atteint (NQ : 1,3 % à 2 ATR, 0,2 % à 3 ATR ; ES 1,7 % et 0,3 % ; YM 1,3 % et 0,1 %), et le stop sert dans 12 à 13 % des cas. Ces variantes sont donc presque V0, avec un stop de catastrophe :

| | NQ RR 2 | NQ RR 3 | ES RR 2 | ES RR 3 | YM RR 2 | YM RR 3 |
|---|---|---|---|---|---|---|
| Net (pts) | +2,02 | +2,17 | +0,42 | +0,42 | −1,48 | −1,52 |
| t NW | 1,75 | 1,87 | 1,20 | 1,20 | −0,47 | −0,48 |
| Gagnants | 51,7 % | 51,6 % | 50,4 % | 50,4 % | 48,6 % | 48,6 % |
| Pire creux | −47 335 $ | −45 527 $ | −33 453 $ | −33 453 $ | −44 115 $ | −45 644 $ |

Sur NQ, le stop de 1 ATR coûte 0,7 à 0,8 pt par trade par rapport à V0 (+2,83), sans réduire le creux (−2 367 contre −2 202 pts). Sur YM, il transforme un V0 à +0,91 en −1,48 : les ventes stoppées perdent (−3,05 pts/trade).

## Conclusion

1. **L'effet est propre à NQ** et à 2016-2021. ES montre une trace faible (V0 +0,68 pt, t 2,1, mais pas mieux que « toujours long » et DSR ≈ 0). YM : rien.
2. **Les sorties ne changent pas l'histoire** : les objectifs fixes courts (1R-3R) coûtent, les stops très serrés ne marchent que sur NQ, et un stop large ressemble à « pas de stop ».
3. **B1 ❌ sur les trois indices** : le passage apparent de NQ (DSR 0,953) disparaît avec la famille complète (DSR 0,02). Ligne ajoutée au registre ; la réserve 2021-10 → 2026-08 reste non lue.
