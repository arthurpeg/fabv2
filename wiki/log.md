---
type: log
---

# Journal du wiki

Append-only : une entrée par événement, ajoutée en bas, jamais modifiée. Format : `## [AAAA-MM-JJ] <type> | <ce qui s'est passé> | <résultat>`. Types : `setup`, `experiment`, `prereg`, `ingest`, `query`, `lint`, `abandon`, `fix`.

Historique antérieur au wiki (repris de git et des rapports) :

## [2026-10-12] experiment | Lot initial de 93 stratégies intraday (n° 1), puis pistes A/B (n° 2) | 2 survivants ; fade de gap passe, M2 NQ rejeté (DSR)
## [2026-10-12] experiment | 42 réplications fidèles (n° 3) et timing d'exécution FX (n° 4) | effets bruts retrouvés mais < coût ; X3 utile pour l'exécution ; compteur 138
## [2026-10-14] experiment | Gap d'ouverture DAX, NP-FDA (n° 5) | ❌ ; compteur 174
## [2026-10-15] experiment | Reprise FX 18:00 (n° 6) et fix de Londres (n° 7) | ❌ les deux ; compteur 201
## [2026-10-20] experiment | Asymétrie Valenti (n° 8) et momentum LETF (n° 9) | ❌ les deux ; compteur 224
## [2026-10-29] experiment | Contrôle pile ou face SL/TP ATR sur NQ | aucun edge, comme prévu
## [2026-10-30] experiment | Récolte 1 (927 tests post-hoc), puis règle NQ de nuit n° 10 à 12 et robustesse 13 | n° 10 ❌, n° 11 ✅, n° 12 α +6 %/an ; compteur 1 467

