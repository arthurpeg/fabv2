"""Exploratoire (non pré-enregistré) : plusieurs comptes FTMO 1-Step décalés dans le temps, tous sur la règle NQ de nuit.

uv run python run_propfirm_farm.py  → results/propfirm_farm/ (run.log, windows.csv)

Chaque « emplacement » achète une éval 10k (87 $), la passe ou la rate, puis tourne en financé jusqu'à
la perte max, puis rachète une éval le jour suivant. Éval 2 % de risque, financé 1 %, spread 1,5 point,
règles FTMO vérifiées (RAZ après reward, reward au 10e jour de bourse du compte, 90 %), 3 jours de
vérification entre l'éval et le financé. Les trades sont ceux de l'historique réel, dans l'ordre :
tous les comptes prennent les mêmes trades les mêmes nuits ; seul l'instant de départ diffère.
Un emplacement décalé de k mois a démarré k mois avant la fenêtre : tous sont observés sur les mêmes nuits.

Fenêtres de 2 ans (504 trades) commençant tous les 5 trades sur 2011-07 → 2026-08 (bouclage) ;
on compare le gain net par emplacement selon la façon de répartir 5 emplacements.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.ftmo import DAILY, MAXLOSS, SPLIT, TARGET

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_farm")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
SIZE, FEE = 10_000, 79 * 1.10
R_EVAL, R_FUND, CYCLE, REVIEW = 2.0, 1.0, 10, 3
COST = 1.5 / 25_684.0
H, STEP, K = 504, 5, 5


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


t = pd.read_csv("results/couts_reels_nq_nuit/trades.csv").sort_values("entry_idx")
R = t.R_brut.to_numpy()
C = COST / t.risk.fillna(t.risk.median()).to_numpy()
NT = len(R)


def slot_cash(start: int, lead: int = 0) -> np.ndarray:
    """Flux en $ d'un emplacement sur les H nuits à partir de `start` ; l'emplacement a démarré `lead` nuits
    plus tôt (il arrive donc dans la fenêtre à un autre moment de sa vie)."""
    L = lead + H
    cash = np.zeros(L)
    start -= lead
    i = 0
    while i < L:
        cash[i] -= FEE  # achat d'une éval
        P = hi = best = 0.0
        passed = False
        while i < L:
            j = (start + i) % NT
            risk = min(R_EVAL, P - (hi - MAXLOSS))
            pnl = risk * (R[j] - C[j]) / (1 + C[j])
            floor = hi - MAXLOSS
            P += pnl; i += 1
            if P <= floor + 1e-9 or pnl <= -DAILY:
                break
            best = max(best, pnl); hi = max(hi, P)
            if P >= TARGET and best <= 0.5 * P:
                passed = True
                break
        if not passed:
            continue
        i += REVIEW
        P = hi = best = 0.0
        cyc = 0
        while i < L:
            j = (start + i) % NT
            floor = hi - MAXLOSS
            risk = min(R_FUND, P - floor)
            if risk < 0.05:
                break
            pnl = risk * (R[j] - C[j]) / (1 + C[j])
            P += pnl; i += 1; cyc += 1
            if P <= floor + 1e-9 or pnl <= -DAILY:
                break
            best = max(best, pnl); hi = max(hi, P)
            if cyc >= CYCLE and P > 0 and best <= 0.5 * P:
                cash[i - 1] += SPLIT * P / 100 * SIZE
                P = hi = best = 0.0; cyc = 0
        i += 1
    return cash[lead:]


def main() -> None:
    rng = np.random.default_rng(7)
    starts = np.arange(0, NT, STEP)
    one = {s: slot_cash(s, 0) for s in starts}
    configs = {
        "1 emplacement": lambda s: [one[s]],
        "5 synchrones (même départ)": lambda s: [one[s]] * K,
        "5 décalés de 1 mois (21 nuits)": lambda s: [slot_cash(s, 21 * k) for k in range(K)],
        "5 décalés de 3 mois (63 nuits)": lambda s: [slot_cash(s, 63 * k) for k in range(K)],
        "5 indépendants (histoires différentes)": lambda s: [one[starts[rng.integers(len(starts))]] for _ in range(K)],
    }
    rows = []
    say(f"Ferme FTMO 10k, règle NQ de nuit ; {len(starts)} fenêtres de {H} nuits ; gain net par emplacement sur 2 ans")
    say(f"{'configuration':<40} {'moyenne':>8} {'écart-type':>10} {'P(perte)':>8} {'5e centile':>10} {'pire':>8} "
        f"{'mois sans reward (méd.)':>24}")
    for name, f in configs.items():
        tot, gaps = [], []
        for s in starts:
            cs = f(s)
            farm = np.sum(cs, axis=0)
            tot.append(farm.sum() / len(cs))
            m = np.add.reduceat(np.clip(farm, 0, None), np.arange(0, H, 21))  # rewards par mois
            gaps.append((m == 0).mean())
            rows.append(dict(config=name, start=s, net_per_slot=tot[-1], months_no_reward=gaps[-1]))
        tot = np.array(tot)
        say(f"{name:<40} {tot.mean():>+8.0f} {tot.std():>10.0f} {np.mean(tot < 0):>8.0%} {np.percentile(tot, 5):>+10.0f} "
            f"{tot.min():>+8.0f} {np.median(gaps):>23.0%}")
    pd.DataFrame(rows).to_csv(OUT / "windows.csv", index=False)


if __name__ == "__main__":
    main()
