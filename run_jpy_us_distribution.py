"""Distribution des rendements du short yen en session US (11:00 → 16:55 ET) : effet constant ou porté par
quelques séances ? Descriptif, données déjà vues (6J 2016-01 → 2026-08-28, plus spot USDJPY 2012-2015).
Rien après le 2026-08-28 (holdout du n° 28).

uv run python -X utf8 run_jpy_us_distribution.py   → results/jpy_us_distribution/ (summary.txt, groupes.csv, figure.png)

Coupes figées avant calcul (commit antérieur au premier lancement). Aucune règle n'est choisie, le compteur
global ne bouge pas ; si une coupe sert un jour de filtre, son n_famille comptera toutes les coupes ci-dessous (34).
Variable : rendement BRUT du short 6J (bp), positif = le yen baisse.

A. Forme de la distribution : moyenne, médiane, moyennes tronquées symétriques (1, 5, 10, 25 %), moyenne
   winsorisée 5 %, % de séances positives, asymétrie, kurtosis. Profil de décalage (q(p) + q(1−p)) / 2 pour
   p = 0,05 … 0,45 avec IC bootstrap 95 % : plat ≈ moyenne si toute la distribution est décalée, nul au centre
   si l'effet vient des queues. Comparaison au rendement du reste de la journée (16:55 → 11:00 suivant).
B. Concentration par séance : part du total due aux k meilleures / pires séances ; moyenne sans les 1 %, 5 %
   des séances les plus extrêmes en |r| ; contribution des séances par quintile de |r|.
C. Concentration dans le temps : par année, par trimestre (test de dispersion χ² des moyennes trimestrielles
   contre une moyenne constante, écart type NW), part des blocs de 63 séances positifs contre l'attendu iid,
   autocorrélations 1-5, ratio de variance des sommes sur 21 et 63 séances.
D. Calendrier : jours de décision FOMC (14:00 dans la fenêtre), minutes FOMC (14:00), autres jours d'annonce
   macro (avant 11:00), jours sans annonce ; dernier jour ouvré du mois (fixing de Londres à 11:00 ET) ;
   jour de semaine. Welch F entre groupes.
E. Conditions : quintiles de volatilité ex ante (écart type des 20 fenêtres précédentes) et de volatilité
   réalisée dans la fenêtre (1 min) ; terciles du rendement ES dans la même fenêtre (risk-on / risk-off) ;
   terciles du rendement du yen de 00:00 à 11:00 ET le même jour.
F. Spot USDJPY 2012-2015 (mid) : A et B résumés, pour voir si la forme est la même avant 2016.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from fab.protocole import nw_t  # noqa: E402
from run_jpy_us_backtest import END, NY, window_prices  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/jpy_us_distribution")
OUT.mkdir(parents=True, exist_ok=True)
LINES: list[str] = []
rng = np.random.default_rng(28)


def say(s=""):
    print(s)
    LINES.append(str(s))


def moy_tronq(x, a):
    return stats.trim_mean(x, a)


def profil(x, ps):
    q = np.quantile(x, ps)
    q2 = np.quantile(x, 1 - ps)
    return (q + q2) / 2


def forme(r: pd.Series, nom: str):
    x = r.values
    say(f"\n== A/B. {nom} : n = {len(x)}, {r.index.min()} → {r.index.max()}")
    say(f"  moyenne {x.mean():+.2f} bp (t NW {nw_t(x):+.2f}), médiane {np.median(x):+.2f}, "
        f"écart type {x.std(ddof=1):.1f}, positives {100 * (x > 0).mean():.1f} %, "
        f"asymétrie {stats.skew(x):+.2f}, kurtosis {stats.kurtosis(x, fisher=False):.1f}")
    say("  moyennes tronquées symétriques : " + ", ".join(f"{int(a * 100)} % {moy_tronq(x, a):+.2f}" for a in [.01, .05, .10, .25])
        + f" ; winsorisée 5 % {stats.mstats.winsorize(x, (.05, .05)).mean():+.2f}")
    ps = np.arange(0.05, 0.50, 0.05)
    pr = profil(x, ps)
    boot = np.array([profil(rng.choice(x, len(x)), ps) for _ in range(2000)])
    lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
    say("  profil de décalage (q(p)+q(1−p))/2 [IC 95 %] :")
    for p, v, a, b in zip(ps, pr, lo, hi):
        say(f"    p = {p:.2f} : {v:+.2f} [{a:+.2f} ; {b:+.2f}]")
    # B. concentration
    tot = x.sum()
    s = np.sort(x)
    say(f"  total {tot:+.0f} bp ; 10 meilleures séances {s[-10:].sum():+.0f}, 10 pires {s[:10].sum():+.0f}, "
        f"50 meilleures {s[-50:].sum():+.0f}, 50 pires {s[:50].sum():+.0f}")
    a = np.abs(x)
    for qq in [0.99, 0.95]:
        m = a <= np.quantile(a, qq)
        say(f"  sans les {100 * (1 - qq):.0f} % de séances les plus extrêmes en |r| : moyenne {x[m].mean():+.2f} "
            f"(t NW {nw_t(x[m]):+.2f}), n = {m.sum()}")
    qt = pd.qcut(a, 5, labels=False)
    say("  par quintile de |r| (Q1 calme → Q5 agité) : " + " ; ".join(
        f"Q{k + 1} moy {x[qt == k].mean():+.2f}, part du total {100 * x[qt == k].sum() / tot:+.0f} %, positives {100 * (x[qt == k] > 0).mean():.0f} %"
        for k in range(5)))
    return ps, pr, lo, hi


def groupes(r: pd.Series, g: pd.Series, titre: str, rows: list):
    d = pd.DataFrame({"r": r, "g": g}).dropna()
    say(f"\n  {titre}")
    vals = []
    for k, sub in d.groupby("g", observed=True):
        x = sub.r.values
        vals.append(x)
        say(f"    {str(k):<28} n {len(x):>5}  moy {x.mean():+6.2f}  méd {np.median(x):+6.2f}  t NW {nw_t(x) if len(x) > 10 else np.nan:+5.2f}"
            f"  positives {100 * (x > 0).mean():4.1f} %  part du total {100 * x.sum() / d.r.sum():+5.0f} %")
        rows.append({"coupe": titre, "groupe": str(k), "n": len(x), "moy_bp": x.mean(), "med_bp": np.median(x),
                     "t_nw": nw_t(x) if len(x) > 10 else np.nan, "pos_%": 100 * (x > 0).mean()})
    if len(vals) > 1:
        f, p = stats.f_oneway(*vals)  # ANOVA ; Welch ci-dessous
        k = len(vals)
        n = np.array([len(v) for v in vals]); m = np.array([v.mean() for v in vals]); v = np.array([v.var(ddof=1) for v in vals])
        w = n / v; mw = (w * m).sum() / w.sum()
        num = (w * (m - mw) ** 2).sum() / (k - 1)
        lam = ((1 - w / w.sum()) ** 2 / (n - 1)).sum()
        fw = num / (1 + 2 * (k - 2) / (k ** 2 - 1) * lam)
        pw = stats.f.sf(fw, k - 1, (k ** 2 - 1) / (3 * lam))
        say(f"    Welch F = {fw:.2f}, p = {pw:.3f}")


def main() -> None:
    j = pd.read_parquet("D:/quant-data/Cotations/forex/6J_v0_1m.parquet")
    j.index = j.index.tz_convert(NY)
    j = j[j.index < END]
    w = window_prices(j)
    r = (-1e4 * np.log(w.p_out / w.p_in)).rename("r")
    r.index = pd.to_datetime(r.index)

    # reste de la journée : 16:55 → 11:00 suivant (short yen aussi)
    reste = (-1e4 * np.log(w.p_in.shift(-1).values / w.p_out.values))
    reste = pd.Series(reste, index=r.index).dropna()

    ps, pr, lo, hi = forme(r, "6J short 11:00 → 16:55 ET, brut")
    _, pr_o, lo_o, hi_o = forme(reste, "Référence : même short de 16:55 → 11:00 suivant")

    # C. temps
    say("\n== C. Concentration dans le temps")
    sd = r.std(ddof=1)
    yrs = r.groupby(r.index.year)
    say("  par année : " + " ; ".join(f"{y} {g.mean():+.2f} ({100 * (g > 0).mean():.0f} %)" for y, g in yrs))
    q = r.groupby(r.index.to_period("Q"))
    mq, nq = q.mean(), q.size()
    chi = ((mq - r.mean()) ** 2 * nq / sd ** 2).sum()
    say(f"  trimestres : {len(mq)}, positifs {int((mq > 0).sum())} ; dispersion χ² = {chi:.1f} pour {len(mq) - 1} ddl, "
        f"p = {stats.chi2.sf(chi, len(mq) - 1):.3f} (H0 : moyenne constante)")
    say(f"  meilleur trimestre {mq.idxmax()} {mq.max():+.2f}, pire {mq.idxmin()} {mq.min():+.2f} ; "
        f"total sans les 4 meilleurs trimestres : moyenne {r[~r.index.to_period('Q').isin(mq.nlargest(4).index)].mean():+.2f}")
    for L in [21, 63]:
        blocs = r.groupby(np.arange(len(r)) // L).sum()
        blocs = blocs[r.groupby(np.arange(len(r)) // L).size() == L]
        attendu = stats.norm.cdf(r.mean() * np.sqrt(L) / sd)
        vr = blocs.var(ddof=1) / (L * r.var(ddof=1))
        say(f"  blocs de {L} séances : {len(blocs)}, positifs {100 * (blocs > 0).mean():.0f} % (attendu iid {100 * attendu:.0f} %), "
            f"ratio de variance {vr:.2f}")
    ac = [r.autocorr(k) for k in range(1, 6)]
    say("  autocorrélations 1-5 : " + ", ".join(f"{a:+.3f}" for a in ac) + f" (± {2 / np.sqrt(len(r)):.3f})")

    rows: list = []
    # D. calendrier
    say("\n== D. Calendrier")
    cal = pd.read_csv("config/calendrier_macro_us.csv")
    cal["date"] = pd.to_datetime(cal.date)
    dec = set(cal.date[cal.annonce == "FOMC décision"])
    mins = set(cal.date[cal.annonce == "FOMC minutes"])
    autres = set(cal.date[~cal.annonce.isin(["FOMC décision", "FOMC minutes"])])
    lab = pd.Series("aucune annonce", index=r.index)
    lab[r.index.isin(list(autres))] = "annonce avant 11:00"
    lab[r.index.isin(list(mins))] = "minutes FOMC 14:00"
    lab[r.index.isin(list(dec))] = "décision FOMC 14:00"
    groupes(r, lab, "Annonces", rows)
    fin_mois = r.index.to_series().groupby(r.index.to_period("M")).transform("max") == r.index.to_series()
    groupes(r, pd.Series(np.where(fin_mois, "dernier jour du mois", "autres jours"), index=r.index), "Fin de mois (fixing 11:00 ET)", rows)
    groupes(r, pd.Series(r.index.dayofweek.map(dict(enumerate(["1 lun", "2 mar", "3 mer", "4 jeu", "5 ven"]))), index=r.index), "Jour de semaine", rows)

    # E. conditions
    say("\n== E. Conditions")
    vol_ante = r.rolling(20).std().shift(1)
    groupes(r, pd.qcut(vol_ante, 5, labels=[f"Q{k}" for k in range(1, 6)]), "Volatilité ex ante (20 fenêtres précédentes)", rows)
    jj = j[(j.index.hour * 60 + j.index.minute >= 660) & (j.index.hour * 60 + j.index.minute < 1015)]
    lr = np.log(jj.close).groupby(jj.index.date).diff()
    rv = np.sqrt((lr ** 2).groupby(jj.index.date).sum()) * 1e4
    rv.index = pd.to_datetime(rv.index)
    groupes(r, pd.qcut(rv.reindex(r.index), 5, labels=[f"Q{k}" for k in range(1, 6)]), "Volatilité réalisée dans la fenêtre (1 min)", rows)
    es = window_prices(pd.read_parquet("D:/quant-data/Cotations/indices/ES_v0_1m.parquet"))
    esr = pd.Series(1e4 * np.log(es.p_out / es.p_in).values, index=pd.to_datetime(es.index)).reindex(r.index)
    groupes(r, pd.qcut(esr, 3, labels=["ES baisse", "ES neutre", "ES hausse"]), "Rendement ES dans la même fenêtre", rows)
    mat = window_prices(j, t_in="00:00", t_out="11:00")
    pre = pd.Series(-1e4 * np.log(mat.p_out / mat.p_in).values, index=pd.to_datetime(mat.index)).reindex(r.index)
    groupes(r, pd.qcut(pre, 3, labels=["yen monte 00-11", "neutre", "yen baisse 00-11"]), "Mouvement du yen 00:00 → 11:00 ET", rows)
    pd.DataFrame(rows).to_csv(OUT / "groupes.csv", index=False)

    # F. spot 2012-2015
    sp = pd.read_csv("results/jpy_us/trades_spot.csv", index_col=0, parse_dates=True)
    sp = sp[sp.index < "2016-01-01"]
    sp_mid = pd.Series(1e4 * np.log(sp.p_out / sp.p_in).values, index=sp.index)  # long USDJPY = short yen (prix d'exécution)
    forme(sp_mid, "F. Spot USDJPY 2012-2015 (prix d'exécution bid/ask, avant coûts fixes)")

    (OUT / "summary.txt").write_text("\n".join(LINES), encoding="utf-8")

    # figure
    ink, muted, grid, c1, c2 = "#1f1f1f", "#6b6b6b", "#e6e6e6", "#2a6fdb", "#9a9a9a"
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))
    for a in ax.flat:
        a.spines[["top", "right"]].set_visible(False)
        a.grid(axis="y", color=grid, lw=0.8)
        a.tick_params(colors=muted)
        a.axhline(0, color=muted, lw=0.8)
    a = ax[0, 0]
    a.fill_between(ps, lo, hi, color=c1, alpha=0.15, lw=0)
    a.plot(ps, pr, color=c1, lw=2, marker="o", ms=4, label="11:00 → 16:55")
    a.plot(ps, pr_o, color=c2, lw=2, marker="o", ms=4, label="16:55 → 11:00 (référence)")
    a.axhline(r.mean(), color=c1, lw=1, ls="--")
    a.set_title("Décalage de la distribution, (q(p)+q(1−p))/2, bp", color=ink, loc="left", fontsize=10)
    a.set_xlabel("p (0,05 = queues, 0,45 = centre)", color=muted)
    a.legend(frameon=False)
    a = ax[0, 1]
    eq = r.cumsum()
    a.plot(eq.index, eq.values, color=c1, lw=2)
    a.set_title("Brut cumulé du short, bp", color=ink, loc="left", fontsize=10)
    a = ax[1, 0]
    ym = yrs.mean()
    a.bar(ym.index.astype(str), ym.values, color=c1, width=0.6)
    a.set_title("Moyenne par année, bp", color=ink, loc="left", fontsize=10)
    a = ax[1, 1]
    g = pd.DataFrame(rows)
    g = g[g.coupe.str.startswith("Volatilité ex ante")]
    a.bar(g.groupe, g.moy_bp, color=c1, width=0.6)
    a.set_title("Moyenne par quintile de volatilité ex ante, bp", color=ink, loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "figure.png", dpi=130)


if __name__ == "__main__":
    main()
