---
type: hot
updated: 2026-11-04 15:40
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

- [2026-11-04] query | Deux comptes FTMO 10k (A mom, B 3n + M2), un seul chemin du 2011-07-01 au 2026-11-03, règle des annonces + cible + attente (run_ftmo_deux_comptes_historique.py, reports/ftmo_deux_comptes_historique_report.md, exploratoire, hors compteur) | net +68 562 $ (+4 469 $/an), 52 évals, 217 rewards, aucune année négative, max DD de trésorerie −435 $, pire série sans reward 5 évals (A) / 3 (B), corrélation P&L +0,24, flux mensuels +0,01
- [2026-11-04] query | Deux comptes FTMO (A mom, B 3n + M2) avec la règle des annonces (build_news_trades.py : mom coupé à 8:19 les jours NFP / CPI / PIB, M2 à 13:55 les jours de Fed ; dates sept.-oct. 2026 relevées sur BLS et Fed, PIB T3 supposé le 29/10) et la politique cible + attente ; horloge du reward corrigée (jours de bourse, tradés ou non) (run_ftmo_deux_comptes.py, reports/ftmo_deux_comptes_report.md) | 12 mois : +4 082 $ sans la règle, +3 843 $ avec, +3 864 $ avec cible + attente (10e c. +2 473 $, 12,9 rewards par an) ; départ 01/09/2026 : +598 / +685 / +740 $
- [2026-11-04] query | Deux comptes FTMO 10k en même temps : A = mom, B = 3n + M2 (M2 si 3n sort ni au SL ni au TP, taille bornant la journée à −r / +2r) ; éval 2,5 % / financé 1 %, objectif 2 R ramené au reste à faire en éval, règles FTMO actuelles (run_ftmo_deux_comptes.py, reports/ftmo_deux_comptes_report.md, exploratoire, hors compteur) | 721 départs 2011-2025, 12 mois : net moyen +4 060 $ (A +2 469, B +1 591), 10e c. +2 096 $, aucun départ perdant, pire creux −782 $ ; départ réel 01/09/2026 : A −174 $, B +771 $ (2 rewards en octobre), total +598 $
- [2026-11-04] query | Contrôle sans edge de la politique « cible + attente » (run_ftmo_payout_policy_sans_edge.py, reports/ftmo_payout_policy_report.md, exploratoire, hors compteur) ; page anglaise complétée avec les métriques sans edge et mom (reports/propfirm_ftmo_overview.html) | sans edge 2016-26 : +107 → +133 $ par tentative 10k, +798 → +886 $ par mois 100k ; 2011-15 : +64 → +86 $ ; la politique gagne aussi sans edge (effet de contrat) ; mom en cible + attente ×6,9 par tentative, ×2,5 par mois
- [2026-11-04] doc | Page HTML en anglais présentant la branche propfirm-ftmo, sans les règles de trading (reports/propfirm_ftmo_overview.html) | contrat vu comme option, règles FTMO modélisées, simulateur, enseignements, limites
- [2026-11-04] query | Compte financé FTMO avec mom : viser juste ce qui manque pour la règle des 50 % puis attendre le 14e jour (run_ftmo_payout_policy.py, reports/ftmo_payout_policy_report.md, exploratoire, hors compteur) | septembre 2026 réel (Consistency) : départ 01/09 → objectif réduit le 22/09 (+0,14 %), reward 3,53 % le 28/09, au lieu de 0 ; historique 2016-26 : cible + attente +912 $ contre +707 $ par tentative 10k, +2 201 $ contre +2 044 $ par mois ; 2011-15 : neutre par tentative, −11 % par mois ; l'attente fait l'essentiel
- [2026-11-04] query | Conditions de reward FTMO 1-Step relues sur ftmo.com (Trading Objectives, FAQ reward) et rejeu de septembre avec les règles exactes (run_ftmo_septembre.py, reports/ftmo_septembre_report.md) | meilleur jour ≤ 50 % du gain net pour les comptes commandés depuis le 12/10/2026 (= simulateur), ≤ 50 % des seuls jours gagnants avant (Legacy) ; reward dès le 14e jour après le 1er trade ; départ 01/09 en Legacy : reward 1,55 % le 28/09, net +68 $ / +998 $ ; en Consistency : 0 reward
- [2026-11-04] query | Correction des simulations FTMO à liste de trades : objectif d'éval ramené au reste à faire avec le MFE de chaque trade (build_mfe_mom.py, run_propfirm_combo.simule, run_propfirm_trio / mix / eval_rapide corrigés ; reports/propfirm_correction_reste_report.md) | passage +1 à +7 points (mom seul 2016-26 : 43,6 → 50,7 % ; trio 59,8 → 64,7 % ; 3n + M2 60,5 → 65,5 %) ; EV par tentative +3 à +17 % ; classements inchangés ; vérification 2019-26 : trio 61 % en 19 séances, mom 2 % + M2 0,5 % 57,5 % en 15

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
