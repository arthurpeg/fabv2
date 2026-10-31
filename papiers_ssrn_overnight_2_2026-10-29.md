# Papiers SSRN : l'overnight, deuxième série (indices US, FX majeurs, or, pétrole)

*Session du 2026-10-29. Suite de [papiers_ssrn_overnight_2026-10-21.md](papiers_ssrn_overnight_2026-10-21.md). Source : API OpenAlex filtrée sur SSRN (`S4210172589`), 65 requêtes (overnight return/anomaly/drift/reversal/momentum/sentiment/volatility/jump, close-to-open, open-to-close, trading break, extended hours, after-hours, sessions FX/or/pétrole, Globex), environ 4 100 candidats triés par titre. OpenAlex ne fournit plus les résumés : ils viennent de Crossref ou de Semantic Scholar. Résumés **paraphrasés en français**. Tous les papiers déjà fournis (voir [papers/seen_papers.json](papers/seen_papers.json)), y compris ceux du 2026-10-21, sont exclus.*

**Légende** : 🔴 échec ou condition limite · ⚠️ le signal dépend d'une donnée non OHLCV (flux, carnet d'ordres, news) ou d'un marché hors périmètre · 🧪 papier SSRN récent d'auteur indépendant, non relu par des pairs

---

## 0. Ce que cette deuxième série apporte

La première série couvrait les grands papiers sur **l'origine** du rendement de nuit (Overnight Drift, Berkman et al., tug of war). Le stock SSRN restant sur le sujet est surtout composé de :

- **A.** Mécanismes complémentaires : contraintes de vente à découvert, désaccord, ancrage, version « marché entier » du tug of war.
- **B.** Volatilité de nuit : quelle partie de la nuit prédit la séance, comment modéliser les deux périodes, et ce que cela change pour les stops.
- **C.** FX et liens entre places : peu de papiers SSRN, mais quelques résultats utiles.

🔴 **Couverture** : aucun nouveau papier SSRN sur l'overnight de l'**or** ou du **pétrole** n'a pu être retenu. Les seuls candidats (« Gold and Silver Shine During the Day », « Risk Transmissions around the Clock » sur des ETF matières premières) n'ont pas de résumé accessible : ils sont listés à la fin. Le pétrole n'apparaît qu'indirectement dans [15] (secteur énergie).

⚠️ **Heure d'hiver** : l'Europe est passée à l'heure d'hiver le 25 octobre, les États-Unis le font le 1er novembre 2026. Jusqu'au 1er novembre, la clôture cash US a lieu à **21h00** et l'ouverture à **14h30** heure de Paris.

---

## A. Indices US : mécanismes du rendement de nuit (suite)

### [1] Market-Level Tug of War and Asset Pricing

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5036288
- **Actifs :** marché actions US (indicateur agrégé)
- **Plage horaire / Session :** nuit contre séance, au niveau du marché
- **Date :** 2024 | **Auteurs :** Lei Zhao, Chardin Wese Simen, Ran Tao | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : chaque jour, entre la nuit et la séance. **Qui subit la contrainte** : les traders de séance, qui **corrigent trop** la poussée de la nuit. **Effet sur les bougies** : un indicateur simple classe chaque jour en « calme » (nuit et séance dans le même sens) ou « bruité » (nuit et séance opposées, tug of war au niveau du marché). Le CAPM fonctionne les jours calmes et échoue les jours bruités.

> **Résumé (abstract paraphrasé) :** Les auteurs construisent une fonction indicatrice à partir du tug of war agrégé entre traders de nuit et de séance. La relation beta/rendement tient les jours calmes et échoue les jours bruités, même après contrôle des annonces macro et des résultats d'entreprises. Ils proposent et testent une explication par la sur-correction.
>
> **Pour nous :** c'est la version indice du tug of war (la version actions était [5] de la série du 2026-10-21). Variable OHLCV immédiate sur ES/NQ : signe(gap) ≠ signe(ouverture → clôture). À tester comme filtre de régime : nos stratégies de séance marchent-elles différemment après un jour « bruité » ?

