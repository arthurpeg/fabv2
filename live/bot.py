"""Bot de démo FTMO : book A (mom) ou book B (3n + M2) sur US100.cash, via MetaTrader 5. Un processus par book.

uv run python -m live.bot --config live/config_A.toml             → tourne en continu
uv run python -m live.bot --config live/config_A.toml --signaux   → calcule les signaux du moment, sans ordre, et sort
uv run python -m live.bot --config live/config_A.toml --test-ordre → ordre test au lot minimum, fermé après 5 s

Règles (plan retenu le 2026-11-04, wiki/experiments/propfirm-ftmo-option.md, section « Plan retenu ») :
  A  mom : 20:00 ET, sens = signe du momentum 12-1 du mois de la séance, SL 2 ATR M15, TP 4 ATR (2 R) ou objectif
     réduit, sortie 9:30 ; en financé (virtuel), sortie à 8:19 les jours NFP / CPI / PIB avancé.
  B  3n : long 20:05 → 03:00 si la somme des 3 nuits précédentes ≤ 0, SL 2 ATR M15, TP 4 ATR ;
     M2 : 9:35 → 16:00 si 3n n'a pas tradé ou est sorti à 03:00, SL 4 ATR M15, TP 8 ATR, taille
     ρ = min(r + x, (2r − x)/2) ; en financé (virtuel), sortie à 13:55 les jours de Fed.
  Gestion : compte FTMO virtuel (live/compte.py) : éval 2,5 %, financé 1 %, objectif réduit au reste à faire,
  cible + attente, reward au 14e jour. Tailles calculées sur le nominal (10 000 $), pas sur le solde de l'essai.

Écarts connus avec le backtest (à mesurer avec le journal) : prix CFD US100.cash au lieu du future NQ (momentum
calculé sur le CFD, non ajusté du portage ; spread réel au lieu de 1,5 pt) ; jours écourtés : M2 sort à la clôture
XNYS (13:00) au lieu de la dernière barre NQ ; 3n sorti sur un objectif réduit en éval compte comme « TP » (pas de M2).
Journal : <dossier>/trades.csv (une ligne par trade), signaux.csv (une ligne par signal calculé), bot.log, compte.json.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import time
import tomllib
import traceback
from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd

from live import signals as S
from live.compte import CompteVirtuel

NY = "America/New_York"
FENETRE_ENTREE = pd.Timedelta(minutes=5)


def hms(d, h: int, m: int, s: int = 0) -> pd.Timestamp:
    return pd.Timestamp(f"{pd.Timestamp(d):%Y-%m-%d} {h:02d}:{m:02d}:{s:02d}", tz=NY)


class Bot:
    def __init__(self, cfg: dict, broker=None, horloge=None):
        self.cfg = cfg
        self.maintenant = horloge or (lambda: pd.Timestamp.now(tz=NY))
        self.book = cfg["book"]  # "A" ou "B"
        self.nominal = float(cfg.get("nominal", 10_000))
        self.dir = Path(cfg.get("dossier", f"live/etat/{self.book}"))
        self.dir.mkdir(parents=True, exist_ok=True)
        self.b = broker
        self._reinit_msg = self.reinitialise_si_demande()
        self.compte = CompteVirtuel.load(self.dir / "compte.json", f"book {self.book}")
        p = self.dir / "etat.json"
        self.etat = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"ouverts": [], "faits": [], "jours": {}}
        self.cal = xc.get_calendar("XNYS")
        a = pd.read_csv(cfg.get("annonces", "live/annonces.csv"), parse_dates=["date"])
        self.annonces = a
        self.matin = {f"{d:%Y-%m-%d}" for d in a.date[a.annonce.isin(["NFP", "CPI", "PIB avancé"])]}
        self.fed = {f"{d:%Y-%m-%d}" for d in a.date[a.annonce.isin(["FOMC décision", "FOMC minutes"])]}
        self._n_events = len(self.compte.events)
        self.bascule_bloquee = False
        if self._reinit_msg:
            self.log(self._reinit_msg)

    def reinitialise_si_demande(self) -> str:
        """Drapeau live/etat/reinitialiser_<book> (posé par live/reinit.py) : au démarrage, le dossier du book est
        déplacé dans live/etat/archive/<book>_<horodatage>/ et le bot repart d'un compte virtuel neuf (éval n° 1, P = 0,
        aucun trade, aucun essai connu). Refusé si une position est suivie. Le drapeau est effacé dans les deux cas."""
        drap = self.dir.parent / f"reinitialiser_{self.book}"
        if not drap.exists():
            return ""
        reel = drap.read_text(encoding="utf-8").strip() == "reel"
        drap.unlink(missing_ok=True)
        p = self.dir / "etat.json"
        ouverts = json.loads(p.read_text(encoding="utf-8")).get("ouverts", []) if p.exists() else []
        if ouverts:
            return (f"!! RÉINITIALISATION REFUSÉE : {len(ouverts)} position(s) suivie(s) "
                    f"({', '.join(str(o.get('strat')) for o in ouverts)}). Relancer live/reinit.py sans position ouverte")
        if not any(self.dir.iterdir()):
            return "réinitialisation demandée : dossier déjà vide, compte virtuel neuf"
        arch = self.dir.parent / "archive" / f"{self.book}_{self.maintenant():%Y%m%d_%H%M%S}"
        arch.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(self.dir), str(arch))
        self.dir.mkdir(parents=True, exist_ok=True)
        if reel:  # marque du mode réel : la bascule ne se refera plus, alerte d'objectif à +10 %
            (self.dir / "etat.json").write_text(json.dumps(
                {"ouverts": [], "faits": [], "jours": {}, "reel": f"{self.maintenant():%Y-%m-%d %H:%M}"}),
                encoding="utf-8")
        self.rapport()
        return (f"RÉINITIALISATION{' (compte réel)' if reel else ''} : ancien état archivé dans {arch} ; "
                f"compte virtuel neuf (éval n° 1, +0,00 %)")

    def bascule_armee(self) -> bool:
        p = Path(self.cfg.get("bascule", "live/bascule.toml"))
        try:
            return bool(tomllib.loads(p.read_text(encoding="utf-8")).get("arme", False))
        except Exception:
            return False

    # ------------------------------------------------------------------ outils
    def log(self, s: str) -> None:
        line = f"{self.maintenant():%Y-%m-%d %H:%M:%S} ET [{self.book}] {s}"
        print(line, flush=True)
        with open(self.dir / "bot.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def save(self) -> None:
        self.compte.save(self.dir / "compte.json")
        (self.dir / "etat.json").write_text(json.dumps(self.etat, ensure_ascii=False, indent=1, default=str),
                                            encoding="utf-8")
        for e in self.compte.events[self._n_events:]:
            self.log(f"COMPTE VIRTUEL : {e}")
        self._n_events = len(self.compte.events)

    def ecrit(self, nom: str, row: dict) -> None:
        p = self.dir / nom
        if p.exists():  # nouvelles colonnes (mise à jour du bot) : réécrit le fichier avec l'union des colonnes
            with open(p, encoding="utf-8") as f:
                tete = f.readline().strip().split(",")
            if tete != list(row):
                old = pd.read_csv(p)
                pd.concat([old, pd.DataFrame([row])], ignore_index=True).to_csv(p, index=False)
                return
        neuf = not p.exists()
        with open(p, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(row))
            if neuf:
                w.writeheader()
            w.writerow(row)

    def fait(self, cle: str) -> bool:
        return cle in self.etat["faits"]

    def marque(self, cle: str) -> None:
        self.etat["faits"] = (self.etat["faits"] + [cle])[-500:]
        self.save()

    def jour(self, seance: str) -> dict:
        return self.etat["jours"].setdefault(seance, {})

    def est_seance(self, d) -> bool:
        return self.cal.is_session(pd.Timestamp(d).tz_localize(None).normalize())

    def prochaine_seance(self, d) -> pd.Timestamp:
        """Première séance XNYS strictement après la date d."""
        return self.cal.date_to_session(pd.Timestamp(d).tz_localize(None).normalize() + pd.Timedelta(days=1), "next")

    def cloture(self, d) -> pd.Timestamp:
        return self.cal.session_close(pd.Timestamp(d).tz_localize(None).normalize()).tz_convert(NY)

    def controle_annonces(self) -> None:
        today = self.maintenant().tz_localize(None).normalize()
        for typ in ("NFP", "CPI", "FOMC décision"):
            z = self.annonces.date[self.annonces.annonce == typ].max()
            if pd.isna(z) or z < today + pd.Timedelta(days=35):
                self.log(f"!! calendrier des annonces : plus de {typ} après {z:%Y-%m-%d} : compléter live/annonces.csv")

    def spread_a(self, t: str) -> float:
        """Spread (prix) de la barre M1 de l'instant t, d'après MT5 ; spread actuel si la barre n'est pas finie."""
        try:
            f = getattr(self.b, "spread_au", None)
            v = f(t) if f else None
            if v is not None and np.isfinite(v):
                return float(v)
            b = self.b.barres("M1", 600)
            k = pd.Timestamp(t).tz_convert(NY).floor("min")
            if "spread" in b and k in b.index:
                return float(b.spread[k]) * float(self.b.info.point)
            return float(self.b.spread())
        except Exception:
            return float("nan")

    def m1_frais(self, strict: bool = True, essais: int = 15) -> pd.DataFrame | None:
        """Barres M1 jusqu'à la minute précédente. Le terminal peut servir un historique en retard (vu le 2026-11-04 sur
        le terminal B : dernière barre 13:57 à 20:05) : on réessaie, puis on refuse de trader sur des données périmées."""
        for i in range(essais):
            m1 = self.b.barres("M1", 30_000)
            retard = (self.maintenant() - (m1.index[-1] + pd.Timedelta(minutes=1))).total_seconds()
            if retard <= 90:
                if i:
                    self.log(f"barres M1 à jour après {i} nouvel(s) essai(s)")
                return m1
            time.sleep(1)
        self.log(f"!! barres M1 EN RETARD : dernière barre {m1.index[-1]:%Y-%m-%d %H:%M} ET ({retard / 60:.0f} min) ; "
                 f"{'PAS DE TRADE' if strict else 'résultat indicatif'}. Ouvrir un graphique M1 de US100.cash dans ce "
                 f"terminal et le laisser ouvert")
        return None if strict else m1

    def compte_mt5(self) -> dict:
        f = getattr(self.b, "compte_info", None)
        try:
            return f() if f else {}
        except Exception:
            return {}

    def controle_compte(self) -> None:
        """Nouvel essai FTMO détecté, trading bloqué par FTMO, objectif de l'essai atteint : alerte une fois par cas."""
        c = self.compte_mt5()
        if not c:
            return
        comptes = self.etat.setdefault("comptes", {})
        k = str(c["login"])
        if k not in comptes and comptes and self.bascule_armee() and not self.etat.get("reel"):
            # 1er vrai compte FTMO connecté : remise à zéro par le chemin éprouvé (drapeaux + relance par lancer.bat)
            if self.etat["ouverts"]:
                if not self.bascule_bloquee:
                    self.log(f"!! BASCULE EN ATTENTE : nouveau compte {k} détecté mais {len(self.etat['ouverts'])} "
                             f"position(s) suivie(s) sur l'ancien. Aucun nouveau trade d'ici la bascule")
                self.bascule_bloquee = True
                return
            self.log(f"BASCULE VERS LE COMPTE RÉEL {k} ({c.get('serveur', '?')}, solde {c['balance']:,.2f} $) : "
                     f"archivage de la démo et compte virtuel neuf ; relance du bot")
            (self.dir.parent / f"reinitialiser_{self.book}").write_text("reel", encoding="utf-8")
            self.bascule_bloquee = True
            self.drapeau.touch()
            return
        if k not in comptes:
            if comptes:
                self.log(f"NOUVEL ESSAI MT5 détecté : {k} (solde {c['balance']:,.2f} $). Le P&L cumulé et le compte "
                         f"virtuel continuent : on additionne comme si c'était le même compte")
            comptes[k] = dict(debut=f"{self.maintenant():%Y-%m-%d %H:%M}", solde_initial=c["balance"], alertes=[])
            self.save()
        e = comptes[k]
        gain = (c["equity"] / e["solde_initial"] - 1) * 100 if e["solde_initial"] else 0.0

        def alerte(cle, msg):
            if cle not in e["alertes"]:
                e["alertes"].append(cle)
                self.log(msg)
                self.save()

        # pause quotidienne du serveur (vers 17:00 ET) : drapeaux de trading coupés quelques minutes, sans conséquence
        # (fausse alerte du 2026-11-04 à 17:01). Alerte seulement après 5 contrôles d'affilée (≈ 5 min) hors pause.
        h = self.maintenant()
        pause = hms(h, 16, 55) <= h <= hms(h, 18, 15)
        if c["trade_ok"]:
            e["ko"] = 0
            if "bloque" in e["alertes"]:
                e["alertes"].remove("bloque")
                self.log(f"trading de nouveau autorisé sur l'essai {k}")
                self.save()
        elif not pause:
            e["ko"] = e.get("ko", 0) + 1
            if e["ko"] >= 5:
                alerte("bloque", f"!! TRADING DÉSACTIVÉ sur l'essai {k} depuis {e['ko']} min (objectif de l'essai "
                                 f"atteint, perte max ou essai expiré) : créer un nouvel essai FTMO et s'y connecter")
        if gain >= float(self.cfg.get("objectif_essai_pct", 10.0 if self.etat.get("reel") else 5.0)):
            alerte("objectif", f"objectif de l'essai atteint sur {k} ({gain:+.2f} %). Sans effet sur le plan : le "
                               f"compte virtuel garde l'objectif réel de +10 %. Si FTMO bloque l'essai, en créer un neuf")
        if gain <= -8.0:
            alerte("perte", f"!! essai {k} à {gain:+.2f} % : proche de sa perte max (10 %), prévoir un nouvel essai")

    def rapport(self) -> None:
        try:
            from live import pnl
            pnl.ecrit_rapport(self.dir.parent)
        except Exception:
            self.log("rapport P&L non écrit :\n" + traceback.format_exc())

    # ------------------------------------------------------------------ signal mom
    def close_1600(self) -> pd.Series:
        h1 = self.b.barres("H1", 12_000)
        a, z = h1.index[0].tz_localize(None).normalize(), self.maintenant().tz_localize(None).normalize()
        sch = self.cal.schedule.loc[a:z]
        fin = pd.DatetimeIndex(sch["close"]).tz_convert(NY)
        debut_barre = fin - pd.Timedelta(hours=1)
        px = h1.close.reindex(debut_barre)
        return pd.Series(px.values, index=pd.DatetimeIndex(sch.index))

    def signe_mom(self, seance: pd.Timestamp) -> tuple[int, float, str]:
        force = int(self.cfg.get("mom_signe", 0))
        if force in (-1, 1):
            return force, float("nan"), "forcé par la config"
        mois = f"{seance:%Y-%m}"
        cache = self.etat.setdefault("mom", {})
        if mois in cache:
            return int(cache[mois][0]), float(cache[mois][1]), "cache"
        s, v = S.mom_signe(self.close_1600(), seance)
        src = "H1 16:00"
        if s == 0:
            d1 = self.b.barres("D1", 600)
            d = (d1.index + pd.Timedelta(hours=7)).tz_localize(None).normalize()  # barre D1 serveur → date de séance
            s, v = S.mom_signe(pd.Series(d1.close.values, index=d), seance)
            src = "D1 (historique H1 trop court)"
        if s != 0:
            cache[mois] = [s, v]
        if np.isfinite(v) and abs(v) < 0.05:
            self.log(f"!! momentum 12-1 proche de 0 ({v:+.3f}) : le signe sur le CFD peut différer de celui du NQ ajusté")
        return s, v, src

    # ------------------------------------------------------------------ une jambe
    def jambe(self, strat: str, seance: pd.Timestamp, side: int, dist: float, risque: float, sortie: pd.Timestamp,
              info: dict) -> None:
        c = self.compte
        if self.bascule_bloquee:
            self.log(f"{strat} {seance:%Y-%m-%d} : pas de trade (bascule vers le compte réel en cours)")
            return
        spread = self.b.spread()
        plan = c.plan_jambe(risque, spread / dist)
        if plan is None:
            raison = "attente du reward" if c.en_attente() else "journée bloquée ou risque < 0,05 %"
            self.log(f"{strat} {seance:%Y-%m-%d} : pas de trade ({raison})")
            return
        r, obj = plan
        vol = self.b.lots(r, self.nominal, dist, spread)
        if vol <= 0:
            self.log(f"{strat} : taille sous le lot minimum (risque {r:.2f} %, distance {dist:.1f} pts)")
            return
        fill = self.b.ouvre(side, vol, dist, obj * dist, f"{strat} {seance:%m%d}")
        o = dict(strat=strat, seance=f"{seance:%Y-%m-%d}", ticket=fill.ticket, side=side, phase=c.phase,
                 heure_entree=f"{self.maintenant():%Y-%m-%d %H:%M:%S}", entry_px=fill.price, bid=fill.bid,
                 ask=fill.ask, spread=spread, dist=dist, risque=r, objectif_R=obj, volume=vol, sortie=str(sortie),
                 spread_ordre=fill.ask - fill.bid,
                 glissement=side * (fill.price - (fill.ask if side > 0 else fill.bid)),
                 px_signal=info.pop("px_signal", np.nan), compte_mt5=self.compte_mt5().get("login", ""),
                 info=json.dumps(info, default=float))
        self.etat["ouverts"].append(o)
        self.log(f"OUVERT {strat} {'long' if side > 0 else 'short'} {vol} lots à {fill.price} (bid {fill.bid}, ask "
                 f"{fill.ask}, spread {fill.ask - fill.bid:.2f}, glissement {o['glissement']:+.2f} pts) ; SL {dist:.1f} pts, "
                 f"objectif {obj:.2f} R, risque {r:.2f} % ({c.phase} virtuel), sortie prévue {sortie:%d/%m %H:%M:%S}")
        self.save()

    def suivi(self, now: pd.Timestamp) -> None:
        for o in list(self.etat["ouverts"]):
            pos = self.b.position(o["ticket"])
            if pos is not None:
                if now >= pd.Timestamp(o["sortie"]):
                    o["spread_sortie"] = self.b.spread()
                    self.log(f"sortie à l'heure : {o['strat']} ticket {o['ticket']} (spread {o['spread_sortie']:.2f})")
                    self.b.ferme(o["ticket"])
                continue
            bil = self.b.bilan(o["ticket"])
            if bil is None:
                login = self.compte_mt5().get("login")
                if login and o.get("compte_mt5") and login != o["compte_mt5"] and not o.get("alerte_compte"):
                    o["alerte_compte"] = True
                    self.log(f"!! position {o['strat']} {o['ticket']} ouverte sur l'ancien essai {o['compte_mt5']} : "
                             f"introuvable sur {login}. Se reconnecter à l'ancien essai jusqu'à sa clôture, puis "
                             f"revenir au nouveau (changer d'essai sans position ouverte)")
                    self.save()
                continue
            if bil["raison"] != "heure" or "spread_sortie" not in o:
                o["spread_sortie"] = self.spread_a(bil["exit_time"])
            pnl = bil["profit"] / self.nominal * 100
            R = bil["profit"] / (o["volume"] * self.b.vpp * o["dist"])
            self.compte.debut_jour(pd.Timestamp(o["seance"]))
            self.compte.enregistre(pnl)
            if o["strat"] == "3n":
                self.jour(o["seance"])["n3"] = dict(raison=bil["raison"], pnl=pnl)
            self.ecrit("trades.csv", {**o, **bil, "pnl_pct": pnl, "R_net": R,
                                      "P_apres": self.compte.P, "phase_apres": self.compte.phase})
            self.etat["ouverts"].remove(o)
            cum = self.etat.setdefault("cumul", {"profit": 0.0, "trades": 0})
            cum["profit"] += bil["profit"]
            cum["trades"] += 1
            self.log(f"FERMÉ {o['strat']} ({bil['raison']}) à {bil['exit_px']} : {bil['profit']:+.2f} $ "
                     f"({pnl:+.2f} %, {R:+.2f} R) ; compte virtuel {self.compte.phase} {self.compte.P:+.2f} % ; "
                     f"P&L cumulé tous essais {cum['profit']:+,.2f} $ sur {cum['trades']} trades "
                     f"(compte continu {self.nominal + cum['profit']:,.2f} $)")
            self.save()
            self.rapport()

    def debut(self, seance: pd.Timestamp) -> float | None:
        """Ouvre la journée FTMO virtuelle ; renvoie le risque de base de la journée (None si compte perdu)."""
        self.compte.debut_jour(seance)
        j = self.jour(f"{seance:%Y-%m-%d}")
        if "base" not in j:
            if self.compte.echec_si_bloque():
                self.save()
                return None
            j["base"] = self.compte.risque_base()
        return j["base"]

    # ------------------------------------------------------------------ événements
    def ev_mom(self, now: pd.Timestamp) -> None:
        t = hms(now, 20, 0, 1)
        if not (t <= now < t + FENETRE_ENTREE):
            return
        seance = self.prochaine_seance(now)
        cle = f"mom:{seance:%Y-%m-%d}"
        if self.fait(cle):
            return
        if any(o["strat"] == "mom" for o in self.etat["ouverts"]):
            self.marque(cle)  # nuit de jour férié : la position de la veille court jusqu'à la même séance
            return
        if not self.b.tick_frais():  # vendredi soir, samedi : on ne marque pas la séance (le dimanche entrera)
            k = f"mom-ferme:{now:%Y-%m-%d}"
            if not self.fait(k):
                self.marque(k)
                self.log(f"mom : marché fermé ce soir à 20:00, pas d'entrée")
            return
        self.marque(cle)
        if self.compte.phase == "financé" and (seance - now.tz_localize(None).normalize()).days > 1:
            # FTMO (FAQ « hold positions overnight or over the weekend », relue le 2026-11-14) : sur le compte financé,
            # pas de position à travers une fermeture de plus de 2 h. Une nuit qui enjambe un jour férié (Thanksgiving,
            # lundis fériés, veille de pont) traverserait la fermeture du férié : pas d'entrée. En éval, c'est permis.
            self.log(f"mom séance {seance:%Y-%m-%d} : la nuit enjambe un jour férié, pas d'entrée en financé "
                     f"(position interdite à travers une fermeture de plus de 2 h)")
            return
        m1 = self.m1_frais()
        if m1 is None:
            return
        t20 = hms(now, 20, 0)
        px = float(m1.close.iloc[-1])
        atr = S.atr15_fin(m1, t20, min_periods=14)
        side, v, src = self.signe_mom(seance)
        self.ecrit("signaux.csv", dict(heure=f"{now:%Y-%m-%d %H:%M:%S}", strat="mom", seance=f"{seance:%Y-%m-%d}",
                                       derniere_barre=str(m1.index[-1]), px=px, atr15=atr, signe=side, mom=v, src=src))
        if side == 0 or not np.isfinite(atr):
            self.log(f"mom : pas de signal (signe {side}, ATR {atr})")
            return
        base = self.debut(seance)
        if base is None:
            return
        sortie = hms(seance, 9, 29, 57)
        if self.compte.phase == "financé" and f"{seance:%Y-%m-%d}" in self.matin:
            sortie = hms(seance, 8, 18, 55)
        self.jambe("mom", seance, side, S.K_SL_NUIT * atr, base, sortie, dict(mom=v, atr15=atr, px_signal=px))

    def ev_3n(self, now: pd.Timestamp) -> None:
        t = hms(now, 20, 5, 1)
        if not (t <= now < t + FENETRE_ENTREE):
            return
        seance = now.tz_localize(None).normalize() + pd.Timedelta(days=1)
        cle = f"3n:{seance:%Y-%m-%d}"
        if self.fait(cle):
            return
        self.marque(cle)
        if not self.b.tick_frais():
            self.log(f"3n {seance:%Y-%m-%d} : marché fermé à 20:05")
            return
        self.compte.debut_jour(seance)  # reward virtuel vérifié chaque jour, même sans signal
        self.save()
        m1 = self.m1_frais()
        if m1 is None:
            return
        sig, r3 = S.signal_3n(m1, seance)
        atr = S.atr15_fin(m1, hms(now, 20, 5))
        self.ecrit("signaux.csv", dict(heure=f"{now:%Y-%m-%d %H:%M:%S}", strat="3n", seance=f"{seance:%Y-%m-%d}",
                                       derniere_barre=str(m1.index[-1]), px=float(m1.close.iloc[-1]), atr15=atr,
                                       signe=int(sig), mom=r3, src="r3_bps"))
        self.log(f"3n {seance:%Y-%m-%d} : somme des 3 nuits {r3:+.1f} bps → {'LONG' if sig else 'rien'}")
        if not sig or not np.isfinite(atr):
            return
        # anti-hedging FTMO : pas de 3n long une nuit où le book A (mom) est short ; M2 trade alors à pleine taille
        s_mom = self.signe_mom(self.prochaine_seance(now))[0]
        if s_mom < 0:
            self.log(f"3n {seance:%Y-%m-%d} : mom est short ce soir (book A), pas de 3n long (règle anti-hedging)")
            return
        base = self.debut(seance)
        if base is None:
            return
        self.jambe("3n", seance, 1, S.K_SL_NUIT * atr, base, hms(seance, 3, 0, 1), dict(r3_bps=r3, atr15=atr))

    def ev_m2(self, now: pd.Timestamp) -> None:
        if not self.est_seance(now):
            return
        t = hms(now, 9, 35, 1)
        if not (t <= now < t + pd.Timedelta(minutes=3)):
            return
        seance = now.tz_localize(None).normalize()
        ds = f"{seance:%Y-%m-%d}"
        cle = f"M2:{ds}"
        if self.fait(cle):
            return
        self.marque(cle)
        if any(o["strat"] == "3n" and o["seance"] == ds for o in self.etat["ouverts"]):
            self.log("M2 : le 3n de la nuit est encore ouvert (?), pas de M2")
            return
        n3 = self.jour(ds).get("n3")
        m1 = self.m1_frais()
        if m1 is None:
            return
        s = S.signal_m2(m1, seance)
        self.ecrit("signaux.csv", dict(heure=f"{now:%Y-%m-%d %H:%M:%S}", strat="M2", seance=ds,
                                       derniere_barre=str(m1.index[-1]), px=float(m1.close.iloc[-1]), atr15=s["atr15"],
                                       signe=s["side"] if s["m2"] else 0, mom=s["strength"],
                                       src=f"reversal {s['reversal']:+.1f} bps"))
        self.log(f"M2 {ds} : sens {s['side']:+d}, force {s['strength']:.2f}, retournement {s['reversal']:+.1f} bps → "
                 f"{'SIGNAL' if s['m2'] else 'rien'} ; 3n de la nuit : {n3}")
        if not s["m2"] or not np.isfinite(s["atr15"]):
            return
        if n3 is not None and n3["raison"] != "heure":
            self.log(f"M2 : 3n sorti au {n3['raison']} cette nuit, pas de M2")
            return
        base = self.debut(seance)
        if base is None:
            return
        x = n3["pnl"] if n3 is not None else 0.0
        rho = max(0.0, min(base + x, (2 * base - x) / 2))
        if rho <= 0:
            self.log(f"M2 : taille nulle (base {base:.2f} %, nuit {x:+.2f} %)")
            return
        clot = self.cloture(seance)
        sortie = hms(seance, 15, 59, 57) if clot.hour >= 16 else clot - pd.Timedelta(seconds=3)
        if self.compte.phase == "financé" and ds in self.fed:
            sortie = min(sortie, hms(seance, 13, 54, 55))
        self.jambe("M2", seance, s["side"], S.K_SL_M2 * s["atr15"], rho, sortie,
                   dict(force=s["strength"], reversal_bps=s["reversal"], atr15=s["atr15"], x_nuit=x, base=base))

    def ev_fin_jour(self, now: pd.Timestamp) -> None:
        t = hms(now, 17, 0, 0)
        ds = f"{now:%Y-%m-%d}"
        if t <= now and self.compte.jour == ds and not self.fait(f"fin:{ds}") and not self.etat["ouverts"]:
            self.compte.fin_jour()
            self.marque(f"fin:{ds}")
            self.log(f"fin de journée : {self.compte.phase} virtuel {self.compte.P:+.2f} %, meilleur jour "
                     f"{self.compte.best:+.2f} %, rewards {self.compte.rewards} ({self.compte.rewards_pct:.2f} %)")

    def pas(self) -> None:
        now = self.maintenant()
        self.suivi(now)
        if self.book == "A":
            self.ev_mom(now)
        else:
            self.ev_3n(now)
            self.ev_m2(now)
        self.ev_fin_jour(now)

    @property
    def drapeau(self) -> Path:
        """Fichier posé par live/maj_auto.ps1 après une mise à jour validée : le bot sort proprement entre deux pas,
        live/lancer.bat le relance avec le nouveau code. L'état est déjà sauvé à chaque changement."""
        return self.dir.parent / f"redemarrer_{self.book}"

    def boucle(self) -> None:
        self.drapeau.unlink(missing_ok=True)  # on démarre déjà avec le code à jour
        self.log(f"démarrage (code {self.version()}) ; compte virtuel {self.compte.phase} {self.compte.P:+.2f} %, "
                 f"{len(self.etat['ouverts'])} position(s) suivie(s)")
        msg = self.b.controle_heure()
        if msg:
            self.log(f"!! {msg}")
        self.controle_annonces()
        self.controle_compte()
        dernier_controle = self.maintenant().date()
        dernier_compte = time.monotonic()
        while True:
            if self.drapeau.exists():
                self.drapeau.unlink(missing_ok=True)
                self.log("mise à jour du code reçue : arrêt propre, relance par lancer.bat")
                self.save()
                raise SystemExit(0)
            try:
                self.pas()
                if time.monotonic() - dernier_compte > 60:
                    dernier_compte = time.monotonic()
                    self.controle_compte()
                if self.maintenant().date() != dernier_controle:
                    dernier_controle = self.maintenant().date()
                    self.controle_annonces()
            except Exception:
                self.log("ERREUR\n" + traceback.format_exc())
                time.sleep(10)
            time.sleep(1)

    @staticmethod
    def version() -> str:
        import subprocess
        try:
            return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                                  timeout=5).stdout.strip() or "?"
        except Exception:
            return "?"

    def signaux(self) -> None:
        """Calcule et affiche les signaux du moment, sans passer d'ordre."""
        now = self.maintenant()
        m1 = self.m1_frais(strict=False)
        self.log(f"barres M1 : {m1.index[0]} → {m1.index[-1]} ({len(m1)}) ; spread {self.b.spread():.2f}")
        if self.book == "A":
            seance = self.prochaine_seance(now - pd.Timedelta(days=1 if now.hour < 10 else 0))  # nuit en cours ou à venir
            s, v, src = self.signe_mom(seance)
            atr = S.atr15_fin(m1, now, min_periods=14)
            self.log(f"mom séance {seance:%Y-%m-%d} : signe {s:+d} (12-1 = {v:+.4f}, {src}) ; ATR M15 {atr:.1f} pts "
                     f"→ stop {2 * atr:.1f} pts")
        else:
            seance = now.tz_localize(None).normalize() + pd.Timedelta(days=1 if now.hour >= 3 else 0)  # nuit à venir
            sig, r3 = S.signal_3n(m1, seance)
            self.log(f"3n nuit → {seance:%Y-%m-%d} : 3 nuits {r3:+.1f} bps → {'LONG' if sig else 'rien'}")
            jour = now.tz_localize(None).normalize()
            self.log(f"M2 {jour:%Y-%m-%d} : {S.signal_m2(m1, jour)}")
        self.log(f"compte virtuel : {self.compte}")

    def test_ordre(self) -> None:
        """Contrôle du chemin des ordres sur la démo : taille théorique d'un trade réel, puis un vrai ordre au lot
        minimum avec stop et objectif, fermé après 5 s, et lecture du P&L réalisé. Ne touche pas au compte virtuel."""
        now = self.maintenant()
        m1 = self.m1_frais(strict=False)
        atr = S.atr15_fin(m1, now, min_periods=14)
        spread = self.b.spread()
        k_sl = S.K_SL_NUIT if self.book == "A" else S.K_SL_M2
        dist = k_sl * atr
        r = self.compte.r()
        vol = self.b.lots(r, self.nominal, dist, spread)
        perte = vol * self.b.vpp * (dist + spread)
        self.log(f"taille d'un trade réel maintenant : ATR M15 {atr:.1f} pts, stop {dist:.1f} pts, spread {spread:.2f}, "
                 f"risque {r} % → {vol} lots ; perte au stop {perte:.2f} $ ({perte / self.nominal * 100:.2f} %), "
                 f"gain à 2 R {vol * self.b.vpp * (2 * dist - spread):.2f} $")
        vmin = self.b.info.volume_min
        fill = self.b.ouvre(1, vmin, dist, 2 * dist, "test ordre")
        p = self.b.position(fill.ticket)
        s_f = fill.ask - fill.bid  # stop à dist + spread, objectif à 2 dist − spread (broker.ouvre)
        ok_sl = p is not None and abs((fill.price - p.sl) - (dist + s_f)) < 0.05
        ok_tp = p is not None and abs((p.tp - fill.price) - (2 * dist - s_f)) < 0.05
        self.log(f"ordre test : {vmin} lot long à {fill.price} (ask {fill.ask}, bid {fill.bid}), ticket {fill.ticket} ; "
                 f"SL {None if p is None else p.sl} ({'OK' if ok_sl else 'ÉCART'}), "
                 f"TP {None if p is None else p.tp} ({'OK' if ok_tp else 'ÉCART'})")
        time.sleep(5)
        self.b.ferme(fill.ticket, "test ordre")
        for _ in range(20):
            bil = self.b.bilan(fill.ticket)
            if bil is not None:
                break
            time.sleep(0.5)
        self.log(f"fermeture test : {bil}")
        self.log("TEST OK" if (ok_sl and ok_tp and bil is not None) else "!! TEST EN ÉCHEC : me montrer ce journal")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--signaux", action="store_true", help="affiche les signaux du moment et sort, sans ordre")
    ap.add_argument("--test-ordre", action="store_true", help="ordre test au lot minimum (démo), fermé après 5 s")
    a = ap.parse_args()
    cfg = tomllib.loads(Path(a.config).read_text(encoding="utf-8"))
    from live.broker import MT5
    bot = Bot(cfg)
    bot.b = MT5(cfg["terminal"], cfg.get("symbole", "US100.cash"), int(cfg["magic"]),
                int(cfg.get("decalage_serveur_ny_h", 7)), log=bot.log)
    if a.test_ordre:
        bot.test_ordre()
    elif a.signaux:
        bot.signaux()
    else:
        bot.boucle()


if __name__ == "__main__":
    main()
