"""Rendement de l'or (GC) par session, 1 minute Databento 2016-2026.

uv run python run_gc_sessions.py   → results/gc_sessions/ (run.log, sessions.csv, summary.csv,
by_period.csv, by_year.csv, hours.csv)

Exploratoire, non pré-enregistré, demandé en séance. Question : quelle session de la journée
de l'or rapporte, et est-ce significatif ?

Jour GC = clôture 17:00 NY du jour ouvré précédent (vendredi pour le lundi) → 17:00 NY : la
première session contient l'arrêt 17:00 → 18:00 et le gap de réouverture (pas de barre dans
[17:55, 17:59], la borne 18:00 n'a pas de prix) ; lundi à vendredi, arrêt au 2026-08-28 (holdout non touché). Sessions (heures murales, heure d'été gérée
par fuseau), partition de la séance :
  reprise   17:00 NY (veille)      → 09:00 Shanghai (ouverture SGE, 20:00 ou 21:00 NY)
  asie      09:00 Shanghai          → 08:00 Londres
  ldn_am    08:00 Londres           → 10:30 Londres (fixing LBMA du matin)
  ldn_mid   10:30 Londres           → 08:20 NY (ouverture de la séance COMEX)
  comex_am  08:20 NY                → 15:00 Londres (fixing LBMA de l'après-midi)
  comex_pm  15:00 Londres           → 13:30 NY (règlement COMEX)
  post      13:30 NY                → 17:00 NY (arrêt quotidien)
Puis une décomposition heure par heure (23 heures NY ; la première, 17:00 veille → 19:00, inclut l'arrêt).

Prix à un instant = clôture ajustée (ratio aux roulements G J M Q V Z, recolte1.engine.load)
de la dernière barre démarrant dans [T-5 min, T-1 min]. Rendement de chaque session long
calculé par vectorbt (recolte1.engine.run), brut et net (1 tick + 5 $ aller-retour), contrôlé
contre le calcul direct.

Significativité : t de Newey-West (5 retards), IC 95 % bootstrap par blocs, Holm sur les
7 sessions, Benjamini-Hochberg sur les 23 heures, stabilité par sous-période et par année.
L'or a triplé sur la période : on teste aussi l'écart à la dérive « proportionnelle »
(moyenne journalière × part de la durée de la session), pour savoir si une session capte
plus que sa part de la tendance.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as st

import recolte1.engine as E

OUT = Path("results/gc_sessions")
NY, LDN, SH = "America/New_York", "Europe/London", "Asia/Shanghai"
START, END = "2016-01-04", "2026-08-28"
PERIODS = [("2016-2019", "2016", "2019"), ("2020-2022", "2020", "2022"), ("2023-2026", "2023", "2026")]
SESS = ["reprise", "asie", "ldn_am", "ldn_mid", "comex_am", "comex_pm", "post"]
LABEL = {
    "reprise": "Reprise 17:00 NY veille → 9:00 Shanghai",
    "asie": "Asie 9:00 Shanghai → 8:00 Londres",
    "ldn_am": "Londres 8:00 → fix AM 10:30",
    "ldn_mid": "Fix AM 10:30 Ldn → 8:20 NY",
    "comex_am": "COMEX 8:20 NY → fix PM 15:00 Ldn",
    "comex_pm": "Fix PM 15:00 Ldn → 13:30 NY",
    "post": "Post-règlement 13:30 → 17:00 NY",
}
LINES: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


def bounds() -> pd.DataFrame:
    d = pd.bdate_range(START, END)
    b = pd.DataFrame(index=d)
    b["t_0"] = E.at(d - pd.offsets.BDay(1), "17:00", NY).set_axis(d)
    b["t_1"] = E.at(d, "09:00", SH)
    b["t_2"] = E.at(d, "08:00", LDN)
    b["t_3"] = E.at(d, "10:30", LDN)
    b["t_4"] = E.at(d, "08:20", NY)
    b["t_5"] = E.at(d, "15:00", LDN)
    b["t_6"] = E.at(d, "13:30", NY)
    b["t_7"] = E.at(d, "17:00", NY)
    t = b[[f"t_{i}" for i in range(8)]]
    assert (t.diff(axis=1).iloc[:, 1:].apply(lambda c: c.dt.total_seconds()) > 0).all().all()
    for i in range(8):
        b[f"p_{i}"], b[f"f_{i}"] = E.price_at("GC", b[f"t_{i}"])
    return b


def nw_t(x: np.ndarray, lags: int = 5) -> float:
    """t de la moyenne avec variance de Newey-West."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    u = x - x.mean()
    n = len(u)
    v = (u ** 2).sum() / n
    for k in range(1, lags + 1):
        v += 2 * (1 - k / (lags + 1)) * (u[k:] * u[:-k]).sum() / n
    return x.mean() / np.sqrt(v / n)


