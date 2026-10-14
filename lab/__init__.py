"""Labo de stratégies à signaux, backtestées dans vectorbt.

Indépendant du protocole pré-enregistré de `fab/` : ici on itère librement.
Réutilise uniquement les données (`fab.core.load`) et les coûts (`Asset.rt_cost`).
"""

from lab.engine import bars, run, report

__all__ = ["bars", "run", "report"]
