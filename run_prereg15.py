"""Pré-enregistrement n° 15 : filtres VIX (Donninger, Vojtko) et taille selon la volatilité, règle de nuit 20:00.

uv run python run_prereg15.py   → results/prereg15/ (results.csv, nights.csv, run.log)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_prereg12 as Q  # historique 2010-2015 actif ; nuits 2011-07 → 2026-08
import run_prereg10 as P
import run_recolte1_atr as A
from recolte1.engine import NY
from recolte1.rules import at, base, monthly, next_month_sign

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg15")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
N_RANDOM = 500


def log(*a):
    print(*a)
    print(*a, file=LOG, flush=True)


def nights_R(asset: str) -> pd.Series:
    bb = base(asset)
    mom = next_month_sign(bb, monthly(bb, "cc").shift(1).rolling(11, min_periods=11).sum()).reindex(Q.D).fillna(0.0)
    e = Q.table(at(Q.D, "20:00", NY, -1), Q.B["t_open"], mom, asset)
    A.VARIANTS = Q.STOP
    T = A.simulate(asset, e)
    t = T[T["cost"] == "net"].copy()
    t["R"] = P.r_multiples(asset, e, t).values
    return t.groupby(pd.to_datetime(t["night"]))["R"].sum()


def vix_close(name: str) -> pd.Series:
    v = pd.read_csv(f"config/cboe_{name}_history.csv", parse_dates=["DATE"], date_format="%m/%d/%Y")
    return v.set_index("DATE")["CLOSE"].reindex(Q.D).ffill()


def signals(asset: str) -> pd.DataFrame:
    vix, v3 = vix_close("VIX"), vix_close("VIX3M")
    cc = base(asset)["cc"]
    s20 = cc.rolling(20, min_periods=20).std()
    med = s20.expanding(min_periods=250).median()
    f = pd.DataFrame({
        "F5": (vix / v3) > 0.87,
        "F6": vix < vix.rolling(20, min_periods=20).mean(),
        "w": np.minimum(1.0, med / s20),
    }, index=Q.D)
    f = f.shift(1)  # valeurs de la séance d-1 pour la nuit d
    f["F5"] = f["F5"].fillna(False).astype(bool)
    f["F6"] = f["F6"].fillna(False).astype(bool)
    f["w"] = f["w"].fillna(1.0)
    return f


def dd(R):
    c = R.cumsum()
    return float((c - c.cummax()).min())


def evaluate(R: pd.Series, sig: pd.DataFrame, years: float, random_ctrl: bool) -> list[dict]:
    b_dd, b_ran = dd(R), R.sum() / years
    rows = [{"essai": "base", "nuits": len(R), "R_par_an": b_ran, "max_dd_R": b_dd, "ratio": b_ran / -b_dd}]
    for k in ["F5", "F6"]:
        keep = sig[k].reindex(R.index).values
        x = R[keep]
        red = 1 - dd(x) / b_dd
        row = {"essai": k, "nuits": len(x), "participation_%": keep.mean() * 100, "R_par_an": x.sum() / years,
               "R_an_vs_base_%": x.sum() / years / b_ran * 100, "max_dd_R": dd(x), "reduction_dd_%": red * 100,
               "ratio": (x.sum() / years) / -dd(x), "c1": red >= 0.30, "c2": x.sum() / years >= 0.8 * b_ran}
        if random_ctrl:
            reds = np.array([1 - dd(R.iloc[np.sort(np.random.default_rng(i).choice(len(R), int(keep.sum()), replace=False))]) / b_dd
                             for i in range(N_RANDOM)])
            row |= {"aleatoire_p95_%": np.percentile(reds, 95) * 100, "c3": red > np.percentile(reds, 95)}
        rows.append(row)
    w = sig["w"].reindex(R.index).values
    x = R * w
    red = 1 - dd(x) / b_dd
    ratio = (x.sum() / years) / -dd(x)
    rows.append({"essai": "T1", "nuits": len(x), "taille_moyenne": float(np.mean(w)), "R_par_an": x.sum() / years,
                 "R_an_vs_base_%": x.sum() / years / b_ran * 100, "max_dd_R": dd(x), "reduction_dd_%": red * 100,
                 "ratio": ratio, "ratio_vs_base_%": (ratio / (b_ran / -b_dd) - 1) * 100,
                 "c1": red >= 0.20, "c2": ratio >= 1.2 * b_ran / -b_dd})
    return rows


def main():
    sets = [("NQ", "sélection 2016-2026", "2016-01-01", "2026-08-28", True),
            ("NQ", "confirmation 2011-2015", "2011-07-01", "2015-12-31", False),
            ("ES", "confirmation 2011-2026", "2011-07-01", "2026-08-28", False),
            ("YM", "confirmation 2011-2026", "2011-07-01", "2026-08-28", False)]
    cache, rows = {}, []
    for asset, lab, a, z, rc in sets:
        if asset not in cache:
            cache[asset] = (nights_R(asset), signals(asset))
            log(f"{asset} simulé")
        R, sig = cache[asset]
        R = R[(R.index >= a) & (R.index <= z)]
        years = (R.index.max() - R.index.min()).days / 365.25
        for r in evaluate(R, sig, years, rc):
            rows.append({"marché": asset, "période": lab} | r)
    pd.concat([pd.DataFrame({"R": v[0]}).assign(marché=k) for k, v in cache.items()]).to_csv(OUT / "nights.csv")
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "results.csv", index=False)
    pd.set_option("display.width", 260)
    log(res.round(3).to_string(index=False))
    for k in ["F5", "F6", "T1"]:
        r = res[res["essai"] == k]
        s = r[r["période"].str.startswith("sélection")].iloc[0]
        sel = bool(s["c1"] and s["c2"] and (s.get("c3", True) if k != "T1" else True))
        conf = sel and bool((r[r["période"].str.startswith("confirmation")][["c1", "c2"]].all(axis=1)).all())
        log(f"{k} : retenu en sélection = {sel} ; confirmé = {conf}")


if __name__ == "__main__":
    main()