def holm(p: np.ndarray) -> np.ndarray:
    o = np.argsort(p)
    m = len(p)
    adj = np.maximum.accumulate((m - np.arange(m)) * p[o])
    out = np.empty(m)
    out[o] = np.minimum(adj, 1)
    return out


def bh(p: np.ndarray) -> np.ndarray:
    o = np.argsort(p)[::-1]
    m = len(p)
    adj = np.minimum.accumulate(p[o] * m / (m - np.arange(m)))
    out = np.empty(m)
    out[o] = np.minimum(adj, 1)
    return out


def describe(r: pd.Series, share: float, drift: float) -> dict:
    """r en fraction ; share = part de la durée de la séance ; drift = moyenne journalière C2C."""
    r = r.dropna()
    t = nw_t(r.values)
    m, lo, hi = E.ci_mean(r.values)
    ex = r - share * drift
    return {
        "n": len(r), "moy_bp": m * 1e4, "ic_lo": lo * 1e4, "ic_hi": hi * 1e4,
        "t_nw": t, "p": 2 * st.norm.sf(abs(t)), "pos%": (r > 0).mean() * 100,
        "sigma_bp": r.std() * 1e4, "sharpe": r.mean() / r.std() * np.sqrt(252),
        "part_durée%": share * 100, "excès_bp": ex.mean() * 1e4, "t_excès": nw_t(ex.values),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    b = bounds()
    full = b.dropna(subset=[f"p_{i}" for i in range(8)])
    log(f"GC, {len(b)} jours ouvrés {b.index[0].date()} → {b.index[-1].date()}, "
        f"{len(full)} complets (8 bornes présentes)")

    # heures de cotation : la reprise compte depuis la réouverture de 18:00 (dimanche le lundi)
    dur = pd.DataFrame({s: (full[f"t_{i+1}"] - full[f"t_{i}"]).dt.total_seconds() / 3600
                        for i, s in enumerate(SESS)})
    dur["reprise"] = (full["t_1"] - E.at(full.index, "18:00", NY, -1)).dt.total_seconds() / 3600
    tot = dur.sum(axis=1)
    share = (dur.div(tot, axis=0)).mean()
    log("Durée moyenne (h) : " + ", ".join(f"{s} {dur[s].mean():.2f}" for s in SESS)
        + f" ; séance {tot.mean():.2f} h")

    # rendements directs, contrôle de décomposition
    sess = pd.DataFrame({s: full[f"p_{i+1}"] / full[f"p_{i}"] - 1 for i, s in enumerate(SESS)})
    c2c = full["p_7"] / full["p_0"] - 1
    assert np.allclose((1 + sess).prod(axis=1) - 1, c2c, atol=1e-10)
    sess["séance"] = c2c
    sess.mul(1e4).round(3).to_csv(OUT / "sessions.csv")
    drift = c2c.mean()

    # vectorbt : long sur chaque session, brut et net
    net = {}
    for i, s in enumerate(SESS):
        tr = pd.DataFrame({"t_in": full[f"t_{i}"], "t_out": full[f"t_{i+1}"], "w": 1.0, "day": full.index})
        res = E.run("GC", tr)
        g = res["gross"]["trades"].set_index("day")["ret"].sort_index()
        assert len(g) == len(full) and np.allclose(g.values, sess[s].reindex(g.index).values, atol=1e-9)
        net[s] = res["net"]["trades"].set_index("day")["ret"].sort_index()

    rows = []
    for s in SESS + ["séance"]:
        sh = 1.0 if s == "séance" else share[s]
        d = describe(sess[s], sh, drift)
        if s in net:
            n_ = net[s]
            d["net_bp"] = n_.mean() * 1e4
            d["t_net"] = nw_t(n_.values)
            d["sharpe_net"] = n_.mean() / n_.std() * np.sqrt(252)
        rows.append({"session": s, "libellé": LABEL.get(s, "Séance 17:00 → 17:00"), **d})
    summ = pd.DataFrame(rows)
    m = summ["session"] != "séance"
    summ.loc[m, "p_holm"] = holm(summ.loc[m, "p"].values)
    summ.loc[m, "p_excès"] = 2 * st.norm.sf(summ.loc[m, "t_excès"].abs())
    summ.loc[m, "p_excès_holm"] = holm(summ.loc[m, "p_excès"].values)
    summ.round(4).to_csv(OUT / "summary.csv", index=False)

    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    log(f"\nDérive journalière (séance 17:00 → 17:00) : {drift*1e4:+.2f} bp")
    log("\n=== Sessions (toute la période ; bp, t Newey-West 5 retards, IC bootstrap par blocs) ===")
    cols = ["session", "n", "moy_bp", "ic_lo", "ic_hi", "t_nw", "p", "p_holm", "pos%", "sigma_bp",
            "sharpe", "net_bp", "t_net", "sharpe_net", "part_durée%", "excès_bp", "t_excès", "p_excès_holm"]
    log(summ[cols].round(3).to_string(index=False))

    per = []
    for pn, a, z in PERIODS:
        mm = (sess.index >= a) & (sess.index <= f"{z}-12-31")
        dr = c2c[mm].mean()
        for s in SESS + ["séance"]:
            sh = 1.0 if s == "séance" else share[s]
            per.append({"période": pn, "session": s, **describe(sess[s][mm], sh, dr)})
    per = pd.DataFrame(per)
    per.round(4).to_csv(OUT / "by_period.csv", index=False)
    log("\n=== Par sous-période : moyenne (bp) ===")
    log(per.pivot(index="session", columns="période", values="moy_bp").loc[SESS + ["séance"]].round(2).to_string())
    log("t Newey-West")
    log(per.pivot(index="session", columns="période", values="t_nw").loc[SESS + ["séance"]].round(2).to_string())
    log("excès sur la dérive proportionnelle (bp)")
    log(per.pivot(index="session", columns="période", values="excès_bp").loc[SESS].round(2).to_string())

    yr = sess.groupby(sess.index.year).mean().mul(1e4)
    yr.round(2).to_csv(OUT / "by_year.csv")
    log("\n=== Par année : moyenne (bp) ===")
    log(yr.round(1).to_string())
    log("Années positives : " + ", ".join(f"{s} {(yr[s] > 0).sum()}/{len(yr)}" for s in SESS + ["séance"]))

    # heure par heure, 17:00 veille → 17:00 NY (la première tranche couvre 17:00 → 19:00, arrêt compris)
    d = pd.bdate_range(START, END)
    hrs = [(-1, h) for h in range(18, 24)] + [(0, h) for h in range(0, 18)]
    edges = [E.at(d - pd.offsets.BDay(1), "17:00", NY).set_axis(d)]
    for off, h in hrs[1:]:
        edges.append(E.at(d, f"{h:02d}:00", NY, off))
    px = [E.price_at("GC", e)[0] for e in edges]
    hr = []
    for k in range(len(edges) - 1):
        r = px[k + 1] / px[k] - 1
        off, h = hrs[k]
        dd = describe(r, 1 / 23, drift)
        hr.append({"heure_NY": f"{h:02d}:00", **{k_: dd[k_] for k_ in ["n", "moy_bp", "ic_lo", "ic_hi", "t_nw", "p",
                                                                      "pos%", "sigma_bp", "excès_bp", "t_excès"]},
                   **{f"moy_{pn}": (r[(r.index >= a) & (r.index <= f'{z}-12-31')].mean() * 1e4)
                      for pn, a, z in PERIODS}})
    hr = pd.DataFrame(hr)
    hr["q_bh"] = bh(hr["p"].values)
    hr["p_excès"] = 2 * st.norm.sf(hr["t_excès"].abs())
    hr["q_excès_bh"] = bh(hr["p_excès"].values)
    hr.round(4).to_csv(OUT / "hours.csv", index=False)
    log("\n=== Heure par heure (heure NY de début ; rendement h → h+1, brut) ===")
    log(hr.round(2).to_string(index=False))
    log(f"\nSomme des moyennes horaires : {hr['moy_bp'].sum():+.2f} bp (séance {drift*1e4:+.2f})")
    (OUT / "run.log").write_text("\n".join(LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
