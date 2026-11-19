"""Lance les 93 tests pré-enregistrés et écrit results/summary.csv.

    uv run python run_backtests.py            # tout
    uv run python run_backtests.py M1 ES      # filtre par préfixe de stratégie / actif
"""

import sys
import time
from pathlib import Path

import pandas as pd

from fab.core import backtest, summarize
from fab.strategies import registry

OUT = Path("results")


def main(args):
    OUT.mkdir(exist_ok=True)
    rows, daily = [], {}
    tests = registry()
    if args:
        tests = [t for t in tests if t[0].startswith(args[0]) and (len(args) < 2 or t[1].name == args[1])]
    for name, asset, make in tests:
        t0 = time.time()
        trades, tz, dates = make()
        res = backtest(name, asset, trades, tz, dates)
        row = summarize(res)
        rows.append(row)
        daily[f"{name}|{asset.name}"] = res.daily_net
        print(
            f"{name:22s} {asset.name:3s} n={row['n_trades']:5d} "
            f"SR net IS={row['sharpe_net_IS']:+.2f} OOS={row['sharpe_net_OOS']:+.2f} "
            f"| gross IS={row['sharpe_gross_IS']:+.2f} OOS={row['sharpe_gross_OOS']:+.2f} "
            f"| ticks gross={row['avg_ticks_gross']:+.2f} cost={row['cost_ticks']:.1f} "
            f"{'SURVIT' if row['survives'] else ''} ({time.time() - t0:.0f}s)",
            flush=True,
        )
    df = pd.DataFrame(rows)
    suffix = "" if not args else "_" + "_".join(args)
    df.to_csv(OUT / f"summary{suffix}.csv", index=False, float_format="%.4f")
    pd.DataFrame(daily).to_parquet(OUT / f"daily_net{suffix}.parquet")
    print(f"\n{len(df)} tests, {int(df['survives'].sum())} survivants")


if __name__ == "__main__":
    main(sys.argv[1:])
