# Papiers SSRN overnight et session asiatique dont le résumé manquait

*Session du 2026-10-29. Ce fichier reprend tous les papiers du registre [papers/seen_papers.json](papers/seen_papers.json) marqués `no_abstract` dont le **titre** touche à l'overnight (nuit, close-to-open, heures étendues, périodes de fermeture, week-end, 24h/24) ou à la session asiatique (Shanghai, fuseaux horaires, heure de la journée en FX). Cela fait **25 papiers**. Quatre papiers `no_abstract` plus anciens, sur l'intraday sans rapport avec la nuit, sont laissés de côté : 2726505, 4680994, 2137576, 4713271.*

*Nouvelle tentative de récupération des résumés : Crossref (aucun résumé déposé pour ces 25 DOI), API Semantic Scholar (bloquée par la limite de débit), OpenAlex (quota du jour épuisé), puis site Semantic Scholar dans le navigateur, qui a fini par ralentir. Résultat : **4 résumés retrouvés** (partie A). Pour les **21 autres** (partie B), seules les métadonnées sont disponibles.*

**Légende** : 🔴 échec ou condition limite · ⚠️ le signal dépend d'une donnée non OHLCV ou d'un marché hors périmètre · 🧪 papier SSRN récent d'auteur indépendant, non relu par des pairs · ❓ résumé introuvable, contenu **déduit du seul titre, non vérifié**

---

## A. Résumé retrouvé (format habituel)

