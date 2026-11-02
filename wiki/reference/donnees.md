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
| Argent (SI) 1 min London Strategic Edge, 2017-04 → 2026-08-28, prix **non ajustés**, contrat front qui roule au 1er jour du mois de livraison (≈ 2-3 séances quasi vides avant chaque roulement, gap moyen 0,8 % au roulement) | `cache/lse/SI_lse_1m.parquet` | [fetch_lse.py](../../fetch_lse.py) (docstring) |
| HistData (DAX, Nikkei…) | `cache/histdata/` | [[wiki/concepts/histdata-fuseau]] |
| Papiers PDF et textes | `papers/`, `papiers overnight ssrn/` (hors git) | [[wiki/research/recoltes-ssrn]] |
| Clés API | `.env` (hors git, ne jamais copier) | — |
