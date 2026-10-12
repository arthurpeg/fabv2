# Mécanismes causaux en trading intraday (OHLCV uniquement)
### Indices US · Forex majeurs · Pétrole · Or. Chaînes de papiers (SSRN / OpenAlex) et conditions d'échec

*Recherche du 2026-10-11. Source principale : API OpenAlex (source SSRN = `S4210172589`). Les chaînes ont été remontées avec `referenced_works` (références citées) et descendues avec `cites:` (papiers qui citent). Les résumés viennent d'OpenAlex, et à défaut de Crossref ou Semantic Scholar. SSRN bloque l'accès direct (vérification anti-bot), donc aucun PDF n'a été lu : tout repose sur les résumés.*

---

## 0. Méthode et lecture

**Filtre OHLCV.** Je n'ai retenu que les mécanismes dont le **signal** se calcule avec des barres OHLCV (rendements par tranche horaire, gap overnight, range d'ouverture, VWAP, volume relatif, heure de la journée). Si un papier *explique* l'effet avec des données externes (gamma des options, VIX, flux d'ordres) alors que son signal reste OHLCV, je le garde et je le marque ⚠️. On peut trader le signal, mais on ne peut pas observer directement la cause.

**Légende**
- 🟢 papier qui établit ou étend le mécanisme
- 🔴 papier qui montre un échec ou une condition limite
- ⚠️ l'explication causale demande des données non OHLCV
- 📄 papier SSRN (DOI `10.2139/ssrn.*`)
- ❓ résumé absent de toutes les API : le contenu décrit vient du titre et de ma connaissance du papier, **à vérifier**
- 🧪 papier SSRN récent (2026) d'auteur indépendant, non relu par des pairs. Utile comme réplication, mais à pondérer.

Identifiants : `W…` = ID OpenAlex (`https://openalex.org/W…`).

---

## 1. Momentum intraday de marché (« le début de séance prédit la dernière demi-heure »)

