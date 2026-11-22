---
type: hot
updated: 2026-11-22 12:57
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 798** (source : [[reports/jpy_us_distribution_report]])
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

- [2026-11-22] schema | Nouveau registre wiki/book-multi-strategies.md : règles à avantage mesuré mais inadaptées au format prop firm (éval en < 1 mois), candidates pour un book diversifié ; lien dans l'index | 8 lignes : short yen n° 28, R4 n° 29, dernière heure / décile haut du yen, reprise de l'or, or 16:00 → 19:00, enchère Xetra du DAX, rebond de nuit après forte baisse, sessions FX GBP/CAD/CHF ; aucun calcul, compteur inchangé 1 937
- [2026-11-21] experiment | Dérive du yen concentrée pour la prop firm (fiche wiki/experiments/yen-derive-concentree, réserve par question 6J 2023-07-01 → 2026-08-28 déclarée et non ouverte) : grille A (18 tranches de 30 min × tous/R4, 24 fenêtres de 1 à 3 h × tous/R4) + B (déciles et 4 seuils glissants de la hausse du yen à 3 jours), figée avant calcul (run_yen_derive_ab.py, commit 068ce8a), exploration 6J 2016-01 → 2023-06, compteur 1 839 → 1 937 | ❌ critère gain / bruit ≥ 0,15 : A meilleure fenêtre R4 15:00 → 16:55 à 0,051 (< 0,081 pour 11:00 → 16:55 ; rien avant 11:00 ; 16:00 → 16:55 ≈ moitié du brut, t 4,3, mais −0,1 net) ; B décile haut +5,5 bp net (0,18, t 3,0), seuil q 0,8 à 0,134 (+3,6 bp, 17 % des jours), DSR 0,40 à N = 140 ; ligne au registre
- [2026-11-21] query | Short yen filtré R4, SL k × ATR M15 (k = 2-5) avec TP 2R et 3R (run_jpy_us_r4_m15_tp.py, 8 essais figés avant calcul, 6J 2017-01-30 → 2026-08-28 déjà vu), compteur 1 831 → 1 839 | meilleur 4 ATR M15 + TP 2R +0,040 R (n° 29 : +0,041) ; TP touché 0,3-8 %, effet ±0,005 R ; SL 2 ATR M15 + TP 2R +0,017 R, creux −37 R ; seuil d'avenant +0,046 non atteint, n° 29 inchangé
- [2026-11-21] query | Short yen filtré R4 avec SL k × ATR M15 sans TP, k = 2-5 (run_jpy_us_r4_m15.py, 4 essais figés avant calcul, 6J 2017-01-30 → 2026-08-28 déjà vu), compteur 1 827 → 1 831 | meilleur 4 ATR M15 (33 bp) +0,038 R contre +0,041 R pour 2 ATR H1 (n° 29) ; 2 ATR M15 (16,5 bp) +0,024 R, 32 % de SL, creux −34 R ; seuil d'avenant (+0,046 R) non atteint, n° 29 inchangé
- [2026-11-21] query | Short yen filtré R4, SL 2 ATR H1 avec TP 2R au lieu de 3R (run_jpy_us_r4_tp2.py, 1 essai figé avant calcul, 6J 2017-01-30 → 2026-08-28 déjà vu), compteur 1 826 → 1 827 | +0,043 R/trade (t NW 2,54) contre +0,042 avec TP 3R : TP touché 1,9 % des trades (21 sur 1 110, +1,95 R) contre 0,3 % ; SL 10,6 % (−1,04 R), sortie à 16:55 87 % (+0,13 R) ; écart négligeable, n° 29 inchangé (TP 3R figé)
- [2026-11-21] decision | Protocole : réserve par question (PROTOCOLE.md étape 0 point 4, wiki/concepts/is-oos.md point 6) ; stops sur le short yen filtré R4 (run_jpy_us_r4_stops.py, reports/jpy_us_r4_stops_report.md, 8 essais figés avant calcul, compteur 1 814 → 1 822) ; n° 29 écrit et commité avant tout téléchargement (PREREGISTRATION_29.md, run_prereg29.py), compteur 1 822 → 1 826 | Stops R4 : SL 2 ATR H1 + TP 3R retenu par le critère figé (R net max) : +0,041 R/trade, 10,8 % de SL, TP 0,3 % (≈ SL seul ≈ 30 bp), pire creux −13 R ; SL 4 ATR H1 +2,02 bp sur +2,09 sans stop ; 1 σ20 s'effondre (+0,008 R) ; bougies dollar non testées (règle en temps, comptant sans volume). N° 29 : H1 écart jours R4 − autres > 0 (brut mid), H2 R net > 0, Holm sur 2 ; étape 3 sur USDJPY comptant Dukascopy 2003-05 → 2009-12 (vierge, ticks disponibles, déclarée réservée), étape 4 sur 6J aux dates du n° 28 ; puissance ≈ 44 % (H1) / 30 % (H2) → échec à écart positif = non concluant ; contrôle du code sur 6J déjà vu : R +0,042 (redonne S7)
- [2026-11-21] experiment | Short yen 11:00 → 16:55 ET filtré par jour (étape 1, données déjà vues 6J 2017-01 → 2026-08-28) : 4 filtres de volatilité ex ante (V1-V4) et 4 de retournement (yen en hausse sur la fenêtre de la veille, 3 fenêtres, la journée 16:55 → 16:55 de la veille, 3 journées : R1-R4), grille figée et commitée avant calcul (run_jpy_us_filtres.py, reports/jpy_us_filtres_report.md, results/jpy_us_filtres/, branche strategies-vbt), compteur 1 806 → 1 814 | Volatilité ❌ B1 (Sharpe quotidien 0,52-0,67 contre 0,64, t écart ≤ 1,6) → registre ; retournement ✅ B1 pour R1-R4, R4 la meilleure : net +2,09 bp les jours pris (46 %, t NW 3,5) contre −0,11 les autres (t 2,4), Sharpe quotidien 1,00, moitiés +1,80 / +2,38, 9/10 ans, DSR 0,98 à N = 42 → « À surveiller » ; condition de réouverture de Piccotti (retournement concentré en intraday) remplie ; pas de réserve : candidat à un pré-enregistrement n° 29 sur les données du n° 28 (non écrit)
- [2026-11-21] query | Short yen 11:00 → 16:55 ET avec trailing stop k × ATR M15 / H1 (k = 1-4, sans TP), grille figée et commitée avant calcul, exploratoire sur 6J 2016-2026-08 déjà vu (run_jpy_us_trailing.py, reports/jpy_us_trailing_report.md, results/jpy_us_trailing/, branche strategies-vbt), compteur 1 798 → 1 806 | aucune des 8 ne bat la règle sans stop (+0,88 bp net, Sharpe 0,59) : trailing 1 ATR M15 −0,79 bp (97 % stoppés, Sharpe −1,18), 2 ATR M15 −0,47, 1 ATR H1 −0,29 ; larges = référence (4 ATR H1 +0,87, 4 % stoppés) ; trades stoppés à brut moyen négatif partout ; ligne au registre (stops sur le short yen, SL/TP + trailing) ; n° 28 inchangé

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
