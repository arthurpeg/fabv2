# Résumés détaillés : 2e récolte de papiers overnight (SSRN)

*Rédigé le 2026-10-29 à partir de la lecture intégrale des 15 PDF fournis (texte, tableaux et annexes, extraits avec pdftotext). La numérotation [n] reprend celle de [papiers_ssrn_overnight_2_2026-10-29.md](papiers_ssrn_overnight_2_2026-10-29.md). Tout ce qui suit est extrait des papiers. Quand un chiffre est illisible dans l'extraction du PDF ou que le papier se contredit, c'est signalé. Les heures sont celles du papier. Les rendements sont dans l'unité du papier (souvent en % par jour).*

Papiers de la récolte **non fournis** (donc non résumés) : [10] Firm-Specific News, Extended-Hours Trading, and Variances Over Trading and Nontrading Periods (SSRN 476281), [14] Liquidity Provision in the Overnight Foreign Exchange Market (SSRN 882835).

### Index
| # | Papier | Actifs / période | En une ligne (d'après le papier) |
|---|---|---|---|
| [1] | Market-Level Tug-of-War (Tao, Wese Simen, Zhao) | Actions US, 1992–2022 | Les jours où beaucoup d'actions montent la nuit puis baissent en séance (> 28 %), le CAPM échoue ; il tient les autres jours |
| [2] | Dispersion of Opinions (Berkman et al.) | 3 000 plus grandes actions US, 1996–2004 | Ouverture trop haute corrigée dans la 1re heure, seulement pour les titres à fort désaccord et vente à découvert contrainte ; toujours sous les coûts |
| [3] | Heterogeneity… INFO-Z et PTA (Chen, Stivers, Sun) | Actions US hors microcaps, 1997–2021 | Asymétrie d'information forte → momentum de nuit et retournement en séance plus forts (horizon mensuel) |
| [4] | Anchoring Bias (Kim, Goh) | Actions US, 1993–2020 | La prime AB_NR (équipondérée) vient surtout des titres loin de leur plus haut 52 semaines |
| [5] | 4-Factor Model (Kakushadze) | Top 2 000 actions US, 2009–2014 | Prix, séance de la veille, range 21 j et volume 21 j expliquent la nuit en coupe ; retournement intraday ~1 cent/action sans coûts |
| [6] | GARCH-Copula (Kang, Babbs) | 15 ETF US, 2006–2011 | La séance dépend négativement de la nuit qui précède (moyenne, variance, corrélation) ; nuit à queues plus épaisses |
| [7] | After-Hours Volatility (Chen, Yu, Zivot) | 4 actions NASDAQ, 2001–2004 | Seule la variance du preopen 8:00–9:30 ET améliore la prévision de la volatilité de séance |
| [8] | Coupled Component GARCH (Linton, Wu) | Dow 30 1991–2016, déciles CRSP 1992–2015 | Le poids de la volatilité de nuit monte pour les grandes capitalisations ; nuit à ν ≈ 3 |
| [9] | Realized Variances and Overnight Returns (Opschoor, Lucas) | 93 actions S&P 500 + 19 indices, 2001–2018 | Le ratio variance totale / variance de séance varie (pics en crise) ; utile pour la VaR des actions en période agitée |
| [11] | Jumps Day or Night (Jeon, McCurdy, Szaura) | Actions US, 2000–2020 | Saut de nuit 1 nuit sur 165, surtout lié aux news hors séance et au volume after-hours |
| [12] | Stop-Loss and Overnight Gaps (Arratia, Dorador) | 30 actions NYSE, horaire, 2017 (simulation) | Le stop suiveur en % fixe améliore le Sharpe mais baisse l'espérance et le Sortino en marché haussier |
| [13] | Round-Number Anchoring Blue Ocean (Lim) | 30 titres, Blue Ocean ATS, 2025–2026 | Taille d'ordre de nuit la plus fréquente : 20 actions ; descriptif, sans prix |
| [15] | What Crosses Borders (Kinoshita) | 9 marchés Asie + 17 secteurs TOPIX, 2009–2024 | Le gap d'ouverture asiatique se prévoit avec la séance au comptant du S&P 500, pas avec sa nuit ni les futures après 16:00 |
| [16] | Intraday Seasonality Filtering (Laakkonen) | EUR/USD 5 min, 1999–2004 | Profil intraday du FX et effet des annonces (2 h) ; méthode FFF recommandée |
| [17] | Extending Trading Hours (Lin, WFE) | Structure de marché | US actions en 23/5 dès décembre 2026 (clôture 20:00 ET) ; décalage de financement CLS pour les ordres 18:00–20:00 ET |

### Ce qui revient d'un papier à l'autre (constaté dans les papiers, sans extrapolation)
- **Queues épaisses de la nuit** : degrés de liberté ≈ 3 pour la nuit des actions individuelles dans [8] et [9] (≈ 5 pour les indices dans [9]), 4 à 9,6 pour la nuit des ETF dans [6] (FXE 15,4).
- **Retournement nuit → séance** : présent en coupe sur les actions ([1], [2], [3], [4], [5]) ; mais en série temporelle sur les portefeuilles de taille pondérés, une nuit positive est suivie d'une séance plutôt positive ([8], sauf le décile des plus grandes, non significatif) ; mélangé selon les ETF dans [6].
- **Coûts** : [2] montre explicitement que l'effet reste sous les coûts (spread d'ouverture moyen 98 pb) ; [5] et [12] travaillent sans coûts ; [15] précise que la précision directionnelle n'est pas un résultat de trading.
- **Information de nuit utile pour la séance** : volatilité du preopen ([7]), variance de nuit qui monte en crise ([9]), séance au comptant de NY pour l'ouverture de l'Asie ([15]), news hors séance pour les sauts de nuit ([11]).

---

## [1] Market-Level Tug-of-War and Asset Pricing (Tao, Wese Simen, Zhao)

**SSRN 5036288 · version du 30 septembre 2026 · Bristol / Liverpool / ESCP**

### Question
Le CAPM échoue-t-il partout, ou seulement certains jours ? Les auteurs construisent un indicateur de « tug-of-war » (lutte nuit/jour) au niveau du marché pour classer chaque jour en jour **bruité (n-day)** ou **calme (q-day)**, puis testent le CAPM séparément sur chaque type de jour.

