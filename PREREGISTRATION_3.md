# Pré-enregistrement n° 3 : réplications fidèles

*2026-10-12. Écrit après la lecture des textes intégraux ([PAPER_SPECS.md](PAPER_SPECS.md)) et avant toute exécution. Données, coûts (1 tick + 5 $ aller-retour), exécution à l'open de la barre et découpage IS (2016-2022) / OOS (2023-2026-08) sont identiques à [PREREGISTRATION.md](PREREGISTRATION.md). Les résultats sont rapportés **bruts et nets**, puisque la plupart des papiers ignorent les coûts.*

**Principe** : chaque règle reprend le texte du papier. Quand le texte est muet ou quand nos données l'imposent, l'écart est écrit ci-dessous **avant** l'exécution. Aucun paramètre n'est optimisé.

## Réplications (42 nouveaux tests ; le compteur passe de 96 à 138)

| ID | Papier | Règle | Actifs | Tests |
|---|---|---|---|---|
| R1 | Gao et al. | η(r₁, r₁₂) : r₁ = clôture J-1 → 10:00, r₁₂ = 15:00 → 15:30 ; long (short) sur 15:30 → 16:00 si les deux sont > 0 (≤ 0), sinon rien | ES, NQ, YM | 3 |
| R2a | Baltussen et al. | η(r_ROD), session FX **8:20-15:00 ET** | 6E, 6J, 6B, 6A | 4 |
| R2b | Baltussen et al. | η(r_ONFH), session FX 8:20-15:00 ET | 6E, 6J, 6B, 6A | 4 |
| R2c | Baltussen et al. | joint η(r_ONFH, r_ROD), sessions de leur Table 1 | les 9 actifs | 9 |
| R3 | Zarattini et al. | M2 + **volatilité cible** : levier du jour = min(4, 2 % / σ₁₄), σ₁₄ = écart-type des 14 derniers rendements clôture-clôture (16:00) de l'actif | ES, NQ, YM | 3 |
| R4 | Zarattini & Aziz | Sens de la bougie 9:30-9:35, entrée à 9:35, stop à l'extrême de la bougie, objectif 10R, sinon sortie à 16:00. Doji = \|close − open\| ≤ 1 tick → pas de trade. Taille = min(4, 1 % / R%) | NQ, ES, YM | 3 |
| R5a | Krohn et al. | Tokyo : short sur le future (long USD) de 08:00 à 09:55 JST, puis long sur le future de 09:55 à 15:00 JST | 6E, 6J, 6B, 6A | 4 |
| R5b | Krohn et al. | Europe : short sur le future de 02:00 à 08:15 ET, puis long sur le future de 11:00 à 16:55 ET | 6E, 6J, 6B, 6A | 4 |
| R6 | Breedon & Ranaldo | 6E, 6B : short de 02:00 à 08:00 ET, puis long de 08:00 à 16:00 ET. 6A : short de 10:00 à 16:00 heure de Sydney, puis long de 08:00 à 16:00 ET. 6J (USD/JPY, USD = devise de base) : short sur le future (long USD) de 08:00 à 15:00 JST, puis long sur le future de 08:00 à 16:00 ET | 6E, 6B, 6A, 6J | 4 |
| R7a | Caporale & Plastun, stratégie 1 | Jour 00:00-24:00 en GMT+3 fixe. Seuils = moyenne ± 2σ des rendements open → close des **252 jours précédents**. Contrôle à chaque heure pleine : dès que le rendement depuis l'open franchit un seuil, position dans ce sens jusqu'à 23:55 GMT+3. Premier déclenchement seulement | GC, CL | 2 |
| R7b | Caporale & Plastun, stratégie 2 | Le lendemain d'un jour anormal (mêmes seuils, jour complet). CL : position dans le sens du mouvement de l'open à 23:55. GC : contrarien, de l'open à 06:00 GMT+3 après un jour positif, et de l'open à 23:55 après un jour négatif | GC, CL | 2 |

**Non répliqués** : Tsai (fenêtre optimisée, pas une règle fixe) ; Bondarenko (seul le résumé est disponible, la fenêtre vient d'une source secondaire) ; Rosa, Wen, Elaut, Grant et les papiers SSRN de 2026 (non lus).

## Écarts imposés par les données ou le silence des textes (fixés d'avance)

- **Futures au lieu d'ETF ou de spot** : ES, NQ et YM remplacent SPY et QQQ ; 6E, 6J, 6B et 6A remplacent les paires spot (Krohn, Breedon) ; GC et CL remplacent les CFD MetaQuotes (Caporale).
- **R3/R4 (levier)** : le moteur vectorbt simule à 1× ; le levier du jour multiplie ensuite le rendement net du jour. C'est équivalent ici, puisque les positions sont intrajournalières et que la taille est fixée à l'ouverture. Le levier compte dans les coûts : ils sont aussi multipliés.
- **R5a** : la fenêtre pré-Tokyo commence officiellement à 17:00 ET, pendant la pause de maintenance du CME (17:00-18:00 ET). Je la fais commencer à 08:00 JST, soit 18:00 ou 19:00 ET selon l'heure d'été. La fin post-Tokyo est fixée à 15:00 JST (au lieu de 2:00 ET, soit 15:00 ou 16:00 JST).
- **R5b** : la sortie post-Londres est à 16:55 ET au lieu de 17:00 (pause du CME).
- **R7** : la période n des seuils n'est pas lisible dans le PDF (formules perdues). Je prends 252 jours glissants passés. Fuseau GMT+3 fixe (le papier dit « GMT+3 »).

## Critère

Le même qu'avant : Sharpe net > 0,5 en IS **et** > 0,3 en OOS, et trade moyen net positif. Tout survivant est ensuite soumis au **Deflated Sharpe Ratio avec N = 138** (seuil 0,95). Les Sharpe bruts sont rapportés pour juger la fidélité de la réplication : par exemple, retrouve-t-on l'effet brut annoncé ?
