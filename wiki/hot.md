---
type: hot
updated: 2026-10-31 17:49
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

- [2026-10-31] query | Plan FTMO : 10k puis 100k dès que les gains des 10k paient 1, 2 ou 3 trios d'évals 100k (run_propfirm_paths.py) | bascule ~10 / 13 / 18 mois ; +104 / +93 / +78 k$ médiane à 3 ans contre +67 k$ en paliers et +148 k$ en 100k d'emblée
- [2026-10-31] query | Chemin complet du plan FTMO (run_propfirm_paths.py, 612 départs, 3 ans) : paliers / 10k→100k / 100k d'emblée | 10k→100k jamais plus rapide ; 100k d'emblée : +148 k$ médiane à 3 ans contre +67 k$, meilleur dans 97 % des départs, apport max 1 374 $ en plus des 1 750 $ ; règle de réserve du plan initial trop prudente
- [2026-10-31] query | Plan de montée en taille FTMO (reports/plan_scaling_ftmo.md, run_propfirm_scaling.py) ; règles lues sur ftmo.com : 400 k$ max par trader ou stratégie, Scaling Plan +25 %/4 mois jusqu'à 2 M$ | trio 10k → 100k en 1,5 à 3 ans ; trio 100k +134 k$ sur 2 ans en moyenne, pire creux −11 k$
- [2026-10-31] prereg | N° 19 : S1 + stop dur 1R (plancher 0,5 %, 1 NQ) hors échantillon, trades 2010-09 → 2015-12 (run_prereg19.py) | ÉCHEC : +0,030 R/trade [−0,026 ; +0,090], p = 0,15 ; sous-périodes +0,005 / +0,052 ; Sharpe $ 0,57 (2016–2026 : 1,12) ; le stop n'apporte rien (S1 d'origine 0,55) ; au coût MNQ +0,004 R ; compteur 1 485
- [2026-10-31] query | Exploratoire : ferme FTMO 10k, un signal par compte (19:00 / 20:00 / 21:00), vectorbt + règles FTMO (run_propfirm_farm_heures.py) | mois sans reward 58 % → 42 %, corr. trimestrielle 1,00 → 0,56, creux moyen −300 → −238 $ ; écart-type sur 2 ans inchangé (1 885 → 1 880 $/compte) ; gain moyen 4 766 → 4 270 $
- [2026-10-31] query | S1 Noise Area NQ + stop dur 1R (fichier S1_R_stop.py transmis) refait avec vectorbt (run_s1_r_stop_vbt.py), 2016-01 → 2026-08-28 | S1 d'origine 1 827 trades (1 828 annoncés), Sharpe $ 1,03 ; plancher 0,5 % + stop 1R, 1 MNQ : +0,106 R/trade (t 4,0), Sharpe en R 1,26, +2 406 $/an, pire baisse 2 521 $ ; risque 500 $ : +7 932 $/an, pire baisse 5 800 $ ; boucle d'origine reproduite trade par trade (écarts ≤ 0,09 $) ; plancher choisi après coup, hors compteur, M2 reste rejetée
- [2026-10-31] query | Règle NQ de nuit, entrée 19:00 / 20:00 / 21:00 ET recalculée avec vectorbt (run_nq_nuit_heures.py), corrélations | R net +0,076 / +0,088 / +0,083, Sharpe 0,91 / 1,00 / 0,87 ; corr. par nuit 0,85 / 0,78 / 0,70 ; panier égal Sharpe 1,01 ; descriptif, hors compteur
- [2026-10-31] query | Exploratoire 2026 (run_propfirm_2026.py) : FTMO 10k, règle NQ de nuit, 1 éval puis 1 de plus par reward, du 2026-01-02 au 2026-08-28 | à la lettre : 2 évals, 1 reward, net +346 $ ; avec rachat après échec : 29 évals, 7 rewards, net +1 574 $ (8 financés ouverts à −3,68 %)

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
