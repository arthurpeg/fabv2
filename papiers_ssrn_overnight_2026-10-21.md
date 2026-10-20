# Papiers SSRN : l'overnight (rendement de nuit, anomalie overnight) sur indices US, FX majeurs, or et pétrole

*Session du 2026-10-21. Source : API OpenAlex filtrée sur SSRN (`S4210172589`), 60 requêtes ciblées (overnight return/anomaly/drift/reversal/momentum/volatility, close-to-open, non-trading hours, around the clock, sessions FX, or et pétrole par session, Globex/E-mini overnight), environ 2 300 candidats triés par titre. OpenAlex ne fournit plus les résumés : ils viennent de Crossref ou de Semantic Scholar. Résumés **paraphrasés en français**. Les papiers déjà fournis (voir [papers/seen_papers.json](papers/seen_papers.json)) sont exclus : Cooper-Cliff-Gulen, Branch-Ma 2006, Knuteson, Haghani, Cai-Qiu, Lou-Polk-Skouras (tug of war), Bondarenko-Muravyev (around the clock), Krohn-Mueller-Whelan (FX fixings), Ranaldo (segmentation FX) ne sont donc pas répétés.*

**Légende** : 🔴 échec ou condition limite · ⚠️ le signal dépend d'une donnée non OHLCV (sentiment, VIX, flux) ou d'un marché hors périmètre · 🧪 papier SSRN récent d'auteur indépendant, non relu par des pairs

---

## 0. Point de départ : ce que « overnight » veut dire selon l'actif

- **Indices US (ES/NQ)** : l'overnight est la période de 22h00 à 15h30 heure de Paris (clôture cash → ouverture cash). Les futures cotent pendant presque toute cette période, sauf la pause CME de 23h00 à 0h00. On peut donc **découper** la nuit (soirée US, Asie, ouverture européenne, pre-market US) avec des barres OHLCV, ce que les papiers sur actions individuelles ne peuvent pas faire.
- **FX majeurs, or, pétrole** : ces marchés cotent presque 24h/24. Il n'y a pas de vraie « nuit ». L'équivalent est le **découpage par session** : Asie (1h–9h Paris), Europe (9h–15h30), US (15h30–23h). La question devient : quelle session porte le rendement, et laquelle le rend ?
- **Couverture** : la littérature SSRN est très riche sur les actions US, beaucoup plus pauvre sur FX, or et pétrole. Aucun papier SSRN spécifique au **pétrole** et à l'overnight n'a été trouvé. Le pétrole n'est couvert que par [13] (Fattinger-Ziegler, multi-actifs).

⚠️ **Heure d'été et d'hiver** : l'Europe change d'heure le 25 octobre 2026 et les États-Unis le 1er novembre 2026. Pendant cette semaine, la clôture cash US a lieu à **21h00** et l'ouverture à **14h30** heure de Paris.

---

## A. Indices US : d'où vient le rendement de nuit ?

### [1] The Overnight Drift

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3546173
- **Actifs :** actions US, futures sur indices US
- **Plage horaire / Session :** nuit, avec un pic **pendant l'ouverture des marchés européens** (environ 8h–10h heure de Paris)
- **Date :** 2020 (publié RFS 2023) | **Auteurs :** Nina Boyarchenko, Lars Christian Larsen, Paul Whelan | **Citations :** 24

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture de l'Europe, au milieu de la nuit US. **Qui subit la contrainte** : les teneurs de marché, qui ont absorbé les **déséquilibres d'ordres de la clôture US** et doivent porter ce stock pendant la nuit. Ils se déchargent quand la liquidité européenne arrive. **Effet sur les bougies** : un rendement positif, fort et régulier sur les barres de l'ouverture européenne. La réaction est **asymétrique** : après une séance de **baisse**, le rebond de nuit est fort ; après une séance de hausse, le retournement est faible.

> **Résumé (abstract paraphrasé) :** Les rendements des actions US sont grands et positifs pendant les heures d'ouverture des marchés européens. L'effet est très significatif et lié aux déséquilibres d'ordres de la clôture US de la veille, comme le prédisent les modèles de risque d'inventaire. Le drift positif en moyenne vient de l'asymétrie : les ventes massives donnent de forts rebonds la nuit, les hausses très peu. Les auteurs l'expliquent par une capacité de prise de risque des teneurs de marché qui varie dans le temps.
>
> **Pour nous :** c'est le papier le plus directement testable en OHLCV. Variable : rendement ES/NQ de 8h00 à 10h00 Paris, conditionné au rendement de la séance cash de la veille (et à sa dernière demi-heure). Hypothèse : rebond plus fort après une séance baissière. Les mêmes auteurs ont un papier 2026 « The Disappearing Overnight Drift » (hors SSRN, LSE) qui suggère que l'effet **s'affaiblit** : à vérifier sur les dernières années.

