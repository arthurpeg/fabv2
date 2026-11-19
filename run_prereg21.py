"""Pré-enregistrement n° 21 : continuation de la nuit (17:00 veille → 5:00 NY) sur le reste du jour
(5:00 → 17:00 NY), or et argent au comptant, 2003-2017 (hors échantillon dans le temps).

uv run python run_prereg21.py   → results/prereg21/ (run.log, days_XAU.csv, days_XAG.csv, by_year.csv)

Protocole figé dans PREREGISTRATION_21.md (commit a2dc0b1) ; rien n'est modifié ici.
Données : cache/lse/XAU_lse_1m.parquet, XAG_lse_1m.parquet (fetch_lse.py, marché commodities).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as st

import recolte1.engine as E
from run_gc_sessions import NY, holm, nw_t

OUT = Path("results/prereg21")
ASSETS = {  # code : (fin de période, coût aller-retour en $/oz, coupure des sous-périodes)
    "XAU": ("2015-12-31", 0.15),
    "XAG": ("2017-03-31", 0.006),
}
START = "2003-05-05"
SPLIT = "2009-01-01"
LINES: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


def price_at(df: pd.DataFrame, when: pd.Series) -> pd.Series:
    """Clôture de la dernière barre démarrant dans [T−5 min, T−1 min] (règle de recolte1.engine.price_at)."""
    t = df.index.as_unit("ns").asi8
    w = pd.DatetimeIndex(when).as_unit("ns").asi8
    pos = np.searchsorted(t, w - 60 * 10**9, side="right") - 1
    ok = (pos >= 0) & (when.notna().values)
    pos = np.maximum(pos, 0)
    ok &= t[pos] >= w - 5 * 60 * 10**9
    return pd.Series(np.where(ok, df["close"].values[pos], np.nan), index=when.index)


def slope(n: np.ndarray, d: np.ndarray) -> dict:
    nc, dc = n - n.mean(), d - d.mean()
    c = (nc * dc).sum() / (nc ** 2).sum()
    e = dc - c * nc
    se = np.sqrt((nc ** 2 * e ** 2).sum()) / (nc ** 2).sum()  # White HC0
    return {"c": c, "se": se, "t": c / se, "p1": st.norm.sf(c / se), "n": len(n)}


def p_one_sided_boot(x: np.ndarray) -> float:
    """p unilatéral (moyenne > 0), bootstrap par blocs recentré sous H0."""
    idx = E._block_index(len(x))
    b = (x - x.mean())[idx].mean(1)
    return float((b >= x.mean()).mean())


def run(code: str, end: str, cost: float) -> dict:
    df = pd.read_parquet(E.LSE / f"{code}_lse_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    d = pd.bdate_range(START, end)
    p0 = price_at(df, E.at(d - pd.offsets.BDay(1), "17:00", NY).set_axis(d))
    p1 = price_at(df, E.at(d, "05:00", NY))
    p2 = price_at(df, E.at(d, "17:00", NY))
    t = pd.DataFrame({"p0": p0, "p1": p1, "p2": p2}).dropna()
    t["N"] = np.log(t.p1 / t.p0)
    t["D"] = np.log(t.p2 / t.p1)
    # règle : sens de N, 5:00 → 17:00, coût aller-retour rapporté au prix d'entrée
    sgn = np.sign(t["N"])
    t["rule_gross"] = sgn * (t.p2 / t.p1 - 1)
    t["rule_net"] = t["rule_gross"] - (sgn != 0) * cost / t.p1
    t.round(8).to_csv(OUT / f"days_{code}.csv")

    log(f"\n=== {code} {t.index[0].date()} → {t.index[-1].date()} : {len(t)} jours "
        f"(sur {len(d)} jours ouvrés) ===")
    log(f"N (17:00 veille → 5:00) : moyenne {t.N.mean()*1e4:+.2f} bp, σ {t.N.std()*1e4:.1f} ; "
        f"D (5:00 → 17:00) : moyenne {t.D.mean()*1e4:+.2f} bp, σ {t.D.std()*1e4:.1f}")
    main = slope(t.N.values, t.D.values)
    log(f"Pente c (principal) : {main['c']:+.4f} (se {main['se']:.4f}, t {main['t']:+.2f}, p unilatéral {main['p1']:.4f}) "
        f"→ b = {1 + main['c']:.3f}")
    subs = {}
    for name, m in [("2003-2008", t.index < SPLIT), (f"2009-{end[:4]}", t.index >= SPLIT)]:
        s = slope(t.N.values[m], t.D.values[m])
        subs[name] = s
        log(f"   {name} : c {s['c']:+.4f} (t {s['t']:+.2f}, n {s['n']})")
    q = lambda z: np.clip(z, *np.percentile(z, [1, 99]))
    w = slope(q(t.N.values), q(t.D.values))
    rho = st.spearmanr(t.N, t.D)
    log(f"Rapportés : c winsorisé 1 % {w['c']:+.4f} (t {w['t']:+.2f}) ; corrélation de rang {rho.statistic:+.4f} (p {rho.pvalue:.4f})")
    yr = pd.DataFrame([{"année": y, "actif": code, **slope(g.N.values, g.D.values)} for y, g in t.groupby(t.index.year)])
    log("c par année : " + ", ".join(f"{int(r.année)} {r.c:+.3f}" for r in yr.itertuples()))
    rules = {}
    for k in ("rule_gross", "rule_net"):
        x = t[k].values
        m_, lo, hi = E.ci_mean(x)
        rules[k] = {"moy_bp": m_ * 1e4, "lo": lo * 1e4, "hi": hi * 1e4, "t_nw": nw_t(x), "p1": p_one_sided_boot(x)}
        log(f"Règle {k.split('_')[1]} : {m_*1e4:+.2f} bp/jour [{lo*1e4:+.2f} ; {hi*1e4:+.2f}], t NW {nw_t(x):+.2f}, "
            f"p unilatéral {rules[k]['p1']:.4f}, Sharpe {x.mean()/x.std()*np.sqrt(252):+.2f}")
    log(f"Coût moyen aller-retour : {(cost / t.p1).mean()*1e4:.2f} bp")
    return {"main": main, "subs": subs, "rules": rules, "yr": yr}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {c: run(c, e, k) for c, (e, k) in ASSETS.items()}
    p = np.array([res[c]["main"]["p1"] for c in ASSETS])
    ph = holm(p)
    log("\n=== Décision (critères fixés dans PREREGISTRATION_21.md) ===")
    ok = {}
    for (c, r), h in zip(res.items(), ph):
        sub_ok = all(s["c"] > 0 for s in r["subs"].values())
        ok[c] = (h < 0.05) and sub_ok
        log(f"{c} : c {r['main']['c']:+.4f}, p unilatéral {r['main']['p1']:.4f}, p Holm {h:.4f} ; "
            f"signe positif dans les 2 sous-périodes : {sub_ok} → {'remplit' if ok[c] else 'ne remplit pas'} 1 et 2")
    n_ok = sum(ok.values())
    log("VERDICT : " + ("SUCCÈS" if n_ok == 2 else "SUCCÈS PARTIEL" if n_ok == 1 else "ÉCHEC"))
    rp = holm(np.array([res[c]["rules"]["rule_net"]["p1"] for c in ASSETS]))
    for (c, r), h in zip(res.items(), rp):
        log(f"Règle nette {c} (secondaire) : {r['rules']['rule_net']['moy_bp']:+.2f} bp/jour, p unilatéral Holm {h:.4f}")
    pd.concat([r["yr"] for r in res.values()]).round(5).to_csv(OUT / "by_year.csv", index=False)
    (OUT / "run.log").write_text("\n".join(LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
