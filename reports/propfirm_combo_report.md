# FTMO 1-Step : 3n + M2 combinées, un trade par jour, éval 2,5 % et financé 1 %, objectif à 2 R

*2026-11-04. **Exploratoire, hors compteur** (évaluation d'un contrat sur des trades existants). Script : [run_propfirm_combo.py](../run_propfirm_combo.py). Sorties : `results/propfirm_combo/` (`run.log`, `trades_tp2.csv`, `ftmo.csv`). 20 000 comptes par bibliothèque, graine 1826.*

## Réglages

- **Trades.** 3n (20:05 → 03:00 ET, stop 2 × ATR M15) et M2 (9:35 → 15:55, stop 4 × ATR M15), recalculés avec vectorbt et **un objectif à 2 R** (4 ATR M15 pour 3n, 8 ATR M15 pour M2). Contrôle par une boucle à la main : 0 écart pour 3n ; 3 trades M2 diffèrent par période, à cause d'un stop ou d'un objectif touché dans la barre d'entrée.
- **Un trade par jour.** Si 3n a tradé la nuit qui se termine le matin du jour J, on ne prend pas M2 le jour J.
- **Moteur du n° 18** (`propfirm.ftmo`). Un trade = une journée FTMO. Coût CFD de 1,5 point au niveau actuel du NQ. Éval : **2,5 %** risqués par trade ; financé : **1 %**. Perte max 10 %, perte du jour 3 %, règle du meilleur jour à 50 %, reward tous les 10 trades, partagé à 90 %, perte max remise à zéro après chaque reward.

## Résultats

| Bibliothèque | Trades/an | R brut moyen | Passage | Durée de l'éval | Valeur du financé | Vie du financé | **EV 10k** | **EV 100k** | **EV par mois d'emplacement (100k)** |
|---|---|---|---|---|---|---|---|---|---|
| **Combiné 2016-2026** | 168 | +0,145 | 60,3 % | 13 trades ≈ 0,9 mois | 36,7 % | 22 mois | **+2 123 $** | **+21 546 $** | **+1 477 $** |
| Combiné 2016-2026, sans edge | 168 | 0 | 33,5 % | 1,0 mois | 5,4 % | 7 mois | +95 $ | +1 270 $ | +372 $ |
| 3n seul 2016-2026 | 110 | +0,151 | 62,7 % | 1,7 mois | 39,8 % | 31 mois | +2 407 $ | +24 386 $ | +1 159 $ |
| M2 seul 2016-2026 | 100 | +0,153 | 54,8 % | 1,2 mois | 21,2 % | 15 mois | +1 073 $ | +11 046 $ | +1 164 $ |
| mom, TP 2 R (référence) 2016-2026 | 251 | +0,100 | 43,9 % | 0,4 mois | 16,3 % | 6 mois | +626 $ | +6 583 $ | **+1 989 $** |
| **Combiné 2010-2015** (hors échantillon des deux règles) | 151 | +0,108 | 52,3 % | 1,1 mois | 18,9 % | 18 mois | **+904 $** | **+9 363 $** | +876 $ |
| Combiné 2010-2015, sans edge | 151 | 0 | 31,7 % | 1,2 mois | 4,2 % | 8 mois | +47 $ | +793 $ | +210 $ |
| 3n seul 2010-2015 | 102 | +0,144 | 73,0 % | 2,0 mois | 31,1 % | 36 mois | +2 180 $ | +22 123 $ | +773 $ |
| M2 seul 2010-2015 | 82 | +0,091 | 53,6 % | 1,7 mois | 19,6 % | 36 mois | +963 $ | +9 953 $ | +474 $ |

Pour le combiné 2016-2026 : P(reward) 95 %, 8,4 rewards par compte financé, premier reward après environ 1,4 mois. La part de trades qui atteignent l'objectif de 2 R est de 7,5 % pour 3n et de 23 % pour M2 ; 27 % et 46 % touchent le stop.

## Lecture

1. **Par tentative, le combiné vaut environ 2 100 $ (10k) ou 21 500 $ (100k) sur 2016-2026.** C'est 3,4 fois mom au même réglage. C'est un peu moins que 3n seul, car la règle d'un trade par jour retire des M2 bons en moyenne, et parce que M2 a plus de stops.
2. **Par mois d'emplacement, le combiné fait mieux que chaque stratégie seule** (+1 477 $ contre environ +1 160 $), car il trade plus souvent (168 trades par an). Mais il reste **sous mom** (+1 989 $), qui trade chaque nuit.
3. **Sur 2010-2015, l'avantage du combiné fond de moitié environ** (+904 $ par tentative ; +876 $ par mois). Il reste nettement au-dessus du même flux sans edge (+47 $). En FTMO, le coût est compté au prix actuel (0,02 R par trade) et non au prix de l'époque (0,1 R). Il n'y a donc pas de contradiction avec l'échec des n° 24 et 25. La prime de nuit et le léger signal de sens de M2 suffisent sur un CFD bon marché, même si les filtres eux-mêmes n'ont pas été validés.
4. **Réserves :**
   - La période 2016-2026 est celle où les deux règles ont été choisies. Le chiffre réaliste se situe entre la ligne 2010-2015 et la ligne 2016-2026.
   - La **règle FTMO des annonces** n'est pas modélisée. 3n n'est jamais exposé (à plat à 03:00), mais M2 garde la position pendant les annonces de 10:00 et de 14:00 (FOMC). Un stop ou un objectif touché à moins de 2 minutes d'une annonce majeure ferme le compte financé.
   - Le moteur arrête un compte financé à 500 trades, soit environ 3 ans ici. Le partage des rewards est supposé sans refus. Le spread réel du CFD n'est pas mesuré.
