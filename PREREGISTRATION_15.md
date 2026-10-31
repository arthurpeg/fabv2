# Pré-enregistrement n° 15 : filtres VIX des papiers (Donninger, Vojtko) et taille selon la volatilité, règle NQ de nuit

*2026-10-31, avant tout calcul avec ces données. Suite des n° 13 et 14 (filtres de prix et d'annonces rejetés). Les deux filtres sont des règles écrites dans des papiers de la récolte 1, laissées de côté faute de données VIX ; seuils fixés par les papiers.*

## Données ajoutées (figées)

[config/cboe_VIX_history.csv](config/cboe_VIX_history.csv) et [config/cboe_VIX3M_history.csv](config/cboe_VIX3M_history.csv) : historiques quotidiens officiels du CBOE (téléchargés le 2026-10-31). Clôture du jour d−1 (16:15 ET), connue avant l'entrée de 20:00 ET.

## Règle de base (inchangée)

NQ, compte 20:00 ET, momentum 12-1, SL 2 ATR / TP 5 ATR, sortie 9:30 ET, coût 1 tick + 5 $, en R. Nuit d = nuit qui se termine à l'ouverture de la séance NYSE d ; les variables portent sur la séance d−1.

## Trois essais (compteur 1 475 → 1 478)

| # | Source | Règle |
|---|---|---|
| F5 | Donninger [14] | trader la nuit seulement si VIX / VIX3M (clôtures de d−1) > **0,87** |
| F6 | Vojtko-Hanicová [15] | trader la nuit seulement si VIX (clôture de d−1) < sa moyenne mobile **20** séances |
| T1 | taille selon la volatilité | multiplier le résultat de la nuit (en R) par w = min(1 ; M / σ20), σ20 = écart-type des rendements close-to-close NQ sur les 20 séances jusqu'à d−1, M = médiane historique de σ20 (fenêtre expansive, ≥ 250 obs). La taille n'est jamais augmentée, seulement réduite quand la volatilité dépasse sa médiane. |

**Réserve déclarée avant calcul** : le rapport descriptif [robust13](reports/robust13_report.md) a déjà montré que les nuits de volatilité haute avaient le meilleur rendement moyen (en bp) mais un Sharpe plus faible. T1 n'a pas été calculé, mais sa direction a été « vue » en partie.

## Critères (fixés à l'avance)

**Sélection : NQ, 2016-01 → 2026-08.**
- F5, F6 (filtres) : mêmes critères que le n° 13 — drawdown max en R réduit d'au moins 30 %, R/an ≥ 80 % de la base, réduction de DD > 95e centile de 500 filtres aléatoires de même participation.
- T1 (taille) : le ratio R/an ÷ |max DD| doit dépasser celui de la base d'au moins **20 %**, et le max DD doit baisser d'au moins 20 %.

**Confirmation (pour ce qui passe la sélection)** : les mêmes critères, hors contrôle aléatoire, doivent tenir sur **NQ 2011-07 → 2015-12**, **et** sur **ES et YM 2011-07 → 2026-08** (même règle de base 20:00 sur ces marchés, avec leur propre momentum ; pour T1, σ20 de chaque marché).

Verdict par essai : retenu (sélection) → confirmé (les trois confirmations) ; sinon rejeté.

## Interdit après calcul

Changer 0,87, la MM20, la fenêtre de 20 séances, le plafond de taille (1), la médiane, combiner les règles, changer critères, périodes ou marchés.