### [2] Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1625495
- **Actifs :** actions US
- **Plage horaire / Session :** nuit, puis séance qui suit (ouverture → clôture)
- **Date :** 2011 (publié JFQA 2012) | **Auteurs :** Henk Berkman, Paul D. Koch, Laura A. Tuttle, Ying Zhang | **Citations :** 232

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture. **Qui subit la contrainte** : les particuliers, qui passent leurs ordres le soir ou le matin sur les titres qui ont attiré leur attention et achètent **à l'ouverture**. **Effet sur les bougies** : un prix d'ouverture élevé par rapport au reste de la séance. La nuit est positive et la séance retourne vers le bas.

> **Résumé (abstract paraphrasé) :** Les rendements sont nettement positifs la nuit et suivis d'un retournement en séance. Ce schéma vient d'un prix d'ouverture élevé par rapport aux prix de la journée. Il est concentré sur les titres qui ont attiré l'attention des particuliers, sur ceux difficiles à évaluer ou à arbitrer, et dans les périodes de sentiment haussier. Le coût implicite d'acheter à l'ouverture dépasse souvent le demi-spread.
>
> **Pour nous :** c'est la référence pour le mécanisme « acheteurs particuliers à l'ouverture ». Sur l'indice, l'équivalent est la séance qui suit une forte hausse de la veille (attention élevée).

### [3] A One-factor Model for Expected Night-minus-day Stock Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3854046
- **Actifs :** actions US (portefeuilles nuit moins jour)
- **Plage horaire / Session :** nuit contre séance
- **Date :** 2021 | **Auteurs :** Zhongjin Lu, Zhongling Qin | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture. **Qui subit la contrainte** : les fournisseurs de liquidité, qui absorbent la demande des particuliers à l'ouverture et exigent une compensation. **Effet sur les bougies** : l'écart nuit/jour est un **prix de la liquidité** : la nuit monte jusqu'à l'ouverture (demande des particuliers), la séance rend cette prime.

> **Résumé (abstract paraphrasé) :** Un seul facteur explique environ 80 % des écarts entre portefeuilles nuit-moins-jour. Ce facteur est lié aux déséquilibres d'ordres des particuliers à l'ouverture et au rendement exigé par les fournisseurs de liquidité. L'équilibre est celui où la liquidité est payée pour accueillir une demande guidée par le sentiment.

### [4] Return Extrapolation and Day/Night Effects

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4181093
- **Actifs :** actions US
- **Plage horaire / Session :** séance de la veille → **15 premières minutes** de la séance suivante
- **Date :** 2022 | **Auteurs :** Christopher S. Jones, Sungjune Pyun, Tong Wang | **Citations :** 4

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : dans les **15 premières minutes** de la séance. **Qui subit la contrainte** : les investisseurs qui extrapolent, surtout particuliers, qui achètent le matin ce qui a monté la veille. **Effet sur les bougies** : après une forte séance haussière, les déséquilibres acheteurs à l'ouverture sont élevés, ce qui donne une nuit positive. L'effet est **asymétrique** : plus fort après une hausse qu'après une baisse.

> **Résumé (abstract paraphrasé) :** L'écart nuit/jour viendrait de l'extrapolation des rendements. Après une séance forte, les déséquilibres d'ordres des 15 premières minutes sont élevés. L'effet est plus fort sur les titres surévalués et prisés des particuliers. Il explique la plus grande partie du « tug of war » entre nuit et jour, et la pente positive entre beta et rendement de nuit.
>
> **Pour nous :** cela complète [1] avec un signe opposé. Selon [1], c'est la **baisse** de la veille qui donne un rebond de nuit (stock des teneurs de marché) ; selon [4], c'est la **hausse** de la veille qui pousse l'ouverture (extrapolation). Les deux peuvent coexister sur des heures différentes : 8h–10h Paris pour [1], 15h30–15h45 pour [4]. C'est à tester séparément.

