---
type: hot
updated: 2026-11-22 21:02
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 940** (source : [[reports/fx_balance_report]])
- Dernier pré-enregistrement : n° 31 ([[PREREGISTRATION_31]])
- Idées abandonnées au registre : 54 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-22

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/ml-anomalies\|Machine learning sur les anomalies que les filtres classiques n'ont pas améliorées]] | active | 1er essai (filtre binaire sur mom) rejeté ; autres candidates à faire |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-22] research | Bande de bruit : 5 textes intégraux lus (Beat the Market v. 22/09/2025 avec FAQ, Chuk 7609644, Paz 7290621, Delgado 7323419, Maróy 5095349) ; fiches corrigées, notes dans wiki/experiments/m2-bande-bruit-nq | Notre m2_noise n'exige pas le VWAP à l'entrée (le code des auteurs si) ; période ancienne faible partout ; faiblesse depuis sept. 2025 sur SPY ; FAQ : 33 futures, Sharpe moyen 0,60, Nasdaq 1,23 ; Maróy = surapprentissage ; aucun calcul
- [2026-11-22] prereg | N° 31 : ORB 30 min de Subhani le vendredi sur NQ (A sans objectif, B objectif 2R), réserve 2010-06 → 2015-12, hors protocole (B1 non franchie, demandé par l'utilisateur), commité avant calcul (c7fb825), une exécution ; compteur 2 079 → 2 085 | ❌ C1 et C3 pour A et B : +0,041 R (t 0,52), +0,038 R (t 0,54), Holm 0,59 ; placebo : vendredi au niveau du jeudi ; rejet, réserve consommée, phénomène annoté « contredit »
- [2026-11-22] experiment | ORB 30 min NQ lundi-jeudi : clôture au-delà de la borne (1 et 5 min), heure de cassure, ordres limite sur les bords ; grille commitée (dd00ed2), 2 trades vérifiés à la main, compteur 2 073 → 2 079 | ❌ B1 : tout entre −0,024 et +0,022 R ; ligne au registre
- [2026-11-22] experiment | ORB 30 min NQ lundi-jeudi, régime RSI 5 jours (gamma, Zarattini-Aziz-Barbon 2024) : V1 filtre, V2 cassure/réintégration ; grille commitée (99a2573), 2 réintégrations vérifiées à la main, compteur 2 071 → 2 073 | ❌ B1 : V1 +0,018 R (t 0,48), V2 +0,006 R ; aucune pente par quintile de RSI ; ligne au registre
- [2026-11-22] decision | ORB 30 min NQ : réserve 2010-06 → 2015-12 gardée en attente (décision de l'utilisateur, d'autres papiers pourraient aider les autres jours) | règles de réserve et de famille (N = 73) écrites dans wiki/experiments/orb30-jours-semaine ; prochaine action ajoutée à hot.md
- [2026-11-22] experiment | ORB 30 min NQ lundi-jeudi, biais EMA 20/50 multi-unités + réintégration (idée de l'utilisateur), 13 variantes ; grille commitée (d6cf9d3), bug de sens corrigé après vérification manuelle, exploration 2016-2026, compteur 2 058 → 2 071 | ❌ B1 : meilleure +0,045 R (t 1,40) contre +0,015 sans biais ; stop mèche négatif ; ligne au registre
- [2026-11-22] experiment | ORB 30 min NQ lundi-jeudi objectif 2R, conditions C1 (range étroit), C2 (NR7), C3 (annonces) ; grille commitée (d04655c), exploration 2016-2026, compteur 2 055 → 2 058 | ❌ B1 : base +0,011 R, meilleure C2 +0,044 R (t 0,76) ; seul le vendredi marche ; ligne au registre
- [2026-11-22] experiment | ORB 30 min de Subhani avec objectif 2R / 3R (NQ, ES, YM × vendredi, tous les jours) ; grille commitée (4d51084), exploration 2016-2026, compteur 2 043 → 2 055 | Aucun gain : NQ vendredi +0,164 R (2R et 3R) contre +0,190 sans objectif ; ❌ B1 ; Sharpe du rapport précédent corrigé (≈ 1,04 par an, pas 2,33)

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- **Vrais comptes FTMO en éval depuis le 2026-11-14** : A = compte 511480419 (FTMO-Server), B = 541521340 (FTMO-Server4), 10 000 $ chacun, bascule automatique faite (démo archivée dans `live/etat/archive/`). 1er trade réel : mom SL le 15/11 (A éval −2,50 %, B 0 %) ; relire le journal (`git fetch origin vps-journal`). Toujours en attente de la réponse du support FTMO (A + B long la même nuit, voir [[live/README]]).
- **Plan FTMO retenu (2026-11-04)** : compte A = mom, compte B = 3n + M2, règle des annonces + cible + attente, éval 2,5 % / financé 1 %, scaling 10k → 400k ; détail dans [[wiki/experiments/propfirm-ftmo-option]] (section « Plan retenu »).
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
- **N° 28 (short yen en session US)** : aucun calcul sur le yen après le 2026-08-28 avant la lecture L1 du 2028-02-29 (acheter alors 6J.v.0 Databento avec NQ), puis `uv run python run_prereg28.py --lecture 2028-02-29`.
<!-- NEXT-ACTIONS:END -->
