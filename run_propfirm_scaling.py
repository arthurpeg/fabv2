"""Exploratoire : chiffres par taille de compte FTMO 1-Step pour un plan de montée en taille (règle NQ de nuit,
un compte par heure 19:00 / 20:00 / 21:00, éval 2 % TP 5, financé 1 % TP 4, rachat permanent).

uv run python run_propfirm_scaling.py  → results/propfirm_scaling/ (run.log, sizes.csv)

Rendements de chaque nuit : results/propfirm_farm_heures/returns.csv (vectorbt). Règles : run_propfirm_vbt.replay.
Prix 1-Step (octobre 2026, non revérifiés) : 10k 79 €, 25k 199 €, 50k 319 €, 100k 499 €, 200k 999 € ; 1 € = 1,10 $.
Par taille : sur 662 fenêtres de 2 ans, gain net d'un trio de comptes (un par heure), frais, rewards, pire creux de
trésorerie, plus longue série d'évals ratées et plus longue période sans reward pour le trio.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_propfirm_vbt as V
from propfirm.ftmo import EUR, PRICES_EUR

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_scaling")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
HOURS = ("19:00", "20:00", "21:00")
H, STEP = 504, 5


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


R = pd.read_csv("results/propfirm_farm_heures/returns.csv", index_col=0, parse_dates=True)
NT = len(R)


def slot(hour: str, start: int, n: int):
    r5, r4, s = R[f"ret_{hour}_tp5"].to_numpy(), R[f"ret_{hour}_tp4"].to_numpy(), R[f"stop_{hour}"].to_numpy()

    def pnl(i, ph, risk):
        x = (r5 if ph == "éval" else r4)[i]
        return 0.0 if np.isnan(x) else risk * x / (s[i] + V.COST)

    ev, _ = V.replay(pnl, start + n, start)
    return ev


def main() -> None:
    starts = np.arange(0, NT - H, STEP)
    events = {(h, s0): slot(h, s0, H) for h in HOURS for s0 in starts}
    say(f"Trio de comptes FTMO 1-Step (19:00 / 20:00 / 21:00), rachat permanent, {len(starts)} fenêtres de {H} nuits (2 ans)")
    rows = []
    for size, eur in PRICES_EUR.items():
        fee = eur * EUR
        res = []
        for s0 in starts:
            cash = np.zeros(H); nfee = nrew = 0; fails = []
            for h in HOURS:
                run = best = 0
                for k, j, *x in events[(h, s0)]:
                    if k == "achat":
                        cash[j - s0] -= fee; nfee += 1
                    elif k == "reward":
                        cash[j - s0] += x[0] / 100 * size; nrew += 1
                    elif k == "ratée":
                        run += 1; best = max(best, run)
                    elif k == "validée":
                        run = 0
                fails.append(best)
            cum = np.cumsum(cash)
            dd = (cum - np.maximum.accumulate(np.concatenate([[0.0], cum]))[1:]).min()
            pay = np.flatnonzero(cash > 0)
            gaps = np.diff(np.concatenate([[0], pay, [H - 1]]))
            res.append((cum[-1], nfee * fee, nrew, dd, max(fails), gaps.max(), -cum.min()))
        a = np.array(res)
        row = dict(taille=size, prix_usd=fee, net_2ans_moy=a[:, 0].mean(), net_5e=np.percentile(a[:, 0], 5), net_pire=a[:, 0].min(),
                   frais_2ans_moy=a[:, 1].mean(), rewards_2ans_moy=a[:, 2].mean(), creux_pire=a[:, 3].min(), creux_5e=np.percentile(a[:, 3], 5),
                   ratées_pire=a[:, 4].max(), sans_reward_pire_nuits=a[:, 5].max(), mise_max_pire=a[:, 6].max())
        rows.append(row)
        say(f"  {size // 1000:>3}k (éval {fee:,.0f} $) : net sur 2 ans pour le trio moy. {row['net_2ans_moy']:+,.0f} $, 5e centile "
            f"{row['net_5e']:+,.0f} $, pire {row['net_pire']:+,.0f} $ ; frais moy. {row['frais_2ans_moy']:,.0f} $ ; "
            f"{row['rewards_2ans_moy']:.1f} rewards ; pire creux {row['creux_pire']:,.0f} $ (5e centile {row['creux_5e']:,.0f} $) ; "
            f"pire mise de départ avant d'être payé {row['mise_max_pire']:,.0f} $ ; pire série d'évals ratées (un compte) "
            f"{row['ratées_pire']:.0f} ; plus longue période sans reward pour le trio {row['sans_reward_pire_nuits']:.0f} nuits".replace(",", " "))
    pd.DataFrame(rows).to_csv(OUT / "sizes.csv", index=False)


if __name__ == "__main__":
    main()
