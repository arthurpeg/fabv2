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

## Ce qu'on sait
- Le signal est intermittent : fort sur 2016-2021 (t 4,3), nul sur 2022-2024 (t 1,1 sans stop), de retour sur 2025-2026 (t 2,1).
- Le stop ne change pas l'E[R]. Il plafonne la pire nuit (−3 629 $ au lieu de −12 715 $) et coupe le max DD d'environ 40 %.
- Deux pièges sont documentés dans le rapport : la séance calculée sur un index tz-aware perd le lundi qui suit le passage à l'heure d'hiver, et vectorbt teste le stop sur toute la barre de sortie avant la sortie à l'open.

## Ouvert
- Rien n'est pré-enregistré, et la sélection du filtre n'est pas corrigée (pas de DSR). À pré-enregistrer sur le holdout postérieur au 2026-08-28 avant tout usage.
- Corrélation avec la [[wiki/experiments/nq-nuit-momentum|règle NQ de nuit]] : les fenêtres se recouvrent.
- Stratégie 2 du zip (EMA 9:30) : pas encore refaite.

## Sources brutes
[run_nq_nuit_3n_vbt.py](../../run_nq_nuit_3n_vbt.py), `results/nq_nuit_3n/` (`run.log`, `comparaison.csv`, trades), `results/nq_nuit_3n/replique/`.
