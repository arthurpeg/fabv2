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