**Signal OHLCV** : r₁ = rendement de la clôture J-1 à la fin de la 1ʳᵉ demi-heure (ou de la clôture J-1 jusqu'à 15h30) → prédit r_last = rendement de la dernière demi-heure, dans le même sens.

**Causalité proposée, dans l'ordre d'apparition** :
1. Rééquilibrage peu fréquent et traders informés tardivement (Gao et al.)
2. Aversion des fournisseurs de liquidité au risque overnight (Elaut et al., FX)
3. Couverture gamma des teneurs de marché d'options et des ETF à levier : les dealers short gamma achètent la hausse et vendent la baisse avant la clôture (Baltussen et al.) ⚠️
4. Liquidité faible, volatilité haute, information discrète (Li, Sakkas, Urquhart)

### 1.a Chaîne d'évolution (du plus ancien au plus récent)

| Année | Papier | Actifs | Apport et évolution du mécanisme |
|---|---|---|---|
| 2011/12 | 🟢 Moskowitz, Ooi, Pedersen, *Time series momentum* (W3124639629) | 58 futures | Ancêtre en fréquence mensuelle : le rendement passé d'un actif prédit son propre rendement futur. |
| 2010 | 🟢 Heston, Korajczyk, Sadka, *Intraday Patterns in the Cross-section of Stock Returns* (W3121894513) | Actions US | Continuation à la même demi-heure les jours suivants. Le reversal très court terme vient de déséquilibres de liquidité de moins d'une heure et du bid-ask bounce. |
| 2014 | 🟢📄 Gao, Han, Li, Zhou, *Market Intraday Momentum* (SSRN 10.2139/ssrn.2440866, W2584318538). Version JFE 2018 : W3123013550 | SPY 1993-2013, 10 autres ETF, futures d'indices | **Papier fondateur.** La 1ʳᵉ demi-heure (overnight inclus) prédit la dernière. L'effet est plus fort les jours volatils, à fort volume, en récession et lors des annonces macro. |
| 2015/16 | 🟢📄 Elaut, Frömmel, Lampaert, *Intraday Momentum in FX Markets* (ssrn.2694985, W2176059366 ; JFM 2016 W3125300284) | RUB-USD 2005-2014 | Premier transfert au FX. La cause n'est **pas** le trading informé mais l'aversion au risque overnight des fournisseurs de liquidité. |
| 2019/20 | 🟢📄 Wen, Gong, Ma, Xu, *Intraday Momentum: Evidence from the Crude Oil Market* (ssrn.3416022, W2994693740 ; Econ. Modelling 2020 W3010884068) | USO 2006-2018 | Pétrole : **seule** la 1ʳᵉ demi-heure prédit, et sa composante overnight porte l'essentiel de l'information. Effet plus fort en crise, sur volatilité élevée, volume élevé, gros overnight et sauts. Le profil de volume est propre au pétrole (annonces de stocks). |
| 2020 | 🟢 Xu, Bouri, Saeed, Wen, *Intraday return predictability: commodity ETFs* (W3084072443) | **Or (GLD)**, argent, pétrole | Le mécanisme existe sur l'or, mais **la demi-heure prédictive n'est pas forcément la première** : elle dépend du marché. Effet plus fort les jours volatils et avec sauts. |
| 2021 | 🟢 Li, Sakkas, Urquhart, *Intraday time series momentum: Global evidence* (W3121499907) | 16 marchés développés | Effet confirmé in-sample et out-of-sample. **Plus fort quand la liquidité est faible, la volatilité haute et l'information discrète** : à la fois microstructure et comportement. |
| 2021 | 🟢⚠️📄 Baltussen, Da, Lammers, Martens, *Hedging Demand and Market Intraday Momentum* (ssrn.3760365, W3129336974 ; JFE W3106590193) | Plus de 60 futures (actions, taux, **matières premières, devises**), 1974-2020 | **Généralisation « partout ».** Le prédicteur devient tout le rendement de la clôture J-1 à 15h30. Cause : couverture gamma. **L'effet se retourne les jours suivants.** |
| 2022 | 🟢 Wen, Indriawan, Lien, Xu, *Crude oil: role of EIA inventory announcements* (W4289515728) | Pétrole | Raffinement calendaire : le mercredi (EIA à 10h30 ET), c'est la **3ᵉ** demi-heure qui prédit la dernière. Les autres jours, seule la 1ʳᵉ prédit. |
| 2023 | 🟢❓📄 Xu, Li, Singh, Li, *Cross-Market Intraday Time-Series Momentum* (ssrn.4651331, W4389266274) | Multi-marchés | Titre seul : extension inter-marchés (le signal d'un marché prédit un autre). |
| 2024 | 🟢📄 Zarattini, Aziz, Barbon, *Beat the Market: An Effective Intraday Momentum Strategy for SPY* (ssrn.4824172, W4396887499) | SPY 2007-2024 | **Adaptation praticienne.** Entrée dès que le prix sort d'une « noise area » (bande calibrée sur le mouvement moyen à chaque heure), au lieu d'attendre 15h30. Stop suiveur dynamique (VWAP). Résultats annoncés : +19,6 %/an, Sharpe 1,33 net de frais. |
| 2025 | 🟢⚠️ Aleti, Bollerslev, Siggaard, *Intraday Market Return Predictability Culled from the Factor Zoo* (Mgmt Sci, W4405992032) | ETF liquides | La prédictibilité intraday se concentre dans les périodes de forte incertitude et vient d'un capital qui bouge lentement. Les signaux passent par les facteurs en coupe (pas uniquement OHLCV de l'indice). |
| 2026 | 🟢🧪📄 Seeck, *Intraday Momentum in Spot FX and Currency Futures* (ssrn.7008318, W7169752305) | EURUSD, GBPUSD, USDJPY…, futures 6J, 2012-2024 | Le signal des 30 premières minutes **après l'ouverture de Londres** est significatif sur 5 instruments sur 6, hors échantillon. Les paires en JPY ont un coefficient environ 3,8× plus grand (effet carry / risk-off). |

### 1.b Conditions où le mécanisme ne marche pas

| Papier | Condition d'échec |
|---|---|
| 🔴 Rosa 2022, *Understanding intraday momentum strategies* (J. Futures Mkts, W4294956096) | **La prédictibilité disparaît hors échantillon** (version « overnight prédit la dernière demi-heure »). Un modèle à changement de régime montre que l'effet n'existe que quand **le signal est fort**. Adaptation : n'activer la stratégie qu'au-delà d'un seuil, plutôt que tous les jours. |
| 🔴 Limkriangkrai, Chai, Zheng 2023, *Market intraday momentum: APAC evidence* (W4383070008) | **Absent à Hong Kong et Singapour**, faible en Corée. **Plus faible pendant le COVID.** La volatilité compte plus que le volume. Le mécanisme dépend donc de la structure du marché. |
| 🔴 Gao et al. 2014 et Li et al. 2021, par contraste | Effet faible les **jours calmes, liquides et à faible volume**, sans information discrète. |
| 🔴 Wen et al. 2020/2022 (pétrole) | La 2ᵉ à l'avant-dernière demi-heure n'ont **pas** de pouvoir prédictif. Les jours EIA, le « bon » prédicteur change (3ᵉ demi-heure). Une règle unique appliquée tous les jours est donc mal spécifiée. |
| 🔴 Xu et al. 2020 (or) | Sur l'or, la 1ʳᵉ demi-heure **n'est pas forcément** le prédicteur. Copier la règle du S&P sur l'or est une erreur. |
| 🔴 Baltussen et al. 2021 | Le momentum **se retourne les jours suivants** : il ne faut pas garder la position overnight. ⚠️ Effet plus faible quand les dealers sont long gamma (non observable en OHLCV ; proxy possible : régimes de faible range réalisé). |
| 🔴📄 Baltussen, Da, Soebhag 2024, *End-of-Day Reversal* (ssrn.5039009, W4405486608) | Au niveau **des actions individuelles en coupe**, on observe l'inverse : un **reversal** dans les 30 dernières minutes, porté par les perdants du jour (achats retail d'attention, couverture des vendeurs à découvert). Le momentum intraday est un phénomène **d'indice ou de marché**, pas de titre. |
| 🔴❓📄 Iwanaga & Sakemoto 2025, *Intraday Time Series Reversal* (ssrn.5807282, W4417288532) | Titre seul : documente un **reversal** en série temporelle intraday. Il faut lire le papier pour savoir dans quelles conditions il remplace le momentum. |
| 🔴❓ Iwanaga & Sakemoto 2026, *Does overnight return predict the first half-hour return for U.S. market indices?* (NAJEF, W7204708060) | Titre seul : teste la première étape de la chaîne (overnight → 1ʳᵉ demi-heure) sur les indices US. |
| 🔴🧪📄 Seeck 2026 (FX) | **GBPUSD a un signal de signe inversé.** Après coûts réels, **seul USDJPY spot reste rentable** ; 4 paires spot et le future 6J ne passent pas. **En 2022, le contrôle de la courbe des taux par la BoJ a détruit le signal spot** (Sharpe −0,56), alors que le future 6J a mieux tenu. Les interventions de banque centrale cassent donc le mécanisme. |
| 🔴🧪📄 Paz 2026, *Out-of-Sample Evaluation of an Intraday Momentum Strategy for SPY* (ssrn.7290621, W7203785194) | Réplication in-sample fidèle (Sharpe 1,34), mais **hors échantillon (mai 2024 à mars 2026) : Sharpe 0,39**, +9,4 % contre +29,5 % en buy & hold. Explications avancées : microstructure, **montée des options 0DTE**. |
| 🔴🧪📄 Delgado 2026, *"Beat the Market" Revisited* (ssrn.7323419, W7203884123) | Réplication quasi exacte. Après publication, deux régimes : mai 2024 à août 2025 bon (Sharpe environ 1,1 à 1,3), puis **septembre 2025 à août 2026 à −8,1 % (Sharpe −0,46)**. **Probabilité de surapprentissage du backtest (PBO) d'environ 38 à 41 %** sur les variantes optimisées. |
| 🔴🧪📄 Mesfin 2026, *Structural Limits of OHLCV-Based Intraday Signals in MNQ Futures* (ssrn.6709401, W7160017466) | Sur le Micro Nasdaq 2021-2025 en barres de 5 minutes, **aucune** des 14 familles de signaux OHLCV (ORB, gap, volume, momentum de la session Asie…) ne passe un coût aller-retour de 2 points. L'avantage brut plafonne entre 0,07 et 1,5 point. |

