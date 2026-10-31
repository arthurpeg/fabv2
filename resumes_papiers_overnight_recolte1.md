# Résumés détaillés : 1re récolte de papiers overnight (SSRN)

*Rédigé le 2026-10-29 à partir de la lecture intégrale des 18 PDF fournis (texte, tableaux et annexes). La numérotation [n] reprend celle de [papiers_ssrn_overnight_2026-10-21.md](papiers_ssrn_overnight_2026-10-21.md). Tout ce qui suit est extrait des papiers. Quand un chiffre est illisible dans le PDF ou que le papier se contredit, c'est signalé. Les heures sont celles du papier (ET = heure de New York, sauf mention contraire).*

Papiers de la récolte **non fournis** (donc non résumés) : [5] Lou-Polk-Skouras (tug of war), [12] Scheduled Coordination Density, [16] The Economic Value of Conditioning on Overnight Information.

### Index
| # | Papier | Actifs / période | En une ligne (d'après le papier) |
|---|---|---|---|
| [1] | The Overnight Drift (Boyarchenko, Larsen, Whelan) | ES, 1998–2020 | Le gain de l'ES se fait vers 2:00–3:00 ET (ouverture européenne), surtout après un flux vendeur en fin de séance US |
| [2] | Paying Attention (Berkman et al.) | Actions US, 1996–2008 | Ouverture trop haute sur les titres qui ont attiré l'attention des particuliers, corrigée dans la 1re heure |
| [3] | One-factor NMD (Lu, Qin) | Actions US, 1996–2020 | Un facteur résume les écarts nuit−jour ; distorsion à l'ouverture, payée aux teneurs de marché |
| [4] | Return Extrapolation (Jones, Pyun, Wang) | Actions US + SPY, 1993–2021 | Les particuliers extrapolent les hausses de la veille dans les 15 premières minutes |
| [6] | A Tale of Night and Day (Hendershott et al.) | Actions US et 39 pays | Le bêta est payé la nuit et pénalisé le jour |
| [7] | Bad Days and Good Nights (Tompkins, Wiener) | Futures S&P, FTSE, DAX, CAC, Nikkei, 1982–2007 | Hors US : séance négative, nuit positive |
| [8] | Cycles of Declines and Reversals (Abdi) | Actions US, 1993–2016 | Depuis 2001 : nuit de baisse du marché → séance en baisse (titres volatils) → rebond la nuit suivante |
| [9] | Invisible Hand, Retrospective (Branch, Ma) | Actions US + SPY, 2011–2017 | Retournement nuit→séance pour les petites valeurs, disparu pour le SPY |
| [10] | Dark Side of the Day (Bahcivan et al.) | Actions US, 1993–2021 | Après un saut de nuit, ~20 % (baisse) ou 8–16 % (hausse) repris dans la séance |
| [11] | New Tug-of-War Pattern (Bahcivan) | Actions US, 1993–2021 | Les sauts de nuit affaiblissent la persistance mensuelle des rendements de nuit |
| [13] | Overnight Bitcoin Losses (Song) | SPY, QQQ, BTC, 2018–2026 | Baisse du BTC la nuit = gap baissier, mais pas de prévision de la séance |
| [14] | Lovers by Night (Donninger) | ES, NQ, 2010–2014 | Stratégie de nuit battue par le buy & hold sur l'ES après 1 tick de coût |
| [15] | Market Sentiment and an Overnight Anomaly (Vojtko, Hanicová) | SPY, 2018–2021 | Nuit du SPY meilleure si SPY > MM20, VIX < MM20 ou sentiment > MM20 (sans coûts) |
| [17] | Is Overnight Volatility Overlooked? (Zhang, Zhao) | SPY, QQQ, ES, NQ, 2009–2020 | >40 % de la variance journalière est de nuit ; la RV de nuit prédit la RV de séance |
| [18] | Realized Volatility and Overnight Returns (Ahoniemi, Lanne) | S&P 500 cash, 1994–2007 | Comment intégrer la nuit dans la RV ; l'ouverture du S&P 500 cash est fausse avant 2006 |
| [19] | Making Money While You Sleep? (Aretz, Bartram) | 48 000 actions, 35 pays, 1993–2012 | À l'international, le jour rapporte plus que la nuit ; les anomalies se font le jour |
| [20] | Risk and Return Around the Clock (Fattinger, Ziegler) | 13 futures (ES, pétrole, or, FX…), 2010–2013 | Rendement et risque arrivent ensemble ; pour l'ES et le pétrole, rien avant l'ouverture européenne |
| [21] | Who Moves the Price? (Wei) | Or et argent spot, 2024–2026 | La hausse de l'or s'est faite en session asiatique ; la session US a été négative |

---

## [1] The Overnight Drift — Boyarchenko, Larsen, Whelan

**Référence :** Federal Reserve Bank of New York Staff Report n° 917, février 2020, révisé août 2022. SSRN 3546173. (Publié ensuite dans la RFS.)

### Question
Le rendement des futures S&P 500 ne s'accumule pas de façon linéaire sur 24 h. Où se forme-t-il, et pourquoi ?

### Données
- **Contrat** : E-mini S&P 500 (ES), CME Globex. Toujours le contrat le plus traité (en pratique le front, sauf au roll).
- **Source** : tick-by-tick trades et quotes Refinitiv Datascope Select, complétés par la CME. Horodatage à la milliseconde en UT, converti en ET. Carnet sur 5 niveaux disponible depuis 2009.
- **Période** : 5 janvier 1998 – 31 décembre 2020 (23 ans).
- **Rendements** : calculés sur les **mid quotes** (meilleur bid/ask). Le jour de trading CME commence à 18:00 ET. Le rendement du week-end est inclus dans le premier rendement de la nuit du lundi (dernière observation vendredi 18:00, première dimanche 18:01).
- **Sens des trades** : un trade au ask = achat, au bid = vente.
- **Volume overnight** : environ 2 % du volume total jusqu'en 2002, environ 15 % en 2010 (stable jusqu'en 2018), environ 20 % en 2019-2020.
- Horaires CME : aujourd'hui du dimanche 18:00 au vendredi 17:00, maintenance 17:00–18:00 (depuis 2020). Entre 1994 et 2012, séance de 18:00 à 17:30 le lendemain avec pause 16:15–16:30. Pause 23:00–00:00 du mardi au vendredi d'octobre 1998 à septembre 2003.

### Résultat principal : le « overnight drift » (OD)
- Le rendement le plus fort de la journée est entre **2:00 et 3:00 ET**, à l'ouverture des marchés européens (Euronext, Eurex, Deutsche Börse, pré-ouverture du LSE, toutes à 2:00 ET). En moyenne **3,7 % annualisé**, soit **1,48 bp par jour**.
- Rendement close-to-close moyen : 5,9 % par an. Plus de la moitié vient de la séance de nuit : de 16:15 à 9:30, 3,6 % par an.
- Table I (bp par heure, mid quotes, 1998–2020) :
  - 24:00–1:00 : 0,46 (t = 2,77) ; 1:00–2:00 : 0,43 (t = 2,75) ; **2:00–3:00 : 1,48 (t = 7,13, p = 1,1×10⁻¹²)**, médiane 0,64 (les autres heures de nuit ont une médiane de 0 à cause du tick) ; 3:00–4:00 : 0,35 (t = 1,33) ; 6:00–7:00 : 0,61 (t = 2,46).
  - **9:00–10:00 (« opening hour ») : −1,24 (t = −2,60)**. 17:00–18:00 : −0,43 (t = −3,62). Les autres heures de séance sont plates.
- La hausse est continue sur 1:00–4:00 (barres de 5 minutes), pas due à quelques valeurs extrêmes dans l'heure.
- Sur les trades (VWAP, Table A.1), mêmes conclusions : 2:00–3:00 = 1,51 bp (t = 5,78) ; 9:00–10:00 = −1,33 bp (t = −2,96).

### Tests de robustesse statistique
- **Bootstrap par blocs** (10 000 tirages, longueur de bloc Patton-Politis-White) : la distribution des rendements horaires est bimodale. Le mode haut correspond à 2:00–3:00. La borne basse à 2,5 % de l'OD est au-dessus de la borne haute à 97,5 % de toutes les heures réunies. Sans 2:00–3:00, le second mode disparaît.
- **Tests multiples** : avec Bonferroni (seuil 0,05/24) et Benjamini-Yekutieli, seules 2:00–3:00 et 17:00–18:00 restent significatives. L'heure 17:00–18:00 n'est pas étudiée : peu d'importance économique, non significative sur les prix de trades. Avec BY à 1 %, seule l'OD reste.
- **Sous-périodes** : 1998–2010 et 2011–2020, l'OD est positive et significative à 5 % dans les deux. L'opening hour est fortement négative en 1998–2010 mais légèrement positive et non significative en 2011–2020.
- **Persistance** : OD positive **20 années sur 23**, significative à 10 % dans **17**. Plus forte année : **2020 (10,7 % annualisé)**. Légèrement négative en **2002, 2008 et 2019**.
- 1 $ investi uniquement de 2:00 à 3:00 devient **2,4 $** fin 2020 (contre 3,8 $ en close-to-close). 24:00–1:00 ou 1:00–2:00 seuls donnent environ la moitié. L'OD fait 50 % du rendement de la fenêtre 24:00–3:00.
- **Jours de la semaine** (Table A.5) : 2:00–3:00 positive et significative à 1 % **tous les jours**, avec des montants proches.
- **Mois** (Table A.6) : positive les 12 mois, significative dans 9 mois sur 12.
- **Opening hour (9:00–10:00)** : négative surtout en récession ou en stress (2000–2003, 2007–2008, 2020), plate sinon. Significative seulement les **jeudis (−2,10 bp, t = −2,02) et vendredis (−3,03 bp, t = −2,76)**. Pistes avancées : plus d'annonces macro US à 8:30 ces jours-là (avec retournement après l'annonce), peu de FOMC ces jours-là, et la plupart des jours d'annonces de résultats négatives sont des jeudis et vendredis. En septembre, l'opening hour vaut −3,45 %.

### Mécanisme : risque d'inventaire des teneurs de marché (Grossman-Miller 1988)
- Pas de teneur de marché désigné sur l'E-mini : ce sont tous ceux qui postent des limites des deux côtés.
- Histoire : pression vendeuse en fin de séance US → les teneurs de marché achètent, portent le stock la nuit et se font payer par un rendement attendu positif quand ils revendent aux nouveaux participants qui arrivent (Asie, puis Europe).
- Formule : E[R_ON | F₁] = déséquilibre d'ordres en dollars × variance du rendement × (capacité de prise de risque)⁻¹. Donc plus fort si (1) gros déséquilibre, (2) forte incertitude, (3) faible capacité de prise de risque.
- **Pourquoi pas plus tôt ?** Le volume chute brutalement à la clôture 16:15. En 2009–2020, le volume des heures asiatiques (18:00–2:00) est **50 à 100 fois** plus faible qu'en séance US. En 2020, le volume du seul intervalle 16:10–16:15 (≈ 85 000 contrats ≈ 13 Md$) dépasse tout le volume de 18:00 à 3:00 (≈ 13 500 contrats ≈ 2 Md$).
- **Temps en volume** : il faut environ **60 000 contrats** (le volume cumulé moyen atteint vers 3:00) pour absorber le déséquilibre de clôture. Dans ce temps-volume, la relation flux signé → rendement est presque linéaire mais **asymétrique**.
- Calibrage : aversion relative au risque implicite des teneurs de marché ≈ **8,5** (rendement 17 %/an après les ventes, déséquilibre 150 Md$, VIX² = 0,04, capital à risque des dealers 300 Md$). Les auteurs le jugent plausible par rapport à la littérature (7,6 à 91,2 sur les Treasuries, 88 sur les MBS).

### Mesure du déséquilibre de clôture
- **RSV** (relative signed volume) = (achats − ventes) / (achats + ventes), entre −1 et 1. **RSV_close** est mesuré sur la **dernière heure avant la pause, 15:15–16:15**.
- RSV close-to-close moyen = −2,4 % (les futures servent de couverture). RSV négatif en séance mais **positif entre 1:00 et 4:00** ; pendant l'OD, RSV moyen = 2,4 % (t = 6,7). SV (non normalisé) utilisé en robustesse sur 2007–2020 (volume stable sur cette période).

