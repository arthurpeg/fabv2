"""Lance les 42 réplications fidèles (PREREGISTRATION_3.md) → results/replications.csv"""

import sys
import time

import pandas as pd

from fab.core import summarize
from fab.replications import registry


def main(args):
    rows, daily = [], {}
    tests = [t for t in registry() if not args or t[0].startswith(args[0])]
    for rid, a, make in tests:
        t0 = time.time()
        res = make()
        res.name = rid
        row = summarize(res)
        rows.append(row)
        daily[f"{rid}|{a.name}"] = res.daily_net
        print(f"{rid:22s} {a.name:3s} n={row['n_trades']:5d} "
              f"SR net IS={row['sharpe_net_IS']:+.2f} OOS={row['sharpe_net_OOS']:+.2f} "
              f"| brut IS={row['sharpe_gross_IS']:+.2f} OOS={row['sharpe_gross_OOS']:+.2f} "
              f"| ticks brut={row['avg_ticks_gross']:+.2f} coût={row['cost_ticks']:.1f} "
              f"{'SURVIT' if row['survives'] else ''} ({time.time() - t0:.0f}s)", flush=True)
    if not args:
        pd.DataFrame(rows).to_csv("results/replications.csv", index=False, float_format="%.4f")
        pd.DataFrame(daily).to_parquet("results/replications_daily_net.parquet")
    print(f"\n{len(rows)} réplications, {sum(r['survives'] for r in rows)} survivantes")


if __name__ == "__main__":
    main(sys.argv[1:])