### [1] Are Extended Hours Prices Predictive of Subsequent Stock Returns?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2809950
- **Actifs :** actions US
- **Plage horaire / Session :** after-hours (16h–20h ET, soit 22h–2h Paris) et pre-market (4h–9h30 ET, soit 10h–15h30 Paris), puis séance principale
- **Date :** 2016 | **Auteurs :** Shai Levi, Joshua Livnat, Li Zhang, Xiao-Jun Zhang | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : pendant les heures étendues, puis la séance qui suit. **Qui subit la contrainte** : les institutionnels qui traitent en heures étendues **pour des besoins de liquidité** les jours sans nouvelle. **Effet sur les bougies** : les **jours normaux**, le rendement des heures étendues est **négativement** lié à celui de la séance (retournement). Les **jours de nouvelle** (résultats, changement de recommandation d'analyste, dépôt SEC), il est **positivement** lié à la séance et même à la dérive de long terme (sous-réaction).

> **Résumé (abstract paraphrasé) :** Les heures étendues sont surtout fréquentées par les institutionnels, les particuliers y étant découragés. Sans nouvelle, le mouvement des heures étendues se retourne pendant la séance, ce qui indique un trading de liquidité. Avec une nouvelle importante, il continue pendant la séance et au-delà : le marché sous-réagit. Le rendement des heures étendues aide donc à prévoir la dérive après une nouvelle.
>
> **Pour nous :** c'est le même partage que Lescourret (série du 2026-10-14) : gap **sans** nouvelle → retournement, gap **avec** nouvelle → continuation. En OHLCV sur ES/NQ, l'approximation la plus simple est le calendrier macro : gap construit avant ou après une annonce de 14h30 Paris.

### [2] Does Unconstrained Short Selling Result in Unbiased Security Prices? Evidence from the Weekend Effect in Futures Markets

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2433233
- **Actifs :** contrats futures (pas de contrainte de vente à découvert)
- **Plage horaire / Session :** autour du **week-end**, la plus longue période de fermeture
- **Date :** 2014 (publié Journal of Futures Markets 2019 sous le titre « Risky Short Positions and Investor Sentiment: Evidence from the Weekend Effect in Futures Markets ») | **Auteurs :** Vijay Singal, Jitendra Tayal | **Citations :** 25

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : avant et après le week-end. **Qui subit la contrainte** : les **vendeurs à découvert**, qui refusent de porter un risque élevé pendant la fermeture du week-end, même sans contrainte réglementaire. **Effet sur les bougies** : les prix des futures sont **biaisés vers le haut autour du week-end**. Le biais est plus fort quand la volatilité est élevée. Le risque des positions longues n'a pas d'effet comparable.

> **Résumé (abstract paraphrasé) :** Les contraintes de vente à découvert ne peuvent pas être supprimées sur les actions, d'où l'utilisation des futures, où long et short sont symétriques. Même sans friction sur le short, les prix sont biaisés à la hausse autour des week-ends, surtout en période de forte volatilité, quand les vendeurs à découvert refusent un risque plus élevé. Le biais vient de l'asymétrie de risque entre positions courtes et longues.
>
> **Pour nous :** c'est directement testable sur ES, NQ, GC (or) et CL (pétrole) : rendement du vendredi soir au lundi matin, conditionné à la volatilité de la semaine. Hypothèse : biais haussier plus fort quand l'ATR est élevé. C'est aussi un mécanisme qui s'applique à la nuit : les shorts sont réduits avant une fermeture, ce qui pousse le prix vers le haut.

### [3] Volume, Intraday and Overnight Returns for Volatility Prediction: Profitability or Accuracy?

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1438041
- **Actifs :** actions (volatilité des titres)
- **Plage horaire / Session :** volume journalier, rendement de séance et rendement de nuit comme prédicteurs
- **Date :** 2010 (publié Review of Quantitative Finance and Accounting 2014) | **Auteurs :** Ana-Maria Fuertes, Elena Kalotychou, Natasa Todorovic | **Citations :** 29

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : le jour suivant. **Qui subit la contrainte** : le trader technique, dont le gain dépend de la prévision de volatilité. **Effet sur les bougies** : en précision statistique, le **rendement de séance** est le meilleur prédicteur de la volatilité du lendemain. En gain économique, c'est la combinaison **rendements journaliers + volume** qui rapporte le plus. Acheter quand la volatilité prévue est **extrêmement élevée** paraît très rentable.

> **Résumé (abstract paraphrasé) :** Le papier compare trois sources d'information pour prévoir la volatilité : volume journalier, rendements de séance et rendements de nuit. La précision statistique et la valeur économique ne se recoupent pas : la première vient des rendements de séance, la seconde du volume. En période de forte volatilité prévue, acheter est rentable, signe d'une forte relation rendement/risque en période de turbulence.
>
> **Pour nous :** 🔴 le rendement de nuit n'est **pas** le meilleur prédicteur de volatilité, contrairement à Zhang-Zhao sur les futures (série du 2026-10-21, mais là avec la volatilité réalisée de nuit, pas un simple rendement). L'achat en volatilité extrême rejoint l'Overnight Drift (rebond après les séances de stress).

### [4] Volatility Around the Clock: Bayesian Modeling and Forecasting of Intraday Volatility in the Financial Crisis

- **Lien SSRN :** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2175338
- **Actifs :** futures sur indice actions, rendements 5 minutes « around the clock » (2007–2012)
- **Plage horaire / Session :** 24h/24, avec profil horaire et annonces
- **Date :** 2012 | **Auteurs :** Michael S. Johannes, Jonathan R. Stroud | **Citations :** 1

> **Mécanisme causal intraday (pourquoi et quand) : Quand** : à toute heure, avec des composantes horaires et des pics aux annonces. **Qui subit la contrainte** : le modélisateur de risque. **Effet sur les bougies** : la volatilité des futures 24h a plusieurs facteurs persistants, des sauts de prix et de volatilité, un profil selon l'heure, et une corrélation entre chocs de rendement et de volatilité.

> **Résumé (abstract paraphrasé) :** Les auteurs estiment un modèle de rendements de futures sur indice à 5 minutes sur les 24 heures, avec volatilité stochastique multi-facteurs, sauts, saisonnalité horaire, effet de levier et effets d'annonce. Une méthode MCMC intégrée estime ensemble les paramètres journaliers et intraday sans passer par la volatilité réalisée. Sur la crise 2007–2009 puis hors échantillon 2009–2012, la prévision de volatilité réalisée s'améliore jusqu'à 50 %.
>
> **Pour nous :** papier de méthode. Il confirme qu'il faut modéliser **l'heure de la journée** sur les futures 24h, nuit comprise, plutôt que de traiter la nuit comme un seul bloc.

---

## B. Toujours sans résumé (❓ contenu déduit du titre seul, non vérifié)

Pour chaque papier : lien, auteurs, date, et ce que le titre laisse attendre. **Rien ici ne vient du papier lui-même.** Ouvrir le lien dans un navigateur suffit à lire le résumé (le blocage SSRN ne vise que les accès automatiques).

### B1. Session asiatique, FX et or

| # | Papier | Auteurs, date | Ce que le titre annonce ❓ |
|---|---|---|---|
| 5 | [Bidirectional Spillovers from Shanghai Gold Futures to London and New York Gold Markets](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5216421) | Shiyan Lou, Yinggui Wang, Zhichen Liu, 2025 | Transmission dans les deux sens entre l'or de Shanghai (session asiatique) et Londres/New York. **Priorité haute** : c'est la question de [21] de la série du 2026-10-21 (rendement de l'or concentré en Asie). |
| 6 | [Gold and Silver Shine During the Day](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5976178) | Michael A. Kelly, 2026 🧪 | Rendement de l'or et de l'argent concentré **en journée** plutôt que la nuit, à l'inverse des actions. « Jour » au sens US probablement, à vérifier : cela pourrait contredire ou compléter Wei (Asie). **Priorité haute.** |
| 7 | [How Does the Daily Volatility of Foreign Exchange Rates Depend on the Time of Day at Which the Daily Returns Are Calculated?](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3651344) | Małgorzata Doman, Ryszard Doman, 2020 | La volatilité « journalière » d'une paire FX change selon l'heure de coupure de la journée (Tokyo, Londres, New York). Utile pour choisir l'heure de clôture des barres journalières FX. |
| 8 | [The Dynamics of Linkages Between Major Currencies: How Does It Change Depending on the Time of Day?](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3652087) | Małgorzata Doman, Ryszard Doman, 2020 | Les corrélations entre majeures varient selon l'heure, donc selon la session (asiatique, européenne, américaine). |
| 9 | [Risk Transmissions around the Clock: Evidence from Bitcoin, Treasury, Commodity, and Equity ETFs](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5022720) | Shimeng Shi, 2024 | Transmission du risque heure par heure, y compris la nuit, entre ETF actions, Treasuries, **matières premières** (or, pétrole probablement) et Bitcoin. Seul candidat restant pour le **pétrole**. |

### B2. Indices US : rendement de nuit

| # | Papier | Auteurs, date | Ce que le titre annonce ❓ |
|---|---|---|---|
| 10 | [Overnight Reversal and the Asymmetric Reaction to News](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4307675) | Thomas Dangl, Stefan Salbrechter, 2022 | Retournement après la nuit, différent selon que la nouvelle est bonne ou mauvaise. Proche de l'asymétrie de l'Overnight Drift. **Priorité haute.** |
| 11 | [Overnight Returns as a Market Timing Strategy](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3692068) | Michael A. Kelly, 2020 | Utiliser le rendement de nuit pour décider quand être investi sur le marché. Même auteur que [6]. **Priorité haute** (signal OHLCV a priori). |
| 12 | [Overnight Returns Following Large Price Movements](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573576) | Anchor Y. Lin, Hung-Yi Lin, Lin-Hsiang Huang, Yueh-Neng Lin, 2023 (publié Finance Research Letters 2024) | Rendement de la nuit qui suit une forte hausse ou baisse en séance. **Priorité haute** : c'est la variable centrale de l'Overnight Drift et du cycle d'Abdi. |
| 13 | [Mind the Gap: Is There a Trading Break Equity Premium?](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4284444) | Patrizia J. Perras, Niklas F. Wagner, 2022 | Existe-t-il une prime pour porter le risque pendant les pauses de cotation (nuit, week-end) ? Wagner est aussi co-auteur de Riedel-Wagner (série 3). |
| 14 | [Investigating the Sources of Day and Night Returns](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3728858) | Austin Hill-Kleespie, 2020 | D'où viennent les rendements de jour et de nuit (probablement mémoire ou thèse). |
| 15 | [Volume Shocks and Overnight Returns](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5156605) | Álvaro Cartea, Mihai Cucuringu, Qi Jin, Mungo Ivor Wilson, 2025 | Un choc de volume en séance prédit-il le rendement de la nuit suivante ? Signal OHLCV direct (volume). |
| 16 | [Overnight Return Momentum and the Timing of Trading Volume](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5004991) | Thomas Perreten, Martin Wallmeier, 2024 | Momentum des rendements de nuit, selon le moment de la journée où le volume se fait. Perreten est l'auteur du papier sur le pre-market (série du 2026-10-14). |
| 17 | [Overnight vs. Intraday Returns: Investor Disagreement, Information Uncertainty, and Future Stock Returns](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5164956) | Richard D. F. Harris, Nan Li, Nicholas Taylor, 2025 | Écart nuit/séance lié au désaccord et à l'incertitude, prédicteur des rendements futurs (actions). Proche de Berkman et al. (série 2). |
| 18 | [Overnight Returns: Investor Sentiment or Investor Attention?](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4015493) | Ahmed Ameya Prapan, Evangelos Vagenas-Nanos, 2022 | Le rendement de nuit mesure-t-il le sentiment ou l'attention ? Prolonge Aboody et al. (série 3). |
| 19 | [The Dynamics of Daily, Intraday and Overnight Betas](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3686528) | Alessandra Insana, 2020 | Beta mesuré séparément sur la nuit et la séance. Prolonge Hendershott et al. (série du 2026-10-21). |
| 20 | [Exploring Market Anomalies with Nearly 12 Million Intraday and Overnight Stock Market Records](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5169186) | Jan Zirk-Sadowski, Aneta Hryckiewicz, 2025 | Grande base de rendements nuit et séance pour tester plusieurs anomalies. |
| 21 | [A Tug of War across the Market: Overnight-vs-Daytime Lead-Lag Networks and Clustering-Based Portfolio Strategies](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5371952) | Yutong Lu, Ning Zhang, Gesine Reinert, Mihai Cucuringu, 2025 | Relations d'avance/retard entre rendements de nuit et de jour de titres différents, et portefeuilles construits dessus. |
| 22 | ⚠️ [Testing a Contrarian Hypothesis: The Predictive Power of Overnight News Sentiment on S&P 500 Intraday Returns](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5723163) | Nikhil Chitturi, 2025 🧪 | Le sentiment des nouvelles de nuit prédit-il, à contre-sens, la séance du S&P 500 ? Demande des données de news. |

### B3. Risque de nuit, week-end et cotation 24h

| # | Papier | Auteurs, date | Ce que le titre annonce ❓ |
|---|---|---|---|
| 23 | [Overnight News and Daily Equity Trading Risk Limits](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2065017) | Katja Ahoniemi, Ana-Maria Fuertes, Jose Olmo, 2012 | Intégrer l'information de nuit dans les limites de risque journalières (VaR) des positions actions. Mêmes auteurs que [3] et qu'Ahoniemi-Lanne (série du 2026-10-21). |
| 24 | [The Weekend Effect: A Trading Robot and Fractional Integration Analysis](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2456123) | Guglielmo Maria Caporale, Luis A. Gil-Alana, Alex Plastun, Inna Makarenko, 2014 | Effet week-end testé par un robot de trading. Caporale et Plastun ont écrit des papiers sur les indices US, le FX, l'or et le pétrole déjà fournis : actifs probablement dans le périmètre. |
| 25 | [24-Hour Trading: Systems and Challenges](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5181265) | Henry Dao, 2025 | Passage des actions à la cotation 24h : systèmes et difficultés. Contexte, probablement sans signal. |

---

## C. À retenir

- **Les 4 résumés retrouvés** ajoutent deux mécanismes testables : retournement du mouvement des heures étendues les jours **sans** nouvelle et continuation les jours **avec** nouvelle [1] ; biais haussier des futures autour du **week-end**, plus fort quand la volatilité est haute [2]. Ce dernier est testable sur ES, NQ, or et pétrole.
- **À lire en priorité à la main** (titre très proche de nos hypothèses) : [12] Overnight Returns Following Large Price Movements, [10] Overnight Reversal and the Asymmetric Reaction to News, [11] Overnight Returns as a Market Timing Strategy, [5] Shanghai Gold Spillovers, [6] Gold and Silver Shine During the Day, [9] Risk Transmissions around the Clock.
