# Protocole de validation d'une idée

*Adopté le 2026-11-19. S'applique à toute nouvelle idée ou hypothèse : papier, phénomène trouvé par nous, stratégie transmise. Les étapes sont toujours les mêmes, dans le même ordre. On s'arrête à la première barrière ratée. Statistiques et fiche : [fab/protocole.py](fab/protocole.py). Modèle de pré-enregistrement : [templates/preregistration.md](templates/preregistration.md). Ce qui change ce document se fait par commit, jamais au milieu d'un test.*

## Vue d'ensemble

| Étape | Données | Ce qu'on fait | Barrière pour passer à la suivante |
|---|---|---|---|
| 0. Fiche d'idée | aucune | Triage sans calcul | B0 : idée nouvelle, taille plausible face au coût |
| 1. Exploration | tranche **explorable** | Grille figée, variantes comptées, une règle choisie | B1 : six critères (ci-dessous) |
| 2. Pré-enregistrement | aucune | Modèle rempli, commité | Commit antérieur à tout calcul sur la réserve |
| 3. Confirmation | **réserve**, une seule fois | Calcul unique de la règle figée | C1-C4 → règle **confirmée** |
| 4. Forward | données nouvelles ou paper trading | Dates de lecture ou durée fixées d'avance | F1-F3 → éligible au réel |
| 5. Réel | compte | Taille et coupe-circuit fixés d'avance | K1-K2 → arrêt et retour à l'analyse |

Deux parcours :

- **Stratégie** : étapes 0 à 5, sur le rendement **net** (coût standard).
- **Phénomène** (brique non tradable seule) : étapes 0 à 3, sur le rendement **brut**. Le succès donne une ligne « Confirmés » de [wiki/phenomenes](wiki/phenomenes.md), sinon « À surveiller ».

## Étape 0 : fiche d'idée (aucun calcul)

Elle s'écrit dans la page `wiki/experiments/<idée>.md` (statut `planned`). Elle contient :

1. **Déjà vu ?** Chercher dans [le registre des échecs](wiki/Failed%20Ideas/ledger.md), [les phénomènes](wiki/phenomenes.md) et [les réserves](wiki/reserves.md). Si l'idée est au registre, la condition de réouverture doit être remplie. Si c'est un phénomène déjà connu sous un autre nom, on ne le recompte pas.
2. **Mécanisme**, en une phrase : qui perd cet argent, et pourquoi il ne s'arrête pas. Sans mécanisme, l'idée peut quand même avancer, mais c'est noté.
3. **Taille attendue face au coût.** Si l'effet brut attendu (papier, ou ordre de grandeur connu) est inférieur à 1,5 fois le [coût standard](wiki/concepts/cout-standard.md), seul le parcours **phénomène** est ouvert.
4. **Découpage des données**, avant tout calcul (règle 4 de `CLAUDE.md`) :
   - **Idée tirée d'un papier** : la période du papier est explorable. Nos données postérieures non consommées servent de réserve.
   - **Idée à nous** : déclarer la réserve dans `wiki/reserves.md`, par défaut les 30 % les plus récents, au moins 3 ans.
   - **Couche nouvelle sur un effet déjà exploré** (filtre, condition, gestion de sortie ajoutés à une règle connue) : la tranche est explorée pour l'effet de base, mais la **question nouvelle** ne l'est pas encore. On garde donc les 30 % les plus récents de la tranche (au moins 3 ans) pour cette seule question, tant que ce découpage n'a jamais été calculé, et on le déclare dans `wiki/reserves.md` avec la question réservée. Le pré-enregistrement le dit : sur cette réserve, C1 (net > 0) n'est **pas informatif**, puisqu'on sait déjà que la règle de base y gagne. Le verdict repose sur l'écart avec la règle de base, par exemple jours pris − jours sautés pour un filtre, ou règle avec stop − règle sans stop sur les mêmes jours. Si un indice de la couche (une autocorrélation, une coupe descriptive) a déjà été vu sur la tranche entière, on l'écrit et on préfère une version de la couche qui n'en est pas la traduction directe. *Ajouté le 2026-11-21, après le filtre de retournement du yen, testé sur toutes les années faute de cette règle.*
   - **Plus de réserve disponible** : on cherche d'abord une tranche vierge plus **ancienne** (même actif, autre source, comme l'or au comptant du n° 21), puis on passe à l'étape 4 avec des données nouvelles et des dates de lecture (cas du n° 28).
