---
type: experiment
updated: 2026-11-22
status: planned
verdict: —
prereg: []
trials: 0
---

# Devise d'un pays exportateur en hausse pendant ses heures domestiques, devise d'un pays importateur en baisse

**Une phrase** : si les flux commerciaux se convertissent pendant les heures de bureau du pays, la devise d'un pays exportateur devrait monter pendant sa session domestique (les exportateurs vendent leurs recettes en devises), et celle d'un pays importateur baisser (les importateurs achètent des devises pour payer). Le sens de l'effet dépendrait donc du solde commercial du pays, alors que Zhang (2018) et Breedon-Ranaldo prédisent le même sens pour toutes les devises.

## Étape 0 : fiche d'idée (2026-11-22, aucun calcul)

### 1. Déjà vu ?

- **Registre des échecs** :
  - « Zhang (2018) : la devise baisse pendant ses heures domestiques (H1) et monte pendant la session US (H2) » (2026-11-19, ❌ hors échantillon). C'est une **idée voisine mais distincte** : Zhang prédit le même signe pour toutes les devises, cette idée prédit un signe qui dépend du solde commercial. Elle n'est pas au registre, donc aucune condition de réouverture n'est requise.
  - « Saisonnalité des fixings comme stratégie autonome » (2026-10-12) : autre mécanisme (flux autour d'une heure précise), sans rapport avec le pays.
- **Phénomènes** : aucun phénomène lié au solde commercial. Ceux qui touchent les mêmes séries (« le yen baisse en session US », et « À surveiller » : GBP et CAD hors session US, CHF Londres-New York) portent sur d'autres sessions que la session domestique.
- **Indice déjà vu sur les 7 majeures** (EUR, GBP, JPY, CHF, AUD, CAD, NZD). La moyenne de la session domestique (08:00-16:00 heure locale) est déjà calculée pour 2010-2015 et 2016-2026 ([[reports/zhang_fx_report]]). C'est exactement la quantité que cette idée mesurerait. Lecture à l'œil, sans calcul formel (2026-11-22), sur 2010-2015 : rien ne va dans le sens de l'idée.
  - Pays excédentaires : EUR −2,17 bp, mais CHF +1,51.
  - Japon, déficitaire de 2011 à 2015 : JPY +0,88.
  - Exportateurs de matières premières : AUD −1,89, CAD −1,62, NZD −2,56.
  - Sur 2016-2026, toutes les sessions domestiques sont proches de 0 (de −0,78 à +0,76 bp, aucun |t| > 1,2).

  **Conséquence** : les 7 majeures ne peuvent servir ni d'exploration ni de réserve. Leur résultat est connu à l'œil, et il est défavorable. Elles seront rapportées à part, comme « déjà vues ».
- **Idée voisine non testée** : l'effet Gotobi (importateurs japonais acheteurs de dollars au fixing de Tokyo les jours 5, 10, 15, 20, 25 et 30 du mois ; [[papiers_ssrn_overnight_3_2026-10-29]]). C'est le même mécanisme de flux commerciaux, mais calendaire et propre au yen. Il n'est pas couvert par cette fiche.

### 2. Mécanisme supposé

- **Qui paie l'effet** : les entreprises qui convertissent leurs flux commerciaux au comptant, pendant leurs heures de bureau et sans regarder le prix. Elles payent une petite concession de prix aux intermédiaires qui portent le stock jusqu'aux heures étrangères.
- **Pourquoi ça ne s'arrête pas** : la conversion est une contrainte de trésorerie, pas un pari. Et le coût de cette concession est minuscule face à la marge commerciale de ces entreprises.
- **Poids du commerce dans les flux (corrigé le 2026-11-22)** :
  - En volume **brut**, le commerce mondial (environ 100 Md$ par jour) ne pèse que 1 à 2 % du volume de change (7 500 Md$ par jour en avril 2022, enquête triennale de la BRI, de mémoire, non revérifié).
  - Mais l'essentiel de ce volume ne pousse pas le prix : environ la moitié sont des swaps de change (achat et revente simultanés, pour le financement), et environ 45 % sont des échanges entre banques qui se repassent le stock reçu des clients.
  - Ce qui fait bouger un cours, c'est le flux **net** d'ordres directionnels (Evans et Lyons, 2002). Rapporté à ce flux net, le commerce pèse nettement plus que 1 à 2 %, et ses flux sont réguliers et insensibles au prix.
  - La taille du commerce n'est donc **pas** une objection décisive.
- **Objections qui restent, notées d'avance** :
  - Une grande partie des exportateurs couvrent leurs flux à terme (forwards), à des dates et des heures qui ne suivent pas forcément leurs encaissements ni leurs heures de bureau. C'est le doute principal.
  - Breedon et Ranaldo (2013) trouvent le sens inverse pour toutes les devises, et l'attribuent aux flux des investisseurs, pas au commerce.
  - Les flux de portefeuille (achats de titres étrangers et leur couverture), le carry trade et les banques centrales peuvent dominer le flux net et noyer l'effet du commerce.
  - L'effet attendu reste donc faible (point 3).

### 3. Taille attendue face au coût

- **Ordre de grandeur connu** : les moyennes des sessions domestiques valaient ±2 bp sur 2010-2015 et environ 0 bp depuis 2016, toutes devises confondues. Un écart exportateurs − importateurs de **0,5 à 2 bp par jour** est le haut de ce qu'on peut espérer.
- **Coût** : au comptant, le demi-spread d'entrée plus celui de sortie vaut environ 0,8 à 1,2 bp sur une session de journée pour les majeures (n° 27). Il est nettement plus large sur les devises émergentes (plusieurs bp sur MXN, ZAR, TRY).
- **Conclusion** : l'effet brut attendu est sous 1,5 fois le [[wiki/concepts/cout-standard|coût standard]]. **Seul le parcours phénomène est ouvert.** Le but est de savoir si le solde commercial explique le sens des sessions domestiques, pas de trader.

### 4. Découpage des données (idée à nous)

- **Univers** : les devises flottantes contre le dollar qui ont une session domestique distincte, hors les 7 majeures, déjà vues.
  - Candidates : NOK, SEK, PLN, CZK, HUF, MXN, ZAR, SGD, TRY, ILS, plus d'autres selon la disponibilité.
  - Exclues : les devises ancrées ou très administrées (HKD, DKK, CNH, SAR…).
  - La liste finale sera figée avant tout calcul, après un **contrôle de qualité seulement** : couverture, trous et spreads au comptant Dukascopy, sans aucune moyenne de rendement.
- **État** : vierges. USDNOK et USDSEK 2010-2016 sont déjà téléchargés, mais seulement contrôlés ([[wiki/reserves]]) ; les autres ne sont pas téléchargés.
- **Exploration** : du 2010-01-01 au 2021-08-31 (environ 70 %).
- **Réserve** : du 2021-09-01 au 2026-08-28 (5 ans), déclarée dans [[wiki/reserves]] le 2026-11-22. Elle ne sera ouverte qu'une fois, par un pré-enregistrement commité. Rien après le 2026-08-28 n'est utilisé.
- **Variable explicative, connue d'avance** : le solde commercial (biens et services) en % du PIB **de l'année précédente**, publié par le FMI ou la Banque mondiale.
  - Limite : les données sont révisées, donc la vintage en temps réel n'est pas disponible. On le note.
  - Variante : le signe seul, excédent ou déficit.
- **Session domestique** : 08:00-16:00 heure locale, comme chez Zhang (2018), changements d'heure compris.
- **Tests prévus**, à figer dans la grille de l'étape 1 :
  1. **Panel** : rendement de la session domestique de la devise c, jour t, régressé sur le solde de l'année précédente. Erreurs de Driscoll-Kraay (corrélation entre devises le même jour). Hypothèse : coefficient > 0.
  2. **Portefeuille** : chaque jour, long les devises excédentaires et short les devises déficitaires pendant leurs sessions domestiques respectives, à poids égaux. On compare la moyenne à 0 et au portefeuille de sens tiré au hasard.
  3. **Contrôle propre** : une comparaison **dans le même fuseau européen**, entre devises excédentaires (NOK, SEK, CZK…) et déficitaires (PLN, HUF, TRY selon les années). Les heures sont identiques, ce qui neutralise l'effet d'heure du dollar.
- **Référence triviale** : la moyenne de la session domestique de toutes les devises, sans distinction (l'hypothèse de Zhang).

### 5. Puissance (calcul a priori, aucune donnée)

Hypothèses :
- environ 1 250 jours dans la réserve ;
- un écart type quotidien du portefeuille long-short de 20 à 30 bp (sessions de 8 h, devises corrélées entre elles) ;
- un test unilatéral à 5 %.

| Écart attendu | Écart type 20 bp | Écart type 30 bp |
|---|---|---|
| 0,5 bp/jour | 22 % | 15 % |
| 1 bp/jour | 55 % | 32 % |
| 2 bp/jour | 97 % | 76 % |

À l'effet le plus plausible (≤ 1 bp), **la réserve ne peut pas trancher** : la puissance est d'au plus 55 %. Il faudra une étape 4 longue, ou élargir l'univers de devises. L'écart type réel du portefeuille sera mesuré pendant l'exploration, puis la puissance recalculée avant le pré-enregistrement.

**B0** : ✅. L'idée n'est pas au registre, le découpage est écrit et la réserve est déclarée, la puissance est connue (faible) et le parcours est limité au phénomène.

## Prochaine étape

Étape 1 : choisir les devises par contrôle de qualité. Ensuite, figer et commiter la grille (univers, source du solde commercial, les 3 tests, nombre d'essais), puis explorer 2010-01 → 2021-08 seulement.

## Liens

[[reports/zhang_fx_report]] · [[PREREGISTRATION_27]] · [[wiki/reserves]] · [[wiki/Failed Ideas/ledger]] · Breedon et Ranaldo (2013), *Intraday patterns in FX returns and order flow*, JMCB 45(5) · Zhang (2018), SSRN 3138756 · Evans et Lyons (2002), *Order flow and exchange rate dynamics*, JPE 110(1)
