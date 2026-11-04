"""Compte financé FTMO 1-Step avec mom : faut-il viser juste ce qui manque pour la règle des 50 %, puis attendre la date
du reward, plutôt que de trader normalement ? (demande du 2026-11-04). EXPLORATOIRE, hors compteur.

uv run python run_ftmo_payout_policy.py [N] → results/ftmo_payout_policy/ (run.log, septembre.csv, historique.csv)

Politiques du compte financé (risque 1 % par trade, objectif normal 2 R = TP 4 ATR M15) :
  « actuel »       : on trade chaque nuit ; reward dès qu'il est permis ;
  « cible »        : si le gain est > 0 et que seul le meilleur jour bloque (gain ≥ meilleur jour), le trade vise juste ce
                     qui manque (2 x meilleur jour - gain, + 0,01 %) au lieu de 2 R ; il l'atteint si le mouvement
                     favorable maximal du trade (MFE) le dépasse ;
  « attente »      : dès que le gain est > 0 et la règle respectée, on ne trade plus jusqu'à la date du reward ;
  « cible+attente » : les deux (proposition de l'utilisateur).
Règle du meilleur jour « Consistency » (comptes commandés depuis le 12/10/2026) : meilleur jour ≤ 50 % du gain net.
Reward : 90 % du gain, nouveau compte (perte max remise à zéro).
1. Rejeu réel de septembre (Databento + LSE, fenêtre déjà vue) : même éval que run_ftmo_septembre.py (2,5 %, objectif
   ramené au reste à faire), reward à partir du 14e jour calendaire après le 1er trade du compte, règles Consistency et
   Legacy (meilleur jour ≤ 50 % des seuls jours gagnants, comptes commandés avant le 12/10/2026).
2. Historique de mom, 2016-01 → 2026-08 et 2011-07 → 2015-12 (bibliothèque TP 4 ATR + MFE, build_mfe_mom.py) :
   20 000 comptes financés, départ au hasard, nuits consécutives ; le délai de 14 jours est compté comme 10 nuits de
   bourse (convention du moteur du n° 18) ; une nuit d'attente fait avancer l'horloge sans trade. EV par tentative
   avec l'éval mom à 2,5 % (objectif ramené au reste à faire, run_propfirm_trio.run_eval).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import run_ftmo_septembre as S
import run_propfirm_trio as T
from propfirm.ftmo import DAILY, EUR, MAXLOSS, MIN_RISK, PRICES_EUR, SPLIT, ev

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/ftmo_payout_policy")
SEED = 1830
COST = 1.5 / 25_684.0
R_FUND, TP_R, CYCLE = 1.0, 2.0, 10
POLITIQUES = ["actuel", "cible", "attente", "cible+attente"]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


# ----------------------------------------------------------------------------- 1. rejeu réel de septembre
def finance_reel(t: pd.DataFrame, debut: pd.Timestamp, politique: str, regle: str) -> dict:
    """Compte financé ouvert la nuit `debut`, rejoué jusqu'au 2026-11-03. Montants en % du capital."""
    t = t[t.night >= debut]
    P, hi, best, pos, f0, paid, n_rew, morts, journal = 0.0, 0.0, 0.0, 0.0, None, 0.0, 0, 0, []

    def regle_ok():
        return P > 0 and best <= 0.5 * (pos if regle == "legacy" else P) + 1e-9

    for d, R, s, mfe in zip(t.night, t.R, t.s, t.MFE_R):
        if f0 is not None and (d - f0).days >= 13 and regle_ok():  # reward demandé avant la nuit d
            paid += SPLIT * P
            n_rew += 1
            journal.append(dict(nuit=d, événement=f"reward {SPLIT * P:.2f} %", solde=P))
            P, hi, best, pos, f0 = 0.0, 0.0, 0.0, 0.0, None
        if "attente" in politique and f0 is not None and regle_ok():
            journal.append(dict(nuit=d, événement="attente", solde=P))
            continue
        floor = hi - MAXLOSS
        risk = min(R_FUND, P - floor)
        c = COST / s
        Rk = R
        need = (2 * best - (pos if regle == "legacy" else P)) + 0.01
        if "cible" in politique and P > 0 and not regle_ok() and need <= best + 1e-9:
            k = need * (1 + c) / risk + c
            if k < TP_R:
                Rk = k if mfe >= k else R
        pnl = risk * (Rk - c) / (1 + c) if risk >= MIN_RISK else 0.0
        P += pnl
        f0 = d if f0 is None else f0
        best, hi, pos = max(best, pnl), max(hi, P), pos + max(pnl, 0.0)
        journal.append(dict(nuit=d, événement=f"trade {Rk:+.2f} R", solde=P))
        if P <= floor + 1e-9 or pnl <= -DAILY:
            morts += 1
            journal.append(dict(nuit=d, événement="compte perdu", solde=P))
            break
    return dict(rewards_pct=paid, n_rewards=n_rew, solde_final=P, perdu=morts > 0, journal=journal)


