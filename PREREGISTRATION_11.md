# Pré-enregistrement n° 11 : la règle NQ de nuit (n° 10) hors échantillon dans le temps, 2011–2015

*2026-10-30, écrit pendant le téléchargement des données 2010–2015, avant de les avoir ouvertes. Données : Databento `GLBX.MDP3`, `ohlcv-1m`, `NQ.v.0`, `ES.v.0`, `YM.v.0`, 2010-06-06 → 2016-01-03 (achat de 19,93 $), dans `cache/databento_2010/`.*

## Pourquoi

La règle a été choisie sur NQ 2016–2026 après un tri de ~1 200 combinaisons (récolte 1). Le n° 10 l'a testée sur ES et YM 2016–2026 : échec. Les années 2010–2015 n'ont jamais été vues par aucune étape de cette recherche : c'est un vrai test hors échantillon dans le temps.

## Règle (identique au n° 10, rien ne change)

- Marché principal : **NQ**. Signal : momentum 12-1 de l'actif (somme des log-rendements close-to-close NYSE des mois M−12 à M−2) ; long si > 0, short si < 0, pour toutes les nuits du mois M.
- Entrée **20:00 ET** ; SL **2 × ATR**, TP **5 × ATR** (ATR de Wilder 14, bougies 15 min, dernière bougie terminée avant l'entrée) ; sortie à 9:30 ET sinon ; aucun trade après 17:00 ET.
- Exécution vectorbt `from_signals` 1 min (code de `run_recolte1_atr.py` / `run_prereg10.py`, inchangé) ; coût 1 tick + 5 $ par aller-retour.
- Données : série 2010–2015 raboutée à la série actuelle (`D:/quant-data/Cotations`, 2016+) à la date de jonction 2016-01-03, même ajustement en ratio des roulements (`recolte1.engine.load`).
- **Période de test : nuits du 2011-07-01 au 2015-12-31.** Juin 2010 est incomplet ; le premier mois de signal complet est juillet 2011 (mois de calcul juillet 2010 → mai 2011).

## Tests (4 essais ; compteur 1 455 → 1 459)

- **Principal (1)** : NQ, compte 20:00.
- **Secondaires (3)** : NQ bloc 19:00 + 20:00 + 21:00 (R par nuit) ; ES compte 20:00 ; YM compte 20:00.

## Critères, fixés à l'avance

Bootstrap par blocs mobiles circulaires (blocs de 10, 2 000 tirages), p unilatéral pour H1 : R moyen net > 0.

1. **Succès** si NQ 20:00 a un R moyen net par trade > 0 avec p unilatéral < 0,05, **et** un R moyen positif sur chacune des deux sous-périodes 2011-07 → 2013-12 et 2014 → 2015.
2. **Échec** sinon. Les tests secondaires sont rapportés tels quels et ne peuvent pas changer le verdict.

## Réserve connue avant calcul

Les spreads de nuit de 2010–2012 étaient plus larges qu'aujourd'hui sur NQ ; le coût fixe de 1 tick peut être optimiste au début de la période. On ne le corrige pas : le verdict porte sur le coût pré-enregistré, et on rapportera aussi le résultat brut.

## Interdit après calcul

Changer l'heure, les multiples d'ATR, l'ATR, la sortie, le signal, le coût, la période ou les sous-périodes ; ajouter un filtre ; exclure une année.
