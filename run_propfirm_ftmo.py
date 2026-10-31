"""Pré-enregistrement n° 18 : espérance d'une éval FTMO 1-Step avec des trades au hasard.

uv run python run_propfirm_ftmo.py [N]  → results/propfirm/ (run.log, eval.csv, funded.csv, ev.csv)

Modes : binaire (pile ou face gain t % / perte r %) et NQ réel (trajectoires 1 min du NQ,
entrée 9:35 ET, sortie 15:54 ET au plus tard, stop s % du prix). Voir propfirm/.
Bibliothèque de journées en cache : cache/propfirm/nq_days_<s>.pkl.
"""

from __future__ import annotations

import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.days import build, session_bars
from propfirm.ftmo import PRICES_EUR, Market, ev, refusal_breakeven, run_eval, run_funded

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/propfirm")
OUT.mkdir(parents=True, exist_ok=True)
CACHE = Path("cache/propfirm")
CACHE.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
SEED = 18

EVAL_GRID = [(r, t) for r in (1.0, 2.0, 2.9) for t in (2.0, 3.0, 4.9)]
FUNDED_GRID = [(0.5, 1.0), (0.5, 2.0), (0.75, 1.5), (1.0, 1.0), (1.0, 2.0)]
STOPS = (0.0025, 0.005, 0.01)
MAIN = dict(s=0.005, ev=(2.0, 4.9), fd=(1.0, 2.0))


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def libs() -> dict[float, object]:
    out, bars = {}, None
    for s in STOPS:
        f = CACHE / f"nq_days_{s:g}.pkl"
        if f.exists():
            out[s] = pickle.loads(f.read_bytes())
            continue
        bars = bars or session_bars("NQ")
        out[s] = build(bars, s)
        f.write_bytes(pickle.dumps(out[s]))
    return out


def eval_stats(m: Market, rng) -> list[dict]:
    rows = []
    for r, t in EVAL_GRID:
        ok, d = run_eval(m, r, t, N, rng)
        p = ok.mean()
        rows.append(dict(r=r, t=t, p_pass=p, se_p=np.sqrt(p * (1 - p) / N),
                         days_pass=d[ok].mean(), days_all=d.mean()))
    return rows


def funded_stats(m: Market, rng, reset: bool, cycle: int = 10) -> list[dict]:
    rows = []
    for r, t in FUNDED_GRID:
        paid, n, d, first = run_funded(m, r, t, N, rng, cycle=cycle, reset=reset)
        rows.append(dict(r=r, t=t, reset=reset, v_pct=paid.mean(), se_v=paid.std() / np.sqrt(N),
                         p_reward=(n > 0).mean(), n_rewards=n.mean(), life=d.mean(),
                         first_med=np.median(first[first > 0]) if (first > 0).any() else np.nan))
    return rows


