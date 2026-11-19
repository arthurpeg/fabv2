# Règle anti-hedging FTMO : pas de 3n long quand mom est short

Demande du 2026-11-05. EXPLORATOIRE, hors compteur. FTMO interdit d'avoir des positions opposées sur deux comptes. Le compte A (mom, 20:00 → 9:30) et le compte B (3n, long 20:05 → 03:00) se chevauchent chaque nuit : une nuit où mom est short, 3n long ferait du hedging.

**Règle ajoutée** (`ANTI_HEDGE = True` dans `run_ftmo_deux_comptes.py`, appliquée dans `tableau()` ; bot : `live/bot.py`, `ev_3n`, test `tests/test_live_bot.py::test_book_B_anti_hedging`) : si le signal mom de la nuit est short, pas de 3n ; M2 trade alors le matin à pleine taille (pas de chevauchement : mom sort à 9:30, M2 entre à 9:35). Règle conservatrice : appliquée même si le compte A ne trade pas ce soir-là (attente, compte perdu).

## Combien de fois c'est arrivé

192 nuits sur 1 635 nuits 3n (11,7 %), toutes dans les années où le momentum 12-1 était négatif : 2016 (45), 2019 (35), 2020 (4), 2022 (68), 2023 (40). Aucune en 2026 (mom long depuis le début de l'année). Le R moyen de 3n ces nuits-là : +0,12 R (contre +0,16 R quand mom est long). Une seule nuit où mom short était déjà sorti avant 20:05.

## Effet sur les simulations (avant → après)

Anciens journaux conservés en `results/<dossier>/*_avant_hedge.log`.

| Simulation | Avant | Après |
|---|---|---|
| Historique 2011-2026 (`run_ftmo_deux_comptes_historique.py`) : net B | +31 592 $ (98 rewards) | +29 793 $ (93 rewards) |
| idem : net total | +68 562 $ | +66 764 $ (−2,6 %) |
| idem : corrélation P&L journalier A / B | +0,24 | +0,29 |
| Monte-Carlo 3 ans, net médian (historique / récent / edge ÷ 2) | +12 889 / +12 305 / +7 939 $ | +12 752 / +11 919 / +7 936 $ |
| Max DD de trésorerie, 99e c. (historique) | −782 $ | −797 $ |
| 1re éval : au moins un compte validé (historique) | 82,3 % | 80,6 % (B 63,8 → 62,1 %) |
| 1re éval : au moins un payout | 78,9 % | 77,6 % |
| ≤ 2 évals par compte : au moins un payout | 96,6 % | 96,5 % |
| Scaling : 400k en (médiane, MC historique / edge ÷ 2) | 12,0 / 17,7 mois | 12,4 / 17,7 mois |
| Scaling : cagnotte à 5 ans, médiane MC historique | +375 k$ | +370 k$ |
| Scaling : revenu mensuel moyen à 400k (MC historique / edge ÷ 2) | 7 680 / 4 991 $ | 7 592 / 4 983 $ |

Conclusion : la règle coûte peu (≈ 2 à 3 % du gain de B, 1 à 2 points de probabilité de validation), parce que les nuits concernées sont celles où 3n gagne le moins et que M2 reprend sa pleine taille ces jours-là.
