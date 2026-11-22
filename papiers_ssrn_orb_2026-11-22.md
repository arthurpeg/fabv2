# Papiers SSRN : l'opening range breakout (ORB) sur indices US

*Session du 2026-11-22. Recherche par **OpenAlex** (source SSRN, `S4210172589`, recherche plein texte puis `title_and_abstract.search`), complétée par **l'API Crossref filtrée sur les DOI SSRN** (`prefix:10.2139`) quand OpenAlex renvoyait 429 : 57 requêtes, environ 2 000 candidats, 126 gardés par mots-clés, triés par titre puis par résumé. Résumés venant d'OpenAlex ou de Crossref, **paraphrasés en français**. Tous les papiers déjà fournis (voir [papers/seen_papers.json](papers/seen_papers.json)) sont exclus de la liste numérotée ; ils sont rappelés seulement dans la carte de la section 0.*

**Mots-clés** : opening range breakout, opening range, ORB (strategy, day trading, intraday), 5-minute / 15-minute / 30-minute opening range, first five minutes, first 15 minutes, first 30 minutes return, first hour return, stocks in play, breakout strategy intraday, volatility breakout, intraday breakout futures, E-mini S&P intraday breakout, initial balance, market profile, Crabel, range expansion, day trading S&P 500 / Nasdaq / QQQ / SPY, intraday trend day, morning vs afternoon return, opening volatility index futures, Donchian intraday, stop loss intraday breakout, leveraged ETF day trading, Zarattini / Aziz (auteurs).

**Légende** : 🔴 échec ou condition limite · ⚠️ le signal dépend d'une donnée non OHLCV (options, VIX, calendrier d'annonces) ou d'un marché hors périmètre · 🧪 papier SSRN récent d'auteur indépendant, non relu par des pairs

> **Avant tout test : l'ORB est au registre des échecs** ([wiki/Failed Ideas/ledger.md](wiki/Failed%20Ideas/ledger.md), ligne du 2026-10-12, sans condition de réouverture). Nos M3a / M3b / M3c ([PREREGISTRATION.md](PREREGISTRATION.md), [RESULTS.md](RESULTS.md) §M3) : 10 ORB sur 27 tués par les coûts, aucun ne survit. Relancer un ORB demande d'abord d'écrire dans le registre une condition de réouverture précise (par exemple un mécanisme absent de M3 : filtre d'événements, régime, sens de la 1ʳᵉ bougie), puis une fiche d'idée selon [PROTOCOLE.md](PROTOCOLE.md).

**Bilan honnête de la récolte** : la littérature SSRN sur l'ORB est **mince et déjà presque entièrement fournie** (11 papiers ORB déjà au registre, voir section 0). Cette récolte n'ajoute que **6 papiers** utiles, dont **une seule réplication indépendante sur indices US** ([1]) et **une adaptation de la bande de bruit à NQ** ([5]) qui touche directement notre expérience M2 en paper trading.

**Écartés** : Aziz-Zarattini, *Can Day Trading Really Be Profitable?* (SSRN 4898296, nouvelle mise en ligne du 4416622 fourni le 2026-10-11) ; Wang-Gangwar, *Optimizing Intraday Breakout Strategies on the NSE* (SSRN 5198458 : ORB 5/15/30 min sur une seule action indienne, Tata Motors, un an) ; Rogul, *Hybrid Systematic-Discretionary Channel Breakout for NQ* (SSRN 6469419 : sens choisi à la main) ; Hashimoto, *SMT Formal Verification… Opening Range Compression Gates* (SSRN 7684999 : vérification formelle de code, l'ORB n'y est qu'accessoire) ; Poudel, *Small-Cap Stock Trading Strategies for Retail Traders* (SSRN 5921742 : petites capitalisations, sans résumé) ; Magner-Sanhueza-Lavin, *Breakout trading pays only when…* (SSRN 6898600 : cassures de plus hauts sur 52 semaines, quotidien) ; Khan, *Turtle Trend Following* (SSRN 7573918 : quotidien) ; Spells, *Do Options Markets Anticipate Momentum Breakout Failures?* (SSRN 6456100 : quotidien, options).

---

## 0. Carte des ORB par durée du range (papiers déjà fournis + nos résultats)

Rappel seulement : aucun de ces papiers n'est redonné. Fiches détaillées dans [recherche_causalite_intraday.md](recherche_causalite_intraday.md) (section ORB) et [PAPER_SPECS.md](PAPER_SPECS.md).

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

### [2] Regime-Conditional Alpha in SPY 0DTE Opening Range Breakout Strategies: A Filtering and Strike Selection Framework

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6355218
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

## Bilan pour la suite

1. **ORB classique (cassure du range 5/15/30/60 min) sur futures d'indices** : la littérature indépendante récente (Fetna, Mesfin, Wijesinghe, Donninger) et notre M3 disent la même chose : rien après coûts. La nouvelle réplication [1] ne porte que sur la période d'origine.
2. **Les seules pistes non encore testées chez nous** viennent de papiers déjà fournis : le **filtre « vendredi sans annonce »** de Subhani (ORB 30 min) et la **règle de la 1ʳᵉ bougie de 5 min** de Zarattini-Aziz, qui n'est pas une cassure (M3b testait une cassure). Les deux supposent d'abord une condition de réouverture au registre.
3. **La bande de bruit sur NQ** ([5]) est le résultat le plus proche de ce que nous avons en paper trading : le confronter à la page M2 au moment de la lecture du forward, sans recalcul d'ici là.
