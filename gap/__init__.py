"""Gap d'ouverture du DAX prédit par les courbes étrangères de la nuit.

Protocole : PREREGISTRATION_5.md (amendement 1). Paramètres : config/opening_gap.toml.

- `calendar`    : sessions, jours fériés, instants de décision (UTC) ;
- `data`        : chargement (Databento, HistData), courbes 5 min, cibles A′ et B ;
- `features`    : courbes normalisées, ACP fonctionnelle, rendements ;
- `models`      : MCO et NP-FDA (moyenne, médiane, mode, CPI) ;
- `walkforward` : validation glissante et audit anti-fuite ;
- `signals`     : règles de trading ;
- `backtest`    : exécution vectorbt, références, métriques, permutations, DSR.
"""

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_config(path: str | Path = ROOT / "config" / "opening_gap.toml") -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)
