# Récolte 1 — règles des papiers overnight, IC 95 % sur NQ, ES, YM, GC et forex

*2026-10-30. 18 PDF de la récolte 1 relus en entier (texte, tableaux, annexes présentes dans les PDF). Code : [recolte1/rules.py](../recolte1/rules.py), [recolte1/engine.py](../recolte1/engine.py), [run_recolte1.py](../run_recolte1.py). Résultats bruts : [results/recolte1/ic.csv](../results/recolte1/ic.csv).*

## Méthode

- **Données** : `D:/quant-data/Cotations`, barres 1 minute Databento `.v.0`, 2016-01 → 2026-08. Actifs : NQ, ES, YM, GC, 6E, 6B, 6J, 6A.
- **Roulements** : ajustement en ratio, un roulement par cycle d'échéance (règle de `run_sessions.py`, et non `fab.core.load` qui en rate une dizaine par actif). Trimestriels (indices, forex) : plus grand écart à 00:00 UTC entre le 7 et le 22 de mars/juin/sept./déc. → 42 roulements par actif. Or : plus grand écart entre le 20 d'un mois impair et le 5 du mois suivant → 64 roulements.
- **Prix à l'instant T** : clôture de la dernière barre démarrant dans [T−5 min, T−1 min] ; sinon le trade est écarté. Fenêtre élargie pour [20] (60 min, fin de période dans la pause CME) et [21] (dernière clôture de la session, comme le papier).
- **Horloge** : séances NYSE (calendrier XNYS, 9:30 → 16:00, 13:00 les demi-séances) pour tous les actifs, sauf quand le papier fixe son horloge (heures ET de [1], [4], [14] ; sessions UTC de [21] ; périodes CET de [20]). « Nuit » = clôture de la veille → ouverture ; « jour » = ouverture → clôture. Pour [7] (séance officielle du future), variante supplémentaire sur la séance propre de GC (8:20–13:30 NY) et du forex (8:00–16:00 Londres).
- **Exécution** : vectorbt `Portfolio.from_orders` (taille en % cible, long et short), rendement de chaque trade lu dans `pf.trades`. Brut = sans frais ; net = 1 tick + 5 $ de commission par aller-retour (convention du dépôt).
- **IC 95 %** : bootstrap par blocs mobiles circulaires (blocs de 10, 2 000 tirages, percentile) sur (a) le rendement moyen par trade en points de base, brut et net, et (b) le Sharpe annualisé des rendements journaliers nets (jours sans position = 0). ▲ = IC net par trade entièrement > 0 ; ▼ = entièrement < 0.
- **Adaptations** : les papiers sur actions trient en coupe transversale ; sur un seul actif, le tri est remplacé par le signe du signal (série temporelle) et les quantiles par des quantiles historiques en fenêtre expansive (aucune donnée future). Chaque adaptation est signalée ci-dessous.
- **Multiplicité** : environ un millier de tests ; à 5 %, ~50 IC excluent zéro par hasard. Un IC qui exclut zéro n'est pas une validation.

## Règles extraites, papier par papier

Seules des règles écrites dans les papiers sont testées. Les adaptations au cas d'un seul actif sont signalées par « adapt. ».

