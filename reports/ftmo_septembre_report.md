# FTMO 1-Step avec mom, départ en septembre 2026 : rejeu sur les vraies nuits jusqu'au 2026-11-03

*2026-11-04. **Descriptif, hors compteur.** Script : [run_ftmo_septembre.py](../run_ftmo_septembre.py). Sorties : `results/ftmo_septembre/` (`run.log`, `journal_0109.csv`, `departs.csv`, `trades_mom_tp4.csv`).*

## Méthode

- **Données.** Fenêtre déjà vue du holdout (avenant A du n° 26), série Databento + LSE. Rien à partir du 2026-11-04.
- **Trades.** mom, avec l'objectif du plan FTMO : TP 4 ATR M15 = 2 R, R brut, recalculé avec vectorbt (`run_holdout_anticipe.h1_mom`). Sur la période, 44 nuits : 12 TP, 27 SL, R brut total −1,1.
- **Règles.** Celles du moteur du n° 18 :
  - éval : 2,5 % de risque par trade, objectif +10 %, perte max 10 % sous le plus haut, perte du jour 3 %, règle du meilleur jour ;
  - financé : 1 % de risque, reward tous les 10 jours, 90 % versés ;
  - coût CFD de 1,5 point ;
  - une éval ratée est rachetée dès la nuit suivante, et le compte financé démarre la nuit qui suit la validation (en réalité FTMO met 1 à 3 jours ouvrés).
- **Trous de données** : le 05/10 au soir et le 12/10. Les nuits concernées sont sautées.

## Départ le 1er septembre

| Date | Événement | Solde |
|---|---|---|
| 01/09 → 03/09 | 3 stops d'affilée | −7,5 % |
| 04/09 → 11/09 | 4 TP sur 5 nuits | +9,1 % |
| 14/09 → 16/09 | 3 stops | +1,6 % |
| 17/09 → 18/09 | 2 TP | **+11,25 % : éval validée en 13 nuits** |
| 21/09 | 1er trade financé, TP | +1,9 % (plus haut du compte) |
| 22/09 → 30/10 | 21 SL, 6 TP, 3 sorties à 9:30 | jusqu'à −7,65 % |
| 02/11 → 03/11 | risque réduit à 0,4-0,5 % près du plancher | **−8,08 % = plancher (+1,9 − 10) : compte perdu** |

Aucun reward n'a été versé. Le compte financé n'est jamais revenu au-dessus de 0 après le 25/09, alors qu'un reward suppose un gain positif au bout du cycle de 10 jours.

**Bilan au 03/11 :** 2 évals achetées (la 2e démarre le 04/11), 0 $ de rewards.
- Compte 10k : **−174 $** de frais.
- Compte 100k : **−1 098 $** de frais.

## Tous les jours de départ possibles en septembre (21 départs)

| Départ | Évals achetées au 03/11 | Rewards | Net 10k | Net 100k |
|---|---|---|---|---|
| 01/09 → 09/09, 11/09, 16/09, 17/09 (9 départs) | 2 (1 validée, financé perdu le 03/11) | 0 | −174 $ | −1 098 $ |
| 10/09, 14/09, 15/09, 18/09 → 29/09 (11 départs) | 4 (évals ratées) | 0 | −348 $ | −2 196 $ |
| 30/09 | 3 | 0 | −261 $ | −1 647 $ |

## Lecture

- **Septembre-octobre 2026 est une mauvaise période pour mom** : −1,1 R brut sur 44 nuits, avec 61 % de stops (contre 52 % en moyenne historique). Sur 15 ans, mom ne fait jamais −10 R sur une année. Mais un compte FTMO financé à 1 % saute dès −10 R sous son plus haut, et c'est ce qui s'est passé ici.
- **Ce résultat est dans la distribution attendue.** Sur 2016-2026, la simulation donnait 44 % de passage et une vie moyenne du financé d'environ 6 mois, avec 17 % des comptes financés sans aucun reward. Deux mois ne suffisent pas à juger : sur un emplacement, l'espérance se construit sur une trentaine d'évals.
- **Le coût de ce scénario reste borné aux frais** : 174 à 348 $ par emplacement de 10k sur la période.
