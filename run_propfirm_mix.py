"""FTMO 1-Step : un plan pour l'éval, un autre pour le compte financé (demande du 2026-11-04 : mom seul en éval, puis le
trio une fois financé). EXPLORATOIRE, hors compteur.

uv run python run_propfirm_mix.py [N] → results/propfirm_mix/ (run.log, mix.csv)

Plans et moteur : ceux de run_propfirm_trio.py (mêmes trades, objectif à 2 R, coût CFD 1,5 point). Éval à 2,5 % :
« mom » = mom seul à 2,5 % ; « trio » = 3n à 2,5 % si signal, sinon mom 1,25 % + M2 1,25 %. Financé à 1 % : « mom » =
mom seul à 1 % ; « trio » = 3n 1 %, sinon mom 0,5 % + M2 0,5 %. Les quatre croisements sont simulés.
EV par tentative = P(passage) x valeur du financé - prix de l'éval ; par mois d'emplacement = EV / (durée moyenne
d'une tentative + P(passage) x vie moyenne du financé), chaque phase convertie en mois avec la fréquence de son plan.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_propfirm_trio as T
from propfirm.ftmo import ev

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/propfirm_mix")
SEED = 1829
PERIODES = {"2016-01 → 2026-08": ("2016-01-01", "2026-08-28"), "2011-07 → 2015-12": ("2011-07-01", "2015-12-31"),
            "2019-01 → 2026-08": ("2019-01-01", "2026-08-28")}
PLANS = {"mom": "mom seul", "trio": "trio"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    log = [f"FTMO 1-Step, plan d'éval × plan de financé ; éval {T.R_EVAL} %, financé {T.R_FUND} % ; {N} comptes, graine {SEED}"]
    t = T.bibliotheque()
    rng = np.random.default_rng(SEED)
    rows = []
    for p, (a, z) in PERIODES.items():
        tp = t[(t.date >= a) & (t.date <= z)]
        an = (pd.Timestamp(z) - pd.Timestamp(a)).days / 365.25
        J = {k: T.plan(tp, v) for k, v in PLANS.items()}
        arr = {k: {c: j[c].to_numpy(float) for c in ("R1", "w1", "c1", "R2", "w2", "c2")} for k, j in J.items()}
        freq = {k: len(j) / an for k, j in J.items()}
        E = {}
        for k in PLANS:
            ok, d = T.run_eval(arr[k], T.R_EVAL, N, rng)
            E[k] = (ok.mean(), d[ok].mean() / freq[k] * 12, d.mean() / freq[k] * 12)
        F = {}
        for k in PLANS:
            paid, nr, life, first = T.run_funded(arr[k], T.R_FUND, N, rng)
            F[k] = (paid.mean(), paid.std() / np.sqrt(N), (nr > 0).mean(), nr.mean(), life.mean() / freq[k] * 12,
                    np.median(first[first > 0]) / freq[k] * 12)
        for ke in PLANS:
            for kf in PLANS:
                pp, m_ok, m_t = E[ke]
                v, sv, pr, nrw, vie, prem = F[kf]
                row = dict(période=p, éval=ke, financé=kf, passage=pp, mois_eval=m_ok, valeur_financé=v, p_reward=pr,
                           rewards=nrw, vie_mois=vie, premier_reward_mois=prem)
                for size in (10_000, 100_000):
                    x, ci = ev(pp, np.sqrt(pp * (1 - pp) / N), v, sv, size)
                    row[f"EV {size // 1000}k"], row[f"IC {size // 1000}k"] = x, ci
                    row[f"EV/mois {size // 1000}k"] = x / (m_t + pp * vie)
                rows.append(row)
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "mix.csv", index=False)
    cols = ["période", "éval", "financé", "passage", "mois_eval", "valeur_financé", "p_reward", "rewards", "vie_mois",
            "premier_reward_mois", "EV 10k", "EV 100k", "EV/mois 10k", "EV/mois 100k"]
    log.append(R[cols].round(3).to_string(index=False))
    print("\n".join(log))
    (OUT / "run.log").write_text("\n".join(log), encoding="utf-8")


if __name__ == "__main__":
    main()
