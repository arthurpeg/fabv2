"""Or (GC) : anatomie de la session de reprise (17:00 NY veille → 9:00 Shanghai), 2016-2026.

uv run python run_gc_reprise.py   → results/gc_reprise/ (run.log, legs.csv, dow.csv, by_year.csv,
cond.csv, volume.csv)

Exploratoire, non pré-enregistré, demandé en séance, suite de [[reports/gc_sessions_report]] où
la reprise est la seule session significative (+2,0 bp brut, t 3,5). Descriptif : rien ici ne
valide une règle.

Questions :
  1. Découpage : gap de l'arrêt (17:00 → 18:05, première cotation après la réouverture),
     18:05 → 19:00, 19:00 → 20:00, 20:00 → 9:00 Shanghai (20:00 ou 21:00 NY selon l'heure d'été).
  2. Jour de la semaine (le lundi, la session contient le week-end).
  3. Roulements : ils tombent à 00:00 UTC (19:00 ou 20:00 NY), dans la session. Résultat sans
     les jours de roulement (± 1 jour).
  4. Queues : médiane, moyenne tronquée, sans les 1 % de jours extrêmes.
  5. Conditionnement : signe de la séance précédente (17:00 → 17:00), tendance 20 jours,
     tercile de volatilité des 20 jours précédents.
  6. Liquidité : volume moyen par minute dans la reprise contre les autres sessions.
t de Newey-West (5 retards), IC 95 % bootstrap par blocs (recolte1.engine).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as st

import recolte1.engine as E
from run_gc_sessions import END, NY, SH, START, nw_t

OUT = Path("results/gc_reprise")
PERIODS = [("2016-2019", "2016", "2019"), ("2020-2022", "2020", "2022"), ("2023-2026", "2023", "2026")]
LINES: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


def desc(r: pd.Series) -> dict:
    r = r.dropna()
    m, lo, hi = E.ci_mean(r.values)
    t = nw_t(r.values)
    return {"n": len(r), "moy_bp": m * 1e4, "ic_lo": lo * 1e4, "ic_hi": hi * 1e4, "t_nw": t,
            "p": 2 * st.norm.sf(abs(t)), "pos%": (r > 0).mean() * 100, "sigma_bp": r.std() * 1e4}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    d = pd.bdate_range(START, END)
    prev = d - pd.offsets.BDay(1)
    t = pd.DataFrame(index=d)
    t["c17"] = E.at(prev, "17:00", NY).set_axis(d)
    t["o1805"] = E.at(d, "18:05", NY, -1)
    t["h19"] = E.at(d, "19:00", NY, -1)
    t["h20"] = E.at(d, "20:00", NY, -1)
    t["sh9"] = E.at(d, "09:00", SH)
    t["c17_today"] = E.at(d, "17:00", NY)
    p = pd.DataFrame({k: E.price_at("GC", t[k])[0] for k in t})
    p = p.dropna()
    log(f"GC, {len(p)} jours complets {p.index[0].date()} → {p.index[-1].date()}")

    rep = p["sh9"] / p["c17"] - 1
    legs = pd.DataFrame({
        "gap 17:00 → 18:05": p["o1805"] / p["c17"] - 1,
        "18:05 → 19:00": p["h19"] / p["o1805"] - 1,
        "19:00 → 20:00": p["h20"] / p["h19"] - 1,
        "20:00 → 9:00 SH": p["sh9"] / p["h20"] - 1,
        "reprise": rep,
    })
    rows = []
    for c in legs:
        row = {"jambe": c, **desc(legs[c])}
        for pn, a, z in PERIODS:
            m = (legs.index >= a) & (legs.index <= f"{z}-12-31")
            row[pn] = legs[c][m].mean() * 1e4
        rows.append(row)
    lg = pd.DataFrame(rows)
    lg.round(4).to_csv(OUT / "legs.csv", index=False)
    log("\n=== 1. Découpage de la reprise (brut, bp) ===")
    log(lg.round(2).to_string(index=False))
    log("(20:00 → 9:00 Shanghai : 0 h en hiver NY si Shanghai 9:00 = 20:00 NY ; 1 h en été)")

    # 2. jour de la semaine
    dow = pd.DataFrame([{"jour": j, **desc(rep[rep.index.dayofweek == k]),
                         "gap_bp": legs["gap 17:00 → 18:05"][legs.index.dayofweek == k].mean() * 1e4}
                        for k, j in enumerate(["lundi (week-end)", "mardi", "mercredi", "jeudi", "vendredi"])])
    dow.round(4).to_csv(OUT / "dow.csv", index=False)
    log("\n=== 2. Par jour de la semaine (jour de la séance qui commence) ===")
    log(dow.round(2).to_string(index=False))
    log("Hors lundis : " + str({k: round(v, 3) for k, v in desc(rep[rep.index.dayofweek != 0]).items()}))

    # 3. roulements (00:00 UTC = jour de séance GC du même jour calendaire UTC)
    rolls = E.load("GC").attrs["rolls"].index
    rd = pd.DatetimeIndex(rolls.tz_convert(None).normalize())
    near = pd.DatetimeIndex(sorted({x + pd.Timedelta(days=k) for x in rd for k in (-1, 0, 1)}))
    no_roll = rep[~rep.index.isin(near)]
    log(f"\n=== 3. Roulements : {len(rd)} roulements, {rep.index.isin(rd).sum()} jours de séance concernés ===")
    log("  jours de roulement : " + str({k: round(v, 3) for k, v in desc(rep[rep.index.isin(rd)]).items()}))
    log("  sans roulement ±1 j : " + str({k: round(v, 3) for k, v in desc(no_roll).items()}))

    # 4. queues
    r = rep.values
    q1, q99 = np.percentile(r, [1, 99])
    log("\n=== 4. Queues ===")
    log(f"  moyenne {r.mean()*1e4:+.2f} bp, médiane {np.median(r)*1e4:+.2f}, "
        f"moyenne tronquée 5 % {st.trim_mean(r, 0.05)*1e4:+.2f}, skew {st.skew(r):+.2f}, kurtosis {st.kurtosis(r):.1f}")
    mid = rep[(rep > q1) & (rep < q99)]
    log("  sans les 1 % de chaque queue : " + str({k: round(v, 3) for k, v in desc(mid).items()}))
    top = rep.abs().sort_values(ascending=False).head(10)
    log("  10 plus grands |mouvements| (bp) : " + ", ".join(f"{i.date()} {rep[i]*1e4:+.0f}" for i in top.index))
    log(f"  part de la somme apportée par les 20 meilleurs jours : {rep.nlargest(20).sum()/rep.sum()*100:.0f} %")

    # 5. conditionnement (tout connu à 17:00 la veille)
    day = (p["c17_today"] / p["c17"] - 1)  # séance 17:00 → 17:00 du jour
    prev_day = day.shift(1)
    trend20 = (p["c17"] / p["c17"].shift(20) - 1)
    vol20 = day.shift(1).rolling(20).std()
    cond = []
    for name, x in [("séance précédente", prev_day), ("tendance 20 j", trend20)]:
        for lab, m in [("> 0", x > 0), ("< 0", x < 0)]:
            cond.append({"variable": name, "état": lab, **desc(rep[m])})
    terc = pd.qcut(vol20, 3, labels=["basse", "moyenne", "haute"])
    for lab in ["basse", "moyenne", "haute"]:
        cond.append({"variable": "vol 20 j (tercile)", "état": lab, **desc(rep[terc == lab])})
    cond = pd.DataFrame(cond)
    cond.round(4).to_csv(OUT / "cond.csv", index=False)
    log("\n=== 5. Conditionnement (variables connues à 17:00 la veille) ===")
    log(cond.round(2).to_string(index=False))
    for name, x in [("séance précédente", prev_day), ("tendance 20 j", trend20)]:
        a, b = rep[x > 0].dropna(), rep[x < 0].dropna()
        tw = st.ttest_ind(a, b, equal_var=False)
        log(f"  écart {name} > 0 vs < 0 : {(a.mean()-b.mean())*1e4:+.2f} bp, t Welch {tw.statistic:+.2f}")
    log(f"  corr(séance précédente, reprise) {prev_day.corr(rep):+.3f}")

    # 6. liquidité : volume moyen par minute, par tranche horaire NY
    df = E.load("GC")
    df = df[(df.index >= START) & (df.index <= f"{END} 23:59")]
    hh = df.index.tz_convert(NY).hour
    vol = df["volume"].groupby(hh).mean()
    vol.round(1).to_csv(OUT / "volume.csv")
    log("\n=== 6. Volume moyen par minute (contrats), par heure NY ===")
    log(" ".join(f"{h:02d}h {v:.0f}" for h, v in vol.items()))
    log(f"  reprise (18-20 h) {vol.loc[[18, 19]].mean():.0f} contre COMEX (8-13 h) {vol.loc[8:13].mean():.0f}")

    yr = legs.groupby(legs.index.year).mean().mul(1e4)
    yr.round(2).to_csv(OUT / "by_year.csv")
    log("\n=== Par année (bp) ===")
    log(yr.round(1).to_string())
    (OUT / "run.log").write_text("\n".join(LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
