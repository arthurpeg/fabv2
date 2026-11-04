"""Contrôle du moteur FTMO Python par vectorbt (demande du 2026-11-04) : le compte A (mom) du chemin historique
(run_ftmo_deux_comptes_historique.py : règle des annonces, cible + attente, objectif d'éval ramené au reste à faire) est
rejoué dans vectorbt avec, pour chaque trade, la taille, le stop, l'objectif et la sortie décidés par le moteur.
EXPLORATOIRE, hors compteur.

uv run python run_ftmo_verif_vbt.py → results/ftmo_verif_vbt/ (run.log, trades.csv)

Le moteur calcule le P&L d'un trade en % du capital : risque x (R - c) / (1 + c), avec c = coût CFD en R (1,5 point au
niveau actuel du NQ, soit 1,5 / 25 684 du prix). Ici on refait le trade en dollars sur les barres 1 min (série
recolte1.engine.load("NQ") avec l'historique 2010-2015, celle de cache/propfirm/nq_nuit_tp4_mfe.parquet) :
  - Portfolio.from_signals, entrée au close de la barre entry_idx, sens du trade ;
  - sl_stop = distance du stop / prix ; tp_stop = objectif utilisé par le moteur (2 R, ou réduit au reste à faire) x
    distance / prix ; sortie au close de exit_idx (9:30, ou 8:19 les jours d'annonce quand le compte est financé) ;
  - unités = risque en $ / (distance du stop + coût) : un stop coûte exactement le risque, coût compris ;
  - coût de l'aller-retour (unités x coût en points) en frais fixes à l'entrée.
On compare le P&L de chaque trade vectorbt au P&L du moteur (% x 10 000 $), puis le solde du compte jour par jour.
Période : 2011-07-01 → 2026-08-28 (la fenêtre 2026-08-31 → 2026-11-03 est sur une autre série, non rejouée ici).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import vectorbt as vbt

import recolte1.engine as eng
import run_ftmo_deux_comptes as M
from build_news_trades import NY

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/ftmo_verif_vbt")
P_REF = 25_684.0
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lib = M.bibliotheque()
    jours = [j for j in M.tableau(lib) if j[0] <= pd.Timestamp("2026-08-28")]
    A = M.Compte("A mom", True, True, "cible+attente")
    A.journal = []
    for d, row in jours:
        A.jour(d, M.jambes_A(row))
    J = pd.DataFrame(A.journal)
    say(f"Moteur : compte A, {len(J)} trades du {J.date.min():%Y-%m-%d} au {J.date.max():%Y-%m-%d} ; "
        f"{A.evals} évals, {A.rewards} rewards ; objectif réduit sur {int((J.objectif < 2).sum())} trades, "
        f"coupe d'annonce sur {int(J.coupe.sum())}")

    m = pd.read_parquet("cache/propfirm/nq_nuit_tp4_mfe.parquet")
    m["date"] = pd.to_datetime(m.night)
    m["s"] = m.risk.fillna(m.risk.median())
    T = J.merge(m[["date", "entry_idx", "exit_idx", "dir", "reason", "s"]], on="date", how="left")
    assert T.entry_idx.notna().all()
    eng.USE_2010 = True
    eng.load.cache_clear()
    df = eng.load("NQ")
    idx = df.index
    n = len(df)
    # sortie : 8:19 les jours d'annonce coupés (comme build_news_trades.coupe_mom), sinon la sortie d'origine
    x = T.exit_idx.to_numpy().copy()
    for i in np.flatnonzero(T.coupe.to_numpy()):
        cut = pd.Timestamp(f"{T.date.iloc[i]:%Y-%m-%d} 08:18", tz=NY).tz_convert("UTC")
        x[i] = idx.searchsorted(cut, side="right") - 1
    e = T.entry_idx.to_numpy().astype(int)
    cl = df.close.to_numpy()
    en = cl[e]
    dist = T.s.to_numpy() * en
    cout = 1.5 / P_REF * en
    unites = (T.risque.to_numpy() / 100 * M.SIZE) / (dist + cout)

    le, se, ex = np.zeros(n, bool), np.zeros(n, bool), np.zeros(n, bool)
    sl, tp, size, ff = np.full(n, np.nan), np.full(n, np.nan), np.full(n, np.nan), np.zeros(n)
    le[e[T.dir.to_numpy() > 0]] = True
    se[e[T.dir.to_numpy() < 0]] = True
    ex[x.astype(int)] = True
    sl[e] = T.s.to_numpy()
    tp[e] = T.objectif.to_numpy() * T.s.to_numpy()
    size[e] = unites
    ff[e] = unites * cout
    pf = vbt.Portfolio.from_signals(close=df.close, open=df.open, high=df.high, low=df.low, entries=le, exits=ex,
                                    short_entries=se, short_exits=ex, sl_stop=sl, tp_stop=tp, size=size,
                                    size_type="amount", fixed_fees=ff, init_cash=1e9, freq="1min")
    rec = pf.trades.records_readable
    assert len(rec) == len(T), (len(rec), len(T))
    T["pnl_moteur"] = T.pnl / 100 * M.SIZE
    T["pnl_vbt"] = rec["PnL"].to_numpy()
    T["ecart"] = T.pnl_vbt - T.pnl_moteur
    T.to_csv(OUT / "trades.csv", index=False)
    ok = T.ecart.abs() < 0.01
    say(f"\nvectorbt : {len(rec)} trades ; P&L identique au centime près : {int(ok.sum())} / {len(T)} "
        f"({100 * ok.mean():.2f} %) ; écart absolu max {T.ecart.abs().max():.2f} $ ; somme des écarts {T.ecart.sum():+.2f} $")
    say(f"P&L total : moteur {T.pnl_moteur.sum():+,.2f} $, vectorbt {T.pnl_vbt.sum():+,.2f} $")
    if (~ok).any():
        bad = T[~ok]
        say(f"Trades qui diffèrent : {len(bad)} ; par objectif réduit {int((bad.objectif < 2).sum())}, par coupe d'annonce "
            f"{int(bad.coupe.sum())}, par sortie d'origine {bad.reason.value_counts().to_dict()}")
        say(bad[["date", "phase", "reason", "R_brut", "R", "objectif", "risque", "pnl_moteur", "pnl_vbt", "ecart"]]
            .head(15).round(3).to_string(index=False))
    # solde jour par jour (P&L cumulé de trading, hors remises à zéro)
    cum = T.groupby("date")[["pnl_moteur", "pnl_vbt"]].sum().cumsum()
    say(f"\nP&L de trading cumulé : écart max entre moteur et vectorbt sur un jour {(cum.pnl_vbt - cum.pnl_moteur).abs().max():.2f} $")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
