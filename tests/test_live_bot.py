"""Rejeu du bot complet (live/bot.py) avec un faux terminal MT5 sur les barres NQ d'août 2026, horloge simulée :
le bot doit prendre exactement les trades 3n / M2 / mom du backtest (mêmes séances, même sens, même stop)."""

from __future__ import annotations

import itertools
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from live.bot import Bot

NQ = Path("D:/quant-data/Cotations/indices/NQ_v0_1m.parquet")
NY = "America/New_York"
pytestmark = pytest.mark.skipif(not NQ.exists(), reason="données NQ absentes")


class FauxMT5:
    """Marché rejoué sur des barres 1 min : exécution à l'open de la minute en cours, SL / TP sur les hauts et bas."""

    vpp = 1.0

    def __init__(self, m1: pd.DataFrame, horloge, bascule=None):
        self.m1, self.h, self.pos, self.fermes, self.n = m1, horloge, {}, {}, itertools.count(1)
        self.bascule = bascule  # instant du passage à un nouvel essai FTMO (nouveau login, solde remis à 10 000 $)
        self.info = type("I", (), dict(volume_step=0.01, volume_min=0.01, volume_max=1e4, digits=2))()

    def _vu(self):
        return self.m1[self.m1.index + pd.Timedelta(minutes=1) <= self.h()]

    def _px(self):
        t = self.h().floor("min")
        return float(self.m1.open.get(t, self._vu().close.iloc[-1]))

    def barres(self, tf="M1", n=30_000):
        return self._vu().iloc[-n:]

    def tick_frais(self, max_age_s=120):
        v = self._vu()
        return len(v) > 0 and (self.h() - v.index[-1]).total_seconds() < max_age_s + 60

    def spread(self):
        return 1.0

    def compte_info(self):
        neuf = self.bascule is not None and self.h() >= self.bascule
        return dict(login=222 if neuf else 111, serveur="FTMO-Demo", balance=10_000.0, equity=10_000.0, trade_ok=True)

    def controle_heure(self):
        return ""

    def lots(self, risque_pct, nominal, dist, spread):
        return float(np.floor(risque_pct / 100 * nominal / (dist + spread) / 0.01) * 0.01)

    def ouvre(self, side, volume, dist_sl, dist_tp, comment):
        px, k = self._px(), next(self.n)
        self.pos[k] = dict(side=side, vol=volume, px=px, sl=px - side * dist_sl, tp=px + side * dist_tp,
                           t=self.h(), vu=self.h().floor("min"))
        return type("F", (), dict(ticket=k, price=px, volume=volume, bid=px, ask=px))()

    def _maj(self):
        for k, p in list(self.pos.items()):
            b = self.m1[(self.m1.index >= p["vu"]) & (self.m1.index + pd.Timedelta(minutes=1) <= self.h())]
            for t, r in b.iterrows():
                s = p["side"]
                if (s > 0 and r.low <= p["sl"]) or (s < 0 and r.high >= p["sl"]):
                    self._clos(k, min(p["sl"], r.open) if s > 0 else max(p["sl"], r.open), "SL")
                    break
                if (s > 0 and r.high >= p["tp"]) or (s < 0 and r.low <= p["tp"]):
                    self._clos(k, p["tp"], "TP")
                    break
            else:
                p["vu"] = self.h().floor("min")

    def _clos(self, k, px, raison):
        p = self.pos.pop(k)
        self.fermes[k] = dict(profit=p["side"] * (px - p["px"]) * p["vol"] - p["vol"] * 1.0, exit_px=px,
                              exit_time=str(self.h()), raison=raison)

    def position(self, ticket):
        self._maj()
        return self.pos.get(ticket)

    def ferme(self, ticket, comment=""):
        self._clos(ticket, self._px(), "heure")
        return True

    def bilan(self, ticket):
        return self.fermes.get(ticket)


def rejoue(book, tmp_path, a="2026-07-26", z="2026-08-28", signe=1, bascule=None, annonces="live/annonces.csv",
           phase=None):
    m = pd.read_parquet(NQ)
    m = m[~m.index.duplicated()].sort_index()
    m1 = m[(m.index >= "2026-06-01") & (m.index < "2026-08-29")].tz_convert(NY)
    clock = {"t": pd.Timestamp(a, tz=NY)}
    cfg = dict(book=book, dossier=str(tmp_path / book), mom_signe=signe, annonces=annonces)
    if phase is not None:  # compte virtuel déjà dans cette phase au départ
        from live.compte import CompteVirtuel
        (tmp_path / book).mkdir(parents=True, exist_ok=True)
        CompteVirtuel(nom=f"book {book}", phase=phase).save(tmp_path / book / "compte.json")
    bot = Bot(cfg, horloge=lambda: clock["t"])
    bot.b = FauxMT5(m1, lambda: clock["t"], bascule)
    for minute in pd.date_range(pd.Timestamp(a, tz=NY), pd.Timestamp(z + " 17:00", tz=NY), freq="1min"):
        for sec in (1, 57):
            clock["t"] = minute + pd.Timedelta(seconds=sec)
            bot.pas()
            if sec == 1 and minute.minute == 0:
                bot.controle_compte()
    return pd.read_csv(tmp_path / book / "trades.csv")


