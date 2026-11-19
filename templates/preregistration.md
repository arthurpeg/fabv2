# Pré-enregistrement n° <n> : <titre court>

*<AAAA-MM-JJ>, écrit et commité avant tout calcul sur la réserve. Protocole : [PROTOCOLE.md](PROTOCOLE.md), étape <2 → 3 | 2 → 4>. Parcours : <stratégie | phénomène>.*

## Origine et fiche d'idée (étape 0)

- Source : <papier (référence, période d'estimation) | exploration n° … | stratégie transmise>.
- Registre des échecs : <aucune ligne proche | ligne du … , condition de réouverture : … remplie parce que …>.
- Registre des phénomènes : <nouveau | même effet que … (ne pas recompter)>.
- Mécanisme : <qui perd cet argent, et pourquoi il ne s'arrête pas | inconnu>.
- Taille attendue face au coût : <effet brut attendu> contre <coût standard> (rapport <x>).

## Déjà vu

- Tranches explorées pour cette idée : <actif, dates> (voir `wiki/reserves.md`).
- Résultats de l'exploration (étape 1) : <fiche : n, brut, net, Sharpe, t NW, DSR famille>, n_famille = <k>, rapport <lien>.
- Barrière B1 : <les six critères, avec leurs valeurs>.

## Règle (figée)

- Actif, données, source, ajustement des roulements : …
- Entrée : …
- Sortie : …
- Sens, taille : …
- Coût : <coût standard 1 tick + 5 $ | autre, justifié>.
- Code figé : `<script>.py` (commit `<hash>`). Seuls les fichiers d'entrée et les dates changent.

## Référence triviale (fixée avant calcul)

<même position sans condition, mêmes heures | même position sur les autres heures du jour | …>

## Données de confirmation

- Réserve : <actif, dates> (statut « réservée » dans `wiki/reserves.md`, depuis le <date>).
- Ou forward (étape 4) : <holdout à dates de lecture L1 / L2 / L3 avec seuils | paper trading ≥ 6 mois et 60 trades>.
- Puissance de C1, à l'effet de l'exploration et à la moitié de cet effet : <x % / y %>.

## Critères (PROTOCOLE.md, étape 3 ; tous requis)

- **C1** : net moyen > 0, p unilatéral NW (5 retards) ≤ 0,05 (Holm sur <k> règles si plusieurs).
- **C2** : net > référence triviale.
- **C3** : net > 0 sans la meilleure année.
- **C4** : net > 0 avec 1 tick de coût en plus.

<Pour le parcours phénomène : brut au lieu de net, C4 sans objet.>
<Si la puissance est < 50 % : en cas d'échec, « non concluant », puis étape 4 (prévue ici) | rejet.>

## Hypothèses et compteur

<k> essais ; compteur <X> → <Y>.

## Interdit après calcul

On ne change ni la règle, ni le coût, ni la réserve, ni les critères, ni la référence triviale. On n'ajoute aucun filtre. La réserve passe en « consommée » quel que soit le résultat.
