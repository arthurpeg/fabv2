# Book C sans edge chez FundingPips, en plus des books A et B chez FTMO

Demande du 2026-11-05. EXPLORATOIRE, hors compteur. Code : `run_book_c.py` ; sorties : `results/book_c/` (run.log, vrai_chemin.csv, glissants.csv, mc.csv).

**Book C** : un trade chaque nuit aux heures de mom (20:00 → 9:30, SL 2 ATR M15, objectif 2 R), **sens tiré à pile ou face** (aucun edge), sur un **FundingPips 1 Step Flex 10k**, la 2e prop firm 1-step de notre classement ([[propfirm_multi]]). Règles relevées le 2026-10-31 : objectif +12 %, perte max 12 % fixe, perte du jour 3 %, levier 1:5 en financé (option Swing), pas de consistance, retrait toutes les 2 semaines (min 1 %, 80 %). Le site a refusé nos requêtes le 2026-11-05 : **prix du 10k supposé** à 116 $ (733 $ du 100k × rapport 10k / 100k de FTMO). Gestion calquée sur le plan FTMO : éval 2,5 % avec objectif ramené au reste à faire, financé 1 % à 2 R, compte racheté après chaque échec. A et B : plan retenu (annonces, cible + attente, anti-hedging) ; le hedging ne s'applique qu'à l'intérieur d'une même prop firm.

| | Vrai chemin 2011-07 → 2026-08 (200 tirages des sens) | 12 mois glissants (721 départs) | Monte-Carlo 3 ans (1 000 chemins) |
|---|---|---|---|
| C seul | +17 199 $ médiane (+1 125 $/an), P(< 0) 0 % | +727 $ médiane, P(< 0) **19,6 %**, pire −1 160 $ | +2 909 $ médiane, P(< 0) 2,5 % ; à 1 an +686 $, P(< 0) 19,7 % |
| A + B | +65 498 $ | +3 767 $, P(< 0) 0 % | +12 940 $, P(< 0) 0 % |
| **A + B + C** | **+82 697 $** (+26 %) | **+4 583 $** (+22 %), pire +464 $ | **+16 054 $** (+24 %), 1er c. +8 999 $ |
| Max DD de trésorerie A + B → A + B + C | −435 → −580 $ | médiane −261 → −434 $, pire −695 → −1 218 $ | médiane −348 → −522 $, 99e c. −782 → −1 275 $ |

- C : ≈ 48 évals achetées en 15 ans (≈ 5 600 $ de frais), 25 validées, 103 retraits. Son gain vient de la seule convexité du contrat (on perd au plus le prix de l'éval, on retire le profit et le compte repart à zéro).
- Corrélation des flux mensuels C / A +0,10, C / B +0,03 ; mois négatifs du total 12 % → 13 %.
- Lecture : C ajoute ≈ 800 à 1 100 $ par an, soit environ +25 % au total, et augmente le creux de trésorerie d'environ 50 %. Seul, il est perdant sur un an dans 1 cas sur 5.

Réserves : prix FundingPips supposé ; levier 1:5 et option perte du jour 3 % non vérifiés ; un trade au hasard chaque nuit peut être vu comme du « gambling » par certaines prop firms (refus de retrait non modélisé) ; mêmes trades NQ que mom (mêmes nuits, même stop), donc C n'est pas indépendant du marché, seulement du sens.
