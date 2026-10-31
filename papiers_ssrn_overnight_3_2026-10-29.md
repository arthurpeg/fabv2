# Papiers SSRN : l'overnight, troisième série, centrée sur la session asiatique (indices US, FX majeurs, or)

*Session du 2026-10-29 (deuxième passe). Suite de [papiers_ssrn_overnight_2026-10-21.md](papiers_ssrn_overnight_2026-10-21.md) et [papiers_ssrn_overnight_2_2026-10-29.md](papiers_ssrn_overnight_2_2026-10-29.md). Le quota OpenAlex du jour étant épuisé, la recherche passe par l'**API Crossref filtrée sur les DOI SSRN** (`prefix:10.2139`) : 50 requêtes, environ 4 900 candidats triés par titre. Résumés venant de Crossref et de Semantic Scholar, **paraphrasés en français**. Tous les papiers déjà fournis (voir [papers/seen_papers.json](papers/seen_papers.json)) sont exclus.*

**Mots-clés ajoutés pour la session asiatique** : Asian session, Asian trading session returns, Asian hours returns, Asian anomaly, Asian trading hours, Tokyo session, Tokyo trading hours, Tokyo opening, Tokyo fix, Gotobi, Sydney session, Hong Kong trading session, Asia/Europe/America trading sessions, trading sessions returns decomposition, time zone returns, Shanghai gold, Shanghai Gold Exchange, Shanghai crude oil futures, gold price Asian demand, Asian markets / US futures overnight, Nikkei futures overnight, Japan/US time difference, yen intraday, USD/JPY intraday, currency returns Asian time, exchange rate Tokyo/London/New York, Osaka night session, SGX Nikkei futures, overnight transmission Asia. Les mots-clés overnight des deux séries précédentes ont été relancés sur Crossref.

**Légende** : 🔴 échec ou condition limite · ⚠️ le signal dépend d'une donnée non OHLCV (flux, interventions, VIX) ou d'un marché hors périmètre · 🧪 papier SSRN récent d'auteur indépendant, non relu par des pairs

---

## 0. Ce que « session asiatique » veut dire selon l'actif

- **FX majeurs** : la session asiatique va d'environ **1h00 à 9h00** heure de Paris (Sydney puis Tokyo, Hong Kong, Singapour). C'est la « nuit » européenne et américaine. Pour EUR, GBP et CHF, c'est la session **étrangère** ; pour JPY et AUD, c'est la session **domestique**.
- **Or** : Tokyo, Hong Kong et Shanghai (Shanghai Gold Exchange, futures SHFE) cotent pendant cette session. La série du 2026-10-21 ([21], Wei) montrait que la session asiatique a porté l'essentiel de la hausse de l'or depuis 2024.
- **Indices US** : la session asiatique correspond à la partie 0h00–8h00 Paris de la nuit des futures ES/NQ. La question est double : la clôture de New York prédit-elle l'Asie, et l'Asie prédit-elle le reste de la nuit US ?
- **Pétrole** : 🔴 aucun papier SSRN exploitable sur le pétrole en session asiatique (Shanghai crude oil futures : uniquement des papiers de volatilité sur le marché chinois, hors périmètre).

⚠️ **Heure d'hiver** : l'Europe est passée à l'heure d'hiver le 25 octobre, les États-Unis le font le 1er novembre 2026. La session de Tokyo (9h00–15h00 JST) correspond à **1h00–7h00** heure de Paris en hiver.

---

## A. FX : qui porte le rendement pendant la session asiatique ?

### [1] Currency Returns in Different Time Zones

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2613592
- **Actifs :** devises européennes contre dollar (EUR, GBP, CHF…), devises G10
- **Plage horaire / Session :** heures ouvrées US contre heures ouvrées du pays étranger
- **Date :** 2015 | **Auteurs :** Zhengyang Jiang | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant les heures ouvrées américaines (environ 14h00–22h00 Paris). **Qui subit la contrainte** : les investisseurs américains, qui exigent une **prime de risque plus élevée** pour détenir des devises étrangères risquées pendant les heures où arrivent les nouvelles sur la croissance US. **Effet sur les bougies** : les devises européennes **montent** en moyenne pendant les heures US et **baissent** pendant les heures du pays étranger. L'écart est plus grand pour les devises plus risquées et quand le change est plus volatil.

