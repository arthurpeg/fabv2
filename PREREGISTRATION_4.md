# Pré-enregistrement n° 4 : timing d'exécution FX

*2026-10-12, avant exécution. Données et découpage IS (2016-2022) / OOS (2023-2026-08) comme avant.*

## Cadre

Un opérateur **doit** exécuter chaque jour ouvré un ordre FX (acheter ou vendre la devise contre USD), par exemple pour une couverture ou un paiement. Il paie le spread **quel que soit l'horaire**, donc les coûts de transaction disparaissent de la comparaison. On mesure l'**économie d'exécution** de la règle par rapport à un benchmark naïf, en points de base du prix :

- acheteur de la devise : économie = (prix benchmark − prix règle) / prix ;
- vendeur de la devise : économie = (prix règle − prix benchmark) / prix.

**Métrique principale = moyenne des économies acheteur et vendeur.** Elle neutralise la tendance de fond : un drift haussier aiderait l'acheteur exactement autant qu'il pénaliserait le vendeur. Il ne reste que la valeur du choix de l'heure.

**Honnêteté** : ces effets ont déjà été mesurés en brut (pré-enregistrement n° 3), OOS compris. Ce test ne découvre rien ; il mesure **si un effet connu mais trop petit pour être tradé vaut quelque chose quand on doit trader de toute façon**. L'OOS n'est donc plus vierge, et il faut lire les résultats comme des estimations de magnitude, pas comme des preuves.

## Règles (12 tests ; le compteur passe à 150)

| ID | Effet source | Fenêtre d'exécution, benchmark | Acheteur de la devise | Vendeur de la devise |
|---|---|---|---|---|
| X1 | Breedon & Ranaldo + Krohn (Europe) : la devise baisse de 2:00 à 8:00 ET, puis monte de 8:00 à 16:00 ET | 02:00-16:00 ET, **TWAP** des minutes | exécute à **08:00 ET** | exécute à **16:00 ET** |
| X2 | Krohn (Tokyo) : USD au plus haut au fix de 9:55 JST | 08:00-15:00 JST, TWAP des minutes | exécute à **09:55 JST** | exécute à **15:00 JST** |
| X3 | Baltussen (futures FX, session 8:20-15:00 ET) | Ordre à exécuter entre 14:30 et 15:00 ET. Benchmark : exécuter à **14:30** | si r_ROD (15:00 J-1 → 14:30) > 0 : exécute à 14:30, sinon attend 15:00 | si r_ROD ≤ 0 : exécute à 14:30, sinon attend 15:00 |

Actifs : 6E, 6J, 6B, 6A (prix du future = USD par unité de devise). Prix d'exécution = open de la barre 1 minute à l'heure indiquée (première barre dans les 5 minutes, sinon jour exclu). TWAP = moyenne des clôtures 1 minute de la fenêtre.

## Critère

Une règle est **utile** pour une devise si l'économie moyenne (acheteur et vendeur) est **> 0 en IS et en OOS**, et si sa t-stat sur toute la période dépasse 2. La t-stat est calculée par bootstrap par blocs de 10 jours. Sont rapportés : l'économie en points de base, en ticks, en dollars par million de notionnel, et l'économie de chaque côté séparément.
