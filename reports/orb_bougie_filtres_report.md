# NQ, règle de la 1ʳᵉ bougie (stop 0,5 ATR, objectif 2R) : filtres F1, F2, F3

*2026-11-22. Suite de l'étape 1 de [[wiki/experiments/nq-orb-bougie-sorties]] (précédents : [[reports/nq_orb_bougie_report]], [[reports/orb_bougie_indices_report]]). Grille figée et commitée dans l'en-tête de [run_orb_bougie_filtres.py](../run_orb_bougie_filtres.py) avant tout calcul (commit `b97b69c`). NQ Databento 1 min, 2010-06 → 2021-09-30 ; la réserve 2021-10-01 → 2026-08-28 n'a pas été lue. Compteur global : 2 024 (2 021 + 3 essais). Sorties : `results/orb_bougie_filtres/` (`filtres.csv`, `trades.csv`, `summary.txt`).*

## Règle de base et filtres

Base : sens de la bougie 9:30-9:35 ET, entrée à 9:35, stop 0,5 × ATR14, objectif 2R, sinon sortie à 16:00, 1 contrat, coût 0,50 pt. Ici 2 665 trades (les 20 premières séances manquent, faute de médiane de volume) : **+2,22 pts/trade, Sharpe 0,68**.

- **F1** : on saute les jours d'annonce à 10:00 ou 14:00 (ISM, JOLTS, FOMC), d'après `config/calendrier_macro_us.csv`.
- **F2** : on ne trade que si le volume 9:30-9:34 dépasse 1,5 × sa médiane des 20 séances précédentes.
- **F3** : on ne trade que si le corps de la 1ʳᵉ bougie dépasse 0,05 × ATR14.

Référence d'un filtre = les jours qu'il fait sauter (t de Welch de l'écart). Famille : 85 essais (81 variantes de sortie sur ES, YM, NQ + R4 + 3 filtres).

## Résultats (points nets par trade)

| Filtre | Jours pris | Net pris | Net sautés | t écart | t NW (pris) | Sharpe | DSR (N 85) | 2010-15 | 2016-21 | 2020 | Années + |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 pas d'annonce 10:00 / 14:00 | 2 138 | +2,75 | +0,06 | 1,10 | 2,40 | 0,84 | 0,013 | +1,40 | +3,97 | −2,54 | 10/12 |
| F2 volume > 1,5 × médiane | 293 | **−3,49** | +2,92 | **−2,55** | −1,49 | −1,42 | 0,001 | −1,32 | −6,63 | −27,5 | 6/12 |
| **F3 corps > 0,05 ATR** (choisi) | 1 981 | **+2,91** | +0,23 | 1,23 | 2,32 | 0,87 | **0,019** | +0,92 | +4,68 | +0,61 | **11/12** |

**Filtre choisi (meilleur Sharpe) : F3.** n 1 981 · net +2,91 pts (médiane −2,5) · écart-type 52,9 · Sharpe 0,87 · t NW 2,32 · 48 % de gagnants · pire creux −1 743 pts · moitiés +0,59 / +5,22 · sans la meilleure année +1,97 · avec 1 tick de plus +2,66 · jours sautés +0,23 (écart +2,67, t 1,23) · **DSR 0,019**.

**B1 : ❌ ratée.** Seul le DSR échoue, mais de très loin (0,019 pour 0,95).

## Lecture

1. **Aucun filtre ne double le Sharpe.** F1 et F3 le portent de 0,68 à environ 0,85, ce qui ne suffit pas avec 85 essais. Dans les deux cas, l'écart entre jours pris et jours sautés n'est qu'à t 1,1 à 1,2.
2. **F1 (annonces) tient à une seule année.** En 2021, les jours sans annonce font +16,5 pts/trade et les jours d'annonce −20,9. En 2010, 2016 et 2020, c'est l'inverse : les jours d'annonce sont nettement meilleurs (+4,4, +5,2 et +11,7). Il n'y a pas de régularité.
3. **F3 (bougie franche) est le plus régulier** : 11 années positives sur 12, et en 2010-2015 les jours pris font +0,92 contre une base de +0,96. Mais l'écart avec les jours sautés change de signe d'une année sur l'autre (sautés meilleurs en 2010, 2011, 2013 et 2016).
4. **F2 (volume) donne l'inverse de l'hypothèse « stocks in play ».** Les 293 jours à fort volume d'ouverture **perdent** (−3,49 pts/trade, écart t −2,55), surtout en 2020 et 2021. Une bougie d'ouverture très chargée est donc plutôt suivie d'un retour que d'une continuation. C'est cohérent avec le filtre de volume M3c déjà raté sur la cassure (2026-10-12) et peut-être avec le fade de gap post-0DTE (les gros volumes d'ouverture vont souvent avec les gros gaps). Ce n'est **pas** un résultat : c'est 1 essai sur 85, dans le sens contraire de celui qui était prévu. Il n'est pas versé aux phénomènes.

## Conclusion

B1 ❌ pour les trois filtres. La règle de la 1ʳᵉ bougie sur NQ reste un effet de 2016-2021, d'un Sharpe autour de 0,7 à 0,9, qu'aucune sortie ni aucun de ces filtres ne rend démontrable. Ligne ajoutée au registre. La réserve 2021-10 → 2026-08 n'est pas ouverte.
