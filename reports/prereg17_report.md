# Pré-enregistrement n° 17 — exécution au VWAP : non retenue

*2026-10-31. Protocole : [PREREGISTRATION_17.md](../PREREGISTRATION_17.md). Code : [run_prereg17.py](../run_prereg17.py). Résultats : [results/prereg17/](../results/prereg17/). Compteur global : 1 482.*

Gain en R d'une exécution répartie au VWAP par rapport au prix à heure fixe (positif = le VWAP fait mieux), règle de nuit 20:00, nuits 2011-07 → 2026-08.

| Marché | E1 : entrée au VWAP 20:00–21:00 [IC 95 %] | E2 : sortie au temps au VWAP 9:00–9:30 [IC 95 %] | R moyen par trade de la règle |
|---|---|---|---|
| NQ | +0,0045 [−0,007 ; +0,015] | −0,0007 [−0,013 ; +0,011] (1 222 sorties au temps) | +0,088 |
| ES | +0,013 [+0,002 ; +0,023] | −0,005 [−0,018 ; +0,007] | +0,009 |
| YM | +0,013 [+0,001 ; +0,023] | −0,001 [−0,017 ; +0,016] | +0,026 |

## Verdict pré-enregistré

**Ni E1 ni E2 retenus** : sur NQ, l'IC des deux gains inclut zéro. On garde l'exécution à heure fixe.

- Entrée : le VWAP de 20:00–21:00 est en moyenne très légèrement plus favorable que le prix de 20:00 (de +0,005 à +0,013 R, soit 5 à 15 % de l'avantage de la règle sur NQ). C'est significatif sur ES et YM, pas sur NQ. L'écart est petit face à l'incertitude de coût d'une exécution étalée (spread payé ou gagné), non mesurée ici.
- Sortie : aucun gain à étaler la sortie avant l'ouverture.
- Approximations (déclarées avant calcul) : SL/TP non resimulés avec le nouveau prix d'entrée ; spread non pris en compte. Les données `bbo-1m` permettront de mesurer le coût réel d'une exécution à heure fixe contre étalée.
