---
type: hot
updated: 2026-11-22 17:06
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 940** (source : [[reports/fx_balance_report]])
- Dernier pré-enregistrement : n° 29 ([[PREREGISTRATION_29]])
- Idées abandonnées au registre : 44 ([[wiki/Failed Ideas/ledger]])
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

- [2026-11-22] research | Récolte SSRN sur l'opening range breakout (indices US, ranges 5/15/30 min) : papiers_ssrn_orb_2026-11-22.md, OpenAlex (429 fréquents) + Crossref, 57 requêtes, ~2 000 candidats | 8 papiers fournis (dont réplication de Zarattini-Aziz QQQ 5 min sur la seule période d'origine, bande de bruit NQ +10 $/jour 2 survivants sur 144 essais, ORB 15 min sur l'or nul), 8 écartés, carte des ORB déjà fournis par durée ; aucun calcul, compteur inchangé ; ORB toujours au registre sans condition de réouverture
- [2026-11-22] experiment | Étape 1 de wiki/experiments/fx-exportateur-importateur : grille figée avant calcul (run_fx_balance.py, commit 5f8afd2), 12 devises hors majeures téléchargées (fetch_fx_balance.py, Dukascopy 1 h), contrôle de qualité → 7 gardées (NOK, SEK, PLN, MXN, ZAR, SGD, TRY), solde commercial Banque mondiale de l'année précédente, exploration 2010-01 → 2021-08, compteur 1 937 → 1 940 | ❌ B1 : T1 exportateurs − importateurs −0,60 bp (t −0,72) ; T2 fuseau européen +2,71 bp (t 2,09, Holm 0,054, DSR 0,89, une seule devise importatrice : PLN 2010-2013) ; T3 t 0,49 ; à la place, session domestique négative toutes devises −1,38 bp (t −2,36, sens Zhang H1) → « À surveiller » ; ligne au registre ; réserve 2021-09 → 2026-08 non ouverte
- [2026-11-22] experiment | Fiche fx-exportateur-importateur corrigée : le poids du commerce (1-2 % du volume brut) n'est plus une objection décisive, car le prix suit le flux net directionnel (swaps et échanges entre banques ne poussent pas le prix) ; objection principale = couverture à terme des exportateurs | aucun calcul
- [2026-11-22] experiment | Fiche d'idée (étape 0) wiki/experiments/fx-exportateur-importateur : la devise d'un pays exportateur monte pendant sa session domestique, celle d'un importateur baisse ; réserve 2021-09-01 → 2026-08-28 déclarée dans wiki/reserves.md sur des devises flottantes hors 7 majeures (exploration 2010-01 → 2021-08) | B0 ✅ ; aucun calcul, compteur inchangé 1 937 ; 7 majeures déjà vues (n° 27, indice défavorable à l'œil), parcours phénomène seulement (effet attendu < 1,5 × coût), puissance ≤ 55 % à 1 bp/jour
- [2026-11-22] schema | Papier façon SSRN sur le FX en session US : reports/fx_us_session_paper.html + .pdf (9 pages A4, réplication de Zhang 2018 sur 2010-2015, échec hors échantillon 2016-2026, le yen en baisse en session US : coûts, forme, conditions, filtres de retournement, tests pré-enregistrés n° 28 et 29 à venir ; auteur Arthur Pegliasco) | aucun calcul, chiffres repris de reports/zhang_fx_report, jpy_us_backtest, jpy_us_distribution, jpy_us_filtres, yen_derive_ab ; aucune mention de stop ni d'objectif
- [2026-11-22] schema | Papier overnight (reports/overnight_drift_paper.*) : toutes les mentions du stop et de l'objectif de mom retirées à la demande de l'utilisateur (règle décrite par l'entrée 20:00, la sortie au plus tard 9:30 et le momentum 12-1 ; lignes « stop sur le range du soir » retirées des tableaux 6 et A1) | aucun calcul ; l'ancien PDF reports/overnight_research_en.pdf et l'historique git les contiennent encore
- [2026-11-22] schema | Version papier façon SSRN de la recherche overnight : reports/overnight_drift_paper.html + .pdf (11 pages A4, résumé, JEL, 6 tableaux + annexe A1, 22 références ; auteur Arthur Pegliasco), réécrite depuis reports/overnight_research_en.pdf du 2026-11-06 sans nom du dépôt ni chemins internes | aucun calcul, chiffres repris du PDF du 6 novembre (compteur 1 742 à cette date)
- [2026-11-22] schema | Version papier façon SSRN de l'étude de convexité prop firm : reports/propfirm_convexity_paper.html + .pdf (9 pages A4, résumé, JEL, 7 tableaux, figure, références ; auteur Arthur Pegliasco), remplace propfirm_ftmo_overview.pdf | aucun calcul, chiffres repris de la présentation

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
