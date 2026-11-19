"""Gap d'ouverture du DAX prédit par les courbes étrangères (PREREGISTRATION_5.md).

    uv run python run_opening_gap.py              # tout, selon config/opening_gap.toml
    uv run python run_opening_gap.py --config autre.toml

Sorties dans results/opening_gap/ : prévisions, tables de prévision et de
trading, découpages, DSR, permutations, courbes de capital.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from gap import ROOT, load_config
from gap.backtest import (arithmetic, dsr, forecast_metrics, permutation_test, sharpe, simulate,
                          trading_metrics)
from gap.data import build_sample
from gap.signals import npfda_positions, ols_positions
from gap.walkforward import walk_forward

OUT = ROOT / "results" / "opening_gap"
IS_END = pd.Timestamp("2022-12-31")


def periods(index: pd.DatetimeIndex) -> dict[str, np.ndarray]:
    return {"all": np.ones(len(index), bool), "≤2022": index <= IS_END, "≥2023": index > IS_END}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows cp1252
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "config" / "opening_gap.toml"))
    cfg = load_config(ap.parse_args().config)
    OUT.mkdir(parents=True, exist_ok=True)
    ks, sig, ev = cfg["timing"]["exit_k"], cfg["signals"], cfg["evaluation"]
    c = cfg["costs"]
    cost_pts = c["tick"] + c["commission_rt"] / c["point_value"]

    # ------------------------------------------------------------- échantillon
    s = build_sample(cfg)
    print("Échantillon :", json.dumps(s.excluded, ensure_ascii=False, indent=1))
    targets = {"A": s.y_a, **{f"B{k}": s.y_b[k] for k in ks}}

    # ------------------------------------------------------------- prévisions
    preds = {}
    for spec, markets in cfg["specs"].items():
        preds[spec] = walk_forward(s, markets, targets, cfg)  # lève LeakError si fuite
        for t, p in preds[spec].items():
            p.to_parquet(OUT / f"pred_{spec}_{t}.parquet")
    oos = preds["c12"]["A"].index
    pos = s.days.get_indexer(oos)
    print(f"Hors échantillon : {len(oos)} jours, {oos[0].date()} → {oos[-1].date()}")

    rows = []
    for spec in cfg["specs"]:
        for t in targets:
            p = preds[spec][t]
            for lab, m in periods(p.index).items():
                rows.append({"spec": spec, "target": t, "period": lab, **forecast_metrics(p[m])})
    fc = pd.DataFrame(rows)
    fc.to_csv(OUT / "forecast.csv", index=False)

    # ------------------------------------------------------------- trading (CFD)
    ep = s.entry_px[pos]
    cost_frac = cost_pts / ep
    daily, weights, gross, stress = {}, {}, {}, {}
    for k in ks:
        xp = s.exit_px[k][pos]
        W = {}
        for spec in cfg["specs"]:
            p = preds[spec][f"B{k}"]
            W[f"npfda_{spec}_k{k}"] = npfda_positions(p, cost_frac, sig)
            W[f"ols_{spec}_k{k}"] = ols_positions(p, cost_frac, sig)
        W[f"long_k{k}"] = np.ones(len(oos))
        W[f"us_sign_k{k}"] = np.sign(s.us_ret[pos])
        W[f"overnight_sign_k{k}"] = np.sign(s.overnight[pos])
        Wdf = pd.DataFrame(W, index=oos)
        entry, exit_ = s.entry_ts[pos], s.exit_ts[k][pos]
        net = simulate(entry, exit_, ep, xp, Wdf, cost_pts)
        # contrôle croisé vectorbt / arithmétique
        diff = max(np.abs(net[col].values - arithmetic(Wdf[col].values, ep, xp, cost_pts)).max() for col in Wdf)
        assert diff < 1e-5, f"vectorbt et arithmétique divergent ({diff:.2e})"
        g = simulate(entry, exit_, ep, xp, Wdf, 0.0)
        st = simulate(entry, exit_, ep, xp, Wdf, cost_pts * c["cost_stress"])
        for col in Wdf:
            daily[col], weights[col], gross[col], stress[col] = net[col], Wdf[col].values, g[col], st[col]
    daily = pd.DataFrame(daily)
    daily.to_parquet(OUT / "daily_net.parquet")

    candidates = [f"{m}_{spec}_k{k}" for m in ["npfda", "ols"] for spec in cfg["specs"] for k in ks]
    n_trials = len(candidates)
    pr = ev["primary"]
    primary = f"{pr['model']}_{pr['spec']}_k{pr['k']}"
    best = max(candidates, key=lambda col: sharpe(daily[col]))

    rows = []
    for col in daily:
        for lab, m in periods(oos).items():
            row = {"strategy": col, "period": lab, **trading_metrics(daily[col][m], weights[col][m]),
                   "sharpe_gross": sharpe(gross[col][m]), "sharpe_cost_x2": sharpe(stress[col][m])}
            rows.append(row)
    tr = pd.DataFrame(rows)
    tr.to_csv(OUT / "trading.csv", index=False)

    # ------------------------------------------------------------- tests multiples
    trials = daily[candidates]
    res = {"n_trials_study": n_trials, "n_trials_global": ev["prior_trials"] + n_trials,
           "primary": primary, "best": best}
    for name, col in [("primary", primary), ("best", best)]:
        for N, lab in [(n_trials, "study"), (ev["prior_trials"] + n_trials, "global")]:
            d, sr0 = dsr(trials, col, N)
            res[f"dsr_{name}_{lab}"], res[f"sr0_ann_{lab}"] = d, sr0
        k = int(col.rsplit("_k", 1)[1])
        p_perm, perm = permutation_test(weights[col], ep, s.exit_px[k][pos], cost_pts, ev["n_permutations"], ev["seed"])
        res[f"perm_p_{name}"] = p_perm
        res[f"perm_sharpe_q95_{name}"] = float(np.quantile(perm, 0.95))
        res[f"sharpe_{name}"] = sharpe(daily[col])
    kp = pr["k"]
    res["primary_beats_long"] = bool((1 + daily[primary]).prod() > (1 + daily[f"long_k{kp}"]).prod())
    res["primary_beats_us_sign"] = bool((1 + daily[primary]).prod() > (1 + daily[f"us_sign_k{kp}"]).prod())
    res["B_passes"] = bool(res["sharpe_primary"] > 0 and res["perm_p_primary"] < 0.05
                           and res["dsr_primary_study"] > 0.95 and res["primary_beats_long"]
                           and res["primary_beats_us_sign"])
    a = fc[(fc.spec == "c12") & (fc.target == "A") & (fc.period == "all")].iloc[0]
    res["A_np_beats_ols_mse"] = bool(a["mse_np_mean"] < a["mse_ols"] and a["dm_p"] < 0.05)
    res["A_mode_sign_ok"] = bool(a["sign_p_np_mode"] < 0.05 and a["sign_err_np_mode_%"] < a["sign_err_ols_%"])
    # garde-fou « trop beau »
    hot = tr[(tr.period == "all") & ((tr.sharpe > 3) | (tr["hit_%"] > 70)) & tr.strategy.isin(candidates)]
    res["too_good"] = hot.strategy.tolist()
    (OUT / "tests.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float))

    # ------------------------------------------------------------- découpages
    vol = pd.Series(s.vol20[pos], index=oos)
    terc = pd.qcut(vol, 3, labels=["vol basse", "vol moyenne", "vol haute"])
    rows = []
    show = [primary, best, f"ols_c12_k{kp}", f"long_k{kp}", f"us_sign_k{kp}", f"overnight_sign_k{kp}"]
    for col in dict.fromkeys(show):
        for key, grp in [("année", oos.year), ("volatilité", terc.values)]:
            for g in pd.unique(grp):
                m = np.asarray(grp == g)
                rows.append({"strategy": col, "split": key, "group": str(g), **trading_metrics(daily[col][m], weights[col][m])})
    pd.DataFrame(rows).to_csv(OUT / "breakdown.csv", index=False)

    # ------------------------------------------------------------- validation FDAX (2025-03 →)
    fx_ok = np.isfinite(s.fdax_entry_px[pos])
    rows = []
    if fx_ok.any():
        fpos = pos[fx_ok]
        for k in ks:
            fe, fxp = s.fdax_entry_px[fpos], s.fdax_exit_px[k][fpos]
            ok = np.isfinite(fxp)
            cols = [col for col in daily if col.endswith(f"_k{k}")]
            Wf = pd.DataFrame({col: weights[col][fx_ok][ok] for col in cols}, index=oos[fx_ok][ok])
            rf = simulate(s.entry_ts[fpos][ok], s.exit_ts[k][fpos][ok], fe[ok], fxp[ok], Wf, cost_pts)
            rc = daily[cols][fx_ok][ok]
            for col in cols:
                rows.append({"strategy": col, **trading_metrics(rf[col], Wf[col].values),
                             "sharpe_cfd_same_days": sharpe(rc[col]),
                             "corr_daily_cfd_fdax": float(np.corrcoef(rf[col], rc[col])[0, 1]) if rf[col].std() > 0 else np.nan})
    pd.DataFrame(rows).to_csv(OUT / "fdax_validation.csv", index=False)

    # ------------------------------------------------------------- graphiques
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
    for ax, k in zip(axes.ravel(), ks):
        for col, style in [(f"npfda_c12_k{k}", "-"), (f"ols_c12_k{k}", "-"), (f"long_k{k}", "--"),
                           (f"us_sign_k{k}", ":"), (f"overnight_sign_k{k}", ":")]:
            ax.plot((1 + daily[col]).cumprod(), style, lw=1, label=col.rsplit("_k", 1)[0])
        ax.axvspan(pd.Timestamp("2020-06-15"), pd.Timestamp("2023-12-01"), color="0.9", lw=0)
        ax.set_title(f"Sortie 09:00 + {k} min (net de coûts, CFD DAX)")
        ax.axhline(1, color="0.5", lw=0.5)
    axes[0, 0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "equity_by_k.png", dpi=120)
    plt.close(fig)

    with pd.option_context("display.width", 220, "display.max_columns", 30, "display.float_format", "{:.4g}".format):
        print("\n== Prévision (toute la période hors échantillon)")
        cols = ["spec", "target", "n", "mse_zero", "mse_ols", "mse_np_mean", "dm_p", "sign_err_ols_%",
                "sign_err_np_mode_%", "sign_p_np_mode", "cpi_coverage_%", "no_signal_%"]
        print(fc[fc.period == "all"][cols].to_string(index=False))
        print("\n== Trading (net, toute la période)")
        print(tr[tr.period == "all"].drop(columns="period").to_string(index=False))
        print("\n== Tests :", json.dumps(res, indent=1, ensure_ascii=False, default=float))


if __name__ == "__main__":
    main()