### [5] Overnight Returns, Daytime Reversals, and Future Stock Returns: The Risk of Investing in a Tug of War With Noise Traders

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3324880
- **Actifs :** actions US **et marché global**
- **Plage horaire / Session :** nuit positive puis séance négative, comptée sur un mois
- **Date :** 2019 | **Auteurs :** Ferhat Akbas, Ekkehart Boehmer, Chao Jiang, Paul D. Koch | **Citations :** 4

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : chaque jour, entre la nuit et la séance. **Qui subit la contrainte** : les arbitragistes de journée, qui corrigent la poussée de nuit des noise traders et **finissent par trop corriger** quand cela se répète. **Effet sur les bougies** : un mois avec beaucoup de jours « nuit positive, séance négative » est suivi de **rendements plus élevés**, pour les titres et pour **l'indice**.

> **Résumé (abstract paraphrasé) :** Une fréquence élevée de nuits positives suivies de séances négatives signale une lutte persistante entre clientèles. Plus cette lutte est persistante, plus les rendements futurs sont élevés, au niveau du titre comme du marché. Les arbitragistes de journée sous-estiment la possibilité que de bonnes nouvelles arrivent la nuit et corrigent trop.
>
> **Pour nous :** variable OHLCV directe sur l'indice : nombre de jours sur 20 avec (ouverture > clôture veille) et (clôture < ouverture). Cible : rendement du mois suivant. C'est un horizon long, à utiliser comme filtre de régime.

### [6] Asset Pricing: A Tale of Night and Day

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3117663
- **Actifs :** actions US et internationales, portefeuilles triés par beta ; **futures sur Treasuries**
- **Plage horaire / Session :** nuit contre séance
- **Date :** 2018 (publié JFE 2020) | **Auteurs :** Terrence Hendershott, Dmitry Livdan, Dominik Rösch | **Citations :** 147

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit d'un côté, la séance de l'autre. **Qui subit la contrainte** : les porteurs de risque de marché, qui ne sont rémunérés que pendant la nuit. **Effet sur les bougies** : la nuit, les titres à beta élevé montent plus. En séance, c'est l'inverse : la relation avec le beta est **négative**. Le taux sans risque implicite diffère aussi entre nuit et jour, ce qui se voit sur les futures Treasuries.

> **Résumé (abstract paraphrasé) :** Le CAPM marche mal sur 24 heures car la sensibilité au beta s'inverse entre nuit et séance. Le résultat tient pour les titres, les portefeuilles, les industries, aux États-Unis et ailleurs. Les rendements des futures sur Treasuries diffèrent aussi entre nuit et jour.
>
> **Pour nous :** le NQ a un beta plus élevé que l'ES. Hypothèse : l'écart nuit/jour est plus marqué sur NQ que sur ES (cohérent avec [16]).

### [7] Bad Days and Good Nights: A Re-Examination of Non-Traded and Traded Period Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1102165
- **Actifs :** grands indices hors US et indices US
- **Plage horaire / Session :** séance contre fermeture
- **Date :** 2008 | **Auteurs :** Zvi Wiener, Robert George Tompkins | **Citations :** 5

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant la séance, puis la nuit. **Qui subit la contrainte** : les teneurs de marché sur dérivés actions, soumis aux exigences de capital (Bâle I), qui doivent réduire leur risque en séance. **Effet sur les bougies** : hors US, séances négatives et nuits positives. 🔴 Aux **États-Unis**, sur la période étudiée, nuit et séance étaient **toutes deux positives**.

> **Résumé (abstract paraphrasé) :** Pour les grands marchés hors US, les rendements sont nettement négatifs en séance et positifs la nuit. Les auteurs l'attribuent aux règles de gestion du risque des teneurs de marché sur dérivés. L'introduction des exigences de Bâle I semble avoir amplifié l'anomalie.

---

## B. Indices US : conditionner la nuit et la séance qui suit

### [8] Cycles of Declines and Reversals following Overnight Market Declines

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3287680
- **Actifs :** actions US (NYSE, AMEX, Nasdaq), effet de marché
- **Plage horaire / Session :** nuit de baisse → séance → nuit suivante
- **Date :** 2018 | **Auteurs :** Farshid Abdi | **Citations :** 3

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le jour qui suit une **nuit de baisse du marché**, puis la nuit d'après. **Qui subit la contrainte** : les fournisseurs de liquidité contraints en capital, qui se retirent après le choc. La liquidité des titres volatils se dégrade. **Effet sur les bougies** : après une nuit de baisse, la séance **continue de baisser** (titres volatils), puis la **nuit suivante rebondit**. Le phénomène est apparu après 2001.

