# Pré-enregistrement n° 10 : momentum 12-1 de nuit, entrée horaire avec SL/TP en ATR M15, sur ES et YM

*2026-10-30, avant tout calcul sur ES et YM avec cette règle. Origine : exploration de la récolte 1 ([reports/recolte1_report.md](reports/recolte1_report.md), [reports/recolte1_atr_report.md](reports/recolte1_atr_report.md)). La règle a été choisie sur NQ uniquement ; ES et YM servent de test hors échantillon partiel.*

## Pourquoi un test seulement « partiel »

- Sur NQ 2016–2026, la règle a été retenue après un tri : 927 tests de la récolte 1 → 4 règles → 5 variantes de SL/TP × 15 heures d'entrée. Le compte 20:00 a été choisi parce qu'il était le meilleur. Ses statistiques sur NQ sont donc biaisées vers le haut.
- ES et YM ont déjà été vus au premier tri : la prime de nuit simple (clôture → ouverture) y avait un IC net positif sur 2016–2026. En revanche, **l'entrée horaire, les SL/TP en ATR M15, la sortie à 9:30 ET et le choix de 20:00 n'ont jamais été calculés sur ES ni sur YM.**
- Un vrai test hors échantillon dans le temps (NQ avant 2016) demande des données absentes de `D:/quant-data/Cotations` ; il n'est pas couvert ici.

## Règle figée (aucun paramètre ne sera modifié après calcul)

| Élément | Valeur |
|---|---|
| Marchés | ES et YM (`ES.v.0`, `YM.v.0`, 1 minute, Databento), ajustés en ratio aux roulements trimestriels (`recolte1.engine.load`) |
| Période | 2016-01 → 2026-08 (trades à partir de 2017, warm-up du momentum) |
| Signal | momentum 12-1 **de l'actif lui-même** : somme des log-rendements close-to-close NYSE (16:00 ET) des mois M−12 à M−2 ; long si > 0, short si < 0, pour toutes les nuits du mois M |
| Entrée | **20:00 ET** (America/New_York, heure d'été gérée), nuits précédant une séance NYSE ; prix = clôture de la dernière barre 1 min démarrant dans [19:55, 19:59] |
| SL / TP | **SL = 2 × ATR, TP = 5 × ATR** ; ATR de Wilder 14 sur bougies de 15 min, dernière bougie terminée avant l'entrée |
| Sortie au temps | 9:30 ET (ouverture NYSE) si ni SL ni TP ; aucun trade ne traverse 17:00 ET |
| Exécution | vectorbt `Portfolio.from_signals` sur barres 1 min, stops sur high/low, SL prioritaire si les deux dans la même minute (code de `run_recolte1_atr.py`) |
| Coût | 1 tick + 5 $ par aller-retour (ES 0,25 + 0,10 point ; YM 1 + 1 point) |
| Mesure | R par trade = rendement net / (2 × ATR / prix d'entrée) |

## Tests (4 essais)

- **Principaux (2)** : compte 20:00 sur ES ; compte 20:00 sur YM.
- **Secondaires (2)** : bloc 19:00 + 20:00 + 21:00 (trois comptes, R par nuit additionnés) sur ES et sur YM.

Compteur global d'essais : 224 avant ce document. L'exploration de la récolte 1 n'avait pas été comptée : 927 tests de règles + 300 combinaisons (4 règles × 5 variantes × 15 heures), soit 1 227. Le compteur passe donc à 224 + 1 227 = 1 451, puis à **1 455** avec ces 4 essais.

## Critères de succès, fixés à l'avance

IC 95 % et p-valeurs par bootstrap par blocs mobiles circulaires (blocs de 10 trades, 2 000 tirages ; `recolte1.engine.ci_mean`), p unilatéral pour H1 : R moyen net > 0.

1. **Succès principal** si, **pour ES et pour YM**, le compte 20:00 a un R moyen net > 0 avec p unilatéral < 0,05 après correction de Holm sur les 2 marchés.
2. **Et** le R moyen net est positif sur chacune des deux sous-périodes 2017–2020 et 2021–2026, sur les deux marchés (signe seulement, pas de seuil).
3. **Succès partiel** : un seul des deux marchés remplit 1 et 2. **Échec** : aucun.
4. Les tests secondaires (bloc 19–21) sont rapportés quel que soit le résultat, et ne peuvent pas transformer un échec principal en succès.

Rapportés en plus, sans valeur de décision : R par an, drawdown maximal en R, années positives, part des sorties TP / SL / 9:30.

## Ce qui est interdit après calcul

Changer l'heure, les multiples d'ATR, la période de l'ATR, la sortie, le signal, le coût ou la période ; ajouter un filtre ; exclure une année ; remplacer ES ou YM par un autre marché.
