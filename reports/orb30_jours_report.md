# ORB 30 minutes de Subhani, par jour de la semaine, sur NQ, ES, YM

*2026-11-22. Étape 1 (exploration) de [[wiki/experiments/orb30-jours-semaine]]. Grille figée et commitée dans l'en-tête de [run_orb30_jours.py](../run_orb30_jours.py) avant tout calcul (commit `f40b125`). Données Databento 1 min, **2016-01-01 → 2026-08-28** ; la réserve 2010-06-08 → 2015-12-31 n'a pas été lue. Compteur global : 2 043 (2 025 + 18 essais). Sorties : `results/orb30_jours/` (`grille.csv`, `trades_<actif>.csv`, `summary.txt`).*

## Règle (Subhani 2026, transposée aux futures)

Range = plus haut et plus bas 9:30-9:59 ET, 1 R = sa largeur W. Entrée par ordre stop sur la borne, à la première barre qui la dépasse à partir de 10:00 (achat ou vente). Stop fixe à une largeur de range de l'entrée. Pas d'objectif, sortie à 16:00. 1 contrat, coût standard 1 tick + 5 $ (médiane : 0,007 R sur NQ, 0,027 R sur ES, 0,016 R sur YM). W médian : NQ 70 pts, ES 13 pts, YM 125 pts. Environ 39 à 46 % des trades sortent au stop.

## Résultats (R net par trade)

| Actif | Lundi | Mardi | Mercredi | Jeudi | **Vendredi** | Tous |
|---|---|---|---|---|---|---|
| **NQ** | −0,03 (t −0,7) | +0,10 (1,8) | +0,00 (0,1) | −0,00 (−0,1) | **+0,19 (t 3,50)** | +0,05 (2,4) |
| ES | −0,01 (−0,2) | +0,09 (1,6) | −0,05 (−0,9) | +0,03 (0,4) | +0,11 (t 2,02) | +0,03 (1,3) |
| YM | −0,02 (−0,4) | +0,08 (1,5) | −0,04 (−0,6) | +0,03 (0,5) | +0,05 (0,8) | +0,02 (0,8) |

Tableau complet (Sharpe, gagnants, points, dollars, sous-périodes, DSR) : `results/orb30_jours/grille.csv`.

- **NQ vendredi** : +0,190 R (+12,2 pts, +244 $ par trade, 1 contrat), 527 trades, 50,7 % de gagnants, **10 années positives sur 11**, 2016-2022 +0,156, 2023-2026 +0,254. Il bat les autres jours de la semaine (+0,019 R ; écart t 2,75).
- **ES vendredi** : +0,113 R (t 2,02), 8 années sur 11. **YM vendredi** : rien de significatif.
- **Le vendredi est le meilleur jour sur NQ et ES**, comme dans le papier ; le mardi est deuxième sur NQ et ES et premier sur YM (+0,08 à +0,10 R, t 1,5 à 1,8). Lundi et mercredi sont nuls ou négatifs sur les trois indices.
- « Tous les jours » sur NQ : +0,053 R, t 2,43, mais sans direction il fait −0,003 R (écart t 1,63). C'est l'équivalent de M3a, déjà vu.

## Réplication du papier (période 2018-05-01 → 2026-06-12)

| | Nous (futures) | Subhani (ETF) |
|---|---|---|
| NQ / QQQ, vendredi | **+0,219 R, t 3,34** | +0,199 R, t 3,05 |
| ES / SPY, vendredi | +0,137 R, t 2,06 | t 1,88 |

**La réplication est réussie** : même signe, même ordre de grandeur, même hiérarchie NQ > ES, sur d'autres instruments (futures et non ETF) et avec nos propres données et coûts.

## Fiche de la règle choisie (meilleur Sharpe : NQ, vendredi)

n 527 · brut +0,201 R · net **+0,190 R** (médiane +0,026) · écart-type 1,29 R · Sharpe 0,147 par trade, soit ≈ 1,04 par an pour ≈ 50 trades par an (la colonne `sharpe_an` de grille.csv annualise par √252 et le surestime d’environ 2,2 fois ; corrigé le 2026-11-22) · **t NW 3,50**, p 0,0002 · 50,7 % de gagnants · pire creux −9,5 R · 10/11 années positives · moitiés +0,099 / +0,280 · sans la meilleure année +0,162 · avec 1 tick de plus +0,184 · autres jours +0,019 (écart t 2,75) · **DSR (N = 45) 0,846**.

**B1 : ❌ ratée sur le seul DSR** (0,846 pour 0,95). Les cinq autres critères passent nettement.

## Lecture

1. C'est le **résultat le plus solide de toute cette série ORB** : la règle a été publiée par un autre auteur, avec le vendredi comme hypothèse fixée avant nous, et elle se retrouve sur un autre instrument (NQ au lieu de QQQ) avec presque les mêmes chiffres.
2. Le DSR est calculé, comme prévu dans la grille, en traitant « NQ vendredi » comme choisi parmi 45 essais (nos 18 + les 27 ORB de M3). Or le vendredi n'a pas été choisi par nous : c'était l'hypothèse du papier. Ce raisonnement ne change pas le critère, qui était fixé d'avance, mais il explique pourquoi la règle reste intéressante.
3. Réserves : aucun mécanisme connu ; un effet de jour de la semaine est le cas d'école de la recherche de données ; 50 trades par an seulement ; la moitié récente porte une plus grande part du gain (+0,28 contre +0,10 R).
4. La réserve 2010-2015 (≈ 280 vendredis) aurait une **puissance d'environ 80 %** à l'effet observé, bien plus que les tests précédents.

## Suite

Selon le protocole, B1 ratée interdit d'ouvrir la réserve sans écart assumé. Ligne « À surveiller » ajoutée à [[wiki/phenomenes]] (NQ vendredi, significatif, réplique un papier, non confirmé hors échantillon) et ligne au registre des échecs. La réserve 2010-06 → 2015-12 reste réservée, non lue.
