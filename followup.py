"""Tests pré-enregistrés dans PREREGISTRATION_2.md (pistes A et B)."""

from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats

from fab.core import ASSETS, IS_END, backtest, sharpe
from fab.strategies import _with_session, gap_z, m4b_gap_fade

rng = np.random.default_rng(20261012)
N_TRIALS = 96
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)


# =========================================================================== A
say("## A. Fade de gap — indices\n")
daily, trade_rets = {}, []
for n in ["ES", "NQ", "YM"]:
    a = ASSETS[n]
    t, tz, dates = _with_session(a, lambda g: m4b_gap_fade(a, g, zmin=1, zmax=2))
    daily[n] = backtest("A1", a, t, tz, dates).daily_net
    # trades poolés |z|>1 pour A2/A3 (rendement net par trade)
    tt, _, _ = _with_session(a, lambda g: m4b_gap_fade(a, g, zmin=1))
    zz = _with_session(a, lambda g: gap_z(a, g))[0]
    cost = a.rt_cost * tt["f_in"] / tt["p_in"]
    tt = tt.assign(asset=n, ret=(tt["p_out"] / tt["p_in"] - 1) * tt["dir"] - cost,
                   absz=zz.reindex(tt["date"]).abs().values)
    trade_rets.append(tt)

port = pd.DataFrame(daily).fillna(0).mean(axis=1)
is_m, oos_m = port.index <= IS_END, port.index > IS_END
say(f"A1 — gaps 1<|z|≤2 (jours jamais tradés), portefeuille ES/NQ/YM : "
    f"Sharpe net IS={sharpe(port[is_m]):+.2f}  OOS={sharpe(port[oos_m]):+.2f}")
for n, r in daily.items():
    say(f"     {n}: IS={sharpe(r[r.index <= IS_END]):+.2f}  OOS={sharpe(r[r.index > IS_END]):+.2f}")
a1 = sharpe(port[oos_m]) > 0.5

T = pd.concat(trade_rets)
T["post"] = pd.to_datetime(T["date"]) > IS_END
pre, post = T.loc[~T.post, "ret"], T.loc[T.post, "ret"]
tstat, p2 = stats.ttest_ind(post, pre, equal_var=False, alternative="greater")
say(f"A2 — trades |z|>1 poolés : moyenne pré-2023={pre.mean() * 1e4:+.1f} pb (n={len(pre)}), "
    f"post={post.mean() * 1e4:+.1f} pb (n={len(post)}), Welch t={tstat:.2f}, p={p2:.3f}")
a2 = p2 < 0.05

bins = pd.cut(T.loc[T.post, "absz"], [1, 1.5, 2, np.inf])
dose = T.loc[T.post].groupby(bins, observed=True)["ret"].agg(["mean", "count"])
say("A3 — dose-réponse post-2023 (pb par trade net) : "
    + ", ".join(f"{iv}: {m * 1e4:+.1f} (n={c})" for iv, (m, c) in dose.iterrows()))
a3 = bool(np.all(np.diff(dose["mean"].values) > 0))
say(f"\n→ A1 {'OK' if a1 else 'ÉCHEC'} · A2 {'OK' if a2 else 'ÉCHEC'} · A3 {'OK' if a3 else 'ÉCHEC'} "
    f"⇒ piste A {'SURVIT' if a1 and a2 and a3 else 'REJETÉE'}\n")

# =========================================================================== B
say("## B. M2 bande de bruit NQ — correction des tests multiples\n")
D = pd.read_parquet("results/daily_net.parquet")
D = D[D.index.dayofweek < 5].fillna(0.0)
target = "M2_noise|NQ"
x = D[target].values
Tn = len(x)
sr_all = D.mean() / D.std()  # Sharpe journaliers (non annualisés)
sr = sr_all[target]

