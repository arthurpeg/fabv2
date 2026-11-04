---
type: hot
updated: 2026-11-04 13:38
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

- [2026-11-04] query | Conditions de reward FTMO 1-Step relues sur ftmo.com (Trading Objectives, FAQ reward) et rejeu de septembre avec les règles exactes (run_ftmo_septembre.py, reports/ftmo_septembre_report.md) | meilleur jour ≤ 50 % du gain net pour les comptes commandés depuis le 12/10/2026 (= simulateur), ≤ 50 % des seuls jours gagnants avant (Legacy) ; reward dès le 14e jour après le 1er trade ; départ 01/09 en Legacy : reward 1,55 % le 28/09, net +68 $ / +998 $ ; en Consistency : 0 reward
- [2026-11-04] query | Correction des simulations FTMO à liste de trades : objectif d'éval ramené au reste à faire avec le MFE de chaque trade (build_mfe_mom.py, run_propfirm_combo.simule, run_propfirm_trio / mix / eval_rapide corrigés ; reports/propfirm_correction_reste_report.md) | passage +1 à +7 points (mom seul 2016-26 : 43,6 → 50,7 % ; trio 59,8 → 64,7 % ; 3n + M2 60,5 → 65,5 %) ; EV par tentative +3 à +17 % ; classements inchangés ; vérification 2019-26 : trio 61 % en 19 séances, mom 2 % + M2 0,5 % 57,5 % en 15
- [2026-11-04] query | FTMO septembre, correction (run_ftmo_septembre.py, reports/ftmo_septembre_report.md) : coût CFD 0,02-0,035 R par trade (TP = 4,75-4,88 % au lieu de 5 %) ; objectif d'éval ramené au reste à faire avec le MFE de chaque nuit | départ 01/09 validé le 14/09 au lieu du 18/09 (la nuit du 14/09 monte à +0,88 R, il fallait 0,38 R) ; 12 départs sur 21 valident au lieu de 9 ; toujours 0 reward au 03/11 ; les simulations à bibliothèque de trades (TradeLib) gardaient l'objectif fixe en éval : passage un peu sous-estimé
- [2026-11-04] query | FTMO 1-Step avec mom, départ en septembre 2026, rejeu jour par jour sur les vraies nuits jusqu'au 03/11 (run_ftmo_septembre.py, reports/ftmo_septembre_report.md, descriptif, fenêtre vue du holdout) ; h1_mom de run_holdout_anticipe.py paramétré (tp, cost) | départ 01/09 : éval validée le 18/09, financé perdu le 03/11 sans reward ; 21 départs de septembre : 0 reward, −174 à −348 $ par 10k ; mom −1,1 R brut sur 44 nuits, 61 % de SL
- [2026-11-04] query | Performances de mom (règle NQ de nuit, compte 20:00) du 2011-07 au 2026-11-03, trades vectorbt existants + fenêtre vue du holdout (run_mom_perf.py, results/mom_perf/, descriptif) ; correction du R de H1 dans run_holdout_anticipe.py (ATR à 20:00, pas 19:59) | 3 831 nuits, +0,087 R/nuit, 21,7 R/an, Sharpe 1,01, max DD −25,4 R, t 4,0 ; 2011-15 +0,115 R, 2016-24 +0,072, 2025-08/2026 +0,102, fenêtre vue −0,023 (44 nuits) ; années négatives : 2011 (−1,0 R, demi-année) et 2022 (−1,7 R)
- [2026-11-04] query | FTMO 1-Step, plan d'éval × plan financé (mom seul / trio ; run_propfirm_mix.py, reports/propfirm_mix_report.md, exploratoire, hors compteur) | 2016-2026 : mom → trio +1 451 $ / tentative 10k, +1 518 $ par mois 100k ; trio → trio +2 037 $ / +1 476 $ ; mom → mom +617 $ / +1 978 $ ; même ordre sur 2011-2015 et 2019-2026 ; le plan financé compte plus que celui de l'éval
- [2026-11-04] query | Évals FTMO plus rapides : grille de 384 plans 3n / mom / M2 (perte du jour ≤ 2,5 %), choix sur 2011-2018, vérification sur 2019-2026 (run_propfirm_eval_rapide.py, reports/propfirm_eval_rapide_report.md, exploratoire, hors compteur) | aucun plan plus rapide à passage égal : trio 58 % en 21 séances (2019-26) ; choisi A 2,5/2,0/0 : 61 % → 48 % en ≈ 16 séances ; mom seul 2,5 % : 42 % en 9,5 séances ; vitesse = risque, pas edge
- [2026-11-04] query | FTMO 1-Step, plan à trois : 3n à plein risque si signal, sinon mom r/2 + M2 r/2 (éval 2,5 %, financé 1 %, objectif 2 R ; run_propfirm_trio.py, reports/propfirm_trio_report.md, exploratoire, hors compteur) | 2016-2026 : +2 020 $ / +20 519 $ par tentative, +1 478 $ par mois d'emplacement 100k (3n + M2 +2 618 $ / +1 446 $ ; mom seul +625 $ / +1 989 $) ; 2011-2015 : +3 362 $, +1 616 $ par mois (mom seul +1 786 $, +3 397 $ par mois) ; le trio retire à mom ses meilleures nuits (celles où 3n est long)

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
