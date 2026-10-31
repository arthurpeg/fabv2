---
type: reference
updated: 2026-10-31
---

# Où est le code

Page d'aiguillage : un module par famille de tests, un `run_*.py` par exécution.

| Module | Rôle | Point d'entrée |
|---|---|---|
| `fab/` | chargement (`core.load`), stratégies du lot initial, réplications, DSR | [run_backtests.py](../../run_backtests.py), [run_replications.py](../../run_replications.py) |
| `gap/` | gap d'ouverture DAX : calendriers, alignement DST, NP-FDA | [run_opening_gap.py](../../run_opening_gap.py) |
| `fxreopen/`, `fxfix/` | reprise FX 18:00, fix de Londres | [run_fx_reopen.py](../../run_fx_reopen.py), [run_fx_fix.py](../../run_fx_fix.py) |
| `asym/`, `letf/` | Valenti, ETF à levier ; `asym.backtest` contient le test de permutation | [run_asym.py](../../run_asym.py), [run_letf.py](../../run_letf.py) |
| `recolte1/` | moteur et règles des papiers overnight, IC bootstrap | [run_recolte1.py](../../run_recolte1.py), [run_prereg10.py](../../run_prereg10.py) → 12, [run_robust13.py](../../run_robust13.py) |
| `coinflip/` | contrôle sans edge | [run_coinflip.py](../../run_coinflip.py) |
| `propfirm/` | prop firm comme option : moteurs FTMO 1-Step (`ftmo.py`), LucidFlex (`lucid.py`) et Smart Trader Funds 1 Phase (`stf.py`) | [run_propfirm_ftmo.py](../../run_propfirm_ftmo.py), [run_propfirm_nq_nuit.py](../../run_propfirm_nq_nuit.py), [run_propfirm_lucid.py](../../run_propfirm_lucid.py), [run_propfirm_lucid_plan.py](../../run_propfirm_lucid_plan.py), [run_propfirm_stf.py](../../run_propfirm_stf.py), [run_propfirm_rr2.py](../../run_propfirm_rr2.py), [run_propfirm_streaks.py](../../run_propfirm_streaks.py), [build_nq_nuit_tp.py](../../build_nq_nuit_tp.py) |
| (racine) | S1 Noise Area NQ + stop 1R, vectorbt contre boucle d'origine (exploratoire), puis n° 19 sur 2010-2015 | [run_s1_r_stop_vbt.py](../../run_s1_r_stop_vbt.py), [run_prereg19.py](../../run_prereg19.py) |
| `tests/` | pytest (`uv run pytest`) | — |

Lancer : `uv run python <script>.py`.
