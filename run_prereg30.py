"""Pré-enregistrement n° 30 : NQ, règle de la 1ʳᵉ bougie, stop 0,5 × ATR14, objectif 2R, sur la réserve 2021-10-01 →
2026-08-28. Une seule exécution. Règle, référence et critères : PREREGISTRATION_30.md.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from fab.core import NY, load
from fab.protocole import fiche, imprimer, verdict_confirmation
from run_nq_orb_bougie import first_open, simule

DEBUT, FIN = pd.Timestamp("2021-10-01"), pd.Timestamp("2026-08-28")
AMORCE = pd.Timestamp("2021-08-01")  # séances explorées, seulement pour l'ATR14
OUT = Path("results/prereg30")
OPEN, ENTREE, FERME = 570, 575, 960
TICK, COUT, K, RR = 0.25, 0.50, 0.50, 2.0
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    b = load("NQ")
    b = b[(b.index >= pd.Timestamp(AMORCE, tz="UTC")) & (b.index < pd.Timestamp(FIN + pd.Timedelta(days=2), tz="UTC"))]
    df = b[["open", "high", "low", "close"]].div(b["factor"], axis=0)
    loc = df.tz_convert(NY)
    m = loc.index.hour * 60 + loc.index.minute
    keep = (m >= OPEN) & (m < FERME + 5) & (loc.index.dayofweek < 5)
    loc = loc[keep]
    loc = loc.assign(d=loc.index.tz_localize(None).normalize(), m=m[keep])
    loc = loc[loc.d <= FIN]
    cols = range(OPEN, FERME + 5)
    O, H, L, C = (loc.pivot(index="d", columns="m", values=c).reindex(columns=cols) for c in ["open", "high", "low", "close"])
    sess, rc = list(range(OPEN, FERME)), list(range(OPEN, ENTREE))
    atr = (H[sess].max(axis=1) - L[sess].min(axis=1)).rolling(14, min_periods=14).mean().shift(1)
    o1, c1 = first_open(O, OPEN), C[rc].ffill(axis=1).iloc[:, -1]
    h1, l1 = H[rc].max(axis=1), L[rc].min(axis=1)
    p_in, p_end = O[ENTREE], first_open(O, FERME)
    ok = (o1.notna() & c1.notna() & p_in.notna() & p_end.notna() & atr.notna() & ((c1 - o1).abs() > TICK)
          & (O.index >= DEBUT) & (O.index <= FIN))
    d = pd.DataFrame({"o1": o1, "c1": c1, "h1": h1, "l1": l1, "p_in": p_in, "p_end": p_end, "atr": atr})[ok]
    d["side"] = np.where(d.c1 > d.o1, 1, -1)
    idx = d.index
    tc = list(range(ENTREE, FERME))
    Hm, Lm, Om = H.loc[idx, tc].values, L.loc[idx, tc].values, O.loc[idx, tc].values
    side, pin, pend = d.side.values, d.p_in.values, d.p_end.values
    say(f"Réserve : {idx[0].date()} → {idx[-1].date()}, {len(d)} trades (séances : {int(((O.index >= DEBUT) & (O.index <= FIN)).sum())}), "
        f"ATR14 moyen {d.atr.mean():.1f} pts")

    sd = K * d.atr.values
    po, kd = simule(side, pin, sd, RR * sd, Hm, Lm, Om, pend)
    net = pd.Series(side * (po - pin) - COUT, idx)
    r4_stop = np.where(side == 1, pin - d.l1.values, d.h1.values - pin)
    sd4 = np.where(r4_stop > 0, r4_stop, np.inf)
    po4, _ = simule(side, pin, sd4, 10 * sd4, Hm, Lm, Om, pend)
    r4 = pd.Series(side * (po4 - pin) - COUT, idx)[r4_stop > 0]
    pl, _ = simule(np.ones_like(side), pin, sd, RR * sd, Hm, Lm, Om, pend)
    long_ = pd.Series(pl - pin - COUT, idx)

    f = fiche(net, net + COUT, r4, n_famille=1, tick_bp=TICK)
    say(imprimer(f, "Règle n° 30 sur la réserve (référence C2 = R4, 1 contrat, mêmes jours)"))
    ok_, raisons = verdict_confirmation(f)
    for r in raisons:
        say("  " + r)
    say(f"\nVERDICT : {'C1-C4 remplis → confirmée hors protocole (B1 non franchie) ; étape 4 obligatoire' if ok_ else 'REJET'}")
    say(f"\nSorties : stop {100 * (kd == 1).mean():.1f} %, objectif {100 * (kd == 2).mean():.1f} %, 16:00 {100 * (kd == 0).mean():.1f} %"
        f" | achats {net[side == 1].mean():+.2f} (n {(side == 1).sum()}) | ventes {net[side == -1].mean():+.2f} (n {(side == -1).sum()})")
    say(f"Référence non critère « toujours long », mêmes sorties : {long_.mean():+.2f} pts/trade")
    say(f"Net en $ par trade : {net.mean() * 20:+.1f} ; total {net.sum() * 20:,.0f} $ ; pire creux "
        f"{((net.cumsum() - net.cumsum().cummax()).min()) * 20:,.0f} $")
    y = net.index.year
    say("\nPar année (pts/trade) :")
    say(pd.DataFrame({"regle": net.groupby(y).mean(), "R4": r4.groupby(r4.index.year).mean(),
                      "toujours_long": long_.groupby(y).mean(), "n": net.groupby(y).size()}).round(2).to_string())
    pd.DataFrame({"net": net, "side": side, "sortie": kd, "r4": r4.reindex(idx), "long": long_}).to_csv(OUT / "trades.csv")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