### 1.c Synthèse causale (mécanisme 1)
- **Quand ça marche** : jours à forte volatilité réalisée, gros gap overnight, volume relatif élevé, information discrète, liquidité faible (crises). Avec le signal reconstitué du début de journée, pas seulement la 1ʳᵉ demi-heure (Baltussen). Sortie à la clôture.
- **Quand ça casse** : signal faible (Rosa), marchés à structure différente (HK, SG), régime de dealers long gamma (non observable en OHLCV), interventions de banque centrale (BoJ 2022), coûts de transaction (FX retail, micro-futures), période post-2024 sur SPY (0DTE ?), actions individuelles (reversal).
- **Évolution** : fenêtre fixe 1ʳᵉ → dernière demi-heure (2014), puis tout le jour → dernière demi-heure, multi-actifs (2021), puis prédicteur dépendant du calendrier ou de l'actif (pétrole EIA, or, 2020-22), puis entrée continue par bande de bruit avec stop suiveur (2024), puis audits hors échantillon négatifs (2026).

---

## 2. Cassure du range d'ouverture (ORB) et bande de bruit intraday

**Signal OHLCV** : on fixe le plus haut et le plus bas des N premières minutes (5/15/30/60), puis on entre dans le sens de la cassure. Variantes : seuil adaptatif selon la volatilité, filtre VWAP, filtre de volume relatif (« stocks in play »).
**Causalité proposée** : l'ouverture concentre l'information de la nuit, et une cassure signale un déséquilibre offre/demande qui persiste dans la journée. Pour les détracteurs, c'est simplement une continuation de l'expansion de volatilité, sans lien avec l'ouverture.

### 2.a Chaîne d'évolution

