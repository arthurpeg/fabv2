---
type: concept
updated: 2026-10-31
---

# Découpage IS / OOS et holdout

**Convention** : IS = 2016–2022, OOS = 2023 → 2026-08 (premiers pré-enregistrements). Depuis le n° 11, 2011-07 → 2015 sert d'OOS temporel (Databento 2010–2015 achetés, `cache/databento_2010/`).

**Holdout unique** : les données postérieures au 2026-08-28. On ne les ouvre qu'une fois, pour un test pré-enregistré.

**Plan figé au [[PREREGISTRATION_26]]** (2026-11-03) : mom, M2 (EMA 9:30), 3n SL et le rebond après forte baisse. Lectures le 2028-02-29 et le 2029-08-31 (succès seulement si z ≥ 3,0), puis le 2031-08-29 (verdict, Holm). D'ici là, **aucun calcul de prix, de rendement, de signal ou de paper trading de ces règles sur ces données** ; seuls le téléchargement mensuel et la vérification de couverture sont permis (`cache/lse/NQ_lse_1m.parquet`, voir [[wiki/reference/donnees]]).

**Hors échantillon « partiel »** : un autre actif sur la même période (ex. ES/YM au n° 10) ; utile mais faible, car les indices sont corrélés.

**Voir aussi** : [[wiki/concepts/pre-enregistrement]]
