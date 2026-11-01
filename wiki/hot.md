---
type: hot
updated: 2026-11-01 22:00
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 553** (source : [[reports/prereg20_report]])
- Dernier pré-enregistrement : n° 20 ([[PREREGISTRATION_20]])
- Idées abandonnées au registre : 29 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-01

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-01] abandon | Matinée US → reste de séance (règle n° 20) | rouverte seulement avec une donnée de gamma des options (OPRA)
- [2026-11-01] experiment | n° 20 sur ES et YM, 2010-2026 (run_prereg20.py) | ÉCHEC : ES +2,1 bp/trade net p Holm 0,35, YM −1,1 bp p 0,71 ; les deux négatifs sur 2010-2017 ; ES et YM portés par 2025
- [2026-11-01] prereg | n° 20 : matinée US 9:30→11:30 (|z| > 1) → position 11:30→16:00 sur ES et YM (PREREGISTRATION_20.md, commit 035a8bb) | compteur 1 553 → 1 555 (annoncé 1 520 → 1 522, essais de l'or comptés entre-temps)
- [2026-11-01] query | Rendement de l'or (GC) par session, 2016-2026 : reprise, Asie SGE, Londres (fix AM), COMEX (fix PM), post-règlement, puis heure par heure (run_gc_sessions.py, exploratoire, compteur 1 553) | seule la reprise 17:00 → 9:00 Shanghai est significative (+2,0 bp brut, t 3,5, Holm 0,003 ; +1,1 bp net, Sharpe 0,60) ; autres sessions nulles ; 16:00 → 20:00 NY porte ≈ 3 des 4 bp/jour ; 16:00 → 19:00 a posteriori +1,4 bp net, nul en 2016-19
- [2026-11-01] query | Pouvoir prédictif de la matinée US (9:30 → 10:00…13:00) sur le reste de séance et la dernière 1/2 h, NQ 2010-2026 (run_nq_matin_aprem.py, exploratoire, compteur 1 520) | reste de séance : r +0,03 à +0,07, positif dans les 24 cases fenêtre × période, nul en vol basse ; dernière 1/2 h ≈ rien ; suivre 9:30→11:30 si |z| > 1 : +5,8 bp/trade net (t 2,4, ~75/an), sélection après coup, à tester seulement sur le holdout
- [2026-11-01] experiment | Corrélation entre sessions NQ Asie → Europe → US, coupe à l'ouverture suivante (A) ou à la vraie clôture (B) (run_nq_sessions_corr.py, exploratoire, 2010-2026, compteur 1 501) | rejeté : Europe → US r −0,003, nuit → US r 0,000 ; Asie → Europe r −0,05 (retournement, éteint depuis 2023) ; Europe jusqu'à 16:30 Ldn → reste US r +0,066 mais porté par 9:30-11:30 NY (momentum intraday US), pas par l'Europe
- [2026-11-01] experiment | Règle NQ de nuit, SL au bord du range 17:00→20:00 au lieu de 2 ATR, TP 1 à 2,5 R (run_nq_nuit_sl_range.py, exploratoire, compteur 1 493) | rejeté : net −0,10 (TP 1 R) à −0,03 R/trade (TP 2,5 R), brut +0,03 à +0,10 ; stop médian 0,86 ATR, 60 % de SL ; réf. +0,088 R, Sharpe 1,00
- [2026-11-01] query | Quantification de l'edge de la règle NQ de nuit au coût réel (2011-07 → 2026-08) | +0,076 R/trade [+0,033 ; +0,116], t 3,4, PF 1,13, 43 % gagnants, payoff 1,52, Kelly 5 % ; ≈ 57 $/trade NQ (160 $ en 2024-26) ; DSR 0,52 avec N = 1 485 contre PSR 0,99 sur le test unique 2011-2015

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
