# Pré-enregistrement n° 22 : lecture de niveaux sur NQ (cassure du range de la veille avec cible « measured move » ; règle des 80 % du profil de volume)

*2026-11-02, avant tout calcul de ces deux règles. Origine : captures TradingView « αλλο research » transmises en séance (NQ et QQQ, 26-30 octobre 2026, indicateur « AVP Zones », zones HVN / LVN, rectangles de range et flèches de projection ; total affiché « 2 438 points pour la semaine, 487 par jour »). Lecture faite en séance : chaque flèche mesure la hauteur du rectangle voisin, tracée après coup ; aucune entrée, sortie ni stop n'est montrée. Ce document traduit les deux idées sous-jacentes en règles exécutables, figées à l'avance.*

## Hypothèses

- **R1, measured move** : quand NQ casse pendant la séance US le plus haut (plus bas) de la séance US de la veille, le prix va plus souvent atteindre une extension égale à la hauteur du range de la veille que revenir au milieu de ce range. Sous une marche au hasard sans dérive, la probabilité d'atteindre la cible avant le stop vaut d_stop / (d_stop + d_cible) et le R net moyen est négatif (coûts) : c'est le contrôle pile ou face du registre.
- **R2, règle des 80 % (Market Profile, Steidlmayer / Dalton)** : si la séance s'ouvre hors de la zone de valeur (70 % du volume) de la séance de la veille, puis y est acceptée pendant deux périodes de 30 minutes consécutives, le prix traverse la zone de valeur jusqu'au bord opposé dans « 80 % » des cas. C'est la règle la plus précise et la plus répandue parmi celles qui se servent d'un profil de volume (HVN / LVN, POC, zone de valeur).

## Déjà vu, et pourquoi c'est différent

- Le registre contient l'opening range breakout (ORB 5 et 30 min, Zarattini), qui a échoué. R1 casse **le range de la séance précédente entière**, pas celui de l'ouverture, et sort sur une cible fixée par la hauteur de ce range : cette règle n'a jamais été calculée dans le dépôt.
- Le momentum intraday (Gao) et la bande de bruit M2 sont des règles de tendance d'une autre construction (rendement de la première demi-heure, bande de volatilité autour de l'ouverture).
- Aucun profil de volume, zone de valeur ou POC n'a jamais été calculé dans le dépôt (vérifié par recherche dans le code et le wiki le 2026-11-02).
- Contrôle pile ou face ([run_coinflip.py](run_coinflip.py)) : sans avantage, taux de réussite ≈ 1 / (1 + RR) et R net < 0. C'est la référence des deux règles.

## Données et conventions communes

