"""Pré-enregistrement n° 22 : lecture de niveaux sur NQ (ES et YM rapportés).

R1 : cassure du range US de la veille, stop au milieu, cible measured move (H + h / L − h).
R2 : règle des 80 % : ouverture hors de la zone de valeur (70 % du volume) de la veille, acceptée
     deux périodes de 30 min → traversée jusqu'au bord opposé, stop à l'extrême de la séance.

uv run python run_prereg22.py   → results/prereg22/ (run.log, results.csv, by_year.csv, trades.csv)

Règle, critères et interdits : PREREGISTRATION_22.md (commité avant calcul).
"""

from __future__ import annotations

import sys
from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd
import vectorbt as vbt

import recolte1.engine as E

E.USE_2010 = True

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/prereg22")
NY = "America/New_York"
END = "2026-08-28"
LINES: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LINES.append(s)


def p_one_sided(x: np.ndarray) -> float:
    """Comme run_prereg20.p_one_sided."""
    x = x[np.isfinite(x)]
    m = (x - x.mean())[E._block_index(len(x))].mean(axis=1)
    return float((m >= x.mean()).mean())


def sessions(df: pd.DataFrame) -> list[dict]:
    """Séances XNYS pleines : positions [a, b] des barres 9:30 → 15:59 (b incluse) et décalage en minutes."""
    sched = xc.get_calendar("XNYS").schedule.loc[str(df.index[0].date()):END]
    sched = sched[sched["close"].dt.tz_convert(NY).dt.hour == 16]
    idx = df.index.as_unit("ns")
    o = pd.DatetimeIndex(sched["open"]).as_unit("ns")
    c = pd.DatetimeIndex(sched["close"]).as_unit("ns")
    a = idx.searchsorted(o)
    b = idx.searchsorted(c) - 1
    full = xc.get_calendar("XNYS").schedule.loc[str(df.index[0].date()):END].index
    out = []
    for k, d in enumerate(sched.index):
        ok = a[k] < len(idx) and idx[a[k]] == o[k] and idx[b[k]] == c[k] - pd.Timedelta(minutes=1)
        out.append(dict(day=d, a=int(a[k]), b=int(b[k]), ok=bool(ok), open=o[k]))
    # la séance précédente doit être la séance pleine qui précède immédiatement dans le calendrier
    pos = {d: i for i, d in enumerate(full)}
    for k, s in enumerate(out):
        s["prev"] = out[k - 1] if k > 0 and full[pos[s["day"]] - 1] == out[k - 1]["day"] else None
    return out


def value_area(lo: np.ndarray, hi: np.ndarray, vol: np.ndarray, L: float, H: float, bin_: float):
    """POC, VAL, VAH (70 %) d'un profil où le volume de chaque barre est réparti également sur ses cases."""
    n = max(int(np.ceil((H - L) / bin_ - 1e-9)), 1)
    k0 = np.clip(np.floor((lo - L) / bin_ + 1e-9).astype(int), 0, n - 1)
    k1 = np.clip(np.floor((hi - L) / bin_ - 1e-9).astype(int), 0, n - 1)
    k1 = np.maximum(k1, k0)
    per = vol / (k1 - k0 + 1)
    diff = np.zeros(n + 1)
    np.add.at(diff, k0, per)
    np.add.at(diff, k1 + 1, -per)
    prof = np.cumsum(diff)[:n]
    mid_k = ((L + H) / 2 - L) / bin_ - 0.5
    cand = np.flatnonzero(prof == prof.max())
    poc = int(cand[np.lexsort((cand, np.abs(cand - mid_k)))][0])
    lo_k = hi_k = poc
    tot, acc = prof.sum(), prof[poc]
    while acc < 0.7 * tot:
        up = prof[hi_k + 1] if hi_k + 1 < n else -1.0
        dn = prof[lo_k - 1] if lo_k - 1 >= 0 else -1.0
        if up >= dn:
            hi_k += 1
            acc += up
        else:
            lo_k -= 1
            acc += dn
    return L + (poc + 0.5) * bin_, L + lo_k * bin_, L + (hi_k + 1) * bin_


