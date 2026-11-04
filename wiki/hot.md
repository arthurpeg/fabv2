---
type: hot
updated: 2026-11-04 18:20
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 738** (source : [[reports/holdout_anticipe_report]])
- Dernier pré-enregistrement : n° 26 ([[PREREGISTRATION_26]])
- Idées abandonnées au registre : 35 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-04

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-04] build | Bot de démo FTMO sur VPS : MT5 + Python, book A (mom) et B (3n + M2), compte FTMO virtuel, règle des annonces avec calendrier BLS / Fed relu (live/, tests/test_live.py, tests/test_live_bot.py) | signaux et compte identiques au backtest (78 tests verts) ; reste à installer sur le VPS Contabo (Windows requis) et à créer les deux essais FTMO
- [2026-11-04] decision | Plan FTMO retenu par l'utilisateur : compte A = mom, compte B = 3n + M2 (M2 si 3n n'a pas tradé ou est sorti à 03:00), éval 2,5 % avec objectif réduit, financé 1 %, règle des annonces, cible + attente, scaling 10k → 400k (wiki/experiments/propfirm-ftmo-option.md, section « Plan retenu » ; mémoire ftmo-plan-retenu) | à utiliser par défaut dans les prochaines conversations
- [2026-11-04] query | Métriques complètes de la montée en taille FTMO 10k → 100k (run_ftmo_scaling_metrics.py, reports/ftmo_scaling_report.md, section métriques) | 400k en 12,0 mois médian (MC historique) / 17,7 (edge / 2) ; ruine 0,2 % / 2,5 % ; cagnotte à 5 ans 375 k$ / 212 k$ ; revenu mensuel à 400k ≈ 7 700 $ / 5 000 $, mois négatifs 11 % / 22 % ; max DD de cagnotte médian −3 293 $ / −5 489 $ ; frais ≈ 18 k$ / 28 k$ sur 5 ans
- [2026-11-04] query | Contrôle du moteur FTMO Python par vectorbt : compte A (mom) du chemin historique rejoué avec les tailles, stops, objectifs et coupes d'annonce décidés par le moteur (journal ajouté à Compte ; run_ftmo_verif_vbt.py, reports/ftmo_verif_vbt_report.md) | 3 639 / 3 646 trades identiques au centime ; 7 écarts (objectif réduit franchi par un gap : vectorbt exécute à l'ouverture, plus favorable, max 6,18 $) ; P&L total +32 724 $ (moteur) contre +32 746 $ (vectorbt) : moteur validé, légèrement prudent
- [2026-11-04] query | Montée en taille FTMO : A mom + B 3n + M2, paliers 1/2/3 × 10k puis 1/2 × 100k par stratégie (400k), palier suivant quand la cagnotte (dépôt 869 $ + rewards − frais) couvre 10 évals par paire ; Compte de run_ftmo_deux_comptes.py paramétré (taille, prix, rachat) (run_ftmo_scaling.py, reports/ftmo_scaling_report.md, exploratoire, hors compteur) | 400k en ≈ 12 mois médian (historique) / 17,7 mois (edge / 2, 96 %) ; cagnotte à 5 ans médiane +375 k$ / +212 k$ ; vrai chemin : 400k le 25/04/2012, 1,31 M$ au 03/11/2026 ; risque concentré sur les 6 premiers mois (cagnotte à 0 dans 1 à 6 % des chemins)
- [2026-11-04] query | Monte-Carlo des deux comptes FTMO 10k (A mom, B 3n + M2, règle des annonces + cible + attente), bootstrap stationnaire par blocs de 20 séances, 5 000 chemins de 3 ans, scénarios historique / 2019-2026 / espérance divisée par 2 (run_ftmo_monte_carlo.py, reports/ftmo_monte_carlo_report.md, exploratoire, hors compteur) | net à 3 ans médian +12 889 / +12 305 / +7 939 $, P(< 0) 0 % ; à 1 an P(< 0) 0,1 / 0,2 / 2,7 % ; max DD de trésorerie 99e c. −782 / −869 / −1 304 $ ; série d'évals sans reward A 95e c. 7 / 9 / 10, B 4 / 4 / 7
- [2026-11-04] query | Deux comptes FTMO 10k (A mom, B 3n + M2), un seul chemin du 2011-07-01 au 2026-11-03, règle des annonces + cible + attente (run_ftmo_deux_comptes_historique.py, reports/ftmo_deux_comptes_historique_report.md, exploratoire, hors compteur) | net +68 562 $ (+4 469 $/an), 52 évals, 217 rewards, aucune année négative, max DD de trésorerie −435 $, pire série sans reward 5 évals (A) / 3 (B), corrélation P&L +0,24, flux mensuels +0,01
- [2026-11-04] query | Deux comptes FTMO (A mom, B 3n + M2) avec la règle des annonces (build_news_trades.py : mom coupé à 8:19 les jours NFP / CPI / PIB, M2 à 13:55 les jours de Fed ; dates sept.-oct. 2026 relevées sur BLS et Fed, PIB T3 supposé le 29/10) et la politique cible + attente ; horloge du reward corrigée (jours de bourse, tradés ou non) (run_ftmo_deux_comptes.py, reports/ftmo_deux_comptes_report.md) | 12 mois : +4 082 $ sans la règle, +3 843 $ avec, +3 864 $ avec cible + attente (10e c. +2 473 $, 12,9 rewards par an) ; départ 01/09/2026 : +598 / +685 / +740 $

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- **Démo FTMO sur VPS** : installer le bot [[live/README]] sur le VPS Contabo (Windows requis), deux essais gratuits MT5, `--signaux` puis `live\lancer.bat A` / `B` ; renouveler les essais tous les 14 jours ; compléter `live/annonces.csv` (PIB 2027, minutes Fed).
- **Plan FTMO retenu (2026-11-04)** : compte A = mom, compte B = 3n + M2, règle des annonces + cible + attente, éval 2,5 % / financé 1 %, scaling 10k → 400k ; détail dans [[wiki/experiments/propfirm-ftmo-option]] (section « Plan retenu »).
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
