"""Télécharge des barres 1 minute de futures continus depuis London Strategic Edge (marché `futures`,
plan gratuit) et les écrit au format des fichiers Databento (index ts_event UTC, open high low close
volume), dans cache/lse/<CODE>_lse_1m.parquet (cache/ hors git ; pas d'accès en écriture à
D:/quant-data depuis les sessions Claude : copier à la main si besoin).

uv run python fetch_lse.py                 → argent (SILVER → SI), 2017-04 → 2026-08-28
uv run python fetch_lse.py PLATINUM PL     → autre symbole du marché futures, code local PL
uv run python fetch_lse.py XAU/USD XAU commodities 2003-01-01 2015-12-31   → or au comptant (n° 21)

Clé : LONDONSTRATEGIE_KEY dans .env, envoyée dans l'en-tête X-API-Key (jamais affichée).
API : GET https://download.londonstrategicedge.com/v3/export (doc : github.com/londonstrategicedge/lse-data,
docs/api.md). Limites du plan gratuit : 60 appels/min, 2,5 M lignes par export, 12,5 M lignes par jour.

Ce que vaut la série (vérifié le 2026-11-02) :
- horodatage UTC au début de la minute, comme Databento : GOLD colle à GC Databento à 1 tick près ;
- contrat « front » qui ne roule qu'au premier jour du mois de livraison : les 2-3 derniers jours
  avant chaque roulement sont sur un contrat quasi vide (ex. 2024-02-29 : 58 barres). Prix NON ajustés.
  Traiter ces jours (filtre de volume) et ajuster les roulements avant tout calcul ;
- pas de données avant 2017-04-02 pour SILVER.
Arrêt au 2026-08-28 par défaut : le holdout reste à part.
"""

from __future__ import annotations

import io
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://download.londonstrategicedge.com"
DATA = Path("cache/lse")
START, END = "2017-01-01", "2026-08-28"


def key() -> str:
    for line in open(".env", encoding="utf-8"):
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return os.environ["LONDONSTRATEGIE_KEY"]


def export(sym: str, a: str, b: str, h: dict, market: str = "futures") -> pd.DataFrame | None:
    for _ in range(5):
        r = requests.get(f"{BASE}/v3/export", headers=h, timeout=600, params={
            "market": market, "symbol": sym, "timeframe": "1m", "from": a, "to": b, "format": "csv"})
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 30)))
            continue
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return pd.read_csv(io.StringIO(r.text), parse_dates=["time"])
    raise RuntimeError(f"{sym} {a}→{b} : trop de refus 429")


def main(sym: str = "SILVER", code: str = "SI", market: str = "futures", start: str = START, end: str = END):
    h = {"X-API-Key": key()}
    parts = []
    for y in range(int(start[:4]), int(end[:4]) + 1):
        a, b = max(f"{y}-01-01", start), min(f"{y}-12-31", end)
        d = export(sym, a, b, h, market)
        n = 0 if d is None else len(d)
        print(f"{sym} {a} → {b} : {n} barres", flush=True)
        if d is not None:
            parts.append(d)
    df = pd.concat(parts).drop_duplicates("time").sort_values("time")
    out = pd.DataFrame({c: df[c].astype(float).values for c in ["open", "high", "low", "close", "volume"]},
                       index=pd.DatetimeIndex(df["time"]).tz_localize("UTC").rename("ts_event"))
    DATA.mkdir(parents=True, exist_ok=True)
    dest = DATA / f"{code}_lse_1m.parquet"
    out.to_parquet(dest)
    print(f"{len(out)} barres {out.index[0]} → {out.index[-1]} écrites dans {dest}")


if __name__ == "__main__":
    main(*sys.argv[1:6]) if len(sys.argv) >= 3 else main()
