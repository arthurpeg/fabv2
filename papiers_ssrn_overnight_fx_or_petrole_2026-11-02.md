# Papiers SSRN : l'overnight sur FX majeurs, or et pétrole (quatrième série)

*Session du 2026-11-02. Suite de [papiers_ssrn_overnight_2026-10-21.md](papiers_ssrn_overnight_2026-10-21.md), [papiers_ssrn_overnight_2_2026-10-29.md](papiers_ssrn_overnight_2_2026-10-29.md) et [papiers_ssrn_overnight_3_2026-10-29.md](papiers_ssrn_overnight_3_2026-10-29.md). Périmètre restreint aux **FX majeurs, à l'or et au pétrole** (indices US exclus). Recherche par l'**API Crossref filtrée sur les DOI SSRN** (`prefix:10.2139`) : 98 requêtes, environ 750 candidats triés par titre puis par résumé. Résumés venant de Crossref, **paraphrasés en français**. Tous les papiers déjà fournis (voir [papers/seen_papers.json](papers/seen_papers.json)) sont exclus.*

**Mots-clés** : overnight returns (foreign exchange, currency, gold, crude oil, commodity futures), overnight anomaly, overnight drift, night trading / night session, day-night returns, close-to-open, non-trading period returns, trading period vs non-trading period, Asian session, Asian hours, Tokyo session, Tokyo fixing, Gotobi, Sydney open, London open, New York close, FX rollover 5pm, FX weekend gap, Sunday open, around-the-clock trading, time of day, time zone, working hours, home bias trading hours, gold Asian session, Shanghai gold night session, Tokyo Commodity Exchange gold, COMEX Asian, gold London fix, gold weekend / Monday effect, crude oil night, oil futures Globex, oil weekend gap, oil overnight news, OPEC intraday, Brent/WTI price discovery intraday, energy futures time of day.

**Légende** : 🔴 échec ou condition limite · ⚠️ le signal dépend d'une donnée non OHLCV (flux, interventions, annonces) ou d'un marché hors périmètre · 🧪 papier SSRN récent d'auteur indépendant, non relu par des pairs

**Écartés comme doublons** de papiers déjà fournis : Ranaldo, *Segmentation and Time-of-Day Patterns in FX* (SSRN 960209, version publiée fournie le 2026-10-11) ; Hauptfleisch-Putniņš-Lucey, *Who Sets the Price of Gold?* (SSRN 2606587, fourni le 2026-10-11) ; Tolušić, *The First Hour* (SSRN 7356684, nouvelle version du 7135159 fourni le 2026-10-13 et testé au n° 6) ; Zhang, *Price Discovery in Gold Markets: China and the U.S.* (SSRN 2528721, version antérieure de [10]).

---

## 0. Ce que « nuit » veut dire selon l'actif (heure d'hiver depuis le 1er novembre)

- **FX majeurs** : la journée FX se coupe à **17:00 New York** (23:00 Paris), heure du rollover. La « nuit » d'un trader européen ou américain est la **session asiatique** (Sydney puis Tokyo, environ 23:00 à 8:00 Paris). Le futur CME (6E, 6J, 6B, 6A) s'arrête de 17:00 à 18:00 NY : c'est le gap quotidien du futur.
- **Or** : le futur GC s'arrête aussi de 17:00 à 18:00 NY ; la nuit est portée par **Tokyo (TOCOM), Hong Kong et Shanghai** (SGE, séance de nuit SHFE de 21:00 à 2:30 heure de Pékin, soit 14:00 à 19:30 Paris). Notre rapport [reports/gc_sessions_report](reports/gc_sessions_report.md) : seule la reprise 17:00 NY → 9:00 Shanghai est significative.
- **Pétrole** : CL s'arrête de 17:00 à 18:00 NY ; il n'existe pas de grand marché de pétrole en Asie qui « porte » la nuit (le contrat INE de Shanghai est hors périmètre). 🔴 **La littérature SSRN sur l'overnight du pétrole est quasi vide** : un seul papier exploitable [15], plus un sans résumé.

---

## A. FX : qui fait le prix la nuit, et dans quel sens ?

