# ml/ — machine learning sur les anomalies confirmées

Branche `ml` (mère : `strategies-vbt`, donc tous les backtests et leurs générateurs de trades sont importables).

But : améliorer, par un modèle appris, les anomalies significatives de `wiki/phenomenes.md` que les filtres classiques n'ont pas améliorées. Fiche d'idée, candidates et règles propres au ML : `wiki/experiments/ml-anomalies.md`.

Règles (en plus de `PROTOCOLE.md`) :
- grille modèle × variables × hyperparamètres commitée avant calcul ; chaque case compte dans le compteur d'essais ;
- validation chronologique avec purge et embargo, jamais de donnée de réserve (`wiki/reserves.md`) ni de holdout ouvert ;
- toujours comparer à la règle brute et au meilleur filtre classique déjà testé ;
- intraday uniquement : toute position ouverte un jour est fermée le même jour.

Dépendances ML (scikit-learn, LightGBM…) : dans le groupe `ml` de `pyproject.toml` (`uv add --group ml <paquet>`), jamais dans les dépendances par défaut : le VPS ne les installe pas et ne relance pas les bots quand ce groupe change (`live/maj_auto.ps1`). Lancer les scripts avec `uv run --group ml python ...`.