### [2] Dispersion of Opinions, Limits to Arbitrage, and Overnight Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1214564
- **Actifs :** 3 000 plus grandes actions US (9 ans de données intraday)
- **Plage horaire / Session :** nuit, puis séance qui suit
- **Date :** 2008 | **Auteurs :** Henk Berkman, Paul D. Koch, Laura A. Tuttle, Ying Zhang | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture. **Qui subit la contrainte** : les vendeurs à découvert, freinés par les contraintes de short et les coûts. Seuls les optimistes fixent le prix d'ouverture (Miller, 1977). **Effet sur les bougies** : l'ouverture est trop haute par rapport au reste de la séance. Nuit positive, puis retournement en séance. 🔴 Ce n'est **pas** une clôture trop basse : une simple prime de liquidité de nuit ne suffit pas à expliquer l'effet.

> **Résumé (abstract paraphrasé) :** Les actions ont des rendements de nuit positifs suivis de retournements en séance, à cause d'une ouverture élevée. L'effet est limité aux titres où le désaccord est fort près de l'ouverture et sur la journée. Il augmente avec les limites à l'arbitrage : contraintes de short plus fortes, coûts de transaction plus élevés.
>
> **Pour nous :** c'est la version de travail du papier « Paying Attention » (fourni le 2026-10-21), centrée sur le désaccord. Une version 2007 (SSRN 993304) dit la même chose. Proxy OHLCV du désaccord sur l'indice : range de la veille / ATR élevé. Hypothèse : retournement de la première heure plus fort les jours qui suivent une séance très large.

### [3] Heterogeneity in Overnight-versus-Intraday Stock-Return Behavior with Asymmetric Information and 52-week Price Anchoring

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7443340
- **Actifs :** actions US
- **Plage horaire / Session :** rendements de nuit et de séance du mois précédent → mois suivant
- **Date :** 2026 | **Auteurs :** Chen Chen, Chris T. Stivers, Licheng Sun | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : d'un mois sur l'autre, séparément pour la nuit et la séance. **Qui subit la contrainte** : les investisseurs qui **s'ancrent sur le plus haut de 52 semaines** et ceux qui ont moins d'information. **Effet sur les bougies** : les titres à forte asymétrie d'information ont un fort **momentum de nuit** et un retournement en séance. Près du plus haut de 52 semaines, le momentum de séance est plus faible. Les effets sont plus forts quand le sentiment est haut.

> **Résumé (abstract paraphrasé) :** L'anomalie nuit/séance varie beaucoup entre titres selon deux dimensions. Un indicateur composite d'asymétrie d'information prédit comment le rendement de nuit du mois passé se propage. La distance au plus haut de 52 semaines prédit comment le rendement de séance se propage. Les titres à forte asymétrie gagnent plus la nuit et moins en séance.
>
> **Pour nous :** la variable « distance au plus haut de 52 semaines » est OHLCV. Sur l'indice : le drift de nuit est-il différent quand l'ES est proche de son plus haut annuel ?

### [4] Overnight Returns, Daytime Reversals, and Anchoring Bias

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4482812
- **Actifs :** actions US
- **Plage horaire / Session :** nuit → séance (tug of war)
- **Date :** 2023 (publié Applied Economics Letters 2024) | **Auteurs :** Donghoon Kim, Jihoon Goh | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit, puis la séance. **Qui subit la contrainte** : les noise traders de nuit, qui butent sur la **barrière psychologique** du plus haut de 52 semaines. **Effet sur les bougies** : l'intensité anormale du tug of war rapporte une prime plus forte pour les titres **loin** de leur plus haut de 52 semaines.

> **Résumé (abstract paraphrasé) :** L'étude relie le biais d'ancrage au tug of war quotidien entre nuit et séance, en fonction de la distance au plus haut de 52 semaines. La prime liée à l'intensité anormale du tug of war est significative pour les titres éloignés de ce plus haut. Les barrières psychologiques des investisseurs de nuit façonnent la dynamique des rendements.
>
> **Pour nous :** même variable d'ancrage que [3], résultat cohérent. Papier court.

