# Pré-enregistrement n° 20 : matinée US → reste de séance sur ES et YM

*2026-11-01. Règle et critères : [[PREREGISTRATION_20]] (commit 035a8bb, avant calcul). Compteur global : 1 553 → 1 555 (le pré-enregistrement annonçait 1 520 → 1 522 ; 33 essais sur l'or ont été comptés entre-temps dans une autre session). Code : [run_prereg20.py](../run_prereg20.py). Sorties : `results/prereg20/` (run.log, results.csv, by_year.csv, trades.csv).*

## Règle testée (figée)

Matinée X = 9:30 → 11:30 NY. Si |X| dépasse 1 écart-type des 20 séances précédentes, position dans le sens de X de 11:30 à 16:00, backtest vectorbt, net 1 tick + 5 $. ES et YM, 2010-06 → 2026-08-28, séances NYSE pleines. Origine : NQ, +5,8 bp/trade net (t 2,4), [[reports/nq_matin_aprem_report]].

## Résultats

| | ES | YM | NQ (origine, pour mémoire) |
|---|---|---|---|
| Trades (par an) | 1 196 (74) | 1 220 (76) | 1 215 (75) |
| Net bp/trade [IC 95 %] | +2,1 [−1,7 ; +6,7] | −1,1 [−4,7 ; +2,8] | +5,8 |
| p unilatéral / p Holm | 0,17 / 0,35 | 0,71 / 0,71 | — |
| 2010-2017 / 2018-2026 (bp/trade) | −0,6 / +4,3 | −3,7 / +1,2 | — |
| Brut bp/trade | +3,5 | −0,2 | +6,7 |
| Sharpe (vrai nombre de trades) | 0,25 | −0,15 | ≈ 0,6 |
| Années positives 2011-2025 | 8 / 15 | 5 / 15 | — |
| Sans seuil (tous les jours), net bp (t) | +0,9 (0,9) | −0,6 (−0,6) | +2,3 (2,0) |
| Corrélation X → reste de séance (t) | +0,045 (1,6) | +0,009 (0,3) | +0,054 (2,3) |

Source : `results/prereg20/results.csv`, `run.log`.

**Verdict pré-enregistré : ÉCHEC.** Aucun des deux marchés n'a p Holm < 0,05, et les deux perdent sur 2010-2017.

## Lecture

1. **YM : rien**, même en brut (−0,2 bp). La corrélation matinée → après-midi est nulle (+0,009).
2. **ES : même sens que NQ, mais deux à trois fois plus faible** et non significatif. Tout le gain vient de 2018-2026, et 2025 seul fait +1 848 bp sur +2 476 bp cumulés (+1 764 bp pour YM la même année). Sans 2025, ES est presque à zéro et YM nettement négatif.
3. **La hiérarchie NQ > ES > YM** suit la part de valeurs technologiques à forte volatilité, et donc probablement la part d'options et de couverture gamma. Elle colle aussi à un pur effet de sélection : la règle a été choisie sur l'actif où elle marchait le mieux. Ce test ne permet pas de trancher.
4. Comme pour la règle de nuit (n° 10), l'effet trouvé sur NQ ne se transmet pas aux autres indices US. Mais ici, NQ lui-même n'avait qu'un t de 2,4 après sélection.

## Conséquence (fixée à l'avance)

Ligne au [[wiki/Failed Ideas/ledger|registre des échecs]]. La règle n'est rouverte qu'avec une donnée de mécanisme (gamma des vendeurs d'options, OPRA, disponible depuis 2013), et pas pour un simple test sur le holdout NQ.

*Suite exploratoire sur NQ avec SL/TP en ATR M15 : [[reports/nq_matin_sltp_report]].*
