---
type: experiment
updated: 2026-11-19
status: active
verdict: 1er essai (filtre binaire sur mom) rejeté ; autres candidates à faire
prereg: []
trials: 1807
---

# Machine learning sur les anomalies que les filtres classiques n'ont pas améliorées

**Une phrase** : chercher si un modèle appris (arbres boostés, régression régularisée, classifieur de signe…) sélectionne ou dimensionne mieux les trades d'une anomalie déjà confirmée que les filtres à une variable déjà essayés. Branche git `ml` (voir CLAUDE.md, section « Branches »), code dans `ml/`. 1er essai le 2026-11-19 : filtre binaire sur mom, rejeté (voir ci-dessous).

## Origine

Demande de l'utilisateur du 2026-11-19. Les anomalies ci-dessous sont significatives sur nos données ([[wiki/phenomenes]]), mais chaque tentative de les améliorer par un filtre simple a échoué. Les chiffres sont des repères : le rapport lié fait foi.

## Candidates (à prioriser à l'étape 0)

| Anomalie | Ce qui a déjà échoué | Source | Contraintes |
|---|---|---|---|
| Short yen en session US (11:00 → 16:55 ET, Zhang) | Aucune coupe ex ante ne concentre l'effet (34 coupes) ; SL/TP en ATR tous moins bons que sans stop | `reports/jpy_us_distribution_report.md` (main), `reports/jpy_us_sltp_report.md` (strategies-vbt), [[PREREGISTRATION_28]] | Yen après le 2026-08-28 = holdout du n° 28 : ne jamais l'utiliser pour entraîner ni évaluer |
| Règle NQ de nuit (momentum 12-1) | Filtres anti-DD de prix, VIX, pression vendeuse (n° 13, 15, 16) : aucun ne bat le hasard | [[wiki/experiments/nq-nuit-momentum]], [[PREREGISTRATION_13]], [[PREREGISTRATION_15]], [[PREREGISTRATION_16]] | Traverse minuit : vérifier avec l'utilisateur qu'elle reste compatible avec la règle « intraday uniquement » ; holdout NQ n° 26 intouchable |
| Reprise de l'or (GC 17:00 → 9:00 Shanghai) | +1,1 bp net seulement, nulle le lundi | `reports/gc_sessions_report.md` (main) | Fenêtre du même jour (≈ 17:00 → 20:00/21:00 NY) |
| Signe de la minute 08:55 → 09:00 du DAX (enchère Xetra) | 55 % de bons signes mais Sharpe net 0,13 | `reports/opening_gap_report.md` (strategies-vbt) | Coût élevé par rapport au mouvement |

## Règles propres au ML (en plus de [[PROTOCOLE]])

- Chaque combinaison modèle × jeu de variables × hyperparamètres compte comme un essai du [[wiki/concepts/compteur-essais|compteur]] ; la grille est commitée avant calcul (étape 1).
- Validation strictement chronologique (walk-forward avec purge et embargo) ; aucune donnée de réserve ([[wiki/reserves]]) dans l'entraînement ni la sélection.
- Référence triviale obligatoire : la règle brute sans filtre, et le meilleur filtre classique déjà testé.
- Variables connues à l'heure de décision seulement (contrôle d'alignement comme `tests/test_leakage.py`).

## Essais

| Date | Anomalie | Essai | Résultat | Source |
|---|---|---|---|---|
| 2026-11-19 | Règle NQ de nuit mom (TP 4 ATR, compte A FTMO) | Filtre binaire à taille fixe 1 R, garder 70 / 50 / 35 % des nuits ; logit L2 et LightGBM contraint sur 4 variables (mom continu, nuit d−1 Abdi, clôture − VWAP BLW, NFP/CPI) ; Purged K-Fold 5 blocs, embargo 5 ; jugé sur P(réussite) Monte Carlo (+10/−10 R, +8/−6 R, FTMO 2,5 %) ; 9 filtres (compteur 1 798 → 1 807) | ❌ AUC hors bloc 0,50-0,51 ; aucun filtre ML significatif (Holm 1,0), P(réussite) dans le bruit des filtres aléatoires et sous Abdi seule ; jours de passage × 1,4 à 2,9 ; tous les filtres négatifs sur 2023-2026 sauf logit 70 % | [[reports/ml_propfirm_filter_report]] (branche `ml`), [ml_propfirm_filter.py](../../experiments/ml_propfirm_filter/ml_propfirm_filter.py) |

Leçon : à taille fixe, filtrer ne change P(réussite) que par l'E[R] par trade ; un filtre au hasard laisse P inchangée et allonge la durée en 1/q.

## Ouvert

- Choix de la première anomalie et du jeu de variables (prix, volatilité réalisée, calendrier macro `config/`, VIX).
- Bibliothèque (scikit-learn, LightGBM) : à ajouter à `pyproject.toml` sur la branche `ml` seulement.

## Sources brutes

- `reports/ml_propfirm_filter_report.md`, `experiments/ml_propfirm_filter/` (branche `ml`) : `git show ml:reports/ml_propfirm_filter_report.md` depuis une autre branche.
