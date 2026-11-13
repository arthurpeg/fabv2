# Bot de démo FTMO (books A et B) sur VPS

Ce bot fait tourner le plan FTMO retenu le 2026-11-04 ([[wiki/experiments/propfirm-ftmo-option]], section « Plan retenu ») sur deux essais gratuits FTMO en MT5 :

- **book A = mom** ;
- **book B = 3n + M2**.

Il y a un processus Python par book, et chaque processus a son propre terminal MT5.

- Code : [bot.py](bot.py) (boucle et événements), [signals.py](signals.py) (signaux), [compte.py](compte.py) (compte FTMO virtuel), [broker.py](broker.py) (MT5).
- Contrôles : `uv run pytest tests/test_live.py tests/test_live_bot.py`. Sur les barres NQ, les signaux 3n et M2 et les stops sont identiques au backtest. Le compte virtuel reproduit `run_ftmo_deux_comptes.Compte`. Un rejeu complet d'août 2026 avec un faux terminal donne les mêmes trades que le backtest.

## Principe

- Le bot calcule les signaux sur les barres **US100.cash** du terminal, aux heures du backtest (heure de New York) :
  - mom : 20:00, sortie 9:30 ;
  - 3n : 20:05, sortie 03:00 ; pas de 3n une nuit où mom est short (règle anti-hedging de FTMO, le book B calcule lui-même le signe de mom) ;
  - M2 : 9:35, sortie 16:00.
- Le stop et l'objectif sont posés chez le broker juste après l'entrée.
- Le bot ferme lui-même la position à l'heure de sortie.
- **Compte FTMO virtuel.** Chez FTMO, un essai gratuit reste toujours une « éval ». Le bot tient donc lui-même un compte FTMO virtuel, qui décide pour chaque trade :
  - du risque : 2,5 % en éval, 1 % en financé ;
  - de l'objectif : réduit au reste à faire en éval, cible + attente en financé ;
  - de la règle des annonces (en financé seulement) ;
  - du reward virtuel au 14e jour.
- **Tailles.** Elles sont calculées sur **10 000 $ nominaux**, pas sur le solde de l'essai.
- **Dans les journaux** :
  - « COMPTE VIRTUEL : … reward → demander le payout » marque l'instant où, en vrai, on demanderait le payout ;
  - « éval perdu » marque l'instant où l'on rachèterait une éval.

## Installation du VPS (Contabo)

1. **Windows obligatoire.** Le package Python `MetaTrader5` ne fonctionne que sous Windows. Si le VPS Contabo est sous Linux, il faut le réinstaller en Windows Server depuis le panneau Contabo (licence Windows en option). MT5 sous Wine est possible mais fragile, et n'est pas prévu ici.
2. **Connexion et heure.** Se connecter en bureau à distance (RDP). Le fuseau horaire du VPS n'a pas d'importance : le bot convertit tout en heure de New York. L'horloge doit en revanche être juste, à vérifier avec `w32tm /query /status`.
3. **Essais FTMO.** Créer **deux essais gratuits FTMO** (Free Trial) de 10 000 $, plateforme **MT5**, depuis l'espace client FTMO.
4. **Deux installations de MT5.** Télécharger le terminal MT5 de FTMO et l'installer **deux fois**, dans `C:\MT5_A` et `C:\MT5_B` : à la 2e installation, choisir « Paramètres » et changer le dossier. Dans chaque terminal :
   - *Fichier → Se connecter* à l'essai correspondant, en cochant « Enregistrer le mot de passe ». Le bot ne connaît aucun mot de passe : il s'attache au terminal déjà connecté ;
   - *Outils → Options → Expert Advisors* : cocher « Autoriser le trading algorithmique » ;
   - *Outils → Options → Graphiques* : « Barres max. dans le graphique » = **Illimité**. Sans ce réglage, l'historique H1 est trop court pour le momentum 12-1 ;
   - afficher **US100.cash** dans l'observation du marché, puis ouvrir un graphique H1 et un graphique M1 et remonter loin vers la gauche, pour télécharger l'historique.
