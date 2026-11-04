"""Accès au terminal MetaTrader 5 (package Python officiel `MetaTrader5`, Windows uniquement).

Un processus Python = un terminal = un compte : le bot du book A et celui du book B tournent chacun avec leur propre
installation de MT5 (dossier séparé), connectée au compte d'essai FTMO correspondant. Le mot de passe n'est jamais
dans le code ni dans la config : on se connecte une fois à la main dans le terminal (« enregistrer le mot de passe »),
et le bot s'attache au terminal déjà connecté.

Heure : les barres MT5 sont horodatées en heure du serveur. FTMO = heure de New York + 7 h toute l'année (minuit
serveur = 17:00 ET) ; contrôlé au démarrage contre l'horloge du VPS (`decalage_serveur_ny_h` dans la config).
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
import pandas as pd

NY = "America/New_York"


@dataclass
class Fill:
    ticket: int
    price: float
    volume: float
    bid: float
    ask: float


class MT5:
    def __init__(self, terminal: str, symbole: str, magic: int, decalage_h: int = 7, log=print):
        import MetaTrader5 as mt5  # import tardif : le reste du bot (et les tests) n'en dépend pas
        self.mt5, self.sym, self.magic, self.dec, self.log = mt5, symbole, magic, decalage_h, log
        if not mt5.initialize(path=terminal):
            raise RuntimeError(f"MT5 initialize a échoué : {mt5.last_error()} (terminal {terminal})")
        acc = mt5.account_info()
        if acc is None:
            raise RuntimeError("aucun compte connecté dans le terminal : s'y connecter à la main d'abord")
        self.log(f"MT5 connecté : compte {acc.login} sur {acc.server}, solde {acc.balance:,.2f} {acc.currency}")
        if not mt5.symbol_select(symbole, True):
            raise RuntimeError(f"symbole {symbole} introuvable")
        self.info = mt5.symbol_info(symbole)
        self.vpp = self.info.trade_tick_value / self.info.trade_tick_size  # $ par point et par lot
        self.log(f"{symbole} : {self.vpp:g} $ par point et par lot, lot min {self.info.volume_min}, "
                 f"pas {self.info.volume_step}, digits {self.info.digits}")

    def compte_info(self) -> dict:
        """Compte MT5 connecté en ce moment (change à chaque nouvel essai FTMO)."""
        a, t = self.mt5.account_info(), self.mt5.terminal_info()
        if a is None:
            return {}
        return dict(login=int(a.login), serveur=a.server, balance=float(a.balance), equity=float(a.equity),
                    trade_ok=bool(a.trade_allowed and a.trade_expert and (t is None or t.trade_allowed)))

    # ------------------------------------------------------------------ heure et données
    def serveur_vers_ny(self, t_sec: np.ndarray) -> pd.DatetimeIndex:
        naive = pd.to_datetime(t_sec, unit="s") - pd.Timedelta(hours=self.dec)
        return naive.tz_localize(NY, ambiguous="NaT", nonexistent="NaT")

    def controle_heure(self) -> str:
        """Compare l'heure du dernier tick à l'horloge du VPS ; renvoie un message (vide si cohérent)."""
        tk = self.mt5.symbol_info_tick(self.sym)
        if tk is None:
            return "pas de tick"
        t_ny = self.serveur_vers_ny(np.array([tk.time]))[0]
        now = pd.Timestamp.now(tz=NY)
        ecart = (now - t_ny).total_seconds()
        if abs(ecart) > 3 * 3600:
            return f"écart d'heure suspect : dernier tick {t_ny} contre horloge {now:%Y-%m-%d %H:%M:%S} ET"
        return ""

    def tick_frais(self, max_age_s: int = 120) -> bool:
        tk = self.mt5.symbol_info_tick(self.sym)
        if tk is None:
            return False
        t_ny = self.serveur_vers_ny(np.array([tk.time]))[0]
        return pd.notna(t_ny) and (pd.Timestamp.now(tz=NY) - t_ny).total_seconds() < max_age_s

    def spread(self) -> float:
        tk = self.mt5.symbol_info_tick(self.sym)
        return float(tk.ask - tk.bid)

    def barres(self, tf: str = "M1", n: int = 30_000) -> pd.DataFrame:
        """Barres TERMINÉES, indexées par l'heure de début en NY (la barre en cours de formation est retirée)."""
        code = {"M1": self.mt5.TIMEFRAME_M1, "H1": self.mt5.TIMEFRAME_H1, "D1": self.mt5.TIMEFRAME_D1}[tf]
        r = self.mt5.copy_rates_from_pos(self.sym, code, 0, n)
        if r is None or len(r) == 0:
            raise RuntimeError(f"pas de barres {tf} : {self.mt5.last_error()}")
        df = pd.DataFrame(r)
        idx = self.serveur_vers_ny(df.time.values.astype("int64"))
        df = df.set_index(idx)[["open", "high", "low", "close", "spread"]]
        df = df[df.index.notna()]
        df = df[~df.index.duplicated()].sort_index()
        duree = {"M1": pd.Timedelta(minutes=1), "H1": pd.Timedelta(hours=1), "D1": pd.Timedelta(days=1)}[tf]
        return df[df.index + duree <= pd.Timestamp.now(tz=NY)]

    # ------------------------------------------------------------------ ordres
    def lots(self, risque_pct: float, nominal: float, dist: float, spread: float) -> float:
        """Taille telle qu'un stop coûte exactement risque_pct du nominal, spread compris
        (P&L = risque × (R − c) / (1 + c) comme le moteur, c = spread / dist)."""
        v = risque_pct / 100 * nominal / (self.vpp * (dist + spread))
        step = self.info.volume_step
        v = np.floor(v / step + 1e-9) * step
        v = min(v, self.info.volume_max)
        return round(float(v), 8) if v >= self.info.volume_min else 0.0

    def _remplissage(self):
        fm = self.info.filling_mode
        if fm & 1:
            return self.mt5.ORDER_FILLING_FOK
        if fm & 2:
            return self.mt5.ORDER_FILLING_IOC
        return self.mt5.ORDER_FILLING_RETURN

    def ouvre(self, side: int, volume: float, dist_sl: float, dist_tp: float, comment: str) -> Fill:
        """Ordre au marché ; stop et objectif posés juste après, à distance du prix d'exécution réel."""
        mt5 = self.mt5
        tk = mt5.symbol_info_tick(self.sym)
        req = dict(action=mt5.TRADE_ACTION_DEAL, symbol=self.sym, volume=volume,
                   type=mt5.ORDER_TYPE_BUY if side > 0 else mt5.ORDER_TYPE_SELL,
                   price=tk.ask if side > 0 else tk.bid, deviation=50, magic=self.magic, comment=comment[:31],
                   type_time=mt5.ORDER_TIME_GTC, type_filling=self._remplissage())
        res = mt5.order_send(req)
        if res is None or res.retcode != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(f"ordre refusé : {None if res is None else (res.retcode, res.comment)} {mt5.last_error()}")
        pos = self._position_de_l_ordre(res.order)
        px = pos.price_open if pos is not None else res.price
        ticket = pos.ticket if pos is not None else res.order
        d = self.info.digits
        # Le backtest mesure stop et objectif sur le prix moyen ; ici l'entrée se fait à l'ask (achat) et la sortie se
        # déclenche sur le bid. Pour que les niveaux tombent au même prix moyen que dans le backtest : stop à
        # dist + spread du prix d'exécution, objectif à dist_tp − spread. Perte au stop = (dist + spread) × taille
        # = risque prévu (lots()), gain à l'objectif = (k·dist − spread) × taille = risque × (k − c) / (1 + c).
        s = float(tk.ask - tk.bid)
        sl = round(px - side * (dist_sl + s), d)
        tp = round(px + side * (dist_tp - s), d)
        self.modifie(ticket, sl, tp)
        return Fill(ticket=ticket, price=px, volume=volume, bid=tk.bid, ask=tk.ask)

    def _position_de_l_ordre(self, order: int):
        for _ in range(20):
            for p in self.mt5.positions_get(symbol=self.sym) or []:
                if p.identifier == order or p.ticket == order:
                    return p
            time.sleep(0.1)
        return None

    def modifie(self, ticket: int, sl: float, tp: float) -> None:
        mt5 = self.mt5
        res = mt5.order_send(dict(action=mt5.TRADE_ACTION_SLTP, symbol=self.sym, position=ticket, sl=sl, tp=tp,
                                  magic=self.magic))
        if res is None or res.retcode != mt5.TRADE_RETCODE_DONE:
            # sans stop, on ne garde pas la position
            self.log(f"!! SL/TP refusés ({None if res is None else (res.retcode, res.comment)}) : fermeture immédiate")
            self.ferme(ticket)
            raise RuntimeError("SL/TP refusés")

    def position(self, ticket: int):
        p = self.mt5.positions_get(ticket=ticket)
        return p[0] if p else None

    def ferme(self, ticket: int, comment: str = "sortie heure") -> bool:
        mt5 = self.mt5
        p = self.position(ticket)
        if p is None:
            return False
        tk = mt5.symbol_info_tick(self.sym)
        buy = p.type == mt5.POSITION_TYPE_BUY
        req = dict(action=mt5.TRADE_ACTION_DEAL, symbol=self.sym, volume=p.volume, position=ticket,
                   type=mt5.ORDER_TYPE_SELL if buy else mt5.ORDER_TYPE_BUY, price=tk.bid if buy else tk.ask,
                   deviation=50, magic=self.magic, comment=comment[:31], type_time=mt5.ORDER_TIME_GTC,
                   type_filling=self._remplissage())
        res = mt5.order_send(req)
        if res is None or res.retcode != mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(f"fermeture refusée : {None if res is None else (res.retcode, res.comment)}")
        return True

    def bilan(self, ticket: int) -> dict | None:
        """Bilan d'une position fermée : profit total ($), prix et heure de sortie, raison (SL / TP / heure)."""
        mt5 = self.mt5
        deals = mt5.history_deals_get(position=ticket)
        if not deals:
            return None
        sortie = [d for d in deals if d.entry in (mt5.DEAL_ENTRY_OUT, mt5.DEAL_ENTRY_OUT_BY)]
        if not sortie:
            return None
        x = sortie[-1]
        raison = {mt5.DEAL_REASON_SL: "SL", mt5.DEAL_REASON_TP: "TP"}.get(x.reason, "heure")
        profit = sum(d.profit + d.swap + d.commission + getattr(d, "fee", 0.0) for d in deals)
        t = self.serveur_vers_ny(np.array([x.time]))[0]
        return dict(profit=float(profit), exit_px=float(x.price), exit_time=str(t), raison=raison)
