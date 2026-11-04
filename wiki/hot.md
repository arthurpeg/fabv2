---
type: hot
updated: 2026-11-04 19:41
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

- [2026-11-04] query | Probabilité de toucher un payout en démarrant le plan retenu avec deux comptes 10k (run_ftmo_proba_payout.py, reports/ftmo_proba_payout_report.md, exploratoire, hors compteur) | 1re éval de chaque compte : au moins un payout 79 % (A 47 %, B 61 %) ; ≤ 2 évals par compte 97 % ; ≤ 3 évals 99,7 % ; ≤ 5 évals (dépôt 869 $) 100 % ; espérance / 2 : 62 / 84 / 94 / 99 % ; 1er payout médian en 30 séances
- [2026-11-04] build | Bot de démo : suivi du P&L tous essais FTMO additionnés (live/pnl.py → live/etat/pnl.md : P&L cumulé, compte continu, creux, par stratégie et par essai, résultat FTMO virtuel), numéro d'essai MT5 sur chaque trade, alertes nouvel essai / trading désactivé / objectif de l'essai (5 %, 1-Step) / essai à −8 % | 13 tests verts (rejeu avec changement d'essai le 15/08 : cumul et compte virtuel continus)
- [2026-11-04] fix | Bot de démo : stop et objectif posés au même prix moyen que le backtest (stop à dist + spread du prix d'exécution, objectif à k·dist − spread), après le test d'ordre réel sur les deux essais FTMO (taille 1,05 / 0,52 lot, perte au stop 2,50 / 2,47 %, SL / TP posés, P&L lu) | 9 tests verts ; déployé par la mise à jour automatique
- [2026-11-04] build | Mise à jour automatique du bot sur le VPS : tâche planifiée toutes les 5 min (live/maj_auto.ps1), git pull en avance rapide, tests du bot avant d'adopter le code (retour arrière sinon), redémarrage propre des bots par drapeau ; option --test-ordre (ordre test au lot minimum) | testé sur un dépôt simulé : mise à jour valide appliquée, mise à jour cassée refusée et annulée, doc seule sans redémarrage
- [2026-11-04] build | Bot de démo FTMO sur VPS : MT5 + Python, book A (mom) et B (3n + M2), compte FTMO virtuel, règle des annonces avec calendrier BLS / Fed relu (live/, tests/test_live.py, tests/test_live_bot.py) | signaux et compte identiques au backtest (78 tests verts) ; reste à installer sur le VPS Contabo (Windows requis) et à créer les deux essais FTMO
- [2026-11-04] decision | Plan FTMO retenu par l'utilisateur : compte A = mom, compte B = 3n + M2 (M2 si 3n n'a pas tradé ou est sorti à 03:00), éval 2,5 % avec objectif réduit, financé 1 %, règle des annonces, cible + attente, scaling 10k → 400k (wiki/experiments/propfirm-ftmo-option.md, section « Plan retenu » ; mémoire ftmo-plan-retenu) | à utiliser par défaut dans les prochaines conversations
- [2026-11-04] query | Métriques complètes de la montée en taille FTMO 10k → 100k (run_ftmo_scaling_metrics.py, reports/ftmo_scaling_report.md, section métriques) | 400k en 12,0 mois médian (MC historique) / 17,7 (edge / 2) ; ruine 0,2 % / 2,5 % ; cagnotte à 5 ans 375 k$ / 212 k$ ; revenu mensuel à 400k ≈ 7 700 $ / 5 000 $, mois négatifs 11 % / 22 % ; max DD de cagnotte médian −3 293 $ / −5 489 $ ; frais ≈ 18 k$ / 28 k$ sur 5 ans
- [2026-11-04] query | Contrôle du moteur FTMO Python par vectorbt : compte A (mom) du chemin historique rejoué avec les tailles, stops, objectifs et coupes d'annonce décidés par le moteur (journal ajouté à Compte ; run_ftmo_verif_vbt.py, reports/ftmo_verif_vbt_report.md) | 3 639 / 3 646 trades identiques au centime ; 7 écarts (objectif réduit franchi par un gap : vectorbt exécute à l'ouverture, plus favorable, max 6,18 $) ; P&L total +32 724 $ (moteur) contre +32 746 $ (vectorbt) : moteur validé, légèrement prudent

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
