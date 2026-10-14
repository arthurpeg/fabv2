"""Une stratégie = une fonction `(bars, **params) -> lab.engine.Signals`.

Ajouter un fichier ici et l'enregistrer dans `REGISTRY` (paramètres par défaut,
pour `run_strategies.py`) et dans `GRIDS` (grille + contrainte éventuelle, pour
`optimize_strategies.py`).
"""

from strategies.donchian import donchian
from strategies.rsi_reversion import rsi_reversion
from strategies.sma_cross import sma_cross

# nom → (fonction, paramètres par défaut)
REGISTRY = {
    "sma_cross": (sma_cross, {"fast": 20, "slow": 100}),
    "rsi_reversion": (rsi_reversion, {"n": 14, "low": 30, "high": 70}),
    "donchian": (donchian, {"n": 55, "exit_n": 20}),
}

# nom → (grille, contrainte sur une combinaison ou None)
GRIDS = {
    "sma_cross": (
        {"fast": [5, 10, 20, 50], "slow": [50, 100, 200, 400]},
        lambda c: c["fast"] < c["slow"],
    ),
    "rsi_reversion": (
        {"n": [7, 14, 21], "low": [20, 25, 30, 35], "high": [65, 70, 75, 80]},
        lambda c: c["low"] + c["high"] == 100,  # seuils symétriques
    ),
    "donchian": (
        {"n": [20, 55, 100, 200], "exit_n": [10, 20, 50]},
        lambda c: c["exit_n"] < c["n"],
    ),
}
