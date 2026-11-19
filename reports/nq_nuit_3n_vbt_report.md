# NQ overnight long 20:05 → 03:00 ET, filtre 3 nuits : backtest refait avec vectorbt

Date : 2026-11-03. **Exploratoire, hors compteur** : on refait un backtest externe sans rien choisir. Script : [run_nq_nuit_3n_vbt.py](../run_nq_nuit_3n_vbt.py). Sorties : `results/nq_nuit_3n/` (version corrigée) et `results/nq_nuit_3n/replique/` (séances calculées comme dans l'original). Données : NQ.v.0 Databento 1 min non ajusté, 2016-01-03 → 2026-08-28 ; le holdout postérieur au 2026-08-28 n'est pas touché.

Source : `scripts_strategies_NQ.zip` (transmis le 2026-11-03 : `bt_overnight_long.py`, `sl_atr_overnight_long.py`, `sl2atr15_overnight_long.py`, `oos_overnight_long.py`) et le rapport d'origine (artefact « Rapport NQ overnight », généré le 02/11/2026).

## Règles (reprises telles quelles)

- Long 1 NQ à l'open de la barre 5 min de 20:05 ET, sortie à l'open de la barre de 03:00 ET (même séance CME).
- **3n** : on ne prend la nuit que si la somme des rendements des 3 nuits précédentes est ≤ 0 bps. **REF** : toutes les nuits.
- **SL** : stop à 2 × ATR(14) Wilder sur barres 15 min (dernière barre terminée à 20:00), vérifié sur les plus bas 5 min ; fill au stop, ou à l'open en cas de gap.
- 20 $ par point, 15 $ l'aller-retour. 1 R = 2 × ATR M15 pour toutes les variantes. IS = 2016-2024, OOS = 2025 → 28/08/2026.

Le script est réécrit de zéro. vectorbt (`Portfolio.from_signals`, prix réels, `sl_stop`) fait toute l'exécution ; une boucle à la main, copie de la règle d'origine, sert de contrôle trade par trade.

## 1. Réplique : on retrouve les chiffres d'origine

Avec les séances calculées comme dans l'original (mode `--replique`), sur les 12 couples variante × période du rapport, Sharpe, max DD, profit factor, E[R] et t NW sont **identiques à 0,01 près**. Sur 2025-2026, le P&L est identique au dollar près (3n 03h : 34 890 $/an ; 3n 03h SL : 32 103 $/an). Sur 2016-2024, il y a une nuit de plus chez nous (2 314 trades au lieu de 2 313), parce que l'original lisait un autre fichier 5 min pour cette période ; l'effet est ≤ 0,1 % sur le P&L.

Les sorties vectorbt sont les mêmes que celles de la boucle sur tous les trades (0 écart, mêmes 676 / 259 / 146 / 54 stops).

## 2. Deux défauts trouvés en chemin

1. **Nuits perdues au changement d'heure (bug de l'original).** La séance est calculée par `index.normalize() + 1 jour` sur un index tz-aware. Le dimanche du passage à l'heure d'hiver, minuit + 24 h = 23:00 le dimanche, et la nuit du dimanche au lundi disparaît. Cela fait 11 nuits sur 2016-2026, dont 9 sur l'IS et 1 sur l'OOS. Corrigé ici avec la date locale naïve + 1 jour. *(Ma première version avait l'erreur inverse : elle perdait les lundis de mars.)*
2. **Piège vectorbt pour les sorties à l'open.** Sur la barre de sortie, vectorbt teste le stop sur tout le range de la barre (haut/bas) **avant** d'exécuter la sortie à l'open. Il « stoppe » donc des trades qui sont en réalité sortis à 03:00 au-dessus du stop. Cela touchait 31 trades sur l'IS (jusqu'à 47 points chacun), et coûtait 0,05 de Sharpe à REF SL sur l'IS et 0,08 à 3n SL sur 2022-2024. Corrigé en ramenant le haut et le bas de la barre de 03:00 à son open. À retenir pour tout backtest vectorbt avec stop et sortie à l'open.

## 3. Version corrigée (toutes les nuits) vs rapport d'origine

| Variante · période | Trades (orig.) | Net $/an (orig.) | Sharpe (orig.) | Max DD $ (orig.) | PF (orig.) | t NW (orig.) | E[R] |
|---|---|---|---|---|---|---|---|
| REF 03h · IS | 2 323 (2 313) | 9 756 (9 393) | 0,66 (0,63) | 19 040 (19 200) | 1,15 (1,14) | 2,32 (2,24) | 0,04 |
| REF 03h SL · IS | 2 323 (2 313) | 7 303 (6 927) | 0,57 (0,54) | 12 550 (12 550) | 1,11 (1,11) | 2,01 (1,92) | 0,03 |
| 3n 03h · IS | 984 (982) | 13 814 (13 594) | 1,33 (1,29) | 20 510 (20 165) | 1,55 (1,53) | 3,91 (3,74) | 0,14 |
| **3n 03h SL · IS** | 984 (982) | 12 097 (12 142) | **1,36 (1,36)** | 12 418 (12 073) | 1,49 (1,49) | 4,39 (4,35) | 0,13 |
| 3n 03h · 2016-2021 | — | 16 837 (16 394) | 1,95 (1,86) | 8 545 (8 545) | 1,97 (1,91) | 4,31 (4,00) | 0,20 |
| 3n 03h SL · 2016-2021 | — | 13 385 (13 335) | 1,67 (1,65) | 4 870 (4 870) | 1,71 (1,70) | 4,41 (4,32) | 0,17 |
| 3n 03h · 2022-2024 | — | 7 775 (8 004) | 0,59 (0,60) | 20 510 (20 165) | 1,19 (1,19) | 1,09 (1,12) | 0,02 |
| 3n 03h SL · 2022-2024 | — | 9 524 (9 760) | 0,91 (0,93) | 12 418 (12 073) | 1,26 (1,26) | 1,70 (1,74) | 0,05 |
| REF 03h · OOS | 428 (427) | 12 203 (13 211) | 0,36 (0,39) | 33 895 (33 895) | 1,07 (1,07) | 0,58 (0,63) | 0,01 |
| REF 03h SL · OOS | 428 (427) | 25 932 (26 862) | 0,93 (0,96) | 16 626 (16 626) | 1,16 (1,17) | 1,48 (1,54) | 0,05 |
| 3n 03h · OOS | 182 (181) | 32 380 (34 890) | 1,44 (1,57) | 10 605 (10 605) | 1,48 (1,53) | 2,07 (2,24) | 0,16 |
| **3n 03h SL · OOS** | 182 (181) | 31 245 (32 103) | **1,59 (1,63)** | 8 301 (8 301) | 1,50 (1,52) | 2,17 (2,25) | 0,14 |

Sharpe = P&L $ par jour de sortie, jours sans trade à 0, × √252 (mesure du rapport d'origine). Max DD sur l'equity des trades, départ à 0. Détail complet, stats vectorbt (`Trades.stats()`, `Returns.stats()` d'un compte de 100 000 $) et P&L par année : `results/nq_nuit_3n/run.log`.

**Lecture.** La correction des nuits change peu de chose. Sur l'IS, elle améliore légèrement les chiffres (3n SL : Sharpe 1,36 inchangé, t NW 4,39). Sur l'OOS, elle les baisse un peu : 3n sans stop passe de 1,57 à 1,44, 3n SL de 1,63 à 1,59. La nuit OOS ajoutée (lundi 2025-11-03, −31 bps) n'est pas prise par 3n, mais elle entre dans la somme des 3 nuits suivantes et change leur signal. La version retenue par l'original (3n, 03h, SL 2 × ATR M15) **tient** : Sharpe 1,36 IS / 1,59 OOS, max DD 12 418 $ / 8 301 $.

## 4. Ce qui ne change pas (limites déjà dans le rapport d'origine, confirmées)

- **Le filtre est intermittent.** Sur 2022-2024, 3n sans stop fait t 1,09 et Sharpe 0,59, pas mieux que REF (0,54). En 2023, toutes les variantes perdent.
- **Le filtre a été choisi** parmi plusieurs candidats (ATR, range, nuit précédente, 3 nuits, rendement de la journée). Les t ci-dessus ne sont pas corrigés pour cette sélection, et aucun DSR n'est calculé ici.
- **L'OOS ne fait que 20 mois.** Son t NW est d'environ 2,1-2,2, et 2026 seul pèse la moitié du P&L.
- **Le stop sert surtout de plafond de perte.** La pire nuit passe de −12 715 $ à −3 629 $, mais l'E[R] reste à peu près le même (0,13 sans stop contre 0,14 avec, sur l'IS).
- **Le coût est fixé à 15 $ l'aller-retour**, plus que notre [[wiki/concepts/cout-standard|coût standard]] (1 tick + 5 $ = 10 $ sur NQ) : c'est donc prudent. Le coût réel de nuit reste à vérifier avec les spreads bbo-1m, comme pour la règle NQ de nuit ([[reports/couts_reels_nq_nuit_report]]).

## 5. Lien avec nos travaux

- Il s'agit d'une autre [[wiki/concepts/prime-de-nuit|prime de nuit]] conditionnée. Elle diffère de la [[wiki/experiments/nq-nuit-momentum|règle NQ de nuit]] (momentum 12-1, 20:00 → 9:30) : signal de **retour à la moyenne** sur 3 nuits, sortie à 03:00, long seul.
- Le n° 13 avait testé « nuit précédente < 0 » comme filtre à plat sur la règle NQ de nuit, sans battre le hasard. Ce test ne dit rien du 3n ici : la règle, les horaires et le critère (drawdown) diffèrent.
- Avant toute combinaison avec la règle de nuit, il faut vérifier la corrélation des P&L : les fenêtres se recouvrent de 20:05 à 03:00.
