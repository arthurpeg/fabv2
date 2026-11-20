---
type: hot
updated: 2026-11-20 11:26
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 798** (source : [[reports/jpy_us_distribution_report]])
- Dernier pré-enregistrement : n° 28 ([[PREREGISTRATION_28]])
- Idées abandonnées au registre : 39 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-20

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/ml-anomalies\|Machine learning sur les anomalies que les filtres classiques n'ont pas améliorées]] | active | 1er essai (filtre binaire sur mom) rejeté ; autres candidates à faire |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-20] query | Performances de mom depuis septembre 2026, sans rien recalculer sur le holdout NQ (≥ 2026-11-04, réservé n° 26) : fenêtre vue 2026-08-31 → 11-03 relue dans results/mom_perf/ (LSE, code figé) + trades live du bot (démo puis réel, 11-04 → 11-20) | backtest fenêtre vue : 44 nuits longues, −1,01 R (−0,023 R/nuit, 34 % gagnants, 64 % de stops, max DD −10,4 R, t −0,13) ; live : 12 trades, 2 gagnants, −7,34 R ; ensemble 56 trades −8,35 R (−0,15 R/trade) : 4,8 % des fenêtres de 56 trades du backtest 2011-07 → 2026-08 font aussi mal (script jetable, hors compteur) ; aucun calcul sur NQ après le 2026-11-03
- [2026-11-20] decision | Règle d'arrêt de mom en live figée avant le trade du soir (live/arret_mom.toml, live/bot.py regle_arret / bilan_mom / mom_arrete, live/README, 3 tests dans tests/test_live.py ; calibrage par script jetable sur cache/propfirm/nq_nuit_tp4_mfe.parquet, hors compteur) | frontière cumul R < 0,106 N − 2,5 × 1,287 √N (N ≥ 10, 7 trades démo + trades réels) ou 6 évals A perdues d'affilée ; fausse alarme ≈ 3 % en 200 trades (chemins historiques 3,2 %, bootstrap blocs 3,2 %), puissance en 200 trades 20 % (0 R) / 37 % (−0,05) / 58 % (−0,10) ; état au 20/11 : 12 trades, −7,34 R, frontière −9,87 R, marge +2,53 R (4 stops de plus déclenchent) ; arrêt collant, B non concerné ; correction : le décompte du 20/11 au matin (13 trades, −8,36 R) comptait un trade de trop
- [2026-11-20] query | Journal VPS du 20/11 (nuit du 19 au 20) | A (nouvelle éval réelle 531542597, FTMO-Server3, détectée le 19/11 05:03 ET) : mom long 1,13 lot 20:00:03 à 26 392,88, stop 217,9 pts, SL à 02:25:22, −248,66 $ (−1,01 R), éval n° 2 −2,49 % ; B : 3n rien (+66,6 bps), éval −0,02 % (3n SL la nuit du 18 au 19, −249,83 $, efface le TP M2 du 17/11 ; pas de M2 le 19 : 3n au SL) ; exécution conforme ; mom live 13 trades, 2 gagnants, −8,36 R, 7 stops de suite : 0,8 % des fenêtres de 13 trades du backtest 2011-07 → 2026-08 font aussi mal (script jetable, hors compteur)
- [2026-11-20] ingest | Lecture complète de Batten et Lucey, « Volatility in the Gold Futures Market » (SSRN 996235) ; fiche [14] de papiers_ssrn_overnight_fx_or_petrole_2026-11-02.md précisée (COMEX proche 8:20-15:30 NY, 1999-2005, sans nuit) | Aucun calcul, compteur inchangé 1 798 ; volatilité maximale à l'ouverture de la criée, décroissante ensuite, cohérente avec nos phénomènes Fattinger-Ziegler sur GC ; aucun signal
- [2026-11-20] ingest | Lecture complète de Jin, Li, Wang, Yang, « Price Discovery in the Chinese Gold Market » (SSRN 2776581, PDF MPRA 71135 dans papers/ ; Xu-Zhang SSRN 2951302 introuvable en accès libre, publié payant au JFM 2019) ; fiche [7] de papiers_ssrn_overnight_fx_or_petrole_2026-11-02.md précisée | Aucun calcul, compteur inchangé 1 798 ; découverte du prix interne à la Chine (futur SHFE > comptant SGE, ILS 61,7 %), sans COMEX : contexte seulement
- [2026-11-19] ingest | Relecture complète de Zhang, « Price discovery in gold markets: China and the US » (SSRN 2564688) ; fiche [10] de papiers_ssrn_overnight_fx_or_petrole_2026-11-02.md corrigée (données 2010-03 → 2012-03, avant la nuit SHFE ; SHFE et COMEX se relaient pour mener le comptant SGE, pas entre eux) | Aucun calcul, compteur inchangé 1 798 ; contexte de découverte du prix, pas de règle de trading
- [2026-11-19] decision | Dépendances ML isolées du bot : LightGBM et scikit-learn passent dans le groupe uv `ml` (hors défaut, `uv run --group ml`) ; live/maj_auto.ps1 ne fait `uv sync` et ne relance les bots que si `uv export` (groupes par défaut) change avant / après la mise à jour | Cause : l'ajout de LightGBM aux dépendances par défaut avait relancé les bots A et B à 14:52 ET (sans position ouverte, état conservé) ; tests test_live 14/14 ; maj_auto testé sous PowerShell 5.1 (analyse sans erreur, comparaison des exports)
- [2026-11-19] experiment | Filtre ML binaire à taille fixe 1 R sur mom (TP 4 ATR) pour le passage prop firm, branche ml : logit L2 et LightGBM contraint sur mom continu, nuit d−1 (Abdi), clôture − VWAP (BLW), NFP/CPI ; Purged K-Fold 5 × embargo 5 ; 70/50/35 % gardés ; Monte Carlo 10 000 chemins (+10/−10 R, +8/−6 R, FTMO 2,5 %) ; grille commitée avant calcul (2c9dcd6), reports/ml_propfirm_filter_report.md | ❌ AUC hors bloc 0,498 / 0,507 (Abdi seule 0,512) ; aucun filtre ML significatif (p brut ≥ 0,18, Holm 1,0), P(réussite) baseline 80,2 / 65,7 / 50,0 % contre ML ≤ 81,7 / 68,5 / 52,1 % (dans le p95 aléatoire) et Abdi seule 86,2 / 73,0 / 53,8 % à 35 % (non significative non plus) ; jours × 1,4-2,9 ; filtres négatifs sur 2023-2026 ; holdout non lu ; compteur 1 798 → 1 807

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
