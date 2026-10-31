"""Pré-enregistrement n° 18, avenant C : la règle NQ de nuit sur un compte FTMO 1-Step.

uv run python run_propfirm_nq_nuit.py [N]  → results/propfirm_nq_nuit/ (run.log, eval.csv, funded.csv, ev.csv)

Trades : results/couts_reels_nq_nuit/trades.csv (compte 20:00 ET, momentum 12-1, SL 2 ATR / TP 5 ATR,
sortie 9:30 ET), R brut et distance du stop. Un trade = une journée FTMO ; chaque compte part d'un trade
tiré au hasard et enchaîne les suivants. Coût CFD en points au niveau actuel du NQ. Moteur : propfirm.ftmo.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.ftmo import PRICES_EUR, Market, TradeLib, ev, refusal_breakeven, run_eval, run_funded

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/propfirm_nq_nuit")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
SEED = 1818

P_REF = 25_684.0
COSTS = {"1,5 pt": 1.5 / P_REF, "3 pt": 3.0 / P_REF}
EVAL_R = (0.5, 1.0, 1.5, 2.0, 2.5)
FUNDED_R = (0.25, 0.5, 1.0, 1.5, 2.0)
MAIN = dict(lib="règle 2011-2026", cost="1,5 pt", ev=2.0, fd=1.0)


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def main() -> None:
    t = pd.read_csv("results/couts_reels_nq_nuit/trades.csv", parse_dates=["night"]).sort_values("entry_idx")
    t["risk"] = t.risk.fillna(t.risk.median())  # 2 trades à R = 0 sans ATR (2014-05-28, 2016-12-15) : seul le coût en dépend
    full = TradeLib(t.night.values, t.risk.to_numpy(), t.R_brut.to_numpy())
    oos = t[t.night < "2016-01-01"]
    libs = {
        "règle 2011-2026": full,
        "sans edge (R − moyenne)": TradeLib(full.dates, full.s, full.R - full.R.mean()),
        "règle 2011-2015 (OOS)": TradeLib(oos.night.values, oos.risk.to_numpy(), oos.R_brut.to_numpy()),
    }
    say(f"Avenant C — règle NQ de nuit sur FTMO 1-Step ; {N} comptes par réglage, graine {SEED}")
    for k, lib in libs.items():
        say(f"  {k} : {lib.n} trades, R brut moyen {lib.R.mean():+.3f}, stop médian {np.median(lib.s):.3%} du prix, "
            + ", ".join(f"coût {c} {np.median(f / lib.s):.3f} R" for c, f in COSTS.items()))

    rng = np.random.default_rng(SEED)
    E, F = [], []
    for k, lib in libs.items():
        for c, frac in COSTS.items():
            m = Market(lib, np.nan, frac)
            say(f"\n=== {k}, coût {c} ===")
            for r in EVAL_R:
                ok, d = run_eval(m, r, 0.0, N, rng)  # t ignoré : objectif fixé par la règle
                p = ok.mean()
                E.append(dict(lib=k, cost=c, r=r, p_pass=p, se_p=np.sqrt(p * (1 - p) / N),
                              days_pass=d[ok].mean(), days_all=d.mean()))
                say(f"  éval {r:>4} % : passage {p:.1%} ± {1.96 * E[-1]['se_p']:.1%}, "
                    f"{E[-1]['days_pass']:.1f} trades si validé, {d.mean():.1f} par tentative")
            for reset in (True, False):
                for r in FUNDED_R:
                    paid, n, d, first = run_funded(m, r, 0.0, N, rng, reset=reset)
                    F.append(dict(lib=k, cost=c, r=r, reset=reset, v_pct=paid.mean(), se_v=paid.std() / np.sqrt(N),
                                  p_reward=(n > 0).mean(), n_rewards=n.mean(), life=d.mean(),
                                  first_med=np.median(first[first > 0]) if (first > 0).any() else np.nan))
                    x = F[-1]
                    say(f"  financé {r:>4} % {'RAZ' if reset else 'sans RAZ'} : valeur {x['v_pct']:.2f} % ± "
                        f"{1.96 * x['se_v']:.2f}, P(reward) {x['p_reward']:.0%}, {x['n_rewards']:.2f} rewards, "
                        f"vie {x['life']:.0f} trades, 1er reward méd. {x['first_med']:.0f}")
    E, F = pd.DataFrame(E), pd.DataFrame(F)
    E.to_csv(OUT / "eval.csv", index=False)
    F.to_csv(OUT / "funded.csv", index=False)

    rows = []
    for (k, c), e in E.groupby(["lib", "cost"], sort=False):
        for reset in (True, False):
            f = F[(F.lib == k) & (F.cost == c) & (F.reset == reset)]
            main = "principal" if (k, c) == (MAIN["lib"], MAIN["cost"]) else "même réglage"
            picks = {main: (e[e.r == MAIN["ev"]].iloc[0], f[f.r == MAIN["fd"]].iloc[0]),
                     "meilleur de la grille": (e.loc[e.p_pass.idxmax()], f.loc[f.v_pct.idxmax()])}
            for which, (ee, ff) in picks.items():
                for size in PRICES_EUR:
                    x, ci = ev(ee.p_pass, ee.se_p, ff.v_pct, ff.se_v, size)
                    rows.append(dict(lib=k, cost=c, reset=reset, choix=which, eval_r=ee.r, funded_r=ff.r,
                                     p_pass=ee.p_pass, v_pct=ff.v_pct, size=size, ev_usd=x, ci95=ci,
                                     refus_max=refusal_breakeven(ee.p_pass, ff.v_pct, size)))
    V = pd.DataFrame(rows)
    V.to_csv(OUT / "ev.csv", index=False)
    say("\n=== Espérance par tentative (10k et 100k) ===")
    for _, x in V[V["size"].isin([10_000, 100_000])].iterrows():
        say(f"  {x.lib:<24} {x.cost:<6} {'RAZ' if x.reset else 'sans RAZ':<8} {x.choix:<22} éval {x.eval_r:<4} "
            f"financé {x.funded_r:<4} {x['size'] // 1000:>3}k : EV {x.ev_usd:+8_.0f} $ ± {x.ci95:_.0f} "
            f"(passage {x.p_pass:.1%}, financé {x.v_pct:.2f} %, refus max {x.refus_max:.0%})".replace("_", " "))


if __name__ == "__main__":
    main()
