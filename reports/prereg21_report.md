# Rapport n° 21 : continuation de la nuit sur l'or, hors échantillon dans le temps (or au comptant 2003-2015)

*2026-11-21. Protocole : [[PREREGISTRATION_21]] (commit a2dc0b1 du 2026-11-02, avant tout calcul) et son avenant A (commit 7fde669, avant calcul : argent indisponible, compté p = 1). Code : `run_prereg21.py`. Sorties : `results/prereg21/` (run.log, days_XAU.csv, by_year.csv).*

## Verdict : ❌ ÉCHEC

La continuation trouvée sur GC 2016-2026 (pente b(5:00) = 1,13, portée par 2023-2026, voir [[reports/gc_fattinger_report]]) **ne se retrouve pas** sur 13 ans d'or au comptant jamais regardés auparavant. Pente c = −0,005 (b = 0,995), t −0,09, p unilatéral 0,54, p Holm 1,00 ; signe négatif sur 2003-2008. Conformément au protocole, l'effet de 2023-2026 est traité comme propre à ce régime.

## Ce qui a été testé

- **Hypothèse** : le mouvement de 17:00 NY (veille) à 5:00 NY se prolonge de 5:00 à 17:00 NY. Régression D = a + c·N, avec N = ln(P5:00 / P17:00 veille) et D = ln(P17:00 / P5:00) ; succès si c > 0.
- **Données** : XAU/USD au comptant, London Strategic Edge, 1 minute, 2003-05-05 → 2015-12-31, aucun recouvrement avec l'échantillon de découverte (GC dès 2016). Prix à un instant T : clôture de la dernière barre démarrant dans [T−5 min, T−1 min].
- **Argent** : non testé (avenant A). Les données 2003-2017 ne sont plus accessibles (LSE limité à 10 ans, Dukascopy sans barres avant 2016). Compté p = 1 dans la correction de Holm sur 2 tests, ce qui revient à doubler le p de l'or. Le meilleur verdict possible était donc « succès partiel ».

## Résultats (or)

| Mesure | Valeur |
|---|---|
| Jours retenus | 2 803 sur 3 304 jours ouvrés (couverture faible en 2003-2005 : 37, 82 et 189 jours ; ≥ 237 par an dès 2006) |
| N (17:00 veille → 5:00) | moyenne +3,80 bp, σ 59,4 bp |
| D (5:00 → 17:00) | moyenne −0,93 bp, σ 106,9 bp |
| **Pente c (principal)** | **−0,0054** (écart-type White 0,0585, t −0,09, p unilatéral 0,54, **p Holm 1,00**) → b = 0,995 |
| 2003-05 → 2008-12 | c −0,1015 (t −1,03, n 1 066) : **signe négatif**, critère 2 non rempli |
| 2009-01 → 2015-12 | c +0,0819 (t +1,35, n 1 737) |
| c winsorisé 1 % (rapporté) | +0,0168 (t +0,39) |
| Corrélation de rang N / D (rapportée) | +0,023 (p 0,22) |

c par année : 2003 +0,05 ; 2004 +0,10 ; 2005 −0,16 ; 2006 +0,10 ; 2007 +0,18 ; 2008 −0,26 ; 2009 +0,10 ; 2010 +0,00 ; 2011 −0,01 ; 2012 −0,06 ; 2013 +0,25 ; 2014 +0,16 ; 2015 −0,05. Sept années positives sur treize, sans tendance nette.

**Règle tradable (secondaire)** : dans le sens de N, de 5:00 à 17:00, coût 0,15 $/oz (≈ 1,69 bp en moyenne) :
- brut +1,39 bp/jour [−2,27 ; +5,20], t NW +0,70, p unilatéral 0,25, Sharpe +0,21 ;
- **net −0,30 bp/jour** [−3,97 ; +3,52], t NW −0,15, p unilatéral 0,56 (Holm 1,00), Sharpe −0,04.

## Lecture

- Sur 2003-2015, la nuit de l'or ne dit rien de la suite de la journée : la pente est nulle et les deux sous-périodes ont des signes opposés. La pente de GC 2016-2026 (0,97 / 1,07 / 1,21 selon les sous-périodes) était déjà nulle en 2016-2019 ; l'ensemble est cohérent avec un effet propre à la forte tendance de 2023-2026, ou à du bruit sélectionné parmi 23 coupures.
- Limites : comptant et non future (même prix à quelques points de base près) ; couverture incomplète en 2003-2005 ; argent non testé. Aucune de ces limites ne peut transformer une pente de −0,005 en effet positif.

## Conséquences (fixées dans le protocole)

- Ligne au [[wiki/Failed Ideas/ledger|registre des échecs]]. Réouverture seulement avec une variable de régime écrite à l'avance (mécanisme), testée sur le holdout postérieur au 2026-08-28.
- [[wiki/phenomenes]] : la ligne « À surveiller » reçoit la mention « ⚠️ contredit le 2026-11-21 ».
- [[wiki/reserves]] : or au comptant 2003-2015 → consommée.
- Compteur global inchangé (essais déjà comptés au pré-enregistrement).
