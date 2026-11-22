# Papiers SSRN : l'opening range breakout (ORB) sur indices US

*Session du 2026-11-22. Recherche par **OpenAlex** (source SSRN, `S4210172589`, recherche plein texte puis `title_and_abstract.search`), complétée par **l'API Crossref filtrée sur les DOI SSRN** (`prefix:10.2139`) quand OpenAlex renvoyait 429 : 57 requêtes, environ 2 000 candidats, 126 gardés par mots-clés, triés par titre puis par résumé. Résumés venant d'OpenAlex ou de Crossref, **paraphrasés en français**. Sections A à D : papiers nouveaux. **Section E : les 16 papiers ORB déjà fournis (2026-10-11 et 2026-10-13), remis au même format** à la demande de l'utilisateur (résumés repris de Crossref ou d'OpenAlex, nos résultats en regard).*

**Mots-clés** : opening range breakout, opening range, ORB (strategy, day trading, intraday), 5-minute / 15-minute / 30-minute opening range, first five minutes, first 15 minutes, first 30 minutes return, first hour return, stocks in play, breakout strategy intraday, volatility breakout, intraday breakout futures, E-mini S&P intraday breakout, initial balance, market profile, Crabel, range expansion, day trading S&P 500 / Nasdaq / QQQ / SPY, intraday trend day, morning vs afternoon return, opening volatility index futures, Donchian intraday, stop loss intraday breakout, leveraged ETF day trading, Zarattini / Aziz (auteurs).

**Légende** : 🔴 échec ou condition limite · ⚠️ le signal dépend d'une donnée non OHLCV (options, VIX, calendrier d'annonces) ou d'un marché hors périmètre · 🧪 papier SSRN récent d'auteur indépendant, non relu par des pairs

> **Avant tout test : l'ORB est au registre des échecs** ([wiki/Failed Ideas/ledger.md](wiki/Failed%20Ideas/ledger.md), ligne du 2026-10-12, sans condition de réouverture). Nos M3a / M3b / M3c ([PREREGISTRATION.md](PREREGISTRATION.md), [RESULTS.md](RESULTS.md) §M3) : 10 ORB sur 27 tués par les coûts, aucun ne survit. Relancer un ORB demande d'abord d'écrire dans le registre une condition de réouverture précise (par exemple un mécanisme absent de M3 : filtre d'événements, régime, sens de la 1ʳᵉ bougie), puis une fiche d'idée selon [PROTOCOLE.md](PROTOCOLE.md).

**Bilan honnête de la récolte** : la littérature SSRN sur l'ORB est **mince et déjà presque entièrement fournie** (16 papiers ORB ou proches déjà au registre, remis en section E). Cette récolte n'ajoute que **6 papiers** utiles, dont **une seule réplication indépendante sur indices US** ([1]) et **une adaptation de la bande de bruit à NQ** ([5]) qui touche directement notre expérience M2 en paper trading.

