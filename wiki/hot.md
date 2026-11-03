---
type: hot
updated: 2026-11-03 22:22
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 726** (source : [[reports/prereg25_report]])
- Dernier pré-enregistrement : n° 25 ([[PREREGISTRATION_25]])
- Idées abandonnées au registre : 35 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-03

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-03] query | N° 25, diagnostic après coup : niveau de prix et normalisation (reports/prereg25_report.md, dernière section) | bps = déjà % du prix ; le coût de 15 $ pèse 3,3 bps en 2010-12 contre 0,8 ; brut 8,5 contre 15,9 bps à volatilité égale (σ 90 contre 100 bps) ; normalisé par σ 0,061 contre 0,165, en R brut 0,057 contre 0,245 : la normalisation ne sauve pas M2
- [2026-11-03] prereg | N° 25 : stratégie transmise EMA 9:30 / M2 hors échantillon NQ 2010-06 → 2012-12, ES et YM rapportés (PREREGISTRATION_25 commit f130eeb, run_prereg25.py, reports/prereg25_report.md), compteur 1 726 → 1 734 | ÉCHEC : M2 +20,7 $/trade (5,2 bps), p 0,19 ; jours M2 − jours exclus +4,2 $, p 0,45 ; moitiés positives ; M2 + stop +0,066 R (t 0,91) ; ES p 0,039, YM p 0,054 avant correction
- [2026-11-03] query | EMA 9:30, M2 + stop 4 × ATR M15 en R (1 R = distance du stop ; reports/nq_ema930_vbt_report.md, results/nq_ema930/m2_stop_R.csv) | IS +0,200 R/trade, 19,6 R/an, Sharpe 1,29, DD −18,5 R, t 4,06 ; OOS +0,241 R, 23,9 R/an, Sharpe 1,79, DD −12,5 R ; toutes les années positives en R sauf 2017 (−2,8 R)
- [2026-11-03] query | EMA 9:30 / M2 : backtest vectorbt comparé au rapport d'origine (artefact transmis ; reports/nq_ema930_vbt_report.md) | sans stop identique au dollar près (C, D, M2, M2 + taille, 4 périodes) ; avec stop +0,01 à +0,03 de Sharpe (2 stops dans la barre d'entrée) ; seuils du post choisis sur 2013-2024 : seul 2010-06 → 2012-12 est hors échantillon
- [2026-11-03] experiment | Stratégie transmise NQ intraday close 9:30 contre EMA12 (C) et modèle M2 (force > 2,2 ATR ou retournement < −60 bps, taille / σ 20 j), backtest refait avec vectorbt (run_nq_ema930_vbt.py, reports/nq_ema930_vbt_report.md, exploratoire, hors compteur) | trades M2 par année = post ; vectorbt = boucle sauf 2 stops dans la barre d'entrée ; M2 + taille Sharpe 1,28 IS / 1,86 OOS, t 4,05 ; C seul 0,62 (t 1,96) ; gains concentrés (10 meilleurs 70-80 % depuis 2022) ; comparaison avec l'original en attente
- [2026-11-03] prereg | N° 24 : stratégie transmise 3n (long 20:05 → 03:00 si 3 nuits ≤ 0, stop 2 ATR M15) hors échantillon NQ 2010-2015, ES et YM rapportés (PREREGISTRATION_24 commit 90085fb, run_prereg24.py, reports/prereg24_report.md), compteur 1 719 → 1 726 | ÉCHEC : +0,016 R/trade net (15 $), p 0,32, −0,031 sur 2010-2012 ; filtre prises − sautées +0,042 R, p 0,19 ; brut +0,128 R (t 3,6) mais nuits sautées +0,092 (prime de nuit) ; coût 0,11 R/trade à l'époque (stop 8 pts)
- [2026-11-03] query | FTMO 1-Step avec la stratégie transmise 3n (20:05 → 03:00, stop 2 ATR M15) contre mom, réglages de l'avenant C (run_propfirm_3n_vs_mom.py, reports/propfirm_3n_vs_mom_report.md, exploratoire, hors compteur) | par tentative 3n +2 499 $ (10k) / +25 307 $ (100k) contre mom +468 $ / +5 000 $ sur 2016-2026 (sans edge +85 $ / +79 $) ; par mois d'emplacement 100k, mom +1 814 $ contre 3n +1 164 $ (109 trades/an) ; 3n hors règle des annonces ; 3n encore dans son échantillon de sélection
- [2026-11-03] query | Hypothèse : plus la somme des 3 nuits précédentes (r3) est positive, plus la nuit 20:05 → 03:00 suivante baisse ; NQ, ES, YM sur 2010-2015 et 2016-2026 (run_nq_nuit_r3_pente.py, reports/nq_nuit_r3_pente_report.md, exploratoire, compteur 1 695 → 1 719, 24 tests) | REJETÉE : pente côté r3 > 0 \|t\| ≤ 1,5 partout, Holm 1,0 ; nuit ≈ 0 après des hausses ; effet asymétrique : rebond après forte baisse (décile bas de r3 : +7 à +17 bps, t 2-3,7, 6 échantillons sur 6), ajouté « à surveiller »

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