### Résultats conditionnels
- **Tri par RSV_close** (Figure 10) : les déséquilibres de clôture sont suivis de retournements la nuit. Le retournement est **beaucoup plus fort après une vente** (RSV négatif) qu'après une hausse. Avec RSV comme variable de tri, le profil ressemble à une fonction en escalier centrée sur zéro. Quand RSV_close ≈ 0, le rendement OD est faible et non significatif.
- **Double tri RSV × VIX de clôture (16:15)** (Table IV) : la distribution du VIX est semblable les jours de RSV positif et négatif (l'asymétrie ne vient donc pas de la volatilité). **Jours de RSV positif : pas de schéma clair.** **Jours de RSV négatif** : l'OD augmente avec la taille du déséquilibre (à VIX donné) et avec le VIX (à déséquilibre donné). Les rendements OD moyens vont d'environ 3 bp (VIX bas) à environ 13 bp (VIX haut). Seule exception : en VIX haut, l'effet du déséquilibre est grand mais plat. Écarts haut−bas significatifs dans 5 cas sur 6.
- **Régressions horaires** (Table V) : rendement horaire de la nuit sur RSV_close. Coefficients négatifs, **les plus forts entre 2:00 et 4:00** : −17,25 sur 2:00–3:00 (t = −8,10), −17,85 sur 3:00–4:00 (t = −6,02). Également 20:00–21:00 (−6,70, t = −4,19 : ouverture TSE/ASX). Un recul de 1 écart-type de RSV_close (6,55 %) donne +1,15 bp sur 2:00–3:00. Les déséquilibres mesurés plus tôt (14:15–15:15, 13:15–14:15) ont un effet décroissant, non significatif au-delà de 14:15.
- **Test de falsification** (Table VI) : le RSV de l'heure précédente ne prédit presque rien la nuit (une seule heure significative, 23:00–24:00, avec un signe positif). Avec 12 retards, seule la **diagonale « déséquilibre de clôture US »** est forte, exactement aux ouvertures de Tokyo et de l'Europe. L'autocorrélation négative ordinaire de l'ES ne dure que 30 minutes au plus (souvent seulement le premier retard de 5 min).
- **Asymétrie** (Table VII a) : la variable muette « RSV_close < 0 » n'est grande et significative **que sur 2:00–3:00** (+3,60 bp, t = 3,46).
- **Interaction avec le VIX** (Table VII b) : sur 2:00–3:00, RSV = 66,39, RSV × VIX = −5,33 (t = −4,23). Pour une baisse de 1 écart-type de RSV : **+2,6 bp avec VIX = 20, +6,1 bp avec VIX = 30 (90e centile), presque rien avec VIX = 12 (10e centile)**.

### Expérience naturelle : heure d'été (DST)
- Le Japon ne change pas d'heure. Vu des États-Unis, la TSE ouvre à **19:00 ET en hiver US et 20:00 ET en été US** (Table II : heures de 2018, TSE 20:00 ET en été). Pic de volume à l'ouverture de la TSE et à la reprise après sa pause déjeuner.
- Hiver US : l'effet RSV est sur 18:00–21:00 (−9,34 ; −13,46 ; −6,70). Été US : il se décale d'une heure (1,43 ; −1,43 ; −6,85).
- **Semaines où l'écart US–Europe vaut 4 h au lieu de 5 h** (environ 3 semaines par an, 240 jours contre 3 282) : la prévisibilité **disparaît sur 2:00–3:00** et se déplace vers **4:00–5:00** (dans le texte), qui est alors la première heure de séance à Londres et Francfort. Estimation peu précise (moins de 300 jours).
- Les régressions des Tables V à VII **excluent les jours où l'écart Londres–New York n'est pas de 5 h**.

### Stratégies de trading (Table IX, 2004–2020)
Période choisie car le spread de nuit a atteint 1 tick en 2004. Rendements et écarts-types annualisés en %. Sharpe avec le T-bill 4 semaines.

| Stratégie | Fenêtre (ET) | Moyenne sans coûts | Sharpe sans coûts | Moyenne avec coûts | Sharpe avec coûts |
|---|---|---|---|---|---|
| CTC (buy & hold) | 16:15 → 16:15 | 8,95 | 0,42 | 8,95 | 0,42 |
| CTO | 16:15 → 9:30 (texte) / 8:30 (légende) | 4,62 | 0,34 | 0,38 | −0,04 |
| OTC | 9:30 → 16:15 | 4,20 | 0,23 | −0,05 | −0,06 |
| OD | 2:00 → 3:00 | 3,75 | 1,10 | −0,59 | −0,54 |
| OD+ | 1:30 → 3:30 | 6,21 | 1,30 | 1,91 | 0,26 |
| **BtD (buy-the-dip)** | 1:30 → 3:30 **seulement si RSV_close < 0** | 6,07 | **1,78** | 4,04 | **1,10** |

- Coûts : achat au ask, vente au bid (quotes Refinitiv).
- BtD est en position environ **50 % des jours**. Il paie donc le spread deux fois moins souvent, et les jours choisis rapportent plus. Volatilité plus faible, skewness positive (le filtre enlève beaucoup de jours négatifs).
- Bêta proche de 0 (0,02 à 0,04) pour OD, OD+ et BtD.
- BtD a des **rendements positifs pendant les crises financières**, alors qu'elle n'est jamais vendeuse. 1 $ en 2004 → 1,9 $ fin 2020 après coûts (ne bat pas le buy & hold, mais Sharpe bien supérieur et pas de grosses pertes liées au cycle).
- Sans coûts, OD → 1,9 $ et OD+ → 2,8 $. Après coûts, **l'OD seule n'est pas rentable**.
- Interprétation : les teneurs de marché placent leurs limites pour que le trade contrarien qui paie le spread ne soit pas rentable.
- Les auteurs mentionnent que NightShares a lancé deux ETF en juin 2022 pour capter ce drift.

### Explications écartées (annexe A.4)
- **Annonces de résultats** publiées après 16:00 (I/B/E/S, Compustat) : l'OD est positive et significative dans les 5 groupes de surprise, y compris les jours sans aucune annonce (environ 46 % des jours). Les surprises négatives ne sont intégrées qu'à l'ouverture US, les positives dès la nuit. Les jours sans nouvelle ont le meilleur rendement close-to-close (4,57 %/an, t = 1,86).
- **Annonces macro** (US 8:30, zone euro 2:00, UK 4:30, Japon 19:50 ET) et **banques centrales** (FOMC 14:15, BCE 6:45 puis conférence 7:30, BoE 7:00, BoJ entre 22:00 et 1:00 ET) : la constante sur 2:00–3:00 reste 1,52 bp (t = 5,98) puis 1,40 bp (t = 6,52). Aucune variable muette d'annonce n'est significative sur cette heure. Annonces US de 8:30 : +3,22 bp (t = 2,29). BoE : positif, marginalement significatif sur 4:00–5:00.
- **Risque de volatilité** : volatilité en U dans chaque session (Asie, Europe, US). La volatilité US est plus de deux fois celle de l'Asie. Pas de lien visible entre la quantité de risque et le rendement.
- **Liquidité** : lambda de Kyle, Amihud, spread. Le spread est presque toujours à 1 tick (0,25 point), plus large seulement après 16:30. Profondeur : environ 100 contrats au premier niveau avant 2:00 (≈ 10 M$), environ 80 M$ sur 5 niveaux. Rien qui explique l'OD.
- **Résolution d'incertitude (VIX futures, VX)** : les VX baissent fortement à la clôture US (plus de −80 %/an), remontent en Asie (+50 %/an de 18:00 à 1:00) et baissent à l'ouverture européenne (environ −50 %/an de 2:00 à 4:00). Corrélation ES/VX à 1 minute ≈ −80 % (effet de levier). Mais **le déséquilibre de clôture de l'ES prédit les rendements de nuit de l'ES et des VX**, alors que le déséquilibre des VX ne prédit que les VX. Les auteurs rejettent donc l'explication par résolution d'incertitude.

### Pourquoi l'asymétrie ? (hypothèses des auteurs, non testées à fond)
1. Pas d'obligation de cotation sur l'E-mini : lors des fortes ventes, des teneurs de marché sortent du marché.
2. Contraintes de **VaR** : la volatilité monte quand le marché baisse (effet de levier), ce qui resserre la contrainte et augmente l'aversion effective. Une baisse de volatilité ne la relâche pas symétriquement.
3. Coûts de financement (Brunnermeier-Pedersen) : la CME relève les marges initiales pendant les baisses prolongées.

### À retenir pour nous (strictement d'après le papier)
- Fenêtre : **2:00–3:00 ET** (OD) ou **1:30–3:30 ET** (OD+). En heure de Paris, c'est l'ouverture des marchés européens (8:00–9:00 Paris quand l'écart Paris–New York est de 6 h). Quand l'écart US–Europe n'est que de 4 h (semaines de décalage DST), l'effet se déplace d'après le papier vers 4:00–5:00 ET.
- Signal conditionnel : **flux signé de la dernière heure de séance (15:15–16:15 ET) négatif** ; effet renforcé quand le **VIX de clôture est élevé**. Le flux signé exige des données de trades et de quotes (classement au bid/ask), pas seulement de l'OHLCV.
- Après coûts, seule la version conditionnelle (BtD) reste rentable dans le papier.
- Les données s'arrêtent fin 2020.

---

## [2] Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open — Berkman, Koch, Tuttle, Zhang

**Référence :** version de mars 2011, SSRN 1625495 (publié ensuite dans le JFQA, 2012).

### Question
Pourquoi les actions US montent-elles la nuit puis baissent-elles en séance ? Les auteurs testent une explication par l'**attention des particuliers** (prolongement de Barber et Odean 2008) : un événement qui attire l'attention le jour t pousse les particuliers à acheter **à l'ouverture de t+1**, première occasion depuis la clôture. Ils n'achètent que ce qui attire leur attention ; pour vendre, ils se limitent à ce qu'ils possèdent (pas de vente à découvert).

### Hypothèses testées
1. Un jour de forte attention est suivi d'achats nets des particuliers près de l'ouverture du lendemain.
2. Cette pression rend le prix d'ouverture élevé par rapport au reste de la séance, surtout pour les titres difficiles à évaluer et coûteux à arbitrer.
3. L'effet est plus fort quand le sentiment global des particuliers est élevé.

### Données
- **Échantillon principal** : les 3 000 plus grandes actions US (capitalisation au 1er juillet de chaque année), **1996–2008** (3 268 jours). En pratique 2 383 à 2 604 titres par jour après filtres.
- **Échantillon réduit** : actions Nasdaq **1997–2001**, données propriétaires Nasdaq-OMX avec l'identité des participants. Chaque côté de chaque trade est classé particulier ou institution (méthode Griffin et al. 2003).
- **Prix** : quotes TAQ. **Ouverture = milieu du premier bid/ask valide après 9:30** (taille non nulle des deux côtés ; sur le Nasdaq, les market makers mettent souvent plusieurs minutes à coter). **Clôture = milieu du dernier bid/ask valide avant 16:00.** Ajustés des dividendes et splits (CRSP). Résultats robustes avec le mid exactement à 9:30, et avec les prix de trades.
- Rendements en log : cto = nuit (close-to-open), otc = séance (open-to-close), ctc = cto + otc, oto = open-to-open.
- **Filtres** : quote non normale ou ask > 1,5 × bid exclus ; jour exclu si spread négatif, spread d'ouverture ou de clôture > 5 $ ou > 30 % du mid, demi-spread effectif > 2,50 $ ou > 15 %, ou ouverture à plus de 25 % de la clôture précédente et de la suivante ; titre exclu s'il manque plus de 25 % des jours.
- Les auteurs notent que l'after-hours et la pré-ouverture sur ECN existent, mais sont dominés par les professionnels (coûts élevés pour les particuliers).

### Variables
- **Attention** (veille, ajustée de la taille) : (i) **VOL_{t−1} = carré du rendement close-to-close de la veille** ; (ii) **Retail_NetBuy_{t−1}** = achats nets des particuliers sur toute la veille, en % du volume (Nasdaq seulement). Robuste avec le turnover de la veille.
- **Achats nets des particuliers près de l'ouverture** (Nasdaq) : NetBuy_Open = proportion de titres dont le premier trade est un achat de particulier, moins 0,5 ; NetBuy_15Min = achats nets / volume des particuliers sur les 15 premières minutes ; NetBuy_DIFF = (achats nets de la 1re heure − achats nets des 5,5 h suivantes / 5,5) / actions en circulation.
- **Contraintes de vente à découvert** : détention institutionnelle INST (13F, CDA Spectrum ; 0 si absente) et short interest relatif RSI.
- **Coûts** : spread en % à l'ouverture (moyenne **1,06 %**), à la clôture (**0,62 %**), demi-spread effectif (**0,17 %**).
- Contrôle de taille : capitalisation moyenne des 20 jours précédents.

### Résultats descriptifs (Table 1)
- Moyenne sur tous les titres et jours : **nuit +9,8 bp/jour, séance −6,6 bp/jour**. Long nuit / short séance (DIFF) = +16,5 bp/jour avant coûts. **Après déduction du spread moyen d'ouverture et de clôture : −70,8 bp/jour.**
- Rendement 24 h ≈ 3 bp/jour (≈ 8 %/an), non significatif.
- **Profil intraday** (Figure 1, mid à 5 min sur les 30 premières et dernières minutes, 30 min ailleurs) : le prix d'ouverture est en moyenne **8 bp au-dessus de la clôture**. Le prix baisse pendant les **60 premières minutes**, puis reste plat, puis remonte un peu dans les dernières minutes. Le schéma vient donc d'une **ouverture trop haute**, pas d'une clôture trop basse.
- Corrélations : les deux mesures d'attention sont corrélées positivement au rendement de nuit et négativement à la séance. INST faible ou RSI élevé → nuit plus forte et séance plus faible. Spread élevé → idem. Petites capitalisations → nuit plus forte.
- Le risque de liquidité overnight (Acharya-Pedersen, Pastor-Stambaugh) n'explique rien (test non publié).

### Résultats principaux
- **Achats des particuliers** (Table 2) : les trois mesures d'achat à l'ouverture sont significativement plus élevées pour les titres de forte attention (différence haut − bas significative à 1 %). Pour ces titres, l'achat net est plus intense dans la 1re heure que dans le reste de la séance.
- **Tri par attention, contrôle de taille** (Table 2) :
  - 3 000 titres, attention = VOL_{t−1} : forte attention **+13 bp la nuit, −13 bp en séance** ; faible attention +3 / −3 bp.
  - Nasdaq 1997–2001, attention = achats nets de la veille : forte attention **+26 / −27 bp** ; faible attention +4 / −12 bp.
  - **Le rendement close-to-close n'est jamais significativement différent de zéro.** C'est une surévaluation temporaire à l'ouverture, corrigée dans la séance.
- **Double tri attention × détention institutionnelle** (Table 3, environ 261 titres par case) :
  - Forte attention et faible INST : **+17 bp la nuit, −17 bp en séance** (3 000 titres) ; **+34 / −42 bp** (Nasdaq, environ 90 titres par case).
  - Faible attention et forte INST : +2 / −3 bp (3 000 titres) ; +2 / −9 bp (Nasdaq), non significatif en séance.
  - Close-to-close jamais significatif.
- **Titres difficiles à évaluer et coûteux à arbitrer** (Table 4). Filtres successifs chaque jour : (1) 50 % des titres avec la plus forte volatilité des 20 derniers jours ; (2) parmi eux, 50 % avec le plus fort demi-spread effectif ; (3) parmi eux, 20 % avec le plus fort short interest relatif.
  - Forte attention et faible INST : **+43 bp la nuit, −45 bp en séance** (3 000 titres, environ 13 titres par case) ; **+61 / −70 bp** (Nasdaq, environ 5 titres par case).
  - Les auteurs notent qu'un retournement de 45 bp/jour cumule à 112,5 %/an.

### Sentiment (section 5)
- Deux mesures mensuelles : l'**indice de sentiment Baker-Wurgler** (disponible jusqu'à fin 2007) et un **indice de sentiment des particuliers** = achats nets des particuliers dans la 1re heure, en % des actions en circulation, moyenne sur tous les titres et jours du mois (Nasdaq 1997–2001).
- Portefeuille couvert : long forte attention / faible INST, short faible attention / forte INST.
- Corrélation avec Baker-Wurgler : **+0,30 avec le rendement de nuit, −0,33 avec la séance**. Avec l'indice des particuliers : **+0,47 et −0,51**. Les deux indices sont corrélés à 0,77.
- Rendements de nuit et retournements de séance **plus de deux fois plus grands** les mois de sentiment élevé.
- Le rendement de nuit du portefeuille couvert devient très grand juste avant le krach technologique de mars 2000 et reste positif en 2001. L'essentiel de la correction de 2000 sur ces titres a eu lieu **en séance**.
- Le coût implicite d'acheter à l'ouverture est du même ordre que le demi-spread effectif sur la majeure partie de la période, et **peut dépasser deux fois le demi-spread** en période de sentiment élevé.

### Robustesse (Table 5)
- Robuste aux rendements ajustés du marché, aux médianes, aux prix de trades (1996–2004), à l'exclusion des titres sous 5 $.
- Présent sur Nasdaq et NYSE, petites et grandes capitalisations, croissance et valeur, gagnants et perdants du momentum. **Plus fort** pour les petites capitalisations, le Nasdaq, les titres de croissance et les **perdants du momentum** (+32 / −31 bp).
- **Plus fort le lundi** (cas de base 3 000 titres : +20 bp nuit, **−35 bp séance**), mais présent les autres jours (+16 / −12 bp).
- Présent dans toutes les sous-périodes mais **en baisse dans le temps** : 1996–2000 +25 / −24 bp ; 2001–2004 +16 / −22 bp ; 2005–2008 +13 / −16 bp. Les auteurs évoquent la décimalisation (2001) et l'essor du trading algorithmique.
- Fama-MacBeth (variables explicatives en rangs déciles, variable dépendante winsorisée à 1 %) : attention → nuit + et séance − ; détention institutionnelle → nuit − et séance + ; les petites capitalisations ont un retournement de séance plus fort.

### À retenir pour nous (strictement d'après le papier)
- Papier **en coupe transversale sur actions individuelles**, pas sur indices ni futures.
- Le signal (forte variation de la veille, au carré) prédit **une ouverture trop haute qui se corrige surtout dans la première heure**.
- Une stratégie long nuit / short séance **perd environ 71 bp/jour** une fois payé le spread d'ouverture et de clôture. Les auteurs présentent surtout le résultat comme un **coût caché** pour ceux qui achètent à l'ouverture.
- Données 1996–2008, effet en baisse sur la fin.

---

## [3] A One-factor Model for Expected Night-minus-day Stock Returns — Zhongjin (Gene) Lu, Zhongling (Danny) Qin

**Référence :** 1re version avril 2021, version de septembre 2021. SSRN 3854046. University of Georgia et Auburn University.

### Question
Plus d'une dizaine de caractéristiques prédisent, en coupe transversale, le rendement **nuit moins jour (NMD)** des actions, et les modèles factoriels classiques ne l'expliquent pas. Peut-on résumer ces prévisibilités par **un seul facteur**, et quelle force économique est derrière ?

### Données et mesures
- Actions ordinaires US (NYSE, AMEX, NASDAQ), CRSP. Prix d'ouverture CRSP disponible depuis le 15 juin 1992. TAQ à partir du 4 janvier 1993. Rendements des portefeuilles mesurés du **1er février 1996 au 31 décembre 2020**.
- Filtres : jour exclu si rendement intraday > 1000 % ou ouverture manquante ; titre inclus si volume quotidien médian du mois > 1 000 actions, au plus une ouverture manquante dans le mois, **prix > 5 $ et capitalisation au-dessus du quintile inférieur NYSE**. Portefeuilles pondérés par la capitalisation.
- Rendement de séance r_D = clôture / ouverture − 1. Rendement de nuit r_N = (1 + r_close-to-close) / (1 + r_D) − 1. **NMD = r_N − r_D.** Ouverture principale = prix d'ouverture CRSP. Robuste avec le premier mid (Berkman et al.), le mid de 9:45 (Bogousslavsky) ou le VWAP 9:30–10:00 (Lou-Polk-Skouras), et aux titres au-dessus de la médiane NYSE.
- Le taux sans risque est supposé gagné la nuit. Tous les rendements NMD sont **ajustés du marché** (moins bêta CAPM × rendement du marché sur la même période).

### Actifs testés
- **17 portefeuilles long-short de Lou, Polk et Skouras (2019)** (déciles, long décile haut / short décile bas, rebalancement mensuel). Caractéristiques : rendement intraday et overnight passés (simples et moyennes exponentielles), BETA, IVOL, BM, ISSUE, ACCRUALS, INV, ROE, ME, SUE, MOM, STR, TURNOVER, INDMOM.
- La plupart de ces portefeuilles ont des rendements de nuit et de jour de signe opposé et de taille proche. NMD moyens non ajustés de **−26,0 % à +69,6 % par an**. 13 sur 17 significatifs à 1 % après ajustement CAPM. Les modèles FF5, HXZ4, SY4, DHS3 n'expliquent pas ces écarts.
- Test hors échantillon : + **80 portefeuilles** tirés des caractéristiques de Green, Hand et Zhang (2017) non étudiées par LPS. 58 sur 80 ont un NMD significatif à 5 %.

### Construction du facteur (deux versions)
1. **NMD SDF** : estimateur bayésien de Kozak, Nagel et Santosh (2020), proche d'une régression ridge, b = (Σ + γI)⁻¹ μ. γ choisi par validation croisée à 3 blocs. Poids w_i = b_i / Σ|b_i| (1 $ long, 1 $ short). **Utilise toute la période** (information future).
2. **NMD CS** : score composite. Régression Fama-MacBeth mensuelle du NMD sur les 17 caractéristiques en rangs normalisés, coefficients moyennés sur 12 mois glissants, puis long-short trié sur ce score. **N'utilise que l'information disponible au moment de la construction.**
- Corrélation journalière entre les deux : 0,81.

### Résultats de pricing
| Facteur | Moyenne (%/an) | Sharpe annualisé | Skewness | Kurtosis | AR(1) |
|---|---|---|---|---|---|
| NMD SDF | 44,89 | 4,99 | 0,20 | 31,54 | 0,07 |
| NMD CS | 94,73 | 4,36 | −0,17 | 20,36 | 0,05 |
| LIQ (Nagel 2012) | 59,26 | 5,83 | −0,92 | 59,78 | 0,01 |
| FF REV (Ken French) | 14,02 | 0,92 | 1,58 | 25,12 | 0,16 |

- Sharpe des 17 portefeuilles LPS pris un par un : de 0,1 à 3,4.
- **17 portefeuilles LPS** : R² en coupe = **94 % (SDF), 84 % (CS)**, contre 0 % (CAPM, par construction) et 6 à 11 % pour les autres modèles. Alpha absolu moyen : 7,3 % (SDF) et 12,4 % (CS) contre environ 30 % pour les modèles classiques ; |t| moyen 1,26 et 2,06 contre plus de 6.
- **97 portefeuilles** (hors échantillon) : R² = **79 % (SDF), 78 % (CS)**, contre 14 à 19 % pour les modèles classiques.

### Structure factorielle
- ACP des NMD des 17 portefeuilles : PC1 = 26 %, PC2 = 22 %, PC3 = 13 %, PC4 = 7 %, PC5 = 6 % de la variance (61 % pour les 3 premières). Même structure sur les rendements de nuit seuls et de jour seuls.
- NMD SDF : PC1 explique 47 % de sa variance, PC1 + PC2 65 %. NMD CS : PC1 58 %, PC1 + PC2 64 %. Un modèle PC1 + PC2 donne un R² en coupe de 76 %.
- Interprétation des auteurs (Kozak-Nagel-Santosh 2018) : pas de quasi-arbitrage ; pour toucher la prime il faut porter le risque commun. Ce n'est **pas compatible avec un simple data mining**.

### D'où vient la demande : l'ouverture, pas la clôture (Table 6)
- Le score CS prédit le NMD **jusqu'à 60 mois** après la formation, mais ne prédit pas le rendement close-to-close.
- Test : on remplace l'ouverture par le mid à 9:30, 10:00, 10:30, 11:00, ou la clôture par le mid à 14:30, 15:00, 15:30, 16:00 (NBBO TAQ ; jours d'ouverture tardive ou de clôture anticipée exclus).
  - **Ouverture décalée** : NMD SDF passe de **48,7 % (9:30) à 16,6 % (10:00), 10,4 % (10:30), 7,5 % (11:00)** par an. NMD CS : 106,6 % → 36,5 % → 20,9 % → 17,8 %.
  - **Clôture avancée** : presque aucun effet (NMD SDF 46,0 % à 50,2 % ; NMD CS 106,1 % à 113,7 %).
  - Conclusion : la mauvaise valorisation est **maximale à l'ouverture** et se corrige surtout dans la **première demi-heure**.

### Qui crée la demande : les particuliers (Table 6, panel B, novembre 2007 – décembre 2020)
- Flux des particuliers identifiés par l'algorithme de **Boehmer, Jones, Zhang et Zhang (2020)** (trades hors midpoint avec amélioration de prix inférieure au cent, code TAQ « D », après Reg NMS). Flux total par Lee-Ready. Non-particuliers = total − particuliers. Déséquilibres en dollars rapportés à la capitalisation de la veille, annualisés.
- Sur **9:30–10:00** : NMD SDF, OI total = 1,41 %, particuliers (ROI) = 1,12 % (t = 7,12), non-particuliers = 0,29 % (non significatif). NMD CS : OI = 2,99 %, ROI = 3,01 %, non-particuliers ≈ 0. La demande d'achat à l'ouverture sur la jambe longue vient **presque entièrement des particuliers**.
- Le ROI reste positif mais décroît au fil de la journée. Pas de flux agressif opposé net dans les demi-heures suivantes : les auteurs pensent que l'effet est absorbé par des **ordres non marchés (limites)** en sens inverse.

