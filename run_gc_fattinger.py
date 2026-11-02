"""Or (GC) : les affirmations de Fattinger-Ziegler (« Risk and Return around the Clock »,
SSRN 2606706) testées sur nos données, 5 minutes, 2016-2026.

uv run python run_gc_fattinger.py      → results/gc_fattinger/ (run.log, hypotheses.csv, periods.csv,
unbiasedness.csv, intervals.csv)
uv run python run_gc_fattinger.py SI   → results/si_fattinger/ : argent, série London Strategic Edge
2017-04 → 2026-08 (recolte1.engine._load_lse) ; séances minces (contrat qui expire) et séances
de roulement écartées en plus.

Exploratoire, non pré-enregistré, demandé en séance. Le papier couvre 2010-2013 ; nos données
GC commencent en 2016 : c'est une réplication hors échantillon dans le temps. Arrêt au
2026-08-28 (holdout non touché). Rien ici n'est une règle de trading.

Construction (comme le papier) :
- jour GC = clôture 17:00 NY du jour ouvré précédent → 17:00 NY ; intervalle 0 = gap de l'arrêt
  (clôture 17:00 → ouverture de la première barre de 18:00), puis 276 intervalles de 5 minutes
  (18:00 → 17:00), prix = dernière clôture ajustée (ratio aux roulements, recolte1.engine.load),
  report du dernier prix si l'intervalle n'a pas de transaction ; rendements logarithmiques ;
- jours où l'écart New York / Europe centrale n'est pas de 6 h supprimés (comme le papier) ; jours
  fériés et séances courtes (moins de 85 % du nombre médian de barres) supprimés ;
- heures données en NY ; CET = NY + 6 h sur tous les jours gardés.

Familles d'hypothèses (H = affirmation du papier pour l'or) et tests :
  A. Où se fait le prix : H1 contribution au prix quasi nulle avant l'ouverture européenne
     (17:00 → 3:00 NY) ; H2 contribution au prix = contribution à la variance dans chacune des
     8 périodes du papier.
  B. Efficience : H3 régressions d'absence de biais r = a + b·r_c, b < 1 (bruit) les 2 à 5
     premières heures de cotation, b ≈ 1 en séance US (23 coupures horaires, Holm) ;
     H4 l'efficience Δ = R² − Var(r_c)/Var(r) baisse entre la clôture asiatique (1:00 NY) et
     l'ouverture européenne (3:00 NY).
  C. Volatilité : H5 pics (ouverture de Tokyo, montée pendant l'Asie, ouverture européenne,
     8:20, 8:30, 10:00, 13:30, 14:00 jours FOMC, 16:00) ; H6 pas de U en séance COMEX
     (variance de diffusion, jours sans annonce).
  D. Sauts (MedRV + Lee-Mykland, K = un jour, 99,9 %) : H7 sauts ≥ 5 % de la variance ;
     H8 l'intervalle 8:30 est le plus gros contributeur (hors réouverture) ; H9 10:00 > Fed ;
     H10 le saut de 8:30 vient des jours d'annonce.
  E. Volume : H11 volume < volatilité hors séance COMEX 8:20-13:30 ; H12 à 8:30 et 10:00 le
     volume monte plus que la volatilité ; H13 idem à 8:20, 13:30 et 9:30 ; H14 contribution au
     prix par unité de volume > 1 la nuit.
IC et p : bootstrap par blocs de 10 jours (recolte1.engine), t de Newey-West pour les moyennes,
écarts-types de White pour les pentes. Holm dans chaque famille.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as st

import recolte1.engine as E
from run_gc_sessions import END, NY, START, holm, nw_t

ASSET = "GC"
OUT = Path("results/gc_fattinger")
CET, TOKYO = "Europe/Berlin", "Asia/Tokyo"
NI = 277  # gap + 276 intervalles de 5 minutes
SUBP = [("2016-2019", "2016", "2019"), ("2020-2022", "2020", "2022"), ("2023-2026", "2023", "2026")]
# périodes du papier (CET) traduites en NY ; la première contient le gap de l'arrêt
PERIODS = [("P1 00-01 CET", "18:00", "19:00"), ("P2 01-08 Japon", "19:00", "02:00"),
           ("P3 08-09 pré-Europe", "02:00", "03:00"), ("P4 09-13 Europe", "03:00", "07:00"),
           ("P5 13-15:30 macro US", "07:00", "09:30"), ("P6 15:30-17:30 Eur+US", "09:30", "11:30"),
           ("P7 17:30-22 US", "11:30", "16:00"), ("P8 22-23 après", "16:00", "17:00")]
ANN_830 = {"NFP", "CPI", "PPI", "Ventes au détail", "PIB avancé", "PCE (revenus et dépenses)"}
ANN_1000 = {"ISM manufacturier", "ISM services", "JOLTS"}
LINES: list[str] = []
HYP: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


def hyp(fam: str, code: str, claim: str, stat: str, val: float, lo: float, hi: float, p: float,
        expect: str, ok: bool | None):
    HYP.append({"famille": fam, "code": code, "affirmation": claim, "statistique": stat, "valeur": val,
                "ic_lo": lo, "ic_hi": hi, "p": p, "attendu": expect, "conforme_brut": ok})


def p_boot(b: np.ndarray, h0: float) -> float:
    """p bilatéral percentile : part des tirages de l'autre côté de h0."""
    b = b[np.isfinite(b)]
    return float(min(1.0, 2 * min((b <= h0).mean(), (b >= h0).mean()) + 1 / len(b)))


