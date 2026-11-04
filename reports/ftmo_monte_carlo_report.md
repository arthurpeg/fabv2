# Monte-Carlo des deux comptes FTMO 10k (A = mom, B = 3n + M2), règle des annonces + cible + attente

*2026-11-04. **Exploratoire, hors compteur.** Script : [run_ftmo_monte_carlo.py](../run_ftmo_monte_carlo.py). Sorties : `results/ftmo_monte_carlo/` (`run.log`, `chemins_<scénario>.csv`). 5 000 chemins de 3 ans (756 séances) par scénario, graine 1831.*

## Méthode

**Historiques synthétiques.** Chaque chemin est tiré par bootstrap stationnaire (Politis-Romano) des séances 2011-07 → 2026-11-03 :
- les blocs ont une longueur moyenne de 20 séances, soit environ un mois : les séries et les régimes de marché sont conservés à cette échelle ;
- une séance tirée garde ensemble ses trades mom, 3n et M2 : la corrélation entre les deux comptes est conservée.

**Règles.** Celles de [[reports/ftmo_deux_comptes_historique_report]] : éval à 2,5 % avec objectif ramené au reste à faire ; financé à 1 % ; règle des annonces ; cible + attente ; reward après 10 séances ; rachat immédiat.

**Scénarios.**
- **Historique** : toutes les séances.
- **Récent** : 2019-2026 seulement, une période plus difficile pour mom.
- **Edge / 2** : on retire à chaque trade la moitié du R moyen de sa stratégie (3n +0,160, M2 +0,137, mom +0,124). L'espérance est divisée par deux, la volatilité ne change pas. C'est le scénario prudent pour 3n et M2, qui ont échoué hors échantillon.

## Résultats

| Deux comptes 10k, 3 ans | **Historique** | **Récent (2019-2026)** | **Edge / 2** |
|---|---|---|---|
| Net à 1 an : médiane (5e centile) | +3 916 $ (+1 680 $) | +3 649 $ (+1 420 $) | +2 301 $ (+327 $) |
| P(net < 0 à 1 an) | 0,1 % | 0,2 % | 2,7 % |
| **Net à 3 ans : médiane (5e / 1er centile)** | **+12 889 $** (+8 798 / +7 243 $) | **+12 305 $** (+8 092 / +6 420 $) | **+7 939 $** (+4 175 / +2 730 $) |
| P(net < 0 à 3 ans) | 0 % | 0 % | 0 % |
| Net à 3 ans, A / B (médianes) | +7 096 / +5 827 $ | +5 414 / +6 811 $ | +4 636 / +3 213 $ |
| Corrélation des nets A / B | +0,10 | +0,14 | +0,08 |
| **Max DD de trésorerie : médiane / 95e / 99e centile / pire** | −348 / −608 / −782 / −1 477 $ | −348 / −695 / −869 / −1 304 $ | −521 / −956 / −1 304 / −2 781 $ |
| **Pire série d'évals sans reward, A : médiane / 95e / 99e / max** | 3 / 7 / 9 / 15 | 4 / 9 / 12 / 17 | 5 / 10 / 14 / 26 |
| P(série A ≥ 6 évals) | 14 % | 28 % | 42 % |
| **Pire série d'évals sans reward, B : médiane / 95e / 99e / max** | 2 / 4 / 6 / 10 | 2 / 4 / 6 / 10 | 3 / 7 / 10 / 20 |
| Plus longue période sans aucun reward : médiane / 95e centile (séances) | 80 / 132 | 82 / 138 | 106 / 178 |
| Premier reward : médiane / 95e centile (séances) | 30 / 78 | 30 / 81 | 36 / 104 |
| Évals sur 3 ans (A / B) | 8,9 / 3,2 | 11,6 / 3,4 | 14,1 / 6,6 |
| Rewards sur 3 ans | 41,8 | 40,9 | 29,8 |

## Lecture

1. **Même avec une espérance divisée par deux, les deux comptes restent gagnants sur 3 ans dans tous les chemins.** La médiane est à +7 900 $ et le 1er centile à +2 700 $. Le contrat FTMO borne la perte au prix de l'éval, alors que le gain d'un compte financé n'a pas de plafond. Tant que les stratégies ont une espérance positive, même faible, un emplacement racheté finit gagnant. C'était déjà la leçon du n° 18. Sur un an, le scénario prudent reste perdant dans 2,7 % des chemins.
2. **Réserve de trésorerie à prévoir.** Dans 99 % des chemins, il suffit de 800 à 900 $ (historique et récent), ou de 1 300 $ avec une espérance divisée par deux. Le pire chemin demande 2 800 $.
3. **Séries d'évals ratées.** Sur le compte A (mom), 7 à 10 évals d'affilée sans reward arrivent dans 5 % des chemins, et jusqu'à 15-26 évals dans les pires cas. Une série de 6 évals ou plus arrive dans 14 % des chemins (historique) à 42 % (edge / 2). Le compte B est beaucoup plus stable, avec 4 à 7 évals au 95e centile : la politique d'attente garde ses comptes financés longtemps.
4. **Les deux comptes se compensent** : la corrélation de leurs résultats n'est que de +0,08 à +0,14. Au 95e centile, on reste environ 130 à 180 séances (6 à 8 mois) sans aucun reward.
5. **Limites** :
   - Les blocs d'un mois ne reproduisent pas les régimes plus longs, comme les phases de 2022 ou de 2023.
   - Les délais FTMO, les refus de reward et le spread réel du CFD ne sont pas modélisés.
   - Le scénario « edge / 2 » est la référence prudente pour 3n et M2.
