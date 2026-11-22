# ORB 30 minutes NQ, lundi à jeudi : biais EMA 20/50 multi-unités, cassure et réintégration

*2026-11-22. Suite de l'étape 1 de [[wiki/experiments/orb30-jours-semaine]]. Idée de l'utilisateur. Grille figée et commitée dans l'en-tête de [run_orb30_biais.py](../run_orb30_biais.py) avant tout calcul (commit `d6cf9d3`). **Un bug de sens** (les réintégrations étaient prises à l'envers) a été trouvé à la vérification manuelle du premier calcul, corrigé sans toucher à la grille (commit suivant), et le calcul relancé ; le premier résultat est écarté. NQ, exploration 2016-06 → 2026-08 ; réserve 2010-06 → 2015-12 non lue. Compteur global : 2 071 (2 058 + 13 essais). Sorties : `results/orb30_biais/`.*

## Règle

- **Biais à 10:00** : EMA 20 contre EMA 50 sur 15 min, 1 h, 4 h (nuit comprise) et jour (clôtures de 16:00), bougies terminées seulement ; vote majoritaire. Sur les 2 120 lundis-jeudis : haussier 1 182, baissier 435, égalité 2-2 503 ; les 4 votes ne sont d'accord que 33 % du temps.
- **Cassure dans le sens du biais** : ordre stop sur la borne (range 9:30-9:59), stop à 1 W.
- **Réintégration contre le biais** : après une cassure de l'autre borne puis une clôture 1 min de retour dans le range, ordre limite sur cette borne (rempli si le prix la dépasse d'1 tick) ; stop à 1 W ou au-delà de la mèche.
- Un trade par jour, objectif 2R, sinon 16:00 ; 1 contrat, coût 0,50 pt.
- **Vérification manuelle** (2016-07-19, biais haussier) : cassure du bas à 13:55, reclôture dans le range à 14:00, achat limite rempli à 14:01 sur le bas du range ; stop sous la mèche à 1,5 pt, objectif 3 pts atteint (+2,50 net). Conforme.

## Résultats (R net par trade ; référence = ORB 30 min objectif 2R sans biais, mêmes jours : +0,015 R, +0,88 pt par jour)

| Variante | Égalité | Trades | R net | t NW | R cassures | R réintégrations | Écart avec la référence (pts/jour, t) | Années + |
|---|---|---|---|---|---|---|---|---|
| Complète, stop 1 W | pas de trade | 1 493 | +0,037 | 1,44 | +0,030 | +0,048 | +1,51 (0,54) | 9/11 |
| Complète, stop 1 W | ORB classique | 1 985 | +0,015 | 0,68 | +0,030 | +0,048 | +0,53 (0,21) | 6/11 |
| Complète, stop 1 W | le jour tranche | 1 970 | +0,032 | 1,44 | +0,022 | +0,046 | +1,30 (0,46) | 8/11 |
| Complète, stop mèche | pas de trade | 1 492 | −0,009 | −0,30 | +0,030 | −0,063 | +0,43 (0,23) | 4/11 |
| Complète, stop mèche | ORB classique | 1 984 | −0,019 | −0,79 | +0,030 | −0,063 | −0,55 (−0,34) | 4/11 |
| Complète, stop mèche | le jour tranche | 1 969 | −0,028 | −1,08 | +0,022 | −0,097 | +0,16 (0,09) | 3/11 |
| Cassure seule | pas de trade | 1 099 | +0,033 | 1,11 | +0,033 | — | +0,63 (0,35) | 9/11 |
| Cassure seule | ORB classique | 1 591 | +0,007 | 0,28 | +0,033 | — | −0,34 (−0,23) | 7/11 |
| Cassure seule | le jour tranche | 1 453 | +0,033 | 1,37 | +0,033 | — | +0,62 (0,37) | 8/11 |
| **Réintégration seule, stop 1 W** | pas de trade | 931 | **+0,045** | 1,40 | — | +0,045 | +1,37 (0,44) | 7/11 |
| Réintégration seule, stop 1 W | le jour tranche | 1 227 | +0,033 | 1,14 | — | +0,033 | +1,61 (0,48) | 7/11 |
| Réintégration seule, stop mèche | pas de trade | 930 | −0,093 | −2,08 | — | −0,093 | −0,63 (−0,29) | 1/11 |
| Réintégration seule, stop mèche | le jour tranche | 1 226 | −0,126 | −3,35 | — | −0,126 | −0,56 (−0,25) | 1/11 |

**Règle choisie (meilleur Sharpe)** : réintégration seule, stop 1 W, pas de trade en cas d'égalité. n 931 · +0,045 R · t NW 1,40 · 48,4 % de gagnants · pire creux −23 R · 7/11 années · moitiés +0,045 / +0,044 · écart avec la référence +1,37 pt par jour (t 0,44) · DSR (N = 73) 0,009. **B1 : ❌** (t, DSR et référence).

## Lecture

1. **Le biais de tendance n'ajoute presque rien.** Les meilleures variantes font +0,03 à +0,045 R par trade contre +0,015 R sans biais, avec des écarts à t 0,2 à 0,5 seulement. Aucune n'atteint t = 2.
2. **Réintégration et cassure se valent** (+0,045 et +0,030 R avec le stop à 1 W) : prendre la fausse cassure contre le biais ne coûte rien, mais ne rapporte pas non plus de façon démontrable.
3. **Le stop sous la mèche est mauvais** : il est souvent minuscule (quelques ticks), le coût pèse lourd en R, et le prix revient le chercher (objectif atteint ~32 % du temps, mais 1 année positive sur 11 en réintégration seule).
4. **L'égalité 2-2 traitée par l'ORB classique** dilue le résultat ; « pas de trade » ou « le jour tranche » font mieux, sans que la différence soit significative.
5. Le biais est très déséquilibré (56 % de jours haussiers, 21 % baissiers) : il reflète surtout la hausse de long terme du Nasdaq.

## Conclusion

B1 ❌. Du lundi au jeudi, ni l'ORB, ni ses conditions (C1-C3), ni ce biais de tendance avec réintégration ne donnent un avantage démontrable sur NQ. Ligne au registre des échecs.
