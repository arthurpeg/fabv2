"""Pile ou face NQ 01:00 Paris, RR 1 (stop = objectif = K × ATR), AVEC coûts.

uv run python run_coinflip_costs.py [K] [FREQ]   (défaut : 1 15min)
→ results/coinflip/costs/ pour 1 ATR M15, sinon results/coinflip/costs/{K}atr_{FREQ}/
(run.log, summary.csv, trades_*.csv, costs_mc.png)

Mêmes entrées et mêmes tirages que run_coinflip.py ; stop et objectif placés à
± K ATR du prix d'exécution réel. Scénarios (coûts en points bruts NQ, convertis
en points ajustés par le facteur de roulement de la barre d'entrée) :

- CFD FTMO : spread 2 pts, sans commission. Les cotations NQ jouent le rôle du
  bid (convention MetaTrader) et l'ask vaut bid + 2. Un long achète à l'ask
  (30 000 → 30 002) et sort sur le bid ; un short vend au bid et sort sur l'ask.
  Il faut donc K ATR + 2 pts de mouvement favorable pour gagner, K ATR − 2 pts
  de mouvement défavorable pour perdre. Swap non modélisé : le log compte les
  trades encore ouverts au changement de jour serveur (23:00 Paris).
- Futures NQ (20 $/pt) : entrée au marché 1 tick (0,25 pt) au-delà de l'open,
  objectif limite exécuté au niveau, stop exécuté au niveau (ou à l'open en cas de
  gap), commission + frais 5 $ aller-retour = 0,25 pt.
- Futures MNQ (2 $/pt) : même exécution, commission + frais 1,50 $ aller-retour = 0,75 pt.

Une seule position à la fois : si le trade de la veille est encore ouvert à
01:00, l'entrée du jour est sautée (vectorbt). Le contrôle numpy et le Monte
Carlo prennent tous les jours, chaque trade indépendant.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import vectorbt as vbt  # noqa: E402

from coinflip.rules import TZ, entries_with_atr, first_touch  # noqa: E402
from fab.core import load  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
K = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
FREQ = sys.argv[2] if len(sys.argv) > 2 else "15min"
TF = {"15min": "M15", "1h": "H1"}.get(FREQ, FREQ)
OUT = Path("results/coinflip/costs")
if (K, FREQ) != (1.0, "15min"):
    OUT = OUT / f"{K:g}atr_{FREQ}"
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")

SEED = 42
N_MC = 10_000


@dataclass(frozen=True)
class Costs:
    name: str
    slug: str
    long_in: float  # pts payés à l'entrée d'un long (au-dessus de l'open)
    short_in: float  # pts payés à l'entrée d'un short (sous l'open)
    spread: float  # écart ask − bid : un short sort sur l'ask
    commission: float  # pts par aller-retour
    usd_per_pt: float | None = None


SCENARIOS = [
    Costs("sans coûts", "free", 0.0, 0.0, 0.0, 0.0),
    Costs("CFD FTMO : spread 2 pts", "cfd", 2.0, 0.0, 2.0, 0.0),
    Costs("futures NQ : 1 tick + 5 $ AR", "nq", 0.25, 0.25, 0.0, 5.0 / 20, 20.0),
    Costs("futures MNQ : 1 tick + 1,50 $ AR", "mnq", 0.25, 0.25, 0.0, 1.5 / 2, 2.0),
]


def say(s: str = "") -> None:
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def outcomes(df: pd.DataFrame, pos: np.ndarray, dist: np.ndarray, c: Costs) -> pd.DataFrame:
    """Issue d'un long et d'un short chaque jour, en points ajustés, stop et
    objectif à ± dist du prix d'exécution. Stop et objectif touchés dans la même
    barre comptent comme stop. Barre de sortie −1 : jamais résolu."""
    O, H, L = df.open.to_numpy(), df.high.to_numpy(), df.low.to_numpy()
    F = df.factor.to_numpy()
    rows = []
    for p, a in zip(pos, dist):
        f = F[p]
        # long : achat à l'ask, sorties déclenchées par le bid (= cotation)
        e = O[p] + c.long_in * f
        j, code = first_touch(H, L, p, e + a, e - a)
        lx = max(e + a, O[j]) if code == 1 else min(e - a, O[j])
        # short : vente au bid, sorties déclenchées par l'ask (= cotation + spread)
        s = c.spread * f
        es = O[p] - c.short_in * f
        k, kode = first_touch(H, L, p, es + a - s, es - a - s)
        sx = min(es - a, O[k] + s) if kode == -1 else max(es + a, O[k] + s)
        comm = c.commission * f
        rows.append((df.index[p], O[p], a, f, code == 1, lx - e - comm, j,
                     kode == -1, es - sx - comm, k))
    t = pd.DataFrame(rows, columns=["entry_time", "open", "dist", "factor", "long_win", "long_pnl",
                                    "long_bar", "short_win", "short_pnl", "short_bar"])
    for s in ("long", "short"):
        t[f"{s}_exit"] = df.index[t[f"{s}_bar"].clip(lower=0)]
    return t


def taken(t: pd.DataFrame, side: np.ndarray) -> np.ndarray:
    """Une position à la fois : un jour est sauté si le trade pris précédemment
    n'est pas sorti avant son entrée."""
    ex = np.where(side == 1, t.long_exit, t.short_exit)
    ent = t.entry_time.to_numpy()
    ok = np.zeros(len(t), dtype=bool)
    free_at = ent[0]
    for i in range(len(t)):
        if ent[i] >= free_at:
            ok[i] = True
            free_at = ex[i]
    return ok


