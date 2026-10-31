---
type: ledger
updated: 2026-10-31
---

# Registre des idées abandonnées

> **À lire avant de commencer tout nouveau travail** (nouvelle règle, nouveau papier, nouvelle variante). Si l'idée ressemble à une ligne ci-dessous, ne la relance pas sans remplir d'abord la colonne « Ne rouvrir que si » : la condition doit être vraie, et un nouveau pré-enregistrement doit le dire.
>
> Une ligne par idée, ajoutée le jour de l'abandon, jamais supprimée. Si une idée est rouverte, on ajoute une nouvelle ligne qui renvoie à l'ancienne. Les chiffres viennent des rapports liés ; en cas de doute, c'est le rapport qui fait foi.

| Date | Idée | Expérience / source | Verdict | Pourquoi elle a échoué | Ne rouvrir que si |
|---|---|---|---|---|---|
| 2026-10-12 | Momentum intraday (Gao, Baltussen, Rosa) sur indices ES/NQ/YM | [[PREREGISTRATION]] M1, [[RESULTS]] §1–2, réplication R1 | ❌ | Sharpe net négatif partout ; l'effet de Gao est absent depuis 2016 même en brut | Jamais sur indices avec ces données |
| 2026-10-12 | Momentum intraday sur futures FX comme stratégie | [[PREREGISTRATION_3]] R2a–c, [[RESULTS]] | ❌ net | L'effet brut existe (avec la session 8:20–15:00 ET), mais vaut 0,5 à 1,3 tick contre 1,8 tick de coût | Coûts institutionnels ou exécution par ordres limites démontrée |
| 2026-10-12 | Opening range breakout (30 min, 5 min, filtre volume ; ORB de Zarattini) | [[PREREGISTRATION]] M3, [[PREREGISTRATION_3]] R4 | ❌ | 10 ORB sur 27 sont tués par les coûts. Zarattini se reproduit sur NQ 2016–22 (+0,96 net) puis s'effondre après publication (+0,17) | — |
| 2026-10-12 | Saisonnalité des fixings (Tokyo, Krohn ; Europe ; Breedon-Ranaldo EUR) comme stratégie autonome | [[PREREGISTRATION]] M5, [[PREREGISTRATION_3]] R5–R6 | ❌ net | Mouvement de 1 à 2,5 ticks pour 1,8 à 2 ticks de coût ; déclin après 2023 | Usage seulement comme timing d'exécution : voir [[wiki/experiments/fx-timing-execution]] |
| 2026-10-12 | Contrarien sur l'or le lendemain d'un jour anormal (Caporale-Plastun) | [[PREREGISTRATION_3]] R7b | ❌ | Le signe est inversé sur nos données (Sharpe −0,68 / −0,88) | — |
| 2026-10-12 | Bande de bruit M2 sur ES | [[PREREGISTRATION]] M2, [[RESULTS]] §3 | ❌ | Perd depuis la publication (−0,16) et sur la fenêtre Delgado (−0,74) | — |
| 2026-10-12 | Bande de bruit M2 sur NQ (critère formel) | [[PREREGISTRATION_2]] piste B | ❌ (DSR 0,03) | Rejetée selon la règle fixée à l'avance (DSR **et** Reality Check) ; gains concentrés sur les crises. Gardée en paper trading : voir [[wiki/experiments/m2-bande-bruit-nq]] | Seulement sur des données postérieures au 2026-08-28 (holdout unique) |
| 2026-10-14 | Prévoir le gap d'ouverture du DAX avec les courbes Asie/US (NP-FDA, De Gooijer et al.) | [[PREREGISTRATION_5]], [[reports/opening_gap_report]] | ❌ | Le gap est prévisible mais linéairement (MCO R² ≈ 28 %) ; aucune règle tradable (meilleur DSR 0,27) ; NP-FDA ne bat jamais le MCO | — |
| 2026-10-14 | Signe de la minute 08:55 → 09:00 du DAX | [[reports/opening_gap_report]] (exploratoire) | ❌ | Prévu à 55 % (p = 0,0008), mais Sharpe net 0,13 | Coût proche de zéro |
| 2026-10-15 | Fade de la première heure FX après la reprise de 18:00 ET (Tolušić) | [[PREREGISTRATION_6]], [[reports/fx_reopen_report]] | ❌ | −2,55 pips/trade net ; l'effet tient dans la première minute (enchère de 18:00) et n'est pas captable | Données bid/ask au comptant autour de 17:00 NY |
| 2026-10-15 | Retournement après le fix de Londres en fin de mois ; flux de couverture actions (Melvin-Prins) | [[PREREGISTRATION_7]], [[reports/fx_fix_report]] | ❌ | +2,4 pips net non significatif (p = 0,28), négatif sur 2016–20 ; la règle de couverture perd (−3,1 pips) | — |
| 2026-10-20 | Asymétrie intraday ancrée sur l'ouverture (Valenti) sur ES / DAX | [[PREREGISTRATION_8]], [[reports/asym_report]] | ❌ | DSR 0,58 ; corrélé à 0,90 au simple contrarien ouverture → clôture, sans apport (t = 0,05) ; gains de 2020 et 2025 ; DAX négatif | — |
| 2026-10-20 | Momentum de fin de séance après un grand mouvement (ETF à levier, Shum et al.) | [[PREREGISTRATION_9]], [[reports/letf_report]] | ❌ | ES : tout vient de 2020 (hors 2020 −4 pb). NQ : +12 pb mais DSR 0,75 ; déclenchements rares | — |
| 2026-10-29 | « Le money management crée l'edge » : entrée pile ou face avec SL/TP en ATR | [run_coinflip.py](../../run_coinflip.py), [run_coinflip_costs.py](../../run_coinflip_costs.py), `results/coinflip/` (contrôle) | ❌ | Taux de réussite = 1/(1+RR) comme prévu ; avec coûts, négatif (CFD spread 2 pts : −0,13 R/trade) | Jamais : c'est un contrôle |
| 2026-10-30 | Traiter les 56 IC nets positifs de la récolte 1 comme 56 stratégies | [[reports/recolte1_56_ic_net_positifs]] | ❌ | ~23 faux positifs attendus sur 927 tests ; 51 des 56 sont la même prime de nuit comptée plusieurs fois ; rien de pré-enregistré | — |
| 2026-10-30 | Close-to-open GC 16:15 → 8:30 avec entrées horaires et SL/TP ATR | [[reports/recolte1_atr_report]] | ❌ | Net négatif dans toutes les variantes (≈ −0,9 pb/trade) | — |
| 2026-10-30 | Étendre la règle NQ de nuit (momentum 12-1, 20:00, SL 2 / TP 5 ATR) à ES et YM | [[PREREGISTRATION_10]], [[reports/prereg10_report]] | ❌ | ES p Holm 0,25 ; YM négatif sur 2021–26. Effet 3 à 5 fois plus faible que sur NQ | — |
| 2026-10-30 | Affiner les stops ATR ou l'heure d'entrée (20:00) de la règle NQ de nuit | [[PREREGISTRATION_12]], [[reports/prereg12_report]] | ❌ | SL/TP n'améliorent pas le Sharpe de façon démontrable (+0,14 [−0,22 ; +0,50]) ; l'avantage de 20:00 vient de la durée d'exposition | Objectif de queue de distribution, pas de Sharpe (voir [[reports/robust13_report]]) |
| 2026-10-31 | Filtres « à plat » pour réduire le drawdown de la règle NQ de nuit (Jones 9:45→15:00 > 0, nuit précédente < 0, VOL veille tercile haut, clôture > MM20) | [[PREREGISTRATION_13]], [[reports/prereg13_report]] | ❌ | Aucun ne réduit le max DD de 30 % en gardant 80 % des R/an ; tous sous le 95e centile de 500 filtres aléatoires de même taille ; MM20 aggrave le DD | Un filtre a une raison écrite d'éviter précisément les nuits de la queue gauche, et est testé d'abord sur des données jamais vues (holdout post-2026-08-28) |
| 2026-10-31 | Éviter les annonces NFP/CPI de 8:30 ET (pas de trade, ou sortie à 8:25) dans la règle NQ de nuit | [[PREREGISTRATION_14]], [[reports/prereg14_report]] | ❌ | Inversé : les nuits d'annonce sont les meilleures (+0,30 R/trade contre +0,05), aucune parmi les 10 pires ; les retirer aggrave le DD | Jamais dans ce sens ; le sens inverse (surpondérer les annonces) se teste sur le holdout |
