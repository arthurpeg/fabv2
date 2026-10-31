"""Pré-enregistrement n° 18, avenant E : FTMO 1-Step, éval sur la règle NQ de nuit (TP 5 ATR, 2 %),
financé sur la même règle avec TP 4 ATR = 2 R (1 % risqué, 2 % visés).

uv run python run_propfirm_rr2.py [N]  → results/propfirm_rr2/ (run.log, metrics.csv)
Trades TP 4 : cache/propfirm/nq_nuit_tp4.parquet (build_nq_nuit_tp.py 4). Moteur : propfirm.ftmo.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.ftmo import EUR, PRICES_EUR, Market, TradeLib, run_eval, run_funded

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/propfirm_rr2")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
SEED = 1820
P_REF = 25_684.0
COSTS = {"1,5 pt": 1.5 / P_REF, "3 pt": 3.0 / P_REF}
R_EVAL, R_FUND = 2.0, 1.0


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def lib(path_or_df, sub=None, demean=False) -> TradeLib:
    t = path_or_df.sort_values("entry_idx")
    if sub is not None:
        t = t[t.night < sub]
    R = t.R_brut.to_numpy()
    return TradeLib(t.night.values, t.risk.fillna(t.risk.median()).to_numpy(), R - R.mean() if demean else R)


def main() -> None:
    t5 = pd.read_csv("results/couts_reels_nq_nuit/trades.csv", parse_dates=["night"])
    t4 = pd.read_parquet("cache/propfirm/nq_nuit_tp4.parquet")
    cases = {  # nom : (éval, financé)
        "financé RR 2 (TP 4 ATR)": (lib(t5), lib(t4)),
        "financé RR 2,5 (TP 5 ATR, avenant C)": (lib(t5), lib(t5)),
        "sans edge, financé RR 2": (lib(t5, demean=True), lib(t4, demean=True)),
        "2011-2015, financé RR 2": (lib(t5, "2016-01-01"), lib(t4, "2016-01-01")),
    }
    say(f"Avenant E — FTMO 1-Step, éval 2 % (TP 5 ATR), financé 1 % ; {N} comptes, graine {SEED}")
    rng = np.random.default_rng(SEED)
    rows = []
    for name, (le, lf) in cases.items():
        for c, frac in COSTS.items():
            if c != "1,5 pt" and not name.startswith("financé RR 2 "):
                continue
            ok, d = run_eval(Market(le, np.nan, frac), R_EVAL, 0.0, N, rng)
            paid, n, life, first = run_funded(Market(lf, np.nan, frac), R_FUND, 0.0, N, rng)
            p, v = ok.mean(), paid.mean()
            se_p, se_v = np.sqrt(p * (1 - p) / N), paid.std() / np.sqrt(N)
            row = dict(cas=name, coût=c, passage=p, nuits_éval_validée=d[ok].mean(), nuits_par_tentative=d.mean(),
                       valeur_financé_pct=v, p_reward=(n > 0).mean(), rewards_moy=n.mean(),
                       reward_moyen_pct=paid.sum() / max(n.sum(), 1), premier_reward_méd=np.median(first[first > 0]),
                       vie_financé=life.mean(), vie_méd=np.median(life), p_500=(life >= 500).mean(),
                       gain_par_nuit_financé_pct=v / life.mean())
            for size in (10_000, 100_000):
                fee = PRICES_EUR[size] * EUR
                row[f"EV_{size // 1000}k"] = p * v / 100 * size - fee
                row[f"IC_{size // 1000}k"] = 1.96 * size / 100 * np.sqrt((v * se_p) ** 2 + (p * se_v) ** 2)
                row[f"refus_max_{size // 1000}k"] = 1 - fee / (p * v / 100 * size)
            rows.append(row)
            say(f"\n=== {name}, coût {c} ===")
            say(f"  éval : passage {p:.1%} ± {1.96 * se_p:.1%}, {row['nuits_éval_validée']:.1f} nuits si validée, "
                f"{d.mean():.1f} par tentative")
            say(f"  financé : valeur {v:.2f} % ± {1.96 * se_v:.2f} du capital, P(≥ 1 reward) {row['p_reward']:.0%}, "
                f"{n.mean():.2f} rewards, reward moyen {row['reward_moyen_pct']:.2f} %, 1er reward méd. "
                f"{row['premier_reward_méd']:.0f} nuits, vie moy. {life.mean():.0f} (méd. {np.median(life):.0f}) nuits, "
                f"encore en vie à 500 nuits {row['p_500']:.0%}, {row['gain_par_nuit_financé_pct'] * 100:.1f} pb du capital par nuit")
            say(f"  EV : 10k {row['EV_10k']:+,.0f} $ ± {row['IC_10k']:,.0f} (refus tolérés {row['refus_max_10k']:.0%}) ; "
                f"100k {row['EV_100k']:+,.0f} $ ± {row['IC_100k']:,.0f} ({row['refus_max_100k']:.0%})".replace(",", " "))
    pd.DataFrame(rows).to_csv(OUT / "metrics.csv", index=False)


if __name__ == "__main__":
    main()
