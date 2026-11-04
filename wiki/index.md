---
type: index
updated: 2026-10-31
---

# Index du wiki

> **Premier fichier à lire à chaque session**, puis [[wiki/Failed Ideas/ledger|le registre des échecs]], [[wiki/phenomenes|le registre des phénomènes]] et [[wiki/hot|l'état courant]]. Une ligne par page : lien, résumé, statut, date. Règles et modèles : [[wiki/SCHEMA]].

## Hubs
- [[wiki/SCHEMA|SCHEMA]] — règles, modèles de page, procédures, lint · 2026-10-31
- [[wiki/hot|État courant]] — généré par `update_hot.py` : compteur, expériences ouvertes, journal récent, prochaines actions
- [[wiki/log|Journal]] — chronologie append-only
- [[wiki/lessons|Leçons]] — ce que toutes les expériences ont appris · 2026-10-31
- [[wiki/phenomenes|Registre des phénomènes confirmés]] — ce qui se vérifie sur nos données, tradable seul ou non, pour combiner en stratégies · 2026-11-02
- [[wiki/Failed Ideas/ledger|Registre des idées abandonnées]] — 32 idées, avec la raison et la condition de réouverture · 2026-11-02

## Expériences
- [[wiki/experiments/nq-nuit-momentum|Règle NQ de nuit (momentum 12-1, 20:00 ET)]] — n° 10 à 13 ; validée OOS 2011–15, α +6 %/an, β 0,09 ; filtres anti-DD (prix, annonces, VIX, taille) et stop au range du soir rejetés · `active` · 2026-11-01
- [[wiki/experiments/nq-nuit-3n-reversal|NQ overnight long 20:05 → 03:00, filtre 3 nuits (transmise)]] — refaite avec vectorbt : réplique exacte de l'original ; corrigée, 3n + SL 2 ATR M15 Sharpe 1,36 IS / 1,59 OOS ; ❌ hors échantillon 2010-2015 (n° 24 : +0,016 R, p 0,32 ; brut = prime de nuit) · `abandoned` · 2026-11-03
- [[wiki/experiments/nq-ema930-m2|NQ intraday close 9:30 contre EMA12, modèle M2 (transmise)]] — refaite avec vectorbt : M2 + taille Sharpe 1,28 IS / 1,86 OOS (t 4,05) ; C seul 0,62 ; ❌ hors échantillon 2010-2012 (n° 25 : 5 bps/trade, p 0,19 ; filtre M2 sans effet) · `abandoned` · 2026-11-03
- [[wiki/experiments/fade-gap-indices|Fade de gap sur indices]] — n° 2 ; reversal depuis 2022 (régime 0DTE) · `paper-trading` · 2026-10-31
- [[wiki/experiments/m2-bande-bruit-nq|Bande de bruit M2 sur NQ]] — n° 1–3, 19 ; Sharpe 1,1 mais DSR 0,03 ; variante stop 1R ratée hors échantillon 2010–15 · `paper-trading` · 2026-10-31
- [[wiki/experiments/propfirm-ftmo-option|Prop firm comme option (FTMO 1-Step)]] — **plan retenu le 2026-11-04 : A = mom, B = 3n + M2, annonces + cible + attente, scaling 10k → 400k** ; n° 18 ; trades au hasard sur NQ, entrée 9:50, stop 1 ATR M15, spread 1,5 pt : EV ≈ +161 $ / éval 10k, +1 933 $ / 100k si les rewards sont versés ; avec la règle NQ de nuit : +853 $ / +8 849 $ ; LucidFlex 50K : +157 $ (plan « 2 coups » : +66 $ / +234 $) ; Smart Trader Funds 1 Phase (à plat avant les annonces 8:30) : +390 $ / +4 512 $ ; 10 prop firms comparées : FundingPips et FTMO en tête · `active` · 2026-11-04
- [[wiki/experiments/fx-timing-execution|Timing d'exécution FX (X3)]] — n° 4 ; ≈ 0,2 pb par ordre, pas un alpha · `done` · 2026-10-31
- Expériences abandonnées (n° 5 à 9, récolte 1, contrôle pile ou face…) : voir [[wiki/Failed Ideas/ledger]]

## Concepts
- [[wiki/concepts/pre-enregistrement|Pré-enregistrement]] — protocole : tout est figé et commité avant calcul
- [[wiki/concepts/compteur-essais|Compteur d'essais]] — N cumulé, sert au DSR ; 1 485 au n° 19
- [[wiki/concepts/dsr|Deflated Sharpe Ratio]] — critère > 0,95
- [[wiki/concepts/reality-check|Reality Check, PBO, permutation, bootstrap]] — autres tests de multiplicité
- [[wiki/concepts/cout-standard|Coût standard]] — 1 tick + 5 $ aller-retour
- [[wiki/concepts/prime-de-nuit|Prime de nuit]] — l'effet le plus robuste trouvé
- [[wiki/concepts/roulements|Roulements]] — ajustement en ratio ; piège de `fab.core.load`
- [[wiki/concepts/is-oos|IS / OOS / holdout]] — découpages et holdout unique post-2026-08-28
- [[wiki/concepts/histdata-fuseau|Fuseau HistData]] — décalage EU-DST, fichier DAX corrompu

## Recherche
- [[wiki/research/recoltes-ssrn|Revues de papiers SSRN]] — lots du 13 au 29 octobre et ce qu'ils ont donné · `ingested`
- [[wiki/research/fattinger-ziegler-or|Fattinger-Ziegler sur l'or]] — découverte du prix sur 24 h (SSRN 2606706) testée sur GC 2016-2026 et SI 2017-2026 : microstructure reproduite, « pas de prix avant l'Europe » contredit · `tested` · 2026-11-02
- [[wiki/research/litterature-intraday|Littérature intraday M1–M5]] — mécanismes, papiers, contradictions · `ingested`

## Référence (aiguillage)
- [[wiki/reference/resultats|Où trouver les résultats]] — RESULTS.md, reports/, results/
- [[wiki/reference/donnees|Où sont les données]] — Databento, cache, HistData, PDF
- [[wiki/reference/code|Où est le code]] — modules et scripts `run_*.py`

## Outils
- [update_hot.py](update_hot.py) — régénère `hot.md` (stdlib, lancé par le hook Stop)
