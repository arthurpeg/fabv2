---
type: hot
updated: 2026-10-31 16:26
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

- [2026-10-31] query | En cours : contrôle vectorbt de la trace FTMO avenant E (run_propfirm_vbt.py) | vectorbt exécute les 3 708 trades prévus, P&L à ≤ 0,0145 $ du calcul Python ; le rejeu des règles bifurque encore sur des seuils à quelques millionièmes (MIN_RISK 0,05 % le 2023-11-01) ; tolérances ajoutées aussi à run_propfirm_streaks.py, ses résultats sont à relancer
- [2026-10-31] prereg | N° 18 avenant E : FTMO, financé en RR 2 (TP 4 ATR, 1 %) sur la règle NQ de nuit | EV +1 009 $ ± 21 (10k), +10 408 $ (100k), +14 % contre RR 2,5 ; pires séries : 6 évals ratées, 239 nuits sans reward (2022) ; hors compteur
- [2026-10-31] query | Exploratoire : pires séries FTMO + règle NQ de nuit (run_propfirm_streaks.py, 657 départs) | 6 évals ratées d'affilée au pire (521 $ sur 10k) ; 11 mois sans reward (2018-03 → 2019-01) ; creux de trésorerie −608 $ (10k) / −3 842 $ (100k) ; cause : meilleur jour 50 % avec des TP de +2,5 %
- [2026-10-31] prereg | N° 18 avenant D : règle NQ de nuit sur LucidFlex 50K en MNQ (règles lues sur lucidtrading.com), éval 400 $ / financé 200 $ | EV +157 $ ± 6 par éval au prix actuel du NQ (+65 $ en points historiques, protocole) ; sans edge −55 $ ; hors compteur
- [2026-10-31] query | Exploratoire : 5 comptes FTMO 10k décalés de 1 ou 3 mois sur la règle NQ de nuit (run_propfirm_farm.py) | ne lisse pas : écart-type ~2 000 $/compte sur 2 ans (indépendants : 873 $) ; 4,1/5 rachètent la même nuit, corrélation 0,97
- [2026-10-31] query | Vérification des règles FTMO 1-Step sur ftmo.com (perte max, RAZ après reward, perte journalière, meilleur jour, reward au 14e jour) | toutes conformes au simulateur du n° 18 ; RAZ confirmée (« fully resets ») ; « does not reset » = Instant Account
- [2026-10-31] prereg | N° 18 avenant C : règle NQ de nuit (3 787 trades 2011-2026) sur FTMO 1-Step, éval 2 % / financé 1 %, spread 1,5 pt | passage 50,8 %, EV +853 $ (10k), +8 849 $ (100k) ; sans edge +98 $ / +1 295 $ ; sans RAZ +307 $ / +3 390 $ ; hors compteur
- [2026-10-31] fix | Renommage costs18 → couts_reels_nq_nuit (script, rapport, résultats) pour éviter la confusion avec le pré-enregistrement n° 18 (FTMO) | liens mis à jour

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