# --------------------------------------------------------------------------- données


def build() -> dict:
    df = E.load(ASSET)
    t_bar = df.index.as_unit("ns").asi8  # ns UTC
    d = pd.bdate_range(START, END)
    c_prev = E.at(d - pd.offsets.BDay(1), "17:00", NY).set_axis(d)
    t_open = E.at(d, "18:00", NY, -1)
    t_end = E.at(d, "17:00", NY)
    ok = c_prev.notna() & t_open.notna() & t_end.notna()
    ok &= (t_end - t_open) == pd.Timedelta(hours=23)

    def off(ts):
        return ts.dt.tz_convert(CET).dt.tz_localize(None) - ts.dt.tz_convert(NY).dt.tz_localize(None)

    ok &= (off(t_open) == pd.Timedelta(hours=6)) & (off(t_end) == pd.Timedelta(hours=6))
    d = d[ok.values]
    c_prev, t_open, t_end = c_prev[d], t_open[d], t_end[d]

    # séances complètes : nombre de barres entre la réouverture et 17:00
    to_ns = pd.DatetimeIndex(t_open).as_unit("ns").asi8
    i0 = np.searchsorted(t_bar, to_ns)
    i1 = np.searchsorted(t_bar, pd.DatetimeIndex(t_end).as_unit("ns").asi8)
    nbar = i1 - i0
    full = nbar >= 0.85 * np.median(nbar)
    p0, _ = E.price_at(ASSET, c_prev)
    # ouverture : première barre dans [18:00, 18:05)
    o_ok = (i0 < len(t_bar))
    o_t = t_bar[np.minimum(i0, len(t_bar) - 1)]
    o_ok &= (o_t >= to_ns) & (o_t < to_ns + 5 * 60 * 10**9)
    p_open = np.where(o_ok, df["open"].values[np.minimum(i0, len(t_bar) - 1)], np.nan)
    keep = full & o_ok & p0.notna().values
    if E.SPECS[ASSET].folder == "lse":  # contrat qui expire (séances minces) et séance de roulement
        ss = E.lse_sessions(pd.read_parquet(E.LSE / f"{ASSET}_lse_1m.parquet"))
        thin = ss["thin"].reindex(d).astype("boolean").fillna(True).to_numpy(bool)
        roll = d.isin(pd.DatetimeIndex(df.attrs["roll_table"]["séance"]))
        print(f"{ASSET} : {(thin & full).sum()} séances minces et {roll.sum()} séances de roulement écartées")
        keep &= ~thin & ~roll
    d = d[keep]
    p0, p_open = p0.values[keep], p_open[keep]
    t_open = pd.DatetimeIndex(t_open[d]).as_unit("ns").tz_convert(None)
    i0 = i0[keep]

    # bornes des intervalles 1..276 : 18:05 ... 17:00 ; prix = dernière clôture d'une barre démarrant avant
    k = np.arange(1, NI)
    edges = t_open.values[:, None] + (k * 5 * 60 * 10**9).astype("timedelta64[ns]")[None, :]
    flat = edges.ravel()
    pos = np.searchsorted(t_bar, flat.astype("int64"), side="left") - 1  # dernière barre < borne
    close = df["close"].values
    px = close[np.maximum(pos, 0)].reshape(len(d), NI - 1)
    after_open = (pos.reshape(len(d), NI - 1) >= i0[:, None])
    px = np.where(after_open, px, np.nan)
    px = pd.DataFrame(px).T.ffill().T.values  # report du dernier prix
    px = np.where(np.isnan(px), p_open[:, None], px)
    lp = np.log(np.column_stack([p0, p_open, px]))
    R = np.diff(lp, axis=1)  # (jours, 277) : gap, 18:00→18:05, …, 16:55→17:00

    cv = np.concatenate([[0.0], np.cumsum(df["volume"].values)])
    vpos = np.searchsorted(t_bar, flat.astype("int64"), side="left")
    cve = cv[vpos].reshape(len(d), NI - 1)
    V = np.diff(np.column_stack([cv[i0], cve]), axis=1)
    V = np.column_stack([np.zeros(len(d)), V])  # pas de volume dans le gap

    starts = np.column_stack([np.full(len(d), np.datetime64("NaT"), dtype="datetime64[ns]"),
                              t_open.values[:, None] + ((k - 1) * 5 * 60 * 10**9).astype("timedelta64[ns]")[None, :]])
    lab = ["gap"] + [(pd.Timestamp("2000-01-01 18:00") + pd.Timedelta(minutes=5 * (j - 1))).strftime("%H:%M")
                     for j in range(1, NI)]
    return {"days": d, "R": R, "V": V, "starts": starts, "lab": lab, "nbar": nbar}


