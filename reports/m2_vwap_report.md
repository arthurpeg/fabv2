# Bande de bruit M2 : exiger le VWAP à l'entrée (code des auteurs)

*2026-11-22. Vérification de fidélité de [[wiki/experiments/m2-bande-bruit-nq]], demandée par l'utilisateur. Grille figée et commitée dans l'en-tête de [run_m2_vwap.py](../run_m2_vwap.py) avant tout calcul (commit `f59c2d5`). **Rien n'a été modifié dans `fab/strategies.py` ni publié vers le bot du VPS** (le bot n'utilise d'ailleurs pas la bande de bruit). Données 2016-01 → 2026-08-28 déjà explorées ; aucune réserve lue ; pas de verdict B1 (la bande de bruit NQ reste au registre, réouverture seulement sur des données après le 2026-08-28). Compteur global : 2 091 (2 085 + 6 essais). Sorties : `results/m2_vwap/`.*

## Ce qui change

Notre `m2_noise` entre dès que la clôture d'un contrôle sort de la bande. Le code publié par Zarattini, Aziz et Barbon (et les répliques de Delgado, Paz et Chuk) exige en plus que le prix soit **du même côté du VWAP** : achat si clôture > bande haute **et** > VWAP, vente si < bande basse **et** < VWAP. Tout le reste est identique (σ sur 14 jours, bande avec la clôture de la veille, VWAP au prix typique, contrôles 10:00 → 15:30, stop suiveur max(bande, VWAP), sortie à 16:00, coût 1 tick + 5 $).

Vérification manuelle : le 29/01/2026 à 15:00, NQ est sous la bande basse mais au-dessus du VWAP ; la version actuelle vend, la version VWAP s'abstient. Sur NQ, 103 entrées disparaissent et 17 apparaissent (effet sur les trades suivants de la journée).

## Résultats (Sharpe net annualisé ; IS 2016-2022, OOS 2023 → 2026-08)

| Actif | Taille | Entrée | Trades | IS | OOS | Total | Pts nets/trade | Écart journalier VWAP − actuelle (t NW) |
|---|---|---|---|---|---|---|---|---|
| **NQ** | 1× | actuelle | 2 333 | 1,18 | 1,14 | 1,16 | 6,39 | |
| **NQ** | 1× | **VWAP** | 2 247 | **1,26** | **1,19** | **1,23** | **7,11** | **+0,24 bp (2,27)** |
| NQ | vol. cible | actuelle | 2 333 | 0,83 | 1,08 | 0,92 | | |
| NQ | vol. cible | VWAP | 2 247 | 0,85 | 1,15 | 0,95 | | +0,17 bp (1,14) |
| ES | 1× | actuelle | 2 380 | 0,67 | 0,45 | 0,60 | 0,85 | |
| ES | 1× | VWAP | 2 307 | 0,71 | 0,52 | 0,65 | 0,94 | +0,12 bp (1,45) |
| ES | vol. cible | actuelle | 2 380 | 0,59 | 0,14 | 0,44 | | |
| ES | vol. cible | VWAP | 2 307 | 0,62 | 0,15 | 0,46 | | +0,09 bp (0,67) |
| YM | 1× | actuelle | 2 379 | 0,06 | −0,19 | −0,01 | 0,11 | |
| YM | 1× | VWAP | 2 303 | 0,09 | −0,17 | 0,02 | 0,39 | +0,08 bp (0,67) |
| YM | vol. cible | actuelle | 2 379 | −0,12 | −0,04 | −0,09 | | |
| YM | vol. cible | VWAP | 2 303 | −0,15 | −0,09 | −0,13 | | −0,15 bp (−0,98) |

Sharpe par année : `results/m2_vwap/sharpe_par_annee.csv`. NQ 1× avec VWAP : 2016 −0,66 · 2017 +0,94 · 2018 +2,85 · 2019 +0,18 · 2020 +1,47 · 2021 +1,18 · 2022 +1,70 · 2023 +2,29 · 2024 +1,41 · 2025 +0,86 · 2026 +0,46. La version VWAP fait mieux ou autant que l'actuelle dans 9 années sur 11 sur NQ.

## Lecture

1. **Le VWAP à l'entrée améliore M2, modestement mais régulièrement** : sur NQ à taille fixe, Sharpe 1,16 → 1,23, +0,7 pt par trade, 4 % de trades en moins, écart journalier positif à t 2,27. Sur ES, même sens, plus faible (0,60 → 0,65). Sur YM et avec la volatilité cible, l'effet est dans le bruit.
2. **Avec cette correction, NQ à taille fixe retrouve exactement le chiffre des auteurs pour le future Nasdaq (Sharpe 1,23 sur 2007-2024, FAQ Q13)**, sur une autre période (2016-2026). ES reste loin de leur S&P (0,65 contre 1,32) : l'écart ne vient donc pas de notre entrée, mais probablement de la période (leur échantillon inclut 2008-2015) et des coûts.
3. Ce n'est **pas** une validation : ces données ont déjà servi à M2, et la correction a été choisie pour coller au code publié, pas pour améliorer le résultat. Elle rend notre M2 conforme au papier ; la seule validation possible reste le forward (données après le 2026-08-28).

## Suite proposée

Adopter l'entrée avec VWAP comme définition de référence de la bande de bruit NQ dans nos travaux (et dans tout futur pré-enregistrement forward), sans toucher au bot tant que l'utilisateur ne le demande pas.
