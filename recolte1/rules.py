"""Règles extraites des papiers de la récolte 1, une fonction par papier.

Chaque fonction reçoit un actif et renvoie {nom de règle: trades}, où trades a les colonnes
t_in, t_out (UTC), w (poids signé : +1 long, -1 short) et day (séance NYSE de l'entrée).
Horloge commune : séance NYSE (calendrier XNYS, 9:30 → clôture officielle, 13:00 les
demi-séances), sauf quand le papier fixe une autre horloge (sessions UTC de [21], CET de [20]).
Les seuils "historiques" (terciles, quartiles, médianes) n'utilisent que le passé.
"""

from __future__ import annotations

from functools import lru_cache

import exchange_calendars as xc
import numpy as np
import pandas as pd

from recolte1.engine import CET, LDN, NY, at, load, price_at

START, END = "2016-01-05", "2026-08-28"


@lru_cache(maxsize=None)
def sessions() -> pd.DataFrame:
    s = xc.get_calendar("XNYS").schedule.loc[START:END]
    b = pd.DataFrame(index=pd.DatetimeIndex(s.index, name="day"))
    b["t_open"] = pd.DatetimeIndex(s["open"].values).tz_localize("UTC")  # calendrier en UTC
    b["t_close"] = pd.DatetimeIndex(s["close"].values).tz_localize("UTC")
    b["t_prev"] = b["t_close"].shift(1)
    b["half"] = b["t_close"].dt.tz_convert(NY).dt.hour < 16
    return b.iloc[1:]


@lru_cache(maxsize=None)
def base(name: str) -> pd.DataFrame:
    """Une ligne par séance : prix à la clôture précédente, à l'ouverture et à la clôture."""
    b = sessions().copy()
    for c in ["prev", "open", "close"]:
        b[f"p_{c}"] = price_at(name, b[f"t_{c}"])[0]
    b["on"] = b["p_open"] / b["p_prev"] - 1  # nuit : clôture veille → ouverture
    b["id"] = b["p_close"] / b["p_open"] - 1  # jour : ouverture → clôture
    b["cc"] = b["p_close"] / b["p_prev"] - 1
    return b


def tr(t_in, t_out, w, day) -> pd.DataFrame:
    t = pd.DataFrame({"t_in": t_in, "t_out": t_out, "w": w, "day": day})
    return t.dropna(subset=["t_in", "t_out"])


def night(b, w=1.0, mask=None):
    """Nuit qui se termine à l'ouverture de la séance `day`."""
    w = pd.Series(w, index=b.index) if np.isscalar(w) else w
    if mask is not None:
        w = w.where(mask, 0.0)
    return tr(b["t_prev"], b["t_open"], w.fillna(0.0), b.index)


def day(b, w=1.0, mask=None):
    w = pd.Series(w, index=b.index) if np.isscalar(w) else w
    if mask is not None:
        w = w.where(mask, 0.0)
    return tr(b["t_open"], b["t_close"], w.fillna(0.0), b.index)


def both(*parts):
    return pd.concat(parts, ignore_index=True)


def monthly(b: pd.DataFrame, col: str) -> pd.Series:
    """Somme des log-rendements du mois civil (indexée par fin de mois)."""
    return np.log1p(b[col]).groupby(b.index.to_period("M")).sum()


def next_month_sign(b: pd.DataFrame, msig: pd.Series) -> pd.Series:
    """Signe du signal du mois m, appliqué à chaque séance du mois m+1."""
    per = b.index.to_period("M")
    return pd.Series(np.sign(msig.reindex(per - 1).values), index=b.index)


# --------------------------------------------------------------------------- [1] Boyarchenko-Larsen-Whelan


