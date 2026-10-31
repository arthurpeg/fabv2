"""Exploratoire : le plan FTMO refait chez Smart Trader Funds, challenge « 1 Phase » (une étape). Règle NQ de nuit.

uv run python run_propfirm_stf.py  → results/propfirm_stf/ (run.log, exits.csv, grid.csv, reserve.csv, paths_p95.csv,
    paths_pire_chemin.csv)

Règles STF : propfirm/stf.py (lues sur smartraderfunds.com le 2026-10-31). Rendements de chaque nuit :
results/propfirm_farm_heures/returns.csv (vectorbt, spread 1,5 point, inconnu chez STF). Mêmes réglages que le plan
FTMO : éval risque 2 % TP 5 ATR, financé 1 % TP 4 ATR (stop 2 ATR M15, entrée 20:00 ET, sortie 9:30 ET au plus tard).

0. vectorbt rejoue les nuits pour avoir l'heure de sortie : une sortie par stop ou objectif entre 8:25 et 8:35 ET
   (éval) ou 8:20 et 8:40 (financé) un jour d'annonce 8:30 (config/calendrier_macro_us.csv) viole la règle des
   annonces → compte perdu. Les nuits dont l'entrée tombe un jour férié NYSE de semaine ne sont pas tradées.
1. Contrat : passage, durée, valeur du financé, EV par éval 10k / 100k (une tentative par nuit de départ, départs
   jusqu'à 2 ans avant la fin), réglage FTMO puis grille de risques (choisie sur les mêmes données : optimiste).
2. Réserve pour un seul compte 10k racheté à chaque échec (comme run_propfirm_start1, section 1).
3. Chemins sur 3 ans depuis un seul compte 10k, seuils au pire chemin puis au 95e centile (run_propfirm_start1,
   sections 3 et 4) : A2 1 × 10k → 1 × 100k → 2 × 100k → trio 100k ; B2 1 × 10k → trio 10k → trio 100k ;
   C2 1 × 10k → trio 100k. Plafond STF : 800 k$ de capital cumulé, jamais atteint ici (trio 100k = 300 k$).
"""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd

import run_propfirm_vbt as V
from propfirm import stf as S

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/propfirm_stf")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")
HOURS = ("19:00", "20:00", "21:00")
H, STEP, HORIZON_EV = 756, 5, 504
F10, F100 = S.PRICES_USD[10_000], S.PRICES_USD[100_000]
R_E, TP_E, R_F, TP_F = 2.0, 5, 1.0, 4
SFX = "_n"  # sections 2 et 3 : variante à plat avant les annonces ("" = règle d'origine)

R = pd.read_csv("results/propfirm_farm_heures/returns.csv", index_col=0, parse_dates=True)
NT = len(R)
DATES = pd.DatetimeIndex(R.index)


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def exits() -> pd.DataFrame:
    """Heure de sortie (ET) de chaque nuit, par heure d'entrée et objectif, et date d'entrée (ET)."""
    f = OUT / "exits.csv"
    if f.exists():
        return pd.read_csv(f, index_col=0, parse_dates=True)
    from recolte1.engine import load

    df = load("NQ").copy()
    df.attrs = {}
    idx = df.index.tz_convert(V.NY) if df.index.tz is not None else df.index.tz_localize("UTC").tz_convert(V.NY)
    cols = {}
    for h in HOURS:
        e, _ = V.nights(h, df)
        cols[f"entry_{h}"] = pd.Series(idx[e.p_in.to_numpy()].tz_localize(None).normalize(), index=e.night.values)
        # variante « à plat » : les jours d'annonce 8:30, sortie à la clôture de la barre 8:18 ET (≈ 8:19)
        e2 = e.copy()
        on = e2.night.dt.normalize().isin(NEWS).to_numpy()
        t19 = pd.to_datetime(e2.night.dt.strftime("%Y-%m-%d") + " 08:19").dt.tz_localize(V.NY).dt.tz_convert("UTC")
        p19 = V.A.bar_pos(df.index.as_unit("ns"), t19)
        e2.loc[on & (p19 > e2.p_in.to_numpy()), "p_out"] = p19[on & (p19 > e2.p_in.to_numpy())]
        for tp in (5.0, 4.0):
            for sfx, ee in (("", e), ("_n", e2)):
                _, rec = V.run_vbt(df, ee, np.arange(len(ee)), tp, 1e4)
                ok = rec["exit_idx"].notna().to_numpy()
                t = np.full(len(ee), np.datetime64("NaT", "ns"))
                t[ok] = idx[rec["exit_idx"].to_numpy()[ok].astype(int)].tz_localize(None).to_numpy()
                cols[f"exit_{h}_tp{tp:g}{sfx}"] = pd.Series(t, index=ee.night.values)
                cols[f"{'chk' if not sfx else 'ret'}_{h}_tp{tp:g}{sfx}"] = pd.Series((rec["pnl"] / 1e4).to_numpy(), index=ee.night.values)
    X = pd.DataFrame(cols).reindex(DATES)
    X.to_csv(f)
    return X


