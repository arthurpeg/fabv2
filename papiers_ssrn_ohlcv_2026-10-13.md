# Papiers SSRN : mécanismes intraday OHLCV (Indices US · Forex majeurs · Pétrole · Or)

*Session du 2026-10-13. Source : API OpenAlex, filtrée sur la source SSRN (`S4210172589`), 72 requêtes thématiques, environ 5 300 candidats triés par titre puis lus un par un. Les résumés viennent d'OpenAlex, puis de Semantic Scholar ou Crossref quand OpenAlex n'en a pas. Les résumés ci-dessous sont **paraphrasés en français** à partir de l'abstract officiel, pas recopiés.*

*Exclus d'office : les papiers déjà fournis lors des sessions précédentes (voir [papers/seen_papers.json](papers/seen_papers.json)) et ceux dont le signal demande des données externes (VIX/VXN, options, sentiment, carnet d'ordres).*

**Légende** : 🔴 échec ou condition limite · ⚠️ la cause ou le filtre dépend d'une donnée non OHLCV (calendrier, flux) · ❓ résumé introuvable dans les API, contenu tiré de ma connaissance du papier, **à vérifier** · 🧪 papier SSRN récent d'auteur indépendant, non relu par des pairs

---

## A. Indices US

### [1] Nasdaq-100 Index Futures: Intraday Momentum or Reversal?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=712168
- **Actifs :** Indices (futures Nasdaq-100)
- **Plage horaire / Session :** session overnight (clôture → ouverture) ; heures d'ouverture ; 4 sous-périodes intraday ; lundi
- **Date :** 2005 | **Auteurs :** Susana Yu, Joel C. Rentzler, Avner S. Wolf | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture, juste après le rendement overnight, et dans les premières heures de séance. **Qui subit la contrainte** : les positions prises la nuit, sur un marché peu liquide, sont soldées ou corrigées quand la liquidité du jour arrive. **Effet sur les bougies** : le rendement overnight est surtout suivi d'un **retournement** en séance. Le rendement de la veille peut donner momentum ou retournement selon son signe, celui de la nuit, et le jour (lundi).

> **Résumé (abstract paraphrasé) :** Une régression relie le rendement intraday du jour au rendement de la veille et à celui de la nuit. Elle tient compte du signe de chacun, du régime haussier ou baissier et du jour de la semaine. Il n'y a pas d'effet simple « momentum » ou « retournement » : les deux coexistent et dépendent des signes et du lundi. La nuit est surtout associée à des retournements. La prévision est efficace sur quatre périodes intraday, ce qui suggère une particularité structurelle des heures d'ouverture.

### [2] Can Simple Buy and Sell Rules Increase Index Future Day Trading Profitability

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=523762
- **Actifs :** Indices (futures d'indices US)
- **Plage horaire / Session :** ouverture → clôture ; gap d'ouverture
- **Date :** 2004 | **Auteurs :** Joel C. Rentzler, Susana Yu | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : entrée à l'ouverture, sortie à la clôture ou sur un stop intraday. **Qui subit la contrainte** : le day trader en tendance, qui supporte des journées de retournement ; le stop coupe les séances où la tendance d'ouverture échoue. **Effet sur les bougies** : la distribution open→close a une queue gauche qu'un stop tronque, d'où un gain pour la stratégie tendance. Rien de tel pour la stratégie de retournement de gap.

> **Résumé (abstract paraphrasé) :** Teste deux stratégies courantes de day trading sur futures d'indices : suivre la tendance (achat à l'ouverture, vente à la clôture) et retourner le gap. Les stops intraday semblent ajouter du rendement à la stratégie tendance. Aucune preuve solide que les règles de sécurisation du profit aident, ni que l'une ou l'autre règle de sortie améliore la stratégie de retournement de gap. 🔴 pour le gap reversal.

### [3] 🔴 Closing the Question on the Continuation of Turn-of-The-Month Effects: Evidence from the S&P 500 Index Futures Contract

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=244085
- **Actifs :** Indices (futures S&P 500, spot S&P 500)
- **Plage horaire / Session :** calendaire : dernier jour du mois + 3 premiers jours
- **Date :** 2000 | **Auteurs :** Edwin D. Maberly, Daniel F. Waggoner | **Citations :** 9

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : de la clôture de J-1 du mois jusqu'à J+3. **Qui subit la contrainte** : les flux d'achat des particuliers en début de mois. Quand ces flux passent par les fonds communs, ils changent de calendrier et l'effet s'efface. **Effet sur les bougies** : avant 1990, bougies haussières anormales autour du changement de mois ; **après 1990, plus d'effet**.

> **Résumé (abstract paraphrasé) :** L'effet « turn of the month » (rendements anormaux du dernier jour du mois aux trois suivants) **disparaît après 1990** sur les futures S&P 500, et aussi sur le spot. Hypothèse des auteurs : les particuliers achètent désormais via des fonds plutôt qu'en direct. Les anomalies calendaires dépendent de la microstructure et peuvent changer sans prévenir, d'où un appel à la prudence sur les inférences hors échantillon.

