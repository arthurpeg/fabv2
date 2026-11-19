"""Pré-enregistrement n° 25 : la stratégie transmise EMA 9:30 / M2 hors échantillon dans le temps, NQ 2010-06 → 2012-12.

uv run python run_prereg25.py → results/prereg25/ (run.log, tests.csv, trades_<actif>_<variante>.csv)

Règles, tests et critères : PREREGISTRATION_25.md (commit f130eeb, avant calcul). Code d'exécution inchangé :
run_nq_ema930_vbt.py (seances, portefeuille vectorbt, stop_main, stats). Seul changement prévu au protocole : la taille
/ σ 20 j est normalisée par la moyenne de 1 / σ des 250 séances précédentes (pas de normalisation sur 2016-2024).
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
OUT = Path("results/prereg25")
D10 = Path("cache/databento_2010")
ACTIFS = {"NQ": 20.0, "ES": 50.0, "YM": 5.0}
DEBUT, FIN = pd.Timestamp("2010-06-08").date(), pd.Timestamp("2012-12-31").date()
MOITIES = {"2010-06 → 2011-09": ("2010-06-08", "2011-09-30"), "2011-10 → 2012-12": ("2011-10-01", "2012-12-31")}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def t_unilat(x: np.ndarray) -> tuple[float, float, float]:
    m, t = hac_ols(np.asarray(x, float), None)
    return m, t, float(stats.norm.sf(t))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for actif, pv in ACTIFS.items():
        B.SRC, E.PV = D10 / f"{actif}_v0_1m_2010.parquet", pv
        b5, b15 = B.bars()
        d = E.seances(b5, b15)
        raw = 1 / d.sigma20
        size = np.round(raw / raw.shift(1).rolling(250, min_periods=20).mean(), 1).clip(lower=0.1)
        d["size"] = size.fillna(1.0).values
        d = d[(d.date >= DEBUT) & (d.date <= FIN)].reset_index(drop=True)
        tr = E.portefeuille(b5, d)
        px, hit = E.stop_main(b5, d, E.K_SL * d.atr15.values)
        for c, (jours, sens, stop, taille) in E.VARIANTES.items():
            m = d.m2.values if jours == "m2" else np.ones(len(d), bool)
            ref = px[m] if stop else d.exit_px.values[m]
            ecart = int((np.abs(tr[c].exit_px.values - ref) > 1e-9).sum())
            tr[c]["hit"] = hit[m] if stop else False
            tr[c] = tr[c].merge(d[["date", "atr15"]], on="date")
            tr[c]["R"] = tr[c].pnl / (E.K_SL * tr[c].atr15 * pv * tr[c]["size"])
            if actif == "NQ" or c == "M2":
                say(f"Contrôle {actif} {c:32s} : {len(tr[c])} trades, sorties ≠ boucle : {ecart}")
        gap = max(np.abs(b5.open.values[e + 1:z + 1] / b5.close.values[e:z] - 1).max() for e, z in zip(d.e, d.z)) * 1e4
        say(f"\n===== {actif} : {len(d)} séances ({d.date.iloc[0]} -> {d.date.iloc[-1]}), M2 : {int(d.m2.sum())}, "
            f"plus grand saut pendant un trade : {gap:.1f} bps, taille moyenne M2 : {d['size'][d.m2].mean():.2f} =====")
        noms = list(tr) if actif == "NQ" else ["M2"]
        tab = {c: E.stats(tr[c], d.date) for c in noms}
        say(pd.DataFrame(tab).round(2).to_string())
        for c in noms:
            t = tr[c]
            t.to_csv(OUT / f"trades_{actif}_{c.split(' (')[0].replace(' ', '_').replace('/', '').replace('×', 'x')}.csv",
                     index=False)
            m, tt, p = t_unilat(t.pnl.values)
            dts = pd.to_datetime(t.date)
            rows.append(dict(actif=actif, test=c, n=len(t), moyenne=m, t=tt, p=p, E_R=t.R.mean(),
                             **{f"moy. {k}": t.pnl[(dts >= a) & (dts <= z)].mean() for k, (a, z) in MOITIES.items()}))
        if actif == "NQ":
            c_ = tr["C"]
            x, y = c_.pnl[d.m2.values].values, c_.pnl[~d.m2.values].values
            w = stats.ttest_ind(x, y, equal_var=False, alternative="greater")
            rows.append(dict(actif=actif, test="P2 C jours M2 − jours exclus", n=len(c_), moyenne=x.mean() - y.mean(),
                             t=w.statistic, p=w.pvalue, E_R=np.nan))
            say(f"C sur jours M2 : {len(x)}, {x.mean():+.1f} $/trade ; jours exclus : {len(y)}, {y.mean():+.1f} $/trade")
            sl = tr["M2 + stop 4×ATR M15"]
            r = sl.R.values
            eq = np.r_[0, np.cumsum(r)]
            say(f"M2 + stop en R : E[R] {r.mean():+.3f}, t {B.nw_t(r):.2f}, R/an {r.sum() / (len(d) / 252):.1f}, "
                f"win {100 * (r > 0).mean():.1f} %, max DD {(eq - np.maximum.accumulate(eq)).min():.1f} R, "
                f"stoppés {100 * sl.hit.mean():.1f} %")
            yr = pd.DataFrame({c: t.groupby("year").pnl.sum() for c, t in tr.items()}).round(0)
            say(f"P&L net par année ($) :\n{yr.to_string()}")
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "tests.csv", index=False)
    say("\n===== Tests ($ net / trade, 15 $ l'aller-retour ; t HAC NW 5 retards, unilatéral ; P2 Welch unilatéral) =====")
    say(res.round(4).to_string(index=False))

    p1 = res[(res.actif == "NQ") & (res.test == "M2")].iloc[0]
    p2 = res[res.test.str.startswith("P2")].iloc[0]
    moities_ok = all(p1[f"moy. {k}"] > 0 for k in MOITIES)
    if p1.p < 0.05 and moities_ok:
        v = "SUCCÈS" if p2.p < 0.05 else "SUCCÈS PARTIEL (le signal marche, la sélection des jours n'est pas démontrée)"
    else:
        v = "ÉCHEC"
    say(f"\nP1 : M2 {p1.moyenne:+.1f} $/trade, t {p1.t:.2f}, p {p1.p:.4f} ; moitiés "
        + ", ".join(f"{k} {p1[f'moy. {k}']:+.1f} $" for k in MOITIES)
        + f"\nP2 : écart {p2.moyenne:+.1f} $/trade, t {p2.t:.2f}, p {p2.p:.4f}\nVERDICT : {v}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
