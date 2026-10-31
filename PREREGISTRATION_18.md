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

## Avenant A (2026-10-31, avant calcul de la variante) : stop à 1 ATR M15

Demande de l'utilisateur après le premier rapport : le stop n'est plus à `s` % du prix mais à **1 ATR M15** (ATR de Wilder sur 14 barres de 15 minutes, série 1 min complète 24 h, lu sur la dernière barre terminée à l'entrée, soit la barre 9:15-9:30 ET ; même calcul que `coinflip.rules.atr_tf`). Distance du stop du jour = ATR / prix d'entrée ; le coût de 1 pb du prix vaut donc 1 pb / (ATR / prix) en R, variable selon les jours.

- Nouveau **résultat principal** : NQ réel, stop 1 ATR M15, éval 2 % / 4,9 %, financé 1 % / 2 %, remise à zéro de la perte max. Même grille éval et financé, même période, même coût, mêmes règles FTMO, même graine.
- Les variantes en % du prix (0,25 ; 0,5 ; 1 %) restent rapportées pour comparaison ; leurs chiffres ne changent pas (la variante ATR est simulée après elles).
- Le roulement `.v.0` à 00:00 UTC peut gonfler une barre M15 ; à 9:30 ET son poids dans l'ATR de Wilder est ≤ (13/14)^50 ≈ 2,5 %, négligé.

## Avenant B (2026-10-31, avant calcul de la variante) : entrée 9:50 ET, spread 1 à 1,5 point

Remarque de l'utilisateur : chez FTMO, le spread de l'US100 est beaucoup plus large juste après 9:30 et revient ensuite à **1 à 1,5 point**. Le bbo-1m du future NQ ne montre pas cet élargissement (médiane 0,5 point de 9:20 à 10:30 sur 2016-2026, pics de moyenne à 9:45 et 10:00 = annonces macro), c'est donc un effet propre au CFD, non mesurable ici. On suit la remarque :

- **Entrée à l'open de la première barre ≥ 9:50 ET** (après l'ouverture et l'annonce de 9:45). Stop 1 ATR M15 lu sur la barre 9:30-9:45 (dernière terminée à 9:50). Sortie inchangée (15:54 ET au plus tard).
- **Coût = 1,5 point** par aller-retour (cas principal) et **1 point** (variante), exprimé en fraction du prix au niveau actuel : 1,5 / 25 684 = 0,58 pb et 1 / 25 684 = 0,39 pb (25 684 = médiane du NQ du 2025-08-29 au 2026-08-28). Raison : le spread en points d'un CFD suit le niveau de l'indice ; appliquer 1,5 point au NQ de 2016 (≈ 4 500) le gonflerait 5 fois.
- **Nouveau résultat principal** : entrée 9:50, stop 1 ATR M15, coût 1,5 point, éval 2 % / 4,9 %, financé 1 % / 2 %, remise à zéro. Même grille, mêmes règles, simulé après toutes les variantes précédentes (dont les chiffres ne changent pas).

## Avenant C (2026-10-31, avant calcul) : la règle NQ de nuit au lieu de trades au hasard

Demande de l'utilisateur : refaire la simulation FTMO avec la stratégie NQ de nuit ([[wiki/experiments/nq-nuit-momentum]] : compte 20:00 ET, momentum 12-1, SL 2 ATR / TP 5 ATR en M15, sortie 9:30 ET). Évaluation d'un contrat : compteur d'essais inchangé, la règle n'est pas modifiée.

- **Trades** : les 3 787 trades de `results/couts_reels_nq_nuit/trades.csv` (2011-07-01 → 2026-08-28), colonne `R_brut` (1 R = distance du stop, 2 ATR) et `risk` (distance du stop en fraction du prix). Entrées du dimanche au jeudi à 20:00 ET, sorties avant 9:30 ET : pas de position le week-end, chaque trade tient dans une journée FTMO (minuit serveur = 17:00 ET), pas de swap.
- **Moteur** : celui du n° 18 ; chaque compte part d'un trade tiré au hasard et enchaîne les trades suivants dans l'ordre (bouclage). Un trade = une journée FTMO. Objectif et stop **non modifiés** (pas de réduction de l'objectif près des 10 %) : la règle est tradée telle quelle, seule la taille change. Risque net de coût, comme avant.
- **Coût CFD** : 1,5 point par aller-retour au niveau actuel du NQ (1,5 / 25 684 du prix), variante 3 points (spreads de nuit plus larges).
- **Grille** : éval r ∈ {0,5 ; 1 ; 1,5 ; 2 ; 2,5} % ; financé r ∈ {0,25 ; 0,5 ; 1 ; 1,5 ; 2} %.
- **Résultat principal** : éval 2 %, financé 1 %, coût 1,5 point, remise à zéro de la perte max, 2011-07 → 2026-08.
- **Contrôles** : (a) mêmes trades avec R − moyenne(R) (même distribution, edge retirée) ; (b) trades de 2011-07 à 2015-12 seulement (période hors échantillon de la règle ; 2016-2026 a servi à la choisir, donc les chiffres complets sont optimistes).

## Avenant D (2026-10-31, avant calcul) : la règle NQ de nuit sur un compte LucidFlex 50K

Demande de l'utilisateur. Règles relevées le 31 octobre 2026 sur lucidtrading.com et support.lucidtrading.com (collection « LucidFlex », articles Evaluation, Funded, Payouts, Consistency, Scaling Plan, Drawdown, Customization, Allowed Trading Times) :

- **Éval 50K** : objectif +3 000 $ ; perte max (MLL) 2 000 $ en fin de séance sous le plus haut solde de clôture, **bloquée à +100 $** dès que le solde dépasse +2 100 $ ; consistance : meilleur jour ≤ 40 % du profit (50 % en option) ; 4 minis ou 40 micros max ; pas de limite de temps. Prix affiché 115 $ (80,50 $ avec coupon) ; option 50 % supposée à +15 $ (prix non lu).
- **Financé** : même MLL (2 000 $, bloquée à +100 $ au-delà de +2 100 $, et ramenée à +100 $ dès le premier payout) ; pas de consistance ; scaling : 2 minis / 20 micros sous 1 000 $ de profit, 3 / 30 de 1 000 à 1 999 $, 4 / 40 au-delà (mis à jour en fin de séance). Payout : 5 jours à ≥ 150 $ de profit dans le cycle et profit net du cycle > 0 ; montant = 50 % du profit, plafonné à 2 000 $, minimum 500 $ ; 90 % au trader ; 5 payouts puis passage en réel (**le compte réel n'est pas valorisé** : la simulation s'arrête au 5e payout, prudent).
- Limite journalière (DLL 1 200 $) : option « ON » retenue (moins chère, payouts à la demande) ; elle ne mord pas avec un seul trade par nuit dont le risque est ≤ 1 000 $.
- Horaires : positions fermées à 16:45 ET, reprise à 18:00 ET ; le trade 20:00 → 9:30 tient dans une séance, il est autorisé.

Simulation :
- Mêmes 3 787 trades qu'à l'avenant C, en **MNQ** (2 $ le point) : nombre de contrats = plancher(risque visé / (stop en points × 2 $)), plafonné par la taille max (éval 40, financé selon le scaling) et par la marge avant la MLL ; nuit sautée si 0 contrat ; éval ou compte abandonné si la marge ne permet plus 1 contrat. Stop en points = distance du stop × prix brut d'entrée (série `recolte1.engine.load`, historique 2010 activé).
- Coût par MNQ et par aller-retour : demi-spread d'entrée + demi-spread de sortie réels (bbo-1m, colonnes MNQ, sinon NQ ; 0,50 $ le tick) + **1,50 $ de commission** (hypothèse de la session précédente, non publiée par Lucid).
- Grille : risque visé par trade en éval ∈ {200 ; 400 ; 600 ; 800 ; 1 000} $, en financé ∈ {200 ; 400 ; 600 ; 800 ; 1 000} $. **Résultat principal** : éval 400 $, financé 200 $ (même proportion de la perte max que l'éval 2 % / financé 1 % de FTMO), consistance 40 %, 2011-07 → 2026-08.
- Contrôles : R − moyenne (sans edge) et 2011-2015 seul, comme à l'avenant C ; variante consistance 50 % à 130 $.
- 20 000 comptes par réglage, départ tiré au hasard dans l'historique, trades enchaînés dans l'ordre.
