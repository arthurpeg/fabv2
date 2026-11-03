---
type: reference
updated: 2026-11-02
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
| HistData (DAX, Nikkei…) | `cache/histdata/` | [[wiki/concepts/histdata-fuseau]] |
| Papiers PDF et textes | `papers/`, `papiers overnight ssrn/` (hors git) | [[wiki/research/recoltes-ssrn]] |
| Clés API | `.env` (hors git, ne jamais copier) | — |
