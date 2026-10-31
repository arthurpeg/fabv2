"""Tables du rapport de la récolte 1 à partir de results/recolte1/ic.csv et vol_relations.csv.

uv run python report_recolte1.py   → results/recolte1/tables.md
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("results/recolte1")
ORDER = ["NQ", "ES", "YM", "GC", "6E", "6B", "6J", "6A", "univers"]


def f(m, lo, hi, d=1):
    if not np.isfinite(m):
        return "—"
    s = f"{m:+.{d}f}"
    return s + (f" [{lo:+.{d}f} ; {hi:+.{d}f}]" if np.isfinite(lo) else "")


def flag(lo, hi):
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return ""
    return "▲" if lo > 0 else ("▼" if hi < 0 else "")


def main():
    ic = pd.read_csv(OUT / "ic.csv")
    ic["ord"] = ic["asset"].map({a: i for i, a in enumerate(ORDER)})
    lines = []
    tot = ic.dropna(subset=["net_bp_lo"])
    lines.append(f"Tests avec IC calculable : {len(tot)} (règle × actif). "
                 f"IC net par trade > 0 : {(tot['net_bp_lo'] > 0).sum()} ; < 0 : {(tot['net_bp_hi'] < 0).sum()}. "
                 f"IC brut > 0 : {(tot['gross_bp_lo'] > 0).sum()} ; < 0 : {(tot['gross_bp_hi'] < 0).sum()}.\n")
    # synthèse par papier
    lines.append("| Papier | Tests | Brut IC > 0 | Brut IC < 0 | Net IC > 0 | Net IC < 0 | Sharpe net IC > 0 |")
    lines.append("|---|---|---|---|---|---|---|")
    for p, g in ic.groupby("paper", sort=False):
        g = g.dropna(subset=["sharpe_net"])
        lines.append(f"| {p} | {len(g)} | {(g['gross_bp_lo'] > 0).sum()} | {(g['gross_bp_hi'] < 0).sum()} | "
                     f"{(g['net_bp_lo'] > 0).sum()} | {(g['net_bp_hi'] < 0).sum()} | {(g['sharpe_net_lo'] > 0).sum()} |")
    lines.append("")
    for p, g in ic.groupby("paper", sort=False):
        lines.append(f"\n### {p}\n")
        lines.append("| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |")
        lines.append("|---|---|---|---|---|---|---|")
        rule_order = {r: i for i, r in enumerate(dict.fromkeys(g["rule"]))}
        g = g.assign(ro=g["rule"].map(rule_order)).sort_values(["ro", "ord"])
        for _, r in g.iterrows():
            lines.append(
                f"| {r['rule']} | {r['asset']} | {int(r['n']) if np.isfinite(r['n']) else 0} | "
                f"{f(r.get('gross_bp', np.nan), r.get('gross_bp_lo', np.nan), r.get('gross_bp_hi', np.nan))} | "
                f"{f(r.get('net_bp', np.nan), r.get('net_bp_lo', np.nan), r.get('net_bp_hi', np.nan))} | "
                f"{f(r.get('sharpe_net', np.nan), r.get('sharpe_net_lo', np.nan), r.get('sharpe_net_hi', np.nan), 2)} | "
                f"{flag(r.get('net_bp_lo', np.nan), r.get('net_bp_hi', np.nan))} |")
    vr = pd.read_csv(OUT / "vol_relations.csv")
    lines.append("\n### [17] Zhang-Zhao et [18] Ahoniemi-Lanne : relations de volatilité (pas de règle de trading)\n")
    lines.append("| Papier | Relation | Actif | n | Valeur [IC 95 %] |")
    lines.append("|---|---|---|---|---|")
    for _, r in vr.iterrows():
        lines.append(f"| {r['paper']} | {r['relation']} | {r['asset']} | {int(r['n'])} | "
                     f"{f(r['corr'], r.get('lo', np.nan), r.get('hi', np.nan), 3)} |")
    (OUT / "tables.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:25]))


if __name__ == "__main__":
    main()
