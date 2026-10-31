---
type: hot
updated: 2026-10-31 15:06
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 482** (source : [[reports/prereg17_report]])
- Dernier pré-enregistrement : n° 18 ([[PREREGISTRATION_18]])
- Idées abandonnées au registre : 24 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-10-31

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-10-31] experiment | Règle NQ de nuit recalculée avec les spreads réels bbo-1m (NQ 2011-2026, MNQ 2019-2026) | +0,076 R/trade contre +0,088 au coût fixe ; MNQ +0,067 à 1,24 $ A/R ; compteur inchangé
- [2026-10-31] prereg | N° 18 avenant A : stop 1 ATR M15 (≈ 0,12 % du prix) au lieu de 0,5 % | EV +71 $ ± 4 (10k), +1 035 $ ± 43 (100k) ; le spread 1 pb (0,083 R/trade) explique tout l'écart (sans coût +3 023 $) ; hors compteur
- [2026-10-31] prereg | N° 18 : prop firm comme option, FTMO 1-Step avec trades NQ au hasard (branche propfirm-ftmo) | EV +178 $ ± 6 (10k), +2 098 $ ± 64 (100k) ; sans RAZ de la perte max −34 % ; hors compteur (1 482)
- [2026-10-31] ingest | Achat Databento bbo-1m NQ 2010-2026 + MNQ 2019-2026 (11,20 $) dans cache/databento_bbo | spread NQ médian 2-4 ticks (pas 1) ; copie vers D: refusée (accès Windows), préparée dans cache/a_copier_vers_D
- [2026-10-31] prereg | N° 17 : exécution au VWAP (entrée 20:00-21:00, sortie au temps 9:00-9:30) pour la règle de nuit | non retenue (NQ +0,005 R IC inclut 0 ; ES/YM +0,013 R) ; compteur 1 482
- [2026-10-31] prereg | N° 16 : clôture sous VWAP 15:15-16:15 (pression vendeuse) sur règle de nuit, sélection ES+YM, confirmation NQ | ❌ H et filtre ; compteur 1 480
- [2026-10-31] prereg | N° 15 : filtres VIX (Donninger 0,87, Vojtko MM20) et taille selon σ20 sur la règle NQ de nuit | ❌ les 3 ; 9 filtres anti-DD rejetés au total ; compteur 1 478
- [2026-10-31] ingest | Historiques VIX et VIX3M du CBOE dans config/ | pour le n° 15

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
