"""Réinitialisation du compte virtuel d'un ou deux books (passage des essais gratuits aux vrais comptes FTMO).

uv run python -m live.reinit A B          → pose les drapeaux, les bots en marche se relancent et repartent à zéro
uv run python -m live.reinit A B --voir   → affiche l'état actuel sans rien poser

Le script ne touche à aucun fichier d'état : il pose live/etat/reinitialiser_<book> et live/etat/redemarrer_<book>. Le
bot sort proprement entre deux pas, lancer.bat le relance, et c'est le bot qui, au démarrage, archive son dossier dans
live/etat/archive/<book>_<horodatage>/ puis repart d'un compte virtuel neuf (Bot.reinitialise_si_demande). Ainsi un bot
en marche ne peut pas réécrire l'ancien état par-dessus le nouveau. Refusé (par le script et par le bot) si une position
est suivie. Si le bot est arrêté, la réinitialisation se fait à son prochain lancement.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def etat_book(dossier: Path, book: str) -> tuple[dict, list]:
    d = dossier / book
    c = json.loads((d / "compte.json").read_text(encoding="utf-8")) if (d / "compte.json").exists() else {}
    e = json.loads((d / "etat.json").read_text(encoding="utf-8")) if (d / "etat.json").exists() else {}
    return c, e.get("ouverts", [])


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("books", nargs="+", choices=["A", "B"])
    ap.add_argument("--dossier", default="live/etat")
    ap.add_argument("--voir", action="store_true", help="affiche l'état sans poser de drapeau")
    a = ap.parse_args()
    dossier = Path(a.dossier)
    code = 0
    for b in a.books:
        c, ouverts = etat_book(dossier, b)
        print(f"book {b} : {c.get('phase', '—')} {c.get('P', 0.0):+.2f} %, évals {c.get('evals', '—')}, "
              f"rewards {c.get('rewards', '—')}, positions suivies {len(ouverts)}")
        if a.voir:
            continue
        if ouverts:
            print(f"  !! refusé : position ouverte ({', '.join(str(o.get('strat')) for o in ouverts)}) ; "
                  f"relancer après sa sortie")
            code = 1
            continue
        dossier.mkdir(parents=True, exist_ok=True)
        (dossier / f"reinitialiser_{b}").touch()
        (dossier / f"redemarrer_{b}").touch()
        print(f"  drapeaux posés : le bot {b} va se relancer et repartir d'un compte virtuel neuf "
              f"(contrôler « RÉINITIALISATION » dans {dossier / b / 'bot.log'})")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
