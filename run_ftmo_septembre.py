"""Et si on avait commencé FTMO 1-Step avec mom en septembre 2026 ? Rejeu jour par jour sur les vraies nuits jusqu'au
2026-11-03 (demande du 2026-11-04). DESCRIPTIF, hors compteur.

uv run python run_ftmo_septembre.py → results/ftmo_septembre/ (run.log, journal_0109[_reste].csv, departs[_reste].csv,
trades_mom_tp4.csv)

Données : fenêtre déjà vue du holdout (avenant A du n° 26), série Databento + LSE raboutée
(cache/holdout_anticipe/ajuste/) ; rien à partir du 2026-11-04. Trades : mom (compte 20:00, momentum 12-1, SL 2 ATR)
avec l'objectif du plan FTMO, TP 4 ATR M15 = 2 R, recalculés avec vectorbt (run_holdout_anticipe.h1_mom, R brut).
MFE_R : mouvement favorable maximal du trade avant sa sortie, en R, barre du stop exclue (on ne sait pas si le haut
est venu avant le bas dans cette minute).
Règles (moteur du n° 18, propfirm/ftmo.py, une nuit = une journée FTMO) : éval 2,5 % risqués par trade, objectif
+10 %, perte max 10 % sous le plus haut, perte du jour 3 %, meilleur jour ≤ 50 % du gain ; financé 1 % par trade,
reward tous les 10 jours si gain > 0 et meilleur jour ≤ 50 %, 90 % versés, perte max remise à zéro. Coût CFD 1,5 point
au niveau actuel : gain d'un trade = risque x (R - c) / (1 + c), c = coût en R (le stop coût compris vaut le risque).
Deux variantes de l'éval : objectif fixe à 2 R (comme les simulations à bibliothèque de trades), ou objectif ramené au
reste à faire (cible +10 % et règle du meilleur jour) quand il est sous 2 R, comme le moteur du n° 18 en mode « jours ».
Une éval ratée est rachetée la nuit suivante ; une éval réussie donne le compte financé la nuit suivante (en réalité
FTMO met 1 à 3 jours ouvrés). Prix : 79 € (10k), 499 € (100k), 1 € = 1,10 $.
"""

from __future__ import annotations

import sys
from pathlib import Path

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


def rejoue(t: pd.DataFrame, debut: pd.Timestamp, reste: bool = False, regle: str = "simulateur") -> tuple[pd.DataFrame, dict]:
    """Journal nuit par nuit à partir de `debut` ; montants en % du capital.

    `regle` (règle du meilleur jour et moment du reward) :
      « simulateur »  : meilleur jour ≤ 50 % du gain net ; reward tous les 10 jours tradés (moteur du n° 18) ;
      « consistency » : FTMO, comptes commandés depuis le 12/10/2026 : meilleur jour ≤ 50 % du gain net (somme des
                        jours gagnants et perdants) ; reward possible le 14e jour (calendaire) après le 1er trade du compte ;
      « legacy »      : FTMO, comptes commandés avant le 12/10/2026 : meilleur jour ≤ 50 % de la somme des jours
                        gagnants seulement ; reward possible le 14e jour après le 1er trade.
    Avec les règles FTMO, le reward est demandé dès qu'il est possible (gain > 0, meilleur jour respecté) ; un nouveau
    compte repart alors à zéro (perte max remise à zéro). La même règle du meilleur jour vaut pour valider l'éval."""
    t = t[t.night >= debut]
    phase, P, hi, best, pos, cyc, n_eval, paid, f0 = "éval", 0.0, 0.0, 0.0, 0.0, 0, 1, 0.0, None
    rows, events = [], [f"{debut:%d/%m} : achat de l'éval n° 1"]

    def meilleur_ok(P, best, pos):
        return best <= 0.5 * (pos if regle == "legacy" else P) + 1e-9

    for d, R, s, mfe in zip(t.night, t.R, t.s, t.MFE_R):
        r = R_EVAL if phase == "éval" else R_FUND
        floor = hi - MAXLOSS
        risk = min(r, P - floor)
        c = COST / s
        objectif = 2.0
        if reste and phase == "éval" and risk >= MIN_RISK:
            need_best = (2 * best - pos) if regle == "legacy" else (2 * best - P)
            need = max(TARGET - P, need_best, 0.01)
            k = need * (1 + c) / risk + c  # objectif en R qui rapporte exactement `need` net du coût
            if k < 2.0:
                objectif = k
                if mfe >= k:
                    R = k
        pnl = risk * (R - c) / (1 + c) if risk >= MIN_RISK else 0.0
        P += pnl
        if f0 is None:
            f0 = d
        fail = P <= floor + 1e-9 or pnl <= -DAILY
        best, hi, pos = max(best, pnl), max(hi, P), pos + max(pnl, 0.0)
        rows.append(dict(nuit=d, phase=phase, objectif_R=objectif, MFE_R=mfe, R=R, risque=risk, pnl=pnl, solde=P,
                         meilleur_jour=best, somme_jours_gagnants=pos, plancher=hi - MAXLOSS))
        if fail:
            events.append(f"{d:%d/%m} : {phase} perdu ({P:+.2f} %)")
            phase, P, hi, best, pos, cyc, f0 = "éval", 0.0, 0.0, 0.0, 0.0, 0, None
            n_eval += 1
            events.append(f"{d:%d/%m} : achat de l'éval n° {n_eval}")
            continue
        if phase == "éval" and P >= TARGET - 1e-9 and meilleur_ok(P, best, pos):
            events.append(f"{d:%d/%m} : éval n° {n_eval} validée ({P:+.2f} %) → compte financé")
            phase, P, hi, best, pos, cyc, f0 = "financé", 0.0, 0.0, 0.0, 0.0, 0, None
            continue
        if phase == "financé":
            cyc += 1
            date_ok = cyc >= CYCLE if regle == "simulateur" else (d - f0).days >= 13
            if date_ok and P > 0 and meilleur_ok(P, best, pos):
                paid += SPLIT * P
                events.append(f"{d:%d/%m} : reward de {SPLIT * P:.2f} % du capital (solde {P:+.2f} %)")
                P, hi, best, pos, cyc, f0 = 0.0, 0.0, 0.0, 0.0, 0, None
    fin = dict(évals=n_eval, phase_finale=phase, solde_final=P, rewards_pct=paid, events=events)
    return pd.DataFrame(rows), fin


