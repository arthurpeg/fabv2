"""Exploratoire (non pré-enregistré) : ferme de comptes FTMO 1-Step 10k, un signal par compte (règle NQ de nuit
entrée 19:00, 20:00 ou 21:00 ET), pour voir si des signaux différents lissent la variance.

uv run python run_propfirm_farm_heures.py  → results/propfirm_farm_heures/ (run.log, returns.csv, windows.csv)

1. vectorbt (run_propfirm_vbt.run_vbt, Portfolio.from_signals sur barres 1 min) : rendement net de chaque nuit,
   pour chaque heure, en TP 5 ATR (éval) et TP 4 ATR (financé), spread FTMO 1,5 point dans les frais.
2. Règles FTMO (run_propfirm_vbt.replay) : éval 2 %, financé 1 % (RR 2), rachat d'une éval dès qu'un compte est
   raté ou perdu. Une nuit sans trade pour une heure (données manquantes) compte comme une nuit à 0.
3. Fenêtres de 2 ans (504 nuits) commençant toutes les 5 nuits sur 2011-07 → 2026-08 ; tous les comptes démarrent
   le premier jour de la fenêtre. Configurations :
   - 3 comptes, même signal (20:00) ;
   - 3 comptes, un signal chacun (19:00, 20:00, 21:00) ;
   - 6 comptes, deux par signal ;
   - 3 comptes indépendants : signal 20:00 sur trois fenêtres de l'historique tirées au hasard (borne théorique).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_propfirm_vbt as V
from propfirm.ftmo import EUR, PRICES_EUR
from recolte1.engine import load

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_farm_heures")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
HOURS = ("19:00", "20:00", "21:00")
H, STEP = 504, 5
SIZE = 10_000
FEE = PRICES_EUR[SIZE] * EUR


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def returns() -> pd.DataFrame:
    f = OUT / "returns.csv"
    if f.exists():
        return pd.read_csv(f, index_col=0, parse_dates=True)
    df = load("NQ").copy()
    df.attrs = {}
    cols = {}
    for h in HOURS:
        e, _ = V.nights(h, df)
        for tp in (5.0, 4.0):
            _, rec = V.run_vbt(df, e, np.arange(len(e)), tp, 1e4)
            cols[f"ret_{h}_tp{tp:g}"] = pd.Series((rec["pnl"] / 1e4).to_numpy(), index=e.night.values)
        cols[f"stop_{h}"] = pd.Series(2 * e.atr_frac.to_numpy(), index=e.night.values)
    R = pd.DataFrame(cols).reindex(V.Q.NIGHTS)
    R.to_csv(f)
    return R


def slot_cash(R: pd.DataFrame, hour: str, start: int, n: int) -> np.ndarray:
    """Flux en $ d'un emplacement (rachat permanent) sur les nuits [start, start + n) avec le signal `hour`."""
    r5, r4, s = R[f"ret_{hour}_tp5"].to_numpy(), R[f"ret_{hour}_tp4"].to_numpy(), R[f"stop_{hour}"].to_numpy()

    def pnl(i, ph, risk):
        x = (r5 if ph == "éval" else r4)[i]
        return 0.0 if np.isnan(x) else risk * x / (s[i] + V.COST)

    ev, _ = V.replay(pnl, start + n, start)
    cash = np.zeros(n)
    for k, j, *x in ev:
        if k == "achat":
            cash[j - start] -= FEE
        elif k == "reward":
            cash[j - start] += x[0] / 100 * SIZE
    return cash


def farm_stats(slots: list[np.ndarray]) -> dict:
    f = np.sum(slots, axis=0)
    cum = np.cumsum(f)
    dd = (cum - np.maximum.accumulate(np.concatenate([[0.0], cum]))[1:]).min()
    months = np.add.reduceat(np.clip(f, 0, None), np.arange(0, H, 21))
    q = np.array([np.add.reduceat(c, np.arange(0, H, 63)) for c in slots])
    cc = np.corrcoef(q) if len(slots) > 1 and q.std(axis=1).min() > 0 else None
    return dict(net=cum[-1] / len(slots), dd=dd / len(slots), no_reward_months=(months == 0).mean(),
                corr=np.nanmean(cc[np.triu_indices(len(slots), 1)]) if cc is not None else np.nan)