### Données
- CRSP, toutes les actions ordinaires US (share code 10 ou 11) de l'AMEX, du NASDAQ et du NYSE.
- **Juillet 1992 – décembre 2022** (CRSP ne donne le prix d'ouverture qu'à partir de 1992).
- Filtres : on retire toute observation sans prix d'ouverture ou de clôture, et toute observation avec un rendement intraday **ou** overnight **égal à zéro** (filtre appliqué au calcul du tug-of-war et aux actifs testés ; résultats robustes si appliqué seulement au tug-of-war, non tabulé).
- Taux sans risque = T-bill 1 mois ; marché = indice CRSP pondéré par la capitalisation (site de K. French). TED spread (FRED, s'arrête au 28 janvier 2022), VIX (Bloomberg), indice d'aversion au risque de Bekaert, Engstrom et Xu (2022).

### Définitions exactes
- Rendement intraday : R_day = P_close / P_open − 1.
- Rendement overnight (Lou et al. 2019) : R_night = (1 + R_close-to-close) / (1 + R_day) − 1, avec R_close-to-close pris directement dans CRSP (donc ajusté des dividendes et splits).
- **Tug-of-war d'une action** : ToW(i,t) = 1 si R_night > 0 **et** R_day < 0, sinon 0.
- **Tug-of-war du marché** : ToW_m(t) = moyenne des ToW(i,t) sur toutes les actions présentes ce jour-là (part des actions qui montent la nuit puis baissent en séance).
- **Règle de classement** : n-day si ToW_m(t) > **0,28** (médiane de l'échantillon complet, égale à la moyenne), q-day sinon. La médiane est calculée **sur tout l'échantillon** (ex post, le papier le dit : « ex-post »).
- Pourquoi seulement « nuit positive puis séance négative » et pas l'inverse : les particuliers sont actifs à l'ouverture, les institutionnels le reste de la journée, et les frais de vente à découvert overnight sont élevés, donc les particuliers peuvent difficilement ouvrir des positions courtes.

### Statistiques descriptives (Table 1)
- ToW_m : moyenne 0,28 ; écart-type 0,12 ; AR(1) = −0,06, AR(2) = −0,02, AR(3) = −0,02 (quasiment aucune persistance) ; min 0,03 ; max 0,86 ; médiane 0,28.
- Part de n-days par jour de semaine : lundi 52,42 %, mardi 50,60 %, mercredi 49,02 %, jeudi 48,58 %, vendredi 49,54 % (pas d'effet jour de semaine).
- Par mois : entre 46,29 % (novembre) et 53,21 % (juin) (pas d'effet saisonnier).
- Figure 2 : dans la première partie de l'échantillon, la part de n-days dépassait généralement 50 % ; elle est plus faible récemment, avec un minimum autour de 40 %.
- Variables d'état (n-day vs q-day) : **rendement excédentaire moyen du marché −0,05 % vs +0,12 % par jour** ; TED 0,45 vs 0,45 ; VIX 19,30 vs 19,97 ; aversion au risque 2,98 vs 3,11. Seule différence notable : le rendement du marché.
- Jours macro : 50,63 % sont des n-days ; jours non macro : 49,91 % n-days. Jours LEAD : 47,92 % n-days ; non-LEAD : 46,29 % n-days (le texte dit que 53,71 % des non-LEAD sont des q-days).
- Le bootstrap mentionne **3 720 n-days** dans l'échantillon.

### Méthode de test
- Actifs testés principaux : **10 portefeuilles triés par bêta, pondérés par la capitalisation**. Bêta pré-classement : régression sur **252 jours** de rendements close-to-close (minimum 126 observations), à chaque fin de mois ; portefeuilles tenus le mois suivant, rééquilibrés mensuellement.
- Fama-MacBeth : bêta post-classement de chaque portefeuille sur les 252 derniers jours à la fin du mois m ; chaque jour du mois m+1, régression en coupe des rendements excédentaires sur une constante et ce bêta → γ (constante) et λ (prime de marché). On fait la moyenne sur les n-days ou sur les q-days. Erreurs Newey-West, noyau de Bartlett à **10 retards**. Seuil de significativité 5 %.
- Le test du CAPM retenu n'est pas le signe de la pente mais deux restrictions : (i) **pente moyenne = rendement excédentaire moyen réalisé du marché** sur ces jours (« slope restriction ») ; (ii) **constante moyenne = 0**. Plus un test joint.
- Régression poolée : effets fixes jour, erreurs clusterisées par jour, avec une indicatrice n-day et son interaction avec le bêta.

### Résultats principaux (Table 2, 10 portefeuilles VW)
| | γ (constante) | λ (pente) | R² ajusté | Rm − Rf moyen | λ − (Rm − Rf) |
|---|---|---|---|---|---|
| n-day | 0,06 (t 3,15) | **−0,13 (t −4,23)** | 40,46 % | −0,05 (t −3,23) | **−0,08 (t −3,60)** |
| q-day | −0,00 (t −0,25) | **0,15 (t 5,15)** | 45,66 % | 0,12 (t 5,39) | **0,02 (t 1,22)** |

- Tous jours confondus (Table A1) : pente plate λ = 0,01 (t 0,56), constante 0,03 (t 2,28) → CAPM rejeté sur l'échantillon total.
- Test joint : non rejeté sur q-days (p = 0,41), rejeté sur n-days (p = 0,00).
- Pooled : tous jours, constante 0,05 (t 3,25), pente −0,01 (t −0,33). Avec indicatrice : constante q-days −0,00 (t −0,01), pente q-days 0,14 (t 4,48) ; différence de constante n − q = 0,10 (t 3,58) ; différence de pente n − q = −0,30 (t −7,65).
- Conclusion : **la ligne de marché des titres (SML) monte les jours calmes et descend les jours bruités** ; le CAPM tient les q-days (environ la moitié des jours) et échoue les n-days.

### Robustesse
- **Portefeuilles équipondérés** (Table A2) : n-days λ = −0,25 (t −8,17), λ − (Rm−Rf) = −0,20 (t −9,34) ; q-days λ = 0,15 (t 5,70), λ − (Rm−Rf) = 0,03 (t 1,65).
- **Actions individuelles** (Table A3) : q-days λ = 0,10 (t 5,68), écart −0,02 (t −1,78) non rejeté ; n-days λ = −0,16 (t −9,23), écart −0,11 (t −8,57). Avec contrôles taille, book-to-market, momentum (12-1 mois) : n-days écart −0,08 (t −5,80), q-days −0,01 (t −0,86).
- **45 portefeuilles** (10 bêta + 25 taille×B/M + 10 industries, critique de Lewellen et al. 2010) (Table A4) : n-days λ = −0,17 (t −5,71), écart −0,12 (t −5,46) ; q-days λ = 0,15 (t 5,06), écart 0,03 (t 1,38).
- **Seuils alternatifs** : 0,25 (probabilité théorique 25 % d'avoir nuit + / jour −) (Table A5 : n-days écart −0,10, t −5,21 ; q-days 0,04, t 1,61) ; 70e percentile (Table A6 : n-days λ = −0,31, écart −0,16, t −5,29 ; q-days écart 0,01, t 0,43). Résultats inchangés.
- **Version directe sur l'indice** (Table A7) : n-day = jour où l'indice CRSP VW lui-même a R_night > 0 et R_day < 0. **96,34 % des n-days de cette version directe sont aussi des n-days de la version agrégée.** n-days : λ = −0,42 (t −10,75), Rm−Rf = −0,31 (t −18,32), écart −0,11 (t −3,49) ; q-days : λ = 0,14 (t 6,29), Rm−Rf = 0,16 (t 8,73), écart −0,02 (t −1,27).
- **Bruit de microstructure** : moindres carrés pondérés (poids 1 + R(t−1), Asparouhova et al. 2010) sur actions individuelles (Table A8) : peu de différence.
- **Bootstrap conditionnel** : 1 000 pseudo-échantillons de 3 720 n-days tirés avec remise, en ne gardant que ceux dont le rendement moyen du marché est **positif** : la prime estimée reste négative, en moyenne **−0,12**. Le signe négatif n'est donc pas mécanique.

### Mécanisme proposé : sur-correction (Akbas et al. 2022)
- La nuit est dominée par des traders « de bruit » contraints en levier (frais de vente à découvert élevés la nuit), qui tradent à l'ouverture ; la journée par les institutionnels/arbitragistes.
- Quand **beaucoup d'actions montent la nuit le même jour**, les arbitragistes en déduisent que c'est du bruit et corrigent trop fort en séance, en sous-estimant la part d'information fondamentale. Comme les traders de bruit se concentrent sur les **titres à bêta élevé**, la sur-correction est la plus forte sur ceux-ci (Figure 1 : l'écart q-day − n-day augmente avec le bêta, la pente négative des n-days vient surtout des bêtas élevés).

Prédictions testées :
1. **Découpage nuit / séance des n-days** (Table 3, 45 portefeuilles) :
   - Nuit : λ = 0,36 (t 19,10), Rm−Rf = 0,31 (t 38,38), écart **+0,06 (t 5,28)** → déjà une déviation la nuit (pression des traders de bruit).
   - Séance : λ = −0,55 (t −20,45), Rm−Rf = −0,37 (t −27,19), écart **−0,18 (t −9,06)** → rejet beaucoup plus fort en séance (sur-correction).
   - Séance des q-days : λ = 0,38 (t 14,45), Rm−Rf = 0,37 (t 21,98), écart 0,01 (t 0,32) → **le CAPM tient en séance les jours calmes**. Donc l'échec intraday n'est pas général (contrairement à Hendershott et al. 2020), il est propre aux n-days.
   - Rendements excédentaires nuit/séance : on retire 17,5/24 du taux sans risque journalier pour la nuit et 6,5/24 pour la séance (Lou et al. 2024).
2. **Jours de news macro** (IPP, chômage, taux des fed funds ; Savor et Wilson 2014) (Table 4) : n-days macro : λ = −0,08 (t −0,98), écart −0,07 (t −1,37), non significatif ; n-days autres jours : λ = −0,18 (t −5,74), écart −0,12 (t −5,20). Sur les autres jours, q-days : λ = 0,12 (t 3,72), écart 0,01 (t 0,64).
3. **Jours LEAD** (mardi à jeudi de la 1re semaine de la saison de résultats, si ≥ 50 sociétés du S&P 500 publient cette semaine ; Chan et Marsh 2022) (Table 5) : n-days LEAD : λ = 0,12 (t 0,69), écart 0,19 (t 1,42) non rejeté ; n-days non-LEAD : λ = −0,15 (t −3,77), écart −0,12 (t −4,14). Non-LEAD q-days : écart 0,01 (t 0,24).
4. **Sentiment** (Baker-Wurgler, mois optimiste si l'indice de fin du mois précédent > 0) (Table 6) : n-days pessimistes λ = −0,13 (t −3,02), écart −0,11 (t −3,54) ; n-days optimistes **λ = −0,26 (t −7,84)**, écart −0,13 (t −5,77). En période optimiste, q-days λ = 0,23 (t 6,52), écart 0,04 (t 1,55). Pente plus négative quand le sentiment est haut.
5. **Retournement inverse** (nuit négative puis séance positive, agrégé de la même façon) : pente fortement positive (λ = 0,14, t 6,37) et restriction non rejetée (écart −0,014, t −0,78), non tabulé. Seul le schéma « nuit + puis séance − » est associé à l'échec du CAPM.

### Explications alternatives écartées
- **Absence de news** : 50,09 % des jours non macro et 53,71 % des non-LEAD sont des q-days ; en excluant les jours macro ou LEAD, le résultat tient.
- **Effet heure de la journée (Hendershott et al. 2020)** : rejet aussi la nuit des n-days, et pas en séance les q-days.
- **Bêta spéculatif (Hong et Sraer 2016)** : désaccord = écart-type des prévisions de croissance à long terme des analystes, agrégé pondéré par le bêta ; mois de fort désaccord si le désaccord du mois précédent > médiane. Fort désaccord : n-days écart −0,09 (t −4,04), q-days −0,01 (t −0,47). Faible désaccord, n-days : écart **−0,15 (t −4,12)**, donc plus fort qu'en fort désaccord, ce qui contredit Hong-Sraer (Table 7).
- **Compression des bêtas (Andrei et al. 2023)** : bêtas estimés sur n-days et q-days quasi identiques (Figure 3, sur la diagonale).

### À retenir (d'après le papier)
- La classification est **ex post et contemporaine** : on ne sait qu'un jour est un n-day qu'à la clôture de ce jour (il faut l'ouverture et la clôture de toutes les actions). Le papier ne fait aucune prévision ni stratégie de trading ; c'est un test d'asset pricing.
- Seuil = médiane de l'échantillon complet (0,28), robuste à 0,25 et au 70e percentile.
- La version « indice seul » (CRSP VW avec nuit > 0 et séance < 0) recoupe 96,34 % des n-days.
- Les n-days ont un rendement de marché moyen de −0,05 %/jour contre +0,12 % pour les q-days (par construction en partie, puisque n-day = beaucoup de séances négatives).

---

## [2] Dispersion of Opinions, Limits to Arbitrage, and Overnight Returns (Berkman, Koch, Tuttle, Zhang)

**SSRN 1214564 · version de juin 2009 · Auckland / Kansas / Sharjah / Missouri State** (version de travail de « Paying Attention », JFQA 2012)

### Question
Le rendement de nuit positif suivi d'un retournement en séance vient-il d'un **prix d'ouverture trop haut** ? Et ce prix haut s'explique-t-il par les modèles de désaccord (Miller 1977) : quand le désaccord est fort et que la vente à découvert est contrainte, les optimistes achètent à l'ouverture et les pessimistes restent dehors.

### Données et définitions
- **Les 3 000 plus grandes actions US** (capitalisation au 1er juillet de chaque année), **1996–2004** (9 ans, **2 267 jours**). TAQ, environ 2 491 à 2 585 titres par jour en moyenne (400 à 500 petits titres sans cotations).
- Prix d'ouverture = **milieu de fourchette (midquote) des premières cotations valides après 9:30** (taille non nulle des deux côtés) ; clôture = midquote des **dernières cotations valides avant 16:00**. Ajusté des splits et dividendes. Les midquotes évitent le rebond bid-ask ; robustesse avec les prix de transaction et avec le midquote pris exactement à 9:30.
- Rendements en log : nuit cto = log(open_t / close_{t−1}), séance otc = log(close_t / open_t). **Rendements anormaux** = rendement brut − rendement du portefeuille pondéré par la capitalisation de tout l'échantillon sur la même période.
- Filtres : cotations anormales retirées, ask > 1,5 × bid retiré ; transaction à plus de 1 $ hors de la fourchette retirée ; on retire le jour si spread négatif, spread d'ouverture ou de clôture > 5 $ ou > 30 % du midquote, demi-spread effectif > 2,50 $ ou > 15 %, ou si l'ouverture est à plus de 25 % au-dessus (ou en dessous) **à la fois** de la clôture précédente et de la clôture suivante.
- Désaccord « absolu » (toute la journée) : Abs_TURN = rotation quotidienne (% des actions en circulation) ; Abs_VOL = écart-type des rendements 30 minutes de la journée.
- Désaccord « relatif » à l'ouverture : Rel_TURN = (rotation de la 1re heure − rotation horaire du reste de la journée) / rotation horaire de la journée entière ; Rel_VOL = écart-type des rendements 30 min de la 1re heure − celui du reste de la journée. Toutes ces mesures sont **moyennées sur les 20 jours précédents** (robuste à 10 et 30 jours).
- Contraintes de vente à découvert : détention institutionnelle INST (13F, trimestre précédent ; 0 si absent) et short interest relatif RSI (mensuel). Coûts : spread % à l'ouverture, à la clôture, demi-spread effectif (trades appariés aux cotations avec 1 seconde de décalage).
- Tests : moyenne en coupe chaque jour, puis moyenne de série temporelle ; t-stat sur l'écart-type de la série des moyennes quotidiennes (évite la corrélation en coupe, Bernard 1987).

### Statistiques descriptives (Table 1)
| % par jour | nuit brute | séance brute | nuit − séance | après coûts | nuit anormale | séance anormale | DIFF anormal | après coûts | ctc anormal | oto anormal |
|---|---|---|---|---|---|---|---|---|---|---|
| Moyenne | **0,080** (t 7,4) | **−0,049** (t −2,4) | 0,130 | **−0,766** | 0,020 (t 4,0) | −0,068 (t −7,0) | 0,088 | −0,807 | −0,048 | 0,021 (t 1,9) |
| Médiane | 0,031 | −0,048 | 0,079 | −0,681 | −0,029 | −0,066 | 0,038 | −0,722 | −0,094 | −0,032 |

- Stratégie « long la nuit, short la séance » sur toutes les actions : **+13,0 pb/jour avant coûts, −76,6 pb après** (coût = moyenne des spreads d'ouverture et de clôture).
- Rotation moyenne 0,72 % ; Abs_VOL 0,61 % ; la 1re heure a **39 % de rotation de plus** que les autres heures ; Rel_VOL = +0,014 %. INST moyen 45,6 % ; RSI 3,0 %. **Spread moyen à l'ouverture 0,98 %, à la clôture 0,78 %**, demi-spread effectif 0,21 %. Capitalisation moyenne 4,45 Md$.
- Corrélations (Spearman) : les 4 mesures de désaccord sont positivement corrélées à la nuit ; 3 sur 4 négativement à la séance. INST : corrélé négativement à la nuit, positivement à la séance (inverse pour RSI). Les spreads : positifs avec la nuit, négatifs avec la séance.

### Profil de prix intraday (Figures 1–5)
- Ratio midquote à l'instant T / midquote moyen de la journée (moyenne des points 30 min en excluant les 30 premières et 30 dernières minutes). Échantillon limité aux titres qui ouvrent **exactement à 9:30** (1 929 titres/jour).
- **L'ouverture est significativement au-dessus de la moyenne de la journée**, le prix baisse pendant les **60 premières minutes** vers la moyenne, passe sous la moyenne au milieu de journée, remonte dans les dernières minutes ; la clôture finit au-dessus de la moyenne mais pas significativement. **Pas de clôture anormalement basse** → le retournement vient de l'ouverture trop haute, pas d'une clôture trop basse.
- Ratios d'ouverture (Table 9C) pour les actions US : 9:30 = 1,00079 ; 9:35 = 1,00072 ; 9:40 = 1,00063 ; 9:45 = 1,00056 ; 9:50 = 1,00049 ; 9:55 = 1,00041 ; 10:00 = 1,00037 (soit environ +8 pb à l'ouverture, encore +3,7 pb à 10:00).
- Par quintile d'INST : les deux quintiles à faible INST ont une ouverture plus haute et une clôture plus basse ; plus INST monte, plus le profil « tourne » (ouverture vers 1,0, clôture au-dessus de 1,0).

### Résultats en portefeuilles (double tri 3×3, contrôle de la taille)
Chaque jour : tri en terciles de taille (capitalisation moyenne 20 jours), puis dans chaque tercile, tri indépendant par désaccord relatif (moyenne 20 jours) et par INST (trimestre précédent). Rendements anormaux en % par jour. Pour chaque colonne d'INST, les trois chiffres vont du désaccord relatif faible au désaccord relatif fort.

**Table 2 (tout l'échantillon, ~280 titres par case)** : le phénomène n'existe pas partout.
- Nuit, mesure rotation : INST faible −0,02 / 0,02 / **0,08** ; INST moyen −0,03 / 0,00 / 0,04 ; INST fort −0,03 / 0,00 / 0,02. Fort − faible désaccord : 0,10 (t 12,8), 0,07, 0,05.
- Nuit, mesure volatilité : ligne « désaccord fort » = **0,10** / 0,04 / 0,01 ; fort − faible : 0,07 (t 8,7), 0,03, 0,01.
- Séance, rotation : INST faible −0,03 / −0,08 / **−0,16** ; moyen −0,01 / −0,05 / −0,11 ; fort −0,02 / −0,05 / −0,09. Volatilité : INST faible −0,04 / −0,06 / **−0,20** ; moyen −0,02 / −0,06 / −0,10 ; fort −0,02 / −0,07 / −0,06.
- Conclusion : nuit ≈ +10 pb et séance ≈ −20 pb seulement pour **désaccord relatif fort + INST faible** ; la plupart des 9 cases n'ont pas le schéma.

**Table 3 (tiers des titres au désaccord absolu le plus fort, ~95 titres par case)** :
- Nuit, rotation : INST faible 0,05 / 0,13 / **0,19** ; moyen 0,04 / 0,10 / 0,13 ; fort 0,00 / 0,04 / 0,06. Volatilité : INST faible 0,14 / 0,09 / **0,21** ; moyen 0,10 / 0,06 / 0,14 ; fort 0,06 / 0,05 / 0,08.
- Séance, rotation : INST faible −0,08 / −0,19 / **−0,31** ; moyen −0,06 / −0,16 / −0,23 ; fort −0,05 / −0,09 / −0,15. Volatilité : INST faible −0,09 / −0,26 / **−0,37** ; moyen −0,07 / −0,21 / −0,27 ; fort −0,07 / −0,17 / −0,17.
- Presque toutes les cases ont nuit > 0 et séance < 0 ; le retournement en séance est **plus grand** que le gain de nuit → rendement 24 h négatif (somme significativement négative, non tabulé). Les titres à désaccord absolu faible ou moyen n'ont pas le schéma (ou beaucoup plus petit), non tabulé.
- +20 pb/jour = 1 %/semaine = 52 %/an (chiffres des auteurs) ; −30 pb ≈ −1 % tous les 3 jours ≈ −75 %/an.

**Table 4 (50 % des titres au demi-spread effectif le plus élevé, puis tiers au désaccord absolu le plus fort, ~47 titres par case)** :
- Nuit, rotation INST faible : 0,09 / 0,19 / **0,27** ; volatilité INST faible : 0,20 / 0,15 / **0,31**.
- Séance, rotation INST faible : −0,08 / −0,21 / **−0,40** ; volatilité INST faible : −0,09 / −0,37 / **−0,49**.

**Table 5 (50 % spread le plus élevé, puis 20 % au short interest le plus élevé, puis tiers au désaccord le plus fort, ~9 titres par case)** :
- Nuit, rotation INST faible : 0,16 / 0,30 / **0,37** ; volatilité INST faible : 0,33 / 0,32 / **0,40**.
- Séance, rotation INST faible : −0,27 / −0,42 / **−0,57** ; volatilité INST faible : −0,17 / −0,67 / **−0,78**.
- Conclusion des auteurs : environ **+40 pb la nuit (100 %/an) et −57 à −78 pb en séance**, mais **toujours à l'intérieur des coûts** (spread moyen d'ouverture 98 pb).

### Régressions (Table 6, Fama-MacBeth sur 2 267 jours, rangs en déciles recentrés entre −0,5 et +0,5)
| | nuit (rotation) | séance (rotation) | nuit (volatilité) | séance (volatilité) |
|---|---|---|---|---|
| constante | 0,01 | −0,07 | 0,02 | −0,07 |
| Rel_Disp b1 | **0,14** (t 14,3) | **−0,17** (t −11,6) | 0,02 | −0,10 |
| Abs_Disp b2 | 0,13 (t 8,1) | −0,15 (t −4,6) | 0,21 | −0,27 |
| INST b3 | −0,08 | 0,10 | −0,06 | 0,07 |
| INST × Rel b4 | −0,07 (t −6,3) | 0,14 (t 8,6) | −0,08 | 0,22 |
| INST × Abs b5 | −0,05 (t −5,2) | −0,01 (t −0,3) | −0,13 | 0,09 |
| Taille b6 | −0,15 | 0,10 | −0,05 | −0,01 |
| R² ajusté | 0,031 | 0,033 | 0,036 | 0,058 |

Lecture : passer du décile le plus bas au plus haut de désaccord relatif (rotation) = +14 pb la nuit et −17 pb en séance pour un titre à INST médian. Les interactions avec INST ont le signe opposé : l'effet est atténué quand INST est élevé. Sur les sous-échantillons à spread élevé puis short interest élevé, les coefficients gardent leur signe et grossissent (non tabulé).

### Robustesse (Table 7 : long désaccord relatif fort − short faible, dans le tiers au désaccord absolu fort ; colonnes INST faible / fort)
- Base : nuit 0,14 / 0,06 (rotation), 0,07 / 0,02 (vol) ; séance −0,23 / −0,10 (rotation), −0,29 / −0,10 (vol).
- Médianes au lieu des moyennes, prix de transaction au lieu des midquotes, exclusion des titres < 5 $ (moyenne 3 mois) : résultats similaires (ex. prix de transaction : nuit 0,15 / 0,07 ; séance −0,24 / −0,11).
- **NASD vs NYSE** : plus fort au NASD (séance, mesure volatilité, INST faible : −0,45 contre −0,04 au NYSE), mais présent au NYSE.
- **Petites vs grandes capitalisations** (quintiles) : plus fort pour les petites (nuit rotation 0,17 contre 0,09 ; séance vol −0,36 contre −0,17), mais existe chez les grandes.
- **PIN** (asymétrie d'information, Easley et al. 2002) : un peu plus fort pour PIN élevé, ce qui contredit la théorie de l'asymétrie d'information de nuit (Hong et Wang 2000), qui prédit au contraire une ouverture basse.
- **Risque de liquidité de nuit** (sensibilité des variations de spread du titre aux variations de spread du marché pendant la nuit, estimée par trimestre, ≥ 44 jours) : pas de différence entre quintiles faible et fort ; **aucune clôture anormalement basse**, même pour les titres à fort risque de liquidité (Figure 3). L'explication par une prime de liquidité de nuit est rejetée.

### Stabilité (Table 8)
- Avant et après le **1er mars 2000** : présent dans les deux sous-périodes (nuit rotation INST faible 0,14 et 0,14 ; séance −0,20 et −0,26).
- Par année : 22 cases sur 36 significativement positives la nuit, 21 sur 36 négatives en séance ; aucun résultat significatif de mauvais signe. Années fortes : 1999–2001 (séance vol INST faible −0,79 en 1999, −0,65 en 2000, −0,48 en 2001). Années plus faibles : 2002–2004 (séance rotation INST faible −0,10, −0,12, −0,25).

### Durée de la nuit
- **Lundi** (Table 9) : nuit et retournement plus grands le lundi. Exemple (tiers à désaccord absolu fort, ligne désaccord relatif fort, rotation, INST faible/moyen/fort) : séance lundi −0,50 / −0,39 / −0,31 contre −0,25 / −0,18 / −0,11 les autres jours ; différences de −0,21 à −0,28 selon les cases, toutes significatives à 1 %. La nuit du lundi est plus forte dans 3 cas sur 6 à 5 % (5 sur 6 à 10 %). Le lundi combine **ouverture plus haute et clôture plus basse** (Figure 4). La clôture du vendredi n'est pas plus basse que les autres jours (pas de prime de liquidité du week-end).
- **ADR** (Table 9C, Figure 5) : ADR de fuseaux américains (Canada, Amérique latine, 10 titres/jour) : profil identique aux actions US (ratio 1,00081 à 9:30). ADR d'Asie-Pacifique (21/jour) : 1,00053 ; **ADR européens (51/jour) : 1,00032**. Différence US − Europe significative à chaque intervalle de 5 min de la 1re demi-heure. Plus la période sans cotation entre la clôture du marché d'origine et l'ouverture US est courte, plus le biais d'ouverture est faible → pas une explication de microstructure de l'ouverture US.

### À retenir (d'après le papier)
- Le phénomène vient d'une **ouverture trop haute** qui se corrige surtout dans la **première heure**, pas d'une clôture trop basse.
- Il est **concentré** sur les titres à désaccord fort (rotation/volatilité élevées sur 20 jours), à forte activité relative en 1re heure, à faible détention institutionnelle, fort short interest et spread élevé. Ailleurs, peu ou pas d'effet.
- Il est **toujours inférieur aux coûts de transaction** (spread d'ouverture 98 pb en moyenne) : les auteurs ne présentent pas de stratégie rentable.
- Plus fort le **lundi**, et plus faible quand la nuit sans cotation est plus courte.
- Échantillon ancien (1996–2004), effet plus faible après 2001.

---

## [3] Heterogeneity in Overnight-versus-Intraday Stock-Return Behavior with Asymmetric Information and 52-week Price Anchoring (Chen, Stivers, Sun)

**SSRN 7443340 · 1re version 25 mars 2025, version du 2 octobre 2026 · Old Dominion / Louisville**

### Question
Le schéma de Lou, Polk et Skouras (2019) au niveau **mensuel** (momentum des rendements de nuit d'un mois sur l'autre, momentum des rendements de séance, et retournement croisé nuit ↔ séance) varie-t-il selon deux caractéristiques des titres : l'**asymétrie d'information** (INFO-Z) et la position du prix par rapport à son **historique de 52 semaines** (PTA) ?

### Données
- Toutes les actions ordinaires NYSE, AMEX, NASDAQ, **1997–2021** (période imposée par les données intraday disponibles). CRSP (rendements, prix d'ouverture et de clôture), TAQ (PIN), Compustat.
- Séance : P_close / P_open − 1 ; nuit : (1 + R_close-to-close) / (1 + R_séance) − 1 (Lou et al. 2019). **Rendement mensuel de nuit (de séance) = cumul des rendements quotidiens de nuit (de séance) du mois calendaire.**
- **Exclusions** : titres sous 5 $ et titres du quintile de taille NYSE le plus bas (microcaps). Portefeuilles **pondérés par la capitalisation**.

### Variables de conditionnement
- **INFO-Z** : calculé chaque mois sur les 12 derniers mois à partir de 3 mesures : PIN (Easley et al. 2002, TAQ nettoyé selon Holden-Jacobsen 2014, classement Ellis et al. 2000), volatilité idiosyncratique (modèle Carhart 4 facteurs, rendements quotidiens), spread de Corwin-Schultz (2012) (à partir des hauts et bas quotidiens CRSP). Chaque mesure est winsorisée 1 %/99 %, transformée en score Z ; moyenne des 3 scores ; puis **résidu d'une régression sur l'illiquidité d'Amihud (12 mois) et la rotation (12 mois)** (pour séparer information et illiquidité). Résultats similaires sans ce nettoyage.
- **PTA** (Chen et al. 2026) : moyenne du ratio prix / plus haut 52 semaines (PTH) standardisé et du ratio prix / plus bas 52 semaines (PTL) standardisé, standardisés en coupe chaque mois. Évite le cas d'un titre à range étroit qui serait à la fois proche du haut et du bas. Le PTA fait mieux que le PTH seul ici.
- Corrélation moyenne INFO-Z / PTA en coupe : **0,199** (médiane 0,200 ; quartiles 0,116 et 0,276). INFO-Z est corrélé à −0,508 avec la taille (log) et +0,407 avec le bêta ; PTA quasiment pas (0,043 et 0,027).

### Méthode
- **Calendrier** : INFO-Z ou PTA mesuré à la fin du mois **t−2** ; tri à la fin de **t−1** ; rendement du mois **t**.
- Double tri **séquentiel 5×5** (points de coupure NYSE) : quintiles d'INFO-Z (ou PTA), puis dans chaque quintile, quintiles de rendement de nuit (ou de séance) du mois t−1.
- Rendements excédentaires (− T-bill 1 mois) ; alphas FF6+2 (Fama-French 5 facteurs + momentum Carhart + 2 facteurs comportementaux de Daniel, Hirshleifer et Sun 2020) et Q+2 (q-factor de Hou-Xue-Zhang + les 2 facteurs comportementaux). Newey-West **12 retards**.
- Fama-MacBeth mensuels avec contrôles de Lou et al. (2019) mesurés en t−2 (moyennes mobiles exponentielles des rendements nuit/séance avec demi-vie 60 mois, rendement 12 mois, taille, book-to-market, bêta 12 mois avec 3 retards, rotation 12 mois, ROE, croissance des actifs, émissions, accruals discrétionnaires), effets fixes 48 industries, winsorisation 0,5 %/99,5 %.
- Sentiment : terciles du Baker-Wurgler mesuré en t−2.

### Résultats INFO-Z (Tables 1–5) — en % par mois
**Momentum de nuit** (tri sur la nuit de t−1, rendement de nuit en t) :
| Quintile INFO-Z | perdants (Q1) | Q2 | Q3 | Q4 | gagnants (Q5) | Gagnants − perdants |
|---|---|---|---|---|---|---|
| Faible | −0,11 | −0,04 | 0,21 | 0,49 | 0,97 | **1,08** (t 3,99) |
| 2 | −0,02 | 0,06 | 0,23 | 0,64 | 1,34 | 1,36 |
| 3 | 0,06 | 0,46 | 0,77 | 1,17 | 1,92 | 1,86 |
| 4 | 0,21 | 0,75 | 0,87 | 1,32 | 2,22 | 2,01 |
| Fort | 0,38 | 0,84 | 1,34 | 1,95 | **3,47** | **3,09** (t 5,06) |
| Fort − faible | 0,49 | 0,88 | 1,13 | 1,46 | 2,50 (t 6,26) | **2,01** (t 5,05) |
- Alphas de la différence de momentum : 1,64 % (t 4,76) FF6+2 et 1,65 % (t 4,87) Q+2.
- Le rendement de nuit moyen **augmente avec INFO-Z** dans tous les quintiles de rendement passé (moyenne des 25 portefeuilles : +0,86 %/mois la nuit).

**Momentum de séance** (tri sur la séance de t−1, rendement de séance en t) : peu de variation avec INFO-Z. Faible INFO-Z : −0,46 / 0,39 / 0,18 / 0,48 / 0,82 (écart 1,28, t 4,73) ; fort INFO-Z : −2,15 / −0,62 / −0,59 / −0,53 / −0,36 (écart 1,79, t 3,53) ; différence 0,51 (t 1,27), **non significative**. Par contre le rendement de séance **baisse avec INFO-Z** : différences fort − faible de −1,68, −1,01, −0,77, −1,01, −1,18 selon le quintile (en moyenne −1,13, t ≤ −3,00 partout).

**Sous-périodes** (Table 2 : 1997:01–2009:06 et 2009:07–2021:12) : momentum de nuit croissant avec INFO-Z dans les deux moitiés (plus fort dans la première) ; rendement de séance décroissant avec INFO-Z dans les deux ; momentum de séance : croissant avec INFO-Z dans la 1re moitié, légèrement négatif et non significatif dans la 2e.

**Robustesse** :
- Tris indépendants : différence de momentum de nuit 1,54 % (t 4,28) (de 1,18 à 2,72 %).
- Tri 3×10 : momentum de nuit 1,36 % (INFO-Z faible), 1,98 % (moyen), 3,43 % (fort).
- INFO-Z simple sans nettoyage d'illiquidité : 1,93 % (t 4,77).
- Chaque composante seule : volatilité idiosyncratique 1,54 % (t 4,71), PIN 1,47 % (t 4,62), spread 1,36 % (t 5,54).
- Par taille (Table 3, terciles) : grandes capitalisations : momentum de nuit 1,10 % (INFO-Z faible) contre 2,57 % (fort), différence 1,47 % (t 4,26) ; moyennes 1,47 % (t 3,55) ; petites 1,69 % (t 4,02).

**Retournement croisé** (Table 4) : tri sur la **nuit** de t−1, rendement de **séance** en t : −1,06 % (t −4,93) pour INFO-Z faible contre **−2,79 % (t −7,27)** pour INFO-Z fort ; différence −1,73 % (t −6,15). Tri sur la séance de t−1, rendement de nuit en t : relation seulement marginale avec INFO-Z. Tris indépendants : −1,11 % contre −2,43 %, différence −1,32 % (t −5,34). Sous-périodes : −1,67 % contre −4,26 % (1re moitié) et −0,45 % contre −1,32 % (2e moitié).

**Fama-MacBeth** (Table 5) : sans interaction, nuit(t) sur nuit(t−1) = **8,03** (t 7,70), nuit(t) sur séance(t−1) = −5,42 (t −5,48) ; séance(t) sur nuit(t−1) = **−9,42** (t −9,64), séance(t) sur séance(t−1) = 3,35 (t 3,87). L'interaction INFO-Z × nuit(t−1) est positive pour la nuit ; INFO-Z seul prédit une nuit plus haute. En séance, l'interaction INFO-Z × séance(t−1) est aussi positive (plus faible) ; l'effet niveau négatif d'INFO-Z sur la séance ne résiste pas aux contrôles.

### Résultats PTA (Tables 6–10) — en % par mois
- **Momentum de séance décroissant avec PTA** : gagnants − perdants = **2,42 %** pour PTA faible contre **1,04 %** pour PTA fort ; différence **−1,38 %** (p < 0,1 %), alphas similaires. Sous-périodes : −2,08 % (t −3,20) puis −0,69 % (t −2,12). Tris indépendants : −1,15 % (t −3,10). Par taille : grandes 2,10 % contre 0,71 %, différence −1,39 % (t −3,40) ; moyennes −0,41 % (t −1,14, non significatif) ; petites −1,04 % (t −2,62).
- **Momentum de nuit** : légèrement croissant avec PTA (alphas significatifs seulement à 10 %) ; plus net en tris indépendants et en Fama-MacBeth ; seulement dans la 2e moitié en sous-périodes.
- **Rendement de nuit moyen croissant avec PTA** : en moyenne +0,89 %/mois (fort − faible PTA), contre +1,29 % pour INFO-Z ; 0,86 % et 0,94 % dans les deux moitiés.
- **Retournement croisé** (Table 9) : tri sur la séance de t−1, rendement de nuit en t : **−2,70 % (t −4,07) pour PTA faible contre −1,37 % (t −3,89) pour PTA fort**, différence 1,33 % (t 2,63). Tri sur la nuit de t−1, rendement de séance en t : −2,25 % contre −2,26 %, aucune différence. Indépendants : −2,50 % contre −1,30 % (différence 1,20 %, t 3,05). 1re moitié : −4,91 % contre −2,38 % (p < 1 %) ; 2e moitié : différence non significative (les perdants de séance à PTA fort ont une nuit très haute, 2,18 %).
- Fama-MacBeth (Table 10) : momentum de séance plus faible quand PTA est élevé ; retournement nuit / séance(t−1) plus faible quand PTA est élevé ; l'effet niveau de PTA sur la nuit disparaît avec tous les contrôles.

### Portefeuilles « coins » (section 6.5)
- INFO-Z : le coin **INFO-Z fort + gagnants de nuit** fait le résultat : nuit suivante **+3,47 %/mois** (contre 0,97 % pour INFO-Z faible) et séance suivante **−2,13 %/mois** (contre −0,24 %). Moyennes des 25 portefeuilles : +0,86 % la nuit, −0,09 % la séance.
- PTA : le coin **PTA fort + gagnants de séance** fait le résultat : séance suivante **−0,50 %** (contre +0,49 % pour PTA faible) et nuit suivante **+1,25 %** (contre −0,33 %). Ce coin a une continuation croisée (pas un retournement) ; dans la 2e moitié sa nuit moyenne est de 1,82 %.
- Les portefeuilles de titres à PTA élevé sont plus de 3 fois plus gros en capitalisation (d'après Chen et al. 2026) : les auteurs en déduisent que les titres très illiquides ne pilotent pas les résultats.

### Sentiment (Table 11, terciles Baker-Wurgler en t−2)
- Momentum de nuit fort INFO-Z contre faible INFO-Z : 3,87 % contre 1,33 % (sentiment haut), 4,03 % contre 1,41 % (moyen) ; différence > 2,5 % ; seulement 0,90 % en sentiment bas.
- Momentum de séance PTA fort contre faible : 1,43 % contre 3,12 % (haut), 0,91 % contre 2,80 % (moyen) ; différence −1,7 à −1,9 % ; seulement −0,64 % (non significatif) en sentiment bas.

### Contrôles des autres explications (Table 12)
- LMQ = moyenne mensuelle du déséquilibre d'ordres de détail attendu dans la 1re demi-heure (canal de Lu, Malliaris et Qin 2023) ; JPW = moyenne mensuelle des rendements de séance positifs passés (extrapolation, Jones, Pyun et Wang 2024) ; ABNR = fréquence anormale, par rapport à l'historique du titre, des jours « nuit > 0 puis séance < 0 » dans le mois (Akbas et al. 2022). Variables standardisées, mesurées en t−1.
- L'interaction INFO-Z × nuit(t−1) reste positive (p < 1 %) ; aucune interaction LMQ, JPW ou ABNR n'est significative. LMQ et JPW seuls prédisent mieux le **niveau** du rendement de nuit qu'INFO-Z (qui perd sa significativité en niveau).
- L'interaction PTA × séance(t−1) reste négative (p < 5 %) ; JPW (négatif pour la séance, positif pour la nuit) et ABNR seuls sont très significatifs en niveau.
- Interactions avec taille, book-to-market et bêta (Table A13) : n'enlèvent rien ; résultats INFO-Z et PTA même un peu plus forts.

### À retenir (d'après le papier)
- Horizon **mensuel** et **actions individuelles** (pas d'indice) ; c'est un papier d'asset pricing en coupe, pas une stratégie testée avec coûts.
- Les titres à forte asymétrie d'information (petits, bêta élevé, PIN/spread/volatilité idiosyncratique élevés) ont **une nuit plus forte et une séance plus faible en moyenne**, un momentum de nuit plus fort et un retournement en séance plus fort après une bonne nuit.
- Un titre proche du haut de son range 52 semaines (PTA élevé) a un momentum de séance plus faible et un retournement de nuit plus faible après une bonne séance.
- Les effets sont plus forts en **sentiment élevé** et dans la **première moitié** de l'échantillon (1997–2009).

---

## [4] Overnight Returns, Daytime Reversals, and Anchoring Bias (Kim, Goh)

**SSRN 4482812 · juin 2023 · KAIST / Pusan National University · préprint non relu par des pairs (15 pages, dont 5 de tableaux)**

### Question
La prime AB_NR d'Akbas et al. (2022) (les titres qui ont souvent « nuit positive puis séance négative » rapportent plus le mois suivant) dépend-elle de la distance du prix à son **plus haut 52 semaines** (ancrage, George et Hwang 2004) ?

### Hypothèse des auteurs
Loin du plus haut 52 semaines, les traders de bruit de nuit voient de la « marge de hausse » et poussent fort le prix la nuit ; les arbitragistes de jour sur-corrigent ; les titres à AB_NR élevé deviennent sous-évalués et rapportent plus ensuite. Près du plus haut, moins de pression de nuit, moins de sur-correction, prime plus faible.

### Données et variables (annexe)
- CRSP, actions ordinaires (share codes 10 et 11) NYSE, AMEX, NASDAQ, **mai 1993 – décembre 2020**. Données quotidiennes et mensuelles uniquement.
- Séance RET_OC = clôture / ouverture − 1 ; nuit RET_CO = (1 + RET close-to-close) / (1 + RET_OC) − 1 (Lou et al. 2019).
- **NR(i,t)** = part des jours du mois t avec nuit > 0 **et** séance < 0 ; **PR(i,t)** = part des jours avec nuit < 0 et séance > 0. Il faut **au moins 15 jours de cotation** dans le mois.
- **AB_NR** = NR du mois rapporté (« normalisé ») à la **moyenne de NR sur les 12 mois précédents** ; même chose pour AB_PR.
- **NH** = prix de fin de mois / plus haut des **clôtures quotidiennes** du début du mois t−11 à la fin du mois t (ajusté des distributions avec le facteur CRSP).
- Contrôles : bêta (Scholes-Williams/Dimson, marché t−1, t, t+1), taille (log), book-to-market (log), momentum (rendement t−12 à t−2), volatilité idiosyncratique (résidus FF3 quotidiens du mois), rotation mensuelle, illiquidité d'Amihud, rendement du mois précédent, rendements nuit et séance composés du mois (RETCO_M, RETOC_M).

### Statistiques (Table 1, déciles d'AB_NR)
- AB_NR va de 0,27 (décile bas) à 1,89 (décile haut) ; AB_PR va de 1,23 à 0,77.
- Dans le mois de formation, le décile bas a une séance composée de 0,13 et une nuit de −0,07 ; le décile haut une séance de −0,08 et une nuit de +0,09 (unités non précisées dans le tableau).
- Corrélations : AB_NR avec la nuit du mois +0,310, avec la séance du mois −0,179, avec AB_PR −0,265 ; NH avec le momentum +0,350.

### Résultats
**Tri simple en déciles d'AB_NR (Table 2, détention 1 mois)** :
- **Équipondéré** : du décile bas (0,55 %/mois) au décile haut (1,37 %/mois) ; haut − bas = **0,83 % (t 5,37)**, alpha 4 facteurs 0,70 (t 5,02), alpha 5 facteurs 0,74 (t 4,78).
- **Pondéré par la capitalisation** : 0,69 % → 0,95 % ; haut − bas = **0,27 % (t 1,27), non significatif** ; alphas 0,09 et 0,14 non significatifs. Cohérent avec Akbas et al. selon les auteurs.

**Double tri indépendant NH × AB_NR (Table 3, quintiles, équipondéré)** :
| Quintile NH | AB_NR Q1 | Q2 | Q3 | Q4 | Q5 | Q5 − Q1 | alpha 4F | alpha 5F |
|---|---|---|---|---|---|---|---|---|
| 1 (loin du plus haut) | 0,07 | 0,28 | 0,27 | 0,83 | 1,14 | **1,08** (t 5,50) | 0,93 | 1,06 |
| 2 | 0,31 | 0,57 | 0,63 | 0,88 | 1,26 | 0,95 (t 6,23) | 0,87 | 0,89 |
| 3 | 0,68 | 0,76 | 1,00 | 1,01 | 1,37 | 0,69 (t 5,61) | 0,63 | 0,65 |
| 4 | 0,78 | 1,02 | 1,03 | 1,16 | 1,31 | 0,54 (t 4,65) | 0,45 | 0,52 |
| 5 (près du plus haut) | 0,82 | 1,01 | 1,05 | 1,06 | 1,15 | **0,33** (t 2,83) | 0,28 | 0,33 |
| Près − loin | | | | | | **−0,75** (t −4,23) | −0,66 (t −3,26) | −0,74 (t −3,29) |
- La prime décroît de façon monotone quand le prix se rapproche du plus haut 52 semaines. Pas de version pondérée par la capitalisation pour le double tri.

**Fama-MacBeth mensuels (Table 4, Newey-West 12 retards)** : avec contrôles (modèle 6), AB_NR = 0,142 (t 5,92), **AB_NR × NH = −0,113 (t −4,88)**, AB_PR = −0,012 (non significatif), AB_PR × NH = 0,031 (non significatif), séance du mois RETOC_M = −0,263 (t −4,13), nuit du mois RETCO_M = −0,021 (non significatif), RETOC_M × NH = 0,193, RETCO_M × NH = 0,266 (t 7,27), NH = 0,048 (non significatif). Lecture des auteurs : effet d'AB_NR = 0,029 (non significatif) pour un titre à 1 écart-type au-dessus de la moyenne de NH, 0,255 pour un titre à 1 écart-type en dessous. Le texte dit que NH est standardisé implicitement par cette lecture, mais le papier ne le précise pas ailleurs.

**Sentiment (Table 5, mois de sentiment Baker-Wurgler au-dessus / en dessous de la médiane)** : seuls les alphas sont donnés.
- Sentiment haut : alpha 4F de la prime AB_NR de 1,29 (loin du plus haut) à 0,35 (près) ; différence **−0,94 (t −3,14)** (5F : −1,11, t −3,94).
- Sentiment bas : de 0,68 à 0,20 ; différence **−0,48 (t −1,72)**, non significative à 5 % (5F : −0,44, t −1,59).
- Le texte présente −0,94 et −0,48 comme les différences de prime ; dans le tableau ce sont les alphas 4 facteurs.

### Incohérences dans le papier (signalées telles quelles)
- L'introduction et la section 3.1 disent que « les titres à AB_NR élevé sous-performent », alors que le résumé, l'hypothèse et tous les tableaux montrent qu'ils **surperforment** (décile haut − décile bas positif).
- La prime est décrite comme « la différence entre le décile le plus bas et le plus haut », mais les tableaux affichent « 10 − 1 » positif, c'est-à-dire haut − bas.

### À retenir (d'après le papier)
- Données **mensuelles en coupe** sur actions individuelles, sans coûts de transaction, en **équipondéré** ; la prime AB_NR simple n'est pas significative en pondéré par la capitalisation.
- La prime est surtout présente pour les titres **loin de leur plus haut 52 semaines** et en **sentiment élevé**.
- Papier très court, non relu, sans tests de robustesse au-delà de ces 5 tableaux.

---

## [5] 4-Factor Model for Overnight Returns (Kakushadze)

**SSRN 2511874 · 19 octobre 2014, révisé le 4 juin 2015 · Quantigic Solutions / UConn / Free University of Tbilisi · note courte (13 pages + tableaux)**

### Objet
Proposer un modèle à 4 facteurs pour expliquer **en coupe** le rendement de nuit des actions US, construit uniquement à partir des données quotidiennes ouverture, haut, bas, clôture et volume (pas de données fondamentales ni tick). Principe invoqué : « Horizon Decoupling Principle » : ce qui se passe à un horizon très court n'est pas affecté par les quantités de long terme (value, croissance changent tous les trimestres), donc on les exclut.

### Définitions exactes
- **Rendement de nuit** : R(i,s) = ln(ouverture ajustée du jour s / clôture ajustée du jour précédent). Prix ajustés des splits et dividendes.
- Régression en coupe chaque jour : R(i,s) = Σ_A β(i,A) f(A,s) + ε(i,s), sans constante séparée (la constante est une colonne de 1 dans les β).
- **int** (« bêta de marché ») : β = 1 pour tous les titres. Pas de vrai bêta, jugé trop bruité à court horizon. Neutralité par rapport à int = neutralité dollar.
- **prc** (analogue de la taille) : ln(clôture **ajustée** de la veille). Variante **rprc** : ln(clôture **non ajustée** de la veille), pour prouver qu'il n'y a pas de regard vers le futur via les ajustements. Le nombre d'actions en circulation est exclu (testé, n'ajoute rien).
- **mom** (momentum) : ln(clôture / ouverture) **de la veille**, c'est-à-dire le rendement de séance de la veille.
- **hlv** (volatilité intraday) : ½ ln(U), où U = moyenne sur **d = 21 jours** de [(haut − bas)² / clôture²] (la formule extraite donne (P_H − P_L)² / P_C² ; le facteur exact de la formule est partiellement illisible dans l'extraction). Variantes : ln(moyenne de (haut − bas)/clôture) et ln(moyenne de ln(clôture/ouverture)) (cette dernière telle qu'écrite dans le PDF). Le log est utilisé car la volatilité brute interfère avec la constante.
- **vol** (liquidité) : ln(volume moyen sur 21 jours) (le prix est déjà dans prc, donc on garde seulement la partie volume du volume en dollars). Variante vol1 avec volume ajusté des splits (volume × clôture non ajustée / clôture ajustée).
- **Normalisation** : hlv et vol sont transformés en coupe vers une loi normale de moyenne nulle et d'écart-type égal à celui du facteur brut ; prc et mom ne sont pas normalisés.

### Univers et période
- **Top 2 000 titres par volume moyen en dollars sur 21 jours**, univers recalculé **tous les 21 jours** (pas chaque jour, pour éviter un biais de sélection). Variantes top 3 000 et top 4 000.
- Actions ordinaires et classes d'actions cotées aux US au 6/9/2014 (pas d'OTC ni de préférentielles), prix de Yahoo Finance du 1/8/2008 au 5/9/2014 ; régressions sur **5 ans** (252 × 5 jours, dernier jour le 5/9/2014).
- **Biais de survie assumé** (univers des titres existant en 2014) ; l'auteur juge qu'il affecte peu les t-stats des rendements de facteurs.

### Résultats des régressions (t-stats annualisés à la Fama-MacBeth)
Le texte dit « t-stat quotidien multiplié par 252 » (probablement √252, symbole perdu dans l'extraction).

**Table 1 (constante + un facteur, top 2 000)** :
| Régression | F médian | t(int) | t(facteur) |
|---|---|---|---|
| int seul | 243,8 | 1,09 | — |
| int + prc | 127,4 | 2,65 | **−6,02** |
| int + rprc | 126,8 | 2,52 | −5,29 |
| int + mom | 127,6 | 1,00 | **−2,82** |
| int + hlv | 133,8 | 2,88 | **+3,64** |
| int + vol | 128,2 | −2,45 | **+3,83** |
| variantes hlv1 / hlv2 / vol1 | | | 3,67 / 3,55 / 4,11 |

Signes : **prix bas → nuit plus haute** (prc négatif) ; **séance de la veille positive → nuit plus basse** (mom négatif, retournement) ; **volatilité intraday élevée → nuit plus haute** ; **volume élevé → nuit plus haute**.

**Table 2 (les 4 facteurs ensemble, top 2 000)** : t(int) 2,28 ; t(prc) −4,66 ; t(mom) −3,78 ; t(hlv) 2,95 ; t(vol) 2,91 ; F médian 56,6. Variantes rprc et vol1 similaires (rprc −3,84 à −4,01 ; vol1 3,17 à 3,52).

**Table 3 (univers plus larges)** : top 3 000 : prc −5,92, mom −4,80, hlv 2,85, vol 2,76, F 70,2. Top 4 000 : prc −3,71, **mom −12,96**, hlv 2,60, vol 3,54, F 49,9. Le retournement « séance de la veille → nuit » marche « exceptionnellement bien sur le papier » pour les titres peu liquides entre le rang 3 000 et 4 000 (régression int + mom + vol sur ces seuls titres : t = −9,90, −15,72 et 8,19). Au-delà du top 3 000 environ, le comportement change.

**Table 4 (10 secteurs BICS + 4 facteurs)** : prc −4,83, mom −4,35, hlv 3,16, vol 3,12 ; les t-stats des secteurs passent de 0,70–1,58 (secteurs seuls) à 2,05–2,70 avec les 4 facteurs. Titres sans secteur BICS exclus.

### Test par une stratégie intraday de retournement (Tables 5–6, Figures 1–2)
- On prend les résidus ε de la régression du rendement de nuit (modèles : constante seule ; 4 facteurs + constante ; secteurs seuls ; 4 facteurs + secteurs), normalisés en coupe vers une loi normale.
- Position en dollars H(i) = −ε̃(i) × I / Σ|ε̃| (donc **on achète les titres dont la nuit est anormalement basse et on vend ceux dont la nuit est anormalement haute**), portefeuille neutre en dollars, I = 10 M$ long + 10 M$ short.
- **Entrée à l'ouverture au prix d'ouverture, sortie à la clôture le même jour**, « delay-0 » (le prix d'ouverture sert au signal et à l'exécution). **Sans coûts ni slippage**, l'auteur précise que le but n'est pas de construire une stratégie mais de vérifier que les facteurs apportent quelque chose.

| Modèle des résidus | Rendement annuel sur capital | Sharpe | cents/action |
|---|---|---|---|
| constante seule | 26,94 % | 7,79 | 0,82 |
| constante + 4 facteurs | 28,79 % | 11,22 | 0,87 |
| idem avec rprc | 28,80 % | 11,23 | 0,87 |
| 10 secteurs seuls | 33,27 % | 11,55 | 1,02 |
| secteurs + 4 facteurs | 34,30 % | **14,94** | 1,04 |
- Sans normalisation des résidus (Table 6) : rendements plus élevés (38,64 % à 45,32 %) mais Sharpe plus faibles (5,14 à 6,81) ; cents/action 1,01 à 1,18.
- Le Sharpe est décrit comme « Sharpe quotidien × 252 » (probablement √252). Un « défaut évident » de cette stratégie est renvoyé à Kakushadze (2015a), sans détail ici.

### À retenir (d'après le papier)
- Modèle de risque en coupe pour la nuit des actions individuelles : prix (−), séance de la veille (−), volatilité haut-bas 21 jours (+), volume 21 jours (+).
- La stratégie « retournement en séance de l'écart de nuit » affiche environ **0,8 à 1 cent par action** sans aucun coût, sur 2009–2014, avec biais de survie : le gain par action est du même ordre qu'un coût de transaction typique (l'auteur ne fait pas ce calcul).
- L'auteur pense que le modèle doit aussi marcher en intraday (positions prises vers l'ouverture et soldées avant la clôture).

---

## [6] Modelling Overnight and Daytime Returns Using a Multivariate GARCH-Copula Model (Kang, Babbs)

**SSRN 1710799 · 1re version mars 2010, version de juin 2010 · Options Clearing Corporation (gestion des risques)**

### Objet
Un modèle **multivarié** de la dynamique jointe des rendements de nuit et de séance de plusieurs actifs, pour la gestion du risque (VaR/ES à l'ouverture et à la clôture) et l'allocation. Le papier dit que la littérature n'avait traité que le cas univarié.

### Modèle
**Marges (par actif i)** :
- Moyenne conditionnelle (estimée par MCO) :
  - nuit(t) = c0 + c1 × séance(t−1) + c2 × nuit(t−1) + ε ;
  - séance(t) = d0 + d1 × **nuit(t)** + d2 × séance(t−1) + ε (la séance dépend de la nuit qui vient de se terminer).
- Variance conditionnelle (variante de GARCH croisé) :
  - h_nuit(t) = a0 + a1 × ε²_séance(t−1) + a2 × ε²_nuit(t−1) + a3 × h_nuit(t−1) ;
  - h_séance(t) = b0 + b1 × ε²_nuit(t) + b2 × ε²_séance(t−1) + b3 × h_séance(t−1).
  - Coefficients positifs ; condition de stationnarité sur les valeurs propres d'une matrice 2×2 donnée dans le papier.
- Innovations : Student t standardisée, degrés de liberté propres à la nuit et à la séance (> 2).
- Extensions évoquées mais non faites : plus de variables explicatives, GJR (asymétrie), t asymétrique de Hansen à moments variables.

**Dépendance entre actifs** : deux copules de Student t, une pour les nuits de tous les actifs, une pour les séances. Version à **corrélation constante** et version **dynamique (DCC)** où :
- Q_nuit(t) dépend des produits croisés de la séance (t−1) et de la nuit (t−1), et de Q_séance(t−1) et Q_nuit(t−1) ;
- Q_séance(t) dépend des produits croisés de la nuit (t) et de la séance (t−1), et de Q_nuit(t) et Q_séance(t−1).
- Conditions de stationnarité et de définie positivité (Proposition 1, démonstration en annexe : le système est un VARMA(1,1)).

**Estimation** : en deux étapes (« inference for the margins », Joe 1997 ; Patton 2006) : MCO pour la moyenne, maximum de vraisemblance pour les GARCH, puis maximum de vraisemblance des copules, les matrices de corrélation étant remplacées par les corrélations empiriques (fonction des degrés de liberté). Simulation séquentielle : d'abord la copule de nuit, puis la copule de séance conditionnelle.

### Données
- **15 fonds** : 9 ETF sectoriels SPDR (XLY, XLP, XLE, XLF, XLV, XLI, XLB, XLK, XLU), AGG (obligations agrégées), GSG (matières premières GSCI), USO (pétrole), RWR (immobilier coté), DBV (carry de devises G10), FXE (euro).
- Période annoncée : **21 septembre 2006 – 29 mars 2011** (incohérence : la version du papier est datée de juin 2010). Prix d'ouverture, de clôture et dividendes de Yahoo Finance ; rendements logarithmiques. Période de crise financière (volatilité « sans précédent »).

### Statistiques descriptives (Table 1, rendements log quotidiens)
| | XLY | XLP | XLE | XLF | XLV | XLI | XLB | XLK | XLU | AGG | GSG | USO | RWR | DBV | FXE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Moyenne nuit | 0,0005 | 0,0004 | 0,0003 | 0,0003 | 0,0002 | 0,0006 | 0,0006 | 0,0005 | 0,0005 | 0,0003 | 0,0002 | −0,0005 | 0,0001 | −0,0005 | −0,000004 |
| Moyenne séance | −0,0004 | −0,00022 | 0,0002 | −0,0009 | −0,0001 | −0,0004 | −0,0003 | −0,0003 | −0,0005 | −0,0001 | −0,0003 | 0,0002 | −0,0001 | 0,0005 | 0,0001 |
| Écart-type nuit | 0,011 | 0,008 | 0,012 | 0,017 | 0,008 | 0,011 | 0,011 | 0,010 | 0,008 | 0,003 | 0,012 | 0,016 | 0,013 | 0,009 | 0,005 |
| Écart-type séance | 0,017 | 0,010 | 0,019 | 0,026 | 0,011 | 0,015 | 0,017 | 0,014 | 0,013 | 0,003 | 0,014 | 0,019 | 0,029 | 0,008 | 0,004 |
| Kurtosis nuit | 19,5 | 26,7 | 16,4 | 22,3 | 15,6 | 13,5 | 12,8 | 28,2 | 24,7 | 42,6 | 6,2 | 6,8 | 18,0 | 14,3 | 4,7 |
| Kurtosis séance | 10,0 | 11,9 | 11,8 | 9,8 | 14,9 | 7,3 | 6,9 | 10,8 | 10,6 | 17,8 | 4,8 | 6,5 | 10,1 | 13,7 | 8,7 |
- Nuit moyenne positive et supérieure à la séance **sauf pour USO, DBV et FXE** (pétrole et devises). Les 9 ETF sectoriels ont tous une nuit positive ; 8 sur 9 ont une séance négative (XLE positive).
- Écart-type de séance plus élevé que celui de nuit sauf pour les deux fonds de devises (DBV, FXE). Kurtosis plus élevée la nuit sauf pour FXE. Asymétrie de signe variable.

### Résultats d'estimation
- **Moyenne conditionnelle (Table 2)** : peu de fonds ont une nuit qui dépend significativement de la séance ou de la nuit précédente, avec des signes mélangés. **Plusieurs fonds ont une séance qui dépend négativement de la nuit qui vient de se terminer.** Coefficients de la séance sur la nuit (ordre des colonnes reconstitué d'après l'extraction, écarts-types ≈ 0,02–0,06) : XLY −0,31 ; XLP −0,49 ; XLE 0,18 ; XLF −0,05 ; XLV −0,33 ; XLI −0,11 ; XLB 0,01 ; XLK −0,20 ; XLU −0,19 ; AGG 0,16 ; GSG 0,01 ; USO 0,01 ; RWR 0,04 ; DBV −0,17 ; FXE 0,05. Coefficient de la séance sur la séance précédente : tous entre −0,21 et 0,03.
- **GARCH (Table 3)** : persistance de la variance de nuit a3 entre 0,66 et 0,93 ; de séance b3 entre 0,69 et 0,93. Degrés de liberté **nuit** entre 4,05 et 9,56 (FXE 15,35) ; **séance** entre 6,27 et 40,05. Tous les fonds sauf FXE ont des degrés de liberté plus bas la nuit (queues plus épaisses). La variance de nuit dépend aussi du choc de séance précédent (a1 entre 0,01 et 0,14) et la variance de séance du choc de nuit (b1 entre 0,02 et 0,29 ; XLF 0,29, RWR 0,23).
- Variance conditionnelle de séance plus élevée que celle de nuit pour tous sauf AGG et FXE (Figure 3).
- **Copule constante (Table 4)** : degrés de liberté de la copule de nuit **9,16** contre **21,90** pour la séance → dépendance de queue plus forte la nuit. Corrélations un peu plus fortes la nuit dans la plupart des cas (ex. XLY–GSG 0,38 la nuit contre 0,19 en séance ; USO–XLE 0,76 contre 0,57 d'après la matrice). Log-vraisemblance 13 346,47. Sur une période plus calme (11/3/2003 – 19/7/2007, 9 ETF sectoriels, non tabulé) les corrélations de nuit étaient au contraire plus **faibles** que celles de séance : la comparaison dépend des actifs et de la période.
- **Copule dynamique (Table 5)** : log-vraisemblance 13 945,34 (nettement meilleure). Pour Q_nuit : poids sur Q_nuit(t−1) = 0,97 ; sur la séance précédente quasi nul. Pour Q_séance : β1 = 0,033 (produits croisés de nuit), β3 = 0,365 (Q_nuit(t)), β4 = 0,344. → **la structure de dépendance de la séance dépend de celle de la nuit qui précède**, alors que la dépendance de nuit dépend surtout d'elle-même. Degrés de liberté 11,85 (nuit) et 28,06 (séance).
- Figure 4 : pour 3 des 4 paires montrées, la corrélation de séance est plus élevée. Figure 5 : pour les 4 paires (XLE-XLV, USO-XLE, XLF-AGG, RWR-DBV), le **coefficient de dépendance de queue est plus élevé la nuit**.

### Applications (illustrations)
- **VaR et ES** (Table 6, portefeuille équipondéré, 1 000 scénarios de nuit × 100 de séance) : nuit 1 % : VaR 0,000122, ES 0,000107 ; séance 1 % : VaR −0,00081, ES −0,00083 (valeurs telles qu'imprimées ; les chiffres de nuit sont positifs, le papier ne commente pas).
- **Allocation CRRA** (Table 7, sans taux sans risque, poids positifs et somme < 1) : pour toutes les aversions au risque testées (A = 1 à 15), le portefeuille optimal de **nuit est 100 % XLB** et celui de **séance 100 % DBV**.

### À retenir (d'après le papier)
- Sur ces ETF en 2006–2011 : nuit moyenne plus haute, variance plus faible, queues plus épaisses que la séance (sauf pétrole et devises pour la moyenne, devises pour la variance).
- La séance dépend négativement de la nuit qui vient de se terminer pour plusieurs fonds, en moyenne, en variance et en corrélation.
- Les auteurs relient ces faits à l'asymétrie d'information (Admati et Pfleiderer 1988, 1989). Pas de test hors échantillon (renvoyé à des travaux futurs).

---

## [7] Predicting Stock Volatility Using After-Hours Information (Chen, Yu, Zivot)

**SSRN 1324991 · 12 janvier 2009 · KPMG / Winona State / University of Washington**

### Question
L'information des heures hors séance (after-hours) aide-t-elle à prévoir la **volatilité de la séance suivante** ? Et quelle partie de la nuit compte ?

### Données
- TAQ, transactions de 8:00 à 18:30 ET (heures du NASDAQ Trade Dissemination Service). **4 actions NASDAQ** choisies pour leur liquidité after-hours : **MSFT** (référence), AMGN, CSCO, YHOO.
- **Janvier 2001 – décembre 2004** ; estimation sur les 3,5 premières années (jusqu'à juin 2004), **prévision hors échantillon sur le dernier semestre 2004**.
- Nettoyage : on retire les transactions qui varient de ±25 % par rapport à la précédente, les jours où il manque les données preopen, postclose ou séance, et les splits.
- « Jour » = séance régulière 9:30–16:00 ET.

### Découpage de la nuit (Barclay et Hendershott 2003, 2004)
- **Postclose** 16:00–18:00 ET : environ 80 % du volume s'y fait au prix de clôture ou dans la fourchette de clôture de 16:00 (mais seulement 15 % des transactions) → trading de liquidité, peu d'information.
- **Overnight** 18:00–8:00 ET : pas de données (seulement ~1 % des transactions after-hours selon Barclay-Hendershott).
- **Preopen** 8:00–9:30 ET : probabilité de transaction informée beaucoup plus élevée.

### Mesures
- Variance réalisée : somme des carrés des rendements à **5 minutes en séance (78 points)**, à **15 minutes en after-hours** (6 points en preopen, 8 en postclose) pour limiter le bruit de microstructure.
- Overnight : carré du rendement entre la dernière transaction du postclose de la veille et la première transaction du preopen.
- Statistiques MSFT (Table 1, volatilités réalisées en %) : séance moyenne 1,77 ; preopen 0,58 ; postclose 0,59 ; overnight (rendement au carré) moyenne 0,0053. Distributions asymétriques à droite, queues épaisses. Séance, preopen et postclose ont une mémoire longue ; le rendement absolu d'overnight non.
- Table 2 (MSFT) : volatilité horaire séance 0,273 %, preopen **0,388 %**, postclose 0,294 % ; volatilité par transaction preopen **0,0102 %** contre postclose 0,00592 % (et 0,000181 % en séance). Nombre de transactions par jour : séance 978 959, preopen 5 701, postclose 9 925.

### Modèle 1 : GARCH(1,1) de la séance avec une variable de nuit dans la variance
- Sélection : GARCH(1,1) à erreurs de Student est le meilleur (AIC/BIC).
- h²(t) = ω + α ε²(t−1) + β h²(t−1) + γ x(t−1), avec x = l'une des 4 mesures :
  1. nuit entière = moyenne pondérée par le temps : (1,5/17,5) × RV preopen + (2/17,5) × RV postclose + (14/17,5) × r² overnight ;
  2. RV preopen seule ; 3. RV postclose seule ; 4. r² overnight seul.
- **MSFT (Table 4A)** : α ≈ 0,065, β ≈ 0,93 ; persistance α + β = **0,997** sans variable (proche du 0,9986 de Martens 2002 pour le S&P 500). γ nuit entière = 0,065 (écart-type 0,064, **non significatif**) ; **γ preopen = 0,221 (0,090), significatif** ; γ postclose = −0,007 (0,015), non significatif ; γ overnight = 0,057 (0,057), non significatif. Persistance avec preopen : 0,971.
- AMGN : preopen 0,14 (significatif à 10 %) ; CSCO : preopen 0,155 (5 %), nuit entière 0,202 (5 %) et **overnight 0,144 (5 %)** ; YHOO : preopen 0,163 (5 %). Postclose jamais significatif. L'overnight n'aide que pour CSCO.
- Note : le texte dit que le coefficient non significatif de la nuit entière « s'accorde avec Martens (2002) en ce que la variance close-to-open apporte un pouvoir explicatif » ; vu le reste du papier, il faut probablement lire « n'apporte pas » (formulation du papier).

### Évaluation hors échantillon (prévision glissante à 1 pas, MSFT, Table 5A)
| | GARCH séance | + nuit entière | + preopen |
|---|---|---|---|
| Mincer-Zarnowitz a1 | 0,899 | 0,759 | **0,976** |
| R² ajusté | 0,091 | 0,091 | **0,157** |
| RMSE | 0,440 | 0,452 | **0,424** |
| MAE | 0,206 | 0,244 | **0,202** |
| HRMSE | 0,442 | 0,399 | **0,391** |
| HMAE | 0,208 | 0,223 | 0,204 |
| perte log | −0,049 | −0,133 | −0,029 |
- À 5 pas (Table 5B) : R² 0,031 / 0,029 / **0,073** ; même classement.
- Autres titres (Table 6) : R² ajusté du GARCH séance → avec preopen : AMGN 0,017 → 0,061 ; CSCO 0,039 → 0,054 ; YHOO 0,209 → 0,373.
- Régression d'englobement (Table 7, MSFT) : ajouter la prévision « + preopen » fait passer le R² de 0,098 à **0,171** (coefficient 1,353, significatif ; celui du GARCH simple devient −0,511, non significatif). Ajouter la prévision « + nuit entière » : R² 0,099 (inchangé). Explication reprise de Martens : le rendement au carré close-to-open est une mesure très bruitée.

### Modèle 2 : SEMIFAR (mémoire longue sur la log-variance réalisée)
- Log-variances réalisées standardisées ; séries alternant séance et nuit (ou preopen, ou postclose). d estimé entre 0 et 0,5 (mémoire longue) : séance seule 0,468 ; séance + nuit 0,349 ; séance + preopen 0,412 ; séance + postclose 0,290.
- Prévision : séance + preopen a le meilleur R² et les plus faibles erreurs ; séance + nuit n'améliore pas ; séance + postclose est le pire (R² 0,018). Englobement (Table 11) : R² de 0,146 à **0,192** avec le preopen ; postclose n'apporte rien.
- Note : les Tables 10A et 10B du PDF sont identiques et toutes deux titrées « 5 pas », alors que le texte présente 10A comme la prévision à 1 pas.

### À retenir (d'après le papier)
- **Seule la variance réalisée du preopen (8:00–9:30 ET) améliore la prévision de la volatilité de la séance** ; le postclose (16:00–18:00) et le rendement au carré de la nuit n'apportent rien (sauf CSCO pour l'overnight).
- Explication proposée : débordement de l'information du preopen sur la séance, et traders informés qui tradent avant les annonces. Extension proposée : vérifier si l'effet se concentre sur les premières heures de séance.
- 4 actions NASDAQ seulement, 2001–2004, échantillon hors échantillon de 6 mois.

---

## [8] A Coupled Component GARCH Model for Intraday and Overnight Volatility (Linton, Wu)

**SSRN 3112950 · 17 octobre 2017 · Cambridge / Nanjing · USC Dornsife INET Working Paper 18-01**

### Objet
Un modèle bivarié nuit / séance qui respecte l'ordre temporel (la nuit précède la séance), permet aux deux périodes d'avoir des propriétés différentes et des rétroactions, avec une **composante lente non paramétrique** (tendance) et une **composante rapide paramétrique** de type score dynamique (DCS, Harvey 2013) à innovations de Student t. Théorie asymptotique complète (consistance, normalité). Version multivariée avec corrélations entre titres.

### Modèle
- Séance r_D(t) = ln(clôture_t / ouverture_t) ; nuit r_N(t) = ln(ouverture_t / clôture_{t−1}) ; r(t) = r_D + r_N. **Pas de distinction entre nuits de semaine, week-ends et jours fériés.**
- Moyenne : vecteur (r_D, r_N) avec un terme φ qui relie la séance à la nuit du même jour (sous forme matricielle [1 φ ; 0 1] × (r_D, r_N) = μ + Φ × (r_D(t−1), r_N(t−1)) + u ; d'après le texte, un φ négatif signifie que la nuit a un effet positif sur la séance qui suit). Sous l'hypothèse d'efficience, φ = 0 et Φ = 0.
- Volatilité : u_j = exp(λ_j(t)) × exp(g_j(t/T)) × ε_j, j = D, N : g_j = composante lente (fonction lisse, intégrale nulle pour l'identification), λ_j = composante courte, ε_j ~ Student t à ν_j degrés de liberté.
- λ_D(t) dépend de λ_D(t−1), du score de séance (t−1) **et du score de la nuit du même jour** (paramètre de transmission nuit → séance), plus des effets de levier (signe des chocs) ; λ_N(t) dépend de λ_N(t−1), du score de nuit (t−1) et du score de séance (t−1). Le score de Student pondère automatiquement à la baisse les très gros chocs (robustesse).
- VaR intraday conditionnelle à la nuit du jour : moyenne conditionnelle + écart-type conditionnel × quantile de Student.
- Estimation en plusieurs étapes : MCO pour la moyenne, noyau (avec noyau de bord) pour g, maximum de vraisemblance pour les paramètres dynamiques, puis mise à jour de g par vraisemblance locale. Test de constance du ratio des composantes lentes nuit/séance (statistique en différence de différences sous forme de ratio).
- Multivarié : modèle de marché avec rendement retardé (Scholes-Williams), corrélations lentes estimées par noyau (Pearson ou version robuste par tau de Kendall), composante courte diagonale. L'hypothèse de « pooling » des paramètres entre titres (Blanc, Chicheportiche et Bouchaud 2014) est fortement rejetée.

### Application 1 : 28 actions du Dow Jones, 12/11/1991 – 13/04/2016 (Thomson Reuters Eikon, ajusté des opérations)
- GS et V exclus (introduits en 1999 et 2008).
- Cumul nuit vs séance (Figure B.1) : pour AAPL, CAT, CSCO, HD, INTC, JPM, PFE, UTX, WMT le gain vient surtout de la nuit ; pour MMM, KO, DD, XOM, JNJ, MCD, MRK, NKE, PG, TRV, VZ, DIS il vient surtout de la séance. **Pas de domination claire de la nuit** sur ces titres.
- Moyenne en coupe (méthode Berkman et al.) : séance **2,18 pb/jour** (erreur-type 1,22) ; nuit **1,60 pb/jour** (erreur-type 0,70) ; différence non significative.
- La nuit a une asymétrie plus négative (26 titres sur 28, contre 10 sur 28 en séance) et une kurtosis extrême. **La variance horaire de la séance vaut environ 11 fois celle de la nuit** (French et Roll 1986 trouvaient 13 à 100).
- Moyenne : 12 titres sur 28 ont un coefficient significatif (tous négatifs) de la séance sur la séance de la veille ; 7 sur 28 ont un φ significatif (tous positifs, c'est-à-dire effet négatif de la nuit sur la séance du jour). Pas de schéma clair pour prévoir la nuit. Constantes μ_D et μ_N positives pour la plupart.
- Dynamique : persistance significativement < 1 ; effets de levier significatifs (volatilité plus forte après un rendement négatif). Le niveau de l'échelle courte est plus élevé en séance. **Degrés de liberté de la nuit ≈ 3, de la séance ≈ 8.** L'égalité du paramètre de transmission nuit → séance et séance → nuit n'est pas rejetée (contrairement à Blanc et al. 2014) ; selon les auteurs, **la nuit affecte significativement la volatilité future de la séance**.
- **Ratio volatilité de nuit / volatilité de séance : tendance haussière pour les 28 titres sur 24 ans**, avec des pics vers août 2011. La volatilité de séance dominait nettement celle de nuit dans la première moitié ; cette domination a disparu progressivement, surtout après 2008. La volatilité de séance après 2005 est en général plus faible qu'avant (sauf crise), ce qui va contre l'idée que le trading haute fréquence a augmenté la volatilité. Le test de constance du ratio est rejeté surtout avant 2000 et après 2010.
- Prévision : 10 fenêtres glissantes (5 652 observations en échantillon, 50 hors échantillon) ; test de Giacomini-White : le modèle couplé bat le modèle à une composante sur la séance pour la plupart des titres (parfois significativement).
- Diagnostics : la loi de Student va bien pour la séance ; pour la nuit, plusieurs valeurs extrêmes dans la queue gauche, l'asymétrie négative et la kurtosis ne sont que partiellement capturées.
- Multivarié (1998–2016) : corrélations lentes en hausse nette, élevées en 2008 ; la 1re valeur propre explique près de **50 % du risque de séance en 2008** et **70 % du risque de nuit lors de la chute d'août 2011**. La persistance moyenne baisse de 0,9515 à 0,8796 (séance) et de 0,9553 à 0,8926 (nuit) dans le modèle multivarié. Modèle CAPM : alpha de séance significatif pour 6 titres, **alpha de nuit significatif pour 15 titres** ; bêtas nuit et séance très proches (0,5 à 1,5).

### Application 2 : 10 portefeuilles de taille CRSP, juillet 1992 – décembre 2015
- Filtres : titres non actifs exclus ; rendements de nuit ou de séance > 50 % en valeur absolue exclus ; prix de clôture négatifs CRSP (moyennes bid/ask) exclus. Portefeuilles pondérés par la capitalisation (déciles CRSP), pour NYSE/AMEX/NASDAQ, NASDAQ et NYSE séparément.
- **Rendements moyens (Table A.1, % par jour, NYSE/AMEX/NASDAQ)** :

| Décile | séance | nuit | t (nuit = séance) |
|---|---|---|---|
| 1 (petit) | 0,0942 | 0,0606 | 2,53 |
| 2 | 0,0964 | 0,0323 | 5,81 |
| 3 | 0,0793 | 0,0308 | 4,37 |
| 4 | 0,0601 | 0,0392 | 1,65 |
| 5 | 0,0484 | 0,0414 | 0,48 |
| 6 | 0,0426 | 0,0388 | 0,24 |
| 7 | 0,0401 | 0,0376 | 0,15 |
| 8 | 0,0416 | 0,0253 | 1,01 |
| 9 | 0,0324 | 0,0324 | 0,00 |
| 10 (grand) | **0,0155** | **0,0270** | −0,77 |
  - Toutes positives et significatives sauf la séance du décile 10. Médianes de séance souvent > 10 pb, de nuit ≈ 6 pb (asymétrie à droite de la séance).
  - NASDAQ : décile 10 séance **0,0028 %** contre nuit **0,0672 %** (t −3,02) ; déciles 6 à 10 avec nuit ≥ séance. NYSE : nuit faible pour les petits déciles (décile 1 : séance 0,0793, nuit 0,0063) ; décile 10 : séance 0,0179, nuit 0,0164.
- Autocorrélations : fortes et positives pour les petits déciles (nuit et séance) ; **la nuit des petits déciles décroît très lentement (mémoire longue)** ; la nuit des déciles 5 à 10 a une autocorrélation d'ordre 1 négative d'environ **−0,1** ; la séance du décile 10 seulement ≈ −0,07. Corrélation séance(t) / nuit(t) ≈ 0,1 (non significative pour le décile 10) ; corrélation séance(t−1) / nuit(t) significative et positive pour tous les déciles.
- **Moyenne (Table A.2)** : φ négatif et significatif pour la plupart des déciles (de −0,03 à −0,24 ; décile 10 −0,048 non significatif) : **pour les portefeuilles pondérés, la nuit a un effet positif sur la séance qui suit, en série temporelle**. Les auteurs notent que ce n'est pas contradictoire avec le retournement de Berkman et al., qui est un effet en coupe. Séance sur séance(t−1) : +0,23 (décile 1) à −0,0685 (décile 10). Nuit sur nuit(t−1) : +0,15 (décile 1) à −0,10 (décile 10). Nuit sur séance(t−1) : +0,03 à +0,10.
- Dynamique (Table A.4) : persistance séance 0,906–0,951, nuit 0,931–0,953 ; levier significatif ; degrés de liberté de nuit de 7,1 (décile 1) à 4,4–5,2 (grands déciles), séance 7,6–11,4.
- **Ratio volatilité de nuit / séance** (Figure 3) : **baisse pour les petites capitalisations** (surtout avant 2000), **hausse pour les grandes**, la pente augmente de façon monotone du décile 1 au décile 10. Volatilité de nuit élevée en 2008 et pendant toute la crise des dettes souveraines européennes (2009–2012), puis stable mais au-dessus du niveau d'avant-crise. Même chose sur NASDAQ et NYSE séparés (pentes plus plates au NYSE). Portefeuilles triés par bêta ou par écart-type : ratio en hausse pour presque tous, sans ordre monotone.

### Explications testées du ratio nuit / séance
- **Taille du tick** : dans les années 1990 le tick était de 12,5 cents (et 25 cents de fait au NASDAQ), puis 6,25 cents en juin 1997 et 1 cent après la décimalisation (2001). Sauts d'ouverture de 25 cents fréquents sur les petits titres à bas prix, donc forte volatilité de nuit. Tri 10×10 taille × spread/prix (depuis 1994) : à taille donnée, la pente passe de ≈ 0 (spread faible) à très négative (spread élevé). Explique en partie la baisse pour les petits titres dans les années 1990.
- **Croisements d'ouverture et de clôture du NASDAQ (fin octobre 2004)** : pas d'effet visible (NYSE en groupe témoin).
- **Revenus étrangers / domestiques** (Compustat, ~10 % des titres) : pas d'effet.
- **Industries** (Fama-French 12) : la taille reste la variable dominante ; les Utilities ont un ratio plus faible.
- **Corrélation avec l'indice mondial hors US** (French) : **le ratio augmente nettement pour les titres très corrélés à l'international**, reste stable pour les autres ; les titres très corrélés à l'international sont plus souvent de grandes capitalisations. C'est l'explication principale retenue.
- Autre piste mentionnée : l'E-mini tradable la nuit depuis le 9/9/1997 aurait dû réduire le risque de nuit.
- Robustesse avec VIX / volatilité de Rogers-Satchell (séance seule) sur les 28 titres du Dow : le ratio montre aussi une tendance haussière.

### Corrélations (multivarié CRSP)
- Corrélations lentes nuit et séance en hausse ; le décile 1 avait une corrélation avec les autres d'environ **0,2 la nuit / 0,3 en séance en 1992**, montée à environ **0,8 / 0,6 en 2015**. Pas de grande différence entre corrélations lentes de nuit et de séance.

### À retenir (d'après le papier)
- La nuit est moins volatile mais à **queues beaucoup plus épaisses** (ν ≈ 3 pour les actions du Dow) : les estimations gaussiennes sont fragiles.
- **Le poids de la volatilité de nuit a augmenté** pour les grandes capitalisations depuis 1992, surtout après 2008, en lien avec la corrélation internationale.
- En série temporelle, sur les portefeuilles pondérés de taille, une nuit positive est suivie d'une séance plutôt positive (sauf le décile des plus grandes capitalisations, non significatif).
- Les nuits du week-end ne sont pas traitées à part (extension proposée avec 10 sessions par semaine).

---

## [9] Observation-driven Models for Realized Variances and Overnight Returns Applied to Value-at-Risk and Expected Shortfall Forecasting (Opschoor, Lucas)

**SSRN 3429750 · version du 6 août 2020 · Vrije Universiteit Amsterdam / Tinbergen Institute**

### Objet
Prévoir la variance **close-to-close** quand on n'a des données haute fréquence que pendant la séance. Au lieu de multiplier la variance réalisée de séance (RV) par une constante fixe (Hansen et Lunde 2005, Koopman et al. 2005), le facteur d'échelle **c_t = variance totale / variance de séance varie dans le temps**, avec une dynamique « score-driven » (GAS, Creal, Koopman et Lucas 2013).

### Modèle « GAS tv-c_t »
- RV_t = h_d,t × u_t, u_t ~ **loi F** (ν1, ν2) (queues épaisses de la RV) ;
- r_t = μ + √h_t × ε_t, ε_t ~ **Student t** (ν3) ; **h_t = c_t × h_d,t** ;
- h_d,t+1 = ω1 + α1 × s_h,t + β1 × h_d,t ; c_t+1 = ω2 + α2 × s_c,t + β2 × c_t ;
- s_h,t = (poids × RV_t − h_d,t) et s_c,t = (poids × ε²_t / h_d,t − c_t) : les poids diminuent quand l'observation est extrême (ex. flash crash de 2010), donc les valeurs aberrantes de RV ou de rendement influencent peu la trajectoire.
- Estimation par maximum de vraisemblance en 2 étapes (d'abord la partie F, puis la partie Student) ; perte d'efficacité « très petite » par rapport à une étape.
- VaR et ES à 1 jour en formule fermée sous la Student t.

### Modèles concurrents
- **GAS fix-c** : même modèle avec c constant (α2 = β2 = 0).
- **HEAVY** (Shephard et Sheppard 2010) : h_t+1 = ω + α RV_t + β h_t ; invariant à toute mise à l'échelle constante de RV.
- **GAS sep** : variance de séance (GAS F) + variance de nuit modélisée à part (« GAS t ON », Student t, avec débordement du carré du rendement de séance sur la nuit, comme Ahoniemi et al. 2015) + corrélation nuit/séance constante (pas de DCC, faute de support empirique pour les actions).
- Hors échantillon : **GAS roll-c_t** (le modèle fix-c réestimé tous les 50 jours, donc c varie lentement) et un fix-c de Koopman et al. calculé **sur tout l'échantillon** (avantage injuste, information future).

### Données
- **93 actions du S&P 500** tirées au hasard dans 10 secteurs (18 financières), panel équilibré, **2/1/2001 – 31/12/2018**, 4 472 jours (demi-séances retirées). TAQ 9:30–16:00, nettoyage Barndorff-Nielsen et al. (2009) et Brownlees-Gallo (2006), RV à 5 minutes.
- **19 indices mondiaux** (AEX, All Ordinaries, BFX, Sensex, Dow Jones, CAC 40, FTSE 100, DAX, Hang Seng, IBEX 35, Nasdaq 100, KOSPI, IPC Mexico, Nikkei 225, Russell 2000, S&P 500, Shanghai, SMI, Euro Stoxx 50) : rendements nuit et séance et RV 5 minutes de l'Oxford-Man Realized Library, 4 345 à 4 580 observations.

### Résultats en échantillon (Table 3, moyennes des estimations)
- Degrés de liberté de la Student du rendement total : **≈ 6,3 pour les actions**, ≈ 9,8 pour les indices.
- Dans le modèle séparé, degrés de liberté du rendement **de nuit ≈ 2,98 pour les actions** (moments d'ordre 4 probablement inexistants) et ≈ 5,0 pour les indices. Confirme Linton et Wu (2017).
- Persistance de c_t : **0,916 (actions), 0,961 (indices)** → ratio qui bouge lentement.
- ν2 de la loi F : 13,53 (actions), 14,37 (indices) → RV à queues épaisses.
- La valeur moyenne du c fixe est de 1,329 pour les actions et 1,732 pour les indices (lecture de la ligne du tableau ; l'extraction mélange les colonnes).
- Rapport de vraisemblance c variable contre c fixe : rejet de c constant à 5 % pour **77 actions sur 93** et **12 indices sur 19**. Meilleure vraisemblance que HEAVY pour une grande partie des actions (écart > 80 points pour IPC Mexico et Russell 2000).
- Trajectoires (Figure 2) : **pics de c_t pendant la crise 2008/2009**, surtout pour les financières (AIG, BAC, C, WFC) ; pour certaines actions c_t < 1 en 2005/2006 ; Russell 2000 extrême au début des années 2000. Plus d'information arrive hors séance pendant les périodes agitées.
- Moyenne du c_t glissant sur les 93 actions : **entre 1,20 et 1,40** sur 2005–2018.

### Résultats hors échantillon (fenêtre mobile de 1 000 jours, réestimation tous les 50 jours, hors échantillon du 14/1/2005 au 31/12/2018, 3 472 jours)
Tests : couverture inconditionnelle et conditionnelle de Christoffersen (1998) pour la VaR 99 % et 95 % ; tests inconditionnel et conditionnel (m = 10) de Du et Escanciano (2016) pour l'ES 97,5 % et 95 %. Chiffre = nombre d'actions (sur 93) où le test rejette ; plus petit = mieux.

**Actions, VaR inconditionnelle (rejets à 5 %)** : 99 % : tv-c 27, roll-c **15**, fix-c 43, sep 18, HEAVY 27. 95 % : tv-c **15**, roll-c 16, fix-c 50, sep 39, HEAVY 23.
- **c fixe est le pire partout.** Globalement **roll-c est le meilleur** ; HEAVY gagne seulement pour l'ES en couverture conditionnelle. GAS sep est bon à la VaR 99 % mais mauvais à 95 %.
- **Période agitée 2005–2011** (Table 5) : **tv-c très nettement le meilleur** (VaR 99 % : 8 rejets à 5 % contre 12 roll-c, 42 fix-c, 27 sep, 17 HEAVY ; VaR 95 % : 11 contre 23, 58, 40, 25).
- **Période calme 2012–2018** : à la VaR 99 %, modéliser nuit et séance séparément (sep) marche bien ; à 95 %, tv-c bat fix-c et sep ; HEAVY et roll-c comparables.
- ES (Tables 4 et 6) : tv-c le meilleur en inconditionnel, surtout en période agitée ; HEAVY légèrement meilleur en conditionnel ; sep bon pour l'ES 97,5 % en période calme seulement.

**Indices (Table 7)** : différences faibles entre modèles. c fixe le pire ; roll-c en général le meilleur, parfois devancé par tv-c ou HEAVY ; en test inconditionnel, fix-c et sep rejettent pour (presque) tous les indices. Aucune situation où le modèle séparé nuit/séance est préférable pour les indices.

### À retenir (d'après le papier)
- Le **ratio variance totale / variance de séance n'est pas constant** : il monte en crise (plus d'information arrive la nuit), environ 1,2–1,4 en moyenne pour les actions.
- Les rendements de nuit sont **extrêmement leptokurtiques** (ν ≈ 3 pour les actions, 5 pour les indices).
- Pour la VaR/ES, un ratio variable (même mis à jour lentement) bat un ratio fixe ; l'avantage est surtout net pour les **actions individuelles en période agitée** ; pour les indices tout se vaut à peu près, HEAVY inclus.

---

## [11] Does News, Order Flow, or Illiquidity Drive Jumps in Stock Returns? In the Day or in the Night? (Jeon, McCurdy, Szaura)

**SSRN 4637027 · version de mai 2023 · McMaster / Toronto (Rotman) / BI Norwegian Business School**

### Question
Les sauts des rendements d'actions individuelles viennent-ils des **news**, de l'**illiquidité** ou des **déséquilibres d'ordres** ? Et est-ce différent **la nuit** et **en séance** ? Le papier se dit le premier à analyser ce qui provoque les sauts de la période de nuit.

### Données
- CRSP, actions ordinaires (codes 10 et 11) ; ouverture 9:30 et clôture 16:00 ET disponibles depuis janvier 1993. Échantillon d'analyse **janvier 2000 – février 2020** (certains tableaux jusqu'à décembre 2020).
- Illiquidité et flux : WRDS Intra-Day Indicators (MTAQ 1993–2014, DTAQ 2015–2020). **RES** = spread effectif relatif pondéré par le volume en dollars (Goyenko, Holden et Trzcinka 2009). **OIB** = (volume acheteur en $ − volume vendeur en $) / (somme) (Chordia et Subrahmanyam 2004).
- News : **RavenPack**, uniquement les articles de **nouveauté maximale (100)** ; sentiment RavenPack recentré entre −50 et +50. News de **séance** = horodatées entre 9:30 et 16:00 ; news de **nuit** = entre 16:00 et 9:30 le jour suivant. Version alternative avec Factiva (Jeon, McCurdy et Zhao 2021).
- Variables standardisées ; observations de RES et OIB au-delà de 2 écarts-types retirées.

### Statistiques (Table 1)
- News par jour : 0,37 en moyenne pour toutes les actions, 1,21 pour les 500 plus grandes. **Plus de news la nuit que le jour** : 0,23 contre 0,12 (toutes) ; 0,54 contre 0,43 (top 500). Sentiment moyen plus positif la nuit : 0,24 contre 0,11 (toutes) ; 0,46 contre 0,33 (top 500).
- RES moyen 0,02 (écart-type 0,13) toutes actions ; 0,01 (0,06) top 500. OIB moyen −0,02 (0,37) toutes ; +0,01 (0,18) top 500.

### Détection des sauts (Lee et Mykland 2008, statistique modifiée de Gilder, Shackleton et Taylor 2014)
- Trois périodes : journée entière (16:00 → 16:00), **nuit (16:00 → 9:30)**, **séance (9:30 → 16:00)**.
- Volatilité locale par variation bipuissance sur les K jours précédents, calculée séparément pour la nuit et la séance.
- Saut si |rendement| / volatilité locale > **5,1024** (J99 journée), **4,4881** (J95 journée), **5,28** (séance JD,99 et nuit JN,99).
- **Fréquences (Table 2)** : J99 = 298 110 sauts sur 23,9 millions de jours-titres, **1 saut tous les ~80 jours** ; top 500 : 1 tous les 112 jours. Séance : 384 523 sauts sur 15,76 millions, **1 tous les 41 séances** ; nuit : 95 224, **1 toutes les 165 nuits**. Top 500 : 1 tous les 60 jours (séance) et 153 (nuit). **Les sauts de nuit sont moins fréquents que ceux de séance**, et la volatilité de nuit est plus faible. Vrai aussi hors annonces de résultats, sur 2004–2020, sans 2008–2009 et sans 2020 (non tabulé).

### Probabilité de saut (logit sur la journée entière, Table 3 ; les tableaux disent « probit »)
- News seulement : rapport de cotes (pour 1 écart-type) **1,37** pour le nombre de news, 1,10 pour le sentiment absolu ; R² 5,41 %.
- **RES : 1,48 ; OIB : 1,22** ; R² 5,88 % avec les deux.
- Avec Factiva : news 1,22 ; RES 1,38 ; OIB 1,31.
- Pour l'action moyenne, l'**illiquidité** est la source la plus probable d'un saut ; pour les **500 plus grandes**, ce sont les **news** (Table A.2).

### Taille des sauts (Table 4)
- Tous sauts : taille moyenne liée positivement au nombre de news, au sentiment, à RES et à OIB ; R² de 0,59 % à **10,05 %** quand on ajoute RES et OIB.
- Sauts positifs : positivement liés à RES et OIB (R² 1,35 % → 3,68 %). Sauts négatifs : négativement liés à RES et OIB (R² 7,77 % → 14,18 % ; le texte écrit aussi « 14,818 % »). Autrement dit, plus d'illiquidité et un flux du même côté → saut plus grand.

### Séparer news de nuit et news de séance (Tables 5–7)
- Probabilité de saut journalier : rapport de cotes **1,41 pour le nombre de news de nuit**, **1,14 pour les news de séance**. Le sentiment de séance augmente la probabilité ; **le sentiment de nuit la diminue** (toutes actions) ; pour le top 500, les deux sentiments l'augmentent.
- Table 7 (2000–2014, avec spread coté et volume after-hours ; légende du tableau : 500 plus grandes, titre : toutes les firmes) : news de nuit 1,40–1,43 ; news de séance 1,15–1,16 ; volume en dollars after-hours 1,11–1,15 ; spread coté after-hours ≈ 1 ; RES 1,50 ; OIB 1,31 ; R² jusqu'à 10,85 %.

### Sauts de séance et sauts de nuit séparément (Tables 8 et 9, toutes actions)
- **Sauts de séance** : news de séance 1,11 ; sentiment de séance 1,06 ; |rendement de séance de la veille| 1,08–1,10 ; **RES 1,35 ; OIB 1,13** ; R² très faible (0,67 % à 0,91 %).
- **Sauts de nuit** : **news de nuit 1,62** ; sentiment de nuit 1,09 ; **|rendement de nuit précédent| 0,83 à 0,84** (une grosse nuit précédente réduit la probabilité d'un saut de nuit) ; spread coté de nuit 0,94–0,96 ; **log volume en dollars de nuit 1,35** ; **R² ≈ 19,6–20,1 %**. Les sauts de nuit sont bien plus expliqués par les news et le volume after-hours que les sauts de séance.

### Interactions (Table 10)
- Interactions news × illiquidité (rapport de cotes 0,93), news × OIB (0,99), sentiment × illiquidité / OIB (0,94) : significatives mais **économiquement faibles**. Top 500 : seule interaction sentiment × OIB (1,02).

### Rendements anormaux autour des sauts (Tables 11–15, alphas Fama-French-Carhart, 21 jours avant, jour du saut, 21 jours après)
- Toutes actions, décile supérieur de chaque variable (dans la distribution propre du titre) : alpha du jour du saut **+18,13 % / −14,03 %** (sauts positifs / négatifs) quand on trie sur l'illiquidité ; **+17,23 % / −14,24 %** sur le nombre de news ; +12,70 % / −8,28 % sur OIB ; **+17,62 % / −15,00 %** sur les news de séance ; **+15,75 % / −13,97 %** sur les news de nuit. Hors fenêtre [−3, +3] des résultats : news totales +20,87 % / −15,98 %.
- Top 500 : news de séance +9,43 % / −9,84 % ; news de nuit +8,49 % / −8,83 % ; illiquidité +8,98 % / −9,17 % ; OIB +6,58 % / −5,35 %.
- Après le saut (Table 12, tri sur les news de nuit, toutes actions) : alphas moyens t+1 à t+21 très petits (ordre de 10⁻³ ; unité non précisée). Sauts positifs avec news de nuit dans le top 10 % : +0,7 × 10⁻³ (t 11,8), alors que les sauts positifs **sans news** (moitié inférieure) ont −0,6 × 10⁻³ (t −10,8). Sauts négatifs dans le top 10 % : −0,5 × 10⁻³ (t −6,8) ; moitié inférieure : +0,9 × 10⁻³ (t 12,4). Donc **léger prolongement des sauts accompagnés de news, léger retournement des sauts sans news**.

### Robustesse
- Sans la fenêtre [−3, +3] autour des résultats (Huang, Tan et Wermers 2019) : conclusions inchangées.
- **2004–2020 (marché électronique)** : la sensibilité de la probabilité de saut à l'illiquidité **augmente**, mais la **taille** des sauts (positifs et négatifs) **diminue**. Robuste aussi sans 2008, 2009, 2020 et sans les titres sous 5 $ (non tabulé).

### À retenir (d'après le papier)
- Un saut de nuit arrive environ une nuit sur 165 (une séance sur 41 pour les sauts de séance).
- Les sauts de nuit sont surtout liés aux **news publiées hors séance** (rapport de cotes 1,62) et au **volume after-hours** (1,35) ; les sauts de séance sont mal expliqués (R² < 1 %), surtout par l'illiquidité.
- Une grosse nuit la veille réduit la probabilité d'un saut de nuit le lendemain.
- Les données utilisées (RavenPack, TAQ) ne sont pas de l'OHLCV.

---

## [12] On the Effectiveness of Stop-Loss Rules: An Analytical Framework Based on Modeling Overnight Gaps and the Stationary Bootstrap (Arratia, Dorador)

**SSRN 3087196 · Universitat Politècnica de Catalunya / Banque centrale européenne · non daté dans le PDF (données jusqu'à mai 2017)**

### Question
Les stop-loss améliorent-ils une position acheteuse « buy & hold » ? Les travaux précédents (Acar et Toffel 2001, Kaminski et Lo 2014, James et Yang 2010) ignoraient les **gaps de nuit**, qui font sauter le stop au-delà du niveau prévu. Ici : deux modèles de prix horaires avec et sans gap de nuit, plus un bootstrap stationnaire sur les données réelles.

### Cadre
- **Long seulement**, **sans slippage ni coûts** (justifié par le choix des 30 actions les plus échangées du NYSE en 2013 et parce qu'une politique sans ré-entrée a les mêmes coûts qu'un buy & hold).
- **Politique de stop pure, sans ré-entrée** : dès que la règle se déclenche, on vend tout et on passe en actif sans risque jusqu'à l'horizon T.
- Hypothèse : rendement attendu de l'action > taux sans risque. Calibrage : taux sans risque = rendement moyen du T-bond 1 an 1990–2017 = **3,171 %** ; rendement attendu = rendement moyen du NYSE 1990–2017 = **6,14 %**, soit 3,942924 × 10⁻⁵ par heure.

### Les 4 règles de stop
1. **Pourcentage fixe sous le plus haut** (stop suiveur) : sortie si P_t < P_max(t−1) × (1 − a), avec a réglé dans **[0,03 ; 0,10]** pour maximiser la moyenne des 5 mesures (la valeur retenue n'est pas donnée).
2. **ATR** : sortie si P_t < P_{t−1} − **2,5 × ATR(14 jours)** (ATR quotidien, test horaire).
3. **RSI** : sortie si **RSI(7) ≥ 70** (surachat).
4. **Triple croisement de moyennes mobiles 5-20-70** : sortie si MM5 < MM20 et MM20 < MM70 (en 3-12-30 jours pour le bootstrap, faute d'historique horaire).

### Mesures de performance
Espérance de rendement, Sharpe, Sortino, et deux nouvelles : **RVaR** = (rendement médian − r_f) / (rendement médian − VaR 5 % à 1 an) et **RES** = même chose avec l'Expected Shortfall 5 %.

### Modèles de prix
- Données : **30 actions NYSE** les plus échangées en 2013, **cours horaires** du 13 au 24 mars 2017 (2 070 rendements horaires) pour calibrer.
- Volatilité : GARCH(1,1) ; la meilleure loi d'innovation (AIC moyen, package fGarch) est la loi d'erreur généralisée (GED), forme ≈ 1,45 (entre Laplace et normale).
- **Modèle 1** : r_t ~ GED(3,943 × 10⁻⁵ ; 0,0042 ; 1,326) avec GARCH(1,1) à innovations GED asymétrique (forme 1,4, asymétrie 0,928).
- **Modèle 2** : r_t ~ ARMA(3,0) avec GARCH(1,1) à innovations GED (forme 1,47).
- **Gaps de nuit** (calibrés sur **204 120 gaps** = 27 ans × 30 actions) : gap moyen = ouverture / clôture veille = **1,000463 (+0,0463 %)** ; un gap de plus de 0,1 % se produit **77,93 % des jours**. Gap modélisé par une **loi de Weibull** (facteur multiplicatif du prix), paramètres choisis parmi 7 méthodes d'estimation puis recherche en grille sur un « Stress » = 0,3 × statistique D de Kolmogorov-Smirnov + 0,7 × erreur quadratique moyenne ; puis **correction du biais de survie** (les 30 titres ont survécu de 1990 à 2017) en réduisant le paramètre de forme pour rendre le gap moyen plus négatif que l'empirique. Valeurs finales : **1,0033 et 170,7193** (Stress 0,0363). Gap appliqué une fois par jour (toutes les 7 barres horaires : t mod 7 = 1).
- **Volatilité après gap** : régression du range relatif (haut − bas)/bas sur un polynôme de degré 3 de la taille du gap → multiplicateur d'écart-type **0,80 sans gap** et **0,80 + 0,25 gm + 0,06 gm² − 0,01 gm³** avec gap (gm = taille du gap) : un gap plus grand → plus de volatilité ensuite.
- Simulations : 10 000 répétitions, répétées 50 fois ; test t de Welch contre le buy & hold.

### Résultats des simulations (marché haussier par construction)
| Règle | Modèle | E(r) stop / B&H | Sharpe stop / B&H | Sortino stop / B&H | RVaR stop / B&H | RES stop / B&H |
|---|---|---|---|---|---|---|
| % fixe, sans gap | M1 | 4,57 % / 7,09 % (ns) | **0,81 / 0,32** | 0,24 / 0,34 | 0,85 / 0,16 | 0,75 / 0,14 |
| % fixe, **avec gap** | M1 | 4,04 % / 4,99 % (ns) | **0,81 / 0,29** | 0,14 / 0,17 | **0,84 / 0,15** | **0,69 / 0,12** |
| % fixe, avec gap | M2 | 4,06 % / 4,93 % (ns) | 0,81 / 0,30 | 0,14 / 0,18 | 0,83 / 0,16 | 0,69 / 0,13 |
| RSI, sans gap | M1 | 6,27 % / 7,04 % (ns) | 0,33 / 0,32 (ns) | 0,27 / 0,32 | 0,22 / 0,16 | 0,19 / 0,13 |
| RSI, avec gap | M1 | 4,51 % / 4,99 % (ns) | 0,31 / 0,29 | 0,14 / 0,18 | 0,24 / 0,15 | 0,20 / 0,12 |
| ATR, sans gap | M1 | 6,49 % / 7,23 % (ns) | 0,32 / 0,32 (ns) | 0,31 / 0,34 | 0,15 / 0,16 | 0,13 / 0,14 |
| ATR, avec gap | M1 | 4,03 % / 4,99 % (ns) | 0,33 / 0,29 | 0,12 / 0,18 | 0,16 / 0,15 | 0,13 / 0,12 |
| MM 5-20-70, sans gap | M1 | 5,73 % / 7,12 % (ns) | 0,32 / 0,32 (ns) | 0,27 / 0,33 | 0,16 / 0,16 (ns) | 0,12 / 0,13 |
| MM 5-20-70, avec gap | M1 | 4,28 % / 4,91 % (ns) | 0,31 / 0,28 | 0,13 / 0,17 | 0,16 / 0,15 | 0,13 / 0,12 |
- Toutes les différences de Sharpe, Sortino, RVaR, RES sont significatives à 0,1 % sauf mention « ns ». **Le Sortino baisse toujours avec le stop** ; l'espérance baisse toujours (de moins de 100 pb avec gaps, jamais significatif).
- Le **stop en pourcentage fixe** est le meilleur (Sharpe presque × 3, RVaR et RES environ × 5), puis le RSI ; ATR et MM n'apportent qu'une petite amélioration (et seulement avec gaps).
- Résultat jugé contre-intuitif par les auteurs : avec les gaps, les stops font plutôt **mieux** (sauf le % fixe, stable). Leur explication : les gros gaps baissiers sont beaucoup plus rares qu'on ne le croit (biais de disponibilité), alors que les petits gaps sont fréquents et que certains stops évitent les petits gaps baissiers tout en profitant des haussiers.

### Bootstrap stationnaire (données réelles)
- Bootstrap stationnaire (Politis et Romano 1994), longueur de bloc automatique (Politis et White 2004). Tests de stationnarité (ADF, KPSS, Phillips-Perron, Priestley-Subba Rao) : seuls **11 titres** ont des rendements horaires faiblement stationnaires du **13 mars au 26 mai 2017** : BAC, PFE, F, C, JPM, MRK, XOM, AIG, HAL, KEY, BMY. 200 000 répétitions. Taux sans risque = T-bill 3 mois de mars 2017 = 0,74 %.
- Sur cette période, **9 des 11 titres ont baissé** (seuls C et AIG ont monté).
- **Espérance de rendement buy & hold → stop % fixe** (en % sur ~2,5 mois) : BAC −7,18 → −0,62 ; PFE −5,68 → −1,97 ; **F −12,87 → −1,62** (+11,3 points) ; C 1,52 → 1,27 ; JPM −6,16 → −0,98 ; MRK −0,37 → −0,07 ; XOM 0,10 → 0,13 ; AIG 3,31 → 3,14 ; HAL −9,56 → −0,71 ; KEY −2,81 → −0,12 ; BMY −7,17 → −1,36. En moyenne **plus de 4 points** de mieux que le buy & hold.
- RSI, ATR et MM améliorent peu l'espérance en marché baissier (ex. F −12,67 avec RSI, −10,68 avec ATR, −12,41 avec MM). Pour les deux titres haussiers (C, AIG), le stop RSI améliore toutes les mesures ajustées du risque au prix d'une très légère baisse d'espérance.

### À retenir (d'après le papier)
- Marché haussier : les stops (surtout le **stop suiveur en % fixe**) améliorent le Sharpe, RVaR et RES mais **réduisent légèrement l'espérance et le Sortino**. Marché baissier : les stops améliorent l'espérance, nettement pour le % fixe.
- Les gaps de nuit sont modélisés comme fréquents (78 % des jours au-delà de 0,1 %), en moyenne légèrement positifs (+0,046 %), et suivis d'une volatilité plus forte.
- Limites visibles dans le papier : 30 grandes valeurs liquides, calibrage sur 2 semaines de données horaires, bootstrap sur 2,5 mois, pas de coûts, pas de ré-entrée, valeur de a non publiée.

---

## [13] Round-Number Anchoring in Overnight US Equity Order Sizes: Evidence from 274 Million Order Events on the Blue Ocean ATS (Lim)

**SSRN 6651000 · version du 26 avril 2026 · chercheur indépendant (Singapour) · non relu ; l'auteur déclare avoir utilisé Claude comme aide à la rédaction**

### Objet
Papier **descriptif** sur la **taille des ordres** passés la nuit sur Blue Ocean ATS. Pas de rendement, pas de stratégie.

### Le marché Blue Ocean (section 2)
- Système de négociation alternatif (ATS) américain, carnet d'ordres électronique sur les actions NMS, **20:00 – 4:00 ET, du dimanche au jeudi soir** (heures ouvrées d'Asie-Pacifique).
- **Uniquement des ordres limites à la journée ; vente à découvert désactivée** ; bande de prix de **±20 %** autour d'un prix de référence fixé à **19:30 ET** ; pas de taille minimale.
- Pendant la période étudiée, **aucune autre plateforme américaine « lit » continue** n'opère sur cette fenêtre. Accès direct réservé aux broker-dealers américains ; les clients non américains passent par accès sponsorisé ; **flux dominé par les particuliers coréens** (Korea Times 2026). Selon l'auteur, c'est la principale source de découverte des prix des actions US pendant les heures asiatiques.

### Données
- Databento, jeu **OCEA.MEMOIR** (message par ordre, horodatage à la nanoseconde, identifiant d'ordre persistant), données institutionnelles disponibles depuis août 2025.
- **30 titres** : 5 ETF (SPY, QQQ, DIA, IWM, TQQQ) + 25 actions (AAPL, AMD, AMZN, AVGO, BA, BAC, COIN, CSCO, DIS, GOOGL, JPM, KO, META, MSFT, MU, NFLX, NVDA, PFE, PLTR, SMCI, T, TSLA, VZ, WMT, XOM).
- **24 août 2025 – 30 mars 2026** ; **273 908 859 ajouts d'ordres** (seuls les ajouts sont analysés, pas les annulations, modifications ni exécutions).

### Méthode
- Test du « dip » de Hartigan (approximation par enveloppe unimodale, p-value bootstrap) sur log(taille).
- Mélanges gaussiens en log, k = 1 à 10, choix par BIC (sous-échantillon de 200 000 par titre).
- Masse empirique à chaque entier de 1 à 100 et à des tailles rondes plus grandes.
- Ensemble de **34 tailles rondes** : 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 750, 800, 900, 1 000, 1 500, 2 000, 2 500, 3 000, 5 000, 10 000.

### Résultats
- **Multimodalité** : unimodalité rejetée à 5 % pour 30 distributions sur 31 (30 titres + l'agrégat) ; seul JPM ne rejette pas (p = 1,000, plus petit échantillon : 1,2 million d'ajouts). Le BIC choisit k = 9 ou 10 partout (agrégat k = 10) ; aucune ne choisit k < 3. Plusieurs composantes ont un écart-type quasi nul : ce sont de vraies masses ponctuelles à des entiers.
- **40,0 %** des ordres sont à l'une des 34 tailles rondes.
- **Taille la plus fréquente : 20 actions = 5,27 %** de tous les ajouts (14,4 millions, contre ~1,2 million à 19 actions et ~1,0 million à 21). Puis **1 action 4,67 %**, **100 actions 2,84 %**, 40 actions 1,96 %, 2 actions 1,92 %, 10 actions 1,56 %, 5 actions 1,23 %, 50 actions 1,21 %, 80 actions 1,20 %. Tailles plus grandes : 200 actions 2,83 %, 300 : 2,05 %, 400 : 2,38 %, 500 : 2,39 %, 700 : 1,43 %, 800 : 1,81 %, 1 000 : 0,64 %, 2 000 : 0,13 %, 5 000 : 0,06 %, 10 000 : 0,02 %.
- Les études NYSE/NASDAQ en séance (Alexander et Peterson 2007) trouvent des modes à 500, 1 000 et 5 000 actions, jamais sous 100 : **le mode à 20 actions est propre à ce marché**.
- **Par titre** : part ronde de **15,5 % (TQQQ)** à **67,3 % (DIA)** ; IWM 53,0 %, SPY 54,5 %, QQQ 47,0 % ; BA 64,7 %, NFLX 58,5 % ; TSLA 25,9 %, AVGO 23,9 %, AMD 22,5 %.
- **Le mode dépend du prix du titre** (ancrage sur un montant en dollars) : titres chers (META ~647 $, MSFT ~413 $, NVDA ~183 $) concentrés à 20 actions ; AAPL (~262 $) et COIN (~212 $) entre 20 et 100 ; ETF moins chers à des tailles plus grandes (taille médiane TQQQ 1 300 actions, IWM 460). **TSLA (~364 $) a un mode à 119 actions** (35 % du poids de la composante).
- **T (AT&T) : 23,9 % des ordres à exactement 500 actions** ; VZ 19,4 % ; BAC 13 % ; PFE 12 % (titres à dividende peu chers, comptes de revenu selon l'auteur).
- Mélanges (Table 3) : agrégat, modes à 1, 2, 10, 20, 35, 60, 111, 264, 644, 3 137 actions (poids max 24,5 % sur 264) ; la composante « 1 action » existe pour tous les titres (poids 1,9 % pour TQQQ à 10,4 % pour KO) ; PFE 36,5 % sur ~972 actions.

### Interprétation et limites (d'après l'auteur)
- Le mode à 20 actions, stable sur toute la session de 8 heures, reflète probablement un choix de structure : taille par défaut chez les courtiers sponsors (coréens), optimisation de la grille tarifaire, ou convention des particuliers d'Asie-Pacifique. Non identifiable avec ces données.
- Conséquence : les filtres « 100 actions = lot institutionnel » des études de séance classent mal ce flux de nuit.
- Limites : pas d'identifiant de courtier, seulement les ajouts, 30 grandes valeurs, phase de monopole de Blue Ocean (les motifs peuvent changer quand les bourses ouvriront des sessions de nuit), test du dip approximatif, k plafonné à 10.
- Petites incohérences du texte : TSLA figure à la fois dans la liste des titres à k = 10 et à k = 9 ; « 30 sur 31 » rejettent alors que JPM a p = 1,000 (cohérent : c'est le 31e).

### À retenir
- Concerne seulement la **taille des ordres** de nuit sur un marché de particuliers asiatiques ; aucune information sur les prix ou les rendements.

---

## [15] What Crosses Borders? The New York Cash Session and the Cross-Section of Asia-Pacific Transmission (Kinoshita)

**SSRN 7091018 · Kobe University (Graduate School of Economics) · « working paper, preliminary draft », non daté · l'auteur déclare avoir utilisé Claude pour la langue uniquement**

### Question
Un papier compagnon (Kinoshita 2026, cadre « t−0,5 ») montre que l'information de la clôture de New York prévoit la direction du lendemain en Asie-Pacifique, surtout via le **gap d'ouverture**. Ici : **quelle partie de la journée new-yorkaise** porte l'information (la nuit ou la séance au comptant) et **où elle arrive** (quels marchés, quels secteurs).

### Cadre temporel
- t = 0 : clôture de New York (**06:00 heure de Tokyo, JST**) ; t = 0,5 : ouverture de Tokyo (**09:00 JST**) ; t = 1 : clôture suivante de New York. Les prédicteurs sont connus à 06:00 JST, alors que les cibles ouvrent au plus tôt vers 08:00–10:30 JST : pas de fuite d'information possible selon l'auteur.

### Données et méthode
- Quotidien, **Yahoo Finance (yfinance)**, **1er décembre 2009 – 1er janvier 2024**.
- Prédicteurs (rendements log à la clôture de NY) : S&P 500, VIX, rendement du 10 ans US (TNX), USD/JPY.
- Cible : **signe du gap d'ouverture du lendemain** = log(ouverture / clôture précédente), pour **9 marchés** (Japon, Corée, Hong Kong, Australie, Inde, Taïwan, Singapour, Indonésie, Malaisie) et les **17 ETF sectoriels TOPIX-17** japonais (26 cibles).
- **Régression logistique « walk-forward »** : réestimée chaque jour sur une fenêtre glissante (2 800 jours pour les marchés ; 1 250 pour les secteurs et la décomposition), standardisation sur la seule fenêtre d'apprentissage, prévision à 1 pas.
- Mesure : **précision directionnelle (DA)** hors échantillon, test z contre 50 %, intervalles de Wilson à 95 % pour les secteurs. **Les jours où l'ouverture est égale à la clôture précédente (gap nul, cotation périmée) sont retirés.**
- Test complémentaire : futures E-mini S&P 500 horaires (ES=F), seulement sur les **2 dernières années** (données gratuites), donc « preuve de concept ».

### Résultat 1 : c'est la séance au comptant de New York qui compte (Table 1)
Prédicteur = S&P 500 seul, découpé en nuit ON = log(ouverture/clôture veille), séance ID = log(clôture/ouverture), total FULL.

| Cible | ON | ID | FULL | ID − ON |
|---|---|---|---|---|
| KOSPI (Corée) | 62,2 | **75,8** | 75,7 | +13,6 |
| NIFTY 50 (Inde) | 68,2 | 75,5 | 74,9 | +7,3 |
| Nikkei 225 | 61,4 | 71,9 | 74,1 | +10,5 |
| TAIEX (Taïwan) | 64,0 | 71,2 | 73,1 | +7,3 |
| STI (Singapour) | 58,1 | 70,6 | 71,5 | +12,5 |
| Jakarta | 65,2 | 70,5 | 71,2 | +5,3 |
| Hang Seng | 59,1 | 69,9 | 69,6 | +10,8 |
| ASX 200 (gap peu fiable, beaucoup d'ouvertures périmées) | 57,6 | 67,0 | 66,5 | +9,4 |
| KLCI (Malaisie) | 57,2 | 64,1 | 65,0 | +7,0 |
| Moyenne des 17 secteurs | 60,1 | 65,4 | 66,5 | +5,3 |
- La séance bat la nuit dans **26 cibles sur 26**, de **6,6 points en moyenne** ; la séance seule reproduit **98,6 %** de la précision du rendement total ; ajouter la nuit à la séance n'ajoute que **+0,97 point** en moyenne.
- Explication de l'auteur : la nuit new-yorkaise reflète surtout les séances asiatique et européenne précédentes (un écho) ; la séance au comptant est l'information américaine nouvelle et la plus proche de l'ouverture de Tokyo. L'Inde (la plus éloignée en heure) a une nuit inhabituellement informative.
- Les modèles de cette table (S&P 500 seul) ne sont pas comparables directement au modèle à 4 variables de la section 6.

### Résultat 2 : les futures après la clôture n'ajoutent rien
- Futures : niveau vers 06:00 JST (équivalent de la clôture) → **DA 72,6 %** (p < 0,001). Ajouter la dérive des futures de 06:00 à 08:00 JST (1 heure avant l'ouverture de Tokyo) : **72,2 %** (−0,4 point). La dérive seule : 59,3 %, et ce chiffre est gonflé car le niveau de 08:00 bouge avec l'ouverture. **L'information est figée à la clôture de la séance au comptant de NY.**

### Résultat 3 : coupe transversale et « loi du bêta »
- Les 9 marchés sont prévisibles au seuil de 0,1 %, et partout la précision sur le gap d'ouverture dépasse celle sur le close-to-close.
- **Secteurs TOPIX-17 (Table 2, DA du gap, bêta)** : machines électriques et de précision 72,0 % (0,54) ; IT et services 70,5 % (0,48) ; automobiles 70,1 % (0,49) ; machines 69,9 % (0,61) ; matériaux et chimie 69,5 % (0,50) ; banques 68,9 % (0,43) ; acier et non-ferreux 68,9 % (0,58) ; négoce 68,5 % (0,61) ; construction 68,5 % (0,45) ; immobilier 67,2 % (0,54) ; pharmacie 66,4 % (0,31) ; financières hors banques 66,3 % (0,53) ; transport et logistique 66,2 % (0,34) ; distribution 66,1 % (0,41) ; énergie 64,1 % (0,50) ; alimentation 63,4 % (0,29) ; électricité et gaz 61,6 % (0,19). Tous significatifs à p < 0,001. Les secteurs cycliques exportateurs sont ~10 points au-dessus des défensifs domestiques ; l'ordre fin n'est pas identifié (intervalles qui se chevauchent).
- « Bêta d'information de nuit » = pente de r_secteur(t) sur r_S&P500(t−1) (bêta de réaction décalé, pas un bêta CAPM).
- **DA du gap (%) = 60,07 + 16,26 × bêta** ; r = 0,70, **R² = 0,49**, p = 0,0018 ; permutation (5 000) p = 0,001 ; IC bootstrap de la pente [6,9 ; 22,1].
- Échantillons disjoints (bêta sur la 1re moitié, précision hors échantillon sur la 2e) : pente +6,7, **non significative** (R² = 0,13, p de permutation 0,15).
- Proxy exogène (part des ventes / production à l'étranger, enquêtes METI et JBIC : autos ~48 %, électrique ~41 %, chimie ~31 %, alimentation ~23 % ; secteurs non manufacturiers estimés) : R² = 0,26, p = 0,04, IC [2,2 ; 15,9]. L'auteur parle d'une régularité descriptive, pas causale.

### Résultat 4 : l'exception de l'énergie
- Ajout de chacun des 9 ETF sectoriels américains au modèle de base pour chacun des 17 secteurs (153 ajouts) : effet moyen **+0,01 point** (écart-type 1,06), jamais plus de ~2 points, **sauf énergie** : **XLE ajouté au secteur énergie japonais : +6,6 points** (~6,7 écarts-types) ; l'effet de XLE sur les 16 autres secteurs : +0,08 point en moyenne, max ~1,4.
- Décomposition de XLE pour le secteur énergie (base 64,1 %) : + nuit de XLE → 66,0 % (+1,9) ; + séance de XLE → 68,9 % (+4,8) ; + total → 70,9 % (+6,7). Placebo sur les machines : moins de 0,5 point. Environ un quart de l'effet est déjà présent à l'ouverture de NY (news pétrole pendant la séance européenne), le reste en séance (dont le rapport EIA du mercredi, une heure après l'ouverture de NY).

### Limites (d'après l'auteur)
- La précision directionnelle **n'est pas un résultat de trading** : pas de coûts, pas de slippage, liquidité faible de la pré-ouverture ; l'objectif est de mesurer la transmission, pas de proposer une stratégie. L'auteur lit le résultat comme un **réajustement rationnel à l'ouverture**, pas une anomalie exploitable durable.
- Test futures sur 2 ans seulement ; ETF sectoriels avec des fenêtres hors échantillon plus courtes et des ouvertures périmées ; décomposition faite avec le S&P 500 seul ; tests multiples dans le balayage sectoriel.
- Les précisions élevées (75,8 % KOSPI, 71,9 % Nikkei) viennent du choix de la cible (le gap d'ouverture, peu bruité), pas d'un modèle supérieur (la littérature ML annonce 50–55 % en close-to-close).

### À retenir
- Pour prévoir le **signe du gap d'ouverture asiatique**, le rendement **ouverture → clôture du S&P 500 au comptant** suffit presque ; la nuit du S&P 500 et la dérive des futures après 16:00 ET n'ajoutent rien.
- Prévisibilité proportionnelle à l'exposition au risque mondial ; l'énergie dépend en plus du XLE.

---

## [16] Exchange Rate Volatility, Macro Announcements and the Choice of Intraday Seasonality Filtering Method (Laakkonen)

**SSRN 1032876 · Bank of Finland Research Discussion Papers 23/2007 · Université de Jyväskylä**

### Question
Pour étudier l'effet des annonces macro sur la volatilité intraday, il faut d'abord retirer la **saisonnalité intraday** de la volatilité (le profil en U de la journée). Le choix de la méthode change-t-il les résultats sur l'effet des news ?

### Données
- **EUR/USD, cotations à 5 minutes, 1er janvier 1999 – 31 décembre 2004** (Olsen and Associates). Week-ends et certains jours fériés exclus, **heures d'été US et Europe prises en compte**. Week-end défini comme **vendredi 21:05 GMT → dimanche 21:00 GMT** (définition d'Andersen et Bollerslev 1998).
- Annonces : **Bloomberg World Economic Calendar**, toutes les annonces macro programmées des **États-Unis, d'Allemagne et du Japon**. Les annonces US sont séparées en « **US régulières** » (toujours à **13:30 et 15:00 GMT**) et « autres US ».
- Volatilité mesurée par le rendement absolu.

### Profil intraday de la volatilité EUR/USD (Figure 2.1)
- Petite hausse à l'**ouverture de l'Extrême-Orient vers 23:00 GMT** ; hausse plus forte à l'**ouverture européenne vers 7:00 GMT** ; **niveau le plus haut après l'ouverture américaine vers 14:00 GMT**.
- **Deux pics nets à 13:30 et 15:00 GMT** (heures des principales statistiques US).
- Ce profil répété chaque jour crée un motif en U dans l'autocorrélation de la volatilité (corrélogramme sur 1 500 retards de 5 minutes = 5 jours), presque identique chaque jour.

### Les trois méthodes comparées
1. **FFF (Flexible Fourier Form, Andersen et Bollerslev 1997)** : on divise le rendement absolu (démoyenné) par la volatilité quotidienne GARCH(1,1) / √288, on régresse 2 ln(...) sur des sinus et cosinus (**P = 9** selon AIC et BIC), une tendance quadratique et des indicatrices (jours fériés, jours de semaine, lundi) ; saisonnalité = exp(valeur ajustée / 2). Estimée sur tout l'échantillon, puis par année, trimestre ou **semaine**.
2. **LOWESS (Cleveland 1979)** : lissage par régression locale pondérée, paramètre de lissage 0,0003 / 0,0002 / 0,0001 (fenêtres d'environ 6, 4 et 2 heures).
3. **IAOM (Bauwens, Ben Omrane et Giot 2005)** : racine de la moyenne des rendements au carré pour chaque intervalle de 5 minutes et chaque jour de semaine (vendredi et dimanche fusionnés), sur tout l'échantillon, par année ou par trimestre.
- Dans tous les cas, l'estimation de la saisonnalité est normalisée à une moyenne de 1, et on divise les rendements par elle.

### Résultats sur données réelles
- **Saisonnalité restante** : FFF sur tout l'échantillon ou par année laisse beaucoup de périodicité ; par trimestre c'est mieux ; **par semaine il ne reste plus de périodicité**. LOWESS : plus de périodicité du tout avec 0,0001. IAOM : mieux en sous-périodes courtes, mais l'effet de la longueur est moindre. → **La saisonnalité intraday change dans le temps** (ex. les heures européennes étaient bien plus volatiles dans les premières années de l'euro).
- **Effet des news** : variable de news = profil de décroissance polynomial de degré 3 sur les **25 intervalles de 5 minutes (2 heures)** suivant l'annonce : λ(i) = 0,054 (1 − (i/25)³) − 0,009 (1 − (i/25)²) i + 0,0007 (1 − (i/25)) i². Hausse de volatilité 5 minutes après l'annonce M(1) (Table 3.1) :

| Filtrage | Japon | Allemagne | US autres | US régulières (13:30/15:00) |
|---|---|---|---|---|
| aucun | −25 % | +133 % | +105 % | **+404 %** |
| FFF tout l'échantillon | +4 % (ns) | +12 % | +44 % | +83 % |
| FFF annuel | +10 % | +15 % | +33 % | +52 % |
| FFF trimestriel | +4 % (ns) | +25 % | +40 % | +72 % |
| FFF hebdomadaire | 0 % | +34 % | +42 % | +87 % |
| LOWESS 0,0003 | +2 % | +65 % | +55 % | **+140 %** |
| LOWESS 0,0002 | 0 % | +53 % | +46 % | +106 % |
| LOWESS 0,0001 | −3 % | +41 % | +34 % | +77 % |
| IAOM tout | −3 % | +47 % | +48 % | +83 % |
| IAOM annuel | −1 % | +46 % | +47 % | +78 % |
| IAOM trimestriel | −1 % | +45 % | +45 % | +74 % |
  - **Les annonces US régulières ont de loin le plus gros effet** ; Allemagne et US augmentent significativement la volatilité ; **le Japon n'a pas d'effet** sur l'EUR/USD.
  - La méthode change l'ampleur : de −3 % à +10 % pour le Japon, de **+52 % à +140 %** pour les US régulières. Avec FFF, plus la sous-période est courte, plus les coefficients sont grands ; avec LOWESS et IAOM, c'est l'inverse.
- **Propriétés des rendements filtrés** (Table 4.1) : moyenne et écart-type quasi inchangés ; **kurtosis brute 65,9** ; FFF la change de façon irrégulière (40,9 à 239,4) et **crée de nouveaux sauts** ; LOWESS (5,0 à 8,9) et IAOM (3,9 à 10,0) **écrasent les gros sauts**. FFF reste le plus proche des rendements d'origine.

### Simulation (2 000 réalisations de 1 000 jours × 288 intervalles)
- Rendement simulé = volatilité quotidienne GARCH(1,1) × saisonnalité intraday (modèle à 47 indicatrices de demi-heure estimé chaque mois sur l'EUR/USD, pour ne favoriser aucune méthode) × composante news × choc (mélange de normales : variance 0,5 avec probabilité 0,75, variance 2,0 avec probabilité 0,25).
- News : 2 % des intervalles, conditionnées à l'ouverture du marché concerné ; vraies hausses de volatilité 5 minutes après : **Asie +5 %, Europe +20 %, US +40 %, US régulières +80 %**.
- Biais moyens du coefficient estimé (vraie valeur 1,05 / 1,2 / 1,4 / 1,8) :
  - **Sans filtrage** : Asie −0,38 ; Europe **+0,96** ; US −0,05 ; US régulières **+2,95** → sans filtre on surestime fortement les news européennes et américaines régulières et on sous-estime les asiatiques.
  - Sans saisonnalité dans le processus : biais ≈ 0 (c'est bien la saisonnalité qui pose problème).
  - **FFF** : +0,04 / −0,02 / −0,09 / −0,37. **LOWESS** : −0,01 / −0,12 / −0,30 / −0,55. **IAOM** : +0,01 / +0,06 / −0,12 / −0,51.
- Toutes les méthodes **sous-estiment** l'effet des news US et européennes (elles filtrent une partie de l'effet), et d'autant plus que la news est grosse et **régulière dans l'horaire**. LOWESS filtre le plus d'effet des news ; IAOM est presque aussi bon que FFF sauf pour les annonces à heure fixe, où il est très biaisé.

### À retenir (d'après le papier)
- Pour l'EUR/USD à 5 minutes : la volatilité monte à l'ouverture européenne (7:00 GMT) et surtout américaine (14:00 GMT), avec des pics aux annonces US de 13:30 et 15:00 GMT ; l'effet d'une annonce dure environ **2 heures**.
- Le profil intraday change dans le temps : l'estimer sur des fenêtres courtes (semaine pour FFF).
- **Méthode recommandée : FFF**, en sachant que tout filtrage sous-estime l'effet des news, surtout celles publiées toujours à la même heure.

---

## [17] Extending Exchange Trading Hours: A Coordination Perspective (Lin)

**SSRN 6224760 · juin 2026 · World Federation of Exchanges (avis personnel de l'auteur) · l'auteur déclare avoir utilisé ChatGPT pour la langue uniquement**

### Objet
Papier de **structure de marché, sans données de rendement**. Thèse : allonger les horaires de cotation des actions US vers le **23/5** n'est pas qu'une question d'accès ; c'est un problème de **coordination de tout le cycle de vie de l'ordre** (données de marché, déclaration, compensation, marges, financement, conservation, paiements, règlement-livraison).

### Faits institutionnels donnés par le papier
- **NYSE Arca, Nasdaq et la nouvelle 24X National Exchange** ont reçu l'approbation de la SEC pour passer au **23/5 en décembre 2026** : la semaine commence le **dimanche 21:00 ET** et finit le **vendredi 20:00 ET**, avec une **fermeture quotidienne d'une heure de 20:00 à 21:00 ET**.
- Plateformes de nuit existantes citées : Blue Ocean, Bruce Markets, Interactive Brokers, Moon ATS. Elles restent secondaires : la séance régulière garde la liquidité la plus profonde et la meilleure découverte des prix.
- Table A1 (60 bourses) : toutes les bourses d'actions fonctionnent encore dans une fenêtre bornée, **typiquement 5 à 9 heures par jour** (le tableau lui-même n'est pas lisible dans l'extraction du PDF).
- **NSCC** : ouverture de l'Universal Trade Capture étendue à **1:30 ET en septembre 2024** ; passage en **24/5 en juin 2026** (dimanche soir à vendredi soir).
- Selon l'approbation (FAQ NYSE) : les transactions de la session du soir exécutées **après 21:00 ET et avant minuit** sont envoyées à la DTCC avec la **date de compensation du jour calendaire suivant**, et réglées un jour après.
- **CME Globex** : du dimanche 17:00 au vendredi 16:00 heure de Chicago, avec de courtes pauses ; la compensation n'est pas continue mais suit des cycles intraday et de fin de journée, avec surveillance continue du risque.
- Littérature citée : la nuit contribue à la découverte des prix mais avec moins d'activité et des coûts bien plus élevés (Barclay et Hendershott 2003, 2004) ; la nuit US actuelle est **concentrée sur quelques titres liquides et ETF, et sur les particuliers** (Eaton, Shkilko et Werner 2025) ; les fermetures de marché peuvent servir à **concentrer la liquidité** (Blonien et Ober 2024) ; plus d'accès n'améliore pas forcément la performance des particuliers (deHaan et Glover 2024) ; le sommeil et l'attention jouent sur la qualité des décisions (Han et al. 2025).

### Étude de cas : règlement des changes par CLS
- CLS (paiement contre paiement des deux devises) : ouvert du dimanche 22:00 au samedi 02:00 heure d'Europe centrale (CET) ; une instruction est éligible au cycle T+1 si elle est soumise **avant 00:00 CET** ; règlement entre 07:00 et 09:00 CET ; versement des dollars vers **12:00 CET**.
- Hypothèses : l'investisseur non américain soumet l'ordre de change en même temps que l'achat d'actions, passe par CLS, sans retard opérationnel ; décalage constant de 6 heures entre ET et CET (5 heures pendant les semaines où les changements d'heure ne coïncident pas) ; obligation de paiement des actions à **20:00 ET le jour 1** pour une transaction avant 21:00 ET, et à 20:00 ET le jour 2 pour une transaction entre 21:00 et minuit.
- **Les 5 cas** :
  1. **Séance régulière 9:30–16:00 ET** : change avant la coupure CLS, dollars vers 12:00 CET le jour 1, actions réglées à 02:00 CET le jour 2 → aligné.
  2. **16:00–18:00 ET** : encore avant la coupure, aligné mais plus serré (les intermédiaires imposent souvent des coupures internes plus tôt).
  3. **18:00–20:00 ET** : **après la coupure CLS** (dollars le jour 2 à 12:00 CET) mais **avant le changement de date de compensation de 21:00** (actions dues le jour 1 à 20:00 ET) → **les dollars arrivent trop tard** : il faut préfinancer en USD, utiliser le crédit du courtier ou du conservateur, un change hors CLS, ou décaler l'exécution. **C'est le seul vrai décalage.**
  4. **21:00–00:00 ET** : après la coupure, mais le règlement des actions est repoussé d'un jour → aligné.
  5. **00:00–9:30 ET** : avant la coupure, aligné.
- La fenêtre 18:00–20:00 ET tombe pendant la **matinée des investisseurs d'Asie-Pacifique**, et elle contient la **nouvelle clôture de 20:00 ET**. Si une partie importante du volume se concentre près de cette clôture (comme aujourd'hui près de 16:00, Cushing et Madhavan 2000 ; Bogousslavsky et Muravyev 2023), ou si une **enchère ou un prix de clôture de référence à 20:00 ET** est créé, le problème s'aggrave.
- Concerne surtout les institutions étrangères (gérants, sponsors et participants autorisés d'ETF, conservateurs, courtiers, teneurs de marché) ; pour les particuliers, les courtiers absorbent le change ; les investisseurs domestiques en dollars ne sont pas concernés. Problème modeste tant que la nuit reste dominée par les particuliers.

### Comparaisons
- **Futures** : le 23/5 coexiste avec des cycles de règlement périodiques, parce que capture, marges et risque tournent en parallèle ; mais l'analogie est incomplète (les actions demandent livraison contre paiement, conservation, opérations sur titres, et la devise de règlement).
- **Cryptomonnaies** (BTC, ETH, LTC sur Coinbase, Kraken, FTX, 1er janvier – 30 juin 2021) : même ouvert 24/7, **le volume se concentre autour de 00:00 UTC et 16:00 UTC** (matinée asiatique et chevauchement Europe / Amérique du Nord), plus faible quand ni l'Asie ni les États-Unis ne sont actifs. Illustratif, pas prédictif.
- **Actions tokenisées** : capitalisation passée d'environ **5,42 Md$ début 2025 à 19,32 Md$ en mars 2026** (CoinGecko), moins de 1 % du volume des actions sous-jacentes ; exemple xStocks (Kraken / Backed Finance) ; projets Nasdaq et DTCC. Le token ne règle pas le problème de la jambe cash (préfinancement, monnaie de règlement fiable).

### À retenir (d'après le papier)
- À partir de **décembre 2026**, le marché US actions passerait à 23/5 avec une **clôture quotidienne à 20:00 ET** et une réouverture à 21:00 ET.
- La liquidité de nuit restera probablement plus mince et plus chère ; l'auteur recommande d'utiliser les heures étendues **de façon sélective** et de garder les gros ordres sensibles à la liquidité pour les périodes de forte participation (Keim et Madhavan 1998).
- Aucun test empirique sur les prix ou les rendements.

---