### [5] 4-Factor Model for Overnight Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2511874
- **Actifs :** actions US
- **Plage horaire / Session :** clôture → ouverture
- **Date :** 2014 | **Auteurs :** Zura Kakushadze | **Citations :** 7

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit. **Qui subit la contrainte** : non précisé ; papier empirique de praticien (WorldQuant). **Effet sur les bougies** : quatre facteurs construits **uniquement sur les prix et volumes intraday** de la veille (prix, volatilité, momentum, volume) prédisent le rendement de nuit. Les facteurs fondamentaux (value, growth) n'aident pas à cet horizon.

> **Résumé (abstract paraphrasé) :** L'auteur propose un modèle à quatre facteurs pour les rendements de nuit, analogues à la taille (prix), la volatilité, le momentum et la liquidité (volume). Les régressions de type Fama-MacBeth donnent des statistiques t élevées. Il l'utilise dans une stratégie de retour à la moyenne intraday.
>
> **Pour nous :** les quatre variables sont OHLCV. Sur un seul indice, l'idée se traduit par : volatilité, momentum et volume de la séance comme prédicteurs du rendement de nuit.

### [6] Modelling Overnight and Daytime Returns Using a Multivariate GARCH-Copula Model

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1710799
- **Actifs :** 15 fonds de types différents (actions, obligations, etc.)
- **Plage horaire / Session :** nuit contre séance
- **Date :** 2010 | **Auteurs :** Long Kang, Simon H. Babbs | **Citations :** 6

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la séance qui suit la nuit. **Qui subit la contrainte** : les traders de séance, qui intègrent avec retard une information de nuit asymétrique. **Effet sur les bougies** : pour la plupart des actifs, la nuit a une **moyenne plus haute**, une **variance plus faible** et des **queues plus épaisses** que la séance. Le rendement de séance est **négativement corrélé** au rendement de nuit qui le précède.

> **Résumé (abstract paraphrasé) :** Un modèle GARCH-copule multivarié décrit ensemble les rendements de nuit et de séance de plusieurs actifs. La séance dépend de la nuit précédente en moyenne, en variance et en corrélation. Les résultats sont cohérents avec l'asymétrie d'information de la microstructure. Une copule t à corrélation dynamique améliore nettement l'ajustement.
>
> **Pour nous :** la corrélation négative nuit → séance va dans le sens de Branch-Ma, mais Branch-Ma 2018 (série du 2026-10-21, [9]) montre qu'elle a disparu sur le S&P 500. Les queues épaisses de la nuit justifient de traiter le gap à part dans le risque.

---

## B. Volatilité de nuit, pre-market et stops

### [7] Predicting Stock Volatility Using After-Hours Information

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1324991
- **Actifs :** quatre actions Nasdaq (MSFT, AMGN, CSCO, YHOO)
- **Plage horaire / Session :** post-clôture, nuit entière, **pre-open**
- **Date :** 2009 | **Auteurs :** Chun-hung Chen, Wei-Choun Yu, Eric W. Zivot | **Citations :** 3

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant le **pre-open** (avant 15h30 Paris). **Qui subit la contrainte** : les traders informés, qui agissent avant l'ouverture, alors que la post-clôture est dominée par des échanges de liquidité. **Effet sur les bougies** : la variance du **pre-open** améliore la prévision de la volatilité de la séance suivante. 🔴 La variance post-clôture et le carré du rendement de nuit n'apportent rien.

> **Résumé (abstract paraphrasé) :** Des modèles GARCH et à mémoire longue sont enrichis avec la variance réalisée de la nuit, du pre-open, de la post-clôture et le rendement de nuit au carré. Seule la variance du pre-open améliore la prévision hors échantillon. Cela confirme qu'on trade pour des raisons non informationnelles après la clôture et pour des raisons informationnelles avant l'ouverture.
>
> **Pour nous :** cohérent avec Barclay-Hendershott (série du 2026-10-14). Pour dimensionner une position à l'ouverture, mesurer la volatilité des barres ES/NQ de **14h30 à 15h30** Paris plutôt que celle de toute la nuit.

