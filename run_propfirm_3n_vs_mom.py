"""FTMO 1-Step avec la stratégie transmise 3n (long 20:05 -> 03:00 ET si somme des 3 nuits <= 0, stop 2 x ATR M15),
comparée à notre règle NQ de nuit (mom, avenant C du n° 18). Exploratoire, hors compteur : aucun signal nouveau,
on rejoue des trades existants dans le moteur du n° 18 (propfirm.ftmo), mêmes réglages que l'avenant C.

uv run python run_propfirm_3n_vs_mom.py [N]  → results/propfirm_3n_vs_mom/ (run.log, eval.csv, funded.csv, ev.csv)

Trades :
  mom : results/couts_reels_nq_nuit/trades.csv (comme run_propfirm_nq_nuit.py), R brut, stop en fraction du prix ;
  3n  : results/nq_nuit_3n/trades_3n_03h_SL_*.csv (run_nq_nuit_3n_vbt.py, version corrigée) et
        results/nq_nuit_3n_8h/trades_3n_08h_SL_*.csv ; R brut = (sortie - entrée) / distance du stop,
        stop = distance / prix d'entrée. Les nuits à plat ne sont pas des jours de trading : un trade = un jour FTMO.
Coût CFD en points au niveau actuel du NQ (1,5 pt principal, 3 pt en contrôle), comme l'avenant C.
« Sans edge » = R - moyenne (même distribution, espérance nulle). Pour comparer à durée égale, le nombre de trades
est converti en mois avec la fréquence de chaque règle (mom ≈ 250 nuits/an, 3n ≈ 109) ; « EV par mois d'emplacement » =
EV par tentative / (durée moyenne d'une éval + P(passage) x vie moyenne du financé).
Limites du moteur : un compte financé s'arrête à 500 trades (max_days) ; chaque compte enchaîne les trades de la
bibliothèque en boucle, donc la bibliothèque OOS (182 trades) est rejouée plusieurs fois.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from propfirm.ftmo import PRICES_EUR, Market, TradeLib, ev, refusal_breakeven, run_eval, run_funded

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
OUT = Path("results/propfirm_3n_vs_mom")
SEED = 1818
P_REF = 25_684.0
COSTS = {"1,5 pt": 1.5 / P_REF, "3 pt": 3.0 / P_REF}
EVAL_R = (0.5, 1.0, 1.5, 2.0, 2.5)
FUNDED_R = (0.25, 0.5, 1.0, 1.5, 2.0)
MAIN_EV, MAIN_FD = 2.0, 1.0
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def lib_3n(pattern: str, y0: int = 2016, y1: int = 2026) -> tuple[TradeLib, float]:
    t = pd.concat([pd.read_csv(f) for f in sorted(Path().glob(pattern))])
    t = t.drop_duplicates("entry_time").sort_values("entry_time")  # les fichiers 08h recouvrent des sous-périodes
    d = pd.to_datetime(t.entry_time.str[:10])
    t, d = t[d.dt.year.between(y0, y1).values], d[d.dt.year.between(y0, y1)]
    an = (min(pd.Timestamp(f"{y1}-12-31"), pd.Timestamp("2026-08-28")) - pd.Timestamp(f"{y0}-01-01")).days / 365.25
    return TradeLib(d.values, (t.dist / t.entry_px).to_numpy(), ((t.exit_px - t.entry_px) / t.dist).to_numpy()), len(t) / an


def lib_mom(y0: int) -> tuple[TradeLib, float]:
    t = pd.read_csv("results/couts_reels_nq_nuit/trades.csv", parse_dates=["night"]).sort_values("entry_idx")
    t["risk"] = t.risk.fillna(t.risk.median())
    t = t[t.night.dt.year >= y0]
    an = (t.night.max() - t.night.min()).days / 365.25
    return TradeLib(t.night.values, t.risk.to_numpy(), t.R_brut.to_numpy()), len(t) / an


def sans_edge(lib: TradeLib) -> TradeLib:
    return TradeLib(lib.dates, lib.s, lib.R - lib.R.mean())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    m11, f_m = lib_mom(2011)
    m16, f_m16 = lib_mom(2016)
    n3, f_3 = lib_3n("results/nq_nuit_3n/trades_3n_03h_SL_*.csv")
    n3o, f_3o = lib_3n("results/nq_nuit_3n/trades_3n_03h_SL_*.csv", 2025, 2026)
    n8, f_8 = lib_3n("results/nq_nuit_3n_8h/trades_3n_08h_SL_*.csv")
    libs = {  # nom : (bibliothèque, trades par an, coûts testés)
        "mom 2011-2026 (avenant C)": (m11, f_m, ["1,5 pt"]),
        "mom 2016-2026": (m16, f_m16, ["1,5 pt", "3 pt"]),
        "mom 2016-2026 sans edge": (sans_edge(m16), f_m16, ["1,5 pt"]),
        "3n 03h SL 2016-2026": (n3, f_3, ["1,5 pt", "3 pt"]),
        "3n 03h SL 2016-2026 sans edge": (sans_edge(n3), f_3, ["1,5 pt"]),
        "3n 03h SL 2025-2026 (OOS)": (n3o, f_3o, ["1,5 pt"]),
        "3n 08h SL 2016-2026": (n8, f_8, ["1,5 pt"]),
    }
    say(f"FTMO 1-Step, 3n contre mom ; {N} comptes par réglage, graine {SEED}")
    for k, (lib, f, _) in libs.items():
        say(f"  {k} : {lib.n} trades ({f:.0f}/an), R brut moyen {lib.R.mean():+.3f}, stop médian {np.median(lib.s):.3%}, "
            f"coût 1,5 pt {np.median(COSTS['1,5 pt'] / lib.s):.3f} R, P(R <= -1) {np.mean(lib.R <= -1):.1%}")

    rng = np.random.default_rng(SEED)
    E, F = [], []
    for k, (lib, f, costs) in libs.items():
        for c in costs:
            m = Market(lib, np.nan, COSTS[c])
            say(f"\n=== {k}, coût {c} ===")
            for r in EVAL_R:
                ok, d = run_eval(m, r, 0.0, N, rng)
                p = ok.mean()
                E.append(dict(lib=k, cost=c, r=r, p_pass=p, se_p=np.sqrt(p * (1 - p) / N), days_pass=d[ok].mean(),
                              days_all=d.mean(), mois_pass=d[ok].mean() / f * 12, mois_all=d.mean() / f * 12))
                say(f"  éval {r:>4} % : passage {p:.1%}, {E[-1]['days_pass']:.1f} trades si validé "
                    f"(≈ {E[-1]['mois_pass']:.1f} mois), {d.mean():.1f} par tentative")
            for reset in (True, False):
                for r in FUNDED_R:
                    paid, nr, d, first = run_funded(m, r, 0.0, N, rng, reset=reset)
                    F.append(dict(lib=k, cost=c, r=r, reset=reset, v_pct=paid.mean(), se_v=paid.std() / np.sqrt(N),
                                  p_reward=(nr > 0).mean(), n_rewards=nr.mean(), life=d.mean(), life_mois=d.mean() / f * 12,
                                  first_med=np.median(first[first > 0]) if (first > 0).any() else np.nan,
                                  v_par_mois=paid.mean() / (d.mean() / f * 12)))
                    x = F[-1]
                    say(f"  financé {r:>4} % {'RAZ' if reset else 'sans RAZ'} : valeur {x['v_pct']:.2f} %, P(reward) "
                        f"{x['p_reward']:.0%}, {x['n_rewards']:.2f} rewards, vie {x['life']:.0f} trades "
                        f"(≈ {x['life_mois']:.0f} mois), {x['v_par_mois']:.2f} %/mois de vie")
    E, F = pd.DataFrame(E), pd.DataFrame(F)
    E.to_csv(OUT / "eval.csv", index=False)
    F.to_csv(OUT / "funded.csv", index=False)

    rows = []
    for (k, c), e in E.groupby(["lib", "cost"], sort=False):
        for reset in (True, False):
            f = F[(F.lib == k) & (F.cost == c) & (F.reset == reset)]
            picks = {"éval 2 % / financé 1 %": (e[e.r == MAIN_EV].iloc[0], f[f.r == MAIN_FD].iloc[0]),
                     "meilleur de la grille": (e.loc[e.p_pass.idxmax()], f.loc[f.v_pct.idxmax()])}
            for which, (ee, ff) in picks.items():
                for size in (10_000, 100_000):
                    x, ci = ev(ee.p_pass, ee.se_p, ff.v_pct, ff.se_v, size)
                    rows.append(dict(lib=k, cost=c, reset=reset, choix=which, eval_r=ee.r, funded_r=ff.r,
                                     p_pass=ee.p_pass, mois_eval=ee.mois_pass, v_pct=ff.v_pct, p_reward=ff.p_reward,
                                     vie_mois=ff.life_mois, size=size, ev_usd=x, ci95=ci,
                                     # un emplacement = éval puis, si validée, compte financé jusqu'à sa perte
                                     ev_par_mois=x / (ee.mois_all + ee.p_pass * ff.life_mois),
                                     refus_max=refusal_breakeven(ee.p_pass, ff.v_pct, size)))
    V = pd.DataFrame(rows)
    V.to_csv(OUT / "ev.csv", index=False)
    say("\n=== Espérance par tentative ===")
    for _, x in V.iterrows():
        say(f"  {x.lib:<30} {x.cost:<6} {'RAZ' if x.reset else 'sans RAZ':<8} {x.choix:<22} éval {x.eval_r:<4} "
            f"fin. {x.funded_r:<4} {x['size'] // 1000:>3}k : EV {x.ev_usd:+8_.0f} $ ± {x.ci95:_.0f} (passage "
            f"{x.p_pass:.1%} en {x.mois_eval:.1f} mois, financé {x.v_pct:.2f} %, vie {x.vie_mois:.0f} mois ; "
            f"{x.ev_par_mois:+_.0f} $ par mois d'emplacement)".replace("_", " "))
    (OUT / "run.log").write_text("\n".join(LOG), encoding="utf-8")


if __name__ == "__main__":
    main()
