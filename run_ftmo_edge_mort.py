"""Hasard ou edge qui peut mourir en live ? (demande du 2026-11-22). EXPLORATOIRE, hors compteur (analyse de
sensibilité, aucune nouvelle règle de trading).

uv run python run_ftmo_edge_mort.py [N] → results/ftmo_edge_mort/ (scenarios.csv, priors.csv, run.log)

Question : en prop firm, on gagne déjà sans edge (effet de contrat). Vaut-il mieux trader au hasard, ou trader mom
en sachant que son edge peut ne plus marcher en live ?

Méthode : mom NQ de nuit (bibliothèque TP 4 ATR + MFE), même moteur que run_ftmo_payout_policy.py (éval 2,5 %
objectif ramené au reste à faire, financé 1 %, politiques « actuel » et « cible+attente »). Edge live = h × edge
historique, obtenue par ré-échantillonnage pondéré des vrais trades (inclinaison exponentielle : poids ∝ exp(θ R),
θ tel que la moyenne pondérée de R vaille h × moyenne historique) : les gagnants deviennent plus rares, mais chaque
trade garde son R, son MFE et son stop réels (un stop reste à −1 R). Bibliothèque i.i.d. de 50 000 nuits par
scénario, y compris h = 1 (θ = 0). h = 1 edge intacte, h = 0 edge morte (= hasard : mêmes trades, mêmes coûts, gain
brut moyen nul), h < 0 edge inversée.
Un simple décalage R − (1 − h) × moyenne (comme le contrôle sans edge de run_ftmo_payout_policy_sans_edge.py) pousse
les pires stops (−1,06 R) sous −1,2 R, qui touchent alors la perte journalière de 3 % à 2,5 % de risque : artefact,
écarté ici.
Le « hasard » de référence est h = 0 : c'est exactement ce que devient une stratégie dont l'edge a disparu.
L'EV est linéaire dans la probabilité de chaque scénario : EV(prior) = Σ p(h) × EV(h).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_payout_policy as P
import run_propfirm_trio as T
from propfirm.ftmo import ev

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/ftmo_edge_mort")
SEED = 1840
H = [-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0]
PERIODES = {"2016-01 → 2026-08": ("2016-01-01", "2026-08-28"), "2011-07 → 2015-12": ("2011-07-01", "2015-12-31")}
POLS = ["actuel", "cible+attente"]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


NLIB = 50_000


def incline(m0: pd.DataFrame, cible: float, rng) -> pd.DataFrame:
    """Ré-échantillonne NLIB trades de m0 avec poids ∝ exp(θ R) tels que E_w[R] = cible."""
    R = m0.R_brut.to_numpy()
    lo, hi = -20.0, 20.0
    for _ in range(100):
        th = (lo + hi) / 2
        w = np.exp(th * (R - R.mean()))
        if (w * R).sum() / w.sum() < cible:
            lo = th
        else:
            hi = th
    w /= w.sum()
    idx = rng.choice(len(R), NLIB, p=w)
    return m0.iloc[idx].reset_index(drop=True)


def scenario(m0: pd.DataFrame, h: float, mu: float, f: float, rng) -> list[dict]:
    m = incline(m0, h * mu, rng)
    R, cc, M = m.R_brut.to_numpy(), (P.COST / m.s).to_numpy(), m.MFE_R.to_numpy()
    z = np.zeros(len(m))  # même format que T.plan(m, "mom seul") : une jambe par nuit
    arr = dict(R1=R, w1=z + 1.0, c1=cc, M1=M, R2=z, w2=z, c2=z, M2=z)
    ok, d = T.run_eval(arr, T.R_EVAL, N, rng)
    pp = ok.mean()
    eval_mois = d.mean() / f * 12  # durée moyenne d'une tentative d'éval (réussie ou non)
    rows = []
    for pol in POLS:
        paid, nr, life, _ = P.finance_mc(R, cc, M, pol, N, rng)
        row = dict(h=h, politique=pol, passage=pp, eval_mois=eval_mois, valeur_fin=paid.mean(),
                   p_reward=(nr > 0).mean(), vie_mois=life.mean() / f * 12)
        for size in (10_000, 100_000):
            x, ci = ev(pp, np.sqrt(pp * (1 - pp) / N), paid.mean(), paid.std() / np.sqrt(N), size)
            row[f"EV{size // 1000}k"] = x
            row[f"IC{size // 1000}k"] = ci
            row[f"EVmois{size // 1000}k"] = x / (eval_mois + pp * row["vie_mois"])
        rows.append(row)
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    lib = T.bibliotheque()
    say(f"Hasard ou edge qui peut mourir : mom, edge live = h × edge historique ; {N} comptes par scénario, graine {SEED}")
    rows = []
    for per, (a, z) in PERIODES.items():
        m0 = lib[(lib.strat == "mom") & (lib.date >= a) & (lib.date <= z)].sort_values("date").copy()
        mu = m0.R_brut.mean()
        f = len(m0) / ((pd.Timestamp(z) - pd.Timestamp(a)).days / 365.25)
        say(f"\n{per} : {len(m0)} nuits, edge historique {mu:+.3f} R brut par trade, {f:.0f} trades par an")
        for h in H:
            for r in scenario(m0, h, mu, f, rng):
                r |= dict(période=per, mu=mu, R_live=h * mu)
                rows.append(r)
    S = pd.DataFrame(rows)
    S.to_csv(OUT / "scenarios.csv", index=False)
    pd.set_option("display.width", 250)
    cols = ["période", "politique", "h", "R_live", "passage", "p_reward", "vie_mois", "EV10k", "IC10k", "EV100k",
            "EVmois100k"]
    say("\n" + S[cols].round(3).to_string(index=False))

    # Seuil : probabilité que l'edge soit morte (h = 0) ou inversée (h = -0,5) au-delà de laquelle le hasard gagne
    say("\nSeuils (par tentative 10k / par mois 100k) : q* = part de « edge morte » qui annule l'avantage de l'edge")
    pri = []
    for (per, pol), g in S.groupby(["période", "politique"], sort=False):
        e = g.set_index("h")
        for metric in ("EV10k", "EVmois100k"):
            ref = e.loc[0.0, metric]  # hasard
            for dead in (0.0, -0.5, -1.0):
                gain = e.loc[1.0, metric] - ref
                perte = ref - e.loc[dead, metric]
                q = 1.0 if perte <= 0 else gain / (gain + perte)
                say(f"  {per} {pol:13s} {metric:10s} : edge intacte {e.loc[1.0, metric]:+8.0f} ; hasard {ref:+8.0f} ;"
                    f" scénario mort h={dead:+.1f} {e.loc[dead, metric]:+8.0f} → hasard meilleur si P(mort) > {q:.0%}")
        # quelques priors explicites (p sur h)
        priors = {
            "optimiste (70 % intacte, 30 % morte)": {1.0: 0.7, 0.0: 0.3},
            "McLean-Pontiff (edge live = 0,5 × backtest)": {0.5: 1.0},
            "pessimiste (25 % intacte, 50 % morte, 25 % inversée)": {1.0: 0.25, 0.0: 0.5, -0.5: 0.25},
            "très pessimiste (10 % intacte, 60 % morte, 30 % inversée)": {1.0: 0.1, 0.0: 0.6, -0.5: 0.3},
            "catastrophe (50 % morte, 50 % inversée totale)": {0.0: 0.5, -1.0: 0.5},
        }
        for nom, p in priors.items():
            pri.append(dict(période=per, politique=pol, prior=nom,
                            EV10k=sum(w * e.loc[h, "EV10k"] for h, w in p.items()),
                            hasard10k=e.loc[0.0, "EV10k"],
                            EVmois100k=sum(w * e.loc[h, "EVmois100k"] for h, w in p.items()),
                            hasard_mois100k=e.loc[0.0, "EVmois100k"]))
    Pr = pd.DataFrame(pri)
    Pr.to_csv(OUT / "priors.csv", index=False)
    say("\nPriors (EV de « trader mom » contre « trader au hasard ») :\n" + Pr.round(0).to_string(index=False))
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
