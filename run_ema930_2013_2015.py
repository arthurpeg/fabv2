"""Stratégie transmise EMA 9:30 / M2 sur NQ 2013-2015 (et 2010-06 → 2015-12 en entier) : prolongement descriptif du n° 25.

DESCRIPTIF, hors compteur et hors verdict : les seuils de M2 ont été choisis par l'auteur du post en regardant
2013-2024, donc 2013-2015 n'est pas hors échantillon. Le verdict du n° 25 (2010-06 → 2012-12) ne change pas.

uv run python run_ema930_2013_2015.py → results/prereg25/suite_2013_2015/ (run.log, stats.csv, annees.csv)

Mêmes règles et même code que run_prereg25.py (run_nq_ema930_vbt.py ; taille / σ 20 j normalisée sur les 250 séances
précédentes ; coût 15 $ l'aller-retour ; 1 R = 4 x ATR M15). ES et YM rapportés pour M2.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import run_nq_ema930_vbt as E
import run_nq_nuit_3n_vbt as B
from run_nq_nuit_r3_pente import hac_ols

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg25/suite_2013_2015")
D10 = Path("cache/databento_2010")
ACTIFS = {"NQ": 20.0, "ES": 50.0, "YM": 5.0}
PERIODES = {"2013-2015": ("2013-01-01", "2015-12-31"), "2010-06 → 2015-12": ("2010-06-08", "2015-12-31")}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows, years = [], []
    for actif, pv in ACTIFS.items():
        B.SRC, E.PV = D10 / f"{actif}_v0_1m_2010.parquet", pv
        b5, b15 = B.bars()
        d_all = E.seances(b5, b15)
        raw = 1 / d_all.sigma20
        d_all["size"] = np.round(raw / raw.shift(1).rolling(250, min_periods=20).mean(), 1).clip(lower=0.1).fillna(1.0)
        for p, (a, z) in PERIODES.items():
            dt = pd.to_datetime(d_all.date)
            d = d_all[(dt >= a) & (dt <= z)].reset_index(drop=True)
            tr = E.portefeuille(b5, d)
            px, hit = E.stop_main(b5, d, E.K_SL * d.atr15.values)
            noms = list(E.VARIANTES) if actif == "NQ" else ["M2"]
            tab = {}
            for c in noms:
                jours, sens, stop, taille = E.VARIANTES[c]
                m = d.m2.values if jours == "m2" else np.ones(len(d), bool)
                ref = px[m] if stop else d.exit_px.values[m]
                # vectorbt = boucle à la main, sauf un stop touché dans la barre d'entrée (vectorbt sort une barre après)
                ecart = int((np.abs(tr[c].exit_px.values - ref) > 1e-9).sum())
                if ecart:
                    say(f"Contrôle {actif} {p} {c} : {ecart} sorties ≠ boucle (stop dans la barre d'entrée)")
                t = tr[c].assign(hit=hit[m] if stop else False).merge(d[["date", "atr15", "entry_px"]]
                                                                      .rename(columns={"entry_px": "px0"}), on="date")
                t["R"] = t.pnl / (E.K_SL * t.atr15 * pv * t["size"])
                s = E.stats(t, d.date)
                s["E[R] (stop = 1 R)"], s["t E[R]"] = t.R.mean(), B.nw_t(t.R.values)
                s["Coût (bps)"] = (15 / (pv * t.px0) * 1e4).mean()
                tab[c] = s
                rows.append({"actif": actif, "période": p, "variante": c, **s})
                if p == "2010-06 → 2015-12":
                    years.append(t.groupby("year").pnl.sum().rename(f"{actif} {c}"))
            say(f"\n===== {actif} {p} : {len(d)} séances, M2 {int(d.m2.sum())} =====\n"
                f"{pd.DataFrame(tab).round(3).to_string()}")
            if actif == "NQ":
                c_ = tr["C"]
                x, y = c_.pnl[d.m2.values].values, c_.pnl[~d.m2.values].values
                w = stats.ttest_ind(x, y, equal_var=False, alternative="greater")
                g = d[d.m2]
                z_ = (g.side * (g.exit_px - g.entry_px) / g.sigma20).dropna().values
                say(f"Choix des jours : C jours M2 {x.mean():+.1f} $ ({len(x)}) contre jours exclus {y.mean():+.1f} $ "
                    f"({len(y)}), t Welch {w.statistic:.2f}, p {w.pvalue:.3f} ; M2 brut / σ 20 j : {z_.mean():+.3f} "
                    f"(t {hac_ols(z_, None)[1]:.2f})")
    pd.DataFrame(rows).to_csv(OUT / "stats.csv", index=False)
    yr = pd.concat(years, axis=1).round(0)
    yr.to_csv(OUT / "annees.csv")
    say(f"\n===== P&L net par année ($, 1 contrat ou taille) =====\n{yr.to_string()}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
