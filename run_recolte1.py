"""Intervalles de confiance des règles de la récolte 1 (papiers overnight SSRN) sur NQ, ES, YM,
GC et le forex (6E, 6B, 6J, 6A). Règles : recolte1/rules.py ; moteur vectorbt : recolte1/engine.py.

uv run python run_recolte1.py   → results/recolte1/ (ic.csv, vol_relations.csv, rolls.csv, run.log)

IC 95 % : bootstrap par blocs mobiles circulaires (blocs de 10, 2 000 tirages), percentile,
sur (a) le rendement moyen par trade (brut et net du coût aller-retour) et (b) le Sharpe
annualisé des rendements journaliers nets (jours sans position = 0).
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from recolte1.engine import NY, UNIVERSE, ci_corr, ci_mean, ci_sharpe, load, run
from recolte1.rules import PAPERS, SLACK, at, base, day, night, sessions, both

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "results/recolte1")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


ALL_DAYS = sessions().index


def summarize(paper, rule, asset, res) -> dict:
    row = {"paper": paper, "rule": rule, "asset": asset}
    if not res:
        return row | {"n": 0}
    g, n = res["gross"], res["net"]
    row["n"] = len(g["trades"])
    row["pct_long"] = float((g["trades"]["dir"] > 0).mean() * 100)
    for lab, x in [("gross", g), ("net", n)]:
        m, lo, hi = ci_mean(x["trades"]["ret"].values * 1e4)
        row |= {f"{lab}_bp": m, f"{lab}_bp_lo": lo, f"{lab}_bp_hi": hi}
    row["hit_net_%"] = float((n["trades"]["ret"] > 0).mean() * 100)
    r = n["daily"].reindex(ALL_DAYS).fillna(0.0)
    r = r[r.index >= n["daily"].index.min()]
    s, lo, hi = ci_sharpe(r.values)
    row |= {"sharpe_net": s, "sharpe_net_lo": lo, "sharpe_net_hi": hi}
    rg = g["daily"].reindex(ALL_DAYS).fillna(0.0)
    rg = rg[rg.index >= g["daily"].index.min()]
    row["sharpe_gross"] = ci_sharpe(rg.values)[0]
    row["ann_ret_net_%"] = float(r.mean() * 252 * 100)
    return row


# --------------------------------------------------------------------------- [6] portefeuille bêta jour/nuit


def p06() -> list[dict]:
    """Stratégie 1 de Hendershott-Livdan-Rösch sur l'univers : poids β_i − β̄ la nuit, l'opposé
    le jour ; β_i = pente des nuits de l'actif sur les nuits de l'ES, 12 mois glissants (≥ 30 obs),
    estimée en fin de mois et utilisée le mois suivant."""
    on = pd.DataFrame({a: base(a)["on"] for a in UNIVERSE})
    mk = on["ES"]
    ends = on.groupby(on.index.to_period("M")).tail(1).index
    betas = {}
    for e in ends:
        win = on.loc[e - pd.DateOffset(months=12):e]
        bet = {}
        for a in UNIVERSE:
            ok = win[a].notna() & mk.loc[win.index].notna()
            if ok.sum() >= 30:
                x, y = mk.loc[win.index][ok], win[a][ok]
                bet[a] = float(np.cov(x, y)[0, 1] / x.var())
        betas[e.to_period("M")] = bet
    B = pd.DataFrame(betas).T  # période × actif
    W = B.sub(B.mean(axis=1), axis=0)
    per = on.index.to_period("M")
    rows, daily = [], {}
    for leg in ["nuit", "jour", "nuit + jour"]:
        tot_g = pd.Series(0.0, index=ALL_DAYS)
        tot_n = pd.Series(0.0, index=ALL_DAYS)
        for a in UNIVERSE:
            b = base(a)
            w = pd.Series(W[a].reindex(per - 1).values, index=b.index).fillna(0.0) if a in W else pd.Series(0.0, index=b.index)
            parts = {"nuit": [night(b, w)], "jour": [day(b, -w)], "nuit + jour": [night(b, w), day(b, -w)]}[leg]
            res = run(a, both(*parts))
            if res:
                tot_g = tot_g.add(res["gross"]["daily"].reindex(ALL_DAYS).fillna(0.0), fill_value=0.0)
                tot_n = tot_n.add(res["net"]["daily"].reindex(ALL_DAYS).fillna(0.0), fill_value=0.0)
        start = W.index.min().to_timestamp() + pd.offsets.MonthBegin(1)
        tg, tn = tot_g[tot_g.index >= start], tot_n[tot_n.index >= start]
        row = {"paper": "[6] Hendershott-Livdan-Rösch", "rule": f"β_i − β̄ ({leg}), portefeuille 8 actifs", "asset": "univers"}
        row["n"] = len(tn)
        for lab, x in [("gross", tg), ("net", tn)]:
            m, lo, hi = ci_mean(x.values * 1e4)
            row |= {f"{lab}_bp": m, f"{lab}_bp_lo": lo, f"{lab}_bp_hi": hi}
        s, lo, hi = ci_sharpe(tn.values)
        row |= {"sharpe_net": s, "sharpe_net_lo": lo, "sharpe_net_hi": hi, "sharpe_gross": ci_sharpe(tg.values)[0],
                "ann_ret_net_%": float(tn.mean() * 252 * 100), "hit_net_%": float((tn[tn != 0] > 0).mean() * 100)}
        rows.append(row)
    B.to_csv(OUT / "p06_betas.csv")
    return rows


# --------------------------------------------------------------------------- [17] et [18] : relations de volatilité


def rv_table(name: str) -> pd.DataFrame:
    """RV 5 min de la nuit (18:00 ET veille → 9:30) et du jour (9:30 → clôture), par séance NYSE."""
    c = load(name)["close"]
    c5 = c.resample("5min", label="left").last().dropna()
    r5 = np.log(c5).diff().dropna()
    b = sessions()
    t18 = at(b.index, "18:00", NY, -1)
    idx = r5.index.values
    cs = np.concatenate([[0.0], np.cumsum(r5.values ** 2)])

    def rv(t_a, t_z):
        i = np.searchsorted(idx, pd.DatetimeIndex(t_a).values, side="right")
        j = np.searchsorted(idx, pd.DatetimeIndex(t_z).values, side="right")
        out = cs[j] - cs[i]
        return np.where(j - i >= 6, out, np.nan)  # au moins 6 rendements 5 min

    out = pd.DataFrame(index=b.index)
    out["rv_n"] = rv(t18.values, b["t_open"].values)
    out["rv_d"] = rv(b["t_open"].values, b["t_close"].values)
    out["cc"] = base(name)["cc"]
    return out


def vol_relations() -> pd.DataFrame:
    rows = []
    for a in UNIVERSE:
        t = rv_table(a)
        ln, ld = np.log(t["rv_n"]), np.log(t["rv_d"])
        for paper, rel, x, y in [
            ("[17] Zhang-Zhao", "corr(log RV nuit t, log RV jour t)", ln, ld),
            ("[17] Zhang-Zhao", "corr(log RV jour t-1, log RV nuit t)", ld.shift(1), ln),
            ("[18] Ahoniemi-Lanne", "levier : corr(r close-close t-1, RV jour t)", t["cc"].shift(1), t["rv_d"]),
        ]:
            c, lo, hi = ci_corr(x.values, y.values)
            rows.append({"paper": paper, "relation": rel, "asset": a, "corr": c, "lo": lo, "hi": hi,
                         "n": int((x.notna() & y.notna()).sum())})
        b = base(a)
        share = float(np.nanvar(np.log1p(b["on"])) / np.nanvar(np.log1p(b["cc"])))
        rows.append({"paper": "[17] Zhang-Zhao", "relation": "part de variance nuit Var(r_N)/Var(r)", "asset": a,
                     "corr": share, "n": int(b["on"].notna().sum())})
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    rolls = []
    for a in UNIVERSE:
        df = load(a)
        r = df.attrs["rolls"]
        log(f"{a} : {len(df):,} barres {df.index[0].date()} → {df.index[-1].date()}, {len(r)} roulements "
            f"(|écart| médian {r.abs().median() * 1e4:.1f} bp)")
        rolls.append(r.rename("gap").to_frame().assign(asset=a))
    pd.concat(rolls).to_csv(OUT / "rolls.csv")

    rows = []
    for paper, fn in PAPERS.items():
        for a in UNIVERSE:
            rules = fn(a)
            for rule, trd in rules.items():
                res = run(a, trd, SLACK.get(paper, 5))
                rows.append(summarize(paper, rule, a, res))
            log(f"{paper} {a} : {len(rules)} règles ({time.time() - t0:.0f} s)")
        pd.DataFrame(rows).to_csv(OUT / "ic.csv", index=False)
    rows += p06()
    log(f"[6] fait ({time.time() - t0:.0f} s)")
    ic = pd.DataFrame(rows)
    ic.to_csv(OUT / "ic.csv", index=False)
    vr = vol_relations()
    vr.to_csv(OUT / "vol_relations.csv", index=False)
    log(f"terminé : {len(ic)} lignes, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