> **Résumé (abstract paraphrasé) :** Les devises européennes ont des rendements moyens positifs pendant les heures ouvrées américaines et négatifs pendant les heures étrangères. L'auteur propose une explication par le risque : les nouvelles sur la croissance US arrivent surtout pendant les heures US. L'écart s'élargit avec l'exposition au risque et la volatilité. Le résultat relie les rendements par fuseau horaire aux primes de risque des devises.
>
> **Pour nous :** c'est la version « prime de risque » du résultat de Ranaldo (fourni le 2026-10-11 : la devise domestique se déprécie pendant ses propres heures). Test direct : rendement EURUSD et GBPUSD de 14h00 à 22h00 Paris contre de 9h00 à 14h00, par année, et contre la session asiatique (1h00–9h00).

### [2] Housewives of Tokyo versus the Gnomes of Zurich: Measuring Price Discovery in Sequential Markets

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1343399
- **Actifs :** AUD, JPY, EUR, GBP contre USD (8 ans, 24h/24)
- **Plage horaire / Session :** quatre marchés successifs par fuseau horaire (Asie, Europe, Amérique…)
- **Date :** 2009 | **Auteurs :** Jian-Xin Wang, Minxian Yang | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : dans chaque session, l'une après l'autre. **Qui subit la contrainte** : les institutionnels européens et américains, qui dominent la formation du prix. **Effet sur les bougies** : l'**Europe** reste la session la plus informative pour les quatre paires. L'**Asie** gagne en part d'information sur EUR et GBP mais en **perd** sur AUD et JPY. 🔴 L'influence des « ménagères de Tokyo » (particuliers japonais) sur le prix est **surestimée**.

