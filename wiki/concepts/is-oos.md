---
type: concept
updated: 2026-11-19
---

# Découpage IS / OOS et holdout

**Convention** : IS = 2016–2022, OOS = 2023 → 2026-08 (premiers pré-enregistrements). Depuis le n° 11, 2011-07 → 2015 sert d'OOS temporel (Databento 2010–2015 achetés, `cache/databento_2010/`).

**Holdout unique** : les données postérieures au 2026-08-28. On ne les ouvre qu'une fois, pour un test pré-enregistré.

**Plan figé au [[PREREGISTRATION_26]]** (2026-11-03 ; avenant A : la fenêtre 2026-08-29 → 2026-11-03 a été ouverte en lecture anticipée exploratoire, [[reports/holdout_anticipe_report]], donc **le holdout officiel commence le 2026-11-04**) : mom, M2 (EMA 9:30), 3n SL et le rebond après forte baisse. Lectures le 2028-02-29 et le 2029-08-31 (succès seulement si z ≥ 3,0), puis le 2031-08-29 (verdict, Holm). D'ici là, **aucun calcul de prix, de rendement, de signal ou de paper trading de ces règles sur ces données** ; seuls le téléchargement mensuel et la vérification de couverture sont permis (`cache/lse/NQ_lse_1m.parquet`, voir [[wiki/reference/donnees]]).

**Hors échantillon « partiel »** : un autre actif sur la même période (ex. ES/YM au n° 10) ; utile mais faible, car les indices sont corrélés.

## Réserve hors échantillon par actif (règle depuis le 2026-11-19)

Le but est de pouvoir confirmer un phénomène sur nos données sans attendre des données nouvelles en live.

1. **Idée tirée d'un papier** : la période d'estimation du papier est son échantillon. Toute donnée postérieure à cet échantillon qui n'est pas encore consommée peut servir de hors échantillon, **une seule fois**, après un pré-enregistrement. Exemple : le n° 27 (Zhang, papier 2010-2015, test 2016-2026).
2. **Phénomène trouvé par nous** : avant le premier calcul de rendement sur une tranche vierge, on déclare une réserve dans [[wiki/reserves]]. Par défaut, ce sont les 30 % les plus récents, au moins 3 ans. On explore librement le reste. La réserve s'ouvre une fois, par un pré-enregistrement commité, puis passe en « consommée ».
3. **Une réserve ne sert qu'à une famille d'idées.** Une fois ouverte, elle devient une donnée explorée pour toutes les idées suivantes.
4. **Contrôles de qualité sur une réserve** : comptes de barres, trous, spreads, corrélations. Jamais de moyenne de rendement par session ou par heure. Le contrôle du 2026-11-17 sur le FX a consommé 2016-2025 de cette manière, sans le vouloir.
5. **Le holdout post-2026-08-28 reste le dernier recours**, pour les règles qu'on veut trader.
6. **Réserve par question** (2026-11-21) : une tranche explorée pour un effet de base garde ses 30 % récents pour une **couche nouvelle** (filtre, condition, stop), tant que ce découpage n'a jamais été calculé. Le verdict y porte sur l'écart avec la règle de base, pas sur le net seul. Détail : [PROTOCOLE.md](../../PROTOCOLE.md), étape 0, point 4.

**Limite (puissance)** : une réserve de 3 ans ne détecte qu'un effet fort, environ t 2,4 pour un Sharpe annuel de 1,4. Un effet net faible (Sharpe ≈ 0,6) ne s'y confirme presque jamais. Pour ceux-là, il faut un holdout long ou le live.

**Piège** : une tranche regardée « juste pour voir » est consommée. En cas de doute, [[wiki/reserves]] la classe « explorée ».

**Voir aussi** : [[wiki/concepts/pre-enregistrement]], [[wiki/reserves]]