def run_vbt(df: pd.DataFrame, t: pd.DataFrame, side: np.ndarray, c: Costs) -> pd.DataFrame:
    """Longs sur les cotations (bid), shorts sur l'ask (cotations + spread). Un
    portefeuille par sens ; `t` ne contient que des trades qui ne se chevauchent pas."""
    idx = df.index
    f = df.factor
    out = []
    for sgn, shift, px in ((1, 0.0, df.open + c.long_in * f), (-1, c.spread, df.open - c.short_in * f)):
        q = df[["open", "high", "low", "close"]].add(shift * f, axis=0)
        sig = pd.Series(False, index=idx)
        sig.loc[t.entry_time[side == sgn]] = True
        e = px.loc[t.entry_time]
        frac = pd.Series(np.nan, index=idx)
        frac.loc[t.entry_time] = t.dist.to_numpy() / e.to_numpy()
        pf = vbt.Portfolio.from_signals(
            close=q.close, open=q.open, high=q.high, low=q.low,
            entries=sig if sgn == 1 else False, short_entries=sig if sgn == -1 else False,
            price=px, sl_stop=frac, tp_stop=frac, stop_entry_price="fillprice",
            fixed_fees=c.commission * f / 2, fees=0.0, slippage=0.0,
            init_cash=1e9, size=1, freq="1min",
        )
        out.append(pf.trades.records_readable)
    tr = pd.concat(out, ignore_index=True)
    col = next(c for c in tr.columns if c.startswith("Entry") and ("Timestamp" in c or "Index" in c))
    return tr.sort_values(col).reset_index(drop=True)  # même ordre que `t`


