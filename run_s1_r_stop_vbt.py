"""S1 Noise Area NQ + stop dur 1R + risque fixe (S1_R_stop.py, fichier transmis le 2026-10-31) refait avec vectorbt.

EXPLORATOIRE, hors compteur : c'est la bande de bruit M2 sur NQ (rejetée au DSR, PREREGISTRATION_2 piste B) avec
d'autres réglages (30 séances, bande 1,2 sigma, filtre VWAP) et un stop dur. Le registre des échecs ne la rouvre
que sur le holdout postérieur au 2026-08-28 : ce script s'arrête au 2026-08-28 et ne change aucun verdict.

uv run python run_s1_r_stop_vbt.py → results/s1_r_stop/ (run.log, trades_<config>.csv, controle_<config>.csv)

Règles (docstring de S1_R_stop.py), séance cash XNYS 9:30-16:00 New York (13:00 les demi-séances) :
  1. sigma(t) = moyenne des |Close(t) / Open - 1| des 30 séances précédentes, même minute t ;
  2. Upper = max(Open, clôture veille) x (1 + 1,2 sigma) ; Lower = min(Open, clôture veille) x (1 - 1,2 sigma) ;
  3. contrôle à 10:00, 10:30 ... sur la clôture de la minute : long si Close > Upper et > VWAP, short si
     Close < Lower et < VWAP, sinon à plat ; ordre à l'ouverture de la minute suivante ; sortie à la clôture ;
  4. R = |Close - stop suiveur| (max(Upper, VWAP) / min(Lower, VWAP)), au moins plancher x prix ; stop dur à 1R
     du prix du contrôle, vérifié chaque minute ; contrats = floor(risque / (R x point)), trade sauté si 0.
Le module S1_NoiseAreaNQ (lecture, rolls, séance) n'est pas dans ce dépôt : séance = calendrier XNYS, prix =
recolte1.engine.load("NQ") (ratio aux roulements) ramenés au contrat du jour (division par le facteur de la
séance), clôture veille au même contrat. VOL_SEANCES (seulement un filtre de démarrage) pris égal à 14.

vectorbt (Portfolio.from_signals) : une ligne par minute (OHLC, le stop y est vérifié) plus, après chaque minute
de contrôle, une ligne « contrôle » sans OHLC (clôture = clôture de la minute, prix = ouverture suivante) où
s'exécutent les signaux. Ainsi le stop d'une minute passe avant le contrôle, une ré-entrée reste possible au
contrôle qui suit un stop, et le stop d'une nouvelle position est vérifié dès sa première minute, comme dans
l'original. sl_stop = (ouverture - stop) / ouverture, stop_entry_price = Price. Coût par côté et par contrat :
commission / point + ticks x 0,25 point, en frais proportionnels au prix de la ligne.
Contrôle : la boucle de S1_R_stop.py recopiée sur les mêmes grilles, trade par trade. Seul écart voulu : quand
l'ouverture d'entrée est déjà au-delà du stop, l'original sort AU stop (prix meilleur que le marché), vectorbt à
l'ouverture de la minute suivante ; ces cas sont comptés.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd
import vectorbt as vbt

from recolte1.engine import NY, load

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/s1_r_stop")
LOG = None  # ouvert par main() : importer ce module n'écrase pas run.log

SIGMA_SEANCES, VOL_SEANCES, BANDE, CONTROLE_MIN = 30, 14, 1.2, 30
CONTRATS = {"MNQ": dict(point=2.0, commission=0.60), "NQ": dict(point=20.0, commission=2.25)}
TICK = 0.25
START, END = "2016-01-04", "2026-08-28"  # données 2016-01-03 → 2026-08-28 ; pas de holdout
CONFIGS = [  # nom, plancher, stop dur, risque $, contrat, ticks
    ("s1_origine", 0.0, False, 0.0, "MNQ", 1.0),
    ("stop1R_p0.5_1mnq", 0.005, True, 0.0, "MNQ", 1.0),
    ("stop1R_p0.3_1mnq", 0.003, True, 0.0, "MNQ", 1.0),
    ("stop1R_p0.5_risque500", 0.005, True, 500.0, "MNQ", 1.0),
]


def say(s: str = "") -> None:
    print(s, flush=True)
    if LOG is not None:
        LOG.write(s + "\n")
        LOG.flush()


def seance_cash():
    """Grilles séances x 390 minutes (colonne j = barre 9:30+j), prix du contrat de la séance."""
    sched = xc.get_calendar("XNYS").schedule.loc[START:END]
    jours = pd.DatetimeIndex(sched.index)
    fin = pd.Series(
        ((pd.DatetimeIndex(sched["close"]).tz_convert(NY) - pd.DatetimeIndex(sched["open"]).tz_convert(NY))
         .total_seconds() // 60).astype(int).values, index=jours)
    df = load("NQ")
    t = df.index.tz_convert(NY)
    minute = t.hour * 60 + t.minute - 570
    jour = pd.DatetimeIndex(t.date)
    keep = (minute >= 0) & (minute < 390) & jour.isin(jours)
    d = df[keep].copy()
    d["jour"], d["j"] = jour[keep], minute[keep]
    grille = {c: d.pivot(index="jour", columns="j", values=c).reindex(index=jours, columns=range(390))
              for c in ["open", "high", "low", "close", "volume", "factor"]}
    facteur = grille["factor"].bfill(axis=1).iloc[:, 0]  # constant dans la séance (roulements à 00:00 UTC)
    # veille au contrat du jour : clôture ajustée de la veille / facteur du jour
    C_adj = grille["close"].copy()
    for i, f in enumerate(fin.values):
        C_adj.iloc[i, f:] = np.nan
    C_adj = C_adj.ffill(axis=1)
    clot_adj = pd.Series([C_adj.iat[i, f - 1] for i, f in enumerate(fin.values)], index=jours)
    veille = clot_adj.shift(1) / facteur
    O, H, L, C, V = (grille[c].div(facteur, axis=0) if c != "volume" else grille[c]
                     for c in ["open", "high", "low", "close", "volume"])
    mask = np.arange(390)[None, :] >= fin.values[:, None]
    C = C.ffill(axis=1).mask(mask)
    O, H, L = (x.fillna(C.shift(1, axis=1)).fillna(C).mask(mask) for x in (O, H, L))
    V = V.fillna(0.0).mask(mask)
    return jours, fin, O, H, L, C, V, veille


def entrees(jours, fin, O, H, L, C, V, veille):
    """Indicateurs, cible et taille à chaque contrôle (indépendants de la position)."""
    ouv = O.iloc[:, 0]
    cloture = pd.Series([C.iat[i, f - 1] for i, f in enumerate(fin.values)], index=jours)
    ecart = (C.div(ouv, axis=0) - 1).abs()
    sigma = pd.DataFrame({m: ecart[m].dropna().rolling(SIGMA_SEANCES).mean().shift(1).reindex(jours)
                          for m in ecart.columns})
    vwap = (((H + L + C) / 3) * V).cumsum(axis=1) / V.cumsum(axis=1)
    vol = (cloture / veille - 1).rolling(VOL_SEANCES).std().shift(1)
    return dict(jours=jours, fin=fin.values, ouv=ouv.values, veille=veille.values, vol=vol.values,
                On=O.to_numpy(), Hn=H.to_numpy(), Ln=L.to_numpy(), Cn=C.to_numpy(), VWn=vwap.to_numpy(),
                Sg=sigma.to_numpy())


def controles_du_jour(g, i):
    f = int(g["fin"][i])
    ks = list(range(CONTROLE_MIN, f, CONTROLE_MIN))
    ok = (np.isfinite(g["vol"][i]) and np.isfinite(g["veille"][i]) and np.isfinite(g["ouv"][i])
          and all(np.isfinite(g["Sg"][i, k - 1]) for k in ks))
    return f, ks, ok


def signal(g, i, k, plancher, risque, point):
    """(cible, contrats, stop, R) au contrôle k (clôture de la barre k-1)."""
    j = k - 1
    c, vw, s = g["Cn"][i, j], g["VWn"][i, j], g["Sg"][i, j]
    haut, bas = max(g["ouv"][i], g["veille"][i]), min(g["ouv"][i], g["veille"][i])
    upper, lower = haut * (1 + BANDE * s), bas * (1 - BANDE * s)
    cible = 1 if (c > upper and c > vw) else (-1 if (c < lower and c < vw) else 0)
    if cible == 0:
        return 0, 0, np.nan, np.nan
    suiveur = max(upper, vw) if cible > 0 else min(lower, vw)
    R = max(abs(c - suiveur), plancher * c)
    n = math.floor(risque / (R * point)) if risque > 0 else 1
    return cible, n, (c - R if cible > 0 else c + R), R


def heure(k):
    return f"{(570 + k) // 60:02d}:{(570 + k) % 60:02d}"


# --------------------------------------------------------------------------- vectorbt


def run_vbt(g, plancher, stop_dur, risque, contrat, ticks):
    point = CONTRATS[contrat]["point"]
    cote = CONTRATS[contrat]["commission"] / point + ticks * TICK  # coût par côté et par contrat, en points
    cols = {k: [] for k in ["open", "high", "low", "close", "price", "le", "lx", "se", "sx", "size", "sl",
                            "jour", "k", "type", "R", "stop"]}

    def ligne(**kw):
        for c in cols:
            cols[c].append(kw.get(c, np.nan if c not in ("le", "lx", "se", "sx") else False))

    for i, d in enumerate(g["jours"]):
        f, ks, ok = controles_du_jour(g, i)
        if not ok:
            continue
        ks = set(ks)
        for j in range(f):
            fin_j = j == f - 1
            ligne(open=g["On"][i, j], high=g["Hn"][i, j], low=g["Ln"][i, j], close=g["Cn"][i, j],
                  price=g["Cn"][i, j], lx=fin_j, sx=fin_j, size=point, jour=i, k=j + 1,
                  type="fin" if fin_j else "minute")
            k = j + 1
            if k in ks:
                cible, n, stop, R = signal(g, i, k, plancher, risque, point)
                px = g["On"][i, k]
                kw = dict(close=g["Cn"][i, j], price=px, jour=i, k=k, type="controle", size=point, R=R, stop=stop)
                if cible == 0:
                    kw.update(lx=True, sx=True)
                elif n == 0:
                    kw.update(sx=True) if cible > 0 else kw.update(lx=True)
                else:
                    kw.update(size=n * point, le=cible > 0, se=cible < 0)
                    if stop_dur:
                        sl = (px - stop) / px if cible > 0 else (stop - px) / px
                        kw["sl"] = max(sl, 0.0)
                ligne(**kw)
    t = pd.DataFrame(cols)
    pf = vbt.Portfolio.from_signals(
        close=t["close"].values, open=t["open"].values, high=t["high"].values, low=t["low"].values,
        price=t["price"].values, entries=t["le"].values, exits=t["lx"].values,
        short_entries=t["se"].values, short_exits=t["sx"].values, size=t["size"].values, size_type="amount",
        sl_stop=t["sl"].values if stop_dur else np.nan, stop_entry_price="price",
        upon_opposite_entry="reverse", accumulate=False, fees=(cote / t["price"]).values,
        init_cash=1e12, freq="1min")
    tr = pf.trades.records
    rows = []
    for e_idx, x_idx, sz, pnl, sens, pe, px in zip(tr["entry_idx"], tr["exit_idx"], tr["size"], tr["pnl"],
                                                  tr["direction"], tr["entry_price"], tr["exit_price"]):
        e, x = t.iloc[e_idx], t.iloc[x_idx]
        n = int(round(sz / point))
        if x["type"] == "fin":
            raison = "fin de seance"
        elif x["type"] == "minute":
            raison = "stop 1R"
        else:
            raison = "inversion" if (x["le"] if sens == 1 else x["se"]) else "stop suiveur"
        rows.append(dict(jour=g["jours"][int(e["jour"])].date(), sens="achat" if sens == 0 else "vente",
                         entree=heure(int(e["k"])), sortie=heure(int(x["k"])), prix_entree=pe, prix_sortie=px,
                         stop=e["stop"], R_points=e["R"], contrats=n, resultat_R=pnl / (e["R"] * point * n),
                         pnl_dollars=pnl, raison=raison))
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- boucle d'origine (contrôle)


def run_python(g, plancher, stop_dur, risque, contrat, ticks):
    """Boucle de S1_R_stop.backtest, sur les mêmes grilles."""
    point = CONTRATS[contrat]["point"]
    cout_ar = 2 * (CONTRATS[contrat]["commission"] / point + ticks * TICK)
    On, Hn, Ln, Cn = g["On"], g["Hn"], g["Ln"], g["Cn"]
    trades, saute_stop = [], 0
    for i, d in enumerate(g["jours"]):
        f, ks, ok = controles_du_jour(g, i)
        if not ok:
            continue
        ks = set(ks)
        st = dict(pos=0, n=0, entree=0.0, stop=0.0, R=0.0, k_entree=0, h="")

        def fermer(px, k, raison):
            pts = st["pos"] * (px - st["entree"]) - cout_ar
            trades.append(dict(jour=d.date(), sens="achat" if st["pos"] > 0 else "vente", entree=st["h"],
                               sortie=heure(k), prix_entree=st["entree"], prix_sortie=px, stop=st["stop"],
                               R_points=st["R"], contrats=st["n"], resultat_R=pts / st["R"],
                               pnl_dollars=pts * point * st["n"], raison=raison))

        for k in range(1, f + 1):
            j = k - 1
            if stop_dur and st["pos"] != 0 and k >= st["k_entree"]:
                pos, stop = st["pos"], st["stop"]
                if (Ln[i, j] <= stop) if pos > 0 else (Hn[i, j] >= stop):
                    if k == st["k_entree"]:
                        px = stop
                        saute_stop += (On[i, j] < stop) if pos > 0 else (On[i, j] > stop)
                    else:
                        px = min(On[i, j], stop) if pos > 0 else max(On[i, j], stop)
                    fermer(px, k, "stop 1R")
                    st["pos"] = 0
            if k in ks:
                cible, n, stop, R = signal(g, i, k, plancher, risque, point)
                if cible != st["pos"]:
                    px = On[i, k]
                    if st["pos"] != 0:
                        fermer(px, k, "inversion" if cible == -st["pos"] else "stop suiveur")
                        st["pos"] = 0
                    if cible != 0 and n > 0:
                        st.update(pos=cible, n=n, entree=px, stop=stop, R=R, k_entree=k + 1, h=heure(k))
        if st["pos"] != 0:
            fermer(Cn[i, f - 1], f, "fin de seance")
    return pd.DataFrame(trades), saute_stop


# --------------------------------------------------------------------------- résumé (comme S1_R_stop.resume)


def resume(jours, t: pd.DataFrame) -> str:
    r = t["resultat_R"]
    jr = r.groupby(pd.DatetimeIndex(t["jour"])).sum().reindex(jours).fillna(0.0)
    jd = t.groupby(pd.DatetimeIndex(t["jour"]))["pnl_dollars"].sum().reindex(jours).fillna(0.0)
    sh = lambda x: x.mean() / x.std() * math.sqrt(252)
    ans = len(jours) / 252
    cum = jd.cumsum()
    av, ap = jr[jr.index < "2021-01-01"], jr[jr.index >= "2021-01-01"]
    return "\n".join([
        f"Trades        {len(t)} ({len(t) / ans:.0f} par an) ; sorties : "
        + ", ".join(f"{k} {v}" for k, v in t["raison"].value_counts().items()),
        f"En R          espérance {r.mean():+.3f} R/trade (t {r.mean() / r.std() * math.sqrt(len(r)):+.2f}), "
        f"{r.sum() / ans:+.1f} R/an, gagnants {np.mean(r > 0):.0%} (moyenne {r[r > 0].mean():+.2f} R), "
        f"perdants {r[r <= 0].mean():+.2f} R, pire trade {r.min():+.2f} R",
        f"Sharpe en R   {sh(jr):.2f} (avant 2021 {sh(av):.2f} | 2021-2026 {sh(ap):.2f}) ; pire baisse "
        f"{(jr.cumsum().cummax() - jr.cumsum()).max():.1f} R ; pire jour {jr.min():+.1f} R",
        f"En dollars    {cum.iloc[-1]:+,.0f} $ ({cum.iloc[-1] / ans:+,.0f} $/an) ; pire baisse "
        f"{(cum.cummax() - cum).max():,.0f} $ ; pire jour {jd.min():+,.0f} $ ; contrats médian "
        f"{t['contrats'].median():.0f}",
        "R par année   " + " ".join(f"{y}:{v:+.0f}" for y, v in r.groupby(pd.DatetimeIndex(t["jour"]).year).sum().items()),
    ])


def main():
    global LOG
    OUT.mkdir(parents=True, exist_ok=True)
    LOG = open(OUT / "run.log", "w", encoding="utf-8")
    say("S1 Noise Area NQ + stop dur 1R, vectorbt — EXPLORATOIRE, hors compteur, données ≤ 2026-08-28")
    g = entrees(*seance_cash())
    jours = g["jours"]
    say(f"Séances XNYS {jours[0].date()} → {jours[-1].date()} ({len(jours)}), demi-séances {int((g['fin'] < 390).sum())}")
    for nom, plancher, stop_dur, risque, contrat, ticks in CONFIGS:
        say(f"\n== {nom} : {'stop dur 1R' if stop_dur else 'aucun stop dur'} | plancher {plancher:.1%} | {contrat}, "
            f"{CONTRATS[contrat]['commission']:.2f} $ + {ticks:g} tick par côté | "
            f"risque {risque:,.0f} $ par trade{' (0 = 1 contrat)' if not risque else ''}")
        tv = run_vbt(g, plancher, stop_dur, risque, contrat, ticks)
        tp, saute = run_python(g, plancher, stop_dur, risque, contrat, ticks)
        say(resume(jours, tv))
        tv.to_csv(OUT / f"trades_{nom}.csv", index=False)
        cle = ["jour", "entree", "sens"]
        m = tv.merge(tp, on=cle, how="outer", suffixes=("_vbt", "_py"), indicator=True)
        m["ecart_dollars"] = m["pnl_dollars_vbt"] - m["pnl_dollars_py"]
        m.to_csv(OUT / f"controle_{nom}.csv", index=False)
        both = m[m["_merge"] == "both"]
        diff = both[(both["ecart_dollars"].abs() > 0.01) | (both["sortie_vbt"] != both["sortie_py"])]
        say(f"Contrôle      vectorbt {len(tv)} trades, boucle d'origine {len(tp)} ; communs {len(both)}, "
            f"seulement vbt {int((m['_merge'] == 'left_only').sum())}, seulement boucle "
            f"{int((m['_merge'] == 'right_only').sum())} ; écarts > 0,01 $ ou sortie différente : {len(diff)} "
            f"(dont ouverture d'entrée déjà au-delà du stop : {saute}) ; P&L total vbt {tv['pnl_dollars'].sum():+,.2f} $"
            f" / boucle {tp['pnl_dollars'].sum():+,.2f} $")


if __name__ == "__main__":
    main()
