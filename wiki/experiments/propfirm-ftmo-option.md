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
- **Chemin simulé** ([run_propfirm_paths.py](../../run_propfirm_paths.py)) : commencer en 100k (retour en 10k si la trésorerie ne paie plus l'éval) rapporte plus que les paliers dans 97 % des départs (+148 k$ contre +67 k$ à 3 ans en médiane), pour au pire 3 124 $ de sa poche ; 10k → 100k avec la règle de réserve est toujours plus lent.
- 10k puis 100k dès que les gains des 10k paient 2 trios d'évals 100k (3 293 $) : bascule ~13 mois, +93 k$ médiane à 3 ans (paliers +67 k$), apport en plus des 1 750 $ nul dans 99 % des départs.
- Départ avec un seul 10k : 650 $ couvrent le pire historique (7 évals ratées, signal 20:00) ; 1 × 10k → 1 × 100k → trio 100k : +100 k$ médiane à 3 ans mais apport dans 28 % des départs (≤ 3,5 k$) ; trio 10k d'abord : +76 k$, apport rare. [run_propfirm_start1.py](../../run_propfirm_start1.py)
- Règle stricte (palier seulement quand les rewards couvrent le pire chemin du palier suivant : 1×10k 608 $, 3×10k 1 738 $, 1×100k 3 842 $, 3×100k 10 978 $) : jamais d'apport, mais lent ; meilleur chemin 1×10k → 3×10k → 3×100k, +15,7 k$ médiane à 3 ans, trio 100k atteint dans 24 % des départs.
- Même règle au 95e centile (départ 450 $ ; seuils 1×100k 2 745 $, 3×10k 1 043 $, 3×100k 6 587 $) : apport au pire 158 $ ; 1×10k → 1×100k → 3×100k +55 k$ médiane à 3 ans (5e c. +3,6 k$) ; 1×10k → 3×10k → 3×100k +32 k$ (5e c. +8,7 k$).
- **Plan de montée en taille** : [[reports/plan_scaling_ftmo]] — trio 19h/20h/21h de 10k à 100k, on monte quand les rewards couvrent le pire creux du palier suivant ; plafond FTMO 400k par trader ou stratégie (4 × 100k), ~+90 k$/an en moyenne historique (optimiste).
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
