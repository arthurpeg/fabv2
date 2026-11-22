"""BB (bande de bruit, ancien « M2 ») sur NQ avec un stop loss et un take profit fixes. Exploration.

Fiche : wiki/experiments/m2-bande-bruit-nq.md (section « BB avec SL et TP »). Grille figée ici et commitée AVANT tout
calcul. BB est au registre des échecs (réouverture seulement sur des données postérieures au 2026-08-28) et toutes les
données NQ jusqu'au 2026-08-28 sont explorées : ce test est une EXPLORATION, sans réserve ni verdict de confirmation.
Demande de l'utilisateur (2026-11-22). Rien n'est modifié dans fab/ ni sur la branche du bot.

DONNÉES : NQ Databento 1 min (fab.replications.sgrid, prix ajustés), 2016-01 → 2026-08-28.

BB DE RÉFÉRENCE (run_m2_vwap.py, VWAP exigé à l'entrée) : σ = moyenne sur 14 séances de |cours à HH:MM / ouverture − 1| ;
bande haute = max(ouverture, clôture de la veille) × (1 + σ), basse = min(…) × (1 − σ) ; VWAP au prix typique depuis
9:30 ; contrôles 10:00, 10:30 … 15:30 sur la clôture de la minute précédente, exécution à l'open de la minute du
contrôle : achat si clôture > bande haute et > VWAP, vente si < bande basse et < VWAP ; stop suiveur au contrôle :
sortie d'un achat si clôture < max(bande haute, VWAP) (symétrique) ; pas de ré-entrée dans le sens qu'on vient de
quitter au même contrôle ; sortie à 16:00. 1 contrat, coût 1 tick + 5 $ (0,50 pt) par trade.

AJOUT : SL et TP fixés à l'entrée. SL = k × ATR14 (moyenne des amplitudes 9:30-16:00 des 14 séances précédentes),
TP = RR × SL. Surveillés à chaque minute après l'entrée (minute d'entrée incluse) ; si les deux sont touchés dans la
même minute, le SL passe en premier ; si une minute ouvre au-delà, sortie à cet open. Après une sortie SL/TP, BB peut
reprendre une position aux contrôles suivants selon sa règle d'entrée.
- Mode A : stop suiveur de BB conservé + SL + TP.
- Mode B : stop suiveur supprimé ; une fois en position, sorties uniquement SL, TP ou 16:00 (pas de retournement).

GRILLE (18 essais) : mode {A, B} × k {0,25 ; 0,5 ; 1,0} × RR {1, 2, 3}.
RÉFÉRENCE (non comptée) : BB sans SL ni TP. Écart journalier en points nets (t de Newey-West).
MESURES : P&L journalier en points et en dollars (20 $/pt), Sharpe journalier, net par trade, gagnants, sorties par
type, pire creux, 2016-2022 / 2023-2026 ; meilleure case (Sharpe journalier) avec fiche et DSR (N = 120 : les 96 essais
BB comptés au n° 2, les 6 du VWAP, ces 18), à titre indicatif seulement.

Compteur global : 2 091 → 2 109 (18 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from fab.core import ASSETS
from fab.protocole import fiche, imprimer, nw_t
from fab.replications import sgrid
from fab.strategies import _prev_close

OUT = Path("results/bb_sltp")
KS, RRS = [0.25, 0.5, 1.0], [1, 2, 3]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def prepare():
    a = ASSETS["NQ"]
    g = sgrid(a)
    o, c = a.open_min, a.close_min
    cols = list(range(o, c))
    day_open = g.price_at(o)[0]
    prev = _prev_close(g, a)
    C = g.C[cols].ffill(axis=1)
    sigma = C.div(day_open, axis=0).sub(1).abs().shift(1).rolling(14, min_periods=10).mean()
    tp = (g.H[cols] + g.L[cols] + g.C[cols]) / 3
    V = g.V[cols].fillna(0)
    vwap = (tp.fillna(0) * V).cumsum(axis=1) / V.cumsum(axis=1).replace(0, np.nan)
    amp = g.H[cols].max(axis=1) - g.L[cols].min(axis=1)
    atr = amp.rolling(14, min_periods=14).mean().shift(1)
    return a, g, cols, day_open, prev, C, sigma, vwap, atr


def simulate(P, mode: str | None, k: float | None, rr: float | None) -> pd.DataFrame:
    a, g, cols, day_open, prev, C, sigma, vwap, atr = P
    o, c = a.open_min, a.close_min
    checks = list(range(o + 30, c, 30))
    up_base, lo_base = np.maximum(day_open, prev), np.minimum(day_open, prev)
    Om, Hm, Lm = g.O, g.H, g.L
    rows = []
    for d in g.dates:
        if not (np.isfinite(up_base[d]) and np.isfinite(lo_base[d])):
            continue
        if k is not None and not np.isfinite(atr[d]):
            continue
        O_, H_, L_ = Om.loc[d], Hm.loc[d], Lm.loc[d]
        pos, pe, st, tg, m_in = 0, np.nan, np.nan, np.nan, None
        block = 0
        def close_pos(px, m, kind):
            rows.append({"date": d, "m_in": m_in, "m_out": m, "dir": pos, "p_in": pe, "p_out": px, "sortie": kind})
        bounds = checks + [c]
        for idx, m in enumerate(checks):
            # 1) exécution au contrôle m (open de la minute m) à partir des clôtures de m − 1
            block = 0  # pas de ré-entrée dans le sens qu'on vient de quitter AU MÊME contrôle (règle de m2_noise)
            x, s, v = C.at[d, m - 1], sigma.at[d, m - 1], vwap.at[d, m - 1]
            px = O_.get(m, np.nan)
            if np.isfinite(x) and np.isfinite(s) and np.isfinite(px):
                ub, lb = up_base[d] * (1 + s), lo_base[d] * (1 - s)
                v = v if np.isfinite(v) else x
                if pos != 0 and mode != "B":
                    if (pos == 1 and x < max(ub, v)) or (pos == -1 and x > min(lb, v)):
                        close_pos(px, m, "suiveur")
                        block, pos = pos, 0
                if pos == 0:
                    sig = 1 if (x > ub and x > v) else (-1 if (x < lb and x < v) else 0)
                    if sig != 0 and sig != block:
                        pos, pe, m_in = sig, px, m
                        if k is not None:
                            sd = k * atr[d]
                            st, tg = pe - pos * sd, pe + pos * rr * sd
            # 2) surveillance minute par minute jusqu'au prochain contrôle (exclu)
            if pos != 0 and k is not None:
                for mm in range(m, bounds[idx + 1]):
                    h, l, op = H_.get(mm, np.nan), L_.get(mm, np.nan), O_.get(mm, np.nan)
                    if not np.isfinite(h):
                        continue
                    hit_s = (l <= st) if pos == 1 else (h >= st)
                    hit_t = (h >= tg) if pos == 1 else (l <= tg)
                    if hit_s:
                        gap = mm > m_in and np.isfinite(op) and ((op < st) if pos == 1 else (op > st))
                        close_pos(op if gap else st, mm + 1, "SL")
                        pos = 0
                        break
                    if hit_t:
                        gap = mm > m_in and np.isfinite(op) and ((op > tg) if pos == 1 else (op < tg))
                        close_pos(op if gap else tg, mm + 1, "TP")
                        pos = 0
                        break
        if pos != 0:
            pxc = next((O_.get(mm) for mm in range(c, c + 5) if np.isfinite(O_.get(mm, np.nan))), np.nan)
            if np.isfinite(pxc):
                close_pos(pxc, c, "16:00")
    t = pd.DataFrame(rows)
    t["net_pts"] = t.dir * (t.p_out - t.p_in) - a.rt_cost
    return t


def daily(t, dates):
    return t.groupby("date").net_pts.sum().reindex(dates).fillna(0.0)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    P = prepare()
    dates = P[1].dates
    ref = simulate(P, None, None, None)
    ref_d = daily(ref, dates)
    say(f"BB de référence : {len(ref)} trades, {ref.net_pts.mean():+.2f} pts/trade, {ref_d.sum() * 20 / (len(dates) / 252):,.0f} $/an, "
        f"Sharpe journalier {ref_d.mean() / ref_d.std() * np.sqrt(252):.2f}")
    res = {(m, k, rr): simulate(P, m, k, rr) for m in ("A", "B") for k in KS for rr in RRS}
    sh = [daily(t, dates).mean() / daily(t, dates).std() for t in res.values()]
    rows, fiches = [], {}
    for key, t in res.items():
        dd = daily(t, dates)
        eq = dd.cumsum()
        y = dd.index.year
        diff = dd - ref_d
        f = fiche(dd, None, ref_d, n_famille=120, sharpes_famille=sh, tick_bp=None)
        fiches[key] = f
        rows.append({"mode": key[0], "k_ATR": key[1], "RR": key[2], "trades": len(t), "net_pts_trade": t.net_pts.mean(),
                     "gagnants_%": 100 * (t.net_pts > 0).mean(), "SL_%": 100 * (t.sortie == "SL").mean(),
                     "TP_%": 100 * (t.sortie == "TP").mean(), "suiveur_%": 100 * (t.sortie == "suiveur").mean(),
                     "$_an": dd.sum() * 20 / (len(dates) / 252), "sharpe_jour": dd.mean() / dd.std() * np.sqrt(252),
                     "pire_creux_$": (eq - eq.cummax()).min() * 20, "2016-22_sharpe": dd[y <= 2022].mean() / dd[y <= 2022].std() * np.sqrt(252),
                     "2023-26_sharpe": dd[y >= 2023].mean() / dd[y >= 2023].std() * np.sqrt(252),
                     "ecart_vs_BB_pts_jour": diff.mean(), "t_ecart": nw_t(diff.values), "dsr_120": f["dsr_famille"]})
    tab = pd.DataFrame(rows)
    eq = ref_d.cumsum()
    yy = ref_d.index.year
    ref_row = {"mode": "BB", "k_ATR": np.nan, "RR": np.nan, "trades": len(ref), "net_pts_trade": ref.net_pts.mean(),
               "gagnants_%": 100 * (ref.net_pts > 0).mean(), "SL_%": 0, "TP_%": 0, "suiveur_%": 100 * (ref.sortie == "suiveur").mean(),
               "$_an": ref_d.sum() * 20 / (len(dates) / 252), "sharpe_jour": ref_d.mean() / ref_d.std() * np.sqrt(252),
               "pire_creux_$": (eq - eq.cummax()).min() * 20,
               "2016-22_sharpe": ref_d[yy <= 2022].mean() / ref_d[yy <= 2022].std() * np.sqrt(252),
               "2023-26_sharpe": ref_d[yy >= 2023].mean() / ref_d[yy >= 2023].std() * np.sqrt(252)}
    tab = pd.concat([pd.DataFrame([ref_row]), tab], ignore_index=True)
    tab.to_csv(OUT / "grille.csv", index=False)
    say("\n===== BB NQ avec SL / TP (1 contrat, points nets, 20 $/pt) =====")
    say(tab.round(2).to_string(index=False))
    best = tab.iloc[1:].sort_values("sharpe_jour", ascending=False).iloc[0]
    key = (best["mode"], best.k_ATR, int(best.RR))
    say("\n" + imprimer(fiches[key], f"Meilleure case (Sharpe journalier) : mode {key[0]}, SL {key[1]} ATR, TP {key[2]}R (indicatif)"))
    t = res[key]
    say("\nMeilleure case, P&L $ par année : " + " · ".join(f"{a} {v:+,.0f}" for a, v in (daily(t, dates).groupby(dates.year).sum() * 20).items()))
    say("BB de référence, P&L $ par année : " + " · ".join(f"{a} {v:+,.0f}" for a, v in (ref_d.groupby(dates.year).sum() * 20).items()))
    ref.to_csv(OUT / "trades_BB.csv", index=False)
    t.to_csv(OUT / f"trades_meilleure.csv", index=False)
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
