---
type: hot
updated: 2026-10-31 16:02
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 482** (source : [[reports/prereg17_report]])
- Dernier pré-enregistrement : n° 18 ([[PREREGISTRATION_18]])
- Idées abandonnées au registre : 24 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-10-31

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-10-31] prereg | N° 18 avenant D : règle NQ de nuit sur LucidFlex 50K en MNQ (règles lues sur lucidtrading.com), éval 400 $ / financé 200 $ | EV +157 $ ± 6 par éval au prix actuel du NQ (+65 $ en points historiques, protocole) ; sans edge −55 $ ; hors compteur
- [2026-10-31] query | Exploratoire : 5 comptes FTMO 10k décalés de 1 ou 3 mois sur la règle NQ de nuit (run_propfirm_farm.py) | ne lisse pas : écart-type ~2 000 $/compte sur 2 ans (indépendants : 873 $) ; 4,1/5 rachètent la même nuit, corrélation 0,97
- [2026-10-31] query | Vérification des règles FTMO 1-Step sur ftmo.com (perte max, RAZ après reward, perte journalière, meilleur jour, reward au 14e jour) | toutes conformes au simulateur du n° 18 ; RAZ confirmée (« fully resets ») ; « does not reset » = Instant Account
- [2026-10-31] prereg | N° 18 avenant C : règle NQ de nuit (3 787 trades 2011-2026) sur FTMO 1-Step, éval 2 % / financé 1 %, spread 1,5 pt | passage 50,8 %, EV +853 $ (10k), +8 849 $ (100k) ; sans edge +98 $ / +1 295 $ ; sans RAZ +307 $ / +3 390 $ ; hors compteur
- [2026-10-31] fix | Renommage costs18 → couts_reels_nq_nuit (script, rapport, résultats) pour éviter la confusion avec le pré-enregistrement n° 18 (FTMO) | liens mis à jour
- [2026-10-31] prereg | N° 18 avenant B : entrée 9:50 ET, stop 1 ATR M15, spread 1,5 pt (0,041 R) / 1 pt | EV +161 $ ± 6 (10k), +1 933 $ ± 61 (100k) à 1,5 pt ; +187 $ / +2 187 $ à 1 pt ; hors compteur
- [2026-10-31] experiment | Règle NQ de nuit recalculée avec les spreads réels bbo-1m (NQ 2011-2026, MNQ 2019-2026) | +0,076 R/trade contre +0,088 au coût fixe ; MNQ +0,067 à 1,24 $ A/R ; compteur inchangé
- [2026-10-31] prereg | N° 18 avenant A : stop 1 ATR M15 (≈ 0,12 % du prix) au lieu de 0,5 % | EV +71 $ ± 4 (10k), +1 035 $ ± 43 (100k) ; le spread 1 pb (0,083 R/trade) explique tout l'écart (sans coût +3 023 $) ; hors compteur

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
