"""Contrôle des trous dans NQ 1 minute (D:/quant-data/Cotations/indices/NQ_v0_1m.parquet).

uv run python coinflip_gaps.py → results/coinflip/gaps.csv + résumé console

Séance CME Globex : dimanche 18:00 → vendredi 17:00 heure de New York, pause
quotidienne 17:00–18:00. Chaque intervalle > 1 minute entre deux barres est
classé : pause quotidienne, week-end, jour férié / clôture anticipée, ou
inexpliqué (minute sans transaction ou vraie coupure de données).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
SRC = Path("D:/quant-data/Cotations/indices/NQ_v0_1m.parquet")
OUT = Path("results/coinflip")
OUT.mkdir(parents=True, exist_ok=True)
NY = "America/New_York"


def classify(prev: pd.Timestamp, nxt: pd.Timestamp) -> str:
    """prev, nxt : heures de New York de la barre avant / après le trou."""
    gap = nxt - prev
    reopen_18 = nxt.hour == 18 and nxt.minute == 0
    if reopen_18 and gap <= pd.Timedelta("61min") and prev.hour == 16 and prev.minute == 59:
        return "pause quotidienne"
    if reopen_18 and nxt.dayofweek == 6 and prev.dayofweek == 4 and gap <= pd.Timedelta("49h1min"):
        return "week-end"
    if reopen_18 and gap >= pd.Timedelta("60min"):
        return "férié / clôture anticipée"
    return "inexpliqué"


def main() -> None:
    df = pd.read_parquet(SRC)
    idx = df.index
    print(f"NQ : {len(df):,} barres, {idx[0]} → {idx[-1]} ({(idx[-1] - idx[0]).days / 365.25:.2f} ans)")
    print(f"doublons : {idx.duplicated().sum()}, trié : {idx.is_monotonic_increasing}, NaN : {int(df.isna().sum().sum())}")
    bad = (df.high < df[["open", "close"]].max(axis=1)) | (df.low > df[["open", "close"]].min(axis=1))
    print(f"barres OHLC incohérentes : {int(bad.sum())}, volume nul : {int((df.volume <= 0).sum())}")

    ny = idx.tz_convert(NY)
    d = pd.Series(ny[1:] - ny[:-1], index=ny[1:])
    holes = d[d > pd.Timedelta("1min")]
    rows = [(p, n, (n - p).total_seconds() / 60 - 1, classify(p, n))
            for p, n in zip(holes.index - holes.values, holes.index)]
    g = pd.DataFrame(rows, columns=["avant_ny", "apres_ny", "minutes_manquantes", "type"])
    g.to_csv(OUT / "gaps.csv", index=False)

    print("\nIntervalles > 1 min entre barres :")
    print(g.groupby("type")["minutes_manquantes"].agg(["count", "sum", "median", "max"]).to_string())

    u = g[g.type == "inexpliqué"]
    print("\nTrous inexpliqués par durée (minutes manquantes) :")
    bins = [0, 1, 2, 5, 15, 60, 10_000]
    print(pd.cut(u.minutes_manquantes, bins).value_counts().sort_index().to_string())
    print("\nPlus longs trous inexpliqués :")
    print(u.nlargest(15, "minutes_manquantes").to_string(index=False))

    # couverture de la fenêtre utile : 01:00 heure de Paris, jours de semaine
    paris = idx.tz_convert("Europe/Paris")
    at1 = pd.Series(1, index=paris[(paris.hour == 1) & (paris.minute == 0)].normalize())
    days = pd.bdate_range(paris[0].normalize().tz_localize(None), paris[-1].normalize().tz_localize(None))
    have = set(at1.index.tz_localize(None))
    missing = [x for x in days if x not in have]
    print(f"\nJours ouvrés sans barre à 01:00 Paris : {len(missing)} / {len(days)}")
    print(", ".join(str(x.date()) for x in missing))

    # par heure de Paris : part de minutes présentes pendant la séance asiatique
    asia = df[(paris.hour >= 0) & (paris.hour < 8)]
    p_asia = asia.index.tz_convert("Europe/Paris")
    per_day = pd.Series(1, index=p_asia).groupby(p_asia.date).size()
    print(f"\nSéance 00:00–08:00 Paris : minutes présentes par jour, médiane {per_day.median():.0f}/480, "
          f"jours < 470 : {(per_day < 470).sum()} / {len(per_day)}")


if __name__ == "__main__":
    main()
