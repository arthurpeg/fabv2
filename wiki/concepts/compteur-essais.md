---
type: concept
updated: 2026-10-31
---

# Compteur global d'essais

**Définition** : nombre cumulé de règles testées dans le dépôt depuis le premier pré-enregistrement. Il sert de N dans le [[wiki/concepts/dsr|DSR]] et pour juger combien de faux positifs on attend.

**Dans ce dépôt** : chaque pré-enregistrement annonce « compteur X → Y » ; chaque rapport donne le compteur après exécution. La valeur courante est celle du rapport le plus récent : `wiki/update_hot.py` la relit dans `reports/*.md` et l'affiche dans [[wiki/hot]].

Repères : 93 (lot initial) → 138 (réplications) → 224 (LETF, n° 9) → 1 455 (récolte 1, ~927 tests post-hoc, puis n° 10) → 1 467 (n° 12) → 1 471 (n° 13) → 1 473 (n° 14) → 1 474 (variante « nuits d'annonce seules », exploratoire, non pré-enregistrée) → 1 475 (variante « nuits d'annonce rouge seules », exploratoire) → 1 478 (n° 15) → 1 480 (n° 16) → 1 482 (n° 17) → 1 485 (n° 19) → 1 493 (stop au range du soir, NQ de nuit, exploratoire, 8 variantes) → 1 501 (corrélation entre sessions NQ, exploratoire, 8 paires).

**Piège** : la récolte 1 n'a pas mis le compteur à jour dans son rapport ; il a été rattrapé au n° 10.
