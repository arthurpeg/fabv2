# Argent (SI) : les affirmations de Fattinger-Ziegler, comparées à l'or

*2026-11-02. Exploratoire, non pré-enregistré, demandé en séance. Compteur global : 1 631 → 1 685 (54 tests, mêmes définitions que pour l'or). Code : [run_gc_fattinger.py](../run_gc_fattinger.py) `SI` ; données : [fetch_lse.py](../fetch_lse.py), chargement et roulements dans `recolte1.engine._load_lse` / `lse_rolls`. Sorties : `results/si_fattinger/`. Rapport or : [[reports/gc_fattinger_report]].*

## Données

- Argent 1 minute, London Strategic Edge, marché `futures` (plan gratuit), 2017-04-02 → 2026-08-28. Rien avant 2017. Même horodatage que Databento (leur GOLD colle à notre GC à 1 tick près).
- La série reste sur le contrat qui expire jusqu'au mois de livraison (H K N U Z) : 2 à 3 séances minces avant chaque roulement. Roulement détecté comme la première séance de volume normal qui suit une séance mince, à partir du 1er du mois − 4 jours (48 roulements, écart moyen 0,8 %). Vérifié à la main : 4 roulements restent ambigus (écarts concurrents ≤ 0,4 %, dont juillet et août 2026, où la série n'a plus de séances minces).
- Écartées en plus du filtre de l'or : 19 séances minces et les 48 séances de roulement. Il reste **1 954 jours** (2017-04-04 → 2026-08-26). La sous-période « 2016-2019 » ne commence qu'en avril 2017.
- L'argent est 2,1 fois plus volatil que l'or (σ journalier 219 bp contre 102).

## Résultats, comparés à l'or

| Code | Affirmation | Or (2016-2026) | Argent (2017-2026) | Verdict argent |
|---|---|---|---|---|
| H1 | Contribution au prix ≈ 0 avant 3:00 NY | 26,5 % | **28,5 %** [25,0 ; 32,2] (20 / 27 / 33 % par sous-période) | ❌ contredit, comme l'or |
| H2 (×8) | Prix et variance ensemble | aucun écart | séance Europe+US (9:30-11:30) +2,9 pts (p 0,02, Holm 0,19) ; Asie +2,6 pts (p 0,10) | ✅ (rien après Holm) |
| H3 | Prix bruité (b < 1) en début de Globex | b(19:00) 0,68, n.s. | b(19:00) 0,59, n.s. (0,86 winsorisé) | ❌ non confirmé |
| H3 | b ≈ 1 ensuite | b > 1 de 4:00 à 8:00 (Holm 0,02 à 5:00) | b ≈ 1,2 de 22:00 à 8:00, p 0,005 à 0,07, **aucun après Holm** | ⚠️ même signe que l'or |
| H4 | Efficience qui chute avant l'Europe | non | non (+0,034, p 0,09, sens inverse) | ❌ |
| H5.1 | Pic à l'ouverture de Tokyo | × 2,0 | × 1,7 | ✅ |
| H5.2 | Montée pendant l'Asie | test mal spécifié | test mal spécifié (× 0,87) ; profil : creux 23:00-0:00 (9,1 bp), 3:00 (13,0) | ❌ tel que défini |
| H5.3 | Hausse à l'ouverture européenne | × 1,22 | × 1,19 [0,95 ; 1,61], n.s. | ❌ |
| H5.4 | Pic à 8:20 | × 1,9 | × 1,23 | ✅ |
| H5.5 | Pic à 8:30 | × 4,8 | × 3,2 | ✅ |
| H5.6 | Pic à 10:00 | × 1,9 | × 1,4 | ✅ |
| H5.7 | Pic à 13:30 (ancienne clôture de la corbeille) | × 1,36 | **× 0,99**, rien | ❌ |
| H5.8 | Pic à 14:00 jours FOMC | × 7,3 | × 6,4 | ✅ |
| H5.9 | Pic à 16:00 | non | non | ❌ |
| H6 | Pas de U en séance COMEX | profil décroissant | bords/milieu 0,97, pas de U | ✅ |
| H7 | Sauts 5-13 % de la variance | 9,0 % | 7,3 % [5,9 ; 9,1] | ✅ |
| H8 | Plus gros saut à 8:30 | 2,0 %, rang 1 | 1,15 %, rang 1 (100 % des tirages) | ✅ |
| H9 | Sauts 10:00 > Fed | égaux | 10:00 0,20 % contre Fed 0,35 % (p 0,10) | ❌ |
| H10 | Saut de 8:30 = annonces | 91 % | 94 % | ✅ |
| H11 | Volume < volatilité hors séance COMEX | +15,5 pts | **+21,0 pts** (46 % du volume, 67 % de la volatilité) | ✅ |
| H12 | Le volume monte plus que la volatilité à 8:30 et 10:00 | oui | oui | ✅ |
| H13 | Idem à 8:20, 13:30, 9:30 | oui | **non à 8:20 et 13:30** (volume × 1,0 et × 0,9), oui à 9:30 | ❌ / ✅ |
| H14 | Plus de prix par contrat la nuit | × 1,29 | **× 1,47** [1,31 ; 1,65] | ✅ |

