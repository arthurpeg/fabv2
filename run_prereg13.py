"""Pré-enregistrement n° 13 : 4 filtres « à plat » sur la règle NQ de nuit, contrôle aléatoire.

uv run python run_prereg13.py   → results/prereg13/ (results.csv, random.csv, trades.csv, run.log)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_prereg12 as Q  # active l'historique 2010-2015, période 2011-07 → 2026-08
import run_prereg10 as P
from recolte1.engine import NY, ci_mean, price_at
from recolte1.rules import at

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg13")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
PERIODS = {"sélection 2016-2026": ("2016-01-01", "2026-08-28"), "confirmation 2011-2015": ("2011-07-01", "2015-12-31")}
N_RANDOM = 500


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def filters() -> pd.DataFrame:
    """Booléens indexés par la séance d (la nuit d se termine à l'ouverture de d) ; chaque
    variable porte sur la séance d-1, close avant l'entrée de 20:00 ET."""
    b, bb, d = Q.B, Q.BB, Q.D
    p945, _ = price_at("NQ", at(d, "09:45", NY))
    p1500, _ = price_at("NQ", at(d, "15:00", NY))
    up = (p1500 / p945 - 1 > 0) & ~b["half"]
    cc2 = bb["cc"] ** 2
    hi = cc2 > cc2.expanding(min_periods=60).quantile(2 / 3).shift(1)
    c = bb["p_close"]
    above = c > c.rolling(20, min_periods=20).mean()
    f = pd.DataFrame({
        "F1 jour 9:45→15:00 > 0 (Jones)": up,
        "F2 nuit précédente < 0 (Abdi)": bb["on"] < 0,
        "F3 VOL veille tercile haut (Berkman)": hi,
        "F4 clôture > MM20 (Vojtko)": above,
    }, index=d)
    return f.shift(1, fill_value=False).astype(bool)  # valeur de d-1 utilisée pour la nuit d


def metrics(R: pd.Series, years: float) -> dict:
    cum = R.cumsum()
    dd = float((cum - cum.cummax()).min())
    return {"trades": len(R), "R_par_an": R.sum() / years, "max_dd_R": dd,
            "ratio": (R.sum() / years) / -dd if dd < 0 else np.nan, "R_trade": R.mean()}


def main():
    e = Q.table(at(Q.D, "20:00", NY, -1), Q.B["t_open"], Q.MOM, "R0")
    T = Q.sim(e, Q.STOP)
    t = T[T["cost"] == "net"].copy()
    t["R"] = P.r_multiples("NQ", e, t).values
    t = t.sort_values("entry_idx")
    t["night"] = pd.to_datetime(t["night"])
    F = filters()
    t.to_csv(OUT / "trades.csv", index=False)
    rows, rnd_rows = [], []
    for pname, (a, z) in PERIODS.items():
        tp = t[(t["night"] >= a) & (t["night"] <= z)].reset_index(drop=True)
        years = (tp["night"].max() - tp["night"].min()).days / 365.25
        base = metrics(tp["R"], years)
        rows.append({"période": pname, "filtre": "base (aucun)"} | base | {"participation_%": 100.0})
        rng = np.random.default_rng(13)
        for fname in F.columns:
            keep = F[fname].reindex(tp["night"]).values.astype(bool)
            m = metrics(tp["R"][keep], years)
            red = 1 - m["max_dd_R"] / base["max_dd_R"]
            k = int(keep.sum())
            reds = []
            for i in range(N_RANDOM):
                sel = np.sort(np.random.default_rng(i).choice(len(tp), size=k, replace=False))
                reds.append(1 - metrics(tp["R"].iloc[sel], years)["max_dd_R"] / base["max_dd_R"])
            reds = np.array(reds)
            mm, lo, hi = ci_mean(tp["R"][keep].values)
            row = {"période": pname, "filtre": fname} | m | {
                "participation_%": keep.mean() * 100, "reduction_dd_%": red * 100,
                "R_an_vs_base_%": m["R_par_an"] / base["R_par_an"] * 100,
                "random_dd_red_p95_%": np.percentile(reds, 95) * 100, "random_dd_red_moy_%": reds.mean() * 100,
                "rang_vs_aleatoire_%": (reds < red).mean() * 100, "R_trade_lo": lo, "R_trade_hi": hi,
                "c1_dd_-30%": red >= 0.30, "c2_R_an_80%": m["R_par_an"] >= 0.8 * base["R_par_an"],
                "c3_>p95_aleatoire": red > np.percentile(reds, 95)}
            rows.append(row)
            rnd_rows.append(pd.DataFrame({"période": pname, "filtre": fname, "reduction_dd": reds}))
    Rs = pd.DataFrame(rows)
    Rs.to_csv(OUT / "results.csv", index=False)
    pd.concat(rnd_rows).to_csv(OUT / "random.csv", index=False)
    pd.set_option("display.width", 260)
    cols = ["période", "filtre", "trades", "participation_%", "R_par_an", "R_an_vs_base_%", "max_dd_R", "reduction_dd_%",
            "random_dd_red_moy_%", "random_dd_red_p95_%", "ratio", "R_trade", "R_trade_lo", "R_trade_hi",
            "c1_dd_-30%", "c2_R_an_80%", "c3_>p95_aleatoire"]
    log(Rs[cols].round(3).to_string(index=False))
    sel = Rs[(Rs["période"] == "sélection 2016-2026") & Rs["c1_dd_-30%"].fillna(False) & Rs["c2_R_an_80%"].fillna(False)
             & Rs["c3_>p95_aleatoire"].fillna(False)]["filtre"].tolist()
    conf = Rs[(Rs["période"] == "confirmation 2011-2015") & Rs["filtre"].isin(sel) & Rs["c1_dd_-30%"].fillna(False)
              & Rs["c2_R_an_80%"].fillna(False)]["filtre"].tolist()
    log(f"retenus (sélection) : {sel or 'aucun'} ; confirmés (2011-2015) : {conf or 'aucun'}")


if __name__ == "__main__":
    main()
