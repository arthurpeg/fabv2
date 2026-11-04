# Probabilité de toucher un payout au démarrage (plan retenu, deux comptes 10k)

Demande du 2026-11-04. EXPLORATOIRE, hors compteur. Code : `run_ftmo_proba_payout.py` ; sortie : `results/ftmo_proba_payout/run.log`.

Plan retenu (A = mom, B = 3n + M2, règle des annonces + cible + attente), moteur `Compte` de `run_ftmo_deux_comptes.py`. Chaque compte est racheté après un échec jusqu'à son premier reward (horizon 2 ans). Prix d'une éval 10k : 86,90 $.

| Évals achetées au plus par compte | Historique (3 394 départs, 2011-2024) | MC historique | MC espérance / 2 |
|---|---|---|---|
| 1 (174 $) : au moins un payout | 78,9 % (A 47,4 %, B 61,0 %) | 78,8 % | 62,0 % |
| 2 (348 $) | 96,6 % | 94,8 % | 84,3 % |
| 3 (521 $) | 99,7 % | 98,8 % | 94,1 % |
| 5 (869 $, dépôt du plan) | 100 % | 100 % | 99,2 % |

- Les deux comptes réussissent ou échouent presque indépendamment (corrélation « 1re éval payée » A / B ≈ +0,02 à +0,06).
- Délai du premier payout, tous comptes confondus : médiane 30 séances (≈ 6 semaines), 90e centile 57 séances ; un payout en 3 mois dans 93 % des départs (80 % avec l'espérance divisée par 2).
- Réserves : 3n et M2 ont échoué hors échantillon (n° 24, 25) ; seuls les chiffres du compte A reposent sur une règle validée. La fenêtre 2026 est incluse dans la bibliothèque (vue, avenant A du n° 26).
