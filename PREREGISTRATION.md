# Pré-enregistrement des backtests (vectorbt)

*Écrit le 2026-10-12, **avant** d'avoir lancé un seul backtest. Les paramètres ci-dessous sont figés : aucun ne sera optimisé. Toute variante ajoutée après coup sera marquée « post-hoc » dans le rapport et comptée dans le nombre total de tests.*

Source des hypothèses : [recherche_causalite_intraday.md](recherche_causalite_intraday.md).

## Données

- Futures continus Databento `.v.0` (roulement au volume), barres 1 minute, `D:\quant-data\Cotations`, du 2016-01-03 au 2026-08-28.
- Actifs : ES, NQ, YM (indices US) · CL (pétrole) · GC (or) · 6E, 6J, 6B, 6A (FX). FDAX est exclu (historique trop court).
- **Roulements** : les séries ne sont pas ajustées, et les sauts de roulement tombent sur la barre de 00:00 UTC. Une barre de 00:00 UTC est considérée comme un roulement si `|open/close_préc − 1| > 12 ×` la médiane mobile (1 440 barres) des |rendements 1 minute|, avec un plancher de 0,1 %. Les prix antérieurs sont alors ajustés en ratio. Les coûts sont calculés sur le prix brut.
- **Exécution** : une décision prise à l'heure T utilise uniquement les barres qui se terminent au plus tard à T. Elle est exécutée à l'**open de la barre qui commence à T** (ou de la première barre dans les 5 minutes suivantes ; sinon pas de trade ce jour-là). Les stops ORB sont exécutés au niveau du stop, ou à l'open si le marché a gappé au-delà.
- **Taille** : 100 % du notionnel (±1×), sans levier, sans capitalisation intrajournalière. Toutes les stratégies sont **à plat en fin de fenêtre**, donc aucune position n'est gardée pendant un roulement.

## Coûts (aller-retour, par contrat) = 1 tick de slippage + 5 $ de commission

| Actif | Tick | $/point | Coût aller-retour (points) |
|---|---|---|---|
| ES | 0,25 | 50 | 0,35 |
| NQ | 0,25 | 20 | 0,50 |
| YM | 1 | 5 | 2 |
| CL | 0,01 | 1 000 | 0,015 |
| GC | 0,10 | 100 | 0,15 |
| 6E | 0,00005 | 125 000 | 0,00009 |
| 6B | 0,0001 | 62 500 | 0,00018 |
| 6J | 0,0000005 | 12 500 000 | 0,0000009 |
| 6A | 0,00005 | 100 000 | 0,0001 |

## Sessions de référence

| Actif | Fuseau | Ouverture | Clôture |
|---|---|---|---|
| ES, NQ, YM | America/New_York | 09:30 | 16:00 |
| CL | America/New_York | 09:00 | 14:30 |
| GC | America/New_York | 08:20 | 13:30 |
| 6E, 6J, 6B, 6A | Europe/London | 08:00 | 16:00 |

## Échantillons et critère de survie

- **In-sample (IS)** : 2016-01-01 → 2022-12-31. **Out-of-sample (OOS)** : 2023-01-01 → 2026-08-28. Les deux sont rapportés. Aucun paramètre n'étant ajusté, l'OOS sert de test de stabilité (et de test du régime post-2023 / 0DTE).
- Sharpe annualisé calculé sur les rendements journaliers, jours sans position compris (0), × √252.
- **Une stratégie « survit »** si son Sharpe **net** est > 0,5 en IS **et** > 0,3 en OOS, avec le même signe, **et** si son trade moyen net est positif sur l'ensemble de la période. Avec environ 100 tests, on attend environ 5 faux positifs à 5 %. Ce critère n'est donc qu'un filtre de première passe, pas une preuve.

## Stratégies (paramètres figés)

