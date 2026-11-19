# fabv2

Recherche quantitative : backtests intraday et de nuit sur futures (indices, FX, or) avec vectorbt, sous protocole de pré-enregistrement (`PREREGISTRATION_<n>.md` commité avant tout calcul). Python ≥ 3.12, `uv` ; lancer avec `uv run python <script>.py`, tests avec `uv run pytest`. Docs et rapports en français.

## Branches (à décider au début de chaque nouvelle discussion)

Le dépôt est réparti en branches emboîtées : chaque branche fille contient tout ce que contient sa mère, plus son propre domaine.

| Branche | Contenu propre | Mère |
|---|---|---|
| `main` | Recherche : papiers (`papiers_*.md`, `resumes_*`, `PAPER_SPECS.md`), phénomènes (`wiki/phenomenes.md` et leurs études : `run_zhang`, `run_gc_*`, `run_sessions`, `run_jpy_us_backtest/distribution`, `run_replications`, `run_recolte1*`, `run_inference_overnight`…), wiki, protocole, tous les `PREREGISTRATION*.md`, `RESULTS.md`, code commun (`fab/`, `recolte1/`, `config/`, `fetch_*`, `tools/`) | — |
| `strategies-vbt` | Backtests de stratégies : `run_prereg*`, `run_nq_*`, `run_fx_*`, filtres, SL/TP, packages `gap/ asym/ fxreopen/ lab/…`, leurs `reports/` et `results/` | `main` |
| `propfirm-ftmo` | Simulations prop firm (`run_propfirm_*`, `run_ftmo_*`, `propfirm/`) et bot `live/` | `strategies-vbt` (les simulations importent les backtests) |
| `ml` | Machine learning pour améliorer les anomalies significatives que les filtres classiques n'ont pas améliorées (`ml/`, fiche [[wiki/experiments/ml-anomalies]]) | `strategies-vbt` |
| `vps-journal` | Journaux publiés par le VPS. **Ne jamais y toucher** (lecture seule : `git fetch origin vps-journal`). | — |

**Règle de routage, à appliquer au premier message de chaque nouvelle discussion**, avant tout fichier écrit :
1. Lire la demande et choisir la branche : papier, lecture, phénomène, statistique descriptive, wiki ou protocole seul → `main` ; backtest ou filtre d'une règle de trading → `strategies-vbt` ; prop firm, FTMO, bot, VPS → `propfirm-ftmo` ; modèle appris (ML) → `ml`. En cas de doute, la branche la plus haute qui contient tout ce dont le travail a besoin (un script ne doit importer que des fichiers de sa branche).
2. Annoncer en une ligne la branche choisie et pourquoi, puis `git switch <branche>` si ce n'est pas la branche courante (arbre propre requis ; le hook Stop commite sur la branche courante).
3. Pré-enregistrements, `RESULTS.md` et wiki sont communs : on peut les écrire depuis n'importe quelle branche.
4. **Avant de terminer** tout travail qui a commité quelque chose (sur `main` aussi, pour que les branches filles et le coffre Obsidian le reçoivent) : `uv run python tools/sync_branches.py`. Il remonte sur `main` les fichiers communs modifiés (wiki, pré-enregistrements, `RESULTS.md`…), puis merge en cascade `main → strategies-vbt → propfirm-ftmo / ml` et pousse. Jamais de force push : le VPS suit `propfirm-ftmo` en avance rapide et lance `tests/test_live.py` à chaque mise à jour, donc ne jamais réécrire son historique ni casser ce test.
5. Un lien de wiki vers un rapport d'une autre branche ne s'ouvre pas sur `main` : le lire avec `git show strategies-vbt:reports/<nom>.md`.

## Wiki

`wiki/` est la mémoire persistante de l'agent sur ce dépôt. Règles permanentes :

1. **Avant tout travail substantiel** : lire `wiki/index.md` ET `wiki/Failed Ideas/ledger.md`. Ne relancer aucune idée du registre sans que sa condition de réouverture soit remplie.
2. **Avant de terminer** : mettre à jour la page de wiki concernée, ajouter une ligne datée à `wiki/log.md` (`## [AAAA-MM-JJ] <type> | <quoi> | <résultat>`), et ajouter une ligne au registre des échecs pour toute idée abandonnée.
3. **Phénomènes confirmés** : chaque fois qu'une règle ou hypothèse (d'un papier ou à nous) se vérifie sur nos données, même non tradable seule, l'ajouter à `wiki/phenomenes.md` (critère d'entrée et colonnes en tête du fichier ; « À surveiller » si significatif en brut seulement). But : amasser des phénomènes à combiner en stratégies. Avant de combiner, vérifier qu'ils ne sont pas le même effet compté deux fois, et pré-enregistrer la combinaison.

4. **Réserve hors échantillon** : avant tout calcul de rendement sur un actif ou une période, lire `wiki/reserves.md`. Avant le premier calcul sur une tranche **vierge**, y déclarer une réserve (par défaut les 30 % les plus récents, au moins 3 ans), n'explorer que le reste, et n'ouvrir la réserve qu'une fois, par un pré-enregistrement commité. Sur une réserve, aucun contrôle de qualité ne calcule de moyenne de rendement. Mettre à jour l'état de la tranche (vierge → explorée / réservée → consommée) dès qu'il change. Détail : `wiki/concepts/is-oos.md`.

5. **Protocole de validation** : toute nouvelle idée ou hypothèse suit `PROTOCOLE.md`, avec toujours les mêmes étapes : 0 fiche d'idée, 1 exploration (grille commitée avant calcul, variantes comptées, référence triviale), 2 pré-enregistrement (modèle `templates/preregistration.md`), 3 confirmation sur la réserve, 4 forward, 5 réel. On s'arrête à la première barrière ratée. Les statistiques et la fiche viennent de `fab/protocole.py` (`fiche`, `barriere_exploration`, `verdict_confirmation`), pas de copies locales.

Règle d'immuabilité : le wiki **pointe** vers les sources brutes (pré-enregistrements, `RESULTS.md`, `reports/`, `results/`, code, données) et n'en recopie jamais le contenu comme source de vérité. En cas d'écart, la source a raison.

Structure, modèles de page, procédures et lint : `wiki/SCHEMA.md`. `wiki/hot.md` est régénéré par `wiki/update_hot.py` (hook Stop) : ne pas l'éditer à la main, sauf son bloc « Prochaines actions ».

Automatisation (`.claude/settings.json`, scripts dans `.claude/hooks/`) : au démarrage, `git pull --ff-only` puis affichage de `hot.md` ; à chaque fin de tour, régénération de `hot.md`, puis `git add -A`, commit horodaté et push si l'arbre a changé. Tout est best-effort et ne bloque jamais la session. Les PDF, `cache/` et `.env` sont dans `.gitignore` : vérifier qu'un nouveau dossier de données lourdes ou sensibles y est avant de le créer.

Obsidian : le coffre que l'utilisateur ouvre est `C:\Users\arthu\fabv2-obsidian`, un worktree détaché en lecture seule sur `origin/propfirm-ftmo` (la branche qui contient tout), ramené à jour par le hook Stop ; `papers/` et `papiers overnight ssrn/` y sont des jonctions vers ceux de `fabv2`. L'utilisateur n'y écrit jamais ; ne rien y écrire non plus (tout serait écrasé). Si le dossier disparaît : `git worktree add --detach ..\fabv2-obsidian origin/propfirm-ftmo`. Obsidian réécrit `.obsidian/graph.json` pendant qu'il tourne : ne modifier ce fichier que quand Obsidian est fermé.