> **Résumé (abstract paraphrasé) :** Un modèle VAR structurel identifie, dans des marchés qui se succèdent selon les fuseaux horaires, la contribution de chaque session à la découverte du prix (part d'information de Hasbrouck). Appliqué à quatre paires sur huit ans, il montre que l'Europe domine, que l'Asie progresse sur EUR et GBP et recule sur AUD et JPY. Le marché des changes reste dominé par les institutionnels d'Europe et des États-Unis.
>
> **Pour nous :** la session asiatique compte peu dans le prix final, même pour USDJPY. Un mouvement de session asiatique a donc plus de chances d'être **corrigé** à l'ouverture européenne. Hypothèse à tester : retournement à 9h00–11h00 Paris d'un fort mouvement 1h00–9h00.

### [3] Asymmetric Information and Price Discovery in the FX Market: Does Tokyo Know More About the Yen?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=138495
- **Actifs :** USD/JPY
- **Plage horaire / Session :** session de Tokyo, quand les traders informés y sont concentrés
- **Date :** 1999 | **Auteurs :** Vicentiu Covrig, Michael Melvin | **Citations :** 3

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant certaines périodes de la session de Tokyo où des traders japonais informés sont actifs. **Qui subit la contrainte** : les teneurs de marché du reste du monde, qui suivent les cotations de Tokyo. **Effet sur les bougies** : quand les informés sont actifs, le prix rejoint son niveau d'information complète **six fois plus vite**, et les cotations japonaises **mènent** le reste du marché. Le reste du temps, la causalité va dans les deux sens.

> **Résumé (abstract paraphrasé) :** Les auteurs repèrent une période où des traders informés sur le yen sont concentrés à Tokyo. Les cotations s'ajustent alors six fois plus vite, Tokyo mène le marché, et sa part dans la découverte du prix monte de 5 à 12 points. En temps normal, l'information est publique et les cotations du monde entier évoluent ensemble.
>
> **Pour nous :** nuance [2] : la session de Tokyo peut mener le yen, mais seulement par épisodes (par exemple avant des annonces japonaises). Hors de ces épisodes, pas d'avantage à Tokyo.

### [4] 🧪 Currency Returns and Price Discovery around Global FX Fixings

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7388124
- **Actifs :** les neuf devises les plus échangées, rendements horaires sur 21 ans
- **Plage horaire / Session :** autour des fixings (dont le fixing de **Tokyo** à 9h55 JST, le fixing WM/Reuters de Londres à 16h00)
- **Date :** 2026 | **Auteurs :** Karo He | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : avant et après chaque fixing mondial. **Qui subit la contrainte** : les teneurs de marché FX, qui accumulent du stock en servant les ordres au fixing et doivent ensuite le liquider. **Effet sur les bougies** : un profil en **W** : le dollar **monte avant** les fixings et **baisse après**. Les retournements sont fréquents et significatifs pour toutes les grandes devises ; leur moment dépend des heures de publication des taux de référence.

> **Résumé (abstract paraphrasé) :** L'étude cherche un profil en W sur le dollar autour des fixings, à partir des rendements horaires de neuf devises sur 21 ans. Les retournements autour des fixings sont fréquents et significatifs. Leur calendrier suit la publication des taux de référence. La cause serait le risque d'inventaire pris par les teneurs de marché.
>
> **Pour nous :** c'est une réplication indépendante de Krohn-Mueller-Whelan (fourni le 2026-10-11). Pour la session asiatique, la barre à surveiller est celle du **fixing de Tokyo** (1h55 Paris en hiver, 2h55 en été) : dollar fort avant, plus faible après. Le jour de **Gotobi** (5, 10, 15, 20, 25, 30 du mois), la demande de dollars des importateurs japonais au fixing est réputée plus forte : variable calendaire à ajouter.

### [5] Returns and Volatility Spillovers in the Currency Futures Markets: The Case of the German Mark and the Japanese Yen

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=976570
- **Actifs :** futures sur DEM et JPY à l'IMM (Chicago) et au SIMEX (Singapour)
- **Plage horaire / Session :** séance de Chicago puis séance de Singapour (fuseaux qui ne se chevauchent pas)
- **Date :** 2007 | **Auteurs :** Wan Mansor Wan Mahmood | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture de Singapour, après la séance de Chicago. **Qui subit la contrainte** : le marché asiatique, plus petit, qui reprend l'information du marché américain plus gros. **Effet sur les bougies** : la volatilité se transmet **seulement de Chicago vers Singapour**, pas dans l'autre sens.

> **Résumé (abstract paraphrasé) :** L'étude mesure par des modèles GARCH les transmissions de volatilité entre futures sur devises de l'IMM et du SIMEX. Elle ne trouve de transmission forte que de l'IMM vers le SIMEX, pour les deux devises. Le marché avec le plus de volume détermine le sens de la transmission.
>
> **Pour nous :** cohérent avec [2] : la session asiatique **suit** plus qu'elle ne mène. La volatilité de la séance US prévoit celle de la session asiatique, pas l'inverse.

### [6] ⚠️ Foreign Exchange Interventions, Information, and Intraday Market Dynamics: Evidence from Japan

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6832400
- **Actifs :** USD/JPY, données à la minute (2008–2024)
- **Plage horaire / Session :** autour des interventions de la Banque du Japon (souvent en session asiatique)
- **Date :** 2026 | **Auteurs :** Opale Guyot, Heather Anne Montgomery | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : avant et après une intervention de la Banque du Japon (heure non publiée, retrouvée par méthode bayésienne). **Qui subit la contrainte** : les traders qui anticipent l'intervention sans savoir quand elle aura lieu. **Effet sur les bougies** : la volatilité **monte avant** l'intervention, puis se calme juste après. Le prix bouge dans le sens voulu et **reste déplacé** une bonne partie de la journée : la transmission passe par l'information, pas par un simple effet d'inventaire temporaire.

> **Résumé (abstract paraphrasé) :** L'étude regarde comment les interventions japonaises se transmettent au yen à travers la microstructure, plutôt que leur efficacité sur le niveau. Elle retrouve l'heure des interventions réelles et verbales. Le profil est régulier : volatilité qui monte avant, stabilisation après, niveau déplacé durablement.
>
> **Pour nous :** sur USDJPY, une forte barre de baisse en session asiatique avec volume, après une montée de volatilité, peut signaler une intervention ; dans ce cas, **ne pas parier sur le retournement** dans la journée.

### [7] ⚠️ Overnight Price Discovery and the Internationalization of a Currency: The Case of the Korean Won

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1972641
- **Actifs :** KRW/USD (marchés onshore de Séoul et offshore la nuit)
- **Plage horaire / Session :** nuit coréenne (offshore) contre séance de Séoul
- **Date :** 2011 | **Auteurs :** Jian-Xin Wang | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant la nuit asiatique, sur les marchés offshore (Londres, New York). **Qui subit la contrainte** : le marché domestique, dont le prix est de plus en plus fixé ailleurs. **Effet sur les bougies** : la part de la découverte du prix faite **la nuit offshore** est passée de moins de 10 % (1999–2000) à plus de 50 % (2011–2012).

> **Résumé (abstract paraphrasé) :** L'auteur mesure l'internationalisation d'une devise par la part de la découverte du prix faite la nuit sur les marchés offshore. Pour le won, cette part a fortement augmenté. Ses variations suivent l'efficience du marché de nuit et l'apprentissage des investisseurs.
>
> **Pour nous :** hors des majeures, mais même méthode et même message que [2] : la session domestique asiatique perd de l'importance au profit de l'Europe et des États-Unis.

---

## B. Or : Tokyo, Londres, New York

### [8] Dynamic Conditional Correlation and Volatility Distributions in Tokyo, London, and New York Gold Markets

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5167870
- **Actifs :** or à Tokyo, Londres et New York (1993–2012)
- **Plage horaire / Session :** sessions successives Tokyo → Londres → New York
- **Date :** 2025 | **Auteurs :** Tuan Lai | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : d'une session à l'autre. **Qui subit la contrainte** : la session de **New York**, qui reçoit la variance de Tokyo. **Effet sur les bougies** : New York reprend la **volatilité de Tokyo**, mais Tokyo n'est pas influencé par New York. Londres et Tokyo, comme Londres et New York, ont des corrélations comparables : aucune place ne domine. Plus la corrélation est élevée, plus le risque est grand.

> **Résumé (abstract paraphrasé) :** Un modèle DCC estime corrélations et volatilités de l'or entre les trois places sur 1993–2012. La corrélation Londres-New York monte avec la volatilité. Les trois places sont à peu près équivalentes. New York subit un effet de débordement de la variance de Tokyo, pas l'inverse. Les corrélations sont plus sensibles aux seuils de volatilité extrêmes à Londres et New York.
>
> **Pour nous :** avant 2012 déjà, la session asiatique comptait pour la volatilité de l'or. Variable OHLCV : la volatilité réalisée XAUUSD de 1h00 à 9h00 Paris prévoit-elle celle de la séance US (14h30–22h00) ? Cela complète [21] de la série du 2026-10-21 (rendement de l'or concentré en session asiatique depuis 2024).