5. **Git et uv.** Installer Git pour Windows et `uv` (`powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`), puis :
   ```
   git clone https://github.com/arthurpeg/fabv2.git C:\fabv2
   cd C:\fabv2
   git checkout propfirm-ftmo
   uv sync
   copy live\config_A.example.toml live\config_A.toml
   copy live\config_B.example.toml live\config_B.toml
   ```
   Adapter `terminal` dans les deux fichiers si les dossiers de MT5 diffèrent.
6. **Essai à blanc, sans ordre.** Lancer les deux commandes ci-dessous. Elles doivent afficher les barres reçues, le spread, le signe du momentum (A), le signal 3n et l'état de M2 (B). Le « 12-1 » de A doit être un nombre, et non `nan`.
   ```
   uv run python -m live.bot --config live\config_A.toml --signaux
   uv run python -m live.bot --config live\config_B.toml --signaux
   ```
7. **Lancement.** Ouvrir deux fenêtres `cmd` et lancer `live\lancer.bat A` dans l'une, `live\lancer.bat B` dans l'autre. Le script relance le bot s'il s'arrête. Pour un démarrage automatique, créer une tâche planifiée « À l'ouverture de session » pour chaque book, et activer l'ouverture de session automatique de Windows.
8. **Fermer le RDP sans se déconnecter.** Fermer la fenêtre RDP (croix), mais **ne pas se déconnecter** de la session Windows : MT5 et les bots doivent rester dans une session ouverte.

## Mise à jour automatique depuis GitHub

[maj_auto.ps1](maj_auto.ps1) tourne toutes les 5 minutes, dans une tâche planifiée créée une seule fois. À chaque passage :

1. `git fetch`. Si rien n'est nouveau, il ne fait rien d'autre.
2. Avance rapide seulement. Si un fichier suivi par git a été modifié à la main sur le VPS, rien n'est fait et l'incident est écrit dans le journal.
3. `uv sync` si `pyproject.toml` ou `uv.lock` ont changé.
4. `tests/test_live.py`. En cas d'échec :
   - retour au commit précédent ;
   - les bots gardent l'ancien code ;
   - ce commit n'est plus retenté (il est noté dans `live/etat/maj_refusee.txt`), seul le suivant le sera.
5. Si le code (`*.py`) ou le calendrier (`annonces.csv`) a changé, il pose les drapeaux `live/etat/redemarrer_A` et `_B`. Chaque bot sauve alors son état, sort entre deux pas de sa boucle, et `lancer.bat` le relance 10 s plus tard avec le nouveau code. Une position ouverte reste suivie après la relance.

**Publication des journaux.** À chaque passage, avant la mise à jour, le script copie les journaux sur la branche **`vps-journal`** de GitHub et commite seulement si quelque chose a changé. Ce sont :
- pour chaque book : `trades.csv`, `signaux.csv`, `compte.json`, `etat.json` et `bot.log` ;
- en commun : `pnl.md`, `maj_auto.log` et les journaux de relance.

La branche est séparée du code, donc sans conflit possible avec la mise à jour. Sur le VPS, la copie de travail est dans `C:\fabv2-journal`. Le dépôt est public, donc ces journaux le sont aussi : numéros des essais et P&L, jamais de mot de passe.
- **Première fois.** Lancer le script à la main pour enregistrer l'accès GitHub : `powershell -ExecutionPolicy Bypass -File C:\fabv2\live\maj_auto.ps1`, puis accepter la fenêtre de connexion GitHub.
- **Lecture depuis un autre poste** : `git fetch origin vps-journal`, puis par exemple `git show origin/vps-journal:pnl.md` ou `git show origin/vps-journal:A/trades.csv`.

Le journal de la mise à jour est dans `live/etat/maj_auto.log`. Pour créer la tâche, une fois, dans PowerShell :
```
$a = New-ScheduledTaskAction -Execute "powershell.exe" -Argument '-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\fabv2\live\maj_auto.ps1"'; $t = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 5); Register-ScheduledTask -TaskName "fabv2 - mise a jour du bot" -Action $a -Trigger $t -Settings (New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 20))
```
Limites :
- **Fichier `lancer.bat`.** Une modification de ce fichier ne prend effet qu'après une relance à la main des fenêtres.
- **Branche.** Seule la branche suivie sur le VPS (`propfirm-ftmo`) est mise à jour.
- **Tests sur le VPS.** Les tests des signaux sur les barres NQ y sont sautés, faute de données. Restent le compte virtuel et le drapeau de redémarrage.

