# Compte financé FTMO : viser juste ce qui manque pour la règle des 50 %, puis attendre le reward ?

*2026-11-04. **Exploratoire, hors compteur.** Script : [run_ftmo_payout_policy.py](../run_ftmo_payout_policy.py). Sorties : `results/ftmo_payout_policy/` (`run.log`, `septembre.csv`, `historique.csv`).*

**Question de l'utilisateur.** Avec 1 % de risque et un objectif de 2 R, il faut environ +3,9 % de solde pour que le meilleur jour (environ +1,9 %) pèse moins de 50 % du gain. Quand il ne manque qu'un peu, faut-il ouvrir un trade à 1 % qui ne vise que ce qui manque, puis arrêter de trader jusqu'au 14e jour et demander le reward ? Ou faut-il continuer comme avant ?

**Quatre politiques** pour le compte financé (mom, 1 %, TP normal 4 ATR = 2 R) :
- **actuel** : on trade chaque nuit.
- **cible** : si le gain est positif et que seul le meilleur jour bloque (gain ≥ meilleur jour), le trade vise **2 × meilleur jour − gain + 0,01 %**. Il est atteint si le mouvement favorable maximal du trade (MFE) le dépasse.
- **attente** : dès que le gain est positif et la règle respectée, on ne trade plus jusqu'à la date du reward.
- **cible + attente** : les deux, c'est la proposition testée.

La règle du meilleur jour est **Consistency** (comptes commandés depuis le 12/10/2026, ≤ 50 % du gain net). La règle **Legacy** (≤ 50 % des seuls jours gagnants) est rapportée pour les comptes de septembre.

## 1. Le vrai septembre (éval 2,5 % avec objectif ramené au reste à faire)

Départ le 01/09, compte financé dès le 15/09, règle Consistency, politique **cible + attente** :

| Nuit | Trade | Solde |
|---|---|---|
| 15/09 → 18/09 | SL, SL, TP, TP | +1,85 % |
| 21/09 | TP | +3,78 % (meilleur jour 1,95 % > 50 % de 3,78 %) |
| **22/09** | **objectif réduit à 0,18 R (+0,14 %), atteint** (la nuit est montée à +1,15 R) | **+3,92 % : règle respectée** |
| 23/09 → 25/09 | attente, pas de trade | +3,92 % |
| **28/09** | **reward de 3,53 %** (14e jour après le 1er trade), nouveau compte | — |
| 28/09 → 03/11 | nouveau compte, même série perdante | −9,35 % (encore ouvert, plancher −10 %) |

Rewards au 03/11, en % du capital, pour les départs de septembre qui ont validé leur éval :

| Départ | Règle | actuel | cible | attente | cible + attente |
|---|---|---|---|---|---|
| 01/09 | Consistency | 0 | 3,53 | 0 | **3,53** |
| 03/09, 04/09 | Consistency | 0 | 3,53 | 0 | **3,53** |
| 08/09 | Consistency | 0 | 0 | 4,23 | **3,53** |
| 02/09, 09 → 18/09 (8 départs) | Consistency | 0 | 0 | 0 | 0 |
| 01/09 | Legacy | 2,45 | 0,77 | 3,40 | 1,73 |
| 03/09, 04/09 | Legacy | 2,43 | 2,43 | 1,60 | 1,60 |

Avec la règle actuelle (Consistency), la politique proposée transforme 4 départs sur 12 en un reward d'environ 3,5 % (353 $ en 10k, 3 530 $ en 100k), au lieu de 0. Avec la règle Legacy, elle n'aide pas : cette règle est déjà souple, et réduire le gain pour la respecter coûte de l'argent.

## 2. Sur tout l'historique de mom (20 000 comptes, éval à 2,5 % puis financé à 1 %)

| Période | Politique | P(≥ 1 reward) | Rewards / compte | Reward moyen | Valeur du financé | Vie | **EV 10k** | **EV / mois 100k** |
|---|---|---|---|---|---|---|---|---|
| 2016-2026 | actuel | 83,0 % | 3,7 | 4,33 % | 16,0 % | 6,4 mois | +707 $ | +2 044 $ |
| | cible | 84,1 % | 4,2 | 3,75 % | 15,6 % | 6,5 mois | +684 $ | +1 964 $ |
| | attente | 84,5 % | 4,5 | 4,03 % | 18,3 % | 7,2 mois | +820 $ | +2 137 $ |
| | **cible + attente** | **86,8 %** | **5,8** | 3,45 % | **20,2 %** | 7,8 mois | **+912 $** | **+2 201 $** |
| 2011-2015 | actuel | 90,2 % | 7,6 | 4,45 % | 33,6 % | 8,8 mois | **+1 936 $** | **+3 444 $** |
| | cible | 90,9 % | 8,0 | 3,98 % | 31,7 % | 8,7 mois | +1 820 $ | +3 251 $ |
| | attente | 91,4 % | 8,0 | 4,05 % | 32,2 % | 8,7 mois | +1 854 $ | +3 315 $ |
| | cible + attente | 93,2 % | 9,7 | 3,44 % | 33,5 % | 9,9 mois | +1 927 $ | +3 047 $ |

Avec l'attente, on ne trade que 91 à 94 % des nuits. Le délai de 14 jours est compté comme 10 nuits de bourse.

## Lecture

1. **La proposition marche quand la stratégie est moyenne ou mauvaise.** Sur 2016-2026, elle donne +29 % d'EV par tentative (+912 $ contre +707 $) et +8 % par mois d'emplacement. Les rewards sont plus petits (3,5 % contre 4,3 %), mais plus fréquents (5,8 contre 3,7 par compte), et plus de comptes touchent au moins un reward (87 % contre 83 %). Sur septembre-octobre 2026, elle aurait payé environ 3,5 % sur 4 départs sur 12, au lieu de rien.
2. **Elle coûte quand la stratégie est forte.** Sur 2011-2015 (mom à +0,19 R par nuit), l'EV par tentative ne change pas, et l'EV par mois baisse de 11 %. Arrêter de trader en attendant le reward, c'est renoncer à des nuits à espérance positive, et on encaisse des rewards plus petits.
3. **C'est l'attente qui fait l'essentiel du gain.** La cible seule fait un peu moins bien que la politique actuelle sur les deux périodes, parce qu'on continue de trader après avoir sécurisé et qu'on perd souvent le gain. Combinée à l'attente, elle sécurise le reward au moment où il devient possible.
4. **En pratique** :
   - avec la règle Consistency (comptes commandés aujourd'hui) et une stratégie dont l'edge est modeste ou incertaine (mom sur 2016-2026, Sharpe environ 0,9), **cible + attente** est préférable ;
   - si l'edge est forte, continuer à trader rapporte plus par mois.
5. **Limites** :
   - le MFE vient des barres de 1 min, barre du stop exclue ;
   - dans la simulation sur l'historique, le délai de 14 jours calendaires est approché par 10 nuits de bourse ;
   - le nouveau compte démarre la nuit qui suit le reward (FTMO met 1 à 2 jours ouvrés) ;
   - seul mom est testé, pas le trio.
