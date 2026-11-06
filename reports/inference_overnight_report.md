# Inférence des chiffres overnight : t HAC, dépendance, N effectif, DSR (exploratoire)

*2026-11-06. Exploratoire, aucune règle nouvelle : compteur global inchangé (1 742). Méthodes fixées dans l'en-tête de [run_inference_overnight.py](../run_inference_overnight.py) avant le calcul, sauf le contrôle « V0 » du DSR, ajouté après le premier calcul (signalé). Sorties : `results/inference_overnight/` (`inference.csv`, `n_effectif.csv`, `dsr.csv`, `run.log`). Données ≤ 2026-08-28 : rien du holdout.*

Origine : une relecture du document overnight demandait de préciser l'inférence (HAC / Newey-West), de tester la dépendance et l'hétéroscédasticité, et d'estimer le nombre effectif d'essais parmi les 1 742.

## 1. t iid, t HAC et bootstrap par blocs

| Série | n | Moyenne | t iid | t NW (5) | t NW (auto, 8) | p NW auto | p bloc 10 | ρ1 |
|---|---|---|---|---|---|---|---|---|
| NQ close-to-open 2016-2026 | 2 671 | +4,82 bp/j | 3,12 | 3,37 | **3,51** | 0,0004 | 0,0005 | −0,03 |
| NQ Asie | 2 671 | +4,35 | 3,66 | 4,21 | 4,27 | 0,00002 | < 0,0005 | −0,13 |
| NQ US | 2 671 | +3,02 | 1,42 | 1,58 | 1,60 | 0,11 | 0,11 | −0,10 |
| ES close-to-open | 2 670 | +3,45 | 2,80 | 2,93 | 2,99 | 0,003 | 0,002 | −0,03 |
| ES Asie | 2 670 | +1,99 | 2,13 | 2,38 | 2,39 | 0,017 | 0,016 | −0,13 |
| ES US | 2 670 | +2,11 | 1,31 | 1,48 | 1,51 | 0,13 | 0,13 | −0,09 |
| YM close-to-open | 2 666 | +3,28 | 2,74 | 2,82 | 2,88 | 0,004 | 0,0045 | −0,02 |
| YM Asie | 2 666 | +1,99 | 2,27 | 2,52 | 2,51 | 0,012 | 0,011 | −0,13 |
| YM US | 2 666 | +1,92 | 1,26 | 1,46 | 1,51 | 0,13 | 0,12 | −0,10 |
| mom NQ 2016-2026 (rendement) | 2 420 nuits | +3,18 bp/nuit | 2,92 | 3,08 | 3,16 | 0,0016 | 0,0035 | −0,02 |
| mom NQ OOS 2011-2015 (R) | 1 115 trades | +0,116 R | 2,79 | 2,87 | 2,87 | 0,004 | 0,0045 | −0,04 |

p bilatéraux ; le p unilatéral pré-enregistré du n° 11 (0,0015, bootstrap par blocs) est celui qui fait foi pour mom OOS.

**Lecture** : le t HAC est **plus grand** que le t iid partout. L'autocorrélation d'ordre 1 est négative (−0,13 en Asie, −0,10 en séance US), ce qui réduit la variance de long terme de la moyenne. Le t iid du rapport des sessions était donc prudent, pas optimiste. Le bootstrap par blocs (convention du dépôt) donne les mêmes p que Newey-West. Aucune conclusion ne change : close-to-open significatif sur les trois indices, séance US non significative.

## 2. Dépendance et hétéroscédasticité

| Série | Ljung-Box r (5 / 10) p | Ljung-Box r² (5) p | ARCH-LM (5) | Kurtosis en excès |
|---|---|---|---|---|
| NQ close-to-open | 0,04 / 3e-6 | 6e-71 | 211 (p 1e-43) | 5,3 |
| NQ Asie | 3e-9 / 1e-11 | 4e-77 | 235 | 10,6 |
| ES close-to-open | 0,18 / 8e-4 | 2e-133 | 350 | 6,8 |
| YM close-to-open | 0,10 / 0,01 | 9e-127 | 330 | 8,9 |
| mom NQ 2016-2026 (rendement) | 0,03 / 3e-5 | ≈ 0 | 1 035 | 9,5 |
| **mom NQ OOS 2011-2015 (R)** | 0,10 / 0,04 | **0,40** | **4,6 (p 0,47)** | −1,2 |

