# Règle matinée US sur NQ avec SL/TP en ATR M15 (1/1 et 2/2)

*2026-11-01. Exploratoire, non pré-enregistré, demandé en séance. Compteur global : 1 555 → 1 559 (2 réglages de stops × 2 filtres ; la référence sans stop est un recalcul). Code : [run_nq_matin_sltp.py](../run_nq_matin_sltp.py). Sorties : `results/nq_matin_sltp/` (run.log, summary.csv, trades.csv, by_year.csv).*

Cadre : la règle a échoué sur ES et YM ([[reports/prereg20_report]]) et elle est au [[wiki/Failed Ideas/ledger|registre des échecs]]. Ce test sur NQ, les données où elle a été trouvée, ne la rouvre pas.

## Règle testée

- **Signal et entrée** : matinée X = 9:30 → 11:30 NY sur NQ. Si |X| > 1 écart-type des 20 séances précédentes, entrée à 11:30 dans le sens de X (clôture de la barre 11:29).
- **Sortie** : 16:00, sauf stop touché avant.
- **Stops** : ATR de Wilder 14 sur bougies 15 min, dernière bougie terminée à 11:30. ATR médian 12,5 points NQ (p10 4,3 ; p90 51,7).
  - SL 1 / TP 1 ATR (RR 1) ;
  - SL 2 / TP 2 ATR ;
  - référence sans stop.
- **Filtres** : chaque réglage est testé avec |z| > 1 et sans filtre (tous les jours).
- **Moteur** : vectorbt `from_signals` sur barres 1 min, stops sur high/low, SL prioritaire si SL et TP sont touchés dans la même minute. Net 1 tick + 5 $ (0,5 point). NQ 2010-07 → 2026-08-28.

La référence sans stop donne +4,8 bp net contre +5,8 bp dans [[reports/nq_matin_aprem_report]]. L'écart vient de la fenêtre glissante de 20 séances, calculée ici sur les seules séances valides : 1 255 trades contre 1 215.

## Résultats (net)

| Réglage | Filtre | Trades | bp/trade [IC 95 %] | t | 2010-17 | 2018-26 | 2023-26 | Sharpe | Max DD (bp) | Gagnants | TP / SL / 16:00 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SL 1 / TP 1 ATR | \|z\| > 1 | 1 255 | +1,3 [−0,2 ; +3,0] | 1,6 | +0,6 | +1,9 | +3,1 | 0,41 | −726 | 54 % | 54 / 45 / 1 % |
| **SL 2 / TP 2 ATR** | \|z\| > 1 | 1 255 | **+4,8 [+2,1 ; +7,7]** | **3,3** | −0,4 | +9,0 | +5,5 | **0,83** | −1 174 | 56 % | 45 / 36 / 20 % |
| sans stop | \|z\| > 1 | 1 255 | +4,8 [+0,3 ; +9,5] | 2,0 | +0,3 | +8,4 | +9,7 | 0,49 | −2 013 | 55 % | — / — / 100 % |
| SL 1 / TP 1 ATR | aucun | 4 003 | +0,2 [−0,6 ; +1,0] | 0,4 | −0,6 | +0,8 | +1,4 | 0,11 | −1 539 | 53 % | 52 / 47 / 1 % |
| SL 2 / TP 2 ATR | aucun | 4 003 | +1,3 [−0,1 ; +2,7] | 1,8 | −1,4 | +3,6 | +3,0 | 0,44 | −3 725 | 53 % | 42 / 38 / 20 % |
| sans stop | aucun | 4 003 | +2,4 [+0,3 ; +4,7] | 2,1 | −1,0 | +5,4 | +4,1 | 0,52 | −3 936 | 52 % | — / — / 100 % |

Le Sharpe est annualisé avec le vrai nombre de trades par an (≈ 78 avec le filtre, ≈ 250 sans). En brut, SL 1 / TP 1 avec le filtre fait +2,2 bp : le coût mange 0,9 bp par trade, soit 40 % du gain. Source : `results/nq_matin_sltp/summary.csv`, `run.log`.

## Lecture

1. **RR 1 (SL 1 / TP 1 ATR) : non.** Le stop d'1 ATR (≈ 12 points) est touché dans l'heure, et 99 % des trades sortent sur un stop. On ne garde plus que la direction des premières minutes après 11:30, alors que l'effet se construit sur tout l'après-midi. Le gain brut tombe à +2,2 bp, et le coût fixe pèse plus lourd sur un stop serré : +1,3 bp net, non significatif.
2. **SL 2 / TP 2 ATR : même gain moyen, moitié moins de risque.** Le gain par trade est identique à la référence (+4,8 bp), mais l'écart-type est deux fois plus faible. Le t passe de 2,0 à 3,3, le Sharpe de 0,49 à 0,83 et le drawdown de −2 013 à −1 174 bp. C'est le même constat que pour la règle de nuit (n° 12, [[reports/prereg12_report]]) : les stops ne créent pas d'edge, ils coupent les queues.
3. **Tout le gain est après 2018.** Sur 2010-2017, toutes les variantes sont à ≈ 0 (de −0,4 à +0,6 bp avec le filtre). Les années 2018, 2021, 2022 et 2025 font l'essentiel (`by_year.csv`).
4. **Le filtre |z| > 1 reste utile** quel que soit le stop : sans lui, les gains par trade sont 2 à 4 fois plus faibles.

## Ce que ça ne change pas

- Le meilleur t (3,3) reste sous le maximum attendu par hasard avec N ≈ 1 559 essais (√(2 ln N) ≈ 3,8). Il est obtenu sur les données mêmes où la règle a été choisie, après deux tris (fenêtre, seuil) et maintenant un choix de stop.
- La version figée a échoué sur ES et YM. [[PREREGISTRATION_20]] interdit d'en changer la sortie après calcul et ne permet de rouvrir l'idée qu'avec une mesure de gamma. Tester SL 2 / TP 2 sur ES et YM maintenant serait donc un nouveau tri sur des données déjà vues, pas une validation.

## Conclusion

Sur NQ, SL 1 / TP 1 ATR détruit la règle. SL 2 / TP 2 ATR garde le gain moyen (+4,8 bp/trade net) et divise le risque par deux (Sharpe 0,83 contre 0,49), mais seulement sur 2018-2026 et dans l'échantillon de sélection. Aucune règle retenue ; la ligne du registre (n° 20) reste valable.
