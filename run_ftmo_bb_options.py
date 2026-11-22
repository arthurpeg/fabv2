"""FTMO 1-Step : ajouter BB (bande de bruit) au plan retenu. Option 1 : compte A = mom + BB l'après-midi (règles du
compte B) ; option 2 : troisième compte C = BB seul. Comparé au plan actuel (A = mom, B = 3n + M2 EMA 9:30).
EXPLORATOIRE, hors compteur (simulation de contrat sur des trades existants ; BB n'est pas validé hors échantillon,
voir PREREGISTRATION_32). Demande de l'utilisateur (2026-11-22). Le bot n'est pas modifié.

uv run python run_ftmo_bb_options.py → results/ftmo_bb_options/ (run.log, departs.csv, bb_trades.csv)

Moteur : run_ftmo_deux_comptes.py (Compte, jambes_A, jambes_B), règle des annonces et politique « cible + attente »
(plan retenu) ; éval 2,5 %, financé 1 %, objectif 2 R, objectif d'éval ramené au reste à faire (MFE), coût CFD 1,5 pt.
BB : version prop firm du n° 32 (VWAP exigé à l'entrée, mode A = stop suiveur gardé, SL 0,25 × ATR14, TP 2R, premier
trade de la séance), recalculée ici avec son MFE (run_bb_sltp.simulate, même code).
Option 1 (compte A) : si mom touche son SL ou son TP la nuit, pas de BB ; sinon (sortie à 9:30 ou pas de mom), BB avec
une taille rho = min(r + x, (2 r − x) / 2), x = résultat net de mom, pour garder la journée entre −r et +2 r (règle du
compte B). Mom sort au plus tard à 9:30, BB n'entre pas avant 10:00 : pas de chevauchement.
Option 2 (compte C) : BB seul, mêmes réglages.
Anti-hedging (FTMO) : pas de BB un jour où le M2 du compte B est de sens opposé (règle conservatrice : dès que le M2 a
un signal opposé, même si B ne le trade pas). Annonces en financé : pas de BB les jours de décision ou de minutes de la
Fed (annonce à 14:00, BB serait ouvert).
Période : trades jusqu'au 2026-08-28 seulement (la fenêtre 2026-08-29 → 11-03 est exclue pour BB par le n° 32) ;
départs tous les 5 jours de bourse de 2016-01 à 2025-08, 12 mois de trading.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_deux_comptes as D
from run_bb_sltp import prepare, simulate

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/ftmo_bb_options")
K, RR = 0.25, 2
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def trades_bb() -> pd.DataFrame:
    P = prepare()
    g, atr = P[1], P[8]
    t = simulate(P, "A", K, RR).sort_values(["date", "m_in"]).groupby("date", as_index=False).first()
    t["date"] = pd.to_datetime(t.date)
    dist = K * atr.reindex(t.date).values
    mfe = np.zeros(len(t))
    for i, r in enumerate(t.itertuples()):
        last = int(r.m_out) - (2 if r.sortie == "SL" else 1)  # minute du SL exclue (ordre haut / bas inconnu)
        cols = list(range(int(r.m_in), last + 1))
        if cols:
            h, lo = g.H.loc[r.date, cols].max(), g.L.loc[r.date, cols].min()
            mfe[i] = max(0.0, ((h - r.p_in) if r.dir == 1 else (r.p_in - lo)) / dist[i])
    out = pd.DataFrame({"date": t.date, "R": t.dir * (t.p_out - t.p_in) / dist, "s": dist / t.p_in, "MFE": mfe,
                        "dir": t.dir, "sortie": t.sortie})
    return out[np.isfinite(out.R) & (out.s > 0)]


def jours_bb(lib: pd.DataFrame, bb: pd.DataFrame) -> list[tuple[pd.Timestamp, dict]]:
    m2 = pd.read_csv("results/propfirm_combo/trades_tp2.csv", parse_dates=["date"])
    m2_dir = m2[m2.strat == "M2"].set_index("date").side
    cal = pd.read_csv("config/calendrier_macro_us.csv")
    fed = set(pd.to_datetime(cal[cal.annonce.str.startswith("FOMC")].date))
    jours = D.tableau(lib)
    bbi = bb.set_index("date")
    out, conflits = [], 0
    for d, row in jours:
        if d in bbi.index:
            x = bbi.loc[d]
            opp = d in m2_dir.index and int(np.sign(m2_dir.loc[d])) == -int(x.dir)
            conflits += int(opp)
            if not opp:
                row["BB"] = (float(x.R), D.COST / float(x.s), float(x.MFE), float(x.R), float(x.MFE))
                row["BB_fed"] = d in fed
        out.append((d, row))
    say(f"BB : {len(bb)} trades ; {conflits} jours retirés pour l'anti-hedging (M2 du compte B de sens opposé)")
    return out


def _bb_leg(row, rho, r):
    if "BB" not in row or rho <= 0:
        return []
    if r == D.R_FUND and row.get("BB_fed"):
        return []  # financé : pas de BB un jour de Fed (règle des annonces)
    return [(*row["BB"], rho)]


def jambes_A_bb(row):
    def f(base, r):
        out, x = [], 0.0
        mom = row.get("mom")
        if mom is not None:
            out.append((*mom, base))
            if not (-0.999 < mom[0] < D.TP_R - 1e-3):  # mom a touché son SL ou son TP : pas de BB
                return out
            x = base * (mom[0] - mom[1]) / (1 + mom[1])
        return out + _bb_leg(row, max(0.0, min(base + x, (2 * base - x) / 2)), r)
    return f


def jambes_C(row):
    def f(base, r):
        return _bb_leg(row, base, r)
    return f


def simule(jours, i0, n, option):
    A = D.Compte("A", False, True, "cible+attente")
    B = D.Compte("B", False, True, "cible+attente")
    C = D.Compte("C", False, True, "cible+attente") if option == 2 else None
    tot = []
    for d, row in jours[i0:i0 + n]:
        A.jour(d, jambes_A_bb(row) if option == 1 else D.jambes_A(row))
        B.jour(d, D.jambes_B(row))
        if C is not None:
            C.jour(d, jambes_C(row))
        tot.append(A.cash + B.cash + (C.cash if C else 0.0))
    return A, B, C, np.array(tot)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    bb = trades_bb()
    bb.to_csv(OUT / "bb_trades.csv", index=False)
    say(f"BB (mode A, SL {K} ATR, TP {RR}R, un trade par jour) : R brut moyen {bb.R.mean():+.3f}, MFE médian {bb.MFE.median():.2f} R")
    lib = D.bibliotheque()
    lib = lib[lib.date <= "2026-08-28"]
    jours = jours_bb(lib, bb)
    dates = pd.DatetimeIndex([d for d, _ in jours])
    H = 252
    i_start = int(np.searchsorted(dates, pd.Timestamp("2016-01-04")))
    i_end = int(np.searchsorted(dates, pd.Timestamp("2026-08-29")))
    rows = []
    for option, nom in [(0, "plan actuel (A mom, B 3n + M2)"), (1, "option 1 : A = mom + BB"), (2, "option 2 : + compte C = BB")]:
        for i0 in range(i_start, i_end - H, 5):
            A, B, C, tot = simule(jours, i0, H, option)
            rows.append(dict(option=nom, départ=dates[i0].date(), net_A=A.cash, net_B=B.cash, net_C=C.cash if C else 0.0,
                             net_total=tot[-1], évals_A=A.evals, évals_C=C.evals if C else 0, rewards_A=A.rewards,
                             rewards_B=B.rewards, rewards_C=C.rewards if C else 0, creux=min(0.0, tot.min())))
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "departs.csv", index=False)
    say(f"\n{R.départ.nunique()} départs (2016-01 → 2025-08), 12 mois, comptes 10k, règle des annonces + cible + attente :")
    for nom, g in R.groupby("option", sort=False):
        q = lambda s: f"moy. {s.mean():+,.0f} $, méd. {s.median():+,.0f} $, 10e c. {s.quantile(0.1):+,.0f} $"
        say(f"\n  {nom}")
        say(f"    total : {q(g.net_total)} ; P(< 0) {100 * (g.net_total < 0).mean():.1f} % ; pire creux de trésorerie "
            f"médiane {g.creux.median():,.0f} $, pire {g.creux.min():,.0f} $")
        say(f"    A : {q(g.net_A)} ; évals/an {g.évals_A.mean():.1f} ; rewards/an {g.rewards_A.mean():.1f}")
        say(f"    B : {q(g.net_B)} ; rewards/an {g.rewards_B.mean():.1f}")
        if g.net_C.abs().sum() > 0:
            say(f"    C : {q(g.net_C)} ; évals/an {g.évals_C.mean():.1f} ; rewards/an {g.rewards_C.mean():.1f}")
    par = R.assign(année=pd.to_datetime(R.départ).dt.year).pivot_table(index="année", columns="option", values="net_total",
                                                                        aggfunc="mean").round(0)
    say(f"\nNet total moyen sur 12 mois selon l'année de départ ($) :\n{par.to_string()}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
