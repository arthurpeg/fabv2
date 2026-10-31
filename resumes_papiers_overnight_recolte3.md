# Résumés détaillés : 3e récolte de papiers overnight (SSRN), centrée sur la session asiatique

*Rédigé le 2026-10-29 à partir de la lecture intégrale des 16 PDF fournis (texte, tableaux et annexes, extraits avec pdftotext). La numérotation [n] reprend celle de [papiers_ssrn_overnight_3_2026-10-29.md](papiers_ssrn_overnight_3_2026-10-29.md). Tout ce qui suit est extrait des papiers. Quand un tableau est mal extrait du PDF (colonnes mélangées) ou que le papier se contredit, c'est signalé. Les heures sont celles du papier (avec leur fuseau). Les rendements sont dans l'unité du papier.*

Papiers de la récolte **non fournis** (donc non résumés) : [6] Foreign Exchange Interventions, Information, and Intraday Market Dynamics: Evidence from Japan (SSRN 6832400), [18] Does Investor Time Zone Difference Affect Trading Behaviour? (SSRN 4247375).

### Index
| # | Papier | Actifs / période | En une ligne (d'après le papier) |
|---|---|---|---|
| [1] | Currency Returns in Different Time Zones (Jiang) | 13 devises vs USD, 2007–2019 | Les devises risquées montent pendant les heures US (10:00–16:00 NY) et baissent en dehors ; le yen fait l'inverse ; Sharpe EUR 0,97 brut, 0,25 après spread |
| [2] | Housewives of Tokyo vs Gnomes of Zurich (Wang, Yang) | AUD, JPY, EUR, GBP, 1996–2003 | La session asiatique fait ~31–33 % de la formation du prix de l'AUD et du JPY, 8–14 % pour EUR/GBP ; le chevauchement Londres-NY a le plus fort poids par heure |
| [3] | Does Tokyo Know More About the Yen? (Covrig, Melvin) | USD/JPY, fin 1994 – début 1995 | Avant la levée de la pause déjeuner de Tokyo, le Japon mène les cotations en fin de matinée ; en temps normal, causalité dans les deux sens |
| [4] | Currency Returns and Price Discovery around Global FX Fixings (« Karo Dr He ») | G9 vs USD, 1999–2019 | Préprint qui reprend Krohn-Mueller-Whelan : le dollar monte avant les fixings de Tokyo, BCE, Londres et baisse après (W) ; négatif après coûts pour un preneur de liquidité |
| [5] | Volatility Spillovers DM / JPY futures (Wan Mahmood) | Futures IMM et SIMEX, 1993–1996 | La volatilité va de Chicago vers Singapour, pas l'inverse |
| [7] | Overnight Price Discovery, Korean Won (Wang) | KRW/USD, 1999–2012 | La part de la nuit offshore dans la formation du prix passe de < 10 % à ~50 % ; nuit et jour négativement corrélés chaque année |
| [8] | DCC in Tokyo, London, New York Gold Markets (Lee et al.) | Or, clôtures quotidiennes, 1993–2012 | Corrélations entre places > 0,7, variables, plus fortes quand la volatilité monte (avec contradictions internes) |
| [9] | The t-0.5 Framework (Kinoshita) | Nikkei, KOSPI, Hang Seng, ASX, 2009–2024 | L'info à la clôture de New York prédit le sens du lendemain en Asie (Nikkei 67,8 % hors échantillon) ; disparaît en un jour |
| [10] | Feedback Trading Day and Night (Kusen, Rudolf) | DAX, FTSE, S&P, Nikkei 500, Hang Seng, 2007–2017 | Feedback positif surtout le jour ; très fort la nuit au Japon ; R² ~2 % |
| [11] | Is Risk Higher during Non-Trading Periods? (Riedel, Wagner) | NASDAQ, CAC, DAX, TOPIX, 1988–2010 | Volatilité de nuit < 60 % de celle du jour, mais queues de nuit plus épaisses (non expliquées par le GARCH) |
| [12] | Night Trading: Lower Risk but Higher Returns? (Lachance) | Actions US 1995–2014 + 23 pays | Le biais de nuit d'une action persiste ; long de nuit sur les titres à biais significatif : alpha 10–16 %/an après coûts |
| [13] | Overnight Returns and Firm-Specific Sentiment (Aboody et al.) | Actions US, 1992–2013 | Le rendement de nuit persiste 4 semaines et se retourne sur 12 mois (7,4 %/an long-short) |
| [14] | Cross-Section of Intraday and Overnight Returns (Bogousslavsky) | Actions US, 1986–2015 | Les anomalies de mispricing gagnent dans la journée mais perdent dans la dernière demi-heure (−2,43 pb), plus le vendredi |
| [15] | Intraday Market Making with Overnight Inventory Costs (Adrian et al.) | Treasury 10 ans BrokerTec, 2013–2018 | Spread et impact prix montent à l'approche de la clôture (17:30 NY), ~3 fois plus le vendredi |
| [16] | Overnight Public Information and Pre-Opening (Moshirian et al.) | ASX 100, 2005–2006 | La pré-ouverture intègre les nouvelles de nuit et le NYSE de la veille ; prix indicatif efficient seulement dans les 10 dernières minutes |
| [17] | Effective Extension of Trading Hours (Miwa) | Simulation multi-agents | Seul un pré-marché court améliore la séance ; l'after-hours dégrade l'ouverture si peu de participants |

### Ce qui revient d'un papier à l'autre (constaté dans les papiers, sans extrapolation)
- **FX, la nuit des US (session asiatique + matin européen)** : les devises risquées baissent contre dollar hors heures US et montent pendant les heures US, le yen fait l'inverse ([1]) ; autour des fixings, le dollar monte avant Tokyo (18:30–20:55 ET) et baisse après (20:55–2:00 ET), puis monte avant la BCE et baisse après Londres ([4]) ; la session asiatique pèse surtout sur le prix de l'AUD et du JPY ([2]), et plus pendant certains régimes particuliers ([3]).
- **Coûts** : là où les auteurs calculent les coûts, l'effet brut fond fortement : Sharpe EUR de 0,97 à 0,25 ([1]) ; retournement autour des fixings négatif pour un preneur de liquidité ([4]) ; dégradation de fin de journée inférieure au spread ([14]) ; seule [12] reste positive après coûts (actions US via les enchères d'ouverture/clôture).
- **Fin de séance et nuit** : les intermédiaires réduisent leurs positions avant la nuit → spreads et impact prix plus forts à la clôture ([15]), dégradation des anomalies en dernière demi-heure ([14]), effet plus fort le **vendredi** dans les deux papiers.
- **Queues de la nuit** : volatilité plus faible mais queues plus épaisses la nuit ([11]) ; kurtosis de nuit très élevée aussi dans [10].
- **Asie après New York** : l'information de New York se retrouve dans le premier rendement asiatique ([9], [16] avec le NYSE de la veille pour l'Australie, [10] corrélation jour US → nuit Hong Kong 0,656) et disparaît vite ([9] : rien à h = 2).
- **Persistance de la nuit en coupe (actions)** : rendements de nuit persistants pour une même action ([12] sur des années, [13] sur des semaines), avec retournement à long terme dans [13] et retournement intraday dans les deux.
- **Mesure de l'ouverture** : le prix d'ouverture des indices peut être périmé ([12]) ; les cotations des premières minutes sont souvent aberrantes ([14], qui commence à 9:45) ; la pré-ouverture devient efficiente seulement à la toute fin ([16]).

---

## [1] Currency Returns in Different Time Zones (Zhengyang Jiang)

**SSRN 2613592 · version du 30 janvier 2019 · Kellogg School of Management, Northwestern University**