---

## C. Indices : l'Asie entre la clôture de New York et l'ouverture suivante

### [9] 🧪 Do Bulls and Bears Move across Borders? The t-0.5 Framework and International Information Transmission to Asia-Pacific Markets

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7019738
- **Actifs :** Nikkei 225 et indices Asie-Pacifique ; variables US (S&P 500, VIX…)
- **Plage horaire / Session :** clôture de New York (6h00 JST) → ouverture de Tokyo (t ≈ 0,5)
- **Date :** 2026 | **Auteurs :** Ryo Kinoshita | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture de Tokyo, 3 heures après la clôture de New York. **Qui subit la contrainte** : le marché japonais, fermé pendant la séance US, qui doit l'intégrer d'un coup. **Effet sur les bougies** : la clôture de New York prédit le **sens** du Nikkei le lendemain avec une précision de **67,8 %** hors échantillon (2021–2023). La principale variable est le rendement du S&P 500.

> **Résumé (abstract paraphrasé) :** C'est le premier papier de la série de Kinoshita (les deux suivants ont été fournis le 2026-10-14 et aujourd'hui). Il définit la clôture de New York comme t = 0 et l'ouverture de Tokyo comme t ≈ 0,5. Une régression logistique glissante prédit le Nikkei avec 67,8 % de précision ; une règle triviale sur le signe du VIX fait presque aussi bien (69,4 %). Le S&P 500 est la variable la plus importante.
>
> **Pour nous :** ⚠️ le VIX est hors périmètre, mais le rendement du S&P 500 suffit presque. Ce papier montre que **la séance US explique l'Asie**, ce qui va avec le résultat négatif du papier de la même série fourni le 2026-10-14 ([3] : l'Asie n'apporte rien sur l'ouverture US). Le sens d'information est **US → Asie**, pas l'inverse.

### [10] Feedback Trading: Strategies during Day and Night with Global Interconnectedness

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3275317
- **Actifs :** plusieurs grands marchés actions interconnectés
- **Plage horaire / Session :** rendements de jour contre rendements de nuit, avec débordements entre pays
- **Date :** 2018 | **Auteurs :** Alex Kusen, Markus Rudolf | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : séparément le jour et la nuit. **Qui subit la contrainte** : les feedback traders (qui achètent après une hausse et vendent après une baisse), dont le comportement change selon la période et selon le marché étranger qui vient de bouger. **Effet sur les bougies** : les stratégies de feedback (suivi de tendance ou contrarian) **diffèrent** entre jour et nuit et selon les marchés.

