# Momentum de fin de séance après un grand mouvement (ETF à levier, Shum et al., SSRN 2161057) : rapport

*Protocole : [PREREGISTRATION_9.md](../PREREGISTRATION_9.md), commit `d2a1956`, antérieur à tout calcul de P&L. Code : `letf/`, `asym/metrics.py`, `run_letf.py`, tests `tests/test_letf.py` (commits `9d370df`, `59d2493`). Sorties : `results/letf/` (`run.log`, `metrics_full.csv`, `vbt_summary.csv`, trades, `equity.png`). **16 nouveaux tests, compteur à 224.***

**Données.** Futures ES et NQ, 1 minute, ajustés en ratio aux roulements, 2016-01 → 2026-08. Tout l'échantillon est postérieur à celui du papier (2006-2011).

**Règle.** r = P(T) / C_{t−1} − 1. Si |r| ≥ s, on suit le mouvement de l'open de T au close de 15:59. Exécution vectorbt 1×, au coût de 1 tick + 5 $.

## Verdict : ❌ (rejeté) pour la configuration principale

| | ES 14:30, s = 2 % (principale) | NQ 14:30, s = 2 % (réplication) |
|---|---|---|
| Trades (jours déclencheurs) | 122 (46 en 2020, 31 en 2022) | 255 |
| Moyenne nette par trade | +6,6 pb | **+12,2 pb** |
| Deux moitiés positives | ✅ (+7,1 / +6,0 pb) | ✅ (+18,2 / +7,7 pb) |
| Bootstrap p | 0,25 ❌ | 0,048 ✅ |
| Permutation p | 0,17 ❌ | 0,017 ✅ |
| DSR (N = 16) | 0,24 ❌ | 0,75 ❌ |
| vectorbt : total / annuel / Sharpe / DD max | +7,5 % / +0,77 % / 0,19 / −7,4 % | +34,9 % / +2,95 % / 0,61 / −8,6 % |
| Hors 2020 | **−4,0 pb/trade** (n = 76) | +6,4 pb/trade (n = 203) |

Reality Check sur les 16 règles : p = 0,13. La meilleure règle est NQ 14:30, 2 %.

## Lecture

- **Sur ES, il n'y a rien.** Tout le gain vient de 2020 (+11,1 %). Hors 2020, la règle perd 4 pb par trade.
- **Sur NQ, l'effet est plus net**, ce qui colle au mécanisme : c'est sur le Nasdaq-100 que l'encours d'ETF à levier est le plus gros (TQQQ, SQQQ).
  - Il passe le bootstrap et la permutation et reste positif hors 2020 (+6,4 pb/trade).
  - Il échoue au DSR (0,75 pour N = 16).
  - Il reste concentré sur 2020 (+19,0 %) et 2022 (+6,6 %). Les années calmes sont proches de 0.
- **Le profil prédit par le papier est confirmé dans les deux marchés.**
  - Mieux vaut décider tôt : sur ES, 14:15 donne +11,2 pb et 15:30 +6,4 pb ; sur NQ, 14:30 donne +12,2 pb et 15:30 +4,2 pb.
  - Le seuil de 2 % rapporte plus par trade que celui de 1 % (ES 6,6 contre 1,5 pb ; NQ 12,2 contre 4,5 pb).
- **Taille.** Exposé environ 10 % des séances, à 1×, le meilleur cas (NQ) fait moins de 3 %/an. Le coût pèse peu : 12 pb de gain contre environ 0,3 pb de coût. Le problème n'est pas le coût mais la **rareté** des déclenchements et leur **concentration** sur deux années de crise.

## Métriques complètes (coût principal, période entière)

