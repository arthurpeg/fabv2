"""Étape 1 (exploration) : retournement des rendements 24 h sur les paires yen (Piccotti, SSRN 2446584).

uv run python run_jpy_reversal24.py   → results/jpy_reversal24/ (trades_<variante>.csv, rho_par_an.csv,
                                         familles.csv, summary.txt)

Fiche d'idée : wiki/experiments/fx-retournement-24h-yen.md (étape 0, B0 passée le 2026-11-19).
Protocole : PROTOCOLE.md, étape 1. GRILLE FIGÉE CI-DESSOUS ET COMMITÉE AVANT TOUT CALCUL ; rien n'y change
après le premier lancement. Toute variante supplémentaire = nouvelle ligne au compteur et nouveau commit.

──────────────────────────────── GRILLE (figée le 2026-11-19) ────────────────────────────────
Données (toutes déjà explorées, wiki/reserves.md) — RIEN APRÈS LE 2026-08-28 (yen réservé au n° 28) :
  • spot Dukascopy 1 min, 2012-01-11 → 2015-12-31 (bid = open, ask = ask_open ; mid = moyenne) ;
  • futures Databento .v.0 1 min, 2016-01-01 → 2026-08-28, ajustés en ratio aux roulements
    (règle de run_sessions.load : un roulement par mois d'échéance, plus grand |écart| à 00:00 UTC
    entre le 7 et le 22, barre précédente à ≤ 60 min).
  Le spot horaire 2010-2011 n'est pas utilisé (16:55 n'y existe pas). La période du papier (2007-2010)
  n'est pas disponible : PAS DE RÉPLICATION possible ; on publie à la place, en descriptif, ρ(1) des
  rendements 24 h par variante et par année (même famille, pas d'essai supplémentaire).

Paires (log-prix x en yens par unité étrangère) :
  • USDJPY : spot log(mid USDJPY) ; futures −log(6J).
  • AUDJPY (synthétique) : spot log(mid AUDUSD) + log(mid USDJPY) ; futures log(6A) − log(6J).
Heures H (America/New_York) : 11:00, 15:00, 16:55. Prix à H = open de la première barre dans [H, H+5 min).
→ 2 paires × 3 heures = 6 variantes. n_famille = 6.

Règle (la même pour les 6 variantes) :
  • jours d'entrée : lundi à jeudi (aucune position le week-end) ; sortie à H le jour ouvré suivant ;
  • signal à l'entrée du jour t : r_t = x(t, H) − x(t−1, H), t−1 = jour ouvré précédent disponible
    (lundi : vendredi → lundi, week-end inclus) ; position = −signe(r_t) ; r_t = 0 ou manquant → pas de trade ;
  • brut (bp) = position × 1e4 × (x(t+1, H) − x(t, H)).
Coûts (net) :
  • futures : coût standard 1 tick + 5 $ aller-retour PAR JAMBE, converti en bp du notionnel à l'entrée
    (6J : tick 0,0000005, 12,5 M JPY ; 6A : tick 0,0001, 100 000 AUD, comme run_zhang.py) ;
  • spot : demi-spread bid/ask réel à l'entrée + demi-spread à la sortie, par jambe, + 0,5 bp de commission
    par jambe (comme run_jpy_us_backtest.py).
  « +1 tick » (critère 6 de B1) : un tick de plus par jambe ; spot : 0,1 pip (0,001 JPY, 0,00001 USD) par jambe.
Référence triviale (fixée avant calcul) : la même position sans condition, toujours short yen
  (position = +1 sur x), mêmes jours, mêmes heures, mêmes coûts.
Choix de la règle finale : la variante au plus grand Sharpe net sur toute la tranche 2012-01-11 → 2026-08-28.
Barrière : B1 (fab.protocole.barriere_exploration) sur cette variante, n_famille = 6, sharpes_famille =
  les 6 Sharpe par trade nets. 2020 montré à part. Parcours phénomène en parallèle : même B1 sur le brut
  (critères 3 et 6 ignorés), signalé « À surveiller » / « Confirmés » selon PROTOCOLE.md.
Compteur global : 1 798 → 1 804 (6 variantes).
──────────────────────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from fab.protocole import barriere_exploration, fiche, imprimer, nw_t

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/jpy_reversal24")
NY = "America/New_York"
FUT = Path("D:/quant-data/Cotations/forex")
SPOT = Path("cache/dukascopy")
SPOT_START, SPOT_END = pd.Timestamp("2012-01-11", tz=NY), pd.Timestamp("2016-01-01", tz=NY)
FUT_START, FUT_END = pd.Timestamp("2016-01-01", tz=NY), pd.Timestamp("2026-08-29", tz=NY)
HOURS = ["11:00", "15:00", "16:55"]
PAIRS = ["USDJPY", "AUDJPY"]
SPEC = {"6J": (0.0000005, 12_500_000), "6A": (0.0001, 100_000)}  # tick, multiplicateur
FEE_USD = 5.0
COMM_SPOT_BP = 0.5
N_FAMILLE = 6
COUNTER = (1798, 1804)


# ───────────────────────────── données ─────────────────────────────
def load_fut(sym: str) -> pd.DataFrame:
    """6J / 6A .v.0 1 min ajustés en ratio (règle de run_sessions.load)."""
    df = pd.read_parquet(FUT / f"{sym}_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    gap = df["open"] / df["close"].shift() - 1
    ix = df.index
    prev = pd.Series(ix, index=ix).shift()
    cand = (ix.hour == 0) & (ix.minute == 0) & ((ix - prev) <= pd.Timedelta(minutes=60)).values
    cand &= ix.month.isin([3, 6, 9, 12]) & (ix.day >= 7) & (ix.day <= 22)
    g = gap[cand]
    rolls = pd.DatetimeIndex(g.abs().groupby([g.index.year, g.index.month]).idxmax().tolist())
    step = pd.Series(1.0, index=ix)
    step.loc[rolls] = 1 + gap.loc[rolls]
    factor = step[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
    out = pd.DataFrame({"open": df["open"] * factor, "raw_open": df["open"]})
    out.index = out.index.tz_convert(NY)
    out = out[(out.index >= FUT_START) & (out.index < FUT_END)]
    out.attrs["n_rolls"] = len(rolls[(rolls >= FUT_START) & (rolls < FUT_END)])
    return out


def load_spot(pair: str) -> pd.DataFrame:
    s = pd.read_parquet(SPOT / f"{pair}_1m.parquet")
    s.index = s.index.tz_convert(NY)
    s = s[(s.index >= SPOT_START) & (s.index < SPOT_END)]
    return pd.DataFrame({"mid": (s["open"] + s["ask_open"]) / 2, "spread": s["ask_open"] - s["open"]})


def at_hour(df: pd.DataFrame, t: str) -> pd.DataFrame:
    """Première barre dans [H, H+5 min) de chaque date ET (jours ouvrés)."""
    h, m = map(int, t.split(":"))
    mins = df.index.hour * 60 + df.index.minute
    sel = df[(mins >= h * 60 + m) & (mins < h * 60 + m + 5)]
    first = sel.groupby(sel.index.date).head(1)
    first.index = pd.DatetimeIndex(first.index.date, name="date")
    return first[first.index.dayofweek < 5]


def series_fut(pair: str, t: str) -> pd.DataFrame:
    """x (log-prix, yens par unité étrangère), coût aller-retour en bp et +1 tick en bp, par date."""
    j = at_hour(load_fut("6J"), t)
    tick_j, mult_j = SPEC["6J"]
    cost_j = 1e4 * (tick_j * mult_j + FEE_USD) / (j.raw_open * mult_j)
    tick1_j = 1e4 * tick_j / j.raw_open
    if pair == "USDJPY":
        return pd.DataFrame({"x": -np.log(j.open), "cost_bp": cost_j, "tick_bp": tick1_j})
    a = at_hour(load_fut("6A"), t)
    tick_a, mult_a = SPEC["6A"]
    d = pd.concat({"j": j.open, "a": a.open, "cj": cost_j, "tj": tick1_j,
                   "ca": 1e4 * (tick_a * mult_a + FEE_USD) / (a.raw_open * mult_a),
                   "ta": 1e4 * tick_a / a.raw_open}, axis=1).dropna()
    return pd.DataFrame({"x": np.log(d.a) - np.log(d.j), "cost_bp": d.cj + d.ca, "tick_bp": d.tj + d.ta})


def series_spot(pair: str, t: str) -> pd.DataFrame:
    """Coût par jambe = demi-spread (ici à l'entrée ; la sortie est ajoutée dans trades()) + commission."""
    u = at_hour(load_spot("USDJPY"), t)
    hs_u = 1e4 * u.spread / u.mid / 2
    tick_u = 1e4 * 0.001 / u.mid
    if pair == "USDJPY":
        return pd.DataFrame({"x": np.log(u.mid), "half_spread_bp": hs_u, "n_legs": 1, "tick_bp": tick_u})
    a = at_hour(load_spot("AUDUSD"), t)
    d = pd.concat({"u": u.mid, "a": a.mid, "hu": hs_u, "tu": tick_u,
                   "ha": 1e4 * a.spread / a.mid / 2, "ta": 1e4 * 0.00001 / a.mid}, axis=1).dropna()
    return pd.DataFrame({"x": np.log(d.a) + np.log(d.u), "half_spread_bp": d.hu + d.ha, "n_legs": 2,
                         "tick_bp": d.tu + d.ta})


# ───────────────────────────── règle ─────────────────────────────
def trades(s: pd.DataFrame, spot: bool) -> pd.DataFrame:
    """Entrée lundi-jeudi à H, sortie à H le jour ouvré suivant ; signal = −signe(rendement 24 h écoulé)."""
    s = s.sort_index()
    x_prev, x_next = s.x.shift(1), s.x.shift(-1)
    nxt_date = pd.Series(s.index, index=s.index).shift(-1)
    r_sig = 1e4 * (s.x - x_prev)
    r_fwd = 1e4 * (x_next - s.x)
    dow = s.index.dayofweek
    gap_next = (nxt_date - pd.Series(s.index, index=s.index)).dt.days
    ok = (dow <= 3) & (gap_next == 1) & r_sig.notna() & r_fwd.notna() & (r_sig != 0)
    if spot:
        cost = s.half_spread_bp + s.half_spread_bp.shift(-1) + COMM_SPOT_BP * s.n_legs
    else:
        cost = s.cost_bp
    tr = pd.DataFrame({"r_sig_bp": r_sig, "r_fwd_bp": r_fwd, "cost_bp": cost, "tick_bp": s.tick_bp})[ok].dropna()
    tr["pos"] = -np.sign(tr.r_sig_bp)
    tr["brut_bp"] = tr.pos * tr.r_fwd_bp
    tr["net_bp"] = tr.brut_bp - tr.cost_bp
    tr["ref_brut_bp"] = tr.r_fwd_bp            # toujours short yen = long x
    tr["ref_net_bp"] = tr.r_fwd_bp - tr.cost_bp
    return tr


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []

    def say(s: str = "") -> None:
        print(s)
        lines.append(s)

    say("Retournement 24 h, paires yen — étape 1 (exploration), grille figée dans l'en-tête")
    say(f"Compteur global : {COUNTER[0]} → {COUNTER[1]} (n_famille = {N_FAMILLE})")
    for sym in ("6J", "6A"):
        say(f"  roulements détectés {sym} 2016-2026-08 : {load_fut(sym).attrs['n_rolls']} (attendu ≈ 43)")

    fam, rho_rows = {}, []
    for pair in PAIRS:
        for t in HOURS:
            name = f"{pair}_{t.replace(':', '')}"
            tr = pd.concat([trades(series_spot(pair, t), spot=True).assign(src="spot"),
                            trades(series_fut(pair, t), spot=False).assign(src="fut")]).sort_index()
            tr.to_csv(OUT / f"trades_{name}.csv")
            fam[name] = tr
            yrs = tr.index.year
            for y in sorted(set(yrs)):
                d = tr[yrs == y]
                rho_rows.append({"variante": name, "annee": y, "n": len(d),
                                 "rho1": float(np.corrcoef(d.r_sig_bp, d.r_fwd_bp)[0, 1])})

    rho = pd.DataFrame(rho_rows)
    rho.to_csv(OUT / "rho_par_an.csv", index=False)
    say("\n== Descriptif : ρ(1) des rendements 24 h (signal → suivant), toute la tranche")
    for name, tr in fam.items():
        r = float(np.corrcoef(tr.r_sig_bp, tr.r_fwd_bp)[0, 1])
        say(f"  {name:<12} n {len(tr):5d}  ρ(1) {r:+.3f}  (t ≈ {r * np.sqrt(len(tr)):+.2f})  "
            f"années ρ<0 : {(rho[rho.variante == name].rho1 < 0).sum()}/{(rho.variante == name).sum()}")

    sharpes = {k: v.net_bp.mean() / v.net_bp.std() for k, v in fam.items()}
    rows = []
    say("\n== Les 6 variantes (bp par trade)")
    for name, tr in fam.items():
        rows.append({"variante": name, "n": len(tr), "brut": tr.brut_bp.mean(), "net": tr.net_bp.mean(),
                     "t_nw_net": nw_t(tr.net_bp), "t_nw_brut": nw_t(tr.brut_bp),
                     "sharpe_an_net": sharpes[name] * np.sqrt(252), "ref_net": tr.ref_net_bp.mean(),
                     "net_2020": tr.net_bp[tr.index.year == 2020].mean(),
                     "net_spot": tr.net_bp[tr.src == "spot"].mean(), "net_fut": tr.net_bp[tr.src == "fut"].mean()})
        r = rows[-1]
        say(f"  {name:<12} n {r['n']:5d} | brut {r['brut']:+5.2f} (t {r['t_nw_brut']:+.2f}) | net {r['net']:+5.2f} "
            f"(t {r['t_nw_net']:+.2f}) | Sharpe net an. {r['sharpe_an_net']:+.2f} | réf. net {r['ref_net']:+5.2f} | "
            f"2020 {r['net_2020']:+5.2f} | spot {r['net_spot']:+5.2f} / fut {r['net_fut']:+5.2f}")
    pd.DataFrame(rows).to_csv(OUT / "familles.csv", index=False)

    best = max(sharpes, key=sharpes.get)
    tr = fam[best]
    say(f"\n== Règle choisie (plus grand Sharpe net, critère figé) : {best}")
    f = fiche(tr.net_bp, tr.brut_bp, tr.ref_net_bp, n_famille=N_FAMILLE,
              sharpes_famille=list(sharpes.values()), tick_bp=tr.tick_bp)
    say(imprimer(f, f"Fiche nette {best}"))
    ok, why = barriere_exploration(f)
    say("B1 (stratégie, net) : " + ("PASSÉE" if ok else "ÉCHOUÉE"))
    for w in why:
        say("  " + w)

    sh_brut = {k: v.brut_bp.mean() / v.brut_bp.std() for k, v in fam.items()}
    fb = fiche(tr.brut_bp, tr.brut_bp, tr.ref_brut_bp, n_famille=N_FAMILLE, sharpes_famille=list(sh_brut.values()))
    say(imprimer(fb, f"Fiche brute {best} (parcours phénomène)"))
    _, whyb = barriere_exploration(fb)
    say("B1 (phénomène, brut ; critères 3 et 6 ignorés) :")
    for w in whyb:
        say("  " + w)
    say(f"\nCompteur global : {COUNTER[1]}")
    (OUT / "summary.txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
