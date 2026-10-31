# Pré-enregistrement n° 18 : espérance d'une éval FTMO 1-Step avec des trades au hasard

*2026-10-31, avant calcul. Ce n'est pas la recherche d'une edge de marché : on évalue un contrat (l'éval de prop firm vue comme une option). Le sens de chaque trade est tiré à pile ou face. **Compteur d'essais inchangé (1 482)** : aucune règle de trading n'est sélectionnée sur les données.*

## Idée

La perte d'une tentative est plafonnée au prix de l'éval, alors que le compte financé verse 90 % des profits sans plafond. Même sans edge, l'espérance d'une tentative peut être positive :

EV = P(passer l'éval) × V(compte financé) − prix de l'éval.

Une discussion précédente (session « Hedge sim discussion », 28-29 octobre, scripts `ftmo_sim.py` et `ftmo_funded_cmp.py`, hors dépôt) l'a chiffré avec un pile ou face binaire (gain t % ou perte r %, rien d'autre) : ~41 % de passage, financé ≈ 6,7-6,85 % du capital, ≈ +195 $ par éval 10k. Ce numéro reprend le modèle et le confronte à des **trajectoires réelles du NQ** (queues épaisses, volatilité en grappes, sortie en fin de journée sans SL ni TP, glissement sur le stop).

## Règles FTMO 1-Step modélisées (relevées sur ftmo.com en octobre 2026 dans la session citée)

- Éval : objectif +10 % ; perte journalière ≤ 3 % du capital initial sous le solde de minuit ; perte max 10 % sous le plus haut solde de fin de journée (suiveuse, ne s'arrête jamais) ; meilleur jour ≤ 50 % du profit total ; ni minimum de jours ni limite de temps ; frais non remboursés.
- Compte financé : mêmes 3 % / 10 %. Reward possible 14 jours calendaires après le premier trade du cycle (= **10 jours de bourse**) si profit > 0 et meilleur jour ≤ 50 % du profit ; on touche 90 %. Après un reward, le compte repart du capital initial ; **hypothèse principale : la perte max repart à −10 %** (variante : elle garde son plus haut). Vie max 500 jours de bourse.
- Prix : 10k 79 €, 25k 199 €, 50k 319 €, 100k 499 €, 200k 999 € ; 1 € = 1,10 $.

## Simulation

- **Un trade par jour**, sens au hasard (50/50), bracket : stop à `s` % du prix, risque = `r` % du capital (plafonné à la marge restante), objectif = `t` % du capital (réduit au profit encore nécessaire pour valider, et à ce qu'exige la règle des 50 %).
- **Mode « NQ réel »** : NQ 1 minute Databento `.v.0`, séances NYSE du 2016-01-04 au 2026-08-28 (rien après : holdout). Entrée à l'open de la première barre ≥ 9:35 ET, sortie au plus tard à la clôture de la barre de 15:54 ET (13:00 les demi-séances). Stop et objectif atteints dans la même minute = perte. Stop exécuté au pire de (stop, open de la barre) ; objectif au prix limite. Chaque compte démarre un jour tiré au hasard et avance jour après jour dans l'historique (bouclage à la fin), pour garder la volatilité en grappes. Pas d'ajustement de roulement nécessaire : tout se passe dans la séance, les roulements `.v.0` tombent à 00:00 UTC.
- **Mode « binaire »** (contrôle) : même moteur, issue gagnant/perdant avec p = 1 / (1 + RR), pour vérifier qu'on retrouve les chiffres de la session précédente.
- Coût CFD : **1 pb du prix par aller-retour** (≈ 2 points sur US100 à 20 000), payé sur chaque trade.
- 20 000 évals et 20 000 comptes financés par réglage ; graine fixée.

## Grille (figée)

- Éval : r ∈ {1 ; 2 ; 2,9} % × t ∈ {2 ; 3 ; 4,9} %.
- Financé : (r, t) ∈ {(0,5 ; 1) ; (0,5 ; 2) ; (0,75 ; 1,5) ; (1 ; 1) ; (1 ; 2)} %.
- Stop : s ∈ {0,25 ; 0,5 ; 1} % du prix (mode NQ réel).

## Ce qu'on rapporte

1. Passage, jours par tentative, valeur du financé (% du capital), P(≥ 1 reward), pour chaque réglage.
2. **Résultat principal** : EV par tentative 10k et 100k avec l'éval 2 % / 4,9 % et le financé 1 % / 2 % (le plan retenu dans la session précédente), stop s = 0,5 %, mode NQ réel, remise à zéro de la perte max. IC 95 % de l'EV (erreurs de P(passer) et de V combinées).
3. Taux de refus de reward qui annule l'EV.
4. Écart NQ réel − binaire, et sensibilité à s et à l'hypothèse de remise à zéro.

## Interdit après calcul

Changer l'heure d'entrée, le coût, la grille, la période, ou chercher un « meilleur » réglage hors grille et le présenter comme résultat. Le meilleur réglage de la grille est rapporté comme tel (sélectionné, donc optimiste), à côté du résultat principal fixé ci-dessus.

## Ce que ce numéro ne dit pas

L'EV suppose que FTMO verse les rewards. Ses règles interdisent l'« account rolling » et le trading assimilé à du jeu, et les comptes sont relus avant chaque reward : le risque de refus n'est pas modélisé autrement que par le seuil du point 3.