> **Résumé (abstract paraphrasé) :** L'association entre rendements de nuit et de séance est passée de positive à fortement négative en 24 ans. Après 2001, une baisse de nuit est suivie d'une baisse supplémentaire en séance puis d'un retournement la nuit suivante, comme le prédisent les modèles où des contraintes de capital provoquent des assèchements de liquidité. La volatilité idiosyncratique explique mieux ce cycle que le risque systématique. (Ce papier était en « résumé introuvable » le 2026-10-14 ; résumé retrouvé.)
>
> **Pour nous :** c'est un signal en trois temps directement testable : gap baissier (ES/NQ) → séance baissière → long à la clôture pour la nuit. Il est cohérent avec [1] (rebond de nuit après une séance de baisse).

### [9] Overnight Return, the Invisible Hand Behind The Intraday Return? A Retrospective

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3259614
- **Actifs :** actions US, S&P 500
- **Plage horaire / Session :** nuit → séance qui suit
- **Date :** 2018 | **Auteurs :** Ben S. Branch, Aixin Ma | **Citations :** 12

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : de l'ouverture à la clôture, après la nuit. **Qui subit la contrainte** : le prix d'ouverture des petites valeurs, fixé sur un marché mince. **Effet sur les bougies** : plus la nuit est forte, plus la séance va en sens inverse, de façon **monotone**. 🔴 Mais sur la période récente et calme, l'effet **ne tient plus pour le S&P 500**, seulement pour les petites valeurs.

> **Résumé (abstract paraphrasé) :** Les auteurs reprennent leur étude de 2006 (fournie le 2026-10-14) sur des années plus récentes. L'autocorrélation négative nuit/séance persiste sur les petites capitalisations mais pas sur le S&P 500. Le marché est devenu moins volatil et le facteur marché pèse davantage.
>
> **Pour nous :** c'est un résultat négatif important : le retournement « nuit → séance » des actions individuelles **ne se transpose pas** à l'ES. À tester sur NQ, mais sans trop d'espoir.

### [10] Dark Side of the Day: Overnight Price Jumps and Short-Term Return Predictability

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4335622
- **Actifs :** 9 283 actions NYSE, AMEX, Nasdaq
- **Plage horaire / Session :** saut de nuit (gap extrême) → jours suivants
- **Date :** 2023 | **Auteurs :** Hulusi Bahcivan, Lammertjan Dam, Halit Gonenc | **Citations :** 2

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : après un saut de prix pendant la nuit. **Qui subit la contrainte** : le prix d'ouverture, fixé sans marché continu actif, qui sur-réagit. **Effet sur les bougies** : les gros gaps (positifs comme négatifs) sont suivis d'un **retournement** à court terme. Le retournement s'efface quand le marché continu reprend.

> **Résumé (abstract paraphrasé) :** Les sauts de nuit prédisent négativement les rendements de court terme, à la hausse comme à la baisse, y compris en période de crise. Une stratégie long-short après les jours de saut gagne 1,05 % hors frais, gain qui diminue avec la durée de détention. Sur un mois, la même idée perd de l'argent : la sur-réaction est transitoire. La découverte du prix demande un marché actif.
>
> **Pour nous :** cela confirme l'hypothèse « les gros gaps se retracent » de la session du 2026-10-14 (ses papiers [7] et [9]), mais sur actions et à l'horizon de quelques jours. Variable : gap / ATR en décile extrême.

### [11] Day and Night Expected Returns Under Overnight Information Shocks: New Tug-of-War Pattern

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5240716
- **Actifs :** actions NYSE, AMEX, Nasdaq
- **Plage horaire / Session :** nuit contre séance, sur le mois suivant
- **Date :** 2025 | **Auteurs :** Hulusi Bahcivan | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le mois qui suit des sauts de nuit. **Qui subit la contrainte** : les clientèles de nuit et de jour, qui réagissent différemment selon que la nouvelle de nuit était une surprise. **Effet sur les bougies** : pour les titres avec sauts de nuit, la persistance du rendement de nuit est plus faible (-3,9 %) et la perte de séance plus petite (4,4 %) que dans le « tug of war » classique.

> **Résumé (abstract paraphrasé) :** Les rendements de nuit et de séance sont persistants, mais différemment quand on tient compte des sauts de nuit. La force et l'effet de surprise des nouvelles de nuit modifient les schémas de retournement entre séance et nuit.
>
> **Pour nous :** papier au niveau du titre et à horizon mensuel. Intérêt limité pour l'indice ; à garder en référence.

