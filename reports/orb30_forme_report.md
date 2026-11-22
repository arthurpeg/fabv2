# ORB 30 minutes NQ, lundi à jeudi : clôture au-delà de la borne, heure de la cassure, ordres limite sur les bords

*2026-11-22. Suite de l'étape 1 de [[wiki/experiments/orb30-jours-semaine]]. Demande de l'utilisateur. Grille figée et commitée dans l'en-tête de [run_orb30_forme.py](../run_orb30_forme.py) avant tout calcul (commit `dd00ed2`). NQ, exploration 2016-06 → 2026-08 ; réserve 2010-06 → 2015-12 non lue. Compteur global : 2 079 (2 073 + 6 essais). Sorties : `results/orb30_forme/`.*

## Règles

Range 9:30-9:59 (1 R = W), stop 1 W, objectif 2R, sinon 16:00 ; 1 contrat, coût 0,50 pt ; lundis-jeudis (2 047 jours).
- **K1 / K5** : entrée sur la première bougie 1 min / 5 min (dès 10:00) qui clôture au-delà d'une borne, à l'open de la barre suivante.
- **H1 / H2 / H3** : ORB de Subhani (ordre stop sur la borne), gardé seulement si l'entrée a lieu à 10:00-11:00 / 11:00-13:00 / 13:00-16:00.
- **L** : ordres limite sur les deux bords dès 10:00 (vente au haut, achat au bas), le premier rempli gagne.

Vérification manuelle (2016-06-22) : K5, bougie 10:30-10:35 clôturée à 4 416 au-dessus de ORhi 4 411, achat à 10:35 à 4 416, stop à 4 405,75 ; L, achat limite à ORlo 4 400,75 rempli à 10:00, objectif 2R atteint (+20 pts net). Conformes.

## Résultats (R net par trade ; référence = ORB objectif 2R, toutes heures : 2 035 trades, +0,015 R)

| Règle | Trades | R net | t NW | Écart avec la référence (t) | Années + |
|---|---|---|---|---|---|
| K1 clôture 1 min | 2 025 | +0,000 | 0,01 | −1,48 pt/jour (−1,79) | 6/11 |
| K5 clôture 5 min | 2 002 | −0,003 | −0,12 | −1,67 pt/jour (−1,26) | 6/11 |
| L ordres limite sur les bords | 2 035 | −0,024 | −1,06 | −2,45 pt/jour (−0,59) | 5/11 |
| **H1 cassure 10:00-11:00** | 1 880 | **+0,022** | 0,96 | +0,099 R contre les autres heures (1,55) | 6/11 |
| H2 cassure 11:00-13:00 | 119 | −0,078 | −1,04 | −0,099 R (−1,34) | 4/11 |
| H3 cassure 13:00-16:00 | 36 | −0,072 | −0,64 | −0,089 R (−0,80) | 5/11 |

Par jour (R net) : K1 lun −0,03, mar +0,03, mer +0,03, jeu −0,04 ; L lun −0,05, mar −0,06, mer +0,01, jeu 0,00.

**Règle choisie (meilleur Sharpe) : H1.** n 1 880 · +0,022 R · t 0,96 · DSR (N = 81) ≈ 0. **B1 : ❌** (t et DSR).

## Lecture

1. **Attendre une clôture au-delà de la borne coûte** : on entre plus loin, et le gain disparaît (≈ 0 R, contre +0,015 R pour l'ordre stop). La confirmation ne trie pas les bonnes cassures.
2. **Les ordres limite sur les bords (pari sur le retour dans le range) perdent légèrement** (−0,024 R) : le contraire de la cassure ne marche pas non plus du lundi au jeudi.
3. **Heure** : 92 % des cassures ont lieu avant 11:00 (+0,022 R) ; les cassures tardives, rares, sont négatives (−0,07 à −0,08 R), sans être significatives.
4. Du lundi au jeudi, ni la cassure, ni son contraire, ni la confirmation, ni l'heure ne donnent d'avantage sur NQ.

Ligne au registre des échecs.