# ----------------------------------------------------------------------------- 2. historique (Monte-Carlo)
def finance_mc(R, c, M, politique: str, n: int, rng, max_days: int = 1000):
    nd = len(R)
    P, hi, best = np.zeros(n), np.zeros(n), np.zeros(n)
    cyc, days, alive = np.zeros(n, int), np.zeros(n, int), np.ones(n, bool)
    paid, nrew, traded = np.zeros(n), np.zeros(n, int), np.zeros(n, int)
    start = rng.integers(0, nd, n)
    for _ in range(max_days):
        a = np.flatnonzero(alive)
        if not len(a):
            break
        floor = hi[a] - MAXLOSS
        risk = np.minimum(R_FUND, P[a] - floor)
        dead = risk < MIN_RISK
        alive[a[dead]] = False
        a, floor, risk = a[~dead], floor[~dead], risk[~dead]
        day = (start[a] + days[a]) % nd
        ok = (P[a] > 0) & (best[a] <= 0.5 * P[a] + 1e-9)
        wait = ok & ("attente" in politique)
        cj = c[day]
        Rk = R[day].copy()
        if "cible" in politique:
            need = 2 * best[a] - P[a] + 0.01
            k = need * (1 + cj) / risk + cj
            use = (P[a] > 0) & ~ok & (need <= best[a] + 1e-9) & (k < TP_R)
            Rk = np.where(use & (M[day] >= k), k, Rk)
        pnl = np.where(wait, 0.0, risk * (Rk - cj) / (1 + cj))
        traded[a] += ~wait
        days[a] += 1
        cyc[a] += 1
        P[a] += pnl
        fail = (P[a] <= floor + 1e-9) | (pnl <= -DAILY)
        alive[a[fail]] = False
        best[a] = np.maximum(best[a], pnl)
        hi[a] = np.maximum(hi[a], P[a])
        pay = ~fail & (cyc[a] >= CYCLE) & (P[a] > 0) & (best[a] <= 0.5 * P[a] + 1e-9)
        b = a[pay]
        paid[b] += SPLIT * P[b]
        nrew[b] += 1
        hi[b], P[b], best[b], cyc[b] = 0.0, 0.0, 0.0, 0
    return paid, nrew, days, traded


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    say(f"Compte financé FTMO 1-Step avec mom : 4 politiques ; {N} comptes pour l'historique, graine {SEED}")

    # 1. septembre réel
    t = S.trades()
    rows = []
    for regle in ("consistency", "legacy"):
        for d in sorted(t.night[(t.night >= "2026-09-01") & (t.night <= "2026-09-30")]):
            _, e = S.rejoue(t, d, True, regle)
            valid = [x for x in e["events"] if "validée" in x]
            if not valid:
                continue
            jour = pd.Timestamp(f"2026-{valid[0][3:5]}-{valid[0][:2]}")
            f_start = t.night[t.night > jour].min()
            for pol in POLITIQUES:
                r = finance_reel(t, f_start, pol, regle)
                rows.append(dict(règle=regle, départ=d.strftime("%d/%m"), validée=jour.strftime("%d/%m"),
                                 politique=pol, rewards=r["n_rewards"], rewards_pct=r["rewards_pct"],
                                 solde_au_0311=r["solde_final"], perdu=r["perdu"]))
                if d == pd.Timestamp("2026-09-01"):
                    say(f"\n[{regle}] départ 01/09, financé dès le {f_start:%d/%m}, politique « {pol} » :")
                    for j in r["journal"]:
                        if j["événement"] != "attente" or True:
                            say(f"  {j['nuit']:%d/%m} {j['événement']:<14} solde {j['solde']:+.2f} %")
    Rr = pd.DataFrame(rows)
    Rr.to_csv(OUT / "septembre.csv", index=False)
    say("\nSeptembre réel, départs qui ont validé leur éval (rewards en % du capital au 03/11) :")
    say(Rr.pivot_table(index=["règle", "départ"], columns="politique", values="rewards_pct", sort=False)[POLITIQUES]
        .round(2).to_string())

    # 2. historique
    lib = T.bibliotheque()
    rng = np.random.default_rng(SEED)
    rows = []
    for p, (a, z) in {"2016-01 → 2026-08": ("2016-01-01", "2026-08-28"),
                      "2011-07 → 2015-12": ("2011-07-01", "2015-12-31")}.items():
        m = lib[(lib.strat == "mom") & (lib.date >= a) & (lib.date <= z)].sort_values("date")
        R, cc, M = m.R_brut.to_numpy(), (COST / m.s).to_numpy(), m.MFE_R.to_numpy()
        f = len(m) / ((pd.Timestamp(z) - pd.Timestamp(a)).days / 365.25)
        J = T.plan(m, "mom seul")
        arr = {c_: J[c_].to_numpy(float) for c_ in ("R1", "w1", "c1", "M1", "R2", "w2", "c2", "M2")}
        ok, d = T.run_eval(arr, T.R_EVAL, N, rng)
        pp, m_t = ok.mean(), d.mean() / f * 12
        for pol in POLITIQUES:
            paid, nr, life, traded = finance_mc(R, cc, M, pol, N, rng)
            row = dict(période=p, politique=pol, passage_eval=pp, valeur_financé=paid.mean(), p_reward=(nr > 0).mean(),
                       rewards=nr.mean(), reward_moyen=paid.sum() / max(nr.sum(), 1), vie_mois=life.mean() / f * 12,
                       nuits_tradées_pct=100 * traded.sum() / life.sum())
            for size in (10_000, 100_000):
                x, ci = ev(pp, np.sqrt(pp * (1 - pp) / N), paid.mean(), paid.std() / np.sqrt(N), size)
                row[f"EV {size // 1000}k"] = x
                row[f"EV/mois {size // 1000}k"] = x / (m_t + pp * row["vie_mois"])
            rows.append(row)
    H = pd.DataFrame(rows)
    H.to_csv(OUT / "historique.csv", index=False)
    say(f"\nHistorique de mom (éval 2,5 % puis financé 1 %, {N} comptes) :\n{H.round(3).to_string(index=False)}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