- **Hétéroscédasticité massive** sur tous les rendements en points de base (ARCH p < 1e-28 partout) et queues épaisses (kurtosis 5 à 15). Un t iid serait faux s'il n'y avait pas d'autocorrélation négative pour compenser ; d'où l'intérêt du HAC ou du bootstrap par blocs.
- **Dépendance sérielle faible mais réelle** en Asie et en séance US (ρ1 ≈ −0,1, Ljung-Box p < 1e-5) ; quasi nulle sur le close-to-open entier.
- **Exprimé en R (stop en ATR M15), mom n'a plus d'effet ARCH** (p 0,47) ni de queue épaisse : le dimensionnement en ATR normalise déjà le risque. C'est la même conclusion que le rejet du dimensionnement par la volatilité au n° 15.

## 3. Nombre effectif d'essais

560 séries journalières nettes d'essais sont sauvegardées (93 du lot initial, 42 réplications, 425 de la récolte ATR) ; les ~1 180 autres essais (dont la plupart des 927 IC de la récolte 1) n'ont que des statistiques résumées.

| Mesure | Valeur |
|---|---|
| Séries sauvegardées M | 560 |
| Meff Li & Ji (méthode principale) | **196** (ratio 0,35) |
| Meff Nyholt (contrôle) | 535 |
| Valeurs propres pour 95 % de la variance | 172 |
| Plus grande valeur propre | 76 |
| \|corrélation\| médiane entre essais | 0,027 |
| Part des paires avec \|ρ\| > 0,5 | 6 % |
| **N effectif global extrapolé** (0,35 × 1 742) | **≈ 610** |

La redondance est concentrée : la plupart des paires d'essais sont presque indépendantes (actifs et heures différents), mais quelques grappes très corrélées (une valeur propre de 76 : la prime de nuit, testée à toutes les heures et toutes les variantes de stop) comptent pour beaucoup d'essais. Nyholt est connu pour surestimer Meff quand les corrélations sont faibles en moyenne ; Li & Ji est retenu. L'extrapolation à 1 742 suppose que les essais non sauvegardés sont aussi redondants : c'est probablement prudent pour la récolte 1, où 51 des 56 IC positifs étaient la même prime.

## 4. DSR avec N brut et N effectif

| Série | Sharpe annuel | N | SR0 annuel (V observée) | DSR | SR0 annuel (V0 = 1/T, ajouté après coup) | DSR V0 |
|---|---|---|---|---|---|---|
| mom NQ 2016-2026 | 0,88 | 1 742 | 1,78 | 0,001 | 1,03 | 0,30 |
| mom NQ 2016-2026 | 0,88 | ≈ 610 | 1,63 | 0,005 | 0,94 | 0,42 |
| NQ close-to-open | 0,96 | 1 742 | 1,78 | 0,004 | 1,03 | 0,41 |
| NQ close-to-open | 0,96 | ≈ 610 | 1,63 | 0,016 | 0,94 | 0,53 |

- Passer de 1 742 à ≈ 610 essais effectifs **ne change pas le verdict** : le DSR reste très loin de 0,95. N entre dans SR0 par sa racine logarithmique ; diviser N par 3 abaisse le seuil d'environ 9 % seulement.
- Ce qui pèse est V, la dispersion des Sharpe entre essais. La V observée (0,0011 par jour) inclut les vraies différences entre essais (coûts FX, règles perdantes), donc elle gonfle SR0. Même avec V0 = 1/T (pure dispersion d'échantillonnage, le cas le plus favorable), le DSR plafonne à 0,42-0,53.
- **Conséquence** : aucune règle overnight, ni même la prime de nuit brute, ne passe le DSR contre le compteur global, qu'il soit brut ou effectif. Sur 2016-2026 seules, avec un Sharpe de 0,9 à 1, c'est attendu. La preuve de mom repose sur un autre argument : le test hors échantillon pré-enregistré du n° 11 (2011-2015, une seule hypothèse, p 0,0015), où le N pertinent est 1, et sur le holdout du n° 26.

## Ce qui n'est pas fait

- Romano-Wolf (stepM) ou SPA de Hansen sur une famille complète : demanderait les séries des 927 IC de la récolte 1, non sauvegardées.
- N effectif sur les 1 742 essais réels : idem.
