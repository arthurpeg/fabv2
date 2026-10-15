# Papiers SSRN : prévoir le sens de l'ouverture des indices US (15h30 heure de Paris)

*Session du 2026-10-14. Source : API OpenAlex filtrée sur SSRN (`S4210172589`), 30 requêtes ciblées (overnight, pre-market, opening gap, prix étrangers la nuit, futures/cash, pre-opening, after-hours), environ 3 700 candidats triés par titre. OpenAlex ne fournit plus les résumés : ils viennent de Crossref ou de Semantic Scholar. Résumés **paraphrasés en français**. Les papiers déjà fournis (voir [papers/seen_papers.json](papers/seen_papers.json)) sont exclus.*

**Légende** : 🔴 échec ou condition limite · ⚠️ le signal dépend d'une donnée non OHLCV (news, flux par type d'investisseur) ou d'un marché hors périmètre · 🧪 papier SSRN récent d'auteur indépendant, non relu par des pairs

---

## 0. Point de départ : ce que « le sens de l'opening » veut dire en pratique

À 15h29, le **gap** est déjà connu : les futures ES/NQ cotent toute la nuit et le cash ouvre à peu près sur leur prix. On ne peut donc pas parier sur le gap lui-même à 15h30. Ce qu'on peut chercher à prévoir, c'est **ce que fait le prix après 15h30** : est-ce que le gap continue ou se referme dans les 30 à 60 premières minutes ? Les papiers ci-dessous se répartissent en deux groupes :

- **A.** Comment l'information de la nuit (Asie, Europe, pre-market) se retrouve dans le prix d'ouverture. Cela dit quelle part du gap est « vraie » information et quelle part est du bruit.
- **B.** Ce qui se passe après l'ouverture selon le gap et le comportement de la nuit.

⚠️ **Heure d'été et d'hiver** : l'Europe change d'heure le 25 octobre 2026 et les États-Unis le 1er novembre 2026. Pendant cette semaine, l'ouverture US a lieu à **14h30** heure de Paris. La même chose se produit en mars.

---

## A. Prévoir le gap : la nuit et le pre-market

### [1] Information Flows around the Globe: Predicting Opening Gaps from Overnight Foreign Stock Price Patterns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1510069
- **Actifs :** grands indices mondiaux, dont les indices US
- **Plage horaire / Session :** de la clôture à l'ouverture (gap d'ouverture)
- **Date :** 2009 | **Auteurs :** Jan G. De Gooijer, Cees G. H. Diks, Łukasz Gątarek | **Citations :** 9

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant la fermeture du marché local, quand d'autres places cotent encore. **Qui subit la contrainte** : le marché fermé, qui ne peut intégrer l'information étrangère qu'à sa réouverture. **Effet sur les bougies** : le gap d'ouverture reprend, souvent de façon non linéaire, le parcours des marchés étrangers pendant la nuit. Pour les **États-Unis**, en revanche, un modèle linéaire fondé sur la dernière information disponible suffit : le marché US absorbe déjà efficacement ce qui s'est passé la nuit.

> **Résumé (abstract paraphrasé) :** Les auteurs prévoient les rendements clôture→ouverture des grands indices à partir de la trajectoire des prix étrangers pendant la nuit, traitée comme une courbe (analyse de données fonctionnelles). Le meilleur modèle est non paramétrique, ce qui signale des relations non linéaires. Cela vaut surtout pour l'Europe et l'Asie. L'Amérique du Nord et l'Australie paraissent plus efficaces.
>
> **Pour nous :** pour le S&P et le Nasdaq, la dernière cotation des futures avant 15h30 contient déjà l'essentiel. Les marchés étrangers n'apportent rien de plus pour prévoir le gap.