| Année | Papier | Actifs | Apport |
|---|---|---|---|
| 1990 | ❓ Crabel, *Day Trading with Short-Term Price Patterns and Opening Range Breakout* (livre, non retrouvé dans OpenAlex) | Futures | Origine praticienne de l'ORB. |
| 2010 | 🟢🔴📄 Schulmeister, *The Profitability of Technical Stock Trading has Moved from Daily to Intraday Data* (ssrn.1714980, W2130029527) | S&P 500 spot et futures | 2 580 règles testées. En données journalières, la rentabilité est nulle depuis les années 1990. **En 30 minutes : +8,8 %/an brut sur 1983-2000**, puis **beaucoup moins bien sur 2001-2006** : soit le marché est devenu efficient, soit les tendances sont passées à plus haute fréquence. |
| 2012/13 | 🟢❓ Holmberg, Lönnbark, Lundström, *Assessing the profitability of intraday opening range breakout strategies* (FRL, W2042306668) | **Futures pétrole brut** | Premier test académique de l'ORB, sur le pétrole. Résumé non exposé par les API ; d'après mes souvenirs, rendements conditionnels significativement supérieurs aux non conditionnels (**à vérifier**). |
| 2015 | 🟢❓ Sönnert, *Intraday Momentum: Day trading on the gold futures market using ORB and GARCH* (mémoire KTH, W1456285475) | **Futures or** | Titre seul : ORB sur l'or avec un seuil conditionné par un GARCH. |
| 2019 | 🟢 Tsai, Wu, Syu, Lei, *Timely Opening Range Breakout on Index Futures* (IEEE Access, W2911858053) | DJIA, S&P, NASDAQ, HSI, TAIEX, 2003-2013 | **Adaptation clé** : caler le range sur l'ouverture du **marché cash** et non du future. Plus de 8 %/an. La fenêtre de sondage optimale est courte aux US. |
| 2019 | 🟢 Xin, Lam, Yu, *Effectiveness of filter trading as an intraday trading rule* (W2972000615) | HSI futures | La rentabilité d'un filtre de cassure dépend de la **volatilité réalisée en range (high-low)**, meilleure que la volatilité des rendements pour la prédire. La taille optimale du filtre suit la volatilité réalisée. |
| 2023 | 🟢📄 Zarattini & Aziz, *Can Day Trading Really Be Profitable?* (ssrn.4416622, W4366957240) | QQQ / TQQQ 2016-2023 | ORB 5 minutes sur QQQ : alpha annualisé de 33 % net de commissions (avec levier). |
| 2023 | 🟢📄 Zarattini & Aziz, *VWAP: The Holy Grail for Day Trading Systems* (ssrn.4631351, W4389319238) | QQQ | Règle de tendance prix/VWAP : Sharpe 2,1, drawdown maximal de 9,4 %. |
| 2024 | 🟢📄 Zarattini, Barbon, Aziz, *A Profitable Day Trading Strategy For The U.S. Equity Market* (ssrn.4729284, W4392845171) | Plus de 7 000 actions US | **Filtre causal OHLCV** : ne trader l'ORB que sur les « Stocks in Play » (**volume relatif anormal**). Sharpe 2,81. |
| 2024 | 🟢📄 Zarattini, Aziz, Barbon, *Beat the Market* (cf. 1.a) | SPY | Fusion ORB / momentum intraday : bande de bruit dépendant de l'heure et stop VWAP. |
| 2026 | 🟢🧪📄 Pineda, *Anatomy of the Retest in the QQQ ORB* (ssrn.6745958, W7160849078) | QQQ 2017-2024 | Descriptif : la taille du range est associée à l'amplitude du mouvement qui suit. Le **délai avant le retest** est la variable la plus liée à l'issue. Une forte excursion avant le retest va avec une continuation *moins* probable. |
| 2026 | 🟢🧪📄 Subhani, *ORB on Event-Free Fridays* (ssrn.7589980, W7221068238) | QQQ, SPY, 17 instruments, 2018-2026 | Un ORB 30 minutes **seulement les vendredis sans événement** : +0,44R/trade hors échantillon sur QQQ. L'effet se concentre sur la tech, la croissance et **les métaux**, et il est absent des secteurs défensifs et sensibles aux taux. (Le filtre d'événements suppose un calendrier, mais pas de données de marché externes.) |

### 2.b Conditions où le mécanisme ne marche pas

| Papier | Condition d'échec |
|---|---|
| 🔴🧪📄 Fetna 2026, *ORB Does Not Survive Trading Costs: A Pre-Registered 225-Cell Study* (ssrn.7428398, W7212827098) | **9 futures US (indices, métaux, énergie), 2010-2026, une seule minute de données.** Aucune des 225 cellules pré-enregistrées ne passe à 25 $ l'aller-retour. Avantage brut médian de −0,01 tick. **Le range de 5 minutes est le pire.** La meilleure cellule échoue au test d'ancre aléatoire : c'est de la **continuation d'expansion de volatilité**, pas de l'information propre à l'ouverture. |
| 🔴🧪📄 Mahadzva 2026, *Session Microstructure and the Momentum Mirage* (ssrn.7435081, W7212030704) | **EURUSD, GBPUSD, AUDUSD, USDJPY** (M5 à H4) : **les 4 ORB perdent** hors échantillon et sur le holdout, avec un taux de réussite de 5 à 26 points sous le point mort. Les cassures de volatilité « significatives » (p ≈ 0,03) sont rejetées en walk-forward. Le momentum en coupe sur devises est négatif, et pire à haute fréquence. |
| 🔴🧪📄 Wijesinghe 2026, *Do Simple Technical Trading Rules Survive Realistic Costs?* (ssrn.6977700, W7168216695) | S&P 500 en 5 minutes (2024-2026) : **ORB et mean-reversion sans avantage** (Sharpe dégonflé ≈ 0). |
| 🔴🧪📄 Mesfin 2026 (cf. 1.b) | ORB à plusieurs horizons sur MNQ : échec après 2 points de coûts. |
| 🔴🧪📄 Ladia 2026, *Opening-Range Reversal in Dow Jones Futures: 0DTE Hedging Pressure* (ssrn.7124578, W7171679670) | Depuis 2023, sur le E-mini Dow, c'est un **reversal** à l'ouverture (côté short) qui marche : 59,8 % de réussite contre 45 % avant 2023. Une **rupture de régime** coïncide avec l'essor des 0DTE. L'ORB et son contraire alternent selon le régime. Paramètres non publiés, n faible. |
| 🔴 Schulmeister 2010 | Les règles intraday rentables jusqu'en 2000 **se dégradent sur 2001-2006** : l'avantage se déplace vers des fréquences plus élevées. |
| 🔴 Xin et al. 2019 / Subhani 2026 | Hors des régimes de volatilité en range adaptés, ou les jours d'événements (NFP, CPI, FOMC), l'ORB perd son avantage. |

