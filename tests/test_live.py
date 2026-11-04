"""Le bot de démo (live/) doit refaire exactement le backtest :
  - signaux 3n et M2 calculés sur des barres NQ TRONQUÉES à l'instant de la décision = signaux du backtest
    (run_nq_nuit_3n_vbt.nuits, run_nq_ema930_vbt.seances) sur les mêmes barres ;
  - signe du momentum 12-1 = recolte1.rules.next_month_sign ;
  - compte FTMO virtuel pas à pas (live/compte.py) = run_ftmo_deux_comptes.Compte (calendaire, cible + attente).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from live import signals as S
from live.compte import CompteVirtuel, TP_R

NQ = Path("D:/quant-data/Cotations/indices/NQ_v0_1m.parquet")
NY = "America/New_York"
donnees = pytest.mark.skipif(not NQ.exists(), reason="données NQ absentes")


@pytest.fixture(scope="module")
def m1() -> pd.DataFrame:
    m = pd.read_parquet(NQ)
    m = m[~m.index.duplicated()].sort_index()
    m = m[(m.index >= "2026-05-01") & (m.index < "2026-08-29")]
    return m.tz_convert(NY)


@donnees
def test_3n_tronque_egal_backtest(m1):
    import run_nq_nuit_3n_vbt as B
    b5, b15 = S.resample(m1, "5min"), S.resample(m1, "15min")
    b5["session"] = b5.index.tz_localize(None).normalize() + pd.to_timedelta((b5.index.hour >= 18).astype(int), unit="D")
    n = B.nuits(b5, b15).dropna(subset=["r3_bps"]).tail(40)
    for _, r in n.iterrows():
        cut = m1[m1.index < r.entry_time]  # en direct à 20:05:01 : barres 1 min terminées jusqu'à 20:04
        sig, r3 = S.signal_3n(cut, r.session)
        assert sig == bool(r.sig3n) and r3 == pytest.approx(r.r3_bps, abs=1e-9), r.session
        assert 2 * S.atr15_fin(cut, r.entry_time) == pytest.approx(r.dist, rel=1e-12)


@donnees
def test_m2_tronque_egal_backtest(m1):
    import run_nq_ema930_vbt as E
    b5, b15 = S.resample(m1, "5min"), S.resample(m1, "15min")
    d = E.seances(b5, b15).tail(40)
    for _, r in d.iterrows():
        cut = m1[m1.index < r.entry_time]  # à 9:35:01 : barres terminées jusqu'à 9:34
        s = S.signal_m2(cut, pd.Timestamp(r.date))
        assert s["side"] == r.side and s["m2"] == bool(r.m2), r.date
        assert s["strength"] == pytest.approx(r.strength, rel=1e-12)
        if np.isfinite(r.reversal):
            assert s["reversal"] == pytest.approx(r.reversal, rel=1e-9)
        assert s["atr15"] == pytest.approx(r.atr15, rel=1e-12)


def test_mom_signe_egal_regle():
    import recolte1.rules as rules
    try:
        bb = rules.base("NQ")
    except Exception as e:  # données du moteur absentes
        pytest.skip(str(e))
    ref = rules.next_month_sign(bb, rules.monthly(bb, "cc").shift(1).rolling(11, min_periods=11).sum())
    close = bb.p_close
    jours = ref.index[ref.index >= bb.index[0] + pd.DateOffset(months=15)]  # 13 mois complets avant
    jours = jours[jours.to_period("M").duplicated() == False]  # une séance par mois
    for d in jours[::3]:
        if np.isnan(ref[d]):
            continue
        s, _ = S.mom_signe(close[close.index < d], d)
        assert s == ref[d], d


def _legs_aleatoires(rng, n):
    """Jours synthétiques : (R brut, coût c, MFE) pour 3n, M2 et mom, comme les tuples de run_ftmo_deux_comptes."""
    jours = []
    d = pd.Timestamp("2015-01-02")
    for _ in range(n):
        d += pd.Timedelta(days=int(rng.choice([1, 1, 1, 3])))
        row = {}
        for s, p in (("mom", 1.0), ("3n", 0.45), ("M2", 0.3)):
            if rng.random() < p:
                u = rng.random()
                R = -1.0 if u < 0.45 else (TP_R if u < 0.75 else float(rng.uniform(-0.9, 1.9)))
                mfe = max(R, 0) + float(rng.uniform(0, 1.5)) if R < TP_R else TP_R
                c = float(rng.uniform(0.01, 0.06))
                row[s] = (R, c, mfe, R, mfe)
        jours.append((d, row))
    return jours


def _rejoue_live(jours, book):
    """Le compte virtuel piloté comme dans live/bot.py, jambe par jambe."""
    C = CompteVirtuel(nom=book)
    for d, row in jours:
        C.debut_jour(d)
        if C.echec_si_bloque():
            continue
        base = C.risque_base()
        legs = []
        if book == "A":
            if "mom" in row:
                legs = [("mom", base)]
        else:
            legs = [("3n", base)] if "3n" in row else []
        x, stop_m2 = 0.0, False
        for strat, risque in legs + ([("M2", None)] if book == "B" and "M2" in row else []):
            if strat == "M2":
                if stop_m2 or C.mort_jour:
                    break
                risque = max(0.0, min(base + x, (2 * base - x) / 2))
                if risque <= 0:
                    break
            R, c, mfe = row[strat][:3]
            plan = C.plan_jambe(risque, c)
            if strat == "3n":  # comme jambes_B : x et la décision M2 viennent du R brut, objectif non réduit
                stop_m2 = not (-0.999 < R < TP_R - 1e-3)
                x = base * (R - c) / (1 + c)
            if plan is None:
                continue
            r, obj = plan
            Rf = obj if (obj < TP_R and mfe >= obj) else R
            C.enregistre(r * (Rf - c) / (1 + c))
        C.fin_jour()
    return C


@pytest.mark.parametrize("graine", [1, 2, 3, 4, 5])
def test_compte_virtuel_egal_moteur(graine):
    import run_ftmo_deux_comptes as M
    jours = _legs_aleatoires(np.random.default_rng(graine), 900)
    for book, jambes in (("A", M.jambes_A), ("B", M.jambes_B)):
        ref = M.Compte(book, calendaire=True, annonces=True, politique="cible+attente")
        for d, row in jours:
            ref.jour(d, jambes(row))
        live = _rejoue_live(jours, book)
        assert live.evals == ref.evals, book
        assert live.rewards == ref.rewards, book
        assert live.P == pytest.approx(ref.P, abs=1e-9), book
        assert live.phase == ref.phase, book
        assert live.rewards_pct / 100 * ref.size == pytest.approx(ref.cash + ref.evals * ref.fee, abs=1e-6), book


def test_drapeau_de_mise_a_jour_arrete_le_bot_proprement(tmp_path):
    """live/maj_auto.ps1 pose live/etat/redemarrer_<book> : le bot sauve son état et sort (code 0) avant tout pas."""
    from live.bot import Bot

    class Stub:
        def controle_heure(self):
            return ""

    bot = Bot(dict(book="A", dossier=str(tmp_path / "A"), annonces="live/annonces.csv"), broker=Stub(),
              horloge=lambda: pd.Timestamp("2026-11-04 12:00", tz=NY))
    bot.pas = lambda: (_ for _ in ()).throw(AssertionError("le bot a fait un pas malgré le drapeau"))
    bot.drapeau.touch()  # drapeau ancien : effacé au démarrage, ne doit pas faire sortir
    bot.etat["ouverts"] = [{"strat": "mom", "ticket": 1}]
    import threading
    t = threading.Timer(0.5, bot.drapeau.touch)
    t.start()
    with pytest.raises(SystemExit) as e:
        bot.pas = lambda: None
        bot.boucle()
    t.cancel()
    assert e.value.code == 0 and not bot.drapeau.exists()
    assert "ticket" in (tmp_path / "A" / "etat.json").read_text(encoding="utf-8")
