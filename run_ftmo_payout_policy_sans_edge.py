"""Contrôle sans edge de run_ftmo_payout_policy.py : mom recentré (R − moyenne, MFE − moyenne, plancher 0), mêmes
politiques, même éval, même graine. EXPLORATOIRE, hors compteur.

uv run python run_ftmo_payout_policy_sans_edge.py → results/ftmo_payout_policy/historique_sans_edge.csv
"""
import sys
import numpy as np, pandas as pd
import run_ftmo_payout_policy as P
import run_propfirm_trio as T
from propfirm.ftmo import ev
N = 20_000
rng = np.random.default_rng(P.SEED)
lib = T.bibliotheque()
rows = []
for p, (a, z) in {"2016-01 → 2026-08": ("2016-01-01", "2026-08-28"), "2011-07 → 2015-12": ("2011-07-01", "2015-12-31")}.items():
    m = lib[(lib.strat == "mom") & (lib.date >= a) & (lib.date <= z)].sort_values("date").copy()
    mu = m.R_brut.mean()
    m["R_brut"] -= mu
    m["MFE_R"] = np.maximum(m.MFE_R - mu, 0.0)
    R, cc, M = m.R_brut.to_numpy(), (P.COST / m.s).to_numpy(), m.MFE_R.to_numpy()
    f = len(m) / ((pd.Timestamp(z) - pd.Timestamp(a)).days / 365.25)
    J = T.plan(m, "mom seul")
    arr = {c_: J[c_].to_numpy(float) for c_ in ("R1", "w1", "c1", "M1", "R2", "w2", "c2", "M2")}
    ok, d = T.run_eval(arr, T.R_EVAL, N, rng)
    pp, m_t = ok.mean(), d.mean() / f * 12
    for pol in P.POLITIQUES:
        paid, nr, life, traded = P.finance_mc(R, cc, M, pol, N, rng)
        row = dict(période=p, politique=pol, mu=mu, passage=pp, eval_mois=d[ok].mean() / f * 12, valeur=paid.mean(),
                   p_reward=(nr > 0).mean(), rewards=nr.mean(), reward_moyen=paid.sum() / max(nr.sum(), 1),
                   vie_mois=life.mean() / f * 12)
        for size in (10_000, 100_000):
            x, _ = ev(pp, np.sqrt(pp * (1 - pp) / N), paid.mean(), paid.std() / np.sqrt(N), size)
            row[f"EV{size // 1000}k"] = x
            row[f"EVm{size // 1000}k"] = x / (m_t + pp * row["vie_mois"])
        rows.append(row)
H = pd.DataFrame(rows)
H.to_csv("results/ftmo_payout_policy/historique_sans_edge.csv", index=False)
pd.set_option("display.width", 250)
print(H.round(3).to_string(index=False))
