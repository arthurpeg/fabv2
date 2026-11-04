"""FTMO 1-Step avec les trois stratégies : 3n, mom et M2, selon un plan journalier (demande du 2026-11-04).

EXPLORATOIRE, hors compteur : évaluation d'un contrat sur des trades existants (objectif à 2 R partout).

uv run python run_propfirm_trio.py [N] → results/propfirm_trio/ (run.log, jours.csv, ftmo.csv)

Plan pour chaque journée FTMO J (minuit CE(S)T = 18:00 ou 19:00 ET : la nuit 20:00 ET de J-1, la matinée et la
séance US de J sont dans la même journée FTMO) :
  - signal 3n pour la nuit qui se termine le matin de J -> 3n seul, à plein risque r (pas de mom, pas de M2) ;
  - sinon -> mom à r / 2 (20:00 -> 9:30, SL 2 ATR / TP 4 ATR M15), puis M2 à r / 2 l'après-midi s'il y a un setup
    (9:35 -> 15:55, SL 4 ATR / TP 8 ATR M15). Deux pertes pleines font r = 2,5 % < 3 % (perte du jour FTMO).
r = 2,5 % en éval, 1 % en financé (même plan aux deux phases).
Trades : 3n et M2 avec objectif à 2 R = results/propfirm_combo/trades_tp2.csv (run_propfirm_combo.py) ; mom avec
TP 4 ATR = 2 R = cache/propfirm/nq_nuit_tp4.parquet (build_nq_nuit_tp.py 4, nuit = date de la séance de sortie).
Moteur : celui de propfirm/ftmo.py (run_eval / run_funded) recopié ici avec plusieurs trades par journée ; le
risque de chaque trade = poids x min(r, marge jusqu'au plancher), recalculé avant chaque trade ; perte du jour et
plancher vérifiés après chaque trade ; règle du meilleur jour (50 %) et reward tous les 10 jours tradés sur le P&L
du jour. Coût CFD 1,5 point au niveau actuel du NQ, par trade.
Éval (correction du 2026-11-04) : objectif de chaque trade ramené au reste à faire quand il est sous 2 R, atteint si le
mouvement favorable maximal du trade (MFE_R, barre du stop exclue) le dépasse ; l'ancienne version (objectif fixe à
2 R) est rapportée à côté (p_pass_objectif_fixe).
Périodes : 2016-01 → 2026-08 (sélection de 3n et M2) et 2011-07 → 2015-12 (hors échantillon des trois ; mom y a passé
son test, n° 11 ; 3n et M2 y ont échoué, n° 24 et 25).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.ftmo import DAILY, MAXLOSS, MIN_RISK, SPLIT, TARGET, ev, refusal_breakeven

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/propfirm_trio")
SEED = 1827
COST = 1.5 / 25_684.0
R_EVAL, R_FUND, TP_R = 2.5, 1.0, 2.0
PERIODES = {"2016-01 → 2026-08": ("2016-01-01", "2026-08-28"), "2011-07 → 2015-12": ("2011-07-01", "2015-12-31")}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def bibliotheque() -> pd.DataFrame:
    t = pd.read_csv("results/propfirm_combo/trades_tp2.csv", parse_dates=["date"])
    t = t[["date", "strat", "R_brut", "s", "MFE_R"]]
    m = pd.read_parquet("cache/propfirm/nq_nuit_tp4_mfe.parquet")  # build_mfe_mom.py
    m = pd.DataFrame({"date": pd.to_datetime(m.night), "strat": "mom", "R_brut": m.R_brut,
                      "s": m.risk.fillna(m.risk.median()), "MFE_R": m.MFE_R})
    return pd.concat([t, m], ignore_index=True)


def plan(t: pd.DataFrame, regle: str) -> pd.DataFrame:
    """Une ligne par journée : jusqu'à 2 trades (R brut, poids, coût en R)."""
    g = {s: x.set_index("date") for s, x in t.groupby("strat")}
    jours = sorted(set(t.date))
    rows = []
    for d in jours:
        legs = []
        has = {s: d in g[s].index for s in g}
        if regle == "trio" and has.get("3n"):
            legs = [("3n", 1.0)]
        elif regle == "trio":
            legs = [(s, 0.5) for s in ("mom", "M2") if has.get(s)]
        elif regle == "3n + M2 (1 / jour)":
            legs = [("3n", 1.0)] if has.get("3n") else ([("M2", 1.0)] if has.get("M2") else [])
        elif regle == "mom seul":
            legs = [("mom", 1.0)] if has.get("mom") else []
        if not legs:
            continue
        row = {"date": d, "legs": "+".join(s for s, _ in legs)}
        for k in (1, 2):
            if len(legs) >= k:
                s, w = legs[k - 1]
                x = g[s].loc[d]
                row |= {f"R{k}": float(x.R_brut), f"w{k}": w, f"c{k}": COST / float(x.s), f"M{k}": float(x.MFE_R)}
            else:
                row |= {f"R{k}": 0.0, f"w{k}": 0.0, f"c{k}": 0.0, f"M{k}": 0.0}
        rows.append(row)
    return pd.DataFrame(rows)