5. **Puissance**. Avec la taille attendue et la durée de la réserve, calculer la puissance de C1 (test unilatéral à 5 %). Si elle est sous 50 %, la réserve ne peut pas trancher. On le dit, et on prévoit l'étape 4 longue.

**B0** : l'idée n'est pas au registre (ou sa condition de réouverture est remplie), le découpage est écrit et la puissance est connue.

## Étape 1 : exploration (tranche explorable seulement)

- **La grille est écrite dans l'en-tête du script et commitée avant le calcul** : variantes, paramètres, critère de choix de la règle finale (par exemple, le meilleur Sharpe net).
- **Chaque variante calculée compte** dans le [compteur d'essais](wiki/concepts/compteur-essais.md). On note `n_famille`, le nombre de variantes, cases ou fenêtres parmi lesquelles la règle finale a été choisie, en comptant celles regardées avant le script.
- Toujours calculer la **référence triviale**, fixée avant le calcul :
  - pour une règle conditionnelle (filtre, signal) : la même position prise sans condition sur les mêmes heures ;
  - pour une règle de fenêtre sans condition : la même position sur les autres heures de la même journée. Cela vérifie que c'est l'heure qui compte, pas la tendance.
- Coût standard, données ajustées des roulements, rien après le 2026-08-28. Regarder 2020 à part.
- **Sortie** : une seule règle, entièrement spécifiée (entrée, sortie, sens, taille, coût, données), et sa fiche (`fab.protocole.fiche`).

**B1 (`barriere_exploration`)**. Toutes ces conditions sont requises pour avoir le droit de dépenser une réserve :

1. t de Newey-West du net ≥ 2,0 ;
2. DSR avec N = `n_famille` (et la variance des Sharpe de la famille) ≥ 0,95 ;
3. la règle bat la référence triviale : t de l'écart ≥ 1,0 ;
4. net > 0 dans les deux moitiés de la tranche ;
5. net > 0 sans la meilleure année ;
6. net > 0 avec 1 tick de coût en plus.

Pour un **phénomène**, on remplace le net par le brut, et on ignore les critères 6 et, au besoin, 3. Si l'idée vient d'un papier, on vérifie d'abord la **réplication** : sur la période du papier, on doit retrouver ses chiffres (signe, ordre de grandeur, significativité des cases fortes). Une réplication ratée arrête l'idée, sauf s'il y a une explication de données.

Si B1 échoue : ligne au registre des échecs (ou « À surveiller »), statut `abandoned`. Tout ce qui a été regardé passe à « explorée » dans `wiki/reserves.md`.

## Étape 2 : pré-enregistrement

On remplit [templates/preregistration.md](templates/preregistration.md) dans un fichier `PREREGISTRATION_<n>.md`, puis on le commite avant tout calcul sur la réserve. Il fige :

- la règle de l'étape 1, sans aucun changement ;
- la réserve ;
- la référence triviale ;
- les critères C1-C4 ;
- ce qui a déjà été vu ;
- le compteur, « X → Y ».

Si plusieurs règles sont confirmées ensemble, on applique Holm sur elles.

## Étape 3 : confirmation (réserve, une seule fois)

Le code et les paramètres sont ceux du pré-enregistrement. La réserve passe ensuite en « consommée » dans `wiki/reserves.md`.

**Critères (`verdict_confirmation`)**, tous requis :

- **C1** : net moyen > 0, p unilatéral (t de Newey-West, 5 retards) ≤ 0,05, après Holm s'il y a plusieurs règles ;
- **C2** : net > référence triviale ;
- **C3** : net > 0 sans la meilleure année de la réserve ;
- **C4** : net > 0 avec 1 tick de coût en plus.

**Verdict** :

- C1-C4 remplis : règle **confirmée**, statut `confirmed`, ligne dans `wiki/phenomenes.md`.
- Échec : on rejette, ligne au registre des échecs. On ne refait pas d'étape 1 sur la réserve consommée. Si la puissance annoncée était < 50 %, on écrit « non concluant » et on passe à l'étape 4 au lieu de rejeter, mais seulement si le pré-enregistrement l'avait prévu.

## Étape 4 : forward (données nouvelles ou paper trading)

Obligatoire avant tout argent réel. Une confirmation sur l'historique ne remplace pas ce test. Le pré-enregistrement fixe à l'avance l'une de ces deux formes :

- **Holdout à dates de lecture** (modèle du n° 26) : lectures intermédiaires avec un seuil z ≥ 3,0 (Haybittle-Peto), puis une lecture finale à p ≤ 0,05. Rien n'est calculé entre deux lectures.
- **Paper trading** : au moins 6 mois **et** 60 trades, avec l'exécution réelle (bot, comptes démo).

**Critères** :

- **F1** : le coût réel mesuré (spread, glissement, commission) est ≤ 1,5 fois le coût supposé ;
- **F2** : le net forward n'est pas inférieur de plus de 2 erreurs types au net attendu (z ≥ −2 contre l'espérance de l'étape 3) ;
- **F3** : aucune erreur d'exécution non expliquée.

Si les trois sont remplis, la règle devient **éligible au réel**. La décision de passer en réel revient à l'utilisateur.

## Étape 5 : réel

Avant le premier ordre, on fixe et on écrit :

- la taille (risque par trade) ;
- les deux coupe-circuits :
  - **K1** : un drawdown supérieur à 1,5 fois le pire creux du backtest, à taille égale ;
  - **K2** : sur les 100 derniers trades (ou les 6 derniers mois), un net inférieur de plus de 2 erreurs types au net attendu.

Si K1 ou K2 se déclenche, on arrête, on retourne à l'analyse et on le note au journal. On ne relance pas sans nouveau pré-enregistrement.

## Fiche standard (dans chaque rapport)

`fab.protocole.fiche` donne toujours les mêmes lignes :

- n, dates ;
- brut, net (moyen et médian), écart type, Sharpe annuel ;
- t de Newey-West, p unilatéral, % de gagnants, pire creux ;
- années positives ;
- net de chaque moitié, net sans la meilleure année, net avec 1 tick de plus ;
- n_famille et DSR de la famille ;
- référence triviale et écart avec elle (t).

Chaque rapport finit par le **compteur global** (« Compteur global : N »), la barrière ou le critère appliqué, et le verdict.

## Ce qui n'est pas permis

- Calculer sur une réserve avant le commit du pré-enregistrement, y compris pour un « contrôle de qualité » qui calcule des moyennes de rendement.
- Changer la règle entre l'étape 1 et l'étape 3, ou ajouter un filtre après avoir vu la réserve.
- Choisir la référence triviale après le calcul.
- Ne pas compter une variante calculée.
- Passer en réel sans étape 4.

## Exemple : le yen en session US

- **Étapes 0-1** : n° 27. C'est une idée de papier, la réplication 2010-2015 tient.
- **Étape 3, parcours phénomène** : 2016-2026 est postérieur au papier. Le yen y baisse de −1,72 bp, t −4,3, et devient un phénomène confirmé.
- **Parcours stratégie** : la règle a été choisie parmi les 28 cases (7 devises × 4 sessions) du n° 27, donc n_famille = 28. Sa fiche (2016-2026, net +0,90 bp, t NW 2,20) passe cinq critères de B1 sur six, mais son DSR à N = 28 vaut 0,48 : elle n'aurait pas pu dépenser une réserve. De toute façon, il n'en reste plus. Elle passe donc directement à l'étape 4 avec le n° 28, en holdout à dates de lecture.
- **Variantes SL/TP** : c'est une exploration de 12 essais. B1 échoue pour toutes, parce qu'aucune ne bat la règle sans stop.
