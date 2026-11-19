"""Lance les stratégies de `strategies/` sur vectorbt.

    uv run python run_strategies.py                          # tout, défauts
    uv run python run_strategies.py -s donchian -a ES NQ -t 1D
    uv run python run_strategies.py -s sma_cross -a ES -t 1h --plot
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from fab.core import ASSETS
from lab.engine import report, run
from strategies import REGISTRY

OUT = Path(__file__).resolve().parent / "results" / "lab"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("-s", "--strategies", nargs="+", default=list(REGISTRY))
    p.add_argument("-a", "--assets", nargs="+", default=list(ASSETS))
    p.add_argument("-t", "--tf", nargs="+", default=["1h", "1D"])
    p.add_argument("--plot", action="store_true", help="sauve la courbe de capital (HTML)")
    args = p.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for s in args.strategies:
        fn, params = REGISTRY[s]
        for tf in args.tf:
            for a in args.assets:
                r = run(fn, a, tf, **params)
                rows.append(report(r))
                print(f"{s:15s} {a:3s} {tf:4s} SR IS {rows[-1]['sharpe_IS']:+.2f}  OOS {rows[-1]['sharpe_OOS']:+.2f}")
                if args.plot:
                    r.pf.plot().write_html(OUT / f"{s}_{a}_{tf}.html")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "summary.csv", index=False)
    with pd.option_context("display.width", 200, "display.max_columns", 30, "display.float_format", "{:.2f}".format):
        print(df.drop(columns=[c for c in df if c.startswith("p_")]).to_string(index=False))


if __name__ == "__main__":
    main()
