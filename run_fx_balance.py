"""Étape 1 (exploration) de wiki/experiments/fx-exportateur-importateur : la devise d'un pays exportateur
monte-t-elle pendant sa session domestique, et celle d'un importateur baisse-t-elle ?

uv run --with statsmodels python run_fx_balance.py --qc   → contrôle de qualité seulement (aucun rendement)
uv run --with statsmodels python run_fx_balance.py        → exploration 2010-01-01 → 2021-08-31

Sorties : results/fx_balance/ (qc.csv, sessions_dom.csv, tests.csv, par_devise.csv, summary.txt).

======================================================================================================
GRILLE FIGÉE (commitée avant tout calcul de rendement sur ces devises ; ne pas modifier après calcul)
======================================================================================================
Univers candidat : USDNOK, USDSEK, USDPLN, USDCZK, USDHUF, USDRON, USDILS, USDMXN, USDZAR, USDSGD,
  USDTHB, USDTRY (Dukascopy, barres 1 h bid/ask, mid). Exclues d'office : CNH, DKK, HKD (ancrées ou
  administrées) ; les 7 majeures (déjà vues au n° 27).
Critère de qualité (fixé avant le contrôle, appliqué sans regarder de rendement) : une devise est gardée
  si sa barre horaire existe pour ≥ 90 % des heures de semaine de son créneau 08-16 local sur
  2010-01 → 2026-08-28, et si aucun trou de semaine ne dépasse 120 heures. Le spread est rapporté,
  sans critère (parcours phénomène).
Session domestique : 08:00 → 16:00 heure locale (comme Zhang 2018), lundi-vendredi, grille horaire GMT
  de run_zhang.py. Prix en dollars par unité de devise (signe inversé pour USDxxx) : rendement > 0 =
  la devise monte. Places : Oslo, Stockholm, Varsovie, Prague, Budapest, Bucarest, Jérusalem, Mexico,
  Johannesburg, Singapour, Bangkok, Istanbul.
Variable : solde des biens et services en % du PIB (Banque mondiale NE.RSB.GNFS.ZS, données du
  2026-11-11, results/fx_balance/solde_commercial_wb.csv) de l'année civile PRÉCÉDENTE. Exportateur =
  solde > 0, importateur = solde < 0. Limite : séries révisées, pas de vintage en temps réel.
Tranche : exploration = sessions entièrement comprises entre 2010-01-01 et 2021-09-01 (exclu).
  Réserve 2021-09-01 → 2026-08-28 : aucun rendement calculé (garde-fou dans le code).
Tests (3 essais ; compteur 1 937 → 1 940), t de Newey-West 5 retards, unilatéraux, Holm sur 3 :
  T1 (principal) : chaque jour, moyenne des rendements domestiques des exportateurs − moyenne des
     importateurs, sur tout l'univers retenu ; jours où un côté est vide sautés. H : moyenne > 0.
  T2 (même fuseau) : idem, restreint aux devises européennes de l'univers (heures identiques : l'effet
     d'heure du dollar s'annule). H : moyenne > 0.
  T3 (panel) : chaque jour, pente de la régression en coupe du rendement domestique sur le rang du
     solde (rangs centrés réduits dans l'univers du jour, ≥ 4 devises) ; moyenne des pentes
     (Fama-MacBeth). H : moyenne > 0.
Référence triviale : (a) moyenne domestique toutes devises confondues (hypothèse H1 de Zhang) ;
  (b) pour T1 et T2, 1 000 tirages où les étiquettes exportateur / importateur sont permutées entre
  devises chaque année (mêmes effectifs) : centile de la moyenne observée.
Descriptif non compté : moyenne domestique par devise, par moitié de tranche, par année.
Barrière B1 (PROTOCOLE.md) appliquée à T1, puis T2 ; parcours phénomène seulement (pas de coût).
======================================================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

from run_zhang import hourly_grid, nw_t

sys.stdout.reconfigure(encoding="utf-8")
DK = Path("cache/dukascopy")
OUT = Path("results/fx_balance")
OUT.mkdir(parents=True, exist_ok=True)
# devise → (paire Dukascopy, place, pays ISO3, européenne)
CUR = {
    "NOK": ("USDNOK", "Europe/Oslo", "NOR", True),
    "SEK": ("USDSEK", "Europe/Stockholm", "SWE", True),
    "PLN": ("USDPLN", "Europe/Warsaw", "POL", True),
    "CZK": ("USDCZK", "Europe/Prague", "CZE", True),
    "HUF": ("USDHUF", "Europe/Budapest", "HUN", True),
    "RON": ("USDRON", "Europe/Bucharest", "ROU", True),
    "ILS": ("USDILS", "Asia/Jerusalem", "ISR", False),
    "MXN": ("USDMXN", "America/Mexico_City", "MEX", False),
    "ZAR": ("USDZAR", "Africa/Johannesburg", "ZAF", False),
    "SGD": ("USDSGD", "Asia/Singapore", "SGP", False),
    "THB": ("USDTHB", "Asia/Bangkok", "THA", False),
    "TRY": ("USDTRY", "Europe/Istanbul", "TUR", False),
}
A, B = "2010-01-01", "2021-09-01"       # exploration (B exclu)
FIN = "2026-08-29"                      # fin des données téléchargées (exclue)
COUV_MIN, TROU_MAX = 0.90, 120          # critère de qualité figé
N_PERM = 1000


def load(pair: str) -> pd.DataFrame:
    return pd.read_parquet(DK / f"{pair}_1h.parquet")


def heures_dom(place: str, a: str, b: str) -> pd.DatetimeIndex:
    """Débuts d'heure (UTC) de la session 08-16 locale, lundi-vendredi, entre a et b."""
    h = pd.date_range(pd.Timestamp(a, tz="UTC"), pd.Timestamp(b, tz="UTC"), freq="1h", inclusive="left")
    loc = h.tz_convert(place)
    return h[(loc.hour >= 8) & (loc.hour < 16) & (loc.dayofweek < 5)]


