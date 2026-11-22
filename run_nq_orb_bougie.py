"""NQ : règle de la 1ʳᵉ bougie de 5 minutes (Zarattini-Aziz 2023) avec d'autres sorties. Étape 1 (exploration).

Fiche : wiki/experiments/nq-orb-bougie-sorties.md. Grille figée ici et commitée AVANT tout calcul.

DONNÉES
- NQ Databento 1 min : 2010-06-08 → 2015-12-31 (cache/databento_2010, prix bruts) puis 2016-01-01 → 2021-09-30
  (fab.core.load, prix ajustés ramenés en prix bruts par le facteur de roulement).
- Exploration seulement : 2010-06-08 → 2021-09-30. La réserve de la question « sortie » (2021-10-01 → 2026-08-28,
  wiki/reserves.md) n'est PAS lue : le script coupe toute date postérieure au 2021-09-30.
- Heures de New York. Séance 9:30-16:00. Jours ouvrés seulement.

RÈGLE D'ENTRÉE (identique à R4, PREREGISTRATION_3)
- Bougie 9:30-9:35 : O1 = open de la 1ʳᵉ barre dans [9:30, 9:35), C1 = dernière clôture disponible de 9:30 à 9:34.
- Doji si |C1 − O1| ≤ 1 tick (0,25 pt) : pas de trade.
- Sens = +1 si C1 > O1, −1 sinon. Entrée à l'open de la barre de 9:35 (pas de trade si elle manque).

SORTIES TESTÉES (25 variantes comptées)
- V0 : aucun stop, aucun objectif ; sortie à l'open de la 1ʳᵉ barre dans [16:00, 16:05).
- V(k, RR) : stop = k × ATR14 depuis le prix d'entrée, objectif = RR × stop ; sinon sortie à 16:00 comme V0.
  k ∈ {0,05 ; 0,10 ; 0,25 ; 0,50}, RR ∈ {1, 2, 3, 5, 10, aucun objectif}. 4 × 6 = 24 variantes.
- ATR14 = moyenne des amplitudes (plus haut − plus bas) des séances 9:30-16:00 des 14 séances précédentes
  (amplitude de séance et non « true range », pour ne pas être faussé par les roulements). Pas de trade sans ATR14.
- Stop et objectif surveillés sur les barres 1 min à partir de 9:35 incluse. Si les deux sont touchés dans la même
  barre, le stop passe en premier (prudent). Si l'open d'une barre est déjà au-delà du niveau, sortie à cet open.

RÉFÉRENCES (non comptées)
- R4 recalculé sur les mêmes jours (stop à l'extrême de la bougie, objectif 10R), pour comparaison.
- Référence triviale (PROTOCOLE.md, règle conditionnelle) : même position SANS la condition de sens, c'est-à-dire
  toujours à l'achat, mêmes jours, mêmes sorties que la variante.

COÛT ET MESURE
- 1 contrat fixe, résultat en points par trade. Coût standard aller-retour : 1 tick + 5 $ = 0,50 pt.
- Contrôle croisé : V0 et la règle choisie repassent dans le moteur vectorbt de fab.core (corrélation journalière).

CHOIX ET BARRIÈRE
- Règle choisie = meilleur Sharpe net par trade parmi les 25 variantes, sur toute l'exploration.
- n_famille = 26 (les 25 variantes + R4, déjà vu). Fiche et B1 : fab.protocole.fiche / barriere_exploration.
- Rapporté aussi : 2010-06 → 2015, 2016 → 2021-09, 2020 à part.
- Compteur global : 1 940 → 1 965 (25 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from fab.core import ASSETS, NY, backtest, load, trades_frame
from fab.protocole import barriere_exploration, fiche, imprimer

FIN_EXPLO = pd.Timestamp("2021-09-30")
D10 = Path("cache/databento_2010/NQ_v0_1m_2010.parquet")
OUT = Path("results/nq_orb_bougie")
TICK, COUT = 0.25, 0.25 + 5.0 / 20.0
OPEN, ENTREE, FERME = 570, 575, 960
KS = [0.05, 0.10, 0.25, 0.50]
RRS = [1, 2, 3, 5, 10, None]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def minutes_ny() -> pd.DataFrame:
    a = pd.read_parquet(D10)[["open", "high", "low", "close"]]
    a = a[a.index < pd.Timestamp("2016-01-01", tz="UTC")]
    b = load("NQ")
    b = b[b.index >= pd.Timestamp("2016-01-01", tz="UTC")]
    b = b[["open", "high", "low", "close"]].div(b["factor"], axis=0)  # prix bruts
    df = pd.concat([a, b]).sort_index()
    df = df[~df.index.duplicated()]
    loc = df.tz_convert(NY)
    m = loc.index.hour * 60 + loc.index.minute
    keep = (m >= OPEN) & (m < FERME + 5) & (loc.index.dayofweek < 5)
    loc = loc[keep]
    loc = loc.assign(d=loc.index.tz_localize(None).normalize(), m=m[keep])
    loc = loc[loc.d <= FIN_EXPLO]  # garde-fou : rien dans la réserve
    return loc


def matrices(loc: pd.DataFrame) -> dict[str, pd.DataFrame]:
    cols = range(OPEN, FERME + 5)
    return {c: loc.pivot(index="d", columns="m", values=c).reindex(columns=cols) for c in ["open", "high", "low", "close"]}


def first_open(O: pd.DataFrame, m0: int, slack: int = 5) -> pd.Series:
    sub = O[list(range(m0, m0 + slack))]
    return sub.bfill(axis=1).iloc[:, 0]


def simule(side, p_in, stop_d, tgt_d, H, L, O, p_end):
    """Une sortie par jour. stop_d / tgt_d : distances en points (np.inf = aucune). Retourne prix et type de sortie."""
    n = len(side)
    p_out = p_end.copy()
    kind = np.zeros(n, int)  # 0 = clôture, 1 = stop, 2 = objectif
    for i in range(n):
        s = side[i]
        st = p_in[i] - s * stop_d[i]
        tg = p_in[i] + s * tgt_d[i]
        hh, ll, oo = H[i], L[i], O[i]
        if s == 1:
            st_hit = np.nan_to_num(ll, nan=np.inf) <= st
            tg_hit = np.nan_to_num(hh, nan=-np.inf) >= tg
        else:
            st_hit = np.nan_to_num(hh, nan=-np.inf) >= st
            tg_hit = np.nan_to_num(ll, nan=np.inf) <= tg
        ks, kt = np.flatnonzero(st_hit), np.flatnonzero(tg_hit)
        js = ks[0] if ks.size else 10**9
        jt = kt[0] if kt.size else 10**9
        if js == 10**9 and jt == 10**9:
            continue
        if js <= jt:
            j, lvl, kind[i] = js, st, 1
            gap = np.isfinite(oo[j]) and ((oo[j] < st) if s == 1 else (oo[j] > st))
        else:
            j, lvl, kind[i] = jt, tg, 2
            gap = np.isfinite(oo[j]) and ((oo[j] > tg) if s == 1 else (oo[j] < tg))
        p_out[i] = oo[j] if gap else lvl
    return p_out, kind


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    M = matrices(minutes_ny())
    O, H, L, C = M["open"], M["high"], M["low"], M["close"]
    sess = list(range(OPEN, FERME))
    rng = H[sess].max(axis=1) - L[sess].min(axis=1)
    atr = rng.rolling(14, min_periods=14).mean().shift(1)
    o1 = first_open(O, OPEN)
    c1 = C[list(range(OPEN, ENTREE))].ffill(axis=1).iloc[:, -1]
    h1 = H[list(range(OPEN, ENTREE))].max(axis=1)
    l1 = L[list(range(OPEN, ENTREE))].min(axis=1)
    p_in = O[ENTREE]
    p_end = first_open(O, FERME)
    ok = o1.notna() & c1.notna() & p_in.notna() & p_end.notna() & atr.notna() & ((c1 - o1).abs() > TICK)
    d = pd.DataFrame({"o1": o1, "c1": c1, "h1": h1, "l1": l1, "p_in": p_in, "p_end": p_end, "atr": atr})[ok]
    d["side"] = np.where(d.c1 > d.o1, 1, -1)
    idx = d.index
    tc = list(range(ENTREE, FERME))
    Hm, Lm, Om = H.loc[idx, tc].values, L.loc[idx, tc].values, O.loc[idx, tc].values
    side, pin, pend, a14 = d.side.values, d.p_in.values, d.p_end.values, d.atr.values
    say(f"Jours de séance : {len(O)} ({O.index[0].date()} → {O.index[-1].date()}), trades possibles : {len(d)}, "
        f"dojis ou données manquantes : {len(O) - len(d)}")
    say(f"ATR14 moyen : {d.atr.mean():.1f} pts (2010 : {d.atr[idx.year == 2010].mean():.1f}, "
        f"2021 : {d.atr[idx.year == 2021].mean():.1f})")

    inf = np.full(len(d), np.inf)
    variantes = {"V0 sans stop ni objectif": (inf, inf)}
    for k in KS:
        for rr in RRS:
            sd = k * a14
            variantes[f"k={k:.2f} RR={'clôture' if rr is None else rr}"] = (sd, inf if rr is None else rr * sd)
    r4_stop = np.where(side == 1, pin - d.l1.values, d.h1.values - pin)
    r4_ok = r4_stop > 0

    rows, nets, kinds = [], {}, {}
    for name, (sd, td) in variantes.items():
        po, kd = simule(side, pin, sd, td, Hm, Lm, Om, pend)
        po_l, _ = simule(np.ones_like(side), pin, sd, td, Hm, Lm, Om, pend)
        brut = pd.Series(side * (po - pin), idx)
        net = brut - COUT
        ref = pd.Series(po_l - pin - COUT, idx)
        nets[name], kinds[name] = (net, brut, ref), kd
    # R4 de référence (mêmes jours, stop à l'extrême de la bougie, 10R)
    sd4 = np.where(r4_ok, r4_stop, np.inf)
    po4, kd4 = simule(side, pin, sd4, 10 * sd4, Hm, Lm, Om, pend)
    r4_net = pd.Series(side * (po4 - pin) - COUT, idx)[r4_ok]

    comptees = [n for n in variantes]
    sharpes = [nets[n][0].mean() / nets[n][0].std() for n in comptees]
    for name in comptees + ["R4 (référence, non comptée)"]:
        if name.startswith("R4"):
            net, kd = r4_net, kd4[r4_ok]
            ref = None
        else:
            net, _, ref = nets[name]
            kd = kinds[name]
        f = fiche(net, None, ref, n_famille=26, sharpes_famille=sharpes, tick_bp=TICK)
        row = {"variante": name, "n": f["n"], "net_moy_pts": f["net_moy"], "t_nw": f["t_nw"], "sharpe_an": f["sharpe_an"],
               "gagnants_%": f["gagnants_%"], "stop_%": 100 * (kd == 1).mean(), "objectif_%": 100 * (kd == 2).mean(),
               "pire_creux_pts": f["pire_creux"], "annees_pos": f["annees_pos"],
               "ref_long_moy": f.get("ref_net_moy", np.nan), "t_ecart_ref": f.get("t_ecart_ref", np.nan)}
        y = net.index.year
        for p, msk in {"2010-06→2015": y <= 2015, "2016→2021-09": y >= 2016, "2020": y == 2020}.items():
            row[f"{p} moy"] = net[np.asarray(msk)].mean()
        rows.append(row)
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "grille.csv", index=False)
    pd.set_option("display.width", 250)
    say("\n===== Grille (points nets par trade, 1 contrat, coût 0,50 pt) =====")
    say(tab.round(3).to_string(index=False))

    best = tab[tab.variante.isin(comptees)].sort_values("sharpe_an", ascending=False).iloc[0].variante
    net, brut, ref = nets[best]
    f = fiche(net, brut, ref, n_famille=26, sharpes_famille=sharpes, tick_bp=TICK)
    say("\n" + imprimer(f, f"Règle choisie (meilleur Sharpe net) : {best}"))
    okb, raisons = barriere_exploration(f)
    say("B1 : " + ("✅ franchie" if okb else "❌ ratée"))
    for r in raisons:
        say("  " + r)
    v0 = nets["V0 sans stop ni objectif"][0]
    j = net.index.intersection(r4_net.index)
    say(f"\nÉcart règle choisie − R4 sur les mêmes jours : {(net[j] - r4_net[j]).mean():+.2f} pts/trade (n {len(j)})")
    say(f"Écart V0 − R4 sur les mêmes jours : {(v0[j] - r4_net[j]).mean():+.2f} pts/trade")
    say("\nNet par année (pts/trade) :")
    yr = pd.DataFrame({"V0": v0.groupby(v0.index.year).mean(), best: net.groupby(net.index.year).mean(),
                       "R4": r4_net.groupby(r4_net.index.year).mean(),
                       "n": v0.groupby(v0.index.year).size()})
    say(yr.round(2).to_string())
    pd.DataFrame({"net_pts": net, "brut_pts": brut, "ref_long_net": ref, "side": side}).to_csv(OUT / "trades_choisie.csv")
    pd.DataFrame({"net_pts": v0, "side": side}).to_csv(OUT / "trades_V0.csv")

    # contrôle croisé vectorbt (V0 et règle choisie)
    for name in ["V0 sans stop ni objectif", best]:
        sd, td = variantes[name]
        po, kd = simule(side, pin, sd, td, Hm, Lm, Om, pend)
        mo = np.where(kd == 0, FERME, ENTREE + 1)
        t = trades_frame(pd.DataFrame({"date": idx, "m_in": ENTREE, "p_in": pin, "m_out": mo, "p_out": po,
                                       "dir": side, "f_in": 1.0}))
        res = backtest(name, ASSETS["NQ"], t, NY, idx)
        pts = pd.Series(side * (po - pin) / pin, idx)
        c = np.corrcoef(res.daily_gross.values, pts.values)[0, 1]
        say(f"Contrôle vectorbt [{name}] : corrélation rendement brut journalier / points÷prix = {c:.4f}")
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
