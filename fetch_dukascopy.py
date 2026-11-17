"""Télécharge des barres 1 minute de FX au comptant (bid ET ask) depuis Dukascopy (gratuit, sans clé)
et écrit un fichier par paire au format proche de Databento : index ts_event UTC (début de minute).

uv run --with dukascopy-python python fetch_dukascopy.py              → 9 majeures : heures 2010 → 2016, minutes 2012-01-11 → 2016
uv run --with dukascopy-python python fetch_dukascopy.py --assemble   → reconstruit seulement les fichiers finaux

But : vérifier Zhang (2018, SSRN 3138756) sur sa période (2010-05 → 2015-12) et sur les devises sans
future dans nos fichiers (CHF, CAD, NZD, NOK, SEK). 2016 sert de recouvrement avec les futures CME
(6E, 6B, 6J, 6A) pour contrôler la série. Ce sont des cotations au comptant de l'ECN de Dukascopy
(SWFX), pas des transactions et pas des CFD ; le volume n'est pas celui du marché.

Qualité vérifiée le 2026-11-17 (M15 bid, 2016-2025) : corrélation des rendements 15 min avec 6E/6B/6J
0,993-0,996, rendements de sessions de plusieurs heures identiques à ≤ 0,15 bp près (wiki/log.md).

Sortie : cache/dukascopy/raw/<1m|1h>/<PAIRE>/<bid|ask>_<année>.parquet (reprenable), puis
cache/dukascopy/<PAIRE>_<1m|1h>.parquet : open/high/low/close du bid, open/high/low/close de l'ask,
mid_open, mid_close, spread_close (ask − bid, en prix), volume (bid). Les minutes sans aucune
cotation (week-ends remplis par la bibliothèque : volume nul et prix figé) sont retirées.
Paires cotées comme sur le marché (USDJPY = yens par dollar) : inverser au besoin pour avoir la
devise étrangère en dollars, comme dans le papier.
"""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import dukascopy_python as dk
from dukascopy_python import instruments as I

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("cache/dukascopy")
RAW = OUT / "raw"
PAIRS = {
    "EURUSD": I.I_EUR_USD, "GBPUSD": I.I_GBP_USD, "USDJPY": I.I_USD_JPY, "USDCHF": I.I_USD_CHF,
    "AUDUSD": I.I_AUD_USD, "USDCAD": I.I_USD_CAD, "NZDUSD": I.I_NZD_USD,
    "USDNOK": I.I_USD_NOK, "USDSEK": I.I_USD_SEK,
}
# La bibliothèque ne sert aucune minute avant le 2012-01-11 (vérifié le 2026-11-17 ; les fichiers
# BID_candles_min_1.bi5 du datafeed répondent 503) : minutes 2012-2016, heures 2010-2016 (comme Zhang).
YEARS = {"1m": range(2012, 2017), "1h": range(2010, 2017)}
UNIT = {"1m": dk.TimeUnit.MINUTE, "1h": dk.TimeUnit.HOUR}
SIDES = {"bid": dk.OfferSide.BID, "ask": dk.OfferSide.ASK}


def fetch_year(pair: str, side: str, year: int, freq: str) -> None:
    path = RAW / freq / pair / f"{side}_{year}.parquet"
    if path.exists():
        return
    a = datetime(year, 1, 1, tzinfo=timezone.utc)
    b = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    for attempt in range(4):
        try:
            df = dk.to_dataframe(dk.fetch_candles(PAIRS[pair], 1, UNIT[freq], SIDES[side], a, b))
            break
        except Exception as e:  # réseau : on réessaie, puis on abandonne cette tranche
            print(f"  {pair} {side} {year} : essai {attempt + 1} raté ({e})", flush=True)
            time.sleep(10 * (attempt + 1))
    else:
        print(f"  ÉCHEC {pair} {side} {year}", flush=True)
        return
    if df.empty:
        print(f"  VIDE {pair} {side} {year} {freq}", flush=True)
        return
    df = df[["open", "high", "low", "close", "volume"]]
    df = df[(df.index >= a) & (df.index < b)]
    df = df[~df.index.duplicated()].sort_index()
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)
    print(f"  {pair} {side} {year} {freq} : {len(df)} barres", flush=True)


def assemble(pair: str, freq: str) -> None:
    parts = {}
    for side in SIDES:
        files = sorted((RAW / freq / pair).glob(f"{side}_*.parquet"))
        if len(files) != len(YEARS[freq]):
            print(f"  {pair} {freq} : {side} incomplet ({len(files)}/{len(YEARS[freq])} ans), pas assemblé")
            return
        parts[side] = pd.concat(pd.read_parquet(f) for f in files)
    bid, ask = parts["bid"], parts["ask"]
    df = bid.join(ask.drop(columns="volume").add_prefix("ask_"), how="inner")
    # minutes sans cotation : volume nul et prix figé sur la minute
    vide = (df["volume"] <= 0) & (df["high"] == df["low"]) & (df["ask_high"] == df["ask_low"])
    df = df[~vide]
    df["mid_open"] = (df["open"] + df["ask_open"]) / 2
    df["mid_close"] = (df["close"] + df["ask_close"]) / 2
    df["spread_close"] = df["ask_close"] - df["close"]
    df.index.name = "ts_event"
    df.to_parquet(OUT / f"{pair}_{freq}.parquet")
    print(f"  {pair} {freq} : {len(df)} barres, {df.index.min()} → {df.index.max()}, {vide.sum()} barres vides retirées")


def main() -> None:
    if "--assemble" not in sys.argv:
        for freq in ("1h", "1m"):
            for pair in PAIRS:
                for year in YEARS[freq]:
                    for side in SIDES:
                        fetch_year(pair, side, year, freq)
    for freq in ("1h", "1m"):
        for pair in PAIRS:
            assemble(pair, freq)


if __name__ == "__main__":
    main()
