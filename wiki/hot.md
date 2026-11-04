---
type: hot
updated: 2026-11-04 12:01
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 738** (source : [[reports/holdout_anticipe_report]])
- Dernier pré-enregistrement : n° 26 ([[PREREGISTRATION_26]])
- Idées abandonnées au registre : 35 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-04

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-04] query | FTMO 1-Step, plan d'éval × plan financé (mom seul / trio ; run_propfirm_mix.py, reports/propfirm_mix_report.md, exploratoire, hors compteur) | 2016-2026 : mom → trio +1 451 $ / tentative 10k, +1 518 $ par mois 100k ; trio → trio +2 037 $ / +1 476 $ ; mom → mom +617 $ / +1 978 $ ; même ordre sur 2011-2015 et 2019-2026 ; le plan financé compte plus que celui de l'éval
- [2026-11-04] query | Évals FTMO plus rapides : grille de 384 plans 3n / mom / M2 (perte du jour ≤ 2,5 %), choix sur 2011-2018, vérification sur 2019-2026 (run_propfirm_eval_rapide.py, reports/propfirm_eval_rapide_report.md, exploratoire, hors compteur) | aucun plan plus rapide à passage égal : trio 58 % en 21 séances (2019-26) ; choisi A 2,5/2,0/0 : 61 % → 48 % en ≈ 16 séances ; mom seul 2,5 % : 42 % en 9,5 séances ; vitesse = risque, pas edge
- [2026-11-04] query | FTMO 1-Step, plan à trois : 3n à plein risque si signal, sinon mom r/2 + M2 r/2 (éval 2,5 %, financé 1 %, objectif 2 R ; run_propfirm_trio.py, reports/propfirm_trio_report.md, exploratoire, hors compteur) | 2016-2026 : +2 020 $ / +20 519 $ par tentative, +1 478 $ par mois d'emplacement 100k (3n + M2 +2 618 $ / +1 446 $ ; mom seul +625 $ / +1 989 $) ; 2011-2015 : +3 362 $, +1 616 $ par mois (mom seul +1 786 $, +3 397 $ par mois) ; le trio retire à mom ses meilleures nuits (celles où 3n est long)
- [2026-11-04] query | FTMO 1-Step avec 3n + M2 combinées, un trade par jour, objectif 2 R, éval 2,5 % / financé 1 % (run_propfirm_combo.py, reports/propfirm_combo_report.md, exploratoire, hors compteur) | 2016-2026 : EV +2 123 $ (10k) / +21 546 $ (100k), passage 60 %, financé 37 %, +1 477 $ par mois d'emplacement 100k (3n seul +1 159, M2 seul +1 164, mom TP 2 R +1 989) ; 2010-2015 : +904 $ / +9 363 $ (sans edge +47 $) ; règle des annonces non modélisée pour M2
- [2026-11-03] query | Combinaison 3n SL + M2 + stop, au plus 1 trade par jour avec priorité à la nuit (run_combo_3n_m2.py, reports/combo_3n_m2_report.md, descriptif, hors compteur) | corrélation journalière ≈ 0 ; 2016-24 : max 1/jour 24,9 R/an, Sharpe 1,59 contre 33,0 R/an, Sharpe 1,80 en prenant tout (M2 sautés +0,20 R chacun), même DD −18 R ; pire jour −1,2 contre −2,1 R ; 2010-15 : 0,17 contre 0,58 ; combinaison à pré-enregistrer avant usage
- [2026-11-03] query | Lecture anticipée du holdout (avenant A), variante M2 + stop 4 × ATR M15 (reports/holdout_anticipe_report.md) | 9 trades, 1 stoppé (2026-10-29 short, −1 R au lieu de −0,55 R) ; +4 331 $ (+481 $/trade, t 1,75) contre +6 440 $ sans stop ; E[R] +0,21 ; sans verdict
- [2026-11-03] query | N° 26 avenant A (commit 9f87d69) : lecture anticipée exploratoire du holdout 2026-08-31 → 2026-11-03, Databento + LSE raboutés (run_holdout_anticipe.py, reports/holdout_anticipe_report.md), compteur 1 738 → 1 742 ; holdout officiel décalé au 2026-11-04 | sans verdict : H1 mom −0,023 R/nuit (44 nuits, toutes longues) ; H2 M2 +716 $/trade sur 9 trades (C +625 $) ; H3 3n SL +0,379 R sur 23 trades (p 0,087) ; H4 rebond +19,8 bps d'écart sur 11 nuits (p 0,13) ; aucun roulement visible dans la série LSE en septembre (à vérifier avec Databento)
- [2026-11-03] prereg | N° 26 : holdout NQ post-2026-08-28 (PREREGISTRATION_26 commit f2e4725), compteur 1 734 → 1 738 : H1 mom, H2 M2 (EMA 9:30), H3 3n SL, H4 rebond r3 ≤ −50 bps ; lectures 2028-02-29 et 2029-08-31 (succès si z ≥ 3,0, Haybittle-Peto), verdict 2031-08-29 (Holm) ; Databento acheté à chaque lecture, LSE en repli | aucun calcul sur le holdout avant 2028-02-29 ; puissance à 3 ans 28 à 52 % selon la règle

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
