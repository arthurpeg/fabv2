---
type: concept
updated: 2026-10-31
---

# Compteur global d'essais

**Définition** : nombre cumulé de règles testées dans le dépôt depuis le premier pré-enregistrement. Il sert de N dans le [[wiki/concepts/dsr|DSR]] et pour juger combien de faux positifs on attend.

**Dans ce dépôt** : chaque pré-enregistrement annonce « compteur X → Y » ; chaque rapport donne le compteur après exécution. La valeur courante est celle du rapport le plus récent : `wiki/update_hot.py` la relit dans `reports/*.md` et l'affiche dans [[wiki/hot]].

Repères : 93 (lot initial) → 138 (réplications) → 224 (LETF, n° 9) → 1 455 (récolte 1, ~927 tests post-hoc, puis n° 10) → 1 467 (n° 12) → 1 471 (n° 13) → 1 473 (n° 14) → 1 474 (variante « nuits d'annonce seules », exploratoire, non pré-enregistrée) → 1 475 (variante « nuits d'annonce rouge seules », exploratoire) → 1 478 (n° 15) → 1 480 (n° 16) → 1 482 (n° 17) → 1 485 (n° 19) → 1 493 (stop au range du soir, NQ de nuit, exploratoire, 8 variantes) → 1 501 (corrélation entre sessions NQ, exploratoire, 8 paires) → 1 520 (matinée US → après-midi NQ, exploratoire, 12 couples + 7 règles) → 1 553 (sessions de l'or, exploratoire, 7 sessions + 23 heures + 3 fenêtres a posteriori) → 1 555 (n° 20, matinée US sur ES et YM ; le pré-enregistrement annonçait 1 520 → 1 522 sans voir les essais de l'or menés en parallèle) → 1 559 (matinée US NQ avec SL/TP 1/1 et 2/2 ATR, exploratoire, 4 variantes) → 1 577 (anatomie de la reprise de l'or, exploratoire, 18 découpes) → 1 631 (affirmations de Fattinger-Ziegler sur l'or, exploratoire, 54 tests) → 1 685 (mêmes 54 tests sur l'argent, données London Strategic Edge) → 1 689 (n° 21, réservé) → 1 695 (n° 22, lecture de niveaux : measured move et règle des 80 %, NQ ES YM).

**Piège** : la récolte 1 n'a pas mis le compteur à jour dans son rapport ; il a été rattrapé au n° 10.

**N effectif** : les essais sont très corrélés par grappes (prime de nuit testée à toutes les heures). Estimation au 2026-11-06 : ≈ 610 essais effectifs pour 1 742 (Li & Ji sur 560 séries sauvegardées, extrapolé) ; voir [[reports/inference_overnight_report]]. Le compteur brut reste la référence des pré-enregistrements.
