# Short du yen en session US : filtre de volatilité ou de retournement

*2026-11-21. Exploratoire (étape 1 de [PROTOCOLE.md](../PROTOCOLE.md)), sur données **déjà vues** : 6J du 2017-01-30 au 2026-08-28, soit 2 425 jours, échantillon commun après les fenêtres glissantes de 250 jours. Rien après le 2026-08-28, qui est le holdout du [[PREREGISTRATION_28]]. La grille de 8 essais a été figée et commitée dans l'en-tête de [run_jpy_us_filtres.py](../run_jpy_us_filtres.py) avant le calcul. Compteur global : 1 814 (1 806 + 8). Sorties : `results/jpy_us_filtres/` (`grid.csv`, `summary.txt`).*

## Question

On garde le trade du n° 28 : short 6J de 11:00 à 16:55 ET, coût standard. On ne le prend que certains jours, choisis avec une information connue avant 11:00.

Deux familles de filtres :
- **Volatilité (V)** : trader seulement les jours agités.
- **Retournement (R)** : shorter seulement si le yen a **monté** récemment.

La référence est la même position prise tous les jours. On compare aussi les jours pris aux jours sautés.

## Résultats

Référence sur le même échantillon : net +0,90 bp, Sharpe 0,64, +19 700 $ pour 1 contrat.

| Filtre | Jours pris | Net pris (bp) | Net sautés (bp) | t pris − sautés | t NW pris | Sharpe quotidien* | P&L | Moitiés | Années + | DSR N = 8 / 42 | B1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| V1 vol 20 > médiane | 42 % | +1,31 | +0,60 | 0,75 | 1,73 | 0,52 | +13 000 $ | +1,07 / +1,56 | 8/10 | 0,82 / 0,72 | ❌ |
| V2 vol 20 > tercile haut | 30 % | +1,85 | +0,50 | 1,19 | 1,92 | 0,58 | +12 900 $ | +1,65 / +2,05 | 7/10 | 0,89 / 0,82 | ❌ |
| V3 ATR H1 > médiane | 43 % | +1,58 | +0,39 | 1,25 | 2,10 | 0,62 | +16 500 $ | +1,05 / +2,11 | 6/10 | 0,90 / 0,82 | ❌ |
| V4 ATR H1 > tercile haut | 29 % | +2,20 | +0,36 | 1,59 | 2,27 | 0,67 | +15 500 $ | +1,48 / +2,93 | 7/10 | 0,94 / 0,89 | ❌ |
| R1 fenêtre US de la veille : yen ↑ | 43 % | +1,98 | +0,09 | 2,07 | 3,03 | 0,91 | +18 500 $ | +0,50 / +3,46 | 7/10 | 0,98 / 0,96 | ✅ |
| R2 3 fenêtres US précédentes : yen ↑ | 40 % | +1,67 | +0,38 | 1,42 | 2,70 | 0,78 | +14 800 $ | +0,41 / +2,93 | 8/10 | 0,96 / 0,92 | ✅ |
| R3 journée de la veille : yen ↑ | 46 % | +1,97 | +0,00 | 2,16 | 2,88 | 0,90 | +20 400 $ | +0,83 / +3,11 | 8/10 | 0,98 / 0,96 | ✅ |
| **R4 3 journées précédentes : yen ↑** | 46 % | **+2,09** | **−0,11** | **2,43** | **3,50** | **1,00** | **+22 800 $** | +1,80 / +2,38 | 9/10 | 0,99 / 0,98 | ✅ |

\* Le Sharpe quotidien compte 0 les jours sans position. Il se compare directement au Sharpe de 0,64 de la règle tous les jours.

Pour R3 et R4, une « journée » va de 16:55 à 16:55 ET. R4 somme les rendements du 6J de J−4 à J−1. Un yen en hausse veut dire que le short aurait perdu.

## Lecture

1. **Le filtre de volatilité ne sert à rien.** Les jours agités rapportent plus en bp : jusqu'à +2,2 bp pour V4. Ce n'est pas un meilleur signal, c'est la même dérive à une plus grande échelle, avec un bruit plus grand aussi. Le Sharpe quotidien ne monte pas (0,52 à 0,67 contre 0,64), l'écart avec les jours sautés n'est pas significatif (t ≤ 1,6), et le DSR reste sous 0,95. On l'abandonne.
2. **Le retournement concentre l'effet. Les 4 variantes vont dans le même sens et passent B1.**
   - Le jour où le yen a monté la veille ou sur les 3 derniers jours, le short fait environ +2 bp net, soit **un brut environ 1,5 fois celui de la règle** (+3,1 contre +2,0).
   - Les autres jours, le short ne gagne plus rien net (−0,1 à +0,4 bp).
   - On trade moins de la moitié des jours pour le même P&L total, et le Sharpe quotidien passe de 0,64 à 0,90-1,00.
3. **R4 est la plus robuste.** Elle a le t le plus haut (3,50), l'écart le plus net avec les jours sautés (t 2,43), des moitiés équilibrées (+1,80 / +2,38) et 9 années sur 10 positives. Les variantes R1 et R2, construites sur la fenêtre US seulement, sont faibles sur 2017-2021 (+0,4 à +0,5 bp).
4. **Ce n'est pas une surprise totale.**
   - L'étude de distribution montrait déjà une autocorrélation de −0,07 au premier retard entre fenêtres.
   - Piccotti (SSRN 2446584) décrit un retournement des rendements 24 h du dollar-yen pendant la séance de New York. Cette idée avait été arrêtée à l'étape 0, parce qu'on doutait que le retournement se concentre dans une fenêtre intraday. Cette mesure montre qu'il s'y concentre : c'est la condition de réouverture inscrite au registre.
   - Une lecture plausible : quand le yen a monté (risk-off, rapatriement), la session US défait une partie de ce mouvement.
5. **Ce qui manque pour y croire.**
   - Tout est mesuré sur des données déjà vues, et le DSR à N = 42 tient compte des coupes regardées le 2026-11-19.
   - Le critère de choix entre R1 et R4 n'était pas écrit dans la grille. R4 est retenue parce qu'elle est la meilleure sur toutes les mesures, ce qui la flatte un peu.
   - Il n'y a plus de réserve sur le yen. La seule confirmation possible est l'étape 4, sur les données postérieures au 2026-08-28, que le n° 28 a déjà réservées.
   - Un pré-enregistrement n° 29 ajouterait R4 à ces lectures, avec Holm sur les hypothèses des deux pré-enregistrements. Puissance approximative : +2 bp pour environ 24 bp d'écart type et environ 115 trades par an donnent un t attendu d'environ 1,1 à la lecture de 2028, et d'environ 2 en 2031.

## Verdict

- **Filtre de volatilité : ❌ B1**, au registre des échecs.
- **Filtre de retournement R4 : ✅ B1.** Il est candidat à l'étape 4 par un pré-enregistrement n° 29, pas encore écrit. Il est noté « À surveiller » dans [[wiki/phenomenes]].
- La règle du n° 28 ne change pas.