> **Résumé (abstract paraphrasé) :** Le papier découpe la prime de rendement en jour et nuit et introduit un modèle de feedback trading global qui suppose des liens entre pays. Le comportement de feedback n'est pas le même le jour et la nuit, et il change selon les interactions entre marchés.

### [11] Is Risk Higher during Non-Trading Periods? The Risk Trade-Off for Intraday versus Overnight Market Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2494387
- **Actifs :** grands indices US, France, Allemagne, **Japon**
- **Plage horaire / Session :** nuit contre séance
- **Date :** 2014 | **Auteurs :** Christoph Riedel, Niklas F. Wagner | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit. **Qui subit la contrainte** : le porteur de position pendant la fermeture, qui ne peut pas couper son risque. **Effet sur les bougies** : les innovations de nuit ont un **risque de queue significatif**, celles de séance non. Le risque de baisse de nuit combine une volatilité modérée et un risque de queue important.

> **Résumé (abstract paraphrasé) :** Avec un GARCH et une loi de Pareto généralisée pour les queues, les auteurs comparent le risque de nuit et de séance sur les indices US, français, allemands et japonais. Seule la nuit a des queues épaisses significatives. Une mesure de risque fondée sur la volatilité seule sous-estime fortement le risque de baisse de nuit.
>
> **Pour nous :** même conclusion que Kang-Babbs (série 2) : pour une position tenue la nuit, dimensionner sur la **VaR de queue** du gap, pas sur l'ATR.

---

## D. Indices US : mécanismes du rendement de nuit (compléments)

### [12] Night Trading: Lower Risk But Higher Returns?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2633476
- **Actifs :** actions US
- **Plage horaire / Session :** clôture → ouverture, investissement uniquement de nuit
- **Date :** 2015 (publié Review of Financial Economics) | **Auteurs :** Marie-Eve Lachance | **Citations :** 5

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit. **Qui subit la contrainte** : non identifié précisément ; l'auteure parle de **biais récurrents** propres à chaque titre. **Effet sur les bougies** : un cinquième des titres ont un biais de nuit positif et significatif. Les détenir **seulement la nuit** l'année suivante rapporte **deux fois le rendement du marché** pour **un tiers du beta**. Ces mêmes titres ont des rendements de séance négatifs.

> **Résumé (abstract paraphrasé) :** Les rendements de nuit ont des biais très persistants. Un modèle qui en tient compte identifie les titres à biais de nuit positif. Investir la nuit dans ces titres l'année suivante bat le marché avec moins de risque. Les coûts et la mise en œuvre sont discutés.
>
> **Pour nous :** la **persistance** du biais d'une année sur l'autre est l'élément testable : le biais de nuit de NQ et ES sur l'année N prédit-il celui de l'année N+1 ?

