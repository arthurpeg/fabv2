---
type: research
updated: 2026-10-31
source: SSRN (revues du 2026-10-13, 2026-10-14, 2026-10-21, 2026-10-29)
status: ingested
---

# Revues de papiers SSRN

**Ce que c'est** : des lots de papiers repérés sur SSRN, classés, puis résumés. Les mieux classés deviennent des pré-enregistrements.

## Lots
| Date | Thème | Fichier brut | A donné |
|---|---|---|---|
| 2026-10-13 | OHLCV intraday (24 papiers) | [[papiers_ssrn_ohlcv_2026-10-13]] | n° 6 (Tolušić), 7 (Melvin-Prins), 8 (Valenti), 9 (Shum) : tous ❌ |
| 2026-10-14 | Ouverture US / gap d'ouverture | [[papiers_ssrn_ouverture_us_2026-10-14]] | n° 5 (DAX, De Gooijer) : ❌ |
| 2026-10-21, 10-29 | Overnight (3 récoltes) | [[papiers_ssrn_overnight_2026-10-21]], [[papiers_ssrn_overnight_2_2026-10-29]], [[papiers_ssrn_overnight_3_2026-10-29]], [[papiers_ssrn_overnight_sans_resume_2026-10-29]] ; résumés : [[resumes_papiers_overnight_recolte1]], [[resumes_papiers_overnight_recolte2]], [[resumes_papiers_overnight_recolte3]] | récolte 1 → [[wiki/experiments/nq-nuit-momentum]] |

## Règle d'ingestion
Le registre des papiers déjà vus est `papers/seen_papers.json` : le lire avant de proposer des papiers, et l'enrichir après. Les PDF (`papers/`, `papiers overnight ssrn/`) restent hors git.

## Ce que les papiers ont appris
Voir [[wiki/research/litterature-intraday]] et [[wiki/lessons]] : les effets publiés existent souvent en brut, rarement après coûts, et s'affaiblissent après publication.