def trades() -> pd.DataFrame:
    import recolte1.engine as eng
    T = H.h1_mom(Path("cache/holdout_anticipe/ajuste/indices/NQ_v0_1m.parquet"), tp=4.0, cost="gross")
    df = eng.load("NQ")  # même série ajustée que h1_mom (eng.DATA fixé par h1_mom)
    hi, lo, cl = df.high.values, df.low.values, df.close.values
    mfe = []
    for e, x, d, s, why in zip(T.entry_idx, T.exit_idx, T.dir, T.s, T.reason):
        last = x - 1 if why == "SL" else x
        m = (hi[e + 1:last + 1].max() - cl[e]) if d > 0 else (cl[e] - lo[e + 1:last + 1].min())
        mfe.append(m / (s * cl[e]) if last > e else 0.0)
    T["MFE_R"] = mfe
    return T.assign(night=pd.to_datetime(T.night))[["night", "dir", "reason", "R", "s", "MFE_R"]].sort_values("night")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    T = trades()
    say(f"mom TP 4 ATR (2 R), R brut : {len(T)} nuits du {T.night.min():%d/%m/%Y} au {T.night.max():%d/%m/%Y}, "
        f"{(T.reason == 'TP').sum()} TP, {(T.reason == 'SL').sum()} SL, R brut total {T.R.sum():+.2f}")
    T.to_csv(OUT / "trades_mom_tp4.csv", index=False)
    for reste, regle in ((False, "simulateur"), (True, "simulateur"), (True, "consistency"), (True, "legacy")):
        suffixe = ("_reste" if reste else "") + ("" if regle == "simulateur" else f"_{regle}")
        say(f"\n===== Éval avec objectif {'ramené au reste à faire' if reste else 'fixe à 2 R'}, règle « {regle} » =====")
        j, fin = rejoue(T, pd.Timestamp("2026-09-01"), reste, regle)
        j.to_csv(OUT / f"journal_0109{suffixe}.csv", index=False)
        say("Départ le 1er septembre (nuit du 31/08 au 01/09) :")
        for e in fin["events"]:
            say(f"  {e}")
        say(f"  au 03/11 : {fin['phase_finale']} en cours, solde {fin['solde_final']:+.2f} % ; rewards "
            f"{fin['rewards_pct']:.2f} % ; évals achetées {fin['évals']}")
        for size in (10_000, 100_000):
            fee = PRICES_EUR[size] * EUR
            say(f"  {size // 1000}k : frais {fin['évals'] * fee:,.0f} $, rewards {fin['rewards_pct'] / 100 * size:,.0f} $, "
                f"net encaissé {fin['rewards_pct'] / 100 * size - fin['évals'] * fee:+,.0f} $ ; gain latent du compte "
                f"en cours {fin['solde_final'] / 100 * size:+,.0f} $ (non versé)")
        rows = []
        for d in sorted(T.night[(T.night >= "2026-09-01") & (T.night <= "2026-09-30")]):
            _, f = rejoue(T, d, reste, regle)
            valid = [e for e in f["events"] if "validée" in e]
            rows.append(dict(départ=d.strftime("%d/%m"), évals=f["évals"], validée_le=valid[0][:5] if valid else "",
                             rewards=sum("reward" in e for e in f["events"]), phase_au_0311=f["phase_finale"],
                             solde_pct=f["solde_final"], rewards_pct=f["rewards_pct"],
                             **{f"net {k // 1000}k": f["rewards_pct"] / 100 * k - f["évals"] * PRICES_EUR[k] * EUR
                                for k in (10_000, 100_000)}))
        D = pd.DataFrame(rows)
        D.to_csv(OUT / f"departs{suffixe}.csv", index=False)
        say(f"\nChaque jour de départ possible en septembre :\n{D.round(2).to_string(index=False)}")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