### [13] Overnight Returns and Firm-Specific Investor Sentiment

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2554010
- **Actifs :** actions US
- **Plage horaire / Session :** nuit, persistance sur quelques jours puis retournement à long terme
- **Date :** 2015 (publié JFQA 2018) | **Auteurs :** David Aboody, Omri Even-Tov, Reuven Lehavy, Brett Trueman | **Citations :** 240

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture, plusieurs jours de suite. **Qui subit la contrainte** : les particuliers influencés par le sentiment, dont la demande persiste quelques jours. **Effet sur les bougies** : les rendements de nuit sont **persistants à court terme** (une nuit forte est suivie d'autres nuits fortes), surtout pour les titres difficiles à évaluer. À long terme, les titres à forte nuit **sous-performent** : la surévaluation est temporaire.

> **Résumé (abstract paraphrasé) :** Les auteurs testent si le rendement de nuit peut servir de mesure du sentiment au niveau d'un titre. Il est persistant à court terme, plus encore pour les titres difficiles à évaluer, et suivi d'un retournement à plus long terme. Ce sont les propriétés attendues d'une mesure de sentiment.
>
> **Pour nous :** variable OHLCV : somme des rendements de nuit sur 5 jours. Hypothèse sur NQ : persistance de la nuit à court terme, retournement sur un mois.

### [14] The Cross-Section of Intraday and Overnight Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2869624
- **Actifs :** actions US (anomalies classiques)
- **Plage horaire / Session :** séance, **fin de séance**, nuit
- **Date :** 2016 (publié JFE 2021) | **Auteurs :** Vincent Bogousslavsky | **Citations :** 2

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : en **fin de séance**, avant la nuit. **Qui subit la contrainte** : les arbitragistes, qui paient des **marges plus élevées la nuit** et des frais de prêt facturés seulement sur les positions tenues la nuit. Ils réduisent donc leurs positions avant la clôture. **Effet sur les bougies** : un facteur de mauvaise valorisation gagne pendant la séance mais **perd en fin de séance**. L'effet s'est renforcé dans la seconde moitié de l'échantillon et touche plusieurs anomalies connues.

> **Résumé (abstract paraphrasé) :** Les exigences de marge plus fortes la nuit et les frais de prêt incitent les arbitragistes à réduire leurs positions avant la fin de la journée. Un facteur de mauvaise valorisation rapporte pendant la journée mais performe mal à la clôture. Le schéma se renforce dans le temps.
>
> **Pour nous :** mécanisme qui relie la **dernière demi-heure** et la nuit. Sur l'indice, la réduction des positions avant la nuit est un flux de fin de séance (cohérent avec Overnight Drift : le déséquilibre de la clôture est porté par les teneurs de marché pendant la nuit).

### [15] Intraday Market Making with Overnight Inventory Costs

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2844881
- **Actifs :** marché des Treasuries US (firmes de trading pour compte propre)
- **Plage horaire / Session :** fin de séance, avant la nuit
- **Date :** 2016 | **Auteurs :** Tobias Adrian, Agostino Capponi, Michael J. Fleming, Erik Vogt, Hongzhong Zhang | **Citations :** 2

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'approche de la clôture. **Qui subit la contrainte** : les teneurs de marché à capital limité, qui doivent finir la journée **presque à plat** car garder du stock la nuit coûte cher. **Effet sur les bougies** : les **spreads s'élargissent** à l'approche de la clôture ; plus d'ordres n'implique pas toujours plus de volatilité.

> **Résumé (abstract paraphrasé) :** Le marché des Treasuries est très intermédié par des firmes de trading à capital limité, obligées de finir la journée à plat. Un modèle de tenue de marché avec coût de stock de nuit donne des politiques de prix explicites. Les coûts de transaction augmentent à l'approche de la clôture, comme le prévoit le modèle.
>
> **Pour nous :** c'est le **modèle théorique** derrière l'Overnight Drift : un coût de stock de nuit force la liquidation en fin de séance et crée une prime pour qui porte le risque la nuit. Les Treasuries sont hors périmètre, mais le mécanisme s'applique aux futures sur indices.

---

## E. Ouverture asiatique et heures étendues

### [16] Overnight Public Information, Order Placement and Price Discovery During the Pre-Opening Period

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1785682
- **Actifs :** actions de l'Australian Securities Exchange
- **Plage horaire / Session :** pre-opening de Sydney (première place de la session asiatique)
- **Date :** 2011 | **Auteurs :** Fariborz Moshirian, Lily Nguyen, Peter Kien Pham | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant le pre-opening, après des nouvelles publiées la nuit. **Qui subit la contrainte** : les donneurs d'ordres, plus agressifs quand il y a beaucoup de nouvelles. **Effet sur les bougies** : les nouvelles de **nuit** sont intégrées **immédiatement** à l'ouverture, alors que les nouvelles publiées **en séance** sont intégrées progressivement.

> **Résumé (abstract paraphrasé) :** Les annonces d'entreprises publiées la nuit rendent les prix d'ouverture indicatifs plus efficients et rendent les ordres de pré-ouverture plus agressifs. En comparant les résultats publiés la nuit et en séance, les auteurs montrent que les prix réagissent immédiatement aux premiers et lentement aux seconds.
>
> **Pour nous :** une nouvelle de nuit est « déjà dans le gap » ; une nouvelle en séance laisse de la place à une tendance. Cohérent avec le papier Bitcoin de la série du 2026-10-21.

### [17] Effective Extension of Trading Hours

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2839631
- **Actifs :** marché simulé (modèle multi-agents)
- **Plage horaire / Session :** pre-market et after-hours ajoutés à la séance régulière
- **Date :** 2016 | **Auteurs :** Kotaro Miwa | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant les sessions étendues et à l'ouverture de la séance régulière. **Qui subit la contrainte** : les rares participants des sessions étendues, qui créent un marché illiquide. **Effet sur les bougies** : si la participation est faible, les sessions étendues **concentrent le trading à l'ouverture**, écartent le prix de sa valeur et réduisent la stabilité. Un **pre-market court** est la seule extension qui améliore l'efficience dans tous les cas.

> **Résumé (abstract paraphrasé) :** Avec un modèle multi-agents, l'auteur teste quelles extensions d'horaires améliorent l'efficience et la stabilité des prix. Les sessions étendues peu fréquentées nuisent à la séance régulière ; plus elles sont longues, pire c'est. Le pre-market est bien plus utile que l'after-hours.
>
> **Pour nous :** papier de simulation, cohérent avec les résultats empiriques (Barclay-Hendershott, Chen-Yu-Zivot) : le pre-market est informatif, l'after-hours ne l'est pas.

### [18] Does Investor Time Zone Difference Affect Trading Behaviour?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4247375
- **Actifs :** actions d'une même bourse, particuliers de fuseaux horaires différents
- **Plage horaire / Session :** séance, selon le fuseau de l'investisseur
- **Date :** 2022 | **Auteurs :** Anil Gautam, Grace Lepone | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant la séance, selon l'heure locale de l'investisseur. **Qui subit la contrainte** : les particuliers situés à l'ouest de la bourse (pour eux, c'est plus tôt le matin, avec moins de sommeil). **Effet sur les bougies** : ils passent des ordres **moins agressifs**. L'agressivité sans information nuit à leur performance.

