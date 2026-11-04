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
  - 3n : 20:05, sortie 03:00 ;
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

## Suivi

- **Dossier.** Tout est dans `live/etat/A` et `live/etat/B` (hors git) :
  - `bot.log` : tout ce que fait le bot, avec les erreurs ;
  - `trades.csv` : une ligne par trade, avec le prix du signal, le prix d'exécution, le spread, le stop, l'objectif, le risque, la phase virtuelle, la raison de sortie, le P&L en $, en % et en R ;
  - `signaux.csv` : chaque signal calculé, y compris les jours sans trade ;
  - `compte.json` : le compte virtuel ;
  - `etat.json` : les positions suivies et les événements déjà traités.
- **Redémarrage.** Le bot peut être arrêté et relancé à tout moment. Une position fermée pendant l'arrêt (stop ou objectif) est comptée au redémarrage. Une sortie à l'heure manquée est faite dès le redémarrage. En revanche, une entrée manquée de plus de 5 minutes est abandonnée.
- **Fin d'un essai (14 jours).** L'essai FTMO expire au bout de 14 jours. Il faut alors créer un nouvel essai et s'y connecter dans le **même** terminal (*Fichier → Se connecter*), de préférence le week-end, sans position ouverte. Le compte virtuel continue tel quel. Si l'essai est « perdu » chez FTMO (perte max de l'essai), le trading y est bloqué : même chose, il faut un nouvel essai.
- **Calendrier des annonces.** Il est dans [annonces.csv](annonces.csv) : NFP et CPI relevés sur bls.gov et décisions de la Fed sur federalreserve.gov le 2026-11-04. Les minutes de la Fed et le PIB avancé de 2027 sont *supposés* et à vérifier. Le bot prévient dans `bot.log` quand il reste moins de 35 jours de calendrier.

## Écarts connus avec le backtest (à mesurer)

- **Instrument.** Le bot trade le CFD US100.cash et non le future NQ :
  - le spread réel remplace l'hypothèse de 1,5 point ;
  - le signe du momentum est calculé sur le CFD, non ajusté du portage (≈ 3 à 4 %/an). Le bot prévient si |12-1| < 5 %. Dans ce cas, mettre `mom_signe = +1` ou `-1` dans la config d'après le NQ.
- **Jours écourtés.** M2 sort à la clôture XNYS (13:00) au lieu de la dernière barre NQ.
- **3n sorti à un objectif réduit en éval.** Il compte comme « TP », donc pas de M2 ce jour-là. Le moteur décide sur le R brut.
- **Holdout n° 26.** Ne pas comparer les trades du bot à un backtest recalculé sur les données NQ de la même période avant le 2028-02-29 : ce serait lire le holdout. On ne mesure d'ici là que l'exécution, à partir des seuls journaux du bot (glissement = prix d'exécution − prix du signal, spread, respect des heures).

## Réserves

Le bot est exploratoire et hors compteur d'essais. 3n et M2 ont échoué hors échantillon (n° 24 et 25), et le holdout n° 26 ne se lit qu'à partir du 2028-02-29. Le bot ne fait que la démo : ne pas le brancher sur un compte réel sans relire les règles FTMO du moment (annonces, trading algorithmique, « account rolling »).
