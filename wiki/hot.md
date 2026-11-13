---
type: hot
updated: 2026-11-13 17:01
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 742** (source : [[reports/inference_overnight_report]])
- Dernier pré-enregistrement : n° 26 ([[PREREGISTRATION_26]])
- Idées abandonnées au registre : 35 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-06

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-06] query | Inférence des chiffres overnight (run_inference_overnight.py, reports/inference_overnight_report.md, exploratoire, compteur inchangé) : t HAC Newey-West, bootstrap par blocs, Ljung-Box, ARCH-LM, N effectif (Li & Ji), DSR avec N brut et effectif | t HAC > t iid partout (ρ1 négatif ; NQ close-to-open 3,12 → 3,51) ; ARCH massif en bp, absent en R ; N effectif ≈ 610 / 1 742 ; DSR mom 0,005 et NQ CTO 0,016 avec N ≈ 610 (≤ 0,53 avec V = 1/T) : la preuve de mom reste le hors échantillon du n° 11
- [2026-11-06] query | Version anglaise du document overnight en PDF (reports/overnight_research_en.pdf, 5 pages, généré par reportlab depuis un script du scratchpad) | traduction fidèle du document Claude Docs, aucun nouveau calcul
- [2026-11-06] query | Document overnight : ajout d'une section « L'hypothèse : une prime pour porter le risque de la nuit » (mécanisme de risque d'inventaire de Boyarchenko-Larsen-Whelan, 6 prédictions confrontées à nos résultats) | P1, P2 cohérents ; P3, P5 à surveiller ; P4 non démontré (n° 16, approximation VWAP) ; aucun nouveau calcul
- [2026-11-06] query | Document de synthèse de la recherche overnight (Claude Docs « Recherche overnight : hypothèses, protocole et résultats », https://claude.ai/artifact/Rm8gtyyPCG6zuoVtsPtN2m) : cadre, protocole, hypothèses testées, phénomènes significatifs, échecs, suite | rédigé à partir du wiki, aucun nouveau calcul, hors compteur
- [2026-11-05] query | Book C hypothétique sans edge (sens au hasard, nuits de mom, objectif 2 R) sur FundingPips 1 Step Flex 10k (prix supposé 116 $), en même temps que A et B chez FTMO (run_book_c.py, reports/book_c_report.md, exploratoire, hors compteur) | C seul : +1 125 $/an sur 2011-2026, perdant sur 12 mois dans 20 % des départs ; A + B + C : +24 % de gain (MC 3 ans +16,1 k$ contre +12,9 k$), max DD de trésorerie +50 % (99e c. −1 275 $ contre −782 $), corrélation C / A + B ≈ +0,1
- [2026-11-05] query | Scaling FTMO hypothétique jusqu'à 800k (3 puis 4 × 100k par stratégie ; run_ftmo_scaling_800k.py, paliers généralisés dans run_ftmo_scaling*.py ; reports/ftmo_scaling_800k_report.md, exploratoire, hors compteur) | 800k en 15,0 mois médian (MC historique), 21,2 (edge / 2) ; revenu à 800k ≈ 15 300 $ / mois (10 100 edge / 2) ; cagnotte à 5 ans +706 k$ / +395 k$ ; max DD médian −6,6 k$ ; ruine 1,1 / 5,9 %
- [2026-11-05] query | Sortie de mom avant les annonces de 8:30 (bot live/bot.py ev_mom) : en financé virtuel, sortie à 8:18:55 ET les jours NFP / CPI / PIB avancé de live/annonces.csv, sinon 9:29:57 ; en éval, pas de coupure (règle FTMO réservée au compte financé, comme le plan retenu) | vérifié par rejeu (test_book_A_finance_sort_avant_les_annonces : nuit allant à 9:29:57 fermée à 8:18:55 un jour d'annonce, autres nuits inchangées) ; nuit du 05 au 06/11 (NFP) en éval : gardée jusqu'à 9:29:57, conforme au plan
- [2026-11-05] fix | Règle anti-hedging FTMO : pas de 3n long sur le compte B une nuit où mom est short (ANTI_HEDGE dans run_ftmo_deux_comptes.py, bot live/bot.py ev_3n + test), toutes les simulations FTMO A + B relancées (reports/ftmo_anti_hedging_report.md) | 192 nuits sur 1 635 (11,7 %, 2016/2019/2020/2022/2023, aucune en 2026) ; net historique 2011-2026 +68,6 k$ → +66,8 k$ ; 1re éval au moins un validé 82,3 → 80,6 % ; 400k en 12,4 mois médian (12,0) ; 17 tests du bot verts

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