def _jour(P, hi, r, J, a, day, best=None):
    """Joue la journée `day` pour les comptes `a` ; renvoie (pnl du jour, échec). Si `best` (meilleur jour passé des
    comptes `a`) est donné, phase d'éval avec objectif ramené au reste à faire : quand l'objectif qui apporte juste
    ce qui manque (cible +10 % et règle du meilleur jour) est sous TP_R, il est atteint si le MFE du trade le dépasse."""
    pnl = np.zeros(len(a))
    fail = np.zeros(len(a), bool)
    for k in (1, 2):
        w = J[f"w{k}"][day]
        act = (w > 0) & ~fail
        if not act.any():
            continue
        floor = hi[a] - MAXLOSS
        risk = w * np.minimum(r, P[a] - floor)
        c = J[f"c{k}"][day]
        R = J[f"R{k}"][day]
        if best is not None:
            need = np.maximum(np.maximum(TARGET - P[a], 2 * np.maximum(best, pnl) - P[a]), 0.01)
            obj = need * (1 + c) / np.maximum(risk, 1e-12) + c
            R = np.where((obj < TP_R) & (J[f"M{k}"][day] >= obj), obj, R)
        leg = np.where(act & (risk >= MIN_RISK * w), risk * (R - c) / (1 + c), 0.0)
        P[a] += leg
        pnl += leg
        fail |= (P[a] <= floor + 1e-9) | (pnl <= -DAILY)
    return pnl, fail


def run_eval(J: dict, r: float, n: int, rng, max_days: int = 3000, reste: bool = True):
    nd = len(J["R1"])
    P, hi, best = np.zeros(n), np.zeros(n), np.zeros(n)
    days, st = np.zeros(n, int), np.zeros(n, int)
    start = rng.integers(0, nd, n)
    for _ in range(max_days):
        a = np.flatnonzero(st == 0)
        if not len(a):
            break
        dead = np.minimum(r, P[a] - (hi[a] - MAXLOSS)) < MIN_RISK
        st[a[dead]] = -1
        a = a[~dead]
        day = (start[a] + days[a]) % nd
        pnl, fail = _jour(P, hi, r, J, a, day, best[a] if reste else None)
        days[a] += 1
        st[a[fail]] = -1
        best[a] = np.maximum(best[a], pnl)
        hi[a] = np.maximum(hi[a], P[a])
        ok = ~fail & (P[a] >= TARGET - 1e-9) & (best[a] <= 0.5 * P[a] + 1e-9)
        st[a[ok]] = 1
    return st == 1, days


