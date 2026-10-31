---
type: hot
updated: 2026-10-31 18:50
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 485** (source : [[reports/prereg19_report]])
- Dernier pré-enregistrement : n° 19 ([[PREREGISTRATION_19]])
- Idées abandonnées au registre : 25 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-10-31

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-10-31] query | Plan prop firm refait chez Smart Trader Funds, challenge 1 Phase (run_propfirm_stf.py, règles lues sur smartraderfunds.com) | position gardée pendant les annonces 8:30 : EV −62 $ (10k) / +148 $ (100k) ; à plat à 8:19 : +390 $ / +4 512 $ (FTMO +1 009 / +10 408) ; 1×10k → 100k au 95e centile +2,8 k$ à 3 ans (FTMO +54,9 k$) ; 1×100k d'emblée +44,7 k$ médiane, pire +16,9 k$
- [2026-10-31] query | Variante F (1→2→3×10k puis 100k) : délai jusqu'au premier achat d'une éval 100k (run_propfirm_variants.py) | moyenne ~18 mois (379 nuits), médiane 375, 25e-75e centile 281-466 nuits, 90e 533, 3 départs sur 612 sans 100k en 3 ans
- [2026-10-31] query | Neuf variantes de montée FTMO au 95e centile (run_propfirm_variants.py) | meilleure : 1→2→3×10k puis 1→2→3×100k, +69,6 k$ médiane à 3 ans (5e c. +20,2 k$, pire +5,1 k$) ; remplacement un par un : pire +7,7 k$ ; grands sauts derniers
- [2026-10-31] query | Plan FTMO, seuils au 95e centile de l'argent sorti avant remboursement (run_propfirm_start1.py, section 4) | départ 450 $ ; A (10k→100k→trio 100k) +54,9 k$ médiane à 3 ans, pire +550 $ ; B (10k→trio 10k→trio 100k) +31,9 k$, pire +5,95 k$ ; apport au pire 158 $
- [2026-10-31] query | Plan FTMO, règle stricte du pire chemin (run_propfirm_start1.py, section 3) | pires chemins 608 / 1 738 / 3 842 / 7 685 / 10 978 $ ; B2 (1×10k → 3×10k → 3×100k) +15,7 k$ médiane à 3 ans, pire +5,1 k$, aucun apport ; trio 100k en 3 ans dans 24 % des départs
- [2026-10-31] query | Démarrer FTMO avec un seul 10k (run_propfirm_start1.py) : réserve et 3 chemins | réserve 650 $ (pire : 7 évals, 20:00) ; A 10k→100k→trio 100k +99,9 k$ médiane à 3 ans, apport dans 28 % ; B trio 10k→trio 100k +75,7 k$, apport dans 7 % ; C 10k→trio 100k +67 k$
- [2026-10-31] query | Plan FTMO : 10k puis 100k dès que les gains des 10k paient 1, 2 ou 3 trios d'évals 100k (run_propfirm_paths.py) | bascule ~10 / 13 / 18 mois ; +104 / +93 / +78 k$ médiane à 3 ans contre +67 k$ en paliers et +148 k$ en 100k d'emblée
- [2026-10-31] query | Chemin complet du plan FTMO (run_propfirm_paths.py, 612 départs, 3 ans) : paliers / 10k→100k / 100k d'emblée | 10k→100k jamais plus rapide ; 100k d'emblée : +148 k$ médiane à 3 ans contre +67 k$, meilleur dans 97 % des départs, apport max 1 374 $ en plus des 1 750 $ ; règle de réserve du plan initial trop prudente

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
