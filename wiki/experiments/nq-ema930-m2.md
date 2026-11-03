---
type: experiment
updated: 2026-11-03
status: abandoned
verdict: ❌ hors échantillon 2010-2012 (n° 25)
prereg: [25]
trials: 1734
---

# NQ intraday « close de 9:30 contre EMA12 », modèle M2 (stratégie transmise)

**Une phrase** : on suit le sens du close de 9:30 par rapport à l'EMA12, de 9:35 à 15:55, seulement les jours extrêmes (écart à l'EMA > 2,2 ATR M5, ou veille perdante de plus de 60 bps dans le sens du jour). Taille inverse à la volatilité. Refait avec vectorbt : Sharpe 1,28 sur 2016-2024 et 1,86 sur 2025 → 08/2026, t NW 4,05.

## Origine
Stratégie transmise le 2026-11-03 (`scripts_strategies_NQ.zip`, scripts `bt_ema930.py`, `explore_c_ema930.py` et `bt_m2_ema930.py`), reprise d'un post Discord. Les seuils de M2 viennent du post, dont les nombres de trades vont jusqu'en 2026.

## Tests
| Test | Résultat | Rapport |
|---|---|---|
| Backtest refait avec vectorbt (C, D, M2, taille, stop), comparé au rapport d'origine | Sans stop : **identique** à l'original (C, D, M2, M2 + taille, au dollar près, sur les 4 périodes) ; avec stop : +0,01 à +0,03 de Sharpe (2 trades à stop dans la barre d'entrée, vectorbt sort une barre plus tard) ; Trades M2 par année identiques au post (sauf 2020 : 123 contre 125) ; vectorbt = boucle (2 trades à stop dans la barre d'entrée diffèrent) ; M2 + taille : Sharpe 1,28 IS / 1,86 OOS ; C seul 0,62 / 1,57 | [[reports/nq_ema930_vbt_report]] |

| **N° 25 : hors échantillon NQ 2010-06 → 2012-12 (pré-enregistré)** | ❌ ÉCHEC : M2 +20,7 $/trade (5 bps), p 0,19 ; jours M2 ≈ jours exclus (p 0,45) ; M2 + stop +0,066 R (t 0,91) ; ES / YM p 0,04-0,05 avant correction | [[reports/prereg25_report]] |

## Ce qu'on sait
- C seul (tous les jours) est faible : Sharpe 0,62, t 1,96 sur 2016-2024, cohérent avec les échecs du momentum intraday (voir le registre). Le filtre M2 fait l'essentiel.
- Gains concentrés : les 10 meilleurs trades font 70 à 80 % du net sur 2022-2024 et 2025-2026.

## Ouvert
- Le n° 25 rejette M2 sur 2010-06 → 2012-12. Ne rouvrir que sur le holdout postérieur au 2026-08-28 (voir le registre des échecs).
- Hors échantillon 2025-26, le choix des jours par M2 n'est significatif qu'à 10 % (rapport d'origine).

## Sources brutes
[run_nq_ema930_vbt.py](../../run_nq_ema930_vbt.py), `results/nq_ema930/`.
