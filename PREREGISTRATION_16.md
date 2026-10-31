# Pré-enregistrement n° 16 : pression vendeuse de fin de séance (clôture sous le VWAP de la dernière heure) et règle de nuit 20:00

*2026-10-31, avant tout calcul. Mécanisme : Boyarchenko-Larsen-Whelan [1] (récolte 1) — des ventes nettes en fin de séance US (15:15–16:15 ET) sont absorbées par les teneurs de marché et suivies d'un rendement de nuit plus élevé. Le papier mesure ce déséquilibre par le volume signé (RSV), absent de nos données ; on l'approche par la position de la clôture par rapport au VWAP de la dernière heure.*

## Signal (connu à 16:15 ET de la séance d−1, avant l'entrée de 20:00)

- VWAP = Σ (prix typique × volume) / Σ volume, prix typique = (haut + bas + clôture) / 3, sur les barres 1 minute qui démarrent dans [15:15 ; 16:15[ ET de la séance d−1.
- Prix de clôture = clôture de la dernière barre qui se termine à 16:15 ET (convention `price_at`).
- **S = 1 si clôture < VWAP** (la dernière heure a surtout échangé au-dessus de la clôture → pression vendeuse). Demi-séances et heures sans barres : S indéfini, la nuit ne compte pas comme S.

## Règle de base (inchangée)

Compte 20:00 ET, momentum 12-1 de l'actif, SL 2 ATR / TP 5 ATR (ATR 14 sur M15), sortie 9:30 ET, coût 1 tick + 5 $, en R. Nuits 2011-07 → 2026-08 (historique 2010-2015 rabouté).

## Deux essais (compteur 1 478 → 1 480)

- **H (hypothèse du papier)** : le R moyen par trade des nuits S est supérieur à celui des autres nuits. Différence testée par bootstrap par blocs (blocs de 10, 2 000 tirages), p unilatéral.
- **V1 (filtre)** : ne trader que les nuits S.

## Critères (fixés à l'avance)

**Sélection : ES et YM, 2011-07 → 2026-08, chacun séparément** (marchés où l'heure, les stops et le signal n'ont jamais été choisis).
- H : différence > 0 avec p unilatéral < 0,05 **sur ES et sur YM**.
- V1 : sur ES et sur YM, mêmes critères que le n° 13 : drawdown max en R réduit d'au moins 30 %, R/an ≥ 80 % de la base, réduction de DD > 95e centile de 500 filtres aléatoires de même participation.

**Confirmation : NQ 2011-07 → 2026-08**, pour ce qui passe la sélection : H avec p < 0,05 ; V1 avec les deux premiers critères.

## Interdit après calcul

Changer la fenêtre (15:15–16:15), le prix typique, le sens du signal, combiner avec d'autres filtres, changer critères, marchés ou périodes.
