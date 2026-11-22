---
type: report
date: 2026-11-22
statut: exploration (hors compteur, analyse de sensibilité)
---

# FTMO : trader au hasard, ou trader une edge qui peut mourir en live ?

Demande du 2026-11-22. Script : [run_ftmo_edge_mort.py](../run_ftmo_edge_mort.py) ; sorties : `results/ftmo_edge_mort/` (`scenarios.csv`, `priors.csv`, `run.log`). 20 000 comptes par scénario, graine 1840.

## Question

En FTMO 1-Step, on gagne déjà sans edge (effet de contrat : perte plafonnée au prix de l'éval, gain sans plafond). Une edge (mom) augmente fortement l'EV, mais elle peut ne plus marcher en live. Vaut-il mieux trader au hasard ?

## Méthode

- Stratégie : mom NQ de nuit (TP 4 ATR = 2 R, bibliothèque avec MFE), moteur de [run_ftmo_payout_policy.py](../run_ftmo_payout_policy.py) : éval 2,5 % (objectif ramené au reste à faire), financé 1 %, politiques « actuel » et « cible+attente » (plan retenu). Spread 1,5 pt.
- Edge live = h × edge historique. Obtenue par **ré-échantillonnage pondéré des vrais trades** (poids ∝ exp(θ R), θ choisi pour que le R moyen vaille h × moyenne historique) : les gagnants deviennent plus rares, mais chaque trade garde son R, son MFE et son stop réels. 50 000 nuits i.i.d. par scénario (h = 1 compris).
- h = 1 : edge intacte ; **h = 0 : edge morte = hasard** (mêmes trades, mêmes coûts, gain brut moyen nul) ; h < 0 : edge inversée (le marché fait l'inverse du signal, pire que le hasard).
- L'EV est linéaire dans les probabilités des scénarios : EV(croyance) = Σ p(h) × EV(h).

Correction d'un artefact : un simple décalage R − (1 − h) × moyenne (méthode du contrôle sans edge de [run_ftmo_payout_policy_sans_edge.py](../run_ftmo_payout_policy_sans_edge.py)) pousse les pires stops (−1,06 R) sous −1,2 R ; à 2,5 % de risque ils dépassent la perte journalière de 3 % et le passage chute brutalement (2011-2015 : 35 % à h = 0, 9 % à h = −0,1). Le contrôle sans edge du rapport [[reports/ftmo_payout_policy_report]] est donc un peu pessimiste (+133 $ par tentative 10k contre +190 $ ici, l'écart venant aussi de l'ordre i.i.d.).

## Résultats (politique « cible+attente »)

| Période | h | R live / trade | Passage | P(reward) | Vie financé (mois) | EV par tentative 10k ($) | EV par mois, 100k ($) |
|---|---|---|---|---|---|---|---|
| 2016-2026 | −1,00 | −0,100 | 29 % | 46 % | 2,4 | +0 ± 3 | +290 |
| 2016-2026 | −0,50 | −0,050 | 35 % | 56 % | 2,9 | +57 ± 4 | +622 |
| 2016-2026 | −0,25 | −0,025 | 37 % | 61 % | 3,2 | +117 ± 5 | +917 |
| 2016-2026 | **0 (hasard)** | 0 | 41 % | 66 % | 3,5 | **+190 ± 6** | **+1 177** |
| 2016-2026 | +0,25 | +0,025 | 42 % | 70 % | 4,0 | +255 ± 8 | +1 364 |
| 2016-2026 | +0,50 | +0,050 | 46 % | 75 % | 4,5 | +352 ± 10 | +1 554 |
| 2016-2026 | +0,75 | +0,075 | 49 % | 78 % | 5,4 | +556 ± 14 | +1 923 |
| 2016-2026 | **+1 (intacte)** | +0,100 | 53 % | 84 % | 6,3 | **+783 ± 17** | **+2 177** |
| 2011-2015 | −1,00 | −0,189 | 21 % | 31 % | 1,8 | −55 ± 1 | −286 |
| 2011-2015 | −0,50 | −0,094 | 30 % | 48 % | 2,5 | +8 ± 3 | +345 |
| 2011-2015 | 0 (hasard) | 0 | 40 % | 65 % | 3,4 | +157 ± 6 | +1 056 |
| 2011-2015 | +0,50 | +0,094 | 51 % | 82 % | 5,9 | +672 ± 16 | +2 049 |
| 2011-2015 | +1 (intacte) | +0,189 | 60 % | 91 % | 10,4 | +1 963 ± 36 | +2 985 |

(± = demi-largeur d'IC 95 % ; la politique « actuel » donne les mêmes conclusions, voir `scenarios.csv`.)

### Seuils : probabilité d'échec de l'edge au-delà de laquelle le hasard devient meilleur

| Ce que devient l'edge quand elle échoue | 2016-2026, par tentative 10k | 2016-2026, par mois 100k | 2011-2015, par mois 100k |
|---|---|---|---|
| morte (h = 0) | jamais (100 %) | jamais (100 %) | jamais (100 %) |
| à moitié inversée (h = −0,5) | 82 % | 64 % | 73 % |
| totalement inversée (h = −1) | 76 % | 53 % | 59 % |

### Quelques croyances explicites (2016-2026, cible+attente)

| Croyance sur l'edge en live | EV mom / tentative 10k | Hasard | EV mom / mois 100k | Hasard |
|---|---|---|---|---|
| 70 % intacte, 30 % morte | +605 | +190 | +1 877 | +1 177 |
| à moitié (McLean-Pontiff : −50 % après publication) | +352 | +190 | +1 554 | +1 177 |
| 25 % intacte, 50 % morte, 25 % à moitié inversée | +305 | +190 | +1 288 | +1 177 |
| 10 % intacte, 60 % morte, 30 % à moitié inversée | +210 | +190 | +1 111 | +1 177 |
| 50 % morte, 50 % totalement inversée | +95 | +190 | +734 | +1 177 |

## Lecture

1. **Une edge morte, c'est exactement du hasard.** Si l'edge disparaît en live, mom devient un tirage au hasard avec la même structure de trades, donc la même EV que le hasard. Utiliser une edge qui « ne marche plus » ne coûte rien par rapport au hasard : le pire cas réaliste est égal à l'alternative, et le meilleur cas est 4 fois mieux par tentative, 2 fois mieux par mois.
2. **Le hasard ne gagne que si l'edge devient négative en live** (le marché fait systématiquement l'inverse du signal, après coûts identiques), et seulement si ce scénario est très probable : plus de 50 à 80 % selon l'intensité de l'inversion et la mesure. Une edge qui s'inverse durablement est rare : la décroissance typique documentée (McLean-Pontiff) va vers zéro, pas sous zéro.
3. **Les coûts d'exécution ne départagent pas** : un spread ou un glissement plus élevé en live frappe le hasard autant que mom (même nombre de trades, mêmes stops). Ce n'est pas un risque propre à l'edge.
4. **L'inversion se surveille** : si le R live de mom est durablement négatif, on peut basculer au hasard ; cela coupe la branche h < 0 et rend l'edge encore plus dominante. Mais il faut beaucoup de trades pour la détecter (écart-type ≈ 1,3 R par trade, un écart de 0,1 R demande ≈ 700 trades pour t = 2) : pratiquement, la surveillance ne protège que contre une inversion forte.

**Conclusion : garder les edges.** Le choix n'est pas « edge risquée contre hasard sûr » : le hasard est le plancher vers lequel une edge morte retombe. Tant qu'on ne croit pas l'inversion plus probable que la survie, l'edge domine.

## Limites

- Ordre des nuits i.i.d. (pas de régimes ni de séries) ; l'ordre historique donne des niveaux voisins (+707 $ contre +779 $ par tentative pour mom intacte, politique « actuel »).
- Le « hasard » ici garde la structure de mom (nuit, TP 2 R) ; le hasard intraday 9:50 du n° 18 est un autre moteur (≈ +161 $ par tentative 10k), du même ordre.
- Rewards supposés versés (risque de refus non modélisé, voir [[wiki/experiments/propfirm-ftmo-option]]).
- Un seul compte, mom seul ; le plan retenu a deux comptes, la logique est la même pour chacun.