def p01(name):
    b = sessions()
    d = b.index
    r = {
        "CTC 16:15→16:15": tr(at(d, "16:15", NY).shift(1), at(d, "16:15", NY), 1.0, d),
        "CTO 16:15→9:30": tr(at(d, "16:15", NY).shift(1), at(d, "09:30", NY), 1.0, d),
        "CTO 16:15→8:30": tr(at(d, "16:15", NY).shift(1), at(d, "08:30", NY), 1.0, d),
        "OTC 9:30→16:15": tr(at(d, "09:30", NY), at(d, "16:15", NY), 1.0, d),
        "-OR short 8:30→10:00": tr(at(d, "08:30", NY), at(d, "10:00", NY), -1.0, d),
        "OD 2:00→3:00 ET": tr(at(d, "02:00", NY), at(d, "03:00", NY), 1.0, d),
        "OD+ 1:30→3:30 ET": tr(at(d, "01:30", NY), at(d, "03:30", NY), 1.0, d),
        "OD ouverture Europe 7:00→8:00 Londres": tr(at(d, "07:00", LDN), at(d, "08:00", LDN), 1.0, d),
        "short 9:00→10:00 ET": tr(at(d, "09:00", NY), at(d, "10:00", NY), -1.0, d),
        "short 9:00→10:00 ET jeu+ven": tr(at(d, "09:00", NY), at(d, "10:00", NY),
                                          np.where(d.dayofweek.isin([3, 4]), -1.0, 0.0), d),
    }
    # Table I : chaque heure ET du jour CME (18:00 veille → 17:00)
    for h in list(range(18, 24)) + list(range(0, 17)):
        off = -1 if h >= 18 else 0
        r[f"heure {h:02d}:00→{(h + 1) % 24:02d}:00 ET"] = tr(at(d, f"{h:02d}:00", NY, off),
                                                            at(d, f"{(h + 1) % 24:02d}:00", NY, off if h < 23 else 0), 1.0, d)
    return r


# --------------------------------------------------------------------------- [2] Berkman et al.


def p02(name):
    b = base(name)
    vol = b["cc"].shift(1) ** 2  # attention : (rendement close-to-close d'hier)²
    # tercile haut des cc² connus à la clôture d'hier (jours ≤ d-1)
    hi = vol > (b["cc"] ** 2).expanding(min_periods=60).quantile(2 / 3).shift(1)
    vol20 = b["cc"].rolling(20, min_periods=15).std().shift(1)
    hard = vol20 > vol20.expanding(min_periods=60).median().shift(1)
    mon = pd.Series(b.index.dayofweek == 0, index=b.index)
    return {
        "DIFF long nuit + short jour": both(night(b), day(b, -1.0)),
        "long nuit si VOL(t-1) tercile haut": night(b, mask=hi),
        "short jour si VOL(t-1) tercile haut": day(b, -1.0, mask=hi),
        "DIFF si VOL(t-1) tercile haut": both(night(b, mask=hi), day(b, -1.0, mask=hi)),
        "DIFF si VOL(t-1) haut et vol 20 j > médiane": both(night(b, mask=hi & hard), day(b, -1.0, mask=hi & hard)),
        "DIFF si VOL(t-1) haut, lundis": both(night(b, mask=hi & mon), day(b, -1.0, mask=hi & mon)),
    }


# --------------------------------------------------------------------------- [3] Lu-Qin


def p03(name):
    b = sessions()
    d = b.index
    r = {}
    for o in ["10:00", "10:30", "11:00"]:
        t_o = at(d, o, NY)
        r[f"NMD ouverture déplacée à {o}"] = both(tr(b["t_prev"], t_o, 1.0, d), tr(t_o, b["t_close"], -1.0, d))
    full = ~b["half"]
    for c in ["14:30", "15:00", "15:30"]:
        t_c = at(d, c, NY)
        t_c_prev = t_c.shift(1)
        w = pd.Series(np.where(full & full.shift(1, fill_value=False), 1.0, 0.0), index=d)
        r[f"NMD clôture avancée à {c}"] = both(tr(t_c_prev, b["t_open"], w, d), tr(b["t_open"], t_c, -w, d))
    # signaux mensuels (tri croissant, Table 1) : MOM (t-12..t-2) → NMD +, STR (mois t) → NMD -
    bb = base(name)
    m_cc = monthly(bb, "cc")
    mom = m_cc.shift(1).rolling(11, min_periods=11).sum()  # mois m-11..m-1 au mois m → t-12..t-2 vu de m+1
    s_mom = next_month_sign(bb, mom)
    s_str = -next_month_sign(bb, m_cc)
    r["NMD × signe(MOM 12-1)"] = both(night(bb, s_mom), day(bb, -s_mom))
    r["NMD × -signe(STR 1 mois)"] = both(night(bb, s_str), day(bb, -s_str))
    return r


# --------------------------------------------------------------------------- [4] Jones-Pyun-Wang


