# Session domestique et solde commercial : la devise d'un exportateur monte-t-elle pendant ses heures ?

*2026-11-22. Étape 1 (exploration) de [[wiki/experiments/fx-exportateur-importateur]]. Grille figée et commitée dans l'en-tête de [run_fx_balance.py](../run_fx_balance.py) avant tout calcul (commit `5f8afd2`). Données : [fetch_fx_balance.py](../fetch_fx_balance.py) (Dukascopy, barres 1 h bid/ask) ; solde des biens et services en % du PIB de la Banque mondiale (`results/fx_balance/solde_commercial_wb.csv`, données du 2026-11-11). Exploration du 2010-01-01 au 2021-08-31 seulement ; la réserve 2021-09-01 → 2026-08-28 n'a servi qu'aux contrôles de qualité (spreads), sans aucun rendement. Compteur global : 1 940 (1 937 + 3 essais). Sorties : `results/fx_balance/` (`qc.csv`, `sessions_dom.csv`, `tests.csv`, `par_devise.csv`, `summary.txt`).*

## Verdict

**❌ B1.** Le test principal va dans le mauvais sens : les devises des pays exportateurs ne montent pas plus que celles des importateurs pendant leurs heures domestiques. Le seul test positif (même fuseau européen) repose sur une seule devise importatrice et ne passe ni Holm ni le DSR. L'idée s'arrête ; la réserve n'est pas ouverte.

## Contrôle de qualité (critère figé : couverture ≥ 90 % des heures 08-16 locales, aucun trou de semaine > 120 h)

| Devise | Couverture | Trou max (h) | Spread à 08:00 local (bp, exploration) | Gardée |
|---|---|---|---|---|
| NOK | 99,5 % | 26 | 4,0 | ✅ |
| SEK | 99,5 % | 26 | 3,5 | ✅ |
| PLN | 99,5 % | 26 | 6,9 | ✅ |
| MXN | 98,9 % | 27 | 2,5 | ✅ |
| ZAR | 99,5 % | 26 | 6,6 | ✅ |
| SGD | 99,7 % | 26 | 1,9 | ✅ |
| TRY | 99,3 % | 29 | 7,1 | ✅ |
| HUF | 99,0 % | **188** | 7,4 | ❌ |
| CZK, RON, ILS, THB | 57 à 64 % | — | 4 à 16 | ❌ (pas de barres horaires avant 2016-2017) |

## Tests (sessions 08:00-16:00 locales, rendement en dollars par unité de devise, bp)

| Test | Jours | Moyenne | t NW | p unilatéral | p Holm | Moitiés | Années + | Centile des permutations |
|---|---|---|---|---|---|---|---|---|
| **T1** exportateurs − importateurs, tout l'univers | 3 043 | **−0,60** | −0,72 | 0,76 | 0,76 | +0,36 / −1,56 | 5/12 | 0,25 |
| T2 idem, fuseau européen (NOK, SEK, PLN) | 1 216 | +2,71 | 2,09 | 0,018 | 0,054 | +4,39 / +1,02 | 3/5 | 0,96 |
| T3 Fama-MacBeth, pente sur le rang du solde | 3 043 | +0,16 | 0,49 | 0,31 | 0,63 | +0,59 / −0,26 | 7/12 | — |

Barrière B1 ([fab/protocole.py](../fab/protocole.py), `barriere_exploration`, N = 3) :
- **T1** : ❌ (t négatif).
- **T2** : ❌. t 2,09 ✅, moitiés > 0 ✅, sans la meilleure année +1,79 ✅, mais **DSR 0,89** ❌ et pas de référence battue de façon significative ❌.

## Lecture

1. **T2 n'est qu'un seul cas.** Dans le fuseau européen, le seul importateur est la Pologne de 2010 à 2013 (solde 2009-2012 de −0,8 à −2,4 % du PIB), plus la Norvège en 2021 (solde 2020 −0,7 %). Les années PLN : +4,8 / +6,1 / +2,6 / −0,2 bp. L'année NOK 2021 : −0,8 bp, dans le mauvais sens. Avec trois devises, la permutation n'a que trois étiquetages possibles par année : son centile de 0,96 ne veut presque rien dire. T2 dit « le zloty a baissé contre la couronne norvégienne et la couronne suédoise pendant les heures européennes de 2010-2012 », pas « les importateurs baissent ».
2. **Sur tout l'univers, rien ne suit le solde.** Singapour, le plus gros excédent (+26 % du PIB en moyenne), est à 0,0 bp. La Norvège (+8 %) baisse de −1,6 bp, la Turquie (−2 %) de −2,8, le Mexique (−1,3 %) de −0,8.
3. **Ce qui ressort à la place, c'est l'hypothèse de Zhang, pas la nôtre.** Toutes devises confondues, la session domestique est négative : **−1,38 bp, t −2,36** (6 devises sur 7 négatives, PLN −2,7 t −2,6, TRY −2,8 t −2,4). C'est la référence (a) de la grille : rapportée, non comptée, pas un phénomène à part entière. Elle va dans le sens de Breedon-Ranaldo (une devise baisse pendant ses propres heures), sur des devises que le n° 27 n'avait pas vues, en exploration seulement. Elle est notée « À surveiller » dans [[wiki/phenomenes]], avec cette réserve : le n° 27 l'a vue disparaître après 2015 sur les majeures.
4. **Limites** : 7 devises seulement, solde commercial révisé (pas de vintage en temps réel), et le fuseau européen n'a presque jamais d'importateur. Les quatre devises sans données avant 2016 (CZK, RON, ILS, THB) auraient pu élargir l'univers, mais pas avec le critère de qualité figé.

## Ce qui change dans le wiki

- [[wiki/experiments/fx-exportateur-importateur]] : `abandoned`, ❌ B1.
- [[wiki/Failed Ideas/ledger]] : nouvelle ligne.
- [[wiki/phenomenes]] : « À surveiller » : session domestique négative sur NOK, SEK, PLN, MXN, ZAR, SGD, TRY, 2010-2021 (−1,4 bp, t −2,4), référence de la grille, non comptée.
- [[wiki/reserves]] : la réserve 2021-09 → 2026-08 de ces devises reste réservée, non ouverte ; l'exploration 2010-01 → 2021-08 devient « explorée ».
