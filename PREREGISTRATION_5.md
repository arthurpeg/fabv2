# Pré-enregistrement n° 5 : gap d'ouverture du DAX prédit par les courbes étrangères

*2026-10-14, avant tout code de modélisation et toute exécution. Inspiré de De Gooijer, Diks & Gątarek (2009), « Information Flows around the Globe », TI 2009-107/4 ; résumé dans [papiers_ssrn_ouverture_us_2026-10-14.md](papiers_ssrn_ouverture_us_2026-10-14.md), texte intégral non disponible. Paramètres : [config/opening_gap.toml](config/opening_gap.toml).*

## Question

L'article trouve que l'ouverture européenne se prévoit, surtout en signe, à partir des courbes intrajournalières américaines de la veille et asiatiques de la nuit, avec une régression à noyau fonctionnelle (NP-FDA) meilleure que le linéaire. L'échantillon de test de l'article fait 35 jours (2007-2008).

Deux questions, séparées :
1. **A′ (prévision, non tradable)** : sur nos données, NP-FDA prévoit-il le gap clôture → ouverture du DAX mieux que le linéaire ?
2. **B (trading, test décisif)** : à 08:55 heure de Berlin, le FDAX a déjà intégré l'essentiel de la nuit. Reste-t-il un résidu prévisible entre 08:55 et 09:00 + k minutes, après coûts ?

## Données (aucune donnée inventée)

| Rôle | Série | Source | Période |
|---|---|---|---|
| Cible | FDAX `.v.0`, 1 min | Databento XEUR.EOBI | 2025-03-11 → 2026-08-28 |
| Amérique du Nord | ES et YM `.v.0`, 1 min (futures, heures du comptant 09:30-16:00 ET) | Databento GLBX | idem |
| Asie | Nikkei 225 (JPXJPY), Hang Seng (HKXHKD), ASX 200 (AUXAUD), 1 min | HistData, **CFD de courtier, pas le comptant** | 2025-01 → 2026-08 |

- Pas de TSX ni de comptant : la cible A′ est un **proxy sur le future** (FDAX 09:00 / FDAX 17:30 la veille − 1), pas le DAX au comptant.
- Les horodatages HistData suivent les règles d'heure d'été **européennes** (heure brute + 7 h = `Europe/Athens`), contrairement à leur FAQ. Mesuré sur l'ouverture des futures de Hong Kong ; testé automatiquement.
- Le contrat FDAX continu change au premier tick du 3e vendredi de mars, juin, septembre et décembre (saut de 0,5 à 0,9 %). Ces 6 nuits sont **exclues de A′**. B, qui reste dans la même matinée, n'est pas concerné.
- Sessions et jours fériés : `exchange_calendars` (XETR, XNYS, XTKS, XHKG, XASX). Un jour cible D est exclu si XETR n'a pas de séance la veille, si la séance NYSE de la veille Xetra manque, ou si l'un des 3 marchés asiatiques est fermé le jour D. **Échantillon commun à toutes les spécifications** : environ 325 jours (calcul préalable : 22 fériés Tokyo, 13 Hong Kong, 4 Sydney, 10 New York), moins les trous de données.

## Alignement temporel

- Tout est en UTC en interne.
- `t_decision` = 08:55 heure de Berlin du jour D (06:55 UTC l'été, 07:55 UTC l'hiver).
- Une barre 1 min étiquetée `s` (début) n'est utilisable que si `s + 1 min ≤ t_decision`.
- Fenêtres des courbes, choisies pour se terminer avant le `t_decision` le plus précoce (06:55 UTC), quelle que soit la saison :

| Marché | Fenêtre de la courbe |
|---|---|
| Nikkei | 09:00-15:30 JST du jour D (00:00-06:30 UTC) |
| Hang Seng | 09:30 HKT → 06:50 UTC du jour D (**tronquée** : la séance finit à 08:00 UTC, après `t_decision`) |
| ASX | 10:00-16:00 heure de Sydney du jour D |
| ES, YM | 09:30-16:00 ET de la séance NYSE de la veille Xetra |

- Pauses de midi (Tokyo, Hong Kong) : dernier prix reporté.

## Cibles

- **A′** : y = FDAX(open de la barre de 09:00, jour D) / FDAX(open de la barre de 17:30, veille) − 1.
- **B** : y_k = FDAX(open de la barre de 09:00 + k) / FDAX(open de la barre de 08:55) − 1, avec k ∈ {0, 15, 30, 60}. Les prix sont l'open de la première barre dans les 5 minutes, sinon le jour est exclu (convention de `fab/core.py`).

## Variables (toutes ajustées sur la fenêtre d'entraînement uniquement)

