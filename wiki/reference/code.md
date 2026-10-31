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
| `tests/` | pytest (`uv run pytest`) | — |

Lancer : `uv run python <script>.py`.