### [12] 🧪 Scheduled Coordination Density and the Sign of Overnight Returns in U.S. Equity Markets

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6818821
- **Actifs :** 15 ETF actions US (2016–2024)
- **Plage horaire / Session :** clôture (fenêtre d'exécution) → nuit
- **Date :** 2026 | **Auteurs :** Avaneendra Trivedi | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : les jours où plusieurs flux institutionnels **programmés** (rebalancements d'indices, ETF à levier, échéances d'options, fins de mois et de trimestre) tombent sur la **même clôture**. **Qui subit la contrainte** : les institutionnels obligés d'exécuter à la clôture. **Effet sur les bougies** : contre l'hypothèse pré-enregistrée de retournement, une forte coordination prédit une **continuation** pendant la nuit (-5 bp par écart-type de l'indice de coordination, dans le sens de la clôture). Aux fins de trimestre, l'effet s'inverserait vers un retournement (signal faible).

> **Résumé (abstract paraphrasé) :** L'auteur construit un indice de densité de coordination à partir de calendriers publics et de prix/volumes. Le terme de recouvrement est significatif contre un test de permutation des calendriers. L'effet n'existe pas sur 1993–2024 mais apparaît depuis 2010, et surtout depuis 2016, ce que l'auteur relie à la croissance des ETF à levier et des options courtes. Quatre hypothèses de « pression transitoire » pré-enregistrées ont été rejetées.
>
> **Pour nous :** la démarche pré-enregistrée ressemble à la nôtre. Le calendrier (échéances, rebalancements, fins de mois) est public et donc compatible OHLCV. Lien avec notre test LETF de fin de journée : effet récent, propre à l'ère des ETF à levier.

### [13] ⚠️🧪 Overnight Bitcoin Losses and the Timing of US Equity Repricing

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7579278
- **Actifs :** SPY, QQQ ; Bitcoin jusqu'à 9h00 New York
- **Plage horaire / Session :** gap d'ouverture contre séance qui suit (2018–2026)
- **Date :** 2026 | **Auteurs :** Minwoo Song | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'ouverture cash, après une nuit (ou un week-end) de baisse du Bitcoin. **Qui subit la contrainte** : le marché actions fermé, qui reprend le choc à la réouverture. **Effet sur les bougies** : **87 à 98 %** de la réaction est dans le **gap**. 🔴 La séance qui suit **n'est pas prévisible**, ni dans l'échantillon ni hors échantillon.

> **Résumé (abstract paraphrasé) :** Les pertes du Bitcoin le week-end prédisent la baisse des actions US le lundi. Ici, cette relation est située dans la journée : elle passe presque entièrement par le gap d'ouverture, en semaine comme le week-end. L'apparente réaction intraday du VIX s'explique surtout par le gap et n'est pas robuste.
>
> **Pour nous :** résultat négatif utile. Comme les futures ES/NQ cotent la nuit, ils intègrent déjà le choc Bitcoin avant 15h30. Pas de signal exploitable après l'ouverture.

---

## C. Stratégies overnight et volatilité de nuit

### [14] 🧪 Lovers by Night, Strangers by Day? An Investigation of Simple Overnight Trading Strategies

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2495490
- **Actifs :** S&P 500 (SPY, futures E-mini), **Nasdaq-100 E-mini**
- **Plage horaire / Session :** achat à la clôture, vente à l'ouverture
- **Date :** 2014 | **Auteurs :** Chrilly Donninger | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : de la clôture à l'ouverture. **Qui subit la contrainte** : aucune explication causale proposée ; le papier teste la faisabilité. **Effet sur les bougies** : l'effet existe toujours, mais il est **plus faible** que dans la littérature ancienne. Les rendements de nuit sont **positivement liés aux périodes de turbulence**. 🔴 Avec des coûts réalistes, la stratégie sur **E-mini S&P est pire** qu'un simple achat-conservation de SPY. Le **Nasdaq-100 E-mini** est plus prometteur.

> **Résumé (abstract paraphrasé) :** L'auteur vérifie si la concentration des gains la nuit, avec moins de volatilité, tient sur des données récentes et si elle est exploitable. L'effet subsiste mais en plus faible. Sans coûts, la stratégie serait simple et attractive. Avec coûts, l'ES ne bat pas le buy-and-hold ; le NQ est un meilleur candidat.
>
> **Pour nous :** cohérent avec [6] (beta plus élevé du NQ) et avec notre résultat LETF (NQ passe, ES non). Le lien avec la turbulence rejoint [1] et [8] : la nuit paie surtout après les séances de stress.

### [15] ⚠️ Market Sentiment and an Overnight Anomaly

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3829582
- **Actifs :** SPY
- **Plage horaire / Session :** clôture → ouverture
- **Date :** 2021 | **Auteurs :** Radovan Vojtko, Daniela Hanicova (Quantpedia) | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit. **Qui subit la contrainte** : non précisé ; le sentiment du marché sert de filtre. **Effet sur les bougies** : le rendement de nuit de SPY dépend du régime de sentiment, mesuré par un indicateur propriétaire (Brain), le VIX et la **tendance courte de SPY**.

> **Résumé (abstract paraphrasé) :** Le papier présente plusieurs mesures du sentiment et étudie l'anomalie overnight filtrée par trois d'entre elles. Le but n'est pas un système de trading : les coûts d'une stratégie quotidienne seraient très élevés. Les auteurs proposent plutôt d'utiliser le filtre comme surcouche pour choisir quand trader.
>
> **Pour nous :** seul le filtre « tendance courte de SPY » est OHLCV. C'est une variable simple à ajouter au test de nuit (par exemple clôture au-dessus ou au-dessous de la moyenne 10 jours).

### [16] The Economic Value of Conditioning on Overnight Information

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=676705
- **Actifs :** indices européens et US
- **Plage horaire / Session :** nuits de semaine, week-ends, jours fériés, longs week-ends → séance suivante
- **Date :** 2006 | **Auteurs :** Ilias Tsiakas | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la séance qui suit une période de fermeture, avec un traitement séparé des nuits, des week-ends et des jours fériés. **Qui subit la contrainte** : le prix d'ouverture, surtout là où l'enchère d'ouverture est tenue par un spécialiste avec obligation de continuité des prix (il lisse l'ouverture). **Effet sur les bougies** : l'information accumulée pendant la fermeture prédit le rendement espéré **et la volatilité** de la séance. L'effet est plus fort sur les marchés à spécialiste (NYSE de l'époque).

> **Résumé (abstract paraphrasé) :** Un modèle à volatilité stochastique conditionné sur l'information de nuit, qui distingue les types de fermeture, est évalué par méthodes bayésiennes. Un investisseur averse au risque paierait une commission élevée pour passer à une stratégie qui tient compte de l'information de nuit. La valeur est élevée en Europe comme aux États-Unis et résiste à des coûts de transaction raisonnables. (Ce papier était en « résumé introuvable » le 2026-10-14 ; résumé retrouvé.)

### [17] Is Overnight Volatility Overlooked?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3574323
- **Actifs :** futures S&P 500 et Nasdaq-100 (quasi 24h)
- **Plage horaire / Session :** nuit (Globex) contre séance cash
- **Date :** 2020 | **Auteurs :** Zehua Zhang, Ran Zhao | **Citations :** 4

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit puis la séance, et inversement. **Qui subit la contrainte** : la volatilité, qui se propage d'une session à l'autre. **Effet sur les bougies** : **plus de 40 %** de la volatilité journalière a lieu la nuit. La volatilité réalisée de nuit prédit fortement celle de la séance suivante, et réciproquement.

> **Résumé (abstract paraphrasé) :** Avec des données haute fréquence de jour et de nuit sur les futures, les auteurs mesurent la volatilité réalisée du S&P 500 et du Nasdaq-100. Ajouter la volatilité de nuit réduit de 27,8 % l'erreur de prévision de la volatilité de séance. Leur modèle jour-nuit donne les meilleures prévisions de densité hors échantillon. La volatilité calculée sur les futures quasi 24h mesure bien la volatilité journalière.
>
> **Pour nous :** directement utilisable pour le **dimensionnement** des positions et les stops : calculer la volatilité réalisée sur les barres ES/NQ de 0h à 15h30 et l'utiliser pour prévoir l'amplitude de la séance.

### [18] Realized Volatility and Overnight Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1756705
- **Actifs :** S&P 500 et autres marchés non cotés 24h
- **Plage horaire / Session :** nuit (traitement dans la volatilité réalisée)
- **Date :** 2011 | **Auteurs :** Katja Ahoniemi, Markku Lanne | **Citations :** 8

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la nuit. **Qui subit la contrainte** : le modélisateur, plutôt que le marché : c'est un papier de méthode. **Effet sur les bougies** : le choix du traitement du rendement de nuit change le classement des modèles de volatilité. Pour le S&P 500, la définition du rendement de nuit est particulièrement délicate.

> **Résumé (abstract paraphrasé) :** Il n'y a pas de consensus sur la façon d'intégrer le rendement de nuit dans la volatilité réalisée. Le choix modifie les résultats de plusieurs applications courantes, dont la sélection du meilleur modèle de prévision. Les estimateurs pondérés sont préférables. Les auteurs proposent deux mesures alternatives du rendement de nuit du S&P 500.

### [19] Making Money While You Sleep? Anomalies in International Day and Night Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2670841
- **Actifs :** plus de 48 000 actions de 35 pays, dont les États-Unis
- **Plage horaire / Session :** jour contre nuit
- **Date :** 2015 | **Auteurs :** Kevin Aretz, Söhnke M. Bartram | **Citations :** 8

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : séance contre nuit. **Qui subit la contrainte** : non identifié explicitement. **Effet sur les bougies** : 🔴 contrairement aux États-Unis, **à l'international les rendements de jour dépassent ceux de nuit** pour une volatilité comparable. La plupart des anomalies (taille, value, momentum…) viennent du jour. Le momentum de nuit est propre aux États-Unis.

> **Résumé (abstract paraphrasé) :** Les primes sont décomposées en jour et nuit sur 35 pays. Les stratégies sur caractéristiques gagnent le jour et perdent ou font zéro la nuit. Le résultat de Lou, Polk et Skouras (momentum américain la nuit) est l'exception. Les résultats sont robustes, avec des écarts de magnitude entre pays.
>
> **Pour nous :** le drift de nuit n'est **pas universel**. Ne pas supposer qu'un résultat US vaut pour le DAX ou d'autres indices.

---

## D. FX majeurs, or et pétrole : le rendement par session

### [20] Risk and Return Around the Clock

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2606706
- **Actifs :** actions, **devises**, obligations, **matières premières (dont pétrole et or)**
- **Plage horaire / Session :** les 24 heures, heure par heure
- **Date :** 2015 | **Auteurs :** Felix Fattinger, Alexandre Ziegler | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : toutes les heures, avec des pics à l'ouverture et à la clôture du marché de l'actif **ou d'autres marchés**, et aux annonces macro US. **Qui subit la contrainte** : la profondeur de marché, qui baisse avant les annonces programmées car les traders anticipent les gros mouvements. **Effet sur les bougies** : une découverte du prix importante **à toute heure**, et une relation risque/rendement à peu près constante dans la journée. 🔴 La plupart des actifs ne montrent **pas** la courbe en U de la volatilité des actions US. Les pics de volatilité viennent des ouvertures/clôtures et des annonces.

> **Résumé (abstract paraphrasé) :** La découverte du prix est étudiée sur 24 heures pour actions, devises, obligations et matières premières. Elle est importante et efficace à toute heure. La distribution risque/rendement est assez stable d'une heure à l'autre. Diffusion et sauts expliquent les profils de volatilité ; les annonces macro US pèsent beaucoup dans la volatilité due aux sauts. Au moment des sauts, la relation volume/volatilité habituelle ne tient pas pour certains actifs. (Ce papier était en « résumé introuvable » le 2026-10-14 ; résumé retrouvé.)
>
> **Pour nous :** c'est le seul papier de cette session qui couvre **pétrole et FX** ensemble. Message principal : en dehors des actions, il n'y a **pas de « nuit » qui paie** en moyenne. Le rendement par heure est proportionnel au risque. Les heures à surveiller sont celles des ouvertures d'autres marchés (8h–9h Paris, 15h30) et des annonces.

### [21] 🧪 Who Moves the Price? Trading-Session Return Decomposition and Cross-Session Momentum in Gold and Silver Markets

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7257240
- **Actifs :** or (XAU/USD), argent (XAG/USD), spot horaire
- **Plage horaire / Session :** Asie (1h–9h Paris en hiver), Europe (9h–15h30), US jusqu'à minuit UTC
- **Date :** 2026 | **Auteurs :** Wenling Wei | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant la **session asiatique**. **Qui subit la contrainte** : les acheteurs asiatiques et les banques centrales, qui accumulent de l'or depuis 2022 et fixent le prix marginal à l'Est. **Effet sur les bougies** : la session Asie a fait **77 %** du rendement cumulé de l'or (62 % pour l'argent), l'Europe a ajouté une part positive, et la session **US a retiré** du rendement (-13 %), tout en étant la plus volatile. Les rendements de session ont un léger **momentum**, surtout vers la session asiatique (autocorrélation de +0,13).

> **Résumé (abstract paraphrasé) :** Les rendements de l'or et de l'argent sont découpés en trois sessions sur juillet 2024 – août 2026, période de forte hausse (+81 % pour l'or). L'Asie contribue positivement chaque année ; la correction de 2026 a eu lieu presque entièrement en heures US. Après 0,02 % de frais par changement de position, seule la version **long uniquement** du momentum de session survit, avec un Sharpe net de 1,68 sur l'or et un drawdown divisé par deux environ. Le momentum à l'intérieur de la session US perd de l'argent après frais.
>
> **Pour nous :** c'est l'équivalent du « drift overnight » pour l'or : la « nuit » européenne (session asiatique) porte la hausse. 🔴 L'échantillon est court (2 ans) et en pleine tendance haussière : à revalider sur notre historique XAUUSD long (avant 2022, quand l'or était plutôt fixé à Londres). Test simple : rendement de 1h à 9h Paris contre le reste, par année.

---

## E. Synthèse : ce qui est testable en OHLCV

1. **Indices US, découper la nuit** : le rendement de nuit n'est pas uniforme. Il est concentré sur l'**ouverture européenne** (8h–10h Paris) [1] et sur l'**ouverture cash** (poussée des particuliers) [2] [3] [4]. Les futures ES/NQ permettent de mesurer chaque morceau.
2. **Conditionnement par la veille** : après une séance de **baisse**, rebond de nuit fort [1] [8] [14] ; après une **hausse**, ouverture poussée par l'extrapolation [4]. Après une **nuit** de baisse, la séance continue de baisser puis la nuit suivante rebondit [8].
3. **NQ plutôt qu'ES** : beta plus élevé [6], stratégie de nuit viable seulement sur NQ après coûts [14], et retournement nuit → séance disparu sur le S&P 500 [9].
4. **Gros gaps** : retournement de court terme [10], mais le gap absorbe déjà toute l'information extérieure (Bitcoin) [13].
5. **FX et pétrole** : pas de prime de nuit en moyenne [20]. Pour le FX, voir les papiers déjà fournis (Krohn et al., Ranaldo : la devise domestique se déprécie pendant ses heures de marché).
6. **Or** : la session asiatique porte la hausse depuis 2022 [21]. À vérifier avant 2022.
7. **Volatilité** : la volatilité de nuit des futures prédit celle de la séance [17] ; à utiliser pour la taille des positions.

**Tests proposés** (à pré-enregistrer, comme les précédents) :
- **H1 (overnight drift conditionnel)** : rendement ES/NQ de 8h00 à 10h00 Paris, en fonction du rendement de la séance cash de la veille (quintiles). Attendu : plus fort après une séance baissière [1].
- **H2 (cycle Abdi)** : si gap < 0 et séance < 0, long de la clôture à l'ouverture suivante. Comparer à la nuit inconditionnelle [8].
- **H3 (or par session)** : part du rendement XAUUSD de 1h à 9h Paris, par année depuis le début de l'historique ; long-only sur cette fenêtre contre buy-and-hold [21].
- **H4 (FX par session)** : même découpage Asie/Europe/US sur EURUSD, USDJPY, GBPUSD, comme contrôle négatif attendu [20].

### Résumé introuvable, à revoir (SSRN et Semantic Scholar bloquent l'accès automatique)
- Overnight Reversal and the Asymmetric Reaction to News (Dangl, Salbrechter) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4307675
- Overnight Returns as a Market Timing Strategy (Kelly) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3692068
- Gold and Silver Shine During the Day (Kelly) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5976178
- Liquidity Provision in the Overnight Foreign Exchange Market (Bjønnes, Rime, Solheim) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=882835
- How Does the Daily Volatility of Foreign Exchange Rates Depend on the Time of Day at Which the Daily Returns Are Calculated? (Doman, Doman) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3651344
- The Dynamics of Linkages Between Major Currencies: How Does It Change Depending on the Time of Day? (Doman, Doman) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3652087
- Does Unconstrained Short Selling Result in Unbiased Security Prices? Evidence from the Weekend Effect in Futures Markets (Singal, Tayal) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2433233
- Mind the Gap: Is There a Trading Break Equity Premium? (Perras, Wagner) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4284444
- Investigating the Sources of Day and Night Returns (Hill-Kleespie) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3728858
- Volume Shocks and Overnight Returns (Cartea, Cucuringu, Jin, Wilson) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5156605
- Overnight Return Momentum and the Timing of Trading Volume (Perreten, Wallmeier) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5004991
- Exploring Market Anomalies with Nearly 12 Million Intraday and Overnight Stock Market Records (Zirk-Sadowski, Hryckiewicz) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5169186
- Volatility Around the Clock: Bayesian Modeling and Forecasting of Intraday Volatility in the Financial Crisis (Johannes, Stroud) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2175338
- Volume, Intraday and Overnight Returns for Volatility Prediction: Profitability or Accuracy? (Fuertes, Kalotychou, Todorovic) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1438041