> **Résumé (abstract paraphrasé) :** Les particuliers d'un même marché mais de fuseaux différents n'ont pas la même agressivité. Ceux qui sont « en retard » sur l'heure de la bourse sont moins agressifs. L'effet d'un décalage permanent diffère de celui, temporaire, du passage à l'heure d'été.
>
> **Pour nous :** intérêt limité. À garder en tête pour la semaine de décalage d'horaire (en ce moment même) : le comportement des acteurs change quand l'heure locale change.

---

## F. Synthèse : la session asiatique, ce qui est testable en OHLCV

1. **FX** : la session asiatique **suit** plus qu'elle ne mène [2] [5] [7], sauf épisodes d'information japonaise [3] ou d'intervention [6]. Les devises européennes montent pendant les heures US et baissent pendant leurs propres heures [1].
2. **Fixing de Tokyo** : le dollar monte avant et baisse après les fixings [4], à tester sur la barre de 1h55 Paris, avec un effet attendu plus fort les jours de **Gotobi**.
3. **Or** : la volatilité de la session de Tokyo se transmet à New York [8] ; le rendement est concentré en Asie depuis 2024 (série du 2026-10-21).
4. **Indices** : l'information va de **New York vers l'Asie** [9], pas dans l'autre sens. La nuit a des queues épaisses [11].
5. **Mécanisme de la nuit US** : les teneurs de marché et arbitragistes doivent finir à plat [14] [15], ce qui crée une prime pour la nuit ; le biais de nuit persiste d'une année sur l'autre [12] et à court terme [13].

**Tests proposés** (à pré-enregistrer) :
- **H8 (FX par fuseau)** : rendement moyen EURUSD et GBPUSD par bloc 1h–9h / 9h–14h / 14h–22h Paris, par année. Attendu : positif en heures US, négatif en heures européennes [1].
- **H9 (retournement après la session asiatique)** : si |rendement 1h–9h| > 1 écart-type de la session, rendement de 9h00 à 11h00 Paris de signe opposé ? (USDJPY, EURUSD, XAUUSD) [2].
- **H10 (fixing de Tokyo et Gotobi)** : rendement USDJPY de 1h00 à 1h55 Paris contre 1h55 à 3h00, jours de Gotobi contre autres jours [4].
- **H11 (persistance du biais de nuit)** : corrélation entre le rendement de nuit moyen de NQ/ES sur l'année N et celui de l'année N+1 [12].

### Résumé introuvable, à revoir
- Bidirectional Spillovers from Shanghai Gold Futures to London and New York Gold Markets — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5216421
- Overnight Returns Following Large Price Movements (Lin, Lin, Huang, Lin) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573576
- A Tug of War across the Market: Overnight-vs-Daytime Lead-Lag Networks and Clustering-Based Portfolio Strategies — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5371952
- Overnight News and Daily Equity Trading Risk Limits — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2065017
- Les 15 papiers listés à la fin de la série 2 restent à revoir.
