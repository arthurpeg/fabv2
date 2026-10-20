# Pré-enregistrement n° 8 : asymétrie intraday ancrée sur l'ouverture (Valenti 2026)

*2026-10-20, avant tout calcul de rendement ou de P&L. Papier : Valenti (2026), « Intraday Price Asymmetry and Next-Day Intraday Returns in the S&P 500 », SSRN 6074846, texte intégral : [papers/ssrn_2026-10-13/c/ssrn-6074846.txt](papers/ssrn_2026-10-13/c/ssrn-6074846.txt). Troisième de la revue des papiers du 2026-10-13, après les n° 6 et 7, tous deux rejetés.*

## Ce que dit le papier

- **Signal** : Asym_t = ln(H_t / O_t) + ln(L_t / O_t), sur la séance régulière du jour t de SPY.
- **Règle** : si Asym_t < 0, long de l'ouverture à la clôture de t+1 ; si Asym_t > 0, short. Pas de seuil, pas d'optimisation, pas de frais.
- Données : SPY (Bloomberg), 2002-08 → 2025-12.
- Résultats annoncés (annualisés **sur les seuls jours actifs**) :
  - long conditionnel : 16,9 %, ratio 1,09 ;
  - short conditionnel : 8,9 %, ratio 0,64 ;
  - combiné : 12,9 %, ratio 0,88 ;
  - long inconditionnel ouverture → clôture : 4,1 %.
- Variantes du papier (combiné, contrariant) :
  - ancrée sur la clôture de la veille : 4,6 % ;
  - ancrée sur la clôture du jour : −9,5 % ;
  - rendement ouverture → clôture du jour : 11,0 % ;
  - clôture → clôture : 4,2 %.
- **Objection soulevée à la lecture (2026-10-15)** : on a l'identité exacte Asym_O = Asym_C + 2·ln(C/O). Le signal mélange donc le contrariant sur le rendement du jour (qui marche seul à 11 %) et la position de la clôture dans le range (qui perd en contrariant). Ce qu'Asym apporte en plus d'un simple retournement ouverture → clôture n'est pas démontré.

## Données

- **ES** (proxy de SPY) : futures CME 1 minute, Databento `ES.v.0`, **2016-01 → 2026-08**, prix bruts. Séance régulière 09:30 → 16:00 heure de New York.
  - O = open de la barre de 09:30 ;
  - H et L = max des high et min des low des barres 09:30 → 15:59 ;
  - C = close de la barre de 15:59.
  - Un jour n'est retenu que s'il a une barre à 09:30 et une à 15:59. Les demi-séances (clôture à 13:00) sont donc exclues, comme jour de signal et comme jour de trade.
  - Les roulements tombent sur une barre de 00:00 UTC, jamais dans la séance : prix bruts sans risque, car tout se calcule dans une même séance.
- **DAX, réplication hors États-Unis** : CFD HistData GRX/EUR (cache UTC), séance 09:00 → 17:30 heure de Berlin.
  - Le fichier n'a que open et close : H et L = max et min des open et close 1 minute de la séance.
  - Entre le 2020-06-15 et le 2023-12-01, le fichier contient un autre indice européen (amendement 3 du n° 5). Les signaux et les trades restent intra-séance, donc on garde ces jours. On exclut seulement les paires (t, t+1) qui chevauchent les deux dates de bascule.
- **Recouvrement avec le papier** : 2016-2025 est inclus dans l'échantillon du papier. Ce n'est pas un test hors échantillon dans le temps. C'est une réplication sur un autre instrument (future au lieu de l'ETF, prix de transactions 1 minute) et sur un autre marché (DAX). Seuls 2026-01 → 2026-08 sont postérieurs : 8 mois, rapportés sans critère.

## Règles testées (7 essais, le compteur global passe de 201 à 208)

Sur ES, entrée à l'open de 09:30 de t+1, sortie au close de 15:59 de t+1. Sens selon le signal du jour t (−signe pour un signal contrariant) :

| # | Règle | Signal du jour t | Rôle |
|---|---|---|---|
| 1 | **ES_asym** | Asym_O = ln(H/O) + ln(L/O) | **principale**, règle du papier (long et short) |
| 2 | ES_asym_prevC | ln(H/C_{t−1}) + ln(L/C_{t−1}) | variante du papier |
| 3 | ES_asym_C | ln(H/C) + ln(L/C) | variante du papier (attendu : perdant) |
| 4 | ES_roc | ln(C/O) du jour t | **le concurrent direct** : contrariant sur le rendement du jour |
| 5 | ES_asym_long | Asym_O < 0 → long, sinon à plat | jambe longue seule |
| 6 | ES_asym_short | Asym_O > 0 → short, sinon à plat | jambe courte seule |
| 7 | DAX_asym | Asym_O sur le DAX, 09:00 → 17:30 Berlin | réplication hors États-Unis |

