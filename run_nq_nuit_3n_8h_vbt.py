"""Variante de la stratégie transmise 3n : garder la position jusqu'à l'open de 08:00 ET au lieu de 03:00, puis
comparaison avec notre règle NQ de nuit (mom). Exploratoire, hors compteur : la variante 08h figurait déjà dans le
rapport d'origine (exit8h_overnight_long.py, sl2atr15_overnight_long.py), on la refait avec vectorbt.

uv run python run_nq_nuit_3n_8h_vbt.py → results/nq_nuit_3n_8h/ (run.log, nuits.csv, trades_<variante>.csv, annees.csv)

Tout comme run_nq_nuit_3n_vbt.py (version corrigée des séances), sauf la sortie : open de la 1re barre 5 min de
08:00 à 08:30 de la même séance ; stop 2 x ATR M15 vérifié jusqu'à la barre de 07:55. Le signal 3n garde sa
définition d'origine (somme des 3 nuits 20:05 -> 03:00, calculée sur toutes les nuits 03h). Nuits gardées : celles
qui ont une sortie 03:00 ET une sortie 08:00, pour comparer 03h et 08h sur les mêmes nuits.
Comparaison avec mom : même méthode que run_nq_nuit_3n_vs_mom.py (coût du dépôt 1 tick + 5 $ pour tous, R = 2 ATR M15,
nuits communes, nuit sans trade = 0).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_nq_nuit_3n_vbt as B
from recolte1.engine import ci_corr, ci_sharpe

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/nq_nuit_3n_8h")
FEE_DEPOT = 10.0
PERIODS = B.PERIODS
LOG: list[str] = []

# rapport d'origine, section 5 (15 $ l'aller-retour)
ORIGINE = {
    ("3n 08h", "2016-2024 (IS)"): dict(NetAn=16996, WR=59.27, PF=1.42, Sharpe=1.13, DD=30250, tNW=3.57, ER=0.18),
    ("3n 08h SL", "2016-2024 (IS)"): dict(NetAn=14963, WR=48.78, PF=1.42, Sharpe=1.25, DD=19179, tNW=4.03, ER=0.16),
    ("3n 08h", "2016-2021"): dict(NetAn=18884, WR=60.94, PF=1.62, Sharpe=1.45, DD=10125, tNW=3.61, ER=0.25),
    ("3n 08h SL", "2016-2021"): dict(NetAn=16932, WR=49.84, PF=1.64, Sharpe=1.64, DD=6444, tNW=4.24, ER=0.22),
    ("3n 08h", "2022-2024"): dict(NetAn=13225, WR=56.14, PF=1.22, Sharpe=0.72, DD=30250, tNW=1.36, ER=0.04),
    ("3n 08h SL", "2022-2024"): dict(NetAn=11033, WR=46.78, PF=1.20, Sharpe=0.75, DD=19179, tNW=1.42, ER=0.04),
    ("3n 08h", "2025-08/2026 (OOS)"): dict(NetAn=42887, WR=61.33, PF=1.44, Sharpe=1.38, DD=19390, tNW=2.09, ER=0.15),
    ("3n 08h SL", "2025-08/2026 (OOS)"): dict(NetAn=46988, WR=50.83, PF=1.59, Sharpe=1.85, DD=13928, tNW=2.61, ER=0.18),
}
CLES = {"NetAn": "Net $/an", "WR": "Taux de réussite %", "PF": "Profit factor", "Sharpe": "Sharpe", "DD": "Max DD $",
        "tNW": "t NW", "ER": "E[R]"}


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def nuits_8h(b5: pd.DataFrame, n: pd.DataFrame) -> pd.DataFrame:
    t = b5.index.hour * 60 + b5.index.minute
    pos = pd.DataFrame({"pos_out": np.arange(len(b5)), "session": b5.session.values})
    ext = pos[(t >= 8 * 60) & (t <= 8 * 60 + 30)].groupby("session").head(1)
    n8 = n.drop(columns=["pos_out"]).merge(ext, on="session")
    n8["exit_time"], n8["exit_px"] = b5.index[n8.pos_out], b5.open.values[n8.pos_out]
    n8["ret_bps"] = (n8.exit_px / n8.entry_px - 1) * 1e4
    return n8


def trades(b5: pd.DataFrame, n: pd.DataFrame, h: str) -> dict[tuple[str, str], pd.DataFrame]:
    """Trades vectorbt par variante et période (mêmes colonnes que run_nq_nuit_3n_vbt.py)."""
    ctrl_px, _ = B.stops_main(b5, n)
    out = {}
    for p, (y0, y1) in PERIODS.items():
        per = n.year.between(y0, y1).values
        np_ = n[per].reset_index(drop=True)
        pf = B.portefeuille(b5, np_)
        for c, (filt, stop) in B.VARIANTES.items():
            m = np_.sig3n.values if filt == "3n" else np.ones(len(np_), bool)
            sel = np_[m].reset_index(drop=True)
            rec = pf[c].trades.records_readable
            tr = pd.DataFrame({"session": sel.session, "entry_time": sel.entry_time, "exit_time": rec["Exit Timestamp"].values,
                               "entry_px": rec["Avg Entry Price"].values, "exit_px": rec["Avg Exit Price"].values,
                               "pnl": rec["PnL"].values, "dist": sel.dist})
            ref = ctrl_px[per][m] if stop else sel.exit_px.values
            assert np.allclose(tr.exit_px.values, ref), (h, c, p)  # vectorbt = boucle à la main
            tr["hit"] = tr.exit_time.values != sel.exit_time.values
            tr["R"] = tr.pnl / (tr.dist * B.PV)
            tr["ret_net_bps"] = tr.pnl / (B.PV * tr.entry_px) * 1e4
            out[(c.replace("03h", h), p)] = tr
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    b5, b15 = B.bars()
    n_all = B.nuits(b5, b15)
    n8 = nuits_8h(b5, n_all)
    n3 = n_all[n_all.session.isin(set(n8.session))].reset_index(drop=True)
    assert (n3.session.values == n8.session.values).all()
    say(f"Nuits avec sortie 03:00 et 08:00 : {len(n8)} (sur {len(n_all)}) | signal 3n : {int(n8.sig3n.sum())} | "
        f"saut max pendant un trade 08h : {max(np.abs(b5.open.values[a + 1:z + 1] / b5.close.values[a:z] - 1).max() for a, z in zip(n8.pos_in, n8.pos_out)) * 1e4:.1f} bps")
    tr = {**trades(b5, n3, "03h"), **trades(b5, n8, "08h")}
    say("Contrôle : sorties vectorbt = boucle à la main pour toutes les variantes et périodes (assert passé)")

    rows = []
    for (c, p), t in tr.items():
        y0, y1 = PERIODS[p]
        days = sorted(set(n3[n3.year.between(y0, y1)].exit_time.dt.date))
        t = t.assign(exit_time=pd.to_datetime(t.session))  # jour = séance (même calendrier pour 03h et 08h)
        rows.append({"variante": c, "période": p, **B.stats_dollars(t, days)})
    res = pd.DataFrame(rows)
    order = ["REF 03h", "REF 08h", "REF 03h SL", "REF 08h SL", "3n 03h", "3n 08h", "3n 03h SL", "3n 08h SL"]
    say("\n===== Toutes les variantes, mêmes nuits (vectorbt, 1 NQ, 15 $ l'aller-retour) =====")
    for p in PERIODS:
        g = res[res["période"] == p].set_index("variante").loc[order].drop(columns="période").T
        say(f"\n--- {p} ---\n{g.round(2).to_string()}")

    comp = []
    for (c, p), o in ORIGINE.items():
        r = res[(res.variante == c) & (res["période"] == p)].iloc[0]
        comp += [{"variante": c, "période": p, "métrique": lab, "origine": o[k], "vectorbt": r[lab]} for k, lab in CLES.items()]
    comp = pd.DataFrame(comp)
    piv = comp.pivot_table(index=["variante", "période"], columns="métrique", values=["origine", "vectorbt"], sort=False)
    say(f"\n===== Comparaison avec le rapport d'origine (08h) =====\n"
        f"{piv.swaplevel(axis=1).sort_index(axis=1, level=0, sort_remaining=False).round(2).to_string()}")

    # tranche 03:00 -> 08:00 seule (sans stop), selon le signal 3n
    seg = (n8.exit_px / n3.exit_px - 1) * 1e4
    say("\n===== Tranche 03:00 -> 08:00 (brut, bps), selon le signal 3n =====")
    rr = {}
    for p, (y0, y1) in PERIODS.items():
        m = n8.year.between(y0, y1).values
        x, y = seg[m & n8.sig3n.values], seg[m & ~n8.sig3n.values]
        rr[p] = {"3n long : n": len(x), "bps": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))),
                 "3n à plat : n": len(y), "bps ": y.mean(), "t ": y.mean() / (y.std() / np.sqrt(len(y)))}
    say(pd.DataFrame(rr).T.to_string(float_format=lambda v: f"{v:.2f}"))

    # comparaison avec mom, coût du dépôt, en R et en % du notionnel
    mom = pd.read_csv("results/nq_nuit_heures/nights.csv", parse_dates=["day"])
    mom_bps = pd.Series(mom["20:00"].values * 1e4, index=pd.to_datetime(mom.day))
    tm = pd.read_csv("results/nq_nuit_heures/trades.csv")
    tm = tm[(tm.clock == "20:00") & (tm.cost == "net")]
    mom_r = tm.groupby(pd.to_datetime(tm.night)).R.sum()

    def serie(c: str, en_r: bool) -> pd.Series:
        t = pd.concat([tr[(c, p)] for p in ("2016-2024 (IS)", "2025-08/2026 (OOS)")])
        pnl = t.pnl.values + 2 * B.FEE - FEE_DEPOT
        x = pnl / (B.PV * t.dist.values) if en_r else pnl / (B.PV * t.entry_px.values) * 1e4
        return pd.Series(x, index=pd.to_datetime(t.session.values)).groupby(level=0).sum()

    idx = pd.to_datetime(n3.session).values
    idx = pd.DatetimeIndex(idx).intersection(mom_bps.index)
    cols = ["3n 03h SL", "3n 08h SL", "3n 08h"]
    R = pd.DataFrame({"mom": mom_r, **{c: serie(c, True) for c in cols}}).reindex(idx).fillna(0.0)
    P = pd.DataFrame({"mom": mom_bps, **{c: serie(c, False) for c in cols}}).reindex(idx).fillna(0.0)
    for c in ("3n 03h SL", "3n 08h SL"):
        R[f"mom + {c}"] = R.mom + R[c]
    R.to_csv(OUT / "nuits_R.csv")
    say(f"\n===== Comparaison avec mom (coût du dépôt, R = 2 ATR M15), {len(idx)} nuits communes =====")
    for p, (y0, y1) in {"2016-2026": (2016, 2026), **PERIODS}.items():
        s, q = R[(R.index.year >= y0) & (R.index.year <= y1)], P[(P.index.year >= y0) & (P.index.year <= y1)]
        tab = {}
        for c in R.columns:
            x = s[c]
            eq = np.r_[0.0, x.cumsum().values]
            sr, lo, hi = ci_sharpe(x.values)
            tab[c] = {"E[R] / trade": x[x != 0].mean(), "R / an": x.sum() / (len(x) / 252), "Sharpe (R)": sr,
                      "IC 95 %": f"[{lo:+.2f} ; {hi:+.2f}]", "Max DD R": (eq - np.maximum.accumulate(eq)).min()}
            if c in P:
                tab[c]["Sharpe (% notionnel)"] = q[c].mean() / q[c].std() * np.sqrt(252)
        say(f"\n--- {p} ---\n{pd.DataFrame(tab).to_string(float_format=lambda v: f'{v:.3f}')}")
        r8, l8, h8 = ci_corr(s.mom.values, s["3n 08h SL"].values)
        r3 = np.corrcoef(s.mom, s["3n 03h SL"])[0, 1]
        say(f"Corrélation par nuit avec mom : 3n 03h SL {r3:+.2f} ; 3n 08h SL {r8:+.2f} [{l8:+.2f} ; {h8:+.2f}]")

    yr = R.groupby(R.index.year).sum()
    yr.to_csv(OUT / "annees.csv")
    say(f"\n===== R net par année =====\n{yr.round(1).to_string()}")
    for (c, p), t in tr.items():
        if "08h" in c:
            t.to_csv(OUT / f"trades_{c.replace(' ', '_')}_{PERIODS[p][0]}-{PERIODS[p][1]}.csv", index=False)
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