def jumps(R: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Diffusion (MedRV, Andersen-Dobrev-Schaumburg) et sauts (Lee-Mykland), comme le papier."""
    r = R.ravel()
    a = np.abs(r)
    stack = np.vstack([np.r_[a[0], a[:-1]], a, np.r_[a[1:], a[-1]]])
    cmed = np.pi / (6 - 4 * np.sqrt(3) + np.pi)
    DV = cmed * np.median(stack, axis=0) ** 2
    K = NI
    S = np.concatenate([[0.0], np.cumsum(DV)])
    i = np.arange(len(r))
    sig2 = np.full(len(r), np.nan)
    m = i >= K
    sig2[m] = (S[i[m] - 1] - S[i[m] - K + 1]) / (K - 2)
    L = r / np.sqrt(sig2)
    n = NI
    c = np.sqrt(2 / np.pi)
    Cn = np.sqrt(2 * np.log(n)) / c - (np.log(np.pi) + np.log(np.log(n))) / (2 * c * np.sqrt(2 * np.log(n)))
    Sn = 1 / (c * np.sqrt(2 * np.log(n)))
    jump = ((np.abs(L) - Cn) / Sn) > -np.log(-np.log(0.999))
    JV = np.where(jump, np.maximum(r ** 2 - DV, 0), 0.0)
    sh = R.shape
    return DV.reshape(sh), JV.reshape(sh), jump.reshape(sh)


# --------------------------------------------------------------------------- outils


def tmask(lab: list[str], a: str, b: str) -> np.ndarray:
    """Intervalles dont le début NY est dans [a, b) sur l'horloge de séance 18:00 → 17:00 ;
    a = "18:00" inclut le gap."""
    order = {h: j for j, h in enumerate(lab)}

    def idx(h):
        return 0 if h == "18:00" else order[h] if h in order else NI
    ja, jb = idx(a), (NI if b == "17:00" else idx(b))
    m = np.zeros(NI, bool)
    m[ja:jb] = True
    return m


def boot_ratio(num: np.ndarray, den: np.ndarray, h0: float) -> tuple[float, float, float, float]:
    idx = E._block_index(len(num))
    b = num[idx].sum(1) / den[idx].sum(1)
    v = num.sum() / den.sum()
    return v, np.percentile(b, 2.5), np.percentile(b, 97.5), p_boot(b, h0)


def boot_mean(x: np.ndarray, h0: float = 0.0) -> tuple[float, float, float, float]:
    idx = E._block_index(len(x))
    b = x[idx].mean(1)
    return x.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5), p_boot(b, h0)


def reg_moments(x: np.ndarray, y: np.ndarray):
    xc, yc = x - x.mean(), y - y.mean()
    vx, vy, cxy = (xc ** 2).mean(), (yc ** 2).mean(), (xc * yc).mean()
    return vx, vy, cxy


def unbiased(x: np.ndarray, y: np.ndarray) -> dict:
    vx, vy, cxy = reg_moments(x, y)
    b = cxy / vx
    xc = x - x.mean()
    e = (y - y.mean()) - b * xc
    se = np.sqrt((xc ** 2 * e ** 2).sum()) / (xc ** 2).sum()
    r2 = cxy ** 2 / (vx * vy)
    return {"beta": b, "se": se, "t_b1": (b - 1) / se, "p_b1": 2 * st.norm.sf(abs((b - 1) / se)),
            "R2": r2, "var_share": vx / vy, "delta": r2 - vx / vy}


def boot_delta(x: np.ndarray, y: np.ndarray, idx: np.ndarray) -> np.ndarray:
    xs, ys = x[idx], y[idx]
    xc = xs - xs.mean(1, keepdims=True)
    yc = ys - ys.mean(1, keepdims=True)
    vx, vy, c = (xc ** 2).mean(1), (yc ** 2).mean(1), (xc * yc).mean(1)
    return c ** 2 / (vx * vy) - vx / vy


def spike(X: np.ndarray, starts: np.ndarray, T: pd.Series, rows: np.ndarray | None = None):
    """Rapport moyenne(X à l'intervalle qui démarre à T) / moyenne(X des voisins : [T-30, T) et
    [T+15, T+45)). Bootstrap par blocs sur les jours. T : instant UTC par jour."""
    Tv = pd.DatetimeIndex(T).as_unit("ns").values[:, None]
    dt = (starts - Tv) / np.timedelta64(1, "m")
    tgt = dt == 0
    nb = ((dt >= -30) & (dt < 0)) | ((dt >= 15) & (dt < 45))
    has = tgt.any(1) & (nb.sum(1) >= 10)
    if rows is not None:
        has &= rows
    num = np.where(tgt, X, 0).sum(1)[has]
    den = (np.where(nb, X, 0).sum(1) / np.maximum(nb.sum(1), 1))[has]
    v, lo, hi, p = boot_ratio(num, den, 1.0)
    return v, lo, hi, p, int(has.sum())


# --------------------------------------------------------------------------- main


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    D = build()
    days, R, V, starts, lab = D["days"], D["R"], D["V"], D["starts"], D["lab"]
    n = len(days)
    r = R.sum(1)
    log(f"{ASSET} 5 minutes, {n} jours gardés {days[0].date()} → {days[-1].date()} "
        f"(écart NY/CET = 6 h, séances complètes) ; {NI} intervalles par jour (gap + 276)")
    log(f"Rendement journalier moyen {r.mean()*1e4:+.2f} bp, σ {r.std()*1e4:.1f} bp ; "
        f"part d'intervalles sans volume (hors gap) {(V[:, 1:] == 0).mean()*100:.1f} %")

    cal = pd.read_csv("config/calendrier_macro_us.csv", parse_dates=["date"])
    dset = lambda names: set(cal.loc[cal["annonce"].isin(names), "date"].dt.normalize())
    a830 = days.isin(dset(ANN_830))
    a1000 = days.isin(dset(ANN_1000))
    fomc = days.isin(dset({"FOMC décision", "FOMC minutes"}))
    log(f"Jours d'annonce : 8:30 {a830.sum()}, 10:00 {a1000.sum()}, FOMC (décision ou minutes) {fomc.sum()}")

    # ---------------------------------------------------------------- A. contribution au prix et à la variance
    log("\n=== A. Contribution au prix et à la variance, 8 périodes du papier (heures NY) ===")
    R2 = R ** 2
    absr = np.abs(r)
    rows = []
    pcs, vcs = {}, {}
    for name, a, b in PERIODS:
        m = tmask(lab, a, b)
        ra = R[:, m].sum(1)
        pc_raw = (ra / np.where(r == 0, np.nan, r))
        pc_raw = pc_raw[np.isfinite(pc_raw)]  # jours à rendement nul exclus
        lo_w, hi_w = np.percentile(pc_raw, [1, 99])
        pc_w = np.clip(pc_raw, lo_w, hi_w)
        wpc_num = np.sign(r) * ra  # contribution pondérée (Barclay-Warner) = Σ sign(r)·r_a / Σ|r|
        vc = R2[:, m].sum(1) / R2.sum(1)
        pcs[name], vcs[name] = (wpc_num, absr), vc
        w, wlo, whi, wp = boot_ratio(wpc_num, absr, 0.0)
        # H2 : WPC − VC, bootstrap commun
        idx = E._block_index(n)
        bd = wpc_num[idx].sum(1) / absr[idx].sum(1) - vc[idx].mean(1)
        diff = w - vc.mean()
        rows.append({"période": name, "NY": f"{a}-{b}", "PC_papier%": pc_raw.mean() * 100,
                     "PC_wins%": pc_w.mean() * 100, "t_PC_wins": nw_t(pc_w), "WPC%": w * 100,
                     "WPC_lo": wlo * 100, "WPC_hi": whi * 100, "VC%": vc.mean() * 100,
                     "WPC-VC%": diff * 100, "diff_lo": np.percentile(bd, 2.5) * 100,
                     "diff_hi": np.percentile(bd, 97.5) * 100, "p_diff": p_boot(bd, 0.0),
                     "moy_bp": ra.mean() * 1e4, "t_moy": nw_t(ra)})
    per = pd.DataFrame(rows)
    per["p_diff_holm"] = holm(per["p_diff"].values)
    per.round(4).to_csv(OUT / "periods.csv", index=False)
    log(per.round(2).to_string(index=False))
    log("PC_papier = moyenne de r_période / r_jour (mesure du papier, instable quand r_jour ≈ 0) ; "
        "PC_wins = idem winsorisé 1 % ; WPC = Σ sign(r)·r_période / Σ|r| (robuste) ; VC = part de Σr².")
    for i, row in per.iterrows():
        hyp("A", f"H2.{i+1}", f"prix = variance, {row['période']}", "WPC − VC (pts de %)", row["WPC-VC%"],
            row["diff_lo"], row["diff_hi"], row["p_diff"], "≈ 0", row["p_diff"] > 0.05)

    m_night = tmask(lab, "18:00", "03:00")
    rn = R[:, m_night].sum(1)
    w, wlo, whi, wp = boot_ratio(np.sign(r) * rn, absr, 0.0)
    vcn = (R2[:, m_night].sum(1) / R2.sum(1)).mean()
    log(f"\nH1 nuit 17:00 → 3:00 NY (avant l'Europe) : WPC {w*100:.1f} % [{wlo*100:.1f} ; {whi*100:.1f}], "
        f"p(=0) {wp:.4f} ; part de variance {vcn*100:.1f} % ; rendement moyen {rn.mean()*1e4:+.2f} bp (t {nw_t(rn):.2f})")
    hyp("A", "H1", "contribution au prix ≈ 0 avant l'ouverture européenne (17:00→3:00 NY)", "WPC nuit (%)",
        w * 100, wlo * 100, whi * 100, wp, "≈ 0", wp > 0.05)
    for pn, a_, z_ in SUBP:
        mm = (days >= a_) & (days <= f"{z_}-12-31")
        ww = (np.sign(r) * rn)[mm].sum() / absr[mm].sum()
        log(f"   {pn} : WPC nuit {ww*100:.1f} %, part de variance {(R2[mm][:, m_night].sum(1)/R2[mm].sum(1)).mean()*100:.1f} %")

    # ---------------------------------------------------------------- B. efficience
    log("\n=== B. Régressions d'absence de biais r_jour = a + b·r_(17:00 → coupure) ===")
    hours = [f"{h:02d}:00" for h in list(range(18, 24)) + list(range(0, 17))]
    cum = np.cumsum(R, axis=1)
    ub = []
    idx = E._block_index(n)
    deltas = {}
    for h in hours:
        if h == "18:00":
            j = 0  # gap seul (17:00 → 18:00)
        else:
            j = lab.index(h) - 1  # dernier intervalle avant h
        x = cum[:, j]
        u = unbiased(x, r)
        # winsorisé 1 % (robustesse)
        q = lambda z: np.clip(z, *np.percentile(z, [1, 99]))
        uw = unbiased(q(x), q(r))
        deltas[h] = boot_delta(x, r, idx)
        ub.append({"coupure_NY": h, "CET": f"{(int(h[:2]) + 6) % 24:02d}:00", **u,
                   "beta_wins": uw["beta"], "t_b1_wins": uw["t_b1"],
                   "delta_lo": np.percentile(deltas[h], 2.5), "delta_hi": np.percentile(deltas[h], 97.5)})
    ub = pd.DataFrame(ub)
    ub["p_b1_holm"] = holm(ub["p_b1"].values)
    ub.round(4).to_csv(OUT / "unbiasedness.csv", index=False)
    log(ub[["coupure_NY", "CET", "beta", "se", "t_b1", "p_b1", "p_b1_holm", "beta_wins", "t_b1_wins", "R2",
            "var_share", "delta", "delta_lo", "delta_hi"]].round(3).to_string(index=False))
    log("b < 1 ⇔ le mouvement jusqu'à la coupure est en partie défait ensuite (cov(r_c, reste) < 0).")
    for _, row in ub.iterrows():
        early = row["coupure_NY"] in ("19:00", "20:00", "21:00", "22:00", "23:00")
        hyp("B", f"H3 {row['coupure_NY']}", "b < 1 (bruit) les 2-5 premières heures" if early else "b ≈ 1 ensuite",
            "b (pente)", row["beta"], row["beta"] - 1.96 * row["se"], row["beta"] + 1.96 * row["se"], row["p_b1"],
            "< 1" if early else "≈ 1", (row["beta"] < 1 and row["p_b1"] < 0.05) if early else row["p_b1"] > 0.05)
    bd = deltas["03:00"] - deltas["01:00"]
    dv = ub.set_index("coupure_NY").loc["03:00", "delta"] - ub.set_index("coupure_NY").loc["01:00", "delta"]
    log(f"\nH4 Δ(3:00) − Δ(1:00) = {dv:+.4f} [{np.percentile(bd, 2.5):+.4f} ; {np.percentile(bd, 97.5):+.4f}], p {p_boot(bd, 0):.4f}")
    hyp("B", "H4", "l'efficience baisse entre clôture asiatique (1:00) et ouverture européenne (3:00)", "ΔΔ",
        dv, np.percentile(bd, 2.5), np.percentile(bd, 97.5), p_boot(bd, 0), "< 0", dv < 0 and p_boot(bd, 0) < 0.05)
    for pn, a_, z_ in SUBP:
        mm = (days >= a_) & (days <= f"{z_}-12-31")
        hh = ("19:00", "20:00", "22:00", "03:00", "05:00", "12:00", "15:00")
        bs = [unbiased(cum[mm][:, lab.index(h) - 1], r[mm]) for h in hh]
        log(f"   {pn} : " + " ; ".join(f"b({h}) {u['beta']:.3f} (t vs 1 {u['t_b1']:+.2f})" for h, u in zip(hh, bs)))

    # ---------------------------------------------------------------- C. volatilité
    log("\n=== C. Pics de volatilité : E[r²] à l'intervalle / E[r²] des voisins ([T-30, T) et [T+15, T+45)) ===")
    ev = [
        ("H5.1", "ouverture de Tokyo 9:00 JST", E.at(days, "09:00", TOKYO), None),
        ("H5.4", "8:20 NY (ancienne ouverture de la corbeille)", E.at(days, "08:20", NY), None),
        ("H5.5", "8:30 NY (macro US, tous les jours)", E.at(days, "08:30", NY), None),
        ("H5.6", "10:00 NY (macro US, tous les jours)", E.at(days, "10:00", NY), None),
        ("H5.7", "13:30 NY (règlement COMEX, ancienne clôture de la corbeille)", E.at(days, "13:30", NY), None),
        ("H5.8", "14:00 NY jours FOMC", E.at(days, "14:00", NY), fomc),
        ("H5.9", "16:00 NY (clôture des actions US)", E.at(days, "16:00", NY), None),
    ]
    vrows = []
    for code, name, T, rows_ in ev:
        v, lo, hi, p, nn = spike(R2, starts, T, rows_)
        vrows.append({"code": code, "événement": name, "n": nn, "rapport": v, "lo": lo, "hi": hi, "p": p})
        hyp("C", code, f"pic de volatilité : {name}", "rapport de variance", v, lo, hi, p, "> 1", lo > 1)
    # montée pendant l'Asie et marche à l'ouverture européenne (niveaux horaires)
    def lvl(a, b):
        return R2[:, tmask(lab, a, b)].mean(1)
    for code, name, (a1, b1), (a2, b2) in [
        ("H5.2", "montée pendant l'Asie : 2:00-3:00 contre 20:00-21:00", ("02:00", "03:00"), ("20:00", "21:00")),
        ("H5.3", "ouverture européenne : 3:00-4:00 contre 2:00-3:00", ("03:00", "04:00"), ("02:00", "03:00")),
    ]:
        v, lo, hi, p = boot_ratio(lvl(a1, b1), lvl(a2, b2), 1.0)
        vrows.append({"code": code, "événement": name, "n": n, "rapport": v, "lo": lo, "hi": hi, "p": p})
        hyp("C", code, name, "rapport de variance", v, lo, hi, p, "> 1", lo > 1)
    vt = pd.DataFrame(vrows).sort_values("code")
    vt["p_holm"] = holm(vt["p"].values)
    log(vt.round(3).to_string(index=False))

    # profil horaire de volatilité (RMS en bp par intervalle de 5 min)
    rms = np.sqrt(R2.mean(0)) * 1e4
    top = pd.Series(rms[1:], index=lab[1:]).sort_values(ascending=False).head(15)
    log("\n15 intervalles les plus volatils (hors gap), RMS en bp par 5 min : "
        + ", ".join(f"{k} {v:.1f}" for k, v in top.items()))
    log(f"Gap de l'arrêt : RMS {rms[0]:.1f} bp ; médiane des intervalles {np.median(rms[1:]):.1f} bp")
    hr_ = [f"{h:02d}:00" for h in list(range(18, 24)) + list(range(0, 17))]
    log("Volatilité horaire (RMS moyen des intervalles de 5 min, bp ; descriptif) : " + ", ".join(
        f"{h} {np.sqrt(R2[:, tmask(lab, h, hr_[i+1] if i + 1 < len(hr_) else '17:00')][:, (1 if h == '18:00' else 0):].mean()) * 1e4:.1f}"
        for i, h in enumerate(hr_)))

    # ---------------------------------------------------------------- D. sauts
    DV, JV, J = jumps(R)
    TV = DV + JV
    log("\n=== D. Diffusion et sauts (MedRV + Lee-Mykland, K = 277, seuil 99,9 %) ===")
    ok_rows = np.arange(n) >= 1  # le premier jour n'a pas de fenêtre complète
    jshare = boot_ratio(JV[ok_rows].sum(1), TV[ok_rows].sum(1), 0.05)
    jshare_r2 = JV[ok_rows].sum() / R2[ok_rows].sum()
    log(f"H7 part des sauts dans la variance : {jshare[0]*100:.2f} % de ΣTV [{jshare[1]*100:.2f} ; {jshare[2]*100:.2f}] "
        f"({jshare_r2*100:.2f} % de Σr²) ; sauts détectés : {J[ok_rows].mean()*100:.3f} % des intervalles, "
        f"{J[ok_rows].sum(1).mean():.2f} par jour")
    log(f"   sans le gap : {JV[ok_rows][:, 1:].sum() / TV[ok_rows].sum() * 100:.2f} % ; gap seul : "
        f"{JV[ok_rows][:, 0].sum() / TV[ok_rows].sum() * 100:.2f} %")
    hyp("D", "H7", "sauts = 5 à 13 % de la variance journalière", "part des sauts (%)", jshare[0] * 100,
        jshare[1] * 100, jshare[2] * 100, np.nan, "5-13 %", 5 <= jshare[0] * 100 <= 13)
    for pn, a_, z_ in SUBP:
        mm = ok_rows & (days >= a_) & (days <= f"{z_}-12-31")
        log(f"   {pn} : sauts {JV[mm].sum()/TV[mm].sum()*100:.2f} % ; 8:30 {JV[mm][:, lab.index('08:30')].sum()/TV[mm].sum()*100:.2f} %")
    contrib = JV[ok_rows].sum(0) / TV[ok_rows].sum(1).sum()
    ct = pd.Series(contrib, index=lab)
    rank = ct.drop(["gap", "18:00"]).sort_values(ascending=False)
    log("Plus gros contributeurs de sauts (hors réouverture), % de la variance totale : "
        + ", ".join(f"{k} {v*100:.2f}" for k, v in rank.head(10).items()))
    j830 = lab.index("08:30")
    tvd = TV[ok_rows].sum(1)
    c830 = boot_ratio(JV[ok_rows][:, j830], tvd, 0.0)
    log(f"H8 8:30 : {c830[0]*100:.2f} % [{c830[1]*100:.2f} ; {c830[2]*100:.2f}] (papier : or 1,22 %), rang {list(rank.index).index('08:30') + 1}")
    # rang 1 dans les tirages bootstrap
    idx = E._block_index(int(ok_rows.sum()))
    JVo = JV[ok_rows][:, 2:]
    sums = np.stack([JVo[ix].sum(0) for ix in idx[:500]])
    r1 = (sums.argmax(1) == (j830 - 2)).mean()
    log(f"   8:30 au rang 1 dans {r1*100:.0f} % de 500 tirages bootstrap")
    hyp("D", "H8", "8:30 = plus gros contributeur de sauts (hors réouverture)", "part 8:30 (%) ; rang",
        c830[0] * 100, c830[1] * 100, c830[2] * 100, 1 - r1, "rang 1", rank.index[0] == "08:30")
    j1000 = lab.index("10:00")
    fed = [lab.index(h) for h in ("14:00", "14:05", "14:10", "14:15", "14:20", "14:25", "14:30", "14:35", "14:40")]
    JVd = JV[ok_rows]
    x10 = JVd[:, j1000]
    xfed = JVd[:, fed].max(1)  # le plus gros saut de 14:00-14:45, comme le tableau 7
    diff = (x10 - xfed)
    v, lo, hi, p = boot_ratio(diff, tvd, 0.0)
    log(f"H9 10:00 − max(14:00-14:45) : {v*100:+.3f} pts [{lo*100:+.3f} ; {hi*100:+.3f}], p {p:.4f} "
        f"(10:00 {x10.sum()/tvd.sum()*100:.2f} %, Fed {xfed.sum()/tvd.sum()*100:.2f} %)")
    hyp("D", "H9", "métaux : sauts de 10:00 > sauts de la Fed (14:00-14:45)", "écart (pts de %)", v * 100, lo * 100,
        hi * 100, p, "> 0", lo > 0)
    a830o = a830[ok_rows]
    ja, jn = JVd[a830o, j830].mean(), JVd[~a830o, j830].mean()
    share_ann = JVd[a830o, j830].sum() / JVd[:, j830].sum()
    xx = JVd[:, j830]
    # écart des moyennes jour d'annonce / sans annonce, bootstrap
    bb = []
    for ix in E._block_index(len(xx)):
        aa = a830o[ix]
        bb.append(xx[ix][aa].mean() - xx[ix][~aa].mean())
    bb = np.array(bb)
    log(f"H10 saut moyen à 8:30 : jours d'annonce {ja*1e8:.2f} contre {jn*1e8:.2f} (bp²) ; "
        f"{share_ann*100:.0f} % de la variance de saut de 8:30 tombe les jours d'annonce ({a830o.mean()*100:.0f} % des jours)")
    hyp("D", "H10", "le saut de 8:30 vient des annonces", "écart de saut moyen (bp²)", (ja - jn) * 1e8,
        np.percentile(bb, 2.5) * 1e8, np.percentile(bb, 97.5) * 1e8, p_boot(bb, 0), "> 0", np.percentile(bb, 2.5) > 0)
    dv_ = pd.Series(np.sqrt(DV.mean(0)) * 1e4, index=lab)

    # U en séance COMEX : diffusion, jours sans annonce
    quiet = ~(a830 | a1000 | fomc)
    def dvl(a, b):
        return DV[quiet][:, tmask(lab, a, b)].mean(1)
    first, mid, last = dvl("08:20", "09:20"), dvl("10:50", "11:50"), dvl("12:30", "13:30")
    v, lo, hi, p = boot_ratio((first + last) / 2, mid, 1.0)
    log(f"\nH6 U en séance COMEX (diffusion, {quiet.sum()} jours sans annonce) : (8:20-9:20 + 12:30-13:30)/2 ÷ 10:50-11:50 "
        f"= {v:.3f} [{lo:.3f} ; {hi:.3f}], p {p:.4f} ; début/milieu {first.mean()/mid.mean():.2f}, fin/milieu {last.mean()/mid.mean():.2f}")
    hyp("C", "H6", "pas de U en séance COMEX (or)", "rapport bords/milieu", v, lo, hi, p, "≈ 1 (pas de U)", not (lo > 1))

    # ---------------------------------------------------------------- E. volume et volatilité
    log("\n=== E. Volume et volatilité (parts journalières, gap exclu) ===")
    Vs = V[:, 1:] / V[:, 1:].sum(1, keepdims=True)
    A = np.abs(R[:, 1:])
    As = A / A.sum(1, keepdims=True)
    lab1 = lab[1:]
    comex = tmask(lab, "08:20", "13:30")[1:]
    diff_out = (As[:, ~comex] - Vs[:, ~comex]).sum(1)
    v, lo, hi, p = boot_mean(diff_out)
    log(f"H11 hors séance COMEX : part de volatilité − part de volume = {v*100:+.1f} pts [{lo*100:+.1f} ; {hi*100:+.1f}], p {p:.4f} "
        f"(volume hors séance {Vs[:, ~comex].sum(1).mean()*100:.1f} %, volatilité {As[:, ~comex].sum(1).mean()*100:.1f} %)")
    hyp("E", "H11", "volume < volatilité hors séance COMEX (8:20-13:30)", "écart de parts (pts)", v * 100, lo * 100,
        hi * 100, p, "> 0", lo > 0)
    D_ = Vs - As
    st1 = starts[:, 1:]
    erows = []
    for code, name, T in [("H12.1", "8:30", E.at(days, "08:30", NY)), ("H12.2", "10:00", E.at(days, "10:00", NY)),
                          ("H13.1", "8:20", E.at(days, "08:20", NY)), ("H13.2", "13:30", E.at(days, "13:30", NY)),
                          ("H13.3", "9:30", E.at(days, "09:30", NY))]:
        Tv = pd.DatetimeIndex(T).as_unit("ns").values[:, None]
        dt = (st1 - Tv) / np.timedelta64(1, "m")
        tgt, nb = dt == 0, ((dt >= -30) & (dt < 0)) | ((dt >= 15) & (dt < 45))
        x = np.where(tgt, D_, 0).sum(1) - np.where(nb, D_, 0).sum(1) / nb.sum(1)
        v, lo, hi, p = boot_mean(x)
        vol_sp = Vs[tgt.any(1)][tgt[tgt.any(1)]].mean() / Vs[nb].mean()
        abs_sp = As[tgt.any(1)][tgt[tgt.any(1)]].mean() / As[nb].mean()
        erows.append({"code": code, "heure": name, "pic_volume×": vol_sp, "pic_volatilité×": abs_sp,
                      "excès_pts": v * 100, "lo": lo * 100, "hi": hi * 100, "p": p})
        hyp("E", code, f"à {name}, le volume monte plus que la volatilité", "excès de part (pts)", v * 100, lo * 100,
            hi * 100, p, "> 0", lo > 0)
    et = pd.DataFrame(erows)
    et["p_holm"] = holm(et["p"].values)
    log(et.round(3).to_string(index=False))

    m_n1 = m_night[1:]
    vn = Vs[:, m_n1].sum(1)
    num = np.sign(r) * R[:, m_night].sum(1)
    idx = E._block_index(n)
    b = (num[idx].sum(1) / absr[idx].sum(1)) / vn[idx].mean(1)
    val = (num.sum() / absr.sum()) / vn.mean()
    log(f"H14 nuit 18:00 → 3:00 : WPC / part de volume = {val:.2f} [{np.percentile(b, 2.5):.2f} ; {np.percentile(b, 97.5):.2f}] "
        f"(part de volume {vn.mean()*100:.1f} %)")
    hyp("E", "H14", "plus de prix par contrat la nuit (VWPC > 1)", "WPC/part de volume", val, np.percentile(b, 2.5),
        np.percentile(b, 97.5), p_boot(b, 1.0), "> 1", np.percentile(b, 2.5) > 1)

    # ---------------------------------------------------------------- synthèse
    pd.DataFrame({"intervalle": lab, "rms_bp": rms, "diffusion_rms_bp": dv_.values,
                  "saut_part%": contrib * 100, "volume_part%": np.r_[0, Vs.mean(0)] * 100,
                  "volatilité_part%": np.r_[0, As.mean(0)] * 100, "moy_bp": R.mean(0) * 1e4}).round(4).to_csv(
        OUT / "intervals.csv", index=False)
    H = pd.DataFrame(HYP)
    H["p_holm_famille"] = np.nan
    for f, g in H.groupby("famille"):
        ok = g["p"].notna()
        H.loc[g.index[ok], "p_holm_famille"] = holm(g.loc[ok, "p"].values)
    H.round(4).to_csv(OUT / "hypotheses.csv", index=False)
    log(f"\n=== Synthèse : {len(H)} tests ===")
    log(H[["code", "affirmation", "valeur", "ic_lo", "ic_hi", "p", "p_holm_famille", "attendu", "conforme_brut"]]
        .round(4).to_string(index=False))
    (OUT / "run.log").write_text("\n".join(LINES), encoding="utf-8")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ASSET = sys.argv[1]
        OUT = Path(f"results/{ASSET.lower()}_fattinger")
    main()
