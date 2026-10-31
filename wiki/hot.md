---
type: hot
updated: 2026-10-31 12:48
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 467** (source : [[reports/prereg12_report]])
- Dernier pré-enregistrement : n° 12 ([[PREREGISTRATION_12]])
- Idées abandonnées au registre : 18 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-10-31

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-10-31] query | Chiffrage Databento des coûts d'exécution NQ/MNQ (bbo-1m, bbo-1s, tbbo) | bbo-1m NQ 2010-2026 7,71 $ + MNQ 2019-2026 3,49 $ ; tbbo > 1 600 $ ; rien acheté
- [2026-10-31] setup | Création du wiki (hubs, SCHEMA, ledger rempli, 4 expériences, 9 concepts, hooks, Obsidian) | wiki opérationnel
- [2026-10-30] experiment | Récolte 1 (927 tests post-hoc), puis règle NQ de nuit n° 10 à 12 et robustesse 13 | n° 10 ❌, n° 11 ✅, n° 12 α +6 %/an ; compteur 1 467
- [2026-10-29] experiment | Contrôle pile ou face SL/TP ATR sur NQ | aucun edge, comme prévu
- [2026-10-20] experiment | Asymétrie Valenti (n° 8) et momentum LETF (n° 9) | ❌ les deux ; compteur 224
- [2026-10-15] experiment | Reprise FX 18:00 (n° 6) et fix de Londres (n° 7) | ❌ les deux ; compteur 201
- [2026-10-14] experiment | Gap d'ouverture DAX, NP-FDA (n° 5) | ❌ ; compteur 174
- [2026-10-12] experiment | 42 réplications fidèles (n° 3) et timing d'exécution FX (n° 4) | effets bruts retrouvés mais < coût ; X3 utile pour l'exécution ; compteur 138

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