## Suivi

- **Dossier.** Tout est dans `live/etat/A` et `live/etat/B` (hors git) :
  - `bot.log` : tout ce que fait le bot, avec les erreurs ;
  - `trades.csv` : une ligne par trade, avec le prix du signal, le bid, l'ask et le prix d'exécution, le glissement, le spread à l'entrée (`spread_ordre`) et à la sortie (`spread_sortie`), le stop, l'objectif, le risque, la phase virtuelle, la raison de sortie, le P&L en $, en % et en R ;
  - `signaux.csv` : chaque signal calculé, y compris les jours sans trade ;
  - `compte.json` : le compte virtuel ;
  - `etat.json` : les positions suivies et les événements déjà traités.
- **Redémarrage.** Le bot peut être arrêté et relancé à tout moment. Une position fermée pendant l'arrêt (stop ou objectif) est comptée au redémarrage. Une sortie à l'heure manquée est faite dès le redémarrage. En revanche, une entrée manquée de plus de 5 minutes est abandonnée.
- **Suivi du P&L, tous essais additionnés.** Il est dans `live/etat/pnl.md`, régénéré après chaque trade fermé, ou à la demande avec `uv run python -m live.pnl`. Les essais sont additionnés comme un seul compte de 10 000 $ par book. Le suivi donne :
  - le P&L cumulé, le compte continu et son plus gros creux ;
  - le détail par stratégie et par essai MT5 ;
  - le résultat FTMO virtuel (rewards − évals achetées).

  Chaque ligne de `trades.csv` porte le numéro de l'essai (`compte_mt5`).
- **Alertes du bot** (dans `bot.log`, contrôlées toutes les 60 s) :
  - « NOUVEL ESSAI MT5 détecté » : le cumul continue ;
  - « TRADING DÉSACTIVÉ » : objectif de l'essai atteint, perte max ou essai expiré. Il faut créer un nouvel essai ;
  - « objectif de l'essai atteint » : l'essai gratuit 1-Step vise +5 %, alors que le compte virtuel garde le vrai objectif de +10 % ;
  - essai à −8 %.