### [8] A Coupled Component GARCH Model for Intraday and Overnight Volatility

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3112950
- **Actifs :** actions du Dow Jones (1991–2016), portefeuilles CRSP par taille
- **Plage horaire / Session :** nuit contre séance
- **Date :** 2018 | **Auteurs :** Oliver B. Linton, Jianbin Wu | **Citations :** 3

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : sur deux décennies, nuit contre séance. **Qui subit la contrainte** : la séance, qui perd une partie de la découverte du prix au profit de la nuit. **Effet sur les bougies** : le **rapport volatilité de nuit / volatilité de séance a augmenté** pour les actions du Dow et les grandes capitalisations, et diminué pour les petites. Les corrélations de nuit et de séance entre titres ont toutes deux fortement augmenté.

> **Résumé (abstract paraphrasé) :** Un modèle GARCH semi-paramétrique sépare les dynamiques de nuit et de séance, avec un modèle à queues épaisses pour la nuit. L'estimation combine noyau et maximum de vraisemblance. Plus la capitalisation est grande, plus la part de la nuit a augmenté.
>
> **Pour nous :** sur les indices, une part croissante du risque est dans le gap. Cela renforce l'intérêt de travailler sur les futures 24h plutôt que sur le cash.

### [9] Observation-driven Models for Realized Variances and Overnight Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3429750
- **Actifs :** 100 actions du S&P 500 (2001–2014)
- **Plage horaire / Session :** ouverture → clôture et clôture → ouverture
- **Date :** 2019 | **Auteurs :** Anne Opschoor, André Lucas | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit. **Qui subit la contrainte** : le gestionnaire de risque, qui sous-estime le risque s'il ignore la nuit. **Effet sur les bougies** : le rapport entre volatilité totale et volatilité de séance **varie fortement dans le temps**, surtout pour les valeurs financières.

> **Résumé (abstract paraphrasé) :** Le modèle découpe la volatilité journalière en une volatilité de séance (filtrée sur données haute fréquence) et un facteur d'échelle variable. Des dynamiques à score sur lois à queues épaisses limitent l'effet des grosses observations isolées. Le modèle bat les alternatives en Value-at-Risk et Expected Shortfall.

### [10] Firm-Specific News, Extended-Hours Trading, and Variances Over Trading and Nontrading Periods

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=476281
- **Actifs :** actions Nasdaq
- **Plage horaire / Session :** after-hours, pre-market, séance régulière
- **Date :** 2003 | **Auteurs :** Volodymyr M. Zdorovtsov | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant la séance, comparée aux périodes de fermeture. **Qui subit la contrainte** : le prix, poussé par le trading des **informés** et par les nouvelles publiques en heures ouvrées. **Effet sur les bougies** : la variance par heure est bien plus forte en séance que la nuit. Elle vient à la fois de l'information privée révélée par les échanges et de l'information publique.

> **Résumé (abstract paraphrasé) :** La littérature propose trois explications à la variance plus forte en séance : plus d'information publique, l'information privée des informés, ou le bruit créé par le trading. Avec les flux d'ordres after-hours, pre-market et séance, et une base de nouvelles, l'auteur valide l'hypothèse d'information privée, et aussi celle d'information publique.

### [11] Does News, Order Flow, or Illiquidity drive jumps in stock returns? In the day or in the night?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4637027
- **Actifs :** actions US
- **Plage horaire / Session :** sauts de séance contre sauts de nuit
- **Date :** 2023 | **Auteurs :** Yoontae Jeon, Thomas H. McCurdy, Stephen Szaura | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : séparément la nuit et en séance. **Qui subit la contrainte** : les prix soumis aux nouvelles, aux déséquilibres d'ordres et à l'illiquidité. **Effet sur les bougies** : l'intensité et la taille des sauts sont liées à ces trois sources, avec des différences entre nuit et séance.

> **Résumé (abstract paraphrasé) :** Les auteurs relient les nouvelles d'entreprise, l'illiquidité et les déséquilibres d'ordres aux sauts de prix et au risque de saut idiosyncratique, sur la journée entière, la séance et la nuit. Cela aide à distinguer les sauts dus à l'information de ceux dus à la liquidité ou au trading stratégique.
>
> **Pour nous :** ⚠️ les sources demandent des données externes. Intérêt surtout conceptuel : un gap dû à une nouvelle et un gap dû à la liquidité ne se comportent pas pareil (cohérent avec Lescourret, série du 2026-10-14).

