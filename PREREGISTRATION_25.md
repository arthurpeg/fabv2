# Pré-enregistrement n° 25 : la stratégie transmise EMA 9:30 / M2 hors échantillon dans le temps, NQ 2010-06 → 2012-12

*2026-11-03, écrit et commité avant de lancer la stratégie sur ces données. Données : Databento `GLBX.MDP3`, `ohlcv-1m`, `NQ.v.0` (et `ES.v.0`, `YM.v.0`), non ajustées, `cache/databento_2010/` (achat du n° 11).*

## Pourquoi

La stratégie EMA 9:30 / M2 a été transmise le 2026-11-03 et refaite dans [[reports/nq_ema930_vbt_report]], où vectorbt reproduit l'original au dollar près. Ses seuils (force > 2,2 ATR, retournement < −60 bps) ont été choisis par l'auteur du post en regardant 2013-2024. Le hors échantillon 2025-2026 est court, et le choix des jours n'y est significatif qu'à 10 %. **Les séances de juin 2010 à décembre 2012 n'ont jamais servi à cette stratégie** : ni au post, ni à l'original, ni à nous.

## Ce qui est déjà connu de ces données (à déclarer)

Aucun calcul intraday 9:30 → 15:55 n'a été fait sur 2010-2012 pour cette stratégie. Ces données ont servi à d'autres tests de la nuit (n° 11 pour la règle NQ de nuit, n° 24 et l'étude r3 pour 3n), mais pas à la séance US. Le n° 20 (suivre la matinée US, ES et YM sur 2010-2017) a échoué ; c'est une autre règle (|z| de 9:30 → 11:30), qui recouvre en partie l'idée de C.

## Règle (celle de l'original, rien ne change)

- **Barres.** Barres 5 min, heure NY. EMA(12) des closes et ATR(14) de Wilder M5 sur toutes les barres, Globex compris. On ne garde que les séances qui ont une barre de 9:30 et une barre de 9:35.
- **Sens.** Close de la barre de 9:30 au-dessus de l'EMA12 : long ; en dessous : short.
- **Exécution.** Entrée à l'open de 9:35, sortie au close de la dernière barre RTH (15:55, ou plus tôt les jours écourtés). 15 $ l'aller-retour par contrat.
- **M2.** On ne trade que si force = |close 9:30 − EMA12| / ATR M5 > 2,2, ou si le retournement est < −60 bps. Le retournement est le rendement 9:35 → 15:55 de la séance précédente, signé dans le sens du jour.
- **Stop (variante).** Fixe à 4 × ATR(14) M15, calculé sur la barre 9:15-9:30. On le vérifie sur les plus bas et plus hauts 5 min ; le fill se fait au stop, ou à l'open en cas de gap. 1 R = la distance du stop.
- **Taille / σ 20 j (variante).** σ est l'écart-type du mouvement 9:35 → 15:55, en points, sur les 20 séances précédentes. Taille = (1 / σ) divisé par la moyenne de (1 / σ) sur les 250 séances précédentes. On arrondit à 0,1, avec un minimum de 0,1 ; la taille vaut 1 tant que l'historique manque. La normalisation glissante remplace celle de l'original, qui se calait sur 2016-2024 : on ne peut pas utiliser le futur.
- **Code.** `run_nq_ema930_vbt.py`, inchangé : séances, vectorbt, contrôle par une boucle à la main.
- **Période.** Séances du 2010-06-08 au 2012-12-31. Les 20 premières séances ont une taille de 1 ; la règle M2 s'applique dès la 2e séance.

## Tests (8 essais ; compteur 1 726 → 1 734)

**Principaux (2), sur NQ, 1 contrat, sans stop :**
- **P1.** Le P&L net moyen par trade de M2 est > 0. On utilise un t HAC Newey-West (5 retards), en test unilatéral.
- **P2.** Le filtre M2 choisit de meilleurs jours. On mesure le P&L net moyen du signal C sur les jours M2, moins celui des jours que M2 exclut, avec un t de Welch unilatéral.

**Secondaires (6), rapportés sans changer le verdict :**
- NQ : C (tous les jours) ; M2 + stop, avec E[R] > 0 ; M2 + taille ; M2 + stop + taille ;
- M2 sur ES et sur YM, avec la valeur du point de chaque contrat.

## Critères, fixés à l'avance

1. **Succès** si les trois conditions sont remplies : P1 a p < 0,05 ; P2 a p < 0,05 ; le P&L net moyen de M2 est positif sur chacune des deux moitiés, 2010-06 → 2011-09 et 2011-10 → 2012-12.
2. **Succès partiel** (« le signal marche, la sélection des jours n'est pas démontrée ») si P1 et les deux moitiés sont remplis, mais pas P2.
3. **Échec** sinon.

## Interdit après calcul

Après le calcul, on ne change ni l'EMA, ni les seuils (2,2 ATR, −60 bps), ni les heures, ni le stop, ni la taille, ni le coût, ni la période, ni les moitiés. On n'ajoute aucun filtre et on n'exclut aucun jour.