### 2.c Synthèse causale (mécanisme 2)
- Les résultats spectaculaires portent sur **des actions ou ETF tech avec filtre** (QQQ, Stocks in Play, volume relatif). Les tests **pré-enregistrés sur futures (indices, or, pétrole) et FX majeurs sont négatifs après coûts.**
- L'ingrédient causal qui survit le mieux n'est pas « l'ouverture » mais **l'expansion de volatilité et un volume relatif anormal**.
- Conditions d'échec : petite fenêtre de range (5 minutes sur futures), FX, coûts réalistes, jours d'événements, régime post-2023 (0DTE) sur les indices.

---

## 3. Sur-réaction intraday et reversal (après un gros mouvement ou un gap overnight)

**Signal OHLCV** : grand mouvement à l'ouverture, grand gap ou barre « anormale » (en multiples d'ATR ou d'écart-type) → position contrarienne intraday. Ou, à l'inverse, continuation (« inertie »).
**Causalité proposée** : sur-réaction comportementale, coût d'immobilisation de la liquidité (fermeture périodique du marché), déséquilibres d'ordres temporaires.

### 3.a Chaîne d'évolution

| Année | Papier | Actifs | Apport |
|---|---|---|---|
| 1985 | 🟢 De Bondt & Thaler, *Does the Stock Market Overreact?* (W2144487825) | Actions | Hypothèse de sur-réaction (horizon long). |
| 1990 | 🟢🔴 Atkins & Dyl, *Price Reversals, Bid-Ask Spreads, and Market Efficiency* (JFQA, W2136023526) | Actions | Reversal après les grosses variations d'une journée, surtout les baisses, **mais d'une ampleur inférieure au spread**. Efficient après coûts. |
| 1995 | 🟢❓ Fabozzi, Ma, Chittenden, Pace, *Predicting Intraday Price Reversals* (JPM, W2177834589) | Actions | Résumé non disponible. |
| 2000 | 🟢❓ Fung, Mok, Lam, *Intraday price reversals for index futures in the US and Hong Kong* (JBF, W2010300367) | **S&P 500 futures**, HSI | Résumé non disponible ; d'après mes souvenirs, reversals significatifs après un gros mouvement d'ouverture sur futures d'indices (**à vérifier**). |
| 2004 | 🟢❓ Fung & Lam, *Overreaction of index futures in Hong Kong* (JEF, W1979310853) | HSI | Suite HK. |
| 2004/05 | 🟢🔴❓ Grant, Wolf, Yu, *Intraday price reversals in the US stock index futures market: A 15-year study* (JBF, W2032382731) | **S&P 500 futures** | Résumé non disponible ; d'après mes souvenirs, reversals significatifs après de gros mouvements à l'ouverture, mais un avantage qui ne survit pas aux coûts (**à vérifier**). |
| 2013 | 🟢 Fabozzi, Fung, Lam, Wong, *Market overreaction and underreaction: directional and magnitude effects* (W2069609142) | Actions US | Effet **directionnel** et **de magnitude** : plus le mouvement initial est extrême, plus l'ajustement est grand. |
| 2014/18 | 🟢🔴📄 Caporale, Gil-Alana, Plastun, *Short-Term Price Overreactions: Identification, Testing, Exploitation* (ssrn.2532883, W3121258062) | **FX, matières premières**, actions US | **Bifurcation clé.** Le contrarien après sur-réaction **ne marche pas en FX ni sur les matières premières** (seulement parfois sur les actions US). En FX et sur les matières premières, c'est **l'inertie (continuation)** qui paie. |
| 2014 | 🔴 Mazouz & Wang, *Commodity futures price behaviour following large one-day price changes* (W2033042910) | 18 futures sur matières premières | Sous-réactions ou sur-réactions apparentes, mais **efficientes après ajustement du risque systématique et de l'hétéroscédasticité**. |
| 2016 | 🟢❓ Dao, McGroarty, Urquhart, *Weekend overreaction (and subsequent reversal) in spot FX* (W2548446757) | FX spot | Titre : sur-réaction le week-end puis reversal (gap du dimanche). |
| 2019 | 🟢 Miwa, *Trading hours extension and intraday price behavior* (W2965513440) | Futures sur actions japonaises | La sur-réaction overnight/intraday (corrélation négative entre overnight et intraday) **s'accentue quand la session étendue est plus longue et plus active**. |
| 2019 | 🟢 Lou, Polk, Skouras, *A tug of war: Overnight versus intraday* (JFE, W2797315895) | Actions (coupe) | Les composantes overnight et intraday se continuent chacune, avec un reversal croisé entre elles. |
| 2021 | 🟢 Borgards, Czudaj, Hoang, *Price overreactions in commodity futures: intraday analysis of Covid-19* (W3118474073) | 20 futures, dont **pétrole et or** | Sur-réaction intraday confirmée (de 1 minute à 1 heure), **plus fréquente et plus ample pendant le COVID**. **Énergie et métaux précieux sur-réagissent plus** que les softs et les métaux industriels. Le **pétrole est asymétrique** (plus de sur-réactions négatives). Indépendant de la fréquence des données. |
| 2021 | 🟢🔴 Caporale & Plastun, *Gold and oil prices: abnormal returns, momentum and contrarian effects* (W3149462930) | **Or, pétrole** | Le jour anormal se détecte en séance, et le prix **continue** jusqu'à la clôture. **Le lendemain : momentum pour le pétrole, contrarien pour l'or.** |
| 2023 | 🟢❓📄 Kosowski, Liu, Liu, Wang, *Overnight-Intraday Reversal Everywhere* (ssrn.4605208, W4387717685) | Multi-actifs (titre) | Titre seul : reversal overnight → intraday généralisé. Ses références (Lou et al., Bogousslavsky, Akbas et al.) en font une extension multi-actifs. |
| 2023 | 🟢 Lu, Malliaris, Qin, *Heterogeneous liquidity providers and night-minus-day return predictability* (JFE, W4362575183) | Actions | Cause : les arbitragistes rapides exigent une prime à l'ouverture (asymétrie d'information) qui s'atténue ensuite, d'où des rendements overnight et intraday de signes opposés. |

