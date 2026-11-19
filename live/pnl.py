"""Suivi du P&L des books FTMO de démo, tous essais additionnés comme un seul compte.

uv run python -m live.pnl                 → affiche le suivi et écrit live/etat/pnl.md
uv run python -m live.pnl --dossier X     → autre dossier d'état (défaut live/etat)

Les essais gratuits FTMO durent 14 jours et repartent à 10 000 $. En vrai, on garderait le même compte : le suivi
additionne donc tous les trades des journaux (live/etat/<book>/trades.csv), quel que soit l'essai MT5 sur lequel ils
ont été passés. Les tailles sont déjà calculées sur 10 000 $ nominaux, donc le cumul est directement celui d'un
compte unique de 10 000 $. Deux lectures :
  - « compte continu » : 10 000 $ + somme de tous les trades (comme si le compte n'était jamais remis à zéro) ;
  - « résultat FTMO virtuel » : ce que le plan aurait réellement encaissé = rewards virtuels − évals achetées
    (compte.json ; 79 € = 86,90 $ par éval de 10k, la 1re comprise).
Le bot régénère ce fichier après chaque trade fermé.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

NOMINAL = 10_000.0
FRAIS_EVAL = 79 * 1.10
BOOKS = {"A": "mom", "B": "3n + M2"}


def charge(dossier: Path, book: str) -> pd.DataFrame:
    p = dossier / book / "trades.csv"
    if not p.exists():
        return pd.DataFrame()
    t = pd.read_csv(p)
    if t.empty:
        return t
    t["sortie_t"] = pd.to_datetime(t.exit_time, utc=True, errors="coerce").dt.tz_convert("America/New_York")
    t = t.sort_values("sortie_t").reset_index(drop=True)
    if "compte_mt5" not in t:
        t["compte_mt5"] = ""
    t["compte_mt5"] = t.compte_mt5.fillna("").astype(str).str.replace(r"\.0$", "", regex=True)
    t["book"] = book
    return t


def courbe(t: pd.DataFrame) -> tuple[pd.Series, float, float]:
    """Compte continu après chaque trade, plus gros creux ($ et % du plus haut)."""
    eq = NOMINAL + t.profit.cumsum()
    haut = np.maximum.accumulate(np.r_[NOMINAL, eq.values])[1:]
    creux = eq.values - haut
    i = int(np.argmin(creux)) if len(creux) else 0
    return eq, float(creux.min(initial=0.0)), float((creux / haut).min(initial=0.0) * 100) if len(creux) else 0.0


def virtuel(dossier: Path, book: str) -> dict:
    p = dossier / book / "compte.json"
    if not p.exists():
        return {}
    c = json.loads(p.read_text(encoding="utf-8"))
    rew = c.get("rewards_pct", 0.0) / 100 * NOMINAL
    return dict(phase=c.get("phase"), P=c.get("P", 0.0), best=c.get("best", 0.0), evals=c.get("evals", 1),
                rewards=c.get("rewards", 0), rewards_usd=rew, net=rew - c.get("evals", 1) * FRAIS_EVAL,
                events=c.get("events", [])[-5:])


def bloc_book(t: pd.DataFrame, v: dict, nom: str) -> list[str]:
    L = [f"## Book {nom}", ""]
    if t.empty:
        L += ["Aucun trade fermé pour l'instant.", ""]
    else:
        eq, dd, ddp = courbe(t)
        gagnants = (t.profit > 0).mean() * 100
        L += [f"- **P&L cumulé, tous essais : {t.profit.sum():+,.2f} $** ({t.profit.sum() / NOMINAL * 100:+.2f} %) "
              f"sur {len(t)} trades, du {t.sortie_t.min():%d/%m/%Y} au {t.sortie_t.max():%d/%m/%Y}",
              f"- Compte continu : {eq.iloc[-1]:,.2f} $ ; plus gros creux {dd:,.2f} $ ({ddp:.2f} %)",
              f"- Trades gagnants {gagnants:.0f} % ; R net moyen {t.R_net.mean():+.2f} ; "
              f"sorties : {', '.join(f'{k} {n}' for k, n in t.raison.value_counts().items())}", ""]
        for c in ("spread_ordre", "spread_sortie", "glissement"):  # colonnes ajoutées le 2026-11-04
            if c not in t:
                t[c] = np.nan
        t["spread_ordre"] = t.spread_ordre.fillna(t.spread)
        g = t.groupby("strat").agg(trades=("profit", "size"), pnl=("profit", "sum"), R_moyen=("R_net", "mean"),
                                   sp_in=("spread_ordre", "mean"), sp_out=("spread_sortie", "mean"),
                                   sp_max=("spread_sortie", "max"), gl=("glissement", "mean"))
        L += ["| Stratégie | Trades | P&L ($) | R net moyen | Spread entrée (pts) | Spread sortie (pts, max) "
              "| Glissement entrée (pts) |", "|---|---|---|---|---|---|---|"]
        L += [f"| {s} | {int(r.trades)} | {r.pnl:+,.2f} | {r.R_moyen:+.2f} | {r.sp_in:.2f} | {r.sp_out:.2f} "
              f"({r.sp_max:.2f}) | {r.gl:+.2f} |" for s, r in g.iterrows()]
        L += ["", "Spread et glissement en points d'indice (1,5 pt supposé dans le backtest) ; glissement > 0 = "
              "exécuté plus cher que le prix affiché.", ""]
        e = t.groupby("compte_mt5", sort=False).agg(trades=("profit", "size"), pnl=("profit", "sum"),
                                                    debut=("sortie_t", "min"), fin=("sortie_t", "max"))
        L += ["| Essai MT5 | Trades | P&L ($) | Période |", "|---|---|---|---|"]
        L += [f"| {k or '?'} | {int(r.trades)} | {r.pnl:+,.2f} | {r.debut:%d/%m} → {r.fin:%d/%m} |" for k, r in e.iterrows()]
        L += [""]
    if v:
        L += [f"- **Compte FTMO virtuel** : {v['phase']}, cycle {v['P']:+.2f} % (meilleur jour {v['best']:+.2f} %), "
              f"évals achetées {v['evals']}, rewards {v['rewards']} ({v['rewards_usd']:,.2f} $) → "
              f"**résultat FTMO virtuel {v['net']:+,.2f} $** (rewards − frais d'éval)"]
        L += [f"  - {e}" for e in v["events"]]
        L += [""]
    return L


def rapport(dossier: Path = Path("live/etat")) -> str:
    T = {b: charge(dossier, b) for b in BOOKS}
    V = {b: virtuel(dossier, b) for b in BOOKS}
    now = pd.Timestamp.now(tz="America/New_York")
    L = [f"# Suivi P&L des books FTMO (démo), au {now:%d/%m/%Y %H:%M} ET", "",
         "Tous les essais FTMO sont additionnés comme un seul compte de 10 000 $ par book (tailles calculées sur ce "
         "nominal). Source : `live/etat/<book>/trades.csv` et `compte.json`.", ""]
    tout = pd.concat([t for t in T.values() if not t.empty], ignore_index=True) if any(
        not t.empty for t in T.values()) else pd.DataFrame()
    if not tout.empty:
        tout = tout.sort_values("sortie_t")
        net_v = sum(v.get("net", 0.0) for v in V.values())
        L += [f"**Total A + B : {tout.profit.sum():+,.2f} $ de trading** sur {len(tout)} trades "
              f"(2 × 10 000 $ → {2 * NOMINAL + tout.profit.sum():,.2f} $) ; résultat FTMO virtuel {net_v:+,.2f} $.", ""]
        # journée FTMO = date de séance (minuit serveur = 17:00 ET) : la nuit mom du 04 au 05 compte pour le 05
        jour = tout.seance.astype(str) if "seance" in tout else tout.sortie_t.dt.strftime("%Y-%m-%d")
        j = tout.assign(jour=jour).pivot_table(
            index="jour", columns="book", values="profit", aggfunc="sum").fillna(0.0)
        j["total"] = j.sum(axis=1)
        L += ["### Dix dernières journées FTMO ($)", "", "| Jour | " + " | ".join(j.columns) + " |",
              "|---" * (len(j.columns) + 1) + "|"]
        L += [f"| {d} | " + " | ".join(f"{x:+,.2f}" for x in r.values) + " |" for d, r in j.tail(10).iterrows()]
        L += [""]
    for b, nom in BOOKS.items():
        L += bloc_book(T[b], V[b], f"{b} ({nom})")
    return "\n".join(L)


def ecrit_rapport(dossier: Path = Path("live/etat")) -> Path:
    p = Path(dossier) / "pnl.md"
    p.write_text(rapport(Path(dossier)), encoding="utf-8")
    return p


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dossier", default="live/etat")
    a = ap.parse_args()
    p = ecrit_rapport(Path(a.dossier))
    print(p.read_text(encoding="utf-8"))
    print(f"\n(écrit dans {p})")


if __name__ == "__main__":
    main()