_CAL = pd.read_csv("config/calendrier_macro_us.csv", parse_dates=["date"])
NEWS = set(_CAL.loc[_CAL.heure_ET == "08:30", "date"].dt.normalize())


def flags(X: pd.DataFrame):
    sessions = set(xc.get_calendar("XNYS").sessions_in_range("2011-01-01", "2026-12-31").tz_localize(None).normalize())
    viol, hol = {}, {}
    for h in HOURS:
        ent = pd.to_datetime(X[f"entry_{h}"])
        hol[h] = (ent.dt.dayofweek < 5) & ~ent.isin(sessions) & ent.notna()
        for tp in (5, 4):
            for sfx in ("", "_n"):
                t = pd.to_datetime(X[f"exit_{h}_tp{tp}{sfx}"])
                on_news = t.dt.normalize().isin(NEWS)
                mins = t.dt.hour * 60 + t.dt.minute - (8 * 60 + 30)
                for w in (5, 10):
                    viol[(h, tp, w, sfx)] = (on_news & (mins.abs() <= w)).to_numpy()
    return viol, {h: v.to_numpy() for h, v in hol.items()}


X = exits()
VIOL, HOL = flags(X)


def pnl_fn(hour: str, tp_e: int, tp_f: int, sfx: str):
    src = X if sfx else R
    re_, rf_ = src[f"ret_{hour}_tp{tp_e}{sfx}"].to_numpy(), src[f"ret_{hour}_tp{tp_f}{sfx}"].to_numpy()
    s = R[f"stop_{hour}"].to_numpy()
    hol = HOL[hour]

    def pnl(i, ph, risk):
        x = (re_ if ph == "éval" else rf_)[i]
        return np.nan if hol[i] else risk * x / (s[i] + V.COST)

    return pnl


@lru_cache(maxsize=None)
def events(hour: str, start: int, end: int, size: int, r_e: float = R_E, tp_e: int = TP_E, r_f: float = R_F,
           tp_f: int = TP_F, news: bool = True, once: bool = False, sfx: str = None):
    sfx = SFX if sfx is None else sfx
    ve = VIOL[(hour, tp_e, 5, sfx)] if news else np.zeros(NT, bool)
    vf = VIOL[(hour, tp_f, 10, sfx)] if news else np.zeros(NT, bool)
    return tuple(S.replay(pnl_fn(hour, tp_e, tp_f, sfx), DATES, end, start, size, r_e, r_f, ve, vf, once))


