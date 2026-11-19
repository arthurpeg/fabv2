"""Pré-enregistrement n° 24 : la stratégie transmise 3n hors échantillon dans le temps, NQ 2010-2015.

uv run python run_prereg24.py → results/prereg24/ (run.log, tests.csv, trades_<actif>_<variante>.csv)

Règles, tests et critères : PREREGISTRATION_24.md (commit 90085fb, avant calcul). Code d'exécution inchangé :
run_nq_nuit_3n_vbt.py (bars, nuits, portefeuille vectorbt, stops_main, stats_dollars) et
run_nq_nuit_3n_8h_vbt.nuits_8h pour la sortie à 08:00. Coût 15 $ l'aller-retour (7,50 $ par ordre).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import run_nq_nuit_3n_8h_vbt as H
import run_nq_nuit_3n_vbt as B
from run_nq_nuit_r3_pente import hac_ols

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg24")
D10 = Path("cache/databento_2010")
ACTIFS = {"NQ": 20.0, "ES": 50.0, "YM": 5.0}
SOUS = {"2010-06 → 2012-12": (2010, 2012), "2013 → 2015": (2013, 2015)}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def trades_de(b5: pd.DataFrame, n: pd.DataFrame, ctrl: np.ndarray) -> dict[str, pd.DataFrame]:
    pf = B.portefeuille(b5, n)
    out = {}
    for c, (filt, stop) in B.VARIANTES.items():
        m = n.sig3n.values if filt == "3n" else np.ones(len(n), bool)
        sel = n[m].reset_index(drop=True)
        rec = pf[c].trades.records_readable
        assert len(rec) == len(sel)
        tr = pd.DataFrame({"session": sel.session, "sig3n": sel.sig3n, "entry_time": sel.entry_time,
                           "exit_time": rec["Exit Timestamp"].values, "entry_px": rec["Avg Entry Price"].values,
                           "exit_px": rec["Avg Exit Price"].values, "pnl": rec["PnL"].values, "dist": sel.dist,
                           "year": sel.year.values})
        ref = ctrl[m] if stop else sel.exit_px.values
        assert np.allclose(tr.exit_px.values, ref), c  # vectorbt = boucle à la main
        tr["hit"] = tr.exit_time.values != sel.exit_time.values
        tr["R"] = tr.pnl / (tr.dist * B.PV)
        tr["R10"] = (tr.pnl + 15.0 - 10.0) / (tr.dist * B.PV)  # coût du dépôt sur NQ (10 $), rapporté seulement
        tr["ret_net_bps"] = tr.pnl / (B.PV * tr.entry_px) * 1e4
        out[c] = tr
    return out


def t_unilat(x: np.ndarray) -> tuple[float, float, float]:
    m, t = hac_ols(np.asarray(x, float), None)
    return m, t, float(stats.norm.sf(t))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for actif, pv in ACTIFS.items():
        B.SRC, B.PV = D10 / f"{actif}_v0_1m_2010.parquet", pv
        b5, b15 = B.bars()
        n = B.nuits(b5, b15)
        n = n[n.r3_bps.notna()].reset_index(drop=True)
        say(f"\n===== {actif} : {b5.index[0]:%Y-%m-%d} -> {b5.index[-1]:%Y-%m-%d}, {len(n)} nuits avec signal, "
            f"3n long {int(n.sig3n.sum())} =====")
        say(f"Plus grand saut open/close pendant un trade : {n.max_gap_bps.max():.1f} bps "
            f"({int((n.max_gap_bps > 30).sum())} nuits > 30 bps)")
        ctrl, _ = B.stops_main(b5, n)
        tr = trades_de(b5, n, ctrl)
        n8 = H.nuits_8h(b5, n)
        n8 = n8[n8.r3_bps.notna()].reset_index(drop=True)
        ctrl8, _ = B.stops_main(b5, n8)
        tr["3n 08h SL"] = trades_de(b5, n8, ctrl8)["3n 03h SL"]
        say("Contrôle : sorties vectorbt = boucle à la main pour toutes les variantes (assert passé)")
        days = sorted(set(n.exit_time.dt.date))
        noms = list(tr) if actif == "NQ" else ["3n 03h SL"]
        tab = {c: B.stats_dollars(tr[c], days) for c in noms}
        say(pd.DataFrame(tab).round(3).to_string())
        for c in noms:
            tr[c].to_csv(OUT / f"trades_{actif}_{c.replace(' ', '_')}.csv", index=False)
            m, t, p = t_unilat(tr[c].R.values)
            rows.append(dict(actif=actif, test=c, n=len(tr[c]), E_R=m, t=t, p=p,
                             E_R_10=tr[c].R10.mean(), **{f"E[R] {k}": tr[c].R[tr[c].year.between(a, z)].mean()
                                                         for k, (a, z) in SOUS.items()}))
        if actif == "NQ":
            ref = tr["REF 03h SL"]
            x, y = ref.R[ref.sig3n].values, ref.R[~ref.sig3n].values
            w = stats.ttest_ind(x, y, equal_var=False, alternative="greater")
            rows.append(dict(actif=actif, test="P2 écart prises − sautées (long SL)", n=len(ref), E_R=x.mean() - y.mean(),
                             t=w.statistic, p=w.pvalue, E_R_10=np.nan,
                             **{f"E[R] {k}": ref.R[ref.sig3n & ref.year.between(a, z)].mean()
                                - ref.R[~ref.sig3n & ref.year.between(a, z)].mean() for k, (a, z) in SOUS.items()}))
            say(f"Nuits prises : {len(x)}, E[R] {x.mean():+.3f} ; sautées : {len(y)}, E[R] {y.mean():+.3f}")
            yr = pd.DataFrame({c: tr[c].groupby(tr[c].year).R.sum() for c in tr}).round(1)
            say(f"R net par année :\n{yr.to_string()}")
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "tests.csv", index=False)
    say("\n===== Tests (R net, 15 $ l'aller-retour ; t HAC NW 5 retards, unilatéral ; P2 : Welch unilatéral) =====")
    say(res.round(4).to_string(index=False))

    p1 = res[(res.actif == "NQ") & (res.test == "3n 03h SL")].iloc[0]
    p2 = res[res.test.str.startswith("P2")].iloc[0]
    sous_ok = all(p1[f"E[R] {k}"] > 0 for k in SOUS)
    if p1.p < 0.05 and p2.p < 0.05 and sous_ok:
        v = "SUCCÈS"
    elif p1.p < 0.05 and sous_ok:
        v = "SUCCÈS PARTIEL (prime de nuit seulement)" if p2.p >= 0.05 else "ÉCHEC"
    else:
        v = "ÉCHEC"
    say(f"\nP1 : E[R] {p1.E_R:+.3f}, t {p1.t:.2f}, p {p1.p:.4f} ; sous-périodes "
        + ", ".join(f"{k} {p1[f'E[R] {k}']:+.3f}" for k in SOUS)
        + f"\nP2 : écart {p2.E_R:+.3f} R, t {p2.t:.2f}, p {p2.p:.4f}\nVERDICT : {v}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