def test_book_B_egal_backtest(tmp_path):
    t = rejoue("B", tmp_path)
    ref = pd.read_csv("results/propfirm_combo/trades_tp2.csv", parse_dates=["date"])
    ref = ref[(ref.date >= "2026-07-27") & (ref.date <= "2026-08-28")]
    # backtest : M2 seulement si 3n n'a pas tradé ou est sorti à 03:00
    n3 = ref[ref.strat == "3n"].set_index("date")
    garde = [s == "3n" or d not in n3.index or (-0.999 < n3.R_brut[d] < 1.999) for d, s in zip(ref.date, ref.strat)]
    ref = ref[garde]
    got = set(zip(pd.to_datetime(t.seance), t.strat, t.side))
    exp = set(zip(ref.date, ref.strat, ref.side))
    assert got == exp
    for _, r in t.iterrows():
        x = ref[(ref.date == pd.Timestamp(r.seance)) & (ref.strat == r.strat)].iloc[0]
        assert r.dist == pytest.approx(x.dist, rel=1e-9)


def test_book_B_anti_hedging(tmp_path):
    """mom short (book A) : aucun 3n long, et M2 trade chaque fois qu'il a un signal (pas de 3n ce jour-là)."""
    t = rejoue("B", tmp_path, signe=-1)
    ref = pd.read_csv("results/propfirm_combo/trades_tp2.csv", parse_dates=["date"])
    ref = ref[(ref.date >= "2026-07-27") & (ref.date <= "2026-08-28") & (ref.strat == "M2")]
    assert (t.strat != "3n").all()
    assert set(zip(pd.to_datetime(t.seance), t.strat, t.side)) == set(zip(ref.date, ref.strat, ref.side))


def test_book_A_entre_chaque_nuit(tmp_path):
    t = rejoue("A", tmp_path, a="2026-08-02")
    ref = pd.read_parquet("cache/propfirm/nq_nuit_tp4_mfe.parquet")
    ref = ref[(pd.to_datetime(ref.night) >= "2026-08-03") & (pd.to_datetime(ref.night) <= "2026-08-28")]
    # nuits sans trade attendues : éval virtuelle perdue en début de journée (risque possible < 0,05 %), comme Compte
    import json
    ev = json.loads((tmp_path / "A" / "compte.json").read_text(encoding="utf-8"))["events"]
    perdus = {pd.Timestamp(e[:10]) for e in ev if "perdu" in e}
    perdus -= set(pd.to_datetime(t.seance))
    assert set(pd.to_datetime(t.seance)) == set(pd.to_datetime(ref.night)) - perdus
    ref = ref[~pd.to_datetime(ref.night).isin(perdus)]
    assert (t.side == 1).all() and (ref.dir == 1).all()
    # stop mom : 2 ATR M15 / prix, sur la série NON ajustée ici (le backtest est sur la série ajustée : écart < 1 %)
    s_bot = (t.dist / t.px_signal).values
    s_ref = ref.sort_values("night").risk.values
    assert np.allclose(s_bot, s_ref, rtol=0.01)


def test_suivi_pnl_additionne_les_essais(tmp_path):
    """Changement d'essai FTMO le samedi 15/08 : le bot le détecte, le P&L cumulé et le compte virtuel continuent,
    et live/pnl.py additionne les deux essais comme un seul compte."""
    from live import pnl
    t = rejoue("B", tmp_path, bascule=pd.Timestamp("2026-08-15 12:00", tz=NY))
    assert set(t.compte_mt5.astype(str)) == {"111", "222"}
    log = (tmp_path / "B" / "bot.log").read_text(encoding="utf-8")
    assert "NOUVEL ESSAI MT5 détecté : 222" in log
    etat = __import__("json").loads((tmp_path / "B" / "etat.json").read_text(encoding="utf-8"))
    assert etat["cumul"]["profit"] == pytest.approx(t.profit.sum()) and etat["cumul"]["trades"] == len(t)
    r = pnl.rapport(tmp_path)
    assert f"{t.profit.sum():+,.2f} $" in r and "| 111 |" in r and "| 222 |" in r
    assert (tmp_path / "pnl.md").exists()  # régénéré par le bot après chaque trade
    # le compte virtuel n'a pas été remis à zéro par le changement d'essai
    c = __import__("json").loads((tmp_path / "B" / "compte.json").read_text(encoding="utf-8"))
    assert c["P"] == pytest.approx(t.P_apres.iloc[-1])


def test_book_A_finance_sort_avant_les_annonces(tmp_path):
    """Compte virtuel financé, annonce 8:30 (NFP fictif) le jeudi 13/08, nuit qui serait allée jusqu'à 9:29:57 :
    elle est fermée à 8:18:55 ET, hors de la fenêtre FTMO interdite (8:28 → 8:32) ; les autres nuits sortent à 9:29:57."""
    cal = tmp_path / "annonces.csv"
    cal.write_text("date,annonce,heure,source\n2026-08-13,NFP,08:30,test\n", encoding="utf-8")
    t = rejoue("A", tmp_path, a="2026-08-02", z="2026-08-14", annonces=str(cal), phase="financé")
    t["s"] = t.seance.astype(str).str[:10]
    prevue = pd.to_datetime(t.sortie).dt.strftime("%H:%M:%S")
    assert (prevue[t.s == "2026-08-13"] == "08:18:55").all() and (prevue[t.s != "2026-08-13"] == "09:29:55").sum() == 0
    assert (prevue[t.s != "2026-08-13"] == "09:29:57").all()
    x = t[t.s == "2026-08-13"].iloc[0]
    fin = pd.Timestamp(x.exit_time).tz_convert(NY)
    assert x.raison == "heure" and pd.Timestamp("2026-08-13 08:18:55", tz=NY) <= fin < pd.Timestamp("2026-08-13 08:28", tz=NY)
    assert (t.risque == 1.0).all()
