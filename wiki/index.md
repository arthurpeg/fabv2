---
type: index
updated: 2026-10-31
---

# Index du wiki

> **Premier fichier à lire à chaque session**, puis [[wiki/Failed Ideas/ledger|le registre des échecs]] et [[wiki/hot|l'état courant]]. Une ligne par page : lien, résumé, statut, date. Règles et modèles : [[wiki/SCHEMA]].

## Hubs
- [[wiki/SCHEMA|SCHEMA]] — règles, modèles de page, procédures, lint · 2026-10-31
- [[wiki/hot|État courant]] — généré par `update_hot.py` : compteur, expériences ouvertes, journal récent, prochaines actions
- [[wiki/log|Journal]] — chronologie append-only
- [[wiki/lessons|Leçons]] — ce que toutes les expériences ont appris · 2026-10-31
- [[wiki/Failed Ideas/ledger|Registre des idées abandonnées]] — 18 idées, avec la raison et la condition de réouverture · 2026-10-31

## Expériences
- [[wiki/experiments/nq-nuit-momentum|Règle NQ de nuit (momentum 12-1, 20:00 ET)]] — n° 10 à 13 ; validée OOS 2011–15, α +6 %/an, β 0,09 ; filtres anti-DD (prix, annonces, VIX, taille) rejetés · `active` · 2026-10-31
- [[wiki/experiments/fade-gap-indices|Fade de gap sur indices]] — n° 2 ; reversal depuis 2022 (régime 0DTE) · `paper-trading` · 2026-10-31
- [[wiki/experiments/m2-bande-bruit-nq|Bande de bruit M2 sur NQ]] — n° 1–3 ; Sharpe 1,1 mais DSR 0,03 · `paper-trading` · 2026-10-31
- [[wiki/experiments/propfirm-ftmo-option|Prop firm comme option (FTMO 1-Step)]] — n° 18 ; trades au hasard sur NQ, entrée 9:50, stop 1 ATR M15, spread 1,5 pt : EV ≈ +161 $ / éval 10k, +1 933 $ / 100k si les rewards sont versés ; avec la règle NQ de nuit : +853 $ / +8 849 $ · `done` · 2026-10-31
- [[wiki/experiments/fx-timing-execution|Timing d'exécution FX (X3)]] — n° 4 ; ≈ 0,2 pb par ordre, pas un alpha · `done` · 2026-10-31
- Expériences abandonnées (n° 5 à 9, récolte 1, contrôle pile ou face…) : voir [[wiki/Failed Ideas/ledger]]

## Concepts
- [[wiki/concepts/pre-enregistrement|Pré-enregistrement]] — protocole : tout est figé et commité avant calcul
- [[wiki/concepts/compteur-essais|Compteur d'essais]] — N cumulé, sert au DSR ; 1 482 au n° 17
- [[wiki/concepts/dsr|Deflated Sharpe Ratio]] — critère > 0,95
- [[wiki/concepts/reality-check|Reality Check, PBO, permutation, bootstrap]] — autres tests de multiplicité
- [[wiki/concepts/cout-standard|Coût standard]] — 1 tick + 5 $ aller-retour
- [[wiki/concepts/prime-de-nuit|Prime de nuit]] — l'effet le plus robuste trouvé
- [[wiki/concepts/roulements|Roulements]] — ajustement en ratio ; piège de `fab.core.load`
- [[wiki/concepts/is-oos|IS / OOS / holdout]] — découpages et holdout unique post-2026-08-28
- [[wiki/concepts/histdata-fuseau|Fuseau HistData]] — décalage EU-DST, fichier DAX corrompu

## Recherche
- [[wiki/research/recoltes-ssrn|Revues de papiers SSRN]] — lots du 13 au 29 octobre et ce qu'ils ont donné · `ingested`
- [[wiki/research/litterature-intraday|Littérature intraday M1–M5]] — mécanismes, papiers, contradictions · `ingested`

## Référence (aiguillage)
- [[wiki/reference/resultats|Où trouver les résultats]] — RESULTS.md, reports/, results/
- [[wiki/reference/donnees|Où sont les données]] — Databento, cache, HistData, PDF
- [[wiki/reference/code|Où est le code]] — modules et scripts `run_*.py`

## Outils
- [update_hot.py](update_hot.py) — régénère `hot.md` (stdlib, lancé par le hook Stop)