def p04(name):
    b = sessions()
    d = b.index
    p945, _ = price_at(name, at(d, "09:45", NY))
    p1500, _ = price_at(name, at(d, "15:00", NY))
    sig = np.sign(p1500 / p945 - 1).where(~b["half"], 0.0).fillna(0.0)
    t_959 = b["t_close"] - pd.Timedelta(minutes=1)  # 15:59 (12:59 les demi-séances)
    t945_next = at(d, "09:45", NY).shift(-1)
    t959_next = t_959.shift(-1)
    pos = sig.clip(lower=0)
    return {
        "nuit 15:59→9:45 × signe(r 9:45→15:00)": tr(t_959, t945_next, sig, d),
        "nuit long si r(9:45→15:00) > 0": tr(t_959, t945_next, pos, d),
        "jour suivant 9:45→15:59 × -signe(r)": tr(t945_next, t959_next, -sig, d),
        "nuit - jour suivant": both(tr(t_959, t945_next, sig, d), tr(t945_next, t959_next, -sig, d)),
    }


# --------------------------------------------------------------------------- [6] Hendershott-Livdan-Rösch : voir run_recolte1.p06 (portefeuille multi-actifs)


# --------------------------------------------------------------------------- [7] Tompkins-Wiener


OWN = {  # séance propre du future (fab.core.ASSETS)
    "GC": ("08:20", "13:30", NY), "6E": ("08:00", "16:00", LDN), "6B": ("08:00", "16:00", LDN),
    "6J": ("08:00", "16:00", LDN), "6A": ("08:00", "16:00", LDN),
}


def p07(name):
    b = base(name)
    r = {
        "O/C long (jour)": day(b),
        "C/O long (nuit)": night(b),
        "alpha : long nuit + short jour": both(night(b), day(b, -1.0)),
    }
    if name in OWN:
        o, c, tz = OWN[name]
        d = b.index
        t_o, t_c = at(d, o, tz), at(d, c, tz)
        r["O/C long (séance propre)"] = tr(t_o, t_c, 1.0, d)
        r["C/O long (séance propre)"] = tr(t_c.shift(1), t_o, 1.0, d)
        r["alpha (séance propre)"] = both(tr(t_c.shift(1), t_o, 1.0, d), tr(t_o, t_c, -1.0, d))
    return r


# --------------------------------------------------------------------------- [8] Abdi


def p08(name):
    b = base(name)
    es = base("ES")["on"].reindex(b.index)
    neg = b["on"] < 0
    neg_es = es < 0
    nxt = lambda m: m.shift(1, fill_value=False)  # nuit d+1 = nuit qui se termine à l'ouverture de d+1
    return {
        "short jour si nuit < 0": day(b, -1.0, mask=neg),
        "long nuit suivante si nuit < 0": night(b, mask=nxt(neg)),
        "cycle : short jour + long nuit suivante si nuit < 0": both(day(b, -1.0, mask=neg), night(b, mask=nxt(neg))),
        "cycle avec signal marché = nuit ES < 0": both(day(b, -1.0, mask=neg_es), night(b, mask=nxt(neg_es))),
    }


# --------------------------------------------------------------------------- [9] Branch-Ma


def p09(name):
    b = base(name)
    on = b["on"]
    q_neg = on.where(on < 0).expanding(min_periods=60).quantile(0.25).shift(1)
    q_pos = on.where(on > 0).expanding(min_periods=60).quantile(0.75).shift(1)
    ext = pd.Series(np.where(on <= q_neg, 1.0, np.where(on >= q_pos, -1.0, 0.0)), index=b.index)
    return {
        "jour × -signe(nuit)": day(b, -np.sign(on)),
        "jour × -signe(nuit), quartile extrême": day(b, ext),
    }


# --------------------------------------------------------------------------- sauts de Lee-Mykland (utilisés par [10] et [11])


def lm_jumps(r: pd.Series, alpha: float, K: int = 16) -> pd.Series:
    """Saut si (|L| - C_n)/S_n > -ln(-ln(1-alpha)), L = r / sqrt(IntV),
    IntV = 1/(K-2) Σ_{j=i-K+2}^{i-1} |r_j||r_{j-1}| ; n = nombre d'observations."""
    x = np.log1p(r)
    a = (x.abs() * x.abs().shift(1))
    intv = a.shift(1).rolling(K - 2, min_periods=K - 2).sum() / (K - 2)
    L = x / np.sqrt(intv)
    n = x.notna().sum()
    c = np.sqrt(2 / np.pi)
    ln = np.sqrt(2 * np.log(n))
    Cn = ln / c - (np.log(np.pi) + np.log(np.log(n))) / (2 * c * ln)
    Sn = 1 / (c * ln)
    return ((L.abs() - Cn) / Sn) > -np.log(-np.log(1 - alpha))


# --------------------------------------------------------------------------- [10] Bahcivan-Dam-Gonenc