### [1] Intraday Patterns in Foreign Exchange Returns and Realized Volatility

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3138756
- **Actifs :** 16 devises contre dollar (dont les majeures), 2010-2015
- **Plage horaire / Session :** heures de la session domestique de chaque devise contre heures US **après la clôture de Londres** (environ 17:30-23:00 Paris)
- **Date :** 2018 | **Auteurs :** Hao Zhang | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant la session domestique (baisse), puis pendant l'après-midi US une fois Londres fermé (hausse). **Qui subit la contrainte** : les teneurs de marché, qui absorbent le flux d'ordres local ; leur risque d'inventaire, mesuré par la volatilité réalisée et la sensibilité du prix au flux, fixe l'ampleur. **Effet sur les bougies** : la devise domestique **se déprécie** pendant ses propres heures et **s'apprécie** pendant les heures US d'après-Londres. Le profil existe aussi pour des devises à contrôle des capitaux.

> **Résumé (abstract paraphrasé) :** Sur 16 devises contre dollar en haute fréquence (2010-2015), les devises domestiques baissent pendant leur session et montent pendant la session US une fois Londres fermé. Le profil est significativement lié à la volatilité réalisée, qui reflète le risque du flux d'ordres et la sensibilité du marché à ce flux, chez soi et à l'étranger.
>
> **Pour nous :** c'est l'extension 2010-2015 de Breedon-Ranaldo (fourni le 2026-10-11). Pour EUR et GBP, le bloc à tester est **17:30 → 23:00 Paris** (après Londres, avant le rollover) : la devise européenne devrait y monter. Pour JPY et AUD, la session domestique est la **nuit** européenne : USDJPY devrait monter pendant Tokyo (yen qui baisse). ⚠️ La saisonnalité des fixings est déjà au registre (mouvements de 1 à 2,5 ticks pour un coût de 1,8 à 2 ticks) : vérifier que l'effet par bloc de plusieurs heures dépasse ce coût.

### [2] Pricing Errors and the Geography of Trade in the Foreign Exchange Market

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2446584
- **Actifs :** taux de change majeurs contre dollar
- **Plage horaire / Session :** cycle de 24 h : **session asiatique** → chevauchement Europe / New York
- **Date :** 2014 | **Auteurs :** Louis R. Piccotti | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : les erreurs de prix sont **maximales pendant la session asiatique**, puis diminuent jusqu'au chevauchement Europe-New York (14:00-17:30 Paris), où le cycle recommence. **Qui subit la contrainte** : les traders hors de leur place d'origine, qui supportent des coûts plus élevés, surtout des coûts **sans lien avec l'information** (liquidité, inventaire). **Effet sur les bougies** : la nuit asiatique produit des prix plus bruités, donc des écarts temporaires qui se corrigent ; chaque devise a moins de bruit pendant ses propres heures.

> **Résumé (abstract paraphrasé) :** Les erreurs de prix des taux de change sont les plus fortes en Asie et décroissent jusqu'au chevauchement Europe-New York. Le profil varie selon la devise ; chaque devise est moins bruitée pendant ses heures domestiques. Les coûts sans lien avec l'information comptent au premier ordre, ceux liés à l'information au second.
>
> **Pour nous :** fonde l'hypothèse « un mouvement de nuit asiatique sur EURUSD ou GBPUSD est en partie du bruit, corrigé à l'ouverture européenne » (H9 de la série 3). Sur USDJPY et AUDUSD, la nuit est au contraire la session la moins bruitée : ne pas les traiter comme EUR et GBP.

### [3] Where Does Price Discovery Occur in FX Markets?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=966446
- **Actifs :** FX, transactions interdealers par place géographique
- **Plage horaire / Session :** 24 h, par fuseau régional (Asie, Londres, New York…)
- **Date :** 2007 | **Auteurs :** Chris D'Souza | **Citations :** 6

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant les heures ouvrées de chaque région. **Qui subit la contrainte** : les dealers étrangers, moins bien placés pour traiter l'information fondamentale d'un pays que les dealers du pays. **Effet sur les bougies** : les transactions initiées à **Londres et New York** contiennent plus d'information que celles initiées ailleurs ; le flux de nuit (Asie) déplace donc moins durablement le prix.