| Règle | Trades | Expo. | Total | CAGR | Vol | Sharpe | Sortino | DD max | Calmar | Gagnants | Moy. pb | PF | Années + |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ES 14:15, 2 % | 121 | 4,6 % | +13,6 % | +1,22 % | 3,9 % | 0,33 | 0,50 | −6,8 % | 0,18 | 53,7 % | +11,2 | 1,37 | 6/11 |
| **ES 14:30, 2 %** | 122 | 4,6 % | +7,5 % | +0,69 % | 4,0 % | 0,19 | 0,29 | −7,4 % | 0,09 | 54,9 % | +6,6 | 1,21 | 6/11 |
| ES 14:45, 2 % | 135 | 5,1 % | +4,4 % | +0,41 % | 3,8 % | 0,13 | 0,20 | −13,2 % | 0,03 | 50,4 % | +3,7 | 1,12 | 4/11 |
| ES 15:30, 2 % | 141 | 5,3 % | +8,8 % | +0,81 % | 3,3 % | 0,26 | 0,41 | −9,1 % | 0,09 | 50,4 % | +6,4 | 1,26 | 4/11 |
| ES 14:15, 1 % | 508 | 19,1 % | +9,9 % | +0,90 % | 5,3 % | 0,20 | 0,30 | −17,7 % | 0,05 | 49,2 % | +2,1 | 1,10 | 7/11 |
| ES 14:30, 1 % | 524 | 19,7 % | +6,6 % | +0,61 % | 5,1 % | 0,14 | 0,22 | −17,5 % | 0,03 | 47,9 % | +1,5 | 1,07 | 7/11 |
| ES 14:45, 1 % | 551 | 20,7 % | −8,4 % | −0,83 % | 4,8 % | −0,15 | −0,22 | −22,8 % | −0,04 | 45,9 % | −1,4 | 0,93 | 5/11 |
| ES 15:30, 1 % | 587 | 22,1 % | −5,5 % | −0,53 % | 3,9 % | −0,12 | −0,18 | −19,1 % | −0,03 | 46,0 % | −0,8 | 0,94 | 6/11 |
| NQ 14:15, 2 % | 257 | 9,7 % | +29,7 % | +2,50 % | 4,8 % | 0,53 | 0,87 | −6,9 % | 0,36 | 52,9 % | +10,6 | 1,43 | 6/11 |
| **NQ 14:30, 2 %** | 255 | 9,6 % | +34,9 % | +2,88 % | 4,9 % | 0,61 | 0,99 | −8,6 % | 0,34 | 56,1 % | +12,2 | 1,53 | 9/11 |
| NQ 14:45, 2 % | 271 | 10,2 % | +17,7 % | +1,56 % | 4,5 % | 0,36 | 0,57 | −8,3 % | 0,19 | 55,0 % | +6,4 | 1,27 | 6/11 |
| NQ 15:30, 2 % | 306 | 11,5 % | +13,0 % | +1,16 % | 3,7 % | 0,33 | 0,53 | −10,4 % | 0,11 | 50,0 % | +4,2 | 1,23 | 6/11 |
| NQ 14:15, 1 % | 818 | 30,8 % | +39,3 % | +3,19 % | 6,2 % | 0,54 | 0,83 | −14,6 % | 0,22 | 52,3 % | +4,3 | 1,22 | 6/11 |
| NQ 14:30, 1 % | 840 | 31,6 % | +42,7 % | +3,43 % | 6,2 % | 0,57 | 0,91 | −15,0 % | 0,23 | 51,9 % | +4,5 | 1,24 | 7/11 |
| NQ 14:45, 1 % | 851 | 32,0 % | +20,8 % | +1,81 % | 6,0 % | 0,33 | 0,50 | −17,8 % | 0,10 | 50,3 % | +2,5 | 1,13 | 6/11 |
| NQ 15:30, 1 % | 898 | 33,8 % | +4,3 % | +0,40 % | 4,6 % | 0,11 | 0,17 | −13,2 % | 0,03 | 48,0 % | +0,6 | 1,04 | 4/11 |

Le détail par moitié, avec gain et perte moyens, ratio gain/perte, meilleur et pire trade, asymétrie, kurtosis, plus long drawdown, ainsi que la grille de coûts de 0 à 5 pb, est dans `results/letf/run.log` et `metrics_full.csv`.

**Année par année (%)** :
- ES 14:30, 2 % : 2016 −3,1 · 2017 0,0 · 2018 −3,5 · 2019 +0,3 · **2020 +11,1** · 2021 −0,8 · 2022 +2,5 · 2023 +0,1 · 2024 −1,4 · 2025 +2,0 · 2026 +0,9.
- NQ 14:30, 2 % : 2016 −1,1 · 2017 +0,5 · 2018 +2,1 · 2019 +0,3 · **2020 +19,0** · 2021 +0,1 · **2022 +6,6** · 2023 +1,7 · 2024 −2,4 · 2025 +2,4 · 2026 +2,6.

## Conclusion

- La règle du papier ne réplique pas sur ES (la configuration principale). Le mécanisme laisse une trace dans le sens attendu : décider tôt vaut mieux, le seuil de 2 % vaut mieux que celui de 1 %, et c'est plus fort sur NQ, où l'encours d'ETF à levier est le plus gros.
- NQ 14:30, 2 % est le résultat le plus intéressant des quatre papiers testés depuis le n° 6 : +12 pb par trade, les tests simples passés, positif hors 2020. Mais il ne passe pas la correction pour multiplicité, et son rendement à 1× est faible parce que la règle est rarement active.
- Pour aller plus loin, il faudrait un nouveau pré-enregistrement centré sur NQ (et éventuellement RTY/SOXX, pas disponibles ici), sur des données nouvelles (2026-09+). On pourrait aussi pondérer par une estimation de l'encours des ETF à levier (stratégie « ETF » du papier, qui demande des données d'encours externes).
