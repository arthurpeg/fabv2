"""Combinaison descriptive des deux stratégies transmises : 3n SL (nuit 20:05 -> 03:00) et M2 + stop 4 x ATR M15
(séance 9:35 -> 15:55), avec au plus un trade par jour : si la nuit qui se termine le matin du jour J a un trade 3n,
on ne prend pas M2 le jour J.

DESCRIPTIF, hors compteur : aucune règle nouvelle, on assemble des trades existants. Les deux règles ont échoué
hors échantillon (n° 24 et n° 25) ; une combinaison ne peut servir qu'après pré-enregistrement (CLAUDE.md, règle 3).

uv run python run_combo_3n_m2.py → results/combo_3n_m2/ (run.log, stats.csv, annees.csv, trades_<période>.csv)

Trades recalculés avec le code figé (run_nq_nuit_3n_vbt.py, run_nq_ema930_vbt.py), 15 $ l'aller-retour.
1 R = distance du stop de chaque règle (2 x ATR M15 pour 3n, 4 x ATR M15 pour M2) : en R, chaque trade risque
la même chose. Calendrier = séances RTH de la période ; un jour sans trade compte 0.
Périodes : 2016-2024 (sélection des deux règles), 2025-08/2026, 2010-06 → 2015-12 (hors échantillon des deux
règles, 2013-2015 vu par le post de M2), 2026-08-31 → 2026-11-03 (lecture anticipée du holdout, avenant A du n° 26).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_nq_ema930_vbt as E
import run_nq_nuit_3n_vbt as B

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/combo_3n_m2")
SOURCES = {  # période : (fichier, début, fin, fin des barres)
    "2010-06 → 2015-12": ("cache/databento_2010/NQ_v0_1m_2010.parquet", "2010-06-08", "2015-12-31", "2016-01-01"),
    "2016-2024": ("D:/quant-data/Cotations/indices/NQ_v0_1m.parquet", "2016-01-01", "2024-12-31", "2026-08-29"),
    "2025-08/2026": ("D:/quant-data/Cotations/indices/NQ_v0_1m.parquet", "2025-01-01", "2026-08-28", "2026-08-29"),
    "holdout vu 2026-08-31 → 11-03": ("cache/holdout_anticipe/brut/NQ_v0_1m.parquet", "2026-08-31", "2026-11-03",
                                      "2026-11-04"),
}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def trades(src: str, a: str, z: str, fin: str) -> tuple[pd.DataFrame, pd.DatetimeIndex]:
    B.SRC, B.END = Path(src), pd.Timestamp(fin, tz="America/New_York")
    b5, b15 = B.bars()
    n = B.nuits(b5, b15)
    n = n[(n.session >= a) & (n.session <= z)].reset_index(drop=True)
    rec = B.portefeuille(b5, n)["3n 03h SL"].trades.records_readable
    s = n[n.sig3n].reset_index(drop=True)
    t3 = pd.DataFrame({"date": pd.to_datetime(s.session), "strat": "3n", "pnl": rec["PnL"].values,
                       "R": rec["PnL"].values / (s.dist.values * B.PV)})
    d = E.seances(b5, b15)
    d = d[(pd.to_datetime(d.date) >= a) & (pd.to_datetime(d.date) <= z)].reset_index(drop=True)
    m2 = E.portefeuille(b5, d)["M2 + stop 4×ATR M15"].merge(d[["date", "atr15"]], on="date")
    tm = pd.DataFrame({"date": pd.to_datetime(m2.date), "strat": "M2", "pnl": m2.pnl.values,
                       "R": m2.pnl.values / (E.K_SL * m2.atr15.values * E.PV)})
    jours = pd.DatetimeIndex(sorted(set(pd.to_datetime(d.date)) | set(t3.date)))
    return pd.concat([t3, tm], ignore_index=True), jours


def stats(t: pd.DataFrame, jours: pd.DatetimeIndex) -> dict:
    out = {"Trades": len(t), "Trades/an": len(t) / (len(jours) / 252)}
    for col, unit in [("R", "R"), ("pnl", "$")]:
        x = t[col].values
        daily = t.groupby("date")[col].sum().reindex(jours, fill_value=0.0).values
        eq = np.r_[0.0, np.cumsum(daily)]
        out |= {f"Moy./trade ({unit})": x.mean(), f"Par an ({unit})": x.sum() / (len(jours) / 252),
                f"Sharpe ({unit} journalier)": daily.mean() / daily.std() * np.sqrt(252),
                f"Max DD ({unit})": (eq - np.maximum.accumulate(eq)).min()}
    out["Win %"] = 100 * (t.R > 0).mean()
    out["t NW (R)"] = B.nw_t(t.R.values) if len(t) > 5 else np.nan
    out["Pire jour (R)"] = t.groupby("date").R.sum().min()
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows, years = [], []
    for p, (src, a, z, fin) in SOURCES.items():
        t, jours = trades(src, a, z, fin)
        nuit = set(t.date[t.strat == "3n"])
        conflit = (t.strat == "M2") & t.date.isin(nuit)
        V = {"3n SL seul": t[t.strat == "3n"], "M2 + stop seul": t[t.strat == "M2"], "les deux (tous les trades)": t,
             "max 1 / jour (priorité à la nuit)": t[~conflit]}
        t[~conflit].sort_values("date").to_csv(OUT / f"trades_{p.split()[0].replace('/', '-')}.csv", index=False)
        say(f"\n===== {p} : {len(jours)} séances ; jours avec les deux signaux : {int(conflit.sum())} "
            f"(M2 sautés, {t.R[conflit].sum():+.1f} R et {t.pnl[conflit].sum():+,.0f} $ laissés) =====")
        tab = {k: stats(v, jours) for k, v in V.items()}
        say(pd.DataFrame(tab).round(3).to_string())
        rows += [{"période": p, "variante": k, **s} for k, s in tab.items()]
        c = t[~conflit]
        years.append(c.groupby(c.date.dt.year).R.sum().rename(p))
        both = t.pivot_table(index="date", columns="strat", values="R", aggfunc="sum").reindex(jours).fillna(0.0)
        say(f"Corrélation journalière 3n / M2 (R) : {both['3n'].corr(both['M2']):+.3f}")
    pd.DataFrame(rows).to_csv(OUT / "stats.csv", index=False)
    yr = pd.concat(years, axis=1).sum(axis=1).round(1)
    yr.to_csv(OUT / "annees.csv")
    say(f"\n===== R net par année, max 1 / jour =====\n{yr.to_string()}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
