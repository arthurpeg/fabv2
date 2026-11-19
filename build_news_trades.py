"""Trades mom et M2 du compte financé FTMO avec la règle des annonces (demande du 2026-11-04).

uv run python build_news_trades.py → cache/propfirm/news_trades.parquet (date, strat, R_news, MFE_news, coupé)

Règle FTMO (compte financé Standard, relue le 2026-11-01, voir reports/propfirm_multi.md) : aucun ordre exécuté, stop et
objectif compris, 2 min avant et après les annonces restreintes. Pour l'US100 on retient : NFP, CPI, PIB avancé (8:30 ET),
décision et minutes de la Fed (14:00 ET).
  - mom (20:00 → 9:30) : les jours d'annonce de 8:30, position fermée au close de la barre 1 min de 8:18 (8:19 ET),
    comme run_propfirm_multi (news_f) ; un trade déjà sorti avant reste tel quel ;
  - M2 (9:35 → 15:55) : les jours de Fed, position fermée au close de la barre 5 min de 13:50 (13:55 ET) ;
  - 3n (20:05 → 03:00) n'est jamais concerné.
Calendrier : config/calendrier_macro_us.csv (build_calendar_macro.py, jusqu'au 2026-08-26), complété pour la fenêtre déjà
vue : NFP 2026-09-04 et 2026-10-02, CPI 2026-09-11 et 2026-10-14 (archives BLS), Fed 2026-09-16 et 2026-10-28,
minutes 2026-10-07 (federalreserve.gov), PIB avancé T3 supposé le 2026-10-29 (non publié dans le calendrier BEA consulté).
Seuls les trades modifiés sont écrits ; R et MFE en R (MFE jusqu'à la nouvelle sortie).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
NY = "America/New_York"
AJOUTS = [("2026-09-04", "NFP"), ("2026-10-02", "NFP"), ("2026-09-11", "CPI"), ("2026-10-14", "CPI"),
          ("2026-09-16", "FOMC décision"), ("2026-10-28", "FOMC décision"), ("2026-10-07", "FOMC minutes"),
          ("2026-10-29", "PIB avancé")]


def calendrier() -> tuple[set, set]:
    c = pd.read_csv("config/calendrier_macro_us.csv")
    c = pd.concat([c, pd.DataFrame(AJOUTS, columns=["date", "annonce"])], ignore_index=True)
    c["date"] = pd.to_datetime(c.date)
    matin = set(c.date[c.annonce.isin(["NFP", "CPI", "PIB avancé"])])
    fed = set(c.date[c.annonce.isin(["FOMC décision", "FOMC minutes"])])
    return matin, fed


def coupe_mom(df: pd.DataFrame, t: pd.DataFrame, matin: set) -> pd.DataFrame:
    """t : night, entry_idx, exit_idx, dir, risk ; df : barres 1 min indexées en UTC (série ajustée du moteur)."""
    loc = df.index.tz_convert(NY)
    cl, hi, lo = df.close.values, df.high.values, df.low.values
    rows = []
    for night, e, x, d, risk in zip(pd.to_datetime(t.night), t.entry_idx, t.exit_idx, t.dir, t.risk):
        if night not in matin:
            continue
        cut = pd.Timestamp(f"{night:%Y-%m-%d} 08:18", tz=NY).tz_convert("UTC")
        k = df.index.searchsorted(cut, side="right") - 1  # dernière barre ≤ 8:18
        if not (e < k < x):
            continue  # trade sorti avant 8:19 : rien à couper
        en = cl[e]
        R = d * (cl[k] - en) / (risk * en)
        mfe = ((hi[e + 1:k + 1].max() - en) if d > 0 else (en - lo[e + 1:k + 1].min())) / (risk * en)
        rows.append(dict(date=night, strat="mom", R_news=R, MFE_news=max(mfe, 0.0), coupé=f"{loc[k]:%H:%M}"))
    return pd.DataFrame(rows)


def coupe_m2(src: str, a: str, z: str, fin: str, fed: set) -> pd.DataFrame:
    import run_nq_ema930_vbt as E
    import run_nq_nuit_3n_vbt as B
    import run_propfirm_combo as C
    B.SRC, B.END = Path(src), pd.Timestamp(fin, tz=NY)
    b5, b15 = B.bars()
    d = E.seances(b5, b15)
    dd = pd.to_datetime(d.date)
    d = d[(dd >= a) & (dd <= z) & d.m2 & dd.isin(fed)].reset_index(drop=True)
    if not len(d):
        return pd.DataFrame()
    hm = b5.index.hour * 60 + b5.index.minute
    z_new = []
    for e, zz in zip(d.e, d.z):
        cand = np.flatnonzero(hm[e:zz + 1] == 13 * 60 + 50)
        z_new.append(e + cand[0] if len(cand) else zz)
    t, _ = C.simule(b5, d.e.values, np.array(z_new), d.side.values, E.K_SL * d.atr15.values, False)
    return pd.DataFrame({"date": pd.to_datetime(d.date), "strat": "M2", "R_news": t.R_brut, "MFE_news": t.MFE_R,
                         "coupé": "13:55"})


def main() -> None:
    matin, fed = calendrier()
    import recolte1.engine as eng
    eng.USE_2010 = True
    eng.load.cache_clear()
    df = eng.load("NQ")
    m = pd.read_parquet("cache/propfirm/nq_nuit_tp4_mfe.parquet")
    m = m.assign(risk=m.risk.fillna(m.risk.median()))
    parts = [coupe_mom(df, m, matin)]
    # fenêtre déjà vue : trades mom TP 4 ATR recalculés sur la série raboutée (Databento + LSE)
    import run_holdout_anticipe as H
    w = H.h1_mom(Path("cache/holdout_anticipe/ajuste/indices/NQ_v0_1m.parquet"), tp=4.0, cost="gross")
    dfw = eng.load("NQ")
    parts.append(coupe_mom(dfw, w.rename(columns={"s": "risk"}).assign(risk=w.s / 1.0), matin))
    parts.append(coupe_m2("cache/databento_2010/NQ_v0_1m_2010.parquet", "2010-06-08", "2015-12-31", "2016-01-01", fed))
    parts.append(coupe_m2("D:/quant-data/Cotations/indices/NQ_v0_1m.parquet", "2016-01-01", "2026-08-28", "2026-08-29", fed))
    parts.append(coupe_m2("cache/holdout_anticipe/brut/NQ_v0_1m.parquet", "2026-08-31", "2026-11-03", "2026-11-04", fed))
    out = pd.concat([p for p in parts if len(p)], ignore_index=True)
    out.to_parquet("cache/propfirm/news_trades.parquet")
    for s, g in out.groupby("strat"):
        print(f"{s} : {len(g)} trades coupés ({g.date.min():%Y-%m-%d} → {g.date.max():%Y-%m-%d}), R moyen après coupe "
              f"{g.R_news.mean():+.3f}")
    print(out[out.date >= "2026-08-29"].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
