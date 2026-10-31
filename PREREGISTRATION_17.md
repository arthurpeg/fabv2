# Pré-enregistrement n° 17 : exécution au VWAP au lieu d'un prix à heure fixe (règle de nuit 20:00)

*2026-10-31, avant calcul. Question d'exécution, pas un nouveau signal : les nuits tradées et leur sens ne changent pas.*

## Ce qu'on compare

Pour chaque trade de la règle de nuit (compte 20:00 ET, momentum 12-1, SL 2 ATR / TP 5 ATR, sortie 9:30 ET), on mesure en R l'écart de prix entre une exécution répartie au VWAP et l'exécution actuelle à heure fixe :

- **E1 entrée** : prix moyen VWAP des barres 1 minute de 20:00 à 21:00 ET (prix typique (H+B+C)/3 pondéré par le volume) au lieu du prix de 20:00.
  Gain en R = sens × (P20:00 − VWAP) / (2 × ATR).
- **E2 sortie au temps** (seulement les trades sortis à 9:30, ni SL ni TP) : VWAP de 9:00 à 9:30 ET au lieu du prix de 9:30.
  Gain en R = sens × (VWAP − P9:30) / (2 × ATR).

Approximation déclarée : on garde les sorties SL/TP de la base (on ne resimule pas les stops avec le nouveau prix d'entrée), et on ignore le coût de transaction propre à une exécution étalée (spread payé ou gagné), qui demandera les données `bbo-1m` en cours de téléchargement.

## Critère (fixé à l'avance ; compteur 1 480 → 1 482)

Pour E1 et E2 séparément : l'exécution VWAP est **retenue** si le gain moyen en R est > 0 avec un IC 95 % (bootstrap par blocs) entièrement > 0 sur **NQ 2011-07 → 2026-08**, et de même signe sur ES et YM. Sinon on garde l'exécution à heure fixe.

## Interdit après calcul

Changer les fenêtres (20:00–21:00, 9:00–9:30), le prix typique, ou chercher une autre fenêtre de VWAP.
