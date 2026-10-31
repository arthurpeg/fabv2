# Pré-enregistrement n° 14 : éviter les annonces macro de 8:30 ET dans la règle NQ de nuit

*2026-10-31, avant tout calcul. Suite du n° 13 (filtres de prix rejetés). Ici, le filtre est fixé par un calendrier extérieur au prix : aucun seuil à régler.*

## Pourquoi

La position de la règle est ouverte de 20:00 ET à 9:30 ET. Les annonces BLS de l'emploi (NFP) et de l'inflation (CPI) tombent à **8:30 ET**, pendant la position. Boyarchenko-Larsen-Whelan attribuent la faiblesse de l'heure d'ouverture des jeudis et vendredis aux annonces macro de 8:30 ; sur NQ, les entrées de 7:00 à 9:00 perdent (récolte 1, comptes horaires). Hypothèse : une part des grosses pertes de nuit vient de ces annonces.

## Calendrier (figé)

[config/calendrier_macro_bls.csv](config/calendrier_macro_bls.csv) : 388 dates NFP et CPI, 2010-06 → 2026-08, extraites des archives officielles du BLS (lien de chaque communiqué dans le fichier ; toutes à 8:30 ET). PIB et PCE (BEA) non inclus : calendrier non récupéré, annonces de moindre impact. **Nuit d'annonce** = nuit qui se termine à l'ouverture d'une séance NYSE dont la date figure au calendrier.

## Règle de base (inchangée)

NQ, compte 20:00 ET, momentum 12-1, SL 2 ATR / TP 5 ATR (ATR 14 sur M15), sortie 9:30 ET, coût 1 tick + 5 $, en R, `run_recolte1_atr.simulate`.

## Deux variantes (2 essais ; compteur 1 471 → 1 473)

- **V1 : pas de trade les nuits d'annonce.**
- **V2 : sortie à 8:25 ET les nuits d'annonce** (au lieu de 9:30), SL/TP inchangés ; les autres nuits sont identiques à la base.

## Critères (identiques au n° 13)

Sur **2016-01 → 2026-08** (sélection), une variante est retenue si :
1. drawdown maximal en R réduit d'au moins 30 % ;
2. R par an ≥ 80 % de la base ;
3. réduction de drawdown supérieure au 95e centile de 500 contrôles aléatoires : on applique le même traitement (V1 : retirer ; V2 : sortir à 8:25) au même nombre de nuits tirées au hasard parmi les nuits sans annonce.

Puis **confirmée** si 1 et 2 tiennent sur 2011-07 → 2015-12.

Rapporté en plus, sans valeur de décision : R par trade des nuits d'annonce contre les autres nuits, et part des 10 pires nuits de la base qui sont des nuits d'annonce.

## Interdit après calcul

Ajouter des annonces (FOMC, PIB, PCE, ISM…), changer l'heure de sortie (8:25), combiner V1 et V2, changer critères ou périodes.