### [12] On the Effectiveness of Stop-Loss Rules: An Analytical Framework Based on Modeling Overnight Gaps and the Stationary Bootstrap

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3087196
- **Actifs :** actions NYSE
- **Plage horaire / Session :** gap de nuit (le stop ne peut pas être exécuté pendant la fermeture)
- **Date :** 2017 | **Auteurs :** Argimiro Arratia, Albert Dorador | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture, quand le gap saute par-dessus le stop. **Qui subit la contrainte** : le porteur d'une position avec stop, exécuté au prix d'ouverture et non au niveau du stop. **Effet sur les bougies** : en marché haussier, les stops améliorent le rendement ajusté du risque ; en marché baissier, ils améliorent le rendement absolu. Le stop en **pourcentage fixe** est le plus efficace, devant le stop basé sur le RSI.

> **Résumé (abstract paraphrasé) :** Quatre règles de stop-loss sont évaluées par deux méthodes : des modèles de prix d'action NYSE qui intègrent les gaps de nuit, et un bootstrap stationnaire sur données historiques. Les stops ajoutent de la valeur dans la plupart des cas. Le stop en pourcentage fixe arrive en tête.
>
> **Pour nous :** sur les futures ES/NQ, le gap est plus petit (cotation quasi continue), sauf au-dessus de la pause CME et du week-end. À garder pour les stratégies tenues pendant le week-end.

### [13] ⚠️🧪 Round-Number Anchoring in Overnight US Equity Order Sizes: Evidence from 274 Million Order Events on the Blue Ocean ATS

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6651000
- **Actifs :** 30 titres et ETF US (dont TQQQ, DIA) sur Blue Ocean ATS
- **Plage horaire / Session :** **séance de nuit** US (Blue Ocean, août 2025 – mars 2026)
- **Date :** 2026 | **Auteurs :** Boon Chuan Lim | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant la nuit US, sur la principale plateforme de nuit. **Qui subit la contrainte** : les particuliers en accès sponsorisé (courtiers grand public), qui dominent ce marché. **Effet sur les bougies** : aucun effet direct sur les prix mesuré. **40 %** des ordres sont à une taille ronde ; la taille la plus fréquente est **20 actions**, ce qui signe un flux très majoritairement particulier.

> **Résumé (abstract paraphrasé) :** Sur 274 millions d'ordres, les tailles se regroupent fortement autour de nombres ronds, avec un mode à 20 actions inconnu sur les marchés de jour. Le regroupement va de 15 % (TQQQ) à 67 % (DIA). Le marché de nuit est un lieu distinct, continu, dominé par les particuliers.
>
> **Pour nous :** confirme que la nuit US est désormais **un marché de particuliers**, ce qui va dans le sens des mécanismes « demande des particuliers » ([2], et Lu-Qin, Berkman de la série précédente). Pas de signal de prix direct.

---

## C. FX, liens entre places et heures de cotation

### [14] ⚠️ Liquidity Provision in the Overnight Foreign Exchange Market

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=882835
- **Actifs :** SEK/EUR (presque toutes les transactions sur près de 10 ans)
- **Plage horaire / Session :** positions tenues d'un jour à l'autre (overnight)
- **Date :** 2005 (publié JIMF) | **Auteurs :** Geir H. Bjønnes, Dagfinn Rime, Haakon Solheim | **Citations :** 116

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : d'une journée à la suivante, sur les positions gardées la nuit. **Qui subit la contrainte** : les banques et clients **financiers**, qui prennent des positions directionnelles ; les clients **non financiers** (entreprises) absorbent ces positions et fournissent la liquidité. **Effet sur les bougies** : la position nette des non-financiers est **négativement** corrélée au taux de change (ils achètent quand ça baisse), celle des financiers positivement.