### 3.b Conditions où le mécanisme ne marche pas

| Papier | Condition d'échec |
|---|---|
| 🔴 Atkins & Dyl 1990 / Grant et al. 2005 ❓ | Reversal **inférieur aux coûts** (spread). |
| 🔴📄 Caporale et al. 2014/18 | **Le contrarien échoue en FX et sur les matières premières** : il faut jouer l'inertie à la place. |
| 🔴 Mazouz & Wang 2014 | L'« anomalie » disparaît après ajustement du risque et de la volatilité conditionnelle (GARCH) : le reversal brut peut être un artefact de volatilité. |
| 🔴 Caporale & Plastun 2021 | **Or ≠ pétrole** : le même signal donne un reversal sur l'or et une continuation sur le pétrole le lendemain. |
| 🔴 Borgards et al. 2021 | L'intensité dépend du **régime** (crise > normal) ; métaux industriels et softs peu concernés. |
| 🔴 Laly 2025, *High-frequency momentum and contrarian strategies in U.S. blue chips* (W4414253355) | 288 stratégies momentum et contrariennes à haute fréquence (2020-2021) : certaines battent le benchmark avant coûts, **aucune après coûts raisonnables**. |
| 🔴 Miwa 2019 (inversement) | Le reversal overnight/intraday **varie avec la durée de la session étendue**. Sur des produits presque 24h (ES, CL, GC, FX), la notion de « gap » perd son sens. |

### 3.c Synthèse causale (mécanisme 3)
- **Indices US** : reversal après un gros mouvement à l'ouverture, documenté depuis 2000 mais faible face aux coûts.
- **Or** : plutôt contrarien le lendemain d'un jour anormal. **Pétrole et FX** : plutôt **inertie**.
- Le signal doit être **normalisé par la volatilité** (sinon on confond sur-réaction et hétéroscédasticité). Il est plus fort en crise et en énergie / métaux précieux.

---

## 4. Saisonnalité horaire et flux de « fixings » (heure de la journée = signal)

**Signal OHLCV** : seulement l'horloge, plus le rendement avant une fenêtre (ex. 15h55-16h05 à Londres). Rendement moyen par tranche horaire, et reversal autour d'un fix de référence.
**Causalité proposée** : demande non informée et prévisible (couvertures, benchmarks), risque d'inventaire des dealers, achats de devises « à domicile », résolution de l'incertitude à l'ouverture européenne.

### 4.a Chaîne d'évolution