def contract(hour="20:00", r_e=R_E, tp_e=TP_E, r_f=R_F, tp_f=TP_F, news=True, sfx="") -> dict:
    """Une tentative par nuit de départ (jusqu'à HORIZON_EV nuits avant la fin), 10k et 100k."""
    out = {}
    for size, fee in ((10_000, F10), (100_000, F100)):
        rows = []
        for s0 in range(0, NT - HORIZON_EV):
            ev = events(hour, s0, NT, size, r_e, tp_e, r_f, tp_f, news, True, sfx)
            res = ev[1]
            paid = sum(x[2] for x in ev if x[0] == "reward") / 100 * size
            refund = fee if any(x[0] == "reward" and x[3] for x in ev) else 0.0
            nrew = sum(1 for x in ev if x[0] == "reward")
            end = [x for x in ev if x[0] == "financé perdu"]
            rows.append(dict(ok=res[0] == "validée", nuits=res[1] - s0 + 1, why=res[2] if res[0] == "ratée" else "",
                             paid=paid, refund=refund, nrew=nrew,
                             fund_why=end[0][2] if end else "", fund_nights=end[0][1] - res[1] if end else 0))
        D = pd.DataFrame(rows)
        F = D[D.ok]
        out[size] = dict(p=D.ok.mean(), nuits_ok=F.nuits.median(), nuits_ko=D[~D.ok].nuits.median(),
                         causes=D[~D.ok].why.value_counts(normalize=True).to_dict(),
                         v=(F.paid + F.refund).mean(), nrew=F.nrew.mean(), p_rew=(F.nrew > 0).mean(),
                         vie=F.fund_nights.median(), fin=F.fund_why.value_counts(normalize=True).to_dict(),
                         ev=(D.paid + D.refund).mean() - fee, se=(D.paid + D.refund).std() / np.sqrt(len(D)) * np.sqrt(20))
    return out  # se : erreur-type grossière (départs chevauchants, ~20 nuits par tentative)


def show(c: dict, lab: str) -> None:
    a, b = c[10_000], c[100_000]
    say(f"  {lab} : passage {a['p']:.1%} ({a['nuits_ok']:.0f} nuits médiane si validée, {a['nuits_ko']:.0f} si ratée) ; "
        f"financé : P(≥ 1 retrait) {a['p_rew']:.0%}, {a['nrew']:.1f} retraits, vie médiane {a['vie']:.0f} nuits, "
        f"valeur {a['v']:,.0f} $ (10k) / {b['v']:,.0f} $ (100k) remboursement compris ; "
        f"EV par éval {a['ev']:+,.0f} $ (10k, ±{1.96 * a['se']:,.0f}) / {b['ev']:+,.0f} $ (100k, ±{1.96 * b['se']:,.0f})".replace(",", " "))


def cash_series(config, s0: int) -> np.ndarray:
    cash = np.zeros(H)
    for h, size in config:
        fee = S.PRICES_USD[size]
        for x in events(h, s0, s0 + H, size):
            if x[0] == "achat":
                cash[x[1] - s0] -= fee
            elif x[0] == "reward":
                cash[x[1] - s0] += x[2] / 100 * size + (fee if x[3] else 0.0)
    return cash


THR: dict[str, float] = {}