### Qui arbitre : les teneurs de marché (hypothèse de fourniture de liquidité)
- La stratégie NMD demande deux allers-retours par jour (long la nuit, short la journée). **Avec des ordres au marché, les coûts (estimations Novy-Marx et Velikov 2016) dépassent largement le rendement.** Selon l'annexe en ligne, elle reste très rentable si l'on exécute le matin au VWAP de la 1re demi-heure et l'après-midi au prix de clôture, ce qui n'est réaliste que pour les teneurs de marché les plus rapides. Exemple cité : Citadel Securities exécute environ 47 % du volume des particuliers US.
- **LIQ** = rendement de la stratégie de retournement court terme de Nagel (2012) (Lehmann 1990, tri sur les rendements des 1 à 5 jours précédents), à partir de janvier 1998.
- Régressions mensuelles (1998–2020, Table 7) : NMD SDF = 0,65 × LIQ (t = 5,49), R² = 36 % ; NMD CS = 1,30 × LIQ (t = 5,72), R² = 28 %. **Alphas réduits de plus de 80 % et non significatifs** (t = 1,1 et 1,5).
- Placebo : le retournement à 21 jours de Ken French (FF REV) n'explique rien (R² ≈ 0).
- Le facteur NMD et LIQ **baissent tous deux dans le temps** (concurrence entre teneurs de marché selon les auteurs) et **montent ensemble pendant les crises** : krach dot-com 2000, crise 2009, krach Covid 2020.

### Sentiment et liquidité ensemble (Table 8)
- Variables standardisées, avec une variable muette avant la décimalisation (avant avril 2001).
- 1998–2020 : un écart-type de LIQ → +16,3 points/an (SDF) et +35,0 (CS) ; un écart-type de déséquilibre d'ouverture OI → +12,8 et +24,4. Les deux significatifs.
- Après octobre 2007 : LIQ → +16,3 et +42,0 ; ROI → +4,9 et +12,1. **La rémunération exigée par les fournisseurs de liquidité pèse plus que la demande des particuliers.**
- Avec LIQ normalisé par sa volatilité prévue (GARCH(1,1)), le chargement reste positif et significatif : la **volonté** des teneurs de marché de fournir de la liquidité compte aussi.

### À retenir pour nous (strictement d'après le papier)
- Papier **en coupe transversale d'actions** (portefeuilles long-short), pas sur indices.
- La distorsion porte sur le **prix d'ouverture** et disparaît en grande partie dès **10:00**.
- L'ampleur du phénomène suit la **prime de liquidité** (plus forte en crise, en baisse sur le long terme).
- **Non exploitable avec des ordres au marché** selon les auteurs.

---

## [4] Return Extrapolation and Day/Night Effects — Christopher S. Jones, Sungjune Pyun, Tong Wang

**Référence :** version d'avril 2024, SSRN 4181093. USC Marshall, Yonsei, University of Oklahoma.

