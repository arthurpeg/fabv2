"""Une stratégie = une fonction `(bars, **params) -> lab.engine.Signals`.

Ajouter un fichier ici et l'enregistrer dans `REGISTRY` pour qu'il soit lancé
par `run_strategies.py`.
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