### M1. Momentum intraday (section 1 de la recherche)
- **M1a, Gao et al.** : prédicteur = rendement entre la clôture de session J-1 et ouverture + 30 minutes. On prend la position `sign(prédicteur)` sur la dernière demi-heure [clôture − 30 min, clôture]. Les 9 actifs.
- **M1b, Baltussen et al.** : prédicteur = rendement entre la clôture J-1 et clôture − 30 minutes. Même cible. Les 9 actifs.
- **M1c, Rosa + Li/Sakkas/Urquhart (conditionnel)** : M1b, mais seulement si |z| > 1, où z = prédicteur / écart-type des 60 jours précédents du prédicteur, **et** si le range (high − low)/open de la session jusqu'à clôture − 30 min dépasse la médiane des 60 jours précédents. Les 9 actifs.
- **M1d, pétrole EIA (Wen et al. 2022)** : sur CL, le mercredi, le prédicteur est la demi-heure de réaction 10:30 → 11:00 ET (le communiqué EIA tombe à 10:30). Les autres jours, on applique M1a. Cible : 14:00 → 14:30.

### M2. Bande de bruit (Zarattini, Aziz, Barbon 2024, « Beat the Market »)
- ES, NQ, YM, sur la session 09:30-16:00 ET. σ(m) = moyenne, sur les 14 jours précédents, de |prix(m)/open − 1| pour chaque minute m. Bande haute = max(open, clôture J-1)·(1+σ(m)), bande basse = min(open, clôture J-1)·(1−σ(m)).
- Contrôle toutes les 30 minutes, de 10:00 à 15:30 : position longue si prix > bande haute, courte si prix < bande basse. Le stop suiveur, vérifié aux mêmes heures, est max(bande haute, VWAP) pour une position longue et min(bande basse, VWAP) pour une courte. Clôture à 16:00. Pas de dimensionnement à volatilité cible (on reste à 1×).

### M3. Opening Range Breakout (section 2)
- **M3a** : range des 30 premières minutes de la session. Entrée stop à la première cassure du haut ou du bas, stop à l'autre extrémité du range, sortie à la clôture de session. Un trade par jour ; si une même barre casse les deux côtés avant l'entrée, pas de trade. Les 9 actifs.
- **M3b** : même règle avec un range de 5 minutes (le « pire » selon Fetna 2026). Les 9 actifs.
- **M3c** : M3a, seulement si le volume du range dépasse 1,5 fois la moyenne des 14 jours précédents (proxy « in play »). Les 9 actifs.

### M4. Sur-réaction et reversal (section 3)
- **M4a** : z = rendement des 30 premières minutes / écart-type des 60 jours précédents. Si |z| > 2 : position **contrarienne** sur les indices (ES, NQ, YM), dans le **sens du mouvement** pour CL, GC et le FX (inertie, Caporale et al.). Entrée à ouverture + 30 minutes, sortie à la clôture. Les 9 actifs.
- **M4b, fade du gap sur indices** : gap = open de session / clôture J-1 − 1, z sur 60 jours. Si |z| > 2, position contrarienne de ouverture + 1 minute jusqu'à la clôture. ES, NQ, YM.
- **M4c, lendemain d'un jour anormal (Caporale & Plastun 2021)** : z du rendement de session (clôture/clôture) sur 60 jours. Si |z| > 2, le lendemain : position **contrarienne** sur GC et **dans le sens du mouvement** sur CL, de l'ouverture à la clôture de session.

### M5. Saisonnalité horaire et fixings (section 4)
- **M5a, Bondarenko & Muravyev** : ES long de 01:00 à 05:00 ET (4 heures autour de l'ouverture européenne de 03:00 ET), chaque jour ouvré.
- **M5b, fix WMR de Londres (Krohn et al.)** : jambe pré-fix long USD (short sur le future) de 15:00 à 16:00 Londres ; jambe post-fix short USD (long sur le future) de 16:00 à 17:00 Londres. Les deux jambes sont rapportées séparément. 6E, 6B, 6J, 6A.
- **M5c, fix de Tokyo (Krohn et al.)** : long USD de 08:55 à 09:55 JST, short USD de 09:55 à 10:55 JST. Deux jambes, 4 devises.
- **M5d, Breedon & Ranaldo** : la devise se déprécie pendant ses propres heures. Short 6E et 6B de 08:00 à 12:00 Londres, short 6J de 09:00 à 15:00 Tokyo, short 6A de 10:00 à 16:00 Sydney.

**Total pré-enregistré** : M1 28 + M2 3 + M3 27 + M4 14 + M5 1+8+8+4 = **93 tests**.
