---
type: hot
updated: 2026-11-22 14:53
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 937** (source : [[reports/yen_derive_ab_report]])
- Dernier pré-enregistrement : n° 29 ([[PREREGISTRATION_29]])
- Idées abandonnées au registre : 43 ([[wiki/Failed Ideas/ledger]])
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

- [2026-11-22] schema | Version papier façon SSRN de la recherche overnight : reports/overnight_drift_paper.html + .pdf (11 pages A4, résumé, JEL, 6 tableaux + annexe A1, 22 références ; auteur Arthur Pegliasco), réécrite depuis reports/overnight_research_en.pdf du 2026-11-06 sans nom du dépôt ni chemins internes | aucun calcul, chiffres repris du PDF du 6 novembre (compteur 1 742 à cette date)
- [2026-11-22] schema | Version papier façon SSRN de l'étude de convexité prop firm : reports/propfirm_convexity_paper.html + .pdf (9 pages A4, résumé, JEL, 7 tableaux, figure, références ; auteur Arthur Pegliasco), remplace propfirm_ftmo_overview.pdf | aucun calcul, chiffres repris de la présentation
- [2026-11-22] schema | Présentation reports/propfirm_ftmo_overview.html préparée pour publication : nom du dépôt, branches et chemins de fichiers retirés, auteur Arthur Pegliasco + e-mail ajoutés, styles d'impression, export PDF reports/propfirm_ftmo_overview.pdf (7 pages A4) | aucun calcul
- [2026-11-22] schema | Présentation reports/propfirm_ftmo_overview.html recentrée à la demande de l'utilisateur sur les seules études de convexité du payoff : retrait du bot, des vrais comptes, de la règle d'arrêt de mom, du scaling ; section 8 = deux comptes sur signaux différents, Monte-Carlo 3 ans (net > 0 dans tous les chemins même edge ÷ 2) | aucun calcul
- [2026-11-22] schema | Présentation anglaise reports/propfirm_ftmo_overview.html mise à jour (sections 8 plan à deux comptes + scaling, 9 bot et vrais comptes au 20/11 + règle d'arrêt de mom, réserves : consigne du support FTMO, spread réel 1,95 pt, règle des fermetures, holdout ; règles anti-hedging / fermetures / plafond 400k au tableau des règles) | aucun calcul, chiffres repris des rapports (anti-hedging appliqué quand disponible) et du journal vps-journal ; signaux toujours non décrits
- [2026-11-22] schema | Nouveau registre wiki/book-multi-strategies.md : règles à avantage mesuré mais inadaptées au format prop firm (éval en < 1 mois), candidates pour un book diversifié ; lien dans l'index | 8 lignes : short yen n° 28, R4 n° 29, dernière heure / décile haut du yen, reprise de l'or, or 16:00 → 19:00, enchère Xetra du DAX, rebond de nuit après forte baisse, sessions FX GBP/CAD/CHF ; aucun calcul, compteur inchangé 1 937
- [2026-11-21] experiment | Dérive du yen concentrée pour la prop firm (fiche wiki/experiments/yen-derive-concentree, réserve par question 6J 2023-07-01 → 2026-08-28 déclarée et non ouverte) : grille A (18 tranches de 30 min × tous/R4, 24 fenêtres de 1 à 3 h × tous/R4) + B (déciles et 4 seuils glissants de la hausse du yen à 3 jours), figée avant calcul (run_yen_derive_ab.py, commit 068ce8a), exploration 6J 2016-01 → 2023-06, compteur 1 839 → 1 937 | ❌ critère gain / bruit ≥ 0,15 : A meilleure fenêtre R4 15:00 → 16:55 à 0,051 (< 0,081 pour 11:00 → 16:55 ; rien avant 11:00 ; 16:00 → 16:55 ≈ moitié du brut, t 4,3, mais −0,1 net) ; B décile haut +5,5 bp net (0,18, t 3,0), seuil q 0,8 à 0,134 (+3,6 bp, 17 % des jours), DSR 0,40 à N = 140 ; ligne au registre
- [2026-11-21] query | Short yen filtré R4, SL k × ATR M15 (k = 2-5) avec TP 2R et 3R (run_jpy_us_r4_m15_tp.py, 8 essais figés avant calcul, 6J 2017-01-30 → 2026-08-28 déjà vu), compteur 1 831 → 1 839 | meilleur 4 ATR M15 + TP 2R +0,040 R (n° 29 : +0,041) ; TP touché 0,3-8 %, effet ±0,005 R ; SL 2 ATR M15 + TP 2R +0,017 R, creux −37 R ; seuil d'avenant +0,046 non atteint, n° 29 inchangé

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
<!-- NEXT-ACTIONS:END -->
