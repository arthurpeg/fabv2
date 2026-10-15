# Pré-enregistrement n° 7 : le fix de Londres à 16h en fin de mois (Melvin et Prins)

*2026-10-15, avant tout calcul de rendement ou de P&L. Papier : Melvin et Prins, « Exchange Rates, Equity Hedging, and the London 4pm Fix », SSRN 2019274, texte intégral : [papers/ssrn_2026-10-13/c/ssrn-2019274.txt](papers/ssrn_2026-10-13/c/ssrn-2019274.txt). Classé deuxième de la revue des papiers du 2026-10-13, après le fade de la reprise FX (pré-enregistrement n° 6, rejeté).*

## Ce que dit le papier

- Données : G10 contre USD, barres de 5 minutes, **2004-2008**, donc avant la réforme du fix de février 2015. Depuis, le fix WM/Reuters est calculé sur une fenêtre de 5 minutes (15:57:30-16:02:30 Londres) au lieu d'une minute.
- Mécanisme : les gérants actions internationaux ajustent leur couverture de change au fix de 16h, le dernier jour ouvré du mois. Les banques garantissent le prix du fix et poussent le marché dans le sens des ordres pendant la fenêtre (« market-impact-maximizing trades »). L'impact est temporaire.
- **Résultat A (retournement)**, régression poolée sur les devises :
  r(16:00 jour J → 12:00 jour J+1) = −0,178 × r(15:00 → 16:00) − 0,518 × r(15:00 → 16:00) × 1{fin de mois}.
  En fin de mois, environ 70 % du mouvement de l'heure précédant le fix est annulé le lendemain midi. Les deux coefficients ont p = 0,00 ; R² = 0,66 %.