def qc() -> pd.DataFrame:
    """Comptes, trous et spreads seulement : aucune moyenne de rendement (règle des réserves)."""
    rows = []
    for c, (pair, place, iso, _) in CUR.items():
        df = load(pair)
        dom = heures_dom(place, A, FIN)
        present = dom.isin(df.index)
        wk = pd.date_range(pd.Timestamp(A, tz="UTC"), pd.Timestamp(FIN, tz="UTC"), freq="1h", inclusive="left")
        wk = wk[wk.dayofweek < 5]
        have = wk.isin(df.index)
        run = (have != np.roll(have, 1)).cumsum()
        trous = pd.Series(~have).groupby(run).sum()
        sp = (df["spread_close"] / df["mid_close"] * 1e4)
        loc = df.index.tz_convert(place)
        a8 = sp[(loc.hour == 7)]   # barre 07:00-08:00 locale : spread à l'ouverture de la session
        a16 = sp[(loc.hour == 15)]  # barre 15:00-16:00 locale : spread à la fermeture
        expl = df.index < pd.Timestamp(B, tz="UTC")
        rows.append({
            "devise": c, "debut": df.index.min().date(), "fin": df.index.max().date(),
            "couverture_dom": present.mean(), "trou_max_h": int(trous.max()),
            "spread_08_bp_expl": a8[expl[loc.hour == 7]].median(),
            "spread_16_bp_expl": a16[expl[loc.hour == 15]].median(),
            "spread_08_bp_reserve": a8[~expl[loc.hour == 7]].median(),
            "barres_figees_%": 100 * ((df["high"] == df["low"]) & (df["ask_high"] == df["ask_low"])).mean(),
        })
    q = pd.DataFrame(rows).set_index("devise")
    q["garde"] = (q.couverture_dom >= COUV_MIN) & (q.trou_max_h <= TROU_MAX)
    q.to_csv(OUT / "qc.csv")
    print(q.round(3).to_string())
    return q


def solde() -> pd.Series:
    s = pd.read_csv(OUT / "solde_commercial_wb.csv")
    return s.set_index(["pays", "annee"])["solde_biens_services_pct_pib"]


def sessions_dom(c: str) -> pd.DataFrame:
    pair, place, iso, eur = CUR[c]
    df = load(pair)
    p = hourly_grid(df["mid_close"], A, B)
    assert p.index.max() < pd.Timestamp(B, tz="UTC"), "garde-fou : rien dans la réserve"
    r = -np.log(p).diff().dropna()          # USD par devise : signe inversé
    start = r.index - pd.Timedelta(hours=1)
    loc = start.tz_convert(place)
    m = (loc.hour >= 8) & (loc.hour < 16) & (loc.dayofweek < 5)
    g = pd.DataFrame({"r": r.values[m], "jour": loc[m].date, "start": start[m]})
    s = g.groupby("jour").agg(ret=("r", "sum"), n=("r", "size"), start=("start", "min"))
    s = s[(s.n == 8) & (s.start >= pd.Timestamp(A, tz="UTC"))]
    s["ret"] *= 1e4
    s["devise"], s["pays"], s["eur"] = c, iso, eur
    s.index = pd.to_datetime(s.index)
    return s.reset_index().rename(columns={"index": "jour"})