def path(policy: str, s0: int, cash0: float) -> dict:
    """Comme run_propfirm_start1.path (A2 / B2 / C2) avec les règles STF. La taille d'un compte est choisie à
    chaque achat ; ses événements sont ceux de cette taille (seul le retrait minimum de 100 $ en dépend)."""
    end = s0 + H
    plan = {"A2": [("19:00", THR["2x100k"]), ("21:00", THR["3x100k"])],
            "B2": [("19:00", THR["3x10k"]), ("21:00", THR["3x10k"])],
            "C2": [("19:00", THR["3x100k"]), ("21:00", THR["3x100k"])]}[policy]
    to100 = {"A2": THR["1x100k"], "B2": THR["3x100k"], "C2": THR["3x100k"]}[policy]
    big = policy != "B2"  # comptes ajoutés directement en 100k
    cash, low, fees = cash0, cash0, 0.0
    ptr, evs, cur = {}, {}, {}
    switched, t_switch, t_trio = False, None, None
    marks = {252: None, 504: None}
    # Les deux tailles donnent quasiment les mêmes événements ; on suit ceux de 10k jusqu'au premier achat en
    # 100k, puis ceux de 100k à partir de la nuit de cet achat.
    def add(h, j, size):
        evs[h] = events(h, j, end, size); ptr[h] = 0

    add("20:00", s0, 10_000)
    for j in range(s0, end):
        for m in marks:
            if marks[m] is None and j - s0 >= m:
                marks[m] = cash - cash0
        todo = []
        for h in list(evs):
            while ptr[h] < len(evs[h]) and evs[h][ptr[h]][1] == j:
                todo.append((0 if evs[h][ptr[h]][0] == "reward" else 1, h, evs[h][ptr[h]]))
                ptr[h] += 1
        for _, h, x in sorted(todo, key=lambda z: z[0]):
            if x[0] == "reward":
                cash += x[2] / 100 * cur[h] + (S.PRICES_USD[cur[h]] if x[3] else 0.0)
            elif x[0] == "achat":
                if not switched and cash - cash0 >= to100:
                    switched, t_switch = True, j - s0
                size = 100_000 if switched or (h != "20:00" and big) else 10_000
                if size != cur.get(h, 10_000) or (size == 100_000 and h not in cur):
                    # rebrancher le compte sur les événements de sa nouvelle taille, depuis cette nuit
                    evs[h] = events(h, j, end, size)
                    ptr[h] = 1  # l'achat de cette nuit est celui qu'on traite
                cur[h] = size
                cash -= S.PRICES_USD[size]; fees += S.PRICES_USD[size]
                low = min(low, cash)
        gain = cash - cash0
        for h, thr in plan:
            if h not in evs and gain >= thr:
                add(h, j + 1, 100_000 if big else 10_000)
        if t_trio is None and len(cur) == 3 and all(v == 100_000 for v in cur.values()):
            t_trio = j - s0
    return dict(politique=policy, start=DATES[s0].date(), bascule=t_switch, trio_100k=t_trio,
                net_1an=marks[252], net_2ans=marks[504], net_3ans=cash - cash0, apport=max(0.0, -low), frais=fees)