Pour C_{t−1} (règle 2), on prend la clôture de 15:59 du jour de séance régulière précédent. On exclut le cas où un roulement sépare t−1 et t, c'est-à-dire où une barre de 00:00 UTC du 8 au 21 d'un mois trimestriel tombe entre les deux.

Lecture secondaire, **sans compter d'essai** : entrée à 09:31 au lieu de 09:30 pour la règle 1, pour l'exécutabilité.

## Coûts

- ES : **coût principal = 1 tick + 5 $ aller-retour** (0,35 point, environ 0,7 à 1,7 pb selon le niveau). Grille : 0, 1, 2 et 5 pb aller-retour.
- DAX (CFD) : **coût principal = 2 pb aller-retour** (environ 1 spread de CFD plus le glissement). Grille identique.
- La grille porte sur les mêmes positions : elle ne compte pas comme des essais en plus.

## Backtest et mesures

- **vectorbt** : `Portfolio.from_orders`, une colonne par règle et par marché, cible ±100 % du capital (1×, sans levier). Ordre d'entrée à l'open de t+1 et ordre de sortie au close de t+1, frais = demi-coût par ordre. Les jours sans signal ou à plat, rendement nul.
- Rendements journaliers sur le calendrier des séances, Sharpe annualisé avec √252, drawdown maximal, courbes de capital.
- Pour comparer au papier, on rapporte aussi la moyenne et la volatilité annualisées **sur les seuls jours actifs**.
- Par trade : gain moyen en pb, taux de réussite, PF, années perdantes.
- Fenêtres : **2016-2020**, **2021-2026-08**, et l'ensemble. Sur ES, les 8 mois de 2026 sont rapportés à part.

## Critères de décision (fixés avant exécution)

La règle principale **ES_asym** survit si elle remplit **toutes** ces conditions, au coût principal :
1. rendement moyen net > 0 et PF > 1 sur **chacune** des deux moitiés (2016-2020 et 2021-2026-08) ;
2. p < 0,05 pour la moyenne du rendement journalier net vectorbt > 0, par bootstrap stationnaire (blocs de 10 jours, 10 000 tirages) ;
3. p de permutation < 0,05 : 10 000 permutations du sens (±1) entre les jours de trade, mêmes instants, statistique = rendement moyen net par trade ;
4. **DSR > 0,95** avec N = 7 (le DSR avec N = 208 est rapporté) ;
5. **apport par rapport au contrariant ouverture → clôture**. On estime par MCO r_{t+1} = a + b·Asym_O,t + c·ln(C_t/O_t), avec des erreurs types de Newey-West (5 retards), sur 2016-2026. Il faut b < 0 avec p < 0,05 (unilatéral). Sans ce critère, la règle n'ajoute rien au retournement déjà connu.

Lectures secondaires, fixées elles aussi à l'avance :
- le papier prédit : jambe longue > jambe courte, ancrage sur la clôture du jour perdant, ancrage sur la clôture de la veille plus faible. On rapporte si chaque prédiction est vérifiée ;
- **DAX_asym** : on applique les critères 1 à 3 au coût de 2 pb. C'est une réplication, pas une condition de survie de ES_asym ;
- Reality Check de White sur les 7 règles au coût principal ;
- écart entre l'entrée à 09:30 et l'entrée à 09:31.

**Puissance.** Environ 2 650 jours de trade sur ES. Avec un écart type journalier ouverture → clôture d'environ 0,9 %, l'erreur type du rendement moyen par trade est d'environ 1,7 pb. Le papier implique environ 12,9 % / 252 ≈ 5 pb par jour : c'est détectable (t ≈ 3) si l'effet tient.

**Garde-fou.** Si le Sharpe journalier net dépasse 2 ou si le taux de réussite dépasse 60 %, on cherche d'abord une fuite (prix du jour t+1 utilisé dans le signal, mauvais fuseau, barres de 15:59 manquantes) avant de présenter le résultat.

## Rapport

[reports/asym_report.md](reports/asym_report.md) et une section dans [RESULTS.md](RESULTS.md) : tableaux des 7 règles par fenêtre et par coût (vectorbt et par trade), comparaison aux chiffres du papier (jours actifs), régression d'apport, critères, DSR, permutations, Reality Check, courbes de capital, verdict.