### Question
Les devises ont des rendements différents pendant les heures ouvrées américaines et pendant les heures « étrangères ». Le papier propose une explication **par le risque** (et non par la segmentation/les flux d'ordres comme Cornett et al. 1995, Ranaldo 2009, Breedon et Ranaldo 2013) : les nouvelles sur la croissance américaine arrivent surtout pendant les heures US, donc l'investisseur américain (préférences récursives, risque de long terme) exige plus de prime pour détenir des devises risquées pendant ces heures.

### Fait de départ (introduction, Figure 1)
- L'euro a un rendement moyen **positif** contre dollar pendant les heures US et **négatif** en dehors ; sur 10 ans, les deux cumuls divergent alors que le taux de change reste stable.
- Stratégie simple « long EUR pendant les heures US, short EUR pendant les heures étrangères » : **Sharpe annualisé 0,97 avant coûts, 0,25 après ajustement du spread bid-ask** (cotations indicatives).
- Le yen fait l'inverse : rendement moyen **négatif** contre dollar pendant les heures US, **positif** en dehors.
- Bloomberg News (cité, note 1) estime l'écart quotidien entre heures US et heures européennes à **4 à 6 points de base**.

### Modèle (section I)
- Temps discret, périodes alternées : t impair = heures US, t pair = heures étrangères, sans chevauchement ; deux périodes consécutives = une journée.
- Investisseur US à préférences Epstein-Zin (γ aversion au risque, ψ élasticité intertemporelle ; préférence pour la résolution précoce : γ > 1 > 1/ψ).
- Consommation US avec croissance de long terme x_t ; la volatilité de l'innovation de x_t vaut σ_US pendant les heures US et σ_F pendant les heures étrangères, avec **σ_US > σ_F** (hypothèse : les nouvelles sur la croissance US arrivent surtout pendant les heures US).
- Rendement excédentaire d'une devise i : r = E[r] + φ·β_i·ε_x (charge β_i sur le choc de long terme US ; φ commun à toutes les devises, plus φ est grand plus toutes les devises sont volatiles).
- **Proposition 1** : r̄_US − r̄_F est proportionnel à (σ_US − σ_F)·φ·β_i, et croissant en β_i et en φ.
- **Corollaire 1** : en coupe, l'écart heures US − heures étrangères croît avec le **bêta action** de la devise (régression du rendement mensuel de la devise sur le rendement excédentaire mensuel du marché actions US). Une devise à bêta positif gagne plus pendant les heures US ; une devise à bêta négatif gagne moins.
- **Corollaire 2** : l'écart s'élargit quand la volatilité globale des changes (φ) est plus forte.

### Données et définitions (section II.A)
- Taux de change interbancaires **Bloomberg BFIX**, cotations toutes les **30 minutes**.
- 13 devises contre USD : GBP, EUR, DKK, AUD, SEK, CHF, NZD, NOK, CNH, CAD, SGD, HKD, JPY. Début : 2007-03 pour la plupart, 2007-05 pour JPY et CHF, 2012-01 pour CNH. Fin : 2019-01. Taux exprimé de sorte qu'**une hausse = devise étrangère plus forte**.
- **Rendement heures US** : log e(16:00 New York) − log e(10:00 New York), même jour.
- **Rendement heures étrangères** : log e(10:00 NY jour t) − log e(16:00 NY jour t−1).
- La somme = rendement 16:00 → 16:00 NY.
- Pourquoi 10:00 NY : c'est 16:00 Londres, le fixing WM/Reuters (« London Fix », fenêtre de 60 secondes autour de 16:00 Londres), que les banques utilisent comme prix de clôture.
- Rendements **non ajustés des taux d'intérêt**, car un trader intraday ne paie pas de portage s'il solde avant 17:00 New York (fin du cycle de 24 h).
- Actions US : CRSP pondéré par la capitalisation, dividendes inclus ; taux sans risque T-bill 1 mois (site de K. French).
- Contexte de marché (annexe, Euromoney 2018) : 65,48 % du volume passe par 10 intermédiaires ; JPMorgan premier avec 12,13 %.

### Résultats en coupe (Table I, quotidien, 2007-03 → 2019-01, % annualisé, écarts-types par 10 000 bootstraps)
Table reconstruite (l'extraction mélange les lignes, mais l'ordre est cohérent avec le texte) :

| Devise | Heures US | Heures étrangères | Écart US − étr. | Total | Bêta action |
|---|---|---|---|---|---|
| GBP | 5,12 (1,43) | −8,56 (2,33) | **13,68** (2,71) | −3,44 | 0,30 (0,05) |
| EUR | 3,91 (1,56) | −5,15 (2,22) | **9,07** (2,72) | −1,24 | 0,36 (0,06) |
| DKK | 3,71 | −4,97 | 8,68 (2,67) | −1,26 | 0,35 |
| AUD | 3,16 | −3,95 | 7,11 (3,58) | −0,78 | 0,59 |
| SEK | 2,22 | −4,29 | 6,51 (3,55) | −2,07 | 0,51 |
| CHF | 4,10 | −2,38 | 6,48 (2,94) | 1,72 | 0,22 |
| NZD | 3,06 | −3,39 | 6,45 (3,95) | −0,34 | 0,61 |
| NOK | 1,74 | −4,46 | 6,20 (3,52) | −2,72 | 0,48 |
| CNH | 1,90 | −3,09 | 4,99 (1,61) | −1,18 | 0,12 |
| CAD | 1,52 | −2,57 | 4,09 (2,78) | −1,05 | 0,45 |
| SGD | 1,38 | −0,42 | 1,79 (1,60) | 0,96 | 0,22 |
| HKD | 0,32 | −0,35 | 0,67 (0,16) | −0,03 | 0,00 |
| JPY | **−2,02** (1,60) | **+2,89** (2,57) | **−4,91** (3,00) | 0,87 | **−0,16** (0,07) |

- Texte : l'euro s'apprécie de 3,91 %/an pendant les heures US et se déprécie de 5,15 %/an pendant les heures étrangères ; écart 9,07 %/an, alors qu'il ne perd que 1,24 %/an sur la période.
- GBP, AUD, DKK aussi plus forts pendant les heures US ; JPY se déprécie pendant les heures US et s'apprécie pendant les heures étrangères.
- **Régression en coupe** de l'écart annualisé sur le bêta action : coefficient **12 %**, constante non significative, **R² = 40 %**. Une devise à bêta 1 s'apprécie de 12 %/an de plus pendant les heures US ; à bêta 0, pas d'écart.
- Robustesse : bêta mesuré en quotidien (Table V) → relation similaire mais plus faible (retournements de court terme et effets lead-lag hors modèle). Avec la **prime forward** comme mesure de risque (Table VII, Figure 4 ; prime prise au début de l'échantillon, 2007-05, car les devises européennes ont des taux nuls ou négatifs après la crise), les devises à prime forward plus élevée ont aussi un écart plus grand. L'auteur dit ne pas résoudre le fait que la prime forward est déconnectée de l'exposition au risque après la crise.
- Rappel de la littérature antérieure (Ranaldo 2009, 1993–2005, heures US définies 7:00–19:00 NY) : écart **19,20 %/an CHF, 16,10 % GBP, 12,30 % DEM, 13,00 % EUR, seulement 0,60 % JPY**.

### Variation dans le temps (Table II, hebdomadaire, écarts-types HAC)
- Étape 1 : la volatilité annualisée quotidienne d'une semaine prédit celle de la semaine suivante (coefficient positif pour toutes les devises : de 0,23 CHF à 0,62 AUD, tous significatifs).
- Étape 2 : régression de l'écart moyen (heures US − heures étrangères) de la semaine w sur la volatilité de la semaine w−1.
  - GBP : coefficient **1,72 (0,93)** ; EUR 1,35 (0,82) ; DKK 1,35 (0,80) ; CNH 1,42 (1,53) ; **JPY −1,63 (0,62)**. Les autres sont proches de zéro ou de signe instable (AUD −0,18, CHF −0,38, NZD −0,67…).
  - Le papier conclut : quand la volatilité est prévisiblement plus forte, le GBP a un écart encore plus positif, le JPY encore plus négatif ; **le résultat est plus faible pour les autres devises**.
- Chiffres de l'introduction (tri en quartiles de volatilité prévue) : EUR, écart la semaine suivante **0,72 %/an** dans le quartile le moins volatil contre **18,82 %/an** dans le plus volatil ; JPY **−0,26 %/an** contre **−17,55 %/an**.
- En mensuel (Table VI) : résultats cohérents mais **non significatifs** (échantillon plus petit).

### Annonces FOMC (Table III)
- Régression : rendement (heures US ou étrangères) = a + b·1(heures US) + c·1(jour FOMC) + d·1(heures US)·1(FOMC). Les heures étrangères de la date t précèdent les heures US de la date t.
- Pour GBP et EUR : b positif (GBP 0,06 (0,01), EUR 0,04 (0,01)) → rendement plus élevé pendant les heures US indépendamment du FOMC ; c positif (GBP 0,13 (0,05), EUR 0,10 (0,04)) → rendements plus élevés **pendant les deux plages** les jours FOMC ; **d non significatif** → l'écart heures US / étrangères **ne s'élargit pas** les jours FOMC.
- JPY : b = −0,02 (0,01).
- Interprétation du papier : le FOMC augmente la volatilité de la croissance de long terme pendant les deux plages ; l'effet « heures US » est plus général que le FOMC, car les annonces macro US (Figure 3, calendrier 2018) sont réparties sur tout le mois et tombent pendant les heures US.

### Robustesse sur la définition des heures (annexe D)
- Heures US 9:00–17:00 NY (Table VIII) : écarts GBP 10,82, EUR 9,25, DKK 9,13, CHF 9,70, AUD 2,91, **JPY −3,66** %/an. Bêta de la volatilité du JPY : −1,79 (0,63).
- Heures US 8:00–16:00 NY (Table X) : GBP 11,20, EUR 8,71, DKK 8,60, CHF 8,11, AUD 3,13, CAD −3,94, **JPY −2,01**. JPY volatilité : −2,08 (0,63).
- Note de lecture : dans le PDF, la Table V (« agrégée au niveau quotidien ») contient exactement les mêmes chiffres que la Table VIII (9:00–17:00) ; c'est ce que montre l'extraction, le papier ne le commente pas.

### Conditions et limites (d'après le papier)
- Résultat **avant coûts** : Sharpe 0,97 brut, 0,25 après le spread des cotations indicatives (stratégie EUR seule).
- Fenêtres : heures US = 10:00–16:00 NY ; « heures étrangères » = 16:00 NY (veille) → 10:00 NY, donc elles couvrent la session asiatique **et** la matinée européenne jusqu'au fix de Londres.
- L'effet volatilité est surtout significatif pour GBP et JPY.
- Le papier ne présente pas de backtest complet au-delà de la stratégie EUR citée.

---

## [2] Housewives of Tokyo versus the Gnomes of Zurich: Measuring Price Discovery in Sequential Markets (Jianxin Wang, Minxian Yang)

**SSRN 1343399 · octobre 2008 · Australian School of Business, UNSW**

### Question
Quelle part de la formation du prix (« information share » au sens de Hasbrouck 1995) revient à chaque fuseau horaire quand les marchés se succèdent sans se chevaucher (marchés « séquentiels ») ? En particulier, le trading pendant les heures japonaises (les « housewives of Tokyo », Mrs Watanabe, citées par K. Nishimura, BoJ, juillet 2007) pèse-t-il plus sur le yen que l'Europe ou les États-Unis ?

### Données
- Cotations Reuters FX (via SIRCA) : **AUD, JPY, EUR, GBP contre USD**, 1er janvier 1996 (1er janvier 1999 pour l'EUR) au 31 décembre 2003.
- Retirés : week-ends (trading trop mince) ; jours avec un trou de plus de **4 heures** sans cotation (panne ou jours fériés) ; **7 et 8 octobre 1998** (volatilité « once-in-a-generation » du JPY, passé de ~130 à ~120 par USD en une journée ; AUD et GBP aussi très volatils).
- Restent : **1 884 jours AUD, 1 902 JPY, 1 189 EUR, 1 879 GBP**.
- Prix = **mid-quote** échantillonné à la fin de chaque période ; s'il n'y a pas de cotation exactement à l'heure, moyenne pondérée des mid-quotes juste avant et juste après (poids inverses à la distance). Rendement = 100·[ln(P_close) − ln(P_open)], **open-to-close de chaque période le même jour**.

### Découpage des 24 heures (Table 1, heures GMT)
| Période | GMT | Durée |
|---|---|---|
| Asie | 23:00 (veille) → 06:00 | 8 h |
| Europe | 07:00 → 12:00 (Francfort/Zurich) | 6 h |
| Londres-New York (chevauchement) | 13:00 → 14:00 | 2 h |
| États-Unis (Amériques hors chevauchement) | 15:00 → 22:00 | 8 h |

(Note : la Reserve Bank of Australia et la Bank of England publient leurs cours quotidiens à 16:00 heure locale.)

### Méthode
- **VAR structurel** sur le vecteur des rendements open-to-close des marchés séquentiels (un seul marché ouvert à la fois), chocs structurels propres à chaque marché, non corrélés, identifiés par **Cholesky** (B0⁻¹ triangulaire inférieure, dans l'ordre chronologique des marchés).
- Décomposition de **Beveridge-Nelson** : la variation quotidienne du prix efficient = Σ h_i·ε_i, avec h' = ι'·A(1)⁻¹·B0⁻¹.
- **Information share** IS_i = h_i² / Σ h_j² ; **component share** CS_i = h_i / Σ h_j.
- Les mesures sont **invariantes au choix de l'heure de début** du cycle de 24 h (démontré en annexe).
- Retards choisis par AIC : **1 pour AUD et GBP, 5 pour JPY, 2 pour EUR**. Écarts-types par **bootstrap à 1 000 réplications**.
- Avantage revendiqué : pas de dépendance à la fréquence d'échantillonnage intraday (contrairement aux modèles de marchés parallèles), et séparation propre des chocs par marché.
- Mesures descriptives comparées : **WPC** (weighted price contribution, Barclay et Warner 1993) et part de la **variance réalisée** (rendements 30 minutes interpolés).

### Statistiques descriptives (Table 2)
- AUD et JPY ont leur plus forte volatilité **pendant la session asiatique** (écart-type open-to-close Asie 0,361 AUD, 0,424 JPY) ; EUR et GBP la plus forte **pendant l'Europe** (EUR 0,415, GBP 0,299).
- EUR et GBP ont leur plus forte asymétrie et kurtosis pendant la session asiatique.
- Ljung-Box à 10 retards : JPY et EUR fortement autocorrélés ; GBP pas d'autocorrélation.
- Pour la plupart des devises, le rendement du chevauchement Londres-NY est **négativement corrélé** au rendement de l'Europe et **positivement** à celui des US.
- **JPY** : le rendement pendant la session asiatique a une forte autocorrélation mais **aucune corrélation avec les autres marchés** ; les auteurs : « les mouvements de prix pendant l'Asie sont soit ignorés soit retournés pendant l'Europe qui suit ».

### Volumes (Table 3, BIS avril 2007)
- AUD : 51 % du volume dans les places asiatiques du top 10 (Australie 33,4 %).
- JPY : plus de JPY-USD traité au Royaume-Uni (28,6 %) qu'au Japon (25,8 %) ; Asie 39,4 % vs Europe 36,9 %.
- EUR et GBP dominés par l'Europe (57,7 % et 63,8 %), l'Asie y pèse moins que les US (Asie 10,7 % EUR, 12,2 % GBP).

### Parts de rendement et de volatilité (Table 4)
| | Asie | Europe | Londres-NY | US |
|---|---|---|---|---|
| AUD part de rendement | 30,4 % | 25,0 % | 14,0 % | 30,6 % |
| AUD part de variance | 28,6 % | 28,5 % | 12,2 % | 30,6 % |
| JPY rendement | 35,3 % | 29,0 % | 15,0 % | 20,7 % |
| JPY variance | 30,7 % | 29,7 % | 13,8 % | 25,8 % |
| EUR rendement | 13,8 % | 33,6 % | 18,5 % | 34,2 % |
| EUR variance | 17,4 % | 34,3 % | 16,4 % | 31,9 % |
| GBP rendement | 13,6 % | 36,2 % | 17,5 % | 32,8 % |
| GBP variance | 16,3 % | 37,5 % | 15,1 % | 31,1 % |

- L'Asie fait 51 % du volume AUD mais ~30 % du rendement et de la variance ; les US (13,5 % du volume AUD) en font plus que l'Asie. « Plus de volume ne veut pas toujours dire plus d'impact sur le prix. »
- Les parts de rendement sont beaucoup plus bruitées que les parts de variance.

### Résultat principal : information shares (Table 5, échantillon complet)
| | Asie | Europe | Londres-NY | US |
|---|---|---|---|---|
| AUD (K=1) | **33,1 %** | 29,6 % | 13,1 % | 24,3 % |
| JPY (K=5) | **30,9 %** | 27,9 % | 20,3 % | 20,9 % |
| EUR (K=2) | **8,1 %** | **44,3 %** | 21,0 % | 26,6 % |
| GBP (K=1) | 13,6 % | **38,8 %** | 17,3 % | 30,2 % |

(La colonne US est reconstruite à partir de l'extraction, où elle est décalée ; les totaux font bien ~100 %.)
- Intervalles bootstrap 90 % (ex. AUD Asie 28,4–38,1 %, JPY Asie 23,3–39,2 %, EUR Asie 4,0–13,5 %, EUR Europe 37,0–50,8 %, GBP Europe 34,6–43,7 %). Toutes les parts sont significativement > 0.
- Pour l'EUR : Europe > US > Asie, différences significatives (bornes des intervalles disjointes).
- Pour les 4 devises, au moins un élément hors diagonale de B0⁻¹ est significatif → les chocs de forme réduite sont corrélés entre marchés, d'où l'intérêt du modèle structurel.

### Évolution dans le temps (Table 6, un VAR par année)
- **AUD** : Asie 41,9 % (1996) → 24,0 % (2003) ; moyennes Asie 34,0 % (1996–99) → 30,4 % (2000–03) ; Europe 21,9 % → 30,7 %.
- **JPY** : Asie 35,7 % → 28,8 % ; Europe 28,2 % → 31,6 % ; Londres-NY 15,3 % → 18,9 %.
- **EUR** : Asie 7,6 % (1999–2001) → 19,9 % (2002–03) ; Europe 42,8 % → 31,2 %.
- **GBP** : Asie 12,5 % → 13,2 % ; Europe 37,3 % → 36,1 %.
- Conclusion des auteurs : l'Asie perd de l'information sur ses devises (AUD, JPY) et en gagne sur l'EUR ; l'Europe l'inverse → égalisation entre « marchés domestiques » et « non domestiques ». Les auteurs précisent que ces évolutions reposent sur des estimations ponctuelles (8 années seulement).

### Comparaison avec volume, rendement, variance (Table 7)
- Écart absolu moyen (MAD) entre information share et part de variance ≈ 3 % sauf EUR (7,3 %) ; GBP le plus faible (< 2 %), cohérent avec son absence d'autocorrélation.
- Quand les corrélations sériales et croisées sont faibles (GBP), la part de variance peut approximer l'information share ; **pas pour AUD et EUR** (trois termes hors diagonale significatifs).
- **Par heure de trading** (Panel B) : le chevauchement Londres-NY a la plus forte contribution horaire à la variance, au rendement et à l'information **pour les 4 devises** ; pour l'EUR, l'impact horaire de Londres-NY est **2 à 10 fois** celui des US et de l'Asie.

### Conclusions du papier
- L'Europe reste très importante pour les 4 devises.
- La session asiatique est la plus informative pour AUD et JPY (31–33 %) et la moins pour EUR et GBP (8–14 %), mais elle **perd** du poids sur AUD et JPY.
- Le chevauchement Londres-NY (2 h) est très significatif et stable ; pour EUR et GBP il pèse plus que les 8 heures asiatiques.
- Les US hors chevauchement ont moins de poids que l'Europe pour les 4 devises (note 4 : 22 des 28 annonces macro US d'Andersen et al. 2003 tombent dans le chevauchement Londres-NY, ce qui peut expliquer la faible part du reste des heures US).
- « L'impact de Mrs Watanabe a peut-être été surestimé » ; le trading de devises reste dominé par les institutionnels d'Europe et des US.
- Le papier ne dit pas ce qui détermine la part d'information d'un marché (piste : quantité et qualité du flux d'ordres, présence de grandes institutions).

### Limites
- Pas de stratégie de trading ; mesure de contribution à la formation du prix.
- Données 1996–2003, mid-quotes indicatives Reuters.

---

## [3] Asymmetric Information and Price Discovery in the FX Market: Does Tokyo Know More About the Yen? (Vincentiu Covrig, Michael Melvin)

**SSRN 138495 · non daté dans le PDF (références à 1998 « forthcoming ») · Arizona State University**

*(Le texte de ce PDF est illisible en extraction automatique (polices encodées) ; il a été lu sur les images des pages.)*

### Question
Identifier une période où des traders **informés** sur le yen/dollar sont concentrés à Tokyo, puis tester trois prédictions de la microstructure en comparant cette période à une période semblable sans concentration d'informés.

### L'expérience naturelle
- Jusqu'au **22 décembre 1994**, le marché des changes de Tokyo interdisait de traiter le yen pendant la **pause déjeuner de 12:00 à 13:30 (heure de Tokyo)**. Le 22 décembre 1994, la restriction est levée (cf. Ito, Lyons, Melvin 1998, « The Tokyo Experiment »).
- **BEFORE** = fin de matinée avant la levée (période supposée riche en informés : ils doivent exploiter leur information avant la fermeture). **AFTER** = même heure de la journée après la levée (plus de fermeture, plus de concentration).
- Hypothèse supplémentaire : les traders japonais ont une information supérieure sur le yen/dollar. Sources possibles citées (sans preuve dure, disent les auteurs) : flux d'ordres clients (les grandes banques japonaises reçoivent les opérations de change des grandes entreprises japonaises), connaissance anticipée des publications ou décisions des autorités japonaises (exemple de Peiers 1997 : Deutsche Bank leader de prix autour des interventions de la Bundesbank ; anecdote de Niederhoffer et article du WSJ de 1998 sur des fuites présumées du *tankan* à la Banque du Japon).
- Indice préliminaire (Figures 1 et 2, variances sur 20 jours, cotations à 1 minute) : **BEFORE**, la variance des cotations d'origine japonaise a une forme en **U** sur la matinée asiatique (9–10 h, 10–11 h, 11–12 h, remontée vers midi), celle des cotations non japonaises est **décroissante** ; **AFTER**, le U japonais **disparaît** (les deux courbes décroissent). Les auteurs reconnaissent qu'un U peut aussi venir du rééquilibrage d'inventaire avant une fermeture (Brock et Kleidon 1992), d'où les tests suivants.

### Données
- Cotations du yen/dollar sur l'écran **Reuters FXFX** (Olsen & Associates, Zurich), novembre 1994 – janvier 1995.
- Fenêtres de 20 jours : **BEFORE = 24 novembre → 21 décembre 1994** ; **AFTER = 4 janvier → 31 janvier 1995** (les fêtes sont exclues : activité anormalement faible).
- Rendements **1 minute** = variation du log du milieu bid-ask de la dernière cotation avant chaque minute.
- Cotations séparées selon leur **origine** : banques japonaises vs non japonaises (et, en robustesse, Hong Kong et Singapour).

### Modèle théorique (section II.A)
- Modèle à la Kyle (1985) / Subrahmanyam (1991) : k traders informés averses au risque observant un signal bruité δ + u, traders de liquidité, teneur de marché neutre au risque, prix P = F̄ + λω.
- λ (inverse de la profondeur) est une fonction unimodale de k ; l'efficience informationnelle Q = 1 + 1/[φ + σ_z²/(k²β²)] **augmente avec k** (kβ, l'agressivité totale des informés, croît avec k). Donc : plus d'informés → prix plus informatifs → convergence plus rapide vers le prix de pleine information.
- Si les traders de liquidité sont stratégiques (Admati-Pfleiderer), ils se concentrent aussi BEFORE (λ plus faible), ce qui peut expliquer le U de volatilité.

### Test 1 : vitesse d'ajustement (Table 1)
- Modèle **MA(1)-GARCH(1,1)** sur les rendements 1 minute de la fin de matinée **10:30–12:00 Tokyo**, avec une indicatrice pour la 1re observation de chaque jour.
- Demi-vie d'un choc de volatilité = −ln 2 / ln(γ1 + γ2).
- Estimations BEFORE / AFTER : α1 (terme MA, « rebond bid-ask ») −0,293 (t −8,1) / −0,328 (t −13,0) ; γ1 0,701 / 0,856 ; γ2 0,042 / 0,097 ; skewness des résidus 10,66 / 0,37 ; kurtosis 301,70 / 8,24.
- **Demi-vie : 2,33 minutes BEFORE contre 14,09 minutes AFTER** → les cotations rejoignent le niveau de pleine information **environ 6 fois plus vite** quand les informés sont actifs.

### Test 2 : causalité entre cotations japonaises et non japonaises
**a) Grandes révisions de cotation (Table 2)** — régression r_t^d = a + b·r_{t−1}^i + c·r_{t−1}^d (Newey-West), rendements en points de base (×10 000).
- Filtre : on ne garde que les rendements de la variable explicative **supérieurs à 2,5 points de base** ; la variable expliquée est la variation de la cotation de l'autre groupe qui suit.
- Trois fenêtres (heure de Tokyo) : 9:00–10:30, 10:30–12:00, 13:30–15:00, BEFORE et AFTER.
- Japon → non-Japon (coefficient b, t-stat) : significatif partout (BEFORE 10:30–12 : 0,175, t 4,36).
- Non-Japon → Japon : significatif partout **sauf BEFORE 10:30–12:00** (b = 0,048, t 1,34).
- Donc : **causalité à sens unique (Japon mène) seulement en fin de matinée BEFORE** ; causalité dans les deux sens dans toutes les autres fenêtres (BEFORE et AFTER).

**b) Méthode des cotations non synchrones (De Jong-Nijman / De Jong-Mahieu-Schotman, Table 3)** — toutes les cotations, corrélations croisées décalées.
- Tests de Wald (χ²(5)) : « Japon mène » 11,6 BEFORE / 11,5 AFTER ; « non-Japon mène » **7,1 BEFORE** / 14,6 AFTER. Lecture des auteurs : causalité dans les deux sens AFTER ; BEFORE, à sens unique (le Japon mène, l'inverse n'est pas significatif).
- Corrélation contemporaine (lag 0) : 0,053 (t 0,22) BEFORE contre **0,668 (t 4,54)** AFTER.

### Test 3 : part d'information de Hasbrouck (Table 4)
- VECM (cotations japonaises et non japonaises cointégrées), échantillonnage 1 minute (cotation précédente), **pas de rendements overnight**, 4 retards (essais de 2 à 12 : peu de changement après 4). Bornes haute/basse par permutation de l'ordre de Cholesky.

| Comparaison | BEFORE haute / basse | AFTER haute / basse |
|---|---|---|
| Japon | 54 % / 44 % | 62 % / 32 % |
| Non-Japon | 56 % / 46 % | 68 % / 38 % |
| Japon (vs Hong Kong) | 72 % / 60 % | 72 % / 59 % |
| Hong Kong | 39 % / 28 % | 41 % / 28 % |
| Japon (vs Singapour) | 55 % / 50 % | 65 % / 34 % |
| Singapour | 50 % / 45 % | 66 % / 36 % |

- Part relative Japon / non-Japon : **96 % BEFORE** (aux deux bornes) contre **91 % (haute) et 84 % (basse) AFTER**.
- Japon / Hong Kong (texte) : 181 % et 213 % BEFORE contre 174 % et 208 % AFTER. Japon / Singapour : 109 % et 110 % BEFORE contre 98 % et 96 % AFTER.
- Les auteurs insistent sur les **parts relatives**, car la méthode est biaisée en faveur de la région qui cote le plus souvent (moins de minutes à rendement nul) ; c'est pourquoi le Japon paraît légèrement sous le reste du monde même BEFORE.
- L'abstract résume : la contribution japonaise est **5 à 12 points de pourcentage plus élevée** quand les informés sont actifs.

### Conclusions du papier
- Réponse au titre : un « oui » nuancé. Par moments, les traders japonais semblent mieux informés (ou le marché le croit), mais **en temps normal le Japon ne domine pas** la formation du prix du yen/dollar ; la causalité à double sens est cohérente avec un marché surtout mû par l'information publique, partagée par tous, ou avec des informés qui révèlent lentement leur information.
- La fermeture de midi à Tokyo comprimait le temps disponible et forçait les informés à révéler leur information plus vite juste avant la pause.
- Les auteurs ne revendiquent pas de généralité au-delà de ce cas.

### Limites
- Deux fenêtres de 20 jours (fin 1994 / début 1995), un seul cours (USD/JPY), cotations indicatives Reuters ; pas de stratégie de trading. Le régime étudié (pause déjeuner sans trading) **n'existe plus depuis le 22 décembre 1994**.

---

## [4] Currency Returns and Price Discovery around Global FX Fixings (« Karo Dr He »)

**SSRN 7388124 · préprint « not peer reviewed » · un seul auteur, « Peking University China » (adresse gmail)**

> **Avertissement de lecture (constat, hors contenu du papier).** Ce préprint reprend, souvent mot à mot reformulé, le plan, les données, les fenêtres, les expériences naturelles et la plupart des chiffres de **Krohn, Mueller et Whelan, « Foreign Exchange Fixings and Returns Around the Clock » (Journal of Finance, SSRN 3521370)**, que tu as déjà dans [papers/krohn_fix.pdf](papers/krohn_fix.pdf) (même abstract reformulé, mêmes 304 jours fériés japonais, même DST, même échantillon G9 1999–2019, même « 1 $ → 12 $ » pour le yen). Le texte anglais du préprint est par endroits incohérent (phrases dupliquées, fenêtres mal décrites, chiffres du texte qui ne correspondent pas toujours aux tableaux), et sa bibliographie ne cite pas Krohn-Mueller-Whelan sous ce titre. Pour toute utilisation, **la source à privilégier est le papier original** ; ci-dessous, seulement ce que dit le préprint.

### Thèse
Le dollar **monte avant** chacun des trois grands fixings (Tokyo, BCE, Londres) et **baisse après**, ce qui trace un **W** sur 24 heures. Explication retenue : le **risque d'inventaire** des dealers qui servent une demande inconditionnelle de dollars aux fixings (pas l'information asymétrique).

### Les fixings (section I, heures ET = New York)
- **Tokyo** : 9:55 heure locale (**20:55 ET** hors heure d'été US ; 19:55 ET en heure d'été US, le Japon n'ayant pas d'heure d'été). Chaque banque fixe son propre taux à partir de ses transactions clients ; publication à 10:00 locale ; s'applique aux ordres clients avant et après.
- **BCE** : 14:15 CET (**8:15 ET**), concertation téléphonique des banques centrales de la zone euro, moyenne bid/offer, pas de transactions. En juillet 2016, la publication passe à 16:00 CET (pour décourager l'usage en trading) ; Thomson Reuters crée alors le **WM/Reuters 14:00 CET**. Le papier insiste : le fix BCE n'est pas à 8:30 ET (heure des annonces macro US).
- **Londres (WM/Reuters)** : **16:00 Londres = 11:00 ET**, fenêtre de transactions 15:57:30 → 16:02:30 (5 minutes), le plus important ; réservé aux ordres soumis avant 16:00.

### Données
- G9 contre USD : AUD, CAD, EUR, JPY, NZD, NOK, SEK, CHF, GBP (~75 % du volume FX selon la BIS), **janvier 1999 – décembre 2019**.
- Refinitiv Tick History (cotations indicatives bid/ask), Refinitiv FX Matching (« RM », interdealer, volumes et flux d'ordres depuis **juin 2006**), CME, ICE (indice dollar USDX), Olsen (avant 1999).
- Rendement close-to-close : 17:00 ET → 17:00 ET. Une valeur négative = dollar qui monte ; les graphiques montrent la devise étrangère contre dollar (hausse = devise plus forte).

### Fenêtres intraday (ET)
1. **Pre-T** (avant Tokyo) : 18:30 → 20:55
2. **Post-T** (après Tokyo) : 20:55 → 2:00
3. **Pre-E** (avant BCE) : 2:00 → 8:15 (2:00 ET = 8:00 Francfort, début de journée européenne)
4. **E-L** (BCE → Londres) : 8:15 → 11:00
5. **Post-L** (après Londres) : 11:00 → 17:00

### Rendements moyens par fenêtre (Table I, points de base par jour, t-stat ; devise contre dollar)
| | Pre-T | Post-T | Pre-E | E-L | Post-L | Close-to-close |
|---|---|---|---|---|---|---|
| AUD | −2,84 (−8,2) | 1,85 (3,9) | −0,41 | −0,05 | 1,93 (3,8) | 0,51 |
| CAD | −1,52 (−8,8) | 1,50 (7,1) | −0,77 | −0,41 | 1,55 (3,8) | 0,38 |
| CHF | −1,24 (−5,6) | 1,25 (4,9) | −2,55 (−4,2) | 1,27 (2,6) | 2,24 (5,2) | 1,02 |
| EUR | −1,80 (−8,8) | 2,34 (9,3) | **−3,53 (−7,3)** | 0,63 | 2,73 (6,8) | 0,41 |
| GBP | −1,89 (−9,1) | 1,27 (5,0) | −2,31 (−4,7) | 0,42 | 2,64 (7,4) | 0,18 |
| JPY | −1,61 (−5,9) | **3,15 (8,2)** | −1,04 (−2,4) | 0,62 | **−1,16 (−3,0)** | −0,07 |
| NOK | −1,94 (−7,5) | 2,95 (9,7) | −1,40 (−2,2) | −2,01 (−3,8) | 2,14 (4,5) | −0,31 |
| NZD | −3,39 (−8,4) | 2,29 (4,0) | −0,35 | 0,56 | 1,81 (3,3) | 0,97 |
| SEK | −1,80 (−6,5) | 2,16 (7,1) | −3,08 (−5,0) | −0,05 | 2,60 (5,4) | −0,20 |
| **DOL** (panier) | **−1,99 (−11,7)** | **2,10 (9,2)** | **−1,68 (−4,5)** | 0,14 | **1,84 (5,5)** | 0,45 |

(Tableau reconstruit : l'extraction décale les étiquettes de lignes ; l'ordre AUD → DOL est cohérent avec le texte pour AUD, NZD, EUR, SEK, JPY, DOL.)
- Toutes les devises baissent contre dollar avant Tokyo et remontent après ; toutes baissent avant la BCE (surtout EUR −3,5 et SEK −3,1) ; **pas de tendance nette entre BCE et Londres** (sauf EUR et JPY qui montent jusqu'à une heure avant Londres, d'après la figure) ; après Londres, toutes montent **sauf le JPY** (−1,2) jusqu'à 17:00 ET.
- **Close-to-close : rien de significatif** (aucune devise au-delà de ~1 pb/jour) → les mouvements intraday se compensent.
- Ordre de grandeur cité : ~2 pb dans chaque sens ; avec les volumes BIS 2019, des variations quotidiennes de plus d'un milliard de dollars.

### Stabilité (Tables II et III)
- Par sous-périodes (DOL, pb) : Pre-T −1,64 / −2,67 / −3,49 / **−0,63** et Post-T 2,48 / 2,91 / 2,31 / **0,82** pour 1999–2003 / 2004–2009 / 2010–2013 / **2014–2019** ; Pre-E −3,43 / −1,50 / −0,35 / −1,25 ; Post-L 2,80 / 2,29 / 1,43 / 0,86 (t 1,62, non significatif en 2014–2019). Le retournement autour de Tokyo reste significatif en 2014–2019 mais **beaucoup plus petit**.
- Autres sources (juin 2006 – déc. 2019, panier CAD, CHF, SEK, EUR, GBP, JPY) : RTH spot Pre-T −1,58 / Post-T 1,88 / Pre-E −1,65 / Post-L 1,20 ; RTH forwards quasi identiques ; **futures CME** −1,46 / 1,80 / −1,64 / 0,64 ; **ICE USDX** −1,27 / 1,37 / −1,70 / 1,12 ; **RM VWAP (prix traités)** −0,87 / 1,18 / −1,10 / 1,14. L'effet existe donc aussi sur les futures et sur les prix réellement traités.

### Stratégie de retournement (section IV, Table IV, avant coûts)
- **Fenêtre Tokyo** = −(Pre-T) + (Post-T) : long dollar de 18:30 à 20:55 ET, short dollar de 20:55 à 2:00 ET.
- **Fenêtre Europe** = −(Pre-E) + (Post-L) : long dollar de 2:00 à 8:15 ET, short dollar de 11:00 à 17:00 ET (la fenêtre BCE → Londres est exclue faute de tendance).
- Tokyo (pb/jour, t, % jours > 0) : AUD 4,69 (8,0, 56 %), CAD 3,02, CHF 2,49, EUR 4,14 (12,6), GBP 3,15, JPY 4,76 (10,1), NOK 4,89, NZD 5,68, SEK 3,96, **DOL 4,09 (t 14,5, 59 %)**. Toutes p = 0,00.
- Europe : AUD 2,34 (51 %), CAD 2,31, CHF 4,79, **EUR 6,26 (t 9,95, 56 %)**, GBP 4,95, **JPY −0,12 (p 0,35, non significatif)**, NOK 3,54, NZD 2,16, SEK 5,68, DOL 3,51 (t 7,0).
- Agrégé au mois : rendement positif au moins **70 % des mois** pour Tokyo ; au moins deux tiers des mois pour les devises européennes dans la fenêtre Europe.
- Annualisé (texte) : Tokyo de 6,2 % à 14,2 % selon la devise ; Europe EUR 15,6 %, GBP 12,4 %, CHF 12 % ; volatilité annualisée ~8 % ; **skewness positive** et queues épaisses (contrairement au carry).
- Indices cumulés (Figure 4, 1 $ investi en 1999) : Tokyo **JPY ≈ 12,20 $**, EUR 8,9 $, GBP 5,3 $, DOL 8,6 $ ; Europe EUR 26,9 $, GBP 13,5 $, DOL 6,4 $, JPY en baisse (~ −6 %).
- Par année : plus de 20 %/an pendant l'éclatement de la bulle internet (2001) et la crise ; faible en 2007 ; **tendance à la baisse en fin d'échantillon** (cause incertaine : capital d'arbitrage, réformes après le scandale de manipulation WM/Reuters de 2013 ; mais 2015 et 2016 parmi les meilleures années pour la fenêtre Europe).
- **Timing** (Figure 5) : décaler les points de retournement de ±5 minutes autour des fixings réduit le rendement, d'autant plus qu'on s'éloigne ; le maximum est exactement aux fixings.

### Expériences naturelles (section V)
- **Heure d'été** : le Japon n'en a pas ; en ET, le pic du dollar autour du fix de Tokyo se déplace d'une heure (19:55 vs 20:55 ET).
- **Jours fériés japonais** non fériés aux US (304 jours ; échantillon de 4 958 jours ouvrés) : sans fix de Tokyo, le retournement Tokyo **disparaît** (DOL 0,93 pb contre 4,12 ; AUD −1,10 contre 4,92 ; JPY 1,38 contre 4,81 ; test unilatéral rejeté à 5 % pour la plupart des devises) ; le retournement **Europe reste** (DOL 5,60 contre 3,23, non significativement plus bas). Le texte du préprint dit à la fois que les 304 jours sont « exclus » et « inclus » ; le tableau les traite séparément.
- **Introduction des fixings** : avant le fix de Londres (février 1986 – décembre 1993, données Olsen), pas de retournement autour de 11:00 ET ; après, le motif apparaît (Figure 7).
- **Fix BCE** (Table VI, rendements par quart d'heure) : avant l'euro (1986–1998), pas de retournement net à 8:15 ; janvier 2000 – juin 2016, rendements négatifs à 7:45–8:00 et 8:00–8:15 (EUR −0,58 et −0,93) puis forte hausse à 8:15–8:30 ; **après juillet 2016**, le point de retournement passe à **8:00 ET** (WM/Reuters 14:00 CET) : EUR −1,28 (7:45–8:00) puis **+1,09 (8:00–8:15)**, GBP +1,02, JPY +0,54.
- Activité (cotations des futures CME, Figure 8) : depuis l'introduction du fix de Londres, l'activité culmine autour de 11:00 ET (surtout après 2006) et baisse en fin de séance de New York ; pic aussi vers 10:00 ET (expiration des options de change).

### Mécanisme : flux d'ordres et inventaire (section VI)
- Volume RM (juin 2006 – déc. 2019, Figure 9) : les deux heures autour du fix de Londres concentrent **17,5 % à 27 %** du volume quotidien ; ensuite les heures avant la BCE ; le fix de Tokyo est visible pour NZD, AUD, JPY.
- Flux d'ordres RM (Table VII, GBP et AUD) : médiane **négative** (= achat de dollars) avant les fixings (Pre-E, Pre-L), **positive** après Londres ; déséquilibre ~**20 millions $** dans la fenêtre avant fix, soit ~6,5 % (GBP) et 7,5 % (AUD) du volume au fix.
- **Doubles tris** (Table VIII, fenêtre Europe) par demande de dollars avant fix (DD faible/moyen/fort) et volatilité de la veille (FXV) :
  - AUD : DD fort → retournement **+15,99 pb (FXV faible) / +31,46 pb (FXV forte)** ; DD faible → **−14,60 / −26,13 pb** (le retournement devient négatif quand il y a offre de dollars avant le fix).
  - GBP : DD fort → +22,12 / +30,87 pb ; DD faible → −11,89 / −25,14 pb.
  - Le retournement grossit avec le déséquilibre et avec la volatilité (Grossman-Miller).
- Régression (Table IX) : rendement post-Londres = α + β1·flux avant fix + β2·flux post-Londres. Flux contemporain fortement positif (AUD 106,26, t 24,4 ; GBP 46,86) ; **flux avant fix négatif** (AUD −9,28 t −5,9 ; GBP −4,16 t −5,7) ; reste significatif avec le seul flux jusqu'au fix BCE. Un choc d'un écart-type du flux avant fix → retournement d'environ 2,5 pb (GBP) et plus de 3,3 pb (AUD).

### Coûts et qui gagne (Table X, 2006–2019)
- **Demandeur de liquidité (LD)**, qui traite au bid/ask client : retournement **négatif après coûts** (AUD Pre-E+Post-L −7,34 pb ; GBP −0,98). Le papier : on ne peut pas simplement arbitrer ces motifs inconditionnels.
- **Fournisseur de liquidité (LP)**, qui achète des dollars sur le marché interdealer avant le fix et sert les clients au fix : AUD +2,45 pb (t 2,6), GBP +3,95 pb (t 4,8) ; jusqu'à +3,08 / +4,21 pb en prenant Pre-L + Post-L.

### Conclusions
- Le motif W est présent pour les 9 devises, dans le spot, les forwards et les futures ; il est lié à l'existence d'un taux de référence publié.
- Explication : demande inconditionnelle de dollars aux fixings servie par des dealers averses au risque, payés via le retournement ; l'origine de cette demande n'est pas expliquée (pistes : dollar monnaie de réserve et actif sûr).

### Conditions et limites pour un usage pratique (d'après le texte)
- Effet **avant coûts** de quelques pb par jour ; **négatif pour un preneur de liquidité** après coûts ; décroissant en fin d'échantillon (2014–2019).
- Heures en ET avec le décalage d'heure d'été pour Tokyo ; fenêtre Europe à décaler à 8:00 ET depuis juillet 2016.
- Jours fériés japonais : pas d'effet Tokyo.

---

## [5] Returns and Volatility Spillovers in the Currency Futures Markets: The Case of the German Mark and the Japanese Yen (Wan Mansor Wan Mahmood)

**SSRN 976570 · non daté (données jusqu'en 1996) · Universiti Teknologi MARA Terengganu, Malaisie**

### Question
La volatilité se transmet-elle entre deux marchés qui cotent **le même contrat** à des heures **qui ne se chevauchent pas** : l'IMM du CME (Chicago) et le SIMEX (Singapour), liés par un système de **mutual offset** (on peut ouvrir une position sur l'un et la fermer sur l'autre) ?

### Données
- Futures sur **mark allemand (DM)** et **yen (JY)**, prix de **règlement quotidiens** (Datastream), **1er novembre 1993 → 24 juin 1996** : 690 prix, **689 rendements** par série.
- Contrat le plus proche jusqu'à la veille du dernier jour de cotation, puis roll.
- Rendement R_t = ln(P_t / P_{t−1}) × 100.
- Horaires (heure de Chicago, CST) : **CME ~07:20 → 14:00** ; **SIMEX ~19:00 → 01:00** ; **aucune séance entre la clôture du CME et l'ouverture du SIMEX** (pas de chevauchement).
- Le SIMEX a introduit ces contrats identiques en septembre 1984 ; son volume est bien plus faible que celui du CME.

### Méthode
- AR(1)-GARCH(1,1) (BHHH) pour chaque série, puis ajout dans l'équation de variance du **rendement au carré de l'autre marché** (coefficient de spillover). Le test ne porte que sur la volatilité : l'équation de moyenne reste un AR(1) propre au marché, malgré le titre « returns and volatility ». (Dans le PDF, l'indice temporel du rendement au carré de l'autre marché n'est pas lisible avec certitude.)

### Résultats
- Racine unitaire rejetée à 1 % pour toutes les séries (DF ≈ −26 à −28 ; ADF ≈ −18).
- Statistiques (Table 2) : moyennes non différentes de zéro (CME DM −0,0079 %, JY −0,0294 % ; SIMEX DM −0,0137 %, JY −0,0059 %) ; écarts-types ~0,62–0,70 % par jour ; kurtosis 3,8 à 5,8 ; effets ARCH significatifs sur les rendements au carré à 6, 12, 24 retards.
- GARCH seuls (Table 3) : persistance α+β proche de 1 (CME DM 0,989, SIMEX DM 0,984, SIMEX JY 0,903) **sauf JY au CME (0,6807)**, dont les résidus gardent une dépendance de second ordre (LB²(12) = 25,1).
- **Spillover IMM → SIMEX** :
  - DM (Table 4) : coefficient **0,6190, t = 1,96** (significatif à 5 %).
  - JY (Table 6) : coefficient **0,0268, t = 4,79** (significatif à 1 %).
- **Spillover SIMEX → IMM** : coefficient **0,0 (t = 0,0)** pour DM et pour JY (Tables 5 et 7). Pas de transmission.
  (Le texte attribue la Table 5 au yen et la Table 7 au mark, alors que les titres des tableaux disent l'inverse ; la conclusion « aucune transmission SIMEX → IMM » vaut pour les deux.)
- Diagnostics : avec spillover, plus de dépendance résiduelle (sauf JY au CME), kurtosis réduite.

### Conclusion du papier
La volatilité va du **grand marché (IMM, Chicago) vers le petit (SIMEX, Singapour)**, pas l'inverse ; cohérent avec Abhyankar (1995) sur les futures Eurodollar. « Les traders peuvent prendre des indices de l'activité des grands marchés de futures de devises pour se positionner sur les plus petits. »

### Limites
- Un peu moins de 3 ans de données quotidiennes (1993–1996) ; prix de règlement ; deux contrats (le DM n'existe plus) ; aucune stratégie, aucun test sur la moyenne des rendements ; le SIMEX est devenu SGX.

---

## [7] Overnight Price Discovery and the Internationalization of a Currency: The Case of the Korean Won (Jianxin Wang)

**SSRN 1972641 · mars 2014 · UTS Business School, Sydney**

### Question
Proposer une mesure de l'internationalisation d'une devise : la part de la formation du prix qui se fait **la nuit, offshore** (hors heures ouvrées locales). Application au **won coréen (KRW/USD)**.

### Contexte (Table 1, BIS)
- Pas de trading **spot** offshore du KRW (interdit) ; le trading offshore passe par les **dérivés**, surtout les **NDF** (non-deliverable forwards) : 0,5–1 Md$/jour en 2003, 2,6 Md$ en 2005, 9,4 Md$ en 2008.
- Part offshore du trading total de KRW : **14 % (2001), 19 % (2004), 20 % (2007), 37 % (2010)** ; volume global 9,76 → 60,27 Md$/jour.

### Données et définitions
- Cours **open, high, low, close** du KRW/USD pendant les heures ouvrées coréennes, publiés par la **Banque de Corée**, **1er janvier 1999 → 31 décembre 2012** (14 ans ; on évite la bande de fluctuation, élargie à 10 % le 19/11/1997 puis abolie le 12/12/1997, et la crise asiatique).
- Rendement de nuit r_N = ln(Open_t / Close_{t−1}) ; de jour r_D = ln(Close_t / Open_t). **Cotation en KRW par USD : un rendement positif = le won se déprécie.**
- Volatilité quotidienne = ln(High/Low).
- Mesures : **WPC** (weighted price contribution, Barclay-Warner 1993) et **information share (IS)** du VAR structurel séquentiel de Wang et Yang (2011) (le papier [2] ci-dessus), retards par BIC. Filtre en robustesse : retirer les jours où le rendement de nuit ou de jour sort de 5 écarts-types de la moyenne annuelle.
- La WPC diverge de l'IS quand les rendements de nuit et de jour sont corrélés ou que le ratio de variance est élevé ; l'IS, fondée sur le prix efficient, est jugée plus appropriée.

### Résultats

**Nuit vs jour (Table 2)**
- Le won tend à **se déprécier la nuit** (r_N cumulé positif 10 années sur 14) et à **s'apprécier le jour** (r_D négatif 9 années sur 14). En moyenne : **+3,89 %/an la nuit, −4,73 %/an le jour**.
- **Corrélation nuit/jour négative chaque année** (moyenne −0,12), significative 9 années sur 14 → désaccord entre investisseurs onshore (jour) et offshore (nuit).
- Exemples : 1999, nuit +22,6 % (dépréciation), jour −28,3 % ; **2008**, jour **+32,4 %** (forte dépréciation onshore), nuit −2,76 % ; **2010**, jour −18,6 %, nuit +16,0 %.
- Ratio volatilité nuit / jour : moyenne **86 %**, en hausse (49–52 % en 1999–2000, **104–112 % en 2010–2012**) ; 4 des 5 dernières années, volatilité de nuit ≥ volatilité de jour.

**Part de la nuit dans la formation du prix (Table 3)**
| Année | IS nuit | WPC nuit |
|---|---|---|
| 1999 | 11,1 % | 19,1 % |
| 2000 | 6,7 % | 17,6 % |
| 2001 | 33,9 % | 38,3 % |
| 2004 | 40,6 % | 52,2 % |
| 2005 | 27,8 % | 46,9 % |
| 2007 | 45,6 % | 50,1 % |
| 2008 | 49,8 % | 44,5 % |
| 2009 | 25,7 % | 36,4 % |
| 2011 | 49,5 % | 59,1 % |
| 2012 | 51,1 % | 58,4 % |
| Moyenne | 32,8 % | 40,7 % |

- Tendance nettement haussière : IS de **< 10 % (1999–2000) à ~50 % (2011–2012)** ; WPC de < 20 % à ~60 %. Remarquable puisqu'il n'y a pas de spot offshore. Creux en 2005 et 2009.
- Avec le filtre 5σ, IS très proches (ex. 2011 : 53,8 %).

**Les traders de jour apprennent-ils de la nuit ? (Table 4)** — régression r_t (close-to-close) = α + β·r_N,t (Biais, Hillion, Spatt 1999 ; β ≈ ratio information/bruit de la nuit selon Barclay-Hendershott 2008).
- β par année (1999 → 2012) : 0,96 ; 0,69 ; 0,80 ; 0,72 ; 0,96 ; 0,87 ; **0,70 (2005)** ; 0,98 ; 0,97 ; 0,78 ; **0,76 (2009)** ; 0,97 ; 0,93 ; 0,90 (moyenne 0,86). β = 1 non rejeté en 1999, 2003, 2006, 2007, 2010 (nuit « très efficiente » ces années-là).
- **R² : de 0,18 et 0,09 (1999, 2000) à 0,50, 0,54, 0,51 (2010–2012)** ; suit la même tendance que l'IS. Les creux de β en 2005 et 2009 coïncident avec ceux de l'IS.
- Lecture du papier : le mouvement de nuit **n'est pas retourné** pendant la séance coréenne (β proche de 1) et pèse de plus en plus dans le rendement quotidien.

**Week-ends (Table 5)** — du vendredi clôture au lundi ouverture.
- IS week-end moyenne **11,2 %** (WPC 11,1 %), soit **~4,25 % par jour** de week-end contre **20,5 % par jour de semaine** ; **pas de tendance** dans le temps (normal : peu d'information le week-end) ; R² de la régression hebdomadaire ~0,10.

### Conclusions
- La nuit offshore joue un rôle croissant dans la formation du KRW/USD ; mesure proposée de l'internationalisation.
- Le KRW reste bien moins internationalisé que l'AUD ou le JPY (~70 % de leur formation du prix hors heures asiatiques selon Wang et Yang 2011).

### Ce qu'il faut retenir pour l'usage
- Données seulement OHLC quotidiennes de la Banque de Corée ; aucune stratégie testée ; pas de coûts.
- Le fait marquant pour un test : rendement de nuit et de jour **négativement corrélés chaque année**, dérive de nuit (dépréciation) et de jour (appréciation) de signes opposés en moyenne, mais **β ≈ 0,7–1** (la nuit n'est pas retournée en séance au sens de la régression).

---

## [8] Dynamic Conditional Correlation and Volatility Distributions in Tokyo, London, and New York Gold Markets (Chia-Ju Lee, Tuan-Nam Lai, Chang-Chou Chiang, Hai-Chin Yu)

**SSRN 5167870 · Investment Management and Financial Innovations 16(4), 2019, p. 146–155 · Chung Yuan University, Taïwan**

### Question
Les prix de l'or à Tokyo, Londres et New York évoluent-ils ensemble, comment leur corrélation varie-t-elle dans le temps, et augmente-t-elle quand la volatilité monte ?

### Données
- **Prix de clôture quotidiens de l'or** à Tokyo, Londres et New York, source : site de **Johnson Matthey**.
- Période : l'abstract dit **1993–2012** ; la section données écrit « 1er janvier 1933 – 31 décembre 2012 » (coquille probable ; le papier ne la corrige pas).
- Le papier **ne précise pas** à quelle heure correspond chaque « clôture » (ni fixing, ni décalage horaire), et n'aligne pas les fuseaux.

### Méthode
- **DCC-GARCH** (Engle 2002, Cappiello et al. 2006) sur les trois marchés.
- Distribution des DCC par tranches de volatilité (déciles 0–10 %, …, 90–100 %).
- **DCC à seuil de volatilité** (Kasch et Caporin 2013) : indicatrice quand la volatilité d'un des deux marchés dépasse le quantile 50 %, 75 %, 90 % ou 95 %.

### Résultats chiffrés
- Statistiques (Table 1) : rendement moyen quotidien Tokyo 0,00010, Londres 0,00013, New York 0,00013 (Tokyo le plus faible) ; écart-type 0,00482 / 0,00427 / 0,00432 ; kurtosis 7,66 / 9,48 / 9,84.
- Corrélations simples (Table 2) : toutes > 0,7 (valeurs extraites 0,7412, 0,7796, 0,8134 ; la plus forte semble être Londres–New York, mais l'extraction ne permet pas d'affirmer l'attribution exacte).
- GARCH (Table 4) : α ≈ 0,075, β ≈ 0,91–0,93 ; persistance Tokyo 0,9877, Londres 0,9892, New York 1,001 (volatilité très persistante).
- DCC (Table 3) : a = 0,0534 (t 10,8), b = 0,9404 (t 158) ; le DCC scalaire est rejeté par le test du rapport de vraisemblance.
- DCC moyen par décile de volatilité (Table 5) : Tokyo–Londres de 0,69 (décile le plus bas) à 0,85/0,82/0,72 (déciles 70–100 %) ; Londres–NY de 0,71 à 0,81–0,90 ; New York–Tokyo de 0,66 à 0,82–0,84. Le texte : « une volatilité plus forte va avec un DCC plus fort dans les trois cas ».

### Volatilité forte vs faible (Figure 2)
- Jours de faible volatilité (< 10 %) : distribution des DCC **leptokurtique** ; jours de forte volatilité (> 90 %) : **platykurtique** (plus étalée).
- **Contradiction interne** : pour Tokyo–Londres, le texte dit que le DCC moyen des jours **peu** volatils est **plus élevé** que celui des jours très volatils (corrélation qui baisse avec la volatilité), alors que la Table 5 et la conclusion disent que le DCC augmente avec la volatilité. Pour Londres–NY, distribution bimodale les jours volatils, pas de conclusion nette ; pour New York–Tokyo, DCC plus élevé les jours volatils.

### DCC à seuil (Table 6)
- Tokyo–Londres : corrélation affectée de façon significative **à tous les seuils** (50, 75, 90, 95 %).
- Londres–New York : significatif seulement **aux seuils 50 % et 95 %** (plus sensible aux extrêmes).
- New York–Tokyo : la corrélation augmente avec la volatilité aux seuils 50, 90, 95 %.
- (Le tableau lui-même est trop mal extrait pour reprendre les coefficients.)

### Conclusions du papier
- Corrélations variables dans le temps, pas constantes.
- Quand l'or devient volatil, Londres et New York sont fortement corrélés : diversifier entre les deux ne réduit plus le risque.
- L'abstract affirme aussi que **New York subit un effet de débordement de la variance de Tokyo, mais pas l'inverse**, et que les marchés de Londres/NY et Tokyo/Londres sont « presque égaux, aucun ne domine » ; **le corps du papier ne présente pas de test de débordement** qui appuie la première affirmation.

### Limites
- Données quotidiennes sans heure précise de clôture ; aucune analyse intraday, aucune stratégie ; incohérences internes signalées ci-dessus.

---

## [9] Do Bulls and Bears Move Across Borders? The t-0.5 Framework and International Information Transmission to Asia-Pacific Markets (Ryo Kinoshita)

**SSRN 7019738 · non daté dans le PDF (données jusqu'en janvier 2024) · Graduate School of Economics, Kobe University** (l'auteur déclare avoir utilisé des LLM pour traduire du japonais et améliorer le texte, pas pour l'analyse)

### Question
Dans quelle mesure l'information disponible à la **clôture de New York** (06:00 heure du Japon en hiver US, **05:00 JST en heure d'été US**) prédit-elle le **sens** du lendemain des indices asiatiques ?

### Le « cadre t-0.5 »
- t = 0 : clôture de New York ; t = 1 : clôture de New York du jour suivant ; l'ouverture de Tokyo (09:00 JST) est le point intermédiaire « t ≈ 0,5 ». t n'est pas une fraction de temps physique, c'est une position conventionnelle dans le cycle.
- Mesure : **précision directionnelle (DA)** ; en efficience totale, DA → 50 %. L'excès au-dessus de 50 % mesure la prévisibilité.
- **Attention (dit par l'auteur)** : la cible est le signe du rendement **close-to-close** du Nikkei 225 du jour t (pas le gap d'ouverture seul) ; il contient le gap d'ouverture **et** la séance ; il ne mesure donc pas directement l'information non intégrée à l'ouverture.

### Données (Yahoo Finance)
- Clôtures quotidiennes **décembre 2009 → janvier 2024** : Nikkei 225 (^N225), **VIX** (^VIX), rendement 10 ans US (^TNX), USD/JPY ; en log-rendements. N = **3 323** jours pour le Nikkei (après retrait des jours fériés non communs). KOSPI N = 3 354, Hang Seng 3 373, ASX 200 3 455.
- Variables supplémentaires (Section 4.6) : SPX (S&P 500), TLT, GLD, DXY, OIL, HYG.
- Prédicteurs pris à la clôture de New York du jour t−1 ; plus le rendement de la veille du marché asiatique (MKT_lag).

### Méthode
- Régression **logistique** (sklearn, lbfgs, max_iter 200), variables standardisées sur la seule fenêtre d'entraînement.
- **Walk-forward** : fenêtre glissante de **2 800 jours**, une prévision hors échantillon par jour (STEP = 1) → **522 prévisions OOS sur 2021–2023**.
- Test : Z binomial contre 50 % (suppose l'indépendance des prévisions).
- Comparaisons : marche aléatoire, AR(1) (signe du rendement de la veille), **règle VIX-signe** (si le VIX baisse à la clôture de New York, prévoir une hausse de l'Asie ; zéro paramètre), LSTM (50 unités, dropout 0,1, lookback 20 jours, 6 seeds).
- SHAP (LinearExplainer, interventional) pour l'attribution.

### Résultats
**Nikkei 225 (Table 2, 522 jours OOS)**
| Modèle | DA | Z |
|---|---|---|
| Marche aléatoire | 50,00 % | — |
| AR(1) | 48,47 % | −0,70 (n.s.) |
| **Règle VIX-signe** | **69,35 %** | 8,84 |
| LSTM (moyenne 6 seeds, n = 502) | 64,51 % | 6,50 |
| **Logistique** | **67,82 %** | 8,141 |
| Logistique 10 variables (n = 519) | **70,33 %** | 9,262 |

**Horizon (Table 3)** : h = 1 : 67,82 % ; **h = 2 : 49,90 % (Z −0,04)** ; h = 3 : 52,12 % ; h = 5 : 53,28 % ; h = 10 : 50,10 % → le signal disparaît **en un jour de bourse**.

**Sous-périodes (Table 5)** : 2021 : 76,00 % (n = 50) ; 2022 (hausses de taux, VIX élevé, marché baissier) : 65,53 % (n = 235) ; 2023 : 68,35 % (n = 237) ; toutes significatives à 0,1 %.

**Autres marchés (Table 6)**
| Marché | AR(1) | Règle VIX-signe | Logistique |
|---|---|---|---|
| Nikkei 225 | 48,47 % | 69,35 % | 67,82 % |
| KOSPI | 50,63 % | 60,58 % | 60,94 % |
| Hang Seng | 51,22 % | 59,27 % | 58,39 % |
| ASX 200 | 49,54 % | 68,65 % | 67,28 % |

**SHAP, 4 variables (Table 4)** : le VIX domine partout (Nikkei 0,4839 ; KOSPI 0,3842 ; Hang Seng 0,3450 ; ASX 0,5120). Pour le Japon, le **TNX (0,1254)** et l'**USD/JPY (0,0916)** pèsent beaucoup plus que pour les autres marchés (TNX < 0,04 ailleurs) → canal taux US / yen propre au Japon.

**SHAP, 10 variables, Nikkei (Table 7)** : **SPX 0,431** > VIX 0,256 > **TLT 0,120** > GLD 0,060 > DXY 0,043 > MKT_lag 0,042 > OIL 0,041 > HYG 0,032 > TNX 0,031 > USDJPY 0,031. Le VIX paraissait dominant dans le modèle à 4 variables parce qu'il sert de proxy (corrélation négative forte) du sens du S&P 500. SPX + VIX + TLT = le « complexe risque actions de New York » (nom de commodité, pas un mécanisme causal démontré).

### Conclusions et limites (énoncées par l'auteur)
- L'information à la clôture de New York prédit le sens du lendemain en Asie ; le signal dure un jour ; il tient dans des régimes différents ; une règle simple (VIX-signe) fait aussi bien que le modèle.
- **Pas de stratégie de trading testée** : l'auteur précise que 67,82 % de DA ne se traduit pas forcément en rendement (coûts, slippage, faible liquidité avant l'ouverture de Tokyo, rapport entre réussite et amplitude non étudié).
- Limites listées : (1) la cible close-to-close est largement gouvernée par le **gap d'ouverture** ; il faudrait séparer gap et séance ; (2) les **futures Nikkei** (séance de nuit d'Osaka, CME) intègrent déjà l'information de New York avant l'ouverture du comptant ; (3) Z-test qui suppose l'indépendance, tests multiples (4 marchés, plusieurs horizons) non corrigés ; (4) SHAP ≠ causalité.
- **Remarque de lecture (déduite des définitions du papier)** : le rendement close-to-close du Nikkei du jour t commence à la clôture de Tokyo de t−1, donc **avant** la séance de New York de t−1 ; une partie de ce qui est « prédit » est la réaction du Nikkei à une séance US déjà terminée au moment de la prévision, d'où la cohérence avec la limite (1) de l'auteur et avec le papier [15] de la 2e récolte (même auteur), qui conclut que c'est la **séance au comptant** de New York qui prédit le gap asiatique.

---

## [10] Feedback Trading: Strategies during Day and Night with Global Interconnectedness (Alex Kusen, Markus Rudolf)

**SSRN 3275317 · working paper du 30 octobre 2018 · WHU – Otto Beisheim School of Management**

### Question
Le **feedback trading** (achat après hausse / vente après baisse = feedback positif ; l'inverse = feedback négatif) diffère-t-il entre la **séance (day)** et la **nuit (night)**, et entre pays, et change-t-il quand on modélise les marchés ensemble (débordements) ?

### Données
- Indices : **DAX 30, FTSE 100, S&P 500, Nikkei 500, Hang Seng**, ouvertures et clôtures quotidiennes Datastream.
- **27 juin 2007 → 7 mars 2017**, **2 165 jours** communs (jours alignés entre marchés ; perte de 8,8 % (Japon) à 12,2 % (Allemagne) des observations).
- Rendements en log × 100 : **nuit** r_n = ln(Open_t / Close_{t−1}) ; **jour** r_d = ln(Close_t / Open_t) ; total = somme.
- Valeur fondamentale : f1 = dividende × (inverse du rendement du dividende comme multiple) ; f2 = bénéfices × PER moyen de long terme. Sentiment B_t = 1 si le **ratio put/call** < 1 (optimiste), 0 sinon.
- Horaires (Figure 2, CET) : pause déjeuner Tokyo 3:30–4:30 CET, Hong Kong 5:00–6:00 CET.

### Modèle
- Sentana et Wadhwani (1992) étendu à trois types d'investisseurs (rationnels, feedback traders, fondamentalistes) :
  r_t = b0 + b1·σ²_t + **b2·σ²_t·r_{t−1}** + b3·σ²_t·B_t + b4·σ²_t·(f_{t−1} − P_{t−1}) + ε_t
- **Lecture du signe** : **b2 < 0 = feedback positif** dominant (il induit une autocorrélation d'ordre 1 négative, d'autant plus forte que la volatilité est élevée) ; b2 > 0 = feedback négatif (contrarian).
- Variance EGARCH(1,1), erreurs GED (pays par pays) ; puis modèle « global » DCC-MGARCH bivarié (loi de Student multivariée).
- Appariement des rendements entre fuseaux : les rendements de **jour** d'Allemagne, du Royaume-Uni et des US sont associés à la **nuit suivante** du Japon et de Hong Kong.

### Statistiques descriptives
- Moyennes (% par jour) — **jour** : Allemagne −0,015, R-U −0,010, US +0,015, Japon −0,036, Hong Kong −0,071 ; **nuit** : Allemagne +0,024, R-U −0,007, US +0,006, Japon +0,048, Hong Kong +0,075. Le papier : moyenne surtout **négative le jour, positive la nuit** (prime de risque de nuit, et les institutionnels traderaient contre le momentum le jour). Le rendement quotidien total est positif en moyenne pour chaque pays (non tabulé).
- Kurtosis beaucoup plus forte la nuit (Jarque-Bera au moins 10 fois plus grand la nuit pour Allemagne, R-U, US) ; effets ARCH significatifs pour tous les rendements de jour, la nuit seulement pour Allemagne, Japon, Hong Kong.
- Corrélations (Table 1) : jour Allemagne–R-U **0,708** (nuit 0,694) ; **jour US → nuit de Hong Kong 0,656**, jour Allemagne → nuit HK 0,492, jour Allemagne → nuit Japon 0,425 ; jour Japon vs nuit Japon **−0,056**, jour Japon vs nuit HK **−0,403** ; jour HK vs nuit Japon −0,163.

### Résultats (Table 4, modèles pays par pays)
- Feedback **positif** en général (b2 surtout négatif, de **−0,174 à −0,007**).
- **Japon et Hong Kong** : b2 significativement négatif **le jour et la nuit** (Japon nuit : **b2 = −0,174** (0,016), de loin le plus fort ; Japon jour −0,013 ; Hong Kong jour −0,014, nuit −0,007).
- **Allemagne** : pas de feedback le jour (b2 = 0,000) ; feedback positif la nuit (b2 = −0,009, significatif à 5 % avec f1).
- **Royaume-Uni** : feedback positif le jour (b2 = −0,010) ; pas de feedback la nuit (b2 = +0,003, non significatif).
- **US** : jour b2 −0,016 ; **nuit non estimable** (vraisemblance plate).
- Sentiment b3 presque toujours positif et significatif (sauf Hong Kong jour avec f1) ; fondamental b4 surtout négatif et significatif (sauf US jour avec f1 : +0,058).
- R² ajusté moyen : **2,2 % le jour, 2,5 % la nuit** (max 6 % Allemagne jour).
- Asymétrie EGARCH : la variance monte plus vite après un choc négatif, jour et nuit. Paramètre GED : 1,28–1,52 (jour), 0,98–1,54 (nuit), plus proche d'une Laplace que d'une normale.
- Interprétation des auteurs : le feedback positif est plus fréquent le jour que la nuit (moins de volume la nuit ; les professionnels dominent l'after-hours).

### Modèle global (Tables 5 et 6, DCC bivarié)
- Le jour, en Allemagne : toujours **aucun** feedback, quel que soit le partenaire ; mais en couple Allemagne–R-U, le feedback positif du **R-U disparaît**. Feedback positif significatif aux US, au Japon, à Hong Kong même en couple avec l'Allemagne.
- La nuit : feedback positif confirmé en Allemagne, aux US, au Japon, à Hong Kong (au moins à 5 %) ; débordement **à sens unique Allemagne → R-U** : en couple avec l'Allemagne, le b2 de nuit du R-U devient **positif (+0,010)** → feedback **négatif** au R-U.
- Persistance DCC (θ1 + θ2) 0,577 à 0,952 ; demi-vie de la volatilité ~105 jours en moyenne (nuit 156 j, jour 54 j) ; degrés de liberté de la Student ~6,4 (jour) et ~4,2 (nuit).

### Robustesse
- Fonction de demande multiplicative du sentiment : pas de changement notable.
- EGARCH meilleur que GARCH, GJR, PARCH, NARCH pour la plupart des pays (Table B1).

### Conclusions et limites
- Les stratégies de feedback diffèrent jour/nuit et entre pays ; des débordements entre marchés modifient les comportements estimés.
- Les auteurs suggèrent qu'un investisseur à faibles coûts pourrait construire des stratégies conditionnelles, **sans en tester aucune**.
- Pouvoir explicatif très faible (R² ~2 %), quotidien seulement ; nuit US non estimée ; sentiment = ratio put/call (donnée hors OHLCV).

---

## [11] Is Risk Higher during Non-Trading Periods? The Risk Trade-Off for Intraday versus Overnight Market Returns (Christoph Riedel, Niklas Wagner)

**SSRN 2494387 · version du 18 mai 2015 · Université de Passau**

### Question
Le risque de baisse extrême (queue gauche) est-il différent la nuit (close → open) et en séance (open → close) ? Le papier sépare le risque en (i) **volatilité conditionnelle** (prévisible par un GARCH) et (ii) **risque de queue des innovations** (non prévisible).

### Données
- **NASDAQ Composite, CAC 40, DAX 30** : 1er septembre 1988 → 30 juillet 2010 (**5 716** rendements) ; **TOPIX** : 1er août 1990 → 30 juillet 2010 (**5 217**).
- Rendements log : CC = ln(Close_t/Close_{t−1}), **CO (nuit)** = ln(Open_t/Close_{t−1}), **OC (séance)** = ln(Close_t/Open_t). La nuit inclut week-ends et jours fériés.

### Méthode
- AR(2)-**TGARCH(1,1,1)** (GJR) à innovations normales, estimé séparément sur CC, CO, OC.
- Innovations standardisées → **théorie des valeurs extrêmes**, peaks-over-threshold, **loi de Pareto généralisée (GPD)** sur chaque queue ; seuil choisi pour garder **7 à 10 %** des observations (ex. NASDAQ nuit, queue haute : 540 dépassements = 9,5 %, zone stable 450–550).
- Test H0 : indice de queue ξ = 0 (queues « modérées », domaine de Gumbel) ; tests du rapport de vraisemblance d'égalité des ξ entre CO, OC et CC.
- VaR conditionnelle = μ + σ·q_p avec q_p quantile GPD.

### Statistiques descriptives (Tables 1–2)
- Moyennes quotidiennes (log) — NASDAQ : CC +0,000315, **nuit +0,000419, séance −0,000104** ; TOPIX : CC −0,000186, **nuit +0,000208, séance −0,000394** ; CAC : CC +0,000183, nuit +0,000137, séance +0,000046 ; DAX : CC +0,000293, **nuit +0,000307, séance −0,0000143**. (Le papier ne commente pas ces moyennes ; elles sont lues dans les tableaux.)
- **Volatilité de nuit < 60 % de celle de séance en moyenne**, alors que la nuit dure environ deux fois plus longtemps.
- Kurtosis plus forte la nuit : NASDAQ nuit 13,6 (séance 11,3) ; CAC nuit 18,1 (7,4) ; **DAX nuit 22,1** (10,4) ; TOPIX ~9 partout. Skewness la plus négative la nuit (DAX nuit −1,31) ; le signal est faible pour le TOPIX.

### Résultats du GARCH (Tables 3–4)
- Propriétés linéaires et non linéaires très semblables entre CC, CO, OC ; seul point notable : le coefficient ARCH (α) est **environ trois fois plus grand pour la nuit** → la volatilité prévisible de nuit est surtout induite par l'innovation de la nuit précédente.
- Innovations standardisées : kurtosis la plus forte et skewness la plus négative **la nuit** dans les quatre marchés (DAX nuit : kurtosis 33,1, skewness −2,12).

### Indice de queue (Table 7)
- 24 cas (3 rendements × 2 queues × 4 marchés). ξ = 0 **non rejeté dans 13 cas**, dont **tous les rendements de séance** (sauf la queue haute du TOPIX en séance, juste au-dessus du seuil) → en séance, le GARCH explique les queues épaisses.
- ξ > 0 (queues épaisses, Fréchet) dans 7 cas : **toutes les queues de nuit** sauf la queue haute du CAC (juste sous le seuil). La **queue basse de nuit est la seule catégorie significative dans les quatre marchés**.
- CC : queues épaisses pour la queue basse du CAC et du DAX ; NASDAQ CC queue haute : rejet en faveur d'une queue *fine* (Weibull).
- Queues basses généralement plus épaisses que les hautes.

### Égalité des indices de queue (Table 8, LR)
- **Nuit vs séance : égalité rejetée à 1 %** pour toutes les queues (ex. DAX queue basse LR = 30,8 ; CAC queue basse 46,3), sauf la queue haute du CAC (rejet à 10 % seulement).
- Nuit vs CC : rejeté à 5 % pour toutes les queues sauf la queue basse du CAC (10 %).
- Séance vs CC : en général **pas de différence**.

### VaR (Table 9, NASDAQ, volatilités inconditionnelles)
- Volatilité quotidienne : séance **1,058 %**, nuit **0,858 %**, CC 1,242 %.
| p | VaR séance | VaR nuit | VaR CC |
|---|---|---|---|
| 99,9 % | 4,59 % | **4,95 %** | 5,40 % |
| 99,5 % | 3,38 % | 3,14 % | 3,94 % |
| 99 % | 2,89 % | 2,51 % | 3,35 % |
| 97,5 % | 2,26 % | 1,80 % | 2,63 % |
| 95 % | 1,80 % | 1,33 % | 2,11 % |
- Quantile GPD à 99,9 % : séance 4,33, **nuit 5,77** (normale : 3,09).
- Ratios quantile nuit / séance à 99,9 % : **NASDAQ 1,33, TOPIX 1,27, CAC 1,33, DAX 1,38** ; à 99 % : 1,07 / 1,03 / 1,05 / 1,02.
- Lecture : la VaR de nuit est égale ou plus basse que celle de séance aux niveaux usuels (la volatilité de nuit est plus faible), mais **plus haute à 99,9 %** pour le NASDAQ, car le risque de queue domine.

### Conclusions
- Volatilité de nuit plus faible, mais **risque de queue de nuit significativement plus élevé** (non expliqué par le GARCH), attribué au manque de fonctionnement et de liquidité du marché la nuit, qui se matérialise par un saut à l'ouverture.
- Une mesure du risque de nuit fondée sur la seule volatilité **sous-estime fortement** le risque de baisse de nuit.

### Limites
- Indices au comptant, quotidien ; pas de stratégie ; échantillon jusqu'en 2010.

---

## [12] Night Trading: Lower Risk but Higher Returns? (Marie-Eve Lachance)

**SSRN 2633476 · version du 18 juillet 2015 · San Diego State University**

### Thèse
Les rendements de nuit sont soumis à des **biais persistants** propres à chaque action ; on peut les mesurer (« Overnight Bias Parameter », OBP), et investir **seulement la nuit** dans les actions à biais positif significatif l'année précédente est rentable **après coûts**.

### Données
- **CRSP**, actions NYSE, NYSE MKT, NASDAQ, ARCA, **1995–2014** (1994 pour les retards) ; hors ETF, ADR, fonds fermés.
- Filtres : ≥ 240 jours de cotation l'année en cours **et** la précédente ; prix moyen ≥ **5 $** chaque mois ; retrait des années à rendement de nuit ou de jour > 250 % ; retrait de certaines observations à |rendement quotidien| > 20 % (0,03 % des observations).
- Reste en moyenne **2 554 actions/an** (43,1 % de l'univers CRSP, mais **91,2 % de la capitalisation**), 12 847 083 observations.
- Rendement de nuit = ln((Open_t + dividende_t)/Close_{t−1}) (dividende compté la nuit) ; de jour = ln(Close_t/Open_t) ; ajustement des splits par facpr. Prix d'ouverture CRSP = premier trade du jour.
- TAQ 2010–2012 pour l'intraday ; international : constituants des indices des 23 marchés développés MSCI World, 2002–2014 (Bloomberg).

### Faits de base (Table 1)
- Moyennes quotidiennes équipondérées : **nuit 0,024 %, jour 0,046 %** ; mais pondérées par la capitalisation : **nuit 6,84 %/an contre jour 3,72 %/an**.
- Volatilité quotidienne **nuit 1,45 % vs jour 2,60 %** ; la nuit est moins volatile pour **98 % des actions**.
- Actions exclues (petites, < 5 $) : nuit +26,06 %/an, jour −12,19 % (les résultats du papier sont donc conservateurs).

### Persistance (Fama-MacBeth mensuel, Figure 1)
- Rendement de nuit du mois relié **positivement à chacun de ses 60 retards mensuels** (t de 2,70 à 43,67, tous significatifs à 1 %) ; information maximale en cumulant ~**6 mois**.
- Relation **négative** avec les rendements de **jour** passés (sauf le dernier retard) ; régression contemporaine nuit sur jour : coefficient −0,19 (t −35,97).

### « Momentum de nuit » par déciles (Table 2, VW, rééquilibrage mensuel, tri sur la nuit de l'année passée, ~255 actions/décile)
| Décile | Nuit seule | Alpha | Bêta | Jour | Journée complète |
|---|---|---|---|---|---|
| 1 (bas) | **−17,08 %** | −20,73 % | 0,28 | **+33,08 %** | ~10 % |
| 5 | 0,86 % | — | 0,25 | — | ~11 % |
| 10 (haut) | **+40,43 %** | **+33,93 %** | 0,36 | **−22,07 %** | ~10 % |
- Les rendements **totaux** ne diffèrent presque pas entre déciles : seul le **partage nuit/jour** change.
- **Pas de retournement** : décile haut, rendement de nuit 24,01 % (an 1), 20,30 % (an 2), 21,11 %, 17,33 %, 11,92 % (an 5).
- Interprétation : variation en coupe des **moyennes** de nuit (Conrad-Kaul), pas un momentum classique.

### International (Table 3, constituants, 2002–2014)
- Nuit > jour dans **les 23 pays** (de justesse pour la Nouvelle-Zélande) ; moyenne nuit **+18,8 %/an**, jour **−9,3 %/an**.
- Avec les cours d'ouverture **publiés des indices**, 5 pays montrent l'inverse : le papier l'attribue aux **cotations périmées** à l'ouverture (ex. le S&P 500 reprend la clôture de la veille pour les titres pas encore ouverts). Exemples « Index » vs « WA » (moyenne pondérée des constituants) : US 1,5 % / 5,8 % la nuit ; Japon Nikkei 225 13,1 % / 16,9 % ; Hong Kong 16,5 % / 21,0 % ; DAX 5,9 % / 13,7 % ; FTSE 100 4,0 % / 19,2 %.
- Tri en quartiles dans chaque pays : la nuit augmente toujours avec le quartile ; écart haut − bas ≈ **40 %** (moyenne Q4 43,7 % vs Q1 3,7 %).

### Le modèle de biais de nuit (section 4)
- E[nuit | total] = **θ** + δ·total ; E[jour | total] = (1 − δ)·total − **θ** (le biais de nuit est compensé le jour, le total n'est pas affecté).
- Estimation par action et par an : régression des rendements de nuit quotidiens sur les rendements totaux ; **OBP = constante θ** (annualisée) ; δ ≈ part de variance de la nuit.
- 51 089 paires d'estimations : δ moyen **17,86 %** (> 99 % sous 0,5, exceptions : titres aussi cotés en Europe) ; OBP moyen **8,38 %**, médian 2,56 %.
- Hors échantillon, le modèle reproduit le partage nuit/jour par percentile de rendement total (R² **0,98** nuit, 0,99 jour). **Les rendements de nuit moyens restent positifs même dans les pires percentiles** de rendement total (OBP moyen 20,88 % dans le décile le plus bas).
- Conséquence : la stratégie nuit seule bat la journée complète tant que le rendement total ne dépasse pas θ/(1 − δ) ; elle convient surtout aux marchés **baissiers ou plats**.

### Groupes (Table 4, test unilatéral à 5 % sur le t de l'OBP)
- **OBG** (OBP positif significatif) : **524 actions/an en moyenne, ~20 %** de l'échantillon, un tiers du volume. IBG (négatif significatif) : 376.
- OBG : plus volatiles (41,1 %), bêta plus élevé (1,05), **turnover bien plus fort** (92 % vs 48 % pour IBG), plus grosses, moins souvent NASDAQ, meilleur rendement l'année passée (30,8 %), moins d'institutionnels ; secteur minier surreprésenté (9,4 % vs 5,3 %).
- Déterminants de l'OBP (Fama-MacBeth) : **OBP de l'année passée** (coef. 0,208, t 19,4, le plus important), volatilité, turnover, rendement de l'année passée (+), propriété institutionnelle (−), cotation NASDAQ (−) ; valeur et taille peu importantes.
- **Introductions en bourse** : rendement de nuit ~**3,5 %/mois** les trois premiers mois après l'émission, puis décroissance sur 5 ans ; rendement de jour 0,3 % au départ puis hausse.

### Stratégie (Table 5, VW, OBP de l'année passée, rééquilibrage mensuel)
| | OBG | Positif non sig. | Négatif non sig. | IBG | Long OBG − short IBG | Toutes |
|---|---|---|---|---|---|---|
| Rendement nuit avant coûts | **25,87 %** | 8,87 % | −0,76 % | −11,98 % | 43,09 % | 6,84 % |
| Alpha avant coûts | **20,13 %** | 3,94 % | −5,06 % | −15,60 % | 42,30 % | 2,07 % (n.s.) |
| Alpha après coûts, 10 000 $/titre | **10,45 %** | −3,90 % | −12,26 % | −22,22 % | 20,60 % | −5,68 % |
| Alpha après coûts, 100 000 $/titre | **15,69 %** | −0,01 % | −8,68 % | −18,84 % | 31,80 % | −1,79 % |
| Écart-type | 11,46 % | 10,38 % | 9,29 % | 8,46 % | 6,60 % | 9,76 % |
| Bêta | **0,31** | 0,29 | 0,26 | 0,22 | 0,09 | 0,28 |
- À comparer au marché en journée complète : 10,00 %/an, écart-type 19,34 %.
- Short IBG seul après coûts (10 000 $) : alpha 9,19 %.

### Robustesse (Table 6)
- Fama-French 3 facteurs : OBG 20,06 % ; équipondéré : 23,86 % ; sans jours d'annonce de résultats : 20,25 %.
- **Alpha OBG positif chacune des 20 années** (meilleure 1999 : 53,43 % ; pire 2001 : 2,41 %, fermeture après le 11 septembre) ; IBG négatif chaque année ; long-short positif et significatif à 1 % chaque année. Les OBG ont un **rendement de jour négatif 18 années sur 20**.
- Par quartile de performance mensuelle du marché : OBG 24,42 % dans les pires mois, 20,20 % dans les meilleurs ; récessions NBER : 22,03 % (non significatif).
- Sous-groupes : OBG le plus fort chez les plus volatils (36,68 %), le plus faible chez les moins volatils (11,51 %) ; turnover haut 35,17 % ; rendement passé haut 36,19 %. Ajouter le filtre OBG améliore toute catégorie de **18,45 points** en moyenne.

### Coûts (section 5.2)
- Barème 2014 : min(7 $ forfait, 0,005 $/action avec minimum 1 $) par ordre + frais SEC section 31 de **0,00221 %** des ventes. Coût aller-retour quotidien moyen : **3,1 pb (10 000 $/titre)** et **1,5 pb (100 000 $/titre)**, donc il faut **4–8 %/an** de rendement anormal de nuit pour couvrir les coûts.
- Spread bid-ask évité en passant par les **enchères d'ouverture et de clôture** (MOC/MOO). Exclure les titres < 50 $ fait monter l'alpha après coûts (10 000 $) à 14,10 %.
- Le papier précise que ce calcul utilise les tarifs de 2014 et ne dit pas que la stratégie aurait marché il y a 20 ans avec les coûts d'alors.

### Mise en œuvre et intraday (section 6, TAQ 2010–2012)
- NASDAQ : MOO/LOO jusqu'à **9:28**, exécution à 9:30 ; MOC/LOC jusqu'à **15:50**, exécution à 16:00. NYSE : MOC/LOC avant **15:45**, MOO/LOO jusqu'à l'ouverture (le DMM peut retarder l'ouverture). Heures moyennes réelles : NASDAQ 9:30:00 / 16:00:03 ; NYSE 9:30:38 / 16:02:28. Les prix CRSP collent aux enchères TAQ 76 % (ouverture) et 98 % (clôture) du temps.
- Rendement moyen à 9:30 : **OBG +0,083 % contre IBG −0,035 %** (écart annualisé 34,5 %). **L'excès de nuit des OBG est réalisé quelques minutes avant 9:30** (pré-ouverture dominée par les professionnels).
- Après l'ouverture, l'excès baisse de 0,02 % si on vend quelques minutes plus tard et **disparaît en ~45 minutes** ; un acheteur de jour évite la perte intraday des OBG en attendant **30–45 minutes** après l'ouverture.
- Volume : OBG = **40 % du volume de pré-ouverture**, 29 % juste après l'ouverture, 17 % à la clôture, pour 15 % de la capitalisation. Enchères OBG : 1,1 M$ (ouverture) et 2,4 M$ (clôture) en moyenne par titre, 3,8 % du volume du jour.
- Liquidité : 10 % (25 %) des OBG font moins de 1 M$ (5 M$) dans les 15 premières minutes ; avec un VWAP 15 minutes, le rendement de nuit quotidien tombe de 0,083 % à **0,056 %** ; avec une horloge de volume de 5 M$, il reste à 0,084 %.

### Conclusion
« Plus faible risque, plus haut rendement la nuit ? » **Oui, mais seulement pour les actions à biais de nuit positif passé** ; après coûts, seulement pour celles à biais **significatif**. La cause des biais reste ouverte (pistes citées : semi-professionnels qui soldent le soir et rachètent le matin, particuliers et attention, pression intraday des institutionnels sur les titres momentum ; les OBG ont un volume très élevé autour de l'ouverture).

---

## [13] Overnight Returns and Firm-Specific Investor Sentiment (David Aboody, Omri Even-Tov, Reuven Lehavy, Brett Trueman)

**SSRN 2554010 · « forthcoming » Journal of Financial and Quantitative Analysis · UCLA, Berkeley, Michigan**

### Question
Le rendement de nuit (close → open) d'une action peut-il servir de **mesure du sentiment des investisseurs propre à l'entreprise** ? Prémisse (Berkman et al. 2012) : les particuliers, les plus sensibles au sentiment, passent leurs ordres hors séance pour exécution à l'ouverture → pression à l'ouverture, rendement de nuit élevé, retourné en séance.

### Données
- CRSP, **juillet 1992 (premiers prix d'ouverture CRSP) → décembre 2013** ; actions à prix > **5 $** et capitalisation > **10 M$** en fin d'année précédente.
- Rendement de nuit quotidien CTO = (Open_d − Close_{d−1}) / Close_{d−1} (ajusté splits et dividendes).
- **Semaine = mercredi de la semaine w−1 → mardi de la semaine w** (comme Lehmann 1990, Barber et al. 2009) ; rendement de nuit hebdomadaire = moyenne des rendements de nuit quotidiens × 5.
- Plus de 1 000 semaines ; t-stats sur la série des écarts hebdomadaires décile 10 − décile 1.

### Description (Table 1, déciles de rendement de nuit de la semaine w)
- Rendement de nuit hebdomadaire de **−8,16 %** (décile 1) à **+8,13 %** (décile 10) ; rendement total hebdomadaire de −2,60 % à +4,12 %.
- Pour 8 déciles sur 10, la nuit a le même signe que le total et est plus grande en valeur absolue → **retournement en séance** (comme Berkman et al.).
- Les déciles extrêmes : titres petits, jeunes, volatils, à fort book-to-market, faible E/P, fort momentum passé (en valeur absolue), moins d'institutionnels.

### 1) Persistance de court terme (Table 2)
| Semaine | Décile 1 | Décile 10 | Écart 10 − 1 | t |
|---|---|---|---|---|
| w+1 | −0,90 % | +0,86 % | **1,76 pt** | 46,0 |
| w+2 | −0,82 % | +0,67 % | 1,48 pt | 42,9 |
| w+3 | −0,76 % | +0,57 % | 1,33 pt | 38,1 |
| w+4 | −0,71 % | +0,49 % | 1,21 pt | 35,9 |
- Rendement de nuit de w+1 **strictement croissant** du décile 1 au décile 10.
- Recalculé avec les **mid-quotes** (dernier bid/ask valide avant la clôture, premier après l'ouverture, données de Berkman et al.) : résultats très proches → pas un artefact de spread.
- **Rendement total (close-to-close)** des semaines suivantes : pas monotone ; écart 10 − 1 de seulement **0,26 pt (w+1, t 4,1)**, 0,11 (t 1,9), 0,15 (t 3,0), 0,06 (t 0,8). La persistance concerne la **nuit**, pas le total.
- Contrôles par double tri (Table 3) : par bêta, écart w+1 de 1,29 à 1,9 pt ; par taille, **2,50 pt pour les plus petites** à 0,98 pt pour les plus grosses ; par book-to-market 1,34–1,8 ; par momentum 1,27–1,87 ; tous significatifs (et en régression multivariée).

### 2) Plus fort pour les titres difficiles à évaluer et peu détenus par les institutionnels (Tables 4–5)
- Écart w+1 (décile 10 − 1) entre quartile « le plus dur » et « le plus facile » : volatilité **1,99 vs 1,04 pt** ; taille **2,32 (petites) vs 0,72 pt (grosses)** ; âge 1,94 vs 1,25 ; rentabilité 2,13 vs 1,30 ; E/P 1,93 vs 0,82. Toutes les différences significatives (de 0,69 à 1,6 pt).
- Propriété institutionnelle : quartile le plus bas (5,1 % d'institutionnels) **2,36 pt** ; plus haut (~63 %) **1,07 pt** ; différence 1,28 pt significative (et sur w+2 à w+4 : 1,07 à 1,26 pt) ; tient après contrôle de la taille.

### 3) Retournement de long terme (Table 6)
- Chaque **décembre** (1992–2012), tri en déciles sur le rendement de nuit quotidien moyen du mois (≥ 15 jours), portefeuilles **équipondérés** détenus **12 mois**, alpha 4 facteurs (marché, SMB, HML, WML).
- Décile 1 (nuit la plus basse) : alpha **+0,40 %/mois** (t 2,98) ; décile 10 : −0,23 %/mois (t −1,56) ; **long décile 1 − short décile 10 : +0,62 %/mois (t 3,54), soit 7,4 %/an**.
- Les titres à forte nuit de court terme sont **surévalués** et sous-performent sur 12 mois.
- Par quartile difficile à évaluer : alpha long-short significatif dans chaque quartile « dur », de 0,37 %/mois (4,4 %/an, plus petites) à **0,81 %/mois (9,7 %/an, plus forte croissance attendue)** ; parmi les « faciles », seulement les plus rentables (0,44 %/mois, 5,3 %/an).

### 4) Application : réaction aux résultats (Table 7)
- Sentiment SENT = 1 si le rendement de nuit quotidien moyen des jours **−20 à −2** avant l'annonce est dans les **2 déciles du haut**, 0 si dans les 2 du bas (seuls ces titres sont gardés).
- Rendement ajusté du marché sur [−1, +1] = 0,0023 + 0,3249·E − 0,1861·AF **− 0,0821·SENT·AF** (t −2,93).
- Quand les investisseurs sont optimistes (nuits élevées avant l'annonce), le prix réagit **moins positivement** au résultat publié ; les résultats publiés corrigent en partie le sentiment.

### Conclusion
Les rendements de nuit ont les caractéristiques attendues d'une mesure de sentiment au niveau de l'entreprise : persistance de court terme, plus forte pour les titres difficiles à évaluer et peu institutionnels, et retournement à long terme.

### Limites pour l'usage
- Actions individuelles US, coupe transversale ; aucun coût de transaction, aucune stratégie de trading à proprement parler (portefeuilles de recherche) ; la persistance de la nuit **ne se traduit presque pas en rendement total**.

---

## [14] The Cross-Section of Intraday and Overnight Returns (Vincent Bogousslavsky)

**SSRN 2869624 · version du 14 juillet 2020 · Boston College**

### Thèse
Les arbitragistes contraints en capital réduisent leurs positions **avant la clôture** parce que tenir la nuit coûte plus cher : **contraintes institutionnelles** (marge Reg T de 50 % la nuit contre ~25 % intraday chez certains courtiers ; frais de prêt de titres et intérêts de marge facturés sur les positions détenues à la clôture) et **risque de nuit** (illiquidité, gros mouvements). Prédiction : une stratégie de correction de mispricing gagne pendant la journée mais **perd dans la dernière demi-heure** ; c'est ce qu'on observe.

### Données et construction
- Actions ordinaires US NYSE, Amex, NASDAQ (NASDAQ à partir de 1993), **1er janvier 1986 → 31 décembre 2015** (ISSM puis TAQ ; août 1987 exclu) ; prix > 5 $ et capitalisation > 100 M$ en fin de mois précédent.
- Rendements **demi-heure sur mid-quotes** pendant 9:30–16:00 ; la dernière demi-heure 15:30–16:00 utilise la dernière cotation en séance.
- **Le premier intervalle commence à 9:45** (les cotations à l'ouverture sont souvent aberrantes : ask anormalement haut → faux rendement de nuit puis faux retournement ; l'annexe donne l'exemple du titre IT les 12 et 13 octobre 2005). Donc le « rendement de nuit » va de la clôture à **9:45** (il inclut les 15 premières minutes). Filtres : on supprime la première cotation du jour et les spreads > 30 fois le spread médian du jour.
- Taux sans risque soustrait seulement de la nuit (le règlement se fait en fin de journée).
- Portefeuilles déciles (bornes NYSE), **pondérés par la capitalisation**, rééquilibrés mensuellement, sans rééquilibrage intraday. Facteur de mispricing de **Stambaugh, Yu, Yuan (2012, 2015)** (moyenne des rangs sur 11 anomalies) : long sous-évalués, short surévalués. Erreurs Newey-West 14 retards (1 jour).

### Marché
- Le portefeuille de marché gagne en moyenne **la nuit** (comme Cliff et al. 2008), sans motif marqué dans la journée (Figure 1).

### Résultat central (Table 1, facteur de mispricing, points de base par intervalle)
- Alpha **nuit +1,25 pb** (t 2,23) ; 9:45 +0,99 ; 10:00 +1,26 ; 10:30 +0,92 ; 11:00 +0,83 ; … ; 14:30 +0,47 ; 15:00 +0,23 ; **15:30–16:00 : −2,43 pb (t −10,09)**, le plus grand en valeur absolue de tous les intervalles, nuit comprise. (Rendement moyen brut de nuit : −0,04 pb, non significatif.)
- Les deux jambes perdent en fin de journée : long −1,15 pb, short +1,28 pb à 15:30 (asymétrie non significative).
- **Plus fort dans la 2e moitié de l'échantillon** : 15:30 = −1,60 pb (1986–2000) contre **−3,19 pb (2001–2015)**. L'auteur y voit des « limites à l'arbitrage haute fréquence » (HFT qui ne portent pas de positions la nuit) qui ne disparaissent pas avec l'efficience.
- La nuit : −1,13 pb (1986–2000) mais +2,28 pb (2001–2015).

### Risque de nuit (Tables 2–3)
- Variance de nuit (log, sur 100 jours) du facteur : un choc de +1 % aggrave le mispricing de ~13 pb à 15:30 (coefficient retardé d'un jour −16,60, t −2,19), soit ~**26 pb** en tout ; effet plus faible à 15:00, nul à 14:30.
- **Vendredi** : le mispricing s'aggrave en fin de journée environ **4 fois plus que le lundi** ; le facteur gagne particulièrement le lundi. La volatilité du week-end du facteur est 6,5 % plus forte que celle d'une nuit de semaine.
- En coupe : la **variance systématique de nuit** prédit positivement la nuit (2,71, t 7,9) et négativement la séance (9:45 −0,53 ; 15:30 −0,41), conforme à Hong et Wang (2000) ; l'interaction sous-évalué × risque de nuit est négative à 15:30 (−0,56, t −2,28).

### Pression sur les prix et retournement (Table 4)
- Rendements du facteur positivement autocorrélés ; après contrôle, **retournement significatif entre 15:30–16:00 et la matinée suivante** ; pas de retournement pour 15:00–15:30.

### Volume, déséquilibre, ventes à découvert (Table 5, NYSE 2005–2006, Reg SHO)
- Titres surévalués : turnover plus élevé toute la journée, pic à 15:30 (+0,58 pb ; +0,24 pb vs autres intervalles, t 3,07) ; déséquilibre d'ordres plus acheteur en fin de journée (+0,10 pb, t 2,35).
- Ventes à découvert : surévalués +6,4 à +8,9 points de % de volume vendu à découvert ; sous-évalués −4 à −9 points.
- Surévalués **difficiles à emprunter** (quintile bas de propriété institutionnelle) : volume à découvert **−5,28 points** à 15:30 par rapport aux autres intervalles (t −3,11).

### Pourquoi ne pas trader plus tôt, et peut-on exploiter le motif ? (Table 6, 2015)
- Spread effectif du short leg : ~38 pb à 9:30, ~7,2 pb à 15:30, 6,4 pb à 16:00 ; profondeur **61 % (50 %) plus haute** à 16:00 qu'à 15:30 pour le short (long) ; impact prix 60 % plus faible à 16:00.
- La variation de spread n'explique qu'un quart à un tiers de la dégradation de fin de journée.
- **Shorter le facteur à 15:30 et le racheter à 16:00 n'est pas rentable** : la variation de mispricing est **inférieure au spread** des deux jambes (avec des ordres au marché).

### Anomalies une par une (Tables 7–8, 10)
- **Rentabilité brute, volatilité idiosyncratique, émissions nettes d'actions** : positives toute la journée, **négatives dans la dernière demi-heure** (rentabilité brute 15:30 : −1,23 pb, t −6,6) ; plus fort récemment ; non expliqué par la taille ou l'illiquidité (Fama-MacBeth).
- **Taille et illiquidité** : fortement positives dans la dernière demi-heure (~3,5 pb, t > 10) ; une bonne partie s'explique par des effets de clientèle (le coefficient d'illiquidité à 15:30 tombe de 0,99 à 0,37 avec le contrôle).
- Rendement moyen de nuit (long-short, pb) : **bêta (bas − haut) −7,44**, **volatilité idiosyncratique −7,62**, book-to-market −2,93, illiquidité −2,76, émissions nettes −1,82, taille −1,05 ; **momentum +5,12** (le momentum est une anomalie de nuit, mais pas sur 1986–1992). Le betting-against-beta gagne en séance et perd la nuit (comme Hendershott et al. 2019).
- 5 des 6 autres anomalies de Stambaugh et al. (croissance des actifs, émissions composites, distress O-score, actifs opérationnels nets, investissements/actifs, ROA) ont un alpha de fin de journée négatif et significatif (ex. émissions composites −2,91 pb, t −12).
- **Placebo** : 10 000 stratégies aléatoires ; 1 057 « significatives » ; elles gagnent surtout la nuit et ne reproduisent pas ces motifs intraday de façon stable.

### Heure de l'« ouverture » (Table 11, 1993–2015)
- Le choix du prix d'ouverture change les conclusions : avec la mid-quote de **9:35**, le rendement de nuit du facteur de mispricing baisse (−0,15 pb) et celui de l'ouverture monte (+1,49 pb) ; pour la taille et l'illiquidité, la nuit augmente quand on échantillonne plus tôt. Un « tug of war » nuit/jour n'apparaît qu'avec la mid-quote de 9:35. **L'ouverture doit être traitée avec précaution.**
- Momentum : nuit +6,9 / +6,7 / +6,3 / +7,5 pb (9:35 / 9:40 / 9:45 / VWAP) ; bêta −7,3 ; volatilité idiosyncratique −8,3 à −9,6.

### Clientèles (Table 9)
- Le rendement moyen de l'année passée **dans le même intervalle** prédit fortement le rendement de cet intervalle (nuit : 5,61, t 20,4), mais ne fait pas disparaître le motif de mispricing.
- La propriété institutionnelle prédit négativement la nuit et le début de matinée, positivement l'après-midi.

### Conclusion et limites
- Plusieurs anomalies se corrigent pendant la journée puis se dégradent en fin de séance à cause des arbitragistes qui réduisent leurs positions avant la nuit ; à interpréter comme du mispricing plutôt que du risque.
- Le motif de fin de journée est **trop petit pour être traité seul** avec des ordres au marché ; actions individuelles US (pas indices ni futures).

---

## [15] Intraday Market Making with Overnight Inventory Costs (Tobias Adrian, Agostino Capponi, Michael Fleming, Erik Vogt, Hongzhong Zhang)

**SSRN 2844881 · non daté (données jusqu'au 29 juin 2018) · FMI, Columbia, Fed de New York, Citadel**

### Question
Sur le marché des Treasuries, une grande part de la liquidité vient des **PTF** (principal trading firms, proches des HFT) qui ont peu de capital et veulent **finir la journée à plat**. Que fait cette contrainte de fin de journée aux prix, aux spreads et à l'impact prix pendant la journée ?

### Faits institutionnels (section 2)
- Les PTF font plus de la moitié du volume sur les plateformes électroniques de Treasuries et ~80 % du trafic de messages (Joint Staff Report 2015).
- Position de fin de journée médiane : **4,4 % du volume quotidien pour les PTF contre 19,0 % pour les banques-dealers** ; position intraday maximale médiane 15,3 % vs 28,3 %.
- Au Royaume-Uni (Benos et Sagade 2016), les HFT finissent la journée avec une position ~5 % de leur volume intraday.
- Les risques intraday sont gérés par des limites d'exposition plutôt que par des marges ; les marges et le financement (repo, prêt de titres, haircuts) pèsent surtout sur les positions de nuit.

### Modèle (sections 3–5)
- Un teneur de marché monopolistique (la PTF) fixe bid et ask en continu sur [0, T] ; ordres d'achat et de vente qui arrivent selon des processus de Poisson ; demande et offre linéaires en prix ; prix fondamental brownien.
- Objectif : maximiser la richesse de fin de journée **moins un coût quadratique η·I_T² sur l'inventaire restant à la clôture** (pas de coût d'inventaire intraday).
- Solutions en forme fermée ; prix bid et ask décroissants en l'inventaire (avec un stock long, la PTF baisse son ask pour vendre et baisse son bid pour moins acheter) ; spread toujours entre p et 2p.
- **Corollaire 4 : le spread bid-ask croît strictement avec le temps (vers la clôture)**, croît avec le coût de nuit η, décroît avec l'intensité des ordres.
- **L'impact prix (pente prix/inventaire) devient plus raide à l'approche de la clôture.**
- Volatilité : plus d'ordres réduit la volatilité si l'on est loin de la clôture, mais l'augmente près de la clôture quand l'impact est fort ; si η est très élevé, la volatilité instantanée **chute brièvement juste avant la clôture** (la PTF ne traite presque plus).
- Bien-être : dans les marchés à fort flux d'ordres, le coût de nuit change peu le surplus des acheteurs/vendeurs et la valeur de la PTF ; dans les marchés à faible flux, il pèse beaucoup.

### Données empiriques (section 6)
- **BrokerTec** (plateforme interdealer, ~80 % du trading électronique interdealer des Treasuries on-the-run), données anonymisées de tous les messages, **2 janvier 2013 → 29 juin 2018 (1 376 jours)**, horodatage à la milliseconde puis à la microseconde (avril 2015).
- Titre étudié : **Treasury 10 ans on-the-run** (40,7 Md$/jour, ~16 000 trades/jour en moyenne).
- Plateforme ouverte 22–23 h/jour ; analyse sur les heures de New York **7:30 → 17:30**.
- Inventaire des teneurs de marché approché par **−(volume net cumulé)** (achats agressifs − ventes agressives, le côté initiateur est fourni par BrokerTec). On commence à 9:00 pour éviter les annonces de 8:30.

### Résultats
- Relation **négative et significative** entre variation de prix (mid) et variation d'inventaire dans chaque demi-heure de 9:00 à 17:30 ; constantes proches de zéro.
- **La pente est nettement plus raide entre 17:00 et 17:30** : différences (17:00–17:30 moins chaque demi-heure antérieure) entre **−0,76 et −1,37** (prix en pb du nominal, inventaire en centaines de millions de dollars), toutes avec p = 0,00 (Table 1).
- **Spread bid-ask** : ~**1,7 pb du nominal** de 7:30 à 17:00, puis **élargissement brutal** près de la clôture ; le spread de 17:25–17:30 est plus large que celui de 9:00–9:05 presque tous les jours de l'échantillon. Pics ponctuels à 8:30 et 10:00 (annonces macro), 13:00 (clôture des adjudications), 14:00/14:15 (FOMC).
- **Vendredi** (prochaine séance à 49–50 heures ; du lundi au jeudi, la séance de nuit rouvre 1 à 2 heures après) : impact prix de 17:00–17:30 **environ 3 fois plus grand** que les autres jours ; élargissement du spread de fin de journée aussi plus fort. (L'heure de réouverture est fixée sur l'ouverture de Tokyo à 8:30 locale, sans heure d'été au Japon, d'où un écart variable.)
- **Part des PTF** (approchée par les trades à moins de 0,01 s du précédent, avril 2015 – juin 2018) : stable dans la journée puis **chute près de la clôture** ; la tenue de marché passe aux dealers à bilan plus large.
- Autres explications discutées : volume plus faible en fin de journée (le volume de 17:00–17:30 est le plus bas des heures de New York) ; **clôture des futures et options du CBOT à 17:00** (on observe une dégradation discrète de la liquidité à 17:00), mais les spreads s'élargissent aussi juste avant 17:00 et juste avant 17:30, surtout pour les gros ordres.

### Conclusion
L'aversion des teneurs de marché à garder de l'inventaire la nuit fait **monter les spreads et l'impact prix à l'approche de la clôture**, plus encore le vendredi.

### Limites
- Marché des Treasuries (10 ans), un seul titre ; pas de prédiction de rendement directionnel ; données anonymisées (inventaire approché par le flux net).

---

## [16] Overnight Public Information, Order Placement and Price Discovery During the Pre-Opening Period (Fariborz Moshirian, Huong Giang (Lily) Nguyen, Peter Kien Pham)

**SSRN 1785682 · version de juin 2012 · UNSW, La Trobe University**

### Question
Les annonces d'entreprises publiées **pendant la nuit** (entre la clôture et l'ouverture) rendent-elles plus efficients les **prix indicatifs d'ouverture** de la pré-ouverture, et changent-elles l'agressivité des ordres ? Les nouvelles de nuit sont-elles intégrées plus vite que celles de séance ?

### Marché étudié : la Bourse australienne (ASX, système SEATS, marché d'ordres pur)
- **Pré-ouverture 7:00 → 10:00** (pas d'échanges, on peut entrer, modifier, annuler des ordres gratuitement, le carnet et le prix indicatif sont visibles) ; **ouverture 10:00 → 10:09** par groupes de titres selon la première lettre du code ; séance continue 10:09 → 16:00 ; pré-clôture 16:00 → 16:10 ; clôture 16:10 → 16:12.
- Algorithme d'ouverture : (1) prix qui maximise le volume exécutable ; (2) puis qui minimise le déséquilibre achat/vente ; (3) prix le plus haut (bas) si le surplus est à l'achat (vente) ; (4) sinon, la clôture de la veille.
- Particularité : par la règle de cotation ASX 3.1 et le Corporations Act (art. 674), **toute annonce passe d'abord par l'ASX**, horodatée, avant tout autre média → horaire exact de la nouvelle.

### Données
- Constituants du **S&P/ASX 100**, **1er juillet 2005 → 30 juin 2006** (un an : carnets trop volumineux), SIRCA (trades, ordres, profondeur, annonces).
- **10 417 annonces** : 5 222 (50,13 %) la nuit, 5 195 (49,87 %) en séance ; ~0,23 annonce de nuit et 0,22 de jour par titre et par jour. Les annonces tombent surtout **entre 9:00 et 10:00** et **entre 15:30 et 17:00**.
- Prix indicatif d'ouverture recalculé en rejouant l'algorithme ASX, minute par minute de 7:00 à l'ouverture. Rendement indicatif = ln(prix indicatif / clôture de la veille).
- Rendement indicatif moyen 0,018 % (jours sans annonce de nuit) et 0,006 % (avec) ; close-to-close 0,046 % et 0,062 %.

### Activité de pré-ouverture (Tables 2–5)
- **63,61 %** des ordres de pré-ouverture arrivent **entre 9:30 et l'ouverture** ; 73,09 % de ceux reçus après 9:00 arrivent **après 9:50**.
- Nouveaux ordres 49,81 %, modifications 50,19 % ; après 9:30, les modifications dominent (38,35 % contre 25,26 %), la taille des nouveaux ordres baisse et celle des modifications augmente (apprentissage, ou ordres « appâts » retirés avant l'ouverture).
- Ordres les plus agressifs (prix au-delà du prix indicatif, « niveau 3 ») : **> 52 %** des ordres (hors annulations), surtout dans la dernière demi-heure.
- Carnet **croisé** (meilleur bid > meilleur ask) **95,3 %** du temps en pré-ouverture ; spread positif 3,06 %, nul 1,65 %.
- **Part du prix de la journée** (WPC) : **clôture → ouverture 31 %** (dont clôture → 9:30 : **17 %**, 9:30 → ouverture : **14 %**), ouverture → clôture **69 %**.

### Efficience des prix indicatifs (Figures 3–4, méthode de Biais, Hillion, Spatt 1999)
- Régression, minute par minute, du rendement close-to-close sur le rendement indicatif (et son interaction avec une indicatrice « au moins une annonce de nuit »).
- Pas de motif avant 9:30. Coefficient du rendement indicatif ~**0,4–0,5 entre 9:30 et 9:50**, bond dans les **10 dernières minutes**, **~0,9 à l'ouverture**, **1,0 environ 15 minutes après l'ouverture** ; plus tard dans la séance il reste au-dessus de 1 puis revient vers 1 à la clôture.
- **L'interaction avec les annonces de nuit est positive et significative** (de 9:30 à l'ouverture) : avec des nouvelles de nuit, le prix indicatif prédit mieux la clôture.
- Robustesse avec l'**indice NYSE Composite de la veille** (le plus corrélé aux titres de l'échantillon, devant S&P 500, NASDAQ, FTSE, CAC, DAX, Nikkei, Hang Seng) : son coefficient est **positif** (l'information de New York entre dans la pré-ouverture australienne) et l'effet des annonces locales reste. Les annonces de séance (même jour ou veille) ne changent rien.

### Agressivité des ordres (Table 6, probit ordonné)
- Plus il y a d'annonces de nuit cumulées, plus les nouveaux ordres et les révisions « vers l'avant » ou « à prix inchangé » sont agressifs (effet marginal sur les nouveaux ordres de niveau 3 : **+0,38 %** par annonce ; niveau 1 : −0,12 %).
- Pour les révisions « vers l'arrière » et les annulations, l'effet va dans le sens d'un retrait des ordres agressifs (cohérent avec apprentissage **ou** manipulation, mais ces ordres sont rares et petits juste avant l'ouverture).
- Le rendement du NYSE de la veille influence aussi l'agressivité (significatif au moins à 10 %) ; profondeur du même côté +2,01 %, côté opposé −1,27 % (sur les nouveaux ordres de niveau 3) ; plus le carnet est croisé, moins les nouveaux ordres sont agressifs.

### Nouvelles de nuit vs de séance : résultats annuels (Tables 7–8, 2003–2007)
- Annonces de résultats annuels (I/B/E/S, surprise = écart à la prévision moyenne des analystes) : le papier annonce **423** annonces, dont **319 (75 %) la nuit** et **114 en séance**, 254 positives et 179 négatives (ces sous-totaux font 433 ; incohérence du papier).
- Portefeuille long surprise positive / short surprise négative, rendements en excès de l'indice par tranches de 15 minutes (l'intervalle 0 d'une annonce de nuit = de la clôture de la veille à l'ouverture).
- **Annonces de nuit** : rendement de **+0,15 %** à l'intervalle 0, encore significatif à +1 (premier quart d'heure), puis plus rien (−0,03 % à +0,03 %).
- **Annonces de séance** : +0,10 % à l'intervalle 0 et significatif jusqu'à +3 (**environ une heure** pour intégrer), avec plus de fluctuations ensuite.
- Les auteurs n'excluent pas un effet de sélection (les entreprises publieraient la nuit les annonces plus importantes).

### Conclusion
La pré-ouverture n'est pas que du bruit : l'apprentissage des prix s'y fait (surtout la dernière demi-heure), d'autant plus qu'il y a des nouvelles de nuit ; publier les nouvelles hors séance aide la formation du prix ; « les rendements d'une journée peuvent être largement prédits par les rendements close-to-open ».

### Limites
- Un an de données, 100 grandes valeurs australiennes, 2005–2006 ; pas de stratégie de trading.

---

## [17] Effective Extension of Trading Hours (Kotaro Miwa)

**SSRN 2839631 · non daté (cite Miwa et Ueda 2016 « in press ») · Tokio Marine Asset Management**

### Question
Quelle extension des horaires de cotation (séance **pré-marché**, séance **after-hours**, ou les deux ; et de quelle durée) améliore réellement l'efficience et la stabilité des prix, alors que peu d'investisseurs y participent ? (Contexte : la Bourse de Tokyo envisage d'étendre ses horaires ; aux US, pré-marché 8:00–9:30 et after-hours 16:00–18:30 selon le papier ; Barclay et Hendershott 2004 : moins de 5 % du volume par unité de temps after-hours.)

### Méthode : **simulation multi-agents (pas de données réelles)**
- Modèle de Brock et Hommes (1998) étendu (Miwa et Ueda 2016) : 4 types d'investisseurs (fondamentalistes, suiveurs de tendance, optimistes, pessimistes) qui changent de stratégie selon les profits récents ; prix d'équilibre walrasien ; valeur fondamentale en marche aléatoire log-normale.
- **Risque de nuit** : au dernier pas avant leur arrêt de trading, les investisseurs ont une aversion au risque plus forte, croissante avec la durée de la fermeture.
- Journée = 24 pas d'une heure ; séance régulière = 6 pas (T1 = « ouverture », T6 = « clôture ») ; after-hours de 0 à 9 h ; pré-marché de 0 à 9 h ; le reste fermé.
- Seule une fraction **Re ∈ {10, 20, 30, 50, 70 %}** des investisseurs trade pendant les séances étendues.
- 100 investisseurs (résultats identiques avec 200), 100 simulations (hors extrêmes) ; le texte dit 1 000 jours de trading, la Table 1 semble indiquer 250 (incohérence de l'extraction ou du papier). Paramètres retenus d = 0,2, g = 1,25, 5, 1, mise à jour 0,2, calés pour reproduire le U du volume et de la volatilité intraday, les queues épaisses et le regroupement de volatilité (conditions : suiveurs de tendance forts, investisseurs biaisés, mise à jour modérée des stratégies, aversion au risque de nuit).
- Critères : écart |log(prix/fondamental)| (efficience), volatilité en séance et ratio volatilité à l'ouverture (clôture) / reste de la séance (stabilité), ratio volume à l'ouverture (clôture) / reste (concentration).

### Résultats
**Pré-marché seul**
- Avec assez de participants (Re ≥ 30 %), réduit l'écart au fondamental, la volatilité et la concentration à l'ouverture ; avec peu de participants (Re ≤ 20 %), les **augmente**. Plus la séance est longue, pire c'est.
- **Exception : un pré-marché court (1 heure) améliore l'efficience et la stabilité quel que soit le nombre de participants**, sans aggraver la concentration. Une **période de pré-ouverture** (ordres accumulés puis fixing unique) s'interprète comme un pré-marché d'un pas : le résultat soutient ce mécanisme.
- Pourquoi : au début du pré-marché, les fondamentalistes ramènent le prix vers la valeur ; ensuite l'illiquidité l'en éloigne progressivement, donc une séance longue arrive à l'ouverture avec un écart plus grand.
- Aucun effet sur la clôture.

**After-hours seul**
- Réduit la concentration et l'instabilité **à la clôture** si assez de participants (moins d'investisseurs portent le risque de nuit à la clôture de la séance régulière).
- Mais dégrade l'efficience et la stabilité en séance, **surtout à l'ouverture**, et augmente la concentration à l'ouverture quand la participation est faible : à la fin de l'after-hours, prix extrêmement instables et loin du fondamental (risque de nuit + peu de participants). Plus long = pire. Moins bénéfique que le pré-marché.

**Les deux ensemble**
- Améliorent la clôture ; mais même courtes, les deux séances combinées **élargissent** l'écart au fondamental ; les inconvénients de l'after-hours dépassent les avantages du pré-marché.

**Gains des participants aux séances étendues**
- Pas de différence significative de gain de richesse ni de volume entre participants et non-participants ; avec des coûts de trading plus élevés hors séance, peu d'incitation à y trader → cause possible de la faible liquidité observée.

### Conclusion
L'extension d'horaires a une faiblesse structurelle (illiquidité) qui peut dégrader la séance régulière ; un **pré-marché court** est la seule extension bénéfique sans contrepartie ; l'after-hours est probablement nuisible vu la faible participation réelle.

### Limites
- Uniquement de la simulation, paramètres calés sur des faits stylisés ; aucune donnée de marché ; aucune stratégie.
