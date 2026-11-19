---
type: experiment
updated: 2026-11-19
status: planned
verdict: à faire (branche ml créée, aucun calcul)
prereg: []
trials: 1798
---

# Machine learning sur les anomalies que les filtres classiques n'ont pas améliorées

**Une phrase** : chercher si un modèle appris (arbres boostés, régression régularisée, classifieur de signe…) sélectionne ou dimensionne mieux les trades d'une anomalie déjà confirmée que les filtres à une variable déjà essayés. Branche git `ml` (voir CLAUDE.md, section « Branches »), code dans `ml/`. Aucun calcul fait au 2026-11-19.

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

## Ouvert

- Choix de la première anomalie et du jeu de variables (prix, volatilité réalisée, calendrier macro `config/`, VIX).
- Bibliothèque (scikit-learn, LightGBM) : à ajouter à `pyproject.toml` sur la branche `ml` seulement.

## Sources brutes

Aucune pour l'instant (branche `ml`, dossier `ml/`).
