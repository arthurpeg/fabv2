---
type: reference
updated: 2026-11-18
---

# Où sont les données

Page d'aiguillage : elle ne fait que pointer vers la source qui fait foi.

| Donnée | Emplacement | Page qui explique |
|---|---|---|
| Futures 1 min Databento `.v.0`, 2016-01 → 2026-08 | `D:/quant-data/Cotations/` | [[wiki/concepts/roulements]] |
| Futures 1 min Databento 2010-06 → 2015-12 | `cache/databento_2010/` | [[PREREGISTRATION_11]] |
| Séries ajustées en cache (anciennes) | `cache/*_adj.parquet` | [[wiki/concepts/roulements]] (piège : roulements manqués) |
| Argent (SI) 1 min London Strategic Edge, 2017-04 → 2026-08-28, prix **non ajustés**, contrat front qui roule au 1er jour du mois de livraison (≈ 2-3 séances quasi vides avant chaque roulement, gap moyen 0,8 % au roulement) | `cache/lse/SI_lse_1m.parquet` ; chargé ajusté par `recolte1.engine.load("SI")` (roulements : `lse_rolls`) | [fetch_lse.py](../../fetch_lse.py) (docstring), [[reports/si_fattinger_report]] |
| **NQ 1 min London Strategic Edge, 2026-01-01 → 2026-11-03** (symbole `NASDAQ100`, marché `futures`, plan gratuit), prix **non ajustés**. Contient le **holdout** (après le 2026-08-28 : 47 séances RTH au 2026-11-03), **pas encore ouvert** (seule la couverture a été vérifiée). Contre Databento sur 2026-01 → 08-28 : écart médian de 1 tick par minute (35 % de minutes identiques), mais le contrat ne roule pas les mêmes jours (2026-03-18, 2026-06-14 → 16 sur un autre contrat, ±220 à 300 pts). Trous dans le holdout : RTH du 2026-10-12 (86 barres), 2026-10-16 9:30 → 9:58, soirs du 2026-10-05, 10-14 et 11-02 | `cache/lse/NQ_lse_1m.parquet` | [fetch_lse.py](../../fetch_lse.py) (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <fin>`) |
| **FX au comptant Dukascopy, bid ET ask** (ECN SWFX : cotations, pas des transactions, pas des CFD ; volume propre à Dukascopy), 9 paires : EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD, USDNOK, USDSEK. **Horaire 2010-01 → 2016-12** ; **1 min 2012-01-11 → 2016-12** (la bibliothèque ne sert pas de minutes avant). **USDCHF, USDCAD, NZDUSD prolongés jusqu'au 2026-08-28** (horaire et 1 min ; pas de future chez nous ; spread médian 2017-2026 ≈ 1,0 bp CHF, 0,9 CAD, 1,7 NZD). NOK et SEK écartés des tests (spread 3-4 bp, au-dessus de l'effet visé). USDJPY janvier-septembre 2010 reconstruit depuis les ticks (identique aux bougies officielles sur 72 heures testées). Index UTC au début de la barre ; colonnes bid OHLC, `ask_*`, `mid_open`, `mid_close`, `spread_close`, `volume`. Paires cotées comme sur le marché (inverser pour USDxxx). Quelques heures de cotation le dimanche avant 20 h UTC en 2010-2012 : exclure le week-end. Contre 6E/6B/6J/6A en 2016 : corrélation horaire 0,997 à 0,999 | `cache/dukascopy/<PAIRE>_1h.parquet`, `cache/dukascopy/<PAIRE>_1m.parquet` (1,3 Go, hors git) | [fetch_dukascopy.py](../../fetch_dukascopy.py) (docstring) |
| Spot FX M15 Dukascopy **bid seul**, EURUSD, GBPUSD, USDJPY, GBPJPY, 2013 → 2025-06 (autre dépôt) | `C:/Users/arthu/strategie trading/data_m15/` | `download_intraday_long.py` de ce dépôt |
| HistData (DAX, Nikkei…) : **des indices en CFD, pas du FX** malgré les noms (AUXAUD, GRXEUR, HKXHKD, JPXJPY) | `cache/histdata/` | [[wiki/concepts/histdata-fuseau]] |
| Papiers PDF et textes | `papers/`, `papiers overnight ssrn/` (hors git) | [[wiki/research/recoltes-ssrn]] |
| Clés API | `.env` (hors git, ne jamais copier) | — |