# B1 — Deflated Sharpe Ratio
g = 0.5772156649
v = sr_all.var()
sr0 = np.sqrt(v) * ((1 - g) * stats.norm.ppf(1 - 1 / N_TRIALS) + g * stats.norm.ppf(1 - 1 / (N_TRIALS * np.e)))
sk, ku = stats.skew(x), stats.kurtosis(x, fisher=False)
dsr = stats.norm.cdf((sr - sr0) * np.sqrt(Tn - 1) / np.sqrt(1 - sk * sr + (ku - 1) / 4 * sr**2))
say(f"B1 — DSR : SR annualisé={sr * np.sqrt(252):.2f}, SR0 attendu du max de {N_TRIALS} essais="
    f"{sr0 * np.sqrt(252):.2f} (annualisé), skew={sk:.2f}, kurt={ku:.1f} → DSR={dsr:.3f}")
b1 = dsr > 0.95


# B2 — White Reality Check, bootstrap stationnaire
def stationary_idx(n, mean_block, reps):
    p = 1 / mean_block
    idx = np.empty((reps, n), dtype=np.int64)
    idx[:, 0] = rng.integers(0, n, reps)
    new = rng.random((reps, n)) < p
    rnd = rng.integers(0, n, (reps, n))
    for t in range(1, n):
        idx[:, t] = np.where(new[:, t], rnd[:, t], (idx[:, t - 1] + 1) % n)
    return idx


M = D.values
mu, sd = M.mean(0), M.std(0, ddof=1)
sd[sd == 0] = np.inf
stat = np.max(np.sqrt(Tn) * mu / sd)
reps, maxes = 5000, []
for chunk in range(10):
    idx = stationary_idx(Tn, 10, reps // 10)
    for row in idx:
        mb = M[row].mean(0)
        maxes.append(np.max(np.sqrt(Tn) * (mb - mu) / sd))
p_rc = float(np.mean(np.array(maxes) >= stat))
best = D.columns[np.argmax(mu / sd)]
say(f"B2 — Reality Check de White : max t-stat={stat:.2f} ({best}), p={p_rc:.4f}")
b2 = p_rc < 0.05

# B3 — PBO par CSCV
S = 16
blocks = np.array_split(np.arange(Tn), S)
bs = np.array([M[b].sum(0) for b in blocks])
bq = np.array([(M[b] ** 2).sum(0) for b in blocks])
bn = np.array([len(b) for b in blocks])[:, None]
lam, oos_neg = [], []
for comb in combinations(range(S), S // 2):
    ins = np.zeros(S, bool)
    ins[list(comb)] = True

    def sr_of(mask):
        n_ = bn[mask].sum()
        m_ = bs[mask].sum(0) / n_
        var = bq[mask].sum(0) / n_ - m_**2
        return m_ / np.sqrt(np.where(var > 0, var, np.inf))

    s_in, s_out = sr_of(ins), sr_of(~ins)
    k = np.argmax(s_in)
    w = (stats.rankdata(s_out)[k]) / (len(s_out) + 1)
    lam.append(np.log(w / (1 - w)))
    oos_neg.append(s_out[k] < 0)
pbo = float(np.mean(np.array(lam) <= 0))
say(f"B3 — PBO (CSCV, S=16, {len(lam)} combinaisons) = {pbo:.3f} ; "
    f"P(Sharpe OOS de la stratégie choisie < 0) = {np.mean(oos_neg):.3f}")

# B4 — IC bootstrap sur 24 mois
rec = D.loc[D.index >= "2024-09-01", target].values
idx = stationary_idx(len(rec), 10, 5000)
boot = np.array([rec[r].mean() / rec[r].std() for r in idx]) * np.sqrt(252)
say(f"B4 — Sharpe NQ M2 2024-09→2026-08 = {rec.mean() / rec.std() * np.sqrt(252):.2f}, "
    f"IC 95 % bootstrap = [{np.percentile(boot, 2.5):.2f} ; {np.percentile(boot, 97.5):.2f}]")

say(f"\n→ B1 {'OK' if b1 else 'ÉCHEC'} · B2 {'OK' if b2 else 'ÉCHEC'} ⇒ piste B {'SURVIT' if b1 and b2 else 'REJETÉE'}")

with open("results/followup.log", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