def main() -> None:
    say(f"Pré-enregistrement n° 18 — FTMO 1-Step, trades au hasard ; {N} comptes par réglage, graine {SEED}")
    rng = np.random.default_rng(SEED)

    # Contrôle : reproduire la session précédente (binaire, cycle 14 jours de bourse, coût ≈ 2 % du risque)
    m = Market(None, 0.005)
    ok, _ = run_eval(m, 2.0, 4.9, N, rng)
    paid, *_ = run_funded(m, 0.5, 2.0, N, rng, cycle=14)
    say(f"\nContrôle binaire (cycle 14 j) : passage 2 / 4,9 = {ok.mean():.1%} (session précédente ≈ 41 %) ; "
        f"financé 0,5 / 2 = {paid.mean():.2f} % (≈ 6,85 %)")

    L = libs()
    say(f"NQ : {L[STOPS[0]].n} séances, {L[STOPS[0]].dates[0].date()} → {L[STOPS[0]].dates[-1].date()}")
    for s in STOPS:
        lib = L[s]
        win = (lib.tp_bar[:, :, 19] < lib.stop_bar).mean()
        stop = (lib.stop_bar < np.iinfo(np.int16).max).mean()
        say(f"  s = {s:.2%} : stop touché {stop:.0%} des jours, 1 R touché avant le stop {win:.0%}, "
            f"glissement moyen au stop {lib.stop_R[lib.stop_bar < 32767].mean() - 1:.3f} R")

    markets = {"binaire": {0.005: Market(None, 0.005)}, "NQ": {s: Market(L[s], s) for s in STOPS}}
    E, F = [], []
    for mode, ms in markets.items():
        for s, m in ms.items():
            say(f"\n=== {mode}, stop {s:.2%} (coût {m.cost_R:.3f} R) ===")
            for row in eval_stats(m, rng):
                E.append(dict(mode=mode, s=s, **row))
                say(f"  éval  {row['r']:>3} / {row['t']:<3} : passage {row['p_pass']:.1%} ± {1.96 * row['se_p']:.1%}, "
                    f"{row['days_pass']:.1f} j si validé, {row['days_all']:.1f} j par tentative")
            for reset in (True, False):
                for row in funded_stats(m, rng, reset):
                    F.append(dict(mode=mode, s=s, **row))
                    say(f"  financé {row['r']:>4} / {row['t']:<3} {'RAZ' if reset else 'sans RAZ'} : "
                        f"valeur {row['v_pct']:.2f} % ± {1.96 * row['se_v']:.2f}, P(reward) {row['p_reward']:.0%}, "
                        f"{row['n_rewards']:.2f} rewards, vie {row['life']:.0f} j, 1er reward méd. {row['first_med']:.0f} j")
    E, F = pd.DataFrame(E), pd.DataFrame(F)
    E.to_csv(OUT / "eval.csv", index=False)
    F.to_csv(OUT / "funded.csv", index=False)

    rows = []
    for (mode, s), e in E.groupby(["mode", "s"]):
        for reset in (True, False):
            f = F[(F["mode"] == mode) & (F.s == s) & (F.reset == reset)]
            picks = {"principal": (e[(e.r == MAIN["ev"][0]) & (e.t == MAIN["ev"][1])].iloc[0],
                                   f[(f.r == MAIN["fd"][0]) & (f.t == MAIN["fd"][1])].iloc[0]),
                     "meilleur de la grille": (e.loc[e.p_pass.idxmax()], f.loc[f.v_pct.idxmax()])}
            for which, (ee, ff) in picks.items():
                for size in PRICES_EUR:
                    x, ci = ev(ee.p_pass, ee.se_p, ff.v_pct, ff.se_v, size)
                    rows.append(dict(mode=mode, s=s, reset=reset, choix=which, eval=f"{ee.r}/{ee.t}",
                                     funded=f"{ff.r}/{ff.t}", p_pass=ee.p_pass, v_pct=ff.v_pct, size=size,
                                     fee_usd=PRICES_EUR[size] * 1.10, ev_usd=x, ci95=ci,
                                     refus_max=refusal_breakeven(ee.p_pass, ff.v_pct, size)))
    V = pd.DataFrame(rows)
    V.to_csv(OUT / "ev.csv", index=False)
    say("\n=== Espérance par tentative (10k et 100k) ===")
    for _, x in V[V["size"].isin([10_000, 100_000])].iterrows():
        say(f"  {x['mode']:<7} s {x.s:.2%} {'RAZ' if x.reset else 'sans RAZ':<8} {x.choix:<22} éval {x['eval']:<8} "
            f"financé {x.funded:<8} {x['size'] // 1000:>3}k : EV {x.ev_usd:+8,.0f} $ ± {x.ci95:,.0f} "
            f"(passage {x.p_pass:.1%}, financé {x.v_pct:.2f} %, refus max {x.refus_max:.0%})".replace(",", " "))


if __name__ == "__main__":
    main()