def main() -> None:
    say(f"# Pile ou face NQ 01:00 Paris, RR 1, stop = objectif = {K:g} ATR {TF}, avec coûts\n")
    df = load("NQ")
    pos, atr = entries_with_atr(df, FREQ)
    dist = K * atr
    say(f"Jours : {len(pos)}, ATR {TF} médian {np.median(atr):.1f} pts ajustés, stop médian "
        f"{np.median(dist / df.factor.to_numpy()[pos]):.1f} pts bruts, "
        f"facteur d'ajustement médian {df.factor.iloc[pos].median():.3f}")
    side_all = np.random.default_rng(SEED).choice([1, -1], size=len(pos))

    rows, mc = [], {}
    for c in SCENARIOS:
        t = outcomes(df, pos, dist, c)
        keep = ((t.long_bar >= 0) & (t.short_bar >= 0)).to_numpy()
        t, side = t[keep].reset_index(drop=True), side_all[keep]
        flips = np.random.default_rng(0).integers(0, 2, size=(N_MC, len(t)), dtype=np.int8) == 1
        win = np.where(side == 1, t.long_win, t.short_win)
        pnl = np.where(side == 1, t.long_pnl, t.short_pnl)
        R = pnl / t.dist.to_numpy()
        ok = taken(t, side)
        tr = run_vbt(df, t[ok].reset_index(drop=True), side[ok], c)
        vwins = int((tr["PnL"] > 0).sum())

        lw, sw = t.long_win.to_numpy(), t.short_win.to_numpy()
        lR, sR = (t.long_pnl / t.dist).to_numpy(), (t.short_pnl / t.dist).to_numpy()
        lP, sP = (t.long_pnl / t.factor).to_numpy(), (t.short_pnl / t.factor).to_numpy()
        mc_wr = np.where(flips, lw, sw).mean(axis=1)
        mc_R = np.where(flips, lR, sR).mean(axis=1)
        mc_pts = np.where(flips, lP, sP).sum(axis=1)
        mc[c.slug] = mc_R
        cost_R = ((c.long_in + c.short_in) / 2 + c.spread / 2 + c.commission) * t.factor / t.dist
        nominal_pts = pnl / t.factor.to_numpy()
        minutes = (pd.DatetimeIndex(np.where(side == 1, t.long_exit, t.short_exit))
                   - pd.DatetimeIndex(t.entry_time)).total_seconds().to_numpy() / 60
        row = {
            "scénario": c.name,
            "trades vbt": len(tr),
            "win rate vbt": vwins / len(tr),
            "R moyen vbt": (tr["PnL"].to_numpy() / t.dist[ok].to_numpy()).mean(),
            "trades numpy": len(t),
            "win rate numpy": win.mean(),
            "R moyen numpy": R.mean(),
            "pts bruts / trade": nominal_pts.mean(),
            "MC win rate": mc_wr.mean(),
            "MC R moyen": mc_R.mean(),
            "MC part de tirages gagnants": (mc_pts > 0).mean(),
            "coût moyen (R)": cost_R.mean(),
        }
        if c.usd_per_pt:
            row["$ / trade / contrat"] = nominal_pts.mean() * c.usd_per_pt
        rows.append(row)

        say(f"\n## {c.name}")
        say(f"vectorbt (seed {SEED}) : {len(tr)} trades ({len(t) - len(tr)} jours sautés, position encore ouverte), "
            f"win rate {vwins / len(tr):.2%}, {row['R moyen vbt']:+.3f} R / trade")
        say(f"numpy, tous les jours : {len(t)} trades, win rate {win.mean():.2%}, {R.mean():+.3f} R, "
            f"{nominal_pts.mean():+.2f} pts bruts / trade ; coût moyen {cost_R.mean():.3f} R ; "
            f"durée médiane {np.median(minutes):.0f} min, > 24 h : {int((minutes > 1440).sum())}")
        say(f"Monte Carlo {N_MC} tirages : win rate {mc_wr.mean():.2%} "
            f"[{np.percentile(mc_wr, 5):.2%}, {np.percentile(mc_wr, 95):.2%}], "
            f"{mc_R.mean():+.3f} R / trade, tirages à PnL total > 0 : {(mc_pts > 0).mean():.1%}")
        if c.usd_per_pt:
            say(f"par contrat : {nominal_pts.mean() * c.usd_per_pt:+.2f} $ / trade")
        if c.slug == "cfd":
            ex = pd.DatetimeIndex(np.where(side == 1, t.long_exit, t.short_exit)).tz_convert(TZ)
            ent = t.entry_time.dt.tz_convert(TZ)
            crosses = ex >= (ent.dt.normalize() + pd.Timedelta("23h")).to_numpy()
            say(f"trades encore ouverts à 23:00 Paris (swap FTMO non modélisé) : {int(crosses.sum())}")
            yr = pd.DataFrame({"année": ent.dt.year, "win": win, "R": R, "coût R": cost_R})
            say("\npar année (CFD, seed 42, tous les jours) :")
            say(yr.groupby("année").mean().to_string(float_format=lambda x: f"{x:.3f}"))
        t.assign(side=side, win=win, pnl=pnl, R=R, taken=ok).to_csv(OUT / f"trades_{c.slug}.csv", index=False)

    s = pd.DataFrame(rows).set_index("scénario")
    s.to_csv(OUT / "summary.csv")
    say("\n## Résumé")
    say(s.T.to_string(float_format=lambda x: f"{x:.4f}"))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for c, col in zip(SCENARIOS, ["#4C72B0", "#C44E52", "#55A868", "#8172B2"]):
        ax.hist(mc[c.slug], bins=60, alpha=0.6, color=col, label=c.name)
    ax.axvline(0, color="k", ls="--", lw=1)
    ax.set_xlabel(f"R moyen par trade (1 R = {K:g} ATR {TF})")
    ax.set_ylabel("tirages")
    ax.set_title(f"NQ pile ou face 01:00 Paris, RR 1, stop {K:g} ATR {TF} — {N_MC} tirages")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "costs_mc.png", dpi=120)


if __name__ == "__main__":
    main()