def main() -> None:
    say(f"Smart Trader Funds 1 Phase, règle NQ de nuit ; {NT} nuits {DATES[0].date()} → {DATES[-1].date()} ; "
        f"éval {F10} $ (10k) / {F100} $ (100k), TradeLocker")
    chk = max(np.nanmax(np.abs(X[f"chk_{h}_tp{tp}"] - R[f"ret_{h}_tp{tp}"])) for h in HOURS for tp in (5, 4))
    say(f"\n0. Contrôle vectorbt : écart max avec returns.csv {chk:.2e} (rendement par $ de notionnel)")
    for h in HOURS:
        n = R[f"ret_{h}_tp5"].notna()
        say(f"  {h} : {n.sum()} nuits tradées ; nuits d'entrée un jour férié (non tradées) {int(HOL[h][n].sum())} ; "
            f"sortie dans la fenêtre d'une annonce 8:30 : éval ±5 min {int(VIOL[(h, 5, 5, '')][n].sum())} "
            f"({VIOL[(h, 5, 5, '')][n].mean():.2%}), financé ±10 min {int(VIOL[(h, 4, 10, '')][n].sum())} "
            f"({VIOL[(h, 4, 10, '')][n].mean():.2%}) ; à plat à 8:19 : {int(VIOL[(h, 5, 5, '_n')][n].sum())} / "
            f"{int(VIOL[(h, 4, 10, '_n')][n].sum())}")
        cut = (X[f"exit_{h}_tp5_n"] != X[f"exit_{h}_tp5"]) & n
        say(f"    nuits raccourcies (annonce 8:30) : {int(cut.sum())}, R moyen {(R[f'ret_{h}_tp5'] / R[f'stop_{h}'] * 2)[cut].mean():+.3f} "
            f"→ {(X[f'ret_{h}_tp5_n'] / R[f'stop_{h}'] * 2)[cut].mean():+.3f} ATR (TP 5)")
    lev = (R_E / 100 / (R["stop_20:00"] + V.COST))
    say(f"  levier à 2 % de risque (notionnel / capital) : médiane {lev.median():.1f}, max {lev.max():.1f} (plafond STF 50)")

    say("\n1. Contrat STF 1 Phase, une tentative par nuit de départ (2011-07 → 2024-08), signal 20:00")
    for lab, kw in ((f"réglage FTMO (éval {R_E:g} % TP {TP_E}, financé {R_F:g} % TP {TP_F}), règle d'origine", {}),
                    ("même réglage, règle des annonces ignorée", dict(news=False)),
                    ("même réglage, à plat à 8:19 les jours d'annonce 8:30", dict(sfx="_n"))):
        c = contract(**kw)
        show(c, lab)
        a = c[10_000]
        say("    causes d'échec de l'éval : " + ", ".join(f"{k} {v:.0%}" for k, v in a["causes"].items())
            + " ; fin du financé : " + ", ".join(f"{k} {v:.0%}" for k, v in a["fin"].items()))
    for h in ("19:00", "21:00"):
        show(contract(h, sfx=SFX), f"signal {h}, à plat")
    rows = []
    for r_e in (1.0, 1.5, 2.0):
        for tp_e in (4, 5):
            for r_f in (0.5, 0.75, 1.0):
                for tp_f in (4, 5):
                    cc = contract("20:00", r_e, tp_e, r_f, tp_f, sfx=SFX)
                    rows.append(dict(r_eval=r_e, tp_eval=tp_e, r_fund=r_f, tp_fund=tp_f, p=cc[10_000]["p"],
                                     nuits=cc[10_000]["nuits_ok"], v10=cc[10_000]["v"], ev10=cc[10_000]["ev"],
                                     ev100=cc[100_000]["ev"]))
    G = pd.DataFrame(rows).sort_values("ev100", ascending=False)
    G.to_csv(OUT / "grid.csv", index=False)
    say("\n  Grille, à plat (36 réglages, choisis sur les mêmes données : le meilleur est optimiste) — 5 meilleurs en EV 100k :")
    for _, g in G.head(5).iterrows():
        say(f"    éval {g.r_eval:g} % TP {g.tp_eval:g}, financé {g.r_fund:g} % TP {g.tp_fund:g} : passage {g.p:.1%}, "
            f"{g.nuits:.0f} nuits, EV {g.ev10:+,.0f} $ (10k) / {g.ev100:+,.0f} $ (100k)".replace(",", " "))
    say(f"    réglages à EV 100k > 0 : {(G.ev100 > 0).sum()} sur {len(G)} ; pire {G.ev100.min():+,.0f} $".replace(",", " "))

    starts = np.arange(0, NT - H, STEP)
    say(f"\nSections 2 et 3 : {'à plat à 8:19 les jours d’annonce 8:30' if SFX else 'règle d’origine'}, réglage FTMO")
    say(f"\n2. Un seul compte 10k racheté à chaque échec, {len(starts)} départs {DATES[starts[0]].date()} → "
        f"{DATES[starts[-1]].date()}, 3 ans")
    rs = []
    for h in HOURS:
        for s0 in starts:
            cash, low, first, run, worst = 0.0, 0.0, None, 0, 0
            for x in events(h, s0, s0 + H, 10_000):
                if x[0] == "achat":
                    cash -= F10; low = min(low, cash)
                elif x[0] == "reward":
                    cash += x[2] / 100 * 10_000 + (F10 if x[3] else 0.0)
                    first = x[1] - s0 if first is None else first
                elif x[0] == "ratée":
                    run += 1; worst = max(worst, run)
                elif x[0] == "validée":
                    run = 0
            rs.append(dict(heure=h, start=DATES[s0].date(), mise=-low, premier_reward=first, ratées=worst, net_3ans=cash))
    Rs = pd.DataFrame(rs)
    Rs.to_csv(OUT / "reserve.csv", index=False)
    for h, g in Rs.groupby("heure"):
        say(f"  {h} : mise médiane {g.mise.median():.0f} $, 95e centile {g.mise.quantile(0.95):.0f} $, pire {g.mise.max():.0f} $ "
            f"({g.mise.max() / F10:.0f} évals) ; 1er retrait médiane {g.premier_reward.median():.0f} nuits, pire "
            f"{g.premier_reward.max():.0f} (sans retrait en 3 ans : {g.premier_reward.isna().mean():.0%}) ; "
            f"pire série d'évals ratées {g.ratées.max()} ; net à 3 ans médiane {g.net_3ans.median():+,.0f} $, "
            f"5e centile {g.net_3ans.quantile(0.05):+,.0f} $".replace(",", " "))

    configs = {"1x10k": [("20:00", 10_000)], "1x100k": [("20:00", 100_000)],
               "2x100k": [("20:00", 100_000), ("19:00", 100_000)],
               "3x100k": [(h, 100_000) for h in HOURS], "3x10k": [(h, 10_000) for h in HOURS]}
    M = {k: np.array([max(0.0, -np.cumsum(cash_series(cfg, s0)).min()) for s0 in starts]) for k, cfg in configs.items()}
    say("\n3. Argent sorti avant remboursement par configuration (3 ans) : médiane / 90e / 95e centile / pire")
    for k, m in M.items():
        say(f"  {k:<7} : {np.median(m):,.0f} / {np.quantile(m, 0.9):,.0f} / {np.quantile(m, 0.95):,.0f} / {m.max():,.0f} $".replace(",", " "))
    for lab, fname, q in (("pire chemin", "paths_pire_chemin.csv", None), ("95e centile", "paths_p95.csv", 0.95)):
        for k, m in M.items():
            THR[k] = float(m.max() if q is None else np.quantile(m, q))
        cash0 = float(np.ceil(THR["1x10k"] / 50) * 50)
        say(f"\n  Seuils au {lab} : " + ", ".join(f"{k} {v:,.0f} $" for k, v in THR.items()).replace(",", " ")
            + f" ; départ avec {cash0:.0f} $")
        P2 = pd.DataFrame([path(p, s0, cash0) for s0 in starts for p in ("A2", "B2", "C2")])
        P2.to_csv(OUT / fname, index=False)
        names = {"A2": "1 × 10k → 1 × 100k → 2 × 100k → trio 100k", "B2": "1 × 10k → trio 10k → trio 100k",
                 "C2": "1 × 10k → trio 100k"}
        for p, g in P2.groupby("politique"):
            say(f"  === {p}. {names[p]} ===")
            say(f"    premier 100k : médiane {g.bascule.median():.0f} nuits, atteint en 3 ans dans {g.bascule.notna().mean():.0%} "
                f"des départs ; trio 100k : médiane {g.trio_100k.median():.0f} nuits, atteint dans {g.trio_100k.notna().mean():.0%}")
            for col, l2 in (("net_1an", "gain net à 1 an"), ("net_2ans", "à 2 ans"), ("net_3ans", "à 3 ans")):
                say(f"    {l2:<16} : médiane {g[col].median():+,.0f} $, 5e centile {g[col].quantile(0.05):+,.0f} $, "
                    f"pire {g[col].min():+,.0f} $".replace(",", " "))
            say(f"    apport en plus des {cash0:.0f} $ : nul dans {(g.apport == 0).mean():.0%} des départs, pire {g.apport.max():,.0f} $".replace(",", " "))


if __name__ == "__main__":
    main()
