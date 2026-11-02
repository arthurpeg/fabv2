# Pré-enregistrement n° 21 : continuation de la nuit sur l'or et l'argent, hors échantillon dans le temps (2003-2017, cours au comptant)

*2026-11-02, avant tout calcul sur ces données. Origine : [[reports/gc_fattinger_report]] (GC 2016-2026 : pente b(5:00) = 1,13, Holm 0,02, portée par 2023-2026) et [[reports/si_fattinger_report]] (SI 2017-2026 : b ≈ 1,2, rien après Holm). Phénomène classé « À surveiller » dans [[wiki/phenomenes]].*

## Hypothèse

Le mouvement de la nuit sur les métaux précieux, de la clôture 17:00 NY de la veille à 5:00 NY, se prolonge dans le même sens de 5:00 à 17:00 NY.

Formulation testée : dans la régression D = a + c·N, avec N = ln(P(5:00) / P(17:00 veille)) et D = ln(P(17:00) / P(5:00)), **c > 0**. C'est exactement la pente « b − 1 » des régressions d'absence de biais des rapports d'origine (b = 1 + c, même écart-type).

## Pourquoi ce test est hors échantillon

- La découverte vient des futures GC 2016-01 → 2026-08 et SI 2017-04 → 2026-08. **Les cours au comptant XAU/USD et XAG/USD de London Strategic Edge (marché `commodities`, 1 minute, depuis 2003-05) n'ont jamais été chargés ni regardés avant ce document.** Seules leurs dates de début et de fin ont été lues (`/v3/overview`).
- Les périodes testées s'arrêtent avant le début des échantillons de découverte : or 2003-05-05 → 2015-12-31, argent 2003-05-05 → 2017-03-31. Aucun recouvrement.
- Le comptant et le future front ne sont pas le même instrument (pas de roulement, autre microstructure), mais ils suivent le même prix à quelques points de base près. Un échec sur le comptant voudrait dire que l'effet de 2023-2026 n'est pas général ; un succès, que la continuation existe sur une autre période de 13 ans.

## Protocole figé (aucun paramètre ne sera modifié après calcul)

| Élément | Valeur |
|---|---|
| Données | XAU/USD et XAG/USD, 1 minute, London Strategic Edge (`/v3/export`, `market=commodities`), téléchargées par `fetch_lse.py` dans `cache/lse/` |
| Périodes | or 2003-05-05 → 2015-12-31 ; argent 2003-05-05 → 2017-03-31 |
| Jours | jours ouvrés lundi-vendredi d ; P0 = 17:00 NY du jour ouvré précédent (vendredi pour le lundi, donc week-end inclus), P1 = 5:00 NY de d, P2 = 17:00 NY de d (heure murale de New York, heure d'été gérée par fuseau) ; jour écarté si l'un des trois prix manque |
| Prix à un instant T | clôture de la dernière barre 1 minute démarrant dans [T−5 min, T−1 min] (même règle que `recolte1.engine.price_at`) |
| Statistique | pente c de la régression MCO de D sur N (avec constante), écart-type de White (HC0, comme `run_gc_fattinger.unbiased`) ; p unilatéral pour c > 0 |
| Règle tradable (secondaire) | position dans le sens de N (long si N > 0, short si N < 0, rien si N = 0) de 5:00 à 17:00 NY ; coût aller-retour du future rapporté au prix du jour : or 0,15 $/oz (1 tick GC + 5 $ / 100 oz), argent 0,006 $/oz (1 tick SI + 5 $ / 5 000 oz) |

## Tests (4 essais)

1. H1 : c > 0 sur l'or au comptant.
2. H2 : c > 0 sur l'argent au comptant.
3. Règle sur l'or : rendement net moyen par jour > 0.
4. Règle sur l'argent : idem.

Compteur global d'essais : 1 685 avant ce document → **1 689**.

## Critères de succès, fixés à l'avance

1. **Succès principal** si H1 **et** H2 ont p unilatéral < 0,05 après correction de Holm sur ces 2 tests.
2. **Et** c > 0 (signe seulement) dans chacune des deux sous-périodes, pour les deux métaux : 2003-05 → 2008-12 et 2009-01 → fin de période.
3. **Succès partiel** : un seul des deux métaux remplit 1 et 2. **Échec** : aucun.
4. Règles tradables (3 et 4) : rapportées avec moyenne nette, t de Newey-West (5 retards), IC 95 % bootstrap par blocs (`recolte1.engine.ci_mean`) et p unilatéral. Elles ne décident pas du succès, mais un succès principal avec des règles nettes ≤ 0 sera rapporté comme « phénomène sans valeur économique seule ».

Rapportés en plus, sans valeur de décision : c winsorisé (1 % de chaque côté de N et D), corrélation de rang N/D, c par année, nombre de jours.

## Conséquence fixée à l'avance

- **Succès** : la continuation passe dans « Confirmés » de [[wiki/phenomenes]] ; une règle (or + argent) est pré-enregistrée pour le holdout postérieur au 2026-08-28, à ouvrir une seule fois quand il comptera au moins 100 jours.
- **Succès partiel** : reste dans « À surveiller », avec le métal qui passe.
- **Échec** : ligne au registre des échecs ; l'effet de 2023-2026 est traité comme propre à ce régime. Réouverture seulement avec une variable de régime écrite à l'avance (mécanisme), testée sur le holdout.

## Ce qui est interdit après calcul

Changer les heures (17:00, 5:00, 17:00), les périodes, la règle de prix, le coût ; ajouter un filtre (tendance, volatilité, jour de semaine) ; exclure une année ; remplacer le comptant par un autre instrument.