def main() -> None:
    R = returns()
    nt = len(R)
    say(f"Ferme FTMO 10k (éval {FEE:.0f} $), règle NQ de nuit, éval 2 % TP 5 / financé 1 % TP 4, rachat permanent ; "
        f"{nt} nuits {R.index[0].date()} → {R.index[-1].date()}, fenêtres de {H} nuits")
    for h in HOURS:
        say(f"  {h} : {R[f'ret_{h}_tp5'].notna().sum()} nuits tradées, rendement net moyen TP 5 "
            f"{R[f'ret_{h}_tp5'].mean() * 1e4:+.2f} pb, TP 4 {R[f'ret_{h}_tp4'].mean() * 1e4:+.2f} pb")
    say("  corrélation des rendements par nuit (TP 4, nuits à 0 sans trade) :\n"
        + R[[f"ret_{h}_tp4" for h in HOURS]].fillna(0).corr().round(3).to_string())

    starts = np.arange(0, nt - H, STEP)
    cache = {(h, s0): slot_cash(R, h, s0, H) for h in HOURS for s0 in starts}
    rng = np.random.default_rng(7)
    configs = {
        "3 comptes, même signal (20:00)": lambda s0: [cache[("20:00", s0)]] * 3,
        "3 comptes, 19:00 / 20:00 / 21:00": lambda s0: [cache[(h, s0)] for h in HOURS],
        "6 comptes, 2 par signal": lambda s0: [cache[(h, s0)] for h in HOURS] * 2,
        "3 comptes indépendants (borne)": lambda s0: [cache[("20:00", starts[rng.integers(len(starts))])] for _ in range(3)],
    }
    rows = []
    say(f"\nPar compte, sur 2 ans ({len(starts)} fenêtres) :")
    say(f"{'configuration':<36} {'gain moy.':>9} {'écart-type':>10} {'P(perte)':>8} {'5e cent.':>9} {'pire':>8} "
        f"{'creux moy.':>10} {'pire creux':>10} {'mois sans reward':>16} {'corr. trim.':>11}")
    for name, f in configs.items():
        st = pd.DataFrame([dict(start=R.index[s0].date(), **farm_stats(f(s0))) for s0 in starts])
        st["config"] = name
        rows.append(st)
        say(f"{name:<36} {st.net.mean():>+9.0f} {st.net.std():>10.0f} {(st.net < 0).mean():>8.1%} "
            f"{st.net.quantile(0.05):>+9.0f} {st.net.min():>+8.0f} {st.dd.mean():>10.0f} {st.dd.min():>10.0f} "
            f"{st.no_reward_months.median():>16.0%} {st["corr"].mean():>11.2f}")
    W = pd.concat(rows)
    W.to_csv(OUT / "windows.csv", index=False)

    # sur tout l'historique : un emplacement par heure, depuis le 2011-07-01
    full = {h: slot_cash(R, h, 0, nt) for h in HOURS}
    M = pd.DataFrame({h: pd.Series(c, index=R.index).groupby(R.index.to_period("M")).sum() for h, c in full.items()})
    Y = M.groupby(M.index.year).sum()
    say(f"\nHistorique complet, un compte par heure depuis le {R.index[0].date()} (gain net par compte) : "
        + ", ".join(f"{h} {c.sum():+,.0f} $".replace(",", " ") for h, c in full.items()))
    say("  corrélation des flux mensuels :\n" + M.corr().round(2).to_string())
    say("  corrélation des flux annuels :\n" + Y.corr().round(2).to_string())
    tot = M.sum(axis=1)
    say(f"  mois sans aucun reward : 20:00 seul {(M['20:00'] <= 0).mean():.0%} des mois ; les trois ensemble {(M.clip(lower=0).sum(axis=1) == 0).mean():.0%}")
    say("  flux annuels ($) :\n" + Y.round(0).astype(int).assign(total=Y.sum(axis=1).round(0).astype(int)).to_string())


if __name__ == "__main__":
    main()