### [2] 🧪 When Does Overnight Price Discovery Occur?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7600620
- **Actifs :** actions du S&P 500 (données à la minute)
- **Plage horaire / Session :** after-market (16h–20h ET), session « dark » (20h–4h ET), pre-market (4h–9h30 ET)
- **Date :** 2026 | **Auteurs :** Thomas Perreten | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant tout le pre-market, de 10h à 15h30 heure de Paris. **Qui subit la contrainte** : les liquidités du pre-market, qui exigent une prime d'illiquidité tant que le carnet est mince. **Effet sur les bougies** : les mouvements de la nuit noire sont positifs en moyenne, mais le pre-market les **corrige en partie**. La correction est la plus forte quand le pre-market est le moins liquide. Plus on avance dans le pre-market, plus le prix explique le gap final. L'ouverture des marchés étrangers ne crée pas de saut dans cette capacité d'explication.

> **Résumé (abstract paraphrasé) :** Le rendement overnight est découpé en trois parties : after-market, période dark et pre-market. Le pouvoir explicatif des rendements de la nuit sur le gap final augmente progressivement tout au long du pre-market. Les rendements dark sont positifs, ceux du pre-market négatifs et en partie inverses. Les premiers mouvements apportent de l'information mais ne sont pas entièrement permanents.
>
> **Pour nous :** la part du gap faite tôt et dans un marché mince est la moins fiable. Variable à tester : la part du gap construite après 14h30 (après les statistiques de 8h30 ET), comparée à celle construite pendant la nuit.

### [3] 🧪 The Global Relay: A Hierarchical Structure of International Information Transmission Originating from the New York Close

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7276580
- **Actifs :** indices et secteurs Asie-Pacifique, Europe et États-Unis ; ETF liés à l'énergie
- **Plage horaire / Session :** de la clôture de New York à l'ouverture suivante de chaque marché
- **Date :** 2026 | **Auteurs :** Ryo Kinoshita | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture de chaque marché, après la clôture de New York. **Qui subit la contrainte** : les marchés qui ouvrent après New York et doivent intégrer la séance US. **Effet sur les bougies** : la séance de jour US prévoit le sens de l'ouverture en Asie, d'autant plus que le secteur ciblé a un beta US élevé (la « beta law »). 🔴 Le seul lien **sans** information, une fois la tendance propre du marché cible contrôlée, est celui **qui revient vers New York**.

> **Résumé (abstract paraphrasé) :** Ce papier prolonge deux papiers du même auteur : la clôture de New York prédit le sens de l'ouverture asiatique mieux qu'une pièce de monnaie, et l'avantage disparaît en un jour. Ici, la boucle New York → Asie → Europe → New York est testée. Tous les liens portent de l'information, sauf le retour vers New York.
>
> **Pour nous :** c'est un résultat négatif utile. L'Europe et l'Asie n'ajoutent pas d'information sur l'ouverture US au-delà de la tendance US elle-même. Ne pas perdre de temps avec un signal du type « le DAX a monté ce matin ».

### [4] 🧪 When Local Markets Close but the World Keeps Trading: Global Information Absorption at Market Reopening

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7248259
- **Actifs :** Nikkei 225, FTSE 100, DAX, S&P 500
- **Plage horaire / Session :** réouverture après un jour férié local, quand les autres marchés ont coté
- **Date :** 2026 | **Auteurs :** Fuli Yang, Tingting Qiu | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le jour de réouverture après un jour de fermeture locale (jour férié US par exemple). **Qui subit la contrainte** : le marché fermé, qui n'intègre l'information étrangère qu'en rouvrant. **Effet sur les bougies** : le rendement du jour de réouverture reprend environ **63 %** du choc étranger (coefficient 0,631). Sur la période cumulée, l'effet est nul : c'est un décalage dans le temps, pas un rendement anormal. Pour le DAX et le Nikkei, la reprise se partage entre le gap (0,37) et la séance qui suit (0,39).

> **Résumé (abstract paraphrasé) :** 809 fermetures sont comparées à des fenêtres témoins de même longueur, appariées sur le signe et la taille du choc étranger. La fermeture change le moment où l'information entre dans le prix, pas son total. L'effet est plus faible en dehors du Japon.
>
> **Pour nous :** c'est pertinent seulement pour l'ouverture **après un jour férié US** où l'Europe a coté. Une partie de la reprise se fait **après** le gap, pendant la séance. C'est un cas rare mais exploitable.

