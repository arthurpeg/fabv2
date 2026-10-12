# Pré-enregistrement n° 2 : les deux pistes issues de RESULTS.md

*Écrit le 2026-10-12, après avoir lu [RESULTS.md](RESULTS.md) (commit `ba9fab0`) et avant d'exécuter les tests ci-dessous. Coûts, données, exécution et découpage IS/OOS sont identiques à [PREREGISTRATION.md](PREREGISTRATION.md).*

## Problème de départ

Les deux pistes ont été repérées **en regardant les données 2023-2026**. Les retester sur ces mêmes données ne prouverait rien. Il n'existe pas de données postérieures au 2026-08-28. On s'en tient donc à deux types de tests :

- **A** : des observations **jamais tradées** (les jours que le premier test a exclus), et des prédictions structurelles du mécanisme causal ;
- **B** : des corrections qui intègrent explicitement les **93 essais déjà faits**.

## A. Fade de gap sur les indices et régime 0DTE (Ladia 2026)

Mécanisme supposé : depuis l'essor des options 0DTE (expirations quotidiennes sur le SPX complétées en mai 2022, volumes en forte hausse en 2023), la couverture des dealers pousse au **reversal** des gros mouvements d'ouverture. Si ce mécanisme est réel, et pas un artefact des environ 50 trades vus, alors :

- **A1, nouvelles observations** : la même règle M4b, appliquée aux gaps **intermédiaires 1 < |z| ≤ 2** (des jours **jamais tradés** dans le premier test), est rentable après 2023. Le test porte sur un portefeuille équipondéré ES/NQ/YM (les trois indices sont trop corrélés pour compter comme trois confirmations). **Critère : Sharpe net OOS du portefeuille > 0,5.**
- **A2, rupture** : sur les trades poolés avec |z| > 1 (les 3 indices), le rendement moyen net par trade est plus élevé en 2023-2026 qu'en 2016-2022. **Critère : test de Welch unilatéral, p < 0,05.**
- **A3, dose-réponse** : en 2023-2026, le rendement moyen net par trade croît avec |z| sur les tranches (1 ; 1,5], (1,5 ; 2], > 2. **Critère : croissance strictement monotone.**

**La piste A survit seulement si A1, A2 et A3 passent tous les trois.** Elle compte pour **3 tests supplémentaires** dans le compteur global (93 → 96).

## B. Bande de bruit sur NQ : correction pour les tests multiples

Ces calculs n'ajoutent pas de stratégie. Ils réévaluent le survivant en tenant compte des 93 essais.

- **B1, Deflated Sharpe Ratio** (Bailey & López de Prado 2014) sur toute la période 2016-2026. N = 96 essais, V[SR] = variance des Sharpe journaliers des 93 tests, avec l'asymétrie et le kurtosis des rendements journaliers de M2 sur NQ. **Critère : DSR > 0,95.**
- **B2, Reality Check de White** (bootstrap stationnaire, 5 000 réplications, blocs de 10 jours en moyenne, statistique = max des t-stats des 93 séries journalières nettes, recentrées). H0 : aucune des 93 stratégies n'a d'espérance positive. **Critère : p < 0,05.**
- **B3, PBO par CSCV** (Bailey et al. 2017) sur la matrice des 93 séries journalières nettes, S = 16 blocs, toutes les C(16,8) = 12 870 combinaisons, sélection IS par le Sharpe. C'est un diagnostic du processus de sélection, **pas** un critère de survie : on rapporte la PBO et la probabilité que la stratégie choisie en IS ait un Sharpe OOS < 0.
- **B4, stabilité récente** : intervalle de confiance bootstrap à 95 % (blocs de 10 jours) du Sharpe net de M2 sur NQ, sur les 24 derniers mois (2024-09 à 2026-08). Rapporté sans critère.

**La piste B survit si B1 et B2 passent.**
