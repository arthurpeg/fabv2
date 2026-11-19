"""Pré-enregistrement n° 19 : S1 + stop dur 1R (plancher 0,5 %, 1 NQ) hors échantillon, trades 2010-09 → 2015-12.

uv run python run_prereg19.py   → results/prereg19/ (run.log, results.csv, by_year.csv, trades_<config>.csv)

Même code que run_s1_r_stop_vbt.py ; seules changent les données (historique 2010-2015 rabouté), la période et
le coût fixés dans PREREGISTRATION_19.md.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kurtosis, norm, skew

import recolte1.engine as E

E.USE_2010 = True

import run_s1_r_stop_vbt as S  # noqa: E402
from recolte1.engine import ci_mean, ci_sharpe  # noqa: E402
from run_prereg10 import p_one_sided  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg19")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
S.START, S.END = "2010-06-07", "2015-12-31"
T0, T1, H1_END = "2010-09-01", "2015-12-31", "2012-12-31"
CONFIGS = [  # nom, plancher, stop dur, risque $, contrat, ticks, principal
    ("stop1R_p0.5_NQ", 0.005, True, 0.0, "NQ", 1.0, True),
    ("s1_origine_NQ", 0.0, False, 0.0, "NQ", 1.0, False),
    ("stop1R_p0.3_NQ", 0.003, True, 0.0, "NQ", 1.0, False),
    ("stop1R_p0.5_MNQ", 0.005, True, 0.0, "MNQ", 1.0, False),
]
N_ESSAIS = 1485
SD_SR = 1.68 / math.sqrt(252)  # SR0 du B1 (N = 96), converti plus bas en écart-type des Sharpe journaliers


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def sr0(n: int) -> float:
    g = 0.5772156649
    z = lambda m: (1 - g) * norm.ppf(1 - 1 / m) + g * norm.ppf(1 - 1 / (m * math.e))
    return SD_SR / z(96) * z(n)


def dsr(d: pd.Series, n: int) -> float:
    sr, s, k = d.mean() / d.std(), skew(d), kurtosis(d, fisher=False)
    return float(norm.cdf((sr - sr0(n)) * math.sqrt(len(d) - 1) / math.sqrt(1 - s * sr + (k - 1) / 4 * sr ** 2)))


def main():
    g = S.entrees(*S.seance_cash())
    jours = g["jours"][(g["jours"] >= T0) & (g["jours"] <= T1)]
    say(f"N° 19 : S1 + stop 1R hors échantillon. Séances test {jours[0].date()} → {jours[-1].date()} ({len(jours)})")
    rows, years = [], []
    for nom, plancher, stop_dur, risque, contrat, ticks, principal in CONFIGS:
        tv = S.run_vbt(g, plancher, stop_dur, risque, contrat, ticks)
        tp, saute = S.run_python(g, plancher, stop_dur, risque, contrat, ticks)
        for t in (tv, tp):
            t.drop(t.index[(pd.to_datetime(t["jour"]) < T0) | (pd.to_datetime(t["jour"]) > T1)], inplace=True)
        tv.to_csv(OUT / f"trades_{nom}.csv", index=False)
        point = S.CONTRATS[contrat]["point"]
        cout_ar = 2 * (S.CONTRATS[contrat]["commission"] / point + ticks * S.TICK)
        r = tv["resultat_R"].to_numpy()
        brut = r + cout_ar / tv["R_points"].to_numpy()
        dt = pd.to_datetime(tv["jour"])
        jr = tv.groupby(dt)["resultat_R"].sum().reindex(jours).fillna(0.0)
        jd = tv.groupby(dt)["pnl_dollars"].sum().reindex(jours).fillna(0.0)
        m, lo, hi = ci_mean(r)
        h1, h2 = r[dt <= H1_END], r[dt > H1_END]
        sh_r, sh_d = ci_sharpe(jr.to_numpy()), ci_sharpe(jd.to_numpy())
        row = dict(config=nom, principal=principal, trades=len(r), R_moyen=m, IC_bas=lo, IC_haut=hi,
                   p_unilateral=p_one_sided(r), R_brut=brut.mean(), R_2010_2012=h1.mean(), R_2013_2015=h2.mean(),
                   sharpe_R=sh_r[0], sharpe_R_IC=f"[{sh_r[1]:.2f} ; {sh_r[2]:.2f}]", sharpe_dollars=sh_d[0],
                   sharpe_dollars_IC=f"[{sh_d[1]:.2f} ; {sh_d[2]:.2f}]", dollars_total=jd.sum(),
                   pire_baisse_dollars=(jd.cumsum().cummax() - jd.cumsum()).max(), dsr_dollars=dsr(jd, N_ESSAIS),
                   ecart_controle=float((tv["pnl_dollars"].sum() - tp["pnl_dollars"].sum())),
                   trades_controle=len(tp), saute_stop=saute)
        rows.append(row)
        for y, v in tv.groupby(dt.dt.year)["resultat_R"].agg(["sum", "mean", "count"]).iterrows():
            years.append(dict(config=nom, annee=y, R_total=v["sum"], R_moyen=v["mean"], trades=int(v["count"])))
        say(f"\n== {nom}{' (PRINCIPAL)' if principal else ''} : {'stop dur 1R' if stop_dur else 'sans stop dur'}, "
            f"plancher {plancher:.1%}, {contrat} {S.CONTRATS[contrat]['commission']:.2f} $ + {ticks:g} tick par côté")
        say(S.resume(jours, tv))
        say(f"Test          R net {m:+.4f} IC [{lo:+.4f} ; {hi:+.4f}], p unilatéral {row['p_unilateral']:.4f} ; "
            f"brut {row['R_brut']:+.4f} ; 2010-09→2012 {row['R_2010_2012']:+.4f} | 2013-2015 {row['R_2013_2015']:+.4f}")
        say(f"              Sharpe R {sh_r[0]:.2f} {row['sharpe_R_IC']} ; Sharpe $ {sh_d[0]:.2f} {row['sharpe_dollars_IC']} ; "
            f"DSR $ approché (N = {N_ESSAIS}) {row['dsr_dollars']:.3f}")
        say(f"Contrôle      vbt {len(tv)} trades / boucle {len(tp)} ; écart de P&L total {row['ecart_controle']:+.2f} $ ; "
            f"entrées au-delà du stop {saute}")
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "results.csv", index=False)
    pd.DataFrame(years).to_csv(OUT / "by_year.csv", index=False)
    p = R[R["principal"]].iloc[0]
    ok = p["R_moyen"] > 0 and p["p_unilateral"] < 0.05 and p["R_2010_2012"] > 0 and p["R_2013_2015"] > 0
    say(f"\nVERDICT n° 19 : {'SUCCÈS' if ok else 'ÉCHEC'} (R net {p['R_moyen']:+.4f}, p {p['p_unilateral']:.4f}, "
        f"sous-périodes {p['R_2010_2012']:+.4f} / {p['R_2013_2015']:+.4f}). Compteur d'essais : {N_ESSAIS}.")


if __name__ == "__main__":
    main()
