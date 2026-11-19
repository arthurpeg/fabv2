# Short du yen en session US : effet constant ou porté par quelques séances ?

*2026-11-19. Descriptif, sur données **déjà vues** : 6J 2016-01 → 2026-08-28 (2 694 séances) et spot USDJPY 2012-2015 (1 030 séances). Rien après le 2026-08-28, qui est le holdout du [[PREREGISTRATION_28]]. Les 34 coupes ont été figées dans l'en-tête de [run_jpy_us_distribution.py](../run_jpy_us_distribution.py) et commitées avant le calcul. Aucune règle n'est choisie, donc le compteur ne bouge pas. Compteur global : 1 798. Si une de ces coupes sert un jour de filtre, son n_famille vaudra au moins 34. Sorties : `results/jpy_us_distribution/` (`summary.txt`, `groupes.csv`, `figure.png`).*

La variable est le rendement **brut** du short 6J de 11:00 à 16:55 ET, en bp. Un rendement positif veut dire que le yen baisse.

## Réponse courte

**L'effet est constant : c'est un décalage de toute la distribution, pas quelques grosses séances.**

## 1. Forme de la distribution (6J 2016-2026)

| Mesure | Valeur |
|---|---|
| Moyenne | +2,03 bp (t NW 4,9) |
| Médiane | **+2,19 bp** |
| Moyennes tronquées symétriques (1 / 5 / 10 / 25 %) | +2,07 / +2,05 / +2,10 / +2,11 |
| Écart type, asymétrie, kurtosis | 23,6 bp ; −0,09 ; 14,5 |
| Séances positives | 54,6 % |
| Sans les 1 % / 5 % de séances les plus extrêmes | +2,01 (t 5,5) / +1,71 (t 5,4) |

- **La médiane et les moyennes tronquées valent la moyenne.** Si l'effet venait de quelques grosses séances, couper les queues le ferait disparaître. Ici, il reste entier.
- **Le profil de décalage est plat.** Le profil (q(p) + q(1−p)) / 2 vaut +1,7 à +2,2 bp de p = 0,05 à p = 0,45. Les séances calmes comme les séances agitées sont décalées du même montant (graphique en haut à gauche).
- **La référence est différente.** Le même short de 16:55 au lendemain 11:00 a une médiane de +1,6 mais une moyenne de −0,9. Ses queues sont asymétriques : les grosses hausses du yen ont lieu hors de la fenêtre US.
- **Les 10 meilleures et les 10 pires séances s'annulent** : +1 342 contre −1 343 bp. Le total de +5 463 bp vient donc du reste.
- Les quintiles de |r| les plus agités portent 80 % du total, mais c'est mécanique : le même décalage pèse plus en bp sur les grosses séances. La part de séances positives est la même partout, 55 à 60 %.

## 2. Dans le temps

- **Toutes les années sont positives**, de +0,47 (2021) à +4,42 (2025). 36 trimestres sur 43 le sont aussi.
- **Les moyennes trimestrielles sont même moins dispersées que le hasard.**
  - Test χ² contre une moyenne constante : 23,7 pour 42 degrés de liberté, p = 0,99.
  - Ratio de variance : 0,69 sur 21 séances, 0,66 sur 63.
  - Cela vient d'une légère autocorrélation négative (−0,07 au premier retard) : une grosse baisse du yen est souvent en partie reprise le lendemain.
- Sans les 4 meilleurs trimestres, la moyenne reste à +1,62 bp.
- Il y a une intensité plus forte en 2022-2026 (+3,1 en moyenne contre +1,2 en 2016-2021), déjà vue au n° 28. Ce n'est pas une rupture, l'effet est présent sur toute la période.

## 3. Calendrier et conditions

Ces résultats sont descriptifs. Une partie des conditions est **contemporaine**, donc inutilisable comme filtre.

| Coupe | Groupe | n | Moyenne (bp) | t NW | Welch p |
|---|---|---|---|---|---|
| Annonces | aucune annonce | 1 621 | +2,62 | 5,2 | 0,059 |
| | annonce avant 11:00 | 897 | +1,03 | 1,5 | |
| | décision FOMC 14:00 | 90 | −4,43 | −1,1 | |
| | minutes FOMC 14:00 | 86 | +8,03 | 2,4 | |
| Fin de mois (fixing 11:00 ET) | dernier jour ouvré | 128 | +1,71 | 0,7 | 0,89 |
| Jour de semaine | lundi → vendredi | ≈ 540 | +2,35 / +2,69 / +2,88 / +1,95 / +0,21 | | 0,39 |
| Volatilité ex ante (Q1 → Q5) | | 535 | +1,10 / +2,40 / +1,08 / +2,46 / +3,21 | | 0,45 |
| Volatilité réalisée dans la fenêtre (Q1 → Q5) | *contemporaine* | 539 | +1,53 / +3,06 / +3,67 / +3,08 / **−1,20** | | **0,004** |
| ES dans la même fenêtre | *contemporaine* : baisse / neutre / hausse | 886 | **+0,01** / +2,55 / +3,45 | | 0,011 |
| Yen de 00:00 à 11:00 ET | monte / neutre / baisse | 898 | +2,65 / +2,06 / +1,38 | | 0,56 |

1. **Aucune coupe connue avant 11:00 ne concentre l'effet.** La volatilité ex ante, le jour de semaine, la fin de mois et le mouvement de la matinée ne donnent rien de significatif. Le vendredi est faible (+0,21), mais p = 0,39 sur 5 jours.
2. **L'effet disparaît les jours de stress.** C'est le seul contraste net :
   - quand ES baisse dans la fenêtre, le yen ne baisse pas (+0,01) ;
   - le quintile de volatilité réalisée le plus agité est négatif (−1,20).
   - C'est cohérent avec le rôle de valeur refuge du yen : le risk-off efface la dérive ce jour-là. Mais on ne le sait qu'après la séance.
   - Avec 7 tests F, seule la volatilité réalisée passe Holm (p ajusté 0,03).
3. **Les jours de décision FOMC vont dans l'autre sens** (−4,4 bp, t −1,1, 90 jours). Ce n'est pas significatif, mais c'est le seul groupe calendaire négatif, contre +8,0 les jours de minutes (t 2,4). Avec 34 coupes, ni l'un ni l'autre ne compte.
4. **Les jours sans annonce portent 78 % du total** pour 60 % des séances (+2,6 contre +1,0 les jours d'annonce matinale, p = 0,06). C'est à surveiller, rien de plus.

## 4. Spot 2012-2015 (avant nos futures)

C'est la même forme : moyenne +1,55, médiane +1,70, moyennes tronquées +1,7 à +2,1, profil plat de +2 bp au centre. Les 10 meilleures et les 10 pires séances s'annulent (+1 017 contre −1 118 bp).

## Conclusion

- Le phénomène n'est **pas** un effet de quelques séances, de quelques trimestres, ni d'un calendrier d'annonces. C'est une dérive lente et régulière d'environ 2 bp par séance, avec une probabilité de séance positive à peine supérieure à 50 % (55 %), présente chaque année.
- Cela confirme la lecture du rapport SL/TP : il n'y a pas de queue à capturer, et un stop ou un objectif ne peut que couper la dérive.
- Pour le n° 28 : aucun filtre n'est ajouté, la règle est figée. La seule zone sans effet est le risk-off du jour, qui n'est pas connu à 11:00.