> **Résumé (abstract paraphrasé) :** L'auteur mesure le contenu en information des transactions interdealers sur une longue période. Il existe des asymétries d'information : les ordres initiés à Londres et New York sont plus informatifs, et l'information dépend des heures ouvrées régionales. Les traders du pays ont un avantage pour traiter l'information fondamentale, comme Hau (2005) l'avait trouvé sur les actions.
>
> **Pour nous :** même conclusion que Wang-Yang (série 3, [2]) : la nuit asiatique **suit** et ne mène pas EUR/GBP. ⚠️ Mesure par le flux d'ordres, non disponible en OHLCV ; seul le corollaire (retournement à l'ouverture de Londres) est testable.

### [4] The Microstructure of Currency Markets: An Empirical Model of Intra-Day Return and Bid-Ask Spread Behavior

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=252510
- **Actifs :** USD/DEM (cotations 1996)
- **Plage horaire / Session :** 24 h, avec la **pause déjeuner asiatique** et la nuit comparées au jour
- **Date :** 2001 | **Auteurs :** Paolo Pasquariello | **Citations :** 3

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : la volatilité baisse autour de la **pause déjeuner de Tokyo** (environ 4:30-5:30 Paris), monte pendant la matinée de Londres, culmine à l'ouverture de New York puis retombe avec la clôture européenne. **Qui subit la contrainte** : les dealers, dont les coûts de transaction varient au cours de la journée (spread en U inversé). **Effet sur les bougies** : la volatilité est **nettement plus forte le jour que la nuit** ; les bougies de nuit sont petites et à spread relatif plus élevé.

> **Résumé (abstract paraphrasé) :** Sur les cotations USD/DEM de 1996, le spread suit un profil en U inversé et la variance des rendements est ordonnée au cours de la journée : creux au déjeuner asiatique, hausse le matin à Londres, pic à l'ouverture de New York. La volatilité est plus forte en séance que la nuit. Un modèle structurel relie le spread à des coûts de transaction asymétriques et variables.
>
> **Pour nous :** utile pour **dimensionner** un stop de nuit (une ATR calculée sur la journée surestime la nuit) et rappelle que le coût relatif (spread / amplitude) est **maximal la nuit** : tout signal de nuit FX doit battre un coût plus lourd en proportion.

### [5] Do Both U.S. and Foreign Macro Surprises Matter for the Intraday Exchange Rate? Evidence from Japan

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1356123
- **Actifs :** USD/JPY, rendements 5 minutes
- **Plage horaire / Session :** annonces japonaises (matinée de Tokyo, **0:50 Paris** en hiver) et annonces US (8:30 NY)
- **Date :** 2009 | **Auteurs :** Rasmus Fatum, Michael M. Hutchison, Thomas Wu | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : dans les minutes qui suivent les publications macro japonaises (nuit européenne) et américaines. **Qui subit la contrainte** : les traders de yen, qui révisent leurs anticipations à la surprise (écart publication / consensus). **Effet sur les bougies** : les surprises japonaises pèsent **autant** que les surprises US sur les bougies 5 minutes ; deux des quatre annonces les plus influentes sont japonaises. Les réactions sont asymétriques selon le signe et dépendent du cycle japonais.

