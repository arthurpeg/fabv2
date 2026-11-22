---
type: registry
updated: 2026-11-22
---

# Registre des données : vierges, explorées, réservées, consommées

> Lire avant tout calcul de rendement sur un actif ou une période. La règle est dans [[wiki/concepts/is-oos]] et dans `CLAUDE.md` (règle 4).
>
> **États** :
> - **vierge** : aucun prix, rendement, signal ou P&L n'a été calculé. Les contrôles de qualité sont permis : comptes de barres, trous, spreads, corrélations, mais aucune moyenne de rendement.
> - **explorée** : on y a regardé des rendements. Tout ce qu'on y trouve est en échantillon.
> - **réservée** : une réserve hors échantillon déclarée ici avant le premier regard, attachée à une famille d'idées.
> - **consommée** : une réserve ouverte une fois par un pré-enregistrement. Elle devient ensuite une donnée explorée pour toute nouvelle idée.
>
> On ajoute une ligne à chaque changement d'état, datée et avec sa source. On ne supprime jamais une ligne : on met à jour la colonne « État », et on garde l'ancien état dans « Historique ». L'inventaire ci-dessous date du 2026-11-19 et a été reconstitué à partir du journal et des pré-enregistrements. En cas de doute, la tranche est classée **explorée**.

## Inventaire

