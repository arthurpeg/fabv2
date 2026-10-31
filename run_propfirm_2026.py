"""Exploratoire : FTMO 1-Step 10k sur la règle NQ de nuit depuis le 2026-01-01, en partant d'une éval
et en achetant une éval de plus à chaque reward reçu.

uv run python run_propfirm_2026.py  → results/propfirm_2026/ (run.log, events.csv)

Rendements de chaque nuit : results/propfirm_vbt/returns.csv (vectorbt, spread 1,5 pt). Réglage de l'avenant E :
éval 2 % de risque (TP 5 ATR), financé 1 % (TP 4 ATR), 3 nuits de vérification, reward au 10e trade du compte,
90 %, RAZ de la perte max, tolérance 0,001 % sur les seuils, éval abandonnée sous 0,05 % de marge.
Tous les comptes prennent le même trade chaque nuit. Données jusqu'au 2026-08-28 (après : holdout, non chargé).

Deux politiques :
- « à la lettre » : un compte ne sert qu'une fois (éval ratée ou financé perdu = fin) ; chaque reward paie une
  nouvelle éval achetée la nuit suivante ;
- « + rachat » : en plus, une éval ratée ou un financé perdu est remplacé par une nouvelle éval la nuit suivante.
Les financés encore en vie le 2026-08-28 ont un profit non retiré qui n'est pas compté.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.ftmo import DAILY, EUR, MAXLOSS, PRICES_EUR, SPLIT, TARGET

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_2026")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
SIZE, FEE = 10_000, PRICES_EUR[10_000] * EUR
R_EVAL, R_FUND, CYCLE, REVIEW = 2.0, 1.0, 10, 3
COST, TOL = 1.5 / 25_684.0, 1e-3
START = "2026-01-01"

r = pd.read_csv("results/propfirm_vbt/returns.csv", parse_dates=["night"])
NIGHT = r.night.dt.date.to_numpy()
NT = len(r)
RET = {"éval": r.ret_tp5.to_numpy(), "financé": r.ret_tp4.to_numpy()}
S = r.stop.to_numpy()


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def pnl(i: int, phase: str, risk: float) -> float:
    return risk * RET[phase][i] / (S[i] + COST)


def account(i: int, acc: int) -> list[tuple]:
    """Vie d'un compte acheté la nuit i : (nuit, compte, événement, $). Finit à l'échec, à la perte du financé
    ou à la fin des données (« en cours »)."""
    ev = [(i, acc, "achat éval", -FEE)]
    P = hi = best = 0.0
    passed = False
    while i < NT:
        floor = hi - MAXLOSS
        risk = min(R_EVAL, P - floor)
        if risk < 0.05:
            break
        x = pnl(i, "éval", risk)
        P += x; i += 1
        if P <= floor + TOL or x <= -DAILY:
            break
        best = max(best, x); hi = max(hi, P)
        if P >= TARGET - TOL and best <= 0.5 * P + TOL:
            passed = True
            break
    if i >= NT and not passed:
        return ev + [(NT - 1, acc, f"éval en cours ({P:+.2f} %)", 0.0)]
    ev.append((i - 1, acc, "éval validée" if passed else "éval ratée", 0.0))
    if not passed:
        return ev
    i += REVIEW
    P = hi = best = 0.0
    cyc = 0
    while i < NT:
        floor = hi - MAXLOSS
        risk = min(R_FUND, P - floor)
        if risk < 0.05:
            break
        x = pnl(i, "financé", risk)
        P += x; i += 1; cyc += 1
        if P <= floor + TOL or x <= -DAILY:
            return ev + [(i - 1, acc, "financé perdu", 0.0)]
        best = max(best, x); hi = max(hi, P)
        if cyc >= CYCLE and P > TOL and best <= 0.5 * P + TOL:
            ev.append((i - 1, acc, "reward", SPLIT * P / 100 * SIZE))
            P = hi = best = 0.0; cyc = 0
    if i >= NT:
        return ev + [(NT - 1, acc, f"financé en cours ({P:+.2f} % non retiré)", 0.0)]
    return ev + [(i - 1, acc, "financé perdu", 0.0)]


def farm(rebuy: bool) -> pd.DataFrame:
    i0 = int(np.searchsorted(NIGHT, pd.Timestamp(START).date()))
    todo, events, n = [(i0, 1)], [], 1
    while todo:
        i, acc = todo.pop(0)
        if i >= NT:
            continue
        ev = account(i, acc)
        events += ev
        for j, _, k, _ in ev:
            if k == "reward" or (rebuy and k in ("éval ratée", "financé perdu")):
                n += 1
                todo.append((j + 1, n))
    E = pd.DataFrame(events, columns=["i", "compte", "événement", "usd"]).sort_values(["i", "compte"])
    E.insert(0, "nuit", NIGHT[E.i])
    return E.drop(columns="i")


def main() -> None:
    say(f"FTMO 1-Step 10k, règle NQ de nuit (rendements vectorbt), du {START} au {NIGHT[-1]} ; éval {FEE:.0f} $")
    for name, rebuy in (("à la lettre (1 éval de plus par reward)", False), ("+ rachat après échec ou compte perdu", True)):
        E = farm(rebuy)
        E.to_csv(OUT / f"events_{'lettre' if not rebuy else 'rachat'}.csv", index=False)
        fees = -E.usd[E.usd < 0].sum(); rew = E.usd[E.usd > 0].sum()
        k = E["événement"]
        say(f"\n=== {name} ===")
        say(f"  évals achetées {int((k == 'achat éval').sum())} ({fees:,.0f} $), validées {int((k == 'éval validée').sum())}, "
            f"ratées {int((k == 'éval ratée').sum())}, financés perdus {int((k == 'financé perdu').sum())}".replace(",", " "))
        say(f"  rewards {int((k == 'reward').sum())} pour {rew:,.0f} $ ; net {rew - fees:+,.0f} $".replace(",", " "))
        say("  en cours au " + str(NIGHT[-1]) + " : " + (", ".join(E[k.str.contains('en cours')]["événement"].tolist()) or "aucun"))
        m = E.assign(mois=pd.to_datetime(E.nuit).dt.to_period("M")).groupby("mois").usd.sum()
        say("  flux net par mois : " + " ; ".join(f"{p} {v:+,.0f} $".replace(",", " ") for p, v in m.items()))
        say("  journal :")
        for row in E.itertuples():
            say(f"    {row.nuit}  compte {row.compte:>2}  {row.événement}" + (f"  {row.usd:+,.0f} $".replace(",", " ") if row.usd else ""))


if __name__ == "__main__":
    main()
