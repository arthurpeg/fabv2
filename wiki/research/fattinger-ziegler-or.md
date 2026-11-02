---
type: research
updated: 2026-11-02
source: SSRN 2606706 (Fattinger, Ziegler, « Risk and Return around the Clock », 2015) ; PDF dans `papiers overnight ssrn/`
status: tested
verdict: [[reports/gc_fattinger_report]], [[reports/si_fattinger_report]]
---

# Fattinger-Ziegler sur l'or : découverte du prix sur 24 h

**Ce que c'est** : papier descriptif sur 13 futures en 5 minutes, 2010-2013. Il mesure où se fait le prix et le risque sur 24 h, l'efficience de la découverte du prix, les pics de volatilité, les sauts, et le lien volume/volatilité. Aucune stratégie. Résumé complet : [[resumes_papiers_overnight_recolte1]] (entrée [20]).

**Affirmations clés pour l'or (papier)** : contribution au prix quasi nulle avant l'ouverture européenne ; prix bruité les 3-4 premières heures de Globex ; pics à Tokyo, 8:30, 10:00, clôture de corbeille, Fed, 16:00 ; pas de U ; sauts 5-13 % de la variance, le saut de 8:30 = 1,22 % ; volume < volatilité hors corbeille.

**Ce qu'on a trouvé (2016-2026, 54 tests)** : voir [[reports/gc_fattinger_report]], qui fait foi.
- Se reproduit : pics de volatilité (8:30 domine, Tokyo, Europe, 8:20, 10:00, 13:30, Fed), pas de U, sauts ≈ 9 % dont 8:30 en tête (≈ 2 %), volume < volatilité la nuit, plus de prix par contrat la nuit.
- **Contredit** : l'or fait aujourd'hui environ un quart de son prix avant 3:00 NY (autant que sa part de variance).
- Non confirmé : début de Globex bruité (pente < 1 non significative), chute d'efficience avant l'Europe, 10:00 > Fed, pic à 16:00.
- Nouveau, non validé : continuation du mouvement 17:00 → 5:00 sur le reste du jour, uniquement en 2023-2026.

**Argent (2017-2026, données London Strategic Edge)** : voir [[reports/si_fattinger_report]]. Même microstructure que l'or en plus bruyante (σ × 2,1) ; un quart du prix aussi avant 3:00 NY ; pas de pic à 13:30 ni de pic de volume aux anciennes heures de corbeille ; sauts 7,3 % (pas plus que l'or) ; profils de diffusion or/argent corrélés à 0,96 mais niveau × 2,2 ; continuation de nuit de même signe, non significative après Holm.

**Liens** : [[reports/gc_sessions_report]] (reprise du soir), [[wiki/research/recoltes-ssrn]], [run_gc_fattinger.py](../../run_gc_fattinger.py).
