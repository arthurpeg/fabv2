"""FTMO 1-Step avec BB (bande de bruit, VWAP à l'entrée), un trade par jour : approche par convexité.

EXPLORATOIRE, hors compteur (comme run_propfirm_combo.py) : évaluation d'un contrat sur des trades existants
(results/bb_1j/, run_bb_1j.py, branche strategies-vbt, NQ 2016-01 → 2026-08 déjà explorés). BB est au registre des
échecs ; aucun chiffre ici n'est hors échantillon.

uv run python run_propfirm_bb.py [N] → results/propfirm_bb/ (ftmo.csv, run.log)

Moteur propfirm.ftmo (n° 18), en mode stratégie : un trade = une journée FTMO, R brut historique, coût CFD 1,5 point au
niveau actuel du NQ (25 684), comme run_propfirm_combo.py. Règles : objectif +10 %, perte max 10 % (glissante sur le plus
haut), perte du jour 3 %, meilleur jour ≤ 50 % du gain, reward tous les 10 trades en financé, partage 90 %.
Grille : les 18 bibliothèques BB (mode A / B × SL 0,25 / 0,5 / 1 ATR × TP 1 / 2 / 3 R) × risque en éval {1 ; 2 ; 2,5 ;
2,9 %} ; financé 1 % (plan retenu). Témoin « sans edge » (R recentré) pour la meilleure. Références : les
bibliothèques du plan (results/propfirm_combo/ftmo.csv, 2016-2026, éval 2,5 %).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.ftmo import Market, TradeLib, ev, run_eval, run_funded

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000
OUT = Path("results/propfirm_bb")
SEED = 1826
COST = 1.5 / 25_684.0
R_EVALS, R_FUND = [1.0, 2.0, 2.5, 2.9], 1.0
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def simulate(t: pd.DataFrame, r_eval: float, f: float, rng) -> dict:
    m = Market(TradeLib(t.date.values, t.s.to_numpy(), t.R_brut.to_numpy()), np.nan, COST)
    ok, d = run_eval(m, r_eval, 0.0, N, rng)
    p = ok.mean()
    paid, nr, life, first = run_funded(m, R_FUND, 0.0, N, rng, reset=True)
    row = dict(trades_an=f, risque_eval=r_eval, p_pass=p, trades_valid_med=np.median(d[ok]) if ok.any() else np.nan,
               trades_echec_med=np.median(d[~ok]) if (~ok).any() else np.nan, mois_tentative=d.mean() / f * 12,
               v_pct=paid.mean(), p_reward=(nr > 0).mean(), vie_mois=life.mean() / f * 12)
    for size in (10_000, 100_000):
        x, ci = ev(p, np.sqrt(p * (1 - p) / N), paid.mean(), paid.std() / np.sqrt(N), size)
        row[f"EV {size // 1000}k"] = x
        row[f"EV/mois {size // 1000}k"] = x / (row["mois_tentative"] + p * row["vie_mois"])
    return row


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    rng = np.random.default_rng(SEED)
    say(f"FTMO 1-Step, BB un trade par jour ; éval {R_EVALS} %, financé {R_FUND} % ; {N} comptes par réglage, graine {SEED}")
    rows = []
    for mode in ("A", "B"):
        for k in (0.25, 0.5, 1.0):
            for rr in (1, 2, 3):
                t = pd.read_csv(f"results/bb_1j/trades_{mode}_{k}_{rr}.csv", parse_dates=["date"])
                t = t[np.isfinite(t.R_brut) & (t.s > 0)].reset_index(drop=True)
                f = len(t) / ((t.date.max() - t.date.min()).days / 365.25)
                for r in R_EVALS:
                    row = simulate(t, r, f, rng)
                    row.update(lib=f"BB {mode} SL {k} ATR TP {rr}R", R_brut_moy=t.R_brut.mean(),
                               cout_R=np.median(COST / t.s))
                    rows.append(row)
    tab = pd.DataFrame(rows)
    cols = ["lib", "risque_eval", "trades_an", "R_brut_moy", "cout_R", "p_pass", "trades_valid_med", "trades_echec_med",
            "mois_tentative", "v_pct", "p_reward", "vie_mois", "EV 10k", "EV 100k", "EV/mois 10k", "EV/mois 100k"]
    tab = tab[cols]
    tab.to_csv(OUT / "ftmo.csv", index=False)
    say(tab.round(3).to_string(index=False))
    best = tab.sort_values("EV/mois 100k", ascending=False).iloc[0]
    say(f"\nMeilleur réglage (EV par mois d'emplacement 100k) : {best.lib}, éval {best.risque_eval} %")
    mode, k, rr = best.lib.split()[1], float(best.lib.split()[3]), int(best.lib.split()[-1][:-1])
    t = pd.read_csv(f"results/bb_1j/trades_{mode}_{k}_{rr}.csv", parse_dates=["date"])
    t = t[np.isfinite(t.R_brut) & (t.s > 0)].reset_index(drop=True)
    f = len(t) / ((t.date.max() - t.date.min()).days / 365.25)
    z = simulate(t.assign(R_brut=t.R_brut - t.R_brut.mean()), best.risque_eval, f, rng)
    say(f"Témoin sans edge (R recentré) : passage {z['p_pass']:.1%}, EV {z['EV 10k']:+,.0f} $ (10k) / {z['EV 100k']:+,.0f} $ "
        f"(100k), par mois {z['EV/mois 100k']:+,.0f} $ (100k)")
    ref = pd.read_csv("results/propfirm_combo/ftmo.csv")
    ref = ref[ref.lib.str.contains("2016")][["lib", "trades_an", "p_pass", "trades_eval", "EV 10k", "EV 100k", "EV/mois 100k"]]
    say("\nRéférences du plan (éval 2,5 %, financé 1 %, 2016-2026) :\n" + ref.round(2).to_string(index=False))
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
