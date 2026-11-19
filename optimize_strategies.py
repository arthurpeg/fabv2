"""Optimisation de paramètres sur l'IS + correction DSR.

    uv run python optimize_strategies.py                         # toutes les grilles
    uv run python optimize_strategies.py -s donchian -a ES GC -t 1D
    uv run python optimize_strategies.py --extra-trials 200      # essais déjà faits ailleurs

`dsr_all` compte tous les essais de la session : lancer moins d'actifs ou de
grilles rend le test moins sévère. Si vous avez déjà regardé d'autres
résultats, ajoutez-les via --extra-trials.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from fab.core import ASSETS
from lab.optimize import grid_search, summarize
from strategies import GRIDS, REGISTRY

OUT = Path(__file__).resolve().parent / "results" / "lab"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("-s", "--strategies", nargs="+", default=list(GRIDS))
    p.add_argument("-a", "--assets", nargs="+", default=list(ASSETS))
    p.add_argument("-t", "--tf", nargs="+", default=["1h", "1D"])
    p.add_argument("--extra-trials", type=int, default=0)
    args = p.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for s in args.strategies:
        fn, _ = REGISTRY[s]
        grid, constraint = GRIDS[s]
        for tf in args.tf:
            for a in args.assets:
                r = grid_search(fn, a, tf, grid, constraint)
                results.append(r)
                print(f"{s:15s} {a:3s} {tf:4s} {len(r.trials):3d} essais, meilleur IS {r.best}")

    trials = pd.concat([r.trials.assign(strategy=r.strategy, asset=r.asset, tf=r.tf) for r in results])
    trials.to_csv(OUT / "opt_trials.csv", index=False)
    df = summarize(results, args.extra_trials)
    df.to_csv(OUT / "opt_best.csv", index=False)

    print(f"\nN essais total (DSR) = {df.attrs['n_trials']}, SR0 annualisé = {df['sr0_all_ann'].iat[0]:.2f}")
    with pd.option_context("display.width", 250, "display.max_columns", 30, "display.float_format", "{:.2f}".format):
        print(df.sort_values("dsr_all", ascending=False).to_string(index=False))
    print(f"\nPassent (DSR_all > 0.95 et SR OOS > 0) : {int(df['passes'].sum())}/{len(df)}")


if __name__ == "__main__":
    main()
