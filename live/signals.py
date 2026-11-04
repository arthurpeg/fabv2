"""Signaux des deux books FTMO, calculés comme dans le backtest, sur des barres 1 min en heure de New York.

Sources reproduites (ne pas modifier sans changer aussi le backtest) :
  - mom : recolte1/rules.py (monthly, next_month_sign) et run_recolte1_atr.py (atr_m15) via run_holdout_anticipe.h1_mom ;
  - 3n  : run_nq_nuit_3n_vbt.py (bars, atr_wilder, nuits) ;
  - M2  : run_nq_ema930_vbt.py (seances).
Les fonctions prennent un DataFrame `m1` (open, high, low, close) indexé par l'heure de DÉBUT de chaque barre 1 min,
tz America/New_York. En direct, ces barres viennent du terminal MT5 (US100.cash) ; dans tests/test_live.py, des
barres NQ du dépôt, pour vérifier que l'on retrouve les signaux du backtest.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

NY = "America/New_York"
K_SL_NUIT, K_SL_M2, TP_R = 2.0, 4.0, 2.0
STR_T, REV_T = 2.2, -60.0
AGG = {"open": "first", "high": "max", "low": "min", "close": "last"}


def resample(m1: pd.DataFrame, freq: str) -> pd.DataFrame:
    """Barres 5 / 15 min horodatées au début, regroupées en UTC comme dans le backtest (même résultat en NY)."""
    b = m1[list(AGG)].tz_convert("UTC").resample(freq).agg(AGG).dropna(subset=["open"])
    return b.tz_convert(NY)


def atr_wilder(b: pd.DataFrame, n: int = 14, min_periods: int = 0) -> pd.Series:
    pc = b.close.shift()
    tr = pd.concat([b.high - b.low, (b.high - pc).abs(), (b.low - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False, min_periods=min_periods).mean()


def atr15_fin(m1: pd.DataFrame, t: pd.Timestamp, min_periods: int = 0) -> float:
    """ATR(14) de Wilder M15 de la dernière bougie 15 min TERMINÉE à l'instant t (fin de bougie ≤ t)."""
    a = atr_wilder(resample(m1, "15min"), min_periods=min_periods)
    a.index = a.index + pd.Timedelta(minutes=15)
    a = a[a.index <= t]
    return float(a.iloc[-1]) if len(a) else float("nan")


# --------------------------------------------------------------------------- mom


def mom_signe(close_1600: pd.Series, seance: pd.Timestamp) -> tuple[int, float]:
    """Signe du momentum 12-1 appliqué aux nuits qui se terminent à la séance `seance`.

    close_1600 : prix à la clôture de 16:00 ET, indexé par date de séance (une valeur par séance XNYS).
    Pour le mois M de la séance : somme des log-rendements mensuels des mois M-12 à M-2, soit
    log(dernière clôture de M-2 / dernière clôture de M-13). Renvoie (signe, valeur du momentum en log)."""
    s = close_1600.dropna().sort_index()
    fin_mois = s.groupby(s.index.to_period("M")).last()
    m = pd.Timestamp(seance).to_period("M")
    a, z = m - 13, m - 2
    if a not in fin_mois.index or z not in fin_mois.index:
        return 0, float("nan")
    # les 11 mois M-12..M-2 doivent tous être présents (rolling(11, min_periods=11) du backtest)
    if any((m - k) not in fin_mois.index for k in range(2, 14)):
        return 0, float("nan")
    v = float(np.log(fin_mois[z] / fin_mois[a]))
    return int(np.sign(v)), v


# --------------------------------------------------------------------------- 3n


