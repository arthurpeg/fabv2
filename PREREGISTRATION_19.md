# Pré-enregistrement n° 19 : S1 Noise Area NQ + stop dur 1R hors échantillon dans le temps, 2010–2015

*2026-10-31, avant calcul. Aucune séance cash 9:30–16:00 de 2010–2015 n'a été passée dans une règle intraday de ce dépôt : les données `cache/databento_2010/` (Databento `NQ.v.0` 1 minute, 2010-06-06 → 2016-01-03) n'ont servi qu'aux règles de nuit (n° 11, 12, prop firm).*

## Pourquoi

La variante « S1 + stop dur 1R » (fichier `S1_R_stop.py` transmis, refait dans [run_s1_r_stop_vbt.py](run_s1_r_stop_vbt.py)) donne sur NQ 2016-01 → 2026-08 : +0,106 R/trade (t 4,0), Sharpe en R 1,26. Mais le plancher de R (0,5 %) a été choisi après avoir vu ces résultats, et la famille (bande de bruit M2 sur NQ) est rejetée au DSR (0,03, [PREREGISTRATION_2](PREREGISTRATION_2.md) piste B). Le DSR approché de la variante est ≈ 0,05 à N = 96 et 0,000 à N = 1 482.

Les années 2010–2015 sont la seule période jamais vue par cette famille avant le holdout post-2026-08-28.

**Registre des échecs** : la ligne « Bande de bruit M2 sur NQ » ne prévoit une réouverture que sur le holdout postérieur au 2026-08-28. Cette condition **n'est pas remplie** ; le test est lancé à la demande explicite de l'utilisateur. En conséquence : **un succès ne rouvre pas M2 et ne vaut pas validation** ; il justifie seulement de pré-enregistrer la variante sur le holdout. Un échec ajoute une ligne au registre pour la variante.

## Règle (figée, identique à `run_s1_r_stop_vbt.py`, configuration « stop1R_p0.5 »)

- Séance cash XNYS 9:30–16:00 New York (13:00 les demi-séances). Prix : `recolte1.engine.load("NQ")` avec l'historique 2010 rabouté (`USE_2010 = True`), ramenés au contrat de la séance ; clôture veille au même contrat.
- sigma(t) = moyenne des |Close(t) / Open − 1| des **30** séances précédentes à la même minute ; Upper = max(Open, veille) × (1 + **1,2** sigma) ; Lower = min(Open, veille) × (1 − 1,2 sigma) ; filtre de démarrage : volatilité close-to-close **14** séances définie.
- Contrôles toutes les 30 min (10:00 … 15:30) : long si Close > Upper et > VWAP, short si Close < Lower et < VWAP, sinon à plat ; ordre à l'ouverture de la minute suivante ; sortie à la clôture.
- R = max(|Close − stop suiveur|, **0,5 %** × Close) ; stop dur à 1R du prix du contrôle, vérifié chaque minute ; **1 contrat** par trade.
- Exécution vectorbt `from_signals` (code de `run_s1_r_stop_vbt.py`, inchangé), contrôlée par la boucle d'origine.
- **Coût principal : NQ, 2,25 $ de commission + 1 tick par côté** (MNQ n'existe qu'à partir de 2019).
- **Période de test : trades du 2010-09-01 au 2015-12-31** (juin–août 2010 servent au démarrage de sigma). Sous-périodes : 2010-09 → 2012-12 et 2013 → 2015.

## Tests (3 essais ; compteur 1 482 → 1 485)

- **Principal (1)** : la règle ci-dessus, R net par trade.
- **Secondaires (2)** : S1 d'origine (sans stop dur, plancher 0) en dollars par jour, coût NQ ; plancher 0,3 % + stop 1R. Rapportés aussi : R brut, coût MNQ (0,60 $ + 1 tick), Sharpe journalier en R et en $, R par année, DSR approché à N = 1 485 (dispersion des Sharpe du B1). Ils ne peuvent pas changer le verdict.

## Critères, fixés à l'avance

Bootstrap par blocs mobiles circulaires (blocs de 10 trades, 2 000 tirages), p unilatéral pour H1 : R moyen net > 0 (`run_prereg10.p_one_sided`).

1. **Succès** si le principal a un R moyen net par trade > 0 avec p unilatéral < 0,05, **et** un R moyen net positif sur chacune des deux sous-périodes.
2. **Échec** sinon.

## Réserves connues avant calcul

- En 2010–2012, le NQ cotait ~1 800–2 800 : R ≥ 0,5 % ≈ 9–14 points, donc le coût aller-retour NQ (≈ 0,73 point) pèse ≈ 0,05–0,08 R, plus qu'en 2016–2026. On ne le corrige pas.
- Volume intraday plus faible en 2010 ; VWAP calculé sur le volume du contrat `.v.0`.

## Interdit après calcul

Changer le plancher, la bande, le nombre de séances, les heures de contrôle, le stop, le coût, la période ou les sous-périodes ; ajouter un filtre ; exclure une année.
