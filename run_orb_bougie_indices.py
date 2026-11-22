"""Règle de la 1ʳᵉ bougie de 5 minutes (Zarattini-Aziz 2023) sur ES, YM et NQ avec d'autres sorties. Étape 1, suite.

Fiche : wiki/experiments/nq-orb-bougie-sorties.md (section « Suite : ES, YM et stop 1 ATR »). Grille figée ici et
commitée AVANT tout calcul. Même règle, mêmes conventions que run_nq_orb_bougie.py (commit a49ca1a), qui a déjà
calculé les 25 premières variantes sur NQ.

DONNÉES
- ES, YM, NQ Databento 1 min : 2010-06 → 2015-12-31 (cache/databento_2010, prix bruts) puis 2016-01-01 → 2021-09-30
  (fab.core.load, ramené en prix bruts par le facteur de roulement). Rien après le 2021-09-30 : la réserve de la
  question « sortie » (2021-10-01 → 2026-08-28, wiki/reserves.md, déclarée pour ES et YM avec ce commit) n'est pas lue.

RÈGLE D'ENTRÉE (identique à R4) : sens de la bougie 9:30-9:35 ET, doji si |C1 − O1| ≤ 1 tick, entrée à l'open de 9:35.

SORTIES
- ES et YM : la grille de NQ entière, V0 (aucun stop ni objectif) + k ∈ {0,05 ; 0,10 ; 0,25 ; 0,50} × RR ∈ {1, 2, 3, 5,
  10, clôture} = 25 variantes, plus k = 1,00 × RR ∈ {2, 3} = 2 variantes. 27 par actif.
- NQ : seulement les 2 nouvelles variantes k = 1,00, RR ∈ {2, 3} (les 25 autres sont déjà calculées ; elles sont
  recalculées ici pour la famille et le détail, sans être recomptées).
- ATR14 = moyenne des amplitudes 9:30-16:00 des 14 séances précédentes. Stop prioritaire si stop et objectif tombent
  dans la même minute ; sortie à l'open si une barre ouvre au-delà du niveau ; sinon sortie à 16:00.

RÉFÉRENCES (non comptées) : R4 (stop à l'extrême de la bougie, 10R) et « toujours long » avec les mêmes sorties.

COÛT : 1 contrat, points par trade, coût standard 1 tick + 5 $ (ES 0,35 pt, YM 2 pts, NQ 0,50 pt).

CHOIX ET BARRIÈRE : par actif, meilleur Sharpe net par trade parmi ses 27 variantes ; n_famille = 28 (27 + R4).
DÉTAIL demandé (descriptif, pas un choix) : k 0,50 RR 2, k 0,50 RR 3, k 1,00 RR 2, k 1,00 RR 3, et V0, sur les trois
actifs : par année, achat / vente, types de sortie, gain et perte moyens, résultat en R, creux, $ par an.

Compteur global : 1 965 → 2 021 (ES 27 + YM 27 + NQ 2 = 56 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from fab.core import ASSETS, NY, load
from fab.protocole import barriere_exploration, fiche, imprimer
from run_nq_orb_bougie import first_open, simule

FIN_EXPLO = pd.Timestamp("2021-09-30")
OUT = Path("results/orb_bougie_indices")
OPEN, ENTREE, FERME = 570, 575, 960
KS = [0.05, 0.10, 0.25, 0.50]
RRS = [1, 2, 3, 5, 10, None]
DETAIL = ["V0 sans stop ni objectif", "k=0.50 RR=2", "k=0.50 RR=3", "k=1.00 RR=2", "k=1.00 RR=3"]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def matrices(name: str) -> dict[str, pd.DataFrame]:
    a = pd.read_parquet(f"cache/databento_2010/{name}_v0_1m_2010.parquet")[["open", "high", "low", "close"]]
    a = a[a.index < pd.Timestamp("2016-01-01", tz="UTC")]
    b = load(name)
    b = b[b.index >= pd.Timestamp("2016-01-01", tz="UTC")]
    b = b[["open", "high", "low", "close"]].div(b["factor"], axis=0)
    df = pd.concat([a, b]).sort_index()
    df = df[~df.index.duplicated()]
    loc = df.tz_convert(NY)
    m = loc.index.hour * 60 + loc.index.minute
    keep = (m >= OPEN) & (m < FERME + 5) & (loc.index.dayofweek < 5)
    loc = loc[keep]
    loc = loc.assign(d=loc.index.tz_localize(None).normalize(), m=m[keep])
    loc = loc[loc.d <= FIN_EXPLO]  # garde-fou : rien dans la réserve
    cols = range(OPEN, FERME + 5)
    return {c: loc.pivot(index="d", columns="m", values=c).reindex(columns=cols) for c in ["open", "high", "low", "close"]}


def variantes(name: str) -> list[tuple[str, float | None, float | None, bool]]:
    """(nom, k, RR, comptée dans ce script)."""
    v = [("V0 sans stop ni objectif", None, None, name != "NQ")]
    v += [(f"k={k:.2f} RR={'clôture' if rr is None else rr}", k, rr, name != "NQ") for k in KS for rr in RRS]
    v += [(f"k=1.00 RR={rr}", 1.0, rr, True) for rr in (2, 3)]
    return v


def run(name: str) -> pd.DataFrame:
    a = ASSETS[name]
    tick, cout, pv = a.tick, a.rt_cost, a.point_value
    M = matrices(name)
    O, H, L, C = M["open"], M["high"], M["low"], M["close"]
    sess = list(range(OPEN, FERME))
    atr = (H[sess].max(axis=1) - L[sess].min(axis=1)).rolling(14, min_periods=14).mean().shift(1)
    o1 = first_open(O, OPEN)
    rc = list(range(OPEN, ENTREE))
    c1 = C[rc].ffill(axis=1).iloc[:, -1]
    h1, l1 = H[rc].max(axis=1), L[rc].min(axis=1)
    p_in, p_end = O[ENTREE], first_open(O, FERME)
    ok = o1.notna() & c1.notna() & p_in.notna() & p_end.notna() & atr.notna() & ((c1 - o1).abs() > tick)
    d = pd.DataFrame({"o1": o1, "c1": c1, "h1": h1, "l1": l1, "p_in": p_in, "p_end": p_end, "atr": atr})[ok]
    d["side"] = np.where(d.c1 > d.o1, 1, -1)
    idx = d.index
    tc = list(range(ENTREE, FERME))
    Hm, Lm, Om = H.loc[idx, tc].values, L.loc[idx, tc].values, O.loc[idx, tc].values
    side, pin, pend, a14 = d.side.values, d.p_in.values, d.p_end.values, d.atr.values
    say(f"\n################ {name} : {len(O)} séances ({O.index[0].date()} → {O.index[-1].date()}), {len(d)} trades, "
        f"coût {cout:.2f} pt, ATR14 moyen {d.atr.mean():.1f} pts (2010 {d.atr[idx.year == 2010].mean():.1f}, "
        f"2021 {d.atr[idx.year == 2021].mean():.1f})")
    inf = np.full(len(d), np.inf)
    res = {}
    for vn, k, rr, _ in variantes(name):
        sd = inf if k is None else k * a14
        td = inf if (k is None or rr is None) else rr * sd
        po, kd = simule(side, pin, sd, td, Hm, Lm, Om, pend)
        pl, _ = simule(np.ones_like(side), pin, sd, td, Hm, Lm, Om, pend)
        res[vn] = (pd.Series(side * (po - pin) - cout, idx), pd.Series(pl - pin - cout, idx), kd, sd)
    r4_stop = np.where(side == 1, pin - d.l1.values, d.h1.values - pin)
    r4_ok = r4_stop > 0
    sd4 = np.where(r4_ok, r4_stop, np.inf)
    po4, kd4 = simule(side, pin, sd4, 10 * sd4, Hm, Lm, Om, pend)
    r4 = pd.Series(side * (po4 - pin) - cout, idx)[r4_ok]

    noms = [v[0] for v in variantes(name)]
    sharpes = [res[n][0].mean() / res[n][0].std() for n in noms]
    rows = []
    for vn, k, rr, compte in variantes(name) + [("R4 (référence)", None, None, False)]:
        net, ref, kd = (r4, None, kd4[r4_ok]) if vn.startswith("R4") else res[vn][:3]
        f = fiche(net, None, ref, n_famille=28, sharpes_famille=sharpes, tick_bp=tick)
        y = net.index.year
        rows.append({"actif": name, "variante": vn, "comptee": compte, "n": f["n"], "net_moy_pts": f["net_moy"],
                     "t_nw": f["t_nw"], "sharpe_an": f["sharpe_an"], "gagnants_%": f["gagnants_%"],
                     "stop_%": 100 * (kd == 1).mean(), "objectif_%": 100 * (kd == 2).mean(),
                     "ref_long_moy": f.get("ref_net_moy", np.nan), "t_ecart_ref": f.get("t_ecart_ref", np.nan),
                     "2010-15": net[y <= 2015].mean(), "2016-21": net[y >= 2016].mean(), "2020": net[y == 2020].mean(),
                     "dsr_28": f["dsr_famille"]})
    tab = pd.DataFrame(rows)
    say(tab.drop(columns="actif").round(3).to_string(index=False))

    best = tab[tab.variante.isin(noms)].sort_values("sharpe_an", ascending=False).iloc[0].variante
    net, ref = res[best][0], res[best][1]
    f = fiche(net, net + cout, ref, n_famille=28, sharpes_famille=sharpes, tick_bp=tick)
    say("\n" + imprimer(f, f"{name} : règle choisie (meilleur Sharpe net) = {best}"))
    okb, raisons = barriere_exploration(f)
    say(f"{name} B1 : " + ("✅ franchie" if okb else "❌ ratée") + " | " + " ; ".join(raisons))

    # ---- détail descriptif
    for vn in DETAIL:
        net, _, kd, sd = res[vn]
        y = net.index.year
        R = net / pd.Series(sd, idx) if np.isfinite(sd).all() else pd.Series(np.nan, idx)
        eq = net.cumsum()
        say(f"\n--- {name} détail : {vn} ---")
        say(f"n {len(net)} | net {net.mean():+.2f} pts ({net.mean() * pv:+.0f} $) | médiane {net.median():+.2f} | "
            f"gagnants {100 * (net > 0).mean():.1f} % | gain moyen {net[net > 0].mean():+.2f} | perte moyenne "
            f"{net[net <= 0].mean():+.2f} | sorties stop {100 * (kd == 1).mean():.1f} %, objectif "
            f"{100 * (kd == 2).mean():.1f} %, clôture {100 * (kd == 0).mean():.1f} %")
        say(f"en R : moyenne {R.mean():+.3f} | stop moyen {np.nanmean(np.where(np.isfinite(sd), sd, np.nan)):.1f} pts | "
            f"pire creux {(eq - eq.cummax()).min():.0f} pts ({(eq - eq.cummax()).min() * pv:,.0f} $) | "
            f"achats {net[side == 1].mean():+.2f} (n {int((side == 1).sum())}) | ventes {net[side == -1].mean():+.2f} "
            f"(n {int((side == -1).sum())})")
        par_an = pd.DataFrame({"net_moy_pts": net.groupby(y).mean(), "total_$": net.groupby(y).sum() * pv,
                               "gagnants_%": (net > 0).groupby(y).mean() * 100, "n": net.groupby(y).size()})
        say(par_an.round(2).to_string())
    out = pd.DataFrame({vn: res[vn][0] for vn in DETAIL})
    out["side"] = side
    out.to_csv(OUT / f"trades_detail_{name}.csv")
    return tab


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 260)
    tabs = [run(n) for n in ["ES", "YM", "NQ"]]
    pd.concat(tabs).to_csv(OUT / "grille.csv", index=False)
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
