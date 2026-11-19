"""Bibliothèque de nuits de la règle NQ de nuit pour les moteurs de prop firms (comme propfirm/days.py, mais la nuit).

Nuits de run_propfirm_vbt.nights("20:00") : entrée à la clôture de la barre de 20:00 ET, sortie au plus tard à la clôture
de la barre de 9:29, stop 2 ATR M15. Pour chaque nuit, chaque sens et deux variantes de sortie (0 : normale ;
1 : à plat à 8:19 ET les jours d'annonce 8:30 de config/calendrier_macro_us.csv), on garde en barres depuis l'entrée :
la barre où le stop est touché, la barre où chaque objectif k × stop est touché (k = 0,05 … 6 R), le R perdu au stop
(pire du stop et de l'ouverture de la barre), le R de sortie et le plus haut R latent avant le stop / sur toute la
nuit (pour les pertes max suiveuses en séance).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

K_STEP, K_N = 0.05, 120
NEVER = np.iinfo(np.int16).max
CACHE = Path("cache/propfirm/nights_lib.npz")


@dataclass
class NightLib:
    dates: pd.DatetimeIndex
    dir: np.ndarray       # [n] sens de la règle (+1 / −1)
    s: np.ndarray         # [n] stop en fraction du prix
    cost: np.ndarray      # [n] coût par MNQ aller-retour ($)
    tp_bar: np.ndarray    # [2 variantes, n, 2 sens, K_N] int16
    stop_bar: np.ndarray  # [2, n, 2] int16
    stop_R: np.ndarray    # [2, n, 2]
    eod_R: np.ndarray     # [2, n, 2]
    mfe_stop: np.ndarray  # [2, n, 2] plus haut R latent avant la barre du stop
    mfe_all: np.ndarray   # [2, n, 2] plus haut R latent sur la nuit

    @property
    def n(self) -> int:
        return len(self.dates)


def _side(x, O, Hh, L, C, s, sign, levels):
    if sign > 0:
        fav, adv, aop, end = (Hh - x) / x, (x - L) / x, (x - O) / x, (C[-1] - x) / x
    else:
        fav, adv, aop, end = (x - L) / x, (Hh - x) / x, (O - x) / x, (x - C[-1]) / x
    hit = np.flatnonzero(adv >= s)
    if len(hit):
        j = int(hit[0]); sb, sr = j, max(1.0, aop[j] / s)
        ms = fav[:j].max() / s if j > 0 else 0.0
    else:
        sb, sr = NEVER, 1.0
        ms = fav.max() / s
    cm = np.maximum.accumulate(fav)
    tp = np.searchsorted(cm, levels * s, side="left")
    tp = np.where(tp >= len(fav), NEVER, tp).astype(np.int16)
    return tp, sb, sr, end / s, max(ms, 0.0), max(fav.max() / s, 0.0)


def build() -> NightLib:
    if CACHE.exists():
        z = np.load(CACHE, allow_pickle=True)
        d = {k: z[k] for k in z.files}
        d["dates"] = pd.DatetimeIndex(d["dates"])
        return NightLib(**d)
    import run_propfirm_vbt as V
    from recolte1.engine import load

    df = load("NQ").copy()
    df.attrs = {}
    e, _ = V.nights("20:00", df)
    cal = pd.read_csv("config/calendrier_macro_us.csv", parse_dates=["date"])
    news = set(cal.loc[cal.heure_ET == "08:30", "date"].dt.normalize())
    on = e.night.dt.normalize().isin(news).to_numpy()
    t19 = pd.to_datetime(e.night.dt.strftime("%Y-%m-%d") + " 08:19").dt.tz_localize(V.NY).dt.tz_convert("UTC")
    p19 = V.A.bar_pos(df.index.as_unit("ns"), t19)
    p_out2 = np.where(on & (p19 > e.p_in.to_numpy()), p19, e.p_out.to_numpy())
    O, Hh, L, C = (df[c].to_numpy() for c in ("open", "high", "low", "close"))
    levels = K_STEP * np.arange(1, K_N + 1)
    n = len(e)
    s = 2 * e.atr_frac.to_numpy()
    tp = np.empty((2, n, 2, K_N), np.int16); sb = np.empty((2, n, 2), np.int16)
    sr, er, ms, ma = (np.empty((2, n, 2)) for _ in range(4))
    for v, pout in enumerate((e.p_out.to_numpy(), p_out2)):
        for i, (a, b) in enumerate(zip(e.p_in.to_numpy(), pout)):
            sl = slice(a + 1, b + 1)
            for k, sign in enumerate((1, -1)):
                tp[v, i, k], sb[v, i, k], sr[v, i, k], er[v, i, k], ms[v, i, k], ma[v, i, k] = _side(
                    C[a], O[sl], Hh[sl], L[sl], C[sl], s[i], sign, levels)
    cost = pd.read_parquet("cache/propfirm/lucid_trades.parquet").set_index("night")["cost"]
    out = dict(dates=e.night.to_numpy(), dir=e.dir.to_numpy(), s=s,
               cost=cost.reindex(e.night.values).fillna(2.0).to_numpy(), tp_bar=tp, stop_bar=sb, stop_R=sr,
               eod_R=er, mfe_stop=ms, mfe_all=ma)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez(CACHE, **out)
    out["dates"] = pd.DatetimeIndex(out["dates"])
    return NightLib(**out)
