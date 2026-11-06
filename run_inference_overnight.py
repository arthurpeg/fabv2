"""Inférence des chiffres overnight : t HAC, dépendance, N effectif, DSR (exploratoire).

Méthodes fixées avant le calcul (2026-11-06) :

A. Séries testées (toutes <= 2026-08-28, rien du holdout) :
   - ES, NQ, YM : rendements journaliers close-to-open, Asie, US (results/sessions/sessions_<A>.csv) ;
   - mom 2016-2026 : NQ, entrée 20:00, SL 2 / TP 5 ATR, net, règle [19] (results/recolte1_atr/trades.parquet) ;
   - mom OOS 2011-2015 : NQ 20:00 net, en R (results/prereg11/trades.csv).
B. Pour chaque série : moyenne, t iid, t HAC Newey-West (noyau de Bartlett) à 5 retards et à
   floor(4 (T/100)^(2/9)) retards, p bilatéral normal, p par bootstrap circulaire par blocs de 10
   (2 000 tirages, graine 0, série centrée), autocorrélation d'ordre 1, Ljung-Box à 5 et 10 retards
   sur r et sur r², ARCH-LM à 5 retards (T · R² de r² sur ses 5 retards), kurtosis en excès.
C. N effectif : séries journalières nettes de tous les essais sauvegardés (results/daily_net.parquet,
   results/replications_daily_net.parquet, recolte1_atr net par actif × heure × variante × règle),
   jours sans trade = 0, fenêtre 2016-01-04 → 2026-08-28, séries constantes retirées.
   Matrice de corrélation de Pearson. Méthode principale : Li & Ji (2005), Meff = Σ f(|λ|),
   f(x) = 1{x >= 1} + (x − floor(x)). Contrôles : Nyholt (2004), nombre de valeurs propres pour 95 %
   de la variance. N effectif global extrapolé = (Meff / M) × 1 742 (hypothèse : les essais non
   sauvegardés sont aussi redondants que ceux qui le sont).
D. DSR (Bailey & López de Prado) : SR0 = sqrt(V) · ((1 − γ) Φ⁻¹(1 − 1/N) + γ Φ⁻¹(1 − 1/(N e))),
   V = variance des Sharpe journaliers des séries sauvegardées ; DSR calculé pour N = 1 742 et pour
   le N effectif extrapolé, sur mom 2016-2026 et sur NQ close-to-open.

Ce script ne teste aucune règle nouvelle : il ne change pas le compteur d'essais.
Lancer : uv run python run_inference_overnight.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/inference_overnight")
OUT.mkdir(parents=True, exist_ok=True)
N_GLOBAL = 1742
START, END = "2016-01-04", "2026-08-28"
RNG = np.random.default_rng(0)


# ------------------------------------------------------------------ outils
def nw_se(x: np.ndarray, lags: int) -> float:
    """Erreur type HAC de la moyenne (Newey-West, Bartlett)."""
    e = x - x.mean()
    T = len(e)
    s = e @ e / T
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1)
        s += 2 * w * (e[k:] @ e[:-k]) / T
    return math.sqrt(s / T)


def ljung_box(x: np.ndarray, lags: int) -> tuple[float, float]:
    e = x - x.mean()
    T = len(e)
    d = e @ e
    q = sum((e[k:] @ e[:-k] / d) ** 2 / (T - k) for k in range(1, lags + 1)) * T * (T + 2)
    return float(q), float(stats.chi2.sf(q, lags))


def arch_lm(x: np.ndarray, lags: int = 5) -> tuple[float, float]:
    y = (x - x.mean()) ** 2
    Y = y[lags:]
    X = np.column_stack([np.ones(len(Y))] + [y[lags - k:-k] for k in range(1, lags + 1)])
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    r2 = 1 - ((Y - X @ beta) ** 2).sum() / ((Y - Y.mean()) ** 2).sum()
    lm = len(Y) * r2
    return float(lm), float(stats.chi2.sf(lm, lags))


def block_boot_p(x: np.ndarray, block: int = 10, n: int = 2000) -> float:
    """p bilatéral : bootstrap circulaire par blocs de la série centrée."""
    T = len(x)
    xc = x - x.mean()
    nb = math.ceil(T / block)
    starts = RNG.integers(0, T, size=(n, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(n, -1)[:, :T] % T
    m = xc[idx].mean(axis=1)
    return float((np.abs(m) >= abs(x.mean())).mean())


def describe(name: str, x: np.ndarray, unit: str, scale: float) -> dict:
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    T = len(x)
    auto = int(math.floor(4 * (T / 100) ** (2 / 9)))
    se_iid = x.std(ddof=1) / math.sqrt(T)
    t_iid = x.mean() / se_iid
    t5 = x.mean() / nw_se(x, 5)
    ta = x.mean() / nw_se(x, auto)
    lb5, plb5 = ljung_box(x, 5)
    lb10, plb10 = ljung_box(x, 10)
    lbs5, plbs5 = ljung_box(x ** 2, 5)
    lbs10, plbs10 = ljung_box(x ** 2, 10)
    lm, plm = arch_lm(x, 5)
    e = x - x.mean()
    return {
        "série": name, "unité": unit, "n": T, "moyenne": x.mean() * scale,
        "t_iid": t_iid, "p_iid": 2 * stats.norm.sf(abs(t_iid)),
        "t_NW5": t5, "p_NW5": 2 * stats.norm.sf(abs(t5)),
        "retards_auto": auto, "t_NWauto": ta, "p_NWauto": 2 * stats.norm.sf(abs(ta)),
        "p_bloc10": block_boot_p(x),
        "rho1": (e[1:] @ e[:-1]) / (e @ e),
        "LB5_p": plb5, "LB10_p": plb10, "LB5_r2_p": plbs5, "LB10_r2_p": plbs10,
        "ARCH5": lm, "ARCH5_p": plm, "kurt_excès": stats.kurtosis(x),
        "skew": stats.skew(x),
    }


# ------------------------------------------------------------------ A-B : séries
rows = []
for a in ["NQ", "ES", "YM"]:
    s = pd.read_csv(f"results/sessions/sessions_{a}.csv", index_col=0, parse_dates=True)
    for col, lab in [("close_to_open", "close-to-open"), ("asia", "Asie"), ("us", "US")]:
        rows.append(describe(f"{a} {lab} 2016-2026", s[col].dropna().values, "bp/jour", 1e4))

tr = pd.read_parquet("results/recolte1_atr/trades.parquet")
net = tr[tr.cost == "net"].copy()
mom = net[(net.asset == "NQ") & (net.clock == "20:00") & (net.variant == "SL 2 ATR / TP 5 ATR")
          & net.rule.str.startswith("[19]")]
mom_ret = mom.groupby("night").ret.sum().sort_index()
rows.append(describe("mom NQ 2016-2026 (rendement)", mom_ret.values, "bp/nuit", 1e4))

p11 = pd.read_csv("results/prereg11/trades.csv")
p11 = p11[(p11.asset == "NQ") & (p11.clock == "20:00") & (p11.cost == "net")]
rows.append(describe("mom NQ OOS 2011-2015 (R)", p11.R.values, "R/trade", 1.0))

inf = pd.DataFrame(rows)
inf.to_csv(OUT / "inference.csv", index=False)

# ------------------------------------------------------------------ C : N effectif
series = {}
for f in ["results/daily_net.parquet", "results/replications_daily_net.parquet"]:
    d = pd.read_parquet(f)
    for c in d.columns:
        series[f"{Path(f).stem}:{c}"] = d[c]
for key, g in net.groupby(["asset", "clock", "variant", "rule"]):
    series["recolte1_atr:" + "|".join(key)] = g.groupby("night").ret.sum()

dates = pd.bdate_range(START, END)
M = pd.DataFrame({k: v.groupby(pd.to_datetime(v.index).normalize()).sum() for k, v in series.items()})
M = M.reindex(dates).fillna(0.0)
M = M.loc[:, M.std() > 0]
m = M.shape[1]
C = np.corrcoef(M.values.T)
lam = np.clip(np.linalg.eigvalsh(C), 0, None)[::-1]
meff_liji = float(np.sum((lam >= 1).astype(float) + (lam - np.floor(lam))))
meff_nyholt = float(1 + (m - 1) * (1 - np.var(lam, ddof=1) / m))
n95 = int(np.searchsorted(np.cumsum(lam) / lam.sum(), 0.95) + 1)
abs_off = np.abs(C[np.triu_indices(m, 1)])
ratio = meff_liji / m
n_eff = ratio * N_GLOBAL

srs = M.mean() / M.std()
V = float(srs.var(ddof=1))


def sr0(N: float, v: float | None = None) -> float:
    g = 0.5772156649
    return math.sqrt(V if v is None else v) * ((1 - g) * stats.norm.ppf(1 - 1 / N) + g * stats.norm.ppf(1 - 1 / (N * math.e)))


def dsr(x: np.ndarray, N: float, v: float | None = None) -> float:
    x = x[np.isfinite(x)]
    sr = x.mean() / x.std(ddof=1)
    sk, ku = stats.skew(x), stats.kurtosis(x, fisher=False)
    return float(stats.norm.cdf((sr - sr0(N, v)) * math.sqrt(len(x) - 1)
                                / math.sqrt(1 - sk * sr + (ku - 1) / 4 * sr ** 2)))


mom_daily = mom_ret.groupby(pd.to_datetime(mom_ret.index).normalize()).sum().reindex(dates).fillna(0.0)
nq = pd.read_csv("results/sessions/sessions_NQ.csv", index_col=0, parse_dates=True)["close_to_open"].dropna()
dsr_rows = []
for name, x in [("mom NQ 2016-2026", mom_daily.values), ("NQ close-to-open 2016-2026", nq.values)]:
    for lab, N in [("N brut 1 742", N_GLOBAL), (f"N effectif ≈ {n_eff:.0f}", n_eff), (f"N = M sauvegardées ({m})", m)]:
        dsr_rows.append({"série": name, "N": lab, "N_val": N, "SR_jour": x.mean() / x.std(ddof=1),
                         "SR_an": x.mean() / x.std(ddof=1) * math.sqrt(252), "SR0_jour": sr0(N),
                         "SR0_an": sr0(N) * math.sqrt(252), "DSR": dsr(x, N),
                         # contrôle ajouté APRÈS le premier calcul : V sous H0 = 1/(T-1)
                         # (dispersion d'échantillonnage seule, sans les vraies différences entre essais)
                         "SR0_an_V0": sr0(N, 1 / (len(dates) - 1)) * math.sqrt(252),
                         "DSR_V0": dsr(x, N, 1 / (len(dates) - 1))})
dsr_df = pd.DataFrame(dsr_rows)
dsr_df.to_csv(OUT / "dsr.csv", index=False)

meff = pd.DataFrame([{
    "séries_sauvegardées": m, "Meff_LiJi": meff_liji, "Meff_Nyholt": meff_nyholt, "n_vp_95pct": n95,
    "ratio_LiJi": ratio, "N_global": N_GLOBAL, "N_effectif_extrapolé": n_eff,
    "corr_abs_médiane": float(np.median(abs_off)), "part_corr_abs>0.5": float((abs_off > 0.5).mean()),
    "V_SR_jour": V, "vp_max": float(lam[0]),
}])
meff.to_csv(OUT / "n_effectif.csv", index=False)

pd.set_option("display.width", 250, "display.max_columns", 40, "display.float_format", "{:.4g}".format)
print("== B. Inférence ==")
print(inf.to_string(index=False))
print("\n== C. N effectif ==")
print(meff.T.to_string(header=False))
print("\n== D. DSR ==")
print(dsr_df.to_string(index=False))
