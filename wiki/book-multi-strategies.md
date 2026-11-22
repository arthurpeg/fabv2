---
type: registre
updated: 2026-11-22
---

# Stratégies pour un book multi-stratégies (hors prop firm)

*Créé le 2026-11-22. Ce registre liste les règles et phénomènes qui ne conviennent pas à notre modèle prop firm, mais qui auraient leur place dans un book de plusieurs stratégies. Notre modèle prop firm demande de valider une éval en moins d'un mois, avec un rapport gain / bruit par trade d'au moins 0,15 et un gros risque par trade. Les règles d'ici ont un petit avantage, régulier et peu corrélé, et ne valent que diversifiées entre elles, dimensionnées par la volatilité et exécutées à faible coût.*

**Règle d'immuabilité.** Cette page **pointe** vers les sources (pré-enregistrements, rapports, [[wiki/phenomenes]]) et n'en recopie pas les résultats comme source de vérité. Les chiffres sont des repères ; en cas d'écart, la source a raison.

## Critères d'entrée dans ce registre

1. **Un avantage mesuré sur nos données.** L'effet est confirmé, ou « À surveiller » avec une raison écrite, dans [[wiki/phenomenes]]. Ou c'est une règle qui a passé au moins la barrière B1 de [PROTOCOLE.md](../PROTOCOLE.md).
2. **Inadaptée à la prop firm pour une raison de format**, pas parce qu'elle échoue. Raisons possibles :
   - rapport gain / bruit par trade trop faible ;
   - trop peu de trades par mois ;
   - effet trop lent ;
   - coût d'exécution trop élevé sur CFD.
3. **Intraday ou de nuit**, sans tenue de 24 h (préférence de l'utilisateur du 2026-11-19). La colonne « Tenue » le précise.

**Entrer ici ne vaut pas validation.** Avant tout argent réel, une règle suit le protocole jusqu'à l'étape 4 (forward). Statut : 🔬 exploration, 📋 pré-enregistrée, ⏳ en forward, ✅ confirmée hors échantillon.

## Candidates

| Règle | Actif · fenêtre ET | Tenue | Repères (net, coût standard) | Pourquoi pas en prop firm | Ce qu'il faudrait pour un book | Statut | Source |
|---|---|---|---|---|---|---|---|
| Short yen en session US, tous les jours | 6J, 11:00 → 16:55 | intraday | +0,9 bp / trade, Sharpe 0,6, 10 années sur 11 positives | Gain / bruit 0,04 ; dérive lente, les stops la détruisent | Coût réel ≤ 1 tick ; à combiner, pas seule | ⏳ n° 28 (L1 le 2028-02-29) | [[PREREGISTRATION_28]], `reports/jpy_us_backtest_report.md` |
| Short yen filtré R4 (yen en hausse sur les 3 journées précédentes), SL 2 ATR H1 | 6J, 11:00 → 16:55, 46 % des jours | intraday | +2,1 bp sans stop, Sharpe quotidien 1,0 ; +0,04 R avec le SL | Gain / bruit 0,07 ; environ 4 mois d'éval à 2,5 % de risque | Confirmation du n° 29 ; c'est **le même effet** que la ligne précédente : en choisir une seule | 📋 n° 29 (comptant 2003-2009, puis forward) | [[PREREGISTRATION_29]], `reports/jpy_us_filtres_report.md`, `reports/jpy_us_r4_stops_report.md` |
| Short yen, dernière heure ou décile haut de la hausse sur 3 jours | 6J, 16:00 → 16:55, ou jours D10 | intraday | Brut ≈ +0,9 bp en 55 min (t 4,3) ; D10 +5,5 bp net (t 3,0) | Le coût d'un trade (≈ 1 bp) mange la dernière heure ; D10 est défini après coup | Exécution à ≤ 0,3 bp ; seuil pré-enregistré sur la réserve 6J 2023-07 → 2026-08 | 🔬 (idée arrêtée pour la prop firm) | [[wiki/experiments/yen-derive-concentree]], `reports/yen_derive_ab_report.md` |
| Reprise de l'or | GC, 17:00 → 9:00 Shanghai (≈ 20:00-21:00 NY) | soirée | +1,1 bp net, t 2,0 ; brut +2,0 bp, Holm 0,003 ; nulle le lundi | Gain par trade minuscule face au bruit | Coût réel la nuit (marché mince) ; pré-enregistrement | 🔬 confirmé en brut | [[wiki/phenomenes]], `reports/gc_sessions_report.md` |
| Fenêtre de l'or autour de l'arrêt | GC, 16:00 → 19:00 | intraday | +1,4 bp net, t 2,7 | Choisie après coup ; nulle en 2016-2019 | Holdout pré-enregistré | 🔬 à surveiller | `reports/gc_sessions_report.md` |
| Signe de l'enchère d'ouverture Xetra | DAX, 08:55 → 09:00 Francfort | quelques minutes | 55 % de bons signes, p 0,0008 ; Sharpe net 0,13 | Le coût d'un aller-retour dépasse le mouvement | Participation passive à l'enchère, ou exécution d'un autre flux à ce moment | 🔬 phénomène confirmé, non tradable tel quel | `reports/opening_gap_report.md` |
| Rebond de nuit après une forte baisse (décile bas de r3) | NQ, ES, YM, 20:05 → 03:00 | nuit (traverse minuit) | D1 : +17 bps NQ, +16 ES, +11 YM (t 2,5 à 3,7), positif dans 6 échantillons sur 6 | Environ 1 nuit sur 10 : trop rare pour une éval | Pré-enregistrement sur le holdout ; à vérifier contre la règle intraday | 🔬 à surveiller | `reports/nq_nuit_r3_pente_report.md` |
| Sessions FX de Zhang : GBP et CAD en baisse hors session US, CHF en hausse pendant LDN-NY | 6B, USDCAD, USDCHF | intraday ou nuit | −1,5 / −1,1 / +1,5 bp, t 2,4 à 2,8 | Trouvées dans un balayage de 28 cases, sans Holm ; brut ≈ coût | Réserve vierge ou forward ; exécution au comptant institutionnel | 🔬 à surveiller | `reports/zhang_fx_report.md` |

## Avant de construire un book

- **Ne pas compter deux fois le même effet.** Les trois lignes du yen sont un seul phénomène. Dans un book, on prend une seule version.
- **Mesurer la corrélation entre jambes** sur données vues, et avec mom, 3n et M2 qui sont en prop firm. Les heures se chevauchent peu : yen 11:00-17:00, or le soir, indices la nuit. C'est un bon signe, mais pas une preuve.
- **Pré-enregistrer la combinaison** (règle 3 du wiki) : poids, cible de volatilité, coupe-circuits K1-K2 de l'étape 5.
- **Le coût décide de presque tout.** La plupart de ces règles ont moins de 2 bp de brut par trade. Un book n'a de sens qu'avec un accès au futur ou au comptant moins cher que le CFD de prop firm.

## Comment alimenter ce registre

Une règle entre ici quand une exploration ou un pré-enregistrement conclut « avantage réel, mais pas pour la prop firm ». On ajoute une ligne avec ses liens, et une entrée au [[wiki/log]]. Une règle rejetée hors échantillon en sort, avec une ligne au [[wiki/Failed Ideas/ledger|registre des échecs]].
