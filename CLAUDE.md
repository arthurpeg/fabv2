# fabv2

Recherche quantitative : backtests intraday et de nuit sur futures (indices, FX, or) avec vectorbt, sous protocole de pré-enregistrement (`PREREGISTRATION_<n>.md` commité avant tout calcul). Python ≥ 3.12, `uv` ; lancer avec `uv run python <script>.py`, tests avec `uv run pytest`. Docs et rapports en français.

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

Obsidian : le coffre est la racine du dépôt. Obsidian réécrit `.obsidian/graph.json` pendant qu'il tourne : ne modifier ce fichier que quand Obsidian est fermé.
