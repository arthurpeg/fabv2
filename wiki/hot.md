---
type: hot
updated: 2026-11-22 19:20
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **2 071** (source : [[reports/orb30_biais_report]])
- Dernier pré-enregistrement : n° 30 ([[PREREGISTRATION_30]])
- Idées abandonnées au registre : 51 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-22

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/ml-anomalies\|Machine learning sur les anomalies que les filtres classiques n'ont pas améliorées]] | active | 1er essai (filtre binaire sur mom) rejeté ; autres candidates à faire |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/orb30-jours-semaine\|ORB 30 minutes, stop à une largeur de range, par jour de la semaine (Subhani 2026) sur NQ, ES, YM]] | active | NQ vendredi réplique le papier (+0,19 R, t 3,50) mais ❌ B1 (DSR) ; lundi-jeudi rien ; réserve 2010-2015 gardée en attente |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-22] decision | ORB 30 min NQ : réserve 2010-06 → 2015-12 gardée en attente (décision de l'utilisateur, d'autres papiers pourraient aider les autres jours) | règles de réserve et de famille (N = 73) écrites dans wiki/experiments/orb30-jours-semaine ; prochaine action ajoutée à hot.md
- [2026-11-22] experiment | ORB 30 min NQ lundi-jeudi, biais EMA 20/50 multi-unités + réintégration (idée de l'utilisateur), 13 variantes ; grille commitée (d6cf9d3), bug de sens corrigé après vérification manuelle, exploration 2016-2026, compteur 2 058 → 2 071 | ❌ B1 : meilleure +0,045 R (t 1,40) contre +0,015 sans biais ; stop mèche négatif ; ligne au registre
- [2026-11-22] experiment | ORB 30 min NQ lundi-jeudi objectif 2R, conditions C1 (range étroit), C2 (NR7), C3 (annonces) ; grille commitée (d04655c), exploration 2016-2026, compteur 2 055 → 2 058 | ❌ B1 : base +0,011 R, meilleure C2 +0,044 R (t 0,76) ; seul le vendredi marche ; ligne au registre
- [2026-11-22] experiment | ORB 30 min de Subhani avec objectif 2R / 3R (NQ, ES, YM × vendredi, tous les jours) ; grille commitée (4d51084), exploration 2016-2026, compteur 2 043 → 2 055 | Aucun gain : NQ vendredi +0,164 R (2R et 3R) contre +0,190 sans objectif ; ❌ B1 ; Sharpe du rapport précédent corrigé (≈ 1,04 par an, pas 2,33)
- [2026-11-22] experiment | Étapes 0-1 de wiki/experiments/orb30-jours-semaine : ORB 30 min de Subhani, 6 calendriers × NQ, ES, YM ; réserve 2010-06 → 2015-12 déclarée, grille commitée (f40b125), exploration 2016-01 → 2026-08, compteur 2 025 → 2 043 | Réplique le papier (NQ vendredi sur sa période +0,219 R, t 3,34) ; NQ vendredi 2016-2026 +0,190 R, t 3,50, 10/11 années ; ❌ B1 sur le seul DSR (0,846, N 45) ; « À surveiller » ; réserve non lue
- [2026-11-22] research | Papier SSRN 7589980 (Subhani, ORB 30 min le vendredi) lu en entier (PDF fourni, 38 p., version du 15/11/2026) : fiche [18] de papiers_ssrn_orb_2026-11-22.md, recherche_causalite_intraday.md et wiki/research/litterature-intraday corrigés | Le résumé d'une version antérieure était faux : tous les vendredis, sans filtre d'annonce (rejeté) ; QQQ test 2024-2026 +0,338 R (t 2,54), complet t 3,05 ; DSR 0,999 (17 essais) ou 0,19-0,47 (239 essais) ; lundi-jeudi ≈ 0 ; entrée « sens de la bougie » essayée et rejetée par l'auteur
- [2026-11-22] prereg | N° 30 : règle de la 1ʳᵉ bougie NQ stop 0,5 ATR / 2R sur la réserve 2021-10 → 2026-08, hors protocole (B1 non franchie, demandé par l'utilisateur), commité avant calcul (bade69c), une exécution ; compteur 2 024 → 2 025 | ❌ C1 : +2,57 pts/trade, t 0,58, p 0,28 ; « toujours long » +2,61 ; rejet ; réserve NQ « sortie » consommée
- [2026-11-22] experiment | Filtres F1 (annonces 10:00/14:00), F2 (volume d'ouverture), F3 (corps de bougie) sur la règle NQ 1ʳᵉ bougie stop 0,5 ATR / 2R ; grille commitée (b97b69c), exploration 2010-06 → 2021-09, compteur 2 021 → 2 024 | ❌ B1 : F3 Sharpe 0,87, DSR 0,019 ; F1 porté par 2021 ; F2 inverse (t −2,55) ; réserve non lue

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- **Vrais comptes FTMO en éval depuis le 2026-11-14** : A = compte 511480419 (FTMO-Server), B = 541521340 (FTMO-Server4), 10 000 $ chacun, bascule automatique faite (démo archivée dans `live/etat/archive/`). 1er trade réel : mom SL le 15/11 (A éval −2,50 %, B 0 %) ; relire le journal (`git fetch origin vps-journal`). Toujours en attente de la réponse du support FTMO (A + B long la même nuit, voir [[live/README]]).
- **Plan FTMO retenu (2026-11-04)** : compte A = mom, compte B = 3n + M2, règle des annonces + cible + attente, éval 2,5 % / financé 1 %, scaling 10k → 400k ; détail dans [[wiki/experiments/propfirm-ftmo-option]] (section « Plan retenu »).
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- ~~Or : continuation 17:00 → 5:00 NY sur le reste du jour~~ : ❌ échec du n° 21 le 2026-11-21 (or au comptant 2003-2015, pente nulle), voir [[reports/prereg21_report]].
- **N° 28 (short yen en session US)** : aucun calcul sur le yen après le 2026-08-28 avant la lecture L1 du 2028-02-29 (acheter alors 6J.v.0 Databento avec NQ), puis `uv run python run_prereg28.py --lecture 2028-02-29`.
- **N° 29 (R4 + SL 2 ATR H1 sur le short yen)** : télécharger les ticks USDJPY 2003-05 → 2009-12 (Dukascopy, barres 1 min bid/ask), contrôle de qualité sans moyenne de rendement, puis `uv run python -X utf8 run_prereg29.py --spot <fichier>` une seule fois ; forward aux dates du n° 28 (`--lecture`).
- **ORB 30 min NQ (Subhani)** : le vendredi réplique le papier (+0,19 R, t 3,50 ; objectif 2R +0,164 R) mais B1 ratée sur le DSR ; lundi-jeudi rien (règle seule, C1-C3, biais EMA). Réserve 2010-06 → 2015-12 **gardée en attente** d'autres papiers pour les autres jours ; famille N = 73. Voir [[wiki/experiments/orb30-jours-semaine]].
<!-- NEXT-ACTIONS:END -->
