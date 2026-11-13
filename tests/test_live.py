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


def test_reinitialisation_archive_et_repart_de_zero(tmp_path, monkeypatch):
    """live/reinit.py pose reinitialiser_<book> : au démarrage, le bot archive son dossier et repart d'un compte neuf ;
    refusé si une position est suivie (et le drapeau est effacé dans les deux cas)."""
    from live.bot import Bot
    from live import reinit

    d = tmp_path / "B"
    d.mkdir()
    CompteVirtuel(nom="book B", phase="financé", P=3.913, best=1.9553, f0="2026-11-11").save(d / "compte.json")
    (d / "trades.csv").write_text("strat,profit\nM2,176.97\n", encoding="utf-8")
    (d / "etat.json").write_text('{"ouverts": [{"strat": "3n"}], "faits": [], "jours": {}}', encoding="utf-8")
    cfg = dict(book="B", dossier=str(d), annonces="live/annonces.csv")
    horloge = lambda: pd.Timestamp("2026-11-14 12:00", tz=NY)  # noqa: E731

    # position suivie : le script refuse, et le bot aussi si le drapeau est posé quand même
    monkeypatch.setattr("sys.argv", ["reinit", "B", "--dossier", str(tmp_path)])
    assert reinit.main() == 1 and not (tmp_path / "reinitialiser_B").exists()
    (tmp_path / "reinitialiser_B").touch()
    bot = Bot(cfg, horloge=horloge)
    assert bot.compte.phase == "financé" and not (tmp_path / "reinitialiser_B").exists()
    assert "REFUSÉE" in (d / "bot.log").read_text(encoding="utf-8")

    # sans position : drapeaux posés, puis archive et compte neuf au démarrage
    (d / "etat.json").write_text('{"ouverts": [], "faits": ["M2:2026-11-13"], "jours": {}}', encoding="utf-8")
    assert reinit.main() == 0 and (tmp_path / "reinitialiser_B").exists() and (tmp_path / "redemarrer_B").exists()
    bot = Bot(cfg, horloge=horloge)
    assert (bot.compte.phase, bot.compte.P, bot.compte.evals, bot.compte.f0) == ("éval", 0.0, 1, None)
    assert bot.etat["faits"] == [] and not (d / "trades.csv").exists()
    arch = tmp_path / "archive" / "B_20261114_120000"
    assert (arch / "trades.csv").exists() and "financé" in (arch / "compte.json").read_text(encoding="utf-8")
    assert "RÉINITIALISATION" in (d / "bot.log").read_text(encoding="utf-8")
    assert not (tmp_path / "reinitialiser_B").exists()
    assert "Book B" in (tmp_path / "pnl.md").read_text(encoding="utf-8")


def test_suivi_pnl_deux_essais(tmp_path):
    """live/pnl.py additionne les trades de deux essais MT5 comme un seul compte de 10 000 $ et lit le compte virtuel."""
    from live import pnl
    (tmp_path / "A").mkdir()
    rows = pd.DataFrame(dict(strat="mom", seance=["2026-11-05", "2026-11-06", "2026-11-23"],
                             compte_mt5=[111, 111, 222], profit=[494.9, -250.0, 120.0], R_net=[1.98, -1.0, 0.48],
                             spread=1.45, raison=["TP", "SL", "heure"],
                             exit_time=["2026-11-05 09:00:00-05:00", "2026-11-06 08:00:00-05:00",
                                        "2026-11-23 09:29:57-05:00"]))
    rows.to_csv(tmp_path / "A" / "trades.csv", index=False)
    c = CompteVirtuel(nom="book A", P=3.649, evals=2, rewards=1, rewards_pct=3.0)
    c.save(tmp_path / "A" / "compte.json")
    r = pnl.rapport(tmp_path)
    assert "+364.90 $" in r and "10,364.90 $" in r
    assert "| 111 | 2 | +244.90 |" in r and "| 222 | 1 | +120.00 |" in r
    assert f"{300 - 2 * pnl.FRAIS_EVAL:+,.2f} $" in r  # résultat FTMO virtuel = rewards − 2 évals
    assert "-250.00 $" in r  # plus gros creux du compte continu


