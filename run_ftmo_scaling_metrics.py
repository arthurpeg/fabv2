"""Métriques complètes de la montée en taille FTMO (run_ftmo_scaling.py : paliers 1-3 x 10k puis 1-2 x 100k par
stratégie, A = mom, B = 3n + M2, règle des annonces + cible + attente) — demande du 2026-11-04. EXPLORATOIRE, hors compteur.

uv run python run_ftmo_scaling_metrics.py [N] → results/ftmo_scaling/metriques_<simulation>.csv, metriques.log

Mêmes règles, mêmes chemins (vrai chemin, départs glissants tous les 20 séances sur 5 ans, Monte-Carlo par blocs sur
5 ans, scénarios historique et espérance divisée par 2) ; la gestion est instrumentée pour compter, par taille de compte,
les évals achetées, ratées, les comptes financés perdus, les rewards (nombre et montant) et les frais, et pour mesurer la
trajectoire de la cagnotte (plus bas, max DD, revenus mensuels une fois les 400k atteints, plus longue attente d'un reward).
Mois = 21 séances.
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as M
import run_ftmo_monte_carlo as MC
import run_ftmo_scaling as S

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000
LOG: list[str] = []
TAILLES = (10_000, 100_000)


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


class Gestion(S.Gestion):
    def __init__(self, calendaire: bool):
        self.st = {f"{k}_{t // 1000}k": 0.0 for k in ("evals", "frais", "evals_ratees", "finances_perdus", "rewards_n",
                                                    "rewards_usd") for t in TAILLES}
        self.rew_t, self.t = [], 0
        super().__init__(calendaire)

    def _ajoute(self, strat, taille, d):
        self.st[f"evals_{taille // 1000}k"] += 1
        self.st[f"frais_{taille // 1000}k"] += S.PRIX[taille]
        super()._ajoute(strat, taille, d)

    def jour(self, t: int, d, row):
        self.t = t
        for s in self.slots:
            c = s["compte"]
            if c is None or c.mort:
                continue
            avant, r0 = c.cash, c.rewards
            c.jour(d, M.jambes_A(row) if s["strat"] == "A" else M.jambes_B(row))
            self.cagnotte += c.cash - avant
            k = f"{s['taille'] // 1000}k"
            if c.rewards > r0:
                self.st[f"rewards_n_{k}"] += c.rewards - r0
                self.st[f"rewards_usd_{k}"] += c.cash - avant
                self.rew_t.append(t)
            if c.mort:
                self.st[("evals_ratees_" if "éval perdu" in c.events[-1][1] else "finances_perdus_") + k] += 1
        for s in self.slots:  # rachats (comme S.Gestion.jour)
            c = s["compte"]
            if c is not None and c.mort:
                self.events.append((d, f"{c.nom} perdu"))
                s["compte"] = None
            if s["compte"] is None and s["rachat"]:
                if self.cagnotte >= S.PRIX[s["taille"]]:
                    self.cagnotte -= S.PRIX[s["taille"]]
                    k = f"{s['taille'] // 1000}k"
                    self.st[f"evals_{k}"] += 1
                    self.st[f"frais_{k}"] += S.PRIX[s["taille"]]
                    s["compte"] = M.Compte(f"{s['strat']} {k}", self.cal, True, "cible+attente", s["taille"],
                                           S.PRIX[s["taille"]], False)
                else:
                    self.idle += 1
        self.slots = [s for s in self.slots if s["compte"] is not None or s["rachat"]]
        if self.palier < 4 and self.cagnotte >= S.reserve(self.palier + 1):
            self._monte(t, d)


def joue(jours, idx, calendaire=False):
    g = Gestion(calendaire)
    traj = np.empty(len(idx))
    for t, i in enumerate(idx):
        d, row = jours[i]
        g.jour(t, d, row)
        traj[t] = g.cagnotte
    return g, traj


def metriques(g: Gestion, traj: np.ndarray) -> dict:
    H = len(traj)
    r = {f"palier_{k}_mois": (g.dates[k] / 21 if k in g.dates else np.nan) for k in range(2, 6)}
    for m in (6, 12, 24, 36, 60):
        r[f"cagnotte_{m}m"] = traj[min(21 * m, H) - 1]
    x = np.r_[S.DEPOT, traj]
    pic = np.maximum.accumulate(x)
    r |= dict(excedent_fin=g.excedent(), min_cagnotte=traj.min(), mois_min=int(traj.argmin()) // 21,
              max_dd=float((x - pic).min()), idle=g.idle, **g.st)
    r["frais_total"] = r["frais_10k"] + r["frais_100k"]
    r["rewards_total_usd"] = r["rewards_usd_10k"] + r["rewards_usd_100k"]
    rt = np.array(sorted(set(g.rew_t)))
    gaps = np.diff(np.r_[0, rt, H - 1]) if len(rt) else np.array([H])
    r["attente_max_mois"] = gaps.max() / 21
    t5 = g.dates.get(5)
    if t5 is not None and H - t5 >= 42:
        seg = traj[t5:]
        flux = np.diff(seg[::21])
        x5 = np.r_[seg[0], seg]
        r |= dict(revenu_mensuel_moy=flux.mean(), revenu_mensuel_med=np.median(flux), mois_negatifs_pct=100 * (flux < 0).mean(),
                  pire_mois=flux.min(), max_dd_apres_400k=float((x5 - np.maximum.accumulate(x5)).min()))
        g5 = rt[rt >= t5]
        r["attente_max_apres_400k_mois"] = (np.diff(np.r_[t5, g5, H - 1]).max() / 21) if len(g5) else (H - t5) / 21
    return r


def resume(nom: str, rows: list[dict]):
    D = pd.DataFrame(rows)
    D.to_csv(S.OUT / f"metriques_{nom}.csv", index=False)
    say(f"\n===== {nom} : {len(D)} chemins =====")
    show = [c for c in D.columns if c not in ("départ",)]
    q = D[show].describe(percentiles=[.05, .1, .5, .9]).T[["mean", "5%", "10%", "50%", "90%", "min", "max"]]
    q.insert(0, "atteint %", 100 * D[show].notna().mean())
    say(q.round(1).to_string())
    return D


def main() -> None:
    lib = M.bibliotheque()
    jours = M.tableau(lib)
    dates = pd.DatetimeIndex([d for d, _ in jours])
    # vrai chemin
    g, traj = joue(jours, np.arange(len(jours)), calendaire=True)
    r = metriques(g, traj)
    say(f"===== Vrai chemin {dates[0]:%Y-%m-%d} → {dates[-1]:%Y-%m-%d} =====")
    say(pd.Series(r).round(1).to_string())
    cag = pd.Series(traj, index=dates)
    fl = cag.resample("ME").last().diff().dropna()
    fl5 = fl[fl.index >= dates[g.dates[5]]]
    say(f"Revenu mensuel une fois les 400k atteints ({dates[g.dates[5]]:%Y-%m}) : moyenne {fl5.mean():,.0f} $, médiane "
        f"{fl5.median():,.0f} $, mois négatifs {100 * (fl5 < 0).mean():.0f} %, pire mois {fl5.min():,.0f} $ "
        f"({fl5.idxmin():%Y-%m}), meilleur {fl5.max():,.0f} $")
    an = cag.resample("YE").last().diff()
    an.iloc[0] = cag.resample("YE").last().iloc[0] - S.DEPOT
    say("Gain par année civile ($) : " + ", ".join(f"{y.year} {v:,.0f}" for y, v in an.items()))
    pd.DataFrame([r]).to_csv(S.OUT / "metriques_vrai_chemin.csv", index=False)

    rows = []
    fin = int(np.searchsorted(dates, pd.Timestamp("2026-08-29")))
    for i0 in range(0, fin - S.H5, 20):
        g, traj = joue(jours, np.arange(i0, i0 + S.H5))
        rows.append(dict(départ=dates[i0].date(), **metriques(g, traj)))
    resume("glissants", rows)
    for nom, src in (("mc_historique", jours), ("mc_edge_2", M.tableau(MC.decale(lib, 0.5)))):
        rng = np.random.default_rng(MC.SEED)
        MC.H = S.H5
        rows = [metriques(*joue(src, MC.indices(len(src), rng))) for _ in range(N)]
        resume(nom, rows)
    (S.OUT / "metriques.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