- **Fin d'un essai (14 jours).** L'essai FTMO expire au bout de 14 jours. Il faut alors créer un nouvel essai et s'y connecter dans le **même** terminal (*Fichier → Se connecter*), de préférence le week-end, sans position ouverte. Le compte virtuel continue tel quel. Si l'essai est « perdu » chez FTMO (perte max de l'essai), le trading y est bloqué : même chose, il faut un nouvel essai.
- **Calendrier des annonces.** Il est dans [annonces.csv](annonces.csv) : NFP et CPI relevés sur bls.gov et décisions de la Fed sur federalreserve.gov le 2026-11-04. Les minutes de la Fed et le PIB avancé de 2027 sont *supposés* et à vérifier. Le bot prévient dans `bot.log` quand il reste moins de 35 jours de calendrier.

## Passage aux vrais comptes FTMO (2 × 1-Step 10k)

Les essais gratuits ont validé l'exécution (signaux, tailles, spreads, glissement, compte virtuel), pas l'edge : la décision repose sur le backtest ([[wiki/experiments/propfirm-ftmo-option]]). Sur un vrai compte, le compte virtuel joue le même rôle que sur la démo : il doit **suivre pas à pas l'état réel chez FTMO** (éval puis financé), d'où la remise à zéro au départ.

**Avant d'acheter**
- [ ] Budget : accepter de perdre le dépôt du plan (869 $ = 10 évals par paire, 79 € l'éval).
- [ ] Relire les règles du 1-Step 10k du moment sur ftmo.com et les comparer à `live/compte.py` : objectif +10 %, perte max 10 % sous le plus haut solde de fin de journée, perte du jour 3 %, meilleur jour ≤ 50 % du gain, reward au 14e jour après le 1er trade, 90 % versés. Relire aussi les règles des annonces (financé seulement), du trading algorithmique, de l'anti-hedging entre comptes et de l'« account rolling ». **Tout écart → me le signaler avant de lancer** : le compte virtuel et les simulations seraient faux.
- [ ] Compléter `live/annonces.csv` : minutes de la Fed et PIB avancé 2027 (supposés à ce jour).
- [ ] Choisir le jour de bascule : un week-end, sans position ouverte. Attention à B : s'il est en attente du reward sur la démo, rien ne presse ; le perdre n'a pas d'importance (virtuel).

**Bascule (sur le VPS, en RDP)**
1. [ ] Acheter deux 1-Step 10k, plateforme **MT5**, un par book.
2. [ ] Dans `C:\MT5_A` : *Fichier → Se connecter* au compte réel A (cocher « Enregistrer le mot de passe »). Idem `C:\MT5_B` avec le compte B. Vérifier dans chaque terminal le trading algorithmique autorisé, US100.cash affiché, graphiques H1 et M1 ouverts.
3. [ ] Dans `live\config_A.toml` et `live\config_B.toml` : `objectif_essai_pct = 10` (alerte à l'objectif réel, au lieu des +5 % de l'essai gratuit).
4. [ ] Réinitialiser les deux comptes virtuels : `uv run python -m live.reinit A B`. Le script refuse si une position est suivie. Chaque bot en marche se relance (≈ 10 s), archive son dossier dans `live\etat\archive\<book>_<horodatage>\` et repart d'une éval n° 1 à +0,00 %. Contrôler dans chaque `bot.log` la ligne « RÉINITIALISATION » puis « NOUVEL ESSAI MT5 détecté » avec le bon numéro de compte et 10 000 $ de solde.
5. [ ] `uv run python -m live.bot --config live\config_A.toml --signaux` (et B) : barres reçues, spread, 12-1 de A non `nan`, compte virtuel en éval à +0,00 %.
6. [ ] Ne **pas** lancer `--test-ordre` sur un compte réel (il passe un vrai ordre).
7. [ ] Le lendemain : `git fetch origin vps-journal` puis `git show origin/vps-journal:pnl.md`. Les trades de la démo ne doivent plus y apparaître.

**Ensuite, à chaque événement**
- [ ] **Éval validée** (« COMPTE VIRTUEL : … validée → financé » et FTMO coupe le compte) : se connecter au compte financé dans le **même** terminal, sans réinitialiser. Le compte virtuel est déjà en financé, risque 1 %.
- [ ] **Éval ou financé perdu** (« éval perdu ») : racheter une éval le jour même, s'y connecter dans le même terminal, sans réinitialiser (le virtuel a déjà compté le rachat).
- [ ] **Reward** (« reward → demander le payout ») : demander le payout dans l'espace client FTMO. Si le virtuel et FTMO divergent (date du reward, gain, meilleur jour), me le signaler.
- [ ] **Jamais de trade à la main** sur ces comptes : le compte virtuel ne le verrait pas et la règle des 50 % pourrait casser.
- [ ] Vérifier chaque jour qu'aucune alerte « !! » n'est restée sans suite (trading désactivé, barres M1 en retard, heure du VPS).

## Écarts connus avec le backtest (à mesurer)

- **Instrument.** Le bot trade le CFD US100.cash et non le future NQ :
  - le spread réel remplace l'hypothèse de 1,5 point ;
  - le signe du momentum est calculé sur le CFD, non ajusté du portage (≈ 3 à 4 %/an). Le bot prévient si |12-1| < 5 %. Dans ce cas, mettre `mom_signe = +1` ou `-1` dans la config d'après le NQ.
- **Jours écourtés.** M2 sort à la clôture XNYS (13:00) au lieu de la dernière barre NQ.
- **3n sorti à un objectif réduit en éval.** Il compte comme « TP », donc pas de M2 ce jour-là. Le moteur décide sur le R brut.
- **Holdout n° 26.** Ne pas comparer les trades du bot à un backtest recalculé sur les données NQ de la même période avant le 2028-02-29 : ce serait lire le holdout. On ne mesure d'ici là que l'exécution, à partir des seuls journaux du bot (glissement = prix d'exécution − prix du signal, spread, respect des heures).

## Réserves

Le bot est exploratoire et hors compteur d'essais. 3n et M2 ont échoué hors échantillon (n° 24 et 25), et le holdout n° 26 ne se lit qu'à partir du 2028-02-29. Ne pas le brancher sur un compte réel sans suivre la checklist « Passage aux vrais comptes FTMO » ci-dessus, en particulier la relecture des règles FTMO du moment.