### [5] Price Discovery and Trading Costs after Hours

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=207914
- **Actifs :** actions NYSE et Nasdaq
- **Plage horaire / Session :** after-hours (après la clôture) et pre-market (avant l'ouverture)
- **Date :** 2000 | **Auteurs :** Michael J. Barclay, Terrence J. Hendershott | **Citations :** 19

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : hors séance, surtout **juste avant l'ouverture**. **Qui subit la contrainte** : les traders informés, qui passent par des ECN anonymes avant l'ouverture, alors que les échanges de liquidité dominent après la clôture. **Effet sur les bougies** : le pre-market contient plus d'information par transaction que l'after-hours. Les prix proches de l'ouverture sont plus informatifs que ceux de la soirée.

> **Résumé (abstract paraphrasé) :** Les volumes hors séance sont faibles, mais chaque transaction y est plus informative qu'en journée, et les coûts de spread y sont deux fois plus élevés. Les transactions informées, petites et anonymes, se concentrent avant l'ouverture. Les grosses transactions de liquidité se concentrent après la clôture.

---

## B. Après l'ouverture : le gap continue-t-il ou se referme-t-il ?

### [6] Return Differences between Trading and Non-Trading Hours: Like Night and Day

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1004081
- **Actifs :** actions US, indices, futures sur indices (NYSE et Nasdaq)
- **Plage horaire / Session :** nuit (clôture → ouverture) contre jour (ouverture → clôture) ; **première heure**
- **Date :** 2008 | **Auteurs :** Michael J. Cooper, Michael T. Cliff, Huseyin Gulen | **Citations :** 99

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture et pendant la **première heure**. **Qui subit la contrainte** : les acheteurs à l'ouverture, qui paient un prix d'ouverture trop haut. **Effet sur les bougies** : la prime de risque actions vient entièrement de la nuit. Le rendement de jour est proche de zéro, parfois négatif. L'effet vient en partie de **prix d'ouverture trop élevés qui baissent pendant la première heure**.

> **Résumé (abstract paraphrasé) :** Sur données transaction par transaction, la prime de risque US de la décennie étudiée vient uniquement de la nuit. L'effet vaut pour les actions, les indices et les futures, quels que soient le jour de la semaine, le jour du mois ou le mois.
>
> **Pour nous :** c'est le biais de base à 15h30. En moyenne, l'ouverture est un peu trop haute et la première heure a une pente négative. À tester : est-ce que ce biais est plus fort après un gap haussier ?

### [7] The Overnight Return, One More Anomaly

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=937997
- **Actifs :** actions NYSE, AMEX, Nasdaq ; fonds fermés
- **Plage horaire / Session :** rendement overnight, puis rendement intraday qui suit
- **Date :** 2006 | **Auteurs :** Ben S. Branch, Aixin Ma | **Citations :** 20

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : de l'ouverture à la clôture, juste après la nuit. **Qui subit la contrainte** : le prix d'ouverture, fixé sur un marché mince, qui dépasse sa cible. **Effet sur les bougies** : il y a une **forte autocorrélation négative** entre le rendement de la nuit et celui de la journée qui suit : un gap haussier est suivi d'une journée plutôt baissière, et inversement.

> **Résumé (abstract paraphrasé) :** L'idée vient d'une étude sur les fonds fermés, où la nuit et la journée qui suit sont fortement corrélées négativement. La même autocorrélation négative se retrouve sur les actions des trois places US. Les auteurs y voient une contradiction avec la forme faible de l'efficience.
>
> **Pour nous :** cela va dans le même sens que [6] et que [1] de la session du 2026-10-13 (Yu et al., retournement après la nuit sur les futures Nasdaq-100). C'est mesuré sur des **actions individuelles**. Sur l'indice, il faut le vérifier.

### [8] Price Gap Anomaly in the US Stock Market: The Whole Story

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3461283
- **Actifs :** Dow Jones, S&P 500, Nasdaq
- **Plage horaire / Session :** jour du gap (ouverture différente de la clôture de la veille)
- **Date :** 2019 | **Auteurs :** Alex Plastun, Xolani Sibande, Rangan Gupta, Mark E. Wohar | **Citations :** 2

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le jour du gap, de l'ouverture à la clôture. **Qui subit la contrainte** : les ordres placés avant l'ouverture, qui créent le gap et attirent du suivi de tendance. **Effet sur les bougies** : le jour d'un gap, le prix **continue dans le sens du gap** en moyenne. L'effet est temporaire et ne dépend pas de la saison. 🔴 L'idée que « les gaps se referment toujours » est réfutée.

> **Résumé (abstract paraphrasé) :** Les auteurs étudient les gaps sur les indices US de 1928 à 2018, avec tests statistiques, régressions et simulation de trading. Après un gap, les mouvements sont anormaux et vont dans le sens du gap. Une stratégie fondée dessus bat le hasard.
>
> **Pour nous :** ce résultat **contredit** [6] et [7]. Les deux peuvent être vrais en même temps selon la **taille** du gap ou l'**époque** (1928–2018 contre les 20 dernières années). C'est la variable de conditionnement principale à tester.

### [9] 🧪 Rough Gaps Exist? Opening Gaps Helps To Surge Returns in Swing and Intraday Trading

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4834097
- **Actifs :** S&P 500, Nasdaq
- **Plage horaire / Session :** gap d'ouverture et séance qui suit
- **Date :** 2024 | **Auteurs :** Sagar Baniya | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : après les gros gaps d'ouverture. **Qui subit la contrainte** : les acheteurs ou vendeurs pris à contre-pied par l'excès de l'ouverture. **Effet sur les bougies** : **plus le gap est grand, plus le retracement est fort**. Le lien avec le volume est faible, et le lien avec l'or ou le dollar quasi nul.

> **Résumé (abstract paraphrasé) :** L'échantillon couvre 750 séances de 2019 à 2021 sur le S&P 500 et le Nasdaq. Il y a une corrélation significative entre taille du gap et retournement. Le pouvoir explicatif des variables macro (or, dollar) est faible.
>
> **Pour nous :** l'échantillon est petit et la méthode peu rigoureuse. Ce papier suggère toutefois la même chose que la tension entre [6] et [8] : **les petits gaps continuent, les gros se retracent**. Hypothèse à tester.

### [10] Non-Fundamental Information and Market-Makers' Behavior During the NASDAQ Preopening Session

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2312375
- **Actifs :** actions Nasdaq
- **Plage horaire / Session :** pre-opening, puis retournement après l'ouverture
- **Date :** 2013 | **Auteurs :** Laurence Lescourret | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : avant l'ouverture et dans les minutes qui suivent. **Qui subit la contrainte** : les teneurs de marché grossistes, exposés au risque d'inventaire, qui cotent tôt les jours de gros chocs de liquidité. **Effet sur les bougies** : leur activité avant l'ouverture est liée aux **retournements du prix d'ouverture**, c'est-à-dire à une pression transitoire. Ces jours ne sont pas des jours de vraie nouvelle (résultats, fusions).

> **Résumé (abstract paraphrasé) :** Les cotations de pré-ouverture des grossistes sont liées aux retournements d'ouverture et aux déséquilibres d'ordres de la veille, pas aux annonces fondamentales. Les autres intermédiaires ne montrent pas ce comportement. L'information non fondamentale compte donc pendant le pre-opening.
>
> **Pour nous :** un gap qui vient d'un **déséquilibre de flux** se retourne, alors qu'un gap qui vient d'une **nouvelle** tient. En OHLCV, on peut approximer cela par : gap sans annonce macro à 14h30 contre gap après une annonce.

### [11] The International Evidence of the Overnight Return Anomaly

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1458789
- **Actifs :** indices actions de 29 pays
- **Plage horaire / Session :** nuit contre séance
- **Date :** 2009 | **Auteurs :** Tao Tony Cai, Mei Qiu | **Citations :** 5

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture, puis pendant la séance. **Qui subit la contrainte** : les vendeurs à découvert, freinés par les contraintes de short ; les optimistes fixent alors le prix d'ouverture (hypothèse de Miller, 1977). **Effet sur les bougies** : l'ouverture est surévaluée et le prix **redescend vers l'équilibre pendant la séance**. L'écart est plus grand là où le short est contraint.

> **Résumé (abstract paraphrasé) :** Dans 23 pays sur 29, le rendement de la nuit dépasse celui de la séance et celui de clôture à clôture. Le désaccord entre investisseurs s'accumule pendant la nuit et fait surévaluer l'ouverture. Les marchés contraints sur le short montrent un écart plus fort.

### [12] ⚠️ Retail Ebb and Flow and the Overnight–Intraday Return Gap

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4752520
- **Actifs :** actions coréennes (données de flux par type d'investisseur)
- **Plage horaire / Session :** ouverture (achats nets) et clôture (ventes nettes)
- **Date :** 2024 | **Auteurs :** Yongkil Ahn, Alfred Qi Fan, Don Noh, Stella Yeayeun Park | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : **à l'ouverture**, puis à la clôture. **Qui subit la contrainte** : les particuliers, qui veulent une exposition de jour, **achètent nets à l'ouverture** et revendent à la clôture. **Effet sur les bougies** : l'ouverture est poussée vers le haut et la séance dérive vers le bas. C'est l'écart nuit/jour.

> **Résumé (abstract paraphrasé) :** Avec des données de flux exhaustives, les auteurs montrent que l'intensité du trading des particuliers explique l'écart nuit/jour. La causalité est établie avec un instrument : le prix nominal de l'action. Le mécanisme est renforcé après les journées volatiles.
>
> **Pour nous :** c'est le mécanisme causal le plus net derrière [6] et [11]. Hypothèse à tester sur le Nasdaq : la baisse de la première heure est plus forte le lendemain d'une séance très volatile.

### [13] ⚠️ Does Overnight News Explain Overnight Returns?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5336382
- **Actifs :** marché actions US
- **Plage horaire / Session :** nuit contre séance
- **Date :** 2025 | **Auteurs :** Paul Glasserman, Kriste Krstovski, Paul Laliberte, Harry Mamaysky | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit, puis pendant la séance. **Qui subit la contrainte** : les investisseurs qui réagissent différemment aux mêmes thèmes de news selon qu'elles sortent la nuit ou le jour. **Effet sur les bougies** : une bonne partie de l'écart nuit/jour, et des schémas de **continuation ou de retournement**, s'explique par le type de news.

> **Résumé (abstract paraphrasé) :** À partir de 2,4 millions d'articles et d'une analyse supervisée par thème, les auteurs expliquent une grande part de l'écart nuit/jour. Hors échantillon, la méthode prévoit quelles actions feront bien la nuit et mal en séance. Le signal demande des news, donc il est hors OHLCV.

### [14] New Findings Regarding Return Autocorrelation Anomalies and the Importance of Non-Trading Periods

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=311525
- **Actifs :** actions (marché non précisé dans le résumé)
- **Plage horaire / Session :** clôture à clôture contre ouverture à clôture ; lundi
- **Date :** 2002 | **Auteurs :** Josep García-Blandón | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : les périodes de fermeture (nuit, week-end, jours fériés), surtout le lundi. **Qui subit la contrainte** : le prix d'ouverture, qui intègre avec retard l'information accumulée. **Effet sur les bougies** : l'autocorrélation des rendements journaliers **disparaît** quand on mesure de l'ouverture à la clôture. Elle vient donc entièrement des périodes de fermeture.

> **Résumé (abstract paraphrasé) :** Les rendements de clôture à clôture sont autocorrélés, surtout le lundi. Ceux d'ouverture à clôture ne le sont pas. Les périodes de fermeture expliquent ces anomalies, ce qui est cohérent avec l'idée d'une information traitée lentement.

### [15] Night Moves: Is the Overnight Drift the Grandmother of All Market Anomalies

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4139328
- **Actifs :** marché large, actions, ETF, crypto
- **Plage horaire / Session :** nuit contre jour
- **Date :** 2022 | **Auteurs :** Victor Haghani, Vladimir V. Ragulin, Richard Dewey | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit, puis le jour. **Qui subit la contrainte** : les participants qui portent le risque en séance. **Effet sur les bougies** : depuis au moins 30 ans, 100 % ou plus du rendement est réalisé quand le marché est fermé. Le rendement de jour est nul ou négatif.

> **Résumé (abstract paraphrasé) :** C'est une revue de la douzaine de papiers sur le sujet et des explications proposées (artefact statistique, prime de risque, friction). Elle sert de point d'entrée pour la bibliographie. Le papier de Knuteson ci-dessous en donne une lecture plus polémique.

### [16] Strikingly Suspicious Overnight and Intraday Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3705017
- **Actifs :** grands indices mondiaux
- **Plage horaire / Session :** nuit contre jour
- **Date :** 2020 | **Auteurs :** Bruce Knuteson | **Citations :** 2

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture et pendant la séance. **Qui subit la contrainte** : selon l'auteur, un acteur qui pousse les prix à la hausse par ses achats en séance puis profite de la nuit. Cette explication est controversée. **Effet sur les bougies** : les rendements de nuit sont très positifs et ceux de séance négatifs sur des décennies, avec une constance « suspecte ».

> **Résumé (abstract paraphrasé) :** Les rendements de nuit des grands indices sont fortement positifs et ceux de séance négatifs, de façon très régulière. L'auteur montre que les caractéristiques de ce schéma rendent difficile une explication innocente. Il en déduit la seule explication avancée jusqu'ici.

---

## C. Synthèse : comment augmenter nos chances à 15h30

1. **Le gap n'est pas à prévoir, il est déjà connu** (ES/NQ à 15h29). Selon [1] et [3], les marchés étrangers n'apportent pas d'information au-delà des futures US. Il faut donc travailler sur **la direction de 15h30 à 16h30 sachant le gap**.
2. **Biais de base** : en moyenne, l'ouverture est trop haute et la première heure baisse [6] [11] [12] [16]. L'avantage est faible mais documenté sur des décennies et dans de nombreux pays.
3. **Conditionnement principal : la taille du gap.** Les petits gaps continuent [8] et les gros se retracent [7] [9]. Variable à tester : gap / ATR(14), en déciles.
4. **Qualité du gap** : un gap construit tard dans le pre-market, dans un marché profond et après une annonce macro de 14h30 tient mieux. Un gap fait la nuit dans un marché mince ou sur un déséquilibre de flux se corrige [2] [5] [10].
5. **Cas particulier** : la réouverture après un jour férié US où l'Europe a coté. Une partie du rattrapage se fait **après** l'ouverture [4].

**Test proposé** (OHLCV seulement, futures ES/NQ à la minute) :
- **Variables :** gap = ouverture à 15h30 / clôture à 22h00 la veille ; normalisé par l'ATR ; part du gap faite entre 14h30 et 15h30 ; rendement de la séance de la veille ; jour suivant une séance très volatile ; présence d'une annonce macro à 14h30.
- **Cible :** signe du rendement de 15h30 à 16h00, et de 15h30 à 16h30.
- **Protocole :** pré-enregistrer les hypothèses, comme pour les tests FX.

### Résumé introuvable, à revoir (SSRN bloque l'accès automatique)
- Cycles of Declines and Reversals following Overnight Market Declines (Abdi) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3287680
- Overnight Reversal and the Asymmetric Reaction to News (Dangl, Salbrechter) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4307675
- Risk and Return Around the Clock (Fattinger, Ziegler) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2606706
- Are Extended Hours Prices Predictive of Subsequent Stock Returns? (Levi, Livnat, Zhang, Zhang) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2809950
- Day and Night Expected Returns Under Overnight Information Shocks: New Tug-of-War Pattern (Bahcivan) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5247123
- The Economic Value of Conditioning on Overnight Information (Tsiakas) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=676705
