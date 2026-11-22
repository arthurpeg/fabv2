# ORB 30 minutes NQ, lundi à jeudi : régime de gamma approché par le RSI 5 jours

*2026-11-22. Suite de l'étape 1 de [[wiki/experiments/orb30-jours-semaine]]. Source : Zarattini, Aziz, Barbon 2024 (*Beat the Market*, section 4.5 : RSI 5 jours bas → gamma négatif des teneurs de marché → tendances intraday prolongées ; pente −3,25, p 0,001 sur leur stratégie). Variante réintégration demandée par l'utilisateur. Grille figée et commitée dans l'en-tête de [run_orb30_rsi.py](../run_orb30_rsi.py) avant tout calcul (commit `99a2573`). NQ, exploration 2016-06 → 2026-08 ; réserve 2010-06 → 2015-12 non lue. Compteur global : 2 073 (2 071 + 2 essais). Sorties : `results/orb30_rsi/`.*

## Règles

RSI de Wilder, période 5, sur les clôtures de 16:00 de NQ, valeur de la veille ; seuil 50 (730 lundis-jeudis sur 2 120 sous 50). Range 9:30-9:59, 1 R = W, stop 1 W, objectif 2R, sinon 16:00 ; 1 contrat, coût 0,50 pt.
- **V1** : RSI < 50 → cassure (ORB de Subhani) ; RSI ≥ 50 → pas de trade.
- **V2** : RSI < 50 → cassure ; RSI ≥ 50 → réintégration des deux côtés (après une cassure puis une clôture de retour dans le range, ordre limite sur la borne, vers l'intérieur).

Vérification manuelle de deux réintégrations (2016-07-14, vente sur le haut après cassure à 10:05, retour à 10:07, remplissage à 10:09 ; 2016-07-05, achat sur le bas après cassure à 10:10, retour à 10:12, remplissage à 11:14) : conformes.

## Résultats (R net par trade)

| | Trades | R net | t NW | Référence | Écart (t) | Années + | DSR (N 75) |
|---|---|---|---|---|---|---|---|
| V1 filtre RSI < 50 | 706 | +0,018 | 0,48 | jours exclus +0,013 R | +0,005 R (0,10) | 7/11 | 0,003 |
| V2 cassure / réintégration | 1 943 | +0,006 | 0,27 | ORB tous les jours +0,88 pt/jour | −0,63 pt/jour (−0,23) | 7/11 | 0,000 |

Décomposition (non comptée) :

| | RSI < 50 | RSI ≥ 50 |
|---|---|---|
| Cassure | +0,018 R (n 706, t 0,45) | +0,013 R (n 1 329, t 0,45) |
| Réintégration | +0,014 R (n 656, t 0,34) | −0,000 R (n 1 237, t −0,01) |

Cassure par quintile de RSI 5 jours (du plus bas au plus haut) : +0,010 · +0,067 · −0,016 · −0,007 · +0,020 R. Aucune pente.

**B1 : ❌** (meilleure V1 : t 0,48, DSR 0,003, moitiés et « sans la meilleure année » ratés).

## Lecture

1. **Le RSI 5 jours ne distingue pas les jours où la cassure marche** : +0,018 R sous 50 contre +0,013 au-dessus, aucune pente par quintile.
2. **La réintégration ne marche pas mieux quand le RSI est haut** (−0,000 R) : l'hypothèse « gamma positif → les cassures échouent » ne se voit pas sur l'ORB de NQ du lundi au jeudi.
3. Le résultat du papier portait sur une autre stratégie (bande de bruit sur SPY, 2007-2024) et sur un indicateur indirect du gamma ; il ne se transpose pas ici.

Ligne au registre des échecs. Lundi-jeudi, l'ORB 30 min reste sans avantage sur NQ après la règle seule, C1-C3, le biais EMA et le RSI 5 jours.
