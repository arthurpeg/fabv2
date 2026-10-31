"""Rendements par session (Asie / Europe / US) sur ES, NQ, YM — 1 minute Databento.

uv run python run_sessions.py   → results/sessions/ (sessions_<ACTIF>.csv, summary.csv, by_year.csv)

Sessions définies en heures locales (heure d'été gérée par fuseau) :
  Asie   : clôture NYSE de la séance précédente (16:00 NY, 13:00 en demi-séance) → 08:00 Londres
  Europe : 08:00 Londres → 09:30 New York
  US     : 09:30 New York → clôture NYSE (16:00, 13:00 en demi-séance)
Jours = séances NYSE (exchange_calendars XNYS).
Asie + Europe = close-to-open ; US = open-to-close.

Prix à l'instant T = clôture de la dernière barre démarrant dans [T-5 min, T-1 min] ;
sinon le point manque et les sessions qui en dépendent sont exclues (trous de données). Prix ajustés en ratio aux roulements, sinon le saut de
roulement (00:00 UTC) tomberait dans la session asiatique. fab.core.load n'est pas
utilisé : son seuil manque ~10 roulements par actif (écart de portage faible en
2017-2019) et prend le trou de données du 2020-06-30 pour un roulement sur YM.

Les rendements de chaque session sont calculés par vectorbt : un portefeuille long
100 % entre le début et la fin de chaque session, sans frais.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import exchange_calendars as xc
import vectorbt as vbt

DATA = Path("D:/quant-data/Cotations/indices")
OUT = Path("results/sessions")
NY, LDN = "America/New_York", "Europe/London"
SLACK = pd.Timedelta(minutes=5)
SESSIONS = ["asia", "europe", "us"]


def load(name: str) -> pd.DataFrame:
    """Barres brutes .v.0 ajustées en ratio : un roulement par mois d'échéance (mars, juin,
    sept., déc.) = le plus grand |écart| à 00:00 UTC entre le 7 et le 22, barre précédente
    à moins de 60 min (ni l'arrêt quotidien 21-22 h UTC, ni un trou de données)."""
    df = pd.read_parquet(DATA / f"{name}_v0_1m.parquet")
    df = df[~df.index.duplicated()].sort_index()
    gap = df["open"] / df["close"].shift() - 1
    ix = df.index
    prev = pd.Series(ix, index=ix).shift()
    cand = (ix.hour == 0) & (ix.minute == 0) & ((ix - prev) <= pd.Timedelta(minutes=60)).values
    cand &= ix.month.isin([3, 6, 9, 12]) & (ix.day >= 7) & (ix.day <= 22)
    g = gap[cand]
    rolls = pd.DatetimeIndex(g.abs().groupby([g.index.year, g.index.month]).idxmax().tolist())
    step = pd.Series(1.0, index=ix)
    step.loc[rolls] = 1 + gap.loc[rolls]
    factor = step[::-1].cumprod()[::-1].shift(-1).fillna(1.0)  # barres strictement antérieures
    out = df[["open", "high", "low", "close"]].mul(factor, axis=0)
    out["factor"] = factor
    out.attrs["rolls"] = gap.loc[rolls]
    return out


def price_at(close: pd.Series, when: pd.Series) -> pd.Series:
    """Clôture de la dernière barre démarrant dans [T-5 min, T-1 min] (barres horodatées au début)."""
    bars = close.rename("px").rename_axis("bar").reset_index()
    q = pd.DataFrame({"T": when, "key": when - pd.Timedelta(minutes=1)}).reset_index(drop=True).sort_values("key")
    m = pd.merge_asof(q, bars, left_on="key", right_on="bar", direction="backward")
    m.loc[m["bar"] < m["T"] - SLACK, "px"] = np.nan
    return pd.Series(m.sort_index()["px"].values, index=when.index)


def boundaries(df: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par séance NYSE (calendrier XNYS) : instants UTC et prix des bornes
    08:00 Londres, ouverture et clôture officielles (13:00 les demi-séances)."""
    sched = xc.get_calendar("XNYS").schedule.loc[str(df.index[0].date()):str(df.index[-1].date())]
    b = pd.DataFrame(index=pd.DatetimeIndex(sched.index))
    b["t_eu"] = (b.index + pd.Timedelta("08:00:00")).tz_localize(LDN).tz_convert("UTC")
    b["t_open"] = sched["open"]
    b["t_close"] = sched["close"]
    b["t_prev"] = b["t_close"].shift(1)  # clôture de la séance NYSE précédente
    b = b.iloc[1:]
    for col in ["prev", "eu", "open", "close"]:
        b[f"p_{col}"] = price_at(df["close"], b[f"t_{col}"])
    b["half_day"] = b["t_close"].dt.tz_convert(NY).dt.hour < 16
    return b


def vbt_session_returns(b: pd.DataFrame, start: str, end: str) -> pd.Series:
    """Long 100 % de `start` à `end`, rendement de chaque aller-retour lu dans pf.trades."""
    ok = b[[f"p_{start}", f"p_{end}"]].notna().all(axis=1)
    s = b[ok]
    ev = pd.concat([
        pd.DataFrame({"ts": s[f"t_{start}"].values, "price": s[f"p_{start}"].values, "size": 1.0, "day": s.index}),
        pd.DataFrame({"ts": s[f"t_{end}"].values, "price": s[f"p_{end}"].values, "size": 0.0, "day": s.index}),
    ])
    # sortie et entrée au même instant (US 16:00 → Asie 16:00) n'arrivent pas : une session à la fois
    ev = ev.sort_values(["ts", "size"]).set_index("ts")
    assert ev.index.is_unique
    pf = vbt.Portfolio.from_orders(
        close=ev["price"], size=ev["size"], size_type="targetpercent",
        direction="longonly", fees=0.0, init_cash=1_000_000.0, freq="1min",
    )
    tr = pf.trades.records_readable
    assert len(tr) == len(s) and (tr["Status"] == "Closed").all()
    ret = pd.Series(tr["Return"].values, index=ev.loc[tr["Entry Timestamp"], "day"].values)
    return ret.sort_index()


def stats(r: pd.Series) -> dict:
    bp = r * 1e4
    lg = np.log1p(r)
    return {
        "n": len(r),
        "mean_bp": bp.mean(),
        "median_bp": bp.median(),
        "std_bp": bp.std(),
        "t_stat": bp.mean() / bp.std() * np.sqrt(len(r)),
        "pct_pos": (r > 0).mean() * 100,
        "cum_log_bp": lg.sum() * 1e4,
        "ann_ret_pct": (np.exp(lg.mean() * 252) - 1) * 100,
        "ann_sharpe": r.mean() / r.std() * np.sqrt(252),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summary, years = [], []
    for name in ["ES", "NQ", "YM"]:
        df = load(name)
        rolls = df.attrs["rolls"]
        print(f"{name} : {len(rolls)} roulements, |écart| min {rolls.abs().min()*1e4:.1f} bp, "
              f"max {rolls.abs().max()*1e4:.1f} bp")
        rolls.mul(1e4).round(2).rename("gap_bp").to_csv(OUT / f"rolls_{name}.csv")
        b = boundaries(df)
        r = pd.DataFrame({
            "asia": vbt_session_returns(b, "prev", "eu"),
            "europe": vbt_session_returns(b, "eu", "open"),
            "us": vbt_session_returns(b, "open", "close"),
            "close_to_open": vbt_session_returns(b, "prev", "open"),
        })
        # close-to-close se chevauche d'un jour à l'autre (16:00 → 16:00) : calcul direct
        r["close_to_close"] = b["p_close"] / b["p_prev"] - 1
        # ne garder que les jours où les trois sessions existent : décomposition exacte
        full = r.dropna(subset=SESSIONS)

        # contrôles : composition des sessions = close-to-open / close-to-close
        c2o = (1 + full["asia"]) * (1 + full["europe"]) - 1
        assert np.allclose(c2o, full["close_to_open"], atol=1e-10)
        c2c = (1 + c2o) * (1 + full["us"]) - 1
        assert np.allclose(c2c, full["close_to_close"], atol=1e-10)
        # contrôle indépendant de vectorbt sur une session
        direct = (b["p_open"] / b["p_eu"] - 1).reindex(full.index)
        assert np.allclose(direct, full["europe"], atol=1e-10)
        # session qui contient un roulement (facteur différent entre ses deux bornes)
        fac = df["factor"]
        f_a = fac.reindex(pd.DatetimeIndex(b.loc[full.index, "t_prev"]), method="ffill").values
        f_b = fac.reindex(pd.DatetimeIndex(b.loc[full.index, "t_eu"]), method="ffill").values
        roll_in_asia = pd.Series(~np.isclose(f_a, f_b), index=full.index)

        full.to_csv(OUT / f"sessions_{name}.csv")
        print(f"\n=== {name} : {full.index[0].date()} → {full.index[-1].date()}, {len(full)} jours "
              f"(sur {len(b)} jours ouvrés ; {len(b) - len(full)} exclus), roulements en Asie : {roll_in_asia.sum()}")
        for col in ["asia", "europe", "us", "close_to_open", "close_to_close"]:
            row = {"asset": name, "session": col, **stats(full[col])}
            summary.append(row)
            print(f"  {col:15s} moy {row['mean_bp']:7.2f} bp  méd {row['median_bp']:7.2f}  t {row['t_stat']:6.2f}  "
                  f"%>0 {row['pct_pos']:5.1f}  cum {row['cum_log_bp']:8.0f} bp  ann {row['ann_ret_pct']:6.2f}%")
        # robustesse : sans les jours de roulement
        nr = full[~roll_in_asia]
        for col in ["asia", "close_to_open"]:
            summary.append({"asset": name, "session": f"{col}_hors_roulements", **stats(nr[col])})
        for y, g in full.groupby(full.index.year):
            for col in ["asia", "europe", "us", "close_to_open"]:
                years.append({"asset": name, "year": y, "session": col, "n": len(g),
                              "mean_bp": g[col].mean() * 1e4, "cum_log_bp": np.log1p(g[col]).sum() * 1e4})

    pd.DataFrame(summary).round(3).to_csv(OUT / "summary.csv", index=False)
    pd.DataFrame(years).round(3).to_csv(OUT / "by_year.csv", index=False)


if __name__ == "__main__":
    main()