- **Résultat B (sens du flux)** : le jour de fin de mois, r(13:00 → 16:00) de la devise est négatif en la performance relative des actions du pays sur le mois (du 1er à l'avant-dernier jour, de clôture à clôture). Les actions qui ont surperformé entraînent une **dépréciation** de leur devise dans les 3 heures avant le fix. Le coefficient est significatif (p = 0,00, R² = 2 %), mais sa valeur est illisible dans le PDF.
- Les heures sont notées « GMT » dans le papier : il s'agit de l'heure de Londres (le fix est à 16:00 heure de Londres toute l'année).

## Données

Futures FX CME de `D:/quant-data/Cotations/forex`, comme au n° 6 : prix de transactions 1 minute, 2016-01-03 → 2026-08-28, contrat continu `.v.0`. On a 6E (EURUSD), 6B (GBPUSD), 6A (AUDUSD) et 6J (inversé en USDJPY). Pas de CAD, CHF, SEK, NOK ni NZD. **L'échantillon est entièrement postérieur à la réforme de 2015** : c'est le test de survie de l'effet.

Pour le résultat B, il faut un indice actions par pays :

| Paire | Indice du pays | Source | Indice US |
|---|---|---|---|
| 6E | DAX (Euro Stoxx 50 du 2020-06-15 au 2023-12-01, voir amendement 3 du n° 5) | HistData GRX/EUR, CFD | ES (Databento) |
| 6A | ASX 200 | HistData AUX/AUD, CFD | ES |
| 6J | Nikkei 225 | HistData JPX/JPY, CFD | ES |
| 6B | **aucun indice britannique** : 6B est exclu du résultat B | — | — |

Les mois de juin 2020 et de décembre 2023 sont exclus pour 6E dans le résultat B : l'indice change en cours de mois. On garde l'Euro Stoxx 50 entre ces dates, comme indice européen de substitution.

## Alignement temporel

- Toutes les heures de règle sont en **`Europe/London`**, qui suit l'heure d'été britannique. Les horodatages Databento sont en UTC. Les fichiers HistData du cache sont déjà en UTC (règle « heure brute + 7 h = `Europe/Athens` », vérifiée au n° 5). Tests unitaires : fix à 16:00 UTC en hiver, 15:00 UTC en été, et semaines où les États-Unis et le Royaume-Uni ne sont pas à la même heure.
- Prix à l'instant T = open de la première barre dans [T, T + 5 min). Sinon, l'événement est exclu (convention de `fab/core.py` et du n° 6).
- **Jour de fin de mois (FDM)**, par paire : la dernière date de Londres du mois civil où le future a une barre dans [16:00, 16:05) heure de Londres. Les jours de fin de trimestre et de fin d'année sont un sous-ensemble, rapporté en descriptif seulement.
- **Jour suivant** (sortie du résultat A) : la prochaine date de Londres où le future a une barre dans [12:00, 12:05) heure de Londres.
- **Roulements** : on travaille en prix bruts. On exclut tout trade dont l'intervalle, du début du signal à la sortie, contient une barre de 00:00 UTC du **8 au 21** d'un mois trimestriel. Ces dates sont fixées par une inspection préalable, faite sans aucun P&L : sur 2016-2026, tous les sauts de plus de 0,05 % à 00:00 UTC des fenêtres de roulement tombent entre le 13 et le 19. Les trades de fin de mois ne sont donc presque jamais touchés.

## Règles testées

### Résultat A : retournement après le fix

- Signal : m = open(16:00) − open(15:00), en pips de la paire, heure de Londres.
- Position : sens = −signe(m), à l'entrée. Sortie à l'open de 12:00 heure de Londres le jour suivant.
- Entrées :
  - E0 = open de 16:00. C'est l'instant où le signal se termine, donc c'est optimiste.
  - E1 = open de 16:01.
  - **E5 = open de 16:05**, après la fin de la fenêtre du fix (16:02:30).
- Jours : **FDM** (prédiction du papier : retournement fort) et **non-FDM** (prédiction : retournement plus faible, coefficient −0,178).

### Résultat B : sens du flux avant le fix

- Signal : x = r_actions(pays) − r_actions(US) sur le mois.
- Chaque indice est relevé à sa **clôture au comptant locale** : dernier close 1 minute à son heure de clôture ou avant, dans les 10 minutes. Heures retenues :
  - ES : 16:00 New York ;
  - DAX : 17:30 Berlin ;
  - ASX : 16:00 Sydney ;
  - Nikkei : 15:00 Tokyo, puis 15:30 à partir du 2024-11-05.
- Le rendement va de la clôture du dernier jour de bourse du mois précédent à celle du dernier jour de bourse strictement antérieur au jour FDM. Tout est connu avant 13:00 à Londres le jour FDM.
- Position sur la paire, dans le sens d'une **dépréciation de la devise dont les actions ont surperformé** :
  - 6E et 6A (XXXUSD) : sens = −signe(x) ;
  - USDJPY : sens = +signe(x).
- Entrée à l'open de 13:00 heure de Londres le jour FDM. Sortie à l'open de **16:00** (fin de la fenêtre du papier) ou de **16:05**.
- Contrôle : la même règle les jours **non-FDM**, avec x calculé du début du mois à la veille. Prédiction : effet plus faible.

## Essais : 9 (le compteur global passe de 192 à 201)

- Résultat A : 3 entrées × 2 types de jours = 6
- Résultat B : 2 sorties les jours FDM, plus le contrôle non-FDM avec sortie à 16:00 = 3

**Deux configurations principales, désignées à l'avance, chacune au seuil α = 0,025 (Bonferroni sur 2) :**
- **A\*** : retournement, jours FDM, entrée E5 (16:05), sortie à 12:00 le lendemain, 4 paires ;
- **B\*** : sens du flux, jours FDM, 13:00 → 16:00, 3 paires.

## Coûts (aller-retour, en pips de la paire)

- **Coût principal = coût standard du dépôt** : 1 tick + 5 $ aller-retour, converti en pips (environ 0,9 à 2 pips). On entre et on sort l'après-midi à Londres, ou à midi, en carnet profond.
- Grille de sensibilité : 0, 1, 2 et 3 pips. Ce sont les mêmes positions : la grille ne compte pas comme des essais en plus.
- Spread de point mort = gain brut moyen par trade, en pips.

## Mesure de la performance

- Par trade : P&L en pips (par paire et poolé), PF, taux de réussite, gain moyen, années perdantes.
- Portefeuille : backtest **vectorbt** (`fxreopen.backtest.simulate`, `Portfolio.from_orders`). Une colonne par paire, 1/4 du capital chacune, sans levier, regroupées. Pour B, la colonne 6B reste vide, donc 3/4 du capital au plus sont engagés. Rendement par séance, Sharpe annualisé avec √252, drawdown maximal, courbes de capital.
- Fenêtres : **2016-2020** et **2021-2026-08** (deux moitiés), plus l'ensemble.
- **Réplication du papier**, en lecture secondaire :
  - pour A, régression poolée r(16:00 → 12:00 J+1) = a + b·m + c·m·1{FDM} sur tous les jours, entrée E0 comme dans le papier, erreurs types groupées par date ;
  - pour B, régression poolée r(13:00 → 16:00) = a + b·x sur les jours FDM.
  On compare les signes et les ordres de grandeur à −0,178 et −0,518.

## Critères de décision (fixés avant exécution)

Une configuration principale **survit** si elle remplit **toutes** ces conditions, au coût principal :
1. gain moyen net > 0 et PF > 1 sur **chacune** des deux moitiés (2016-2020 et 2021-2026-08) ;
2. p < 0,025 pour la moyenne du rendement journalier net vectorbt > 0, par bootstrap stationnaire (blocs de 10 jours en moyenne, 10 000 tirages) sur tout le calendrier des séances ;
3. **p de permutation < 0,025** : 10 000 permutations du sens (±1) entre les événements, paire par paire, avec les mêmes instants ; statistique = gain moyen net par trade ;
4. **DSR > 0,95** avec N = 9 et la variance des Sharpe journaliers des 9 essais au coût principal (le DSR avec N = 201 est rapporté).

Lectures secondaires, fixées elles aussi à l'avance :
- **A, contrôle non-FDM** : le papier prédit un retournement plus faible qu'en FDM. C'est confirmé si le gain brut moyen par trade en non-FDM (E5) est inférieur à celui en FDM.
- **A, exécutabilité** : la part du retournement acquise entre 16:00 et 16:05, en pips (E0 − E5).
- **B, contrôle non-FDM** : confirmé si le gain brut moyen est inférieur à celui des jours FDM.
- Reality Check de White sur les 9 règles au coût principal (bootstrap stationnaire, blocs de 10 jours, 5 000 tirages).

**Puissance (à lire avant les résultats).**
- A\* : environ 127 fins de mois × 4 paires ≈ 500 trades. Avec un écart type de l'ordre de 40 à 60 pips sur environ 20 heures, l'erreur type du gain moyen poolé est d'environ 2 à 3 pips. Un retournement de 70 % d'un mouvement d'environ 10 à 15 pips (soit 7 à 10 pips) serait détectable. Un retournement de 2 pips ne le serait pas.
- B\* : environ 127 × 3 ≈ 380 trades. Avec un écart type d'environ 20 pips sur 3 heures, l'erreur type est d'environ 1 pip.
- Les tests de fin de mois restent peu puissants : un échec n'est pas une preuve d'absence.

**Garde-fou.** Si un résultat dépasse un PF de 3, un taux de réussite de 70 % ou un Sharpe journalier de 2, on cherche d'abord une fuite (horodatage, heure d'été, prix du signal réutilisé, roulement) avant de le présenter.

## Rapport

[reports/fx_fix_report.md](reports/fx_fix_report.md) et une section dans [RESULTS.md](RESULTS.md) :
- anatomie : taille de |m| en FDM et hors FDM ;
- tableaux des 9 règles par fenêtre et par coût, vectorbt et par trade ;
- régressions de réplication, critères, DSR, permutations, Reality Check ;
- courbes de capital ;
- verdict pour A\* et B\*.