1. Rendement de la fenêtre de chaque marché (dernier / premier − 1) : base du modèle linéaire.
2. Courbe normalisée x(t) / x(1) × 100 sur une grille fixe de 5 min.
3. ACP fonctionnelle par marché sur les courbes discrétisées, **q = 5**. Chaque bloc de scores est divisé par la racine de sa variance totale d'entraînement, pour que chaque marché pèse autant.
4. Rendements par sous-période (première heure, milieu, dernière heure) : servent uniquement à un modèle linéaire de diagnostic en A′, jamais tradé.

Spécifications (cible DAX) :
- `c1` = Asie (le bloc qui vient de fermer) ;
- `c2` = Amérique du Nord (le bloc d'avant) ;
- `c12` = les deux.

## Modèles

- **OLS** : MCO sur les rendements de fenêtre de la spécification.
- **NP-FDA** :
  - distance euclidienne sur les scores ACP concaténés ;
  - noyau K(u) = 1,5 (1 − u²) sur [0, 1] ;
  - poids W_s = K(d/h) / Σ K ;
  - fonction de répartition conditionnelle pondérée F̂(y|x) ;
  - trois prédicteurs : moyenne (Nadaraya-Watson), médiane (F̂⁻¹(0,5)), mode (argmax de Σ_s K(|y − y_s| / h_y) W_s sur 200 points couvrant le support d'entraînement).
  - **h** : choisi par leave-one-out sur l'entraînement, en minimisant l'erreur absolue de la médiane conditionnelle, parmi les quantiles {0,05 ; 0,1 ; 0,2 ; … ; 0,9} des distances d'entraînement par paires.
  - **h_y** : 1,06 · σ_y · n^(−1/5) sur l'entraînement.
  - Si tous les poids sont nuls : « pas de signal », soit une prévision de 0 et une position nulle.
- **Intervalle de prévision CPI à 90 %** : [F̂⁻¹(0,05), F̂⁻¹(0,95)]. On rapporte la couverture effective.
- P-FDA (régression fonctionnelle linéaire, base de Fourier à 15 fonctions) : optionnelle, diagnostic A′ seulement, hors compteur.

## Validation glissante

- Fenêtre **expansive**, 120 jours d'entraînement initial, réestimation **tous les 20 jours**. Environ 205 prévisions hors échantillon.
- ACP, mise à l'échelle, h, h_y et coefficients sont réajustés à chaque réestimation, sur l'entraînement seulement.
- **Audit automatique** pour chaque prévision : horodatage de la dernière barre utilisée < `t_decision`, et dernier jour d'entraînement < jour prédit. Le run échoue sinon.

## Règles de trading (variante B)

- **Sens** : signe du mode conditionnel.
- **Taille** : w = min(1, |moyenne conditionnelle| / m_ref), où m_ref = médiane de |y| sur l'entraînement. Pas de levier : |w| ≤ 1.
- **Filtre de confiance** : P̂(y > 0) = Σ W_s 1{y_s > 0}. On n'entre que si P̂ > 0,55 pour un achat, ou P̂ < 0,45 pour une vente.
- **Filtre de coûts** : on n'entre que si |moyenne conditionnelle| > 1 × le coût aller-retour exprimé en rendement.
- **Filtre d'accord** avec OLS : désactivé.
- **OLS tradé** : sens = signe de ŷ, même taille et même filtre de coûts, sans filtre de confiance.
- **Coûts** : 1 tick (0,5 point) + 5 € aller-retour sur FDAX (25 €/point), soit 0,7 point. Sensibilité rapportée : coûts × 2.
- **Exécution** : `vbt.Portfolio.from_orders`, ordres aux horodatages exacts d'entrée et de sortie, `targetpercent`.

## Essais : 24 candidats (le compteur global passe de 150 à 174)

- NP-FDA (mode) × {c1, c2, c12} × k ∈ {0, 15, 30, 60} = 12
- OLS × {c1, c2, c12} × k ∈ {0, 15, 30, 60} = 12

**Configuration principale, désignée à l'avance** : NP-FDA, mode, `c12`, **k = 15**. C'est la piste la plus forte de l'article, et 15 minutes laissent au cours le temps de bouger plus que le coût. Les 23 autres sont secondaires.

Références, mêmes conditions, hors compteur :
- toujours acheteur ;
- signe du rendement d'ES de la séance US de la veille ;
- signe du rendement nocturne du FDAX (17:30 → 08:55) ;
- signal aléatoire : 1 000 permutations des positions de la configuration principale entre les jours hors échantillon.

## Critères de décision (fixés avant exécution)

**A′, prévision.** On dit que NP-FDA bat le linéaire si :
- son MSE (moyenne conditionnelle) est inférieur à celui d'OLS **et** le test de Diebold-Mariano unilatéral (variance HAC) donne p < 0,05, pour au moins `c12` ;
- et que le taux d'erreur de signe du mode est inférieur à 50 % (binomial unilatéral, p < 0,05) **et** inférieur à celui d'OLS.

**B, trading.** Le signal « bat le future après coûts » si la configuration principale vérifie **toutes** les conditions suivantes :
- Sharpe net > 0 ;
- p de permutation < 0,05 ;
- DSR > 0,95 avec N = 24 (on rapporte aussi le DSR avec N = 174) ;
- rendement net supérieur à celui de « toujours acheteur » et à celui du « signe US naïf ».

Une configuration secondaire qui passe ces critères est rapportée comme **exploratoire**, sans conclusion.

**Puissance (à lire avant les résultats).** Avec environ 205 jours hors échantillon :
- l'erreur type du taux de bon signe est d'environ 3,5 points : un taux de bon signe ne devient significatif qu'au-dessus d'environ 56 % ;
- l'erreur type d'un Sharpe annualisé est d'environ 1,1 : un Sharpe ne devient significatif qu'au-dessus d'environ 1,9.

Un échec ne prouvera donc pas l'absence d'effet. Il dira qu'un effet, s'il existe, est trop petit pour être vu sur 1,4 an.

**Garde-fou.** Si un résultat dépasse un Sharpe de 3 ou un taux de réussite de 70 %, on cherche d'abord une fuite d'information avant de le présenter.

## Rapport

[reports/opening_gap_report.md](reports/opening_gap_report.md) :
- A′ contre B ;
- tableaux de prévision (MSE, erreur de signe, couverture du CPI) et de trading (rendement, Sharpe, drawdown maximal, taux de réussite, nombre de trades, rotation, exposition) ;
- découpage par année (2025, 2026) et par tercile de volatilité réalisée passée du FDAX (20 jours, calculée sans regarder le futur) ;
- courbes de capital, limites, conclusion.

---

## Amendement 1 (2026-10-14, avant tout code de modélisation et toute exécution) : 10 ans

À la demande de l'utilisateur, l'étude passe à **2016-01 → 2026-08**. Le FDAX n'existant chez Databento que depuis 2025-03, la cible devient le **DAX en CFD (HistData GRX/EUR)**.

**Validation du proxy, faite avant ce choix** (seuls des prix ont été comparés, aucun modèle n'a été estimé), sur la période commune 2025-03 → 2026-08 :
- corrélation des rendements 5 min avec le FDAX : 0,91 ;
- corrélation de la cible A′ : 0,994 ;
- corrélation de la cible B (08:55 → 09:15) : 0,999, avec le même signe 98 % des jours ;
- aucun décalage temporel.

La règle de fuseau HistData (heure brute + 7 h = `Europe/Athens`) est vérifiée chaque année de 2016 à 2026 sur les ouvertures de Hong Kong (09:15), de Sydney (09:50) et du DAX (08:00 et 09:00).

Changements, et seulement ceux-ci :
- **Cibles A′ et B** : calculées sur le CFD DAX, avec le coût du FDAX (0,7 point aller-retour) exprimé en fraction du prix. Les prix CFD sont des cotations de courtier, pas des prix exécutables sur Eurex. C'est une limite qui sera rappelée dans le rapport.
- **Validation sur le vrai future** : sur 2025-03 → 2026-08, les mêmes prévisions sont exécutées sur les prix FDAX. C'est rapporté à côté, sans compter comme des essais supplémentaires.
- **Validation glissante** : fenêtre expansive, **500 jours d'entraînement initial** (environ 2 ans), réestimation tous les 20 jours. Environ 1 900 prévisions hors échantillon. Rapport aussi découpé avant et après le 2022-12-31, la coupure IS / OOS habituelle du dépôt.
- **Jours exclus en plus** : séances écourtées (fermeture du calendrier avant la fin de la fenêtre d'une courbe) et jours où plus de 20 % des points d'une courbe manquent.
- **Nikkei** : les minutes de reprise quotidienne du CFD (07:00 et 08:00 JST) sont hors de la fenêtre 09:00-15:30 et ne sont donc pas utilisées.
- **Puissance révisée** : avec environ 1 900 jours, l'erreur type d'un Sharpe annualisé est d'environ 0,36. Un Sharpe ne devient significatif qu'au-dessus d'environ 0,6, et un taux de bon signe au-dessus d'environ 52 %.

Tout le reste est inchangé : grille de 24 candidats, configuration principale (NP-FDA, mode, `c12`, k = 15), filtres, critères et compteur (150 → 174). Les critères de B s'appliquent à la série CFD sur toute la période hors échantillon.

## Amendement 2 (2026-10-14, avant toute estimation de modèle) : fenêtre du Nikkei

Le calendrier XTKS montre que la Bourse de Tokyo fermait à **15:00 JST jusqu'au 2024-11-04**, et ne ferme à 15:30 que depuis. Avec la fenêtre 09:00-15:30 prévue, 85 % des jours seraient exclus comme séances écourtées. Pour garder une grille identique sur toute la période, la fenêtre du Nikkei devient **09:00-15:00 JST** (00:00-06:00 UTC). Rien d'autre ne change.
