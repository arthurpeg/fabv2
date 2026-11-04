# Deux comptes FTMO 10k sur tout l'historique (2011-07 → 2026-11-03) : règle des annonces + cible + attente

*2026-11-04. **Exploratoire, hors compteur.** Script : [run_ftmo_deux_comptes_historique.py](../run_ftmo_deux_comptes_historique.py). Sorties : `results/ftmo_deux_comptes_historique/` (`run.log`, `jours.csv`, `evenements.csv`, `mois.csv`, `series_sans_reward.csv`).*

## Méthode

On suit **un seul chemin**. Les deux emplacements 10k sont ouverts le 01/07/2011, puis rachetés après chaque échec, jusqu'au 03/11/2026 (15,3 ans).

- **Comptes.** A = mom ; B = 3n + M2 (M2 seulement si 3n n'est sorti ni au stop ni au TP, avec une journée bornée à −r / +2r).
- **Risque.** 2,5 % en éval, avec l'objectif ramené au reste à faire ; 1 % en financé.
- **Règle des annonces** en financé : mom fermé à 8:19 les jours NFP / CPI / PIB, M2 fermé à 13:55 les jours de Fed.
- **Politique cible + attente** en financé.
- **Reward** au 14e jour calendaire après le premier trade du compte, et éval à 79 €.
- Règles et moteur : ceux de [[reports/ftmo_deux_comptes_report]].

## Résultats

| | Compte A (mom) | Compte B (3n + M2) | **Les deux** |
|---|---|---|---|
| Évals achetées (coût) | 43 (3 737 $) | 9 (782 $) | 52 (4 519 $) |
| Évals validées | 21 | 5 | 26 |
| Rewards | 119 | 98 | 217 |
| **Net (rewards − frais)** | **+36 971 $** (+2 410 $/an) | **+31 592 $** (+2 059 $/an) | **+68 562 $ (+4 469 $/an)** |
| **Max DD de trésorerie** | **−435 $** (31/07 → 26/10/2023, revenu le 27/02/2024) | **−261 $** (30/12/2022 → 30/06/2023) | **−435 $** (29/04 → 30/06/2025, revenu le 04/08/2025) |
| **Pire série d'évals sans reward** | **5 évals (434 $)**, du 31/07 au 23/11/2023 | **3 évals (261 $)**, du 30/12/2022 au 24/08/2023 | — |
| Plus longue attente d'un reward | 202 jours (31/01 → 21/08/2019, 4 évals) | 310 jours (13/06/2012 → 19/04/2013, compte financé en recul mais jamais perdu) | **98 jours sans aucun reward** (17/12/2012 → 25/03/2013) |
| Mois négatifs (flux de trésorerie) | 16 % | 4 % | 13 % |

**Évals achetées entre deux rewards** (nombre de fois) :
- A : 0 → 100 fois, 1 → 9, 2 → 5, 3 → 2, 4 → 2, 5 → 2 ;
- B : 0 → 94 fois, 1 → 2, 2 → 2, 3 → 1.

Dans 84 % (A) et 95 % (B) des cas, un reward suit directement le précédent, sans nouvelle éval.

**Corrélation des deux comptes :**
- P&L journalier de trading : **+0,24** sur les 2 251 jours où les deux tradent. Les nuits 3n tombent dans la nuit mom, d'où une corrélation positive.
- **Flux de trésorerie mensuels : +0,01**. Les rewards et les rachats des deux comptes ne tombent pas les mêmes mois. **Aucun mois n'est négatif pour les deux comptes à la fois.**

**Net par année civile (deux comptes) :**

| 2011 (juil-déc) | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (au 03/11) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| +1 341 | +7 055 | +4 172 | +5 913 | +4 529 | +3 364 | +4 794 | +4 352 | +4 101 | +4 366 | +4 496 | +2 869 | +2 836 | +3 886 | +4 588 | +5 901 |

## Lecture

1. **Sur 15 ans, aucune année n'est négative.** La pire année est 2023 (+2 836 $), et le pire creux de trésorerie n'a jamais dépassé **−435 $**. Il suffit d'avoir **environ 500 $ de côté** pour racheter les évals pendant les mauvaises séries, au-delà des 2 × 87 $ du départ.
2. **Au pire, 5 évals d'affilée sans reward sur A (fin 2023)**, et 3 sur B (2023). Les deux mauvaises séries se chevauchent sur la mi-2023, mais le creux total reste à −435 $, car B touchait encore des rewards pendant ce temps.
3. **Les deux comptes se complètent.** Leurs trades sont un peu corrélés (+0,24), mais leurs encaissements ne le sont pas (+0,01). B, avec la politique d'attente, garde très longtemps ses comptes financés : 9 évals en 15 ans.
4. **Réserves** :
   - Ce chemin est optimiste pour B. 3n et M2 ont été choisis sur 2013-2024 et ont échoué hors échantillon (n° 24 et 25). Leur rentabilité ici vient de la prime de nuit et du coût CFD actuel.
   - **Les délais FTMO ne sont pas modélisés** : examen de l'éval (1 à 4 jours ouvrés), fourniture d'un nouveau compte après un reward (1 à 2 jours).
   - Rewards supposés versés sans refus, spread CFD non mesuré.
   - Le PIB avancé du 29/10/2026 est une date supposée.
   - Le chemin dépend de la date de départ : voir [[reports/ftmo_deux_comptes_report]] pour la distribution sur 721 départs.