| # | Papier | Règles testées | Non testable (donnée absente des cotations) |
|---|---|---|---|
| [1] | Boyarchenko-Larsen-Whelan (ES 1998–2020) | Table IX : CTC 16:15→16:15, CTO 16:15→9:30 (texte) et →8:30 (légende), OTC 9:30→16:15, −OR short 8:30→10:00, OD 2:00→3:00 ET, OD+ 1:30→3:30 ; OD défini comme l'ouverture européenne (7:00→8:00 Londres, qui suit les semaines où l'écart Londres–NY vaut 4 h) ; short 9:00→10:00 (tous jours, puis jeudi et vendredi) ; long chaque heure ET (Table I, 24 règles) | BtD : il faut le RSV de clôture (volume signé au bid/ask) ; interaction avec le VIX |
| [2] | Berkman-Koch-Tuttle-Zhang (actions US 1996–2008) | DIFF = long nuit + short jour ; attention VOL(t−1) = (rendement close-to-close d'hier)² dans le tercile haut → long nuit, short jour, les deux ; + « difficile à évaluer » (vol 20 j > médiane) ; + lundis. Adapt. : terciles sur l'historique de l'actif, fenêtre expansive | Net achat retail, détention institutionnelle, short interest, sentiment Baker-Wurgler |
| [3] | Lu-Qin (actions US 1996–2020) | NMD (long nuit, short jour) avec ouverture déplacée à 10:00, 10:30 et 11:00 et clôture avancée à 14:30, 15:00 et 15:30 (Table 6 A) ; signaux mensuels triés par ordre croissant (Table 1) : MOM 12-1 → NMD +, STR 1 mois → NMD −. NMD 9:30/16:00 = DIFF de [2] | Signaux rD,t et rN,t : leur définition est dans l'annexe en ligne, absente du PDF, et le signe de la Table 1 contredit LPS ; testés via [11]. Facteurs SDF/CS, ordres retail, LIQ |
| [4] | Jones-Pyun-Wang (actions US + SPY 1993–2021) | Signal r = 9:45→15:00 ; nuit 15:59→9:45 × signe(r) ; nuit long seulement si r > 0 (asymétrie) ; jour suivant 9:45→15:59 × −signe(r) ; nuit − jour (Table 8). Demi-séances exclues comme jours de signal | Déséquilibres d'ordres, dispersion transversale, mispricing SYY, Google |
| [6] | Hendershott-Livdan-Rösch (actions US et 39 pays) | Stratégie 1 (sect. 3.6) en coupe transversale sur les 8 actifs : poids β_i − β̄ la nuit, opposé le jour ; β = pente des nuits de l'actif sur les nuits du « marché », 12 mois glissants, ≥ 30 obs. Adapt. : marché = ES | Futures Treasury (day > 0, night ≤ 0) |
| [7] | Tompkins-Wiener (futures S&P, FTSE, DAX, CAC, Nikkei) | O/C long, C/O long, « alpha » = long C/O + short O/C ; variante sur la séance propre du future pour GC et le forex. C/C = CTC de [1] | Rupture Bâle I 1998 (hors échantillon) |
| [8] | Abdi (actions US 1993–2016) | Nuit < 0 → short le jour ; → long la nuit suivante ; cycle complet ; idem avec signal « marché » = nuit de l'ES. Adapt. : l'actif lui-même sert de marché | Spreads effectifs, flux d'ordres, double tri bêta/IVOL |
| [9] | Branch-Ma (actions US + SPY 2011–2017) | Jour × −signe(nuit du jour) (règle de la sect. IV.E) ; restreint aux quartiles extrêmes de la nuit (Table 4). Adapt. : quartiles historiques par signe | — |
| [10] | Bahcivan-Dam-Gonenc (actions US 1993–2021) | Sauts de nuit de Lee-Mykland (K = 16) ; contrarian dès l'ouverture, détention 1 à 5 jours (Table 16) ; jambes négative et positive séparées. α n'est pas donné par le papier → testé à 1 % et 5 % | Tri mensuel transversal des sauts (Table 17) |
| [11] | Bahcivan (actions US 1993–2021) | Tug of war de Lou-Polk-Skouras : cumul nuit du mois m → nuit m+1 (+), jour m+1 (−) ; cumul jour → nuit (−), jour (+) ; tous mois / mois avec saut / sans saut (Lee-Mykland 1 %). Adapt. : signe du cumul de l'actif au lieu des déciles | — |
| [13] | Song (SPY, QQQ, BTC) | — | Tout : le signal est le rendement du Bitcoin |
| [14] | Donninger (ES, NQ 2010–2014) | Long 16:00→9:30 ; sortie 9:30 si la nuit perd, sinon 9:33 ; idem sans entrée le vendredi | Filtre IVTS = VIX/VXV > 0.87 |
| [15] | Vojtko-Hanicová (SPY 2018–2021) | Nuit sans filtre ; nuit si close(veille) > MM10, MM20, MM50 ; MM20 + nuit précédente < 0 | Filtres VIX et Brain Market Sentiment |
| [17] | Zhang-Zhao (SPY, QQQ, ES, NQ) | Aucune règle de trading. Relations vérifiées : corr(log RV nuit, log RV jour), corr(log RV jour t−1, log RV nuit t), part de variance de nuit. Nuit = 18:00 ET veille → 9:30, RV 5 min | Modèles HAR et SV bayésiens (pas des règles) |
| [18] | Ahoniemi-Lanne (S&P 500 cash) | Aucune règle de trading. Relation vérifiée : levier corr(r_{t−1}, RV jour t) | — |
| [19] | Aretz-Bartram (48 000 actions, 35 pays) | Jour long et nuit long par jour de semaine (Table 1) ; momentum 12-1 et reversal 36-13 appliqués au jour et à la nuit. Adapt. : signe du signal de l'actif. Day/night sans condition = O/C et C/O de [7] | Taille, B/M, accruals, émissions, croissance d'actifs, rentabilité |
| [20] | Fattinger-Ziegler (13 futures 2010–2013) | Long pendant chacune des 8 périodes CET (P1 00–01 … P8 22–24). Jours où les US sont en heure d'été et pas l'Europe supprimés, comme dans le papier | — (le papier ne propose aucune stratégie, seulement la décomposition) |
| [21] | Wei (or et argent spot 2024–2026) | Sessions UTC chaînées Asie 00–08, Europe 08–14:30, US 14:30–24 ; long passif par session ; momentum signe(session t) → session t+1 : toutes sessions et chaque session seule, long-short et long-only | — |

Papiers de la récolte non fournis, donc non testés : [5] Lou-Polk-Skouras, [12] Scheduled Coordination Density, [16] Economic Value of Conditioning.

Doublons de définition : DIFF [2] = NMD 9:30/16:00 [3] = alpha [7] ; nuit sans filtre [15] = C/O [7] (même clôture 16:00 et ouverture 9:30). Ils apparaissent dans chaque papier avec des chiffres identiques.

## Ce que disent les chiffres

- **927 tests avec IC** (règle × actif). IC net par trade > 0 : 56 ; < 0 : 332. Le coût (1 tick + commission) fait passer 128 IC bruts positifs à 56 nets.
- **La seule régularité large est la nuit longue sur les indices et l'or** (C/O de [7] = [15] ≈ [14] ≈ CTO de [1]) : net par nuit NQ +4.4 bp [+1.6 ; +7.1], ES +2.5 [+0.3 ; +4.7], YM +2.6 [+0.4 ; +4.8], GC +4.2 [+1.5 ; +7.0] ; Sharpe net 0.63 à 0.88, borne basse de l'IC entre +0.05 et +0.32. Sur le forex, c'est négatif net (6E, 6B, 6J ▼).
- **Le drift de 2:00–3:00 ET ([1])** : IC brut > 0 sur NQ (+0.9 bp [+0.2 ; +1.7]) et ES (+0.7 [+0.1 ; +1.3]), plus rien après coût (ES net −0.3 [−0.9 ; +0.3]). C'est ce que trouve le papier (Sharpe −0.54 après coûts). Négatif sur les quatre devises.
- **Long nuit / short jour** (DIFF, NMD, alpha) : nul sur les indices ; IC net tout juste > 0 sur GC (+1.7 bp [+0.0 ; +3.5]) ; négatif sur le forex. Décaler l'ouverture ou la clôture ([3]) ne fait apparaître aucun IC net > 0.
- **Extrapolation de Jones et al. ([4])** : la jambe asymétrique « nuit long si r(9:45→15:00) > 0 » a un IC net > 0 sur NQ, ES, YM et GC (+3.3 à +5.4 bp). Mais elle est longue la nuit environ un jour sur deux, donc elle hérite de la prime de nuit ci-dessus. La version long-short n'a d'IC net > 0 sur aucun actif.
- **Sauts de nuit ([10])** : de 5 à une trentaine de trades par règle et par actif en 10 ans avec α = 1 % ou 5 %, trop peu pour un IC. Les moyennes sont dans ic.csv, sans IC.
- **Sessions de Wei ([21])** : sur GC, momentum long-only toutes sessions +2.1 bp net [+0.5 ; +3.7], Sharpe 0.69 [+0.13 ; +1.24]. La dominance asiatique du papier (2024–2026) ne se retrouve pas sur GC 2016–2026 : session Asie −0.1 bp net [−1.8 ; +1.7]. La session US de GC est même positive en brut.
- **Portefeuille bêta de [6]** : la jambe nuit est positive en brut (+6.3 bp/jour [+0.5 ; +12.0]) et la jambe jour négative (−6.1 [−11.5 ; −0.5]), même signe que le papier ; le combiné est nul en brut et négatif net.
- **Volatilité ([17], [18])** : corr(log RV nuit, log RV jour) de 0.67 à 0.82, IC loin de 0 sur tous les actifs, comme le papier (0.76). La part de variance de nuit est de 32 % sur les indices (papier : 40–45 % sur SPY/QQQ, avec une nuit plus longue) et de 59 à 69 % sur GC et le forex. Effet de levier corr(r_{t−1}, RV_t) < 0 avec IC sur NQ, ES et 6A ; nul sur YM, GC, 6E et 6B ; positif sur 6J.
- **Multiplicité** : avec ~930 tests, environ 23 IC nets > 0 sont attendus au hasard (2.5 % d'un côté), avant même de compter les doublons et les variantes très corrélées (règles de nuit). Les 56 observés se concentrent presque tous sur la prime de nuit des indices et de l'or, déjà connue dans ce dépôt. Aucun de ces résultats n'a été pré-enregistré, et le compteur d'essais n'a pas été mis à jour.

## Limites

- Les papiers sur actions s'appuient sur la coupe transversale ; leur traduction en série temporelle sur un seul future teste la règle, pas le résultat du papier.
- Prix = clôture de la barre 1 minute qui finit à l'instant T, sans bid/ask. Le coût net (1 tick + 5 $) suppose de traverser le spread une fois par aller-retour.
- Les règles dont les trades se touchent (CTC, [21] toutes sessions) paient un aller-retour par trade. C'est conservateur par rapport à une position tenue en continu.
- Fenêtres qui démarrent à la réouverture CME (18:00 ET = 00:00 CET) : le prix d'entrée est la clôture de 16:59 ET, donc l'écart de réouverture tombe dans cette fenêtre. L'heure 17:00→18:00 ET (maintenance) n'a pas de cotation : rendement brut nul, net négatif.

## Tables complètes
Tests avec IC calculable : 927 (règle × actif). IC net par trade > 0 : 56 ; < 0 : 332. IC brut > 0 : 128 ; < 0 : 42.

| Papier | Tests | Brut IC > 0 | Brut IC < 0 | Net IC > 0 | Net IC < 0 | Sharpe net IC > 0 |
|---|---|---|---|---|---|---|
| [1] Boyarchenko-Larsen-Whelan | 264 | 32 | 16 | 7 | 154 | 8 |
| [2] Berkman-Koch-Tuttle-Zhang | 48 | 3 | 1 | 1 | 8 | 1 |
| [3] Lu-Qin | 64 | 10 | 3 | 0 | 28 | 1 |
| [4] Jones-Pyun-Wang | 32 | 5 | 1 | 4 | 11 | 4 |
| [7] Tompkins-Wiener | 39 | 7 | 3 | 7 | 13 | 7 |
| [8] Abdi | 32 | 4 | 1 | 3 | 10 | 3 |
| [9] Branch-Ma | 16 | 0 | 0 | 0 | 3 | 0 |
| [10] Bahcivan-Dam-Gonenc | 110 | 0 | 1 | 0 | 1 | 1 |
| [11] Bahcivan | 96 | 9 | 0 | 1 | 14 | 3 |
| [14] Donninger | 24 | 12 | 0 | 10 | 7 | 11 |
| [15] Vojtko-Hanicová | 40 | 13 | 1 | 11 | 7 | 12 |
| [19] Aretz-Bartram | 112 | 13 | 3 | 8 | 13 | 11 |
| [20] Fattinger-Ziegler | 64 | 9 | 6 | 0 | 29 | 1 |
| [21] Wei | 88 | 10 | 5 | 4 | 33 | 7 |
| [6] Hendershott-Livdan-Rösch | 3 | 1 | 1 | 0 | 1 | 0 |


### [1] Boyarchenko-Larsen-Whelan

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| CTC 16:15→16:15 | NQ | 2634 | +6.9 [+1.6 ; +11.4] | +6.4 [+1.1 ; +10.9] | +0.73 [+0.17 ; +1.31] | ▲ |
| CTC 16:15→16:15 | ES | 2634 | +5.1 [+1.1 ; +8.7] | +4.1 [+0.1 ; +7.7] | +0.58 [+0.03 ; +1.20] | ▲ |
| CTC 16:15→16:15 | YM | 2630 | +4.8 [+1.1 ; +8.4] | +4.1 [+0.4 ; +7.7] | +0.60 [+0.03 ; +1.23] | ▲ |
| CTC 16:15→16:15 | GC | 2642 | +4.8 [+1.0 ; +8.4] | +4.0 [+0.1 ; +7.6] | +0.60 [+0.04 ; +1.18] | ▲ |
| CTC 16:15→16:15 | 6E | 2644 | -0.4 [-2.0 ; +1.2] | -1.2 [-2.8 ; +0.4] | -0.42 [-1.00 ; +0.14] |  |
| CTC 16:15→16:15 | 6B | 2644 | -0.3 [-2.4 ; +1.8] | -1.7 [-3.8 ; +0.4] | -0.45 [-1.01 ; +0.13] |  |
| CTC 16:15→16:15 | 6J | 2644 | -2.2 [-4.2 ; +0.1] | -3.3 [-5.4 ; -1.0] | -0.89 [-1.48 ; -0.28] | ▼ |
| CTC 16:15→16:15 | 6A | 2644 | +0.2 [-2.1 ; +2.6] | -1.2 [-3.5 ; +1.2] | -0.30 [-0.90 ; +0.27] |  |
| CTO 16:15→9:30 | NQ | 2655 | +3.4 [+0.5 ; +6.1] | +2.9 [-0.0 ; +5.6] | +0.57 [+0.02 ; +1.16] |  |
| CTO 16:15→9:30 | ES | 2655 | +2.7 [+0.3 ; +4.9] | +1.7 [-0.7 ; +3.9] | +0.40 [-0.17 ; +1.01] |  |
| CTO 16:15→9:30 | YM | 2653 | +2.3 [+0.1 ; +4.6] | +1.7 [-0.6 ; +3.9] | +0.40 [-0.18 ; +1.00] |  |
| CTO 16:15→9:30 | GC | 2659 | +4.9 [+2.0 ; +7.7] | +4.0 [+1.2 ; +6.8] | +0.79 [+0.26 ; +1.32] | ▲ |
| CTO 16:15→9:30 | 6E | 2660 | -0.7 [-2.0 ; +0.6] | -1.5 [-2.8 ; -0.2] | -0.63 [-1.22 ; -0.04] | ▼ |
| CTO 16:15→9:30 | 6B | 2660 | -1.4 [-3.1 ; +0.3] | -2.8 [-4.5 ; -1.1] | -0.92 [-1.43 ; -0.38] | ▼ |
| CTO 16:15→9:30 | 6J | 2660 | -1.0 [-2.9 ; +0.9] | -2.1 [-4.0 ; -0.2] | -0.68 [-1.29 ; -0.05] | ▼ |
| CTO 16:15→9:30 | 6A | 2660 | -0.1 [-1.8 ; +1.7] | -1.5 [-3.3 ; +0.3] | -0.46 [-1.00 ; +0.08] |  |
| CTO 16:15→8:30 | NQ | 2654 | +3.8 [+1.1 ; +6.4] | +3.3 [+0.6 ; +5.9] | +0.71 [+0.18 ; +1.30] | ▲ |
| CTO 16:15→8:30 | ES | 2654 | +2.4 [+0.1 ; +4.6] | +1.4 [-0.9 ; +3.6] | +0.35 [-0.19 ; +0.96] |  |
| CTO 16:15→8:30 | YM | 2652 | +2.0 [-0.2 ; +4.2] | +1.3 [-0.9 ; +3.5] | +0.35 [-0.20 ; +0.97] |  |
| CTO 16:15→8:30 | GC | 2658 | +4.6 [+2.1 ; +7.1] | +3.7 [+1.2 ; +6.2] | +0.82 [+0.26 ; +1.37] | ▲ |
| CTO 16:15→8:30 | 6E | 2659 | -0.7 [-1.9 ; +0.5] | -1.5 [-2.7 ; -0.3] | -0.75 [-1.36 ; -0.12] | ▼ |
| CTO 16:15→8:30 | 6B | 2659 | -1.0 [-2.5 ; +0.5] | -2.4 [-3.9 ; -0.9] | -0.86 [-1.40 ; -0.31] | ▼ |
| CTO 16:15→8:30 | 6J | 2659 | -0.9 [-2.5 ; +0.9] | -2.0 [-3.6 ; -0.2] | -0.73 [-1.33 ; -0.10] | ▼ |
| CTO 16:15→8:30 | 6A | 2659 | -0.2 [-1.8 ; +1.3] | -1.6 [-3.2 ; -0.1] | -0.56 [-1.08 ; -0.04] | ▼ |
| OTC 9:30→16:15 | NQ | 2656 | +3.9 [-0.2 ; +7.8] | +3.3 [-0.7 ; +7.3] | +0.47 [-0.04 ; +1.00] |  |
| OTC 9:30→16:15 | ES | 2656 | +2.5 [-0.5 ; +5.6] | +1.5 [-1.5 ; +4.6] | +0.28 [-0.23 ; +0.83] |  |
| OTC 9:30→16:15 | YM | 2654 | +2.4 [-0.5 ; +5.3] | +1.7 [-1.2 ; +4.6] | +0.32 [-0.20 ; +0.84] |  |
| OTC 9:30→16:15 | GC | 2660 | -0.2 [-2.5 ; +2.1] | -1.1 [-3.4 ; +1.2] | -0.27 [-0.79 ; +0.28] |  |
| OTC 9:30→16:15 | 6E | 2661 | +0.3 [-0.7 ; +1.3] | -0.5 [-1.5 ; +0.5] | -0.29 [-0.87 ; +0.28] |  |
| OTC 9:30→16:15 | 6B | 2661 | +1.1 [-0.1 ; +2.3] | -0.3 [-1.5 ; +0.9] | -0.12 [-0.73 ; +0.46] |  |
| OTC 9:30→16:15 | 6J | 2661 | -1.1 [-2.3 ; +0.1] | -2.2 [-3.4 ; -1.1] | -1.12 [-1.75 ; -0.51] | ▼ |
| OTC 9:30→16:15 | 6A | 2661 | +0.3 [-1.1 ; +1.6] | -1.2 [-2.5 ; +0.1] | -0.49 [-1.06 ; +0.08] |  |
| -OR short 8:30→10:00 | NQ | 2676 | -0.6 [-2.5 ; +1.3] | -1.1 [-3.0 ; +0.8] | -0.33 [-0.88 ; +0.23] |  |
| -OR short 8:30→10:00 | ES | 2676 | -0.8 [-2.5 ; +0.7] | -1.9 [-3.5 ; -0.3] | -0.72 [-1.34 ; -0.12] | ▼ |
| -OR short 8:30→10:00 | YM | 2676 | -1.0 [-2.7 ; +0.6] | -1.7 [-3.4 ; -0.1] | -0.64 [-1.31 ; +0.00] | ▼ |
| -OR short 8:30→10:00 | GC | 2676 | +0.5 [-1.0 ; +2.1] | -0.3 [-1.9 ; +1.3] | -0.12 [-0.71 ; +0.48] |  |
| -OR short 8:30→10:00 | 6E | 2676 | -0.2 [-0.9 ; +0.6] | -1.0 [-1.7 ; -0.2] | -0.74 [-1.26 ; -0.12] | ▼ |
| -OR short 8:30→10:00 | 6B | 2676 | +0.1 [-0.7 ; +0.8] | -1.3 [-2.1 ; -0.5] | -0.95 [-1.47 ; -0.40] | ▼ |
| -OR short 8:30→10:00 | 6J | 2676 | -0.0 [-0.9 ; +0.8] | -1.2 [-2.0 ; -0.3] | -0.79 [-1.35 ; -0.18] | ▼ |
| -OR short 8:30→10:00 | 6A | 2676 | -0.1 [-1.0 ; +0.8] | -1.5 [-2.4 ; -0.6] | -0.97 [-1.50 ; -0.40] | ▼ |
| OD 2:00→3:00 ET | NQ | 2676 | +0.9 [+0.2 ; +1.7] | +0.4 [-0.3 ; +1.1] | +0.36 [-0.25 ; +0.97] |  |
| OD 2:00→3:00 ET | ES | 2676 | +0.7 [+0.1 ; +1.3] | -0.3 [-0.9 ; +0.3] | -0.30 [-1.00 ; +0.33] |  |
| OD 2:00→3:00 ET | YM | 2675 | +0.5 [-0.1 ; +1.1] | -0.2 [-0.8 ; +0.4] | -0.22 [-0.91 ; +0.41] |  |
| OD 2:00→3:00 ET | GC | 2675 | +0.5 [-0.3 ; +1.3] | -0.3 [-1.2 ; +0.5] | -0.28 [-0.94 ; +0.31] |  |
| OD 2:00→3:00 ET | 6E | 2676 | -0.4 [-0.8 ; -0.1] | -1.2 [-1.6 ; -0.9] | -1.95 [-2.55 ; -1.37] | ▼ |
| OD 2:00→3:00 ET | 6B | 2676 | -0.7 [-1.1 ; -0.2] | -2.0 [-2.5 ; -1.6] | -2.58 [-3.18 ; -1.94] | ▼ |
| OD 2:00→3:00 ET | 6J | 2676 | -0.4 [-0.9 ; +0.1] | -1.6 [-2.0 ; -1.1] | -2.03 [-2.74 ; -1.39] | ▼ |
| OD 2:00→3:00 ET | 6A | 2676 | -0.3 [-0.9 ; +0.2] | -1.8 [-2.3 ; -1.2] | -1.92 [-2.66 ; -1.21] | ▼ |
| OD+ 1:30→3:30 ET | NQ | 2676 | +1.6 [+0.4 ; +2.8] | +1.0 [-0.2 ; +2.3] | +0.56 [-0.08 ; +1.14] |  |
| OD+ 1:30→3:30 ET | ES | 2676 | +1.3 [+0.2 ; +2.4] | +0.3 [-0.8 ; +1.5] | +0.17 [-0.53 ; +0.81] |  |
| OD+ 1:30→3:30 ET | YM | 2675 | +1.0 [-0.0 ; +2.2] | +0.3 [-0.7 ; +1.5] | +0.18 [-0.51 ; +0.81] |  |
| OD+ 1:30→3:30 ET | GC | 2675 | +0.6 [-0.6 ; +1.7] | -0.2 [-1.4 ; +0.9] | -0.12 [-0.68 ; +0.49] |  |
| OD+ 1:30→3:30 ET | 6E | 2676 | +0.1 [-0.5 ; +0.6] | -0.7 [-1.3 ; -0.2] | -0.81 [-1.42 ; -0.20] | ▼ |
| OD+ 1:30→3:30 ET | 6B | 2676 | -0.4 [-1.0 ; +0.3] | -1.8 [-2.4 ; -1.0] | -1.52 [-2.17 ; -0.85] | ▼ |
| OD+ 1:30→3:30 ET | 6J | 2676 | -0.3 [-0.9 ; +0.4] | -1.4 [-2.0 ; -0.8] | -1.29 [-1.91 ; -0.65] | ▼ |
| OD+ 1:30→3:30 ET | 6A | 2676 | +0.1 [-0.6 ; +0.8] | -1.3 [-2.0 ; -0.6] | -1.03 [-1.63 ; -0.43] | ▼ |
| OD ouverture Europe 7:00→8:00 Londres | NQ | 2676 | +0.9 [+0.1 ; +1.6] | +0.4 [-0.4 ; +1.1] | +0.30 [-0.29 ; +0.88] |  |
| OD ouverture Europe 7:00→8:00 Londres | ES | 2676 | +0.6 [-0.0 ; +1.2] | -0.4 [-1.0 ; +0.2] | -0.41 [-1.03 ; +0.17] |  |
| OD ouverture Europe 7:00→8:00 Londres | YM | 2675 | +0.4 [-0.2 ; +1.0] | -0.3 [-0.9 ; +0.4] | -0.32 [-0.95 ; +0.27] |  |
| OD ouverture Europe 7:00→8:00 Londres | GC | 2675 | +0.3 [-0.4 ; +1.1] | -0.5 [-1.3 ; +0.2] | -0.45 [-1.08 ; +0.16] |  |
| OD ouverture Europe 7:00→8:00 Londres | 6E | 2676 | -0.6 [-1.0 ; -0.2] | -1.4 [-1.8 ; -1.0] | -2.11 [-2.71 ; -1.55] | ▼ |
| OD ouverture Europe 7:00→8:00 Londres | 6B | 2676 | -0.9 [-1.4 ; -0.4] | -2.2 [-2.7 ; -1.8] | -2.71 [-3.29 ; -2.12] | ▼ |
| OD ouverture Europe 7:00→8:00 Londres | 6J | 2676 | -0.6 [-1.1 ; -0.1] | -1.7 [-2.2 ; -1.2] | -2.21 [-2.95 ; -1.54] | ▼ |
| OD ouverture Europe 7:00→8:00 Londres | 6A | 2676 | -0.6 [-1.2 ; -0.1] | -2.1 [-2.6 ; -1.5] | -2.38 [-2.93 ; -1.84] | ▼ |
| short 9:00→10:00 ET | NQ | 2677 | -0.5 [-2.4 ; +1.3] | -1.0 [-2.9 ; +0.8] | -0.35 [-0.93 ; +0.19] |  |
| short 9:00→10:00 ET | ES | 2677 | -0.5 [-1.9 ; +0.8] | -1.6 [-2.9 ; -0.2] | -0.75 [-1.46 ; -0.07] | ▼ |
| short 9:00→10:00 ET | YM | 2677 | -0.7 [-2.1 ; +0.9] | -1.4 [-2.8 ; +0.2] | -0.62 [-1.38 ; +0.13] |  |
| short 9:00→10:00 ET | GC | 2677 | +0.9 [-0.4 ; +2.2] | +0.1 [-1.2 ; +1.3] | +0.03 [-0.57 ; +0.61] |  |
| short 9:00→10:00 ET | 6E | 2677 | -0.1 [-0.6 ; +0.4] | -0.9 [-1.4 ; -0.4] | -1.04 [-1.61 ; -0.42] | ▼ |
| short 9:00→10:00 ET | 6B | 2677 | -0.1 [-0.7 ; +0.5] | -1.5 [-2.1 ; -0.9] | -1.50 [-2.07 ; -0.92] | ▼ |
| short 9:00→10:00 ET | 6J | 2677 | -0.2 [-0.8 ; +0.4] | -1.3 [-1.9 ; -0.7] | -1.30 [-1.88 ; -0.68] | ▼ |
| short 9:00→10:00 ET | 6A | 2677 | -0.0 [-0.7 ; +0.6] | -1.5 [-2.1 ; -0.8] | -1.35 [-1.92 ; -0.77] | ▼ |
| short 9:00→10:00 ET jeu+ven | NQ | 1078 | +0.7 [-2.2 ; +3.6] | +0.2 [-2.7 ; +3.1] | +0.05 [-0.49 ; +0.56] |  |
| short 9:00→10:00 ET jeu+ven | ES | 1078 | -0.4 [-2.3 ; +1.5] | -1.4 [-3.3 ; +0.5] | -0.43 [-0.98 ; +0.11] |  |
| short 9:00→10:00 ET jeu+ven | YM | 1078 | -0.9 [-2.8 ; +1.1] | -1.6 [-3.5 ; +0.4] | -0.47 [-1.06 ; +0.12] |  |
| short 9:00→10:00 ET jeu+ven | GC | 1078 | +1.6 [-0.5 ; +3.4] | +0.7 [-1.3 ; +2.6] | +0.20 [-0.37 ; +0.77] |  |
| short 9:00→10:00 ET jeu+ven | 6E | 1078 | +0.3 [-0.6 ; +1.3] | -0.5 [-1.4 ; +0.5] | -0.30 [-0.87 ; +0.32] |  |
| short 9:00→10:00 ET jeu+ven | 6B | 1078 | +0.4 [-0.6 ; +1.4] | -1.0 [-2.0 ; +0.0] | -0.60 [-1.18 ; +0.00] |  |
| short 9:00→10:00 ET jeu+ven | 6J | 1078 | -0.3 [-1.3 ; +0.6] | -1.5 [-2.4 ; -0.5] | -0.84 [-1.37 ; -0.25] | ▼ |
| short 9:00→10:00 ET jeu+ven | 6A | 1078 | +0.8 [-0.2 ; +1.8] | -0.6 [-1.7 ; +0.4] | -0.34 [-0.90 ; +0.26] |  |
| heure 18:00→19:00 ET | NQ | 2096 | -0.2 [-1.1 ; +0.9] | -0.7 [-1.7 ; +0.3] | -0.45 [-1.07 ; +0.14] |  |
| heure 18:00→19:00 ET | ES | 2096 | -0.0 [-0.9 ; +0.9] | -1.1 [-1.9 ; -0.1] | -0.81 [-1.53 ; -0.22] | ▼ |
| heure 18:00→19:00 ET | YM | 2094 | -0.1 [-1.0 ; +0.9] | -0.8 [-1.7 ; +0.3] | -0.62 [-1.33 ; -0.04] |  |
| heure 18:00→19:00 ET | GC | 2088 | +1.5 [+0.8 ; +2.2] | +0.6 [-0.1 ; +1.4] | +0.52 [-0.10 ; +1.07] |  |
| heure 18:00→19:00 ET | 6E | 2128 | +0.3 [+0.0 ; +0.5] | -0.5 [-0.8 ; -0.3] | -1.23 [-1.88 ; -0.57] | ▼ |
| heure 18:00→19:00 ET | 6B | 2128 | +0.0 [-0.3 ; +0.4] | -1.3 [-1.7 ; -0.9] | -1.93 [-2.94 ; -1.18] | ▼ |
| heure 18:00→19:00 ET | 6J | 2128 | +0.3 [-0.1 ; +0.8] | -0.8 [-1.3 ; -0.3] | -1.14 [-1.80 ; -0.45] | ▼ |
| heure 18:00→19:00 ET | 6A | 2128 | -0.0 [-0.5 ; +0.4] | -1.5 [-1.9 ; -1.0] | -2.00 [-2.63 ; -1.39] | ▼ |
| heure 19:00→20:00 ET | NQ | 2676 | +0.4 [-0.2 ; +1.0] | -0.1 [-0.7 ; +0.5] | -0.04 [-0.57 ; +0.54] |  |
| heure 19:00→20:00 ET | ES | 2676 | +0.1 [-0.4 ; +0.6] | -0.9 [-1.4 ; -0.4] | -0.91 [-1.42 ; -0.38] | ▼ |
| heure 19:00→20:00 ET | YM | 2675 | +0.2 [-0.2 ; +0.7] | -0.5 [-0.9 ; -0.0] | -0.59 [-1.08 ; -0.08] | ▼ |
| heure 19:00→20:00 ET | GC | 2672 | +0.8 [+0.3 ; +1.4] | -0.1 [-0.6 ; +0.5] | +0.20 [-0.47 ; +0.80] |  |
| heure 19:00→20:00 ET | 6E | 2676 | -0.1 [-0.4 ; +0.1] | -0.9 [-1.2 ; -0.7] | -2.11 [-2.68 ; -1.53] | ▼ |
| heure 19:00→20:00 ET | 6B | 2674 | -0.1 [-0.5 ; +0.2] | -1.5 [-1.8 ; -1.2] | -2.45 [-3.38 ; -1.89] | ▼ |
| heure 19:00→20:00 ET | 6J | 2676 | +0.3 [-0.1 ; +0.8] | -0.8 [-1.3 ; -0.4] | -1.11 [-1.78 ; -0.43] | ▼ |
| heure 19:00→20:00 ET | 6A | 2676 | -0.7 [-1.2 ; -0.2] | -2.1 [-2.6 ; -1.6] | -2.70 [-3.40 ; -2.00] | ▼ |
| heure 20:00→21:00 ET | NQ | 2675 | +0.4 [-0.3 ; +1.1] | -0.1 [-0.8 ; +0.6] | -0.03 [-0.56 ; +0.49] |  |
| heure 20:00→21:00 ET | ES | 2675 | +0.0 [-0.5 ; +0.6] | -1.0 [-1.5 ; -0.4] | -0.78 [-1.27 ; -0.27] | ▼ |
| heure 20:00→21:00 ET | YM | 2674 | -0.1 [-0.6 ; +0.5] | -0.7 [-1.3 ; -0.2] | -0.60 [-1.08 ; -0.10] | ▼ |
| heure 20:00→21:00 ET | GC | 2671 | +0.4 [-0.3 ; +1.1] | -0.4 [-1.1 ; +0.2] | -0.27 [-0.84 ; +0.28] |  |
| heure 20:00→21:00 ET | 6E | 2675 | -0.0 [-0.3 ; +0.3] | -0.8 [-1.1 ; -0.5] | -1.38 [-1.97 ; -0.77] | ▼ |
| heure 20:00→21:00 ET | 6B | 2673 | -0.1 [-0.6 ; +0.3] | -1.5 [-2.0 ; -1.1] | -2.75 [-3.34 ; -2.13] | ▼ |
| heure 20:00→21:00 ET | 6J | 2675 | +0.3 [-0.2 ; +0.8] | -0.8 [-1.3 ; -0.3] | -1.20 [-1.82 ; -0.57] | ▼ |
| heure 20:00→21:00 ET | 6A | 2675 | +0.1 [-0.4 ; +0.6] | -1.3 [-1.8 ; -0.8] | -1.47 [-2.00 ; -0.92] | ▼ |
| heure 21:00→22:00 ET | NQ | 2676 | +0.1 [-0.6 ; +0.9] | -0.4 [-1.1 ; +0.4] | -0.34 [-0.91 ; +0.29] |  |
| heure 21:00→22:00 ET | ES | 2676 | +0.1 [-0.5 ; +0.7] | -0.9 [-1.5 ; -0.3] | -0.76 [-1.29 ; -0.22] | ▼ |
| heure 21:00→22:00 ET | YM | 2675 | +0.1 [-0.5 ; +0.6] | -0.6 [-1.2 ; -0.1] | -0.58 [-1.08 ; -0.00] | ▼ |
| heure 21:00→22:00 ET | GC | 2675 | +0.1 [-0.9 ; +1.0] | -0.8 [-1.8 ; +0.1] | -0.63 [-1.14 ; -0.04] |  |
| heure 21:00→22:00 ET | 6E | 2676 | +0.2 [-0.1 ; +0.5] | -0.6 [-0.9 ; -0.3] | -1.36 [-2.07 ; -0.71] | ▼ |
| heure 21:00→22:00 ET | 6B | 2676 | +0.1 [-0.2 ; +0.4] | -1.3 [-1.6 ; -1.0] | -2.42 [-3.11 ; -1.82] | ▼ |
| heure 21:00→22:00 ET | 6J | 2676 | +0.0 [-0.5 ; +0.5] | -1.1 [-1.6 ; -0.6] | -1.30 [-1.93 ; -0.67] | ▼ |
| heure 21:00→22:00 ET | 6A | 2676 | +0.2 [-0.3 ; +0.8] | -1.2 [-1.8 ; -0.6] | -1.10 [-1.66 ; -0.55] | ▼ |
| heure 22:00→23:00 ET | NQ | 2675 | -0.2 [-0.9 ; +0.5] | -0.7 [-1.4 ; -0.1] | -0.83 [-1.35 ; -0.32] | ▼ |
| heure 22:00→23:00 ET | ES | 2675 | -0.2 [-0.8 ; +0.4] | -1.2 [-1.8 ; -0.6] | -1.26 [-1.80 ; -0.83] | ▼ |
| heure 22:00→23:00 ET | YM | 2674 | -0.2 [-0.8 ; +0.3] | -0.9 [-1.5 ; -0.4] | -1.00 [-1.51 ; -0.57] | ▼ |
| heure 22:00→23:00 ET | GC | 2675 | -0.2 [-0.8 ; +0.4] | -1.1 [-1.6 ; -0.5] | -0.85 [-1.46 ; -0.22] | ▼ |
| heure 22:00→23:00 ET | 6E | 2676 | +0.2 [-0.1 ; +0.5] | -0.6 [-0.9 ; -0.3] | -1.02 [-1.73 ; -0.45] | ▼ |
| heure 22:00→23:00 ET | 6B | 2676 | -0.1 [-0.6 ; +0.3] | -1.5 [-2.0 ; -1.1] | -1.50 [-3.39 ; -1.14] | ▼ |
| heure 22:00→23:00 ET | 6J | 2676 | +0.2 [-0.2 ; +0.8] | -0.9 [-1.3 ; -0.4] | -0.73 [-1.75 ; -0.00] | ▼ |
| heure 22:00→23:00 ET | 6A | 2676 | +0.5 [+0.0 ; +1.0] | -0.9 [-1.4 ; -0.4] | -0.95 [-1.53 ; -0.38] | ▼ |
| heure 23:00→00:00 ET | NQ | 2676 | +0.2 [-0.3 ; +0.7] | -0.3 [-0.8 ; +0.2] | -0.29 [-0.88 ; +0.33] |  |
| heure 23:00→00:00 ET | ES | 2676 | +0.2 [-0.3 ; +0.6] | -0.8 [-1.3 ; -0.4] | -1.06 [-1.62 ; -0.48] | ▼ |
| heure 23:00→00:00 ET | YM | 2675 | +0.2 [-0.2 ; +0.5] | -0.5 [-0.9 ; -0.1] | -0.71 [-1.26 ; -0.15] | ▼ |
| heure 23:00→00:00 ET | GC | 2675 | -0.0 [-0.5 ; +0.5] | -0.9 [-1.4 ; -0.3] | -0.93 [-1.63 ; -0.31] | ▼ |
| heure 23:00→00:00 ET | 6E | 2676 | -0.0 [-0.2 ; +0.2] | -0.8 [-1.0 ; -0.7] | -2.40 [-3.03 ; -1.80] | ▼ |
| heure 23:00→00:00 ET | 6B | 2676 | -0.1 [-0.3 ; +0.1] | -1.5 [-1.7 ; -1.3] | -3.83 [-4.54 ; -3.22] | ▼ |
| heure 23:00→00:00 ET | 6J | 2676 | +0.1 [-0.2 ; +0.5] | -1.0 [-1.4 ; -0.6] | -1.44 [-2.25 ; -0.71] | ▼ |
| heure 23:00→00:00 ET | 6A | 2676 | -0.1 [-0.5 ; +0.2] | -1.6 [-1.9 ; -1.2] | -2.29 [-2.88 ; -1.72] | ▼ |
| heure 00:00→01:00 ET | NQ | 2676 | +0.5 [-0.1 ; +1.2] | +0.0 [-0.6 ; +0.7] | +0.00 [-0.74 ; +0.58] |  |
| heure 00:00→01:00 ET | ES | 2676 | +0.5 [-0.1 ; +1.2] | -0.5 [-1.1 ; +0.1] | -0.59 [-1.72 ; +0.20] |  |
| heure 00:00→01:00 ET | YM | 2675 | +0.5 [-0.1 ; +1.2] | -0.2 [-0.8 ; +0.5] | -0.20 [-1.26 ; +0.52] |  |
| heure 00:00→01:00 ET | GC | 2675 | +0.0 [-0.5 ; +0.5] | -0.9 [-1.3 ; -0.4] | -0.96 [-1.59 ; -0.44] | ▼ |
| heure 00:00→01:00 ET | 6E | 2676 | -0.1 [-0.2 ; +0.1] | -0.9 [-1.1 ; -0.7] | -2.80 [-3.51 ; -2.08] | ▼ |
| heure 00:00→01:00 ET | 6B | 2676 | -0.0 [-0.3 ; +0.2] | -1.4 [-1.7 ; -1.2] | -3.81 [-4.48 ; -3.15] | ▼ |
| heure 00:00→01:00 ET | 6J | 2676 | -0.2 [-0.6 ; +0.2] | -1.3 [-1.7 ; -0.9] | -2.05 [-2.92 ; -1.33] | ▼ |
| heure 00:00→01:00 ET | 6A | 2676 | +0.0 [-0.4 ; +0.4] | -1.4 [-1.8 ; -1.0] | -2.02 [-2.61 ; -1.45] | ▼ |
| heure 01:00→02:00 ET | NQ | 2676 | +0.5 [-0.1 ; +1.0] | -0.1 [-0.6 ; +0.5] | -0.07 [-0.67 ; +0.49] |  |
| heure 01:00→02:00 ET | ES | 2676 | +0.3 [-0.1 ; +0.8] | -0.7 [-1.1 ; -0.2] | -0.91 [-1.59 ; -0.32] | ▼ |
| heure 01:00→02:00 ET | YM | 2675 | +0.2 [-0.2 ; +0.6] | -0.5 [-0.9 ; -0.1] | -0.66 [-1.30 ; -0.07] | ▼ |
| heure 01:00→02:00 ET | GC | 2675 | -0.4 [-1.1 ; +0.3] | -1.3 [-2.0 ; -0.6] | -1.15 [-1.66 ; -0.59] | ▼ |
| heure 01:00→02:00 ET | 6E | 2676 | -0.1 [-0.3 ; +0.1] | -0.9 [-1.1 ; -0.7] | -2.23 [-2.92 ; -1.56] | ▼ |
| heure 01:00→02:00 ET | 6B | 2676 | +0.0 [-0.3 ; +0.4] | -1.4 [-1.7 ; -1.0] | -2.43 [-3.64 ; -1.44] | ▼ |
| heure 01:00→02:00 ET | 6J | 2676 | -0.3 [-0.6 ; +0.1] | -1.4 [-1.7 ; -1.0] | -2.39 [-3.01 ; -1.76] | ▼ |
| heure 01:00→02:00 ET | 6A | 2676 | +0.5 [+0.1 ; +1.0] | -0.9 [-1.3 ; -0.4] | -1.30 [-1.96 ; -0.63] | ▼ |
| heure 02:00→03:00 ET | NQ | 2676 | +0.9 [+0.2 ; +1.7] | +0.4 [-0.3 ; +1.1] | +0.36 [-0.25 ; +0.97] |  |
| heure 02:00→03:00 ET | ES | 2676 | +0.7 [+0.1 ; +1.3] | -0.3 [-0.9 ; +0.3] | -0.30 [-1.00 ; +0.33] |  |
| heure 02:00→03:00 ET | YM | 2675 | +0.5 [-0.1 ; +1.1] | -0.2 [-0.8 ; +0.4] | -0.22 [-0.91 ; +0.41] |  |
| heure 02:00→03:00 ET | GC | 2675 | +0.5 [-0.3 ; +1.3] | -0.3 [-1.2 ; +0.5] | -0.28 [-0.94 ; +0.31] |  |
| heure 02:00→03:00 ET | 6E | 2676 | -0.4 [-0.8 ; -0.1] | -1.2 [-1.6 ; -0.9] | -1.95 [-2.55 ; -1.37] | ▼ |
| heure 02:00→03:00 ET | 6B | 2676 | -0.7 [-1.1 ; -0.2] | -2.0 [-2.5 ; -1.6] | -2.58 [-3.18 ; -1.94] | ▼ |
| heure 02:00→03:00 ET | 6J | 2676 | -0.4 [-0.9 ; +0.1] | -1.6 [-2.0 ; -1.1] | -2.03 [-2.74 ; -1.39] | ▼ |
| heure 02:00→03:00 ET | 6A | 2676 | -0.3 [-0.9 ; +0.2] | -1.8 [-2.3 ; -1.2] | -1.92 [-2.66 ; -1.21] | ▼ |
| heure 03:00→04:00 ET | NQ | 2676 | +0.3 [-0.5 ; +1.3] | -0.2 [-1.0 ; +0.8] | -0.11 [-0.71 ; +0.45] |  |
| heure 03:00→04:00 ET | ES | 2676 | +0.3 [-0.4 ; +1.1] | -0.7 [-1.4 ; +0.1] | -0.56 [-1.13 ; -0.01] |  |
| heure 03:00→04:00 ET | YM | 2675 | +0.2 [-0.5 ; +1.0] | -0.5 [-1.2 ; +0.3] | -0.37 [-0.92 ; +0.14] |  |
| heure 03:00→04:00 ET | GC | 2675 | +0.3 [-0.4 ; +1.0] | -0.6 [-1.3 ; +0.1] | -0.45 [-1.01 ; +0.11] |  |
| heure 03:00→04:00 ET | 6E | 2676 | +0.8 [+0.3 ; +1.3] | -0.0 [-0.5 ; +0.5] | -0.02 [-0.62 ; +0.57] |  |
| heure 03:00→04:00 ET | 6B | 2676 | -0.1 [-0.6 ; +0.5] | -1.4 [-2.0 ; -0.9] | -1.50 [-2.11 ; -0.91] | ▼ |
| heure 03:00→04:00 ET | 6J | 2676 | +0.2 [-0.2 ; +0.7] | -0.9 [-1.3 ; -0.4] | -1.08 [-1.68 ; -0.50] | ▼ |
| heure 03:00→04:00 ET | 6A | 2676 | +0.2 [-0.4 ; +0.8] | -1.2 [-1.8 ; -0.7] | -1.26 [-1.84 ; -0.68] | ▼ |
| heure 04:00→05:00 ET | NQ | 2676 | -0.1 [-0.8 ; +0.7] | -0.6 [-1.3 ; +0.1] | -0.43 [-0.97 ; +0.11] |  |
| heure 04:00→05:00 ET | ES | 2676 | +0.1 [-0.6 ; +0.7] | -0.9 [-1.6 ; -0.3] | -0.81 [-1.39 ; -0.28] | ▼ |
| heure 04:00→05:00 ET | YM | 2676 | -0.1 [-0.7 ; +0.5] | -0.8 [-1.4 ; -0.2] | -0.69 [-1.29 ; -0.13] | ▼ |
| heure 04:00→05:00 ET | GC | 2676 | +0.1 [-0.7 ; +0.8] | -0.8 [-1.6 ; -0.1] | -0.68 [-1.21 ; -0.15] | ▼ |
| heure 04:00→05:00 ET | 6E | 2676 | -0.4 [-0.8 ; -0.0] | -1.2 [-1.6 ; -0.8] | -1.78 [-2.35 ; -1.21] | ▼ |
| heure 04:00→05:00 ET | 6B | 2676 | +0.2 [-0.4 ; +0.8] | -1.2 [-1.8 ; -0.6] | -1.24 [-1.84 ; -0.66] | ▼ |
| heure 04:00→05:00 ET | 6J | 2676 | -0.0 [-0.5 ; +0.4] | -1.2 [-1.6 ; -0.7] | -1.51 [-2.25 ; -0.86] | ▼ |
| heure 04:00→05:00 ET | 6A | 2676 | -0.3 [-0.7 ; +0.2] | -1.7 [-2.2 ; -1.2] | -2.04 [-2.65 ; -1.45] | ▼ |
| heure 05:00→06:00 ET | NQ | 2676 | +0.5 [-0.2 ; +1.1] | -0.1 [-0.7 ; +0.6] | -0.05 [-0.64 ; +0.50] |  |
| heure 05:00→06:00 ET | ES | 2676 | +0.5 [-0.1 ; +1.0] | -0.5 [-1.1 ; +0.0] | -0.55 [-1.11 ; -0.00] |  |
| heure 05:00→06:00 ET | YM | 2676 | +0.6 [+0.0 ; +1.1] | -0.1 [-0.6 ; +0.4] | -0.12 [-0.66 ; +0.42] |  |
| heure 05:00→06:00 ET | GC | 2676 | +0.3 [-0.4 ; +0.9] | -0.6 [-1.2 ; +0.0] | -0.60 [-1.28 ; -0.00] |  |
| heure 05:00→06:00 ET | 6E | 2676 | -0.1 [-0.4 ; +0.2] | -0.9 [-1.2 ; -0.6] | -1.50 [-2.07 ; -0.96] | ▼ |
| heure 05:00→06:00 ET | 6B | 2676 | +0.1 [-0.3 ; +0.6] | -1.2 [-1.7 ; -0.8] | -1.56 [-2.14 ; -0.99] | ▼ |
| heure 05:00→06:00 ET | 6J | 2676 | -0.3 [-0.7 ; -0.0] | -1.5 [-1.8 ; -1.1] | -2.61 [-3.20 ; -2.05] | ▼ |
| heure 05:00→06:00 ET | 6A | 2676 | -0.2 [-0.6 ; +0.3] | -1.6 [-2.0 ; -1.2] | -2.25 [-2.80 ; -1.69] | ▼ |
| heure 06:00→07:00 ET | NQ | 2676 | +0.1 [-0.5 ; +0.7] | -0.4 [-1.1 ; +0.2] | -0.35 [-0.86 ; +0.17] |  |
| heure 06:00→07:00 ET | ES | 2676 | +0.4 [-0.2 ; +1.0] | -0.6 [-1.2 ; +0.0] | -0.54 [-1.14 ; +0.01] |  |
| heure 06:00→07:00 ET | YM | 2676 | +0.4 [-0.2 ; +1.0] | -0.3 [-0.9 ; +0.3] | -0.28 [-0.88 ; +0.29] |  |
| heure 06:00→07:00 ET | GC | 2676 | +0.0 [-0.7 ; +0.7] | -0.9 [-1.5 ; -0.2] | -0.73 [-1.27 ; -0.18] | ▼ |
| heure 06:00→07:00 ET | 6E | 2676 | -0.5 [-0.8 ; -0.1] | -1.3 [-1.6 ; -0.9] | -2.11 [-2.68 ; -1.51] | ▼ |
| heure 06:00→07:00 ET | 6B | 2676 | -0.4 [-0.8 ; +0.1] | -1.8 [-2.2 ; -1.3] | -2.08 [-2.72 ; -1.48] | ▼ |
| heure 06:00→07:00 ET | 6J | 2676 | -0.1 [-0.5 ; +0.2] | -1.3 [-1.6 ; -0.9] | -2.18 [-2.85 ; -1.52] | ▼ |
| heure 06:00→07:00 ET | 6A | 2676 | -0.3 [-0.8 ; +0.1] | -1.8 [-2.2 ; -1.3] | -2.59 [-3.16 ; -2.01] | ▼ |
| heure 07:00→08:00 ET | NQ | 2676 | +0.0 [-0.8 ; +0.8] | -0.5 [-1.3 ; +0.3] | -0.37 [-1.01 ; +0.29] |  |
| heure 07:00→08:00 ET | ES | 2676 | -0.1 [-0.9 ; +0.5] | -1.1 [-1.9 ; -0.5] | -0.99 [-1.61 ; -0.35] | ▼ |
| heure 07:00→08:00 ET | YM | 2676 | -0.0 [-0.7 ; +0.7] | -0.7 [-1.4 ; -0.0] | -0.64 [-1.24 ; +0.01] | ▼ |
| heure 07:00→08:00 ET | GC | 2676 | +0.1 [-0.7 ; +0.8] | -0.8 [-1.5 ; -0.0] | -0.65 [-1.26 ; -0.01] | ▼ |
| heure 07:00→08:00 ET | 6E | 2676 | -1.1 [-1.5 ; -0.7] | -1.9 [-2.3 ; -1.5] | -2.95 [-3.63 ; -2.31] | ▼ |
| heure 07:00→08:00 ET | 6B | 2676 | -0.4 [-1.0 ; +0.2] | -1.8 [-2.3 ; -1.2] | -1.97 [-2.56 ; -1.42] | ▼ |
| heure 07:00→08:00 ET | 6J | 2676 | -0.4 [-0.7 ; +0.0] | -1.5 [-1.9 ; -1.1] | -2.32 [-2.91 ; -1.71] | ▼ |
| heure 07:00→08:00 ET | 6A | 2676 | -0.1 [-0.5 ; +0.3] | -1.5 [-1.9 ; -1.1] | -2.07 [-2.67 ; -1.51] | ▼ |
| heure 08:00→09:00 ET | NQ | 2676 | +0.2 [-1.0 ; +1.5] | -0.3 [-1.5 ; +0.9] | -0.13 [-0.73 ; +0.40] |  |
| heure 08:00→09:00 ET | ES | 2676 | +0.4 [-0.7 ; +1.4] | -0.6 [-1.7 ; +0.4] | -0.36 [-0.99 ; +0.20] |  |
| heure 08:00→09:00 ET | YM | 2676 | +0.3 [-0.6 ; +1.2] | -0.4 [-1.3 ; +0.5] | -0.26 [-0.89 ; +0.31] |  |
| heure 08:00→09:00 ET | GC | 2676 | +0.5 [-0.7 ; +1.9] | -0.3 [-1.6 ; +1.0] | -0.15 [-0.72 ; +0.39] |  |
| heure 08:00→09:00 ET | 6E | 2676 | +0.9 [+0.3 ; +1.5] | +0.1 [-0.5 ; +0.7] | +0.09 [-0.45 ; +0.61] |  |
| heure 08:00→09:00 ET | 6B | 2676 | +0.3 [-0.3 ; +0.9] | -1.1 [-1.7 ; -0.4] | -0.98 [-1.55 ; -0.40] | ▼ |
| heure 08:00→09:00 ET | 6J | 2676 | +0.2 [-0.5 ; +0.9] | -0.9 [-1.6 ; -0.2] | -0.79 [-1.39 ; -0.20] | ▼ |
| heure 08:00→09:00 ET | 6A | 2676 | +0.3 [-0.4 ; +1.0] | -1.1 [-1.8 ; -0.4] | -0.89 [-1.43 ; -0.34] | ▼ |
| heure 09:00→10:00 ET | NQ | 2677 | +0.5 [-1.3 ; +2.4] | -0.0 [-1.8 ; +1.8] | -0.00 [-0.53 ; +0.56] |  |
| heure 09:00→10:00 ET | ES | 2677 | +0.5 [-0.8 ; +1.9] | -0.5 [-1.8 ; +0.8] | -0.22 [-0.83 ; +0.44] |  |
| heure 09:00→10:00 ET | YM | 2677 | +0.7 [-0.9 ; +2.1] | -0.0 [-1.6 ; +1.4] | -0.00 [-0.70 ; +0.70] |  |
| heure 09:00→10:00 ET | GC | 2677 | -0.9 [-2.2 ; +0.4] | -1.8 [-3.0 ; -0.5] | -0.86 [-1.44 ; -0.27] | ▼ |
| heure 09:00→10:00 ET | 6E | 2677 | +0.1 [-0.4 ; +0.6] | -0.7 [-1.2 ; -0.2] | -0.78 [-1.41 ; -0.22] | ▼ |
| heure 09:00→10:00 ET | 6B | 2677 | +0.1 [-0.5 ; +0.7] | -1.3 [-1.8 ; -0.7] | -1.27 [-1.86 ; -0.72] | ▼ |
| heure 09:00→10:00 ET | 6J | 2677 | +0.2 [-0.4 ; +0.8] | -1.0 [-1.5 ; -0.4] | -0.98 [-1.66 ; -0.37] | ▼ |
| heure 09:00→10:00 ET | 6A | 2677 | +0.0 [-0.6 ; +0.7] | -1.4 [-2.0 ; -0.8] | -1.27 [-1.90 ; -0.70] | ▼ |
| heure 10:00→11:00 ET | NQ | 2677 | -1.0 [-2.8 ; +0.7] | -1.5 [-3.3 ; +0.2] | -0.49 [-1.06 ; +0.08] |  |
| heure 10:00→11:00 ET | ES | 2677 | -0.4 [-1.8 ; +0.9] | -1.4 [-2.8 ; -0.1] | -0.63 [-1.19 ; -0.04] | ▼ |
| heure 10:00→11:00 ET | YM | 2676 | -0.5 [-1.9 ; +0.7] | -1.2 [-2.5 ; +0.0] | -0.54 [-1.15 ; +0.05] |  |
| heure 10:00→11:00 ET | GC | 2676 | +0.8 [-0.6 ; +2.1] | -0.1 [-1.4 ; +1.2] | -0.05 [-0.62 ; +0.56] |  |
| heure 10:00→11:00 ET | 6E | 2677 | -0.3 [-0.9 ; +0.4] | -1.1 [-1.7 ; -0.4] | -1.07 [-1.75 ; -0.43] | ▼ |
| heure 10:00→11:00 ET | 6B | 2677 | +0.2 [-0.5 ; +1.0] | -1.1 [-1.9 ; -0.4] | -0.97 [-1.64 ; -0.34] | ▼ |
| heure 10:00→11:00 ET | 6J | 2677 | +0.3 [-0.3 ; +0.9] | -0.8 [-1.4 ; -0.2] | -0.76 [-1.39 ; -0.13] | ▼ |
| heure 10:00→11:00 ET | 6A | 2677 | +0.5 [-0.3 ; +1.3] | -0.9 [-1.8 ; -0.2] | -0.73 [-1.39 ; -0.08] | ▼ |
| heure 11:00→12:00 ET | NQ | 2677 | +1.8 [+0.4 ; +3.2] | +1.3 [-0.1 ; +2.7] | +0.53 [-0.02 ; +1.08] |  |
| heure 11:00→12:00 ET | ES | 2677 | +1.1 [+0.0 ; +2.2] | +0.1 [-1.0 ; +1.2] | +0.08 [-0.47 ; +0.60] |  |
| heure 11:00→12:00 ET | YM | 2675 | +0.9 [-0.2 ; +2.0] | +0.2 [-0.9 ; +1.3] | +0.13 [-0.44 ; +0.66] |  |
| heure 11:00→12:00 ET | GC | 2675 | +0.3 [-0.7 ; +1.2] | -0.6 [-1.6 ; +0.4] | -0.38 [-0.96 ; +0.21] |  |
| heure 11:00→12:00 ET | 6E | 2676 | -0.1 [-0.5 ; +0.4] | -0.9 [-1.3 ; -0.4] | -1.18 [-1.78 ; -0.55] | ▼ |
| heure 11:00→12:00 ET | 6B | 2676 | +0.2 [-0.4 ; +0.8] | -1.2 [-1.8 ; -0.6] | -1.30 [-1.93 ; -0.67] | ▼ |
| heure 11:00→12:00 ET | 6J | 2676 | -0.3 [-0.8 ; +0.2] | -1.4 [-2.0 ; -0.9] | -1.79 [-2.52 ; -1.12] | ▼ |
| heure 11:00→12:00 ET | 6A | 2676 | -0.8 [-1.4 ; -0.2] | -2.2 [-2.8 ; -1.6] | -2.24 [-2.82 ; -1.64] | ▼ |
| heure 12:00→13:00 ET | NQ | 2677 | +0.1 [-1.0 ; +1.3] | -0.4 [-1.6 ; +0.8] | -0.18 [-0.74 ; +0.35] |  |
| heure 12:00→13:00 ET | ES | 2677 | +0.4 [-0.5 ; +1.4] | -0.6 [-1.5 ; +0.4] | -0.34 [-0.91 ; +0.16] |  |
| heure 12:00→13:00 ET | YM | 2675 | +0.3 [-0.6 ; +1.3] | -0.4 [-1.3 ; +0.6] | -0.23 [-0.78 ; +0.24] |  |
| heure 12:00→13:00 ET | GC | 2675 | -0.6 [-1.3 ; +0.1] | -1.5 [-2.2 ; -0.8] | -1.20 [-1.77 ; -0.65] | ▼ |
| heure 12:00→13:00 ET | 6E | 2676 | +0.0 [-0.4 ; +0.4] | -0.8 [-1.2 ; -0.4] | -1.37 [-2.03 ; -0.71] | ▼ |
| heure 12:00→13:00 ET | 6B | 2676 | -0.0 [-0.4 ; +0.5] | -1.4 [-1.8 ; -0.9] | -1.94 [-2.55 ; -1.29] | ▼ |
| heure 12:00→13:00 ET | 6J | 2676 | -0.3 [-0.7 ; +0.1] | -1.4 [-1.8 ; -1.0] | -2.32 [-3.01 ; -1.72] | ▼ |
| heure 12:00→13:00 ET | 6A | 2676 | +0.1 [-0.3 ; +0.5] | -1.4 [-1.8 ; -0.9] | -1.87 [-2.48 ; -1.25] | ▼ |
| heure 13:00→14:00 ET | NQ | 2677 | +0.0 [-1.4 ; +1.4] | -0.5 [-1.9 ; +0.9] | -0.23 [-0.93 ; +0.42] |  |
| heure 13:00→14:00 ET | ES | 2677 | -0.3 [-1.4 ; +0.9] | -1.3 [-2.4 ; -0.1] | -0.69 [-1.46 ; +0.01] | ▼ |
| heure 13:00→14:00 ET | YM | 2675 | -0.3 [-1.4 ; +0.7] | -1.0 [-2.1 ; +0.0] | -0.60 [-1.30 ; +0.08] |  |
| heure 13:00→14:00 ET | GC | 2675 | +0.2 [-0.5 ; +0.8] | -0.7 [-1.3 ; -0.1] | -0.60 [-1.18 ; -0.05] | ▼ |
| heure 13:00→14:00 ET | 6E | 2676 | +0.2 [-0.2 ; +0.5] | -0.6 [-1.0 ; -0.3] | -1.16 [-1.77 ; -0.54] | ▼ |
| heure 13:00→14:00 ET | 6B | 2676 | +0.0 [-0.3 ; +0.4] | -1.4 [-1.7 ; -1.0] | -2.14 [-2.76 ; -1.54] | ▼ |
| heure 13:00→14:00 ET | 6J | 2676 | -0.2 [-0.6 ; +0.1] | -1.3 [-1.7 ; -1.0] | -2.10 [-2.71 ; -1.48] | ▼ |
| heure 13:00→14:00 ET | 6A | 2676 | +0.2 [-0.2 ; +0.6] | -1.2 [-1.7 ; -0.8] | -1.67 [-2.44 ; -0.93] | ▼ |
| heure 14:00→15:00 ET | NQ | 2656 | +1.1 [-0.2 ; +2.3] | +0.6 [-0.7 ; +1.8] | +0.26 [-0.27 ; +0.81] |  |
| heure 14:00→15:00 ET | ES | 2656 | +0.8 [-0.2 ; +1.8] | -0.2 [-1.2 ; +0.8] | -0.13 [-0.64 ; +0.41] |  |
| heure 14:00→15:00 ET | YM | 2653 | +0.7 [-0.2 ; +1.7] | +0.0 [-0.9 ; +1.0] | +0.02 [-0.50 ; +0.57] |  |
| heure 14:00→15:00 ET | GC | 2661 | +0.2 [-0.6 ; +1.0] | -0.6 [-1.4 ; +0.2] | -0.46 [-0.98 ; +0.08] |  |
| heure 14:00→15:00 ET | 6E | 2663 | +0.3 [-0.1 ; +0.7] | -0.5 [-0.9 ; -0.1] | -0.78 [-1.39 ; -0.16] | ▼ |
| heure 14:00→15:00 ET | 6B | 2663 | +0.2 [-0.3 ; +0.7] | -1.2 [-1.7 ; -0.7] | -1.61 [-2.23 ; -0.95] | ▼ |
| heure 14:00→15:00 ET | 6J | 2663 | -0.0 [-0.5 ; +0.4] | -1.1 [-1.6 ; -0.7] | -1.59 [-2.26 ; -0.88] | ▼ |
| heure 14:00→15:00 ET | 6A | 2663 | +0.3 [-0.2 ; +0.9] | -1.1 [-1.6 ; -0.5] | -1.21 [-1.83 ; -0.57] | ▼ |
| heure 15:00→16:00 ET | NQ | 2656 | -0.3 [-1.8 ; +1.2] | -0.8 [-2.3 ; +0.7] | -0.28 [-0.77 ; +0.23] |  |
| heure 15:00→16:00 ET | ES | 2656 | -0.2 [-1.5 ; +1.2] | -1.2 [-2.5 ; +0.2] | -0.50 [-1.05 ; +0.05] |  |
| heure 15:00→16:00 ET | YM | 2653 | -0.1 [-1.4 ; +1.1] | -0.8 [-2.1 ; +0.4] | -0.36 [-0.92 ; +0.18] |  |
| heure 15:00→16:00 ET | GC | 2659 | -0.1 [-0.7 ; +0.6] | -0.9 [-1.6 ; -0.3] | -0.81 [-1.41 ; -0.22] | ▼ |
| heure 15:00→16:00 ET | 6E | 2661 | +0.0 [-0.2 ; +0.3] | -0.8 [-1.0 ; -0.5] | -1.70 [-2.32 ; -1.06] | ▼ |
| heure 15:00→16:00 ET | 6B | 2661 | +0.1 [-0.2 ; +0.4] | -1.3 [-1.6 ; -1.0] | -2.53 [-3.15 ; -1.87] | ▼ |
| heure 15:00→16:00 ET | 6J | 2661 | -0.4 [-0.7 ; -0.1] | -1.5 [-1.9 ; -1.2] | -2.94 [-3.53 ; -2.35] | ▼ |
| heure 15:00→16:00 ET | 6A | 2661 | +0.1 [-0.3 ; +0.5] | -1.3 [-1.7 ; -0.9] | -1.99 [-2.60 ; -1.42] | ▼ |
| heure 16:00→17:00 ET | NQ | 2656 | +1.4 [+0.4 ; +2.3] | +0.9 [-0.1 ; +1.8] | +0.53 [-0.04 ; +1.15] |  |
| heure 16:00→17:00 ET | ES | 2656 | +0.6 [-0.2 ; +1.3] | -0.4 [-1.2 ; +0.3] | -0.38 [-0.94 ; +0.28] |  |
| heure 16:00→17:00 ET | YM | 2654 | +1.0 [+0.4 ; +1.6] | +0.3 [-0.3 ; +0.9] | +0.33 [-0.29 ; +1.05] |  |
| heure 16:00→17:00 ET | GC | 2660 | +0.7 [+0.2 ; +1.2] | -0.2 [-0.6 ; +0.3] | -0.23 [-0.95 ; +0.42] |  |
| heure 16:00→17:00 ET | 6E | 2661 | +0.0 [-0.2 ; +0.2] | -0.8 [-1.0 ; -0.6] | -2.56 [-3.22 ; -1.91] | ▼ |
| heure 16:00→17:00 ET | 6B | 2661 | +0.3 [+0.1 ; +0.6] | -1.0 [-1.3 ; -0.8] | -2.59 [-3.40 ; -1.84] | ▼ |
| heure 16:00→17:00 ET | 6J | 2661 | -0.5 [-0.8 ; -0.1] | -1.6 [-1.9 ; -1.3] | -3.20 [-4.55 ; -2.21] | ▼ |
| heure 16:00→17:00 ET | 6A | 2661 | -0.0 [-0.3 ; +0.2] | -1.5 [-1.7 ; -1.2] | -3.15 [-3.84 ; -2.55] | ▼ |

### [2] Berkman-Koch-Tuttle-Zhang

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| DIFF long nuit + short jour | NQ | 5344 | +0.9 [-1.4 ; +3.1] | +0.3 [-2.0 ; +2.6] | +0.08 [-0.46 ; +0.60] |  |
| DIFF long nuit + short jour | ES | 5342 | +0.6 [-1.2 ; +2.4] | -0.4 [-2.2 ; +1.4] | -0.11 [-0.63 ; +0.41] |  |
| DIFF long nuit + short jour | YM | 5337 | +0.6 [-1.0 ; +2.3] | -0.1 [-1.7 ; +1.6] | -0.02 [-0.53 ; +0.52] |  |
| DIFF long nuit + short jour | GC | 5316 | +2.6 [+0.9 ; +4.3] | +1.7 [+0.0 ; +3.5] | +0.55 [+0.02 ; +1.07] | ▲ |
| DIFF long nuit + short jour | 6E | 5350 | -0.4 [-1.3 ; +0.4] | -1.2 [-2.1 ; -0.4] | -0.84 [-1.41 ; -0.21] | ▼ |
| DIFF long nuit + short jour | 6B | 5350 | -1.2 [-2.3 ; -0.3] | -2.6 [-3.7 ; -1.6] | -1.45 [-1.99 ; -0.90] | ▼ |
| DIFF long nuit + short jour | 6J | 5352 | -0.2 [-1.4 ; +0.9] | -1.4 [-2.5 ; -0.3] | -0.75 [-1.37 ; -0.08] | ▼ |
| DIFF long nuit + short jour | 6A | 5345 | -0.2 [-1.3 ; +0.9] | -1.7 [-2.7 ; -0.6] | -0.83 [-1.34 ; -0.30] | ▼ |
| long nuit si VOL(t-1) tercile haut | NQ | 1017 | +5.9 [+0.3 ; +11.3] | +5.5 [-0.1 ; +10.8] | +0.57 [-0.00 ; +1.17] |  |
| long nuit si VOL(t-1) tercile haut | ES | 972 | +3.7 [-1.3 ; +8.8] | +2.7 [-2.2 ; +7.9] | +0.34 [-0.28 ; +0.97] |  |
| long nuit si VOL(t-1) tercile haut | YM | 938 | +3.3 [-2.1 ; +8.5] | +2.7 [-2.8 ; +7.8] | +0.33 [-0.20 ; +0.90] |  |
| long nuit si VOL(t-1) tercile haut | GC | 969 | +4.7 [-0.7 ; +10.6] | +4.0 [-1.5 ; +9.8] | +0.44 [-0.16 ; +1.02] |  |
| long nuit si VOL(t-1) tercile haut | 6E | 843 | -2.1 [-4.7 ; +0.5] | -2.9 [-5.5 ; -0.3] | -0.65 [-1.29 ; -0.05] | ▼ |
| long nuit si VOL(t-1) tercile haut | 6B | 766 | -2.5 [-6.6 ; +1.4] | -3.9 [-8.0 ; +0.0] | -0.57 [-1.10 ; -0.02] |  |
| long nuit si VOL(t-1) tercile haut | 6J | 784 | -0.7 [-4.4 ; +3.5] | -1.8 [-5.6 ; +2.3] | -0.29 [-0.96 ; +0.32] |  |
| long nuit si VOL(t-1) tercile haut | 6A | 832 | +3.7 [-0.2 ; +7.1] | +2.2 [-1.7 ; +5.6] | +0.37 [-0.24 ; +1.00] |  |
| short jour si VOL(t-1) tercile haut | NQ | 1017 | -3.0 [-10.5 ; +4.8] | -3.5 [-10.9 ; +4.4] | -0.27 [-0.82 ; +0.33] |  |
| short jour si VOL(t-1) tercile haut | ES | 972 | -3.3 [-9.5 ; +2.9] | -4.3 [-10.5 ; +1.9] | -0.41 [-0.95 ; +0.15] |  |
| short jour si VOL(t-1) tercile haut | YM | 937 | -4.1 [-9.8 ; +1.8] | -4.8 [-10.4 ; +1.1] | -0.46 [-0.97 ; +0.02] |  |
| short jour si VOL(t-1) tercile haut | GC | 968 | -0.3 [-4.3 ; +3.7] | -1.1 [-5.1 ; +3.0] | -0.15 [-0.70 ; +0.38] |  |
| short jour si VOL(t-1) tercile haut | 6E | 842 | +0.0 [-2.1 ; +2.0] | -0.8 [-2.9 ; +1.2] | -0.23 [-0.81 ; +0.37] |  |
| short jour si VOL(t-1) tercile haut | 6B | 765 | +0.2 [-2.0 ; +2.4] | -1.2 [-3.4 ; +1.0] | -0.28 [-0.88 ; +0.39] |  |
| short jour si VOL(t-1) tercile haut | 6J | 784 | +0.7 [-1.8 ; +3.5] | -0.4 [-3.0 ; +2.3] | -0.11 [-0.78 ; +0.54] |  |
| short jour si VOL(t-1) tercile haut | 6A | 831 | +2.0 [-0.6 ; +4.6] | +0.5 [-2.1 ; +3.2] | +0.12 [-0.52 ; +0.77] |  |
| DIFF si VOL(t-1) tercile haut | NQ | 2034 | +1.5 [-3.3 ; +6.1] | +1.0 [-3.8 ; +5.7] | +0.12 [-0.45 ; +0.70] |  |
| DIFF si VOL(t-1) tercile haut | ES | 1944 | +0.2 [-3.8 ; +3.7] | -0.8 [-4.8 ; +2.7] | -0.12 [-0.70 ; +0.45] |  |
| DIFF si VOL(t-1) tercile haut | YM | 1875 | -0.4 [-3.8 ; +3.1] | -1.0 [-4.5 ; +2.4] | -0.16 [-0.65 ; +0.39] |  |
| DIFF si VOL(t-1) tercile haut | GC | 1937 | +2.2 [-1.2 ; +5.8] | +1.4 [-2.0 ; +5.1] | +0.24 [-0.34 ; +0.78] |  |
| DIFF si VOL(t-1) tercile haut | 6E | 1685 | -1.0 [-2.7 ; +0.6] | -1.8 [-3.5 ; -0.2] | -0.65 [-1.27 ; -0.04] | ▼ |
| DIFF si VOL(t-1) tercile haut | 6B | 1531 | -1.1 [-3.4 ; +1.2] | -2.5 [-4.8 ; -0.2] | -0.67 [-1.18 ; -0.16] | ▼ |
| DIFF si VOL(t-1) tercile haut | 6J | 1568 | +0.0 [-2.5 ; +2.7] | -1.1 [-3.6 ; +1.5] | -0.30 [-1.02 ; +0.37] |  |
| DIFF si VOL(t-1) tercile haut | 6A | 1663 | +2.8 [+0.5 ; +5.1] | +1.4 [-1.0 ; +3.6] | +0.37 [-0.21 ; +0.96] |  |
| DIFF si VOL(t-1) haut et vol 20 j > médiane | NQ | 1580 | +2.3 [-3.8 ; +8.0] | +1.8 [-4.3 ; +7.5] | +0.18 [-0.43 ; +0.75] |  |
| DIFF si VOL(t-1) haut et vol 20 j > médiane | ES | 1486 | -0.1 [-5.0 ; +4.6] | -1.1 [-6.0 ; +3.6] | -0.13 [-0.67 ; +0.47] |  |
| DIFF si VOL(t-1) haut et vol 20 j > médiane | YM | 1383 | +0.5 [-3.6 ; +4.9] | -0.2 [-4.3 ; +4.3] | -0.02 [-0.54 ; +0.52] |  |
| DIFF si VOL(t-1) haut et vol 20 j > médiane | GC | 1389 | +1.5 [-2.7 ; +6.1] | +0.8 [-3.4 ; +5.4] | +0.10 [-0.47 ; +0.69] |  |
| DIFF si VOL(t-1) haut et vol 20 j > médiane | 6E | 949 | -1.6 [-4.0 ; +0.7] | -2.4 [-4.9 ; -0.2] | -0.60 [-1.17 ; +0.01] | ▼ |
| DIFF si VOL(t-1) haut et vol 20 j > médiane | 6B | 708 | -2.4 [-6.8 ; +1.9] | -3.9 [-8.2 ; +0.4] | -0.59 [-1.06 ; -0.09] |  |
| DIFF si VOL(t-1) haut et vol 20 j > médiane | 6J | 994 | +1.2 [-2.5 ; +4.8] | -0.1 [-3.7 ; +3.6] | -0.01 [-0.77 ; +0.62] |  |
| DIFF si VOL(t-1) haut et vol 20 j > médiane | 6A | 996 | +1.5 [-1.9 ; +5.0] | +0.1 [-3.4 ; +3.6] | +0.01 [-0.55 ; +0.59] |  |
| DIFF si VOL(t-1) haut, lundis | NQ | 400 | -5.9 [-17.5 ; +5.7] | -6.4 [-18.0 ; +5.2] | -0.36 [-0.93 ; +0.30] |  |
| DIFF si VOL(t-1) haut, lundis | ES | 410 | -3.2 [-11.0 ; +4.7] | -4.2 [-11.9 ; +3.7] | -0.29 [-0.85 ; +0.31] |  |
| DIFF si VOL(t-1) haut, lundis | YM | 392 | -6.2 [-15.4 ; +2.5] | -6.8 [-16.0 ; +1.9] | -0.49 [-1.04 ; +0.14] |  |
| DIFF si VOL(t-1) haut, lundis | GC | 400 | -1.6 [-9.5 ; +5.7] | -2.4 [-10.3 ; +4.8] | -0.21 [-0.72 ; +0.41] |  |
| DIFF si VOL(t-1) haut, lundis | 6E | 324 | +0.9 [-2.8 ; +4.4] | +0.1 [-3.6 ; +3.6] | +0.01 [-0.61 ; +0.63] |  |
| DIFF si VOL(t-1) haut, lundis | 6B | 306 | -0.5 [-5.3 ; +4.6] | -1.9 [-6.7 ; +3.2] | -0.24 [-0.80 ; +0.32] |  |
| DIFF si VOL(t-1) haut, lundis | 6J | 308 | -1.1 [-7.3 ; +5.5] | -2.3 [-8.5 ; +4.3] | -0.24 [-1.07 ; +0.40] |  |
| DIFF si VOL(t-1) haut, lundis | 6A | 322 | +0.6 [-3.7 ; +5.0] | -0.8 [-5.1 ; +3.5] | -0.11 [-0.67 ; +0.53] |  |

### [3] Lu-Qin

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| NMD ouverture déplacée à 10:00 | NQ | 5354 | +1.8 [-0.5 ; +4.0] | +1.2 [-1.0 ; +3.5] | +0.31 [-0.22 ; +0.81] |  |
| NMD ouverture déplacée à 10:00 | ES | 5354 | +1.1 [-0.8 ; +3.0] | +0.1 [-1.8 ; +2.0] | +0.02 [-0.57 ; +0.61] |  |
| NMD ouverture déplacée à 10:00 | YM | 5349 | +1.3 [-0.6 ; +3.2] | +0.6 [-1.3 ; +2.5] | +0.20 [-0.42 ; +0.81] |  |
| NMD ouverture déplacée à 10:00 | GC | 5313 | +1.8 [-0.0 ; +3.5] | +0.9 [-0.9 ; +2.7] | +0.28 [-0.25 ; +0.83] |  |
| NMD ouverture déplacée à 10:00 | 6E | 5350 | -0.3 [-1.2 ; +0.5] | -1.1 [-2.0 ; -0.3] | -0.76 [-1.34 ; -0.14] | ▼ |
| NMD ouverture déplacée à 10:00 | 6B | 5350 | -0.9 [-1.9 ; +0.1] | -2.3 [-3.3 ; -1.3] | -1.26 [-1.79 ; -0.70] | ▼ |
| NMD ouverture déplacée à 10:00 | 6J | 5352 | -0.1 [-1.2 ; +1.0] | -1.2 [-2.4 ; -0.1] | -0.67 [-1.26 ; -0.02] | ▼ |
| NMD ouverture déplacée à 10:00 | 6A | 5346 | -0.3 [-1.4 ; +0.8] | -1.7 [-2.8 ; -0.6] | -0.86 [-1.39 ; -0.32] | ▼ |
| NMD ouverture déplacée à 10:30 | NQ | 5354 | +1.9 [-0.3 ; +4.3] | +1.4 [-0.9 ; +3.7] | +0.34 [-0.19 ; +0.87] |  |
| NMD ouverture déplacée à 10:30 | ES | 5354 | +1.2 [-0.7 ; +3.1] | +0.2 [-1.7 ; +2.1] | +0.07 [-0.48 ; +0.62] |  |
| NMD ouverture déplacée à 10:30 | YM | 5348 | +1.4 [-0.6 ; +3.4] | +0.7 [-1.3 ; +2.7] | +0.22 [-0.36 ; +0.79] |  |
| NMD ouverture déplacée à 10:30 | GC | 5313 | +2.3 [+0.5 ; +4.2] | +1.4 [-0.4 ; +3.3] | +0.44 [-0.07 ; +1.00] |  |
| NMD ouverture déplacée à 10:30 | 6E | 5349 | -0.2 [-1.1 ; +0.8] | -1.0 [-1.9 ; -0.0] | -0.65 [-1.28 ; -0.01] | ▼ |
| NMD ouverture déplacée à 10:30 | 6B | 5349 | -0.6 [-1.7 ; +0.5] | -2.0 [-3.1 ; -0.9] | -1.13 [-1.71 ; -0.55] | ▼ |
| NMD ouverture déplacée à 10:30 | 6J | 5351 | +0.3 [-0.8 ; +1.4] | -0.9 [-1.9 ; +0.2] | -0.46 [-1.07 ; +0.16] |  |
| NMD ouverture déplacée à 10:30 | 6A | 5345 | -0.0 [-1.1 ; +1.1] | -1.5 [-2.6 ; -0.4] | -0.74 [-1.29 ; -0.17] | ▼ |
| NMD ouverture déplacée à 11:00 | NQ | 5354 | +0.8 [-1.4 ; +3.0] | +0.3 [-1.9 ; +2.5] | +0.07 [-0.44 ; +0.55] |  |
| NMD ouverture déplacée à 11:00 | ES | 5354 | +0.6 [-1.3 ; +2.5] | -0.4 [-2.3 ; +1.5] | -0.11 [-0.65 ; +0.43] |  |
| NMD ouverture déplacée à 11:00 | YM | 5348 | +0.8 [-1.1 ; +2.8] | +0.1 [-1.8 ; +2.1] | +0.04 [-0.57 ; +0.63] |  |
| NMD ouverture déplacée à 11:00 | GC | 5311 | +2.5 [+0.7 ; +4.4] | +1.6 [-0.2 ; +3.6] | +0.52 [-0.03 ; +1.10] |  |
| NMD ouverture déplacée à 11:00 | 6E | 5349 | -0.6 [-1.5 ; +0.3] | -1.4 [-2.3 ; -0.5] | -0.94 [-1.62 ; -0.30] | ▼ |
| NMD ouverture déplacée à 11:00 | 6B | 5349 | -0.7 [-1.7 ; +0.5] | -2.0 [-3.1 ; -0.9] | -1.08 [-1.65 ; -0.50] | ▼ |
| NMD ouverture déplacée à 11:00 | 6J | 5351 | +0.3 [-0.8 ; +1.4] | -0.9 [-1.9 ; +0.3] | -0.45 [-1.09 ; +0.19] |  |
| NMD ouverture déplacée à 11:00 | 6A | 5345 | +0.2 [-0.9 ; +1.3] | -1.2 [-2.4 ; -0.1] | -0.62 [-1.20 ; -0.03] | ▼ |
| NMD clôture avancée à 14:30 | NQ | 5258 | +1.8 [-0.6 ; +4.0] | +1.2 [-1.1 ; +3.5] | +0.29 [-0.21 ; +0.80] |  |
| NMD clôture avancée à 14:30 | ES | 5256 | +1.0 [-0.7 ; +2.7] | +0.0 [-1.7 ; +1.7] | +0.00 [-0.51 ; +0.54] |  |
| NMD clôture avancée à 14:30 | YM | 5250 | +1.0 [-0.7 ; +2.7] | +0.3 [-1.4 ; +2.0] | +0.09 [-0.46 ; +0.63] |  |
| NMD clôture avancée à 14:30 | GC | 5225 | +2.6 [+0.7 ; +4.5] | +1.7 [-0.2 ; +3.7] | +0.52 [-0.05 ; +1.08] |  |
| NMD clôture avancée à 14:30 | 6E | 5266 | -0.4 [-1.2 ; +0.5] | -1.2 [-2.0 ; -0.3] | -0.77 [-1.37 ; -0.13] | ▼ |
| NMD clôture avancée à 14:30 | 6B | 5258 | -1.2 [-2.2 ; -0.1] | -2.6 [-3.6 ; -1.5] | -1.41 [-1.95 ; -0.85] | ▼ |
| NMD clôture avancée à 14:30 | 6J | 5260 | -0.6 [-1.7 ; +0.5] | -1.7 [-2.8 ; -0.6] | -0.93 [-1.59 ; -0.26] | ▼ |
| NMD clôture avancée à 14:30 | 6A | 5247 | -0.0 [-1.1 ; +1.1] | -1.5 [-2.5 ; -0.3] | -0.72 [-1.25 ; -0.19] | ▼ |
| NMD clôture avancée à 15:00 | NQ | 5258 | +0.6 [-1.6 ; +2.8] | +0.1 [-2.2 ; +2.3] | +0.02 [-0.48 ; +0.52] |  |
| NMD clôture avancée à 15:00 | ES | 5256 | +0.3 [-1.4 ; +2.0] | -0.7 [-2.4 ; +1.0] | -0.21 [-0.73 ; +0.32] |  |
| NMD clôture avancée à 15:00 | YM | 5250 | +0.3 [-1.3 ; +2.0] | -0.3 [-2.0 ; +1.4] | -0.11 [-0.64 ; +0.45] |  |
| NMD clôture avancée à 15:00 | GC | 5225 | +2.4 [+0.5 ; +4.2] | +1.6 [-0.4 ; +3.4] | +0.48 [-0.07 ; +1.01] |  |
| NMD clôture avancée à 15:00 | 6E | 5266 | -0.5 [-1.3 ; +0.4] | -1.3 [-2.1 ; -0.4] | -0.85 [-1.44 ; -0.22] | ▼ |
| NMD clôture avancée à 15:00 | 6B | 5264 | -1.2 [-2.2 ; -0.2] | -2.6 [-3.6 ; -1.5] | -1.44 [-2.00 ; -0.88] | ▼ |
| NMD clôture avancée à 15:00 | 6J | 5264 | -0.7 [-1.8 ; +0.5] | -1.8 [-2.9 ; -0.6] | -1.00 [-1.64 ; -0.33] | ▼ |
| NMD clôture avancée à 15:00 | 6A | 5265 | -0.1 [-1.3 ; +1.0] | -1.6 [-2.7 ; -0.4] | -0.78 [-1.30 ; -0.26] | ▼ |
| NMD clôture avancée à 15:30 | NQ | 5258 | +0.8 [-1.6 ; +3.1] | +0.2 [-2.1 ; +2.5] | +0.05 [-0.46 ; +0.57] |  |
| NMD clôture avancée à 15:30 | ES | 5256 | +0.2 [-1.5 ; +1.8] | -0.8 [-2.5 ; +0.8] | -0.26 [-0.78 ; +0.27] |  |
| NMD clôture avancée à 15:30 | YM | 5251 | +0.1 [-1.8 ; +1.9] | -0.6 [-2.4 ; +1.2] | -0.20 [-0.75 ; +0.34] |  |
| NMD clôture avancée à 15:30 | GC | 5216 | +2.5 [+0.7 ; +4.3] | +1.6 [-0.2 ; +3.4] | +0.49 [-0.03 ; +1.00] |  |
| NMD clôture avancée à 15:30 | 6E | 5266 | -0.5 [-1.4 ; +0.3] | -1.3 [-2.2 ; -0.5] | -0.90 [-1.48 ; -0.27] | ▼ |
| NMD clôture avancée à 15:30 | 6B | 5242 | -1.3 [-2.4 ; -0.3] | -2.7 [-3.8 ; -1.7] | -1.51 [-2.05 ; -0.96] | ▼ |
| NMD clôture avancée à 15:30 | 6J | 5258 | -0.4 [-1.5 ; +0.7] | -1.5 [-2.7 ; -0.4] | -0.83 [-1.47 ; -0.17] | ▼ |
| NMD clôture avancée à 15:30 | 6A | 5241 | -0.1 [-1.3 ; +1.0] | -1.6 [-2.7 ; -0.4] | -0.77 [-1.31 ; -0.24] | ▼ |
| NMD × signe(MOM 12-1) | NQ | 4844 | +3.0 [+0.4 ; +5.4] | +2.5 [-0.1 ; +4.9] | +0.58 [+0.01 ; +1.13] |  |
| NMD × signe(MOM 12-1) | ES | 4842 | +2.2 [+0.4 ; +4.2] | +1.3 [-0.5 ; +3.2] | +0.38 [-0.17 ; +0.97] |  |
| NMD × signe(MOM 12-1) | YM | 4837 | +1.8 [+0.0 ; +3.7] | +1.2 [-0.6 ; +3.0] | +0.35 [-0.19 ; +0.91] |  |
| NMD × signe(MOM 12-1) | GC | 4818 | +2.0 [+0.1 ; +3.9] | +1.2 [-0.7 ; +3.0] | +0.38 [-0.22 ; +0.93] |  |
| NMD × signe(MOM 12-1) | 6E | 4850 | +0.0 [-0.9 ; +0.9] | -0.8 [-1.7 ; +0.1] | -0.55 [-1.22 ; +0.08] |  |
| NMD × signe(MOM 12-1) | 6B | 4850 | +1.3 [+0.3 ; +2.3] | -0.0 [-1.1 ; +0.9] | -0.03 [-0.59 ; +0.56] |  |
| NMD × signe(MOM 12-1) | 6J | 4852 | +0.5 [-0.7 ; +1.6] | -0.6 [-1.9 ; +0.5] | -0.37 [-1.00 ; +0.34] |  |
| NMD × signe(MOM 12-1) | 6A | 4847 | +0.2 [-1.0 ; +1.3] | -1.2 [-2.4 ; -0.1] | -0.63 [-1.21 ; -0.08] | ▼ |
| NMD × -signe(STR 1 mois) | NQ | 5310 | -0.9 [-3.3 ; +1.3] | -1.4 [-3.8 ; +0.8] | -0.34 [-0.90 ; +0.23] |  |
| NMD × -signe(STR 1 mois) | ES | 5308 | -1.4 [-3.4 ; +0.3] | -2.4 [-4.4 ; -0.7] | -0.72 [-1.26 ; -0.20] | ▼ |
| NMD × -signe(STR 1 mois) | YM | 5303 | -0.9 [-2.8 ; +0.9] | -1.6 [-3.5 ; +0.2] | -0.51 [-1.03 ; +0.03] |  |
| NMD × -signe(STR 1 mois) | GC | 5282 | -1.3 [-3.1 ; +0.5] | -2.2 [-4.0 ; -0.4] | -0.67 [-1.27 ; -0.15] | ▼ |
| NMD × -signe(STR 1 mois) | 6E | 5316 | -0.3 [-1.2 ; +0.5] | -1.1 [-2.0 ; -0.3] | -0.77 [-1.40 ; -0.13] | ▼ |
| NMD × -signe(STR 1 mois) | 6B | 5316 | -0.8 [-1.9 ; +0.3] | -2.2 [-3.3 ; -1.1] | -1.23 [-1.83 ; -0.64] | ▼ |
| NMD × -signe(STR 1 mois) | 6J | 5318 | +0.4 [-0.7 ; +1.5] | -0.7 [-1.8 ; +0.4] | -0.40 [-0.99 ; +0.21] |  |
| NMD × -signe(STR 1 mois) | 6A | 5311 | -0.4 [-1.5 ; +0.7] | -1.8 [-2.9 ; -0.7] | -0.91 [-1.43 ; -0.36] | ▼ |

### [4] Jones-Pyun-Wang

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| nuit 15:59→9:45 × signe(r 9:45→15:00) | NQ | 2642 | +1.5 [-1.7 ; +4.6] | +1.0 [-2.2 ; +4.1] | +0.19 [-0.39 ; +0.76] |  |
| nuit 15:59→9:45 × signe(r 9:45→15:00) | ES | 2628 | +1.2 [-1.4 ; +3.6] | +0.2 [-2.4 ; +2.6] | +0.04 [-0.52 ; +0.60] |  |
| nuit 15:59→9:45 × signe(r 9:45→15:00) | YM | 2636 | +2.7 [+0.2 ; +5.1] | +2.0 [-0.5 ; +4.4] | +0.47 [-0.08 ; +1.01] |  |
| nuit 15:59→9:45 × signe(r 9:45→15:00) | GC | 2606 | +2.1 [-0.9 ; +5.2] | +1.3 [-1.7 ; +4.3] | +0.24 [-0.39 ; +0.83] |  |
| nuit 15:59→9:45 × signe(r 9:45→15:00) | 6E | 2640 | -1.4 [-2.8 ; +0.0] | -2.2 [-3.6 ; -0.8] | -0.92 [-1.46 ; -0.38] | ▼ |
| nuit 15:59→9:45 × signe(r 9:45→15:00) | 6B | 2625 | -0.6 [-2.4 ; +1.3] | -2.0 [-3.8 ; -0.1] | -0.67 [-1.32 ; -0.05] | ▼ |
| nuit 15:59→9:45 × signe(r 9:45→15:00) | 6J | 2621 | +0.3 [-1.6 ; +2.3] | -0.8 [-2.7 ; +1.2] | -0.25 [-0.84 ; +0.37] |  |
| nuit 15:59→9:45 × signe(r 9:45→15:00) | 6A | 2602 | -0.8 [-2.8 ; +1.2] | -2.2 [-4.2 ; -0.2] | -0.68 [-1.27 ; -0.12] | ▼ |
| nuit long si r(9:45→15:00) > 0 | NQ | 1481 | +5.9 [+1.8 ; +10.2] | +5.4 [+1.2 ; +9.7] | +0.80 [+0.21 ; +1.39] | ▲ |
| nuit long si r(9:45→15:00) > 0 | ES | 1443 | +4.3 [+1.2 ; +7.5] | +3.3 [+0.2 ; +6.5] | +0.62 [+0.04 ; +1.24] | ▲ |
| nuit long si r(9:45→15:00) > 0 | YM | 1430 | +5.9 [+2.6 ; +9.5] | +5.3 [+1.9 ; +8.8] | +0.97 [+0.38 ; +1.58] | ▲ |
| nuit long si r(9:45→15:00) > 0 | GC | 1342 | +6.1 [+1.4 ; +10.7] | +5.2 [+0.5 ; +9.9] | +0.74 [+0.14 ; +1.30] | ▲ |
| nuit long si r(9:45→15:00) > 0 | 6E | 1279 | -1.9 [-3.9 ; +0.3] | -2.7 [-4.7 ; -0.5] | -0.78 [-1.33 ; -0.20] | ▼ |
| nuit long si r(9:45→15:00) > 0 | 6B | 1315 | -1.8 [-4.1 ; +0.5] | -3.2 [-5.5 ; -0.9] | -0.79 [-1.35 ; -0.18] | ▼ |
| nuit long si r(9:45→15:00) > 0 | 6J | 1197 | -0.8 [-3.5 ; +1.9] | -1.9 [-4.6 ; +0.8] | -0.41 [-1.03 ; +0.19] |  |
| nuit long si r(9:45→15:00) > 0 | 6A | 1325 | -0.6 [-3.4 ; +2.0] | -2.0 [-4.8 ; +0.6] | -0.44 [-1.01 ; +0.10] |  |
| jour suivant 9:45→15:59 × -signe(r) | NQ | 2642 | +2.6 [-1.5 ; +6.7] | +2.0 [-2.1 ; +6.2] | +0.32 [-0.28 ; +0.92] |  |
| jour suivant 9:45→15:59 × -signe(r) | ES | 2628 | +2.0 [-1.0 ; +5.2] | +1.0 [-2.0 ; +4.2] | +0.20 [-0.43 ; +0.81] |  |
| jour suivant 9:45→15:59 × -signe(r) | YM | 2634 | +0.6 [-2.6 ; +3.5] | -0.1 [-3.3 ; +2.9] | -0.03 [-0.62 ; +0.56] |  |
| jour suivant 9:45→15:59 × -signe(r) | GC | 2598 | +0.8 [-1.5 ; +3.2] | -0.0 [-2.4 ; +2.3] | -0.01 [-0.64 ; +0.58] |  |
| jour suivant 9:45→15:59 × -signe(r) | 6E | 2639 | -0.4 [-1.5 ; +0.6] | -1.2 [-2.3 ; -0.2] | -0.71 [-1.31 ; -0.13] | ▼ |
| jour suivant 9:45→15:59 × -signe(r) | 6B | 2625 | -0.5 [-1.8 ; +0.8] | -1.9 [-3.2 ; -0.6] | -0.91 [-1.51 ; -0.31] | ▼ |
| jour suivant 9:45→15:59 × -signe(r) | 6J | 2620 | +0.1 [-0.9 ; +1.3] | -1.0 [-2.0 ; +0.2] | -0.51 [-1.14 ; +0.07] |  |
| jour suivant 9:45→15:59 × -signe(r) | 6A | 2602 | -0.8 [-2.1 ; +0.6] | -2.2 [-3.5 ; -0.9] | -0.95 [-1.54 ; -0.40] | ▼ |
| nuit - jour suivant | NQ | 5284 | +2.1 [-0.5 ; +4.6] | +1.5 [-1.0 ; +4.0] | +0.38 [-0.22 ; +0.96] |  |
| nuit - jour suivant | ES | 5256 | +1.6 [-0.5 ; +3.6] | +0.6 [-1.5 ; +2.6] | +0.18 [-0.47 ; +0.78] |  |
| nuit - jour suivant | YM | 5270 | +1.6 [-0.3 ; +3.6] | +0.9 [-0.9 ; +2.9] | +0.29 [-0.34 ; +0.93] |  |
| nuit - jour suivant | GC | 5204 | +1.5 [-0.6 ; +3.5] | +0.6 [-1.5 ; +2.7] | +0.19 [-0.43 ; +0.79] |  |
| nuit - jour suivant | 6E | 5279 | -0.9 [-1.8 ; -0.1] | -1.7 [-2.6 ; -0.9] | -1.15 [-1.78 ; -0.55] | ▼ |
| nuit - jour suivant | 6B | 5250 | -0.6 [-1.7 ; +0.6] | -1.9 [-3.1 ; -0.8] | -1.08 [-1.76 ; -0.48] | ▼ |
| nuit - jour suivant | 6J | 5241 | +0.2 [-0.9 ; +1.3] | -0.9 [-2.0 ; +0.2] | -0.48 [-1.09 ; +0.13] |  |
| nuit - jour suivant | 6A | 5204 | -0.8 [-1.9 ; +0.3] | -2.2 [-3.3 ; -1.1] | -1.10 [-1.67 ; -0.57] | ▼ |

### [7] Tompkins-Wiener

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| O/C long (jour) | NQ | 2672 | +3.2 [-0.6 ; +7.3] | +2.7 [-1.2 ; +6.7] | +0.39 [-0.14 ; +0.92] |  |
| O/C long (jour) | ES | 2671 | +2.3 [-0.5 ; +5.3] | +1.3 [-1.5 ; +4.3] | +0.24 [-0.29 ; +0.77] |  |
| O/C long (jour) | YM | 2668 | +2.0 [-0.8 ; +4.9] | +1.3 [-1.5 ; +4.2] | +0.27 [-0.25 ; +0.77] |  |
| O/C long (jour) | GC | 2658 | -0.2 [-2.6 ; +2.1] | -1.1 [-3.4 ; +1.3] | -0.26 [-0.77 ; +0.29] |  |
| O/C long (jour) | 6E | 2675 | +0.3 [-0.8 ; +1.2] | -0.5 [-1.6 ; +0.4] | -0.29 [-0.87 ; +0.28] |  |
| O/C long (jour) | 6B | 2675 | +1.1 [-0.1 ; +2.3] | -0.3 [-1.5 ; +0.9] | -0.15 [-0.75 ; +0.44] |  |
| O/C long (jour) | 6J | 2676 | -0.8 [-2.0 ; +0.5] | -1.9 [-3.1 ; -0.7] | -0.97 [-1.58 ; -0.35] | ▼ |
| O/C long (jour) | 6A | 2673 | +0.3 [-1.0 ; +1.7] | -1.1 [-2.4 ; +0.2] | -0.46 [-1.01 ; +0.09] |  |
| C/O long (nuit) | NQ | 2672 | +4.9 [+2.1 ; +7.6] | +4.4 [+1.6 ; +7.1] | +0.88 [+0.32 ; +1.44] | ▲ |
| C/O long (nuit) | ES | 2671 | +3.5 [+1.3 ; +5.7] | +2.5 [+0.3 ; +4.7] | +0.63 [+0.05 ; +1.22] | ▲ |
| C/O long (nuit) | YM | 2669 | +3.3 [+1.1 ; +5.5] | +2.6 [+0.4 ; +4.8] | +0.66 [+0.07 ; +1.25] | ▲ |
| C/O long (nuit) | GC | 2658 | +5.0 [+2.4 ; +7.9] | +4.2 [+1.5 ; +7.0] | +0.82 [+0.30 ; +1.35] | ▲ |
| C/O long (nuit) | 6E | 2675 | -0.6 [-2.0 ; +0.7] | -1.4 [-2.8 ; -0.1] | -0.61 [-1.21 ; +0.01] | ▼ |
| C/O long (nuit) | 6B | 2675 | -1.4 [-3.1 ; +0.3] | -2.7 [-4.5 ; -1.0] | -0.92 [-1.43 ; -0.38] | ▼ |
| C/O long (nuit) | 6J | 2676 | -1.2 [-3.0 ; +0.8] | -2.4 [-4.1 ; -0.3] | -0.77 [-1.38 ; -0.14] | ▼ |
| C/O long (nuit) | 6A | 2672 | -0.1 [-1.9 ; +1.7] | -1.5 [-3.3 ; +0.3] | -0.48 [-1.02 ; +0.08] |  |
| alpha : long nuit + short jour | NQ | 5344 | +0.9 [-1.4 ; +3.1] | +0.3 [-2.0 ; +2.6] | +0.08 [-0.46 ; +0.60] |  |
| alpha : long nuit + short jour | ES | 5342 | +0.6 [-1.2 ; +2.4] | -0.4 [-2.2 ; +1.4] | -0.11 [-0.63 ; +0.41] |  |
| alpha : long nuit + short jour | YM | 5337 | +0.6 [-1.0 ; +2.3] | -0.1 [-1.7 ; +1.6] | -0.02 [-0.53 ; +0.52] |  |
| alpha : long nuit + short jour | GC | 5316 | +2.6 [+0.9 ; +4.3] | +1.7 [+0.0 ; +3.5] | +0.55 [+0.02 ; +1.07] | ▲ |
| alpha : long nuit + short jour | 6E | 5350 | -0.4 [-1.3 ; +0.4] | -1.2 [-2.1 ; -0.4] | -0.84 [-1.41 ; -0.21] | ▼ |
| alpha : long nuit + short jour | 6B | 5350 | -1.2 [-2.3 ; -0.3] | -2.6 [-3.7 ; -1.6] | -1.45 [-1.99 ; -0.90] | ▼ |
| alpha : long nuit + short jour | 6J | 5352 | -0.2 [-1.4 ; +0.9] | -1.4 [-2.5 ; -0.3] | -0.75 [-1.37 ; -0.08] | ▼ |
| alpha : long nuit + short jour | 6A | 5345 | -0.2 [-1.3 ; +0.9] | -1.7 [-2.7 ; -0.6] | -0.83 [-1.34 ; -0.30] | ▼ |
| O/C long (séance propre) | GC | 2662 | -0.9 [-3.5 ; +1.7] | -1.8 [-4.3 ; +0.8] | -0.42 [-0.97 ; +0.18] |  |
| O/C long (séance propre) | 6E | 2675 | -0.5 [-1.9 ; +0.8] | -1.3 [-2.7 ; +0.0] | -0.60 [-1.21 ; -0.03] |  |
| O/C long (séance propre) | 6B | 2675 | +0.1 [-1.5 ; +1.9] | -1.3 [-2.9 ; +0.5] | -0.44 [-1.01 ; +0.12] |  |
| O/C long (séance propre) | 6J | 2675 | +0.1 [-1.4 ; +1.6] | -1.0 [-2.5 ; +0.5] | -0.40 [-1.03 ; +0.23] |  |
| O/C long (séance propre) | 6A | 2673 | -0.1 [-1.8 ; +1.5] | -1.5 [-3.2 ; +0.1] | -0.54 [-1.15 ; +0.06] |  |
| C/O long (séance propre) | GC | 2661 | +5.7 [+2.6 ; +8.7] | +4.8 [+1.8 ; +7.9] | +0.98 [+0.41 ; +1.53] | ▲ |
| C/O long (séance propre) | 6E | 2674 | +0.2 [-0.8 ; +1.3] | -0.6 [-1.6 ; +0.5] | -0.31 [-0.91 ; +0.28] |  |
| C/O long (séance propre) | 6B | 2673 | -0.4 [-1.8 ; +0.9] | -1.8 [-3.1 ; -0.5] | -0.75 [-1.27 ; -0.19] | ▼ |
| C/O long (séance propre) | 6J | 2674 | -2.1 [-3.6 ; -0.6] | -3.2 [-4.7 ; -1.7] | -1.20 [-1.76 ; -0.61] | ▼ |
| C/O long (séance propre) | 6A | 2671 | +0.2 [-1.5 ; +2.0] | -1.2 [-2.9 ; +0.6] | -0.39 [-0.93 ; +0.14] |  |
| alpha (séance propre) | GC | 5323 | +3.3 [+1.3 ; +5.3] | +2.4 [+0.4 ; +4.4] | +0.76 [+0.16 ; +1.37] | ▲ |
| alpha (séance propre) | 6E | 5349 | +0.4 [-0.5 ; +1.3] | -0.4 [-1.3 ; +0.5] | -0.28 [-0.89 ; +0.36] |  |
| alpha (séance propre) | 6B | 5348 | -0.3 [-1.3 ; +0.9] | -1.7 [-2.7 ; -0.5] | -0.90 [-1.48 ; -0.29] | ▼ |
| alpha (séance propre) | 6J | 5349 | -1.1 [-2.1 ; -0.0] | -2.2 [-3.3 ; -1.2] | -1.24 [-1.84 ; -0.65] | ▼ |
| alpha (séance propre) | 6A | 5344 | +0.2 [-1.0 ; +1.3] | -1.3 [-2.4 ; -0.1] | -0.61 [-1.18 ; -0.03] | ▼ |

### [8] Abdi

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| short jour si nuit < 0 | NQ | 1163 | -3.1 [-9.2 ; +3.3] | -3.6 [-9.7 ; +2.7] | -0.32 [-0.90 ; +0.24] |  |
| short jour si nuit < 0 | ES | 1168 | -4.8 [-9.5 ; +0.3] | -5.8 [-10.6 ; -0.7] | -0.67 [-1.21 ; -0.16] | ▼ |
| short jour si nuit < 0 | YM | 1208 | -4.9 [-9.5 ; -0.4] | -5.6 [-10.1 ; -1.1] | -0.73 [-1.24 ; -0.21] | ▼ |
| short jour si nuit < 0 | GC | 1192 | +2.8 [-0.9 ; +6.4] | +1.9 [-1.8 ; +5.5] | +0.30 [-0.23 ; +0.85] |  |
| short jour si nuit < 0 | 6E | 1365 | -0.4 [-1.9 ; +0.9] | -1.2 [-2.7 ; +0.1] | -0.50 [-1.07 ; +0.08] |  |
| short jour si nuit < 0 | 6B | 1330 | -0.1 [-1.9 ; +1.8] | -1.5 [-3.3 ; +0.4] | -0.51 [-1.12 ; +0.08] |  |
| short jour si nuit < 0 | 6J | 1438 | +0.9 [-0.5 ; +2.3] | -0.2 [-1.7 ; +1.2] | -0.08 [-0.71 ; +0.58] |  |
| short jour si nuit < 0 | 6A | 1275 | -0.9 [-2.9 ; +1.0] | -2.3 [-4.3 ; -0.5] | -0.69 [-1.19 ; -0.14] | ▼ |
| long nuit suivante si nuit < 0 | NQ | 1160 | +6.7 [+2.0 ; +11.3] | +6.2 [+1.4 ; +10.8] | +0.76 [+0.14 ; +1.40] | ▲ |
| long nuit suivante si nuit < 0 | ES | 1165 | +4.4 [+0.2 ; +8.6] | +3.3 [-0.9 ; +7.5] | +0.51 [-0.13 ; +1.15] |  |
| long nuit suivante si nuit < 0 | YM | 1205 | +2.3 [-1.4 ; +6.1] | +1.6 [-2.1 ; +5.4] | +0.27 [-0.32 ; +0.83] |  |
| long nuit suivante si nuit < 0 | GC | 1191 | +6.2 [+1.8 ; +11.4] | +5.3 [+0.9 ; +10.5] | +0.72 [+0.15 ; +1.29] | ▲ |
| long nuit suivante si nuit < 0 | 6E | 1364 | -0.5 [-2.4 ; +1.2] | -1.3 [-3.2 ; +0.4] | -0.42 [-1.01 ; +0.22] |  |
| long nuit suivante si nuit < 0 | 6B | 1329 | -1.4 [-3.9 ; +1.0] | -2.8 [-5.3 ; -0.4] | -0.70 [-1.27 ; -0.14] | ▼ |
| long nuit suivante si nuit < 0 | 6J | 1437 | -0.8 [-3.2 ; +1.6] | -1.9 [-4.4 ; +0.5] | -0.48 [-1.08 ; +0.10] |  |
| long nuit suivante si nuit < 0 | 6A | 1275 | +1.5 [-1.5 ; +4.4] | +0.1 [-2.9 ; +3.0] | +0.02 [-0.58 ; +0.63] |  |
| cycle : short jour + long nuit suivante si nuit < 0 | NQ | 2323 | +1.8 [-2.1 ; +5.7] | +1.3 [-2.6 ; +5.1] | +0.19 [-0.42 ; +0.79] |  |
| cycle : short jour + long nuit suivante si nuit < 0 | ES | 2333 | -0.2 [-3.3 ; +3.1] | -1.2 [-4.3 ; +2.1] | -0.22 [-0.80 ; +0.35] |  |
| cycle : short jour + long nuit suivante si nuit < 0 | YM | 2413 | -1.3 [-4.0 ; +1.5] | -2.0 [-4.7 ; +0.8] | -0.41 [-0.95 ; +0.14] |  |
| cycle : short jour + long nuit suivante si nuit < 0 | GC | 2383 | +4.5 [+1.9 ; +7.4] | +3.6 [+1.0 ; +6.5] | +0.75 [+0.18 ; +1.38] | ▲ |
| cycle : short jour + long nuit suivante si nuit < 0 | 6E | 2729 | -0.5 [-1.7 ; +0.7] | -1.3 [-2.5 ; -0.1] | -0.63 [-1.21 ; -0.04] | ▼ |
| cycle : short jour + long nuit suivante si nuit < 0 | 6B | 2659 | -0.8 [-2.2 ; +0.8] | -2.1 [-3.6 ; -0.6] | -0.86 [-1.43 ; -0.32] | ▼ |
| cycle : short jour + long nuit suivante si nuit < 0 | 6J | 2875 | +0.1 [-1.3 ; +1.5] | -1.1 [-2.5 ; +0.4] | -0.45 [-1.08 ; +0.17] |  |
| cycle : short jour + long nuit suivante si nuit < 0 | 6A | 2550 | +0.3 [-1.4 ; +2.0] | -1.1 [-2.8 ; +0.6] | -0.38 [-0.97 ; +0.21] |  |
| cycle avec signal marché = nuit ES < 0 | NQ | 2334 | +0.2 [-3.7 ; +4.3] | -0.3 [-4.3 ; +3.8] | -0.04 [-0.63 ; +0.54] |  |
| cycle avec signal marché = nuit ES < 0 | ES | 2333 | -0.2 [-3.3 ; +3.1] | -1.2 [-4.3 ; +2.1] | -0.22 [-0.80 ; +0.35] |  |
| cycle avec signal marché = nuit ES < 0 | YM | 2328 | -0.3 [-3.3 ; +2.7] | -1.0 [-4.0 ; +2.0] | -0.18 [-0.74 ; +0.36] |  |
| cycle avec signal marché = nuit ES < 0 | GC | 2324 | +2.4 [-0.4 ; +5.4] | +1.6 [-1.3 ; +4.5] | +0.32 [-0.22 ; +0.84] |  |
| cycle avec signal marché = nuit ES < 0 | 6E | 2334 | -0.9 [-2.3 ; +0.5] | -1.7 [-3.1 ; -0.3] | -0.74 [-1.38 ; -0.06] | ▼ |
| cycle avec signal marché = nuit ES < 0 | 6B | 2336 | -1.4 [-3.1 ; +0.2] | -2.8 [-4.5 ; -1.2] | -1.02 [-1.61 ; -0.47] | ▼ |
| cycle avec signal marché = nuit ES < 0 | 6J | 2336 | -0.9 [-2.6 ; +1.0] | -2.0 [-3.8 ; -0.1] | -0.70 [-1.35 ; -0.03] | ▼ |
| cycle avec signal marché = nuit ES < 0 | 6A | 2333 | -0.9 [-2.6 ; +0.8] | -2.3 [-4.1 ; -0.6] | -0.73 [-1.32 ; -0.16] | ▼ |

### [9] Branch-Ma

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| jour × -signe(nuit) | NQ | 2669 | -0.5 [-4.4 ; +3.3] | -1.0 [-4.9 ; +2.8] | -0.15 [-0.71 ; +0.41] |  |
| jour × -signe(nuit) | ES | 2651 | +1.9 [-1.2 ; +4.9] | +0.9 [-2.2 ; +3.9] | +0.16 [-0.37 ; +0.71] |  |
| jour × -signe(nuit) | YM | 2655 | +2.4 [-0.5 ; +5.4] | +1.7 [-1.2 ; +4.7] | +0.34 [-0.21 ; +0.92] |  |
| jour × -signe(nuit) | GC | 2635 | -2.2 [-4.6 ; +0.3] | -3.1 [-5.5 ; -0.6] | -0.77 [-1.34 ; -0.20] | ▼ |
| jour × -signe(nuit) | 6E | 2659 | +0.1 [-0.9 ; +1.2] | -0.7 [-1.7 ; +0.4] | -0.37 [-0.99 ; +0.24] |  |
| jour × -signe(nuit) | 6B | 2642 | -0.9 [-2.2 ; +0.3] | -2.3 [-3.5 ; -1.1] | -1.10 [-1.69 ; -0.51] | ▼ |
| jour × -signe(nuit) | 6J | 2653 | -0.3 [-1.5 ; +0.9] | -1.4 [-2.6 ; -0.3] | -0.70 [-1.33 ; -0.08] | ▼ |
| jour × -signe(nuit) | 6A | 2651 | +0.5 [-0.8 ; +1.8] | -0.9 [-2.2 ; +0.4] | -0.40 [-0.95 ; +0.14] |  |
| jour × -signe(nuit), quartile extrême | NQ | 794 | +1.2 [-8.7 ; +10.0] | +0.7 [-9.1 ; +9.5] | +0.05 [-0.54 ; +0.64] |  |
| jour × -signe(nuit), quartile extrême | ES | 727 | +0.1 [-7.4 ; +8.0] | -0.8 [-8.4 ; +7.0] | -0.06 [-0.68 ; +0.51] |  |
| jour × -signe(nuit), quartile extrême | YM | 663 | -0.8 [-8.9 ; +7.0] | -1.5 [-9.6 ; +6.3] | -0.11 [-0.68 ; +0.47] |  |
| jour × -signe(nuit), quartile extrême | GC | 699 | -2.3 [-7.5 ; +2.7] | -3.0 [-8.2 ; +1.9] | -0.32 [-0.90 ; +0.27] |  |
| jour × -signe(nuit), quartile extrême | 6E | 556 | +1.3 [-1.3 ; +3.8] | +0.4 [-2.2 ; +3.0] | +0.11 [-0.51 ; +0.73] |  |
| jour × -signe(nuit), quartile extrême | 6B | 518 | -0.1 [-3.2 ; +3.3] | -1.5 [-4.6 ; +1.9] | -0.26 [-0.84 ; +0.33] |  |
| jour × -signe(nuit), quartile extrême | 6J | 587 | -1.6 [-4.7 ; +1.8] | -2.7 [-5.9 ; +0.7] | -0.55 [-1.15 ; +0.07] |  |
| jour × -signe(nuit), quartile extrême | 6A | 614 | -0.2 [-3.3 ; +2.7] | -1.7 [-4.8 ; +1.3] | -0.31 [-0.85 ; +0.25] |  |

### [10] Bahcivan-Dam-Gonenc

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| contrarian saut nuit α=1% détention 1 j | NQ | 18 | -3.7 | -4.2 | -0.04 [-0.72 ; +0.53] |  |
| contrarian saut nuit α=1% détention 1 j | ES | 19 | -13.1 | -14.1 | -0.20 [-0.78 ; +0.42] |  |
| contrarian saut nuit α=1% détention 1 j | YM | 22 | +13.0 | +12.4 | +0.17 [-0.55 ; +0.65] |  |
| contrarian saut nuit α=1% détention 1 j | GC | 12 | -3.7 | -4.5 | -0.04 [-0.76 ; +0.48] |  |
| contrarian saut nuit α=1% détention 1 j | 6E | 8 | +16.2 | +15.4 | +0.46 [-0.22 ; +0.81] |  |
| contrarian saut nuit α=1% détention 1 j | 6B | 8 | +3.7 | +2.3 | +0.05 [-0.58 ; +0.63] |  |
| contrarian saut nuit α=1% détention 1 j | 6J | 24 | +0.4 | -0.8 | -0.04 [-0.57 ; +0.54] |  |
| contrarian saut nuit α=1% détention 1 j | 6A | 2 | -42.4 | -44.0 | -0.57 [-1.47 ; +1.47] |  |
| contrarian saut nuit α=1% détention 2 j | NQ | 18 | -45.1 | -45.6 | -0.21 [-0.71 ; +0.45] |  |
| contrarian saut nuit α=1% détention 2 j | ES | 19 | -40.1 | -41.1 | -0.25 [-0.66 ; +0.48] |  |
| contrarian saut nuit α=1% détention 2 j | YM | 22 | -19.5 | -20.1 | -0.13 [-0.65 ; +0.49] |  |
| contrarian saut nuit α=1% détention 2 j | GC | 12 | +7.4 | +6.6 | +0.04 [-0.71 ; +0.54] |  |
| contrarian saut nuit α=1% détention 2 j | 6E | 8 | +24.0 | +23.2 | +0.30 [-0.42 ; +0.72] |  |
| contrarian saut nuit α=1% détention 2 j | 6B | 8 | -25.3 | -26.6 | -0.14 [-0.64 ; +0.52] |  |
| contrarian saut nuit α=1% détention 2 j | 6J | 22 | +10.9 | +9.7 | +0.14 [-0.51 ; +0.63] |  |
| contrarian saut nuit α=1% détention 2 j | 6A | 2 | -71.3 | -72.9 | -0.52 [-1.48 ; +1.46] |  |
| contrarian saut nuit α=1% détention 3 j | NQ | 18 | -57.9 | -58.4 | -0.26 [-0.83 ; +0.36] |  |
| contrarian saut nuit α=1% détention 3 j | ES | 19 | -48.0 | -49.0 | -0.27 [-0.75 ; +0.36] |  |
| contrarian saut nuit α=1% détention 3 j | YM | 22 | -25.5 | -26.2 | -0.15 [-0.70 ; +0.48] |  |
| contrarian saut nuit α=1% détention 3 j | GC | 12 | +57.2 | +56.4 | +0.25 [-0.46 ; +0.68] |  |
| contrarian saut nuit α=1% détention 3 j | 6E | 8 | -4.1 | -4.9 | -0.05 [-0.64 ; +0.49] |  |
| contrarian saut nuit α=1% détention 3 j | 6B | 8 | +8.9 | +7.5 | +0.04 [-0.53 ; +0.66] |  |
| contrarian saut nuit α=1% détention 3 j | 6J | 22 | +20.2 | +19.0 | +0.25 [-0.39 ; +0.77] |  |
| contrarian saut nuit α=1% détention 3 j | 6A | 2 | -102.9 | -104.5 | -0.71 [-1.48 ; +1.44] |  |
| contrarian saut nuit α=1% détention 4 j | NQ | 18 | -36.6 | -37.1 | -0.12 [-0.67 ; +0.51] |  |
| contrarian saut nuit α=1% détention 4 j | ES | 19 | -45.1 | -46.0 | -0.18 [-0.65 ; +0.50] |  |
| contrarian saut nuit α=1% détention 4 j | YM | 21 | +10.1 | +9.5 | +0.05 [-0.48 ; +0.72] |  |
| contrarian saut nuit α=1% détention 4 j | GC | 12 | +39.7 | +38.8 | +0.17 [-0.61 ; +0.58] |  |
| contrarian saut nuit α=1% détention 4 j | 6E | 8 | -6.3 | -7.1 | -0.07 [-0.58 ; +0.60] |  |
| contrarian saut nuit α=1% détention 4 j | 6B | 8 | -5.4 | -6.8 | -0.04 [-0.59 ; +0.58] |  |
| contrarian saut nuit α=1% détention 4 j | 6J | 22 | +17.5 | +16.3 | +0.19 [-0.41 ; +0.79] |  |
| contrarian saut nuit α=1% détention 4 j | 6A | 2 | +59.9 | +58.3 | +1.18 [-0.85 ; +1.88] |  |
| contrarian saut nuit α=1% détention 5 j | NQ | 18 | +53.1 | +52.6 | +0.20 [-0.44 ; +0.75] |  |
| contrarian saut nuit α=1% détention 5 j | ES | 19 | +46.8 | +45.8 | +0.21 [-0.37 ; +0.82] |  |
| contrarian saut nuit α=1% détention 5 j | YM | 22 | +43.7 | +43.1 | +0.22 [-0.37 ; +0.88] |  |
| contrarian saut nuit α=1% détention 5 j | GC | 12 | +40.5 | +39.7 | +0.15 [-0.49 ; +0.64] |  |
| contrarian saut nuit α=1% détention 5 j | 6E | 8 | -3.0 | -3.8 | -0.03 [-0.62 ; +0.56] |  |
| contrarian saut nuit α=1% détention 5 j | 6B | 8 | -50.0 | -51.3 | -0.24 [-0.70 ; +0.45] |  |
| contrarian saut nuit α=1% détention 5 j | 6J | 22 | +38.9 | +37.7 | +0.34 [-0.29 ; +0.79] |  |
| contrarian saut nuit α=1% détention 5 j | 6A | 2 | +130.8 | +129.3 | +1.12 [-1.20 ; +1.81] |  |
| long après saut négatif α=1% 1 j | NQ | 10 | +2.3 | +1.8 | +0.01 [-0.65 ; +0.58] |  |
| long après saut négatif α=1% 1 j | ES | 14 | -19.8 | -20.8 | -0.28 [-0.83 ; +0.37] |  |
| long après saut négatif α=1% 1 j | YM | 15 | -4.4 | -5.0 | -0.06 [-0.83 ; +0.46] |  |
| long après saut négatif α=1% 1 j | GC | 7 | -80.8 | -81.5 | -0.72 [-1.02 ; -0.43] |  |
| long après saut négatif α=1% 1 j | 6E | 4 | +19.3 | +18.5 | +0.40 [-0.31 ; +0.76] |  |
| long après saut négatif α=1% 1 j | 6B | 6 | -8.0 | -9.4 | -0.20 [-0.67 ; +0.52] |  |
| long après saut négatif α=1% 1 j | 6J | 8 | -10.9 | -12.1 | -0.41 [-0.78 ; +0.36] |  |
| long après saut négatif α=1% 1 j | 6A | 2 | -42.4 | -44.0 | -0.57 [-1.47 ; +1.47] |  |
| short après saut positif α=1% 1 j | NQ | 8 | -11.2 | -11.7 | -0.07 [-0.74 ; +0.48] |  |
| short après saut positif α=1% 1 j | ES | 5 | +5.7 | +4.8 | +0.03 [-0.62 ; +0.61] |  |
| short après saut positif α=1% 1 j | YM | 7 | +50.3 | +49.7 | +0.36 [-0.48 ; +0.72] |  |
| short après saut positif α=1% 1 j | GC | 5 | +104.4 | +103.4 | +0.42 [-0.34 ; +0.71] |  |
| short après saut positif α=1% 1 j | 6E | 4 | +13.1 | +12.3 | +0.26 [-0.46 ; +0.61] |  |
| short après saut positif α=1% 1 j | 6B | 2 | +38.9 | +37.5 | +0.35 [+0.32 ; +0.64] |  |
| short après saut positif α=1% 1 j | 6J | 16 | +6.0 | +4.8 | +0.18 [-0.38 ; +0.77] |  |
| short après saut positif α=1% 1 j | 6A | 0 | — | — | — |  |
| contrarian saut nuit α=5% détention 1 j | NQ | 24 | -10.8 | -11.3 | -0.13 [-0.77 ; +0.45] |  |
| contrarian saut nuit α=5% détention 1 j | ES | 32 | -14.6 [-34.2 ; +7.9] | -15.6 [-35.2 ; +7.0] | -0.28 [-0.92 ; +0.31] |  |
| contrarian saut nuit α=5% détention 1 j | YM | 25 | +11.6 | +11.0 | +0.16 [-0.52 ; +0.65] |  |
| contrarian saut nuit α=5% détention 1 j | GC | 19 | -25.8 | -26.5 | -0.21 [-0.74 ; +0.43] |  |
| contrarian saut nuit α=5% détention 1 j | 6E | 11 | +14.2 | +13.4 | +0.45 [-0.17 ; +0.83] |  |
| contrarian saut nuit α=5% détention 1 j | 6B | 10 | +3.5 | +2.1 | +0.06 [-0.56 ; +0.64] |  |
| contrarian saut nuit α=5% détention 1 j | 6J | 28 | +0.5 | -0.6 | -0.03 [-0.58 ; +0.60] |  |
| contrarian saut nuit α=5% détention 1 j | 6A | 5 | -18.5 | -20.0 | -0.25 [-0.60 ; +0.49] |  |
| contrarian saut nuit α=5% détention 2 j | NQ | 23 | -20.2 | -20.7 | -0.12 [-0.63 ; +0.55] |  |
| contrarian saut nuit α=5% détention 2 j | ES | 32 | -21.9 [-81.3 ; +32.3] | -22.9 [-82.2 ; +31.4] | -0.21 [-0.67 ; +0.48] |  |
| contrarian saut nuit α=5% détention 2 j | YM | 25 | -23.7 | -24.4 | -0.18 [-0.70 ; +0.42] |  |
| contrarian saut nuit α=5% détention 2 j | GC | 19 | -70.3 | -71.1 | -0.38 [-0.83 ; +0.24] |  |
| contrarian saut nuit α=5% détention 2 j | 6E | 11 | +18.1 | +17.2 | +0.27 [-0.45 ; +0.72] |  |
| contrarian saut nuit α=5% détention 2 j | 6B | 10 | -11.3 | -12.7 | -0.09 [-0.58 ; +0.61] |  |
| contrarian saut nuit α=5% détention 2 j | 6J | 26 | +6.1 | +4.9 | +0.08 [-0.58 ; +0.59] |  |
| contrarian saut nuit α=5% détention 2 j | 6A | 5 | -15.0 | -16.5 | -0.11 [-0.52 ; +0.68] |  |
| contrarian saut nuit α=5% détention 3 j | NQ | 23 | -28.7 | -29.3 | -0.16 [-0.72 ; +0.46] |  |
| contrarian saut nuit α=5% détention 3 j | ES | 32 | -44.1 [-81.2 ; -7.6] | -45.1 [-82.2 ; -8.6] | -0.36 [-0.86 ; +0.28] | ▼ |
| contrarian saut nuit α=5% détention 3 j | YM | 25 | -25.8 | -26.5 | -0.18 [-0.73 ; +0.44] |  |
| contrarian saut nuit α=5% détention 3 j | GC | 19 | -21.8 | -22.6 | -0.13 [-0.77 ; +0.47] |  |
| contrarian saut nuit α=5% détention 3 j | 6E | 11 | -0.2 | -1.0 | -0.01 [-0.67 ; +0.54] |  |
| contrarian saut nuit α=5% détention 3 j | 6B | 10 | +15.5 | +14.1 | +0.09 [-0.50 ; +0.77] |  |
| contrarian saut nuit α=5% détention 3 j | 6J | 26 | +21.4 | +20.2 | +0.29 [-0.34 ; +0.81] |  |
| contrarian saut nuit α=5% détention 3 j | 6A | 5 | -33.3 | -34.8 | -0.22 [-0.59 ; +0.62] |  |
| contrarian saut nuit α=5% détention 4 j | NQ | 23 | +3.8 | +3.2 | +0.01 [-0.54 ; +0.67] |  |
| contrarian saut nuit α=5% détention 4 j | ES | 32 | -45.9 [-101.9 ; +7.9] | -46.9 [-102.8 ; +6.9] | -0.27 [-0.76 ; +0.38] |  |
| contrarian saut nuit α=5% détention 4 j | YM | 24 | +0.3 | -0.4 | -0.00 [-0.53 ; +0.63] |  |
| contrarian saut nuit α=5% détention 4 j | GC | 19 | -34.3 | -35.1 | -0.20 [-0.86 ; +0.38] |  |
| contrarian saut nuit α=5% détention 4 j | 6E | 11 | +3.9 | +3.1 | +0.03 [-0.59 ; +0.59] |  |
| contrarian saut nuit α=5% détention 4 j | 6B | 10 | +14.1 | +12.7 | +0.08 [-0.48 ; +0.69] |  |
| contrarian saut nuit α=5% détention 4 j | 6J | 26 | +19.6 | +18.4 | +0.24 [-0.35 ; +0.80] |  |
| contrarian saut nuit α=5% détention 4 j | 6A | 5 | +38.2 | +36.7 | +0.53 [-0.17 ; +0.81] |  |
| contrarian saut nuit α=5% détention 5 j | NQ | 23 | +76.0 | +75.4 | +0.35 [-0.28 ; +0.88] |  |
| contrarian saut nuit α=5% détention 5 j | ES | 32 | +3.4 [-61.7 ; +61.2] | +2.5 [-62.6 ; +60.2] | +0.02 [-0.56 ; +0.64] |  |
| contrarian saut nuit α=5% détention 5 j | YM | 25 | +31.3 | +30.6 | +0.18 [-0.41 ; +0.83] |  |
| contrarian saut nuit α=5% détention 5 j | GC | 19 | -10.3 | -11.0 | -0.06 [-0.65 ; +0.55] |  |
| contrarian saut nuit α=5% détention 5 j | 6E | 11 | +12.9 | +12.1 | +0.11 [-0.57 ; +0.63] |  |
| contrarian saut nuit α=5% détention 5 j | 6B | 10 | -22.6 | -24.0 | -0.14 [-0.64 ; +0.55] |  |
| contrarian saut nuit α=5% détention 5 j | 6J | 26 | +41.4 | +40.2 | +0.42 [-0.19 ; +0.87] |  |
| contrarian saut nuit α=5% détention 5 j | 6A | 5 | +59.9 | +58.4 | +0.43 [-0.28 ; +0.76] |  |
| long après saut négatif α=5% 1 j | NQ | 16 | -10.6 | -11.1 | -0.12 [-0.74 ; +0.48] |  |
| long après saut négatif α=5% 1 j | ES | 22 | -29.0 | -29.9 | -0.50 [-0.97 ; +0.10] |  |
| long après saut négatif α=5% 1 j | YM | 15 | -4.4 | -5.0 | -0.06 [-0.83 ; +0.46] |  |
| long après saut négatif α=5% 1 j | GC | 14 | -72.3 | -72.9 | -0.52 [-0.90 ; +0.03] |  |
| long après saut négatif α=5% 1 j | 6E | 6 | +20.0 | +19.2 | +0.45 [-0.16 ; +0.81] |  |
| long après saut négatif α=5% 1 j | 6B | 7 | -4.7 | -6.1 | -0.15 [-0.62 ; +0.58] |  |
| long après saut négatif α=5% 1 j | 6J | 9 | -8.3 | -9.6 | -0.36 [-0.74 ; +0.45] |  |
| long après saut négatif α=5% 1 j | 6A | 5 | -18.5 | -20.0 | -0.25 [-0.60 ; +0.49] |  |
| short après saut positif α=5% 1 j | NQ | 8 | -11.2 | -11.7 | -0.07 [-0.74 ; +0.48] |  |
| short après saut positif α=5% 1 j | ES | 10 | +17.1 | +16.1 | +0.13 [-0.63 ; +0.61] |  |
| short après saut positif α=5% 1 j | YM | 10 | +35.6 | +35.0 | +0.33 [-0.40 ; +0.74] |  |
| short après saut positif α=5% 1 j | GC | 5 | +104.4 | +103.4 | +0.42 [-0.34 ; +0.71] |  |
| short après saut positif α=5% 1 j | 6E | 5 | +7.2 | +6.4 | +0.16 [-0.64 ; +0.57] |  |
| short après saut positif α=5% 1 j | 6B | 3 | +22.7 | +21.3 | +0.29 [-0.45 ; +0.58] |  |
| short après saut positif α=5% 1 j | 6J | 19 | +4.7 | +3.6 | +0.14 [-0.40 ; +0.76] |  |
| short après saut positif α=5% 1 j | 6A | 0 | — | — | — |  |

### [11] Bahcivan

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| tri nuit : nuit × signe(nuit m-1), tous mois | NQ | 2655 | +3.0 [-0.1 ; +5.9] | +2.5 [-0.6 ; +5.4] | +0.50 [-0.06 ; +1.06] |  |
| tri nuit : nuit × signe(nuit m-1), tous mois | ES | 2654 | +3.1 [+0.9 ; +5.2] | +2.1 [-0.1 ; +4.2] | +0.51 [-0.09 ; +1.11] |  |
| tri nuit : nuit × signe(nuit m-1), tous mois | YM | 2652 | +2.5 [+0.1 ; +4.7] | +1.8 [-0.6 ; +4.1] | +0.45 [-0.17 ; +1.04] |  |
| tri nuit : nuit × signe(nuit m-1), tous mois | GC | 2641 | +2.4 [-0.5 ; +5.3] | +1.5 [-1.3 ; +4.4] | +0.30 [-0.23 ; +0.87] |  |
| tri nuit : nuit × signe(nuit m-1), tous mois | 6E | 2658 | +0.1 [-1.3 ; +1.6] | -0.7 [-2.1 ; +0.8] | -0.29 [-0.88 ; +0.33] |  |
| tri nuit : nuit × signe(nuit m-1), tous mois | 6B | 2658 | -0.3 [-2.0 ; +1.4] | -1.7 [-3.4 ; -0.0] | -0.58 [-1.17 ; -0.00] | ▼ |
| tri nuit : nuit × signe(nuit m-1), tous mois | 6J | 2659 | +0.4 [-1.5 ; +2.3] | -0.7 [-2.6 ; +1.2] | -0.23 [-0.83 ; +0.39] |  |
| tri nuit : nuit × signe(nuit m-1), tous mois | 6A | 2655 | -0.8 [-2.6 ; +1.1] | -2.2 [-4.0 ; -0.4] | -0.70 [-1.27 ; -0.12] | ▼ |
| tri nuit : jour × -signe(nuit m-1), tous mois | NQ | 2655 | +3.0 [-1.3 ; +7.2] | +2.4 [-1.8 ; +6.7] | +0.35 [-0.20 ; +0.90] |  |
| tri nuit : jour × -signe(nuit m-1), tous mois | ES | 2654 | +0.5 [-2.4 ; +3.7] | -0.5 [-3.4 ; +2.8] | -0.09 [-0.68 ; +0.46] |  |
| tri nuit : jour × -signe(nuit m-1), tous mois | YM | 2651 | +1.9 [-1.1 ; +4.8] | +1.2 [-1.8 ; +4.1] | +0.24 [-0.28 ; +0.75] |  |
| tri nuit : jour × -signe(nuit m-1), tous mois | GC | 2641 | +1.0 [-1.5 ; +3.3] | +0.1 [-2.3 ; +2.5] | +0.02 [-0.53 ; +0.59] |  |
| tri nuit : jour × -signe(nuit m-1), tous mois | 6E | 2658 | +0.2 [-0.8 ; +1.3] | -0.6 [-1.6 ; +0.5] | -0.32 [-0.92 ; +0.31] |  |
| tri nuit : jour × -signe(nuit m-1), tous mois | 6B | 2658 | +1.2 [+0.0 ; +2.4] | -0.2 [-1.3 ; +1.1] | -0.08 [-0.68 ; +0.51] |  |
| tri nuit : jour × -signe(nuit m-1), tous mois | 6J | 2659 | +0.3 [-0.9 ; +1.5] | -0.8 [-2.1 ; +0.4] | -0.40 [-1.01 ; +0.22] |  |
| tri nuit : jour × -signe(nuit m-1), tous mois | 6A | 2656 | +0.6 [-0.8 ; +1.9] | -0.9 [-2.2 ; +0.5] | -0.37 [-0.95 ; +0.25] |  |
| tri jour : nuit × -signe(jour m-1), tous mois | NQ | 2655 | -2.6 [-5.6 ; +0.4] | -3.1 [-6.1 ; -0.2] | -0.63 [-1.20 ; -0.05] | ▼ |
| tri jour : nuit × -signe(jour m-1), tous mois | ES | 2654 | -0.7 [-2.9 ; +1.4] | -1.7 [-3.9 ; +0.4] | -0.44 [-1.02 ; +0.15] |  |
| tri jour : nuit × -signe(jour m-1), tous mois | YM | 2652 | -0.0 [-2.3 ; +2.2] | -0.7 [-2.9 ; +1.5] | -0.19 [-0.79 ; +0.39] |  |
| tri jour : nuit × -signe(jour m-1), tous mois | GC | 2641 | +0.3 [-2.6 ; +3.3] | -0.6 [-3.4 ; +2.4] | -0.11 [-0.69 ; +0.44] |  |
| tri jour : nuit × -signe(jour m-1), tous mois | 6E | 2658 | -0.9 [-2.2 ; +0.6] | -1.7 [-3.0 ; -0.2] | -0.72 [-1.31 ; -0.10] | ▼ |
| tri jour : nuit × -signe(jour m-1), tous mois | 6B | 2658 | -1.0 [-2.9 ; +0.7] | -2.4 [-4.2 ; -0.7] | -0.81 [-1.37 ; -0.24] | ▼ |
| tri jour : nuit × -signe(jour m-1), tous mois | 6J | 2659 | +1.0 [-0.9 ; +2.9] | -0.1 [-2.0 ; +1.7] | -0.04 [-0.65 ; +0.58] |  |
| tri jour : nuit × -signe(jour m-1), tous mois | 6A | 2655 | -0.2 [-2.0 ; +1.7] | -1.7 [-3.4 ; +0.2] | -0.52 [-1.08 ; +0.05] |  |
| tri jour : jour × signe(jour m-1), tous mois | NQ | 2655 | -0.9 [-5.3 ; +3.3] | -1.4 [-5.8 ; +2.8] | -0.20 [-0.73 ; +0.33] |  |
| tri jour : jour × signe(jour m-1), tous mois | ES | 2654 | -2.4 [-5.7 ; +0.9] | -3.4 [-6.7 ; -0.2] | -0.65 [-1.19 ; -0.13] | ▼ |
| tri jour : jour × signe(jour m-1), tous mois | YM | 2651 | -2.1 [-5.0 ; +1.2] | -2.7 [-5.7 ; +0.5] | -0.55 [-1.09 ; -0.02] |  |
| tri jour : jour × signe(jour m-1), tous mois | GC | 2641 | +0.9 [-1.7 ; +3.4] | +0.0 [-2.5 ; +2.6] | +0.00 [-0.54 ; +0.55] |  |
| tri jour : jour × signe(jour m-1), tous mois | 6E | 2658 | +0.7 [-0.3 ; +1.8] | -0.1 [-1.1 ; +1.0] | -0.07 [-0.66 ; +0.54] |  |
| tri jour : jour × signe(jour m-1), tous mois | 6B | 2658 | +0.2 [-1.1 ; +1.5] | -1.2 [-2.5 ; +0.1] | -0.59 [-1.21 ; +0.05] |  |
| tri jour : jour × signe(jour m-1), tous mois | 6J | 2659 | +0.3 [-0.9 ; +1.5] | -0.8 [-2.0 ; +0.4] | -0.42 [-1.10 ; +0.19] |  |
| tri jour : jour × signe(jour m-1), tous mois | 6A | 2656 | -0.9 [-2.2 ; +0.4] | -2.3 [-3.7 ; -1.1] | -0.98 [-1.59 ; -0.37] | ▼ |
| tri nuit : nuit × signe(nuit m-1), mois avec saut | NQ | 372 | -5.2 [-15.7 ; +4.6] | -5.7 [-16.2 ; +4.1] | -0.37 [-0.94 ; +0.19] |  |
| tri nuit : nuit × signe(nuit m-1), mois avec saut | ES | 391 | +1.0 [-5.7 ; +7.8] | +0.0 [-6.6 ; +6.9] | +0.00 [-0.64 ; +0.58] |  |
| tri nuit : nuit × signe(nuit m-1), mois avec saut | YM | 452 | -1.0 [-6.5 ; +4.5] | -1.7 [-7.1 ; +3.9] | -0.18 [-0.74 ; +0.37] |  |
| tri nuit : nuit × signe(nuit m-1), mois avec saut | GC | 249 | -0.7 [-11.2 ; +11.1] | -1.5 [-12.2 ; +10.3] | -0.08 [-0.67 ; +0.50] |  |
| tri nuit : nuit × signe(nuit m-1), mois avec saut | 6E | 165 | -0.7 [-6.2 ; +4.7] | -1.5 [-7.0 ; +3.9] | -0.14 [-0.78 ; +0.42] |  |
| tri nuit : nuit × signe(nuit m-1), mois avec saut | 6B | 169 | +1.0 [-4.9 ; +6.8] | -0.4 [-6.3 ; +5.4] | -0.03 [-0.58 ; +0.52] |  |
| tri nuit : nuit × signe(nuit m-1), mois avec saut | 6J | 413 | -0.0 [-3.9 ; +3.9] | -1.2 [-5.1 ; +2.7] | -0.15 [-0.68 ; +0.35] |  |
| tri nuit : nuit × signe(nuit m-1), mois avec saut | 6A | 40 | +3.9 [-7.3 ; +15.7] | +2.3 [-8.8 ; +14.1] | +0.29 [-0.87 ; +1.36] |  |
| tri nuit : jour × -signe(nuit m-1), mois avec saut | NQ | 372 | +9.7 [+0.2 ; +19.6] | +9.2 [-0.3 ; +19.1] | +0.50 [+0.04 ; +0.97] |  |
| tri nuit : jour × -signe(nuit m-1), mois avec saut | ES | 391 | +6.1 [-0.2 ; +12.6] | +5.2 [-1.2 ; +11.7] | +0.35 [-0.12 ; +0.83] |  |
| tri nuit : jour × -signe(nuit m-1), mois avec saut | YM | 451 | +1.5 [-5.4 ; +8.6] | +0.9 [-6.0 ; +7.9] | +0.07 [-0.41 ; +0.55] |  |
| tri nuit : jour × -signe(nuit m-1), mois avec saut | GC | 249 | -6.2 [-13.7 ; +1.3] | -7.0 [-14.6 ; +0.4] | -0.47 [-1.06 ; +0.02] |  |
| tri nuit : jour × -signe(nuit m-1), mois avec saut | 6E | 165 | -0.8 [-4.9 ; +4.1] | -1.6 [-5.7 ; +3.3] | -0.19 [-0.86 ; +0.48] |  |
| tri nuit : jour × -signe(nuit m-1), mois avec saut | 6B | 169 | +0.6 [-5.0 ; +5.8] | -0.8 [-6.4 ; +4.4] | -0.09 [-0.75 ; +0.57] |  |
| tri nuit : jour × -signe(nuit m-1), mois avec saut | 6J | 413 | +1.1 [-2.2 ; +4.2] | -0.1 [-3.4 ; +3.0] | -0.02 [-0.61 ; +0.64] |  |
| tri nuit : jour × -signe(nuit m-1), mois avec saut | 6A | 40 | +2.6 [-9.1 ; +12.1] | +1.1 [-10.7 ; +10.6] | +0.18 [-1.27 ; +1.69] |  |
| tri jour : nuit × -signe(jour m-1), mois avec saut | NQ | 372 | -4.5 [-15.8 ; +7.9] | -5.0 [-16.3 ; +7.4] | -0.33 [-0.93 ; +0.26] |  |
| tri jour : nuit × -signe(jour m-1), mois avec saut | ES | 391 | -2.2 [-8.9 ; +4.9] | -3.1 [-9.8 ; +4.0] | -0.26 [-0.89 ; +0.31] |  |
| tri jour : nuit × -signe(jour m-1), mois avec saut | YM | 452 | -0.6 [-5.6 ; +4.7] | -1.3 [-6.2 ; +4.1] | -0.14 [-0.77 ; +0.42] |  |
| tri jour : nuit × -signe(jour m-1), mois avec saut | GC | 249 | +11.4 [+0.5 ; +22.9] | +10.6 [-0.4 ; +22.1] | +0.56 [+0.06 ; +1.12] |  |
| tri jour : nuit × -signe(jour m-1), mois avec saut | 6E | 165 | +0.6 [-5.8 ; +7.5] | -0.2 [-6.6 ; +6.7] | -0.02 [-0.61 ; +0.55] |  |
| tri jour : nuit × -signe(jour m-1), mois avec saut | 6B | 169 | +4.3 [-1.8 ; +10.3] | +2.9 [-3.2 ; +8.9] | +0.28 [-0.26 ; +0.83] |  |
| tri jour : nuit × -signe(jour m-1), mois avec saut | 6J | 413 | +0.1 [-4.0 ; +4.1] | -1.0 [-5.2 ; +3.0] | -0.13 [-0.63 ; +0.39] |  |
| tri jour : nuit × -signe(jour m-1), mois avec saut | 6A | 40 | +1.1 [-10.4 ; +14.3] | -0.5 [-12.0 ; +12.8] | -0.06 [-1.25 ; +1.04] |  |
| tri jour : jour × signe(jour m-1), mois avec saut | NQ | 372 | +2.1 [-9.5 ; +12.8] | +1.6 [-10.0 ; +12.3] | +0.09 [-0.43 ; +0.63] |  |
| tri jour : jour × signe(jour m-1), mois avec saut | ES | 391 | -6.0 [-16.3 ; +2.8] | -6.9 [-17.3 ; +1.8] | -0.47 [-0.94 ; +0.03] |  |
| tri jour : jour × signe(jour m-1), mois avec saut | YM | 451 | -4.4 [-12.2 ; +2.8] | -5.1 [-12.9 ; +2.1] | -0.41 [-0.90 ; +0.09] |  |
| tri jour : jour × signe(jour m-1), mois avec saut | GC | 249 | +6.0 [-1.5 ; +13.9] | +5.1 [-2.3 ; +13.0] | +0.34 [-0.14 ; +0.85] |  |
| tri jour : jour × signe(jour m-1), mois avec saut | 6E | 165 | +2.7 [-1.9 ; +7.1] | +1.9 [-2.7 ; +6.3] | +0.22 [-0.43 ; +0.82] |  |
| tri jour : jour × signe(jour m-1), mois avec saut | 6B | 169 | +2.5 [-3.7 ; +8.5] | +1.1 [-5.1 ; +7.1] | +0.13 [-0.51 ; +0.78] |  |
| tri jour : jour × signe(jour m-1), mois avec saut | 6J | 413 | +1.2 [-1.7 ; +3.9] | +0.0 [-2.8 ; +2.8] | +0.00 [-0.60 ; +0.61] |  |
| tri jour : jour × signe(jour m-1), mois avec saut | 6A | 40 | -0.8 [-9.9 ; +7.3] | -2.4 [-11.4 ; +5.7] | -0.40 [-1.98 ; +1.10] |  |
| tri nuit : nuit × signe(nuit m-1), mois sans saut | NQ | 2283 | +4.3 [+1.6 ; +7.2] | +3.8 [+1.1 ; +6.7] | +0.72 [+0.16 ; +1.28] | ▲ |
| tri nuit : nuit × signe(nuit m-1), mois sans saut | ES | 2263 | +3.4 [+1.0 ; +5.9] | +2.4 [-0.0 ; +4.9] | +0.57 [-0.03 ; +1.15] |  |
| tri nuit : nuit × signe(nuit m-1), mois sans saut | YM | 2200 | +3.2 [+0.6 ; +5.7] | +2.5 [-0.1 ; +5.0] | +0.58 [-0.07 ; +1.18] |  |
| tri nuit : nuit × signe(nuit m-1), mois sans saut | GC | 2392 | +2.7 [-0.3 ; +5.8] | +1.9 [-1.2 ; +4.9] | +0.35 [-0.16 ; +0.92] |  |
| tri nuit : nuit × signe(nuit m-1), mois sans saut | 6E | 2493 | +0.2 [-1.3 ; +1.7] | -0.6 [-2.1 ; +0.9] | -0.26 [-0.88 ; +0.38] |  |
| tri nuit : nuit × signe(nuit m-1), mois sans saut | 6B | 2489 | -0.4 [-2.2 ; +1.3] | -1.8 [-3.6 ; -0.0] | -0.59 [-1.15 ; -0.01] | ▼ |
| tri nuit : nuit × signe(nuit m-1), mois sans saut | 6J | 2246 | +0.5 [-1.6 ; +2.5] | -0.6 [-2.8 ; +1.4] | -0.19 [-0.81 ; +0.45] |  |
| tri nuit : nuit × signe(nuit m-1), mois sans saut | 6A | 2615 | -0.9 [-2.7 ; +0.9] | -2.3 [-4.1 ; -0.5] | -0.71 [-1.30 ; -0.14] | ▼ |
| tri nuit : jour × -signe(nuit m-1), mois sans saut | NQ | 2283 | +1.9 [-2.6 ; +6.5] | +1.3 [-3.2 ; +6.0] | +0.18 [-0.36 ; +0.72] |  |
| tri nuit : jour × -signe(nuit m-1), mois sans saut | ES | 2263 | -0.5 [-3.9 ; +3.1] | -1.5 [-4.9 ; +2.1] | -0.26 [-0.84 ; +0.30] |  |
| tri nuit : jour × -signe(nuit m-1), mois sans saut | YM | 2200 | +1.9 [-1.3 ; +5.2] | +1.2 [-1.9 ; +4.5] | +0.23 [-0.32 ; +0.78] |  |
| tri nuit : jour × -signe(nuit m-1), mois sans saut | GC | 2392 | +1.7 [-0.6 ; +4.2] | +0.8 [-1.5 ; +3.3] | +0.20 [-0.33 ; +0.76] |  |
| tri nuit : jour × -signe(nuit m-1), mois sans saut | 6E | 2493 | +0.3 [-0.8 ; +1.3] | -0.5 [-1.6 ; +0.5] | -0.28 [-0.87 ; +0.34] |  |
| tri nuit : jour × -signe(nuit m-1), mois sans saut | 6B | 2489 | +1.3 [+0.0 ; +2.5] | -0.1 [-1.4 ; +1.1] | -0.06 [-0.68 ; +0.54] |  |
| tri nuit : jour × -signe(nuit m-1), mois sans saut | 6J | 2246 | +0.2 [-1.1 ; +1.6] | -0.9 [-2.2 ; +0.5] | -0.43 [-1.04 ; +0.20] |  |
| tri nuit : jour × -signe(nuit m-1), mois sans saut | 6A | 2616 | +0.5 [-0.8 ; +1.9] | -0.9 [-2.3 ; +0.5] | -0.38 [-0.98 ; +0.23] |  |
| tri jour : nuit × -signe(jour m-1), mois sans saut | NQ | 2283 | -2.3 [-5.2 ; +0.5] | -2.8 [-5.7 ; -0.1] | -0.54 [-1.11 ; +0.06] | ▼ |
| tri jour : nuit × -signe(jour m-1), mois sans saut | ES | 2263 | -0.5 [-2.8 ; +1.8] | -1.5 [-3.8 ; +0.8] | -0.36 [-0.96 ; +0.23] |  |
| tri jour : nuit × -signe(jour m-1), mois sans saut | YM | 2200 | +0.1 [-2.4 ; +2.6] | -0.6 [-3.1 ; +1.9] | -0.14 [-0.73 ; +0.47] |  |
| tri jour : nuit × -signe(jour m-1), mois sans saut | GC | 2392 | -0.9 [-3.9 ; +2.2] | -1.7 [-4.8 ; +1.3] | -0.33 [-0.91 ; +0.24] |  |
| tri jour : nuit × -signe(jour m-1), mois sans saut | 6E | 2493 | -1.0 [-2.5 ; +0.5] | -1.8 [-3.3 ; -0.3] | -0.75 [-1.33 ; -0.13] | ▼ |
| tri jour : nuit × -signe(jour m-1), mois sans saut | 6B | 2489 | -1.4 [-3.2 ; +0.2] | -2.8 [-4.6 ; -1.2] | -0.90 [-1.44 ; -0.33] | ▼ |
| tri jour : nuit × -signe(jour m-1), mois sans saut | 6J | 2246 | +1.2 [-0.9 ; +3.3] | +0.0 [-2.0 ; +2.1] | +0.01 [-0.61 ; +0.65] |  |
| tri jour : nuit × -signe(jour m-1), mois sans saut | 6A | 2615 | -0.3 [-2.0 ; +1.6] | -1.7 [-3.4 ; +0.1] | -0.52 [-1.08 ; +0.05] |  |
| tri jour : jour × signe(jour m-1), mois sans saut | NQ | 2283 | -1.4 [-5.9 ; +3.1] | -1.9 [-6.4 ; +2.5] | -0.25 [-0.80 ; +0.31] |  |
| tri jour : jour × signe(jour m-1), mois sans saut | ES | 2263 | -1.8 [-5.3 ; +1.4] | -2.8 [-6.3 ; +0.4] | -0.51 [-1.06 ; +0.04] |  |
| tri jour : jour × signe(jour m-1), mois sans saut | YM | 2200 | -1.6 [-5.1 ; +1.8] | -2.3 [-5.8 ; +1.1] | -0.42 [-0.93 ; +0.14] |  |
| tri jour : jour × signe(jour m-1), mois sans saut | GC | 2392 | +0.3 [-2.2 ; +2.7] | -0.5 [-3.1 ; +1.8] | -0.12 [-0.68 ; +0.42] |  |
| tri jour : jour × signe(jour m-1), mois sans saut | 6E | 2493 | +0.5 [-0.5 ; +1.7] | -0.3 [-1.3 ; +0.9] | -0.14 [-0.72 ; +0.43] |  |
| tri jour : jour × signe(jour m-1), mois sans saut | 6B | 2489 | +0.0 [-1.3 ; +1.3] | -1.4 [-2.7 ; -0.1] | -0.64 [-1.25 ; -0.04] | ▼ |
| tri jour : jour × signe(jour m-1), mois sans saut | 6J | 2246 | +0.1 [-1.1 ; +1.4] | -1.0 [-2.2 ; +0.3] | -0.46 [-1.13 ; +0.18] |  |
| tri jour : jour × signe(jour m-1), mois sans saut | 6A | 2616 | -0.9 [-2.3 ; +0.4] | -2.3 [-3.7 ; -1.0] | -0.97 [-1.58 ; -0.37] | ▼ |

### [14] Donninger

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| long 16:00→9:30 | NQ | 2650 | +4.9 [+2.3 ; +7.8] | +4.4 [+1.7 ; +7.2] | +0.87 [+0.32 ; +1.43] | ▲ |
| long 16:00→9:30 | ES | 2649 | +3.6 [+1.5 ; +5.8] | +2.6 [+0.5 ; +4.8] | +0.64 [+0.07 ; +1.23] | ▲ |
| long 16:00→9:30 | YM | 2647 | +3.4 [+1.3 ; +5.5] | +2.7 [+0.6 ; +4.8] | +0.68 [+0.09 ; +1.27] | ▲ |
| long 16:00→9:30 | GC | 2642 | +4.9 [+2.0 ; +7.6] | +4.0 [+1.2 ; +6.7] | +0.78 [+0.25 ; +1.30] | ▲ |
| long 16:00→9:30 | 6E | 2659 | -0.6 [-2.0 ; +0.7] | -1.4 [-2.8 ; -0.1] | -0.61 [-1.20 ; -0.01] | ▼ |
| long 16:00→9:30 | 6B | 2659 | -1.3 [-2.9 ; +0.3] | -2.7 [-4.3 ; -1.1] | -0.91 [-1.42 ; -0.36] | ▼ |
| long 16:00→9:30 | 6J | 2660 | -1.2 [-3.1 ; +0.6] | -2.4 [-4.2 ; -0.5] | -0.77 [-1.38 ; -0.13] | ▼ |
| long 16:00→9:30 | 6A | 2656 | -0.1 [-1.9 ; +1.7] | -1.5 [-3.3 ; +0.3] | -0.47 [-1.02 ; +0.07] |  |
| long 16:00→9:30 (9:33 si gain) | NQ | 2655 | +4.1 [+1.3 ; +6.9] | +3.6 [+0.7 ; +6.4] | +0.67 [+0.12 ; +1.29] | ▲ |
| long 16:00→9:30 (9:33 si gain) | ES | 2655 | +3.1 [+0.5 ; +5.4] | +2.1 [-0.5 ; +4.4] | +0.46 [-0.11 ; +1.09] |  |
| long 16:00→9:30 (9:33 si gain) | YM | 2653 | +3.3 [+0.9 ; +5.6] | +2.6 [+0.2 ; +4.9] | +0.59 [+0.00 ; +1.23] | ▲ |
| long 16:00→9:30 (9:33 si gain) | GC | 2643 | +4.8 [+2.1 ; +7.5] | +3.9 [+1.3 ; +6.6] | +0.77 [+0.25 ; +1.32] | ▲ |
| long 16:00→9:30 (9:33 si gain) | 6E | 2659 | -0.6 [-1.9 ; +0.8] | -1.4 [-2.7 ; +0.0] | -0.58 [-1.18 ; +0.02] |  |
| long 16:00→9:30 (9:33 si gain) | 6B | 2659 | -1.2 [-2.8 ; +0.4] | -2.6 [-4.2 ; -1.0] | -0.87 [-1.38 ; -0.31] | ▼ |
| long 16:00→9:30 (9:33 si gain) | 6J | 2660 | -1.1 [-3.0 ; +0.7] | -2.3 [-4.1 ; -0.4] | -0.73 [-1.35 ; -0.10] | ▼ |
| long 16:00→9:30 (9:33 si gain) | 6A | 2657 | -0.0 [-1.8 ; +1.8] | -1.4 [-3.2 ; +0.3] | -0.44 [-1.01 ; +0.10] |  |
| idem sans entrée le vendredi | NQ | 2128 | +4.8 [+1.8 ; +8.0] | +4.3 [+1.2 ; +7.4] | +0.75 [+0.25 ; +1.31] | ▲ |
| idem sans entrée le vendredi | ES | 2128 | +3.4 [+0.8 ; +6.0] | +2.4 [-0.2 ; +5.0] | +0.51 [+0.03 ; +1.04] |  |
| idem sans entrée le vendredi | YM | 2126 | +3.6 [+1.2 ; +6.3] | +3.0 [+0.5 ; +5.6] | +0.63 [+0.15 ; +1.16] | ▲ |
| idem sans entrée le vendredi | GC | 2119 | +5.6 [+2.0 ; +8.9] | +4.7 [+1.2 ; +8.0] | +0.84 [+0.30 ; +1.38] | ▲ |
| idem sans entrée le vendredi | 6E | 2134 | -0.5 [-2.0 ; +1.0] | -1.3 [-2.8 ; +0.2] | -0.52 [-1.10 ; +0.09] |  |
| idem sans entrée le vendredi | 6B | 2134 | -1.4 [-3.1 ; +0.4] | -2.8 [-4.5 ; -1.0] | -0.84 [-1.38 ; -0.27] | ▼ |
| idem sans entrée le vendredi | 6J | 2134 | -0.1 [-2.1 ; +2.0] | -1.2 [-3.2 ; +0.8] | -0.36 [-0.99 ; +0.28] |  |
| idem sans entrée le vendredi | 6A | 2134 | -0.6 [-2.7 ; +1.4] | -2.0 [-4.2 ; -0.0] | -0.55 [-1.13 ; +0.00] | ▼ |

### [15] Vojtko-Hanicová

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| nuit sans filtre | NQ | 2672 | +4.9 [+2.1 ; +7.6] | +4.4 [+1.6 ; +7.1] | +0.88 [+0.32 ; +1.44] | ▲ |
| nuit sans filtre | ES | 2671 | +3.5 [+1.3 ; +5.7] | +2.5 [+0.3 ; +4.7] | +0.63 [+0.05 ; +1.22] | ▲ |
| nuit sans filtre | YM | 2669 | +3.3 [+1.1 ; +5.5] | +2.6 [+0.4 ; +4.8] | +0.66 [+0.07 ; +1.25] | ▲ |
| nuit sans filtre | GC | 2658 | +5.0 [+2.4 ; +7.9] | +4.2 [+1.5 ; +7.0] | +0.82 [+0.30 ; +1.35] | ▲ |
| nuit sans filtre | 6E | 2675 | -0.6 [-2.0 ; +0.7] | -1.4 [-2.8 ; -0.1] | -0.61 [-1.21 ; +0.01] | ▼ |
| nuit sans filtre | 6B | 2675 | -1.4 [-3.1 ; +0.3] | -2.7 [-4.5 ; -1.0] | -0.92 [-1.43 ; -0.38] | ▼ |
| nuit sans filtre | 6J | 2676 | -1.2 [-3.0 ; +0.8] | -2.4 [-4.1 ; -0.3] | -0.77 [-1.38 ; -0.14] | ▼ |
| nuit sans filtre | 6A | 2672 | -0.1 [-1.9 ; +1.7] | -1.5 [-3.3 ; +0.3] | -0.48 [-1.02 ; +0.08] |  |
| nuit si close > MM10 (veille) | NQ | 1677 | +2.4 [-0.8 ; +5.5] | +1.9 [-1.3 ; +5.0] | +0.36 [-0.20 ; +0.91] |  |
| nuit si close > MM10 (veille) | ES | 1714 | +2.5 [+0.1 ; +4.9] | +1.4 [-0.9 ; +3.9] | +0.35 [-0.19 ; +0.87] |  |
| nuit si close > MM10 (veille) | YM | 1615 | +3.8 [+1.6 ; +6.3] | +3.1 [+0.9 ; +5.6] | +0.72 [+0.10 ; +1.31] | ▲ |
| nuit si close > MM10 (veille) | GC | 1377 | +5.7 [+1.7 ; +9.6] | +4.9 [+0.8 ; +8.8] | +0.70 [+0.11 ; +1.28] | ▲ |
| nuit si close > MM10 (veille) | 6E | 1263 | -0.6 [-2.7 ; +1.4] | -1.4 [-3.5 ; +0.6] | -0.40 [-1.01 ; +0.22] |  |
| nuit si close > MM10 (veille) | 6B | 1329 | -1.6 [-4.0 ; +0.7] | -3.0 [-5.4 ; -0.6] | -0.69 [-1.23 ; -0.16] | ▼ |
| nuit si close > MM10 (veille) | 6J | 1106 | -0.3 [-3.1 ; +2.7] | -1.4 [-4.2 ; +1.6] | -0.27 [-0.88 ; +0.32] |  |
| nuit si close > MM10 (veille) | 6A | 1349 | -2.1 [-4.8 ; +0.5] | -3.5 [-6.2 ; -0.9] | -0.79 [-1.35 ; -0.21] | ▼ |
| nuit si close > MM20 (veille) | NQ | 1767 | +3.7 [+0.7 ; +6.5] | +3.2 [+0.2 ; +6.0] | +0.65 [+0.09 ; +1.25] | ▲ |
| nuit si close > MM20 (veille) | ES | 1820 | +3.5 [+1.0 ; +5.9] | +2.5 [-0.0 ; +4.9] | +0.63 [+0.03 ; +1.22] |  |
| nuit si close > MM20 (veille) | YM | 1712 | +3.8 [+1.6 ; +6.1] | +3.2 [+0.9 ; +5.5] | +0.78 [+0.21 ; +1.37] | ▲ |
| nuit si close > MM20 (veille) | GC | 1276 | +2.4 [-1.6 ; +6.5] | +1.6 [-2.4 ; +5.7] | +0.21 [-0.34 ; +0.84] |  |
| nuit si close > MM20 (veille) | 6E | 1200 | -0.5 [-2.8 ; +1.8] | -1.3 [-3.6 ; +1.0] | -0.36 [-0.99 ; +0.26] |  |
| nuit si close > MM20 (veille) | 6B | 1318 | -2.3 [-4.5 ; -0.1] | -3.6 [-5.8 ; -1.5] | -0.82 [-1.35 ; -0.30] | ▼ |
| nuit si close > MM20 (veille) | 6J | 1081 | +0.5 [-2.6 ; +3.6] | -0.6 [-3.6 ; +2.5] | -0.11 [-0.70 ; +0.45] |  |
| nuit si close > MM20 (veille) | 6A | 1303 | -1.0 [-3.7 ; +1.5] | -2.4 [-5.1 ; +0.1] | -0.53 [-1.13 ; +0.01] |  |
| nuit si close > MM50 (veille) | NQ | 1862 | +4.0 [+1.1 ; +6.8] | +3.5 [+0.6 ; +6.3] | +0.73 [+0.18 ; +1.31] | ▲ |
| nuit si close > MM50 (veille) | ES | 1896 | +3.4 [+1.4 ; +5.6] | +2.4 [+0.4 ; +4.6] | +0.67 [+0.09 ; +1.23] | ▲ |
| nuit si close > MM50 (veille) | YM | 1815 | +3.0 [+0.8 ; +5.2] | +2.3 [+0.1 ; +4.5] | +0.62 [+0.03 ; +1.19] | ▲ |
| nuit si close > MM50 (veille) | GC | 1012 | +2.9 [-2.1 ; +7.9] | +2.0 [-3.0 ; +7.1] | +0.23 [-0.33 ; +0.83] |  |
| nuit si close > MM50 (veille) | 6E | 1072 | +0.6 [-1.8 ; +2.9] | -0.2 [-2.6 ; +2.1] | -0.05 [-0.70 ; +0.63] |  |
| nuit si close > MM50 (veille) | 6B | 1269 | -1.3 [-3.7 ; +1.1] | -2.6 [-5.0 ; -0.3] | -0.60 [-1.16 ; +0.00] | ▼ |
| nuit si close > MM50 (veille) | 6J | 996 | +0.4 [-2.8 ; +3.4] | -0.7 [-3.9 ; +2.4] | -0.12 [-0.73 ; +0.50] |  |
| nuit si close > MM50 (veille) | 6A | 1147 | +0.0 [-2.9 ; +3.0] | -1.4 [-4.3 ; +1.6] | -0.29 [-0.88 ; +0.25] |  |
| nuit si close > MM20 et nuit précédente < 0 | NQ | 683 | +4.3 [-0.6 ; +9.6] | +3.8 [-1.2 ; +9.1] | +0.45 [-0.13 ; +1.00] |  |
| nuit si close > MM20 et nuit précédente < 0 | ES | 719 | +4.1 [-0.9 ; +8.7] | +3.1 [-2.0 ; +7.7] | +0.46 [-0.11 ; +1.03] |  |
| nuit si close > MM20 et nuit précédente < 0 | YM | 692 | +2.9 [-1.4 ; +7.0] | +2.3 [-2.1 ; +6.4] | +0.35 [-0.23 ; +0.92] |  |
| nuit si close > MM20 et nuit précédente < 0 | GC | 465 | +3.3 [-3.0 ; +10.1] | +2.4 [-3.9 ; +9.2] | +0.21 [-0.38 ; +0.81] |  |
| nuit si close > MM20 et nuit précédente < 0 | 6E | 481 | -1.1 [-3.9 ; +1.7] | -1.9 [-4.7 ; +0.9] | -0.34 [-0.88 ; +0.24] |  |
| nuit si close > MM20 et nuit précédente < 0 | 6B | 540 | -1.9 [-5.0 ; +1.4] | -3.2 [-6.4 ; +0.0] | -0.52 [-1.12 ; +0.10] |  |
| nuit si close > MM20 et nuit précédente < 0 | 6J | 451 | +1.7 [-3.4 ; +7.2] | +0.6 [-4.5 ; +6.1] | +0.07 [-0.51 ; +0.63] |  |
| nuit si close > MM20 et nuit précédente < 0 | 6A | 487 | +1.5 [-2.5 ; +5.5] | +0.0 [-3.9 ; +4.1] | +0.01 [-0.61 ; +0.65] |  |

### [19] Aretz-Bartram

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| jour long le lundi | NQ | 497 | +13.3 [+3.7 ; +23.6] | +12.8 [+3.2 ; +23.1] | +0.89 [+0.27 ; +1.52] | ▲ |
| jour long le lundi | ES | 497 | +7.7 [+0.7 ; +15.0] | +6.7 [-0.3 ; +14.0] | +0.62 [+0.00 ; +1.22] |  |
| jour long le lundi | YM | 497 | +7.0 [-0.3 ; +14.4] | +6.4 [-1.0 ; +13.7] | +0.60 [-0.00 ; +1.20] |  |
| jour long le lundi | GC | 499 | +0.6 [-4.3 ; +5.3] | -0.3 [-5.2 ; +4.5] | -0.03 [-0.64 ; +0.55] |  |
| jour long le lundi | 6E | 499 | -0.0 [-2.0 ; +1.7] | -0.8 [-2.8 ; +0.9] | -0.24 [-0.86 ; +0.41] |  |
| jour long le lundi | 6B | 499 | +0.0 [-2.4 ; +2.3] | -1.4 [-3.8 ; +0.9] | -0.35 [-0.92 ; +0.26] |  |
| jour long le lundi | 6J | 499 | -2.5 [-4.7 ; -0.3] | -3.6 [-5.9 ; -1.4] | -0.99 [-1.57 ; -0.40] | ▼ |
| jour long le lundi | 6A | 499 | +1.0 [-1.5 ; +3.7] | -0.4 [-3.0 ; +2.3] | -0.09 [-0.68 ; +0.53] |  |
| nuit long vers lundi | NQ | 497 | +5.1 [-3.6 ; +13.3] | +4.5 [-4.1 ; +12.8] | +0.37 [-0.24 ; +1.00] |  |
| nuit long vers lundi | ES | 497 | +4.8 [-2.2 ; +11.2] | +3.8 [-3.2 ; +10.2] | +0.37 [-0.23 ; +1.00] |  |
| nuit long vers lundi | YM | 497 | +4.3 [-2.0 ; +10.5] | +3.6 [-2.7 ; +9.8] | +0.35 [-0.26 ; +0.93] |  |
| nuit long vers lundi | GC | 496 | +3.3 [-4.6 ; +11.9] | +2.4 [-5.4 ; +11.0] | +0.19 [-0.36 ; +0.74] |  |
| nuit long vers lundi | 6E | 498 | +1.0 [-1.8 ; +4.0] | +0.2 [-2.6 ; +3.2] | +0.03 [-0.61 ; +0.62] |  |
| nuit long vers lundi | 6B | 498 | +0.6 [-2.9 ; +4.2] | -0.8 [-4.3 ; +2.8] | -0.12 [-0.69 ; +0.49] |  |
| nuit long vers lundi | 6J | 499 | -4.0 [-8.6 ; +0.7] | -5.1 [-9.7 ; -0.4] | -0.70 [-1.45 ; -0.06] | ▼ |
| nuit long vers lundi | 6A | 496 | +2.0 [-1.5 ; +5.5] | +0.6 [-2.9 ; +4.1] | +0.09 [-0.51 ; +0.67] |  |
| jour long le mardi | NQ | 551 | +1.6 [-6.7 ; +9.3] | +1.1 [-7.2 ; +8.7] | +0.08 [-0.52 ; +0.66] |  |
| jour long le mardi | ES | 550 | -1.6 [-7.7 ; +4.3] | -2.6 [-8.7 ; +3.3] | -0.24 [-0.82 ; +0.37] |  |
| jour long le mardi | YM | 549 | -3.7 [-10.4 ; +2.8] | -4.4 [-11.1 ; +2.1] | -0.41 [-1.01 ; +0.20] |  |
| jour long le mardi | GC | 546 | -0.4 [-5.2 ; +4.3] | -1.3 [-6.1 ; +3.5] | -0.15 [-0.69 ; +0.46] |  |
| jour long le mardi | 6E | 551 | -0.5 [-2.5 ; +1.4] | -1.3 [-3.4 ; +0.6] | -0.37 [-0.91 ; +0.19] |  |
| jour long le mardi | 6B | 551 | +1.9 [-0.9 ; +4.6] | +0.5 [-2.3 ; +3.2] | +0.11 [-0.46 ; +0.72] |  |
| jour long le mardi | 6J | 551 | -1.4 [-3.5 ; +0.7] | -2.5 [-4.6 ; -0.4] | -0.64 [-1.18 ; -0.05] | ▼ |
| jour long le mardi | 6A | 551 | +0.6 [-2.0 ; +3.1] | -0.9 [-3.4 ; +1.7] | -0.18 [-0.77 ; +0.39] |  |
| nuit long vers mardi | NQ | 551 | +8.2 [+0.6 ; +16.5] | +7.7 [+0.1 ; +16.0] | +0.67 [+0.07 ; +1.24] | ▲ |
| nuit long vers mardi | ES | 550 | +6.2 [+0.7 ; +12.5] | +5.2 [-0.3 ; +11.5] | +0.59 [-0.01 ; +1.15] |  |
| nuit long vers mardi | YM | 550 | +6.9 [+1.2 ; +12.8] | +6.2 [+0.5 ; +12.1] | +0.70 [+0.09 ; +1.27] | ▲ |
| nuit long vers mardi | GC | 551 | +4.7 [-1.6 ; +11.2] | +3.8 [-2.5 ; +10.4] | +0.33 [-0.28 ; +0.89] |  |
| nuit long vers mardi | 6E | 550 | -0.1 [-2.9 ; +2.9] | -0.9 [-3.7 ; +2.1] | -0.18 [-0.82 ; +0.41] |  |
| nuit long vers mardi | 6B | 550 | -0.7 [-4.2 ; +2.8] | -2.1 [-5.6 ; +1.4] | -0.33 [-0.92 ; +0.27] |  |
| nuit long vers mardi | 6J | 550 | -3.1 [-6.6 ; +0.5] | -4.2 [-7.8 ; -0.6] | -0.66 [-1.31 ; -0.04] | ▼ |
| nuit long vers mardi | 6A | 550 | +0.8 [-3.5 ; +4.9] | -0.7 [-4.9 ; +3.5] | -0.09 [-0.70 ; +0.49] |  |
| jour long le mercredi | NQ | 548 | +3.9 [-4.6 ; +12.1] | +3.4 [-5.1 ; +11.6] | +0.20 [-0.36 ; +0.74] |  |
| jour long le mercredi | ES | 548 | +2.4 [-4.2 ; +8.5] | +1.4 [-5.2 ; +7.5] | +0.11 [-0.45 ; +0.63] |  |
| jour long le mercredi | YM | 548 | +1.3 [-5.2 ; +7.4] | +0.6 [-5.8 ; +6.6] | +0.05 [-0.52 ; +0.59] |  |
| jour long le mercredi | GC | 544 | +0.6 [-4.6 ; +5.7] | -0.2 [-5.5 ; +4.8] | -0.03 [-0.60 ; +0.58] |  |
| jour long le mercredi | 6E | 549 | +1.8 [-0.9 ; +4.8] | +1.0 [-1.7 ; +4.0] | +0.22 [-0.37 ; +0.85] |  |
| jour long le mercredi | 6B | 549 | +2.4 [-0.1 ; +5.1] | +1.0 [-1.5 ; +3.7] | +0.21 [-0.37 ; +0.80] |  |
| jour long le mercredi | 6J | 549 | -2.3 [-5.3 ; +0.8] | -3.4 [-6.4 ; -0.4] | -0.68 [-1.28 ; -0.06] | ▼ |
| jour long le mercredi | 6A | 549 | +2.7 [-0.7 ; +6.5] | +1.3 [-2.1 ; +5.0] | +0.21 [-0.34 ; +0.82] |  |
| nuit long vers mercredi | NQ | 548 | +9.3 [+2.9 ; +16.5] | +8.8 [+2.4 ; +16.0] | +0.86 [+0.28 ; +1.44] | ▲ |
| nuit long vers mercredi | ES | 548 | +6.2 [+0.8 ; +12.2] | +5.2 [-0.2 ; +11.2] | +0.64 [+0.05 ; +1.24] |  |
| nuit long vers mercredi | YM | 547 | +5.9 [+0.4 ; +11.9] | +5.2 [-0.3 ; +11.2] | +0.64 [+0.05 ; +1.25] |  |
| nuit long vers mercredi | GC | 542 | +6.8 [-0.0 ; +14.0] | +6.0 [-0.9 ; +13.2] | +0.57 [-0.03 ; +1.15] |  |
| nuit long vers mercredi | 6E | 549 | -1.8 [-5.0 ; +1.1] | -2.6 [-5.8 ; +0.3] | -0.53 [-1.12 ; +0.05] |  |
| nuit long vers mercredi | 6B | 549 | -0.5 [-3.5 ; +2.5] | -1.9 [-4.9 ; +1.1] | -0.32 [-0.90 ; +0.25] |  |
| nuit long vers mercredi | 6J | 549 | -2.0 [-5.8 ; +1.7] | -3.2 [-6.9 ; +0.6] | -0.51 [-1.11 ; +0.08] |  |
| nuit long vers mercredi | 6A | 549 | -0.1 [-4.5 ; +4.5] | -1.5 [-5.9 ; +3.0] | -0.21 [-0.81 ; +0.40] |  |
| jour long le jeudi | NQ | 539 | -1.0 [-10.3 ; +8.1] | -1.5 [-10.8 ; +7.6] | -0.09 [-0.70 ; +0.53] |  |
| jour long le jeudi | ES | 539 | +1.7 [-5.0 ; +8.3] | +0.7 [-6.0 ; +7.3] | +0.06 [-0.52 ; +0.68] |  |
| jour long le jeudi | YM | 538 | +4.4 [-1.6 ; +9.9] | +3.7 [-2.3 ; +9.2] | +0.33 [-0.23 ; +0.93] |  |
| jour long le jeudi | GC | 536 | +0.6 [-5.2 ; +6.6] | -0.3 [-6.1 ; +5.8] | -0.03 [-0.61 ; +0.54] |  |
| jour long le jeudi | 6E | 540 | -1.0 [-3.4 ; +1.6] | -1.8 [-4.2 ; +0.8] | -0.41 [-1.01 ; +0.16] |  |
| jour long le jeudi | 6B | 540 | -0.3 [-3.1 ; +2.8] | -1.7 [-4.5 ; +1.4] | -0.34 [-0.93 ; +0.18] |  |
| jour long le jeudi | 6J | 540 | -0.2 [-2.9 ; +2.8] | -1.3 [-4.0 ; +1.7] | -0.28 [-0.91 ; +0.29] |  |
| jour long le jeudi | 6A | 540 | -1.6 [-4.5 ; +1.5] | -3.0 [-5.9 ; +0.1] | -0.57 [-1.18 ; +0.03] |  |
| nuit long vers jeudi | NQ | 539 | +2.9 [-4.7 ; +10.4] | +2.4 [-5.2 ; +9.9] | +0.20 [-0.43 ; +0.85] |  |
| nuit long vers jeudi | ES | 539 | -0.5 [-6.6 ; +5.3] | -1.5 [-7.6 ; +4.2] | -0.17 [-0.78 ; +0.47] |  |
| nuit long vers jeudi | YM | 539 | -2.7 [-8.5 ; +2.7] | -3.4 [-9.2 ; +2.0] | -0.42 [-1.01 ; +0.20] |  |
| nuit long vers jeudi | GC | 536 | +2.6 [-4.2 ; +9.4] | +1.7 [-5.1 ; +8.5] | +0.15 [-0.44 ; +0.76] |  |
| nuit long vers jeudi | 6E | 540 | -0.2 [-3.6 ; +3.3] | -1.0 [-4.4 ; +2.6] | -0.19 [-0.82 ; +0.41] |  |
| nuit long vers jeudi | 6B | 540 | -0.1 [-4.2 ; +4.3] | -1.5 [-5.6 ; +2.9] | -0.23 [-0.80 ; +0.35] |  |
| nuit long vers jeudi | 6J | 540 | +4.0 [-0.3 ; +8.4] | +2.9 [-1.5 ; +7.3] | +0.39 [-0.22 ; +0.94] |  |
| nuit long vers jeudi | 6A | 540 | -0.8 [-4.8 ; +3.2] | -2.2 [-6.2 ; +1.8] | -0.31 [-0.89 ; +0.27] |  |
| jour long le vendredi | NQ | 537 | -1.1 [-8.6 ; +6.4] | -1.6 [-9.2 ; +5.9] | -0.10 [-0.72 ; +0.55] |  |
| jour long le vendredi | ES | 537 | +1.6 [-4.2 ; +7.1] | +0.6 [-5.2 ; +6.1] | +0.05 [-0.55 ; +0.72] |  |
| jour long le vendredi | YM | 536 | +1.6 [-4.6 ; +7.5] | +0.9 [-5.3 ; +6.8] | +0.09 [-0.52 ; +0.74] |  |
| jour long le vendredi | GC | 533 | -2.3 [-7.8 ; +3.0] | -3.2 [-8.6 ; +2.2] | -0.33 [-0.90 ; +0.29] |  |
| jour long le vendredi | 6E | 536 | +1.0 [-1.1 ; +3.3] | +0.2 [-1.9 ; +2.5] | +0.06 [-0.55 ; +0.65] |  |
| jour long le vendredi | 6B | 536 | +1.3 [-1.6 ; +4.2] | -0.1 [-3.0 ; +2.8] | -0.02 [-0.62 ; +0.58] |  |
| jour long le vendredi | 6J | 537 | +2.4 [-0.1 ; +5.0] | +1.3 [-1.3 ; +3.9] | +0.28 [-0.30 ; +0.82] |  |
| jour long le vendredi | 6A | 534 | -1.1 [-3.9 ; +1.9] | -2.5 [-5.3 ; +0.5] | -0.44 [-1.05 ; +0.18] |  |
| nuit long vers vendredi | NQ | 537 | -1.0 [-7.3 ; +5.1] | -1.5 [-7.8 ; +4.6] | -0.14 [-0.70 ; +0.48] |  |
| nuit long vers vendredi | ES | 537 | +0.8 [-4.6 ; +5.8] | -0.2 [-5.6 ; +4.8] | -0.02 [-0.60 ; +0.61] |  |
| nuit long vers vendredi | YM | 536 | +2.0 [-3.4 ; +7.0] | +1.3 [-4.1 ; +6.3] | +0.16 [-0.44 ; +0.75] |  |
| nuit long vers vendredi | GC | 533 | +7.7 [+1.8 ; +13.5] | +6.8 [+0.9 ; +12.7] | +0.60 [+0.01 ; +1.20] | ▲ |
| nuit long vers vendredi | 6E | 538 | -1.8 [-5.3 ; +2.0] | -2.6 [-6.1 ; +1.2] | -0.47 [-1.06 ; +0.13] |  |
| nuit long vers vendredi | 6B | 538 | -6.0 [-11.7 ; -0.9] | -7.4 [-13.1 ; -2.3] | -0.93 [-1.42 ; -0.44] | ▼ |
| nuit long vers vendredi | 6J | 538 | -1.2 [-5.4 ; +3.3] | -2.3 [-6.5 ; +2.2] | -0.32 [-0.93 ; +0.24] |  |
| nuit long vers vendredi | 6A | 537 | -2.3 [-6.9 ; +1.9] | -3.8 [-8.3 ; +0.5] | -0.50 [-1.09 ; +0.06] |  |
| momentum 12-1 sur le jour | NQ | 2422 | +0.3 [-4.0 ; +4.4] | -0.2 [-4.5 ; +4.0] | -0.03 [-0.59 ; +0.52] |  |
| momentum 12-1 sur le jour | ES | 2421 | -0.2 [-3.5 ; +2.8] | -1.2 [-4.4 ; +1.9] | -0.22 [-0.77 ; +0.31] |  |
| momentum 12-1 sur le jour | YM | 2418 | -0.0 [-3.0 ; +3.0] | -0.7 [-3.6 ; +2.3] | -0.14 [-0.68 ; +0.39] |  |
| momentum 12-1 sur le jour | GC | 2409 | -0.9 [-3.3 ; +1.6] | -1.7 [-4.1 ; +0.8] | -0.44 [-0.97 ; +0.14] |  |
| momentum 12-1 sur le jour | 6E | 2425 | -0.6 [-1.6 ; +0.5] | -1.4 [-2.4 ; -0.3] | -0.78 [-1.33 ; -0.23] | ▼ |
| momentum 12-1 sur le jour | 6B | 2425 | -1.7 [-2.9 ; -0.4] | -3.1 [-4.3 ; -1.8] | -1.51 [-2.13 ; -0.86] | ▼ |
| momentum 12-1 sur le jour | 6J | 2426 | +0.4 [-0.7 ; +1.6] | -0.7 [-1.9 ; +0.5] | -0.38 [-1.03 ; +0.26] |  |
| momentum 12-1 sur le jour | 6A | 2424 | +0.4 [-1.0 ; +1.7] | -1.1 [-2.4 ; +0.3] | -0.45 [-1.04 ; +0.14] |  |
| momentum 12-1 sur la nuit | NQ | 2422 | +6.2 [+3.3 ; +9.4] | +5.8 [+2.8 ; +8.9] | +1.12 [+0.56 ; +1.70] | ▲ |
| momentum 12-1 sur la nuit | ES | 2421 | +4.2 [+1.9 ; +6.6] | +3.3 [+0.9 ; +5.7] | +0.81 [+0.23 ; +1.39] | ▲ |
| momentum 12-1 sur la nuit | YM | 2419 | +3.6 [+1.2 ; +5.9] | +2.9 [+0.6 ; +5.3] | +0.74 [+0.12 ; +1.34] | ▲ |
| momentum 12-1 sur la nuit | GC | 2409 | +3.1 [+0.4 ; +6.2] | +2.3 [-0.5 ; +5.4] | +0.45 [-0.15 ; +1.04] |  |
| momentum 12-1 sur la nuit | 6E | 2425 | -0.6 [-2.0 ; +0.9] | -1.4 [-2.8 ; +0.1] | -0.60 [-1.28 ; +0.03] |  |
| momentum 12-1 sur la nuit | 6B | 2425 | +1.0 [-0.5 ; +2.7] | -0.4 [-1.9 ; +1.3] | -0.14 [-0.73 ; +0.45] |  |
| momentum 12-1 sur la nuit | 6J | 2426 | +1.4 [-0.4 ; +3.3] | +0.3 [-1.5 ; +2.2] | +0.10 [-0.53 ; +0.78] |  |
| momentum 12-1 sur la nuit | 6A | 2423 | +0.8 [-1.1 ; +2.7] | -0.7 [-2.5 ; +1.3] | -0.21 [-0.82 ; +0.38] |  |
| reversal LT 36-13 sur le jour | NQ | 1920 | -4.3 [-9.4 ; +0.6] | -4.6 [-9.8 ; +0.3] | -0.63 [-1.29 ; -0.02] |  |
| reversal LT 36-13 sur le jour | ES | 1919 | -2.7 [-6.4 ; +0.9] | -3.5 [-7.2 ; +0.0] | -0.63 [-1.22 ; -0.03] |  |
| reversal LT 36-13 sur le jour | YM | 1916 | -1.6 [-5.0 ; +1.8] | -2.2 [-5.6 ; +1.2] | -0.43 [-1.02 ; +0.16] |  |
| reversal LT 36-13 sur le jour | GC | 1911 | +1.6 [-1.4 ; +4.8] | +0.9 [-2.1 ; +4.0] | +0.21 [-0.45 ; +0.83] |  |
| reversal LT 36-13 sur le jour | 6E | 1923 | -0.6 [-1.8 ; +0.5] | -1.4 [-2.6 ; -0.3] | -0.81 [-1.50 ; -0.16] | ▼ |
| reversal LT 36-13 sur le jour | 6B | 1923 | +0.2 [-1.2 ; +1.5] | -1.2 [-2.6 ; +0.1] | -0.56 [-1.28 ; +0.18] |  |
| reversal LT 36-13 sur le jour | 6J | 1924 | -1.3 [-2.7 ; +0.0] | -2.5 [-3.9 ; -1.1] | -1.30 [-2.00 ; -0.62] | ▼ |
| reversal LT 36-13 sur le jour | 6A | 1922 | -0.4 [-2.1 ; +1.2] | -1.9 [-3.6 ; -0.3] | -0.79 [-1.46 ; -0.11] | ▼ |
| reversal LT 36-13 sur la nuit | NQ | 1920 | -3.2 [-6.9 ; +0.5] | -3.5 [-7.3 ; +0.1] | -0.64 [-1.34 ; +0.01] |  |
| reversal LT 36-13 sur la nuit | ES | 1919 | -2.2 [-5.1 ; +0.8] | -3.0 [-6.0 ; -0.0] | -0.70 [-1.44 ; -0.01] | ▼ |
| reversal LT 36-13 sur la nuit | YM | 1917 | -2.4 [-5.2 ; +0.4] | -3.0 [-5.8 ; -0.2] | -0.71 [-1.43 ; +0.01] | ▼ |
| reversal LT 36-13 sur la nuit | GC | 1911 | -2.3 [-6.0 ; +1.3] | -3.1 [-6.7 ; +0.5] | -0.56 [-1.25 ; +0.11] |  |
| reversal LT 36-13 sur la nuit | 6E | 1923 | +1.6 [-0.0 ; +3.1] | +0.8 [-0.8 ; +2.3] | +0.33 [-0.41 ; +1.06] |  |
| reversal LT 36-13 sur la nuit | 6B | 1923 | +1.1 [-0.7 ; +2.7] | -0.3 [-2.1 ; +1.3] | -0.10 [-0.77 ; +0.60] |  |
| reversal LT 36-13 sur la nuit | 6J | 1924 | -0.5 [-2.6 ; +1.6] | -1.6 [-3.8 ; +0.5] | -0.54 [-1.33 ; +0.17] |  |
| reversal LT 36-13 sur la nuit | 6A | 1921 | +1.5 [-0.6 ; +3.5] | +0.0 [-2.1 ; +2.0] | +0.01 [-0.65 ; +0.65] |  |

### [20] Fattinger-Ziegler

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| P1 00:00→01:00 CET | NQ | 1971 | -0.2 [-1.2 ; +0.7] | -0.7 [-1.7 ; +0.2] | -0.48 [-1.08 ; +0.13] |  |
| P1 00:00→01:00 CET | ES | 1971 | -0.1 [-0.9 ; +0.6] | -1.1 [-1.9 ; -0.4] | -0.92 [-1.57 ; -0.28] | ▼ |
| P1 00:00→01:00 CET | YM | 1969 | -0.2 [-0.8 ; +0.5] | -0.9 [-1.5 ; -0.2] | -0.76 [-1.39 ; -0.15] | ▼ |
| P1 00:00→01:00 CET | GC | 1966 | +1.5 [+0.8 ; +2.3] | +0.7 [-0.0 ; +1.5] | +0.54 [-0.10 ; +1.09] |  |
| P1 00:00→01:00 CET | 6E | 2009 | +0.3 [+0.0 ; +0.6] | -0.5 [-0.8 ; -0.2] | -1.10 [-1.78 ; -0.46] | ▼ |
| P1 00:00→01:00 CET | 6B | 2009 | +0.1 [-0.2 ; +0.6] | -1.2 [-1.6 ; -0.8] | -1.77 [-2.80 ; -1.00] | ▼ |
| P1 00:00→01:00 CET | 6J | 2009 | +0.4 [-0.1 ; +0.8] | -0.8 [-1.2 ; -0.3] | -1.06 [-1.73 ; -0.39] | ▼ |
| P1 00:00→01:00 CET | 6A | 2009 | +0.1 [-0.3 ; +0.5] | -1.3 [-1.7 ; -0.9] | -1.89 [-2.48 ; -1.28] | ▼ |
| P2 01:00→08:00 CET | NQ | 2568 | +2.0 [+0.4 ; +3.6] | +1.5 [-0.1 ; +3.1] | +0.48 [-0.02 ; +1.00] |  |
| P2 01:00→08:00 CET | ES | 2568 | +1.1 [-0.2 ; +2.5] | +0.1 [-1.2 ; +1.4] | +0.04 [-0.45 ; +0.53] |  |
| P2 01:00→08:00 CET | YM | 2566 | +1.0 [-0.2 ; +2.3] | +0.3 [-0.9 ; +1.6] | +0.14 [-0.36 ; +0.63] |  |
| P2 01:00→08:00 CET | GC | 2561 | +1.0 [-0.6 ; +2.5] | +0.1 [-1.4 ; +1.7] | +0.03 [-0.55 ; +0.62] |  |
| P2 01:00→08:00 CET | 6E | 2568 | +0.0 [-0.6 ; +0.8] | -0.8 [-1.4 ; -0.0] | -0.70 [-1.30 ; -0.05] | ▼ |
| P2 01:00→08:00 CET | 6B | 2568 | -0.5 [-1.4 ; +0.4] | -1.8 [-2.8 ; -1.0] | -1.15 [-1.74 ; -0.71] | ▼ |
| P2 01:00→08:00 CET | 6J | 2568 | +0.7 [-0.4 ; +1.8] | -0.4 [-1.6 ; +0.6] | -0.21 [-0.84 ; +0.44] |  |
| P2 01:00→08:00 CET | 6A | 2568 | +0.6 [-0.5 ; +1.7] | -0.8 [-1.9 ; +0.3] | -0.43 [-0.99 ; +0.15] |  |
| P3 08:00→09:00 CET | NQ | 2568 | +0.8 [+0.1 ; +1.5] | +0.3 [-0.4 ; +1.0] | +0.26 [-0.33 ; +0.86] |  |
| P3 08:00→09:00 CET | ES | 2568 | +0.6 [-0.0 ; +1.1] | -0.4 [-1.0 ; +0.1] | -0.42 [-1.01 ; +0.17] |  |
| P3 08:00→09:00 CET | YM | 2567 | +0.3 [-0.2 ; +1.0] | -0.3 [-0.9 ; +0.3] | -0.34 [-0.95 ; +0.26] |  |
| P3 08:00→09:00 CET | GC | 2564 | +0.5 [-0.2 ; +1.2] | -0.4 [-1.1 ; +0.3] | -0.28 [-0.93 ; +0.34] |  |
| P3 08:00→09:00 CET | 6E | 2568 | -0.5 [-0.9 ; -0.2] | -1.3 [-1.7 ; -1.0] | -1.98 [-2.57 ; -1.41] | ▼ |
| P3 08:00→09:00 CET | 6B | 2568 | -0.8 [-1.2 ; -0.4] | -2.2 [-2.6 ; -1.8] | -2.66 [-3.24 ; -2.07] | ▼ |
| P3 08:00→09:00 CET | 6J | 2568 | -0.5 [-1.0 ; -0.0] | -1.6 [-2.1 ; -1.1] | -2.06 [-2.77 ; -1.40] | ▼ |
| P3 08:00→09:00 CET | 6A | 2568 | -0.5 [-1.0 ; -0.0] | -1.9 [-2.4 ; -1.4] | -2.29 [-2.84 ; -1.71] | ▼ |
| P4 09:00→13:00 CET | NQ | 2568 | +0.6 [-0.9 ; +1.9] | +0.1 [-1.4 ; +1.4] | +0.02 [-0.49 ; +0.57] |  |
| P4 09:00→13:00 CET | ES | 2568 | +1.1 [-0.1 ; +2.3] | +0.1 [-1.1 ; +1.3] | +0.07 [-0.47 ; +0.66] |  |
| P4 09:00→13:00 CET | YM | 2567 | +1.1 [-0.1 ; +2.4] | +0.4 [-0.8 ; +1.7] | +0.20 [-0.40 ; +0.84] |  |
| P4 09:00→13:00 CET | GC | 2564 | +0.8 [-0.6 ; +2.2] | -0.1 [-1.4 ; +1.3] | -0.04 [-0.60 ; +0.55] |  |
| P4 09:00→13:00 CET | 6E | 2568 | +0.0 [-0.7 ; +0.8] | -0.8 [-1.5 ; -0.0] | -0.55 [-1.13 ; +0.02] | ▼ |
| P4 09:00→13:00 CET | 6B | 2568 | +0.1 [-0.9 ; +1.0] | -1.3 [-2.3 ; -0.4] | -0.75 [-1.31 ; -0.18] | ▼ |
| P4 09:00→13:00 CET | 6J | 2568 | -0.3 [-1.1 ; +0.6] | -1.4 [-2.2 ; -0.6] | -0.93 [-1.53 ; -0.37] | ▼ |
| P4 09:00→13:00 CET | 6A | 2568 | -0.4 [-1.3 ; +0.6] | -1.8 [-2.7 ; -0.9] | -1.13 [-1.74 ; -0.52] | ▼ |
| P5 13:00→15:30 CET | NQ | 2568 | -0.2 [-1.7 ; +1.3] | -0.7 [-2.2 ; +0.8] | -0.24 [-0.84 ; +0.30] |  |
| P5 13:00→15:30 CET | ES | 2568 | +0.3 [-0.9 ; +1.5] | -0.7 [-1.9 ; +0.5] | -0.33 [-0.92 ; +0.23] |  |
| P5 13:00→15:30 CET | YM | 2568 | +0.2 [-1.0 ; +1.3] | -0.5 [-1.6 ; +0.6] | -0.27 [-0.82 ; +0.27] |  |
| P5 13:00→15:30 CET | GC | 2565 | +0.4 [-1.1 ; +2.0] | -0.4 [-1.9 ; +1.1] | -0.14 [-0.72 ; +0.44] |  |
| P5 13:00→15:30 CET | 6E | 2568 | -0.0 [-0.9 ; +0.8] | -0.8 [-1.7 ; -0.0] | -0.53 [-1.13 ; +0.03] | ▼ |
| P5 13:00→15:30 CET | 6B | 2568 | -0.2 [-1.1 ; +0.7] | -1.6 [-2.5 ; -0.7] | -0.97 [-1.54 ; -0.41] | ▼ |
| P5 13:00→15:30 CET | 6J | 2568 | -0.2 [-1.0 ; +0.7] | -1.3 [-2.2 ; -0.4] | -0.78 [-1.37 ; -0.20] | ▼ |
| P5 13:00→15:30 CET | 6A | 2568 | +0.4 [-0.6 ; +1.3] | -1.1 [-2.0 ; -0.1] | -0.62 [-1.18 ; -0.09] | ▼ |
| P6 15:30→17:30 CET | NQ | 2564 | +1.2 [-1.2 ; +3.7] | +0.7 [-1.7 ; +3.1] | +0.17 [-0.37 ; +0.70] |  |
| P6 15:30→17:30 CET | ES | 2564 | +0.9 [-0.9 ; +2.7] | -0.1 [-1.9 ; +1.7] | -0.01 [-0.56 ; +0.53] |  |
| P6 15:30→17:30 CET | YM | 2562 | +0.8 [-1.1 ; +2.5] | +0.1 [-1.7 ; +1.8] | +0.06 [-0.51 ; +0.64] |  |
| P6 15:30→17:30 CET | GC | 2564 | +0.5 [-1.4 ; +2.2] | -0.4 [-2.3 ; +1.3] | -0.11 [-0.65 ; +0.47] |  |
| P6 15:30→17:30 CET | 6E | 2568 | +0.2 [-0.6 ; +1.0] | -0.6 [-1.4 ; +0.2] | -0.48 [-1.11 ; +0.12] |  |
| P6 15:30→17:30 CET | 6B | 2569 | +0.9 [-0.0 ; +1.8] | -0.5 [-1.4 ; +0.4] | -0.36 [-0.99 ; +0.24] |  |
| P6 15:30→17:30 CET | 6J | 2569 | +0.5 [-0.4 ; +1.3] | -0.7 [-1.5 ; +0.2] | -0.43 [-1.02 ; +0.18] |  |
| P6 15:30→17:30 CET | 6A | 2568 | +0.0 [-1.0 ; +1.1] | -1.4 [-2.5 ; -0.4] | -0.81 [-1.41 ; -0.19] | ▼ |
| P7 17:30→22:00 CET | NQ | 2474 | +2.3 [-0.7 ; +5.5] | +1.7 [-1.2 ; +5.0] | +0.34 [-0.13 ; +0.84] |  |
| P7 17:30→22:00 CET | ES | 2474 | +1.7 [-0.6 ; +4.2] | +0.7 [-1.6 ; +3.2] | +0.17 [-0.33 ; +0.69] |  |
| P7 17:30→22:00 CET | YM | 2471 | +1.5 [-0.8 ; +3.9] | +0.8 [-1.5 ; +3.2] | +0.21 [-0.30 ; +0.73] |  |
| P7 17:30→22:00 CET | GC | 2479 | -0.5 [-2.0 ; +1.1] | -1.4 [-2.9 ; +0.2] | -0.54 [-1.08 ; -0.01] |  |
| P7 17:30→22:00 CET | 6E | 2511 | -0.1 [-0.8 ; +0.6] | -0.9 [-1.6 ; -0.2] | -0.78 [-1.34 ; -0.19] | ▼ |
| P7 17:30→22:00 CET | 6B | 2511 | +0.3 [-0.5 ; +1.1] | -1.1 [-1.9 ; -0.3] | -0.82 [-1.37 ; -0.28] | ▼ |
| P7 17:30→22:00 CET | 6J | 2511 | -1.2 [-2.0 ; -0.5] | -2.4 [-3.1 ; -1.6] | -1.81 [-2.36 ; -1.25] | ▼ |
| P7 17:30→22:00 CET | 6A | 2511 | +0.4 [-0.5 ; +1.2] | -1.1 [-1.9 ; -0.2] | -0.66 [-1.19 ; -0.12] | ▼ |
| P8 22:00→24:00 CET | NQ | 2474 | +1.4 [+0.5 ; +2.4] | +0.9 [-0.1 ; +1.9] | +0.55 [+0.02 ; +1.12] |  |
| P8 22:00→24:00 CET | ES | 2474 | +0.7 [+0.1 ; +1.3] | -0.3 [-0.9 ; +0.3] | -0.28 [-0.85 ; +0.28] |  |
| P8 22:00→24:00 CET | YM | 2472 | +1.1 [+0.6 ; +1.7] | +0.4 [-0.1 ; +1.0] | +0.48 [-0.12 ; +1.09] |  |
| P8 22:00→24:00 CET | GC | 2471 | +0.5 [+0.1 ; +1.0] | -0.3 [-0.8 ; +0.2] | -0.43 [-1.12 ; +0.20] |  |
| P8 22:00→24:00 CET | 6E | 2511 | +0.0 [-0.2 ; +0.2] | -0.8 [-1.0 ; -0.6] | -2.47 [-3.09 ; -1.86] | ▼ |
| P8 22:00→24:00 CET | 6B | 2511 | +0.3 [+0.1 ; +0.6] | -1.0 [-1.3 ; -0.8] | -2.72 [-3.47 ; -1.99] | ▼ |
| P8 22:00→24:00 CET | 6J | 2511 | -0.5 [-0.8 ; -0.2] | -1.6 [-1.9 ; -1.3] | -3.15 [-4.46 ; -2.16] | ▼ |
| P8 22:00→24:00 CET | 6A | 2508 | +0.0 [-0.2 ; +0.3] | -1.4 [-1.6 ; -1.1] | -3.18 [-3.83 ; -2.53] | ▼ |

### [21] Wei

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| passif session asia | NQ | 2751 | +2.5 [+0.8 ; +4.3] | +2.0 [+0.3 ; +3.8] | +0.61 [+0.13 ; +1.07] | ▲ |
| passif session asia | ES | 2751 | +1.5 [+0.0 ; +3.0] | +0.5 [-1.0 ; +2.0] | +0.19 [-0.30 ; +0.63] |  |
| passif session asia | YM | 2750 | +1.0 [-0.2 ; +2.4] | +0.3 [-0.9 ; +1.7] | +0.14 [-0.35 ; +0.60] |  |
| passif session asia | GC | 2747 | +0.8 [-1.0 ; +2.6] | -0.1 [-1.8 ; +1.7] | -0.03 [-0.54 ; +0.50] |  |
| passif session asia | 6E | 2751 | +0.0 [-0.8 ; +0.8] | -0.8 [-1.6 ; +0.0] | -0.59 [-1.21 ; +0.02] |  |
| passif session asia | 6B | 2751 | -1.1 [-2.0 ; -0.2] | -2.4 [-3.3 ; -1.6] | -1.46 [-2.02 ; -0.90] | ▼ |
| passif session asia | 6J | 2751 | -0.1 [-1.3 ; +1.1] | -1.2 [-2.4 ; -0.0] | -0.53 [-1.14 ; +0.05] | ▼ |
| passif session asia | 6A | 2751 | +0.7 [-0.5 ; +1.9] | -0.7 [-1.9 ; +0.5] | -0.34 [-0.92 ; +0.27] |  |
| passif session europe | NQ | 2752 | +1.4 [-1.1 ; +3.8] | +0.9 [-1.6 ; +3.3] | +0.22 [-0.38 ; +0.77] |  |
| passif session europe | ES | 2752 | +1.9 [-0.2 ; +3.8] | +0.9 [-1.2 ; +2.8] | +0.27 [-0.34 ; +0.86] |  |
| passif session europe | YM | 2752 | +1.7 [-0.4 ; +3.7] | +1.0 [-1.1 ; +3.0] | +0.30 [-0.31 ; +0.92] |  |
| passif session europe | GC | 2749 | +1.3 [-0.8 ; +3.6] | +0.4 [-1.7 ; +2.8] | +0.12 [-0.43 ; +0.70] |  |
| passif session europe | 6E | 2752 | -0.5 [-1.6 ; +0.6] | -1.3 [-2.4 ; -0.2] | -0.64 [-1.24 ; -0.07] | ▼ |
| passif session europe | 6B | 2752 | +0.2 [-1.2 ; +1.5] | -1.2 [-2.6 ; +0.1] | -0.52 [-1.08 ; +0.03] |  |
| passif session europe | 6J | 2752 | -0.3 [-1.5 ; +0.9] | -1.4 [-2.6 ; -0.2] | -0.64 [-1.24 ; -0.04] | ▼ |
| passif session europe | 6A | 2752 | -0.1 [-1.6 ; +1.2] | -1.5 [-3.0 ; -0.2] | -0.65 [-1.21 ; -0.10] | ▼ |
| passif session us | NQ | 3312 | +2.6 [-0.8 ; +6.0] | +2.0 [-1.4 ; +5.5] | +0.45 [-0.03 ; +1.00] |  |
| passif session us | ES | 3312 | +1.4 [-1.4 ; +4.1] | +0.4 [-2.4 ; +3.1] | +0.24 [-0.24 ; +0.75] |  |
| passif session us | YM | 3311 | +1.4 [-1.3 ; +3.7] | +0.7 [-1.9 ; +3.0] | +0.32 [-0.18 ; +0.82] |  |
| passif session us | GC | 3311 | +2.2 [+0.5 ; +4.0] | +1.3 [-0.4 ; +3.1] | +0.30 [-0.23 ; +0.83] |  |
| passif session us | 6E | 3314 | +0.1 [-0.7 ; +0.9] | -0.7 [-1.5 ; +0.1] | -0.35 [-0.95 ; +0.22] |  |
| passif session us | 6B | 3314 | +0.5 [-0.5 ; +1.5] | -0.9 [-1.8 ; +0.1] | -0.28 [-0.90 ; +0.31] |  |
| passif session us | 6J | 3314 | -1.3 [-2.2 ; -0.3] | -2.4 [-3.4 ; -1.4] | -1.18 [-1.75 ; -0.61] | ▼ |
| passif session us | 6A | 3314 | -0.4 [-1.5 ; +0.7] | -1.8 [-2.9 ; -0.7] | -0.76 [-1.31 ; -0.19] | ▼ |
| momentum toutes sessions long-short | NQ | 8789 | +0.3 [-1.2 ; +1.8] | -0.2 [-1.7 ; +1.2] | -0.08 [-0.59 ; +0.42] |  |
| momentum toutes sessions long-short | ES | 8706 | -0.5 [-1.7 ; +0.8] | -1.5 [-2.7 ; -0.2] | -0.62 [-1.20 ; -0.09] | ▼ |
| momentum toutes sessions long-short | YM | 8763 | -0.7 [-1.8 ; +0.5] | -1.4 [-2.5 ; -0.2] | -0.62 [-1.19 ; -0.10] | ▼ |
| momentum toutes sessions long-short | GC | 8736 | +1.6 [+0.3 ; +2.8] | +0.7 [-0.5 ; +2.0] | +0.33 [-0.26 ; +0.90] |  |
| momentum toutes sessions long-short | 6E | 8730 | -0.5 [-1.0 ; -0.0] | -1.3 [-1.8 ; -0.8] | -1.27 [-1.83 ; -0.72] | ▼ |
| momentum toutes sessions long-short | 6B | 8703 | +0.4 [-0.3 ; +1.0] | -1.0 [-1.7 ; -0.4] | -0.79 [-1.45 ; -0.20] | ▼ |
| momentum toutes sessions long-short | 6J | 8719 | +0.5 [-0.2 ; +1.1] | -0.7 [-1.3 ; -0.0] | -0.43 [-1.04 ; +0.13] | ▼ |
| momentum toutes sessions long-short | 6A | 8674 | -0.6 [-1.4 ; +0.1] | -2.1 [-2.8 ; -1.3] | -1.43 [-2.04 ; -0.87] | ▼ |
| momentum toutes sessions long-only | NQ | 4736 | +2.3 [+0.4 ; +4.2] | +1.8 [-0.1 ; +3.7] | +0.55 [+0.02 ; +1.09] |  |
| momentum toutes sessions long-only | ES | 4716 | +1.1 [-0.4 ; +2.6] | +0.1 [-1.4 ; +1.6] | +0.16 [-0.39 ; +0.68] |  |
| momentum toutes sessions long-only | YM | 4726 | +0.7 [-0.8 ; +2.2] | -0.0 [-1.5 ; +1.5] | +0.09 [-0.46 ; +0.65] |  |
| momentum toutes sessions long-only | GC | 4489 | +3.0 [+1.4 ; +4.5] | +2.1 [+0.5 ; +3.7] | +0.69 [+0.13 ; +1.24] | ▲ |
| momentum toutes sessions long-only | 6E | 4366 | -0.6 [-1.3 ; +0.2] | -1.4 [-2.1 ; -0.6] | -0.91 [-1.50 ; -0.33] | ▼ |
| momentum toutes sessions long-only | 6B | 4381 | +0.2 [-0.6 ; +1.1] | -1.1 [-2.0 ; -0.2] | -0.59 [-1.16 ; +0.00] | ▼ |
| momentum toutes sessions long-only | 6J | 4054 | -0.2 [-1.1 ; +0.8] | -1.3 [-2.2 ; -0.3] | -0.53 [-1.17 ; +0.08] | ▼ |
| momentum toutes sessions long-only | 6A | 4348 | -0.6 [-1.6 ; +0.4] | -2.0 [-3.1 ; -1.0] | -1.02 [-1.61 ; -0.44] | ▼ |
| momentum asia seule long-short | NQ | 2746 | -0.8 [-2.7 ; +1.0] | -1.4 [-3.2 ; +0.4] | -0.39 [-0.93 ; +0.16] |  |
| momentum asia seule long-short | ES | 2729 | -1.2 [-2.8 ; +0.4] | -2.2 [-3.8 ; -0.6] | -0.79 [-1.34 ; -0.24] | ▼ |
| momentum asia seule long-short | YM | 2739 | -0.3 [-1.9 ; +1.1] | -1.0 [-2.6 ; +0.4] | -0.38 [-0.98 ; +0.28] |  |
| momentum asia seule long-short | GC | 2724 | -0.9 [-3.1 ; +1.3] | -1.7 [-3.9 ; +0.4] | -0.52 [-1.25 ; +0.21] |  |
| momentum asia seule long-short | 6E | 2724 | -0.8 [-1.6 ; -0.0] | -1.6 [-2.4 ; -0.8] | -1.15 [-1.72 ; -0.57] | ▼ |
| momentum asia seule long-short | 6B | 2706 | +0.2 [-0.7 ; +1.2] | -1.2 [-2.1 ; -0.2] | -0.61 [-1.27 ; +0.03] | ▼ |
| momentum asia seule long-short | 6J | 2717 | -0.2 [-1.4 ; +1.0] | -1.4 [-2.6 ; -0.2] | -0.59 [-1.19 ; +0.00] | ▼ |
| momentum asia seule long-short | 6A | 2698 | -1.7 [-3.2 ; -0.3] | -3.2 [-4.6 ; -1.8] | -1.29 [-1.87 ; -0.73] | ▼ |
| momentum asia seule long-only | NQ | 1505 | +1.5 [-0.5 ; +3.4] | +1.0 [-1.0 ; +2.9] | +0.25 [-0.25 ; +0.80] |  |
| momentum asia seule long-only | ES | 1492 | +0.2 [-1.4 ; +1.8] | -0.8 [-2.4 ; +0.8] | -0.23 [-0.73 ; +0.27] |  |
| momentum asia seule long-only | YM | 1497 | +0.6 [-1.0 ; +2.3] | -0.1 [-1.7 ; +1.6] | -0.03 [-0.58 ; +0.54] |  |
| momentum asia seule long-only | GC | 1398 | -0.1 [-3.1 ; +2.7] | -1.0 [-4.0 ; +1.9] | -0.24 [-0.89 ; +0.40] |  |
| momentum asia seule long-only | 6E | 1335 | -0.8 [-1.9 ; +0.3] | -1.6 [-2.7 ; -0.5] | -0.84 [-1.46 ; -0.23] | ▼ |
| momentum asia seule long-only | 6B | 1389 | -0.9 [-2.1 ; +0.2] | -2.3 [-3.4 ; -1.1] | -1.05 [-1.59 ; -0.49] | ▼ |
| momentum asia seule long-only | 6J | 1192 | -0.2 [-2.0 ; +1.7] | -1.3 [-3.2 ; +0.5] | -0.37 [-0.91 ; +0.22] |  |
| momentum asia seule long-only | 6A | 1320 | -1.0 [-2.9 ; +0.9] | -2.4 [-4.3 ; -0.5] | -0.77 [-1.37 ; -0.16] | ▼ |
| momentum europe seule long-short | NQ | 2739 | -0.6 [-3.1 ; +1.9] | -1.2 [-3.6 ; +1.4] | -0.23 [-0.75 ; +0.31] |  |
| momentum europe seule long-short | ES | 2690 | -0.3 [-2.2 ; +1.7] | -1.3 [-3.2 ; +0.7] | -0.34 [-0.89 ; +0.23] |  |
| momentum europe seule long-short | YM | 2728 | -1.1 [-2.9 ; +0.7] | -1.8 [-3.6 ; -0.0] | -0.46 [-1.01 ; +0.09] | ▼ |
| momentum europe seule long-short | GC | 2723 | +3.1 [+0.8 ; +5.4] | +2.2 [-0.1 ; +4.6] | +0.61 [+0.04 ; +1.17] |  |
| momentum europe seule long-short | 6E | 2717 | -0.5 [-1.8 ; +0.7] | -1.3 [-2.6 ; -0.1] | -0.67 [-1.25 ; -0.08] | ▼ |
| momentum europe seule long-short | 6B | 2710 | +0.9 [-0.5 ; +2.3] | -0.5 [-1.9 ; +0.9] | -0.23 [-0.82 ; +0.35] |  |
| momentum europe seule long-short | 6J | 2718 | +1.1 [-0.3 ; +2.3] | -0.0 [-1.4 ; +1.1] | -0.03 [-0.60 ; +0.54] |  |
| momentum europe seule long-short | 6A | 2713 | +0.7 [-0.7 ; +2.0] | -0.7 [-2.1 ; +0.6] | -0.27 [-0.85 ; +0.29] |  |
| momentum europe seule long-only | NQ | 1484 | +0.9 [-2.3 ; +3.9] | +0.4 [-2.8 ; +3.4] | +0.10 [-0.47 ; +0.65] |  |
| momentum europe seule long-only | ES | 1438 | +1.8 [-0.7 ; +4.2] | +0.8 [-1.7 ; +3.2] | +0.22 [-0.39 ; +0.81] |  |
| momentum europe seule long-only | YM | 1456 | +0.8 [-1.6 ; +3.2] | +0.1 [-2.3 ; +2.5] | +0.05 [-0.53 ; +0.61] |  |
| momentum europe seule long-only | GC | 1370 | +4.3 [+1.4 ; +7.2] | +3.5 [+0.5 ; +6.4] | +0.75 [+0.15 ; +1.33] | ▲ |
| momentum europe seule long-only | 6E | 1395 | -0.9 [-2.6 ; +0.8] | -1.7 [-3.4 ; -0.0] | -0.59 [-1.21 ; +0.04] | ▼ |
| momentum europe seule long-only | 6B | 1322 | +1.2 [-0.9 ; +3.0] | -0.2 [-2.3 ; +1.6] | -0.09 [-0.68 ; +0.51] |  |
| momentum europe seule long-only | 6J | 1300 | +0.7 [-0.9 ; +2.4] | -0.4 [-2.0 ; +1.3] | -0.11 [-0.69 ; +0.45] |  |
| momentum europe seule long-only | 6A | 1397 | +0.6 [-1.1 ; +2.4] | -0.8 [-2.5 ; +1.0] | -0.23 [-0.81 ; +0.34] |  |
| momentum us seule long-short | NQ | 3304 | +2.0 [-1.1 ; +5.1] | +1.4 [-1.7 ; +4.6] | +0.25 [-0.30 ; +0.76] |  |
| momentum us seule long-short | ES | 3287 | +0.1 [-2.5 ; +2.5] | -0.9 [-3.5 ; +1.5] | -0.17 [-0.78 ; +0.38] |  |
| momentum us seule long-short | YM | 3296 | -0.7 [-3.1 ; +1.7] | -1.4 [-3.8 ; +1.0] | -0.31 [-0.88 ; +0.28] |  |
| momentum us seule long-short | GC | 3289 | +2.3 [+0.4 ; +4.2] | +1.4 [-0.5 ; +3.3] | +0.37 [-0.26 ; +1.00] |  |
| momentum us seule long-short | 6E | 3289 | -0.2 [-1.0 ; +0.6] | -1.0 [-1.9 ; -0.2] | -0.48 [-1.09 ; +0.05] | ▼ |
| momentum us seule long-short | 6B | 3287 | +0.1 [-1.0 ; +1.0] | -1.3 [-2.3 ; -0.3] | -0.63 [-1.31 ; -0.03] | ▼ |
| momentum us seule long-short | 6J | 3284 | +0.5 [-0.4 ; +1.5] | -0.6 [-1.5 ; +0.4] | -0.14 [-0.79 ; +0.46] |  |
| momentum us seule long-short | 6A | 3263 | -0.8 [-2.0 ; +0.4] | -2.3 [-3.4 ; -1.1] | -0.92 [-1.54 ; -0.34] | ▼ |
| momentum us seule long-only | NQ | 1747 | +4.2 [-0.2 ; +8.7] | +3.7 [-0.7 ; +8.1] | +0.55 [+0.03 ; +1.10] |  |
| momentum us seule long-only | ES | 1786 | +1.3 [-1.9 ; +4.3] | +0.3 [-3.0 ; +3.3] | +0.17 [-0.36 ; +0.68] |  |
| momentum us seule long-only | YM | 1773 | +0.6 [-2.3 ; +3.5] | -0.0 [-3.0 ; +2.9] | +0.10 [-0.41 ; +0.62] |  |
| momentum us seule long-only | GC | 1721 | +4.4 [+1.6 ; +7.1] | +3.5 [+0.7 ; +6.2] | +0.68 [+0.07 ; +1.26] | ▲ |
| momentum us seule long-only | 6E | 1636 | -0.1 [-1.3 ; +1.0] | -0.9 [-2.1 ; +0.2] | -0.19 [-0.76 ; +0.40] |  |
| momentum us seule long-only | 6B | 1670 | +0.5 [-0.8 ; +1.8] | -0.9 [-2.2 ; +0.4] | -0.12 [-0.72 ; +0.46] |  |
| momentum us seule long-only | 6J | 1562 | -0.8 [-2.4 ; +0.6] | -2.0 [-3.5 ; -0.5] | -0.45 [-1.06 ; +0.14] | ▼ |
| momentum us seule long-only | 6A | 1631 | -1.3 [-2.8 ; +0.3] | -2.7 [-4.3 ; -1.1] | -0.71 [-1.27 ; -0.17] | ▼ |

### [6] Hendershott-Livdan-Rösch

| Règle | Actif | n | Brut bp/trade [IC 95 %] | Net bp/trade [IC 95 %] | Sharpe net [IC 95 %] | |
|---|---|---|---|---|---|---|
| β_i − β̄ (nuit), portefeuille 8 actifs | univers | 2660 | +6.3 [+0.5 ; +12.0] | +2.9 [-2.9 ; +8.6] | +0.31 [-0.29 ; +0.94] |  |
| β_i − β̄ (jour), portefeuille 8 actifs | univers | 2660 | -6.1 [-11.5 ; -0.5] | -9.5 [-14.9 ; -3.8] | -0.87 [-1.39 ; -0.36] | ▼ |
| β_i − β̄ (nuit + jour), portefeuille 8 actifs | univers | 2660 | +0.2 [-8.1 ; +8.8] | -6.6 [-14.9 ; +2.1] | -0.46 [-1.00 ; +0.15] |  |

### [17] Zhang-Zhao et [18] Ahoniemi-Lanne : relations de volatilité (pas de règle de trading)

| Papier | Relation | Actif | n | Valeur [IC 95 %] |
|---|---|---|---|---|
| [17] Zhang-Zhao | corr(log RV nuit t, log RV jour t) | NQ | 2677 | +0.807 [+0.779 ; +0.832] |
| [17] Zhang-Zhao | corr(log RV jour t-1, log RV nuit t) | NQ | 2676 | +0.806 [+0.777 ; +0.829] |
| [18] Ahoniemi-Lanne | levier : corr(r close-close t-1, RV jour t) | NQ | 2676 | -0.155 [-0.249 ; -0.083] |
| [17] Zhang-Zhao | part de variance nuit Var(r_N)/Var(r) | NQ | 2672 | +0.322 |
| [17] Zhang-Zhao | corr(log RV nuit t, log RV jour t) | ES | 2677 | +0.820 [+0.788 ; +0.846] |
| [17] Zhang-Zhao | corr(log RV jour t-1, log RV nuit t) | ES | 2676 | +0.814 [+0.783 ; +0.840] |
| [18] Ahoniemi-Lanne | levier : corr(r close-close t-1, RV jour t) | ES | 2676 | -0.148 [-0.246 ; -0.053] |
| [17] Zhang-Zhao | part de variance nuit Var(r_N)/Var(r) | ES | 2671 | +0.318 |
| [17] Zhang-Zhao | corr(log RV nuit t, log RV jour t) | YM | 2677 | +0.814 [+0.779 ; +0.844] |
| [17] Zhang-Zhao | corr(log RV jour t-1, log RV nuit t) | YM | 2676 | +0.805 [+0.768 ; +0.835] |
| [18] Ahoniemi-Lanne | levier : corr(r close-close t-1, RV jour t) | YM | 2672 | -0.097 [-0.237 ; +0.018] |
| [17] Zhang-Zhao | part de variance nuit Var(r_N)/Var(r) | YM | 2669 | +0.320 |
| [17] Zhang-Zhao | corr(log RV nuit t, log RV jour t) | GC | 2677 | +0.707 [+0.659 ; +0.747] |
| [17] Zhang-Zhao | corr(log RV jour t-1, log RV nuit t) | GC | 2676 | +0.697 [+0.649 ; +0.739] |
| [18] Ahoniemi-Lanne | levier : corr(r close-close t-1, RV jour t) | GC | 2644 | -0.007 [-0.110 ; +0.082] |
| [17] Zhang-Zhao | part de variance nuit Var(r_N)/Var(r) | GC | 2658 | +0.594 |
| [17] Zhang-Zhao | corr(log RV nuit t, log RV jour t) | 6E | 2677 | +0.668 [+0.622 ; +0.706] |
| [17] Zhang-Zhao | corr(log RV jour t-1, log RV nuit t) | 6E | 2676 | +0.634 [+0.588 ; +0.672] |
| [18] Ahoniemi-Lanne | levier : corr(r close-close t-1, RV jour t) | 6E | 2672 | +0.015 [-0.054 ; +0.081] |
| [17] Zhang-Zhao | part de variance nuit Var(r_N)/Var(r) | 6E | 2675 | +0.645 |
| [17] Zhang-Zhao | corr(log RV nuit t, log RV jour t) | 6B | 2677 | +0.682 [+0.632 ; +0.726] |
| [17] Zhang-Zhao | corr(log RV jour t-1, log RV nuit t) | 6B | 2676 | +0.643 [+0.586 ; +0.690] |
| [18] Ahoniemi-Lanne | levier : corr(r close-close t-1, RV jour t) | 6B | 2672 | -0.090 [-0.188 ; +0.024] |
| [17] Zhang-Zhao | part de variance nuit Var(r_N)/Var(r) | 6B | 2675 | +0.661 |
| [17] Zhang-Zhao | corr(log RV nuit t, log RV jour t) | 6J | 2677 | +0.691 [+0.657 ; +0.723] |
| [17] Zhang-Zhao | corr(log RV jour t-1, log RV nuit t) | 6J | 2676 | +0.671 [+0.632 ; +0.704] |
| [18] Ahoniemi-Lanne | levier : corr(r close-close t-1, RV jour t) | 6J | 2674 | +0.073 [+0.018 ; +0.142] |
| [17] Zhang-Zhao | part de variance nuit Var(r_N)/Var(r) | 6J | 2676 | +0.688 |
| [17] Zhang-Zhao | corr(log RV nuit t, log RV jour t) | 6A | 2676 | +0.666 [+0.612 ; +0.714] |
| [17] Zhang-Zhao | corr(log RV jour t-1, log RV nuit t) | 6A | 2675 | +0.619 [+0.564 ; +0.669] |
| [18] Ahoniemi-Lanne | levier : corr(r close-close t-1, RV jour t) | 6A | 2667 | -0.109 [-0.215 ; +0.003] |
| [17] Zhang-Zhao | part de variance nuit Var(r_N)/Var(r) | 6A | 2672 | +0.652 |