---
type: hot
updated: 2026-11-25 20:07
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **2 127** (source : [[reports/propfirm_bb_report]])
- Dernier pré-enregistrement : n° 32 ([[PREREGISTRATION_32]])
- Idées abandonnées au registre : 54 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-25

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|BB : bande de bruit (« Beat the Market », Zarattini et al.) sur NQ]] | active | rejeté (DSR) ; aucun test sur données neuves ; forward n° 32 (1re lecture 2028-02-29) |
| [[wiki/experiments/ml-anomalies\|Machine learning sur les anomalies que les filtres classiques n'ont pas améliorées]] | active | 1er essai (filtre binaire sur mom) rejeté ; autres candidates à faire |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-25] schema | Papiers publics (nuit, FX/yen, prop firm) passés en version complète après un avis de relecteur : règles divulguées (mom SL 2 ATR / TP 5 ATR, 3n, M2), annexe des pré-enregistrements avec commits GitHub, corrections (Holm sur 21 tests, 2 694 jours, réplication « au centième » nuancée, p 0,0015 = bootstrap pré-enregistré), citations Krohn-Mueller-Whelan 2024, Carpenter 2000, Goetzmann-Ingersoll-Ross 2003, figures (make_paper_figures.py), contrôle du carry du yen au comptant (run_jpy_spot_carry.py, hors compteur), continuation de l'or retirée de « à surveiller » (n° 21) | Comptant 2016-2025 +1,74 bp (t 3,9) contre 6J +1,90 : pas le carry ; profil par demi-heure de NQ : ≈ 2/3 de la nuit avant 02:00 ET, +0,7 bp l'heure de l'ouverture d'Eurex ; n° 10 à 17 commités avec leurs résultats, ordre invérifiable (leçon 10 bis)
- [2026-11-22] schema | Bilan nuancé de la preuve hors échantillon de BB ajouté à sa page ; erreur corrigée dans les rapports ftmo_bb_options, ftmo_4comptes, ftmo_sans3n : mom a été validé hors échantillon (n° 11, NQ 2011-2015), seuls 3n et M2 (EMA 9:30) ont échoué (n° 24, 25) | aucun calcul
- [2026-11-22] experiment | FTMO : hasard ou edge qui peut mourir en live (run_ftmo_edge_mort.py, hors compteur) : mom avec edge live = h × historique, h de −1 à 1, ré-échantillonnage pondéré | 2016-2026 cible+attente : intacte +783 $ / tentative 10k, morte (= hasard) +190 $, inversée −0,5 +57 $ ; le hasard ne gagne que si P(inversion) > 53-82 % ; garder les edges ; exploration
- [2026-11-22] experiment | FTMO : remplacer 3n par BB (run_ftmo_sans3n.py, hors compteur) | Corrélation des R mom / 3n +0,45 ; 2 comptes : A mom + B (M2 puis BB) +3 894 $ contre plan +3 502 $ ; 3 comptes : option 2 (avec 3n) +4 971 $ contre +4 486 $ sans 3n ; exploration
- [2026-11-22] experiment | FTMO jusqu'à 4 comptes (run_ftmo_4comptes.py, hors compteur) : plan, + C = BB, B séparé (B1 3n, B2 M2), 4 comptes | Plan +3 502 $ ; option 2 +4 971 $ ; B séparé +3 659 $ ; 4 comptes +5 129 $ ; C corrélé −0,43 avec A ; l'option 2 reste le meilleur compromis ; exploration
- [2026-11-22] experiment | FTMO : ajouter BB au plan retenu (run_ftmo_bb_options.py, hors compteur) : option 1 A = mom + BB l'après-midi, option 2 compte C = BB ; 494 départs 2016-2025, 12 mois | Plan +3 502 $ ; option 1 +3 749 $ (+7 %) ; option 2 +4 971 $ (+42 %, C +1 469 $) ; creux −1 043 $ ; exploration, BB non validé (n° 32)
- [2026-11-22] prereg | Statut de BB corrigé (n'était pas en paper trading, pas dans le n° 26 ; le 0,55 de 2010-2015 était la variante S1) ; n° 32 : forward de BB (H1 référence, H2 prop firm mode A SL 0,25 ATR TP 2R un trade par jour) sur NQ à partir du 2026-11-04, lectures 2028-02-29 / 2029-08-31 / 2031-08-29, fenêtre LSE 2026-08-29 → 11-03 exclue ; compteur 2 127 → 2 129 | aucun calcul
- [2026-11-22] experiment | BB un trade par jour (18 essais, run_bb_1j.py, grille e1f932a ; compteur 2 109 → 2 127) puis FTMO 1-Step (run_propfirm_bb.py, 18 versions × éval 1-2,9 %, financé 1 %, hors compteur) | Un trade par jour : +0,148 R/trade, creux −14 R ; FTMO à 2-2,5 % : passage 47-56 % en 10-15 trades, ≈ +1 450-1 560 $/mois en 100k, au niveau du plan 3n + M2, sous mom ; exploration

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