### [4] Long Memory and Periodicity in Intraday Volatility of Stock Index Futures

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1460625
- **Actifs :** Indices (E-mini S&P 500, données horaires sur 24 h)
- **Plage horaire / Session :** 24 h : sessions Asie / Europe / US, saisonnalité horaire
- **Date :** 2009 | **Auteurs :** Eduardo Rossi, Dean Fantazzini | **Citations :** 2

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à chaque heure du cycle de 24 h, avec des pics à l'ouverture des marchés au comptant. **Qui subit la contrainte** : la volatilité suit l'arrivée des participants par fuseau horaire. **Effet sur les bougies** : l'amplitude des bougies horaires suit un profil saisonnier stable **et** une persistance de long terme. Il faut normaliser le range par heure avant de l'utiliser comme signal.

> **Résumé (abstract paraphrasé) :** Modélise la volatilité des rendements horaires de l'E-mini S&P 500 avec des EGARCH périodiques à intégration fractionnaire (FIPEGARCH, SFIPEGARCH). La volatilité horaire sur 24 h montre une forte saisonnalité et une persistance significative.

### [5] ❓⚠️ Intraday Share Price Volatility and Leveraged ETF Rebalancing

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2161057
- **Actifs :** Indices (actions et ETF US, ETF à levier)
- **Plage horaire / Session :** dernière heure / fin de séance
- **Date :** 2012 | **Auteurs :** Arthur Rodier, Edgar Haryanto, Pauline M. Shum, Walid Hejazi | **Citations :** 13

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la dernière heure de séance. **Qui subit la contrainte** : les ETF à levier et inverses doivent rééquilibrer leur exposition près de la clôture, **dans le sens du mouvement du jour** (achat si le marché monte, vente s'il baisse). **Effet sur les bougies** : la volatilité de fin de séance augmente avec l'ampleur du rendement du jour ; les bougies de fin de séance prolongent le mouvement. Signal OHLCV (rendement open→15h), cause non observable (encours des LETF) ⚠️.

> **Résumé :** *Résumé absent des API.* D'après ma connaissance du papier, la volatilité de fin de séance des titres détenus par les ETF à levier augmente les jours de fort mouvement, en lien avec la taille des rééquilibrages. **À vérifier sur le PDF.**

### [6] 🧪 Intraday Price Asymmetry and Next-Day Intraday Returns in the S&P 500

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6074846
- **Actifs :** Indices (SPY, plus de 20 ans)
- **Plage horaire / Session :** séance régulière (open, high, low du jour J) → séance de J+1 (open→close)
- **Date :** 2026 | **Auteurs :** Francesco Valenti | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : mesure à la fin de la séance J, effet sur la séance J+1. **Qui subit la contrainte** : les fournisseurs de liquidité qui ont absorbé un déséquilibre directionnel pendant J (pression de prix temporaire, gestion d'inventaire). **Effet sur les bougies** : asymétrie = (High−Open) vs (Open−Low). Une séance tirée vers le bas est suivie d'une séance J+1 plus forte, et inversement : **contrariant**. L'effet côté vente se concentre dans les périodes volatiles.

> **Résumé (abstract paraphrasé) :** Introduit une mesure d'asymétrie construite uniquement avec l'open, le high et le low. Sur SPY, elle prédit à contre-sens le rendement intraday du lendemain. Les expositions conditionnelles donnent des profils de rendement économiquement significatifs, surtout en période de stress. Étude volontairement descriptive, sans hypothèse sur le flux d'ordres.

### [7] 🧪 How Can Intraday Variance Concentration Signal Next-Day Crash Risk? Evidence from S&P 500 High-Frequency Data

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6975778
- **Actifs :** Indices (S&P 500, barres de 5 minutes, 2005-2020)
- **Plage horaire / Session :** séance entière (répartition de la variance entre les barres de 5 minutes) → J+1
- **Date :** 2026 | **Auteurs :** Pradyun Kalagara | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : variance cumulée sur la séance J, risque de krach en J+1. **Qui subit la contrainte** : un stress diffus (variance répartie sur toute la séance) signale un désengagement général, alors qu'un choc isolé (une seule bougie énorme) s'absorbe. **Effet sur les bougies** : à variance totale égale, les séances « larges partout » (indice de Herfindahl de la variance bas) précèdent plus souvent un krach que les séances avec une seule bougie explosive.

> **Résumé (abstract paraphrasé) :** Définit un indice de Herfindahl de la variance intraday. Sous une diffusion pure, son espérance ne dépend pas du niveau de volatilité. À variance réalisée donnée, son coefficient est négatif et significatif. Le modèle logistique hors échantillon a le meilleur score de Brier face à GARCH, HAR-RV et 7 autres modèles. Une stratégie de mise en cash fait passer le Sharpe de 0,25 à 0,58.

### [8] 🧪 Everyone Is a Genius After the Bar Closes: Pre-Registered Tests of Failed Weekly Auction Reversion in Liquid Futures Markets

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6728359
- **Actifs :** Indices (ES ; réplication NQ), Or (GC), T-Note
- **Plage horaire / Session :** profil de volume hebdomadaire (value area) ; exécution en barres de 5 minutes
- **Date :** 2026 | **Auteurs :** Dsmon Perry | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : quand le prix sort de la value area de la semaine précédente puis y revient. **Qui subit la contrainte** : les acheteurs ou vendeurs de breakout piégés hors de la zone acceptée, qui doivent couper leurs positions. **Effet sur les bougies** : séquence en 3 temps : retour dans la value area, retest de la borne, retour vers le POC. Elle n'est visible qu'en barres de 5 minutes ; en barres d'1 h, 72 % des setups sont écrasés dans une seule bougie.

> **Résumé (abstract paraphrasé) :** Backtest pré-enregistré sur ES 2015-2026, 1 017 trades : +0,06 R en moyenne (bootstrap p = 0,014). 🔴 La réplication NQ / or / T-Note ne rejette pas le null (Fisher p = 0,09). Deux résultats secondaires : un artefact de résolution des barres, et un désaccord sur 26 % des barres horaires entre deux approximations OHLC du delta acheteur/vendeur.

### [9] 🧪🔴 Stop Distance, Exit Methodology, and Signal Preservation in Intraday Value Area Breakouts: Evidence from E-mini S&P 500 Futures

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6350238
- **Actifs :** Indices (ES, données à la seconde, janv. 2025 - janv. 2026)
- **Plage horaire / Session :** profil de volume de la séance ; sortie de la value area pendant la séance
- **Date :** 2026 | **Auteurs :** Theo Howard | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : cassure de la value area de la séance précédente, suivie d'un pullback. **Qui subit la contrainte** : les vendeurs ou acheteurs dans la zone de valeur, si l'acceptation hors zone est réelle. Un pullback peu profond signale cette acceptation. **Effet sur les bougies** : la continuation brute n'a **pas d'edge** (−2,2 ticks, non significatif). Les pullbacks peu profonds battent les profonds de 4 ticks. Les stops sur prix détruisent de la valeur à toutes les distances testées.

> **Résumé (abstract paraphrasé) :** Formalise le « Setup 2 » de Market Profile (continuation après cassure de la value area) sur 6 284 événements. Pas de significativité sans filtre, et le résultat ne tient plus si l'on retire un mois de régime particulier. La profondeur du pullback est un prédicteur significatif (p < 0,001). Les 12 distances de stop testées dégradent toutes le résultat par rapport à une sortie à horizon fixe.

### [10] 🧪 Harvesting the Value Area: Auction Geometry as a Durable Intraday Edge in Nasdaq-100 Futures

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7546200 (autre version : abstract_id=7529379)
- **Actifs :** Indices (NQ / MNQ, 2 921 séances, environ 9,5 ans)
- **Plage horaire / Session :** séance régulière ; value area et POC de la séance
- **Date :** 2026 | **Auteurs :** Mansoor Alqaydi | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : quand le prix touche une borne de la value area. **Qui subit la contrainte** : les traders qui testent un prix « non accepté » (peu de volume) ; le rejet ramène le prix vers le prix le plus échangé (POC). **Effet sur les bougies** : rejet (mèche) sur la borne de la value area, puis rotation vers le POC. Environ 95 % du profit vient de cette géométrie, environ 5 % des filtres de flux d'ordres.

> **Résumé (abstract paraphrasé) :** Décrit un système automatisé fondé sur Market Profile. Trois stratégies réparées passent d'un profit factor de 0,57 à plus de 1,2. Le système est calibré par bootstrap journalier et confirmé en walk-forward. Un test de brouillage attribue environ 95 % du profit au rejet des bornes de la value area. Resserrer la limite de perte journalière fait passer la probabilité de ruine de 14 % à environ 1 %. Papier d'ingénierie : beaucoup de degrés de liberté.

### [11] 🧪 Intraday Microstructure Dynamics of E-mini S&P 500 Futures: Volatility Regimes, Liquidity Decay, and Long Memory in Realized Volatility

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6847024
- **Actifs :** Indices (ES, barres OHLCV d'1 minute, avr. 2024 - mai 2026)
- **Plage horaire / Session :** première demi-heure vs dernière demi-heure ; séance régulière
- **Date :** 2026 | **Auteurs :** Max Brown | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : l'activité se concentre à l'ouverture puis décroît. **Qui subit la contrainte** : la liquidité, maximale à l'ouverture (absorption de l'information de la nuit). **Effet sur les bougies** : le range moyen des barres passe de 4,78 à 2,69 points entre la première et la dernière demi-heure (profil en L). La volatilité réalisée est très persistante (autocorrélation d'ordre 1 = 0,71). Le range moyen des barres suffit presque à estimer la volatilité réalisée (r = 0,975).

> **Résumé (abstract paraphrasé) :** Quatre faits sur 529 séances : décroissance de la liquidité en L, quatre régimes de volatilité (dont le choc des tarifs d'avril 2025), mémoire longue de la volatilité réalisée, et range des barres comme statistique quasi suffisante. Conclusion : il faut conditionner les signaux sur l'expansion du range d'ouverture, le régime et la persistance.

### [12] 🧪 Measuring the Memory Structure of Intraday Returns: Evidence from E-mini S&P 500 Futures

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6809080
- **Actifs :** Indices (ES, barres d'1 minute, 514 séances de New York)
- **Plage horaire / Session :** séance de New York
- **Date :** 2026 | **Auteurs :** Max Brown | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : toute la séance, en 1 minute. **Qui subit la contrainte** : *non causal* : outil de mesure (Hurst, d fractionnaire, multifractalité). **Effet sur les bougies** : un Hurst mesuré d'environ 0,66 suggère une persistance des rendements à 1 minute. **Attention** : à 1 minute, ce Hurst est très sensible à la saisonnalité intraday et à la microstructure ; à vérifier avant d'y voir un edge de momentum.

> **Résumé (abstract paraphrasé) :** Boîte à outils (3 estimateurs de Hurst, GPH/ARFIMA, MFDFA, volatilité FIGARCH) codée en MQL5. Le Hurst combiné vaut environ 0,66 sur ES en 1 minute ; d'autres résultats portent sur la mémoire de la volatilité.

### [13] 🧪 ATR as State, Not Signal. Multiscale Forecasting of Extreme Intraday Risk in Equity Index Futures

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7558660
- **Actifs :** Indices (ES, NQ), Or (GC, en contrôle)
- **Plage horaire / Session :** état lent calculé à la clôture J-1 → amplitude intraday de J
- **Date :** 2026 | **Auteurs :** José Enrique Delgado | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : l'extension (clôture − SMA50) / ATR14 à la clôture J-1 conditionne la séance J. **Qui subit la contrainte** : un marché très étiré force le désengagement de positions déjà en profit ou en perte, ce qui augmente l'amplitude sans fixer la direction. **Effet sur les bougies** : une extension extrême prédit des **ranges plus larges et une volatilité réalisée plus forte**, pas un déplacement directionnel. À utiliser pour dimensionner la position, pas pour décider d'une entrée.

> **Résumé (abstract paraphrasé) :** La distance au SMA50 normalisée par l'ATR sert mieux d'état de risque lent que de signal directionnel. Combinée à un prédicteur rapide de volatilité réalisée, elle améliore LogLoss, Brier et AUC sur ES ; le motif d'interaction se retrouve sur NQ et sur l'or. Échantillon déclaré exploratoire (2017-2023 vus pendant le développement).

### [14] 🧪 The One-Minute Edge: Do Nasdaq Futures Lead QQQ? Evidence from a Single-Use Final Holdout

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7217599
- **Actifs :** Indices (MNQ → QQQ, 1 minute, 358 séances)
- **Plage horaire / Session :** séance régulière, horizon 1 minute
- **Date :** 2026 | **Auteurs :** Wenwen Jiang | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la minute suivante. **Qui subit la contrainte** : l'ETF, mis à jour par arbitrage après le future (où l'information arrive d'abord). **Effet sur les bougies** : la bougie 1 minute de MNQ prédit faiblement celle de QQQ (R² hors échantillon +0,19 %). 🔴 L'avantage **disparaît dès qu'on retire la dernière minute de retard** : il n'est donc pas exploitable après latence et frais.

> **Résumé (abstract paraphrasé) :** Sur un holdout final à usage unique (137 472 observations), 5 retards de MNQ ajoutent un R² hors échantillon significatif (p = 0,018). L'effet dépend entièrement du retard le plus récent ; rentabilité nette des frais non démontrée. Pas de preuve de causalité dans la découverte des prix.

### [15] ⚠️ Scheduled Macroeconomic Announcements and Intraday Volatility: Evidence from SPY and QQQ

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6631518
- **Actifs :** Indices (SPY, QQQ, barres de 5 minutes, 2020-2025)
- **Plage horaire / Session :** 8h30 ET (CPI, NFP, ventes au détail, PIB) ; 14h00 ET (FOMC) ; fenêtres de 30 minutes autour
- **Date :** 2026 | **Auteurs :** Anirudh Naveen | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : aux heures fixes des annonces. **Qui subit la contrainte** : tous les participants révisent leurs anticipations ; les teneurs de marché élargissent leurs fourchettes. **Effet sur les bougies** : la volatilité réalisée est multipliée par environ 2,5 dans les 30 minutes qui suivent (environ 3,6 à 4 fois pour le CPI). ⚠️ Il faut un **calendrier** des annonces (pas un flux de prix), mais pas la valeur de la surprise.

> **Résumé (abstract paraphrasé) :** Étude d'événements sur 630 annonces : la volatilité réalisée post-annonce est significativement plus élevée (t ≈ 16 à 19), surtout pour l'inflation. Un modèle de gradient boosting prédit l'amplitude (R² ≈ 0,3) ; les variables temporelles sont les plus informatives.

### [16] 🧪 Sampling Frequency and the Ranking of Range-Based Volatility Estimators: Evidence from U.S. Equity Indices and Spot Gold

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7489499
- **Actifs :** Indices (S&P 500, Nasdaq-100, Dow Jones), Or (spot)
- **Plage horaire / Session :** barres de 15, 30, 65 et 390 minutes
- **Date :** 2026 | **Auteurs :** Rehan Fazal | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : *non causal* : outil de mesure de volatilité en OHLC. **Qui subit la contrainte** : — **Effet sur les bougies** : en barres de 15 minutes, **Parkinson** (high-low) est l'estimateur le plus précis. En barre journalière, **Garman-Klass** l'emporte (significatif seulement sur l'or). Rogers-Satchell n'est jamais le meilleur. Utile pour normaliser les seuils de signaux.

> **Résumé (abstract paraphrasé) :** Compare Parkinson, Garman-Klass et Rogers-Satchell à la variance réalisée 5 minutes. Le classement dépend de la taille des barres. Garman-Klass appartient à une famille d'estimateurs sans biais, et le poids optimal sur le rendement open→close diminue quand les barres raccourcissent. Échantillon court (1 an), résultats préliminaires.

---

## B. Forex majeurs

### [17] 🔴 Intraday Technical Trading in the Foreign Exchange Market

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=189495
- **Actifs :** Forex (majeures)
- **Plage horaire / Session :** intraday, heures de trading réalistes
- **Date :** 1999 | **Auteurs :** Christopher J. Neely, Paul A. Weller | **Citations :** 44

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : toute la journée FX. **Qui subit la contrainte** : le trader technique, face aux frais et aux heures de trading réelles. **Effet sur les bougies** : les règles trouvent des **motifs intraday remarquablement stables**, mais trop petits pour couvrir les frais. Le motif existe, l'edge net non.

> **Résumé (abstract paraphrasé) :** Teste hors échantillon des règles intraday choisies par programmation génétique et par un modèle linéaire optimisé. Avec des frais réalistes et des horaires de trading réels, aucun rendement excédentaire : résultat compatible avec l'efficience, même si les règles détectent des régularités stables.

### [18] Private Information, Excessive Volatility and Intraday Empirical Regularities in the Spot Foreign Exchange Market

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=734083
- **Actifs :** Forex (spot, haute fréquence)
- **Plage horaire / Session :** profil intraday sur 24 h (volume, volatilité, nombre de transactions)
- **Date :** 2005 | **Auteurs :** Frank McGroarty, Stephen H. Thomas, Owain ap Gwilym | **Citations :** 2

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : aux heures de fort volume (chevauchement Londres / New York). **Qui subit la contrainte** : le prix, poussé par le **déséquilibre aléatoire** entre volumes acheteurs et vendeurs plutôt que par de l'information privée. **Effet sur les bougies** : la volatilité intraday suit le volume (plus d'activité, plus de déséquilibre aléatoire, des bougies plus grandes) ; une partie de cette volatilité est du bruit qui se retourne.

> **Résumé (abstract paraphrasé) :** Remet en cause le lien entre volatilité excessive du FX et information privée. Les données suggèrent que la variation aléatoire entre volumes acheteurs et vendeurs explique mieux les régularités intraday (dont la volatilité). Les auteurs proposent des relations théoriques entre variables de marché, testées en haute fréquence.

### [19] ⚠️ Exchange Rates, Equity Hedging, and the London 4pm Fix

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2019274
- **Actifs :** Forex (majeures)
- **Plage horaire / Session :** fixing de Londres 16h00 (WM/Reuters) ; fin de mois
- **Date :** 2012 | **Auteurs :** Michael T. Melvin, John Prins | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : autour de 16h00 Londres, surtout le **dernier jour ouvré du mois**. **Qui subit la contrainte** : les gérants d'actions mondiales qui rehaussent leur couverture de change au fixing (ordres passifs, à exécuter quel que soit le prix). Exemple : si les actions US ont surperformé dans le mois, les étrangers doivent vendre plus d'USD. **Effet sur les bougies** : intensité et volatilité maximales à 16h00, pression directionnelle **temporaire** puis retournement. ⚠️ Le sens du flux s'estime avec le rendement relatif des indices actions sur le mois. C'est calculable en OHLCV (SPX vs indices étrangers), mais ça demande des indices hors du périmètre.

> **Résumé (abstract paraphrasé) :** Première analyse académique du fixing de 16h. Les couvertures passives des portefeuilles actions s'y concentrent. Intensité et volatilité y sont maximales ; les flux de couverture prédisent le sens des mouvements temporaires, avec un impact fort mais transitoire en fin de mois.

### [20] 🧪 The First Hour: How Foreign Exchange Absorbs Its Daily Gap

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7135159
- **Actifs :** Forex (6 paires USD, barres horaires, 2014-2026)
- **Plage horaire / Session :** réouverture quotidienne (17h00 New York, rollover) : première barre horaire
- **Date :** 2026 | **Auteurs :** Marijan Tolušić | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la première heure après la réouverture quotidienne. **Qui subit la contrainte** : la liquidité, au plus bas pendant le rollover des dealers ; le prix de réouverture est une « enchère » mince qui s'écarte de sa valeur. **Effet sur les bougies** : le gap moyen est de 4,8 pips (contre 0,12 pip aux autres heures). **Le fader et tenir 1 h** donne un profit factor net de 2,63 (2019-2026), qui croît avec la taille du gap (3,16 à 2 pips, 4,69 à 5 pips). Tenir jusqu'à la clôture divise l'edge par deux. Les micro-gaps des autres heures perdent : la cause est l'enchère de liquidité, pas la frontière de bougie. 🔴 Avant 2019, l'effet est marginal.

> **Résumé (abstract paraphrasé) :** Documente où et à quelle vitesse le gap de réouverture FX est absorbé. Fader les gaps d'au moins 1 pip sur 1 h est rentable net de spread, sans année perdante de 2019 à 2026. Le Reality Check sur la grille de 18 règles rejette le null (p < 0,0005). La composante overnight se retourne dans l'enchère d'ouverture d'un marché décentralisé.

### [21] 🧪🔴 The Fibonacci Illusion: Confluence, Sequential Dependence, and the Failure of Golden-Pocket Continuation in Intraday FX

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7430898
- **Actifs :** Forex (GBPUSD, EURUSD, AUDUSD, USDJPY ; M15, H1, H4)
- **Plage horaire / Session :** intraday, sans session particulière
- **Date :** 2026 | **Auteurs :** Shepherd Mahadzva | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : après un pullback de 38,2 à 61,8 % suivi d'une bougie de momentum. **Qui subit la contrainte** : le trader particulier qui achète la « confirmation » de continuation. **Effet sur les bougies** : la continuation **ne marche pas**. Son contraire (fader) est retenu par le walk-forward dans 87,5 % des cas, mais l'edge est minuscule (+0,04 R, p = 0,10). La confluence avec les nombres ronds ou les moyennes mobiles n'aide pas.

> **Résumé (abstract paraphrasé) :** Protocole walk-forward avec frais réalistes et correction des tests multiples, sur données de broker jusqu'en septembre 2026. La lecture classique du « golden pocket » échoue. Le fade est cohérent mais pas significatif, même agrégé (1 885 trades). Les variantes avec confluence n'améliorent pas le signal.

---

## C. Pétrole

### [22] ⚠️ An Analysis of Intraday Market Response to Crude Oil Inventory Shocks

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3205211
- **Actifs :** Pétrole (futures WTI)
- **Plage horaire / Session :** mercredi 10h30 ET (rapport EIA) ; fenêtre 10h20-10h25 ; mardi soir (API)
- **Date :** 2018 | **Auteurs :** Richard Ziyuan Li, Hélyette Geman | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : 10h30 ET le mercredi (jeudi les semaines de jour férié), effets pendant environ 25 minutes. **Qui subit la contrainte** : les traders lents face à ceux qui reçoivent l'information plus tôt (accès rapide aux données). **Effet sur les bougies** : saut de prix opposé à la surprise de stocks, hausse de la volatilité et du volume, puis **retour rapide**. Un signal purement OHLCV : **suivre le mouvement de 10h20 à 10h25** bat la stratégie fondée sur la surprise. ⚠️ La surprise elle-même demande le consensus (externe) ; l'horaire et le pré-mouvement, non.

> **Résumé (abstract paraphrasé) :** Le rendement, la volatilité et le volume du WTI réagissent en quelques minutes à la surprise EIA, avec des effets d'environ 25 minutes puis un retournement. La dispersion des anticipations amplifie la réaction. Suivre le mouvement de 10h20-10h25 fait mieux que trader la surprise, ce qui suggère que certains acteurs ont l'information avant sa publication.

### [23] ❓ Closing Pressure, Predatory Trading, and the Negative Price of Oil

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4080137
- **Actifs :** Pétrole (futures WTI, échéance mai 2020)
- **Plage horaire / Session :** fenêtre de settlement (14h28-14h30 ET) ; dernier jour avant expiration
- **Date :** 2022 | **Auteurs :** Yiqing Ge, Wenjin Kang, Ke Tang, Liyan Yang | **Citations :** 2

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la fenêtre de settlement des derniers jours avant expiration. **Qui subit la contrainte** : les détenteurs longs contraints de solder avant la livraison (produits pour particuliers, fonds indiciels). Les traders informés vendent **avant et pendant** leur liquidation (trading prédateur). **Effet sur les bougies** : chute accélérée dans la fenêtre de settlement, avec des prix extrêmes (−37 $ le 20/04/2020), puis rebond après l'expiration. Plus généralement : **pression de clôture près des expirations quand des longs forcés doivent sortir.**

> **Résumé :** *Résumé absent des API.* D'après ma connaissance du papier : le prix négatif du WTI le 20 avril 2020 s'explique par la pression de clôture des longs forcés de sortir et par le trading prédateur de traders informés qui anticipaient cette liquidation. **À vérifier sur le PDF.**

### [24] Intraday Stylized Facts and the Shape of Volatility Build-Up in ICE Brent Crude Oil Futures

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6415578
- **Actifs :** Pétrole (Brent ICE, tick par tick, 2006-2025, 12 premières échéances)
- **Plage horaire / Session :** ouverture européenne ; annonces macro US ; annonces de stocks ; périodes de settlement
- **Date :** 2026 | **Auteurs :** Erik Haugom, Christian-Oliver Ewald, Xianwen Chen, Erik Smith-Meyer | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pics à l'ouverture européenne, aux annonces US de 8h30 ET, aux stocks (10h30 ET le mercredi) et au settlement. **Qui subit la contrainte** : la liquidité se concentre aux heures d'information ; les contrats proches portent plus de variance (effet Samuelson). **Effet sur les bougies** : **autocorrélation d'ordre 1 négative** des rendements (micro-retournement) ; la volatilité s'accumule vite après les ouvertures et accélère aux heures d'annonce. Le volume a un profil multimodal propre au pétrole.

> **Résumé (abstract paraphrasé) :** Documente les faits stylisés intraday du Brent sur près de 20 ans : saisonnalité multimodale du volume, autocorrélation négative à l'ordre 1, queues épaisses, clustering de volatilité sur 24 h. Les auteurs modélisent la volatilité réalisée comme un processus de croissance intra-journalier ; la vitesse d'accumulation varie selon l'heure et l'échéance.

---

## D. Or

### [25] Intraday Seasonality in Efficiency, Liquidity, Volatility and Volume: Platinum and Gold Futures in Tokyo and New York

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3021533
- **Actifs :** Or (futures TOCOM et COMEX), Platine
- **Plage horaire / Session :** sessions de jour de Tokyo, Londres et New York
- **Date :** 2017 (J. Commodity Markets 2018) | **Auteurs :** Kentaro Iwatsubo, Clinton Watkins, Tao Xu | **Citations :** 3

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : selon la session. **Qui subit la contrainte** : en session de Tokyo, le flux est dominé par des traders **non informés** ; en session de New York, par des traders **informés**. **Effet sur les bougies** : en session asiatique, les mouvements de l'or sont plus souvent du bruit qui se retourne ; en session de New York, ils intègrent de l'information et ont plus de chances de persister. Il faut donc conditionner le choix entre retournement et suivi de tendance à la session.

> **Résumé (abstract paraphrasé) :** Étudie la saisonnalité intraday de l'efficience informationnelle, de la volatilité, du volume et de la liquidité de l'or et du platine à Tokyo et New York. Tokyo est dominé par les non-informés ; New York mêle les deux, avec une prédominance informée en séance de jour. Un même sous-jacent a une microstructure différente selon la place et le fuseau horaire.

### [26] The Gold Fixing Game

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2462985
- **Actifs :** Or (spot)
- **Plage horaire / Session :** fixings de Londres 10h30 et 15h00 (heure de Londres)
- **Date :** 2014 | **Auteurs :** Dirk G. Baur | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : autour des deux fixings quotidiens. **Qui subit la contrainte** : les clients dont les ordres sont exécutés au fixing ; les banques participantes connaissent le déséquilibre avant les autres (asymétrie d'information, front-running). **Effet sur les bougies** : mouvement directionnel **avant et pendant** la fenêtre du fixing, dans le sens du déséquilibre des ordres. À tester en OHLCV : rendement de 10h00-10h30 et de 14h30-15h00 Londres.

> **Résumé (abstract paraphrasé) :** Jeu de rôle pédagogique sur tableur, avec simulations de Monte-Carlo, qui reproduit le fixing de Londres. Il montre comment l'asymétrie d'information, le partage d'information et le front-running créent des occasions de manipulation. Les auteurs plaident pour une réforme du design de marché plutôt qu'une détection a posteriori. Papier conceptuel, sans test empirique.

### [27] 🧪 A Regime-Filtered Intraday Trading Framework for Gold: Integrating VWAP Microstructure and EMA-Based Dynamic Exit Mechanisms

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6650958
- **Actifs :** Or (XAU/USD, barres de 15 minutes, 2024)
- **Plage horaire / Session :** VWAP de la séance
- **Date :** 2026 | **Auteurs :** Amaanullah Bhatti | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pullback sur l'EMA50, du bon côté du VWAP de la séance, dans le régime donné par l'EMA200. **Qui subit la contrainte** : les stops fixes, déclenchés par les mèches agressives de l'or (chasse aux stops). **Effet sur les bougies** : de longues mèches intrabar sur l'or ; un stop qui ne se déclenche **qu'à la clôture de bougie** évite ces sorties prématurées.

> **Résumé (abstract paraphrasé) :** Stratégie entièrement codifiée : régime EMA200, entrée sur rejet de l'EMA50 relativement au VWAP, stop suiveur EMA50 évalué à la clôture des bougies. Backtest simulé sur 247 trades en 2024 : PF 1,76, Sharpe 3,99. ⚠️ Un an seulement, en simulation : très fragile.

### [28] ❓🔴 Dangers of Relying on OHLC Prices: the Case of Overnight Drift in GDX ETF

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5139307
- **Actifs :** Or (GDX, ETF de mines d'or)
- **Plage horaire / Session :** session overnight (clôture → ouverture) ; prix d'ouverture
- **Date :** 2025 | **Auteurs :** Radovan Vojtko, Cyril Dujava | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : de la clôture à l'ouverture. **Qui subit la contrainte** : le backtesteur. Le prix « Open » des données OHLC n'est pas forcément un prix exécutable (premier print, enchère, cotation périmée). **Effet sur les bougies** : un « drift overnight » apparent sur GDX qui **disparaît** avec des prix d'ouverture réellement exécutables. Condition d'échec générale pour tout signal gap ou overnight bâti sur l'Open.

> **Résumé :** *Résumé absent des API.* D'après ma connaissance de ce papier Quantpedia : l'anomalie de drift overnight sur GDX vue dans les données OHLC est un artefact du prix d'ouverture. **À vérifier sur le PDF.**

---

## E. Multi-actifs

### [29] 🧪 The Invisible Segment of the Night Market: Predicting the Opening Gap Based on Post-Settlement Distortions

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6743561 (doublons SSRN dans OpenAlex : W7160774855, W7160771333)
- **Actifs :** Indices, Forex, Pétrole, Or (60 futures, plus crypto et obligations)
- **Plage horaire / Session :** settlement officiel → clôture réelle (post-settle) ; clôture → ouverture (gap)
- **Date :** 2026 | **Auteurs :** Raúl Gómez Sánchez | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : entre le prix de settlement et la clôture réelle, puis au gap d'ouverture. **Qui subit la contrainte** : les positions marquées au settlement ; après lui, la liquidité baisse et les écarts au settlement sont « hors référence ». **Effet sur les bougies** : décomposer l'overnight en deux segments (post-settle, puis gap) prédit mieux que de le traiter d'un bloc (rendement ajusté du risque environ 3 fois supérieur). Le meilleur prédicteur du segment post-settle est un indicateur de pression OHLC (propriétaire) calculé jusqu'au settlement.

> **Résumé (abstract paraphrasé) :** Compare deux modèles : l'un prédit le déplacement total du settlement à l'ouverture, l'autre décompose overnight = post-settle + gap. Le modèle décomposé a une performance ajustée du risque environ 3 fois supérieure. Indicateurs en partie propriétaires : réplication difficile.

---

## Papiers vus mais non retenus (notés dans le registre)

| ID OpenAlex | Titre | Raison |
|---|---|---|
| W7204657504 | Volatility as a Signal Switch: Regime-dependent Intraday Mean Reversion in NQ (Seeck 2026) | La bande dépend du **VXN**, une donnée externe |
| W7125912659, W7154159187 | Bhatti 2026, FX : retour à la moyenne (z-score) et VWAP + ADX | Cadres sans backtest |
| W7204463653 | BRSE Heikin-Ashi or 4H | Pas un mécanisme : optimisation d'indicateur |
| W7203600557 | Global Relay from NY close | Cible les marchés Asie et Europe |
| W2181235075 | Trading invariance E-mini | Descriptif de microstructure (taille des transactions), sans signal |
| W2228176416 | Mispricing Forex futures-cash | Base futures-spot, pas un signal intraday |
| W3161419109, W7204536008 | Athènes, B3 Brésil | Hors périmètre géographique |
| W2988626604, W3113347325, W4392776948, W4376481325 | Rebalancing d'indices, actions individuelles, Xetra, ETF à levier | Actions individuelles ou données externes |
| W3173345212, W4393021406, W4403190567 | EIA (version SSRN), Cross-Market Intraday TSMOM (2 versions) | Doublons de papiers déjà fournis |
| W2919785789, W2270014549, W4390484767, W4244239234, W4391453431 | Overnight declines (Abdi), métaux précieux intraday, liquidité pétrole, sauts, illiquidité | **Pas de résumé** : à retenter lors d'une prochaine session (statut `no_abstract`) |