| Actif | Période | Source | État | Historique / qui l'a vue |
|---|---|---|---|---|
| ES, NQ, YM | 2016-01 → 2026-08-28 | Databento 1 min | explorée | n° 1 à 26, récolte 1, overnight, propfirm… |
| ES, NQ, YM | 2010-06 → 2015-12 | Databento 1 min (`cache/databento_2010/`) | explorée | Réserve OOS des n° 11, 12, 19, 24, 25 : consommée plusieurs fois |
| ES, NQ, YM (réserve par question) | 2010-06-08 → 2015-12-31 | Databento 1 min (`cache/databento_2010/`) | **réservée** (question « ORB 30 min par jour de la semaine » seulement) | Déclarée le 2026-11-22, avant tout calcul, par [[wiki/experiments/orb30-jours-semaine]] (règle de Subhani 2026). Jamais vue par une règle ORB. La tranche reste explorée pour tout le reste (n° 11, 12, 19, 24, 25, règle de la 1ʳᵉ bougie) |
| ES, YM (réserve par question) | 2021-10-01 → 2026-08-28 | Databento 1 min | **réservée** (question « sortie » seulement) | Déclarée le 2026-11-22, avant tout calcul, par la suite de [[wiki/experiments/nq-orb-bougie-sorties]] (run_orb_bougie_indices.py) : même question que la ligne NQ ci-dessous, sur ES et YM. R4 y a déjà été vu (Sharpe net 2023-2026 : ES −0,64, YM −0,81) |
| NQ (réserve par question) | 2021-10-01 → 2026-08-28 | Databento 1 min | consommée | Ouverte une fois le 2026-11-22 par [[PREREGISTRATION_30]] (commit bade69c, hors protocole, demandé par l'utilisateur) : rejet ([[reports/prereg30_report]]). Avant : Déclarée le 2026-11-22, avant tout calcul, par [[wiki/experiments/nq-orb-bougie-sorties]] : règle de la 1ʳᵉ bougie de Zarattini-Aziz avec d'autres sorties (sans stop ni objectif ; stop k × ATR et objectif RR × stop). Ces sorties n'ont jamais été calculées sur NQ. La tranche reste explorée pour tout le reste, y compris R4 (stop à l'extrême de la bougie, 10R), déjà vu jusqu'au 2026-08 |
| NQ | 2026-08-29 → 2026-11-03 | London Strategic Edge | explorée | Lecture anticipée du n° 26 (avenant A) |
| NQ | à partir du 2026-11-04 | Databento (à acheter), LSE | **réservée** | Holdout du n° 26 (mom, M2, 3n SL, rebond) ; lectures 2028-02-29, 2029-08-31, 2031-08-29 |
| ES, YM, autres indices | après le 2026-08-28 | — | vierge | Pas téléchargé |
| FDAX, DAX (HistData, CFD) | historique disponible | Databento, HistData | explorée | n° 5 (gap d'ouverture) |
| CL | 2016-01 → 2026-08-28 | Databento 1 min | explorée | n° 1, 3 (R7) |
| GC | 2016-01 → 2026-08-28 | Databento 1 min | explorée | n° 1, 3 (R7), sessions de l'or, Fattinger-Ziegler |
| SI | 2017-04 → 2026-08-28 | London Strategic Edge | explorée | Fattinger-Ziegler |
| 6E, 6B, 6J, 6A | 2016-01 → 2026-08-28 | Databento 1 min | explorée | n° 1 à 4, R2, R5, R6, n° 27, 28 (référence), backtest du yen |
| 6J (réserve par question) | 2023-07-01 → 2026-08-28 | Databento 1 min | **réservée** (questions A et B seulement) | Réserve par question de [[wiki/experiments/yen-derive-concentree]] : profil par demi-heure 08:00-16:55 ET et seuils sur la hausse du yen à 3 jours, jamais calculés ; la tranche reste explorée pour tout le reste (effet de base, R4) |
| EUR, GBP, JPY, CHF, AUD, CAD, NZD spot | 2010-01 → 2015-12 | Dukascopy 1 h / 1 min | explorée | n° 27 (moyennes des 4 sessions de Zhang) ; règle du yen 2012-2015 ; les autres fenêtres horaires n'ont pas été regardées, mais la tranche est classée explorée par prudence |
| CHF, CAD, NZD spot | 2016-01 → 2026-08-28 | Dukascopy 1 h / 1 min | explorée | n° 27 |
| USDNOK, USDSEK spot | 2010-01 → 2016-12 | Dukascopy 1 h / 1 min | **vierge** | Contrôles de qualité seulement (spreads, couverture) |
| EUR, GBP, JPY spot M15 (bid) | 2013 → 2025-06 | Dukascopy (`strategie trading`) | explorée | Contrôle de qualité du 2026-11-17 : moyennes de session vues |
| Yen (6J, USDJPY, toute paire contre JPY) | à partir du 2026-08-29 | Databento (à acheter), Dukascopy | **réservée** | Holdout du n° 28 (short yen en session US), mêmes dates de lecture que le n° 26 ; aussi forward du n° 29 (R4 + SL 2 ATR H1), mêmes dates |
| USDJPY comptant | début des ticks (2003-05) → 2009-12-31 | Dukascopy, ticks du datafeed → barres 1 min bid/ask | **réservée** | Vierge jusqu'au 2026-11-21 (disponibilité vérifiée par 3 codes HTTP, aucun prix lu) ; réserve du n° 29 (PREREGISTRATION_29), à télécharger puis à ouvrir une seule fois |
| Autres FX, CL, GC, SI | à partir du 2026-08-29 | — | vierge | Pas téléchargé |
| XAU/USD comptant (or) | 2003-05-05 → 2015-12-31 | London Strategic Edge 1 min (`cache/lse/XAU_lse_1m.parquet`) | consommée | Réserve du n° 21 (PREREGISTRATION_21, commit a2dc0b1 ; avenant A 7fde669), ouverte une fois le 2026-11-21 : échec ([[reports/prereg21_report]]) ; historique : réservée du 2026-11-02 au 2026-11-21 |
| XAG/USD comptant (argent) | 2003-05-05 → 2017-03-31 | London Strategic Edge 1 min | indisponible | Réserve prévue au n° 21, jamais téléchargée : LSE limité à 10 ans (dès 2016-11-21), Dukascopy sans barres avant 2016 ; n° 21 mené sur l'or seul (avenant A) |

## Réserves déclarées pour des idées futures

*Avant le premier calcul sur une tranche vierge, on ajoute ici : la date, la tranche explorable, la réserve (par défaut les 30 % les plus récents, au moins 3 ans), et la famille d'idées concernée.*

| Date | Famille d'idées | Tranche explorable | Réserve | État |
|---|---|---|---|---|
| 2026-11-22 | Session domestique et solde commercial ([[wiki/experiments/fx-exportateur-importateur]]) | Devises flottantes hors 7 majeures (NOK, SEK, PLN, CZK, HUF, MXN, ZAR, SGD, TRY, ILS…, liste figée à l'étape 1), comptant Dukascopy, 2010-01-01 → 2021-08-31 | Mêmes devises, 2021-09-01 → 2026-08-28 (5 ans) | **réservée**, non ouverte (idée abandonnée à l'étape 1 le 2026-11-22, [[reports/fx_balance_report]]) ; exploration 2010-01 → 2021-08 de NOK, SEK, PLN, MXN, ZAR, SGD, TRY : **explorée** ; spreads de la réserve vus (contrôle de qualité) |

| Date | Actif | Tranche explorable | Réserve | Famille d'idées | État |
|---|---|---|---|---|---|
