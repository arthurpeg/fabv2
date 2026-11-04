"""Et si on avait commencé FTMO 1-Step avec mom en septembre 2026 ? Rejeu jour par jour sur les vraies nuits jusqu'au
2026-11-03 (demande du 2026-11-04). DESCRIPTIF, hors compteur.

uv run python run_ftmo_septembre.py → results/ftmo_septembre/ (run.log, journal_<départ>.csv, departs.csv)

Données : fenêtre déjà vue du holdout (avenant A du n° 26), série Databento + LSE raboutée
(cache/holdout_anticipe/ajuste/) ; rien à partir du 2026-11-04. Trades : mom (compte 20:00, momentum 12-1, SL 2 ATR)
avec l'objectif du plan FTMO, TP 4 ATR M15 = 2 R, recalculés avec vectorbt (run_holdout_anticipe.h1_mom, R brut).
Règles (moteur du n° 18, propfirm/ftmo.py, une nuit = une journée FTMO) : éval 2,5 % risqués par trade, objectif
+10 %, perte max 10 % sous le plus haut, perte du jour 3 %, meilleur jour ≤ 50 % du gain ; financé 1 % par trade,
reward tous les 10 jours si gain > 0 et meilleur jour ≤ 50 %, 90 % versés, perte max remise à zéro. Coût CFD 1,5 point
au niveau actuel. Une éval ratée est rachetée la nuit suivante ; une éval réussie donne le compte financé la nuit
suivante (en réalité FTMO met 1 à 3 jours ouvrés). Prix : 79 € (10k), 499 € (100k), 1 € = 1,10 $.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_holdout_anticipe as H
from propfirm.ftmo import DAILY, EUR, MAXLOSS, MIN_RISK, PRICES_EUR, SPLIT, TARGET

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/ftmo_septembre")
COST = 1.5 / 25_684.0
R_EVAL, R_FUND, CYCLE = 2.5, 1.0, 10
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def rejoue(t: pd.DataFrame, debut: pd.Timestamp) -> tuple[pd.DataFrame, dict]:
    """Journal nuit par nuit à partir de `debut` ; montants en % du capital."""
    t = t[t.night >= debut]
    phase, P, hi, best, cyc, n_eval, paid = "éval", 0.0, 0.0, 0.0, 0, 1, 0.0
    rows, events = [], [f"{debut:%d/%m} : achat de l'éval n° 1"]
    for d, R, s in zip(t.night, t.R, t.s):
        r = R_EVAL if phase == "éval" else R_FUND
        floor = hi - MAXLOSS
        risk = min(r, P - floor)
        c = COST / s
        pnl = risk * (R - c) / (1 + c) if risk >= MIN_RISK else 0.0
        P += pnl
        fail = P <= floor + 1e-9 or pnl <= -DAILY
        best, hi = max(best, pnl), max(hi, P)
        rows.append(dict(nuit=d, phase=phase, R=R, risque=risk, pnl=pnl, solde=P))
        if fail:
            events.append(f"{d:%d/%m} : {phase} perdu ({P:+.2f} %)")
            phase, P, hi, best, cyc = "éval", 0.0, 0.0, 0.0, 0
            n_eval += 1
            events.append(f"{d:%d/%m} : achat de l'éval n° {n_eval}")
            continue
        if phase == "éval" and P >= TARGET - 1e-9 and best <= 0.5 * P + 1e-9:
            events.append(f"{d:%d/%m} : éval n° {n_eval} validée ({P:+.2f} %) → compte financé")
            phase, P, hi, best, cyc = "financé", 0.0, 0.0, 0.0, 0
            continue
        if phase == "financé":
            cyc += 1
            if cyc >= CYCLE and P > 0 and best <= 0.5 * P + 1e-9:
                paid += SPLIT * P
                events.append(f"{d:%d/%m} : reward de {SPLIT * P:.2f} % du capital")
                P, hi, best, cyc = 0.0, 0.0, 0.0, 0
    fin = dict(évals=n_eval, phase_finale=phase, solde_final=P, rewards_pct=paid, events=events)
    return pd.DataFrame(rows), fin


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    T = H.h1_mom(Path("cache/holdout_anticipe/ajuste/indices/NQ_v0_1m.parquet"), tp=4.0, cost="gross")
    T = T.assign(night=pd.to_datetime(T.night))[["night", "dir", "reason", "R", "s"]].sort_values("night")
    say(f"mom TP 4 ATR (2 R), R brut : {len(T)} nuits du {T.night.min():%d/%m/%Y} au {T.night.max():%d/%m/%Y}, "
        f"{(T.reason == 'TP').sum()} TP, {(T.reason == 'SL').sum()} SL, R brut total {T.R.sum():+.2f}")
    T.to_csv(OUT / "trades_mom_tp4.csv", index=False)

    j, fin = rejoue(T, pd.Timestamp("2026-09-01"))
    j.to_csv(OUT / "journal_0109.csv", index=False)
    say("\nDépart le 1er septembre (nuit du 31/08 au 01/09) :")
    for e in fin["events"]:
        say(f"  {e}")
    say(f"  au 03/11 : {fin['phase_finale']} en cours, solde {fin['solde_final']:+.2f} % ; rewards {fin['rewards_pct']:.2f} % ; "
        f"évals achetées {fin['évals']}")
    for size in (10_000, 100_000):
        fee = PRICES_EUR[size] * EUR
        say(f"  {size // 1000}k : frais {fin['évals'] * fee:,.0f} $, rewards {fin['rewards_pct'] / 100 * size:,.0f} $, "
            f"net encaissé {fin['rewards_pct'] / 100 * size - fin['évals'] * fee:+,.0f} $ ; gain latent du compte en cours "
            f"{fin['solde_final'] / 100 * size:+,.0f} $ (non versé)")

    rows = []
    for d in sorted(T.night[(T.night >= "2026-09-01") & (T.night <= "2026-09-30")]):
        _, f = rejoue(T, d)
        rows.append(dict(départ=d.date(), évals=f["évals"], phase_au_0311=f["phase_finale"],
                         solde_pct=f["solde_final"], rewards_pct=f["rewards_pct"],
                         **{f"net {k // 1000}k": f["rewards_pct"] / 100 * k - f["évals"] * PRICES_EUR[k] * EUR
                            for k in (10_000, 100_000)}))
    D = pd.DataFrame(rows)
    D.to_csv(OUT / "departs.csv", index=False)
    say(f"\nChaque jour de départ possible en septembre :\n{D.round(2).to_string(index=False)}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
