---
type: hot
updated: 2026-11-01 21:47
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 493** (source : [[reports/nq_sessions_corr_report]])
- Dernier pré-enregistrement : n° 19 ([[PREREGISTRATION_19]])
- Idées abandonnées au registre : 27 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-01

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-01] experiment | Corrélation entre sessions NQ Asie → Europe → US, coupe à l'ouverture suivante (A) ou à la vraie clôture (B) (run_nq_sessions_corr.py, exploratoire, 2010-2026, compteur 1 501) | rejeté : Europe → US r −0,003, nuit → US r 0,000 ; Asie → Europe r −0,05 (retournement, éteint depuis 2023) ; Europe jusqu'à 16:30 Ldn → reste US r +0,066 mais porté par 9:30-11:30 NY (momentum intraday US), pas par l'Europe
- [2026-11-01] experiment | Règle NQ de nuit, SL au bord du range 17:00→20:00 au lieu de 2 ATR, TP 1 à 2,5 R (run_nq_nuit_sl_range.py, exploratoire, compteur 1 493) | rejeté : net −0,10 (TP 1 R) à −0,03 R/trade (TP 2,5 R), brut +0,03 à +0,10 ; stop médian 0,86 ATR, 60 % de SL ; réf. +0,088 R, Sharpe 1,00
- [2026-11-01] query | Quantification de l'edge de la règle NQ de nuit au coût réel (2011-07 → 2026-08) | +0,076 R/trade [+0,033 ; +0,116], t 3,4, PF 1,13, 43 % gagnants, payoff 1,52, Kelly 5 % ; ≈ 57 $/trade NQ (160 $ en 2024-26) ; DSR 0,52 avec N = 1 485 contre PSR 0,99 sur le test unique 2011-2015
- [2026-11-01] query | Correction FTMO : règle des annonces en financé (±2 min, stop/objectif compris) ajoutée, sortie à 8:19 (run_propfirm_multi, metrics, ftmo_custom) | plan FTMO EV +9,9 k$ (contre +11,1 k$), compte racheté 3 ans +63,2 k$ (contre +73,1 k$) ; sur mesure 2019-2023 +59,3 k$ (choix 1,5 R) / +66,3 k$ (2 R) ; anciens chiffres FTMO ≈ 10 % trop optimistes
- [2026-11-01] query | FTMO et FundingPips sur mesure avec financé ≤ 1 % et éval ≤ 2,5 % (filtre des grilles) | FTMO éval 2,5 % à 2 R, financé 1 % à 2,5 R, protection +4 % : 2019-2023 médiane +69,2 k$, pire +50,1 k$ (plan +48,9 k$) ; FundingPips +56,9 k$ (2 semaines : +49,4 k$)
- [2026-11-01] query | FTMO 1-Step sur mesure + plafond 2,5 % par trade (run_propfirm_ftmo_custom.py ; FundingPips refiltré) | 2019-2023, compte racheté 3 ans : FTMO éval 2 % à 2 R, financé 2,5 % à 1,5 R médiane +92,9 k$ (pire +30,2 k$, 31 évals, 9,9 k$ sortis au max) contre plan +48,9 k$ ; FundingPips éval 2 % à 3 R, financé 1,25 % à 2 R +67,8 k$
- [2026-11-01] query | FundingPips 1 Step Flex, gestion du risque sur mesure, 3 600 réglages, compte racheté 3 ans (run_propfirm_fp_custom.py) | choisi sur 2011-2018 : éval 3 % à 2 R, financé 1,25 % à 2 R, retraits à la demande ; 2019-2023 médiane +72,7 k$, 5e c. +56,0 k$, pire +49,8 k$ (plan FTMO +59,5 k$) ; protection avant retrait nuisible
- [2026-11-01] query | Métriques complètes FTMO et FundingPips, réglage 0,1 × perte max contre plan FTMO (run_propfirm_metrics.py) | EV par éval meilleure à 0,1 (FTMO +16,6 k$, FP +23,5 k$) mais compte racheté 3 ans meilleur avec le plan : FTMO +73,1 k$ médiane (pire +43,7 k$) contre +31,2 k$, FP +61,6 k$ contre +43,8 k$

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