def portefeuille(d: pd.DataFrame) -> pd.Series:
    x = d.dropna(subset=["exp"])
    e = x[x.exp == 1].groupby("jour").ret.mean()
    i = x[x.exp == 0].groupby("jour").ret.mean()
    return (e - i).dropna()


def fama_macbeth(d: pd.DataFrame) -> pd.Series:
    out = {}
    for j, g in d.dropna(subset=["tb"]).groupby("jour"):
        if len(g) < 4:
            continue
        z = g.tb.rank()
        z = (z - z.mean()) / z.std()
        out[j] = float(np.polyfit(z, g.ret, 1)[0])
    return pd.Series(out)


def permutation(d: pd.DataFrame, obs: float, rng) -> float:
    vals = []
    for _ in range(N_PERM):
        x = d.dropna(subset=["exp"]).copy()
        for y, g in x.groupby(x.jour.dt.year):
            cur = g.devise.unique()
            lab = dict(zip(cur, rng.permutation([float(g.loc[g.devise == c, "exp"].iloc[0]) for c in cur])))
            x.loc[g.index, "exp"] = g.devise.map(lab)
        vals.append(portefeuille(x).mean())
    return float((np.array(vals) < obs).mean())


def main() -> None:
    q = qc() if "--qc" in sys.argv else pd.read_csv(OUT / "qc.csv", index_col=0)
    if "--qc" in sys.argv:
        return
    gardees = [c for c in CUR if bool(q.loc[c, "garde"])]
    tb = solde()
    d = pd.concat([sessions_dom(c) for c in gardees], ignore_index=True)
    d["tb"] = [tb.get((p, y - 1), np.nan) for p, y in zip(d.pays, d.jour.dt.year)]
    d["exp"] = np.where(d.tb.isna(), np.nan, (d.tb > 0).astype(float))
    d.to_csv(OUT / "sessions_dom.csv", index=False)
    rng = np.random.default_rng(20261122)

    res = []
    t1 = portefeuille(d)
    t2 = portefeuille(d[d.eur])
    t3 = fama_macbeth(d)
    for nom, s, perm in (("T1 tout l'univers", t1, d), ("T2 fuseau européen", t2, d[d.eur]), ("T3 Fama-MacBeth (rang)", t3, None)):
        t = nw_t(s)
        h = len(s) // 2
        yrs = s.groupby(pd.to_datetime(s.index).year).mean()
        row = {"test": nom, "n_jours": len(s), "moyenne_bp": s.mean(), "t_nw": t,
               "p_unilateral": float(norm.sf(t)),
               "moitie1": s.iloc[:h].mean(), "moitie2": s.iloc[h:].mean(),
               "annees_pos": f"{int((yrs > 0).sum())}/{len(yrs)}"}
        if perm is not None:
            row["centile_permutation"] = permutation(perm, s.mean(), rng)
        res.append(row)
    r = pd.DataFrame(res)
    p = r.p_unilateral.values
    o = np.argsort(p)
    adj = np.empty(3)
    run = 0.0
    for k, i in enumerate(o):
        run = max(run, min(1.0, (3 - k) * p[i]))
        adj[i] = run
    r["p_holm"] = adj
    r.to_csv(OUT / "tests.csv", index=False)

    pdv = d.groupby("devise").agg(n=("ret", "size"), moyenne_bp=("ret", "mean"),
                                  solde_moyen=("tb", "mean"), part_exportateur=("exp", "mean"))
    pdv["t_nw"] = [nw_t(d[d.devise == c].set_index("jour").ret) for c in pdv.index]
    pdv.to_csv(OUT / "par_devise.csv")
    ref = d.groupby("jour").ret.mean()

    lines = ["Exploration 2010-01-01 → 2021-08-31, devises gardées : " + ", ".join(gardees),
             "", r.round(4).to_string(index=False), "",
             f"Référence (a) moyenne domestique toutes devises : {ref.mean():+.3f} bp, t NW {nw_t(ref):.2f}",
             "", pdv.round(3).to_string()]
    (OUT / "summary.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
