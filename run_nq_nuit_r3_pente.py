"""Question (2026-11-03) : plus la somme des rendements des 3 nuits précédentes est positive (et loin de 0), plus la
nuit suivante baisse-t-elle ? Nuit = 20:05 -> 03:00 ET (open à open), comme la stratégie transmise 3n.

EXPLORATOIRE (non pré-enregistré). Compteur global 1 695 -> 1 719 : 24 tests dans la famille Holm (ci-dessous).
NQ 2016-2026 est l'échantillon où le filtre 3n a été trouvé : il ne peut pas confirmer. Les vrais tests sont
NQ 2010-2015 (jamais utilisé pour ce signal) et ES / YM (autres actifs).

uv run python run_nq_nuit_r3_pente.py → results/nq_nuit_r3_pente/ (run.log, tests.csv, quintiles.csv, nuits_<échantillon>.csv)

Signal r3 = somme des rendements (bps) des 3 nuits précédentes, connue à 20:05. Variante « 72 h » : rendement de
l'open de 20:05 trois séances plus tôt à l'open de 20:05 du jour (nuits ET journées), prix ajustés en ratio aux
roulements (règle de run_sessions.py : un roulement par mois d'échéance, plus grand saut à 00:00 UTC entre le 7 et le
22). Les nuits 20:05 -> 03:00 ne contiennent pas de roulement (00:00 UTC = 19:00 ou 20:00 NY).
Tests (statistique t avec écart-type HAC Newey-West, 5 retards) sur les nuits où le signal est > 0 seulement :
  T1 pente : rendement de la nuit ~ r3 (une pente < 0 = « plus r3 est haut, plus la nuit baisse ») ;
  T2 niveau : rendement moyen des nuits du tercile haut de r3 > 0 (< 0 = la nuit baisse vraiment, pas seulement moins) ;
  T3 pente normalisée : (rendement / sigma) ~ (r3 / sigma), sigma = écart-type des 60 nuits précédentes ;
  T4 pente « 72 h » : rendement de la nuit ~ r72 sur r72 > 0.
4 tests x 6 échantillons = 24, Holm sur la famille (unilatéral, sens attendu < 0).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import run_nq_nuit_3n_vbt as B

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/nq_nuit_r3_pente")
D16, D10 = Path("D:/quant-data/Cotations/indices"), Path("cache/databento_2010")
ECHANTILLONS = {  # nom : (fichier, découverte ?)
    "NQ 2016-2026": (D16 / "NQ_v0_1m.parquet", True),
    "NQ 2010-2015": (D10 / "NQ_v0_1m_2010.parquet", False),
    "ES 2016-2026": (D16 / "ES_v0_1m.parquet", False),
    "ES 2010-2015": (D10 / "ES_v0_1m_2010.parquet", False),
    "YM 2016-2026": (D16 / "YM_v0_1m.parquet", False),
    "YM 2010-2015": (D10 / "YM_v0_1m_2010.parquet", False),
}
LAGS = 5
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def hac_ols(y: np.ndarray, x: np.ndarray | None) -> tuple[float, float]:
    """Coefficient (pente si x, sinon moyenne) et t HAC Newey-West (Bartlett, LAGS retards)."""
    X = np.ones((len(y), 1)) if x is None else np.column_stack([np.ones(len(y)), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    u = (y - X @ b)[:, None] * X
    S = u.T @ u
    for k in range(1, LAGS + 1):
        G = u[k:].T @ u[:-k]
        S += (1 - k / (LAGS + 1)) * (G + G.T)
    XtXi = np.linalg.inv(X.T @ X)
    V = XtXi @ S @ XtXi
    j = X.shape[1] - 1
    return float(b[j]), float(b[j] / np.sqrt(V[j, j]))


def facteur_roulements(b5: pd.DataFrame) -> pd.Series:
    """Facteur multiplicatif (ajustement en ratio) des barres 5 min, règle de run_sessions.load."""
    ix = b5.index.tz_convert("UTC")
    gap = pd.Series(b5.open.values / b5.close.shift().values - 1, index=ix)
    prev = pd.Series(ix, index=ix).shift()
    cand = (ix.hour == 0) & (ix.minute == 0) & ((ix - prev) <= pd.Timedelta(minutes=60)).values
    cand &= ix.month.isin([3, 6, 9, 12]) & (ix.day >= 7) & (ix.day <= 22)
    g = gap[cand]
    rolls = pd.DatetimeIndex(g.abs().groupby([g.index.year, g.index.month]).idxmax().tolist())
    step = pd.Series(1.0, index=ix)
    step.loc[rolls] = 1 + gap.loc[rolls]
    return pd.Series(step[::-1].cumprod()[::-1].shift(-1).fillna(1.0).values, index=b5.index)


def nuits(src: Path) -> pd.DataFrame:
    B.SRC = src
    b5, b15 = B.bars()
    n = B.nuits(b5, b15)[["session", "pos_in", "entry_time", "exit_time", "entry_px", "ret_bps", "r3_bps", "year"]]
    f = facteur_roulements(b5).values
    adj = b5.open.values[n.pos_in.values] * f[n.pos_in.values]
    n["r72_bps"] = (adj / pd.Series(adj).shift(3).values - 1) * 1e4
    n["sigma"] = n.ret_bps.shift(1).rolling(60).std()
    return n.dropna(subset=["r3_bps"]).reset_index(drop=True)


def analyse(nom: str, n: pd.DataFrame) -> tuple[list[dict], pd.DataFrame]:
    y = n.ret_bps.values
    pos = n.r3_bps.values > 0
    tests = []
    b, t = hac_ols(y[pos], n.r3_bps.values[pos])
    tests.append(dict(test="T1 pente r3>0 (bps par 100 bps de r3)", coef=100 * b, t=t))
    hi = pos & (n.r3_bps.values >= np.quantile(n.r3_bps.values[pos], 2 / 3))
    m, t = hac_ols(y[hi], None)
    tests.append(dict(test="T2 nuit moyenne, tercile haut de r3>0 (bps)", coef=m, t=t))
    ok = pos & n.sigma.notna().values
    b, t = hac_ols((n.ret_bps / n.sigma).values[ok], (n.r3_bps / n.sigma).values[ok])
    tests.append(dict(test="T3 pente normalisée r3/sigma>0", coef=b, t=t))
    ok = (n.r72_bps.values > 0) & n.r72_bps.notna().values
    b, t = hac_ols(y[ok], n.r72_bps.values[ok])
    tests.append(dict(test="T4 pente r72>0 (bps par 100 bps)", coef=100 * b, t=t))
    for d in tests:
        d.update(échantillon=nom, p=stats.norm.cdf(d["t"]))  # unilatéral, sens attendu < 0

    # descriptif
    b_all, t_all = hac_ols(y, n.r3_bps.values)
    b_neg, t_neg = hac_ols(y[~pos], n.r3_bps.values[~pos])
    m_pos, tm_pos = hac_ols(y[pos], None)
    m_all, _ = hac_ols(y, None)
    rho, p_rho = stats.spearmanr(n.r3_bps.values[pos], y[pos])
    w = np.clip(y, *np.quantile(y, [0.01, 0.99]))
    b_w, t_w = hac_ols(w[pos], n.r3_bps.values[pos])
    say(f"\n===== {nom} : {len(n)} nuits ({n.entry_time.iloc[0]:%Y-%m-%d} -> {n.exit_time.iloc[-1]:%Y-%m-%d}), "
        f"r3 > 0 : {pos.sum()} =====")
    say(f"Nuit moyenne : toutes {m_all:+.2f} bps | r3 > 0 : {m_pos:+.2f} (t {tm_pos:+.2f}) | r3 <= 0 : {y[~pos].mean():+.2f}")
    say(f"Pente sur tout r3 : {100 * b_all:+.2f} bps / 100 bps (t {t_all:+.2f}) | côté r3 <= 0 : {100 * b_neg:+.2f} "
        f"(t {t_neg:+.2f}) | côté r3 > 0 : {tests[0]['coef']:+.2f} (t {tests[0]['t']:+.2f}) ; winsorisé 1 % : "
        f"{100 * b_w:+.2f} (t {t_w:+.2f}) ; Spearman r3 > 0 : {rho:+.3f} (p {p_rho:.3f})")
    q = pd.qcut(n.r3_bps, 10, labels=False)
    tab = n.groupby(q).agg(r3_min=("r3_bps", "min"), r3_max=("r3_bps", "max"), nuits=("ret_bps", "size"),
                           nuit_bps=("ret_bps", "mean"), hausse_pct=("ret_bps", lambda s: 100 * (s > 0).mean()))
    tab["t"] = [hac_ols(n.ret_bps.values[(q == k).values], None)[1] for k in tab.index]
    tab.index = [f"D{k + 1}" for k in tab.index]
    say(f"Déciles de r3 (D10 = r3 le plus haut) :\n{tab.round(2).to_string()}")
    per = []
    for a, z in [(2010, 2015), (2016, 2021), (2022, 2024), (2025, 2026)]:
        s = n[n.year.between(a, z)]
        if len(s) > 100:
            p = s.r3_bps.values > 0
            bb, tt = hac_ols(s.ret_bps.values[p], s.r3_bps.values[p])
            per.append(f"{a}-{z} : {100 * bb:+.2f} (t {tt:+.2f}, {p.sum()} nuits)")
    say("Pente côté r3 > 0 par sous-période : " + " | ".join(per))
    tab.insert(0, "échantillon", nom)
    return tests, tab


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    allt, alltab = [], []
    for nom, (src, _) in ECHANTILLONS.items():
        n = nuits(src)
        n.to_csv(OUT / f"nuits_{nom.replace(' ', '_')}.csv", index=False)
        t, tab = analyse(nom, n)
        allt += t
        alltab.append(tab)
    res = pd.DataFrame(allt)
    order = np.argsort(res.p.values)
    holm = np.empty(len(res))
    holm[order] = np.minimum(1, np.maximum.accumulate((len(res) - np.arange(len(res))) * res.p.values[order]))
    res["p Holm"] = holm
    res["découverte"] = res["échantillon"].map(lambda s: ECHANTILLONS[s][1])
    res.to_csv(OUT / "tests.csv", index=False)
    pd.concat(alltab).to_csv(OUT / "quintiles.csv")
    say("\n===== Tests (unilatéraux, sens attendu < 0), Holm sur 24 =====")
    say(res.pivot_table(index="échantillon", columns="test", values=["coef", "t", "p Holm"], sort=False)
        .swaplevel(axis=1).sort_index(axis=1, level=0).round(3).to_string())
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
