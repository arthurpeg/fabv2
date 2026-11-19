"""Filtre ML binaire à taille fixe (1 R) sur la règle NQ de nuit mom, jugé sur la probabilité de passer un challenge
prop firm. Étape 1 (exploration) du protocole, branche `ml`. Demande de l'utilisateur du 2026-11-19.

uv run --group ml python experiments/ml_propfirm_filter/ml_propfirm_filter.py → experiments/ml_propfirm_filter/results/

GRILLE FIGÉE AVANT CALCUL (commitée avant le premier lancement ; ne rien changer après avoir vu un résultat)
--------------------------------------------------------------------------------------------------------------
Trades : mom = compte 20:00 ET (veille), sens = signe du momentum 12-1, SL 2 ATR M15, TP 4 ATR (2 R), sortie 9:30 ET ;
  bibliothèque cache/propfirm/nq_nuit_tp4.parquet (build_nq_nuit_tp.py 4), nuits 2011-07-01 → 2026-08-28 (données
  explorées). Rien après le 2026-08-28 : ni la fenêtre vue de l'avenant A, ni le holdout n° 26 (≥ 2026-11-04).
  R net = (R brut − c) / (1 + c), c = 1,5 point / 25 684 / risque (coût CFD des simulations FTMO).
  « Nuit d » = nuit qui se termine à l'ouverture de la séance d (entrée 20:00 ET le jour ouvré d'avant).
Cible : y = 1 si R net > 0.
4 variables, toutes connues à 20:00 ET avant l'entrée (atr = risque / 2 = ATR M15 / prix à l'entrée) :
  mom   : valeur continue du momentum 12-1 (somme des log-rendements mensuels close-to-close des mois m−12 … m−2,
          appliquée aux séances du mois m) ; son signe donne le sens (contrôlé).
  abdi  : sens × rendement de la nuit d−1 (20:00 → 9:30) / atr.
  blw   : sens × (clôture 16:15 − VWAP 15:15-16:15, prix typique) / clôture / atr, séance de la veille (définition du
          n° 16) ; demi-séances et trous → 0.
  annonce : 1 si NFP ou CPI à 8:30 ET le matin de la séance d (config/calendrier_macro_bls.csv).
Validation : Purged K-Fold chronologique, 5 blocs contigus, embargo de 5 nuits de chaque côté du bloc test retiré de
  l'entraînement (les étiquettes ne se chevauchent pas : chaque trade est fermé à 9:30). Probabilités hors bloc (OOF).
Modèles (2) :
  A : StandardScaler + régression logistique L2 (C = 1).
  B : LightGBM max_depth 2, num_leaves 3, min_child_samples 50, learning_rate 0,03, n_estimators 100, graine 2611.
Filtres : garder les nuits dont le score dépasse le quantile (1 − q) des scores OOF, q ∈ {70 %, 50 %, 35 %} ; taille
  fixe 1 R. Référence triviale : baseline (100 %). Filtre classique de comparaison : règle Abdi seule, score = −abdi
  (nuit d−1 contre le sens du trade → retournement favorable), mêmes q.
  → 9 filtres comptés (6 ML + 3 Abdi) : compteur 1 798 → 1 807.
Métriques : trades, win %, E[R] net, plus longue série de pertes, R/an, max DD (R) ; AUC OOF.
Monte Carlo (10 000 chemins, graine 2611, tirage i.i.d. des nuits ; une nuit filtrée vaut 0 et compte comme un jour) :
  S1 : +10 R avant −10 R (seuils fixes depuis le départ) ;
  S2 : +8 R avant −6 R (fixes) ;
  S3 : FTMO 1-Step 10k au risque du plan (2,5 % par trade) : +10 % = +4 R avant −10 % sous le plus haut solde = 4 R
       glissants (perte du jour 3 % = 1,2 R jamais atteinte par un seul trade borné à −1 R ; meilleur jour ≤ 50 %
       toujours vrai car un trade rapporte ≤ 2 R).
  Sorties : P(réussite), jours de trading médians (nuits écoulées, filtrées comprises) et trades médians jusqu'à la
  réussite. Sensibilité (non décisionnelle) : même chose en blocs de 20 nuits.
Significativité :
  E[R] : p = part de 2 000 filtres aléatoires de même taille avec E[R] ≥ ; Holm sur les 6 filtres ML.
  P(réussite) : 95e centile de 200 filtres aléatoires de même taille (Monte Carlo 10 000 chemins chacun).
  ML contre Abdi au même q : différence de E[R] par bootstrap par blocs de 20 nuits (2 000 tirages), p unilatéral.
Stabilité : gain de E[R] (gardés − tous) sur 5 sous-périodes 2011-07 → 2013, 2014-16, 2017-19, 2020-22, 2023 →
  2026-08 ; coefficients (A) et importances en gain (B) par bloc.
CRITÈRE (tout doit être vrai pour qu'un filtre ML « batte significativement ») :
  1. E[R] : p Holm < 0,05 contre le hasard ;
  2. P(réussite) > baseline et > 95e centile aléatoire en S1, S2 et S3 ;
  3. E[R] > Abdi au même q avec p < 0,05, et P(réussite) > Abdi en S1, S2 et S3 ;
  4. gain de E[R] > 0 sur au moins 4 sous-périodes sur 5.
  Sinon : recommandation de ne pas utiliser le ML. Aucun holdout n'est lu ici.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import recolte1.engine as E  # noqa: E402

E.USE_2010 = True
import recolte1.rules as RU  # noqa: E402

RU.START = "2010-06-08"
from lightgbm import LGBMClassifier  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
from sklearn.metrics import roc_auc_score  # noqa: E402
from sklearn.pipeline import make_pipeline  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

from recolte1.engine import NY, load, price_at  # noqa: E402
from recolte1.rules import at, base, monthly, sessions  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("experiments/ml_propfirm_filter/results")
A0, Z0 = "2011-07-01", "2026-08-28"
SEED = 2611
COST_PTS, P_REF = 1.5, 25_684.0
FEATS = ["mom", "abdi", "blw", "annonce"]
QS = [0.70, 0.50, 0.35]
K, EMBARGO = 5, 5
N_MC, N_RAND_ER, N_RAND_MC, N_BOOT, BLOCK = 10_000, 2_000, 200, 2_000, 20
SCEN = {"S1 +10/−10": (10.0, 10.0, False), "S2 +8/−6": (8.0, 6.0, False), "S3 FTMO 2,5 % (+4/−4 glissant)": (4.0, 4.0, True)}
PERIODES = [("2011-07 → 2013", A0, "2013-12-31"), ("2014-2016", "2014-01-01", "2016-12-31"),
            ("2017-2019", "2017-01-01", "2019-12-31"), ("2020-2022", "2020-01-01", "2022-12-31"),
            ("2023 → 2026-08", "2023-01-01", Z0)]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


# --------------------------------------------------------------------------- données et variables


def dataset() -> pd.DataFrame:
    t = pd.read_parquet("cache/propfirm/nq_nuit_tp4.parquet")
    t["night"] = pd.to_datetime(t.night)
    t = t[(t.night >= A0) & (t.night <= Z0)].sort_values("night").reset_index(drop=True)
    assert t.night.max() <= pd.Timestamp(Z0) and t.night.is_unique
    t["risk"] = t.risk.fillna(t.risk.median())
    c = COST_PTS / P_REF / t.risk
    t["R"] = (t.R_brut - c) / (1 + c)
    t["y"] = (t.R > 0).astype(int)
    atr = t.risk / 2

    B = sessions()
    D = B.index
    BB = base("NQ")
    msig = monthly(BB, "cc").shift(1).rolling(11, min_periods=11).sum()
    per = D.to_period("M")
    mom = pd.Series(msig.reindex(per - 1).values, index=D)
    # nuit d : 20:00 ET de la veille → 9:30 ET de la séance d
    p_in, _ = price_at("NQ", at(D, "20:00", NY, -1))
    p_out, _ = price_at("NQ", B["t_open"])
    night_ret = (p_out / p_in - 1).shift(1)  # nuit d−1, connue à 20:00 la veille de d
    # BLW (n° 16) : séance d−1, 16:15 contre VWAP 15:15-16:15
    df = load("NQ")
    ny = df.index.tz_convert(NY)
    mins = ny.hour * 60 + ny.minute
    w = df[(mins >= 15 * 60 + 15) & (mins < 16 * 60 + 15)]
    day = w.index.tz_convert(NY).tz_localize(None).normalize()
    tp = (w.high + w.low + w.close) / 3
    vwap = ((tp * w.volume).groupby(day).sum() / w.volume.groupby(day).sum()).reindex(D)
    close, _ = price_at("NQ", at(D, "16:15", NY))
    dist = ((close - vwap) / close).where(~B["half"]).shift(1)
    cal = pd.read_csv("config/calendrier_macro_bls.csv", parse_dates=["date"])
    news = set(cal[cal.annonce.isin(["NFP", "CPI"]) & (cal.heure_ET == "08:30")].date)

    n = t.night
    t["mom"] = mom.reindex(n).values
    assert (np.sign(t.mom) == t.dir).mean() > 0.999, "le signe du momentum ne redonne pas le sens des trades"
    t["abdi"] = t.dir * night_ret.reindex(n).values / atr
    t["blw"] = t.dir * dist.reindex(n).values / atr
    t["annonce"] = n.isin(news).astype(int)
    for f in ["abdi", "blw"]:
        say(f"  {f} : {t[f].isna().sum()} valeurs manquantes → 0")
        t[f] = t[f].fillna(0.0)
    return t


# --------------------------------------------------------------------------- validation croisée purgée


def purged_kfold(n: int, k: int = K, emb: int = EMBARGO):
    for te in np.array_split(np.arange(n), k):
        lo, hi = te[0], te[-1]
        tr = np.r_[np.arange(0, max(lo - emb, 0)), np.arange(min(hi + emb + 1, n), n)]
        yield tr, te


def models():
    return {"A logit L2": lambda: make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000)),
            "B LightGBM": lambda: LGBMClassifier(max_depth=2, num_leaves=3, min_child_samples=50, learning_rate=0.03,
                                                 n_estimators=100, random_state=SEED, verbose=-1)}


def oof(t: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    X, y = t[FEATS].to_numpy(float), t.y.to_numpy()
    scores, imp = pd.DataFrame(index=t.index), []
    for name, make in models().items():
        p = np.full(len(t), np.nan)
        for f, (tr, te) in enumerate(purged_kfold(len(t))):
            m = make().fit(X[tr], y[tr])
            p[te] = m.predict_proba(X[te])[:, 1]
            if name.startswith("A"):
                v = m[-1].coef_[0]
            else:
                g = m.booster_.feature_importance("gain")
                v = g / g.sum()
            imp.append({"modèle": name, "bloc": f + 1, "début": t.night.iloc[te[0]].date(),
                        "fin": t.night.iloc[te[-1]].date(), **dict(zip(FEATS, v))})
        scores[name] = p
    scores["Abdi seule"] = -t.abdi.to_numpy()
    return scores, pd.DataFrame(imp)


# --------------------------------------------------------------------------- métriques


def longest_loss(r: np.ndarray) -> int:
    best = cur = 0
    for x in r:
        cur = cur + 1 if x < 0 else 0
        best = max(best, cur)
    return best


def quality(t: pd.DataFrame, keep: np.ndarray) -> dict:
    r = t.R.to_numpy()[keep]
    eq = np.r_[0.0, np.cumsum(r)]
    years = (t.night.max() - t.night.min()).days / 365.25
    return {"trades": int(keep.sum()), "gardés %": 100 * keep.mean(), "win %": 100 * (r > 0).mean(),
            "E[R]": r.mean(), "sd R": r.std(), "série de pertes max": longest_loss(r), "R/an": r.sum() / years,
            "max DD (R)": (eq - np.maximum.accumulate(eq)).min()}


def mc(x: np.ndarray, kept: np.ndarray, up: float, dn: float, trailing: bool, rng: np.random.Generator,
       n: int = N_MC, block: int = 1, chunk: int = 240, max_steps: int = 50_000):
    """Chemins de nuits tirées avec remise (blocs circulaires de `block` nuits). Renvoie (réussi, nuits, trades)."""
    m = len(x)
    eq, hi = np.zeros(n), np.zeros(n)
    nights, trades = np.zeros(n, int), np.zeros(n, int)
    st = np.zeros(n, np.int8)
    xs, ks = x.astype(np.float64), kept.astype(np.int32)
    steps = 0
    while (st == 0).any() and steps < max_steps:
        a = np.flatnonzero(st == 0)
        if block == 1:
            idx = rng.integers(0, m, (len(a), chunk))
        else:
            s0 = rng.integers(0, m, (len(a), chunk // block))
            idx = ((s0[:, :, None] + np.arange(block)) % m).reshape(len(a), chunk)
        cs = eq[a, None] + np.cumsum(xs[idx], 1)
        ck = np.cumsum(ks[idx], 1)
        if trailing:
            h = np.maximum(hi[a, None], np.maximum.accumulate(cs, 1))
            fail = cs <= h - dn + 1e-12
        else:
            fail = cs <= -dn + 1e-12
        win = cs >= up - 1e-12
        ev = win | fail
        hit = ev.any(1)
        j = ev.argmax(1)
        done, rest = a[hit], a[~hit]
        jd = j[hit]
        st[done] = np.where(win[hit, jd], 1, -1)
        nights[done] += jd + 1
        trades[done] += ck[hit, jd]
        nights[rest] += chunk
        trades[rest] += ck[~hit, -1]
        eq[rest] = cs[~hit, -1]
        if trailing:
            hi[rest] = h[~hit, -1]
        steps += chunk
    return st == 1, nights, trades


def mc_row(x, kept, rng, block=1) -> dict:
    row = {}
    for s, (up, dn, tr) in SCEN.items():
        ok, nn, tt = mc(x, kept, up, dn, tr, rng, block=block)
        row[f"{s} P %"] = 100 * ok.mean()
        row[f"{s} jours méd."] = float(np.median(nn[ok])) if ok.any() else np.nan
        row[f"{s} trades méd."] = float(np.median(tt[ok])) if ok.any() else np.nan
    return row


def holm(p: list[float]) -> np.ndarray:
    p = np.asarray(p)
    o = np.argsort(p)
    adj = np.empty_like(p)
    run = 0.0
    for i, k in enumerate(o):
        run = max(run, (len(p) - i) * p[k])
        adj[k] = min(run, 1.0)
    return adj


# --------------------------------------------------------------------------- programme


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    say(f"Filtre ML binaire, taille fixe 1 R, mom TP 4 ATR, nuits {A0} → {Z0}")
    t = dataset()
    R = t.R.to_numpy()
    n = len(t)
    say(f"{n} trades, E[R] net {R.mean():+.4f}, win {100 * t.y.mean():.1f} %, annonces {t.annonce.sum()}, "
        f"R brut min {t.R_brut.min():.3f}")
    assert R.min() >= -1.2, "un trade perd plus de 1,2 R : la perte du jour FTMO (3 %) n'est plus négligeable"
    say("\nCorrélations entre variables :\n" + t[FEATS].corr().round(3).to_string())

    scores, imp = oof(t)
    out = t[["night", "dir", "reason", "R", "y"] + FEATS].join(scores)
    out.to_csv(OUT / "oof.csv", index=False)
    imp.to_csv(OUT / "importances.csv", index=False)
    say("\nAUC hors bloc : " + ", ".join(f"{c} {roc_auc_score(t.y, scores[c]):.3f}" for c in scores))
    say("\nCoefficients (A, variables centrées réduites) et importances en gain (B) par bloc :\n"
        + imp.round(3).to_string(index=False))

    # filtres
    filt = {"Baseline 100 %": np.ones(n, bool)}
    for c in scores:
        for q in QS:
            s = scores[c].to_numpy()
            filt[f"{c} {q:.0%}"] = s >= np.quantile(s, 1 - q)

    # qualité et E[R] contre le hasard
    rows = []
    for name, keep in filt.items():
        row = {"filtre": name, **quality(t, keep)}
        if not name.startswith("Baseline"):
            k = keep.sum()
            rnd = np.array([R[rng.choice(n, k, replace=False)].mean() for _ in range(N_RAND_ER)])
            row["p E[R] vs hasard"] = float((rnd >= row["E[R]"]).mean())
        rows.append(row)
    Q = pd.DataFrame(rows).set_index("filtre")
    ml = [f for f in Q.index if f.startswith(("A ", "B "))]
    Q.loc[ml, "p Holm (6 ML)"] = holm(Q.loc[ml, "p E[R] vs hasard"].tolist())

    # ML contre Abdi au même q : bootstrap par blocs des nuits
    nb = int(np.ceil(n / BLOCK))
    starts = rng.integers(0, n, (N_BOOT, nb))
    bidx = ((starts[:, :, None] + np.arange(BLOCK)) % n).reshape(N_BOOT, -1)[:, :n]
    for f in ml:
        q = f.split()[-1]
        ka, kb = filt[f], filt[f"Abdi seule {q}"]
        d = R[ka].mean() - R[kb].mean()
        Rb, ka_b, kb_b = R[bidx], ka[bidx], kb[bidx]
        db = (Rb * ka_b).sum(1) / ka_b.sum(1) - (Rb * kb_b).sum(1) / kb_b.sum(1)
        Q.loc[f, "ΔE[R] vs Abdi"] = d
        Q.loc[f, "p vs Abdi"] = float(((db - d) >= d).mean())  # H0 recentrée
    say("\n=== Qualité du signal (hors bloc) ===\n" + Q.round(4).to_string())

    # Monte Carlo prop firm
    say("\n=== Monte Carlo prop firm (10 000 chemins i.i.d.) ===")
    M = []
    for name, keep in filt.items():
        x = np.where(keep, R, 0.0)
        M.append({"filtre": name, **mc_row(x, keep, rng)})
    M = pd.DataFrame(M).set_index("filtre")
    say(M.round(1).to_string())

    # filtres aléatoires pour P(réussite)
    say(f"\nFiltres aléatoires ({N_RAND_MC} par taux) pour P(réussite)…")
    rnd_rows = []
    for q in QS:
        k = int(round(q * n))
        for i in range(N_RAND_MC):
            keep = np.zeros(n, bool)
            keep[rng.choice(n, k, replace=False)] = True
            rr = mc_row(np.where(keep, R, 0.0), keep, rng)
            rnd_rows.append({"q": q, "i": i, **{c: v for c, v in rr.items() if c.endswith("P %")}})
    RN = pd.DataFrame(rnd_rows)
    RN.to_csv(OUT / "aleatoires_mc.csv", index=False)
    p95 = RN.groupby("q").quantile(0.95).drop(columns="i")
    say("95e centile des filtres aléatoires :\n" + p95.round(1).to_string())

    # sensibilité : blocs de 20 nuits
    MB = pd.DataFrame([{"filtre": nm, **{c: v for c, v in mc_row(np.where(kp, R, 0.0), kp, rng, block=BLOCK).items()
                                         if c.endswith("P %")}} for nm, kp in filt.items()]).set_index("filtre")
    say("\nSensibilité (non décisionnelle), P(réussite) en blocs de 20 nuits :\n" + MB.round(1).to_string())

    # stabilité par sous-période
    S = []
    for name, keep in filt.items():
        row = {"filtre": name}
        for lab, a, z in PERIODES:
            p = ((t.night >= a) & (t.night <= z)).to_numpy()
            row[lab] = R[p & keep].mean() - R[p].mean()
        S.append(row)
    S = pd.DataFrame(S).set_index("filtre")
    S["périodes > 0"] = (S[[p[0] for p in PERIODES]] > 0).sum(1)
    say("\n=== Gain de E[R] (gardés − tous) par sous-période ===\n" + S.round(4).to_string())

    # verdict
    say("\n=== Verdict (critères figés) ===")
    V = []
    Pcols = [f"{s} P %" for s in SCEN]
    for f in [x for x in filt if not x.startswith("Baseline")]:
        q = float(f.split()[-1].rstrip("%")) / 100
        c2 = all(M.loc[f, c] > M.loc["Baseline 100 %", c] and M.loc[f, c] > p95.loc[q, c] for c in Pcols)
        row = {"filtre": f, "1 E[R] vs hasard": None, "2 P vs base et p95": c2, "3 vs Abdi": None,
               "4 stabilité": bool(S.loc[f, "périodes > 0"] >= 4)}
        if f in ml:
            row["1 E[R] vs hasard"] = bool(Q.loc[f, "p Holm (6 ML)"] < 0.05)
            ab = f"Abdi seule {f.split()[-1]}"
            row["3 vs Abdi"] = bool(Q.loc[f, "p vs Abdi"] < 0.05 and all(M.loc[f, c] > M.loc[ab, c] for c in Pcols))
            row["passe"] = all(row[k] for k in ["1 E[R] vs hasard", "2 P vs base et p95", "3 vs Abdi", "4 stabilité"])
        else:
            row["1 E[R] vs hasard"] = bool(Q.loc[f, "p E[R] vs hasard"] < 0.05)
        V.append(row)
    V = pd.DataFrame(V).set_index("filtre")
    say(V.to_string())
    win = V.index[V.get("passe", pd.Series(False, index=V.index)).fillna(False).astype(bool)].tolist()
    say("\nConclusion : " + (f"filtre(s) ML qui passent tous les critères : {win}" if win else
                             "aucun filtre ML ne bat significativement la baseline et la règle Abdi → ne pas utiliser "
                             "le ML (aucun holdout lu)."))

    Q.to_csv(OUT / "qualite.csv")
    M.to_csv(OUT / "monte_carlo.csv")
    MB.to_csv(OUT / "monte_carlo_blocs20.csv")
    p95.to_csv(OUT / "aleatoires_p95.csv")
    S.to_csv(OUT / "stabilite.csv")
    V.to_csv(OUT / "verdict.csv")
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
