---
type: experiment
updated: 2026-11-03
status: running
verdict: candidat externe (non pré-enregistré)
prereg: []
trials: hors compteur
---

# NQ overnight long 20:05 → 03:00, filtre 3 nuits (stratégie transmise)

**Une phrase** : être long NQ de 20:05 à 03:00 ET seulement si la somme des 3 nuits précédentes est ≤ 0. Avec un stop à 2 × ATR M15, le backtest vectorbt refait donne un Sharpe de 1,36 sur 2016-2024 et de 1,59 sur 2025 → 08/2026, ce qui confirme le rapport d'origine (1,36 / 1,63).

## Origine
Stratégie transmise le 2026-11-03 (`scripts_strategies_NQ.zip` + artefact « Rapport NQ overnight » du 02/11/2026), elle-même reprise d'un post. Le filtre a été choisi par son auteur parmi plusieurs candidats (ATR, range, nuit précédente, 3 nuits, rendement de jour).

## Tests
| Test | Résultat | Rapport |
|---|---|---|
| Backtest refait avec vectorbt, réplique exacte | Chiffres d'origine retrouvés à 0,01 près ; sorties vectorbt = boucle sur tous les trades | [[reports/nq_nuit_3n_vbt_report]] |
| Version corrigée (nuits du changement d'heure, stop vectorbt sur la barre de sortie) | 3n SL : Sharpe 1,36 IS / 1,59 OOS, t NW 4,39 / 2,17, max DD 12 418 $ / 8 301 $ | idem |
| Comparaison avec la règle NQ de nuit (même coût, en R) | 2016-2026 : 3n SL Sharpe 1,42 contre 0,90 (mom), mais 0,48 contre 0,83 sur 2022-2024 ; corrélation par nuit +0,35 ; mom fait +7,5 bps les nuits « 3n long » contre −0,8 sinon (2016-2024), inversé en 2025-26 | [[reports/nq_nuit_3n_vs_mom_report]] |
| Sortie à 08:00 au lieu de 03:00, et contre mom | Chiffres d'origine retrouvés ; 08h SL : +3,7 R/an mais Sharpe 1,24 contre 1,36 (IS), DD +54 % en $ ; tranche 03→08 sans avantage (t 0,9) ; corrélation avec mom +0,39 contre +0,29 : 03h reste la version retenue | [[reports/nq_nuit_3n_8h_report]] |
| La nuit baisse-t-elle d'autant plus que r3 > 0 est grand ? | ❌ non significatif dans 6 échantillons (Holm 1,0) ; l'effet est asymétrique : rebond après forte baisse (décile bas de r3 positif partout, t 2-3,7), nuit ≈ 0 après des hausses | [[reports/nq_nuit_r3_pente_report]] |
| FTMO 1-Step (réglages de l'avenant C) contre mom | +2 499 $ / tentative 10k contre +468 $ (mom 2016-26) ; par mois d'emplacement, mom fait plus (+1 814 $ contre +1 164 $ sur 100k), car 3n ne trade que 109 nuits par an ; jamais exposée à la règle des annonces | [[reports/propfirm_3n_vs_mom_report]] |

## Ce qu'on sait
- Le signal est intermittent : fort sur 2016-2021 (t 4,3), nul sur 2022-2024 (t 1,1 sans stop), de retour sur 2025-2026 (t 2,1).
- Le stop ne change pas l'E[R]. Il plafonne la pire nuit (−3 629 $ au lieu de −12 715 $) et coupe le max DD d'environ 40 %.
- Deux pièges sont documentés dans le rapport : la séance calculée sur un index tz-aware perd le lundi qui suit le passage à l'heure d'hiver, et vectorbt teste le stop sur toute la barre de sortie avant la sortie à l'open.

## Ouvert
- Rien n'est pré-enregistré, et la sélection du filtre n'est pas corrigée (pas de DSR). À pré-enregistrer sur le holdout postérieur au 2026-08-28 avant tout usage.
- Pas indépendante de la [[wiki/experiments/nq-nuit-momentum|règle NQ de nuit]] : même retour à la moyenne (piste F2 du n° 13). Une combinaison doit être pré-enregistrée sur le holdout.
- Stratégie 2 du zip (EMA 9:30) : pas encore refaite.

## Sources brutes
[run_nq_nuit_3n_vbt.py](../../run_nq_nuit_3n_vbt.py), `results/nq_nuit_3n/` (`run.log`, `comparaison.csv`, trades), `results/nq_nuit_3n/replique/`.
