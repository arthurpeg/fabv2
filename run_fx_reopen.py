"""Pré-enregistrement n° 6 : fade du gap de reprise FX (Tolušić 2026) sur futures CME.

uv run python run_fx_reopen.py   → results/fx_reopen/ (log, CSV, parquet)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from fxreopen.data import PAIRS, load, midnight_jumps
from fxreopen.evaluate import (abdi_ranaldo, bootstrap_p, daily, dsr, permutation_p, reality_check, sharpe,
                               trade_stats, with_cost)
from fxreopen.rules import intraday_trades, reopen_events, reopen_trades

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/fx_reopen")
OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / "run.log", "w", encoding="utf-8")

THRESHOLDS = (1, 2, 5)
ENTRIES = (0, 1, 5, 15)
COSTS = (0, 2, 3, 5, 8)
MAIN_COST = 3
PRIMARY = "reopen_s5_E1"
N_PREREG, N_GLOBAL = 18, 192
WINDOWS = {
    "2016-2018": ("2016-01-01", "2018-12-31"),
    "2019-2026-01": ("2019-01-01", "2026-01-31"),
    "2026-02+": ("2026-02-01", "2026-12-31"),
    "tout": ("2016-01-01", "2026-12-31"),
}


def say(s: str = "") -> None:
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def window(t: pd.DataFrame, w: str) -> pd.DataFrame:
    a, b = WINDOWS[w]
    return t[(t["date"] >= a) & (t["date"] <= b)]


def fmt(d: dict) -> str:
    if d.get("n", 0) == 0:
        return "n=0"
    return (f"n={d['n']:>5} PF={d['pf']:5.2f} win={d['win_%']:5.1f}% net={d['mean_net']:+6.2f} "
            f"brut={d['mean_gross']:+6.2f} SRpap={d['sharpe_paper']:+6.2f} années<0={d['losing_years']}")


def main() -> None:
    say("# Pré-enregistrement n° 6 — fade de la reprise FX (futures CME)\n")
    data = {f: load(f) for f in PAIRS}

    # ---------------------------------------------------------------- contrôles des données
    say("## Contrôle des roulements (sauts > 0,15 % sur une barre de 00:00 UTC)")
    for f, df in data.items():
        j = midnight_jumps(df)
        q = j[j["in_window"]].groupby([j[j["in_window"]].index.year, (j[j["in_window"]].index.month - 1) // 3]).size()
        say(f"{f}: {int(j['in_window'].sum())} dans les fenêtres ({len(q)} trimestres sur ~43), "
            f"{int((~j['in_window']).sum())} hors fenêtres (max |saut| hors fenêtre = "
            f"{j.loc[~j['in_window'], 'jump'].abs().max() if (~j['in_window']).any() else 0:.4f})")

    # ---------------------------------------------------------------- anatomie
    say("\n## Anatomie du gap (pips) — papier : reprise 4,8 pips, 74 % > 1 pip ; autres heures 0,12, 0,9 %")
    intr = {f: intraday_trades(f, df) for f, df in data.items()}
    for f, df in data.items():
        ev = reopen_events(df)
        g = (ev["p_reopen"] - ev["p_prev"]).abs() / PAIRS[f].pip
        gi = intr[f]["gap"].abs()
        n_bound = len(intr[f])  # frontières avec |gap| > 0 seulement (sens défini)
        say(f"{f} ({PAIRS[f].name}) : reprise n={len(g)} |gap| moyen={g.mean():.2f} médian={g.median():.2f} "
            f">1={100 * (g >= 1).mean():.0f}% >2={100 * (g >= 2).mean():.0f}% >5={100 * (g >= 5).mean():.0f}% | "
            f"intrajournalier (gaps non nuls, n={n_bound}) moyen={gi.mean():.2f} >1={100 * (gi >= 1).mean():.1f}%")

    # ---------------------------------------------------------------- trades de base
    base = {}
    for e in ENTRIES:
        base[f"E{e}"] = pd.concat([reopen_trades(f, df, e) for f, df in data.items()], ignore_index=True)
    base["close"] = pd.concat([reopen_trades(f, df, 0, hold="close") for f, df in data.items()], ignore_index=True)
    base["intra"] = pd.concat(intr.values(), ignore_index=True)
    for k, t in base.items():
        t.to_parquet(OUT / f"trades_{k}.parquet")

    rules: dict[str, tuple[pd.DataFrame, object]] = {}
    for s in THRESHOLDS:
        for e in ENTRIES:
            t = base[f"E{e}"]
            rules[f"reopen_s{s}_E{e}"] = (t[t["gap"].abs() >= s].reset_index(drop=True), MAIN_COST)
    for s in THRESHOLDS:
        t = base["intra"]
        rules[f"intra_s{s}"] = (t[t["gap"].abs() >= s].reset_index(drop=True), "std")
    for s in THRESHOLDS:
        t = base["close"]
        rules[f"close_s{s}_E0"] = (t[t["gap"].abs() >= s].reset_index(drop=True), MAIN_COST)
    assert len(rules) == N_PREREG

    cal = pd.DatetimeIndex(sorted(set().union(*[set(reopen_events(df)["date"]) for df in data.values()])))

    # ---------------------------------------------------------------- famille principale × coûts
    rows = []
    say("\n## Famille principale : fade de la reprise, sortie +60 min")
    for s in THRESHOLDS:
        for e in ENTRIES:
            name = f"reopen_s{s}_E{e}"
            t0 = rules[name][0]
            say(f"\n### {name}")
            for c in COSTS:
                tc = with_cost(t0, c)
                for w in WINDOWS:
                    tw = window(tc, w)
                    st = trade_stats(tw)
                    dr = daily(tw, cal[(cal >= WINDOWS[w][0]) & (cal <= WINDOWS[w][1])])
                    rows.append({"rule": name, "s": s, "entry": e, "cost": c, "window": w, **st,
                                 "sharpe_daily": sharpe(dr)})
                    if c in (0, 3, 5) or w == "2019-2026-01":
                        say(f"coût {c} | {w:<13} {fmt(st)} SRj={sharpe(dr):+5.2f}")
    summary = pd.DataFrame(rows)

    # ---------------------------------------------------------------- point mort
    say("\n## Spread de point mort aller-retour (= gain brut moyen, pips)")
    be = summary[summary["cost"] == 0].pivot_table(index=["s", "entry"], columns="window", values="mean_gross")
    say(be[list(WINDOWS)].round(2).to_string())
    be.to_csv(OUT / "breakeven.csv")
    say("\nPar paire (toute la période) :")
    for s in THRESHOLDS:
        for e in ENTRIES:
            t = rules[f"reopen_s{s}_E{e}"][0]
            say(f"s={s} E{e}: " + "  ".join(f"{p}={g['gross'].mean():+.2f} (n={len(g)})" for p, g in t.groupby("pair")))

    # ---------------------------------------------------------------- 18:00 → 18:01
    say("\n## Exécutabilité : mouvement dans le sens du fade entre l'open de 18:00 et l'entrée décalée (pips)")
    e0 = base["E0"].set_index(["pair", "date"])
    for e in ENTRIES[1:]:
        ed = base[f"E{e}"].set_index(["pair", "date"])
        j = e0.join(ed[["p_in"]], rsuffix="_d", how="inner")
        pip = j.index.get_level_values("pair").map({k: p.pip for k, p in PAIRS.items()}).values
        lost = j["dir"] * (j["p_in_d"] - j["p_in"]) / pip
        for s in THRESHOLDS:
            m = j["gap"].abs() >= s
            say(f"E{e}, s={s}: perdu en moyenne {lost[m].mean():+.2f} pips (n={int(m.sum())}) "
                f"sur un gain brut E0 de {j.loc[m, 'gross'].mean():+.2f}")

    # ---------------------------------------------------------------- contrôles
    say("\n## Contrôle (a) : heures intrajournalières (coût standard 1 tick + 5 $)")
    for s in THRESHOLDS:
        t0 = rules[f"intra_s{s}"][0]
        for w in ("2016-2018", "2019-2026-01", "tout"):
            say(f"s={s} {w:<13} brut: {fmt(trade_stats(window(with_cost(t0, 0), w)))}")
            say(f"s={s} {w:<13} net : {fmt(trade_stats(window(with_cost(t0, 'std'), w)))}")
    say("\n## Contrôle (b) : même entrée E0, détention jusqu'au close du jour (16:59 ET) vs sortie +60 min")
    for s in THRESHOLDS:
        for c in (0, MAIN_COST):
            for w in ("2016-2018", "2019-2026-01", "tout"):
                a = trade_stats(window(with_cost(rules[f"reopen_s{s}_E0"][0], c), w))
                b = trade_stats(window(with_cost(rules[f"close_s{s}_E0"][0], c), w))
                say(f"s={s} coût {c} {w:<13} PF 1h={a['pf']:.2f} (net {a['mean_net']:+.2f}) → PF close={b['pf']:.2f} "
                    f"(net {b['mean_net']:+.2f}, n={b['n']})")

    # ---------------------------------------------------------------- tests
    D = pd.DataFrame({k: daily(with_cost(t, c), cal) for k, (t, c) in rules.items()})
    D.to_parquet(OUT / "daily_net.parquet")
    D_alt = pd.DataFrame({k: daily(with_cost(t, MAIN_COST), cal) for k, (t, c) in rules.items()})

    say("\n## Tests au coût principal (3 pips ; intrajournalier au coût standard)")
    tests = []
    for k, (t, c) in rules.items():
        tc = with_cost(t, c)
        r = D[k]
        d18, sr0 = dsr(D, k, N_PREREG)
        d192, _ = dsr(D, k, N_GLOBAL)
        row = {"rule": k, "cost": c, "n": len(tc), "mean_net": tc["net"].mean(), "sharpe_daily": sharpe(r),
               "p_boot": bootstrap_p(r), "p_perm": permutation_p(tc), "dsr_18": d18, "dsr_192": d192,
               "sr0_18": sr0, "dsr_18_alt": dsr(D_alt, k, N_PREREG)[0]}
        tests.append(row)
        say(f"{k:<16} n={row['n']:>5} net={row['mean_net']:+6.2f} SRj={row['sharpe_daily']:+5.2f} "
            f"p_boot={row['p_boot']:.4f} p_perm={row['p_perm']:.4f} DSR18={d18:.3f} DSR192={d192:.3f} "
            f"(SR0={sr0:.2f}) DSR18 alt={row['dsr_18_alt']:.3f}")
    tests = pd.DataFrame(tests)
    tests.to_csv(OUT / "tests.csv", index=False)

    for c in (5, 8):
        tc = with_cost(rules[PRIMARY][0], c)
        say(f"{PRIMARY} à {c} pips : net={tc['net'].mean():+.2f} SRj={sharpe(daily(tc, cal)):+.2f} "
            f"p_boot={bootstrap_p(daily(tc, cal)):.4f}")

    p_rc, best, stat = reality_check(D)
    say(f"\nReality Check de White (18 règles) : max t={stat:.2f} ({best}), p={p_rc:.4f}")
    p_rc2, best2, stat2 = reality_check(D.loc[(D.index >= "2019-01-01") & (D.index <= "2026-01-31")])
    say(f"Reality Check 2019-2026-01 : max t={stat2:.2f} ({best2}), p={p_rc2:.4f}")

    # ---------------------------------------------------------------- configuration principale
    say(f"\n## Configuration principale {PRIMARY} à {MAIN_COST} pips")
    tp = with_cost(rules[PRIMARY][0], MAIN_COST)
    say("Par paire :")
    for p, g in tp.groupby("pair"):
        say(f"  {p}: {fmt(trade_stats(g))}")
    say("Par année :")
    yr = tp.groupby(tp["date"].dt.year).agg(n=("net", "size"), net=("net", "mean"), gross=("gross", "mean"),
                                             tot=("net", "sum"))
    say(yr.round(2).to_string())
    yr.to_csv(OUT / "primary_yearly.csv")
    w1, w2 = (trade_stats(window(tp, w)) for w in ("2016-2018", "2019-2026-01"))
    row = tests.set_index("rule").loc[PRIMARY]
    crit = {
        "1. net>0 et PF>1 sur 2016-2018 et 2019-2026-01": bool(w1["mean_net"] > 0 and w1["pf"] > 1
                                                                and w2["mean_net"] > 0 and w2["pf"] > 1),
        "2. bootstrap p<0,05": bool(row["p_boot"] < 0.05),
        "3. permutation p<0,05": bool(row["p_perm"] < 0.05),
        "4. DSR(N=18)>0,95": bool(row["dsr_18"] > 0.95),
    }
    for k, v in crit.items():
        say(f"  {k}: {'OUI' if v else 'NON'}")
    say(f"  → {'SURVIT' if all(crit.values()) else 'REJETÉE'}")

    say("\n## Entrées décalées E5 et E15 à 3 pips (lecture secondaire)")
    for s in THRESHOLDS:
        for e in (5, 15):
            name = f"reopen_s{s}_E{e}"
            tc = with_cost(rules[name][0], MAIN_COST)
            a, b = (trade_stats(window(tc, w)) for w in ("2016-2018", "2019-2026-01"))
            ok = a["mean_net"] > 0 and b["mean_net"] > 0 and tests.set_index("rule").loc[name, "p_perm"] < 0.05
            say(f"{name}: net 2016-18={a['mean_net']:+.2f} 2019-26={b['mean_net']:+.2f} "
                f"p_perm={tests.set_index('rule').loc[name, 'p_perm']:.4f} → {'tient' if ok else 'ne tient pas'}")

    # ---------------------------------------------------------------- garde-fou
    flags = summary[(summary["cost"] == MAIN_COST) & (summary["window"] == "tout")
                    & ((summary["pf"] > 4) | (summary["win_%"] > 75) | (summary["sharpe_daily"] > 3))]
    say(f"\nGarde-fou (PF>4, win>75 %, SRj>3 à 3 pips, toute la période) : "
        f"{', '.join(flags['rule']) if len(flags) else 'aucun'}")

    # ---------------------------------------------------------------- spread effectif
    say("\n## Spread effectif Abdi-Ranaldo (pips, moyenne des années)")
    win = {"18:00-18:04": (1080, 1085), "18:05-18:59": (1085, 1140), "02:00-16:00": (120, 960)}
    ar = pd.concat([abdi_ranaldo(df, PAIRS[f].pip, win).assign(pair=f) for f, df in data.items()])
    ar.to_csv(OUT / "abdi_ranaldo.csv", index=False)
    say(ar.pivot_table(index="pair", columns="window", values="spread_pips")[list(win)].round(2).to_string())
    say("\nVolume médian par minute (contrats) :")
    for f, df in data.items():
        et = df.index.tz_convert("America/New_York")
        hm = et.strftime("%H:%M")
        say(f"  {f}: " + "  ".join(f"{h}={df['volume'][hm == h].median():.0f}"
                                     for h in ("18:00", "18:01", "18:05", "18:15", "19:00", "03:00", "09:00")))

    summary.to_csv(OUT / "summary.csv", index=False)
    say("\nfin.")


if __name__ == "__main__":
    main()
