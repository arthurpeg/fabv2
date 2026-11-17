---
type: hot
updated: 2026-11-17 23:47
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 742** (source : [[reports/inference_overnight_report]])
- Dernier pré-enregistrement : n° 26 ([[PREREGISTRATION_26]])
- Idées abandonnées au registre : 35 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-17

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-17] query | Qualité du spot Dukascopy (M15, bid seul, strategie trading/data_m15) contre les futures CME (cache/6x_adj) sur 2016-01-04 → 2025-06-30 ; script jetable du scratchpad, contrôle de données hors compteur | corrélation des rendements 15 min 0,996 (EUR), 0,993 (GBP), 0,994 (JPY) ; écart médian 0,25 à 0,41 bp par barre ; rendements des sessions 08-11 et 11-16:45 NY : corrélation journalière 1,000, même signe 98 % des jours, moyennes à ≤ 0,15 bp près ; barres plates ≤ 0,03 % (pire vers 21-22 h UTC, rollover). Dukascopy est utilisable pour combler 2010-2015 et CHF/CAD/NZD/NOK/SEK ; les futures restent la référence 2016-2026. ⚠️ Les moyennes brutes 2016-2025 de ces deux sessions ont été vues (EUR ≈ +0,5 bp, GBP ≈ +0,6, USDJPY +1,8 en session US) : à déclarer dans tout pré-enregistrement Zhang
- [2026-11-17] query | Inventaire des cotations FX de la machine pour tester Zhang (2018) en intraday (fabv2/cache, D:/quant-data/Cotations, mean reversion, strategie trading) | futures CME 1 min 2016-01 → 2026-08 : 6E, 6B, 6J, 6A seulement (Databento) ; spot : Dukascopy M15 2013-2025 EURUSD, GBPUSD, USDJPY, GBPJPY (strategie trading), LSE 1 h USDJPY 2009-2011 seulement (mean reversion), yfinance 1 h 2023-2026 EUR/GBP ; cache/histdata = CFD d'indices, pas du FX ; pas de CHF, CAD, NZD, NOK, SEK en intraday ni de 2010-2012 ; session US de Zhang déjà testée sur 6E/6B/6J/6A (R5b, jambe longue 11:00 → 16:55 ET, ❌ net)
- [2026-11-17] query | Lecture intégrale de Zhang (2018, FRL 27), SSRN 3138756 « Intraday Patterns in FX Returns and Realized Volatility » ; PDF déposé par l'utilisateur (papers/ssrn-3138756.pdf, ignoré par git), texte extrait dans papers/txt/zhang_fx_intraday_rv.txt | 16 devises, Datastream horaire 2010-05 → 2015-12 : devise domestique en baisse sur ses heures (13/16 négatives, 8 significatives), en hausse sur la session US 11:00-17:00 NY (12/16 positives, 6 significatives : DKK, EUR, GBP, INR, NOK, SEK) ; ordres de grandeur ≈ 2 bp par session ; régression sur la volatilité réalisée contemporaine (lag non significatif) : pas de signal prédictif ; aucune analyse de coût. La session US commence au fix de Londres : même effet que la saisonnalité des fixings (Krohn) déjà au registre, pas de nouvelle piste. Fiche du 02/11 corrigée (JPY)
- [2026-11-17] query | Journal VPS du 17/11 | B : M2 short au TP à 10:51 ET (+424,72 $, +4,25 %, +2,01 R), éval +4,97 % ; A : éval −5,04 %, rien d'ouvert ; aucune erreur
- [2026-11-17] query | Série de pertes de mom en live (book A, démo puis réel, 9 trades du 04/11 au 16/11) comparée au backtest 2011-07 → 2026-08 (cache/propfirm/nq_nuit_tp4_mfe.parquet, coût 0,02 R ; script jetable du scratchpad, hors compteur) | live : 2 gagnants sur 9, −4,27 R, 4 stops de suite ; backtest : 44 % de gagnants, +0,11 R par trade ; 8 % des fenêtres de 9 trades font ≤ −4,27 R, 15 % ont ≤ 2 gagnants ; ≥ 4 pertes de suite ≈ 10 fois par an, ≥ 6 ≈ 3 fois par an, record 15 ; pire creux −27 R : série banale, rien d'anormal
- [2026-11-17] query | Réponse du support FTMO aux points flous | générique : pas de validation préalable, contrôle sur les ordres réels, clause 7 (reproductible en réel), article gambling ; repère 20 % de marge et 1,5 % de risque par idée de trade ; écarts : éval 2,5 % par trade, financé A + B long la même nuit = 2 % sur une idée ; aucune modification du bot à ce stade
- [2026-11-17] query | Contrôle du 1er trade M2 réel (book B) | SL 257,5 pts = 4 × ATR M15 (64,4 pts), conforme ; risque 2,14 % = risque dynamique après le 3n de la nuit (+0,73 %), 0,82 lot ; B éval +0,73 % avant ce trade
- [2026-11-16] query | Premier jour des vrais comptes FTMO lu dans le journal vps-journal | A : mom long 1,32 lot dim. 15/11 20:00:04 ET à 28 090,18 (glissement −0,90 pt), SL touché à 20:11 (−249,55 $, −2,50 %, −1,02 R), éval −2,50 % ; B : 3n rien (+54,2 bps), M2 rien, éval +0,00 % ; exécution conforme, aucune position ouverte, aucune erreur

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- **Vrais comptes FTMO en éval depuis le 2026-11-14** : A = compte 511480419 (FTMO-Server), B = 541521340 (FTMO-Server4), 10 000 $ chacun, bascule automatique faite (démo archivée dans `live/etat/archive/`). 1er trade réel : mom SL le 15/11 (A éval −2,50 %, B 0 %) ; relire le journal (`git fetch origin vps-journal`). Toujours en attente de la réponse du support FTMO (A + B long la même nuit, voir [[live/README]]).
- **Plan FTMO retenu (2026-11-04)** : compte A = mom, compte B = 3n + M2, règle des annonces + cible + attente, éval 2,5 % / financé 1 %, scaling 10k → 400k ; détail dans [[wiki/experiments/propfirm-ftmo-option]] (section « Plan retenu »).
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