> **Résumé (abstract paraphrasé) :** L'étude mesure la réaction de USD/JPY à 5 minutes aux surprises macro des deux pays. Les nouvelles japonaises ont une influence comparable aux nouvelles US, deux des quatre plus importantes sont japonaises, et le résultat tient avec trois méthodes. La réaction est asymétrique et dépend de la phase du cycle japonais.
>
> **Pour nous :** ⚠️ le signal demande un calendrier des annonces et le consensus (donnée non OHLCV). Usage OHLCV : les barres 0:50 Paris (Tankan, PIB, CPI de Tokyo…) sont des **barres d'information** de la nuit sur 6J ; à exclure ou à isoler dans un test de nuit sur le yen, comme l'a montré le n° 14 (les nuits d'annonce sont les meilleures sur NQ).

### [6] The Weekend Effect: A Trading Robot and Fractional Integration Analysis

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2463560
- **Actifs :** FX (paires majeures), **or**, indices
- **Plage horaire / Session :** la plus longue « nuit » : clôture du vendredi → reprise du dimanche soir / lundi
- **Date :** 2014 | **Auteurs :** Guglielmo Maria Caporale, Luis A. Gil-Alana, Alex Plastun, Inna Makarenko | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le lundi, après la fermeture du week-end. **Qui subit la contrainte** : non identifié (anomalie de calendrier). **Effet sur les bougies** : les stratégies qui exploitent l'effet week-end sont **rentables dans la plupart des cas sur le FOREX**, seulement dans une minorité de cas sur l'or et les actions ; l'ordre d'intégration fractionnaire est le plus bas le lundi.

> **Résumé (abstract paraphrasé) :** Deux méthodes testent l'effet week-end : un robot de trading qui reproduit les décisions d'un trader, et l'estimation du paramètre d'intégration fractionnaire. Les stratégies week-end rapportent dans une minorité de cas pour l'or et les actions, dans la plupart des cas pour le FX. Le lundi a l'ordre d'intégration le plus bas.
>
> **Pour nous :** 🔴 mêmes auteurs que le contrarien sur l'or (Caporale-Plastun), dont le signe s'est **inversé** sur nos données (registre, 2026-10-12). Notre reprise de l'or est **nulle le lundi** (run_gc_reprise.py) : le lundi est donc à traiter à part, pas comme un signal. Test simple : rendement vendredi 17:00 NY → dimanche 18:00 + 1 h sur 6E, 6J, GC, par année.

---

## B. Or : la séance de nuit asiatique fait-elle le prix ?

### [7] Price Discovery in the Chinese Gold Market

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2776581
- **Actifs :** or au comptant (SGE) et futures (SHFE)
- **Plage horaire / Session :** trois sessions par jour, dont la **séance de nuit** (21:00-2:30 Pékin, soit 14:00-19:30 Paris)
- **Date :** 2016 | **Auteurs :** Muzhao Jin, Youwei Li, Jian-Xin Wang, Yung Chiang Yang | **Citations :** 3

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant chacune des trois sessions, et surtout pendant la **séance de nuit** chinoise. **Qui subit la contrainte** : le marché au comptant, qui suit le futur. **Effet sur les bougies** : la découverte du prix chinois se fait d'abord sur le **futur**, dans toutes les sessions ; la découverte séquentielle (d'une session à l'autre) se fait **davantage la nuit**, c'est-à-dire pendant l'après-midi européen et l'ouverture du COMEX.

> **Résumé (abstract paraphrasé) :** Le futur domine la découverte du prix de l'or en Chine, quelle que soit la mesure (part d'information, part de composante, part de leadership). En découpant la journée en trois sessions, la domination du futur se retrouve partout. La découverte séquentielle sur les deux marchés se fait plus pendant la séance de nuit.
>
> **Pour nous :** la « nuit » chinoise coïncide avec **notre journée** (Londres après-midi, COMEX matin). Elle n'explique donc pas notre reprise 17:00 NY → 9:00 Shanghai ; elle explique plutôt que la séance de jour de Shanghai (2:30-8:30 Paris) apporte peu d'information neuve. Cohérent avec notre résultat : la session Asie SGE seule est nulle (registre, 2026-11-01).

### [8] Night Trading and Intraday Return Predictability: Evidence from Chinese Metal Futures Market

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4282926
- **Actifs :** futures SHFE sur or, argent, cuivre (haute fréquence)
- **Plage horaire / Session :** **première demi-heure de la séance de nuit** (21:00-21:30 Pékin, 14:00-14:30 Paris) → reste de la séance
- **Date :** 2022 | **Auteurs :** Gaoping Ma, Elie Bouri, Yahua Xu, Z. Ivy Zhou | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : avant 2013, la première demi-heure **de jour** prédisait la suite ; depuis l'ouverture de la séance de nuit, c'est la première demi-heure **de nuit**. **Qui subit la contrainte** : les investisseurs chinois, qui réagissent tout de suite aux nouvelles internationales publiées dans leur soirée (annonces US de 8:30 NY = 21:30 Pékin en été). **Effet sur les bougies** : un rendement de début de nuit qui se **prolonge** ; prédictibilité plus forte les jours de volatilité et de volume élevés et les jours de nouvelles globales.

