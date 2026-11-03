---
type: hot
updated: 2026-11-03 20:55
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 719** (source : [[reports/prereg24_report]])
- Dernier pré-enregistrement : n° 24 ([[PREREGISTRATION_24]])
- Idées abandonnées au registre : 34 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-03

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-03] prereg | N° 24 : stratégie transmise 3n (long 20:05 → 03:00 si 3 nuits ≤ 0, stop 2 ATR M15) hors échantillon NQ 2010-2015, ES et YM rapportés (PREREGISTRATION_24 commit 90085fb, run_prereg24.py, reports/prereg24_report.md), compteur 1 719 → 1 726 | ÉCHEC : +0,016 R/trade net (15 $), p 0,32, −0,031 sur 2010-2012 ; filtre prises − sautées +0,042 R, p 0,19 ; brut +0,128 R (t 3,6) mais nuits sautées +0,092 (prime de nuit) ; coût 0,11 R/trade à l'époque (stop 8 pts)
- [2026-11-03] query | FTMO 1-Step avec la stratégie transmise 3n (20:05 → 03:00, stop 2 ATR M15) contre mom, réglages de l'avenant C (run_propfirm_3n_vs_mom.py, reports/propfirm_3n_vs_mom_report.md, exploratoire, hors compteur) | par tentative 3n +2 499 $ (10k) / +25 307 $ (100k) contre mom +468 $ / +5 000 $ sur 2016-2026 (sans edge +85 $ / +79 $) ; par mois d'emplacement 100k, mom +1 814 $ contre 3n +1 164 $ (109 trades/an) ; 3n hors règle des annonces ; 3n encore dans son échantillon de sélection
- [2026-11-03] query | Hypothèse : plus la somme des 3 nuits précédentes (r3) est positive, plus la nuit 20:05 → 03:00 suivante baisse ; NQ, ES, YM sur 2010-2015 et 2016-2026 (run_nq_nuit_r3_pente.py, reports/nq_nuit_r3_pente_report.md, exploratoire, compteur 1 695 → 1 719, 24 tests) | REJETÉE : pente côté r3 > 0 \|t\| ≤ 1,5 partout, Holm 1,0 ; nuit ≈ 0 après des hausses ; effet asymétrique : rebond après forte baisse (décile bas de r3 : +7 à +17 bps, t 2-3,7, 6 échantillons sur 6), ajouté « à surveiller »
- [2026-11-03] query | Filtre 3 nuits transmis, variante sortie 08:00 ET refaite avec vectorbt et comparée à notre règle NQ de nuit (run_nq_nuit_3n_8h_vbt.py, reports/nq_nuit_3n_8h_report.md, exploratoire, hors compteur) | chiffres d'origine retrouvés ; 3n 08h SL +3,7 R/an mais Sharpe IS 1,24 contre 1,36 (03h), DD $ +54 %, 44 % de trades stoppés ; tranche 03:00→08:00 sans avantage (+1,3 bps, t 0,9) ; plus corrélée à mom (+0,39 contre +0,29) : 03h reste préférable
- [2026-11-03] query | Filtre 3 nuits transmis (3n SL, 20:05 → 03:00) comparé à notre règle NQ de nuit (momentum 12-1, 20:00 → 9:30), même coût, en R et en % du notionnel (run_nq_nuit_3n_vs_mom.py, reports/nq_nuit_3n_vs_mom_report.md, descriptif, hors compteur) | 2016-2026 : Sharpe R 1,42 (3n SL) contre 0,90 (mom), mais 0,48 contre 0,83 sur 2022-2024 ; corrélation +0,35 ; mom gagne surtout les nuits « 3n long » (+7,5 contre −0,8 bps, t 3,6, 2016-2024 ; inversé en 2025-26) : pas un effet indépendant
- [2026-11-03] experiment | Stratégie transmise NQ overnight long 20:05 → 03:00 ET, filtre 3 nuits ≤ 0, stop 2 × ATR M15 (scripts_strategies_NQ.zip), backtest refait avec vectorbt (run_nq_nuit_3n_vbt.py, reports/nq_nuit_3n_vbt_report.md, exploratoire, hors compteur) | réplique exacte des chiffres d'origine (0,01 près) ; 2 défauts corrigés : 11 lundis perdus au passage à l'heure d'hiver (séance tz-aware), stop vectorbt testé sur la barre de sortie avant l'open ; version corrigée 3n SL Sharpe 1,36 IS / 1,59 OOS (orig. 1,36 / 1,63), nulle en 2022-2024
- [2026-11-02] prereg | N° 22 : lecture de niveaux sur NQ (R1 cassure du range US de la veille, cible measured move ; R2 règle des 80 % de la zone de valeur), ES et YM rapportés (run_prereg22.py, reports/prereg22_report.md), compteur 1 689 → 1 695 ; origine : captures « αλλο research » (pas d'orderflow, flèches = hauteurs de rectangles tracées après coup) | ÉCHEC des deux : R1 NQ +0,018 R [−0,025 ; +0,061], p Holm 0,43 ; R2 NQ −0,014 R, cible atteinte 45 % au lieu de 80 % ; amplitude moyenne de la séance US NQ 2026 = 415 points
- [2026-11-02] schema | Nouvelle règle de projet : registre des phénomènes confirmés (wiki/phenomenes.md, CLAUDE.md règle 3, SCHEMA) | 17 phénomènes confirmés amorcés (or et argent Fattinger-Ziegler, prime de nuit, règle NQ de nuit, minute 08:55 du DAX, reprise de l'or) et 3 à surveiller

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