Affirmations du papier propres à l'argent :
- **Découverte importante pendant les heures asiatiques** : P2 (19:00 → 2:00 NY) fait 22,6 % du prix pour 20,0 % de la variance ; l'écart n'est pas significatif (p 0,10). Vrai en niveau, pas plus que pour l'or (19 %).
- **Gold et argent ont la même variance de diffusion une fois les sauts retirés** : les profils intraday sont presque identiques (corrélation 0,96 sur les 276 intervalles), mais le niveau de l'argent est 2,2 fois celui de l'or. Vrai pour la forme, faux pour le niveau.
- **Plus de sauts dans l'argent que dans l'or** : non, 7,3 % contre 9,0 %.

## Lecture

- **La microstructure de l'argent ressemble à celle de l'or, en plus bruyante.** Mêmes pics (8:30, Fed, Tokyo, 10:00), en moins marqués, parce que la volatilité de fond de l'argent est plus forte. Les sauts pèsent un peu moins. La nuit, l'argent est encore plus mince que l'or (46 % du volume pour 67 % de la volatilité) et chaque contrat y déplace davantage le prix.
- **L'ancienne corbeille ne marque plus l'argent** : pas de pic de volatilité à 13:30, pas de pic de volume à 8:20 et 13:30. L'or garde ces points focaux, peut-être parce que le règlement COMEX de 13:30 y concentre plus de flux.
- **Comme pour l'or, un quart du prix se fait avant l'Europe**, et l'affirmation du papier ne tient pas.
- **Continuation 22:00-8:00 → reste du jour** : même signe que l'or (b ≈ 1,2), mais rien ne passe Holm, et c'est encore porté par 2023-2026 (b(5:00) 1,04 / 1,12 / 1,28 ; t 2,7 sur 2023-2026). L'or et l'argent sont très corrélés : ce n'est pas une confirmation indépendante.

## Limites

- Données d'un fournisseur nouveau, contrat front non ajusté chez la source : l'ajustement des roulements est le nôtre, et 4 roulements sur 48 restent ambigus (impact limité au gap de l'arrêt de séances déjà écartées).
- Le volume LSE n'a pas été contrôlé contre une autre source pour l'argent (seul le prix de l'or l'a été).
- Mêmes limites que pour l'or : H5.2 mal spécifié, calendrier sans les inscriptions au chômage.

## Conclusion

Sur l'argent, 13 des 23 lignes du tableau se confirment (plus 9:30 pour H13), avec les mêmes échecs (prix avant l'Europe, bruit du début de Globex) et trois écarts : pas de pic à 13:30, pas de pic de volume aux anciennes heures de corbeille, pas de hausse significative à l'ouverture européenne. Aucun résultat tradable. La continuation de nuit vue sur l'or a le même signe sur l'argent, sans être significative, et dépend de 2023-2026.