> **Résumé (abstract paraphrasé) :** L'arrivée de la séance de nuit au SHFE en 2013 a déplacé la prédictibilité intraday : la première demi-heure de nuit prédit désormais le rendement suivant. L'explication est la réaction immédiate des investisseurs domestiques aux nouvelles internationales du soir. Une stratégie de timing bat l'achat-conservation ; la prédictibilité augmente avec la volatilité, le volume et les nouvelles globales positives.
>
> **Pour nous :** ⚠️ marché chinois hors périmètre, mais le mécanisme se transpose : sur **GC**, la fenêtre équivalente est l'ouverture SHFE de nuit (14:00 Paris) et les annonces US de 8:30 NY (14:30 Paris). Hypothèse : le rendement GC 13:30 → 15:00 Paris prédit le signe de 15:00 → 19:30 Paris (fin de la séance de nuit chinoise). C'est de la séance de jour pour nous, pas notre nuit.

### [9] Information Transmission Among World Major Gold Futures Markets: Evidence from High Frequency Synchronous Trading Data

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2131592
- **Actifs :** futures sur or COMEX (New York), MCX (Inde), **TOCOM (Tokyo)**
- **Plage horaire / Session :** heures où les trois marchés cotent en même temps
- **Date :** 2012 | **Auteurs :** Rapeesorn Fuangkasem, Pornchai Chunhachinda, Sarayut Nathaphan | **Citations :** 5

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant les heures de chevauchement. **Qui subit la contrainte** : les marchés asiatiques (TOCOM, MCX), qui suivent le COMEX. **Effet sur les bougies** : l'information se diffuse vite d'une place à l'autre, mais le **COMEX reste le centre** de la découverte du prix : une bougie de nuit sur GC électronique reflète d'abord le COMEX lui-même, pas Tokyo.

> **Résumé (abstract paraphrasé) :** Avec des données intraday synchrones (qui évitent le problème des prix périmés en données journalières), les trois futures sur or sont cointégrés et suivent un facteur commun. L'information circule vite entre les bourses, mais un lien meneur-suiveur demeure, avec le COMEX en tête.
>
> **Pour nous :** en contradiction avec [10] (Chine qui mène) : la domination dépend de la période (2012 contre 2014-2015) et de la place asiatique. Pour GC, la nuit asiatique n'est pas une source d'information propre au moins jusqu'en 2012 ; notre reprise 17:00 → 20:00 NY ressemble donc plus à une **prime de portage** (le gap de l'arrêt) qu'à de l'information asiatique.

### [10] Price Discovery in Gold Markets: China and the US

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2564688
- **Actifs :** futures sur or SHFE et COMEX, or au comptant chinois
- **Plage horaire / Session :** heures communes ; les deux marchés **se relaient**
- **Date :** 2015 | **Auteurs :** Dong Zhang | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : selon les périodes, le meneur change. **Qui subit la contrainte** : le COMEX, qui suit le SHFE sur l'échantillon, contrairement à la littérature antérieure. **Effet sur les bougies** : le futur chinois contribue **plus** que le futur américain à la découverte du prix ; les deux marchés « prennent leur tour » comme meneur.

> **Résumé (abstract paraphrasé) :** La Chine est devenue le premier consommateur d'or et son futur l'un des plus grands au monde. En combinant part d'information et part de composante (méthode de Yan-Zivot et Putniņš, robuste aux différences de bruit), l'auteur trouve que le futur chinois sert bien le comptant chinois et **mène le futur américain**. Les deux marchés alternent comme meneur.
>
> **Pour nous :** argument pour une session asiatique informative sur l'or **depuis 2014**, cohérent avec Wei (série du 2026-10-21 : la hausse de l'or depuis 2024 est portée par l'Asie). Test : la corrélation entre le rendement GC de la séance de jour de Shanghai (2:30-8:30 Paris) et celui de la journée COMEX suivante, avant et après 2014.