> **Résumé (abstract paraphrasé) :** Les clients non financiers sont les principaux fournisseurs de liquidité de nuit sur le marché des changes. Leurs positions sont de sens opposé au taux de change, et leurs variations sont prévues par celles des clients financiers. Ils jouent donc un rôle passif de fournisseur de liquidité.
>
> **Pour nous :** les données de flux ne sont pas disponibles en OHLCV, et la paire est hors des majeures. Le mécanisme (les entreprises absorbent la nuit les excès des financiers) aide pourtant à comprendre pourquoi les gros mouvements de fin de journée sur les majeures peuvent se retourner la nuit.

### [15] 🧪 What Crosses Borders? The New York Cash Session and the Cross-section of Asia-Pacific Transmission

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7091018
- **Actifs :** 9 marchés Asie-Pacifique, 17 ETF sectoriels japonais (TOPIX-17), **E-mini S&P 500**, ETF énergie US
- **Plage horaire / Session :** séance cash de New York → gap d'ouverture asiatique le lendemain (2009–2024)
- **Date :** 2026 | **Auteurs :** Ryo Kinoshita | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture asiatique, juste après la nuit européenne. **Qui subit la contrainte** : les marchés fermés pendant la séance de New York. **Effet sur les bougies** : c'est la **séance cash de New York** (ouverture → clôture) qui porte **98,6 %** du pouvoir prédictif sur le sens du gap asiatique ; le gap overnight de New York en porte très peu. 🔴 La dérive de l'E-mini **après la clôture cash** et avant Tokyo n'ajoute presque rien. Seul le secteur **énergie** a un canal propre (énergie japonaise liée à l'ETF énergie US).

> **Résumé (abstract paraphrasé) :** Ce papier d'un auteur déjà présent dans la série du 2026-10-14 précise quelle partie de la journée new-yorkaise transmet l'information à l'Asie. La précision directionnelle augmente avec la sensibilité du secteur au risque actions mondial (60,1 + 16,3 × beta). Les facteurs de risque larges absorbent l'information sectorielle, sauf pour l'énergie.
>
> **Pour nous :** résultat négatif pour l'overnight des futures US : la dérive ES de **22h00 à 1h00** Paris n'apporte pas d'information au-delà de la clôture cash. Pour le pétrole, c'est un indice qu'un lien énergie US → Asie existe ; à creuser.

### [16] Exchange Rate Volatility, Macro Announcements and the Choice of Intraday Seasonality Filtering Method

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1032876
- **Actifs :** EUR/USD (5 minutes) et données simulées
- **Plage horaire / Session :** profil horaire de la volatilité sur 24h
- **Date :** 2007 | **Auteurs :** Helinä Laakkonen | **Citations :** 25

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : sur les 24 heures, autour des annonces macro. **Qui subit la contrainte** : le chercheur, plutôt que le marché : c'est un papier de méthode. **Effet sur les bougies** : la volatilité de l'EUR/USD a un fort profil horaire (sessions Asie/Europe/US). Si on ne le retire pas correctement, on **sous-estime** l'effet des annonces.

> **Résumé (abstract paraphrasé) :** Le papier compare plusieurs méthodes de retrait de la saisonnalité intraday de la volatilité, pour estimer l'effet des nouvelles sur la volatilité du change. Toutes les méthodes biaisent vers le bas les coefficients des annonces, certaines plus que d'autres. La méthode Flexible Fourier Form est la meilleure.
>
> **Pour nous :** pour tout test FX par session, il faut normaliser le rendement par la volatilité **de l'heure** (profil moyen), pas par une volatilité journalière unique.

### [17] Extending Exchange Trading Hours

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6224760
- **Actifs :** 60 bourses mondiales ; cas du marché des changes (CLS) et des cryptomonnaies
- **Plage horaire / Session :** extension vers le trading 24/5
- **Date :** 2026 | **Auteurs :** Kaitao Lin | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : aux heures où l'exécution est ouverte mais la compensation, le règlement ou le financement ne le sont pas. **Qui subit la contrainte** : les fournisseurs de liquidité, qui ne peuvent pas refinancer ou régler leurs positions en continu. **Effet sur les bougies** : 🔴 un accès continu ne veut **pas** dire une liquidité continue. La qualité de marché varie selon l'heure, comme on le voit sur le FX et les cryptos.

