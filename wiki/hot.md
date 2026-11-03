---
type: hot
updated: 2026-11-03 23:20
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 738** (source : [[reports/holdout_anticipe_report]])
- Dernier pré-enregistrement : n° 26 ([[PREREGISTRATION_26]])
- Idées abandonnées au registre : 35 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-03

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-03] query | N° 26 avenant A (commit 9f87d69) : lecture anticipée exploratoire du holdout 2026-08-31 → 2026-11-03, Databento + LSE raboutés (run_holdout_anticipe.py, reports/holdout_anticipe_report.md), compteur 1 738 → 1 742 ; holdout officiel décalé au 2026-11-04 | sans verdict : H1 mom −0,023 R/nuit (44 nuits, toutes longues) ; H2 M2 +716 $/trade sur 9 trades (C +625 $) ; H3 3n SL +0,379 R sur 23 trades (p 0,087) ; H4 rebond +19,8 bps d'écart sur 11 nuits (p 0,13) ; aucun roulement visible dans la série LSE en septembre (à vérifier avec Databento)
- [2026-11-03] prereg | N° 26 : holdout NQ post-2026-08-28 (PREREGISTRATION_26 commit f2e4725), compteur 1 734 → 1 738 : H1 mom, H2 M2 (EMA 9:30), H3 3n SL, H4 rebond r3 ≤ −50 bps ; lectures 2028-02-29 et 2029-08-31 (succès si z ≥ 3,0, Haybittle-Peto), verdict 2031-08-29 (Holm) ; Databento acheté à chaque lecture, LSE en repli | aucun calcul sur le holdout avant 2028-02-29 ; puissance à 3 ans 28 à 52 % selon la règle
- [2026-11-03] ingest | NQ 1 min London Strategic Edge (symbole NASDAQ100, marché futures gratuit) du 2026-01-01 au 2026-11-03 (fetch_lse.py → cache/lse/NQ_lse_1m.parquet), contient le holdout post-2026-08-28 NON ouvert (couverture seulement) | 297 453 barres ; contre Databento jusqu'au 2026-08-28 : 1 tick d'écart médian, roulements à d'autres dates (03-18, 06-14 → 16) ; holdout : 47 séances RTH, trous le 2026-10-12 (RTH 86 barres) et le 2026-10-16 9:30 → 9:58 ; trop court pour tester M2 (~18 trades)
- [2026-11-03] query | EMA 9:30 / M2 prolongé sur NQ 2013-2015 et 2010-2015, ES et YM (run_ema930_2013_2015.py, reports/prereg25_report.md, descriptif, hors compteur : 2013-2015 vu par le post) | 2013-2015 : 7,6 bps/trade, Sharpe 0,83, t 1,34, choix des jours p 0,07 ; 2010-2015 : 6,4 bps, Sharpe 0,65, t 1,59 (brut / σ t 2,2 ; ES t 2,0) ; environ moitié moins que 2016-2024 ; stop 4 ATR nuisible en 2013-15 ; verdict du n° 25 inchangé
- [2026-11-03] query | N° 25, diagnostic après coup : niveau de prix et normalisation (reports/prereg25_report.md, dernière section) | bps = déjà % du prix ; le coût de 15 $ pèse 3,3 bps en 2010-12 contre 0,8 ; brut 8,5 contre 15,9 bps à volatilité égale (σ 90 contre 100 bps) ; normalisé par σ 0,061 contre 0,165, en R brut 0,057 contre 0,245 : la normalisation ne sauve pas M2
- [2026-11-03] prereg | N° 25 : stratégie transmise EMA 9:30 / M2 hors échantillon NQ 2010-06 → 2012-12, ES et YM rapportés (PREREGISTRATION_25 commit f130eeb, run_prereg25.py, reports/prereg25_report.md), compteur 1 726 → 1 734 | ÉCHEC : M2 +20,7 $/trade (5,2 bps), p 0,19 ; jours M2 − jours exclus +4,2 $, p 0,45 ; moitiés positives ; M2 + stop +0,066 R (t 0,91) ; ES p 0,039, YM p 0,054 avant correction
- [2026-11-03] query | EMA 9:30, M2 + stop 4 × ATR M15 en R (1 R = distance du stop ; reports/nq_ema930_vbt_report.md, results/nq_ema930/m2_stop_R.csv) | IS +0,200 R/trade, 19,6 R/an, Sharpe 1,29, DD −18,5 R, t 4,06 ; OOS +0,241 R, 23,9 R/an, Sharpe 1,79, DD −12,5 R ; toutes les années positives en R sauf 2017 (−2,8 R)
- [2026-11-03] query | EMA 9:30 / M2 : backtest vectorbt comparé au rapport d'origine (artefact transmis ; reports/nq_ema930_vbt_report.md) | sans stop identique au dollar près (C, D, M2, M2 + taille, 4 périodes) ; avec stop +0,01 à +0,03 de Sharpe (2 stops dans la barre d'entrée) ; seuils du post choisis sur 2013-2024 : seul 2010-06 → 2012-12 est hors échantillon

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
