---
type: experiment
updated: 2026-10-31
status: done
verdict: EV positive sans edge (si les rewards sont versés)
prereg: [18]
trials: 0
---

# Prop firm comme option : FTMO 1-Step avec des trades au hasard

**Une phrase** : la perte d'une tentative est plafonnée au prix de l'éval alors que le compte financé paie sans plafond ; avec des trades NQ au sens tiré au hasard, entrée 9:50 ET, stop 1 ATR M15 et spread 1,5 point (avenant B), l'EV vaut ≈ +161 $ par éval 10k et ≈ +1 933 $ par éval 100k (41 % de passage, financé 6 % du capital, éval ~8,5 jours).

## Résultat
- **Avenant E refait avec vectorbt** (marché simulé par `Portfolio.from_signals` sur les barres 1 min, spread dans les frais ; règles FTMO en Python) : mêmes chiffres (EV +1 009 $ / 10k, 6 évals ratées, 239 nuits sans reward en 2022) ; un seul événement de la trace historique décalé (2023-11). [run_propfirm_vbt.py](../../run_propfirm_vbt.py)
- **Avenant E, financé en RR 2** (1 % risqué, TP 4 ATR) : financé 21,2 % du capital (contre 18,8 % en RR 2,5), P(reward) 86 %, 4,8 rewards ; EV **+1 009 $ (10k), +10 408 $ (100k)**. Pires séries : 6 évals ratées (2023-08 → 2023-11), 11 mois sans reward (2022). [run_propfirm_rr2.py](../../run_propfirm_rr2.py)
- **Avenant D, LucidFlex 50K en MNQ** (éval 400 $, financé 200 $, consistance 40 %, 115 $, stop au niveau actuel du NQ) : passage 39,5 %, financé 690 $, EV **+157 $** par éval (sans edge −55 $ ; prix historiques comme au protocole +65 $). Bien moins que FTMO : objectif > perte max, consistance 40 %, et le financé meurt vite (payout = 50 % du profit, plancher ramené à +100 $). [run_propfirm_lucid.py](../../run_propfirm_lucid.py), `results/propfirm_lucid/`.
- **Avenant C, règle NQ de nuit** (éval 2 %, financé 1 %, 1,5 pt) : passage 50,8 %, financé 18,5 % du capital, EV **+853 $ (10k), +8 849 $ (100k)** ; même flux sans edge : +98 $ / +1 295 $. Sans RAZ de la perte max : +307 $ / +3 390 $. Chiffres 2011-2026 optimistes (règle choisie sur 2016-2026). [run_propfirm_nq_nuit.py](../../run_propfirm_nq_nuit.py), `results/propfirm_nq_nuit/`.
- Avenant B : à 9:50, 1 ATR M15 ≈ 0,144 % du prix ; spread 1,5 pt = 0,041 R/trade (1 pt : +187 $ / +2 187 $). Spread du CFD après 9:30 non mesurable ici (le future NQ reste à 0,5 pt).
- Avenant A, entrée 9:35 et coût 1 pb : stop 1 ATR M15 (≈ 0,12 % du prix à 9:30) : le spread (1 pb) coûte 0,083 R par trade et divise l'EV par ~2 ; sans coût, ce stop ferait +3 000 $ sur 100k (diagnostic exploratoire). **Le spread réel FTMO US100 est l'hypothèse décisive.**
- Vraies trajectoires NQ ≈ pile ou face binaire : la convexité ne dépend que du rapport perte max / objectif (10 % / 10 %).
- Le stop en % du prix fixe la durée (0,5 % → ~15 jours par éval ; 1 % → ~35 jours et moins de passage).
- Exploratoire, un signal par compte (19:00 / 20:00 / 21:00) : rentrées plus régulières (mois sans reward 58 % → 42 %, corrélation trimestrielle 1,00 → 0,56, creux −300 $ → −238 $) mais écart-type sur 2 ans inchangé (~1 880 $ par compte) ; borne indépendante 1 101 $. [run_propfirm_farm_heures.py](../../run_propfirm_farm_heures.py)
- Exploratoire, pires séries FTMO + règle de nuit (10k) : 6 évals ratées d'affilée au pire (521 $, 2023-08 → 2023-11) ; jusqu'à **~11 mois sans reward** (2018-03 → 2019-01), surtout parce que le financé ne paie pas : un TP fait +2,5 % en une nuit, donc la règle du meilleur jour (50 %) exige ≥ +5 % avant un reward. [run_propfirm_streaks.py](../../run_propfirm_streaks.py)
- Exploratoire : décaler plusieurs comptes sur la même règle ne lisse pas la variance (écart-type ~2 000 $ par compte sur 2 ans, contre ~870 $ pour des comptes indépendants) : un mauvais passage les tue ensemble et ils se resynchronisent (4,1 sur 5 rachètent la même nuit, corrélation 0,97). [run_propfirm_farm.py](../../run_propfirm_farm.py)
- Remise à zéro de la perte max après un reward : **vérifiée sur ftmo.com le 31 octobre**, c'est la règle du 1-Step (« fully resets ») ; le « does not reset » de la même page concerne l'Instant Account. Les autres règles du simulateur correspondent aussi (voir le rapport, section « Règles FTMO vérifiées »).
- Risque non modélisé : refus de reward / bannissement (account rolling interdit chez FTMO). Seuil de refus qui annule l'EV : 65 % (10k), 78 % (100k) avec l'avenant B.
- Branche git `propfirm-ftmo`. Hors compteur d'essais (évaluation d'un contrat, pas d'une règle de marché).

## Sources brutes
[[PREREGISTRATION_18]] · [[reports/prereg18_report]] · [run_propfirm_ftmo.py](../../run_propfirm_ftmo.py) · [propfirm/](../../propfirm/) · `results/propfirm/` · session « Hedge sim discussion » (scripts `ftmo_sim.py`, `ftmo_funded_cmp.py`, hors dépôt)
