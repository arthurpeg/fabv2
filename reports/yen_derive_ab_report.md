# Dérive du yen en session US : la concentrer dans le temps (A) ou dans les jours (B)

*2026-11-21. Étape 1 de [PROTOCOLE.md](../PROTOCOLE.md). Fiche : [[wiki/experiments/yen-derive-concentree]]. Exploration sur 6J du 2016-01-04 au 2023-06-30. La réserve par question (2023-07-01 → 2026-08-28) a été coupée avant tout calcul. La grille de 98 variantes a été figée et commitée dans l'en-tête de [run_yen_derive_ab.py](../run_yen_derive_ab.py) (commit 068ce8a) avant le calcul. Compteur global : 1 937 (1 839 + 98). Sorties : `results/yen_derive_ab/`.*

**Critère d'intérêt fixé dans la fiche** : rapport gain / bruit par trade (net moyen / écart type) ≥ 0,15. En dessous, on arrête.

## A. Où se fait la dérive dans la journée ?

Tranches de 30 minutes, brut en bp, tous les jours (1 935 jours) :

| Tranche ET | 08:00-11:00 (6 tranches) | 11:00-12:00 | 12:00-12:30 | 12:30-16:00 (7 tranches) | 16:00-16:30 | 16:30-16:55 |
|---|---|---|---|---|---|---|
| Brut cumulé | −0,38 | +0,06 | +0,31 (t 2,0) | +0,45 | **+0,51 (t 4,3)** | **+0,39 (t 3,7)** |

- **Rien avant 11:00.** Le choix de 11:00 comme entrée était le bon.
- **De 11:00 à 16:55, la dérive est étalée**, avec une part plus forte dans la dernière heure : 16:00 → 16:55 porte environ 0,9 bp des 1,7 bp de la fenêtre, avec un bruit de seulement 6,3 bp. **En brut**, c'est le meilleur rapport gain / bruit de la journée, environ 0,14.
- **Mais le coût est le même pour chaque trade.** Avec environ 1,03 bp de coût standard, une fenêtre courte n'a plus assez de dérive pour le payer : 16:00 → 16:55 fait −0,1 bp net.

**Meilleure des 48 fenêtres** : R4, 15:00 → 16:55, net +0,55 bp, rapport gain / bruit **0,051**.
- C'est moins bien que la référence R4 sur 11:00 → 16:55 (rapport 0,081), avec un t de l'écart de −2,2.
- Aucune fenêtre courte ne bat la fenêtre complète.
- ❌ critère d'intérêt, ❌ B1 (t NW 1,57, DSR 0,13).

## B. Les fortes hausses du yen sont-elles mieux reprises ?

Déciles de la hausse du yen sur les 3 journées précédentes, fenêtre 11:00 → 16:55 :

| Décile | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | **D10** |
|---|---|---|---|---|---|---|---|---|---|---|
| Hausse moyenne sur 3 jours (bp) | −171 | −93 | −62 | −35 | −15 | +5 | +24 | +48 | +82 | +188 |
| Net (bp) | −0,77 | −1,04 | +0,58 | −2,78 | +2,64 | +0,15 | −0,72 | +0,73 | +2,64 | **+5,55** (t 3,0) |
| Gain / bruit | −0,03 | −0,04 | +0,03 | −0,14 | +0,11 | +0,01 | −0,04 | +0,03 | +0,11 | **+0,18** |

- **Les plus fortes hausses du yen sont les mieux reprises.** Le décile du haut fait +5,5 bp net, soit +6,6 bp brut, environ trois fois la dérive moyenne. C'est cohérent avec un retournement proportionnel à la hausse, comme le décrit Piccotti.
- **Mais la relation n'est pas régulière d'un décile à l'autre**, ce qui laisse beaucoup de place au bruit : D4 vaut −2,8 et D5 +2,6.

Seuils ex ante (quantile glissant sur 250 jours, connu la veille) :

| Règle | Jours tradés | Net (bp) | Gain / bruit | t NW |
|---|---|---|---|---|
| Tous les jours | 100 % | +0,67 | 0,029 | 1,38 |
| R4 (hausse > 0) | 47 % | +1,96 | 0,081 | 2,82 |
| Hausse > q 0,5 | 43 % | +1,72 | 0,074 | 2,35 |
| Hausse > q 0,7 | 25 % | +2,31 | 0,093 | 2,29 |
| **Hausse > q 0,8** | 17 % | **+3,61** | **0,134** | 2,57 |
| Hausse > q 0,9 | 8 % | +3,61 | 0,118 | 1,90 |

**Meilleur seuil : q 0,8**, avec un rapport gain / bruit de 0,134, presque le double de R4.
- Les deux moitiés sont positives (+4,99 / +2,24).
- Le t de l'écart entre jours pris et jours sautés vaut 2,21.
- Mais ❌ **sous le critère d'intérêt de 0,15**, et ❌ B1 : DSR 0,40 à N = 140. Le choix parmi 4 seuils, après 42 essais antérieurs sur le yen, efface la significativité.

## Verdict

**❌ L'idée s'arrête ici, selon la règle fixée dans la fiche.**
- La dérive ne se concentre pas dans une heure assez courte pour payer le coût d'un trade, et la fenêtre complète reste la meilleure.
- L'intensité du signal aide : le seuil q 0,8 fait presque le double du rapport de R4, mais il reste sous 0,15 et ne survit pas à la correction pour le nombre d'essais.
- La réserve 2023-07 → 2026-08 n'a pas été ouverte. Elle reste « réservée » pour ces deux questions, et ne pourrait servir qu'à une idée nouvelle pré-enregistrée.

**Observations à garder** (dans la fiche, pas dans les phénomènes : c'est le même effet) :
- la dernière heure 16:00 → 16:55 porte environ la moitié de la dérive brute, avec peu de bruit ;
- les 10 % de plus fortes hausses du yen sur 3 jours sont reprises environ trois fois plus fort que la moyenne.

Pour un exécutant au coût plus bas que le futur, par exemple 0,3 bp, ces deux points redeviendraient intéressants. Ce n'est pas le cas en prop firm sur CFD, où il faut compter environ 0,6 à 0,7 bp.