### Thèse
L'écart entre rendements de nuit et de jour vient de l'**extrapolation des rendements passés** par des investisseurs peu sophistiqués. Trois faits combinés : (1) les investisseurs extrapolent ; (2) les non-professionnels tradent surtout le matin ; (3) ils vendent rarement à découvert (13 % des particuliers dans l'échantillon de Gamble et Xu 2017, 24 % parmi ceux qui ont un compte sur marge). Après un rendement positif, ils achètent à l'ouverture et poussent le prix d'ouverture ; après un rendement négatif, ils réagissent peu. D'où une ouverture trop haute en moyenne (« mini-bulles » quotidiennes).

### Données
- Actions ordinaires US (NYSE, Nasdaq, AMEX), **1993–2021**. TAQ pour 1993–2014, **Polygon** pour 2015–2021. CRSP pour les ajustements (dividendes, splits).
- Exclusions : capitalisation sous le 20e centile NYSE et prix < 5 $ à la fin du mois précédent.
- **Définition des périodes** (sur les mid NBBO) : **séance = 9:45 → 15:59**, **nuit = 15:59 (veille) → 9:45**. Les minutes 9:30–9:45 sont évitées (quotes bruitées), de même que la dernière minute (spreads qui s'élargissent). Jours de clôture à 13:00 : fin à 12:59.
- **Déséquilibre d'ordres** : Lee-Ready (trade comparé au mid de la seconde précédente, test du tick en cas d'égalité), (achats − ventes) / actions en circulation, ramené à l'heure. Exclus : enchères d'ouverture et de clôture, trades corrigés, codes anormaux, renversements de plus de 25 %.
- Pour les portefeuilles : moyennes pondérées par la capitalisation, divisées par la moyenne mobile sur 200 jours du turnover agrégé.
- 13 caractéristiques de Lou-Polk-Skouras : bêta (12 mois, Dimson à 5 retards), taille, BM, rentabilité brute, investissement, accruals, momentum (t−13 à t−2), momentum sectoriel, rendement du mois précédent, surprise de résultats, émission nette, volatilité idiosyncratique, turnover.

### Résultats au niveau des actions
- **Déséquilibres d'ordres** (Fama-MacBeth, Table 1), régressés sur le rendement de séance de la veille (9:45–15:59) avec contrôle des déséquilibres de la veille :
  - **9:30–9:45 : coefficient fortement positif (t = 26,9)**. 9:45–10:30 : positif mais plus faible. **10:30–16:00 : négatif (t = −9,7)**. Par demi-heure : positif dans les 30 premières minutes, légèrement négatif dès la 2e heure.
  - Le rendement de nuit de la veille a le même effet, plus faible. Le rendement de la semaine précédente (t−6 à t−2) pousse les achats tout au long de la journée (moins d'urgence selon les auteurs).
  - **Asymétrie** : le terme max(rendement de la veille, 0) est très significatif. Dans les 15 premières minutes, il réduit de plus de moitié le coefficient linéaire : on réagit beaucoup moins aux baisses.
- **Rendements** (Table 2) :
  - Rendement de nuit sur rendement de séance 9:45–15:59 de la veille : **aucune relation** (−0,10, t = −0,87). Les auteurs l'expliquent par un retournement mécanique de court terme qui compense l'extrapolation.
  - **En arrêtant la fenêtre de formation à 15:00 (9:45–15:00)**, forte continuation (0,95, t = 8,12). Le choix de 15:00 est arbitraire et non optimisé. Il écarte aussi les explications par couverture d'options ou rééquilibrage (pas de raison d'attendre le lendemain matin).
  - Avec le terme asymétrique : les rendements positifs de la veille continuent la nuit, les négatifs se retournent. Résiste à 12 contrôles (taille, BM, momentum, etc.).
  - Le rendement de **jour** est aussi relié positivement au rendement de jour de la veille (actions individuelles), mais les auteurs ne le comptent ni pour ni contre leur hypothèse.
- **Tri en déciles** (Table 3) sur le rendement 9:45–15:00 de la veille :
  - Nuit, équipondéré : décile haut − bas = **+7 bp par nuit** (t = 8,91). Seuls les 2 déciles du haut se détachent (environ 12 bp pour le décile haut).
  - Nuit, pondéré par la capitalisation : **+9 bp** (t = 6,20). L'effet n'est **pas** cantonné aux petites capitalisations.
  - Avec la fenêtre 9:45–15:59, aucun écart la nuit.
  - Jour, pondéré par la capitalisation : retournement avec 9:45–15:59 (−4 bp, t = −2,91), rien avec 9:45–15:00. La continuation de jour ne concerne que les petites capitalisations.
- **Hétérogénéité** (Table 4) : l'extrapolation du matin est plus forte pour les titres **surévalués** (mesure de Stambaugh, Yu et Yuan 2015), ceux à fort **volume de recherche Google** (depuis 2004) et à forte **part de volume des particuliers** (Boehmer et al. 2021, depuis 2010). Ces mêmes facteurs rendent la relation négative plus tard dans la journée.

### Portefeuilles
- 130 portefeuilles déciles (13 caractéristiques), rebalancés chaque mois (Table 5) : mêmes résultats qu'au niveau des actions. Rendement de nuit relié positivement au rendement de jour de la veille (1,69, t = 11,71).
- Modèle simple : si le flux d'ordres est proportionnel à max(signal, 0), le déséquilibre moyen augmente avec la moyenne **et la dispersion** des rendements. Effectivement, la **dispersion transversale de la veille** prédit des déséquilibres positifs le matin, un rendement de nuit positif et un rendement de jour négatif.
- **Long-short** (Table 6), régresseurs = rendement **SPY 9:45–15:00** de la veille et dispersion transversale :
  - Le rendement de marché de la veille prédit le déséquilibre net du matin pour 8 portefeuilles sur 13 (6 négatifs : extrapolation plus forte sur la jambe surévaluée). Exceptions : momentum sectoriel et taille (−1 ×).
  - L'écart nuit − jour (« tug of war ») est prédit par le rendement de marché de la veille dans 8 cas sur 13, tous négatifs ; par la dispersion dans 6 cas sur 13.
  - Corrélation entre effet sur le flux d'ordres et effet sur les rendements : 0,889 (0,933 sans contrôles).
  - **Corrélation entre la sensibilité à l'extrapolation et l'écart moyen nuit − jour des portefeuilles : environ 0,96 (rendement de marché) et 0,90 (dispersion)**. R² en coupe = 0,934. Le tug of war de Lou-Polk-Skouras serait donc **surtout un effet d'extrapolation**.
  - L'extrapolation du seul marché (via le bêta des portefeuilles) n'explique qu'une petite part (Figure 6).

### Le bêta la nuit (relecture de Hendershott et al. 2020)
- Pentes Fama-MacBeth (ajustement de Shanken), portefeuilles triés sur le bêta (Table 7) :
  - Toutes les nuits : rendement de nuit = −0,0218 + **0,0650 × bêta de nuit** (t = 7,61).
  - **Après un rendement de marché positif la veille (SPY 9:45–15:00 > 0) : pente 0,1337 (t = 8,84)**.
  - **Après un rendement négatif : pente −0,0155 (t = −1,25), non significative.**
  - En séance, la pente est toujours négative (−0,1109 sur tous les jours ; −0,1588 après une hausse ; −0,0651 après une baisse).
- Déséquilibres 9:30–9:45 : les plus élevés pour les titres à fort bêta, **environ 50 % plus élevés après une hausse du marché qu'après une baisse** (t = −5,9).
- Conclusion des auteurs : le bêta « payé la nuit » ne vient pas de l'aversion au risque de nuit (sinon elle serait plus forte après une baisse), mais de l'**extrapolation après les hausses**.

### Le marché dans son ensemble (Table 8, SPY)
- Déséquilibre d'ordres agrégé 9:30–9:45 relié positivement au rendement SPY 9:45–15:00 de la veille (2,10, t = 6,44). Rien sur 9:45–10:30 et 10:30–16:00. **Mais l'effet disparaît quand on contrôle les déséquilibres passés** : les auteurs demandent de le lire avec prudence.
- **Rendements SPY** : rendement de nuit = 0,0003 + **0,0387 × rendement SPY 9:45–15:00 de la veille** (t = 2,04) ; rendement de jour : **−0,0549** (t = −2,00) ; nuit − jour : **0,0936** (t = 2,90). **Aucun effet de la dispersion** au niveau du marché.
- Les auteurs en concluent que l'extrapolation joue un rôle dans l'écart nuit/jour du marché, mais que l'asymétrie seule ne suffit pas à expliquer le résultat de Kelly et Clark (2011).
- Ils notent aussi que les moyennes mobiles longues des rendements de séance (Lou et al. 2022) prédisent le rendement de nuit du marché, mais qu'elles sont presque indépendantes du rendement d'un jour étudié ici.

### Qui extrapole ? (section 5)
- Particuliers identifiés par Boehmer et al. (2021) ; institutions approchées par les **intermarket sweep orders (ISO)**.
- Les deux extrapolent, surtout dans la 1re demi-heure. Les ISO extrapolent aussi dans les 30 dernières minutes.
- **L'asymétrie (réaction aux hausses seulement) à l'ouverture vient entièrement des particuliers.** Les institutions extrapolent de façon symétrique le matin.
- En fin de séance, les particuliers sont vendeurs nets après une hausse comme après une baisse. Les institutions achètent à la clôture après une hausse (asymétrie de fin de journée), ce qui pousse la clôture et compense en partie.

### Extrapolation des prix ou réaction aux nouvelles ?
- Échantillon sans annonce (résultats, révision ou changement de recommandation d'analyste dans les 24 h à partir de 16:00 ; environ 1 531 titres par jour) contre échantillon avec annonce (environ 282 titres par jour).
- Sans annonce, résultats très proches de l'échantillon complet. Avec annonce, la relation linéaire nuit/jour de la veille est environ deux fois plus forte, mais l'asymétrie est plus faible. Conclusion : c'est surtout une **extrapolation du prix**, pas une mauvaise réaction aux nouvelles.

### À retenir pour nous (strictement d'après le papier)
- Signal testé au niveau du marché : **rendement SPY de 9:45 à 15:00 (heure de New York) de la veille**. Positif → nuit suivante plus forte et séance suivante plus faible (effets significatifs mais t ≈ 2).
- L'extrapolation agit dans les **15 premières minutes** de séance (9:30–9:45).
- La fenêtre de formation qui finit à 15:59 masque l'effet (retournement de court terme) ; finir à 15:00 le fait apparaître.
- L'asymétrie (hausses extrapolées, baisses peu) est un trait des **particuliers**.

---

## [6] Asset Pricing: A Tale of Night and Day — Terrence Hendershott, Dmitry Livdan, Dominik Rösch

**Référence :** préprint Elsevier du 1er décembre 2019, SSRN 3117663 (publié ensuite dans le Journal of Financial Economics, 2020). UC Berkeley et SUNY Buffalo.

### Résultat central
Le CAPM échoue sur 24 h parce que la relation bêta–rendement **change de signe** selon que le marché est ouvert ou fermé : **positive la nuit** (close-to-open), **négative le jour** (open-to-close). Les deux se compensent et la droite de marché (SML) sur 24 h est plate ou légèrement décroissante.

### Données et méthode
- **US** : CRSP, actions ordinaires (codes 10 et 11), **1992–2016** (l'ouverture CRSP n'existe qu'à partir de 1992). 16 jours-titres avec un rendement de jour > 1 000 % exclus.
- **International** : Datastream, **39 pays, 1990–2014**, rendements en monnaie locale. Filtres d'Amihud et al. (2015) : volume ≥ 100 USD, indice de prix > 0,01, |rendement| < 200 %, règle sur les rendements > 100 %, ouverture positive, |jour| et |nuit| < 200 %. Régions : **EU** (France, Allemagne, Grèce, Israël, Italie, Pays-Bas, Norvège, Pologne, Afrique du Sud, Espagne, Suède, Suisse, Royaume-Uni) et **Asie** (Australie, Chine, Hong Kong, Inde, Indonésie, Japon, Corée, Nouvelle-Zélande, Philippines, Singapour, Thaïlande).
- Rendement de nuit = (1 + close-to-close) / (1 + open-to-close) − 1 (méthode Lou-Polk-Skouras). Nuit ≈ 17,5 h, jour ≈ 6,5 h (plus long après week-ends et jours fériés).
- **Bêta pré-classement** : régression des rendements **de nuit** du titre sur le rendement de nuit du marché (pondéré par la capitalisation, au moins 10 titres par pays), fenêtre glissante de 12 mois, au moins 30 observations. Tri mensuel en 10 déciles de bêta. Bêtas post-classement sur tout l'échantillon (figures) ou glissants 12 mois (tables).
- Fama-MacBeth séparés nuit et jour, plus régression en panel avec effets fixes jour et variable muette « jour » × bêta.

### Résultats sur les portefeuilles triés par bêta (US)
- Figure 1 (équipondéré) : **+1 de bêta = +14 bp la nuit, −15 bp le jour**. R² = 96,2 % (nuit) et 92,2 % (jour). Le portefeuille de bêta le plus élevé a le **pire rendement de jour (−8 bp)** et le **meilleur rendement de nuit (+20 bp)**. Le test de Patton-Timmermann confirme une relation monotone croissante la nuit et décroissante le jour.
- Prime de marché implicite du CAPM sur la période : 7,5 bp/jour (T-bill 3 mois).
- Table 1 :
  - Pondéré par la capitalisation : pente de nuit **+6,4 bp** (t = 7,77), constante −0,8 bp (non significative) ; pente de jour **−7,7 bp** (t = −5,52), constante +15,2 bp. Écart nuit − jour = 14,1 bp. Panel : jour × bêta = −15,9 bp (t = −7,00).
  - Équipondéré : nuit **+12,1 bp** (t = 13,39), constante −5,2 bp (significative) ; jour **−13,5 bp** (t = −8,68), constante +16,9 bp. Écart = 25,6 bp. Panel : −26,7 bp (t = −15,65).
- Résultats identiques avec des bêtas estimés sur les rendements close-to-close (Figure 3 : nuit +14 bp, jour −18 bp, R² 96,8 % et 96,2 %), et avec des contrôles de taille, BM et performance passée.

### International
- Figure 2 : pentes de jour **−27 bp (EU) et −25 bp (Asie)** ; pentes de nuit **+14 bp (EU) et +19 bp (Asie)**. R² jour : 93,6 % (EU), 60,7 % (Asie) ; R² nuit : 46,8 % (EU), 79,6 % (Asie). Avec des bêtas close-to-close : jour −23 et −13 bp, nuit +15 et +21 bp.
- Table 2 (pays réunis, variables muettes pays) : pondéré capitalisation, nuit +7,9 bp (t = 9,52), jour −12,7 bp (t = −12,73), écart 20,6 bp ; équipondéré, nuit +11,2 bp, jour −15,4 bp, écart 26,6 bp.

### Durée de fermeture du marché (Table 3, US, équipondéré)
| Nuits fermées | Nombre | Pente nuit | Pente jour |
|---|---|---|---|
| 1 nuit | 4 536 | +11,7 bp (t = 12,61) | −11,6 bp (t = −6,70) |
| 2 nuits (fériés en milieu de semaine) | 53 | +10,0 bp (t = 1,25, ns) | non significatif |
| 3 nuits (week-end) | 1 049 | +13,7 bp (t = 6,97) | −21,5 bp (t = −5,82) |
| 4 nuits (week-end prolongé) | 148 | +17,1 bp (t = 2,88) | −20,5 bp (t = −1,86) |

- Hors cas à 2 nuits (trop peu d'observations), **la prime de nuit augmente avec la durée de fermeture**. En panel, la « décote » de jour augmente aussi avec la durée de la fermeture qui suit. International (Table 4) : prime nette nuit − jour en panel de 20,6 bp (1 nuit), 26,4 bp (3 nuits), 31,8 bp (4 nuits).

### Autres portefeuilles et décompositions
- **10 industries + 25 taille/BM** (Figure 5) : jour −17 bp par unité de bêta (R² 63,7 %), nuit +10 bp (R² 30 %). Table 5 : pondéré capitalisation, nuit +8,1 bp (t = 10,11), jour −7,4 bp (t = −5,20).
- **Bêtas cash-flow et taux d'actualisation** (Campbell-Vuolteenaho 2004) : le jour, −27 bp (cash-flow) et −16 bp (taux) ; la nuit, **+47 bp** et **+35 bp**. Écart nuit − jour 74 bp et 51 bp, plus fort pour le « mauvais » bêta (cash-flow). Les auteurs y voient un signe de spéculation sur les actifs de type loterie.
- **Doubles tris** (5 × 5) avec taille, BM, momentum, retournement d'un mois, volatilité idiosyncratique (Table 6, US) : la nuit croît de façon monotone avec le bêta et le jour décroît, **pour toutes les variables de contrôle**. Haut − bas bêta la nuit : de +10,8 bp (retournement) à +16 bp (taille, volatilité idio) ; le jour : de −13,7 bp (BM) à −18,3 bp (volatilité idio). Même schéma à l'international (Table 7).
- **Actions individuelles** (Table 8, US, environ 20 millions de jours-titres) : nuit +6,3 bp par unité de bêta (t = 11,37), jour −6,8 bp (t = −8,55). Avec taille, BM et rendement 12 mois : nuit +9,1 bp (t = 8,88), jour −9,0 bp (t = −10,10). La nuit, taille et BM sont reliés **négativement** au rendement ; le jour, BM positivement. International (Table 9) : nuit +5,9 bp, jour −8,7 bp.

### Stratégies « parier sur / contre le bêta » (Table 10, US 1992–2016, sans coûts)
| Stratégie | Rendement moyen/jour | Écart-type/jour | Sharpe journalier |
|---|---|---|---|
| A. Titres pondérés par (bêta − bêta moyen), long la nuit, inversé le jour | 0,10 % | 0,791 % | 0,126 (≈ 2,0 annualisé, 25,2 %/an) |
| B. Long décile 10 / short décile 1 la nuit, inversé le jour | 0,44 % | 1,802 % | 0,244 (3,87 annualisé, 110,88 %/an) |
| C. BaB de Frazzini-Pedersen (bêta-neutre) le jour, inversé la nuit (β_L = 0,45, β_H = 1,77) | 0,48 % | 1,433 % | 0,334 (≈ 5,3 annualisé, 120,96 %/an) |

- Le papier donne deux chiffres différents pour la stratégie B : **108,4 %/an et Sharpe 3,78** dans l'introduction, **110,88 % et 3,87** dans la section 3.6.
- Détail B : jour 0,25 %/jour, nuit 0,19 %/jour.
- **Mise en garde des auteurs** : ces stratégies exigent de fortes transactions sur les titres à fort bêta **à chaque ouverture et chaque clôture**, ce qui pourrait réduire fortement ou **éliminer** les rendements.
- Triple tri taille × BM × bêta (Table 11) : haut − bas bêta négatif le jour et positif la nuit dans **24 cases sur 25** (exception : taille moyenne / valeur).

### Annonces macro (section 4.1)
- Jours d'annonce PPI, emploi (8:30, avant l'ouverture) et FOMC programmés (en séance), comme Savor-Wilson (2014). La relation de nuit est fortement positive **les jours avec et sans annonce**. Le jour, elle est fortement négative les jours sans annonce et seulement faiblement négative les jours d'annonce. Les résultats ne viennent donc pas des annonces.
- En annexe, idem autour des annonces de résultats.

### Profil intraday par demi-heure (Figure 8, TAQ 1993–2016, mid quotes)
- La relation bêta–rendement est **négative** dans toutes les demi-heures sauf en milieu de journée (plate entre 11:00 et 14:00).
- Les rendements moyens de tous les portefeuilles **augmentent au fil de la journée** : négatifs de 9:30 à 10:30, légèrement positifs de 10:30 à 15:00, maximum entre 15:30 et 16:00.
- Interprétation proposée (non prouvée) : des spéculateurs amateurs de bêta achètent les titres à fort bêta à l'ouverture et revendent à l'approche de la clôture ; des arbitragistes vendent le matin et rachètent en fin de journée. La nuit, l'investisseur marginal serait l'investisseur de long terme.

### Taux sans risque implicite et futures Treasuries
- Constante de la SML de nuit négative (taux sans risque implicite de nuit trop bas) ; constante de jour positive et supérieure au rendement de chaque portefeuille. Figure 9 (US 1993–2016) : 24 h r = 0,18 − 0,13 β ; jour r = −0,069 + 0,11 β ; nuit r = 0,01 + 0,075 β (droites de la figure).
- **Futures Treasuries 5 et 10 ans** (CBOT, TRTH, prix à 5 minutes, **1996–2013**, mid quotes, winsorisés à 1 %/99 %, mêmes fenêtres jour/nuit que les actions) : rendement de jour **positif et significatif**, de nuit **négatif ou nul** :
  - 5 ans front : jour +0,010 %, nuit −0,006 %, écart +0,016 % (t = 3,46).
  - 5 ans 2e échéance : jour +0,010 %, nuit −0,011 %, écart +0,022 %.
  - 10 ans front : jour +0,009 %, nuit −0,001 %, écart +0,010 % (t = 1,65).
  - 10 ans 2e échéance : jour +0,013 %, nuit −0,007 %, écart +0,020 %.
  - L'écart jour/nuit des futures est **plus petit** que celui impliqué par les constantes des SML.

### Explications discutées
- Les contraintes d'emprunt (Black, Frazzini-Pedersen) peuvent aplatir la SML mais **pas la rendre décroissante** : elles n'expliquent pas tout. Jylhä (2018) trouve une SML décroissante les mois de marges élevées ; les auteurs suggèrent que les investisseurs seraient plus contraints le jour que la nuit.
- Conclusion : il faudrait probablement des modèles à agents hétérogènes dont l'investisseur marginal change entre le jour et la nuit.

### À retenir pour nous (strictement d'après le papier)
- Papier **en coupe transversale d'actions**. Les tests directement liés à un actif unique sont ceux sur les **futures Treasuries** : rendement moyen positif le jour (heures de séance actions), nul ou négatif la nuit, 1996–2013.
- Les titres à **fort bêta** sont forts la nuit et faibles le jour ; l'effet nuit augmente avec la durée de fermeture (week-ends).
- Les stratégies affichées ne tiennent **pas compte des coûts** ; les auteurs disent eux-mêmes qu'ils pourraient les annuler.

---

## [7] Bad Days and Good Nights: A Re-Examination of Non-Traded and Traded Period Returns — Robert G. Tompkins, Zvi Wiener

**Référence :** version du 4 mars 2008, SSRN 1102165. Frankfurt School of Finance and Management et Hebrew University of Jerusalem. Document de travail (certaines références sont marquées « à suivre »).

### Résultat principal
Sur les **futures** d'indices (prix d'ouverture et de clôture = vraies transactions), pour les grands marchés **hors US**, le rendement est **significativement négatif pendant la séance** et **positif quand le marché est fermé**. Pour le S&P 500, les deux sont positifs et la séance porte l'essentiel.

### Données (Table 1)
| Marché | Future | Début | Fin | Source |
|---|---|---|---|---|
| S&P 500 | CME | 21/04/1982 | 16/11/2007 | CME |
| FTSE 100 | LIFFE | 01/03/1988 | 16/11/2007 | LIFFE |
| DAX | Eurex | 21/01/1991 | 16/11/2007 | Deutsche Börse |
| CAC 40 | — | 03/01/1990 | 16/11/2007 | Bloomberg |
| Nikkei 225 | — | 05/09/1988 | 16/11/2007 | Bloomberg |

- Données OHLC quotidiennes. Contrat le plus proche (cycle mars, juin, septembre, décembre), roll à l'échéance. Le rendement de nuit qui suit l'échéance est calculé sur le contrat suivant ; pour les données Bloomberg (« nearby »), les jours d'échéance sont supprimés.
- Pourquoi des futures : les ouvertures d'indices cash ne sont pas de vrais prix. Les auteurs notent que l'ouverture de l'indice S&P 500 était égale à la clôture de la veille sur toute la période, et que l'ouverture du FTSE 100 cash est égale à la clôture précédente depuis janvier 2000.
- Rendements en log : C/C (clôture-clôture), O/C (séance), C/O (nuit).

### Statistiques (Table 2, annualisées)
| Marché | C/C moyenne | O/C (séance) moyenne | C/O (nuit) moyenne | Vol C/C | Vol O/C | Vol C/O |
|---|---|---|---|---|---|---|
| S&P 500 | 10,00 % | 7,72 % | 2,30 % | 18,69 % | 17,49 % | 8,22 % |
| FTSE 100 | 6,38 % | **−7,07 %** | **13,45 %** | 17,23 % | 14,69 % | 9,97 % |
| DAX | 9,88 % | **−4,78 %** | **14,66 %** | 22,50 % | 19,32 % | 12,29 % |
| CAC 40 | 5,77 % | **−3,03 %** | **8,78 %** | 21,48 % | 18,30 % | 11,47 % |
| Nikkei 225 | −3,33 % | **−14,60 %** | **11,24 %** | 22,79 % | 17,61 % | 13,76 % |

- Moments supérieurs : skewness C/O très négative pour le S&P 500 (−13,938) avec kurtosis de 877 ; kurtosis de nuit 13 à 25 pour les autres marchés. **La séance est presque symétrique** (skewness non différente de 0 pour FTSE, Nikkei, CAC) et peu leptokurtique. **Presque toute la non-normalité est de nuit.**
- Hors US, la séance est **significativement négative** (test contre 0). La variance de nuit est toujours significativement plus faible.
- **Dominance stochastique** d'ordre 2 et 3 de la nuit sur la séance pour **FTSE, DAX et Nikkei** (densités par noyaux, méthode de Bawa 1975).

### Décomposition et ratios de Sharpe (Table 3)
- S&P 500 : **77,2 % du rendement et 87 % de la variance** viennent de la séance.
- Part de variance de la séance : FTSE 72,6 %, DAX 73,7 %, Nikkei 61,1 %. On rejette dans tous les cas l'hypothèse que la séance ne porte qu'un tiers de la variance.
- Sharpe (rendement / écart-type, le future n'ayant pas d'excès de rendement attendu) :

| Marché | C/C | O/C | C/O |
|---|---|---|---|
| S&P 500 | 0,535 | 0,443 | 0,279 |
| FTSE 100 | 0,370 | −0,482 | **1,349** |
| DAX | 0,439 | −0,248 | **1,193** |
| CAC 40 | 0,269 | −0,165 | **0,765** |
| Nikkei | −0,146 | −0,820 | **0,816** |

- Si l'on multiplie l'écart-type hors US par √10 × 3 (VaR réglementaire Bâle I), le Sharpe C/O tombe à 0,08–0,13 et le buy & hold redevient le meilleur choix partout sauf au Nikkei.

### Stratégies (section 3)
1. **C/C** : buy & hold du future, roll à l'échéance.
2. **O/C** : achat à l'ouverture, vente à la clôture.
3. **C/O** : achat à la clôture, vente à l'ouverture suivante (contrat suivant le jour de l'échéance).
4. **« Alpha »** : long la nuit et **short la séance** (achat à la clôture ; à l'ouverture, vente de 2 contrats ; rachat d'1 contrat à la clôture).
- Calcul de richesse avec intérêt au jour le jour (LIBID) et un spread s (achat au prix + s/2, vente au prix − s/2). Le papier annonce aussi le spread s* qui annule les profits, mais **ne donne pas de tableau de coûts** ; le seul chiffre après coûts est dans l'introduction : **Nikkei 1988–2008, stratégie de nuit +11,24 %/an, 6,5 % après coûts**, contre −3,3 %/an pour le marché.
- Résultats (Figure 1, échelle log) :
  - **S&P 500** : meilleur = C/C ; avant le krach de 1987, C/O second ; après 1987, O/C meilleur que C/O ; **« alpha » le pire** presque tout le temps.
  - **CAC 40** : C/C et O/C dominent jusqu'en **2002**, puis C/O et « alpha » dominent O/C. Les auteurs l'attribuent au passage, en 2002, à un système d'enchères pour l'ouverture et la clôture des actions françaises (auparavant prix fixés par un petit groupe de teneurs de marché).
  - **DAX, FTSE, Nikkei** : classement sur toute la période **alpha > C/O > C/C > O/C**. La richesse de la stratégie C/O suit une exponentielle qui explique 95 à 99 % de sa variance.
- Évaluation trimestrielle (annexe A, compte de 100 par trimestre, marge = valeur nominale d'un contrat) de la stratégie « alpha » : profit trimestriel moyen **FTSE 1,96** (min −7,23, max 15,22, σ 4,59) ; **DAX 1,52** (min −18,39, max 20,91, σ 7,01) ; **CAC 1,37** (min −9,63, max 12,18, σ 4,45) ; **Nikkei 3,28** (min −17,56, max 19,30, σ 5,37).
- Le papier affirme que l'effet existe en marché haussier comme baissier (contrairement à l'hypothèse de Compton et Kunkel 2003 d'un artefact de marché baissier).

### Explications testées et rejetées
- **Préférence pour la skewness positive** (Harvey-Siddique) : rejetée, le rendement le plus élevé (nuit) a la skewness la plus négative (sauf DAX).
- **Diffusion le jour, sauts la nuit** : les auteurs pensent que la séance suit une diffusion à volatilité stochastique (type Heston) et la nuit un processus à sauts (Merton, Cox-Ross). Mais des primes de risque cohérentes n'expliqueraient pas des rendements de séance **négatifs** hors US et pas aux US.
- **Excès de confiance / sur-trading** ou **prime de liquidité de nuit** : devraient toucher aussi les US.
- **Nouvelles publiées hors séance** : incompatible avec les signes observés hors US.
- **Globex** : avant le 9 septembre 1999 les futures S&P ne se traitaient qu'à la criée (8:15–15:15 heure de Chicago) ; les rendements avant et après l'électronique ne sont pas significativement différents.

### Explication retenue : la réglementation du risque des teneurs de marché sur options
- Hors US, la tenue de marché sur dérivés actions est dominée par des **banques soumises à Bâle I / CAD** : VaR à **10 jours**, multipliée par 3. CAD en vigueur en 1996 (maisons de titres), Bâle I appliqué en 1998 (banques européennes ; la Banque du Japon impose la même approche en 1998).
- Aux US, Glass-Steagall empêchait les banques de faire ce métier avant 2002 ; les teneurs de marché CME sont soumis à SPAN, horizon **1 jour**.
- Mécanisme : un teneur de marché vendeur de puts OTM et acheteur de calls OTM, delta-neutre, réduit sa charge de capital (exemple : de 5 à 1 million) en **vendant des futures à la clôture et en les rachetant à l'ouverture** (Taleb 1998, Hua-Wilmott 1997, Wilmott 1999). Si beaucoup font ainsi, l'indice baisse à la clôture et monte à l'ouverture.
- **Test avant/après le 30 juin 1998** (rendement trimestriel moyen de la stratégie de nuit, Table 4) :

| Marché | Avant | Après | Conclusion des auteurs |
|---|---|---|---|
| S&P 500 | −1,13 % (significativement négatif) | +0,17 % (non différent de 0) | hausse significative |
| CAC 40 | 2,46 % | 0,42 % (non différent de 0) | **baisse** significative |
| DAX | 1,19 % | 1,76 % | hausse non significative, aucune période différente de 0 |
| FTSE 100 | 1,39 % | 2,81 % | **hausse significative**, après 1998 différent de 0 |
| Nikkei 225 | 2,41 % | 4,07 % | **hausse significative**, différent de 0 dans les deux périodes |

- Conclusion des auteurs : hypothèse confirmée pour le FTSE et le Nikkei, pas pour le CAC ni le DAX. Ils supposent que les institutions allemandes auraient adopté la VaR plus tôt ; le cas du CAC (bascule en 2002) reste inexpliqué.

### À retenir pour nous (strictement d'après le papier)
- Futures **DAX, FTSE, CAC, Nikkei** (jusqu'en 2007) : rendement de **séance négatif** et de **nuit positif**. Pour le **S&P 500**, c'est l'inverse (séance > nuit).
- Pour le CAC, l'effet n'apparaît qu'**après 2002**.
- Le seul chiffre après coûts est celui du Nikkei (11,24 % → 6,5 %/an). Aucune donnée après 2007.

---

## [8] Cycles of Declines and Reversals following Overnight Market Declines — Farshid Abdi

**Référence :** Working Papers on Finance n° 2018/29, Swiss Institute of Banking and Finance (Université de Saint-Gall), septembre 2018. SSRN 3287680. Job market paper (Saint-Gall et NYU Stern).

*Note de lecture : dans le PDF, les équations et les noms de lignes des Tables III à VI ne sont pas extractibles (seuls les chiffres sont lisibles, sans savoir à quelle variable ils correspondent). Les résultats ci-dessous viennent donc du texte du papier et des tables I et II, qui sont lisibles.*

### Thèse
Depuis 2001, aux US, une **baisse du marché pendant la nuit** est suivie d'une **nouvelle baisse pendant la séance** pour les actions volatiles, puis d'un **rebond pendant la nuit suivante**. Ces cycles « baisse puis retournement » expliquent pourquoi la relation entre rendements moyens de séance et de nuit est devenue fortement **inverse** en coupe transversale.

### Mécanisme proposé
Liquidité de financement et liquidité de marché (Brunnermeier-Pedersen 2009) : une perte de richesse pendant la nuit resserre les contraintes de financement des investisseurs à levier ; ils doivent vendre dans la séance suivante, la liquidité se dégrade, les prix baissent, puis reviennent. L'auteur relie cela au poids croissant du **financement à très court terme** (repo overnight à renouveler chaque jour) et à l'idée de Dow et Han (2018) : quand les investisseurs informés sont contraints, les autres ne rachètent qu'avec une décote (« lemon »).

### Données
- TAQ fusionné avec CRSP, **janvier 1993 – décembre 2016**. Monthly TAQ jusqu'en septembre 2003, Daily TAQ ensuite (appariement trades/quotes selon Holden et Jacobsen 2014).
- Actions ordinaires (codes 10 et 11) NYSE, AMEX, NASDAQ. Exclus : jours sans trade, mois avec une clôture < 5 $, changement de marché principal, dividende ou split déplaçant le facteur d'ajustement de plus de 1 %. Trades hors séance exclus, ainsi que les spreads effectifs > 40 %.
- **Rendements sur mid quotes** : ouverture = mid qui précède le **premier trade** de la séance ; clôture = mid qui précède le **dernier trade**. Séance = open-to-close, nuit = close-to-open suivant. Pas de pré-ouverture ni d'after-hours (volumes trop faibles).
- Spread effectif pondéré par le volume en dollars ; déséquilibre d'ordres = flux signé net / volume (signe par comparaison au mid).
- Table I : rendement de séance moyen 0,00 % (1993–2000) et **−0,03 %** (2001–2016) ; rendement de nuit moyen **+0,10 %** dans les deux périodes ; spread effectif moyen 1,37 % puis 0,51 %. Environ 7,9 et 12,3 millions d'observations titre-jour.

### Résultat 1 : apparition d'une relation inverse séance/nuit
- Corrélation transversale annuelle entre rendement moyen de séance et rendement moyen de nuit (titres avec au moins 100 jours) : environ **+0,2 en 1993**, en baisse régulière jusqu'à environ **−0,9 en 2016** (le texte écrit « 0.9 », mais le contexte et la figure indiquent une valeur négative). Même schéma avec la corrélation de Spearman et avec les pentes de régression.
- Moyennes (Table II, Newey-West 4 retards) :

| Période | Pearson | Spearman | Pente nuit sur séance | Pente séance sur nuit |
|---|---|---|---|---|
| 1993–2000 | 0,069 | 0,091* | 0,319 | 0,014 |
| 2001–2016 | **−0,549*** | **−0,444*** | **−0,751*** | **−0,427*** |

- En 2001–2016, le quintile au plus faible rendement de séance a environ **18 bp/jour** de rendement de séance en moins, compensés par **+16 bp/jour** la nuit (texte : « 18 basis points (bps) per day, which is met with average overnight returns of +16 bps »). Rien de tel en 1993–2000.
- La corrélation temporelle entre la séance et la nuit qui suit (par titre et par année) évolue de la même façon (Figure 5).

### Résultat 2 : les cycles suivent les baisses de nuit du marché
- Quintiles de volatilité (variance réalisée de l'année civile précédente), rebalancés chaque année.
- 2001–2016 (Figure 6) : après une **baisse du marché pendant la nuit**, les titres volatils **baissent pendant la séance** ; ils ne montent pas significativement après une hausse de nuit. La nuit suivante, tous les quintiles ont un rendement plus élevé après une baisse de nuit qu'après une hausse : **retournement**.
- 1993–2000 (Figure 7) : la baisse de séance après une baisse de nuit fait environ **un tiers** de celle de la période récente, et il n'y a pas de retournement visible la nuit suivante.
- Régressions (Tables III et IV) avec rendements passés de séance et de nuit (portefeuille et marché) et variables muettes pour les rendements négatifs :
  - Depuis 2001, une baisse **de nuit** du marché prédit une baisse de la séance suivante, plus forte pour les quintiles volatils et pour le portefeuille volatil − peu volatil.
  - Le rendement de nuit du portefeuille lui-même ne prédit pas la séance suivante.
  - Le rendement **de séance** du marché la veille ne prédit pas la séance des titres volatils. L'auteur l'explique ainsi : un choc pendant la séance déclenche des ventes immédiates, alors qu'un choc de nuit ne peut se traduire en ventes qu'à l'ouverture.
  - Le portefeuille volatil − peu volatil remonte la nuit suivante après une baisse de nuit du marché. Pas de retournement asymétrique après les baisses **de séance** du marché depuis 2000.
  - Rien de tout cela n'est significatif en 1993–2000.

### Résultat 3 : la liquidité se dégrade après une baisse de nuit (Table V)
- Depuis 2001, une baisse de nuit du marché est suivie d'une **hausse des spreads effectifs** dans la séance suivante, plus forte pour les titres volatils, même en contrôlant les spreads passés. Non significatif en 1993–2000. Extension de Hameed, Kang et Viswanathan (2010), qui travaillaient à l'horizon hebdomadaire.
- **Repo des primary dealers** (Fed de New York, Figure 8) : le repo overnight dépasse le repo à terme **après 2001**, atteint environ **3 000 Md$** avant la crise, environ deux fois le repo à terme, et reste à ce ratio jusqu'à la fin de l'échantillon.

### Résultat 4 : flux d'ordres (Table VI)
- Les investisseurs sont en moyenne **contrariens** après les baisses (ils fournissent la liquidité). Avant 2001, ils réagissent surtout aux baisses **de séance** ; depuis 2001, surtout aux baisses **de nuit**. Le prix baisse quand même ce jour-là, ce que l'auteur relie à la décote « lemon » de Dow et Han (2018).

### Résultat 5 : volatilité idiosyncratique plutôt que bêta (Figure 9)
- Double tri 3 × 3 : bêta, puis volatilité idiosyncratique dans chaque tercile de bêta (modèle Fama-French + momentum, année précédente).
- Après une baisse de nuit, les écarts de baisse en séance puis de rebond la nuit suivante sont plus grands entre terciles de **volatilité idiosyncratique** qu'entre terciles de bêta. Après une hausse de nuit, le rendement de nuit augmente avec la volatilité idiosyncratique mais **diminue** avec le bêta.
- Conséquence selon l'auteur : la séance baisse et la nuit monte avec la volatilité idiosyncratique, surtout après les baisses de nuit, ce qui expliquerait les résultats contradictoires de la littérature sur ce risque.

### Explications alternatives écartées (section VII)
- **Arbitrage des ETF** : les achats ont plus d'impact que les ventes, la séance devrait donc monter, pas baisser.
- **Trading haute fréquence** : les retournements apparaissent avant son essor ; les HFT ne portent pas de positions la nuit ; ils sont surtout actifs sur les grandes valeurs liquides, alors que l'effet est plus fort sur les titres volatils.
- **Betting against beta** (Hendershott et al.) : la volatilité idiosyncratique explique mieux que le bêta ; après les hausses de nuit, la séance **augmente** avec le bêta, contrairement à leur résultat.

### À retenir pour nous (strictement d'après le papier)
- Régime conditionnel : **nuit du marché négative → séance suivante plus faible pour les titres volatils → nuit suivante en rebond**. Valable **depuis 2001**, absent en 1993–2000.
- Le choc qui compte est celui **de la nuit**, pas celui de la séance de la veille.
- Le papier porte sur des portefeuilles d'actions triés par volatilité, sans test de stratégie ni coûts. Données jusqu'en 2016.

---

## [9] Overnight Return, the Invisible Hand Behind the Intraday Return? A Retrospective — Ben Branch, Aixin Ma

**Référence :** SSRN 3259614 (pas de date sur le PDF ; les résultats sont étiquetés « 2018 », période 2011–2017). Mise à jour de Branch et Ma (2012, Journal of Applied Finance), dont les résultats sont repris comme « 2012 ».

### Question
L'autocorrélation **négative entre le rendement de nuit et le rendement de séance qui suit** (même jour), trouvée dans Branch et Ma (2012), a-t-elle survécu sur une période plus récente et plus calme ?

### Données et méthode
- CRSP, prix d'ouverture et de clôture ajustés (CFACPR), **janvier 2011 – décembre 2017** (environ 1 760 jours).
- Marché : **SPY** et non l'indice S&P 500, car l'ouverture de l'indice est calculée à 9:31 avec de nombreux titres pas encore ouverts : c'est souvent la clôture de la veille, d'où un rendement de nuit de 0 % très fréquent. Le SPY ouvre presque toujours à 9:31 avec un prix tiré des futures.
- Rendement de nuit = (ouverture_t − clôture_{t−1}) / clôture_{t−1} ; séance = (clôture_t − ouverture_t) / ouverture_t.
- Méthode inspirée de Fama-MacBeth : corrélations transversales quotidiennes puis moyennes. Pour le SPY, corrélations en série temporelle par titre puis moyenne transversale.
- Robustesse : données winsorisées à 0,05 %, NYSE, AMEX et NASDAQ séparés, **mid bid/ask de clôture** à la place de la clôture (aucun changement significatif).

### Résultats
- **Corrélation nuit/séance des actions** : **−0,191** (2011–2017) contre −0,252 (étude 2012). Toujours négative mais plus faible.
- **SPY** : la corrélation entre sa nuit et sa séance est désormais **légèrement positive**. Le retournement a disparu pour les grandes capitalisations.
- La corrélation entre la nuit des actions et la nuit du SPY est bien plus forte qu'avant (0,389) : le facteur marché pèse davantage la nuit.
- **Moyennes** (2011–2017) : actions, **nuit +0,044 %/jour** (t = 3,82), **séance −0,018 %** (t = −1,16). SPY : nuit 0,020 % (t = 1,48), séance 0,026 % (t = 1,66), non significatifs. Dans l'étude 2012, les deux composantes des actions étaient positives. Rendements nettement moins dispersés qu'avant (marché plus calme).
- **Conditionnement sur le signe de la nuit** (Table 3, 2011–2017) :
  - Nuit négative (moyenne −0,874 %) → séance **+0,216 %** (t = 14,21).
  - Nuit positive (moyenne +0,904 %) → séance **−0,242 %** (t = −15,85).
  - Nuit nulle → séance −0,035 %.
  - (Étude 2012 : −1,838 % → +0,658 % ; +1,914 % → −0,601 %.)
- **Relation monotone** (Table 4, quartiles, 2011–2017) :

| Quartile de la nuit | Nuit négative : nuit moyenne → séance | Nuit positive : nuit moyenne → séance |
|---|---|---|
| Plus extrême | −2,304 % → **+0,640 %** | +2,429 % → **−0,734 %** |
| 2e | −0,705 % → +0,141 % | +0,698 % → −0,164 % |
| 3e | −0,359 % → +0,073 % | +0,358 % → −0,069 % |
| Plus faible | −0,131 % → +0,021 % (ns) | +0,132 % → −0,001 % (ns) |

- **Régressions** (Table 5) de la séance sur la nuit du jour, la séance et la nuit de la veille :
  - Modèle 1 : coefficient de la nuit **−0,319** (contre −0,368 en 2012). R² ajusté environ divisé par deux.
  - Avec interaction nuit × log(capitalisation) (modèles 2 et 4) : interaction **positive** (0,053 dans le modèle 4) : plus le titre est gros, moins il se retourne.
  - Avec la nuit du SPY (modèle 3) : coefficient +0,33 sur la nuit du SPY, −0,295 sur la nuit du titre.

### Explications proposées (non testées)
- **Comportement des teneurs de marché / spécialistes à l'ouverture** : après la clôture, il ne reste que les ordres GTC, le carnet est plus mince et le spread plus large. Face à un déséquilibre d'ordres au marché avant l'ouverture, le teneur de marché a intérêt à ouvrir **dans le sens du déséquilibre** (plus d'ordres limites exécutés, inventaire mieux géré, plus d'activité), ce qui **dépasse le prix d'équilibre** ; le prix revient ensuite dans la séance. Effet plus faible sur les grandes valeurs (plus d'ordres, plus de capital nécessaire pour déplacer le prix).
- Les auteurs notent que la part du volume NYSE faite à la clôture est passée de **17 % en 2012 à 26 % en 2017** (fonds indiciels), ce qui renforce selon eux la fiabilité du prix de clôture.
- **Bid-ask bounce** : écarté (le mid de clôture ne change rien).
- Autres pistes citées : attention des particuliers à l'ouverture (Berkman et al., Barber-Odean).

### Implications pratiques (selon les auteurs)
- Acheter à l'ouverture un titre qui ouvre en baisse (ou vendre à découvert celui qui ouvre en hausse) puis déboucler à la clôture demande de connaître le sens du déséquilibre d'ordres avant l'ouverture, ce que seul le teneur de marché sait ; passer soi-même un ordre à l'ouverture peut modifier ce déséquilibre. Trader juste après l'ouverture est aussi difficile : les coûts et les petits mouvements contraires peuvent effacer le profit. Le pré-marché pourrait donner un indice, mais **cela n'a pas été testé**.
- Conseil explicite : éviter les **ordres au marché à l'ouverture**.

### À retenir pour nous (strictement d'après le papier)
- Sur 2011–2017, le retournement nuit → séance existe pour les **petites valeurs** mais **a disparu pour le SPY** (corrélation légèrement positive).
- Aucune stratégie testée, aucun coût calculé.

---

## [10] Dark Side of the Day: Overnight Price Jumps and Short-Term Return Predictability — Hulusi Bahcivan, Lammertjan Dam, Halit Gonenc

**Référence :** version de juin 2026, SSRN 4335622. Boğaziçi University (Istanbul) et University of Groningen.

### Question
Quand une action fait un **saut de prix pendant la nuit** (choc d'information entre la clôture et l'ouverture), le marché sur-réagit-il, et que se passe-t-il dans les jours qui suivent ? La nuit est vue comme un cadre « propre » : pas de bruit de trading, de déséquilibres de liquidité ni d'apprentissage intraday.

### Données
- **9 283 actions** ordinaires NYSE, AMEX, NASDAQ, **juillet 1993 – décembre 2021** (342 mois). Données CRSP depuis le 15 juin 1992 (premier prix d'ouverture), fusionnées avec COMPUSTAT.
- Filtres : un seul PERMNO par PERMCO, pas d'interruption de cotation, au moins **3 ans** d'historique (2 ans en robustesse), pas de valeur COMPUSTAT manquante. Titres délistés conservés (pas de biais de survie).
- **Ouverture CRSP = prix de l'enchère d'ouverture.** Ouverture manquante (3,62 % des observations) remplacée par la clôture de la veille (rendement de nuit nul, pas de saut détecté). En robustesse, sauts exclus quand la clôture CRSP est une moyenne bid/ask.
- Rendement de nuit = rendement journalier CRSP (ajusté des distributions) − rendement de séance (log).
- Contrôles : taille, BM, levier, momentum coupé en (t−1, t−5) et (t−6, t−11) mois, illiquidité d'Amihud (volume NASDAQ × 0,7), **volatilité idiosyncratique calculée hors jours de saut de nuit** (IVOL-OJI), rendement de la veille du saut (PREV).

### Détection des sauts
- Test non paramétrique de **Lee et Mykland (2008)** : rendement standardisé par la volatilité intégrée estimée par variation bipuissance sur une **fenêtre glissante de K = 16 jours** passés (pas de biais d'anticipation). Le seuil vient de la loi des maxima.
- Appliqué séparément aux séries de nuit, de séance et journalières. Seulement **11,6 %** des jours de saut de nuit sont aussi des jours de saut sur le rendement journalier.
- Les auteurs préfèrent ce test à un simple seuil de percentile (qui manque les sauts modestes en période calme et classe à tort de grands mouvements « continus »).

### Statistiques descriptives (Table 1)
- **380 747 sauts de nuit** (1,57 % des nuits ; environ 700 par mois même en robustesse) : **201 191 négatifs** (moyenne −6,9 %, médiane −4,8 %) et **179 556 positifs** (moyenne +8,6 %, médiane +5,2 %).
- La séance qui suit est de signe **opposé** au saut dans environ la moitié des cas (51 % après un saut négatif ; 47 % sur l'ensemble).
- La veille du saut, le rendement journalier moyen est de signe **opposé** au saut : **+1,1 %** avant un saut négatif, **−0,6 %** avant un saut positif (d'où le contrôle PREV).
- Peu de titres ont plusieurs sauts dans un mois, surtout après 2000 (9,1 % pour les sauts positifs, 10,4 % pour les négatifs).

### Résultat principal : retournement
- Régressions transversales mensuelles du rendement cumulé des 1 à 5 jours suivants sur le rendement du saut, avec contrôles. Erreurs regroupées par code SIC, Newey-West 12 retards.
- **Approche isolée (Table 4)** :
  - Sauts **négatifs** : coefficient **−0,42** sur la séance qui suit (t = −3,89), environ −0,43 à −0,45 jusqu'à 5 jours.
  - Sauts **positifs** : coefficient **−0,09** sur la séance qui suit (t = −11,55), −0,11 à −0,12 jusqu'à 5 jours.
- **Approche cumulée** (sauts du mois agrégés, Tables 5 et 6) : environ **−0,47** (négatifs) et **−0,10** (positifs), significatifs à 1 % quelle que soit la spécification (t = 3,91 et 11,15 en valeur absolue dans le modèle complet). Seuls le saut et la taille sont significatifs sur les 5 jours.
- Robuste à 2 ans d'historique minimum, à l'exclusion des clôtures moyennes bid/ask, à d'autres mesures de volatilité idiosyncratique. Le résultat tient aussi en excluant la séance du jour du saut (coefficients plus faibles, car l'essentiel du retournement se fait ce jour-là).
- **Asymétrie** : retournement bien plus fort après les sauts **négatifs**.

### Ampleur du retournement (Tables 12 et 13)
- Sauts négatifs : environ **20 % ou un peu plus** du saut est repris dans la séance qui suit, dans tous les quintiles de volatilité idiosyncratique (23 % pour Q1, 26 % pour Q5) ; un peu plus à J+2 et J+3.
- Sauts positifs : **8 %** repris le premier jour pour Q1 (faible volatilité idiosyncratique), **16 %** pour Q5 ; peu de changement à J+2 et J+3.
- Saut moyen du quintile le plus calme : −4,4 % / −6,5 % (négatifs) et +5,6 % / +6,9 % (positifs).
- Par quintile d'illiquidité d'Amihud : retournement le plus fort pour Q5 (les plus illiquides).

### Sous-périodes et crises
- Juillet 1993–décembre 2003, janvier 2004–décembre 2021, août 2007–décembre 2013 (crise financière, crise de la dette européenne, reprise) : la prévisibilité est maintenue partout.
- **Le coefficient des sauts négatifs fait plus que doubler en août 2007–décembre 2013** ; celui des sauts positifs bouge peu.
- Crises aiguës (dot-com mars 2000–octobre 2002, crise financière août 2007–juin 2009, Covid février–mai 2020) : coefficients plus élevés en crise qu'hors crise pour les deux types de sauts ; pour les sauts négatifs, plus du double.
- Les ouvertures manquantes deviennent rares après 2003 (5 732 par mois en moyenne avant, 724 après, 133 en 2020–2021).

### Nouvelles de marché ou spécifiques (proxy)
- Jour « de marché » si le rapport sauts positifs / sauts négatifs est < 0,5 ou > 2 (puis 0,33 / 3), avec au moins 30 sauts ce jour-là (aussi 15 et 45).
- En 2004–2021, seuils 0,5 / 2 : après un saut négatif, coefficient **−0,61 les jours de marché contre −0,38** les jours spécifiques ; après un saut positif, −0,10 contre −0,07. Avec 0,33 / 3, les coefficients des sauts négatifs se rejoignent (−0,46 et −0,44). Les auteurs reconnaissent les limites de ce proxy.

### Coupes transversales
- Quintiles de volatilité idiosyncratique (Table 14) : significatif dans tous les quintiles ; sauts négatifs, plus forte significativité en Q1 (−0,31, t = −20,68) et plus fort effet économique en Q5 (−0,51, t = −5,29).
- Quintiles de taille (Table 15) : significatif partout, **plus fort pour les petites capitalisations**.
- À horizon plus long, les t-stats baissent ; pour certains quintiles (taille, illiquidité), le signe s'inverse après quelques jours : la sur-réaction devient une **dérive** dans le sens du saut.

### Stratégies (sans frictions)
- **Événementielle quotidienne** (Table 16) : chaque jour, portefeuilles pondérés par la capitalisation, **long les titres à saut négatif, short les titres à saut positif**. Alpha FF3 :

| Période | 1 jour | 2 jours | 3 jours | 4 jours | 5 jours |
|---|---|---|---|---|---|
| 1993–2021 | **1,05 %** (t = 11,38) | 0,93 % | 0,84 % | 0,79 % | 0,74 % |
| 1993–2003 | 0,74 % | 0,65 % | 0,51 % | 0,37 % | 0,27 % |
| 2004–2021 | 1,24 % | 1,10 % | 1,01 % | 1,02 % | 1,00 % |

- **Mensuelle** (Table 17) : tri en déciles du rendement cumulé des sauts du mois, détention 1 mois. Long D1 / short D10 : alpha FF4 **−0,64 %** (t = −2,03) ; long D1 / short D5 : −0,8 % (t = −2,10). Le retournement ne dure que quelques jours.
- **Limites énoncées par les auteurs** : pas de coûts ni de commissions, pas de contrainte de vente à découvert, pas de glissement, détection du saut et exécution supposées immédiates au prix d'ouverture, débouclage à la clôture. Les alphas sont une **borne supérieure**.

### Interprétation
- Sur-réaction comportementale (aversion aux pertes, attention), plus forte sur les titres petits et volatils, et après les mauvaises nouvelles.
- Ils jugent peu probable une prime de fourniture de liquidité (Grossman-Miller) : la relation est la même dans tous les états de marché ; les teneurs de marché et HFT se retirent quand le choc touche plusieurs titres ; les HFT (78 % du volume US en 2009 selon Zhang 2010) ne gardent pas de positions la nuit. Mais ils reconnaissent ne pas avoir testé ce canal avec des données d'inventaire.
- Le spread ne peut pas expliquer l'ampleur des retournements (ouverture par enchère, spreads en baisse).
- L'after-hours est jugé peu représentatif (liquidité faible, coûts 4 à 5 fois plus élevés selon Jiang et al. 2012) : l'ouverture reste le canal principal.
- Ils pensent que l'effet persistera (clientèle de particuliers le matin, institutions l'après-midi ; biais comportementaux).

### À retenir pour nous (strictement d'après le papier)
- Après un **gap d'ouverture extrême** détecté comme un saut (test de Lee-Mykland sur 16 jours), environ **20 %** d'un gap baissier et **8 à 16 %** d'un gap haussier sont repris **dans la séance qui suit**.
- L'effet est plus fort après les gaps **baissiers**, en **crise**, et les jours où **beaucoup de titres sautent dans le même sens**.
- Papier sur actions individuelles. Les alphas sont calculés sans coûts et supposent une entrée au prix d'ouverture.

---

## [11] Day and Night Expected Returns Under Overnight Information Shocks: New Tug-of-War Pattern — Hulusi Bahcivan

**Référence :** septembre 2025, SSRN 5240716. Boğaziçi University. Auteur unique (même premier auteur que [10], même base de données et même détection des sauts).

### Question
Le « tug of war » de Lou, Polk et Skouras (2019) — persistance des rendements de nuit et de jour d'un mois sur l'autre, et retournement entre les deux — change-t-il quand l'action a subi un **choc d'information de nuit** (un saut de prix de nuit) ? Hypothèse tirée de Da, Gurun et Warachka (2014) : l'information **discrète** (choc) attire l'attention et **affaiblit le momentum**, contrairement à l'information continue.

### Données et méthode
- CRSP, NYSE/AMEX/NASDAQ, **juillet 1993 – décembre 2021** (342 mois), actions ordinaires, un seul PERMNO par PERMCO, historique continu, au moins 3 ans (2 ans en robustesse) ; un peu moins de 9 300 titres. Ouvertures manquantes remplacées par la clôture de la veille.
- Sauts de nuit détectés par **Lee et Mykland (2008)**, fenêtre de 16 jours. **52,8 % des sauts sont négatifs, 47,2 % positifs** (49,5 % / 50,5 % en robustesse).
- Différence avec Lou-Polk-Skouras : eux définissent les « mois de nouvelles » à partir de calendriers d'événements et de Dow Jones Newswire (nouvelles propres à l'entreprise) ; ici le saut est une mesure **après coup** de la surprise, quelle que soit la source (y compris nouvelles de marché, analystes, géopolitique, rumeurs). Un titre « sans saut » peut avoir eu des nouvelles, mais pas assez surprenantes pour rompre la continuité du prix.
- Chaque mois, titres séparés en **avec saut de nuit** et **sans saut**, triés en déciles selon le rendement de nuit cumulé (panel A) ou de séance cumulé (panel B) du mois, puis rendements de nuit et de séance du **mois suivant**, pondérés par la capitalisation. Alphas CAPM et Carhart (FF4), Newey-West 12 retards.

### Résultats (Table 1, alphas mensuels, en fraction)
**Panel A — tri sur le rendement de nuit du mois passé (alpha FF4 du mois suivant) :**

| | Sans saut, nuit | Sans saut, séance | Avec saut, nuit | Avec saut, séance |
|---|---|---|---|---|
| D1 (nuit la plus faible) | −0,021 (t = −4,04) | +0,039 (t = 4,62) | +0,002 (ns) | +0,014 (t = 1,75) |
| D10 (nuit la plus forte) | +0,046 (t = 6,14) | −0,039 (t = −7,17) | +0,030 (t = 4,05) | −0,021 (t = −4,49) |
| D10 − D1 | **+0,067** | **−0,079** | **+0,028** | **−0,035** |

- Les titres sans saut reproduisent le tug of war de Lou-Polk-Skouras.
- Pour les titres avec saut, la stratégie D10 − D1 rapporte **3,9 points de moins** la nuit et perd **4,4 points de moins** en séance.
- Le schéma de Lou-Polk-Skouras est **rompu pour D1 des titres avec saut** : la nuit faible ne se prolonge plus le mois suivant (alpha de nuit +0,2 %, non significatif).
- D10 avec saut : 1,6 point de moins la nuit et 1,8 point de mieux en séance que sans saut.

**Panel B — tri sur le rendement de séance du mois passé :**

| | Sans saut, nuit | Sans saut, séance | Avec saut, nuit | Avec saut, séance |
|---|---|---|---|---|
| D1 | +0,039 | −0,032 | +0,049 | −0,042 |
| D10 | −0,009 | +0,015 | −0,011 | +0,019 |
| D10 − D1 | −0,048 | +0,047 | **−0,060** | **+0,061** |

- Ici le tug of war est **amplifié** pour les titres avec saut (environ 1,2 à 1,4 point de plus).
- Différences avec / sans saut (Table 2) : très significatives pour le tri sur la nuit (D10 − D1 : t = −7,10 la nuit, 7,26 en séance) ; pour le tri sur la séance, différences de stratégie significatives seulement à 10 %.
- En moyenne, les titres avec un saut de nuit négatif (positif) ont un rendement de séance cumulé positif (négatif).
- Robustesse (2 ans d'historique, sauts exclus si la clôture est une moyenne bid/ask, Table 3) : résultats quasi identiques.

### Interprétation de l'auteur
- Conforme à Da et al. (2014) : l'information **discrète** attire l'attention, les investisseurs réagissent fort et ensemble, d'où un **momentum affaibli** sur la composante de nuit. Les sauts étant rares, ils ne persistent pas (comme la faible autocorrélation de la mesure ID de Da et al.).
- Le tri sur la séance donne des alphas plus forts pour les titres avec saut, car la sur-réaction aux chocs de nuit gonfle les rendements de séance mensuels.
- L'auteur précise que ces stratégies à coût nul ne sont pas forcément rentables après coûts et frictions (limites à l'arbitrage, Shleifer-Vishny).

### À retenir pour nous (strictement d'après le papier)
- Résultat en **coupe transversale d'actions**, horizon **mensuel** (portefeuilles déciles).
- La persistance des rendements de nuit (un mois de bonnes nuits suivi de bonnes nuits) est **beaucoup plus faible quand le mois contient un saut de nuit** ; elle disparaît pour les pires nuits.
- Pas de coûts calculés.

---

## [13] Overnight Bitcoin Losses and the Timing of US Equity Repricing — Minwoo Song

**Référence :** 1er octobre 2026, SSRN 7579278. Lehman College (CUNY). Auteur unique, papier court (7 pages) qui se présente lui-même comme **exploratoire**.

### Question
Une **baisse du Bitcoin pendant la nuit** (pendant que la bourse US est fermée) est-elle associée à une ouverture plus basse des actions US, et prédit-elle un **risque de baisse dans la séance qui suit** ?

### Données et timing
- **2 202 séances NYSE**, 2 janvier 2018 – 6 octobre 2026 (dernière année incomplète). 2 201 observations après contrôles.
- Bitcoin : barres **horaires BTC/USD de Gemini** (CryptoDataDownload) ; **Bitstamp** en robustesse (historique plus court). SPY et QQQ : ouverture et clôture **Yahoo Finance**. VIX et SKEW : Cboe.
- **Signal Bitcoin** b_t = 100 × log(BTC à 09:00 New York / BTC à la clôture actions précédente). Clôture normalement à 16:00 (13:00 les jours de clôture anticipée). Prix = clôture de la barre horaire qui **se termine juste avant 09:00**. Les **30 dernières minutes avant l'ouverture** sont volontairement exclues. Lundi et lendemains de férié : toute la fermeture est incluse ; la durée de fermeture est un régresseur. Heure d'été, fériés et week-ends gérés par le calendrier de la bourse.
- Gap d'ouverture g = 100 log(ouverture / clôture veille) ; séance d = 100 log(clôture / ouverture). Prix bruts des ETF (le gap inclut les détachements de dividende ; l'auteur le signale comme à corriger).
- Perte L = max(−b, 0), gain G = max(b, 0), séparés. Contrôles connus avant 09:00 : rendement SPY de la veille, VIX de clôture de la veille, écart-type des 20 dernières séances du SPY, durée de fermeture, jour de la semaine. Newey-West 5 retards.
- **Le gap d'ouverture et la variation du VIX chevauchent la fenêtre du signal** : ce sont des associations, pas des rendements accessibles à 09:00. Seule la **séance** est postérieure au signal.

### Résultats (Table 1 : coefficient de la perte Bitcoin, par point de % de perte en log)
| Variable | Coefficient | p | IC 95 % |
|---|---|---|---|
| Gap SPY | **−0,1077** | 0,0001 | [−0,163 ; −0,052] |
| Séance SPY | −0,0091 | 0,51 | [−0,036 ; 0,018] |
| Gap QQQ | **−0,1252** | < 0,0001 | [−0,180 ; −0,070] |
| Séance QQQ | −0,0053 | 0,75 | [−0,039 ; 0,028] |
| Variation du VIX (points) | **+0,2467** | 0,0029 | [0,084 ; 0,409] |
| Variation du SKEW | −0,0472 | 0,34 | ns |

- Coefficients des **gains** Bitcoin sur le gap : +0,031 (SPY) et +0,049 (QQQ). Le test d'égalité des sensibilités hausse/baisse donne p = 0,028 et 0,030 : **réaction plus forte aux baisses**.
- Les associations gap et VIX survivent à la correction de Benjamini-Hochberg sur 8 tests (mais pas à l'ensemble des spécifications explorées, précise l'auteur).
- **Événements** (non testés formellement) : 211 séances après une baisse nocturne du Bitcoin d'au moins 3 % → gap SPY moyen **−0,453 %** et séance **+0,094 %**, contre +0,086 % et +0,006 % les autres jours.

### Probabilité de baisse et queue de distribution
- Modèle de probabilité linéaire (Table 2) : 1 point de perte Bitcoin → probabilité d'un **gap négatif** +3,085 points (SPY) et +3,469 points (QQQ), significatif. Pour la **séance** : +0,289 point (SPY, p = 0,61) et +0,025 (QQQ, p = 0,96), **rien**. Quelques probabilités ajustées sortent de [0, 1] (5 pour SPY, 7 pour QQQ) : à lire comme des associations locales.
- Régression quantile du **10e percentile** de la séance (Table 3, bootstrap par blocs de 5 séances, 499 tirages) : SPY −0,0171 [−0,047 ; 0,017], QQQ −0,0040 [−0,045 ; 0,038]. **Non significatif.**

### Stabilité et prévision (Table 4, SPY)
| Période | Pente du gap | p | Pente de la séance | p |
|---|---|---|---|---|
| 2018–2019 | −0,0025 | 0,85 | −0,0123 | 0,48 |
| 2020–2022 | −0,1536 | 0,0005 | −0,0174 | 0,46 |
| 2023–2026 | **−0,1700** | < 0,0001 | **+0,0315** | 0,040 |
| Sans mars 2020 | −0,0710 | < 0,0001 | +0,0025 | 0,82 |

- La relation avec le gap est **faible en 2018–2019** et forte ensuite. En 2023–2026, la séance a un coefficient **positif** (p = 0,04) : signe de **retournement intraday** après une baisse du Bitcoin, mais non corrigé pour les tests multiples.
- Bitstamp donne le même schéma. En contrôlant le gap d'ouverture (information disponible à l'ouverture), la perte Bitcoin reste non significative pour la séance.
- Prévisions hors échantillon à fenêtre croissante, évaluées de janvier 2023 à octobre 2026 (943 séances) : R² hors échantillon **−0,101 % (SPY)** et **−0,194 % (QQQ)**. Ajouter le Bitcoin **dégrade** légèrement la prévision de la séance.

### Limites reconnues par l'auteur
- Les fenêtres de nuit se chevauchent : aucune interprétation causale ni de « leadership » informationnel.
- **Les futures ES/NQ n'ont pas été utilisés.** Comme ils cotent pendant la fermeture, l'auteur ne peut pas dire si le Bitcoin apporte quelque chose de plus que les futures. Il propose (sans l'estimer) un modèle qui contrôlerait les mouvements des futures sur la même fenêtre.
- Les extensions (probabilité, quantile) ont été choisies après avoir vu les premiers résultats.

### À retenir pour nous (strictement d'après le papier)
- Une baisse nocturne du Bitcoin coïncide avec un **gap baissier** du SPY/QQQ (environ −0,11 à −0,13 point par point de perte) mais **ne prédit pas la séance qui suit** sur l'ensemble de l'échantillon ; sur 2023–2026, le signe est même positif (retournement).
- Aucun contrôle par les futures ES/NQ : on ne sait pas si l'information est nouvelle par rapport à ce que les futures montrent déjà.

---

## [14] Lovers by Night, Strangers by Day? An Investigation of Simple Overnight Trading Strategies — Chrilly Donninger

**Référence :** Sibyl Working Paper, septembre 2014, SSRN 2495490. Auteur : Chief Scientist du Sibyl-Project (godotfinance.com). Note de praticien de 5 pages, sans tests statistiques formels.

### Question
L'affirmation de Cliff, Cooper et Gulen (2008) et de Dutta et Sharma (2012) — l'essentiel du gain des indices se fait la nuit, avec moins de volatilité — tient-elle encore, et peut-on l'exploiter avec une stratégie réaliste ?

### Données
- Futures **E-mini S&P 500 (ES)** et **E-mini Nasdaq-100 (NQ)**, **7 septembre 2010 – 9 septembre 2014** (4 ans). Séance = 9:30–16:00 ; nuit = 16:00 → 9:30.
- Rappel de Dutta et Sharma (données 2004–2005) : ES séance 0,015 % / nuit 0,026 % ; NQ séance −0,008 % / nuit 0,071 % ; variance de nuit plus faible, skewness de nuit positive.

### Résultats descriptifs (2010–2014)
- **ES** : rendement moyen **0,029 % en séance contre 0,031 % la nuit**, presque égal. Distribution de nuit plus resserrée et moins asymétrique à gauche, mais encore à skewness négative.
- **NQ** : **0,023 % en séance contre 0,055 % la nuit**. Variance plus faible la nuit, skewness à peu près identique.
- **IVTS** = VIX / VXV (volatilité implicite 1 mois / 3 mois), mesurée à **16:00**. IVTS ≤ 0,93 = marché haussier calme ; IVTS > 1 = inversion de la structure (périodes de crise). Les rendements journaliers sont corrélés négativement à l'IVTS, mais **les rendements de nuit sont légèrement corrélés positivement** (Pearson **0,057**, pente positive en MCO et en Theil-Sen), pour l'ES comme pour le NQ. **« Les rendements de nuit sont positivement corrélés aux turbulences de marché. »**

### Stratégie testée
- **Achat de l'ES à 16:00**, détention la nuit, seulement si **IVTS > 0,87** (on évite les marchés très calmes) et **pas le vendredi** (effet week-end).
- **Sortie** : si le rendement de nuit est négatif à l'ouverture, vente à **9:30** ; s'il est positif, on garde **jusqu'à 9:33** (continuation du momentum de nuit juste après l'ouverture, d'après ses travaux précédents et Grant, Wolf et Yu). Couper une position perdante avant 9:30 n'améliore pas le résultat.
- Capital initial 500 000 $, 1 contrat par tranche de 30 000 $.
- **Sans coûts** :
  - ES : gain total **143,2 %** contre **97,3 %** pour le SPY ; Sharpe **1,153** contre 1,011 ; drawdown max **14,7 %** (26/09/2011) contre 18,6 %.
  - NQ (on trade aussi le vendredi : pas d'effet week-end négatif sur la période) : **208,0 %** contre **126,7 %** pour le QQQ ; Sharpe **1,224** contre 1,051 ; drawdown 14,1 % contre 16,1 %.
- **Avec coûts** :
  - ES : **12,5 $ par contrat et par trade** (1 tick, soit le spread ; frais de courtage ignorés), 25 $ l'aller-retour : la performance disparaît, **le buy & hold du SPY est meilleur à tous égards**.
  - NQ : 1 tick = 5 $ ; hypothèse jugée réaliste de **7,5 $ par trade (15 $ l'aller-retour)** : stratégie et buy & hold du QQQ **à peu près équivalents** (Sharpe 1,072 contre 1,051).
- Relever le seuil d'IVTS (ne trader que les régimes plus volatils) **fait baisser le Sharpe** (mois sans trade, courbe en escalier).

### Conclusion de l'auteur
- L'effet existe encore mais **moins fort** que dans la littérature ancienne. Il marche sans coûts, mais il est très difficile pour un trader ordinaire de couvrir des coûts réalistes. Le **NQ est plus prometteur que l'ES**.
- Conseil pratique : **ouvrir les positions en fin de séance et les fermer le matin**. Piste évoquée : une stratégie de moyen terme qui garde les futures tant que certains critères sont remplis.

### À retenir pour nous (strictement d'après le papier)
- Sur 2010–2014 : ES nuit ≈ séance ; NQ nuit > séance.
- Le rendement de nuit est **légèrement plus élevé quand la structure de la volatilité implicite est tendue** (IVTS élevé à 16:00).
- Après 1 tick de coût par trade, la stratégie de nuit sur l'ES **perd contre le buy & hold** ; sur le NQ, elle fait **jeu égal**.

---

## [15] Market Sentiment and an Overnight Anomaly — Radovan Vojtko, Daniela Hanicová

**Référence :** Quantpedia (CEO et analyste quantitative), SSRN 3829582. Pas de date sur le PDF ; les références sont datées de mars 2021. Note de recherche courte, sans tests statistiques.

### Question
Peut-on améliorer le rendement de nuit du SPY en le filtrant par un indicateur de sentiment ? Les auteurs précisent que **leur but n'est pas de construire un système de trading** mais d'analyser le comportement du marché.

### Données
- **SPY, janvier 2018 – janvier 2021** (3 ans, avec deux marchés baissiers : décembre 2018 et mars 2020). OHLC du SPY pour calculer nuit (clôture → ouverture) et séance (ouverture → clôture).
- Trois indicateurs : **clôture du SPY**, **clôture du VIX**, **Brain Market Sentiment (BMS)** — score de 0 à 100 tiré par traitement automatique du langage de milliers d'articles financiers (part de sujets positifs du jour).

### Rendements de base (SPY, 2018 – janvier 2021)
| | Rendement (p.a.) | Volatilité (p.a.) | Sharpe | Drawdown max | CAR / MaxDD |
|---|---|---|---|---|---|
| Journalier | 15,25 % | 23,27 % | 0,66 | −34,10 % | 0,45 |
| Séance | −0,44 % | 15,02 % | −0,03 | −22,41 % | −0,02 |
| **Nuit** | **13,62 %** | 16,24 % | **0,84** | −29,41 % | 0,46 |

(La colonne est intitulée « 3Y cumulative return » dans le tableau mais le texte parle de rendement annuel.)

### Règle testée
- **À la clôture de t−1**, on compare le SPY, le VIX et le BMS à leur moyenne mobile sur 10, 20 ou 50 jours. On regarde le rendement **de nuit** du jour t selon la position par rapport à la moyenne.
- Hypothèses : nuit meilleure si **SPY > MM**, si **VIX < MM**, si **BMS > MM**.

### Résultats (moyenne mobile 20 jours, sans coûts)
| Signal | Rendement (p.a.) | Volatilité | Sharpe |
|---|---|---|---|
| Aucun | 13,62 % | 16,24 % | 0,84 |
| **SPY > MM20** | 15,52 % (texte) / 15,62 % (tableau) | 8,14 % | **1,92** |
| **VIX < MM20** | 15,70 % | 8,72 % | 1,80 |
| **BMS > MM20** | 15,07 % | 8,84 % | 1,71 |

- Drawdowns maximaux des trois versions filtrées : environ −5,3 % à −6,8 % (contre −29,4 % sans filtre).
- Les courbes des trois signaux sont corrélées à un peu moins de 0,6 en moyenne : chaque indicateur apporterait une information en partie différente.
- **Portefeuille équipondéré des trois signaux** :

| Moyenne mobile | Rendement (p.a.) | Volatilité | Sharpe | Drawdown max |
|---|---|---|---|---|
| 10 jours | 14,02 % | 7,77 % | 1,80 | −5,28 % |
| **20 jours** | **15,58 %** | 7,33 % | **2,12** | −3,98 % |
| 50 jours | 11,97 % | 6,74 % | 1,78 | −3,21 % |

- **Filtre supplémentaire** « nuit précédente négative » : la performance **s'améliore quand la nuit précédente est négative** (SPY > MM et nuit précédente < 0 : 11,75 %, Sharpe 2,00). Mais combiné au portefeuille équipondéré, il n'apporte rien (Sharpe 2,10 contre 2,12) ; les auteurs **déconseillent** ce filtre (complexe, peu de valeur ajoutée). Le premier tableau de ce filtre contient une valeur incohérente (Sharpe 0,20 pour la ligne équipondérée, 2,10 dans le tableau suivant).

### Conclusion des auteurs
- Confirme que la nuit domine la séance sur le SPY, et que le résultat est meilleur avec le bon filtre de sentiment.
- **Aucun coût de transaction** n'a été inclus ; ils seraient **très élevés** vu la fréquence. Usage recommandé : en **surcouche** pour décider de décaler un ordre de la clôture à l'ouverture suivante (ou l'inverse) selon le signal.

### À retenir pour nous (strictement d'après le papier)
- Trois ans seulement (2018–2021), aucun test de significativité, aucun coût.
- Le filtre qui marche le mieux seul est **SPY au-dessus de sa moyenne mobile 20 jours** à la clôture (tendance courte haussière), puis **VIX sous sa MM20**.

---

## [17] Is Overnight Volatility Overlooked? — Zehua Zhang, Ran Zhao

**Référence :** SSRN 3574323 (pas de date sur le PDF ; échantillon jusqu'au 1er juillet 2020). McMaster University et Claremont Graduate University.

### Question
La volatilité de nuit des indices US est-elle du bruit, ou un processus à part entière utile pour prévoir la volatilité de la séance (et inversement) ? Les auteurs mesurent la volatilité réalisée de nuit grâce aux **futures E-mini**, qui cotent presque 24 h/24.

### Problème des ouvertures d'indices
- Les fournisseurs du S&P 500 et du DJIA fixent souvent l'ouverture **égale à la clôture de la veille** : le rendement de nuit de l'indice paraît nul (surtout avant 2016), alors que celui du Nasdaq-100 et des composants ne l'est pas. Ahoniemi et Lanne (2013) utilisaient le prix de 9:35.
- Les auteurs utilisent donc les **ETF SPY et QQQ** (prix à 5 minutes, base Kibot) : ouverture = prix à 9:30, clôture = prix à 16:00 (calendrier NYSE, clôtures anticipées comprises). L'ETF intègre la découverte de prix de la pré-ouverture (l'enchère d'ouverture NYSE commence à 4:00).
- Une note précise qu'utiliser les rendements de nuit calculés sur l'ouverture et la clôture de l'**indice** donne de mauvaises prévisions.

### Données de volatilité
- **Futures E-mini S&P 500 et Nasdaq-100, prix à 5 minutes** (Kibot), **29 octobre 2009 – 1er juillet 2020** (2 560 observations journalières selon le texte ; la section HAR mentionne un total de 2 686).
- Horaires CME (au moment de l'étude) : du dimanche 18:00 au vendredi 18:00 ET ; pause 16:15–16:30 ; maintenance 17:00–18:00 du lundi au jeudi.
- **Volatilité réalisée de nuit RV_N** : rendements à 5 minutes de **18:00 la veille à 9:30**. **RV de séance RV_D** : 9:30–16:00 (calculée sur les futures, quasi identique à celle de l'ETF). RV journalière = RV_N + RV_D.
- Variation bipuissance et sauts filtrés (test au seuil de 99 %).

### Faits établis
- **Rendements** (Table 1, en %, 2009–2020) :

| | SPY jour complet | SPY nuit | SPY séance | QQQ jour complet | QQQ nuit | QQQ séance |
|---|---|---|---|---|---|---|
| Moyenne | 0,0486 | **0,0268** | 0,0218 | 0,0711 | **0,0478** | 0,0233 |
| Variance | 1,1361 | 0,5104 | 0,5663 | 1,4369 | 0,5753 | 0,7967 |
| Skewness | −0,71 | **−2,56** | −0,54 | −0,57 | **−2,19** | −0,45 |
| Kurtosis | 14,03 | **44,93** | 5,91 | 9,19 | **34,21** | — |

- La nuit a une moyenne plus élevée et une volatilité plus faible (meilleur Sharpe). **La variance de nuit représente 45 % (SPY) et 40 % (QQQ) de la variance journalière** : « plus de 40 % de la volatilité quotidienne est de nuit ».
- La corrélation entre les **rendements** de nuit et de séance est proche de zéro.
- **Volatilités réalisées S&P 500** (Table 2) : RV moyenne journalière 1,1576, nuit 0,4872, séance 0,6704. **Corrélation RV de nuit → RV de séance suivante : 0,7583.** Donc pas parfaite : réduire la RV journalière à la RV de séance mise à l'échelle suppose à tort une corrélation de 1.
- La RV de nuit montre du regroupement de volatilité comme la séance ; le carré du rendement de nuit est un estimateur très bruité. **Les sauts arrivent surtout en dehors de la séance.** En mars 2020, les futures ont atteint leur limite de baisse de nuit (5 %) avant l'ouverture du NYSE.

### Prévision de la volatilité (modèles HAR, log RV)
- **RV de séance** (Table 3, S&P 500), comparée au HAR-RV de base :
  - + rendements de séance positifs/négatifs de la veille : log Bayes factor 58,73.
  - + volatilité implicite (VIX ; VXN pour QQQ) : −13,2 % d'erreur quadratique de prévision (FMSE).
  - **+ RV de nuit : −16,9 % de FMSE** (QQQ : −14,6 %).
  - + RV de nuit et rendements de nuit : −21,67 %.
  - **Meilleur modèle (avec rendements de nuit et volatilité implicite) : −27,81 %** (QQQ : −27,7 %).
  - Le rendement de nuit est corrélé **négativement** à la RV de la séance suivante (effet de levier) ; les rendements de nuit positifs et négatifs ont chacun un effet.
- **RV de nuit** (Table 4) : la RV de séance de la veille apporte le plus (log Bayes factor 334,59, −22,64 % de FMSE), puis les rendements de séance positifs/négatifs (−14,47 %). La volatilité implicite est aussi utile.
- Résultats identiques pour le Nasdaq-100 (annexe).

### Modèle DN-SV-RV (volatilité stochastique jour/nuit, estimation bayésienne MCMC)
- Les volatilités latentes de jour et de nuit sont modélisées ensemble avec leurs RV. SPY : ρ_D = **0,6171** (volatilité de nuit → séance suivante), ρ_N = **0,3665** (séance → nuit suivante).
- Modélisées séparément, l'autocorrélation de chaque volatilité est d'environ 0,95 ; une fois la volatilité de l'autre période contrôlée, elle devient beaucoup plus faible : **pour prévoir la volatilité de la séance, l'information la plus récente est la volatilité de la nuit**, et inversement.
- **Moyenne ajustée de la volatilité** : la nuit n'a plus une moyenne plus élevée. μ_N = 0,0525 % (SPY) et 0,0772 % (QQQ) contre μ_D = 0,0904 % et 0,1275 %. Selon les auteurs, la volatilité stochastique pourrait expliquer les rendements de nuit élevés observés.
- Hors échantillon : SV-RV bat SV (log Bayes factor 40,82 pour la séance, 50,93 pour la nuit, SPY) ; DN-SV-RV bat SV-RV (20 et 44,11). Même résultat pour QQQ.

### RV journalière (section 5)
- Comparaison de trois mesures de la volatilité close-to-close : RV de séance seule, **RV des futures sur ~24 h**, RV de séance + carré du rendement de nuit.
- La RV de séance **sous-estime** la volatilité journalière (biais −0,4720). La RV sur 24 h a le plus faible bruit (0,2705 ; 92,9 % de sa variance expliquée par la volatilité latente) ; le carré du rendement de nuit est le plus bruité (0,4516) et donne la moins bonne prévision de densité des rendements.

### À retenir pour nous (strictement d'après le papier)
- Sur SPY/QQQ 2009–2020, **plus de 40 % de la variance journalière est de nuit**, avec des rendements de nuit très asymétriques à gauche (skewness −2,6) et à queues épaisses (kurtosis 45).
- La **volatilité réalisée de nuit (futures, 18:00 → 9:30)** est un très bon prédicteur de la volatilité de la séance qui suit (corrélation 0,76 ; −17 % d'erreur de prévision).
- Une fois la volatilité stochastique prise en compte, le rendement moyen de nuit n'est plus supérieur à celui de la séance.

---

## [18] Realized Volatility and Overnight Returns — Katja Ahoniemi, Markku Lanne

**Référence :** Bank of Finland Research Discussion Papers 19/2010, SSRN 1756705. Aalto University School of Economics et University of Helsinki.

### Question
Sur un marché qui n'est pas ouvert 24 h/24, comment intégrer le **rendement de nuit** dans le calcul de la volatilité réalisée (RV) ? Et comment mesurer ce rendement de nuit pour l'indice **S&P 500**, dont l'ouverture publiée est égale à la clôture de la veille ?

### Données
- **Indice S&P 500**, données intraday Tick Data, **1er janvier 1994 – 31 mai 2007** (3 377 jours). Fin choisie pour exclure la crise financière. Rendements à **5 minutes** (78 par séance). Pas de correction du bruit de microstructure (5 minutes jugé suffisant).
- In-sample : 1994–2004 (2 771 jours), sert à calculer le facteur d'échelle et les poids. Hors échantillon : janvier 2005 – mai 2007.

### Le problème de l'ouverture du S&P 500
- La clôture et l'ouverture consécutives de l'indice sont **identiques** avant 2006 (les valeurs non nulles sont probablement des erreurs). Cela change progressivement **en 2006**, avec le passage du NYSE au trading électronique.
- Deux mesures proposées du rendement de nuit :
  1. **Clôture → 9:35** (5 premières minutes de séance comprises). Justification : le carré moyen du rendement des 5 premières minutes est très différent des 77 autres intervalles ; les grandes valeurs mettaient 5 à 6 minutes à ouvrir en 1986 (Stoll-Whaley) et environ 3,5 minutes en 1996–2001 (Spurlin et al.). La RV de séance est alors calculée à partir de 9:35 (77 intervalles).
  2. **Clôture → SOQ (Special Opening Quote)** : valeur calculée par S&P à partir du **prix d'ouverture des 500 composants** (prix de règlement des options CBOE et CME). Sa moyenne est plus du double de celle de la mesure à 9:35.

### Estimateurs comparés
- RV de séance seule (sans nuit) ; RV **mise à l'échelle** pour couvrir 24 h (facteur 1,6380 calculé à la Hansen-Lunde) ; RV + carré du rendement de nuit (9:35 ou SOQ) ; **RV pondérée de Hansen et Lunde (2005b)** (poids optimaux sur la nuit et la séance) ; **RV « naïve » pondérée** proposée par les auteurs (poids proportionnels aux moyennes).
- Poids HL avec la mesure 9:35 : deux fois plus de poids sur la séance que sur la nuit. Avec la SOQ, le poids de la nuit devient très faible (rapport 39,4), alors que les poids naïfs augmentent celui de la nuit.

### Résultats
- **Test de Patton (2009) / Model Confidence Set**, perte quadratique, carré du rendement journalier suivant comme proxy : les plus précis sont la **RV naïve 9:35 (p = 1,000)** et la **RV HL 9:35** ; la RV seule, la RV mise à l'échelle et RV + nuit 9:35 sont rejetées (p = 0,000). Pondérer la nuit et la séance est préférable, et la mesure **9:35 bat la SOQ** dans ce test.
- **Prévision** (GARCH, GJR-GARCH, APARCH ; MSE et R² de Mincer-Zarnowitz, hors échantillon 2005–2007) : selon le R², **GJR-GARCH** est le meilleur quel que soit l'estimateur ; selon le MSE, le modèle choisi (GARCH ou APARCH) **dépend de l'estimateur de RV**. Le meilleur R² est obtenu avec GJR sur la RV HL 9:35, le plus faible MSE avec APARCH sur la RV HL SOQ. Ligne par ligne, la RV HL SOQ gagne 3 fois, la RV HL 9:35 deux fois.
- **Effet de rétroaction de la volatilité** (rendement sur RV contemporaine) : avec l'estimateur courant « RV + carré du rendement de nuit », on conclurait à tort à l'absence d'effet ; il apparaît avec d'autres estimateurs. **Effet de levier** : pas de différence de significativité ; meilleur R² ajusté avec la RV HL SOQ.

### Conclusion des auteurs
- Recommandation : l'estimateur **pondéré de Hansen et Lunde (2005b)**. Deux estimateurs courants sont **déconseillés** : ignorer la nuit, et ajouter le carré du rendement de nuit comme un terme de plus.
- Pour le S&P 500, la mesure 9:35 l'emporte dans le test statistique, la SOQ dans les applications.

### À retenir pour nous (strictement d'après le papier)
- Avant 2006, **l'ouverture publiée de l'indice S&P 500 cash est égale à la clôture de la veille** : un rendement de nuit calculé sur l'indice cash est faux sur cette période. Il faut utiliser le prix à 9:35, la SOQ, ou des futures (Martens 2002 est cité comme utilisant les futures).
- Papier méthodologique sur la mesure de la volatilité ; pas de stratégie ni de rendement moyen de nuit.

---

## [19] Making Money While You Sleep? Anomalies in International Day and Night Returns — Kevin Aretz, Söhnke M. Bartram

**Référence :** SSRN 2670841 (pas de date sur le PDF ; il cite Lou et al. 2015 comme travail contemporain). Manchester Business School et Warwick Business School.

*Note de lecture : le tableau par pays (Table 1, panel B) est mal aligné à l'extraction du PDF (colonnes décalées) ; je ne reprends donc pas les chiffres pays par pays, seulement ce que dit le texte.*

### Question
Sur un échantillon international, les rendements et les primes des anomalies classiques se forment-ils pendant la séance (« jour ») ou pendant la fermeture (« nuit ») ?

### Données
- **48 413 actions de 35 pays** (dont les US), **janvier 1993 – janvier 2012** (début en 1993 car les prix d'ouverture n'existent pas avant dans les bases).
- US : CRSP et Compustat (NYSE, Amex, Nasdaq ; prix du mois précédent ≥ 2 $). Hors US : Datastream (prix en dollars) et WorldScope. Financières (SIC 6000–6999) et fonds propres négatifs exclus.
- Rendement de jour = (clôture + dividende) / ouverture − 1, avec des **prix de transaction**. Rendement de nuit déduit du total. Winsorisation à 0,1 % / 99,9 %.
- Filtres hors US : suppression des renversements extrêmes (jour ou nuit > 100 % avec total < 10 % ; idem sur deux jours), titres non traités plus de 30 % des jours, erreurs évidentes (ouverture et clôture dans des devises différentes). Pays avec moins de 30 titres ou moins de 8 ans exclus. **Grèce, Pakistan et Suède exclus** car leurs ouvertures sont souvent identiques aux clôtures.
- Robustesse US : ouverture **TAQ** = premier trade de taille positive après 9:45 (le texte de la section données dit « après 9 am ») ; on garde les observations où l'écart avec l'ouverture CRSP est < 10 % de la clôture. Résultats « virtuellement identiques ».

### Résultat 1 : le jour rapporte plus que la nuit (au global)
- Moyenne des pays : rendement total **12,3 %/an** (vol 13,8 %) ; **jour 10,50 %/an** (vol 8,21 %) ; **nuit 5,43 %/an** (vol 8,16 %). Écart d'environ 5 points, **significatif (p = 0,01)** ; volatilités indiscernables.
- **Par jour de la semaine** : les rendements de nuit varient peu ; les rendements **de jour sont négatifs en début de semaine et positifs en fin de semaine**, donc l'écart jour − nuit est négatif et très significatif en début de semaine, positif et très significatif en fin de semaine.
- Le jour l'emporte dans la plupart des mois et dans la première moitié de l'échantillon, sans que ce soit toujours significatif.
- **US** : le jour est plus volatil que la nuit (conforme à la littérature) **et rapporte plus** que la nuit (ce qui contredit Rogalski, Harris, Smirlock-Starks mais aussi Cliff-Cooper-Gulen cité en introduction).
- **Entre pays** : à peu près autant de pays où le jour bat la nuit que l'inverse ; l'écart n'est pas expliqué par le niveau de développement (positif et significatif à 10 % pour les pays développés comme pour les pays émergents).
- Les courbes cumulées ne sont pas des stratégies réalistes (elles supposeraient 200 % de rotation par jour).

### Résultat 2 : les anomalies se forment le jour et s'inversent la nuit
- Huit stratégies en quintiles (seuils calculés **par pays et par mois**), équipondérées ou pondérées par la capitalisation, rebalancement mensuel : **taille, book-to-market, momentum (12 mois sauf le dernier), retournement de long terme (36 mois sauf les 12 derniers), accruals, émissions nettes d'actions, croissance des actifs, rentabilité**. Variables comptables à la Fama-French (2008), mises à jour en juin.
- Toutes ont un rendement total positif et significatif (momentum et value les plus forts). **Leurs primes sont fortement positives le jour et généralement négatives la nuit.** Exception : accruals (petit et positif dans les deux).
- Le schéma vaut pays par pays (Figure 2), avec des ampleurs variables (momentum, taille et rentabilité grands dans certains pays ; accruals, croissance des actifs, émissions dix fois plus petits).
- **Momentum US** : comme chez Lou et al., il se fait **la nuit** (grand et positif) et est petit et négatif le jour. Mais **les US sont l'exception** : hors US, le momentum se fait le jour. Les autres stratégies US se forment surtout le jour.
- **Fama-MacBeth** (rendement du mois suivant) : sur le total, BM, momentum et rentabilité positifs ; taille, accruals, émissions et croissance des actifs négatifs. Ces relations viennent du **jour** ; les coefficients de **nuit sont de signe opposé**. Résultat valable pour les US et hors US séparément, et pour les 8 grands pays hors US (Australie, Canada, France, Allemagne, Hong Kong, Italie, Japon, Royaume-Uni), sauf la taille en Australie, le momentum à Hong Kong et la croissance des actifs au Japon.

### Explications théoriques rappelées (non testées)
- Les modèles prédisent soit plus soit moins de rendement pendant la séance : prime pour porter un actif qu'on ne peut pas liquider pendant la fermeture (Longstaff 1995), report du risque sur la réouverture (Slezak 1994), baisse des prix avant la clôture quand on réduit les couvertures puis hausse à la réouverture quand l'asymétrie d'information diminue (Hong-Wang 2000). L'attention des particuliers à l'ouverture (Berkman et al.) est citée pour le résultat de Cliff et al.

### À retenir pour nous (strictement d'après le papier)
- Contrairement à l'idée répandue, **au niveau international et sur 1993–2012, le rendement moyen des actions est plus élevé le jour que la nuit** ; c'est très variable selon les pays.
- Le rendement de jour dépend fortement du **jour de la semaine** (négatif en début de semaine, positif en fin de semaine) ; celui de la nuit beaucoup moins.
- Papier sur actions individuelles, sans coûts.

---

## [20] Risk and Return Around the Clock — Felix Fattinger, Alexandre Ziegler

**Référence :** SSRN 2606706 (pas de date sur le PDF ; échantillon avril 2010 – août 2013). Université de Zurich.

*Note de lecture : les tableaux 2 à 5 (volume, contribution au prix, contribution à la variance par période) sont mal alignés à l'extraction ; je ne reprends que les chiffres cités dans le texte.*

### Question
Sur 24 h, **quand se fait la découverte des prix** (rendement et risque) pour des actifs de toutes les classes, et est-elle efficiente ? Premier papier à le faire de façon unifiée sur des **futures** cotés presque en continu.

### Données
- **13 futures**, prix à 5 minutes (TickData), **10 avril 2010** (début de la cotation 24 h du Nikkei) – **30 août 2013** :
  - Actions : **E-mini S&P 500 (ES)**, EuroStoxx 50 (XX), Nikkei (NK, contrat CME).
  - Obligations : T-Note 10 ans (TY), Bund 10 ans (BN), JGB 10 ans (JB).
  - Devises : **EUR/USD (EC), JPY/USD (JY)**.
  - Pétrole : **WTI (CL), Brent (CO)**.
  - Métaux : **or (GC)**, argent (SV), cuivre (HG).
- Contrat front, roll quand le suivant devient plus liquide (environ une semaine avant la dernière date de trading). Or : seulement les échéances G, J, M, Q, V, Z, roll **35 jours calendaires** avant l'échéance (le volume chute avant la first notice date). Argent et cuivre : H, K, N, U, Z, roll 35 jours avant.
- Toutes les heures en **CET**. **Jours où les US sont en heure d'été mais pas l'Europe supprimés** (environ 4 semaines par an). Ajustement de l'heure d'été pour le Japon.
- 9 contrats cotent 23 h ou plus par jour ; Brent 22 h ; EuroStoxx et Bund 14 h ; JGB 13 h 44. Volume moyen : de ~10 000 contrats/jour (Nikkei CME) à ~1,93 million (ES).
- Rendement de réouverture (clôture → ouverture et après les pauses) attribué à l'intervalle qui se termine à l'ouverture : la somme des rendements est exactement celle d'une position long roulée.
- **Découpage de la journée (CET)** : 00:00–01:00 (fermé sauf devises, annonces japonaises) ; 01:00–08:00 (heures Japon) ; 08:00–09:00 (pré-marché européen) ; 09:00–13:00 (Europe ouverte, annonces européennes) ; 13:00–15:30 (Europe ouverte, US fermés, **principales annonces macro US**) ; 15:30–17:30 (Europe et US ouverts) ; 17:30–22:00 (US seuls) ; 22:00–00:00 (tout fermé sauf devises).

### Résultats sur le volume et la découverte de prix
- Environ **25 % du volume de l'ES** se traite hors des heures d'ouverture des bourses US ; plus de **30 % du volume du Brent** après la clôture européenne ; plus de 85 % du volume du JGB entre 01:00 et 08:00 CET. Volume en heures asiatiques faible pour le pétrole, important pour les métaux.
- **Contribution au prix** (part du rendement journalier réalisée dans chaque période) : **plus de la moitié du rendement du S&P 500 et de l'EuroStoxx**, et presque la moitié de celui du Nikkei, se fait **quand leur marché cash est fermé**.
- Rapportée au volume, la contribution au prix est **plus élevée hors des heures principales** : le S&P 500 a une forte contribution par unité de volume pendant les **heures européennes**, l'EuroStoxx pendant le pré-marché européen, le Nikkei pendant le pré-marché japonais, les obligations US et japonaises pendant le pré-marché US, l'euro pendant les heures asiatiques et le pré-marché européen, le Brent pendant les heures japonaises et le pré-marché US, le WTI pendant les heures européennes.
- **Contribution à la variance** : près de **50 % de la variance du S&P 500** et environ **60 % de celle du Nikkei** ont lieu hors des heures de leur marché cash. Les métaux varient beaucoup toute la journée.
- **Rendement et risque arrivent en même temps** pour un actif donné : « il n'est pas vrai que le rendement s'accumule le matin et le risque l'après-midi ». Quelques écarts persistants : pour le S&P 500 (pendant les heures US) et le WTI, la variance précède le rendement ; c'est l'inverse pour le yen (heures européennes) et l'argent.
- Faits marquants :
  - **S&P 500 : contribution au prix quasi nulle jusqu'à l'ouverture européenne.** Idem pour l'or et le cuivre (malgré la Chine et l'Inde, principaux consommateurs).
  - **Argent** : contribution au prix importante pendant les heures asiatiques.
  - **Pétrole** : contribution quasi nulle (Brent) ou négative non significative (WTI) jusqu'à l'ouverture européenne ; la découverte de prix se fait **plus tôt pour le Brent que pour le WTI**, et elle est essentiellement terminée à la clôture européenne (comme pour les devises).
  - Le yen « découvre » son prix plus tôt dans la journée que l'euro.

### Efficience de la découverte de prix
- Régressions d'« absence de biais » du rendement journalier sur le rendement cumulé jusqu'à chaque instant (Biais-Hillion-Spatt, Barclay-Hendershott) : la plupart des pentes ne sont pas différentes de 1 → découverte de prix **efficiente presque partout**.
- **Inefficiences** concentrées **avant l'ouverture asiatique et pendant les premières heures de trading asiatique** : JGB vers 2:00, yen jusqu'aux heures principales japonaises, T-Note, euro, or, argent et WTI pendant les 2 à 5 premières heures de cotation.
- L'efficience est plus forte pendant les heures principales de chaque actif. S&P 500 : faible au début des heures asiatiques, en hausse pendant les heures européennes, maximale en heures US. T-Note : faible jusqu'aux annonces de 14:30 CET, chute à la fermeture de la corbeille (21:00). Euro : faible jusqu'au début d'après-midi, forte après les annonces US. Métaux : faible les 3–4 premières heures et chute entre la clôture asiatique et l'ouverture européenne. **Pétrole : faible jusqu'à environ 11:00 CET, forte ensuite** (déclin plus tôt le soir pour le Brent).
- La découverte de prix est la plus rapide, pour les actifs européens, quand l'Europe et les US sont ouverts ensemble.

### Profils de volatilité intraday
- **Pas de courbe en U pour la plupart des actifs**, même sur les seules heures de marché. Le **S&P 500** est le seul à avoir un U net, et seulement pendant les heures du marché cash US.
- Les pics de volatilité arrivent à quatre types d'heures : ouverture/fermeture du marché de l'actif ; ouverture/fermeture de la corbeille du future ; ouverture/fermeture **d'autres marchés** ; **annonces macro** (US en trois vagues : 14:30, 16:00 et 20:00–20:45 CET).
- S&P 500 : volatilité très faible en heures asiatiques, petite hausse à 8:00, forte hausse à **9:00 (ouverture européenne)**, pics à 14:30, à **15:30 (ouverture US)**, à 16:00 et 20:00–20:45, chute à la clôture du cash.
- Pétrole : faible en heures asiatiques, forte hausse à l'ouverture européenne, pics à 14:30, à l'ouverture de la corbeille WTI (15:00), à l'ouverture US (15:30), à 16:00, aux **stocks de pétrole US à 16:30**, et à la clôture de la corbeille WTI (20:30). Le Brent est plus volatil que le WTI en début de journée (pic à 2:00 = ouverture du Brent en semaine) ; le WTI plus volatil une fois les US ouverts.
- Métaux : profils les plus erratiques ; pics à l'ouverture japonaise, aux annonces de 14:30 et 16:00, aux **clôtures de corbeille** (19:25 argent, 19:30 or, 19:00 cuivre), à 20:00 (Fed), à la clôture des actions US (22:00).
- Devises : yen plus volatil que l'euro en heures asiatiques, l'inverse en heures européennes ; pics à 14:30 et 16:00.

### Sauts
- Décomposition diffusion / sauts par intervalle de 5 minutes (MedRV d'Andersen-Dobrev-Schaumburg et test de Lee-Mykland, fenêtre de 288 intervalles, seuil 99,9 %).
- **Les sauts représentent environ 5 à 13 % de la variance journalière totale** (le plus pour le yen et les obligations US et japonaises).
- Pour presque tous les actifs, **le plus gros saut est juste après les annonces US de 14:30 CET** (exceptions : Nikkei, et le pétrole dont le plus gros saut est aux **stocks US de 16:30**). Contribution du saut de 14:30 à la variance journalière moyenne : T-Note 4,77 %, **S&P 500 1,69 %**, Bund 1,54 %, **or 1,22 %**. Pour les actions, le 2e groupe le plus important est celui des annonces FOMC ; pour les métaux et les obligations, celui de 16:00.
- Une fois les sauts retirés, le U du S&P 500 en heures US est très net ; l'or et l'argent ont des variances de diffusion très proches, de même que WTI et Brent.

### Volume et volatilité
- Le volume dépasse nettement la volatilité pendant les heures US (sauf JGB).
- Aux sauts, le volume grimpe parfois beaucoup plus que la volatilité (Nikkei, Bund, T-Note, devises, métaux à 14:30), parfois autant (EuroStoxx, S&P 500, pétrole) : selon les auteurs, sur certains marchés les traders anticipent les gros mouvements et la profondeur baisse.
- Les ouvertures et clôtures de marchés ou de corbeilles (y compris d'**autres** actifs) créent des pics de volume bien plus grands que les pics de volatilité : par exemple le volume du Nikkei à l'ouverture US, celui du Brent à la clôture européenne.

### À retenir pour nous (strictement d'après le papier)
- Sur 2010–2013, pour l'**ES**, plus de la moitié du rendement et près de la moitié de la variance se forment hors séance US, mais **quasiment rien avant l'ouverture européenne (9:00 CET)**.
- Pour le **pétrole**, l'or et le cuivre, la découverte de prix démarre aussi à l'**ouverture européenne** ; l'argent fait exception (heures asiatiques).
- Les **premières heures de la session asiatique** sont la période la moins efficiente pour la plupart des actifs.
- Les heures-clés de volatilité (CET) : 9:00, 14:30, 15:30, 16:00, 16:30 (pétrole), clôtures de corbeille, 20:00 (Fed), 22:00.

---

## [21] Who Moves the Price? Trading-Session Return Decomposition and Cross-Session Momentum in Gold and Silver Markets — WEI Wenling

**Référence :** version d'août 2026, SSRN 7257240. CMBC Wealth Management Co. Auteur unique, papier récent non relu par des pairs.

### Question
Pour l'or et l'argent, **quelle session (Asie, Europe, US) produit la hausse cumulée**, et un momentum d'une session à la suivante est-il exploitable après coûts ? Contexte : achats massifs des banques centrales depuis 2022 et débat sur un « déplacement vers l'Est » de la formation du prix.

### Données
- **Spot XAU/USD et XAG/USD, barres horaires Stooq**, téléchargées le 10 août 2026 : **22 juillet 2024 01:00 UTC – 7 août 2026 23:00 UTC** (environ 2,04 ans, 529 jours, **1 587 sessions** par métal ; 12 138 barres pour l'or, 12 126 pour l'argent).
- L'auteur voulait des futures COMEX (Yahoo Finance) mais a été bloqué (erreurs HTTP 429), et **Dukascopy et HistData n'étaient pas accessibles** depuis son environnement ; Stooq ne remonte qu'à environ deux ans.
- Horodatage vérifié en UTC (pic de volatilité de l'or sur les barres 15:00–17:00 UTC, minimum à 23:00 et 06:00), avec une **ambiguïté de ±1 heure** (horodatage à l'ouverture ou à la clôture de la barre).
- Sur la période : or **+81 %** (log +0,591), argent **+119 %** (log +0,782). Marché haussier historique.

### Sessions (UTC, selon l'heure d'ouverture de la barre)
| Session | Fenêtre UTC | Barres |
|---|---|---|
| Asie | 00:00–08:00 | 00 à 07 (= 08:00–16:00 Pékin, 09:00–17:00 Tokyo) |
| Europe | 08:00–14:30 | 08 à 14 (Londres jusqu'avant les annonces US et l'ouverture du COMEX) |
| US + soirée | 14:30–24:00 | 15 à 23 (la soirée 21:00–24:00 se comporte comme la fin d'après-midi US) |

- Rendement de session = dernière clôture horaire de la session / dernière clôture de la session précédente − 1, enchaîné dans l'ordre (US de la veille → Asie → Europe → US). Les log-rendements s'additionnent exactement au total. Week-ends et fériés intégrés à la chaîne. Le décalage d'une heure des changements d'heure est jugé acceptable vu la largeur des fenêtres.

### Décomposition (or, Table 2)
| Session | Moyenne (bp) | Écart-type (bp) | Log cumulé | Part du total | % de sessions en hausse |
|---|---|---|---|---|---|
| **Asie** | **+8,94** | 79,3 | +0,456 | **+77,2 %** | 56,7 % |
| Europe | +4,30 | 70,2 | +0,214 | +36,2 % | 55,2 % |
| US + soirée | −1,09 | **91,0** | −0,079 | **−13,4 %** | 52,9 % |

### Décomposition (argent, Table 3)
| Session | Moyenne (bp) | Écart-type (bp) | Log cumulé | Part du total | % de sessions en hausse |
|---|---|---|---|---|---|
| **Asie** | **+10,35** | 156,9 | +0,482 | **+61,7 %** | 53,1 % |
| Europe | +7,92 | 143,7 | +0,364 | +46,6 % | 55,0 % |
| US + soirée | +0,61 | **189,8** | −0,065 | **−8,2 %** | 51,0 % |

- La session US est **la plus volatile mais retire du rendement**. La fréquence des sessions en hausse est proche partout (51–57 %) : l'asymétrie vient de la **taille** des mouvements. Selon l'auteur, l'Asie a une distribution asymétrique à droite, la session US à gauche (quelques grosses baisses).

### Par année (log-rendements)
| | Or Asie | Or Europe | Or US | Argent Asie | Argent Europe | Argent US |
|---|---|---|---|---|---|---|
| 2024 (S2) | +0,074 | +0,067 | −0,054 | +0,011 | +0,063 | −0,081 |
| 2025 | +0,268 | +0,087 | +0,144 | +0,292 | +0,176 | **+0,440** |
| 2026 (à août) | +0,114 | +0,061 | **−0,169** | +0,179 | +0,126 | **−0,423** |

- Asie **positive chaque année**. En 2025 (accélération de la hausse), la session US contribue aussi positivement. **La correction de 2026 vient presque entièrement de la session US**, pendant que l'Asie continue d'accumuler.

### Autocorrélation
- Autocorrélation lag-1 des rendements de session : +0,02 (or) et +0,05 (argent) globalement, mais **+0,13 (or) et +0,12 (argent) pour la continuation vers la session asiatique** ; proche de zéro ou négative vers l'Europe et les US. L'auteur précise qu'un +0,13 sur ~529 observations n'est que **marginalement significatif**, et que les tests ne sont pas corrigés pour le nombre de variantes.

### Stratégies (signe de la session précédente ; coût 0,02 % par changement de position)
**Or (Table 6)** :
| Stratégie | Rendement annuel | Vol | Sharpe | Drawdown max |
|---|---|---|---|---|
| Buy & hold | 33,6 % | 22,5 % | 1,40 | −28,5 % |
| Toutes sessions, long-short, brut | 37,1 % | 22,5 % | 1,51 | −11,8 % |
| Toutes sessions, long-short, net | 17,4 % | 22,5 % | 0,82 | −15,0 % |
| Toutes sessions, long-only, brut | 37,4 % | 14,9 % | 2,20 | −14,0 % |
| **Toutes sessions, long-only, net** | **27,2 %** | 15,0 % | **1,68** | **−15,7 %** |
| Asie seule, long-only, net | 11,8 % | 8,4 % | 1,37 | −9,3 % |
| Europe seule, long-only, net | 4,7 % | 6,8 % | 0,71 | −5,3 % |
| US seule, long-only, net | −1,0 % | 10,3 % | −0,04 | −12,7 % |

**Argent (Table 7)** :
| Stratégie | Rendement annuel | Vol | Sharpe | Drawdown max |
|---|---|---|---|---|
| Buy & hold | 46,6 % | 45,9 % | 1,07 | −53,6 % |
| Toutes sessions, long-short, net | −11,6 % | 45,9 % | −0,04 | −50,2 % |
| **Toutes sessions, long-only, net** | **22,1 %** | 28,7 % | **0,84** | **−26,2 %** |
| Asie seule, long-only, net | 11,8 % | 15,5 % | 0,79 | −15,2 % |
| US seule, long-short, net | −19,0 % | 30,5 % | −0,54 | −47,0 % |

- Règle long-only : être long à la session suivante si la session qui vient de finir est positive, **à plat sinon**.
- Le long-short change de position environ **780 fois par an** : les coûts coûtent 15 à 20 points par an et le tuent. **Seul le long-only toutes sessions survit** : meilleur Sharpe que le buy & hold, drawdown environ divisé par deux, mais **rendement absolu plus faible**.
- Sharpe brut long-only par session : or Asie 2,01, Europe 1,57 ; argent Asie 1,13, Europe 1,19. **Toutes les variantes limitées à la session US perdent après coûts** ; l'auteur suggère que la session US conviendrait mieux à des règles contrariennes (non testé).

### Interprétation de l'auteur
- Achats « insensibles au prix » des banques centrales asiatiques et émergentes exécutés en heures asiatiques ; demande physique et futures chinoise. La session US traite l'information (volatilité) sans produire de rendement : « l'argent rapide vend sur les nouvelles macro en heures US, la demande patiente absorbe en heures asiatiques ».
- Le rendement d'une session n'est pas la même chose que la découverte de prix au sens de la microstructure.

### Limites reconnues par l'auteur
- **Environ deux ans seulement, entièrement dans un marché haussier historique** ; à revérifier en marché plat ou baissier.
- **Spot** et non futures COMEX ; ambiguïté de ±1 h sur l'horodatage.
- Exécution supposée aux bornes de session, coût fixe de 0,02 %, pas d'impact de marché.
- **Tout est en échantillon** : validation hors échantillon indispensable avant de trader.
- Remarques de lecture (factuelles) : plusieurs références sont indiquées par l'auteur lui-même comme « non vérifiées » ou « telles que citées » (dont un article cité par son seul identifiant PubMed), et la revue de littérature attribue à Hendershott, Livdan et Rösch (2020) l'idée que la nuit ne domine plus le jour, ce qui ne correspond pas au contenu de ce papier tel que résumé en [6] (qui porte sur la relation bêta–rendement).

### À retenir pour nous (strictement d'après le papier)
- Sur juillet 2024 – août 2026, **la hausse de l'or et de l'argent s'est faite surtout en session asiatique (00:00–08:00 UTC)** et un peu en Europe ; la session US (14:30–24:00 UTC) a été la plus volatile et **négative** en contribution.
- Règle simple testée : **rester long seulement après une session positive**, avec un effet surtout sur la continuation vers l'Asie.
- Échantillon très court et haussier : l'auteur lui-même met en garde contre toute extrapolation.

---