| Année | Papier | Actifs | Apport |
|---|---|---|---|
| 1995 | 🟢❓ Cornett, Schwarz, Szakmary, *Seasonalities and intraday return patterns in the foreign currency futures market* (JBF, W1980960732) | Futures FX | Titre : saisonnalités intraday. |
| 2009 | 🟢❓ Ranaldo, *Segmentation and time-of-day patterns in foreign exchange markets* (JBF, W2004040129) | FX | Titre (et suite directe ci-dessous). |
| 2012/13 | 🟢📄 Breedon & Ranaldo, *Intraday Patterns in FX Returns and Order Flow* (ssrn.2099321, W2163127738 ; JMCB W2332431545) | FX majeurs | **Les devises se déprécient pendant leurs propres heures de marché** (les acteurs locaux sont acheteurs nets de devise étrangère). Confirmé sur plusieurs fuseaux. ⚠️ explication par le flux d'ordres, mais signal = horloge. |
| 2014/15 | 🟢❓ Melvin & Prins, *Equity hedging and exchange rates at the London 4 p.m. fix* (JFM, W2040846150) | FX | D'après mes souvenirs : rééquilibrage des couvertures de portefeuilles actions étrangers au fix de fin de mois, prévisible avec les rendements des indices actions (**à vérifier**). |
| 2014 | 🟢 Caminschi & Heaney, *Fixing a Leaky Fixing: London PM Gold Price Fixing* (J. Futures Mkts, W2142404758) | **Futures GC, GLD** | Volume et volatilité montent **dès le début** du fixing de l'or ; rendements anormaux dans les **4 minutes** qui suivent. Le sens des premières transactions prédit celui du fixing dans plus de 90 % des cas : fuite d'information. |
| 2015 | 🟢 Ito & Yamada, *Was the Forex Fixing Fixed?* (NBER, W2147626754) | USDJPY, EURUSD | Peu de pics de prix au fix de Londres (liquidité élevée). Le fix de Tokyo (9h55) fonctionne différemment. |
| 2016 | 🟢 Hauptfleisch, Putniņš, Lucey, *Who Sets the Price of Gold? London or New York* (W2343583846) | Or | Les **futures de New York** dominent la formation du prix, avec des variations intraday selon les heures de jour et les annonces macro. |
| 2017/18 | 🟢❓ Evans, *Forex trading and the WMR Fix* (JBF, W3022362291) | FX | Dynamique des prix autour du fix WMR. |
| 2020/22 | 🟢⚠️📄 Bondarenko & Muravyev, *Market Return Around the Clock: A Puzzle* (ssrn.3596245, W3033072505 ; JFQA W4287218645) | **E-mini S&P 500** 24h | **Les 4 heures autour de l'ouverture européenne génèrent tout le rendement moyen du marché** (Sharpe 1,6, robuste aux coûts). Rendement moyen nul les 20 autres heures. Plus fort pendant le COVID. Signal = horloge ; explication via le VIX ⚠️. |
| 2020 | 🟢 Khademalomoom & Narayan, *Intraday-of-the-week effects: exchange rate data* (W3006049736) | 12 devises contre USD (dont AUD, CAD, EUR, JPY, CHF, GBP) | Effets heure × jour de semaine : dépréciation surtout lundi et mardi, stratégies rentables. |
| 2020/23 | 🟢📄 Krohn, Mueller, Whelan, *Foreign Exchange Fixings and Returns Around the Clock* (ssrn.3521370, W3024923689 ; JF 2023 W4389903555) | 9 devises principales, 21 ans | **Le USD s'apprécie avant les fixes et se déprécie après : profil en W sur 24h.** Expériences naturelles : **c'est l'existence d'un taux de référence publié qui fixe le moment du reversal.** Cause : risque d'inventaire des dealers face à une demande inconditionnelle de dollars. |
| 2024-26 | 🟢❓📄 Oomen & Muhle-Karbe, *A comparison of FX fixing methodologies* (ssrn.4857092) ; Muhle-Karbe, Oomen, Rodríguez Polo, *Information Leakage and Opportunistic Trading Around the FX Fix* (ssrn.5351658, W4412719957) ; Osler & Turnbull, *Dealer misconduct and price dynamics at the fix* (JBF 2026, W7125632880) | FX | Suite récente (titres) : fuite d'information et trading opportuniste autour du fix ; effets de la méthode de calcul. |

### 4.b Conditions où le mécanisme ne marche pas

