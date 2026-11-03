"""Comparaison descriptive (hors compteur) : stratégie transmise « 3n » (long 20:05 -> 03:00 si somme des 3 nuits <= 0,
stop 2 x ATR M15) contre notre règle NQ de nuit (momentum 12-1, 20:00 -> 9:30, SL 2 / TP 5 ATR M15).

uv run python run_nq_nuit_3n_vs_mom.py → results/nq_nuit_3n_vs_mom/ (run.log, nuits.csv, annees.csv)
Lit results/nq_nuit_3n/trades_*.csv (run_nq_nuit_3n_vbt.py, version corrigée) et results/nq_nuit_heures/nights.csv
(run_nq_nuit_heures.py, colonne 20:00 : rendement net par nuit, 1 tick + 5 $). Aucun nouveau signal n'est testé.

Unité commune : rendement net par nuit en points de base du notionnel d'un contrat (pas de composition). Même coût
pour les deux : 3n remis au coût du dépôt (1 tick + 5 $ = 10 $ l'aller-retour au lieu de 15 $). Une nuit = la date
de la séance CME (date du matin de sortie). Calendrier commun : nuits présentes dans les deux fichiers ; une nuit sans
trade compte 0. Sharpe = moyenne / écart-type journaliers x racine(252). Attention : 2016-2026 est la période où notre
règle a été choisie (validée hors échantillon sur 2011-2015 seulement) ; pour 3n, 2016-2024 est son IS.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from recolte1.engine import ci_corr, ci_sharpe

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/nq_nuit_3n_vs_mom")
SRC3 = Path("results/nq_nuit_3n")
PV, FEE_3N, FEE_DEPOT = 20.0, 15.0, 10.0
PERIODS = {"2016-2026": (2016, 2026), "2016-2024 (IS 3n)": (2016, 2024), "2016-2021": (2016, 2021),
           "2022-2024": (2022, 2024), "2025-08/2026 (OOS 3n)": (2025, 2026)}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def trois_n(variante: str, en_r: bool = False) -> pd.Series:
    t = pd.concat([pd.read_csv(f) for f in sorted(SRC3.glob(f"trades_{variante}_20*.csv"))])
    entree = pd.to_datetime(t.entry_time.str[:19])
    nuit = (entree.dt.normalize() + pd.Timedelta(days=1)).dt.date
    pnl = t.pnl.values + FEE_3N - FEE_DEPOT
    x = pnl / (PV * t.dist.values) if en_r else pnl / (PV * t.entry_px.values) * 1e4
    return pd.Series(x, index=pd.Index(nuit, name="nuit")).groupby(level=0).sum()


def stats_r(x: pd.Series) -> dict:
    eq = np.r_[0.0, x.cumsum().values]
    actif = x[x != 0]
    sr, lo, hi = ci_sharpe(x.values)
    return {"E[R] / trade": actif.mean(), "R / an": x.sum() / (len(x) / 252), "Sharpe (R)": sr,
            "IC 95 %": f"[{lo:+.2f} ; {hi:+.2f}]", "Max DD R": (eq - np.maximum.accumulate(eq)).min()}


def stats(x: pd.Series) -> dict:
    eq = np.r_[0.0, x.cumsum().values]
    actif = x[x != 0]
    sr, lo, hi = ci_sharpe(x.values / 1e4)
    return {"Nuits": len(x), "% nuits en position": 100 * len(actif) / len(x),
            "bps / nuit en position": actif.mean(), "% / an": x.sum() / 100 / (len(x) / 252),
            "Vol % / an": x.std() / 100 * np.sqrt(252), "Sharpe": sr, "IC 95 %": f"[{lo:+.2f} ; {hi:+.2f}]",
            "Max DD %": (eq - np.maximum.accumulate(eq)).min() / 100, "Pire nuit %": x.min() / 100,
            "Nuits < -2 %": int((x < -200).sum())}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mom = pd.read_csv("results/nq_nuit_heures/nights.csv", parse_dates=["day"])
    mom = pd.Series(mom["20:00"].values * 1e4, index=mom.day.dt.date)
    d = pd.DataFrame({"mom": mom, "3n SL": trois_n("3n_03h_SL"), "3n": trois_n("3n_03h"),
                      "long 03h": trois_n("REF_03h")})
    d = d[d.mom.notna() & d["long 03h"].notna()].fillna(0.0)  # calendrier commun ; 3n sans trade = 0
    d.index = pd.to_datetime(d.index)
    d["mom + 3n SL"] = d.mom + d["3n SL"]
    # même risque : 3n SL ramené à la volatilité de mom sur 2016-2024 (poids figé, pas de recalcul OOS)
    is_ = d.index.year <= 2024
    w = d.mom[is_].std() / d["3n SL"][is_].std()
    d["mom + 3n SL (même vol)"] = (d.mom + w * d["3n SL"]) / 2
    d.to_csv(OUT / "nuits.csv")
    say(f"Nuits communes : {len(d)} ({d.index[0]:%Y-%m-%d} -> {d.index[-1]:%Y-%m-%d}) ; "
        f"poids de 3n SL à volatilité égale (IS) : {w:.2f}")

    cols = ["mom", "3n SL", "3n", "long 03h", "mom + 3n SL", "mom + 3n SL (même vol)"]
    for p, (a, b) in PERIODS.items():
        s = d[(d.index.year >= a) & (d.index.year <= b)]
        say(f"\n===== {p} (net, % du notionnel d'1 contrat) =====")
        say(pd.DataFrame({c: stats(s[c]) for c in cols}).to_string(float_format=lambda v: f"{v:.2f}"))
        both = s[(s.mom != 0) & (s["3n SL"] != 0)]
        r, lo, hi = ci_corr(s.mom.values, s["3n SL"].values)
        say(f"Corrélation par nuit mom / 3n SL : {r:+.2f} [{lo:+.2f} ; {hi:+.2f}] ; nuits où 3n est en position : "
            f"{r_both(both):+.2f} sur {len(both)} nuits")

    # notre règle selon le signal 3n (le filtre ajoute-t-il quelque chose à mom ?)
    say("\n===== Notre règle (mom) selon le signal 3n de la même nuit, bps net / nuit =====")
    sig = d["3n"] != 0
    rows = {}
    for p, (a, b) in PERIODS.items():
        m = (d.index.year >= a) & (d.index.year <= b)
        x, y = d.mom[m & sig], d.mom[m & ~sig]
        se = np.sqrt(x.var() / len(x) + y.var() / len(y))
        rows[p] = {"3n long : n": len(x), "mom bps": x.mean(), "3n à plat : n": len(y), "mom bps ": y.mean(),
                   "écart": x.mean() - y.mean(), "t Welch": (x.mean() - y.mean()) / se}
    say(pd.DataFrame(rows).T.to_string(float_format=lambda v: f"{v:.2f}"))

    # en R (1 R = 2 ATR M15 pour les deux règles) : chaque trade risque la même chose, comme en prop firm
    t = pd.read_csv("results/nq_nuit_heures/trades.csv")
    t = t[(t.clock == "20:00") & (t.cost == "net")]
    r = pd.DataFrame({"mom": t.groupby(pd.to_datetime(t.night).dt.date).R.sum(), "3n SL": trois_n("3n_03h_SL", True)})
    r.index = pd.to_datetime(r.index)
    r = r.reindex(d.index).fillna(0.0)
    r["mom + 3n SL"] = r.mom + r["3n SL"]
    for p, (a, b) in PERIODS.items():
        s = r[(r.index.year >= a) & (r.index.year <= b)]
        say(f"\n===== {p} en R (net, coût du dépôt) =====")
        say(pd.DataFrame({c: stats_r(s[c]) for c in r.columns}).to_string(float_format=lambda v: f"{v:.3f}"))

    yr = d[cols].groupby(d.index.year).sum() / 100
    yr.to_csv(OUT / "annees.csv")
    say(f"\n===== Rendement net par année (% du notionnel) =====\n{yr.round(1).to_string()}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


def r_both(s: pd.DataFrame) -> float:
    return float(np.corrcoef(s.mom, s["3n SL"])[0, 1]) if len(s) > 2 else np.nan


if __name__ == "__main__":
    main()
