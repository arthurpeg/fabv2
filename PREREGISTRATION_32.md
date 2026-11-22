# Pré-enregistrement n° 32 : forward de BB (bande de bruit) sur NQ, dates de lecture fixées à l'avance

*2026-11-22, écrit et commité avant tout calcul sur les données concernées. Protocole : [PROTOCOLE.md](PROTOCOLE.md), étape 2 → 4 (forward à dates de lecture, modèle du [n° 26](PREREGISTRATION_26.md)). Parcours : stratégie. Demandé par l'utilisateur.*

## Pourquoi

BB (bande de bruit de Zarattini, Aziz et Barbon, ancien « M2 » des n° 1-3) est au registre des échecs depuis le n° 2 (DSR 0,03), avec une condition de réouverture : **seulement sur des données postérieures au 2026-08-28**. Toutes les données NQ antérieures sont explorées ou consommées pour cette famille (2016-2026 : n° 1-3 et explorations du 2026-11-22 ; 2010-2015 : variante S1 au n° 19). Le 2026-11-22, on a constaté qu'aucun forward ne suivait BB (le bot trade le M2 EMA 9:30, pas BB ; BB n'est pas dans le n° 26). Ce pré-enregistrement fixe ce forward.

## Déjà vu

- N° 1 : NQ, Sharpe net +1,15 (2016-2022) / +1,13 (2023 → 2026-08), version sans VWAP à l'entrée. N° 2 : DSR 0,03 → rejet. N° 3 (volatilité cible) : +0,80 / +1,07.
- 2026-11-22 (exploration, 2016-2026) : VWAP exigé à l'entrée, Sharpe 1,16 → 1,23 ([[reports/m2_vwap_report]]) ; SL / TP et un trade par jour ([[reports/bb_sltp_report]], [[reports/propfirm_bb_report]]) : mode A, SL 0,25 ATR, TP 2R, un trade par jour, +0,124 R net par trade (t 4,2), 142 trades par an.
- **La fenêtre 2026-08-29 → 2026-11-03 (LSE) a déjà été regardée pour le n° 26 : elle est exclue**, comme au n° 26 (avenant A). Elle peut seulement servir à amorcer σ, le VWAP et l'ATR14 (aucun trade n'y est compté).

## Hypothèses (2 essais ; compteur 2 127 → 2 129)

Code figé au commit de ce pré-enregistrement : [run_m2_vwap.py](run_m2_vwap.py) (fonction `m2`), [run_bb_sltp.py](run_bb_sltp.py) (fonctions `prepare`, `simulate`), lus par [run_prereg32.py](run_prereg32.py). NQ, 1 contrat, coût standard 1 tick + 5 $ = 0,50 pt aller-retour.

- **H1 : BB de référence.** `m2(a, g, vwap_entry=True)` : σ = moyenne sur 14 séances de |cours à HH:MM / ouverture − 1| ; bande haute = max(ouverture, clôture de la veille à 16:00) × (1 + σ), basse = min(…) × (1 − σ) ; VWAP au prix typique depuis 9:30 ; contrôles 10:00, 10:30 … 15:30 sur la clôture de la minute précédente, exécution à l'open de la minute du contrôle ; achat si clôture > bande haute **et** > VWAP, vente si < bande basse **et** < VWAP ; stop suiveur aux contrôles sur max(bande, VWAP) ; sortie à 16:00. **Test : P&L net journalier moyen en points > 0** (toutes les séances, 0 sans trade ; t de Newey-West, 5 retards).
- **H2 : BB version prop firm.** `simulate(P, "A", 0.25, 2)` en ne gardant que le premier trade de chaque séance : même entrée, stop suiveur conservé, SL = 0,25 × ATR14 (moyenne des amplitudes 9:30-16:00 des 14 séances précédentes), TP = 2 × SL, surveillés à la minute, SL prioritaire dans la même minute, sortie à l'open en cas de saut, sinon 16:00. **Test : R net moyen par trade > 0** (1 R = 0,25 × ATR14 ; t de Newey-West, 5 retards).

Rapporté sans verdict : $ par an, Sharpe, pire creux, gagnants, sorties par type.

## Données et dates de lecture

- **Données comptées : séances du 2026-11-04 au dernier jour de lecture inclus.** Source principale : Databento `GLBX.MDP3`, `ohlcv-1m`, `NQ.v.0`, achetée aux dates de lecture (comme au n° 26), placée dans `D:/quant-data/Cotations/indices/NQ_v0_1m.parquet` ; supprimer `cache/NQ_adj.parquet` avant le calcul. Repli : London Strategic Edge, avec la règle de roulement du n° 26.
- Lectures, mêmes dates et mêmes règles que le n° 26 :

| Lecture | Données jusqu'au | Règle de décision |
|---|---|---|
| L1 (intermédiaire) | **2028-02-29** | Succès d'une hypothèse seulement si z ≥ 3,0 ; sinon on continue. |
| L2 (intermédiaire) | **2029-08-31** | Succès si z ≥ 3,0. Arrêt pour futilité (non contraignant) si z < 0. |
| L3 (finale) | **2031-08-29** | Verdict : p unilatéral, Holm sur les hypothèses non encore décidées, seuil 0,05. |

- **Puissance** (effets de l'exploration, sans doute optimistes) : H1 (Sharpe ≈ 1,1 par an) : z attendu ≈ 1,3 à L1, ≈ 2,4 à L3 → succès à L3 ≈ 67 % (≈ 21 % à la moitié de l'effet). H2 (+0,124 R, écart-type ≈ 1,16 R, ≈ 142 trades par an) : z ≈ 1,4 à L1, ≈ 2,8 à L3 → ≈ 80 % à L3 (≈ 29 % à la moitié). Un succès à L1 est très improbable.

## Interdits

Entre deux lectures, **interdit** de calculer sur ces données un prix, un rendement, un signal ou un P&L de H1 ou H2. Si BB est un jour tradé par le bot (paper ou réel), ses résultats live ne servent pas au verdict et ne doivent pas être agrégés avant les lectures. On ne change ni les règles, ni le coût, ni les seuils, ni les dates, ni la source (sauf indisponibilité de Databento). Aucun filtre ajouté.
