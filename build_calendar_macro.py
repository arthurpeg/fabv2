"""Calendrier des annonces US « rouges » (liste type ForexFactory, sans les inscriptions au chômage),
reconstruit depuis les sources officielles. Écrit config/calendrier_macro_us.csv.

uv run python build_calendar_macro.py

Sources (dates de publication, une ligne par annonce) :
- BLS, pages d'archives (date dans le nom du fichier) : NFP (empsit), CPI, PPI à 8:30 ; JOLTS à 10:00.
- FRED / ALFRED (Fed de Saint-Louis, `FRED_API_KEY` dans .env) : date de première publication de chaque
  observation (`output_type=4`) de GDPC1 (PIB avancé), PCEPI (revenus et dépenses des ménages, PCE) et RSAFS
  (ventes au détail, Census) ; toutes à 8:30. Les archives BEA et le site du Census, incomplets ou bloqués, ne servent pas.
- Réserve fédérale : décisions FOMC (communiqué 14:00) et minutes (14:00).
- ISM manufacturier (1er jour ouvré du mois, 10:00) et services (3e jour ouvré, 10:00) : règle de
  calendrier publiée par l'ISM, appliquée au calendrier NYSE (approximation, signalée dans la colonne `source`).
Les requêtes BLS/BEA portent une adresse de contact dans l'en-tête, comme ces sites l'exigent (accord du 2026-10-31).
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

import exchange_calendars as xc
import pandas as pd
import requests

sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "fabv2-research arthur.peg2@gmail.com"}
START, END = "2010-06-01", "2026-08-28"
OUT = Path("config/calendrier_macro_us.csv")


def get(url: str) -> str:
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    time.sleep(1.0)
    return r.text


def bls(slug: str, label: str, hour: str) -> list[tuple]:
    h = get(f"https://www.bls.gov/bls/news-release/{slug}.htm")
    out = []
    for m in sorted(set(re.findall(rf"archives/{slug}_(\d{{8}})", h))):
        out.append((pd.to_datetime(m, format="%m%d%Y"), label, hour,
                    f"https://www.bls.gov/news.release/archives/{slug}_{m}.htm"))
    return out


def fred_first_release(series: str, label: str) -> list[tuple]:
    """Date de première publication de chaque observation (ALFRED, initial release only)."""
    key = os.environ["FRED_API_KEY"]
    r = requests.get("https://api.stlouisfed.org/fred/series/observations", timeout=60, params=dict(
        series_id=series, api_key=key, file_type="json", output_type=4, observation_start="2009-10-01",
        realtime_start="1776-07-04", realtime_end="9999-12-31"))
    r.raise_for_status()
    return [(pd.Timestamp(o["realtime_start"]), label, "08:30", f"FRED {series} (première publication)")
            for o in r.json()["observations"]]


def fomc() -> list[tuple]:
    out = []
    pages = ["https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"] + [
        f"https://www.federalreserve.gov/monetarypolicy/fomchistorical{y}.htm" for y in range(2010, 2021)]
    for url in pages:
        try:
            h = get(url)
        except requests.HTTPError:
            continue
        for m in set(re.findall(r"monetary(20\d{6})a", h)):
            out.append((pd.to_datetime(m), "FOMC décision", "14:00", url))
        for m in set(re.findall(r"Released ([A-Z][a-z]+ \d{1,2}, 20\d{2})", h)):
            out.append((pd.to_datetime(m), "FOMC minutes", "14:00", url))
    return out


def ism() -> list[tuple]:
    s = xc.get_calendar("XNYS").schedule.loc[START:END].index
    by_month = pd.Series(s, index=s).groupby([s.year, s.month])
    out = []
    for _, days in by_month:
        days = list(days)
        out.append((days[0], "ISM manufacturier", "10:00", "règle ISM : 1er jour ouvré (approximation)"))
        if len(days) >= 3:
            out.append((days[2], "ISM services", "10:00", "règle ISM : 3e jour ouvré (approximation)"))
    return out


def main():
    for line in open(".env", encoding="utf-8"):
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    rows = []
    for slug, lab, hr in [("empsit", "NFP", "08:30"), ("cpi", "CPI", "08:30"), ("ppi", "PPI", "08:30"), ("jolts", "JOLTS", "10:00")]:
        rows += bls(slug, lab, hr)
        print(lab, "ok", flush=True)
    rows += fred_first_release("GDPC1", "PIB avancé")
    rows += fred_first_release("PCEPI", "PCE (revenus et dépenses)")
    rows += fred_first_release("RSAFS", "Ventes au détail")
    print("FRED ok", flush=True)
    rows += fomc()
    print("FOMC ok", flush=True)
    rows += ism()
    d = pd.DataFrame(rows, columns=["date", "annonce", "heure_ET", "source"])
    d["date"] = pd.to_datetime(d["date"]).dt.normalize()
    d = d[(d["date"] >= START) & (d["date"] <= END)].drop_duplicates(["date", "annonce"]).sort_values(["date", "annonce"])
    d.to_csv(OUT, index=False, date_format="%Y-%m-%d")
    print(d.groupby([d["date"].dt.year, "annonce"]).size().unstack(fill_value=0).to_string())


if __name__ == "__main__":
    main()
