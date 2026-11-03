---
type: hot
updated: 2026-11-03 20:38
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 695** (source : [[reports/nq_nuit_r3_pente_report]])
- Dernier pré-enregistrement : n° 22 ([[PREREGISTRATION_22]])
- Idées abandonnées au registre : 33 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-03

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-3n-reversal\|NQ overnight long 20:05 → 03:00, filtre 3 nuits (stratégie transmise)]] | running | candidat externe (non pré-enregistré) |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-03] query | Hypothèse : plus la somme des 3 nuits précédentes (r3) est positive, plus la nuit 20:05 → 03:00 suivante baisse ; NQ, ES, YM sur 2010-2015 et 2016-2026 (run_nq_nuit_r3_pente.py, reports/nq_nuit_r3_pente_report.md, exploratoire, compteur 1 695 → 1 719, 24 tests) | REJETÉE : pente côté r3 > 0 \|t\| ≤ 1,5 partout, Holm 1,0 ; nuit ≈ 0 après des hausses ; effet asymétrique : rebond après forte baisse (décile bas de r3 : +7 à +17 bps, t 2-3,7, 6 échantillons sur 6), ajouté « à surveiller »
- [2026-11-03] query | Filtre 3 nuits transmis, variante sortie 08:00 ET refaite avec vectorbt et comparée à notre règle NQ de nuit (run_nq_nuit_3n_8h_vbt.py, reports/nq_nuit_3n_8h_report.md, exploratoire, hors compteur) | chiffres d'origine retrouvés ; 3n 08h SL +3,7 R/an mais Sharpe IS 1,24 contre 1,36 (03h), DD $ +54 %, 44 % de trades stoppés ; tranche 03:00→08:00 sans avantage (+1,3 bps, t 0,9) ; plus corrélée à mom (+0,39 contre +0,29) : 03h reste préférable
- [2026-11-03] query | Filtre 3 nuits transmis (3n SL, 20:05 → 03:00) comparé à notre règle NQ de nuit (momentum 12-1, 20:00 → 9:30), même coût, en R et en % du notionnel (run_nq_nuit_3n_vs_mom.py, reports/nq_nuit_3n_vs_mom_report.md, descriptif, hors compteur) | 2016-2026 : Sharpe R 1,42 (3n SL) contre 0,90 (mom), mais 0,48 contre 0,83 sur 2022-2024 ; corrélation +0,35 ; mom gagne surtout les nuits « 3n long » (+7,5 contre −0,8 bps, t 3,6, 2016-2024 ; inversé en 2025-26) : pas un effet indépendant
- [2026-11-03] experiment | Stratégie transmise NQ overnight long 20:05 → 03:00 ET, filtre 3 nuits ≤ 0, stop 2 × ATR M15 (scripts_strategies_NQ.zip), backtest refait avec vectorbt (run_nq_nuit_3n_vbt.py, reports/nq_nuit_3n_vbt_report.md, exploratoire, hors compteur) | réplique exacte des chiffres d'origine (0,01 près) ; 2 défauts corrigés : 11 lundis perdus au passage à l'heure d'hiver (séance tz-aware), stop vectorbt testé sur la barre de sortie avant l'open ; version corrigée 3n SL Sharpe 1,36 IS / 1,59 OOS (orig. 1,36 / 1,63), nulle en 2022-2024
- [2026-11-02] prereg | N° 22 : lecture de niveaux sur NQ (R1 cassure du range US de la veille, cible measured move ; R2 règle des 80 % de la zone de valeur), ES et YM rapportés (run_prereg22.py, reports/prereg22_report.md), compteur 1 689 → 1 695 ; origine : captures « αλλο research » (pas d'orderflow, flèches = hauteurs de rectangles tracées après coup) | ÉCHEC des deux : R1 NQ +0,018 R [−0,025 ; +0,061], p Holm 0,43 ; R2 NQ −0,014 R, cible atteinte 45 % au lieu de 80 % ; amplitude moyenne de la séance US NQ 2026 = 415 points
- [2026-11-02] schema | Nouvelle règle de projet : registre des phénomènes confirmés (wiki/phenomenes.md, CLAUDE.md règle 3, SCHEMA) | 17 phénomènes confirmés amorcés (or et argent Fattinger-Ziegler, prime de nuit, règle NQ de nuit, minute 08:55 du DAX, reprise de l'or) et 3 à surveiller
- [2026-11-02] query | Affirmations de Fattinger-Ziegler testées sur l'argent SI 5 min 2017-2026, données London Strategic Edge ajustées par nos soins (run_gc_fattinger.py SI, reports/si_fattinger_report.md, exploratoire, compteur 1 631 → 1 685, 54 tests ; SI ajouté à recolte1.engine avec détection des roulements par le volume) | même microstructure que l'or en plus bruyante : 8:30 × 3,2, Fed × 6,4, Tokyo × 1,7, sauts 7,3 % ; 28,5 % du prix avant 3:00 NY (contredit le papier) ; pas de pic à 13:30 ; début de Globex non bruité ; continuation de nuit b ≈ 1,2 non significative après Holm, portée par 2023-2026
- [2026-11-02] ingest | Argent (SI) 1 minute via l'API London Strategic Edge, plan gratuit, marché `futures` (fetch_lse.py → cache/lse/SI_lse_1m.parquet) | 3,02 M barres 2017-04-02 → 2026-08-28 ; rien avant 2017 ; GOLD de la même source = GC Databento à 1 tick près ; série front non ajustée qui roule au 1er jour du mois de livraison : 114 séances quasi vides (2-3 avant chaque roulement), à filtrer et ajuster avant usage ; contrats individuels (marché cme) payants

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