def run_funded(J: dict, r: float, n: int, rng, cycle: int = 10, max_days: int = 1000):
    nd = len(J["R1"])
    P, hi, best = np.zeros(n), np.zeros(n), np.zeros(n)
    cyc, days, alive = np.zeros(n, int), np.zeros(n, int), np.ones(n, bool)
    paid, nrew, first = np.zeros(n), np.zeros(n, int), np.full(n, -1)
    start = rng.integers(0, nd, n)
    for _ in range(max_days):
        a = np.flatnonzero(alive)
        if not len(a):
            break
        dead = np.minimum(r, P[a] - (hi[a] - MAXLOSS)) < MIN_RISK
        alive[a[dead]] = False
        a = a[~dead]
        day = (start[a] + days[a]) % nd
        pnl, fail = _jour(P, hi, r, J, a, day)
        days[a] += 1
        cyc[a] += 1
        alive[a[fail]] = False
        best[a] = np.maximum(best[a], pnl)
        hi[a] = np.maximum(hi[a], P[a])
        pay = ~fail & (cyc[a] >= cycle) & (P[a] > 0) & (best[a] <= 0.5 * P[a] + 1e-9)
        b = a[pay]
        paid[b] += SPLIT * P[b]
        nrew[b] += 1
        first[b] = np.where(first[b] < 0, days[b], first[b])
        hi[b], P[b], best[b], cyc[b] = 0.0, 0.0, 0.0, 0
    return paid, nrew, days, first


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    say(f"FTMO 1-Step, plan à trois (3n plein risque, sinon mom r/2 + M2 r/2) ; éval {R_EVAL} %, financé {R_FUND} % ; "
        f"{N} comptes, graine {SEED}")
    t = bibliotheque()
    rng = np.random.default_rng(SEED)
    rows, allj = [], []
    for p, (a, z) in PERIODES.items():
        tp = t[(t.date >= a) & (t.date <= z)]
        an = (pd.Timestamp(z) - pd.Timestamp(a)).days / 365.25
        for regle in ("trio", "3n + M2 (1 / jour)", "mom seul"):
            J = plan(tp, regle)
            allj.append(J.assign(période=p, règle=regle))
            f = len(J) / an
            libs = {regle: J}
            if regle == "trio":  # sans edge : chaque stratégie recentrée sur sa propre moyenne
                dm = J.copy()
                for s in ("3n", "mom", "M2"):
                    mu = tp.R_brut[tp.strat == s].mean()
                    for k in (1, 2):
                        sel = J.legs.str.split("+").str[k - 1] == s
                        dm.loc[sel, f"R{k}"] = J.loc[sel, f"R{k}"] - mu
                libs[f"{regle}, sans edge"] = dm
            for k, JJ in libs.items():
                arr = {c: JJ[c].to_numpy(float) for c in ("R1", "w1", "c1", "M1", "R2", "w2", "c2", "M2")}
                ok0, d0 = run_eval(arr, R_EVAL, N, rng, reste=False)
                ok, d = run_eval(arr, R_EVAL, N, rng)
                pp = ok.mean()
                paid, nr, life, first = run_funded(arr, R_FUND, N, rng)
                comp = JJ.legs.value_counts(normalize=True).mul(100).round(1).to_dict()
                row = dict(période=p, règle=k, jours_an=f, R_jour=float((JJ.w1 * JJ.R1 + JJ.w2 * JJ.R2).mean()),
                           p_pass=pp, mois_eval=d[ok].mean() / f * 12, mois_tentative=d.mean() / f * 12,
                           v_pct=paid.mean(), p_reward=(nr > 0).mean(), n_rewards=nr.mean(), vie_mois=life.mean() / f * 12,
                           premier_reward_mois=np.median(first[first > 0]) / f * 12 if (first > 0).any() else np.nan,
                           composition=str(comp), p_pass_objectif_fixe=ok0.mean(),
                           mois_eval_objectif_fixe=d0[ok0].mean() / f * 12)
                for size in (10_000, 100_000):
                    x, ci = ev(pp, np.sqrt(pp * (1 - pp) / N), paid.mean(), paid.std() / np.sqrt(N), size)
                    row[f"EV {size // 1000}k"], row[f"IC {size // 1000}k"] = x, ci
                    row[f"EV/mois {size // 1000}k"] = x / (row["mois_tentative"] + pp * row["vie_mois"])
                rows.append(row)
                say(f"\n{p} · {k} : {f:.0f} journées tradées/an, R moyen par jour (pondéré) {row['R_jour']:+.3f} ; "
                    f"composition {comp}\n  passage {pp:.1%} en ≈ {row['mois_eval']:.1f} mois (objectif fixe : "
                    f"{ok0.mean():.1%} en {row['mois_eval_objectif_fixe']:.1f} mois) ; financé {row['v_pct']:.1f} % "
                    f"du capital, P(reward) {row['p_reward']:.0%}, {row['n_rewards']:.1f} rewards, vie {row['vie_mois']:.0f} mois ; "
                    f"EV {row['EV 10k']:+,.0f} $ (10k) / {row['EV 100k']:+,.0f} $ (100k) ; par mois d'emplacement "
                    f"{row['EV/mois 10k']:+,.0f} / {row['EV/mois 100k']:+,.0f} $")
    pd.DataFrame(rows).to_csv(OUT / "ftmo.csv", index=False)
    pd.concat(allj).to_csv(OUT / "jours.csv", index=False)
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