| Élément | Valeur |
|---|---|
| Marchés | **NQ** (décision), ES et YM (rapportés, voir critères) ; `.v.0`, 1 minute, Databento, 2010-06 → 2026-08-28 (holdout postérieur non touché), ajustés en ratio aux roulements (`recolte1.engine.load`, `USE_2010 = True`) |
| Séance | séance NYSE pleine (calendrier XNYS), barres 1 min démarrant de 9:30 à 15:59 NY ; demi-séances exclues ; jour écarté si la séance précédente n'est pas une séance pleine ou s'il manque la barre 9:30 ou 15:59 |
| Veille | séance XNYS pleine précédente : plus haut H, plus bas L, hauteur h = H − L, milieu M = (H + L) / 2, sur les barres 9:30-15:59 |
| Exécution | vectorbt `Portfolio.from_signals` sur barres 1 min (comme [run_nq_matin_sltp.py](run_nq_matin_sltp.py)) : entrée à la clôture de la barre de signal, stop et cible en fraction du prix d'entrée (`sl_stop`, `tp_stop`), touchés sur high / low des barres suivantes, stop prioritaire si les deux le sont dans la même minute ; sinon sortie à la clôture de la barre 15:59 (16:00) |
| Coût | 1 tick + 5 $ aller-retour (NQ 0,50 point, ES 0,35, YM 2), rapporté au prix non ajusté |
| Mesure | R net par trade = rendement net / (distance du stop / prix d'entrée) ; un trade au plus par jour et par règle |

## R1 : cassure du range de la veille, cible measured move

| Élément | Valeur |
|---|---|
| Jour éligible | ouverture (open de la barre 9:30) strictement dans ]L ; H[ |
| Signal | première barre dont le début est entre 9:30 et 15:29 et dont la clôture est > H (long) ou < L (short) ; seul le premier signal du jour compte |
| Stop | M (milieu du range de la veille) |
| Cible | H + h (long) ; L − h (short) |
| Taux de référence | p0 = d_stop / (d_stop + d_cible), distances mesurées depuis le prix d'entrée, moyenné sur les trades |

## R2 : règle des 80 % sur la zone de valeur de la veille

| Élément | Valeur |
|---|---|
| Profil de volume | séance de la veille, 9:30-15:59 ; le volume de chaque barre 1 min est réparti également sur les cases de prix de 1 tick (taille ajustée : tick × facteur de la dernière barre de la veille) comprises entre son plus bas et son plus haut ; grille de L à H |
| POC | case de volume maximal (en cas d'égalité, la plus proche de M, puis la plus basse) |
| Zone de valeur | 70 % du volume de la séance : on part de la POC et on ajoute une case à la fois, celle des deux cases adjacentes (au-dessus, au-dessous) qui a le plus de volume (au-dessus en cas d'égalité ; la seule restante en bordure de grille) jusqu'à ≥ 70 % ; VAH = bord haut de la case la plus haute, VAL = bord bas de la plus basse |
| Jour éligible | ouverture (open de la barre 9:30) > VAH (cas « au-dessus ») ou < VAL (cas « au-dessous ») |
| Périodes de 30 min | 9:30-10:00, 10:00-10:30, … ; clôture d'une période = clôture de sa dernière barre 1 min |
| Signal | première fois que deux périodes consécutives clôturent dans [VAL ; VAH], la seconde se terminant au plus tard à 15:00 ; entrée à la clôture de la seconde |
| Sens | ouverture au-dessus → short, cible VAL ; ouverture au-dessous → long, cible VAH |
| Stop | extrême de la séance depuis 9:30 jusqu'à l'entrée incluse (plus haut si short, plus bas si long) |
| Taux de référence | p0 = d_stop / (d_stop + d_cible), comme R1 ; l'affirmation à confronter est un taux de cible atteinte de 80 % |

## Tests (6 essais)

R1 et R2 sur NQ, ES et YM. Compteur global d'essais : 1 689 avant ce document (n° 21 compris) → **1 695**.

## Critères de succès, fixés à l'avance (décision sur NQ)

p unilatéral pour « R net moyen > 0 » par bootstrap par blocs mobiles circulaires (blocs de 10 trades, 2 000 tirages, recentré sous H0 ; même fonction que `run_prereg20.p_one_sided`), IC 95 % par `recolte1.engine.ci_mean`.

1. Une règle **réussit** si, sur NQ, son R net moyen est > 0 avec p unilatéral < 0,05 après correction de Holm sur les 2 règles,
2. **et** son R net moyen est positif (signe seulement) sur chacune des sous-périodes 2010-2017 et 2018-2026.
3. ES et YM ne décident pas, mais une règle qui réussit sur NQ avec un R net moyen négatif à la fois sur ES et sur YM est classée « À surveiller » et non candidate.

Rapportés en plus, sans valeur de décision : nombre de trades, taux de cible atteinte contre p0 (et contre 80 % pour R2), répartition des sorties (cible, stop, 16:00), R brut, R par an, Sharpe annualisé avec le vrai nombre de trades par an, drawdown maximal en R, années positives, distance médiane du stop en points, R net par sens (long, short).

## Conséquence fixée à l'avance

- Succès d'une règle : pré-enregistrement de cette règle, telle quelle, sur le holdout NQ postérieur au 2026-08-28, à ouvrir une seule fois quand il comptera au moins 100 trades ; ligne dans [[wiki/phenomenes]].
- Échec : ligne au registre des échecs ; la règle n'est rouverte qu'avec une donnée d'orderflow réelle (volume signé tick par tick, carnet) et un mécanisme écrit.
- Dans tous les cas, le taux de cible atteinte de R2 est comparé aux « 80 % » annoncés et noté dans le rapport.

## Ce qui est interdit après calcul

Changer les heures de séance, la définition du range ou de la zone de valeur (70 %, taille des cases, répartition du volume), les cibles, les stops, la fenêtre de signal, le coût ou la période ; ajouter un filtre (tendance, volatilité, jour de semaine, gap) ; ne garder qu'un sens ; exclure une année ; remplacer un marché.