**Écartés** : Aziz-Zarattini, *Can Day Trading Really Be Profitable?* (SSRN 4898296, nouvelle mise en ligne du 4416622 fourni le 2026-10-11) ; Wang-Gangwar, *Optimizing Intraday Breakout Strategies on the NSE* (SSRN 5198458 : ORB 5/15/30 min sur une seule action indienne, Tata Motors, un an) ; Rogul, *Hybrid Systematic-Discretionary Channel Breakout for NQ* (SSRN 6469419 : sens choisi à la main) ; Hashimoto, *SMT Formal Verification… Opening Range Compression Gates* (SSRN 7684999 : vérification formelle de code, l'ORB n'y est qu'accessoire) ; Poudel, *Small-Cap Stock Trading Strategies for Retail Traders* (SSRN 5921742 : petites capitalisations, sans résumé) ; Magner-Sanhueza-Lavin, *Breakout trading pays only when…* (SSRN 6898600 : cassures de plus hauts sur 52 semaines, quotidien) ; Khan, *Turtle Trend Following* (SSRN 7573918 : quotidien) ; Spells, *Do Options Markets Anticipate Momentum Breakout Failures?* (SSRN 6456100 : quotidien, options).

---

## 0. Carte des ORB par durée du range (papiers déjà fournis + nos résultats)

Tous fournis le 2026-10-11 (revue de départ). **Leurs fiches complètes sont en section E**, numérotées [9] à [24]. Spécifications exactes des papiers lus en texte intégral : [PAPER_SPECS.md](PAPER_SPECS.md).

| Range | Papier (SSRN) | Actif, période | Résultat publié | Nos données |
|---|---|---|---|---|
| **5 min** | Zarattini-Aziz 2023 (4416622) | QQQ, TQQQ 2016-2023 | Alpha annualisé ≈ 33 % avec levier. ⚠️ **Ce n'est pas une cassure** : sens de la 1ʳᵉ bougie de 5 min, entrée à 9:35, stop à l'extrémité de la bougie, objectif 10R (PAPER_SPECS) | Registre : se reproduit sur NQ 2016-2022 (+0,96 net) puis s'effondre après publication (+0,17) |
| **5 min** | Zarattini-Barbon-Aziz 2024 (4729284) | > 7 000 actions US | Sharpe 2,81 en ne tradant que les « stocks in play » (volume relatif anormal) | M3c (proxy volume 1,5 ×) : améliore la médiane, rien ne survit hors échantillon |
| 5 / 15 / 30 / 60 min | Fetna 2026 (7428398) | 9 futures US, 2010-2026, grille pré-enregistrée de 225 cellules | 🔴 0 cellule sur 225 après 25 $ l'aller-retour ; **le 5 min est la pire fenêtre** ; la meilleure cellule échoue au test d'ancre aléatoire (expansion de volatilité, pas information de l'ouverture) | M3b (5 min) : confirme |
| plusieurs | Mesfin 2026 (6709401) | MNQ 2021-2025, barres 5 min | 🔴 ORB et 13 autres familles : avantage brut 0,07 à 1,5 point contre 2 points de coût | — |
| **30 min** | Subhani 2026 (7589980) | QQQ, SPY, 17 instruments, 2018-2026 | +0,44R par trade hors échantillon sur QQQ, **seulement les vendredis sans annonce** (NFP, CPI, FOMC, résultats des méga-capitalisations exclus) ; DSR 0,78 QQQ, 0,42 SPY | Non testé (filtre absent de M3) |
| **30 min** | — | NQ | — | M3a : +0,06 en IS, +0,95 en OOS (régime 2023+) |
| 1 à 5 min (optimisé) | Tsai et al. 2019 (IEEE) | futures d'indices | fenêtre de sondage optimisée en échantillon | non répliqué |
| après cassure | Pineda 2026 (6745958) | QQQ 2017-2024 | descriptif : le délai avant le retest du niveau cassé est la variable la plus liée à l'issue | — |
| inverse | Ladia 2026 (7124578) | E-mini Dow, depuis 2023 | 🔴 pour l'ORB : c'est le **reversal** de l'ouverture qui marche depuis l'essor des 0DTE | cohérent avec le fade de gap post-0DTE (en paper trading) |
| plusieurs | Wijesinghe 2026 (6977700) | S&P 500 5 min 2024-2026 | 🔴 ORB sans avantage significatif (DSR ≈ 0) | — |

---

## A. ORB sur indices US : ce qui est nouveau

### [1] « Can Day Trading Really Be Profitable? » : a Replication Study

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5325376
- **Actifs :** QQQ et TQQQ (plus d'autres titres en extension), 2016-2023
- **Plage horaire / Session :** ouverture du cash US, **1ʳᵉ bougie de 5 minutes** (9:30-9:35 ET), sortie au plus tard à la clôture de 16:00
- **Date :** 2025 | **Auteurs :** Steve Demirev | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : les 5 premières minutes de la séance cash. **Qui subit la contrainte** : le papier ne propose pas de mécanisme ; dans l'original, le déséquilibre d'ordres accumulé pendant la nuit se résorbe à l'ouverture et fixe la direction de la journée. **Effet sur les bougies** : la direction de la 1ʳᵉ bougie de 5 minutes se prolonge assez souvent sur la journée pour qu'un objectif lointain (10R) paye les nombreux petits stops.

> **Résumé (abstract paraphrasé) :** Réplication indépendante de Zarattini-Aziz (2023) sur des données 5 minutes d'Interactive Brokers et des données publiques, avec code et données mis à disposition. Les résultats d'origine se retrouvent sur QQQ (rendement cumulé d'environ 670 %, alpha annualisé d'environ 33 %, bêta non significatif). L'auteur ajoute une variante sans plafond de levier et une version sur TQQQ, puis optimise le stop et la sortie (ce qui gonfle fortement le rendement). **Sur d'autres titres que QQQ et TQQQ, la règle ne surperforme pas de façon régulière** : l'effet semble propre à l'actif.
>
> **Pour nous :** confirme que la règle publiée se reproduit **sur la période d'origine** (comme chez nous sur NQ 2016-2022), mais n'apporte **rien hors échantillon** : même période 2016-2023, pas de coûts de futures, et l'optimisation du stop est un ajustement après coup. Le point utile est l'échec sur les autres titres, qui va dans le sens du registre. 🔴 Aucune donnée après 2023, donc rien sur l'effondrement post-publication que nous avons mesuré.

### [2] 🚫 Regime-Conditional Alpha in SPY 0DTE Opening Range Breakout Strategies: A Filtering and Strike Selection Framework

> 🚫 **Retiré de SSRN** (constaté par l'utilisateur le 2026-11-22) : le lien ne mène plus au papier. OpenAlex et Crossref gardent la notice et le résumé ci-dessous, mais le texte n'est plus disponible. **À ne pas citer comme source.**

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6355218 (retiré)
- **Actifs :** SPY, via des **spreads verticaux d'options 0DTE** (2022-2025)
- **Plage horaire / Session :** ouverture du cash US ; la cassure du range d'ouverture déclenche l'achat d'un spread qui expire le jour même
- **Date :** 2026 | **Auteurs :** Justin Chuk | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : après la formation du range d'ouverture, les jours retenus par le filtre. **Qui subit la contrainte** : non identifié ; l'avantage dépend du régime de volatilité et de l'absence d'annonce macro. **Effet sur les bougies** : taux de réussite d'environ 47 % sans filtre, porté à environ 65 % avec trois filtres (lundi, mercredi, vendredi ; VIX entre 15 et 25 ; pas d'annonce macro).

> **Résumé (abstract paraphrasé) :** Étude **par simulation Monte-Carlo calibrée** sur des paramètres tirés de la littérature, sur 756 jours possibles (2022-2025) dont 214 trades après filtres. Avec des sorties fixes à 25 % / 50 %, le taux de réussite d'équilibre est de 66,7 % : le taux filtré observé (65,4 %, intervalle de Wilson 58,8-71,5 %) est **au bord de la rentabilité** et très sensible au slippage. L'apport annoncé est le choix du strike : la distance entre le niveau de cassure et le strike change le coût et le point mort, et un strike long placé à environ 1-2 $ de la cassure maximise l'espérance simulée.
>
> **Pour nous :** 🔴🧪⚠️ trois réserves fortes : (1) **simulation, pas backtest sur prix réels** ; (2) filtre VIX et options 0DTE hors de notre périmètre OHLCV ; (3) même avec les filtres, l'avantage est nul à l'intervalle près. Seule idée réutilisable : le filtre « pas d'annonce macro », qui rejoint Subhani (7589980) et notre règle des annonces côté FTMO.

### [3] Day Trading: Adapting to Change

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6833239
- **Actifs :** E-mini S&P 500 (ES)
- **Plage horaire / Session :** séance cash US, d'octobre à décembre (une seule année)
- **Date :** 2026 | **Auteurs :** Asher Levine | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : séances de forte volatilité. **Qui subit la contrainte** : non identifié. **Effet sur les bougies** : sur un trimestre de paper trading discrétionnaire, l'ORB gagne plus souvent (75 %) que les autres modèles de continuation (concepts « ICT »).

> **Résumé (abstract paraphrasé) :** L'auteur compare plusieurs stratégies de momentum à court terme, dont l'ORB, en **paper trading sur TradingView** pendant trois mois sur ES. Taux de réussite global de 53 %, ORB à 75 %, différence significative au seuil de 5 % de justesse (z = 1,68, p = 0,047, test unilatéral). Conclusion : les stratégies structurées tiennent en marché volatil avec une gestion du risque stricte.
>
> **Pour nous :** 🔴🧪 anecdotique : un trimestre, exécution manuelle, taux de réussite sans espérance en R, pas de coûts. À ne pas compter comme preuve ; noté pour que personne ne le redonne.

### [4] An Investigation of Simple Intraday Trading Strategies

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2488539
- **Actifs :** futures S&P 500
- **Plage horaire / Session :** séance US, stratégies intraday publiées par des praticiens
- **Date :** 2014 | **Auteurs :** Chrilly Donninger | **Citations :** 2

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : toute la séance, selon le régime de marché. **Qui subit la contrainte** : non identifié ; l'auteur classe les régimes par la **structure par terme de la volatilité implicite** (IVTS). **Effet sur les bougies** : les règles simples ne fonctionnent que dans certains régimes.

> **Résumé (abstract paraphrasé) :** Document de travail qui reprend plusieurs stratégies intraday simples publiées pour les futures S&P 500. Conclusion générale : **elles ne marchent pas comme annoncé** avec des hypothèses d'exécution réalistes. Restreindre les règles à un régime (via l'IVTS) aide ; la meilleure est un jeu de règles d'un trader de fonds. Il reste difficile de bâtir une stratégie intraday simple et attractive.
>
> **Pour nous :** ⚠️ le filtre de régime repose sur la volatilité implicite (hors OHLCV). Utile comme précédent ancien (2014) du même constat que Fetna, Mesfin et notre M3 : les règles d'ouverture publiées meurent sous des coûts réalistes.

---

## B. Le cousin de l'ORB : cassure d'une bande de bruit autour de l'ouverture

### [5] Noise-band Intraday Momentum in Nasdaq-100 Futures

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7609644
- **Actifs :** futures Nasdaq-100 (NQ), un micro-contrat, 2020 → juillet 2026
- **Plage horaire / Session :** séance cash US ; entrée à la sortie d'une « zone de bruit » centrée sur l'ouverture, stop suiveur
- **Date :** 2026 | **Auteurs :** Justin Chuk | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : quand le prix quitte la bande de bruit habituelle autour de l'ouverture (mouvement moyen des jours précédents à la même heure). **Qui subit la contrainte** : dans Zarattini-Aziz-Barbon (2024), les couvertures des teneurs de marché en gamma négatif et les flux de suivi de tendance, qui prolongent un mouvement une fois hors du bruit normal. **Effet sur les bougies** : continuation dans le sens de la sortie de bande jusqu'au stop suiveur ou à la clôture.

> **Résumé (abstract paraphrasé) :** Adaptation de la stratégie « Beat the Market » (bande de bruit sur SPY) à NQ, à taille fixe d'un micro-contrat et sous des contraintes d'exécution automatique par webhook. Sur données 1 minute 2020-2026 : environ +10 $ par jour de bourse net de coûts (intervalle bootstrap par blocs de jours à 95 % : +3 à +17 $), Sharpe quotidien 1,14, positif chaque année civile (deux de justesse). L'auteur chiffre la perte à chaque étape entre la règle publiée et la règle exécutable, audite le stop suiveur contre le biais d'anticipation, et montre qu'**un point d'indice de slippage sur les stops retire 22 % de l'avantage**. La règle est **l'une des deux survivantes parmi 144 tests pré-enregistrés** sur la même archive ; tout est en échantillon, aucun contrat réel n'a été tradé ; seuils du test forward pré-enregistrés.
>
> **Pour nous :** directement lié à [wiki/experiments/m2-bande-bruit-nq.md](wiki/experiments/m2-bande-bruit-nq.md) (M2 sur NQ : +1,15 / +1,13 net chez nous, rejeté par le DSR, en paper trading). Résultat indépendant **du même ordre** sur NQ, avec la même faiblesse : 2 survivants sur 144 essais, tout en échantillon. Deux choses à reprendre sans recalcul : (a) la sensibilité au slippage des stops (22 % de l'avantage par point) pour dimensionner le suivi du paper trading ; (b) leur décomposition « règle publiée → règle exécutable ». ⚠️ Ce n'est pas un ORB au sens strict : la bande de bruit **remplace** le range d'ouverture.

### [6] Improvements to Intraday Momentum Strategies Using Parameter Optimization and Different Exit Strategies

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5095349
- **Actifs :** non précisé (résumé introuvable)
- **Plage horaire / Session :** séance US (d'après le titre, suite de la stratégie de momentum intraday de Zarattini et al.)
- **Date :** 2025 | **Auteurs :** Ákos Maróy | **Citations :** 0

> **Résumé :** introuvable sur OpenAlex et Crossref (statut `no_abstract` au registre, peut être retenté). Le titre annonce une **optimisation des paramètres** et des **sorties alternatives** : à lire avec prudence, une optimisation en échantillon est précisément ce que le protocole compte comme essais.

---

## C. Contre-exemple hors indices : ORB 15 minutes à l'ouverture de New York

### [7] Historical Performance Evaluation of a Mechanical 15-Minute Opening Range Breakout Strategy in the XAU/USD Market During the New York Session (2016-2025)

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7705242
- **Actifs :** or spot (XAU/USD), données 1 minute bid et ask de Dukascopy, 2016-2025
- **Plage horaire / Session :** range = **bougie 9:30-9:45 NY** ; entrée à la clôture d'une bougie de 15 minutes hors du range, à l'open de la minute suivante
- **Date :** 2026 | **Auteurs :** Ali Eman | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : après les 15 premières minutes de la séance actions US, alors que l'or se traite 23 h sur 24. **Qui subit la contrainte** : aucune ; pour l'or, 9:30 NY n'est pas une ouverture (pas d'accumulation d'ordres pendant une fermeture). **Effet sur les bougies** : aucune continuation exploitable.

> **Résumé (abstract paraphrasé) :** Règle entièrement mécanique : stop à l'autre extrémité du range, objectif à 2,3R, exécution sur bid et ask séparés. 2 457 trades en dix ans, 29,5 % de réussite, espérance nette d'environ −0,03R par trade (cumul d'environ −73R), **non significativement différente de zéro** (t ≈ −0,98, p ≈ 0,33 ; intervalle à 95 % de −0,09R à +0,03R).
>
> **Pour nous :** ⚠️ hors indices, mais c'est un bon **test placebo** de l'ORB 15 min : à la même heure, sur un actif sans vraie ouverture, rien. Cohérent avec l'idée que l'avantage de l'ORB, s'il existe, vient de l'ouverture d'un marché fermé (indices cash) et non de l'heure elle-même. 🔴 Ne contredit pas Subhani (or positif certains vendredis) car le filtre n'est pas le même.

---

## D. Méthode

### [8] A Machine-Verified Claims Ledger for Trading-Strategy Research

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7428478
- **Actifs :** programme de recherche sur futures de 18 mois (dont l'étude ORB à 225 cellules du même auteur, 7428398)
- **Plage horaire / Session :** sans objet
- **Date :** 2026 | **Auteurs :** Mulham Fetna | **Citations :** 0

> **Mécanisme causal intraday :** sans objet (papier de méthode).

> **Résumé (abstract paraphrasé) :** Chaque chiffre publié est un « objet de revendication » relié aux fichiers qui l'ont produit et recalculé automatiquement ; chacun exige trois vérifications indépendantes (dont un test de falsification) et un angle mort déclaré. L'intégration continue bloque toute modification qui casse une revendication ; un auto-test rejoue cinq vrais défauts passés et exige qu'ils soient rejetés pour la bonne raison. Autour : pré-enregistrement avec avenants datés, analyse de puissance obligatoire avant un verdict négatif, contrôles bêtes avant un positif, coûts stressés en tête, et suivi en réel hors échantillon par construction, avec paramètres figés par empreinte avant que les données d'évaluation existent.
>
> **Pour nous :** proche de notre [PROTOCOLE.md](PROTOCOLE.md) et de la règle d'immuabilité du wiki. Deux idées absentes chez nous : un **auto-test qui rejoue d'anciens bugs** (par exemple la détection des rolls ou le décalage horaire HistData) et l'**empreinte des paramètres** avant l'ouverture d'une réserve. Aucun calcul de rendement.

---

## E. Les papiers ORB déjà fournis (rappel complet, fournis le 2026-10-11 sauf [24])

### E.1 Origine et premiers tests académiques

### [9] The Profitability of Technical Stock Trading has Moved from Daily to Intraday Data

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1714980
- **Actifs :** S&P 500 spot et futures
- **Plage horaire / Session :** barres de 30 minutes sur la séance, 1983-2006 (comparées aux barres journalières depuis 1960)
- **Date :** 2010 | **Auteurs :** Stephan Schulmeister | **Citations :** 10

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'intérieur de la séance, sur des tendances de quelques heures. **Qui subit la contrainte** : les traders qui réagissent en retard à l'information (effets de momentum et de retournement). **Effet sur les bougies** : les tendances exploitables ont quitté les données journalières dans les années 1990 et se sont déplacées vers les barres de 30 minutes, puis vers des fréquences plus élevées.

> **Résumé (abstract paraphrasé) :** 2 580 règles techniques courantes (suivi de tendance et contrarien). En journalier, la rentabilité baisse depuis 1960 et devient nulle dans les années 1990. En barres de 30 minutes, les mêmes règles rapportent en moyenne 8,8 % par an brut sur 1983-2000, stable sur six sous-périodes ; les 25 meilleures d'une sous-période battent la moyenne sur la suivante. Hors échantillon (2001-2006), les résultats sont nettement moins bons : marché plus efficient, ou tendances passées à plus haute fréquence.
>
> **Pour nous :** 🔴 le précédent historique de toute la famille : un avantage intraday brut qui se dégrade avec le temps, comme l'ORB de Zarattini après 2023. Aucun coût dans les chiffres.

### [10] Assessing the profitability of intraday opening range breakout strategies

- **Lien :** https://doi.org/10.1016/j.frl.2012.09.001 (Finance Research Letters, pas SSRN)
- **Actifs :** futures pétrole brut
- **Plage horaire / Session :** range d'ouverture de la séance
- **Date :** 2012 | **Auteurs :** Ulf Holmberg, Carl Lönnbark, Christian Lundström | **Citations :** 51

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : après la formation du range d'ouverture. **Qui subit la contrainte** : non précisé (résumé indisponible). **Effet sur les bougies** : d'après la revue de départ, rendements conditionnels à la cassure supérieurs aux rendements non conditionnels (**non vérifié**).

> **Résumé :** introuvable sur OpenAlex et Crossref. Premier test académique publié de l'ORB, sur le pétrole.
>
> **Pour nous :** ⚠️ hors indices US. Référence fondatrice à citer, mais sans chiffre vérifiable ici.

### [11] Intraday Momentum: Day trading on the gold futures market using Opening Range Breakouts and GARCH

- **Lien :** DiVA, Université d'Umeå (mémoire, pas SSRN ; OpenAlex W1456285475)
- **Actifs :** futures or
- **Plage horaire / Session :** range d'ouverture, seuil de cassure ajusté par un GARCH
- **Date :** 2015 | **Auteurs :** Tobias Sönnert | **Citations :** 0

> **Mécanisme causal intraday :** seuil de cassure proportionnel à la volatilité prévue (GARCH) ; résumé indisponible.

> **Résumé :** titre seul. ⚠️ Hors indices, mémoire non relu par des pairs.

### [12] Assessing the Profitability of Timely Opening Range Breakout on Index Futures Markets

- **Lien :** https://doi.org/10.1109/access.2019.2899177 (IEEE Access, pas SSRN)
- **Actifs :** futures DJIA, S&P 500, Nasdaq, HSI, TAIEX, 2003-2013, données 1 minute
- **Plage horaire / Session :** **ouverture du marché cash** (9:30 ET pour les US), pas celle du future
- **Date :** 2019 | **Auteurs :** Yi-Cheng Tsai, Mu-En Wu, Jia-Hao Syu, Chin-Laung Lei, Chung-Shu Wu, Jan-Ming Ho, Chuan-Ju Wang | **Citations :** 23

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le volume et la variation des rendements du future culminent à l'ouverture et à la clôture **du marché cash sous-jacent**. **Qui subit la contrainte** : sur le TAIEX, les signaux vont dans le sens des **institutionnels, surtout étrangers**, qui agissent à l'ouverture du cash. **Effet sur les bougies** : une cassure du range calé sur l'ouverture cash se prolonge.

> **Résumé (abstract paraphrasé) :** En alignant les heures actives du future sur celles du marché cash, l'ORB « opportun » rapporte plus de 8 % par an avec des p-valeurs sous 3 % sur les cinq marchés (meilleur : TAIEX, environ 20 % par an). La durée de sondage optimale est **courte aux US** et plus longue en Asie. Sur les données de transactions du TAIEX, les signaux suivent les institutionnels.
>
> **Pour nous :** c'est la raison pour laquelle notre M3 cale le range sur 9:30 ET. ⚠️ La durée de sondage est **optimisée en échantillon** (1 à 5 minutes aux US) et la période s'arrête en 2013 : non répliqué (PAPER_SPECS).

### [13] Effectiveness of filter trading as an intraday trading rule

- **Lien :** https://doi.org/10.1108/sef-09-2018-0294 (Studies in Economics and Finance, pas SSRN)
- **Actifs :** futures Hang Seng (HSIF), tick par tick
- **Plage horaire / Session :** intraday, aucune position gardée la nuit
- **Date :** 2019 | **Auteurs :** Ling Xin, Kin Lam, Philip L. H. Yu | **Citations :** 11

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : les jours dont la volatilité réalisée convient à la taille du filtre. **Qui subit la contrainte** : non identifié (cadre de l'hypothèse des marchés adaptatifs). **Effet sur les bougies** : un filtre de cassure gagne selon la volatilité du jour ; la volatilité mesurée par **l'amplitude (plus haut − plus bas)** prédit mieux le gain que celle mesurée par les rendements.

> **Résumé (abstract paraphrasé) :** Règle de filtre (entrer après un mouvement de x % depuis un extrême) appliquée en intraday. Un modèle de spline relie le gain à la volatilité réalisée : la volatilité fondée sur l'amplitude est le meilleur prédicteur, et la taille optimale du filtre dépend de la volatilité réalisée.
>
> **Pour nous :** ⚠️ hors indices US, mais l'idée est OHLCV pure : **dimensionner le seuil de cassure par l'ATR ou l'amplitude**, plutôt que par le range d'ouverture fixe. Cohérent avec Fetna [20] : ce qui marche ressemble à de l'expansion de volatilité.

### E.2 Zarattini et coauteurs : les résultats qui ont lancé la mode

### [14] Can Day Trading Really Be Profitable?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416622
- **Actifs :** QQQ, TQQQ, 2016-2023
- **Plage horaire / Session :** **1ʳᵉ bougie de 5 minutes** (9:30-9:35 ET), sortie au plus tard à 16:00
- **Date :** 2023 | **Auteurs :** Carlo Zarattini, Andrew Aziz | **Citations :** 5

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : les 5 premières minutes. **Qui subit la contrainte** : non formalisé ; le déséquilibre accumulé pendant la fermeture se résorbe à l'ouverture et donne la direction du jour. **Effet sur les bougies** : la couleur de la 1ʳᵉ bougie de 5 minutes se prolonge assez souvent pour qu'un objectif de 10R paye les nombreux petits stops.

> **Résumé (abstract paraphrasé) :** Sur 2016-2023 (deux marchés baissiers), un ORB appliqué à QQQ bat nettement la détention passive : alpha annualisé de 33 % net de commissions, avec levier. Les plafonds de levier des courtiers limitant le gain, les auteurs passent par TQQQ (ETF à levier 3) : environ +1 480 % sur la période contre +169 % pour QQQ.
>
> **Pour nous :** ⚠️ **ce n'est pas une cassure** (PAPER_SPECS) : long si la 1ʳᵉ bougie est verte, short si rouge, entrée à 9:35, stop à l'extrémité de la bougie, objectif 10R, risque 1 % par trade, levier ≤ 4, pas de slippage. Notre M3b testait une cassure du range de 5 minutes, donc pas cette règle. Registre : se reproduit sur NQ 2016-2022 (+0,96 net), puis +0,17 après publication. Réplication indépendante : [1].

### [15] A Profitable Day Trading Strategy For The U.S. Equity Market

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4729284
- **Actifs :** plus de 7 000 actions US, 2016-2023
- **Plage horaire / Session :** ORB 5 minutes surtout, comparé à 15, 30 et 60 minutes
- **Date :** 2024 | **Auteurs :** Carlo Zarattini, Andrea Barbon, Andrew Aziz | **Citations :** 5

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : les jours où un titre est « in play ». **Qui subit la contrainte** : les investisseurs qui doivent réagir à une **nouvelle fondamentale propre à l'entreprise** ; le volume anormal de l'ouverture signale leur flux. **Effet sur les bougies** : sur ces titres, la cassure du range d'ouverture se prolonge ; sans volume anormal, beaucoup moins.

> **Résumé (abstract paraphrasé) :** Limiter le day trading aux « Stocks in Play » (activité anormalement élevée ce jour-là, souvent à cause d'une nouvelle) améliore nettement l'ORB, même après coûts. Un portefeuille des 20 premiers Stocks in Play fait plus de 1 600 % net sur la période, Sharpe 2,81, alpha annualisé de 36 %, contre 198 % pour le S&P 500. Comparaison des durées de range (5, 15, 30, 60 min) et statistiques par titre.
>
> **Pour nous :** ⚠️ l'effet repose sur la **sélection en coupe** parmi des milliers d'actions, impossible sur un seul future d'indice. Notre transposition (M3c : volume du range > 1,5 × la moyenne de 14 jours) améliore la médiane mais ne survit pas hors échantillon.

### [16] Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172
- **Actifs :** SPY, 2007 → début 2024
- **Plage horaire / Session :** toute la séance, décisions toutes les 30 minutes (HH:00 et HH:30), clôture à 16:00
- **Date :** 2024 | **Auteurs :** Carlo Zarattini, Andrew Aziz, Andrea Barbon | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : dès que le prix sort de la « zone de bruit » normale pour cette heure (mouvement moyen des 14 jours précédents depuis l'ouverture). **Qui subit la contrainte** : les teneurs de marché selon leur **déséquilibre de gamma**, testé par les auteurs comme prédicteur de la rentabilité. **Effet sur les bougies** : une sortie de bande signale un déséquilibre offre/demande anormal qui se prolonge ; stop suiveur au VWAP ou à la bande.

> **Résumé (abstract paraphrasé) :** Au lieu d'attendre la dernière demi-heure comme la littérature académique, la règle suit la tendance dès qu'un déséquilibre anormal apparaît, avec un stop suiveur dynamique. De 2007 à début 2024 : +1 985 % net de coûts, 19,6 % par an, Sharpe 1,33. Tests par régime de volatilité, par déséquilibre de gamma des teneurs de marché, par jour de la semaine, et sensibilité aux commissions et au slippage.
>
> **Pour nous :** c'est notre **M2** : NQ +1,15 / +1,13 net, rejeté par le DSR, en paper trading ([wiki/experiments/m2-bande-bruit-nq.md](wiki/experiments/m2-bande-bruit-nq.md)) ; sur ES, perte depuis la publication. Fusion ORB et momentum : la bande joue le rôle du range d'ouverture, mais elle s'élargit avec l'heure. Adaptation indépendante à NQ : [5].

### E.3 Raffinements récents sur QQQ / SPY

### [17] Anatomy of the Retest in the QQQ Opening Range Breakout

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6745958
- **Actifs :** QQQ, données 1 minute, 2017-2024
- **Plage horaire / Session :** range d'ouverture, puis les minutes qui suivent la cassure
- **Date :** 2026 | **Auteurs :** Mario Pineda | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : entre la cassure et le retour sur le niveau cassé. **Qui subit la contrainte** : inconnu, l'auteur l'écrit lui-même. **Effet sur les bougies** : un range large précède un mouvement ample ; une part régulière des cassures revient tester le niveau ; le **délai avant ce retest** est la variable la plus liée à l'issue ; une grande excursion avant le retest va avec **moins** de continuation.

> **Résumé (abstract paraphrasé) :** Étude exploratoire et descriptive, sans prétention de causalité ni d'exploitabilité. La séquence est découpée en quatre niveaux (range, cassure, retest, issue) et les associations sont mesurées à chaque niveau, avec des définitions opérationnelles précises. L'auteur invite à répliquer.
>
> **Pour nous :** 🧪 aucune règle tradable ni coût. Idée OHLCV utilisable plus tard comme filtre (« entrer au retest, pas à la cassure »), qui serait un nouvel essai à compter.

### [18] Opening-Range Breakouts on Event-Free Fridays: A Search-Aware Replication and Stress Test

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7589980
- **Actifs :** QQQ, SPY et 15 autres instruments (secteurs, métaux…), données 1 minute, 2018-2026
- **Plage horaire / Session :** **range de 30 minutes** (9:30-10:00 ET), seulement les **vendredis sans annonce** (NFP, CPI, FOMC, semaines de résultats des méga-capitalisations exclus)
- **Date :** 2026 | **Auteurs :** Shahmeer Ahmed Subhani | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le vendredi, en l'absence d'annonce programmée. **Qui subit la contrainte** : non identifié ; hypothèse implicite : sans nouvelle, la direction prise à l'ouverture n'est pas contredite par un choc d'information en séance. **Effet sur les bougies** : la cassure du range de 30 minutes se prolonge, surtout sur la tech, la croissance et les métaux ; rien sur les secteurs défensifs et sensibles aux taux.

> **Résumé (abstract paraphrasé) :** Protocole de validation complet : registre pré-enregistré de toutes les configurations essayées, Sharpe dégonflé selon ce nombre, walk-forward à paramètres figés, deux tests de permutation, coûts mesurés sur une exécution réelle. Hors échantillon : +0,44R par trade sur QQQ (facteur de profit 2,77) et +0,31R sur SPY (1,95), les deux sous p < 0,002 au bootstrap. Avec 57 configurations essayées, DSR 0,78 (QQQ) et 0,42 (SPY). 9 instruments sur 17 passent les deux tests nuls. Le flux ORB est presque décorrélé de l'indice (ρ ≈ −0,03) : un mélange 50/50 avec la détention passive améliore le Sharpe de QQQ (de 1,13 et 0,88 à 1,43).
>
> **Pour nous :** 🧪 **la piste ORB la plus sérieuse non testée chez nous** : même protocole que le nôtre (registre, DSR, réserve). ⚠️ Le filtre suppose un calendrier d'annonces (nous l'avons déjà, voir `build_calendar_macro.py`), pas de donnée de marché externe. Un vendredi par semaine donne environ 50 trades par an : puissance faible, à calculer avant toute grille.

### [19] Opening-Range Reversal in Dow Jones Futures: Evidence Consistent with 0DTE Hedging Pressure

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7124578
- **Actifs :** E-mini Dow (YM), janvier 2023 → mars 2026 (194 trades), échantillon reconstruit avant 2023 (115 trades)
- **Plage horaire / Session :** ouverture du cash US, premières fenêtres d'entrée
- **Date :** 2026 | **Auteurs :** Lance Ladia | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : dans les premières fenêtres après l'ouverture, depuis 2023. **Qui subit la contrainte** : probablement les **teneurs de marché d'options 0DTE**, dont les couvertures à l'ouverture créent un flux temporaire qui se retourne (l'auteur reste prudent). **Effet sur les bougies** : le mouvement d'ouverture se **retourne** (côté short) au lieu de se prolonger.

> **Résumé (abstract paraphrasé) :** Avec un gain et une perte symétriques (1:1), le retournement côté short gagne 59,8 % du temps (espérance brute ≈ 0,2R), surtout dans les premières fenêtres (65,6 % contre 39,5 % dans les dernières). Avant 2023, 45,2 % seulement, sous le point mort ; la différence est significative (Fisher, p ≈ 0,014). La rupture coïncide avec l'essor des 0DTE, sans identification causale formelle. Paramètres exacts non publiés.
>
> **Pour nous :** 🔴 pour l'ORB : depuis 2023, l'ouverture des indices US tend à se retourner. Cohérent avec notre **fade de gap post-0DTE** (en paper trading, [wiki/experiments/fade-gap-indices.md](wiki/experiments/fade-gap-indices.md)). Attention au double comptage : fade de gap et retournement de l'ouverture sont probablement le même effet.

### E.4 Échecs pré-enregistrés après coûts

### [20] Opening-Range Breakout Does Not Survive Trading Costs: A Pre-Registered 225-Cell Study on Sixteen Years of Futures Data

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7428398
- **Actifs :** 9 futures US liquides (indices, métaux, énergie), données 1 minute, 2010-2026
- **Plage horaire / Session :** deux ancres (**ouverture cash** et **ouverture Globex 18:00 ET**) × ranges de **5, 15, 30 et 60 minutes** × 3 sorties de la littérature
- **Date :** 2026 | **Auteurs :** Mulham Fetna | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : nulle part de façon exploitable. **Qui subit la contrainte** : personne de façon mesurable ; là où la cassure gagne, elle gagne **à l'intérieur du spread**. **Effet sur les bougies** : avantage brut médian de −0,01 tick ; la meilleure cellule échoue au test d'ancre aléatoire, donc c'est de la **continuation d'expansion de volatilité**, pas une information propre à l'ouverture.

> **Résumé (abstract paraphrasé) :** Grille de 225 cellules pré-enregistrée avant tout calcul, avec fenêtres d'exploration, de confirmation et de réserve figées, analyse de puissance et contrôles de falsification. Aucune cellule ne passe le seuil (t ≥ 2,5 à 25 $ l'aller-retour, signe stable par sous-période et par année). Brut, la grille gagne 1,57 M$ sur la confirmation ; à 25 $ l'aller-retour, elle perd 6,49 M$. 155 cellules sur 225 ont un avantage brut à moins de deux ticks de zéro ; 28 sont négatives avec une puissance suffisante. **Le range de 5 minutes, favori de la littérature, est la pire fenêtre.**
>
> **Pour nous :** 🔴🧪 le papier qui a fixé M3 (PREREGISTRATION n° 1) ; nos résultats le confirment. C'est la raison principale de la ligne ORB du registre. Papier de méthode du même auteur : [8].

### [21] Structural Limits of OHLCV-Based Intraday Signals in MNQ Futures: A Systematic Falsification Study

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6709401
- **Actifs :** Micro E-mini Nasdaq-100 (MNQ), 947 séances, barres 5 minutes, 2021-2025
- **Plage horaire / Session :** séance régulière (RTH) ; ORB à plusieurs horizons parmi 14 familles de signaux
- **Date :** 2026 | **Auteurs :** Mathias Mesfin | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : sans objet. **Qui subit la contrainte** : le trader qui exécute à l'open de la barre suivante, dont le coût (2 points aller-retour) dépasse l'avantage. **Effet sur les bougies** : l'avantage brut des signaux OHLCV plafonne entre 0,07 et 1,5 point par trade.

> **Résumé (abstract paraphrasé) :** 14 familles de signaux testées (ORB à plusieurs horizons, continuation et fade de gap, volume, momentum de la session Asie, chasse à la liquidité, classifieurs de régime, annonces) avec le même seuil : t ≥ 2 en walk-forward hors échantillon, au moins 30 trades, net positif après 2 points, stable chaque année. Aucun ne passe. La continuation short du gap a t = 3,23 mais seulement 22 trades. Deux signaux validés séparément servent de contrôles positifs.
>
> **Pour nous :** 🔴🧪 sur l'actif exact de nos comptes FTMO (NQ), même conclusion que Fetna pour l'ORB.

### [22] Do Simple Technical Trading Rules Survive Realistic Costs? Walk-Forward, Deflated-Sharpe and Monte-Carlo Evidence from 30 Years of Equity-Index Data

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6977700
- **Actifs :** S&P 500 et ASX 200 (journalier 1996-2026), S&P 500 en 5 minutes (2024-2026)
- **Plage horaire / Session :** ORB sur la séance cash (données 5 minutes)
- **Date :** 2026 | **Auteurs :** Udaya Wijesinghe | **Citations :** 0

> **Mécanisme causal intraday :** aucun trouvé : l'ORB et le retour à la moyenne intraday n'ont pas d'avantage significatif (DSR ≈ 0).

> **Résumé (abstract paraphrasé) :** Moyennes mobiles, cassure de tendance, RSI(2) et ORB, en walk-forward avec coûts et financement CFD. Toutes les règles font moins bien que la détention en rendement total. Seule une cassure de tendance journalière sur le S&P 500 améliore le Sharpe et réduit fortement le drawdown, mais pour un rendement quasi nul et sans réplication sur l'ASX. Les règles intraday n'ont aucun avantage significatif.
>
> **Pour nous :** 🔴🧪 l'échantillon intraday est court (2024-2026), mais c'est la période post-0DTE où Ladia [19] voit un retournement : cohérent.

### [23] Session Microstructure and the Momentum Mirage: Opening Ranges, Volatility Breakouts, and Cross-sectional Momentum in FX

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7435081
- **Actifs :** EURUSD, GBPUSD, AUDUSD, USDJPY, de M5 à H4
- **Plage horaire / Session :** ranges d'ouverture de session FX
- **Date :** 2026 | **Auteurs :** Shepherd Mahadzva | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : sans objet. **Qui subit la contrainte** : personne de mesurable. **Effet sur les bougies** : les 4 ORB perdent hors échantillon et sur la réserve, avec un taux de réussite 5 à 26 points sous leur point mort (trop pour les seuls coûts sur GBPUSD et AUDUSD).

> **Résumé (abstract paraphrasé) :** Quatre traductions de l'idée « momentum / cassure » passées au même protocole (walk-forward, coûts réalistes, tests multiples). La continuation après repli sur VWAP/EMA donne deux quasi-succès qui s'inversent sur la réserve. L'ORB est un échec net. Le momentum en coupe sur devises est négatif, et pire à haute fréquence. Quatre cassures de volatilité « significatives » (p jusqu'à 0,03) sont toutes rejetées par le reste des contrôles.
>
> **Pour nous :** ⚠️ hors indices (FX), mais rappelle qu'une cassure significative isolée ne suffit jamais.

### [24] Stop Distance, Exit Methodology, and Signal Preservation in Intraday Value Area Breakouts: Evidence from E-mini S&P 500 Futures

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6350238
- **Actifs :** E-mini S&P 500 (ES), données à la seconde, janvier 2025 → janvier 2026 (6 284 événements)
- **Plage horaire / Session :** cassure de la **value area** (Market Profile) de la séance, pendant la séance
- **Date :** 2026 | **Auteurs :** Theo Howard | **Citations :** 0
- *Fourni le 2026-10-13 ([papiers_ssrn_ohlcv_2026-10-13.md](papiers_ssrn_ohlcv_2026-10-13.md)) ; cousin de l'ORB : la zone de référence est la value area au lieu du range d'ouverture.*

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : après une cassure de la value area suivie d'un repli. **Qui subit la contrainte** : les acheteurs ou vendeurs de la zone de valeur, si le prix est vraiment accepté hors zone ; un repli peu profond signale cette acceptation. **Effet sur les bougies** : continuation brute sans avantage (−2,2 ticks, non significatif) ; les replis peu profonds battent les profonds d'environ 4 ticks ; toutes les distances de stop testées dégradent le résultat.

> **Résumé (abstract paraphrasé) :** Formalisation reproductible du « Setup 2 » de Market Profile. Sans filtre, rien de significatif, et plus rien du tout si l'on retire un mois de régime particulier. La profondeur du repli est un prédicteur significatif. Les 12 distances de stop testées font toutes moins bien qu'une sortie à horizon fixe.
>
> **Pour nous :** 🔴🧪 13 mois seulement. Rejoint Pineda [17] : ce qui se passe **après** la cassure (repli, retest) compte plus que la cassure elle-même.

---

## Bilan pour la suite

1. **ORB classique (cassure du range 5/15/30/60 min) sur futures d'indices** : la littérature indépendante récente (Fetna, Mesfin, Wijesinghe, Donninger) et notre M3 disent la même chose : rien après coûts. La nouvelle réplication [1] ne porte que sur la période d'origine.
2. **Les seules pistes non encore testées chez nous** viennent de papiers déjà fournis : le **filtre « vendredi sans annonce »** de Subhani (ORB 30 min) et la **règle de la 1ʳᵉ bougie de 5 min** de Zarattini-Aziz, qui n'est pas une cassure (M3b testait une cassure). Les deux supposent d'abord une condition de réouverture au registre.
3. **La bande de bruit sur NQ** ([5]) est le résultat le plus proche de ce que nous avons en paper trading : le confronter à la page M2 au moment de la lecture du forward, sans recalcul d'ici là.
