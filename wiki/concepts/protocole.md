---
type: concept
updated: 2026-11-19
---

# Protocole de validation

**Définition** : la suite d'étapes, toujours la même, qu'une idée doit franchir pour devenir une stratégie (ou un phénomène confirmé). La source qui fait foi est [[PROTOCOLE]].

**Dans ce dépôt** : étapes 0 (fiche d'idée) → 1 (exploration, barrière B1) → 2 (pré-enregistrement, [modèle](../../templates/preregistration.md)) → 3 (confirmation sur la réserve, C1-C4) → 4 (forward : holdout à dates de lecture ou paper trading, F1-F3) → 5 (réel, coupe-circuits K1-K2). Les statistiques communes sont dans [fab/protocole.py](../../fab/protocole.py), testées par `tests/test_protocole.py`.

**Piège** : `n_famille` compte toutes les variantes parmi lesquelles la règle a été choisie, y compris celles regardées avant le script. Le short du yen passe le DSR à N = 1 (0,98), mais pas à N = 28 (0,48), le nombre de cases du n° 27 dont il est sorti.

**Voir aussi** : [[wiki/concepts/pre-enregistrement]], [[wiki/concepts/is-oos]], [[wiki/reserves]], [[wiki/concepts/dsr]]
