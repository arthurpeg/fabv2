---
type: experiment
updated: 2026-11-21
status: abandoned
verdict: ❌ critère gain / bruit ≥ 0,15 non atteint (A 0,05, B 0,134)
prereg: []
trials: 1937
---

# Dérive du yen en session US : la concentrer pour un format prop firm

**Une phrase** : chercher une version du short yen en session US dont le rapport gain / bruit par trade est assez élevé pour passer une éval FTMO vite. Deux leviers : les heures où la dérive se concentre (A), et les jours où le signal de retournement est fort (B).

## Étape 0 : fiche d'idée (2026-11-21)

1. **Déjà vu ?**
   - Le phénomène de base est confirmé ([[wiki/phenomenes]], « le yen baisse en session US ») et le filtre R4 est « À surveiller » ([[reports/jpy_us_filtres_report]]).
   - Au registre des échecs : les stops sur le short yen (44 variantes en tout, dont 24 sur R4) et le filtre de volatilité. Aucune des deux questions ci-dessous n'y figure.
   - Ce n'est pas un nouveau phénomène : c'est une **concentration** du même effet, à ne pas compter deux fois.
2. **Mécanisme supposé** :
   - A : 11:00 ET = 16:00 Londres, heure du fixing WM/Reuters, où arrivent de gros flux de change qui pourraient porter une partie de la dérive.
   - B : retournement des hausses récentes du yen (Piccotti, SSRN 2446584), éventuellement proportionnel à leur taille.
3. **Taille attendue face au coût** : sur la fenêtre complète, brut +2,0 bp (+3,2 les jours R4) contre environ 1,1 bp de coût standard. Une fenêtre plus courte garde le même coût par trade, mais son bruit est plus faible.
4. **Critère d'intérêt, fixé avant le calcul** : un **rapport gain / bruit par trade** (net moyen divisé par l'écart type du trade, coût standard 1 tick + 5 $) **≥ 0,15**.
   - Pour comparaison : 0,07 pour R4 avec SL 2 ATR H1, et environ 0,04 pour la règle du n° 28.
   - En dessous de 0,15, l'idée n'est pas utile en prop firm, et on arrête.
5. **Découpage des données (réserve par question, [PROTOCOLE.md](../../PROTOCOLE.md) étape 0, point 4)** :
   - Le 6J 2016 → 2026-08-28 est exploré pour l'effet de base et pour R4. En revanche, le **profil par demi-heure** de 08:00 à 17:00 ET et les **déciles de la hausse sur 3 jours** n'ont jamais été calculés.
   - **Exploration** : 6J du 2016-01-04 au 2023-06-30 (70 %).
   - **Réserve** pour ces deux questions : 6J du 2023-07-01 au 2026-08-28 (3,2 ans), déclarée dans [[wiki/reserves]].
   - Sur la réserve, le verdict portera sur l'écart avec la référence : fenêtre retenue contre fenêtre complète, et seuil retenu contre R4 et contre tous les jours. Le net seul ne comptera pas.
   - **Indices déjà vus sur toutes les années**, donc la réserve n'est pas totalement neuve :
     - R4 (binaire) ;
     - la moyenne par année ;
     - la dérive de la fenêtre 11:00 → 16:55 en entier ;
     - la session « LDN-NY » 08:00 → 11:00 NY du n° 27, qui n'était pas significative pour le yen.
6. **Puissance** : sur environ 360 trades R4 dans la réserve, un rapport de 0,15 donne un t attendu de 2,85, soit une puissance d'environ 89 %. À la moitié de cet effet, elle tombe à environ 41 %.

**B0** : ✅. Idée nouvelle, découpage écrit, puissance connue.

## Étape 1 : exploration

- Grille A + B figée dans l'en-tête de [run_yen_derive_ab.py](../../run_yen_derive_ab.py), commitée avant le calcul.
- Résultats : [[reports/yen_derive_ab_report]] (branche strategies-vbt), compteur 1 839 → 1 937.
- **A** : aucune fenêtre courte ne bat 11:00 → 16:55. La meilleure (R4, 15:00 → 16:55) a un rapport gain / bruit de 0,051 contre 0,081 pour la fenêtre complète. La dernière heure 16:00 → 16:55 porte environ la moitié du brut (t 4,3) avec peu de bruit, mais pas assez pour payer 1 bp de coût.
- **B** : le décile du haut de la hausse sur 3 jours fait +5,5 bp net (gain / bruit 0,18, t 3,0). Le meilleur seuil ex ante est q 0,8 : 17 % des jours, +3,6 bp, rapport 0,134, t 2,6, mais DSR 0,40 à N = 140.
- **Verdict** : ❌, l'idée s'arrête. La réserve 2023-07 → 2026-08 n'est pas ouverte.

## Liens

[[reports/jpy_us_filtres_report]] · [[reports/jpy_us_r4_stops_report]] · [[PREREGISTRATION_28]] · [[PREREGISTRATION_29]]
