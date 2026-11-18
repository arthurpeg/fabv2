# Pré-enregistrement n° 27 : Zhang (2018), sessions intraday du FX, sur les 7 majeures

*2026-11-19, écrit et commité avant tout calcul de rendement de session sur ces données. Papier : Zhang (2018), « Intraday Patterns in Foreign Exchange Returns and Realized Volatility », Finance Research Letters 27, SSRN 3138756 (texte : `papers/txt/zhang_fx_intraday_rv.txt`).*

## Statut : vérification de phénomène, pas une stratégie

La saisonnalité des fixings est au [[wiki/Failed Ideas/ledger|registre des échecs]] comme stratégie autonome (mouvement de 1 à 2,5 ticks pour 1,8 à 2 ticks de coût). La session US de Zhang (11:00 → 17:00 NY) commence au fix WM/R de 16:00 Londres : c'est le même effet que R5b (Krohn, [[PREREGISTRATION_3]]). Ce test **ne rouvre pas** cette ligne. Il vérifie seulement si les observations du papier se retrouvent sur nos données, pour [[wiki/phenomenes]]. Le coût est rapporté à titre d'information, sans verdict.

## Déjà vu (à déclarer)

- Les moyennes brutes 2016-2025 des sessions 08-11 et 11-16:45 NY sur 6E, 6B, 6J et sur le spot M15 Dukascopy ont déjà été vues le 2026-11-17 (EUR ≈ +0,5 bp, GBP ≈ +0,6 bp, USDJPY +1,8 bp en session US ; [[wiki/log]]). R5b et R6 ont testé des fenêtres voisines sur 6E/6B/6J/6A en 2016-2026 (positives en brut, négatives en net).
- Sur le spot Dukascopy 2010-2026, seuls des contrôles de qualité ont été faits : comptes de barres, trous, spreads, corrélation des rendements contre les futures en 2016. Aucune moyenne de session n'a été calculée.
- Les résultats du papier (Table 1, Table 2) sont connus. Ce sont eux qu'on teste.

## Devises et données

Les 7 majeures contre le dollar : EUR, GBP, JPY, CHF, AUD, CAD, NZD. Le prix est en dollars par unité de devise étrangère, comme dans le papier : on inverse USDJPY, USDCHF et USDCAD (et 6J est déjà dans ce sens). NOK, SEK et les autres devises sont écartées pour leur spread.

| Période | Dates | Source |
|---|---|---|
| **R : réplication** (période du papier) | 2010-05-03 → 2015-12-31 | Spot Dukascopy 1 h, mid = (bid + ask) / 2 (`cache/dukascopy/<PAIRE>_1h.parquet`) |
| **O : hors échantillon** | 2016-01-01 → 2026-08-28 | EUR, GBP, JPY, AUD : futures CME 6E, 6B, 6J, 6A 1 min Databento `.v.0` (`D:/quant-data/Cotations/forex`), ajustés en ratio par la règle de roulement de `run_sessions.py::load` (un roulement par mois d'échéance, plus grand écart à 00:00 UTC entre le 7 et le 22). CHF, CAD, NZD : spot Dukascopy 1 h. |

Rien après le 2026-08-28 (holdout).

## Construction (au plus près du papier)

- **Grille horaire** : un prix à chaque heure pleine de 00:00 à 23:00 GMT, du lundi au vendredi, comme Datastream. Prix à l'heure H : spot, `mid_close` de la barre 1 h qui commence à H − 1 h ; futures, clôture de la dernière minute avant H. S'il n'y a pas de cotation, on reporte le dernier prix connu. Le rendement horaire est r = log(P_H / P_{H−1}). Le rendement qui finit le lundi à 00:00 GMT contient le week-end (lecture littérale de la grille du papier).
- **Sessions**, avec l'heure d'été gérée par fuseau. Chaque rendement horaire est classé selon l'heure de début de son intervalle :
  - **domestique** : 08:00-16:00 locales. Places retenues : Francfort (EUR), Londres (GBP), Tokyo (JPY), Zurich (CHF), Sydney (AUD), Toronto (CAD), Wellington (NZD) ;
  - **LDN-NY** : 08:00-11:00 New York ;
  - **US** : 11:00-17:00 New York ;
  - **non-US** : les heures qui ne sont ni domestiques ni dans 08:00-17:00 New York.
- **Recouvrements** : comme dans la note 3 du papier pour CAD, les sessions sont calculées chacune selon sa définition, et une heure peut appartenir à la fois à la session domestique et à LDN-NY ou US (EUR, GBP, CHF, CAD). Seule la session non-US exclut toutes les autres.
- **Rendement de session** : somme des rendements horaires d'une suite continue d'heures de la même session. Il est rapporté en points de base (le papier utilise des %, × 100).

## Hypothèses avec verdict (42 essais ; compteur 1 742 → 1 784)

Les tests sont faits pour chaque devise, et séparément sur R et sur O.

- **H1** : la devise baisse pendant sa session domestique. Test unilatéral : moyenne < 0.
- **H2** : la devise monte pendant la session US. Test unilatéral : moyenne > 0.
- **H3** : la relation rendement / volatilité réalisée est négative en session domestique. On estime l'équation (4) du papier, R = θ + φ RV + Σ ξ_j RV d_j, par MCO avec écarts types HC1. Test unilatéral : φ < 0.

Pour H1 et H2, on utilise le t de Newey-West (5 retards) sur la série des sessions. Correction de Holm sur les 21 tests de chaque période, au seuil 0,05.

**Verdict « le papier dit vrai sur nos données »** : on regarde la période O, avec Holm. Un phénomène est confirmé s'il passe Holm et si son signe tient dans les deux moitiés de O (2016-2020 et 2021-2026-08). S'il est significatif en brut seulement, il va dans « À surveiller ».

## Rapporté sans verdict

- Le tableau de comparaison ligne à ligne avec la Table 1 du papier, sur R : moyennes des 4 sessions, t simples (comme le papier), t à deux échantillons domestique contre chaque autre session, F de Welch. **Critère de réplication** : chaque case marquée ** ou *** dans le papier (p < 0,05) a le même signe et p < 0,05 bilatéral chez nous.
- Le GARCH(1,1) de l'équation (2), avec un AR choisi par BIC jusqu'à 5 retards, et l'équation (4) sous GARCH, si le paquet `arch` est installé. Sinon, seulement les MCO de H3.
- Les mêmes statistiques par année, et le coût : spread médian au début et à la fin de chaque session (spot), 1 tick à l'aller-retour (futures), comparé au rendement moyen de la session.
- Une variante sans le rendement du week-end.

L'équation (4) est **contemporaine** : la volatilité réalisée de la session n'est connue qu'à la fin. Même vérifiée, elle ne donne aucun signal. Le papier dit lui-même que la volatilité réalisée de la session précédente n'est pas significative.

## Interdit après calcul

On ne change ni les sessions, ni les places, ni les sources, ni les dates, ni les tests, ni la correction. On n'ajoute aucune devise et on ne cherche pas de meilleure fenêtre horaire. Si la grille littérale pose un problème de données (par exemple des cotations figées), on le documente sans changer le verdict.
