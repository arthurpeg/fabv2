---
type: hot
updated: 2026-11-19 11:09
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 742** (source : [[reports/inference_overnight_report]])
- Dernier pré-enregistrement : n° 28 ([[PREREGISTRATION_28]])
- Idées abandonnées au registre : 37 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-19

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-19] query | Journal VPS du 19/11 : éval réelle du compte A (511480419) perdue au 4e stop de mom (long 1,34 lot 18/11 20:00:02 ET à 27 487,58, risque réduit à 2,40 %, stop 176,3 pts, SL à 20:25:48, −241,54 $, −1,02 R) | solde 8 998,74 $ (−10,01 %, 1,26 $ sous le plancher à cause du glissement ; sans lui le compte était de toute façon perdu, risque restant < 0,05 %) ; compte virtuel passé à l'éval n° 2 (+0,00 %), FTMO a coupé le trading à 20:30 ; exécution conforme ; rachat d'un 1-Step 10k à connecter dans le terminal A (pas de nouvelle bascule : mode réel déjà marqué) ; mom live 12 trades, 2 gagnants, −7,35 R
- [2026-11-19] schema | Nouvelle règle de projet : réserve hors échantillon par actif (CLAUDE.md règle 4, wiki/concepts/is-oos.md) et registre des données wiki/reserves.md (vierge / explorée / réservée / consommée), SCHEMA et index mis à jour | Inventaire reconstitué : presque tout 2016-2026-08 et ES/NQ/YM 2010-2015 sont explorés ; vierges : USDNOK/USDSEK spot 2010-2016 et tout ce qui est postérieur au 2026-08-28 hors NQ et yen ; réservés : NQ ≥ 2026-11-04 (n° 26), yen ≥ 2026-08-29 (n° 28)
- [2026-11-19] query | Backtest historique (déjà vu, exploratoire, compteur inchangé) du short yen 11:00 → 16:55 ET du n° 28 + pistes d'explication (run_jpy_us_backtest.py, reports/jpy_us_backtest_report.md, results/jpy_us/) ; rien après le 2026-08-28 | 6J 2016-2026-08 vectorbt : brut +2,03 bp (Sharpe 1,37), net standard +0,90 bp (Sharpe 0,61, +22 300 $/contrat, creux −7 100 $, 2,5 ans), 2 ticks +0,28 ; spot 2012-2015 au bid/ask +1,55 bp ; explication : pas un artefact des futures, pas la hausse du dollar (euro +0,41 ; constante −2,05 bp t −5,7 après euro et ES), pas le risk-on moyen (ES n'explique que −0,23 bp), pas que la tendance (2016-2020 yen +0,86/j sur 24 h mais −1,17 en fenêtre US) ; restent flux, carry, taux US (non testables sans ZN ni données de flux)
- [2026-11-19] decision | N° 28 : short du yen pendant la session US (short 6J 11:00 → 16:55 ET, 1 tick + 5 $), test sur données postérieures au 2026-08-28 seulement, lectures 2028-02-29 / 2029-08-31 / 2031-08-29 (PREREGISTRATION_28, run_prereg28.py), compteur 1 784 → 1 786 | R5b sur 6J = sens inverse (long yen, −0,88 tick brut/trade sur ses deux jambes) ; référence historique déjà vue 2016-2026-08 : +2,04 bp brut, +0,92 net, Sharpe net 0,61 (2016-2020 +0,34 net, 2021-2026 +1,44) ; puissance H1 brut 76 % à 3 ans, H2 net 37 % à 5 ans ; calculs sur le yen après le 2026-08-28 interdits entre les lectures ; ligne de réouverture au registre
- [2026-11-19] experiment | N° 27 : Zhang (2018) sur les 7 majeures (PREREGISTRATION_27 commit fd5b243 avant calcul, run_zhang.py, reports/zhang_fx_report.md, results/zhang/), compteur 1 742 → 1 784 | Réplication 2010-2015 sur spot Dukascopy : moyennes au centième de bp de la Table 1 (EUR US +2,20 vs +2,21), 7 des 9 cases ** / *** retrouvées (échecs CHF : choc BNS du 2015-01-15) ; hors échantillon 2016-2026-08 : 0/14 pour H1 (domestique < 0) et H2 (US > 0), H3 (φ < 0) 0/14 partout (coefficients de la taille du papier, non significatifs) ; JPY en baisse en session US −1,72 bp, t −4,3, 16 ans sur 17 → phénomènes (pas une stratégie : jambe 6J des fixings) ; GBP non-US, CAD non-US, CHF LDN-NY à surveiller ; ligne ajoutée au registre
- [2026-11-18] fix | Dukascopy prolongé jusqu'au 2026-08-28 pour les majeures sans future chez nous (USDCHF, USDCAD, NZDUSD ; fetch_dukascopy.py, SANS_FUTURE) ; décision : test Zhang limité aux 7 majeures (EUR, GBP, JPY, CHF, AUD, CAD, NZD), NOK/SEK et devises non majeures écartés pour leur spread | 1 h 2010-01 → 2026-08-28, 1 min 2012-01-11 → 2026-08-28 ; aucune barre le samedi, aucune barre vide, aucun spread négatif ; trous > 3 j seulement au Nouvel An ; spread médian 2017-2026 ≈ 1,0 bp (CHF), 0,9 (CAD), 1,7 (NZD) ; aucun calcul de rendement
- [2026-11-18] query | mom long après une baisse du NQ (backtest 2011-07 → 2026-08, cache/propfirm/nq_nuit_tp4_mfe.parquet, coût 0,02 R, rendement 20 séances à la clôture 16:00 de la veille ; script jetable, exploratoire, hors compteur, 5 découpes regardées) | longs : +0,087 R (n = 2 134) ; après −5 % ou pire sur 20 séances +0,158 R (n = 222, 50 % gagnants) ; −5 à −2 % −0,012 R (n = 238) ; ±2 % +0,068 ; ≥ +2 % +0,106 ; repli ≥ 5 % du plus haut 20 j +0,135 R (n = 345) : aucune preuve qu'une baisse de quelques semaines dégrade mom long ; aucune modification
- [2026-11-18] query | Journal VPS du 18/11 : 3e stop de mom sur le vrai compte A (long 1,09 lot 17/11 20:00:01 ET à 27 355,38, ATR M15 113,4, stop 226,7 pts, SL touché à 20:42:54, −255,33 $, −1,03 R, 5,6 pts de glissement au stop) | exécution conforme ; éval A −7,60 % (reste 2,40 % avant −10 %, prochain risque 2,40 %, un stop de plus = éval perdue, rachat prévu par le plan) ; live mom 11 trades, 2 gagnants, −6,33 R, 5 stops de suite : 2,5 % des fenêtres de 11 trades du backtest 2011-07 → 2026-08 font aussi mal, séries ≥ 5 stops ≈ 5 par an (script jetable, hors compteur)

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
