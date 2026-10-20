"""Test de contrôle sans edge : pile ou face chaque jour à 01:00 heure de Paris sur NQ.

Long ou short tiré au hasard, stop à 1 ATR(14) M15, objectif à RR ATR, sans coûts.
Le taux de réussite attendu est 1 / (1 + RR) : 50 % pour RR 1, 33,3 % pour RR 2.

uv run python run_coinflip.py [RR] → results/coinflip/ (RR 1) ou results/coinflip/rr{RR}/
(run.log, trades.csv, winrate_mc.png). Avec coûts : run_coinflip_costs.py.

- Données : NQ 1 minute ajusté en ratio aux roulements (fab.core.load).
- Entrée, ATR M15 et sortie : coinflip.rules. Si stop et objectif sont touchés dans
  la même barre 1 min, l'ordre est inconnu : la barre compte comme perdante (stop
  d'abord, comme vectorbt).
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import vectorbt as vbt  # noqa: E402
from scipy import stats  # noqa: E402

from coinflip.rules import TZ, entries_with_atr, first_touch  # noqa: E402
from fab.core import load  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
RR = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
P0 = 1 / (1 + RR)
OUT = Path("results/coinflip") if RR == 1 else Path(f"results/coinflip/rr{RR:g}")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")

SEED = 42
N_MC = 10_000


def say(s: str = "") -> None:
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def outcomes(df: pd.DataFrame, pos: np.ndarray, atr: np.ndarray) -> pd.DataFrame:
    """Pour chaque jour, issue d'un long et d'un short (les deux sont déterminés,
    seul le tirage choisit lequel on prend). Stop à 1 ATR, objectif à RR ATR."""
    O, H, L = df.open.to_numpy(), df.high.to_numpy(), df.low.to_numpy()
    rows = []
    for p, a in zip(pos, atr):
        e = O[p]
        jl, cl = first_touch(H, L, p, e + RR * a, e - a)
        js, cs = first_touch(H, L, p, e + a, e - RR * a)
        rows.append((df.index[p], e, a, jl, cl, js, cs))
    t = pd.DataFrame(rows, columns=["entry_time", "entry", "atr", "long_bar", "long_code", "short_bar", "short_code"])
    for s in ("long", "short"):
        ex = pd.Series(df.index[t[f"{s}_bar"].clip(lower=0)], index=t.index).where(t[f"{s}_bar"] >= 0)
        t[f"{s}_min"] = (ex - t.entry_time).dt.total_seconds() / 60
        t[f"{s}_amb"] = t[f"{s}_code"] == 0
    # long gagne si l'objectif (haut) est touché seul ; short si l'objectif (bas) est touché seul
    t["long_win"] = t.long_code == 1
    t["short_win"] = t.short_code == -1
    t["open_end"] = (t.long_bar < 0) | (t.short_bar < 0)
    return t


def run_vbt(df: pd.DataFrame, t: pd.DataFrame, side: np.ndarray) -> vbt.Portfolio:
    idx = df.index
    entries = pd.Series(False, index=idx)
    shorts = pd.Series(False, index=idx)
    entries.loc[t.entry_time[side == 1]] = True
    shorts.loc[t.entry_time[side == -1]] = True
    frac = pd.Series(np.nan, index=idx)
    frac.loc[t.entry_time] = (t.atr / t.entry).to_numpy()
    return vbt.Portfolio.from_signals(
        close=df.close, open=df.open, high=df.high, low=df.low,
        entries=entries, short_entries=shorts, price=df.open,
        sl_stop=frac, tp_stop=RR * frac, stop_entry_price="fillprice",
        fees=0.0, slippage=0.0, init_cash=1e9, size=1, freq="1min",
    )


def main() -> None:
    say(f"# Pile ou face NQ 01:00 Paris, stop 1 ATR M15, objectif {RR:g} ATR (RR {RR:g}), sans coûts")
    say(f"taux de réussite théorique sans edge : 1 / (1 + RR) = {P0:.2%}\n")
    df = load("NQ")
    pos, a = entries_with_atr(df)
    say(f"Barres : {len(df):,}, {df.index[0].date()} → {df.index[-1].date()}")
    say(f"Jours tradés : {len(pos)} (entrées décalées de 1–4 min faute de barre à 01:00 : "
        f"{int((df.index[pos].tz_convert(TZ).minute > 0).sum())})")

    t = outcomes(df, pos, a)
    t = t[~t.open_end].reset_index(drop=True)
    say(f"ATR M15 à l'entrée : médiane {t.atr.median():.1f} pts ({(t.atr / t.entry).median() * 1e4:.1f} pb)")
    say(f"durée médiane : long {t.long_min.median():.0f} min, short {t.short_min.median():.0f} min ; "
        f"> 24 h : long {int((t.long_min > 1440).sum())}, short {int((t.short_min > 1440).sum())}")
    say(f"stop et objectif touchés dans la même barre 1 min (comptés perdants) : "
        f"long {int(t.long_amb.sum())}, short {int(t.short_amb.sum())}\n")

    say("## Issue si on prenait toujours le même côté")
    say(f"toujours long  : {t.long_win.mean():.2%}")
    say(f"toujours short : {t.short_win.mean():.2%}")
    say(f"jours où les deux côtés perdent : {(~t.long_win & ~t.short_win).mean():.2%}\n")

    # --- tirage principal, simulé dans vectorbt
    rng = np.random.default_rng(SEED)
    side = rng.choice([1, -1], size=len(t))
    pf = run_vbt(df, t, side)
    tr = pf.trades.records_readable
    n = len(tr)
    wins = int((tr["PnL"] > 0).sum())
    say(f"## Tirage seed={SEED} — vectorbt")
    say(f"trades : {n} (longs {int((side == 1).sum())}, shorts {int((side == -1).sum())} tirés), "
        f"gagnants : {wins}, taux de réussite : {wins / n:.2%}")
    ci = stats.binomtest(wins, n, P0)
    lo_, hi_ = ci.proportion_ci(0.95)
    say(f"IC 95 % : [{lo_:.2%}, {hi_:.2%}], p-value binomiale vs {P0:.2%} : {ci.pvalue:.3f}")
    say(f"PnL total : {tr['PnL'].sum():+.1f} pts NQ ajustés, moyenne par trade {tr['PnL'].mean():+.2f} pts")

    my_win = np.where(side == 1, t.long_win, t.short_win)
    say(f"contrôle numpy (même tirage) : {my_win.mean():.2%} sur {len(t)} trades "
        f"({len(t) - n} trades sautés par vectorbt car une position était encore ouverte)\n")

    # --- Monte Carlo sur les tirages
    flips = np.random.default_rng(0).integers(0, 2, size=(N_MC, len(t)), dtype=np.int8)
    lw, sw = t.long_win.to_numpy(), t.short_win.to_numpy()
    wr = np.where(flips == 1, lw, sw).mean(axis=1)
    say(f"## Monte Carlo : {N_MC} tirages pile ou face sur les mêmes {len(t)} jours")
    say(f"taux de réussite moyen {wr.mean():.2%}, écart-type {wr.std():.2%}, "
        f"5e–95e centile [{np.percentile(wr, 5):.2%}, {np.percentile(wr, 95):.2%}]")
    say(f"écart-type binomial théorique √(p(1−p)/n) = {np.sqrt(P0 * (1 - P0) / len(t)):.2%}")
    se = np.sqrt(P0 * (1 - P0) / (2 * len(t)))
    say(f"moyenne Monte Carlo vs {P0:.2%} : z ≈ {(wr.mean() - P0) / se:+.2f} (2n issues long + short)\n")

    say(f"## Par année (tirage seed={SEED})")
    t["side"] = side
    t["win"] = my_win
    yr = t.groupby(t.entry_time.dt.year).agg(trades=("win", "size"), winrate=("win", "mean"),
                                              long_wr=("long_win", "mean"), short_wr=("short_win", "mean"))
    say(yr.to_string(float_format=lambda x: f"{x:.3f}"))
    t.to_csv(OUT / "trades.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(wr * 100, bins=60, color="#4C72B0", alpha=0.85)
    ax.axvline(P0 * 100, color="k", ls="--", lw=1, label=f"{P0:.1%} théorique")
    ax.axvline(wins / n * 100, color="#C44E52", lw=2, label=f"tirage seed={SEED} (vectorbt) {wins / n:.1%}")
    ax.set_xlabel("taux de réussite (%)")
    ax.set_ylabel("tirages")
    ax.set_title(f"NQ pile ou face 01:00 Paris, RR {RR:g} (stop 1 ATR M15) — {N_MC} tirages, {len(t)} trades")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "winrate_mc.png", dpi=120)


if __name__ == "__main__":
    main()