| Papier | Condition d'échec |
|---|---|
| 🔴 Krohn et al. 2023 | **Pas de fix publié, pas de reversal** : le mécanisme est institutionnel. Si l'heure ou la méthode du fix change, le pattern se déplace. |
| 🔴 Ito & Yamada 2017, *Did the Reform Fix the London Fix Problem?* (NBER, W2890282142) | Réforme de 2015 (fenêtre de 1 à 5 minutes, sanctions) : **le pic de volume dans la fenêtre disparaît**, mais **les anomalies de prix persistent**, et le trading passif des banques crée une **autre** prédictibilité. Le mécanisme s'adapte au lieu de disparaître. |
| 🔴 Benenchia, Galati, Lepone 2024 (W4392361410, W4405747297) | Après 2015, la fenêtre de 5 minutes est « globalement efficace » : moins de distorsion exploitable dans la fenêtre elle-même. |
| 🔴❓ Caminschi & Heaney 2014 (contexte) | Mécanisme propre à l'**ancien fixing téléphonique de l'or**. Le passage à l'enchère électronique LBMA en 2015 (connaissance générale, non vérifiée via l'API) change probablement la dynamique. |
| 🔴 Laarits 2026, *Discounting timing strategies* (JFE, W7213626887) | Les stratégies de timing (dont la saisonnalité) dont l'alpha paraît élevé à court horizon **perdent plus de la moitié de leur alpha à long horizon** : c'est une rémunération de risque (saisonnalité de la volatilité), pas une inefficience. |
| 🔴 Ito & Yamada 2015 | Au fix de Londres, liquidité élevée et peu de pics : l'impact prix est **faible** quand la liquidité est maximale. |

### 4.c Synthèse causale (mécanisme 4)
- C'est le mécanisme le **plus « causal »** de la liste, avec des expériences naturelles (Krohn et al.) : une demande prévisible et non informée rencontre un inventaire de dealers, ce qui donne un reversal. Le signal est purement l'horloge.
- **FX majeurs** : USD fort avant les fixes, faible après ; dépréciation de la devise pendant ses heures locales.
- **Indices US** : rendement concentré autour de l'ouverture européenne sur ES.
- **Or** : fenêtres de fixing (régime pré-2015).
- **Pétrole** : rien de spécifique trouvé dans OpenAlex/SSRN sur la fenêtre de settlement de 14h28-14h30 ET (piste à creuser) ; le seul pattern calendaire documenté est l'EIA du mercredi (mécanisme 1).
- Échec : changement institutionnel (réforme, méthode du fix), liquidité maximale dans la fenêtre, rémunération de risque plutôt qu'alpha.

---

## 5. Tableau croisé : conditions d'échec par classe d'actifs

| Actif | Mécanisme qui tient le mieux (OHLCV) | Conditions d'échec documentées |
|---|---|---|
| **Indices US** (ES, NQ, YM, SPY) | Momentum intraday les jours volatils ; rendement autour de l'ouverture européenne | Hors échantillon post-2013 (Rosa) ; SPY après septembre 2025 (Delgado, Paz) ; régime 0DTE post-2023 (reversal à l'ouverture, Ladia) ; micro-futures et coûts (Mesfin) ; ORB sur futures (Fetna) |
| **FX majeurs** | Reversal autour des fixes (W-shape) ; dépréciation en heures locales ; momentum Londres sur JPY | GBPUSD de signe inversé ; coûts retail ; BoJ YCC 2022 ; ORB et momentum en coupe négatifs (Mahadzva) ; contrarien après sur-réaction (Caporale) |
| **Pétrole** | 1ʳᵉ demi-heure (surtout l'overnight) → dernière ; 3ᵉ demi-heure les jours EIA ; inertie après un jour anormal | Demi-heures intermédiaires non prédictives ; asymétrie à la baisse ; ORB après coûts (Fetna) ; contrarien (Caporale) |
| **Or** | Momentum intraday avec une demi-heure prédictive propre à l'or ; contrarien le lendemain d'un jour anormal ; fenêtres de fixing | Règle du « 1ʳᵉ demi-heure » du S&P inadaptée ; ORB métaux après coûts (Fetna, mais Subhani positif sur les métaux certains vendredis) ; régime post-2015 du fixing |

---

## 6. Limites de cette recherche
- **SSRN inaccessible directement** (anti-bot) : je n'ai lu aucun texte intégral, seulement les résumés. Les lignes ❓ sont à vérifier en lisant les papiers.
- **Couverture d'OpenAlex** : beaucoup de papiers SSRN ont `referenced_works = 0`. Les chaînes ont donc été reconstituées via les versions publiées en revue et via les papiers citants.
- **Biais des papiers 2026** 🧪 : les réfutations récentes (Fetna, Mahadzva, Mesfin, Paz, Delgado, Seeck, Wijesinghe) sont souvent pré-enregistrées et utiles, mais non relues par des pairs.
- **OHLCV et cause** : les causes les mieux identifiées (gamma des dealers, flux de fixing, VIX) ne sont pas observables en OHLCV. On trade le symptôme, et les conditions d'échec liées à ces causes ne se voient qu'indirectement (volatilité en range, horloge, calendrier).

### Pistes pour la suite
1. Lire en priorité : Iwanaga & Sakemoto 2025 (*Intraday Time Series Reversal*), Kosowski et al. 2023, Grant et al. 2005, Holmberg et al. 2013, Muhle-Karbe et al. 2025 (résumés absents).
2. Chercher la fenêtre de settlement du pétrole (CME, 14h28-14h30 ET) et les effets « trading at settlement ».
3. Tester sur vos données : momentum intraday avec seuil (Rosa) × régime de volatilité en range (Xin et al.) × exclusion des jours EIA/FOMC, sur ES, CL, GC, 6E, 6J.
