"""N° 26, avenant A : lecture anticipée EXPLORATOIRE des 4 hypothèses sur la fenêtre 2026-08-29 → 2026-11-03.

Pas de verdict (avenant A, commit 9f87d69) : cette fenêtre est désormais « vue » et le holdout officiel commence le
2026-11-04. Compteur 1 738 → 1 742.

uv run python run_holdout_anticipe.py → results/holdout_anticipe/ (run.log, tests.csv, trades_<H>.csv)

Données : Databento NQ.v.0 jusqu'au 2026-08-28, London Strategic Edge (NASDAQ100) à partir du 2026-08-29, même contrat
(septembre) à la jonction. Fichiers raboutés écrits dans results/holdout_anticipe/data/ (hors git avec results/ ? non :
ce dossier est ignoré par cache/ ; voir DATA ci-dessous, dans cache/holdout_anticipe/).
Roulement LSE de septembre : saut open / close précédent > 0,6 % à l'ouverture de Globex (18:00 ET), du 7 au 22.
  - H1 (mom) : barres antérieures ajustées en ratio sur ce saut, puis code figé (recolte1.engine.load, rules.sessions
    prolongé au 2026-11-03, run_recolte1_atr.entries_table / simulate, compte 20:00, SL 2 / TP 5 ATR M15, 9:30).
  - H2 (M2), H3 (3n SL), H4 (rebond) : série non ajustée, code figé (run_nq_ema930_vbt.py, run_nq_nuit_3n_vbt.py).
Tests (unilatéraux, sens attendu > 0) : H1 R net moyen ; H2 $ net moyen par trade ; H3 R net moyen ; H4 rendement net
(1 tick + 5 $) des nuits r3 <= -50 bps moins celui des autres nuits (Welch). t HAC Newey-West 5 retards sauf H4.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/holdout_anticipe")
DATA = Path("cache/holdout_anticipe")
DB = Path("D:/quant-data/Cotations/indices/NQ_v0_1m.parquet")
LSE = Path("cache/lse/NQ_lse_1m.parquet")
JONCTION = pd.Timestamp("2026-08-29", tz="UTC")
FIN = "2026-11-03"
DEBUT_SEANCE = pd.Timestamp("2026-08-31")  # première séance du holdout (lundi)
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def raboute() -> tuple[Path, Path, pd.Timestamp | None, float]:
    """Écrit la série brute raboutée et la série ajustée au roulement LSE de septembre."""
    db = pd.read_parquet(DB)
    lse = pd.read_parquet(LSE)
    db = db[~db.index.duplicated()].sort_index()
    lse = lse[~lse.index.duplicated()].sort_index()
    raw = pd.concat([db[db.index < JONCTION], lse[lse.index >= JONCTION][db.columns]])
    a = db[db.index < JONCTION].iloc[-1]
    b = lse[lse.index < JONCTION].iloc[-1] if (lse.index < JONCTION).any() else None
    if b is not None:
        say(f"Jonction : dernier close Databento {a.close} ({db.index[db.index < JONCTION][-1]}), "
            f"LSE {b.close} ({lse.index[lse.index < JONCTION][-1]}), écart {(b.close / a.close - 1) * 1e4:+.1f} bps")
    # roulement LSE : ouverture de Globex (barre précédente > 50 min avant) du 7 au 22 septembre, saut > 0,6 %
    h = raw[raw.index >= JONCTION]
    ix = h.index
    gap_t = pd.Series(ix, index=ix).diff() > pd.Timedelta(minutes=50)
    jump = (h.open / h.close.shift() - 1)
    loc = ix.tz_convert("America/New_York")
    cand = gap_t.values & (loc.month == 9) & (loc.day >= 7) & (loc.day <= 22) & (jump.abs().values > 0.006)
    roll_t, roll_g = None, 0.0
    if cand.any():
        roll_t = ix[cand][np.argmax(np.abs(jump.values[cand]))]
        roll_g = float(jump.loc[roll_t])
        say(f"Roulement LSE détecté : {roll_t.tz_convert('America/New_York')} ET, saut {roll_g * 1e4:+.1f} bps "
            f"({int(cand.sum())} candidat(s))")
    else:
        say("Aucun roulement LSE détecté en septembre (règle de l'avenant A)")
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "brut").mkdir(exist_ok=True)
    (DATA / "ajuste" / "indices").mkdir(parents=True, exist_ok=True)
    p_raw = DATA / "brut" / "NQ_v0_1m.parquet"
    raw.to_parquet(p_raw)
    adj = raw.copy()
    if roll_t is not None:
        adj.loc[adj.index < roll_t, ["open", "high", "low", "close"]] *= 1 + roll_g
    p_adj = DATA / "ajuste" / "indices" / "NQ_v0_1m.parquet"
    adj.to_parquet(p_adj)
    return p_raw, p_adj, roll_t, roll_g


def t_hac(x: np.ndarray) -> tuple[float, float, float]:
    from run_nq_nuit_r3_pente import hac_ols
    m, t = hac_ols(np.asarray(x, float), None)
    return m, t, float(stats.norm.sf(t))


def h1_mom(p_adj: Path) -> pd.DataFrame:
    """Règle NQ de nuit figée (compte 20:00), même enchaînement que run_prereg10 / run_nq_nuit_heures."""
    import recolte1.engine as eng
    import recolte1.rules as rules
    keep = Path("results/recolte1_atr/run.log")
    backup = keep.read_bytes() if keep.exists() else None
    import run_recolte1_atr as A  # ouvre (et vide) results/recolte1_atr/run.log : restauré juste après
    if backup is not None:
        keep.write_bytes(backup)
    eng.DATA = p_adj.parent.parent
    eng.load.cache_clear()
    rules.END = FIN
    rules.sessions.cache_clear()
    rules.base.cache_clear()
    A.VARIANTS = [("SL 2 ATR / TP 5 ATR", 2.0, 5.0)]
    b = rules.sessions()
    bb = rules.base("NQ")
    s = rules.next_month_sign(bb, rules.monthly(bb, "cc").shift(1).rolling(11, min_periods=11).sum())
    w = pd.DataFrame({"t_start": b["t_prev"], "t_end": b["t_open"], "dir": s.reindex(b.index).fillna(0.0)})
    A.windows = lambda rule: ("NQ", w)
    _, e = A.entries_table("holdout")
    e = e[(e["clock"] == "20:00") & (pd.DatetimeIndex(e["night"]) >= DEBUT_SEANCE)]
    T = A.simulate("NQ", e)
    T = T[T.cost == "net"].copy()
    df = eng.load("NQ").copy()
    df.attrs = {}
    atr = A.atr_m15(df)
    idx = df.index.as_unit("ns")
    t_in = idx[T.entry_idx.values]
    frac = atr.reindex(pd.DatetimeIndex(t_in).as_unit("ns"), method="ffill").values / df.close.values[T.entry_idx.values]
    T["R"] = T.ret.values / (2 * frac)
    sig = s.reindex(b.index)
    say("Signe du momentum 12-1 par mois (holdout) : "
        + ", ".join(f"{p} {int(v):+d}" for p, v in sig[sig.index >= DEBUT_SEANCE].groupby(
            sig[sig.index >= DEBUT_SEANCE].index.to_period("M")).first().items()))
    return T


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    p_raw, p_adj, roll_t, roll_g = raboute()
    rows = []

    # H1
    T1 = h1_mom(p_adj)
    T1.to_csv(OUT / "trades_H1_mom.csv", index=False)
    m, t, p = t_hac(T1.R.values)
    rows.append(dict(H="H1 mom (R net / nuit)", n=len(T1), moyenne=m, t=t, p=p))
    say(f"H1 : {len(T1)} nuits, longs {int((T1.dir > 0).sum())}, shorts {int((T1.dir < 0).sum())}, "
        f"sorties {T1.reason.value_counts().to_dict()}, R total {T1.R.sum():+.2f}")

    # H2, H3, H4 sur la série brute raboutée
    import run_nq_ema930_vbt as E
    import run_nq_nuit_3n_vbt as B
    B.SRC, B.END = p_raw, pd.Timestamp("2026-11-04", tz="America/New_York")
    b5, b15 = B.bars()

    d = E.seances(b5, b15)
    d = d[pd.to_datetime(d.date) >= DEBUT_SEANCE].reset_index(drop=True)
    tr2 = E.portefeuille(b5, d)
    m2 = tr2["M2"]
    m2.to_csv(OUT / "trades_H2_M2.csv", index=False)
    m, t, p = t_hac(m2.pnl.values)
    rows.append(dict(H="H2 M2 ($ net / trade, 1 NQ)", n=len(m2), moyenne=m, t=t, p=p))
    say(f"H2 : {len(d)} séances, {len(m2)} trades M2 (longs {int((m2.side > 0).sum())}), net {m2.pnl.sum():+,.0f} $, "
        f"{(m2.pnl / (20 * m2.entry_px)).mean() * 1e4:+.1f} bps/trade ; C (tous les jours) {tr2['C'].pnl.mean():+.1f} $/trade")

    n = B.nuits(b5, b15)
    n = n[n.session >= DEBUT_SEANCE].reset_index(drop=True)
    if roll_t is not None:
        inside = (n.entry_time <= roll_t) & (n.exit_time >= roll_t)
        say(f"Nuits contenant le roulement LSE : {int(inside.sum())} (exclues)")
        n = n[~inside].reset_index(drop=True)
    pf = B.portefeuille(b5, n)
    rec = pf["3n 03h SL"].trades.records_readable
    sel = n[n.sig3n].reset_index(drop=True)
    t3 = pd.DataFrame({"session": sel.session, "pnl": rec["PnL"].values, "dist": sel.dist})
    t3["R"] = t3.pnl / (t3.dist * B.PV)
    t3.to_csv(OUT / "trades_H3_3n.csv", index=False)
    m, t, p = t_hac(t3.R.values) if len(t3) > 1 else (np.nan, np.nan, np.nan)
    rows.append(dict(H="H3 3n SL (R net / trade)", n=len(t3), moyenne=m, t=t, p=p))
    say(f"H3 : {len(n)} nuits, {len(t3)} trades 3n, net {t3.pnl.sum():+,.0f} $ (15 $ l'aller-retour)")

    cost_bps = 10.0 / (20 * n.entry_px) * 1e4
    net = n.ret_bps - cost_bps
    reb = (n.r3_bps <= -50).values
    x, y = net[reb].values, net[~reb].values
    if len(x) >= 2:
        w = stats.ttest_ind(x, y, equal_var=False, alternative="greater")
        tt, pp = w.statistic, w.pvalue
    else:
        tt = pp = np.nan
    n.assign(net_bps=net, rebond=reb).to_csv(OUT / "trades_H4_rebond.csv", index=False)
    rows.append(dict(H="H4 rebond r3 ≤ −50 bps − autres (bps net)", n=len(x), moyenne=np.mean(x) - np.mean(y) if len(x) else np.nan,
                     t=tt, p=pp))
    say(f"H4 : {len(x)} nuits r3 ≤ −50 bps ({np.mean(x) if len(x) else np.nan:+.1f} bps net), "
        f"{len(y)} autres nuits ({np.mean(y):+.1f} bps net)")

    res = pd.DataFrame(rows)
    res.to_csv(OUT / "tests.csv", index=False)
    say("\n===== Lecture anticipée EXPLORATOIRE 2026-08-31 → 2026-11-03 (sans verdict, avenant A du n° 26) =====")
    say(res.round(4).to_string(index=False))
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
