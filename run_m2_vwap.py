"""Bande de bruit M2 : effet d'exiger le VWAP à l'entrée, comme le code publié par Zarattini, Aziz et Barbon.

Fiche : wiki/experiments/m2-bande-bruit-nq.md (section « Vérification de fidélité : VWAP à l'entrée »). Grille figée ici
et commitée AVANT tout calcul. VÉRIFICATION DE FIDÉLITÉ, pas réouverture : la bande de bruit NQ est au registre des
échecs (réouverture seulement sur des données postérieures au 2026-08-28) ; aucun verdict B1, aucune réserve lue.
Rien n'est modifié dans fab/strategies.py ni sur la branche du bot (le bot n'utilise pas la bande de bruit).

DONNÉES ET CONVENTIONS : celles de M2 (PREREGISTRATION.md, fab.core) : Databento 1 min, 2016-01 → 2026-08-28, IS
2016-2022 / OOS 2023 → 2026-08, coût 1 tick + 5 $ aller-retour, exécution à l'open de la minute du contrôle.

RÈGLE M2 (copie de fab.strategies.m2_noise) avec un seul changement possible, l'entrée :
- « actuelle » : long si clôture > bande haute ; court si clôture < bande basse (ce que fait m2_noise aujourd'hui) ;
- « VWAP » : long si clôture > bande haute ET > VWAP ; court si clôture < bande basse ET < VWAP (code des auteurs,
  Delgado 2026, Chuk 2026, Paz 2026).
Bande, σ sur 14 jours, VWAP au prix typique, contrôles 10:00 → 15:30, stop suiveur max(bande, VWAP), sortie à 16:00 :
inchangés.

GRILLE : NQ, ES, YM × {1×, volatilité cible min(4, 2 % / σ14) = R3}. L'entrée « actuelle » est recalculée comme
référence (déjà vue, non comptée) ; l'entrée « VWAP » compte : 6 essais.
MESURES : Sharpe net et brut IS / OOS (fab.core.summarize), trades, points par trade ; écart journalier VWAP −
actuelle (t de Newey-West) ; Sharpe par année.

Compteur global : 2 085 → 2 091 (6 essais).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from fab.core import ASSETS, Asset, Grid, backtest, summarize, trades_frame
from fab.protocole import nw_t
from fab.replications import scaled, sgrid, vol_target_lev
from fab.strategies import _prev_close

OUT = Path("results/m2_vwap")
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def m2(a: Asset, g: Grid, vwap_entry: bool) -> pd.DataFrame:
    o, c = a.open_min, a.close_min
    day_open = g.price_at(o)[0]
    prev = _prev_close(g, a)
    cols = list(range(o, c))
    C = g.C[cols].ffill(axis=1)
    move = C.div(day_open, axis=0).sub(1).abs()
    sigma = move.shift(1).rolling(14, min_periods=10).mean()
    tp = (g.H[cols] + g.L[cols] + g.C[cols]) / 3
    V = g.V[cols].fillna(0)
    vwap = (tp.fillna(0) * V).cumsum(axis=1) / V.cumsum(axis=1).replace(0, np.nan)
    up_base = np.maximum(day_open, prev)
    lo_base = np.minimum(day_open, prev)
    checks = list(range(o + 30, c, 30))
    exec_px = {m: g.price_at(m) for m in checks + [c]}
    rows = []
    for d in g.dates:
        if not (np.isfinite(up_base[d]) and np.isfinite(lo_base[d])):
            continue
        pos, entry = 0, None
        for m in checks:
            x, s, v = C.at[d, m - 1], sigma.at[d, m - 1], vwap.at[d, m - 1]
            if not (np.isfinite(x) and np.isfinite(s)):
                continue
            ub, lb = up_base[d] * (1 + s), lo_base[d] * (1 - s)
            v = v if np.isfinite(v) else x
            new = pos
            if pos == 1 and x < max(ub, v):
                new = 0
            elif pos == -1 and x > min(lb, v):
                new = 0
            if new == 0:
                if vwap_entry:
                    new = 1 if (x > ub and x > v) else (-1 if (x < lb and x < v) else 0)
                else:
                    new = 1 if x > ub else (-1 if x < lb else 0)
                if pos != 0 and new == pos:
                    new = 0
            if new != pos:
                px, mm = exec_px[m][0][d], exec_px[m][1][d]
                if not np.isfinite(px):
                    continue
                if pos != 0:
                    rows.append({**entry, "m_out": mm, "p_out": px})
                entry = {"date": d, "m_in": mm, "p_in": px, "dir": new, "f_in": 1.0} if new else None
                pos = new
        if pos != 0:
            px, mm = exec_px[c][0][d], exec_px[c][1][d]
            rows.append({**entry, "m_out": mm, "p_out": px})
    return trades_frame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    rows, yearly = [], {}
    for n in ["NQ", "ES", "YM"]:
        a = ASSETS[n]
        g = sgrid(a)
        lev = vol_target_lev(a, g)
        res = {}
        for entree in ("actuelle", "VWAP"):
            t = m2(a, g, entree == "VWAP")
            r1 = backtest(f"M2 {entree}", a, t, a.tz, g.dates)
            res[(entree, "1x")] = r1
            res[(entree, "R3")] = scaled(r1, lev)
        for (entree, taille), r in res.items():
            s = summarize(r)
            full = r.daily_net
            rows.append({"actif": n, "entree": entree, "taille": taille, "trades": s["n_trades"],
                         "sharpe_net_IS": s["sharpe_net_IS"], "sharpe_net_OOS": s["sharpe_net_OOS"],
                         "sharpe_brut_IS": s["sharpe_gross_IS"], "sharpe_brut_OOS": s["sharpe_gross_OOS"],
                         "sharpe_net_total": full.mean() / full.std() * np.sqrt(252),
                         "pts_brut_trade": s["avg_ticks_gross"] * a.tick, "pts_net_trade": s["avg_ticks_net"] * a.tick,
                         "gagnants_%": s["hit_rate_net_%"], "compte": entree == "VWAP"})
            yearly[(n, entree, taille)] = full.groupby(full.index.year).apply(lambda x: x.mean() / x.std() * np.sqrt(252))
        for taille in ("1x", "R3"):
            diff = res[("VWAP", taille)].daily_net - res[("actuelle", taille)].daily_net
            say(f"{n} {taille} : écart journalier VWAP − actuelle {diff.mean() * 1e4:+.2f} bp, t NW {nw_t(diff.values):.2f}")
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "comparaison.csv", index=False)
    say("\n===== M2 : entrée actuelle contre entrée avec VWAP (IS 2016-2022, OOS 2023 → 2026-08) =====")
    say(tab.round(3).to_string(index=False))
    say("\nSharpe net par année :")
    yr = pd.DataFrame({f"{k[0]} {k[1]} {k[2]}": v for k, v in yearly.items()})
    say(yr.round(2).to_string())
    yr.to_csv(OUT / "sharpe_par_annee.csv")
    (OUT / "summary.txt").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
