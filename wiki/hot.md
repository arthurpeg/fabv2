---
type: hot
updated: 2026-11-03 21:14
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
| [[wiki/experiments/nq-ema930-m2\|NQ intraday « close de 9:30 contre EMA12 », modèle M2 (stratégie transmise)]] | running | candidat externe (non pré-enregistré) |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-03] query | EMA 9:30 / M2 : backtest vectorbt comparé au rapport d'origine (artefact transmis ; reports/nq_ema930_vbt_report.md) | sans stop identique au dollar près (C, D, M2, M2 + taille, 4 périodes) ; avec stop +0,01 à +0,03 de Sharpe (2 stops dans la barre d'entrée) ; seuils du post choisis sur 2013-2024 : seul 2010-06 → 2012-12 est hors échantillon
- [2026-11-03] experiment | Stratégie transmise NQ intraday close 9:30 contre EMA12 (C) et modèle M2 (force > 2,2 ATR ou retournement < −60 bps, taille / σ 20 j), backtest refait avec vectorbt (run_nq_ema930_vbt.py, reports/nq_ema930_vbt_report.md, exploratoire, hors compteur) | trades M2 par année = post ; vectorbt = boucle sauf 2 stops dans la barre d'entrée ; M2 + taille Sharpe 1,28 IS / 1,86 OOS, t 4,05 ; C seul 0,62 (t 1,96) ; gains concentrés (10 meilleurs 70-80 % depuis 2022) ; comparaison avec l'original en attente
- [2026-11-03] prereg | N° 24 : stratégie transmise 3n (long 20:05 → 03:00 si 3 nuits ≤ 0, stop 2 ATR M15) hors échantillon NQ 2010-2015, ES et YM rapportés (PREREGISTRATION_24 commit 90085fb, run_prereg24.py, reports/prereg24_report.md), compteur 1 719 → 1 726 | ÉCHEC : +0,016 R/trade net (15 $), p 0,32, −0,031 sur 2010-2012 ; filtre prises − sautées +0,042 R, p 0,19 ; brut +0,128 R (t 3,6) mais nuits sautées +0,092 (prime de nuit) ; coût 0,11 R/trade à l'époque (stop 8 pts)
- [2026-11-03] query | FTMO 1-Step avec la stratégie transmise 3n (20:05 → 03:00, stop 2 ATR M15) contre mom, réglages de l'avenant C (run_propfirm_3n_vs_mom.py, reports/propfirm_3n_vs_mom_report.md, exploratoire, hors compteur) | par tentative 3n +2 499 $ (10k) / +25 307 $ (100k) contre mom +468 $ / +5 000 $ sur 2016-2026 (sans edge +85 $ / +79 $) ; par mois d'emplacement 100k, mom +1 814 $ contre 3n +1 164 $ (109 trades/an) ; 3n hors règle des annonces ; 3n encore dans son échantillon de sélection
- [2026-11-03] query | Hypothèse : plus la somme des 3 nuits précédentes (r3) est positive, plus la nuit 20:05 → 03:00 suivante baisse ; NQ, ES, YM sur 2010-2015 et 2016-2026 (run_nq_nuit_r3_pente.py, reports/nq_nuit_r3_pente_report.md, exploratoire, compteur 1 695 → 1 719, 24 tests) | REJETÉE : pente côté r3 > 0 \|t\| ≤ 1,5 partout, Holm 1,0 ; nuit ≈ 0 après des hausses ; effet asymétrique : rebond après forte baisse (décile bas de r3 : +7 à +17 bps, t 2-3,7, 6 échantillons sur 6), ajouté « à surveiller »
- [2026-11-03] query | Filtre 3 nuits transmis, variante sortie 08:00 ET refaite avec vectorbt et comparée à notre règle NQ de nuit (run_nq_nuit_3n_8h_vbt.py, reports/nq_nuit_3n_8h_report.md, exploratoire, hors compteur) | chiffres d'origine retrouvés ; 3n 08h SL +3,7 R/an mais Sharpe IS 1,24 contre 1,36 (03h), DD $ +54 %, 44 % de trades stoppés ; tranche 03:00→08:00 sans avantage (+1,3 bps, t 0,9) ; plus corrélée à mom (+0,39 contre +0,29) : 03h reste préférable
- [2026-11-03] query | Filtre 3 nuits transmis (3n SL, 20:05 → 03:00) comparé à notre règle NQ de nuit (momentum 12-1, 20:00 → 9:30), même coût, en R et en % du notionnel (run_nq_nuit_3n_vs_mom.py, reports/nq_nuit_3n_vs_mom_report.md, descriptif, hors compteur) | 2016-2026 : Sharpe R 1,42 (3n SL) contre 0,90 (mom), mais 0,48 contre 0,83 sur 2022-2024 ; corrélation +0,35 ; mom gagne surtout les nuits « 3n long » (+7,5 contre −0,8 bps, t 3,6, 2016-2024 ; inversé en 2025-26) : pas un effet indépendant
- [2026-11-03] experiment | Stratégie transmise NQ overnight long 20:05 → 03:00 ET, filtre 3 nuits ≤ 0, stop 2 × ATR M15 (scripts_strategies_NQ.zip), backtest refait avec vectorbt (run_nq_nuit_3n_vbt.py, reports/nq_nuit_3n_vbt_report.md, exploratoire, hors compteur) | réplique exacte des chiffres d'origine (0,01 près) ; 2 défauts corrigés : 11 lundis perdus au passage à l'heure d'hiver (séance tz-aware), stop vectorbt testé sur la barre de sortie avant l'open ; version corrigée 3n SL Sharpe 1,36 IS / 1,59 OOS (orig. 1,36 / 1,63), nulle en 2022-2024

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
