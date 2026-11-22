"""Barres horaires bid/ask Dukascopy pour la fiche wiki/experiments/fx-exportateur-importateur.

uv run --with dukascopy-python python fetch_fx_balance.py              → télécharge 2010-01 → 2026-08-28
uv run --with dukascopy-python python fetch_fx_balance.py --assemble   → reconstruit seulement les fichiers finaux

Réutilise fetch_dukascopy.py (même format : cache/dukascopy/<PAIRE>_1h.parquet). Devises flottantes contre
le dollar hors 7 majeures (déjà vues au n° 27) ; ancrées ou très administrées exclues (CNH, DKK, HKD).
Rien après le 2026-08-28. La réserve 2021-09-01 → 2026-08-28 est téléchargée mais ne sert qu'aux contrôles
de qualité (comptes, trous, spreads) jusqu'à son ouverture par un pré-enregistrement.
"""

from __future__ import annotations

import sys

import fetch_dukascopy as fd
from dukascopy_python import instruments as I

PAIRS = {
    "USDNOK": I.I_USD_NOK, "USDSEK": I.I_USD_SEK, "USDPLN": I.I_USD_PLN, "USDCZK": I.I_USD_CZK,
    "USDHUF": I.I_USD_HUF, "USDRON": I.I_USD_RON, "USDILS": I.I_USD_ILS, "USDMXN": I.I_USD_MXN,
    "USDZAR": I.I_USD_ZAR, "USDSGD": I.I_USD_SGD, "USDTHB": I.I_USD_THB, "USDTRY": I.I_USD_TRY,
}

fd.PAIRS = PAIRS
fd.years = lambda pair, freq: range(2010, fd.END.year + 1)


def main() -> None:
    if "--assemble" not in sys.argv:
        for pair in PAIRS:
            for year in fd.years(pair, "1h"):
                for side in fd.SIDES:
                    fd.fetch_year(pair, side, year, "1h")
    for pair in PAIRS:
        fd.assemble(pair, "1h")


if __name__ == "__main__":
    main()
