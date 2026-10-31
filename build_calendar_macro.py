"""Calendrier des annonces US « rouges » (liste type ForexFactory, sans les inscriptions au chômage),
reconstruit depuis les sources officielles. Écrit config/calendrier_macro_us.csv.

uv run python build_calendar_macro.py

Sources (dates de publication, une ligne par annonce) :
- BLS, pages d'archives (date dans le nom du fichier) : NFP (empsit), CPI, PPI à 8:30 ; JOLTS à 10:00.
- BEA, archives de communiqués : PIB estimation avancée (8:30), revenus et dépenses des ménages / PCE (8:30).
- Réserve fédérale : décisions FOMC (communiqué 14:00) et minutes (14:00).
- ISM manufacturier (1er jour ouvré du mois, 10:00) et services (3e jour ouvré, 10:00) : règle de
  calendrier publiée par l'ISM, appliquée au calendrier NYSE (approximation, signalée dans la colonne `source`).
- Ventes au détail (Census, 8:30) : `RETAIL_FILE` si fourni (le site du Census refuse les requêtes scriptées).
Les requêtes BLS/BEA portent une adresse de contact dans l'en-tête, comme ces sites l'exigent (accord du 2026-10-31).
"""

from __future__ import annotations

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
RETAIL_FILE = Path("config/ventes_detail_dates.csv")  # colonne `date`, optionnel


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


def bea(product: int, keep, label: str, hour: str) -> list[tuple]:
    out, page = [], 0
    while True:
        h = get(f"https://www.bea.gov/news/archive?field_related_product_target_id={product}&page={page}")
        items = re.findall(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})[^"]*"[^>]*>.*?</time>.*?<a href="(/news/[^"]+)"[^>]*>([^<]+)</a>', h, re.S)
        if not items:
            items = [(None, a, t) for a, t in re.findall(r'<a href="(/news/20\d\d/[^"]+)"[^>]*>([^<]+)</a>', h)]
        new = 0
        for d, href, title in items:
            if not keep(title):
                continue
            if d is None:
                page_h = get("https://www.bea.gov" + href)
                mm = re.search(r'datetime="(\d{4}-\d{2}-\d{2})', page_h)
                d = mm.group(1) if mm else None
            if d:
                out.append((pd.Timestamp(d), label, hour, "https://www.bea.gov" + href))
                new += 1
        dates = [x[0] for x in out]
        if not items or (dates and min(dates) < pd.Timestamp(START)) or page > 40:
            break
        page += 1
    return out


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
    rows = []
    for slug, lab, hr in [("empsit", "NFP", "08:30"), ("cpi", "CPI", "08:30"), ("ppi", "PPI", "08:30"), ("jolts", "JOLTS", "10:00")]:
        rows += bls(slug, lab, hr)
        print(lab, "ok", flush=True)
    rows += bea(451, lambda t: "Advance" in t, "PIB avancé", "08:30")
    print("PIB ok", flush=True)
    rows += bea(476, lambda t: "Personal Income and Outlays" in t, "PCE (revenus et dépenses)", "08:30")
    print("PCE ok", flush=True)
    rows += fomc()
    print("FOMC ok", flush=True)
    rows += ism()
    if RETAIL_FILE.exists():
        r = pd.read_csv(RETAIL_FILE, parse_dates=["date"])
        rows += [(d, "Ventes au détail", "08:30", str(RETAIL_FILE)) for d in r["date"]]
    else:
        print("ventes au détail : fichier absent, non incluses")
    d = pd.DataFrame(rows, columns=["date", "annonce", "heure_ET", "source"])
    d["date"] = pd.to_datetime(d["date"]).dt.normalize()
    d = d[(d["date"] >= START) & (d["date"] <= END)].drop_duplicates(["date", "annonce"]).sort_values(["date", "annonce"])
    d.to_csv(OUT, index=False, date_format="%Y-%m-%d")
    print(d.groupby([d["date"].dt.year, "annonce"]).size().unstack(fill_value=0).to_string())


if __name__ == "__main__":
    main()