## [2026-10-31] setup | Création du wiki (hubs, SCHEMA, ledger rempli, 4 expériences, 9 concepts, hooks, Obsidian) | wiki opérationnel
## [2026-10-31] query | Chiffrage Databento des coûts d'exécution NQ/MNQ (bbo-1m, bbo-1s, tbbo) | bbo-1m NQ 2010-2026 7,71 $ + MNQ 2019-2026 3,49 $ ; tbbo > 1 600 $ ; rien acheté
## [2026-10-31] prereg | N° 13 : 4 filtres « à plat » anti-drawdown sur la règle NQ de nuit, contrôle aléatoire | ❌ aucun retenu ; règle inchangée ; compteur 1 471
## [2026-10-31] ingest | Calendrier BLS NFP/CPI 2010-2026 (388 dates) dans config/calendrier_macro_bls.csv | figé avant le n° 14
## [2026-10-31] prereg | N° 14 : éviter les annonces NFP/CPI de 8:30 dans la règle NQ de nuit | ❌ ; nuits d'annonce = meilleures nuits (~40 % des R 2016-2026) ; compteur 1 473
## [2026-10-31] query | Exploratoire, non pré-enregistré : règle NQ de nuit limitée aux nuits NFP/CPI (2011-2026) | +0,27 R/trade [+0,13 ; +0,41], 23 trades/an, +6,3 R/an (contre +22 toutes nuits) ; NFP +0,41, CPI +0,13 (IC inclut 0) ; compteur 1 474
## [2026-10-31] ingest | Calendrier US « rouge » 2010-2026 (NFP, CPI, PPI, JOLTS, ventes au détail, PIB avancé, PCE, ISM ×2, FOMC décision et minutes) : build_calendar_macro.py → config/calendrier_macro_us.csv (BLS, FRED/ALFRED, Fed ; ISM par règle) | complet 2011-2026
## [2026-10-31] query | Exploratoire : règle NQ de nuit limitée aux nuits d'annonce rouge | aucun avantage : +0,087 R/trade contre +0,089 sans annonce ; 2016-2026 +0,048, DD −40 R ; compteur 1 475
## [2026-10-31] ingest | Historiques VIX et VIX3M du CBOE dans config/ | pour le n° 15
## [2026-10-31] prereg | N° 15 : filtres VIX (Donninger 0,87, Vojtko MM20) et taille selon σ20 sur la règle NQ de nuit | ❌ les 3 ; 9 filtres anti-DD rejetés au total ; compteur 1 478
## [2026-10-31] prereg | N° 16 : clôture sous VWAP 15:15-16:15 (pression vendeuse) sur règle de nuit, sélection ES+YM, confirmation NQ | ❌ H et filtre ; compteur 1 480
## [2026-10-31] prereg | N° 17 : exécution au VWAP (entrée 20:00-21:00, sortie au temps 9:00-9:30) pour la règle de nuit | non retenue (NQ +0,005 R IC inclut 0 ; ES/YM +0,013 R) ; compteur 1 482
## [2026-10-31] ingest | Achat Databento bbo-1m NQ 2010-2026 + MNQ 2019-2026 (11,20 $) dans cache/databento_bbo | spread NQ médian 2-4 ticks (pas 1) ; copie vers D: refusée (accès Windows), préparée dans cache/a_copier_vers_D
## [2026-10-31] prereg | N° 18 : prop firm comme option, FTMO 1-Step avec trades NQ au hasard (branche propfirm-ftmo) | EV +178 $ ± 6 (10k), +2 098 $ ± 64 (100k) ; sans RAZ de la perte max −34 % ; hors compteur (1 482)
## [2026-10-31] prereg | N° 18 avenant A : stop 1 ATR M15 (≈ 0,12 % du prix) au lieu de 0,5 % | EV +71 $ ± 4 (10k), +1 035 $ ± 43 (100k) ; le spread 1 pb (0,083 R/trade) explique tout l'écart (sans coût +3 023 $) ; hors compteur
## [2026-10-31] experiment | Règle NQ de nuit recalculée avec les spreads réels bbo-1m (NQ 2011-2026, MNQ 2019-2026) | +0,076 R/trade contre +0,088 au coût fixe ; MNQ +0,067 à 1,24 $ A/R ; compteur inchangé
## [2026-10-31] prereg | N° 18 avenant B : entrée 9:50 ET, stop 1 ATR M15, spread 1,5 pt (0,041 R) / 1 pt | EV +161 $ ± 6 (10k), +1 933 $ ± 61 (100k) à 1,5 pt ; +187 $ / +2 187 $ à 1 pt ; hors compteur
## [2026-10-31] fix | Renommage costs18 → couts_reels_nq_nuit (script, rapport, résultats) pour éviter la confusion avec le pré-enregistrement n° 18 (FTMO) | liens mis à jour
## [2026-10-31] prereg | N° 18 avenant C : règle NQ de nuit (3 787 trades 2011-2026) sur FTMO 1-Step, éval 2 % / financé 1 %, spread 1,5 pt | passage 50,8 %, EV +853 $ (10k), +8 849 $ (100k) ; sans edge +98 $ / +1 295 $ ; sans RAZ +307 $ / +3 390 $ ; hors compteur
## [2026-10-31] query | Vérification des règles FTMO 1-Step sur ftmo.com (perte max, RAZ après reward, perte journalière, meilleur jour, reward au 14e jour) | toutes conformes au simulateur du n° 18 ; RAZ confirmée (« fully resets ») ; « does not reset » = Instant Account
## [2026-10-31] query | Exploratoire : 5 comptes FTMO 10k décalés de 1 ou 3 mois sur la règle NQ de nuit (run_propfirm_farm.py) | ne lisse pas : écart-type ~2 000 $/compte sur 2 ans (indépendants : 873 $) ; 4,1/5 rachètent la même nuit, corrélation 0,97
## [2026-10-31] prereg | N° 18 avenant D : règle NQ de nuit sur LucidFlex 50K en MNQ (règles lues sur lucidtrading.com), éval 400 $ / financé 200 $ | EV +157 $ ± 6 par éval au prix actuel du NQ (+65 $ en points historiques, protocole) ; sans edge −55 $ ; hors compteur
## [2026-10-31] query | Exploratoire : pires séries FTMO + règle NQ de nuit (run_propfirm_streaks.py, 657 départs) | 6 évals ratées d'affilée au pire (521 $ sur 10k) ; 11 mois sans reward (2018-03 → 2019-01) ; creux de trésorerie −608 $ (10k) / −3 842 $ (100k) ; cause : meilleur jour 50 % avec des TP de +2,5 %
## [2026-10-31] prereg | N° 18 avenant E : FTMO, financé en RR 2 (TP 4 ATR, 1 %) sur la règle NQ de nuit | EV +1 009 $ ± 21 (10k), +10 408 $ (100k), +14 % contre RR 2,5 ; pires séries : 6 évals ratées, 239 nuits sans reward (2022) ; hors compteur
## [2026-10-31] query | En cours : contrôle vectorbt de la trace FTMO avenant E (run_propfirm_vbt.py) | vectorbt exécute les 3 708 trades prévus, P&L à ≤ 0,0145 $ du calcul Python ; le rejeu des règles bifurque encore sur des seuils à quelques millionièmes (MIN_RISK 0,05 % le 2023-11-01) ; tolérances ajoutées aussi à run_propfirm_streaks.py, ses résultats sont à relancer
## [2026-10-31] query | Avenant E refait avec vectorbt (run_propfirm_vbt.py) : rendements de chaque nuit par Portfolio.from_signals, règles FTMO en Python | Monte-Carlo identique (EV +1 009 $ 10k, +10 408 $ 100k) ; pires séries identiques (6 évals ratées, 239 nuits sans reward) ; contrôle tailles réelles à 3e-11 $ ; tolérance 0,001 % et marge mini 0,05 % ajoutées aux scripts de trace, pires valeurs inchangées
## [2026-10-31] query | Exploratoire 2026 (run_propfirm_2026.py) : FTMO 10k, règle NQ de nuit, 1 éval puis 1 de plus par reward, du 2026-01-02 au 2026-08-28 | à la lettre : 2 évals, 1 reward, net +346 $ ; avec rachat après échec : 29 évals, 7 rewards, net +1 574 $ (8 financés ouverts à −3,68 %)
## [2026-10-31] query | Règle NQ de nuit, entrée 19:00 / 20:00 / 21:00 ET recalculée avec vectorbt (run_nq_nuit_heures.py), corrélations | R net +0,076 / +0,088 / +0,083, Sharpe 0,91 / 1,00 / 0,87 ; corr. par nuit 0,85 / 0,78 / 0,70 ; panier égal Sharpe 1,01 ; descriptif, hors compteur
## [2026-10-31] query | S1 Noise Area NQ + stop dur 1R (fichier S1_R_stop.py transmis) refait avec vectorbt (run_s1_r_stop_vbt.py), 2016-01 → 2026-08-28 | S1 d'origine 1 827 trades (1 828 annoncés), Sharpe $ 1,03 ; plancher 0,5 % + stop 1R, 1 MNQ : +0,106 R/trade (t 4,0), Sharpe en R 1,26, +2 406 $/an, pire baisse 2 521 $ ; risque 500 $ : +7 932 $/an, pire baisse 5 800 $ ; boucle d'origine reproduite trade par trade (écarts ≤ 0,09 $) ; plancher choisi après coup, hors compteur, M2 reste rejetée
## [2026-10-31] query | Exploratoire : ferme FTMO 10k, un signal par compte (19:00 / 20:00 / 21:00), vectorbt + règles FTMO (run_propfirm_farm_heures.py) | mois sans reward 58 % → 42 %, corr. trimestrielle 1,00 → 0,56, creux moyen −300 → −238 $ ; écart-type sur 2 ans inchangé (1 885 → 1 880 $/compte) ; gain moyen 4 766 → 4 270 $