> **Résumé (abstract paraphrasé) :** L'auteur recense les horaires de 60 bourses et analyse les décalages entre exécution et post-marché (chambres de compensation, dépositaires, systèmes de règlement). Les cas du FX et des cryptomonnaies montrent que la qualité du marché dépend de l'heure. Le résultat pour l'investisseur dépend de l'alignement de toute la chaîne, pas seulement du moteur de négociation.
>
> **Pour nous :** contexte utile alors que les actions US passent au 24/5. Les heures où le post-marché est fermé (par exemple autour du rollover FX de 23h00 Paris) sont celles où la liquidité est mince : spreads plus larges, mèches plus longues.

---

## D. Synthèse : ce qui s'ajoute à la première série

1. **Tug of war au niveau de l'indice** [1] : variable simple, signe(gap) ≠ signe(séance). À tester comme filtre de régime pour les stratégies de séance existantes.
2. **Désaccord et ancrage** [2] [3] [4] : la nuit pousse le prix vers le haut et la séance le corrige surtout quand le désaccord est fort (proxy : range de la veille / ATR) et selon la distance au plus haut de 52 semaines.
3. **Prédire le rendement de nuit avec la séance** [5] : volatilité, momentum et volume de la séance comme variables explicatives.
4. **Volatilité** [7] [8] [9] : utiliser le **pre-market** (14h30–15h30 Paris) plutôt que toute la nuit pour prévoir l'amplitude de la séance ; la part de la nuit dans le risque a augmenté sur les grandes capitalisations.
5. **Ce qui ne sert pas** : la dérive ES après la clôture cash [15], la variance post-clôture [7].
6. **FX** : normaliser par la volatilité de l'heure [16] ; éviter les heures de post-marché fermé [17].

**Tests proposés** (à pré-enregistrer) :
- **H5 (tug of war indice)** : rendement de 15h30 à 16h30 Paris le lendemain d'un jour « bruité » (gap et séance de signes opposés) contre un jour « calme ». ES et NQ.
- **H6 (désaccord)** : rendement de la première heure de séance en fonction de (range de la veille / ATR 14), en quintiles.
- **H7 (vol du pre-market)** : la volatilité réalisée de 14h30 à 15h29 prédit-elle mieux le range de la séance que celle de 0h à 15h29 ? Usage : taille de position.

### Résumé introuvable, à revoir (SSRN et Semantic Scholar bloquent l'accès automatique)
Retenus pour leur sujet, dans l'ordre de priorité :
- Risk Transmissions around the Clock: Evidence from Bitcoin, Treasury, Commodity, and Equity ETFs (Shi) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5022720
- Gold and Silver Shine During the Day (Kelly) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5976178
- Overnight Returns as a Market Timing Strategy (Kelly) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3692068
- Overnight Reversal and the Asymmetric Reaction to News (Dangl, Salbrechter) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4307675
- How Does the Daily Volatility of Foreign Exchange Rates Depend on the Time of Day at Which the Daily Returns Are Calculated? (Doman, Doman) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3651344
- The Dynamics of Linkages Between Major Currencies: How Does It Change Depending on the Time of Day? (Doman, Doman) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3652087
- Mind the Gap: Is There a Trading Break Equity Premium? (Perras, Wagner) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4284444
- The Dynamics of Daily, Intraday and Overnight Betas (Insana) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3686528
- Volume Shocks and Overnight Returns (Cartea, Cucuringu, Jin, Wilson) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5156605
- Overnight Return Momentum and the Timing of Trading Volume (Perreten, Wallmeier) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5004991
- Overnight vs. Intraday Returns: Investor Disagreement, Information Uncertainty, and Future Stock Returns (Harris, Li, Taylor) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5164956
- Overnight Returns: Investor Sentiment or Investor Attention? (Prapan, Vagenas-Nanos) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4015493
- Testing a Contrarian Hypothesis: The Predictive Power of Overnight News Sentiment on S&P 500 Intraday Returns (Chitturi) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5723163
- The Weekend Effect: A Trading Robot and Fractional Integration Analysis (Caporale, Gil-Alana, Plastun, Oleksiv) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2456123
- 24-Hour Trading: Systems and Challenges (Dao) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5181265