def signals(name: str, df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    op, hi, lo, cl, vol, fa = (df[c].values for c in ["open", "high", "low", "close", "volume", "factor"])
    tick = E.SPECS[name].tick
    r1, r2 = [], []
    n_skip = {"R1 cible dépassée à l'entrée": 0, "R2 cible nulle": 0}
    for s in sessions(df):
        p = s["prev"]
        if not s["ok"] or p is None or not p["ok"]:
            continue
        a, b = s["a"], s["b"]
        pa, pb = p["a"], p["b"] + 1
        H, L = hi[pa:pb].max(), lo[pa:pb].min()
        h, M = H - L, (H + L) / 2
        mins = ((df.index[a:b + 1] - s["open"]) / pd.Timedelta(minutes=1)).astype(int)  # 0 = 9:30
        base = dict(day=s["day"], p_out=b)
        # ---- R1
        if L < op[a] < H:
            c = cl[a:b + 1]
            hit = np.flatnonzero(((c > H) | (c < L)) & (np.asarray(mins) <= 359))  # barre démarrant à 15:29 au plus tard
            if len(hit):
                i = a + hit[0]
                e = cl[i]
                d = 1 if e > H else -1
                stop, tgt = M, (H + h if d > 0 else L - h)
                sl, tp = d * (e - stop) / e, d * (tgt - e) / e
                if tp <= 0:
                    n_skip["R1 cible dépassée à l'entrée"] += 1
                else:
                    r1.append(dict(base, p_in=i, dir=d, sl=sl, tp=tp, stop_pts=abs(e - stop) / fa[i]))
        # ---- R2
        poc, VAL, VAH = value_area(lo[pa:pb], hi[pa:pb], vol[pa:pb].astype(float), L, H, tick * fa[pb - 1])
        if op[a] > VAH or op[a] < VAL:
            d = -1 if op[a] > VAH else 1
            br = mins // 30
            last_of = pd.Series(np.arange(a, b + 1)).groupby(np.asarray(br)).max()
            inside = (cl[last_of.values] >= VAL) & (cl[last_of.values] <= VAH)
            js = [j for j in range(1, len(last_of)) if inside[j - 1] and inside[j] and last_of.index[j] <= 10]
            if js:
                i = int(last_of.values[js[0]])
                e = cl[i]
                stop = hi[a:i + 1].max() if d < 0 else lo[a:i + 1].min()
                tgt = VAL if d < 0 else VAH
                sl, tp = d * (e - stop) / e, d * (tgt - e) / e
                if tp <= 0 or sl <= 0:
                    n_skip["R2 cible nulle"] += 1
                else:
                    r2.append(dict(base, p_in=i, dir=d, sl=sl, tp=tp, stop_pts=abs(e - stop) / fa[i]))
    for k, v in n_skip.items():
        say(f"  {name} {k} : {v} jour(s) écarté(s)")
    return {"R1": pd.DataFrame(r1), "R2": pd.DataFrame(r2)}


def simulate(name: str, df: pd.DataFrame, e: pd.DataFrame) -> pd.DataFrame:
    """Comme run_nq_matin_sltp.run : vectorbt from_signals, stops sur high/low, net 1 tick + 5 $."""
    N = len(df)
    op, hi, lo, cl = (df[c].values for c in ["open", "high", "low", "close"])
    fee = E.SPECS[name].rt_cost / 2 / (cl / df["factor"].values)
    ent_l = np.zeros(N, bool); ent_s = np.zeros(N, bool); ex = np.zeros(N, bool)
    ent_l[e.loc[e["dir"] > 0, "p_in"].values] = True
    ent_s[e.loc[e["dir"] < 0, "p_in"].values] = True
    ex[e["p_out"].values] = True
    sl = np.full(N, np.nan); tp = np.full(N, np.nan)
    sl[e["p_in"].values] = e["sl"].values
    tp[e["p_in"].values] = e["tp"].values
    pf = vbt.Portfolio.from_signals(close=cl, open=op, high=hi, low=lo, entries=ent_l, exits=ex,
                                    short_entries=ent_s, short_exits=ex, sl_stop=sl, tp_stop=tp,
                                    fees=fee, size=1.0, size_type="percent", init_cash=1_000_000.0, freq="1min")
    rec = pf.trades.records
    rec = rec[rec["status"] == 1]
    assert len(rec) == len(e), (len(rec), len(e))
    m = e.set_index("p_in").reindex(rec["entry_idx"])
    reason = np.where(rec["exit_idx"] == m["p_out"].values, "16:00", np.where(rec["pnl"] > 0, "cible", "stop"))
    gross = (rec["pnl"] + rec["entry_fees"] + rec["exit_fees"]) / (rec["size"] * rec["entry_price"])
    return pd.DataFrame({"jour": m["day"].values, "dir": m["dir"].values, "sortie": reason,
                         "R_brut": np.asarray(gross) / m["sl"].values,
                         "R": np.asarray(rec["return"]) / m["sl"].values,
                         "p0": (m["sl"] / (m["sl"] + m["tp"])).values, "stop_pts": m["stop_pts"].values})


def summarize(t: pd.DataFrame) -> dict:
    t = t.sort_values("jour")
    R = t["R"].to_numpy()
    m, lo, hi = E.ci_mean(R)
    yr = t["jour"].dt.year.values
    yrs = (t["jour"].iloc[-1] - t["jour"].iloc[0]).days / 365.25
    cum = np.cumsum(R)
    by = t.groupby(t["jour"].dt.year)["R"].sum()
    return dict(trades=len(t), trades_par_an=len(t) / yrs, R_net=m, ic_lo=lo, ic_hi=hi, p_unilatéral=p_one_sided(R),
                R_2010_2017=R[yr <= 2017].mean(), R_2018_2026=R[yr >= 2018].mean(), R_brut=t["R_brut"].mean(),
                cible=(t["sortie"] == "cible").mean(), p0=t["p0"].mean(), stop=(t["sortie"] == "stop").mean(),
                fin_16h=(t["sortie"] == "16:00").mean(), R_par_an=by.loc[2011:2025].mean(),
                annees_pos_2011_2025=int((by.loc[2011:2025] > 0).sum()),
                sharpe_reel=R.mean() / R.std() * np.sqrt(len(R) / yrs),
                max_dd_R=float((cum - np.maximum.accumulate(cum)).min()),
                stop_pts_med=t["stop_pts"].median(), R_long=t.loc[t["dir"] > 0, "R"].mean(),
                R_short=t.loc[t["dir"] < 0, "R"].mean())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows, trades, years = [], [], []
    for name in ["NQ", "ES", "YM"]:
        df = E.load(name).copy()
        df.attrs = {}
        say(f"{name} : {df.index[0].date()} → {df.index[-1].date()}")
        sig = signals(name, df)
        for rule, e in sig.items():
            t = simulate(name, df, e)
            rows.append(dict(actif=name, règle=rule, **summarize(t)))
            trades.append(t.assign(actif=name, règle=rule))
            years.append(t.groupby(t["jour"].dt.year)["R"].sum().rename(f"{name} {rule}"))
        if name == "NQ":
            rth = [df["high"].values[s["a"]:s["b"] + 1].max() - df["low"].values[s["a"]:s["b"] + 1].min()
                   for s in sessions(df) if s["ok"] and s["day"].year == 2026]
            say(f"  NQ 2026 (jusqu'au {END}) : amplitude moyenne de la séance US 9:30-16:00 = {np.mean(rth):.0f} points")
    R = pd.DataFrame(rows)
    nq = R[R["actif"] == "NQ"].sort_values("p_unilatéral")
    R.loc[nq.index, "p_holm"] = np.minimum(np.maximum.accumulate(nq["p_unilatéral"].values * np.array([2, 1])), 1)
    R["critère_NQ"] = (R["actif"] == "NQ") & (R["p_holm"] < 0.05) & (R["R_2010_2017"] > 0) & (R["R_2018_2026"] > 0)
    for rule in ["R1", "R2"]:
        ok = bool(R.loc[(R["actif"] == "NQ") & (R["règle"] == rule), "critère_NQ"].iloc[0])
        others = R.loc[(R["actif"] != "NQ") & (R["règle"] == rule), "R_net"]
        v = ("SUCCÈS" if (others > 0).any() else "À SURVEILLER (ES et YM négatifs)") if ok else "ÉCHEC"
        say(f"Verdict pré-enregistré {rule} : {v}")

    pd.set_option("display.width", 250)
    say("\n" + R.round(4).set_index(["actif", "règle"]).T.to_string())
    Y = pd.concat(years, axis=1)
    say("\nR nets par année (somme des trades)")
    say(Y.round(1).to_string())
    R.to_csv(OUT / "results.csv", index=False)
    Y.to_csv(OUT / "by_year.csv")
    pd.concat(trades).to_csv(OUT / "trades.csv", index=False)
    (OUT / "run.log").write_text("\n".join(LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