### [11] Market Openness and Price Discovery in Gold Markets

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2951302
- **Actifs :** or SGE et SGE International (SGEI, ouvert aux étrangers en 2014)
- **Plage horaire / Session :** heures de Shanghai (session asiatique)
- **Date :** 2017 | **Auteurs :** Caihong Xu, Dong Zhang | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : après l'ouverture du SGE aux investisseurs étrangers (septembre 2014). **Qui subit la contrainte** : les marchés occidentaux, dont la part dans la formation du prix mondial baisse. **Effet sur les bougies** : la part du SGE dans la découverte du prix **international** augmente ; une plus forte liquidité relative et une volatilité plus basse renforcent la contribution d'une place, les gros ordres la réduisent.

> **Résumé (abstract paraphrasé) :** Les étrangers inscrits au SGEI ont préféré trader sur le SGE, plus liquide et moins cher ; le volume du SGEI est vite tombé à presque zéro. Après l'ouverture, la contribution du SGE au prix international de l'or a augmenté, même en contrôlant liquidité, volatilité et taille des ordres.
>
> **Pour nous :** date de rupture candidate pour la session asiatique de l'or : **septembre 2014**. Nos données GC commencent en 2010-2016 selon les fichiers : séparer avant / après 2014 quand c'est possible.

### [12] Day of the Week Effect on Gold Returns

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2229290
- **Actifs :** futures sur or MCX (Inde), 2006-2012
- **Plage horaire / Session :** rendement **de séance** (ouverture → clôture) contre **hors séance** (clôture → ouverture suivante)
- **Date :** 2013 | **Auteurs :** Sunita Arora, Narender Garg | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : selon le jour de la semaine, et surtout **hors séance**. **Qui subit la contrainte** : non identifié. **Effet sur les bougies** : un effet jour de la semaine sur les trois séries (veille-veille, séance, hors séance), **plus fort pour le rendement hors séance** que pour la séance.

> **Résumé (abstract paraphrasé) :** Les prix d'ouverture et de clôture du futur or du MCX sont décomposés en rendement de séance et hors séance. Des variables muettes par jour (six jours de cotation), corrigées d'un GARCH(1,1) et complétées d'une analyse des valeurs extrêmes, montrent un effet jour de la semaine sur les trois séries, plus marqué hors séance.
>
> **Pour nous :** 🔴 marché indien, faible qualité (pas de correction pour tests multiples). Seul intérêt : confirme que l'effet calendaire de l'or se loge **dans la nuit**. Cohérent avec notre reprise GC nulle le lundi et à +2,5 bp les autres jours.

### [13] Analysis of Selected Seasonality Effects in the Following Metal Markets: Gold, Silver, Platinum, Palladium and Copper

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2598514
- **Actifs :** or, argent, platine, cuivre (LME / prix de Londres), palladium, 1994-2014
- **Plage horaire / Session :** effet week-end (clôture du vendredi → lundi)
- **Date :** 2015 | **Auteurs :** Krzysztof Borowski, Małgorzata Łukasik | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le **week-end**. **Qui subit la contrainte** : non identifié. **Effet sur les bougies** : pas d'effet mensuel (sauf septembre sur le palladium), pas d'effet jour de la semaine, mais un **effet week-end** sur l'or et le cuivre.

> **Résumé (abstract paraphrasé) :** Sur vingt ans de prix de métaux à Londres, aucun effet mensuel n'apparaît sur l'or, l'argent, le platine et le cuivre ; septembre se distingue sur le palladium. Il n'y a pas d'effet jour de la semaine, mais un effet week-end sur l'or et le cuivre.
>
> **Pour nous :** deuxième indice (avec [6] et [12]) que la nuit du week-end de l'or est **différente** des autres nuits. Le sens de l'effet n'est pas donné dans le résumé : à lire avant de pré-enregistrer.

