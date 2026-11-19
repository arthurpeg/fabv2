"""Deux comptes FTMO 1-Step 10k tradés en même temps sur tout l'historique, du 2011-07-01 au 2026-11-03 (demande du
2026-11-04) : A = mom, B = 3n + M2, règle des annonces respectée, politique « cible + attente » en financé.
EXPLORATOIRE, hors compteur.

uv run python run_ftmo_deux_comptes_historique.py → results/ftmo_deux_comptes_historique/ (run.log, jours.csv,
evenements.csv, mois.csv)

Règles, trades et moteur : run_ftmo_deux_comptes.py (Compte, jambes_A, jambes_B), sans changement ; reward au 14e jour
calendaire après le 1er trade du compte. Un seul chemin : les deux emplacements sont ouverts le 2011-07-01 et rachetés après
chaque échec. Mesures :
  - corrélation des deux comptes : P&L journalier de trading (% du capital, jours où les deux comptes tradent) et flux
    de trésorerie mensuels (rewards - frais) ;
  - max DD de trésorerie : plus grande baisse du cumul (rewards - frais) depuis un plus haut, et sa durée ;
  - séries sans reward : plus grand nombre d'évals achetées entre deux rewards d'un même compte (ou depuis le début),
    leur coût et leur durée ; plus longue période sans aucun reward pour la paire.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as M

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/ftmo_deux_comptes_historique")
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def dd(x: pd.Series) -> tuple[float, pd.Timestamp, pd.Timestamp, pd.Timestamp | None]:
    """(profondeur, date du plus haut, date du creux, date de retour au plus haut ou None)."""
    pic = x.cummax()
    creux = (x - pic).idxmin()
    haut = x[:creux].idxmax()
    retour = x[creux:][x[creux:] >= x[haut]]
    return float((x - pic).min()), haut, creux, (retour.index[0] if len(retour) else None)


def series(ev: pd.DataFrame, compte: str, debut: pd.Timestamp) -> pd.DataFrame:
    """Une ligne par intervalle entre deux rewards : évals achetées, coût, durée."""
    e = ev[ev.compte == compte]
    rows, n, t0 = [], 1, debut  # l'éval de départ compte
    for d, kind in zip(e.date, e.type):
        if kind == "échec":
            n += 1
        elif kind == "reward":
            rows.append(dict(compte=compte, début=t0, fin=d, évals=n, coût=n * M.FEE, jours=(d - t0).days))
            n, t0 = 0, d
    rows.append(dict(compte=compte, début=t0, fin=None, évals=n, coût=n * M.FEE, jours=None))
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lib = M.bibliotheque()
    jours = M.tableau(lib)
    A = M.Compte("A mom", True, True, "cible+attente")
    B = M.Compte("B 3n + M2", True, True, "cible+attente")
    rows = []
    for d, row in jours:
        pa, pb = A.jour(d, M.jambes_A(row)), B.jour(d, M.jambes_B(row))
        rows.append(dict(date=d, pnl_A=pa, pnl_B=pb, cash_A=A.cash, cash_B=B.cash, phase_A=A.phase, phase_B=B.phase))
    J = pd.DataFrame(rows).set_index("date")
    J["cash"] = J.cash_A + J.cash_B
    J.to_csv(OUT / "jours.csv")
    ev = []
    for C in (A, B):
        for d, e in C.events:
            ev.append(dict(compte=C.nom[0], date=d, type="reward" if e.startswith("reward") else
                           ("échec" if "perdu" in e else "validée"), détail=e))
    ev = pd.DataFrame(ev).sort_values("date")
    ev.to_csv(OUT / "evenements.csv", index=False)
    d0, d1 = J.index[0], J.index[-1]
    ans = (d1 - d0).days / 365.25
    say(f"Deux comptes 10k, {d0:%Y-%m-%d} → {d1:%Y-%m-%d} ({ans:.1f} ans), règle des annonces, cible + attente")

    for C in (A, B):
        e = ev[ev.compte == C.nom[0]]
        say(f"  {C.nom} : {C.evals} évals achetées ({C.evals * M.FEE:,.0f} $), {int((e.type == 'validée').sum())} validées, "
            f"{C.rewards} rewards, net {C.cash:+,.0f} $ ({C.cash / ans:+,.0f} $/an)")
    say(f"  total : {J.cash.iloc[-1]:+,.0f} $ ({J.cash.iloc[-1] / ans:+,.0f} $/an)")

    # corrélations
    both = J[["pnl_A", "pnl_B"]].dropna()
    both = both[(both.pnl_A != 0) & (both.pnl_B != 0)]
    mois = J[["cash_A", "cash_B", "cash"]].resample("ME").last().diff().fillna(J[["cash_A", "cash_B", "cash"]]
                                                                           .resample("ME").last().iloc[[0]])
    mois.columns = ["flux_A", "flux_B", "flux_total"]
    mois.to_csv(OUT / "mois.csv")
    say(f"\nCorrélation : P&L journalier de trading A / B {both.pnl_A.corr(both.pnl_B):+.3f} ({len(both)} jours où les deux "
        f"tradent) ; flux de trésorerie mensuels A / B {mois.flux_A.corr(mois.flux_B):+.3f} ; "
        f"mois négatifs : A {100 * (mois.flux_A < 0).mean():.0f} %, B {100 * (mois.flux_B < 0).mean():.0f} %, "
        f"total {100 * (mois.flux_total < 0).mean():.0f} % ; mois négatifs en même temps pour A et B "
        f"{100 * ((mois.flux_A < 0) & (mois.flux_B < 0)).mean():.0f} %")

    # max DD de trésorerie
    say("\nMax DD de trésorerie (cumul rewards - frais, depuis un plus haut) :")
    for k, col in (("A", "cash_A"), ("B", "cash_B"), ("total", "cash")):
        p, h, c, r = dd(J[col])
        say(f"  {k:<5} : {p:,.0f} $ ; du {h:%Y-%m-%d} au {c:%Y-%m-%d} ; retour au plus haut "
            f"{'le ' + f'{r:%Y-%m-%d}' + f' ({(r - h).days} jours)' if r is not None else 'pas encore'}")

    # séries sans reward
    say("\nSéries sans reward (évals achetées entre deux rewards d'un même compte) :")
    S = pd.concat([series(ev, k, d0) for k in ("A", "B")], ignore_index=True)
    S.to_csv(OUT / "series_sans_reward.csv", index=False)
    for k in ("A", "B"):
        s = S[S.compte == k]
        w = s.loc[s.évals.idxmax()]
        lj = s.dropna(subset=["jours"])
        wl = lj.loc[lj.jours.idxmax()]
        dist = s.évals.value_counts().sort_index()
        say(f"  {k} : pire série {int(w.évals)} évals ({w.coût:,.0f} $), du {w.début:%Y-%m-%d} au "
            f"{'%s' % (f'{w.fin:%Y-%m-%d}' if pd.notna(w.fin) else 'aujourd’hui')} ; plus longue attente d'un reward "
            f"{int(wl.jours)} jours (du {wl.début:%Y-%m-%d} au {wl.fin:%Y-%m-%d}, {int(wl.évals)} évals) ; "
            f"répartition (évals entre deux rewards : nombre de fois) {dict(dist)}")
    rw = ev[ev.type == "reward"].date.drop_duplicates().sort_values()
    gaps = rw.diff().dt.days
    i = gaps.idxmax()
    say(f"  la paire : plus longue période sans aucun reward (A ni B) : {int(gaps.max())} jours, "
        f"du {rw.loc[rw.index[rw.index.get_loc(i) - 1]]:%Y-%m-%d} au {rw.loc[i]:%Y-%m-%d}")

    an = J[["cash_A", "cash_B", "cash"]].resample("YE").last().diff()
    an.iloc[0] = J[["cash_A", "cash_B", "cash"]].resample("YE").last().iloc[0]
    an.index = an.index.year
    say(f"\nNet par année civile ($) :\n{an.round(0).to_string()}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