def nuits(m1: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par nuit 20:05 → 03:00 (séance = date du matin), comme run_nq_nuit_3n_vbt.nuits."""
    b5 = resample(m1, "5min")
    d = b5.index.tz_localize(None).normalize() + pd.to_timedelta((b5.index.hour >= 18).astype(int), unit="D")
    t = b5.index.hour * 60 + b5.index.minute
    pos = pd.DataFrame({"pos": np.arange(len(b5)), "session": d})
    ent = pos[(t >= 20 * 60 + 5) & (t <= 20 * 60 + 30)].groupby("session").head(1)
    ext = pos[(t >= 3 * 60) & (t <= 3 * 60 + 30)].groupby("session").head(1)
    n = ent.merge(ext, on="session", suffixes=("_in", "_out"))
    o = b5.open.values
    n["entry_time"], n["exit_time"] = b5.index[n.pos_in], b5.index[n.pos_out]
    n["ret_bps"] = (o[n.pos_out] / o[n.pos_in] - 1) * 1e4
    return n[["session", "entry_time", "exit_time", "ret_bps"]]


def signal_3n(m1: pd.DataFrame, seance: pd.Timestamp) -> tuple[bool, float]:
    """Long la nuit qui se termine à `seance` si la somme des 3 nuits précédentes (complètes) est ≤ 0 bps."""
    n = nuits(m1)
    n = n[n.session < pd.Timestamp(seance).tz_localize(None).normalize()]
    if len(n) < 3:
        return False, float("nan")
    r3 = float(n.ret_bps.iloc[-3:].sum())
    return r3 <= 0, r3


# --------------------------------------------------------------------------- M2


def signal_m2(m1: pd.DataFrame, jour: pd.Timestamp) -> dict:
    """Signal M2 du jour (à calculer après la clôture de la barre 5 min de 9:30, soit à 9:35:00).

    Renvoie side (+1 / -1 / 0), m2 (bool), strength, reversal (bps), atr15 (bougie 9:15-9:30), ret_prev (bps).
    Comme run_nq_ema930_vbt.seances : EMA12 et ATR M5 sur toutes les barres 5 min, Globex compris ; reversal =
    rendement 9:35 → dernière barre ≤ 15:55 de la séance précédente du tableau, signé dans le sens du jour."""
    b5 = resample(m1, "5min")
    jour = pd.Timestamp(jour).tz_localize(None).normalize()
    ema = b5.close.ewm(span=12, adjust=False).mean()
    atr5 = atr_wilder(b5)
    hm = b5.index.hour * 60 + b5.index.minute
    r = pd.DataFrame({"pos": np.arange(len(b5)), "hm": hm, "date": b5.index.tz_localize(None).normalize()})
    r = r[(hm >= 9 * 60 + 30) & (hm <= 15 * 60 + 55)]
    g = r.groupby("date")
    d = pd.DataFrame({"first_hm": g.hm.first(), "sig": g.pos.first(), "z": g.pos.last()})
    out = dict(side=0, m2=False, strength=np.nan, reversal=np.nan, atr15=np.nan, ret_prev=np.nan)
    if jour not in d.index or d.loc[jour, "first_hm"] != 9 * 60 + 30:
        return out
    sig = int(d.loc[jour, "sig"])
    c, o = b5.close.values, b5.open.values
    side = int(np.sign(c[sig] - ema.values[sig]))
    # séances précédentes valides du tableau (9:30 et 9:35 présentes, plus d'une barre)
    prev = d[(d.index < jour) & (d.first_hm == 9 * 60 + 30) & (d.z > d.sig)]
    prev = prev[[hm[int(p) + 1] == 9 * 60 + 35 if int(p) + 1 < len(hm) else False for p in prev.sig]]
    ret_prev = np.nan
    if len(prev):
        e, z = int(prev.sig.iloc[-1]) + 1, int(prev.z.iloc[-1])
        ret_prev = (c[z] / o[e] - 1) * 1e4
    strength = abs(c[sig] - ema.values[sig]) / atr5.values[sig]
    reversal = ret_prev * side
    t_fin = b5.index[sig] + pd.Timedelta(minutes=5)  # 9:35 : dernière bougie 15 min terminée = 9:15-9:30
    out.update(side=side, strength=float(strength), reversal=float(reversal), ret_prev=float(ret_prev),
               atr15=atr15_fin(m1, t_fin),
               m2=bool(side != 0 and ((strength > STR_T) or (reversal < REV_T))))
    return out