def p10(name):
    b = base(name)
    d = b.index
    r = {}
    for alpha in [0.01, 0.05]:
        j = lm_jumps(b["on"], alpha)
        w = pd.Series(np.where(j, -np.sign(b["on"]), 0.0), index=d)
        for h in range(1, 6):
            r[f"contrarian saut nuit α={alpha:.0%} détention {h} j"] = tr(b["t_open"], b["t_close"].shift(-(h - 1)), w, d)
        r[f"long après saut négatif α={alpha:.0%} 1 j"] = day(b, w.clip(lower=0))
        r[f"short après saut positif α={alpha:.0%} 1 j"] = day(b, w.clip(upper=0))
    return r


# --------------------------------------------------------------------------- [11] Bahcivan (tug of war)


def p11(name):
    b = base(name)
    s_on = next_month_sign(b, monthly(b, "on"))
    s_id = next_month_sign(b, monthly(b, "id"))
    jm = lm_jumps(b["on"], 0.01).groupby(b.index.to_period("M")).any()
    jump_prev = pd.Series(jm.reindex(b.index.to_period("M") - 1).fillna(False).astype(bool).values, index=b.index)
    r = {}
    for lab, m in [("tous mois", None), ("mois avec saut", jump_prev), ("mois sans saut", ~jump_prev)]:
        r[f"tri nuit : nuit × signe(nuit m-1), {lab}"] = night(b, s_on, mask=m)
        r[f"tri nuit : jour × -signe(nuit m-1), {lab}"] = day(b, -s_on, mask=m)
        r[f"tri jour : nuit × -signe(jour m-1), {lab}"] = night(b, -s_id, mask=m)
        r[f"tri jour : jour × signe(jour m-1), {lab}"] = day(b, s_id, mask=m)
    return r


# --------------------------------------------------------------------------- [14] Donninger


def p14(name):
    b = sessions()
    d = b.index
    t16 = at(d, "16:00", NY).shift(1)  # 16:00 de la séance précédente
    t930, t933 = at(d, "09:30", NY), at(d, "09:33", NY)
    p16, _ = price_at(name, t16)
    p930, _ = price_at(name, t930)
    t_out = t930.where(p930 / p16 - 1 < 0, t933)
    prev_fri = pd.Series(d, index=d).shift(1).dt.dayofweek == 4
    return {
        "long 16:00→9:30": tr(t16, t930, 1.0, d),
        "long 16:00→9:30 (9:33 si gain)": tr(t16, t_out, 1.0, d),
        "idem sans entrée le vendredi": tr(t16, t_out, np.where(prev_fri, 0.0, 1.0), d),
    }


# --------------------------------------------------------------------------- [15] Vojtko-Hanicová


def p15(name):
    b = base(name)
    c = b["p_close"]
    r = {"nuit sans filtre": night(b)}
    for n in [10, 20, 50]:
        up = (c > c.rolling(n, min_periods=n).mean()).shift(1, fill_value=False)
        r[f"nuit si close > MM{n} (veille)"] = night(b, mask=up)
    up20 = (c > c.rolling(20, min_periods=20).mean()).shift(1, fill_value=False)
    r["nuit si close > MM20 et nuit précédente < 0"] = night(b, mask=up20 & (b["on"].shift(1) < 0))
    return r


# --------------------------------------------------------------------------- [19] Aretz-Bartram


def p19(name):
    b = base(name)
    r = {}
    for k, lab in enumerate(["lundi", "mardi", "mercredi", "jeudi", "vendredi"]):
        m = pd.Series(b.index.dayofweek == k, index=b.index)
        r[f"jour long le {lab}"] = day(b, mask=m)
        r[f"nuit long vers {lab}"] = night(b, mask=m)
    m_cc = monthly(b, "cc")
    mom = m_cc.shift(1).rolling(11, min_periods=11).sum()  # t-12..t-2
    ltr = m_cc.shift(12).rolling(24, min_periods=24).sum()  # t-36..t-13
    s_mom, s_ltr = next_month_sign(b, mom), -next_month_sign(b, ltr)
    r["momentum 12-1 sur le jour"] = day(b, s_mom)
    r["momentum 12-1 sur la nuit"] = night(b, s_mom)
    r["reversal LT 36-13 sur le jour"] = day(b, s_ltr)
    r["reversal LT 36-13 sur la nuit"] = night(b, s_ltr)
    return r


# --------------------------------------------------------------------------- [20] Fattinger-Ziegler


