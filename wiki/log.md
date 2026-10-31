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
