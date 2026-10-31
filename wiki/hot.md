---
type: hot
updated: 2026-10-31 17:39
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 485** (source : [[reports/prereg19_report]])
- Dernier pré-enregistrement : n° 19 ([[PREREGISTRATION_19]])
- Idées abandonnées au registre : 25 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-10-31

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-10-31] prereg | N° 19 : S1 + stop dur 1R (plancher 0,5 %, 1 NQ) hors échantillon, trades 2010-09 → 2015-12 (run_prereg19.py) | ÉCHEC : +0,030 R/trade [−0,026 ; +0,090], p = 0,15 ; sous-périodes +0,005 / +0,052 ; Sharpe $ 0,57 (2016–2026 : 1,12) ; le stop n'apporte rien (S1 d'origine 0,55) ; au coût MNQ +0,004 R ; compteur 1 485
- [2026-10-31] query | Exploratoire : ferme FTMO 10k, un signal par compte (19:00 / 20:00 / 21:00), vectorbt + règles FTMO (run_propfirm_farm_heures.py) | mois sans reward 58 % → 42 %, corr. trimestrielle 1,00 → 0,56, creux moyen −300 → −238 $ ; écart-type sur 2 ans inchangé (1 885 → 1 880 $/compte) ; gain moyen 4 766 → 4 270 $
- [2026-10-31] query | S1 Noise Area NQ + stop dur 1R (fichier S1_R_stop.py transmis) refait avec vectorbt (run_s1_r_stop_vbt.py), 2016-01 → 2026-08-28 | S1 d'origine 1 827 trades (1 828 annoncés), Sharpe $ 1,03 ; plancher 0,5 % + stop 1R, 1 MNQ : +0,106 R/trade (t 4,0), Sharpe en R 1,26, +2 406 $/an, pire baisse 2 521 $ ; risque 500 $ : +7 932 $/an, pire baisse 5 800 $ ; boucle d'origine reproduite trade par trade (écarts ≤ 0,09 $) ; plancher choisi après coup, hors compteur, M2 reste rejetée
- [2026-10-31] query | Règle NQ de nuit, entrée 19:00 / 20:00 / 21:00 ET recalculée avec vectorbt (run_nq_nuit_heures.py), corrélations | R net +0,076 / +0,088 / +0,083, Sharpe 0,91 / 1,00 / 0,87 ; corr. par nuit 0,85 / 0,78 / 0,70 ; panier égal Sharpe 1,01 ; descriptif, hors compteur
- [2026-10-31] query | Exploratoire 2026 (run_propfirm_2026.py) : FTMO 10k, règle NQ de nuit, 1 éval puis 1 de plus par reward, du 2026-01-02 au 2026-08-28 | à la lettre : 2 évals, 1 reward, net +346 $ ; avec rachat après échec : 29 évals, 7 rewards, net +1 574 $ (8 financés ouverts à −3,68 %)
- [2026-10-31] query | Avenant E refait avec vectorbt (run_propfirm_vbt.py) : rendements de chaque nuit par Portfolio.from_signals, règles FTMO en Python | Monte-Carlo identique (EV +1 009 $ 10k, +10 408 $ 100k) ; pires séries identiques (6 évals ratées, 239 nuits sans reward) ; contrôle tailles réelles à 3e-11 $ ; tolérance 0,001 % et marge mini 0,05 % ajoutées aux scripts de trace, pires valeurs inchangées
- [2026-10-31] query | En cours : contrôle vectorbt de la trace FTMO avenant E (run_propfirm_vbt.py) | vectorbt exécute les 3 708 trades prévus, P&L à ≤ 0,0145 $ du calcul Python ; le rejeu des règles bifurque encore sur des seuils à quelques millionièmes (MIN_RISK 0,05 % le 2023-11-01) ; tolérances ajoutées aussi à run_propfirm_streaks.py, ses résultats sont à relancer
- [2026-10-31] prereg | N° 18 avenant E : FTMO, financé en RR 2 (TP 4 ATR, 1 %) sur la règle NQ de nuit | EV +1 009 $ ± 21 (10k), +10 408 $ (100k), +14 % contre RR 2,5 ; pires séries : 6 évals ratées, 239 nuits sans reward (2022) ; hors compteur

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