def p20(name):
    days = pd.bdate_range(START, END)
    ny_dst = pd.Series([bool(pd.Timestamp(x).tz_localize(NY).dst()) for x in days + pd.Timedelta(hours=12)], index=days)
    eu_dst = pd.Series([bool(pd.Timestamp(x).tz_localize(CET).dst()) for x in days + pd.Timedelta(hours=12)], index=days)
    days = days[~(ny_dst & ~eu_dst).values]  # le papier supprime ces jours
    per = [("00:00", "01:00"), ("01:00", "08:00"), ("08:00", "09:00"), ("09:00", "13:00"),
           ("13:00", "15:30"), ("15:30", "17:30"), ("17:30", "22:00"), ("22:00", "24:00")]
    r = {}
    for i, (a, z) in enumerate(per, 1):
        t_z = at(days, "00:00", CET, 1) if z == "24:00" else at(days, z, CET)
        r[f"P{i} {a}→{z} CET"] = tr(at(days, a, CET), t_z, 1.0, days)
    return r


# --------------------------------------------------------------------------- [21] Wei


def p21(name):
    """Sessions UTC chaînées : Asie 00:00-08:00, Europe 08:00-14:30, US+late 14:30-24:00.
    Rendement = dernière clôture de la session / dernière clôture de la session précédente."""
    df = load(name)
    days = pd.date_range(START, END, freq="D")
    rows = []
    for lab, a, z, dz in [("asia", "00:00", "08:00", 0), ("europe", "08:00", "14:30", 0), ("us", "14:30", "00:00", 1)]:
        h, m = map(int, a.split(":"))
        hz, mz = map(int, z.split(":"))
        rows.append(pd.DataFrame({
            "sess": lab,
            "t_a": (days + pd.Timedelta(hours=h, minutes=m)).tz_localize("UTC"),
            "t_z": (days + pd.Timedelta(days=dz, hours=hz, minutes=mz)).tz_localize("UTC"),
            "day": days,
        }))
    s = pd.concat(rows).sort_values("t_a").reset_index(drop=True)
    # garder les sessions qui contiennent au moins une barre
    cnt = np.searchsorted(df.index.values, s["t_z"].values) - np.searchsorted(df.index.values, s["t_a"].values)
    s = s[cnt > 0].reset_index(drop=True)
    s["p_end"] = price_at(name, s["t_z"], slack_min=60 * 24 * 4)[0].values  # dernière clôture de la session
    s["ret"] = s["p_end"] / s["p_end"].shift(1) - 1
    s["t_in"] = s["t_z"].shift(1)  # entrée = fin de la session précédente
    sig = np.sign(s["ret"].shift(1))
    r = {}
    for lab in ["asia", "europe", "us"]:
        r[f"passif session {lab}"] = tr(s["t_in"], s["t_z"], np.where(s["sess"] == lab, 1.0, 0.0), s["day"])
    r["momentum toutes sessions long-short"] = tr(s["t_in"], s["t_z"], sig, s["day"])
    r["momentum toutes sessions long-only"] = tr(s["t_in"], s["t_z"], sig.clip(lower=0), s["day"])
    for lab in ["asia", "europe", "us"]:
        on = (s["sess"] == lab).astype(float)
        r[f"momentum {lab} seule long-short"] = tr(s["t_in"], s["t_z"], sig * on, s["day"])
        r[f"momentum {lab} seule long-only"] = tr(s["t_in"], s["t_z"], sig.clip(lower=0) * on, s["day"])
    return r


PAPERS = {
    "[1] Boyarchenko-Larsen-Whelan": p01,
    "[2] Berkman-Koch-Tuttle-Zhang": p02,
    "[3] Lu-Qin": p03,
    "[4] Jones-Pyun-Wang": p04,
    "[7] Tompkins-Wiener": p07,
    "[8] Abdi": p08,
    "[9] Branch-Ma": p09,
    "[10] Bahcivan-Dam-Gonenc": p10,
    "[11] Bahcivan": p11,
    "[14] Donninger": p14,
    "[15] Vojtko-Hanicová": p15,
    "[19] Aretz-Bartram": p19,
    "[20] Fattinger-Ziegler": p20,
    "[21] Wei": p21,
}
# 75 min : le prix de la réouverture CME (18:00 ET = 00:00 CET) est la clôture de 16:59 ET,
# l'écart de réouverture tombe dans la fenêtre qui commence à la réouverture
SLACK = {"[1] Boyarchenko-Larsen-Whelan": 75, "[20] Fattinger-Ziegler": 75, "[21] Wei": 60 * 24 * 4}