### [14] Volatility in the Gold Futures Market

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=996235
- **Actifs :** futures sur or CBOT, 1999-2005, intraday
- **Plage horaire / Session :** volatilité intraday et entre jours (estimateur de Garman-Klass sur OHLC)
- **Date :** 2007 | **Auteurs :** Jonathan A. Batten, Brian M. Lucey | **Citations :** 4

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : au fil de la journée et de la semaine. **Qui subit la contrainte** : les teneurs de marché, selon les théories de microstructure (arrivée de l'information, chevauchement des places). **Effet sur les bougies** : la volatilité varie significativement au cours de la journée et de la semaine ; elle n'est que faiblement liée au volume mesuré en nombre de transactions.

> **Résumé (abstract paraphrasé) :** En plus des modèles GARCH, les auteurs utilisent l'estimateur de Garman-Klass (ouverture, plus haut, plus bas, clôture) pour mesurer la volatilité intraday et entre jours de l'or. La volatilité varie selon l'heure et le jour, comme le prévoit la microstructure, et dépend peu du nombre de transactions.
>
> **Pour nous :** méthode 100 % OHLCV utile pour comparer la volatilité de nuit et de jour de GC (calibrage des stops de nuit). Pas de signal directionnel.

---

## C. Pétrole

### [15] Intraday Momentum and Return Predictability: Evidence from the Crude Oil Market

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3553682
- **Actifs :** pétrole brut (ETF USO, haute fréquence, 2006-2018)
- **Plage horaire / Session :** **nuit** (clôture → ouverture 9:30 NY) + première demi-heure → **dernière demi-heure** (15:30-16:00 NY)
- **Date :** 2020 | **Auteurs :** Zhuzhu Wen, Xu Gong, Diandian Ma, Yahua Xu | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le rendement de la première demi-heure (nuit comprise) prédit celui de la dernière demi-heure. **Qui subit la contrainte** : les gérants qui **rebalancent rarement** et les **investisseurs informés en retard**, qui traitent en fin de séance l'information arrivée la nuit. **Effet sur les bougies** : seule la première demi-heure prédit (positivement) la dernière ; en décomposant, c'est la **composante de nuit** qui porte l'essentiel de l'information. Le volume intraday du pétrole a un profil propre, créé par les deux publications de stocks (API, EIA), mais ces publications ne prédisent pas la dernière demi-heure.

> **Résumé (abstract paraphrasé) :** L'effet momentum intraday des actions est étendu au pétrole. Contrairement aux actions, seule la première demi-heure prédit la dernière, et une stratégie de timing est très rentable. La décomposition montre que le rendement de nuit contient plus d'information que la première demi-heure de séance. Le rééquilibrage peu fréquent et les investisseurs en retard expliquent l'effet. Les annonces de stocks créent un profil de volume particulier sans prédire la fin de séance.
>
> **Pour nous :** c'est le seul papier « nuit » du pétrole, et il prédit la **dernière demi-heure**, pas la nuit elle-même. 🔴 Le momentum intraday de Gao est au registre comme échec sur les indices, et sur les futures FX il ne passe pas les coûts. Sur CL, c'est **non testé**. Attention : USO suit les heures NYSE (9:30-16:00 ET), alors que la séance de référence du futur CL est **9:00-14:30 ET** (règlement à 14:30). Transposer avec la nuit 14:30 → 9:00 ET + première demi-heure comme signal, et la dernière demi-heure 14:00-14:30 ET comme position.

---

## D. Les fixings qui bordent la nuit (fin de journée FX et or)

### [16] Price Manipulation and Collusion around the London 4pm Fix

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4819478
- **Actifs :** EUR/USD (transactions EBS)
- **Plage horaire / Session :** avant et pendant le fix WM/Reuters de 16:00 Londres (17:00 Paris)
- **Date :** 2024 | **Auteurs :** Paolo Colla, Walter Distaso, Paolo Vitale | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : bien **avant** la fenêtre du fix, et plus encore en **fin de mois**. **Qui subit la contrainte** : les clients qui passent des ordres « au fix » ; les grands dealers qui partagent l'information de couverture les **devancent**. **Effet sur les bougies** : volatilité et coûts plus forts **avant** le fix que pendant ; la manipulation augmente avec la demande de couverture (fin de mois).

> **Résumé (abstract paraphrasé) :** Un modèle où plusieurs grands dealers reçoivent des ordres « fill-at-fix » en avance montre que, s'ils partagent l'information et se coordonnent, ils gagnent à devancer leurs clients. Cela augmente les coûts et la volatilité avant le fix et s'intensifie quand la demande de couverture est forte, par exemple en fin de mois. Les données EBS sur EUR/USD confirment ces prédictions.
>
> **Pour nous :** ⚠️ hors nuit stricte (17:00 Paris), mais c'est la dernière bougie avant la session américaine d'après-Londres de [1]. 🔴 Le retournement après le fix de fin de mois est au registre (n° 7, Melvin-Prins, +2,4 pips non significatif) : ne pas rouvrir.

### [17] Dealer Trading at the Fix

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4923197
- **Actifs :** fixes FX, **or** et argent
- **Plage horaire / Session :** autour des fixes (fix de Londres 16:00, fixes de l'or AM / PM)
- **Date :** 2024 | **Auteurs :** Carol L. Osler, Alastair Turnbull | **Citations :** 0

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à l'approche du fix puis juste après. **Qui subit la contrainte** : les clients « fill-at-fix », dont les dealers OTC contrôlent l'exécution en tradant aussi pour compte propre. **Effet sur les bougies** : **forte volatilité avant le fix**, **tendance qui accélère** à l'approche du fix, puis **retracement partiel** après.

> **Résumé (abstract paraphrasé) :** Un modèle de trading optimal entre dealers OTC qui exécutent les ordres au fix de leurs clients et tradent pour leur compte explique sept faits documentés sur le FX, l'or et l'argent : devancement, « banging the close », partage d'information, collusion, volatilité avant le fix, retracement partiel après, et tendance qui accélère. Un test statistique de l'accélération de la tendance autour des fix FX soutient le modèle.
>
> **Pour nous :** donne le **sens** du profil (tendance avant, retracement partiel après), déjà testé sur le fix de Londres FX (registre : 1 à 2,5 ticks pour 1,8 à 2 de coût). Pour l'or, la session « COMEX après le fix PM » est nulle sur nos données (registre, 2026-11-01). Rien à rouvrir.

---

## E. Synthèse : l'overnight sur FX, or et pétrole, ce qui est testable en OHLCV

1. **FX** : la nuit asiatique est **bruitée** et **suiveuse** pour EUR et GBP [2] [3], informative pour JPY et AUD pendant leurs heures [1] [2] [5]. La devise européenne monte pendant l'après-midi US d'après-Londres [1]. La volatilité de nuit est faible [4], donc le coût relatif est lourd.
2. **Week-end** : la nuit la plus longue se comporte à part sur le FX [6] et l'or [12] [13] ; notre reprise GC est nulle le lundi.
3. **Or** : la découverte du prix est passée en partie en Asie depuis 2014 [10] [11], après une période dominée par le COMEX [9]. La séance de nuit chinoise tombe pendant **notre** journée [7] [8].
4. **Pétrole** : 🔴 rien sur l'overnight lui-même ; seul le rendement de nuit comme **prédicteur** de la dernière demi-heure [15].

**Tests proposés** (à pré-enregistrer, compteur actuel 1 577) :
- **H12 (FX après Londres)** : rendement de 6E et 6B de 17:30 à 23:00 Paris (11:30 → 17:00 NY), par année 2010-2026, net de 1 tick + 5 $. Attendu positif [1]. Contrôle : le même bloc sur 6J doit être de signe opposé pour le yen (USDJPY en baisse).
- **H13 (bruit asiatique corrigé à Londres)** : si |rendement 6E 23:00 → 8:00 Paris| > 1 écart-type (20 jours), position de signe opposé de 8:00 à 10:00 Paris ; 6J comme contrôle (effet attendu absent) [2] [3]. Proche de H9 (série 3) : à fusionner.
- **H14 (pétrole, momentum de la nuit)** : sur CL, rendement 14:30 ET (veille) → 9:30 ET comme signal, position de 14:00 à 14:30 ET [15]. ⚠️ Le momentum intraday est au registre sur les indices et le FX : condition de réouverture « autre actif, coûts vérifiés » à justifier dans le pré-enregistrement.
- **H15 (or, rupture 2014)** : corrélation entre la séance de jour de Shanghai (2:30-8:30 Paris) et la séance COMEX suivante, 2010-2014 contre 2015-2026 [10] [11].

### Résumé introuvable, à revoir
- London or New York: Where and When Does the Gold Price Originate? (Lucey, Larkin, O'Connor, 2012) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2161905
- Weekend Information Gaps and Systemic Risk Transmission to Oil Markets: A COVOL-Based Analysis (Conlon, Corbet, Larkin, Muñiz, 2025) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5549439
