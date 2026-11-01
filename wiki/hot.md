---
type: hot
updated: 2026-11-01 15:45
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 485** (source : [[reports/prereg19_report]])
- Dernier pré-enregistrement : n° 19 ([[PREREGISTRATION_19]])
- Idées abandonnées au registre : 25 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-01

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-01] query | FTMO et FundingPips sur mesure avec financé ≤ 1 % et éval ≤ 2,5 % (filtre des grilles) | FTMO éval 2,5 % à 2 R, financé 1 % à 2,5 R, protection +4 % : 2019-2023 médiane +69,2 k$, pire +50,1 k$ (plan +48,9 k$) ; FundingPips +56,9 k$ (2 semaines : +49,4 k$)
- [2026-11-01] query | FTMO 1-Step sur mesure + plafond 2,5 % par trade (run_propfirm_ftmo_custom.py ; FundingPips refiltré) | 2019-2023, compte racheté 3 ans : FTMO éval 2 % à 2 R, financé 2,5 % à 1,5 R médiane +92,9 k$ (pire +30,2 k$, 31 évals, 9,9 k$ sortis au max) contre plan +48,9 k$ ; FundingPips éval 2 % à 3 R, financé 1,25 % à 2 R +67,8 k$
- [2026-11-01] query | FundingPips 1 Step Flex, gestion du risque sur mesure, 3 600 réglages, compte racheté 3 ans (run_propfirm_fp_custom.py) | choisi sur 2011-2018 : éval 3 % à 2 R, financé 1,25 % à 2 R, retraits à la demande ; 2019-2023 médiane +72,7 k$, 5e c. +56,0 k$, pire +49,8 k$ (plan FTMO +59,5 k$) ; protection avant retrait nuisible
- [2026-11-01] query | Métriques complètes FTMO et FundingPips, réglage 0,1 × perte max contre plan FTMO (run_propfirm_metrics.py) | EV par éval meilleure à 0,1 (FTMO +16,6 k$, FP +23,5 k$) mais compte racheté 3 ans meilleur avec le plan : FTMO +73,1 k$ médiane (pire +43,7 k$) contre +31,2 k$, FP +61,6 k$ contre +43,8 k$
- [2026-10-31] query | 10 prop firms (FTMO, STF, FundedNext, FundingPips, The5ers, Topstep, Apex, MFFU, Tradeify, Lucid), règles relevées sur les sites, grille risque × rr, choix 2011-2018 (run_propfirm_multi.py) | EV OOS 2019-2025 : FundingPips +12,1 k$, FTMO +7,6 k$, STF +6,9 k$, FundedNext +6,1 k$, The5ers +0,9 k$, futures 50K +0,2 à +0,5 k$, Topstep −53 $ ; risque bas (k 0,1) meilleur sauf Apex
- [2026-10-31] query | Plan « 2 coups » LucidFlex 50K, DLL OFF + 50 %, 130 $ (run_propfirm_lucid_plan.py, règles relues sur support.lucidtrading.com) | passage 34,5 % ; EV +66 $ (1 payout) / +234 $ (cycle répété) ; sans edge +32 / +147 $ ; rachat permanent 1 an +3,7 k$ médiane, pire −5,2 k$, ~60 évals/an
- [2026-10-31] query | Plan prop firm refait chez Smart Trader Funds, challenge 1 Phase (run_propfirm_stf.py, règles lues sur smartraderfunds.com) | position gardée pendant les annonces 8:30 : EV −62 $ (10k) / +148 $ (100k) ; à plat à 8:19 : +390 $ / +4 512 $ (FTMO +1 009 / +10 408) ; 1×10k → 100k au 95e centile +2,8 k$ à 3 ans (FTMO +54,9 k$) ; 1×100k d'emblée +44,7 k$ médiane, pire +16,9 k$
- [2026-10-31] query | Variante F (1→2→3×10k puis 100k) : délai jusqu'au premier achat d'une éval 100k (run_propfirm_variants.py) | moyenne ~18 mois (379 nuits), médiane 375, 25e-75e centile 281-466 nuits, 90e 533, 3 départs sur 612 sans 100k en 3 ans

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
