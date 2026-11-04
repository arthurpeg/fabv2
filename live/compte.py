"""Compte FTMO 1-Step virtuel, tenu par le bot : mêmes règles que run_ftmo_deux_comptes.Compte (calendaire, règle des
annonces, politique « cible+attente »), mais pas à pas, trade par trade, pour le direct.

Tout est en % du capital nominal (10 000 $). Le compte de démo FTMO (essai gratuit) reste toujours en « éval » chez
FTMO : la phase éval / financé n'existe que dans ce compte virtuel, qui décide du risque, de l'objectif et de l'attente.
Contrôle d'équivalence avec Compte : tests/test_live.py.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pandas as pd

DAILY, MAXLOSS, TARGET, SPLIT, MIN_RISK = 3.0, 10.0, 10.0, 0.9, 0.05
R_EVAL, R_FUND, TP_R = 2.5, 1.0, 2.0


@dataclass
class CompteVirtuel:
    nom: str
    phase: str = "éval"
    P: float = 0.0          # gain du cycle en cours (%)
    hi: float = 0.0         # plus haut solde de fin de journée du cycle (%)
    best: float = 0.0       # meilleur jour du cycle (%)
    f0: str | None = None   # date du 1er jour tradé du cycle financé (ou de l'éval)
    evals: int = 1
    rewards: int = 0
    rewards_pct: float = 0.0
    jour: str | None = None  # journée FTMO en cours (date de séance)
    pnl_jour: float = 0.0
    trade_jour: bool = False
    mort_jour: bool = False  # éval / financé perdu aujourd'hui : plus de trade jusqu'à demain
    events: list = field(default_factory=list)

    # ------------------------------------------------------------------ persistance
    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=1), encoding="utf-8")

    @classmethod
    def load(cls, path: Path, nom: str) -> "CompteVirtuel":
        if path.exists():
            return cls(**json.loads(path.read_text(encoding="utf-8")))
        return cls(nom=nom)

    # ------------------------------------------------------------------ règles
    def _nouveau(self, phase: str) -> None:
        self.phase, self.P, self.hi, self.best, self.f0 = phase, 0.0, 0.0, 0.0, None

    def _regle_ok(self) -> bool:
        return self.P > 0 and self.best <= 0.5 * self.P + 1e-9

    def _event(self, d: str, s: str) -> None:
        self.events.append(f"{d} {s}")

    def debut_jour(self, d: pd.Timestamp) -> None:
        """À appeler avant le 1er trade de la journée FTMO d (date de séance). Clôt la journée précédente si besoin,
        puis verse le reward s'il est permis (14e jour calendaire après le 1er trade, règle des 50 %)."""
        ds = f"{pd.Timestamp(d):%Y-%m-%d}"
        if self.jour == ds:
            return
        self.fin_jour()
        self.jour, self.pnl_jour, self.trade_jour, self.mort_jour = ds, 0.0, False, False
        if self.phase == "financé" and self.f0 is not None:
            if (pd.Timestamp(ds) - pd.Timestamp(self.f0)).days >= 13 and self._regle_ok():
                self.rewards += 1
                self.rewards_pct += SPLIT * self.P
                self._event(ds, f"reward {SPLIT * self.P:.2f} % → demander le payout ; nouveau cycle financé")
                self._nouveau("financé")

    def fin_jour(self) -> None:
        """Clôt la journée en cours (meilleur jour, plus haut, validation de l'éval)."""
        if self.jour is None or not self.trade_jour or self.mort_jour:
            self.trade_jour = False  # rien à clore (ou déjà clos)
            return
        self.f0 = self.jour if self.f0 is None else self.f0
        self.best, self.hi = max(self.best, self.pnl_jour), max(self.hi, self.P)
        if self.phase == "éval" and self.P >= TARGET - 1e-9 and self._regle_ok():
            self._event(self.jour, f"éval n° {self.evals} validée → financé")
            self._nouveau("financé")
        self.trade_jour = False

    def r(self) -> float:
        return R_EVAL if self.phase == "éval" else R_FUND

    def risque_base(self) -> float:
        """Risque de base de la journée (%), borné par la distance au plancher. 0 si la journée est bloquée."""
        if self.mort_jour:
            return 0.0
        return min(self.r(), self.P - (self.hi - MAXLOSS))

    def en_attente(self) -> bool:
        """Politique « attente » : en financé, gain > 0 et règle des 50 % respectée → ne plus trader."""
        return (self.phase == "financé" and self.f0 is not None and self.P > 0
                and max(self.best, self.pnl_jour) <= 0.5 * self.P + 1e-9)

    def plan_jambe(self, risque: float, c: float) -> tuple[float, float] | None:
        """Risque effectif (%) et objectif (en R, ≤ 2) d'une jambe ; None si elle ne doit pas être jouée.
        `c` = coût de l'aller-retour en R (spread / distance du stop). Si le risque de base de la journée est sous
        MIN_RISK, le compte est perdu (comme Compte.jour) : appeler echec_si_bloque avant."""
        if self.mort_jour or self.en_attente():
            return None
        floor = self.hi - MAXLOSS
        risque = min(risque, self.P - floor)
        if risque < MIN_RISK:
            return None
        obj = TP_R
        b = max(self.best, self.pnl_jour)
        if self.phase == "éval":  # objectif ramené au reste à faire
            need = max(TARGET - self.P, 2 * b - self.P, 0.01)
            k = need * (1 + c) / risque + c
            obj = min(TP_R, k)
        elif self.P > 0:  # cible : juste ce qui manque pour la règle des 50 %
            need = 2 * b - self.P + 0.01
            if b > 0.5 * self.P and need <= b + 1e-9:
                k = need * (1 + c) / risque + c
                obj = min(TP_R, k)
        return risque, obj

    def echec_si_bloque(self) -> bool:
        """Début de journée : si le risque de base est sous MIN_RISK, le compte est perdu (nouvelle éval)."""
        if not self.mort_jour and self.risque_base() < MIN_RISK:
            self._echec()
            return True
        return False

    def enregistre(self, pnl_pct: float) -> None:
        """Résultat réalisé d'une jambe, en % du nominal (frais et spread compris)."""
        self.trade_jour = True
        self.P += pnl_pct
        self.pnl_jour += pnl_pct
        if self.P <= self.hi - MAXLOSS + 1e-9 or self.pnl_jour <= -DAILY:
            self._echec()

    def _echec(self) -> None:
        self._event(self.jour or "?", f"{self.phase} perdu ({self.P:+.2f} %) → nouvelle éval virtuelle (79 €)")
        self.evals += 1
        self._nouveau("éval")
        self.mort_jour, self.trade_jour = True, False
