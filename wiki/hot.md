---
type: hot
updated: 2026-11-21 15:55
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 822** (source : [[reports/jpy_us_r4_stops_report]])
- Dernier pré-enregistrement : n° 29 ([[PREREGISTRATION_29]])
- Idées abandonnées au registre : 42 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-21

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/ml-anomalies\|Machine learning sur les anomalies que les filtres classiques n'ont pas améliorées]] | active | 1er essai (filtre binaire sur mom) rejeté ; autres candidates à faire |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-21] decision | Protocole : réserve par question (PROTOCOLE.md étape 0 point 4, wiki/concepts/is-oos.md point 6) ; stops sur le short yen filtré R4 (run_jpy_us_r4_stops.py, reports/jpy_us_r4_stops_report.md, 8 essais figés avant calcul, compteur 1 814 → 1 822) ; n° 29 écrit et commité avant tout téléchargement (PREREGISTRATION_29.md, run_prereg29.py), compteur 1 822 → 1 826 | Stops R4 : SL 2 ATR H1 + TP 3R retenu par le critère figé (R net max) : +0,041 R/trade, 10,8 % de SL, TP 0,3 % (≈ SL seul ≈ 30 bp), pire creux −13 R ; SL 4 ATR H1 +2,02 bp sur +2,09 sans stop ; 1 σ20 s'effondre (+0,008 R) ; bougies dollar non testées (règle en temps, comptant sans volume). N° 29 : H1 écart jours R4 − autres > 0 (brut mid), H2 R net > 0, Holm sur 2 ; étape 3 sur USDJPY comptant Dukascopy 2003-05 → 2009-12 (vierge, ticks disponibles, déclarée réservée), étape 4 sur 6J aux dates du n° 28 ; puissance ≈ 44 % (H1) / 30 % (H2) → échec à écart positif = non concluant ; contrôle du code sur 6J déjà vu : R +0,042 (redonne S7)
- [2026-11-21] experiment | Short yen 11:00 → 16:55 ET filtré par jour (étape 1, données déjà vues 6J 2017-01 → 2026-08-28) : 4 filtres de volatilité ex ante (V1-V4) et 4 de retournement (yen en hausse sur la fenêtre de la veille, 3 fenêtres, la journée 16:55 → 16:55 de la veille, 3 journées : R1-R4), grille figée et commitée avant calcul (run_jpy_us_filtres.py, reports/jpy_us_filtres_report.md, results/jpy_us_filtres/, branche strategies-vbt), compteur 1 806 → 1 814 | Volatilité ❌ B1 (Sharpe quotidien 0,52-0,67 contre 0,64, t écart ≤ 1,6) → registre ; retournement ✅ B1 pour R1-R4, R4 la meilleure : net +2,09 bp les jours pris (46 %, t NW 3,5) contre −0,11 les autres (t 2,4), Sharpe quotidien 1,00, moitiés +1,80 / +2,38, 9/10 ans, DSR 0,98 à N = 42 → « À surveiller » ; condition de réouverture de Piccotti (retournement concentré en intraday) remplie ; pas de réserve : candidat à un pré-enregistrement n° 29 sur les données du n° 28 (non écrit)
- [2026-11-21] query | Short yen 11:00 → 16:55 ET avec trailing stop k × ATR M15 / H1 (k = 1-4, sans TP), grille figée et commitée avant calcul, exploratoire sur 6J 2016-2026-08 déjà vu (run_jpy_us_trailing.py, reports/jpy_us_trailing_report.md, results/jpy_us_trailing/, branche strategies-vbt), compteur 1 798 → 1 806 | aucune des 8 ne bat la règle sans stop (+0,88 bp net, Sharpe 0,59) : trailing 1 ATR M15 −0,79 bp (97 % stoppés, Sharpe −1,18), 2 ATR M15 −0,47, 1 ATR H1 −0,29 ; larges = référence (4 ATR H1 +0,87, 4 % stoppés) ; trades stoppés à brut moyen négatif partout ; ligne au registre (stops sur le short yen, SL/TP + trailing) ; n° 28 inchangé
- [2026-11-21] query | Short yen 11:00 → 16:55 ET : les SL sont-ils touchés par une hausse du yen qui « rechute » ensuite ? Comparaison des chemins réels 1 min (6J 2016-2026-08, déjà vus) aux mêmes minutes permutées dans la séance (même dérive, même volatilité), 5 combinaisons SL/TP de la grille déjà comptée ; script jetable, hors compteur (1 798) | Non : fréquence des SL identique au hasard (62 % contre 62 % pour SL 1 ATR M5, 31 % contre 31 % pour 2 ATR M15) et les trades stoppés finissent gagnants à 16:55 MOINS souvent que sur chemins permutés (38 % contre 44 % ; 14 % contre 18 %) : quand le yen monte assez pour toucher le stop, il continue plutôt (jours de stress) ; la perte des SL/TP est mécanique (sortie avant que la dérive de 2 bp s'accumule sous 24 bp de bruit), pas un motif intrajournalier
- [2026-11-21] prereg | N° 21 : continuation de la nuit sur l'or hors échantillon dans le temps (or au comptant LSE 2003-05 → 2015-12, run_prereg21.py, reports/prereg21_report.md, results/prereg21/) ; avenant A (7fde669, avant calcul) : argent 2003-2017 indisponible (LSE limité à 10 ans, Dukascopy sans barres avant 2016), non testé, p = 1 dans Holm | ❌ ÉCHEC : 2 803 jours, pente c −0,0054 (b 0,995, t −0,09, p unilatéral 0,54, Holm 1,00), 2003-2008 c −0,10 / 2009-2015 c +0,08 ; règle nette −0,30 bp/jour (brut +1,39) ; registre des échecs, phénomène marqué contredit, réserve or au comptant consommée ; compteur inchangé (essais déjà comptés)
- [2026-11-20] query | Performances de mom depuis septembre 2026, sans rien recalculer sur le holdout NQ (≥ 2026-11-04, réservé n° 26) : fenêtre vue 2026-08-31 → 11-03 relue dans results/mom_perf/ (LSE, code figé) + trades live du bot (démo puis réel, 11-04 → 11-20) | backtest fenêtre vue : 44 nuits longues, −1,01 R (−0,023 R/nuit, 34 % gagnants, 64 % de stops, max DD −10,4 R, t −0,13) ; live : 12 trades, 2 gagnants, −7,34 R ; ensemble 56 trades −8,35 R (−0,15 R/trade) : 4,8 % des fenêtres de 56 trades du backtest 2011-07 → 2026-08 font aussi mal (script jetable, hors compteur) ; aucun calcul sur NQ après le 2026-11-03
- [2026-11-20] decision | Règle d'arrêt de mom en live figée avant le trade du soir (live/arret_mom.toml, live/bot.py regle_arret / bilan_mom / mom_arrete, live/README, 3 tests dans tests/test_live.py ; calibrage par script jetable sur cache/propfirm/nq_nuit_tp4_mfe.parquet, hors compteur) | frontière cumul R < 0,106 N − 2,5 × 1,287 √N (N ≥ 10, 7 trades démo + trades réels) ou 6 évals A perdues d'affilée ; fausse alarme ≈ 3 % en 200 trades (chemins historiques 3,2 %, bootstrap blocs 3,2 %), puissance en 200 trades 20 % (0 R) / 37 % (−0,05) / 58 % (−0,10) ; état au 20/11 : 12 trades, −7,34 R, frontière −9,87 R, marge +2,53 R (4 stops de plus déclenchent) ; arrêt collant, B non concerné ; correction : le décompte du 20/11 au matin (13 trades, −8,36 R) comptait un trade de trop
- [2026-11-20] query | Journal VPS du 20/11 (nuit du 19 au 20) | A (nouvelle éval réelle 531542597, FTMO-Server3, détectée le 19/11 05:03 ET) : mom long 1,13 lot 20:00:03 à 26 392,88, stop 217,9 pts, SL à 02:25:22, −248,66 $ (−1,01 R), éval n° 2 −2,49 % ; B : 3n rien (+66,6 bps), éval −0,02 % (3n SL la nuit du 18 au 19, −249,83 $, efface le TP M2 du 17/11 ; pas de M2 le 19 : 3n au SL) ; exécution conforme ; mom live 13 trades, 2 gagnants, −8,36 R, 7 stops de suite : 0,8 % des fenêtres de 13 trades du backtest 2011-07 → 2026-08 font aussi mal (script jetable, hors compteur)

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
<!-- NEXT-ACTIONS:END -->