def test_journal_trades_nouvelles_colonnes(tmp_path):
    """Un trades.csv écrit par une version plus ancienne du bot reçoit les nouvelles colonnes sans se décaler."""
    from live.bot import Bot
    bot = Bot(dict(book="A", dossier=str(tmp_path / "A"), annonces="live/annonces.csv"), broker=None)
    bot.ecrit("trades.csv", dict(strat="mom", profit=10.0, spread=1.4))
    bot.ecrit("trades.csv", dict(strat="mom", profit=-5.0, spread=1.5, spread_ordre=1.5, spread_sortie=2.5,
                                 glissement=0.2))
    bot.ecrit("trades.csv", dict(strat="mom", profit=3.0, spread=1.5, spread_ordre=1.6, spread_sortie=1.7,
                                 glissement=0.0))
    t = pd.read_csv(tmp_path / "A" / "trades.csv")
    assert list(t.profit) == [10.0, -5.0, 3.0] and np.isnan(t.spread_sortie[0]) and t.spread_sortie[1] == 2.5


class _StubMT5:
    """Terminal minimal : barres M1 jusqu'à `fin`, drapeau de trading réglable."""

    def __init__(self, fin, trade_ok=True):
        idx = pd.date_range(end=fin, periods=200, freq="1min")
        self.m1 = pd.DataFrame(dict(open=1.0, high=1.0, low=1.0, close=1.0), index=idx)
        self.trade_ok = trade_ok

    def barres(self, tf="M1", n=30_000):
        return self.m1

    def compte_info(self):
        return dict(login=1, serveur="FTMO-Demo", balance=1e4, equity=1e4, trade_ok=self.trade_ok)


def _bot(tmp_path, t, broker):
    from live.bot import Bot
    clock = {"t": pd.Timestamp(t, tz=NY)}
    b = Bot(dict(book="B", dossier=str(tmp_path / "B"), annonces="live/annonces.csv"), broker=broker,
            horloge=lambda: clock["t"])
    return b, clock


def test_barres_m1_perimees_refusees(tmp_path, monkeypatch):
    """Vu sur le VPS le 2026-11-04 : terminal B servant des barres arrêtées à 13:57 à 20:05 → aucun trade."""
    import live.bot as LB
    monkeypatch.setattr(LB.time, "sleep", lambda s: None)
    bot, _ = _bot(tmp_path, "2026-11-04 20:05:01", _StubMT5(pd.Timestamp("2026-11-04 13:57", tz=NY)))
    assert bot.m1_frais() is None
    assert "EN RETARD" in (tmp_path / "B" / "bot.log").read_text(encoding="utf-8")
    bot2, _ = _bot(tmp_path, "2026-11-04 20:05:01", _StubMT5(pd.Timestamp("2026-11-04 20:04", tz=NY)))
    assert bot2.m1_frais() is not None


def test_pas_de_fausse_alerte_pendant_la_pause_du_serveur(tmp_path):
    """Drapeaux de trading coupés de 17:00 à 17:10 ET (pause quotidienne) : pas d'alerte ; coupés 5 min à 11:00 : alerte,
    puis « de nouveau autorisé » quand ils reviennent."""
    st = _StubMT5(pd.Timestamp("2026-11-05 17:00", tz=NY), trade_ok=False)
    bot, clock = _bot(tmp_path, "2026-11-05 17:00:30", st)
    for m in range(10):
        clock["t"] = pd.Timestamp("2026-11-05 17:00:30", tz=NY) + pd.Timedelta(minutes=m)
        bot.controle_compte()
    log = tmp_path / "B" / "bot.log"
    assert not log.exists() or "DÉSACTIVÉ" not in log.read_text(encoding="utf-8")
    for m in range(5):
        clock["t"] = pd.Timestamp("2026-11-06 11:00", tz=NY) + pd.Timedelta(minutes=m)
        bot.controle_compte()
    assert "DÉSACTIVÉ" in log.read_text(encoding="utf-8")
    st.trade_ok = True
    bot.controle_compte()
    assert "de nouveau autorisé" in log.read_text(encoding="utf-8")
