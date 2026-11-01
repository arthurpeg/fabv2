# Pré-enregistrement n° 20 : la matinée US prédit le reste de la séance (9:30 → 11:30, |z| > 1, sortie 16:00) sur ES et YM

*2026-11-01, avant tout calcul de cette règle sur ES et YM. Origine : exploration sur NQ uniquement ([reports/nq_sessions_corr_report.md](reports/nq_sessions_corr_report.md), [reports/nq_matin_aprem_report.md](reports/nq_matin_aprem_report.md)). ES et YM servent de test hors échantillon partiel.*

## Pourquoi un test seulement « partiel »

- Sur NQ, la règle est sortie d'un tri après coup : 8 paires de sessions, puis 6 fins de matinée × 2 cibles, puis 7 règles tradables. La fin de matinée 11:30 vient du premier rapport, et le seuil de 1 σ a été choisi au second. Les chiffres NQ (+5,8 bp/trade net, t 2,4) sont donc biaisés vers le haut.
- ES et YM sont très corrélés à NQ (même séance US, mêmes flux). Un succès ici confirme que l'effet n'est pas propre à NQ, pas qu'il existe hors de l'échantillon temporel. Le juge final reste le holdout NQ postérieur au 2026-08-28.
- Déjà vu sur ES et YM : le momentum intraday de Gao (première 1/2 h → dernière 1/2 h) et de Baltussen ([[RESULTS]] §1-2, réplication R1), qui a échoué. **La règle ci-dessous (matinée 9:30 → 11:30, cible 11:30 → 16:00, seuil en σ de 20 séances) n'a jamais été calculée sur ES ni sur YM.**

## Règle figée (aucun paramètre ne sera modifié après calcul)

| Élément | Valeur |
|---|---|
| Marchés | ES et YM (`.v.0`, 1 minute, Databento), 2010-06 → 2026-08-28, ajustés en ratio aux roulements (`recolte1.engine.load`, `USE_2010 = True`) |
| Jours | séances NYSE pleines (calendrier XNYS) ; demi-séances exclues |
| Prix à un instant T | clôture de la dernière barre 1 min démarrant dans [T−5 min, T−1 min] (`recolte1.engine.price_at`) |
| Matinée X | rendement 9:30 → 11:30 NY |
| Seuil | z = X / écart-type de X sur les 20 séances précédentes (fenêtre glissante, sans la séance du jour) ; trade seulement si \|z\| > 1 |
| Position | long si X > 0, short si X < 0, de 11:30 à 16:00 NY (clôture NYSE) |
| Exécution | vectorbt `Portfolio.from_orders` aux deux bornes (code `run_nq_sessions_corr.follow`) |
| Coût | 1 tick + 5 $ aller-retour (ES 0,25 + 0,10 point ; YM 1 + 1 point), rapporté au prix non ajusté |
| Mesure | rendement net par trade, en points de base |

## Tests (2 essais)

Un test principal par marché : la règle sur ES ; la règle sur YM. Compteur global d'essais : 1 520 avant ce document → **1 522**.

## Critères de succès, fixés à l'avance

p unilatéral pour H1 : rendement net moyen > 0, par bootstrap par blocs mobiles circulaires (blocs de 10 trades, 2 000 tirages, recentré sous H0 ; `p_one_sided` de `run_prereg10.py`) ; IC 95 % par `recolte1.engine.ci_mean`.

1. **Succès principal** si, **pour ES et pour YM**, le rendement net moyen est > 0 avec p unilatéral < 0,05 après correction de Holm sur les 2 marchés.
2. **Et** le rendement net moyen est positif sur chacune des deux sous-périodes 2010–2017 et 2018–2026, sur les deux marchés (signe seulement).
3. **Succès partiel** : un seul des deux marchés remplit 1 et 2. **Échec** : aucun.

Rapportés en plus, sans valeur de décision : nombre de trades, gain par an, Sharpe annualisé avec le vrai nombre de trades par an, drawdown maximal, années positives, version sans seuil (tous les jours), corrélation X → Y.

## Conséquence fixée à l'avance

- Succès : la règle NQ est pré-enregistrée telle quelle pour le holdout NQ postérieur au 2026-08-28, à ouvrir une seule fois quand il comptera au moins 100 trades.
- Échec ou succès partiel : ligne au registre des échecs ; la règle n'est rouverte qu'avec une donnée de mécanisme (gamma des options, OPRA), voir [[wiki/Failed Ideas/ledger]].

## Ce qui est interdit après calcul

Changer la fin de matinée, le seuil, la fenêtre de 20 séances, la sortie, le coût ou la période ; ajouter un filtre (régime de volatilité compris) ; exclure une année ; remplacer ES ou YM par un autre marché.
