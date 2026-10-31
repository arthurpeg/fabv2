---
type: concept
updated: 2026-10-31
---

# Roulements (rolls) et ajustement des futures

**Définition** : passage d'une échéance à la suivante ; sans ajustement, le saut de prix entre échéances crée un faux rendement (il tombe à 00:00 UTC, donc en session Asie).

**Règle du dépôt** : ajustement **en ratio**, un roulement par cycle d'échéance, détecté comme le plus grand écart à 00:00 UTC entre le 7 et le 22 de mars/juin/sept./déc. (42 roulements par actif sur 2016–2026) ; or : entre le 20 d'un mois impair et le 5 du suivant (64). Implémentée dans [run_sessions.py](../../run_sessions.py).

**Piège** : `fab.core.load` et le cache `cache/*_adj.parquet` ratent ~10 roulements par actif (écart de portage faible en 2017–2019) et prennent le trou de données du 2020-06-30 sur YM pour un roulement. Ne pas les utiliser pour des rendements de nuit.
