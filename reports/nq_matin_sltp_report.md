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

## Résultats en R (net)

1 R = la distance du SL : 1 ATR pour SL 1 / TP 1, 2 ATR pour SL 2 / TP 2. Pour la version sans stop, les deux unités sont données. Calcul à partir de `results/nq_matin_sltp/trades.csv`, colonne R ; IC par bootstrap par blocs (`recolte1.engine.ci_mean`).

| Réglage | Filtre | R/trade [IC 95 %] | R/an | Max DD (R) | R/an ÷ DD | Gagnants | Gain / perte moyens (R) | PF | 2010-17 / 2018-26 | Années + (2011-25) | Pire année (R) | Pire série de pertes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SL 1 / TP 1 ATR | \|z\| > 1 | +0,039 [−0,011 ; +0,088] | +3,0 | −29,4 | 0,10 | 54 % | +0,95 / −1,04 | 1,08 | +0,001 / +0,069 | 10 / 15 | −11,1 | 10 |
| **SL 2 / TP 2 ATR** | \|z\| > 1 | **+0,079 [+0,029 ; +0,128]** | **+6,1** | **−30,9** | **0,20** | 56 % | +0,85 / −0,90 | 1,20 | −0,011 / +0,151 | 9 / 15 | −5,2 | 9 |
| sans stop (1 R = 2 ATR) | \|z\| > 1 | +0,064 [−0,016 ; +0,142] | +5,0 | −47,4 | 0,11 | 55 % | +1,09 / −1,18 | 1,12 | −0,015 / +0,128 | 10 / 15 | −16,2 | 10 |
| sans stop (1 R = 1 ATR) | \|z\| > 1 | +0,128 [−0,031 ; +0,284] | +10,0 | −94,7 | 0,11 | 55 % | +2,19 / −2,37 | 1,12 | −0,029 / +0,255 | 10 / 15 | −32,3 | 10 |
| SL 1 / TP 1 ATR | aucun | +0,003 [−0,028 ; +0,034] | +0,7 | −86,2 | 0,01 | 53 % | +0,94 / −1,05 | 1,01 | −0,033 / +0,033 | 7 / 15 | −17,9 | 11 |
| SL 2 / TP 2 ATR | aucun | +0,022 [−0,008 ; +0,050] | +5,4 | −88,1 | 0,06 | 53 % | +0,85 / −0,91 | 1,05 | −0,034 / +0,069 | 10 / 15 | −33,5 | 10 |
| sans stop (1 R = 2 ATR) | aucun | +0,028 [−0,016 ; +0,074] | +6,9 | −104,6 | 0,07 | 52 % | +1,10 / −1,13 | 1,05 | −0,024 / +0,072 | 10 / 15 | −39,8 | 16 |

Pour comparaison, la règle NQ de nuit (SL 2 / TP 5 ATR) fait +0,088 R/trade, +22 R/an et un max DD de −25 R ([[reports/nq_nuit_sl_range_report]]).

En R, le gain moyen ne dépasse jamais la perte moyenne (+0,85 R contre −0,90 R en SL 2 / TP 2) : un TP au même niveau que le SL rapporte un peu moins d'1 R, et le stop coûte un peu plus d'1 R, à cause des frais et des sorties à 16:00. Tout l'edge tient au taux de réussite (56 % contre 50 % attendu pour un RR 1 au hasard). Le drawdown de −31 R vaut 5 ans de gains (+6,1 R/an), et tout le gain en R vient de 2018-2026.

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
