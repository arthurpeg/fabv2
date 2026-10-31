---
type: schema
updated: 2026-10-31
---

# SCHEMA : règles du wiki

Le wiki est la mémoire de travail de l'agent sur ce dépôt. L'agent l'écrit et le maintient ; l'humain le lit dans Obsidian. Ce fichier fixe la structure, les modèles de page, les procédures et le contrôle périodique.

## 0. Principes
- **Le wiki pointe, il ne recopie pas.** Les sources brutes (`PREREGISTRATION_*.md`, `RESULTS.md`, `reports/`, `results/`, le code, les données) font foi. Une page de wiki résume en quelques chiffres clés et renvoie à la source ; en cas d'écart, c'est la source qui a raison et la page qu'on corrige.
- Les sources brutes ne sont jamais modifiées pour le wiki.
- Langue : français, comme le reste du dépôt. Les clés de frontmatter restent en anglais.
- Liens : `[[chemin/depuis/la/racine]]` pour les pages `.md` (wiki et sources), lien Markdown relatif pour le code et les données (`[run_x.py](../../run_x.py)`, Obsidian n'indexe pas les `.py`).
- Noms de fichiers : kebab-case sans accents (`prime-de-nuit.md`), sauf `Failed Ideas/`.
- `wiki/hot.md` est généré par [update_hot.py](update_hot.py) : ne jamais l'éditer à la main, sauf le bloc « Prochaines actions » entre ses marqueurs.

## 1. Arborescence
| Chemin | Contenu |
|---|---|
| `index.md` | Catalogue, une ligne par page. Lu en premier à chaque session. |
| `SCHEMA.md` | Ce fichier. |
| `log.md` | Journal append-only. |
| `hot.md` | État courant, généré. |
| `lessons.md` | Leçons transversales. |
| `experiments/` | Une page par expérience ou lignée d'expériences (unité de travail). |
| `concepts/` | Vocabulaire : un terme, une définition, son usage ici. |
| `research/` | Papiers et revues ingérés. |
| `reference/` | Pages d'aiguillage : liens vers la source qui fait foi, rien d'autre. |
| `Failed Ideas/ledger.md` | Registre des idées abandonnées, avec la raison. |

## 2. Modèles de page

### Ligne d'index
```
- [[wiki/<dossier>/<page>|Titre]] — résumé en une ligne · `status` · AAAA-MM-JJ
```

### Expérience (`experiments/`)
```
---
type: experiment
updated: AAAA-MM-JJ
status: planned | running | done | paper-trading | active | abandoned
verdict: ✅ / ❌ / candidat / … (une expression)
prereg: [n°, …]          # numéros de PREREGISTRATION concernés
trials: <compteur global après le test>
---
# <Titre>
**Une phrase** : ce que la règle fait et le résultat principal.
## Origine            — d'où vient l'idée (papier, expérience précédente)
## Tests              — tableau : test, résultat, critère, lien vers le rapport
## Ce qu'on sait / Lecture
## Ouvert             — questions non tranchées
## Sources brutes     — prereg, rapport, script, dossier results/
```

### Concept (`concepts/`)
```
---
type: concept
updated: AAAA-MM-JJ
---
# <Terme>
**Définition** : …
**Dans ce dépôt** : convention locale, seuils, où c'est calculé.
**Piège / À ne pas confondre avec** : …
**Voir aussi** : [[…]]
```

### Recherche (`research/`)
```
---
type: research
updated: AAAA-MM-JJ
source: <papier, SSRN id, ou fichier brut>
status: to-read | ingested | tested
verdict: <si testé : lien vers l'expérience>
---
# <Titre>
**Ce que c'est** · **Affirmations clés** (avec chiffres du papier) · **Ce qu'on a trouvé / contradictions** · **Liens**
```

### Référence (`reference/`)
```
---
type: reference
updated: AAAA-MM-JJ
---
# Où trouver <X>
Tableau « question → source qui fait foi ». Aucun chiffre recopié.
```

### Ligne du registre des échecs
```
| AAAA-MM-JJ | Idée | [[prereg]], [[rapport]] | ❌ | Pourquoi, avec 1 ou 2 chiffres | Condition de réouverture, ou — |
```

## 3. Procédures

**Début de session**
1. Lire `index.md`, puis `Failed Ideas/ledger.md`, puis `hot.md`.
2. Avant une nouvelle idée : chercher dans le registre une ligne similaire ; si elle existe, vérifier la condition de réouverture avant d'aller plus loin.

**Nouveau pré-enregistrement**
1. Écrire `PREREGISTRATION_<n>.md` (source brute) et le commiter avant tout calcul.
2. Créer ou mettre à jour la page `experiments/` (status `planned`), avec le compteur « X → Y ».
3. Ligne dans `index.md` si nouvelle page ; entrée `prereg` dans `log.md`.

**Après une expérience**
1. Mettre à jour la page d'expérience depuis le modèle : verdict, chiffres clés, liens vers rapport et `results/`.
2. Si nouvelle page : ligne dans `index.md`.
3. Entrée `experiment` dans `log.md`.
4. Si abandon : ligne dans `Failed Ideas/ledger.md` + entrée `abandon` dans le log + `status: abandoned` sur la page.
5. Si un nouveau terme apparaît : page `concepts/`. Si une leçon générale apparaît ou est contredite : `lessons.md`.
6. Mettre à jour le compteur d'essais si le rapport ne le fait pas.

**Ingestion d'un papier ou d'une revue**
1. Vérifier et enrichir `papers/seen_papers.json`.
2. Page `research/` (ou ligne dans une page de lot existante), avec les affirmations chiffrées du papier.
3. Relier aux concepts et expériences touchés ; signaler toute contradiction avec nos résultats.
4. Entrée `ingest` dans le log.

**Réponse à une question qui mérite d'être gardée**
Si la réponse synthétise plusieurs sources (comparaison, bilan), la classer comme page (`research/` ou `experiments/`), l'ajouter à l'index, entrée `query` dans le log.

**Fin de session**
Page concernée à jour, entrée datée dans `log.md`, ligne au registre en cas d'abandon. `hot.md` est régénéré par le hook Stop.

## 4. Lint (contrôle périodique)
À lancer sur demande, ou quand `log.md` a reçu ~10 entrées depuis le dernier `lint`.
1. **Orphelines** : pages de `wiki/` qu'aucune autre page ni l'index ne liste.
2. **Index** : chaque page existe dans l'index, et chaque ligne d'index pointe vers une page existante.
3. **Liens cassés** : `[[…]]` sans fichier cible.
4. **Obsolètes** : pages dont `updated` est antérieur à un rapport plus récent sur le même sujet ; status `running` depuis plus de deux semaines.
5. **Contradictions** : chiffres d'une page qui diffèrent du rapport source ; deux pages qui se contredisent ; une leçon contredite par une expérience récente.
6. **Concepts manquants** : termes employés dans plusieurs pages sans page `concepts/`.
7. **Registre** : chaque page `status: abandoned` a sa ligne au registre.
8. **Compteur** : `hot.md` et la dernière page d'expérience donnent le même compteur.
Consigner le résultat : `## [date] lint | <n> problèmes trouvés | <n> corrigés`.
