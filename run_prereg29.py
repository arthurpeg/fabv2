"""Pré-enregistrement n° 29 : short du yen en session US filtré R4, avec SL 2 ATR H1 et TP 3R (PREREGISTRATION_29.md).

Code figé avec le pré-enregistrement. Seuls les fichiers d'entrée et les dates changent.

  uv run python -X utf8 run_prereg29.py --spot cache/dukascopy/USDJPY_1m_2003_2009.parquet
      → confirmation (étape 3) sur USDJPY au comptant, du début des données au 2009-12-31
  uv run python -X utf8 run_prereg29.py --lecture AAAA-MM-JJ <fichier 6J 1 min>
      → lecture forward (étape 4) sur 6J, du 2026-08-29 à la date de lecture
  uv run python -X utf8 run_prereg29.py --controle
      → contrôle du code sur 6J 2017-01-30 → 2026-08-28 (déjà vu) : doit redonner run_jpy_us_r4_stops.py (S7)

Convention : tout est exprimé en USDJPY (yens par dollar). Short yen = long USDJPY. Pour 6J (dollars par yen),
on inverse les prix (high ↔ low). Entrée : open de la première minute dans [11:00, 11:05) ET ; sortie : open de la
première minute dans [16:55, 17:00) ET, ou SL / TP. Jours du lundi au vendredi avec entrée et sortie.
R4 : rendement USDJPY des 3 journées précédentes (16:55 J−4 → 16:55 J−1, prix de sortie mid) < 0, c'est-à-dire
yen en hausse. SL = 2 × ATR de Wilder 14 sur bougies H1 (bid pour le comptant), dernière bougie terminée à 11:00 ;
TP = 3 × SL. Exécution 1 min : open au-delà d'un niveau → sortie à l'open ; SL et TP dans la même minute → SL.
Comptant : achat à l'ask, vente au bid (niveaux SL / TP testés sur le bid), + 0,5 bp de commission par aller-retour.
6J : prix unique, 1 tick + 5 $ par aller-retour.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from fab.protocole import holm, nw_t

sys.stdout.reconfigure(encoding="utf-8")
NY = "America/New_York"
OUT = Path("results/prereg29")
COMM_BP = 0.5
MULT_6J, TICK_6J, FEE_6J = 12_500_000, 0.0000005, 5.0
K_SL, RR = 2.0, 3.0


def depuis_6j(df: pd.DataFrame) -> pd.DataFrame:
    """6J (USD par JPY) → USDJPY synthétique, prix unique (bid = ask)."""
    o = pd.DataFrame(index=df.index)
    o["open"], o["high"], o["low"], o["close"] = 1 / df.open, 1 / df.low, 1 / df.high, 1 / df.close
    for c in ("open", "high", "low", "close"):
        o["ask_" + c] = o[c]
    return o


def atr_h1(df: pd.DataFrame, n: int = 14) -> pd.Series:
    o = df.resample("1h", label="right", closed="left").agg({"high": "max", "low": "min", "close": "last"}).dropna()
    tr = pd.concat([o.high - o.low, (o.high - o.close.shift()).abs(), (o.low - o.close.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def journees(df: pd.DataFrame) -> pd.DataFrame:
    mins = df.index.hour * 60 + df.index.minute
    sel = df[(mins >= 660) & (mins < 1020)]
    a = atr_h1(df)
    rows = []
    for d, g in sel.groupby(sel.index.date):
        if pd.Timestamp(d).dayofweek > 4:
            continue
        gm = g.index.hour * 60 + g.index.minute
        ein = np.flatnonzero((gm >= 660) & (gm < 665))
        eout = np.flatnonzero((gm >= 1015) & (gm < 1020))
        if not len(ein) or not len(eout):
            continue
        i0, i1 = ein[0], eout[0]
        t_atr = g.index[i0].replace(minute=0, second=0)
        av = a[a.index <= t_atr]
        rows.append({
            "date": pd.Timestamp(d), "ask_in": g.ask_open.iat[i0], "bid_in": g.open.iat[i0],
            "bid_out": g.open.iat[i1], "ask_out": g.ask_open.iat[i1],
            "atr": av.iat[-1] if len(av) else np.nan,
            "o": g.open.values[i0:i1], "h": g.high.values[i0:i1], "l": g.low.values[i0:i1],
        })
    j = pd.DataFrame(rows).set_index("date")
    j["mid_in"] = (j.ask_in + j.bid_in) / 2
    j["mid_out"] = (j.ask_out + j.bid_out) / 2
    jour = 1e4 * np.log(j.mid_out / j.mid_out.shift(1))
    j["r4"] = jour.shift(1).rolling(3).sum() < 0  # USDJPY en baisse sur 3 journées = yen en hausse
    j["r4_def"] = jour.shift(1).rolling(3).sum().notna() & j.atr.notna()
    return j


def trades(j: pd.DataFrame, cout_bp: pd.Series) -> pd.DataFrame:
    rows = []
    for d, x in j.iterrows():
        p0 = x.ask_in
        sl_d = K_SL * x.atr
        s, t = p0 - sl_d, p0 + RR * sl_d
        o, h, l = x.o, x.h, x.l
        hit = (l <= s) | (o <= s) | (h >= t) | (o >= t)
        if hit.any():
            i = int(np.argmax(hit))
            if o[i] <= s:
                how, px = "SL", o[i]
            elif o[i] >= t:
                how, px = "TP", o[i]
            elif l[i] <= s:
                how, px = "SL", s
            else:
                how, px = "TP", t
        else:
            how, px = "temps", x.bid_out
        risk = 1e4 * sl_d / p0
        net = 1e4 * np.log(px / p0) - cout_bp[d]
        rows.append({"date": d, "exit": how, "risk_bp": risk, "net_bp": net, "R": net / risk})
    return pd.DataFrame(rows).set_index("date")


def analyse(j: pd.DataFrame, cout_bp: pd.Series, extra_bp: float, titre: str) -> dict:
    j = j[j.r4_def]
    brut = 1e4 * np.log(j.mid_out / j.mid_in)  # short yen, sans stop, mid
    net_ref = 1e4 * np.log(j.bid_out / j.ask_in) - cout_bp[j.index]  # référence triviale : tous les jours, sans stop
    pris, saut = brut[j.r4], brut[~j.r4]
    w = stats.ttest_ind(pris, saut, equal_var=False)
    p1 = float(stats.t.sf(w.statistic, w.df))
    tr = trades(j[j.r4], cout_bp)
    tR = nw_t(tr.R)
    p2 = float(stats.norm.sf(tR))
    adj = holm([p1, p2])
    yrs = tr.index.year
    best = tr.R.groupby(yrs).sum().idxmax()
    diff_y = pris.groupby(pris.index.year).mean() - saut.groupby(saut.index.year).mean()
    sans_best_h1 = pris[pris.index.year != diff_y.idxmax()].mean() - saut[saut.index.year != diff_y.idxmax()].mean()
    res = {
        "titre": titre, "jours": len(j), "debut": str(j.index.min().date()), "fin": str(j.index.max().date()),
        "jours_r4_%": 100 * j.r4.mean(),
        "info_brut_tous_jours_bp": brut.mean(), "info_t_nw_tous_jours": nw_t(brut),
        "H1_brut_pris_bp": pris.mean(), "H1_brut_sautes_bp": saut.mean(), "H1_ecart_bp": pris.mean() - saut.mean(),
        "H1_t_welch": float(w.statistic), "H1_p": p1, "H1_p_holm": adj[0], "H1_ecart_sans_meilleure_annee": sans_best_h1,
        "H2_n": len(tr), "H2_R_moyen": tr.R.mean(), "H2_t_nw": tR, "H2_p": p2, "H2_p_holm": adj[1],
        "H2_net_bp": tr.net_bp.mean(), "H2_ref_net_tous_jours_bp": net_ref.mean(),
        "H2_R_sans_meilleure_annee": tr.R[yrs != best].mean(),
        "H2_R_cout_plus": (tr.R - extra_bp / tr.risk_bp).mean(),
        "H2_SL_%": 100 * (tr.exit == "SL").mean(), "H2_TP_%": 100 * (tr.exit == "TP").mean(),
        "info_spread_med_entree_bp": float(1e4 * ((j.ask_in - j.bid_in) / j.mid_in).median()),
    }
    res["C1_H1"] = res["H1_p_holm"] <= 0.05 and res["H1_ecart_bp"] > 0
    res["C3_H1"] = sans_best_h1 > 0
    res["C1_H2"] = res["H2_p_holm"] <= 0.05 and res["H2_R_moyen"] > 0
    res["C2_H2"] = res["H2_net_bp"] > res["H2_ref_net_tous_jours_bp"]
    res["C3_H2"] = res["H2_R_sans_meilleure_annee"] > 0
    res["C4_H2"] = res["H2_R_cout_plus"] > 0
    return res, tr


def imprimer(res: dict, tr: pd.DataFrame, nom: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    s = "\n".join(f"{k:<34} {v:.4g}" if isinstance(v, float) else f"{k:<34} {v}" for k, v in res.items())
    print(s)
    (OUT / f"{nom}.txt").write_text(s, encoding="utf-8")
    tr.to_csv(OUT / f"{nom}_trades.csv")


def main() -> None:
    a = sys.argv
    if "--spot" in a:
        df = pd.read_parquet(a[a.index("--spot") + 1])
        df.index = df.index.tz_convert(NY)
        df = df[df.index < pd.Timestamp("2010-01-01", tz=NY)]
        j = journees(df)
        cout = pd.Series(COMM_BP, index=j.index)
        res, tr = analyse(j, cout, 0.5, "Étape 3 : USDJPY comptant ≤ 2009-12-31")
        imprimer(res, tr, "spot_2003_2009")
    elif "--lecture" in a or "--controle" in a:
        if "--controle" in a:
            f, lo, hi, nom = "D:/quant-data/Cotations/forex/6J_v0_1m.parquet", "2017-01-30", "2026-08-29", "controle_6j"
        else:
            i = a.index("--lecture")
            f, lo, hi, nom = a[i + 2], "2026-08-29", a[i + 1], f"lecture_{a[i + 1]}"
        raw = pd.read_parquet(f)
        raw = raw[~raw.index.duplicated()].sort_index()
        raw.index = raw.index.tz_convert(NY)
        lo_ts = pd.Timestamp(lo, tz=NY)
        # les 3 journées et l'ATR précédant le début sont pris dans l'historique (≤ 30 jours avant)
        raw = raw[(raw.index >= lo_ts - pd.Timedelta(days=30)) & (raw.index < pd.Timestamp(hi, tz=NY))]
        df = depuis_6j(raw)
        j = journees(df)
        j = j[j.index >= pd.Timestamp(lo)]
        cout = 1e4 * (TICK_6J * MULT_6J + FEE_6J) / (MULT_6J / j.mid_in)  # notional en $ = MULT / USDJPY
        res, tr = analyse(j, cout, 1e4 * TICK_6J * j.mid_in.mean(), f"6J {lo} → {hi}")
        imprimer(res, tr, nom)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
