# Montée en taille FTMO jusqu'à 800k (simulation hypothétique)

Demande du 2026-11-05. EXPLORATOIRE, hors compteur. FTMO plafonne aujourd'hui à 400k hors plan de scaling : ce scénario suppose que 800k serait permis. Code : `run_ftmo_scaling_800k.py` ; sortie : `results/ftmo_scaling_800k/run.log`.

Mêmes règles que le scaling à 400k ([[ftmo_scaling_report]]) : A = mom, B = 3n + M2, annonces + cible + attente, anti-hedging, réserve de 10 évals par paire. Deux paliers ajoutés : 3 × 100k par stratégie (600k, réserve 16 467 $), puis 4 × 100k (800k, réserve 21 956 $).

| | Départs glissants (130) | MC historique (1 000) | MC espérance / 2 (1 000) |
|---|---|---|---|
| 400k atteint (médiane) | 12,0 mois | 12,4 mois | 17,7 mois (96 %) |
| 600k | 13,5 mois | 13,9 mois | 19,8 mois |
| **800k** | **14,7 mois** | **15,0 mois** | **21,2 mois** (96 %) |
| Cagnotte à 2 ans (médiane) | +143 k$ | +153 k$ | +38 k$ |
| Cagnotte à 5 ans (médiane) | +623 k$ | +706 k$ | +395 k$ |
| Revenu mensuel moyen à 800k (médiane) | 13 354 $ | 15 284 $ | 10 070 $ |
| Mois négatifs | 11 % | 11 % | 22 % |
| Max DD de cagnotte (médiane / pire) | −6 587 / −10 978 $ | −6 587 / −32 934 $ | −10 978 / −41 716 $ |
| Ruine (cagnotte < une éval 10k) | 0 % | 1,1 % | 5,9 % |
| Comptes 100k financés perdus en 5 ans (médiane) | 23 | 26 | 36 |

Vrai chemin 2011-2026 : 800k le 14/08/2012 (13,5 mois), revenu à 800k 14 472 $ / mois en moyenne (médiane 14 016 $, 12 % de mois négatifs, pire mois −6 587 $ en 2025-05).

Lecture : 600k et 800k arrivent 1,5 et 3 mois après 400k (les rewards des 100k paient vite les réserves suivantes) ; le revenu mensuel double à peu près (≈ 7 600 $ → ≈ 15 300 $ en MC historique) ; le creux de cagnotte double aussi. Ruine inchangée : elle se joue dans les premiers mois, aux paliers 10k.

Réserves : hypothèse FTMO non réelle ; 3n et M2 ont échoué hors échantillon (n° 24, 25) ; refus de payout, limites de capital et de comptes par personne non modélisés.
