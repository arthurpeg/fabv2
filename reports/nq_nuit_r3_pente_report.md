# Les nuits après 3 nuits fortement haussières baissent-elles davantage ?

Date : 2026-11-03. **Exploratoire, non pré-enregistré.** Compteur global : 1 695 → 1 719 (24 tests, Holm sur la famille). Script : [run_nq_nuit_r3_pente.py](../run_nq_nuit_r3_pente.py). Sorties : `results/nq_nuit_r3_pente/` (`run.log`, `tests.csv`, `quintiles.csv` qui contient les déciles, `nuits_*.csv`).

**Hypothèse testée** : plus la somme des rendements des 3 nuits précédentes (r3, en bps, 20:05 → 03:00) est positive et loin de 0, plus la nuit suivante a tendance à baisser.

**Échantillons.** NQ 2016-2026 est l'échantillon où le filtre 3n a été trouvé : il ne peut pas confirmer l'hypothèse. Les vrais contrôles sont **NQ 2010-2015**, jamais utilisé pour ce signal, ainsi qu'**ES** et **YM** sur les deux périodes. Il y a 6 échantillons, avec données Databento 1 min et nuits calculées comme dans [[reports/nq_nuit_3n_vbt_report]].

**Tests**, tous restreints aux nuits où r3 > 0. Le t utilise une erreur standard HAC Newey-West (5 retards). Les tests sont unilatéraux dans le sens attendu (< 0).
- T1 : pente du rendement de la nuit sur r3.
- T2 : rendement moyen des nuits du tercile haut de r3 > 0. Ce test demande si la nuit baisse vraiment, pas seulement si elle monte moins.
- T3 : même pente que T1, avec rendement et r3 divisés par la volatilité des 60 nuits précédentes.
- T4 : même pente que T1, avec à la place de r3 le rendement sur 72 h (nuits et journées, prix ajustés aux roulements).

## Résultat : non significatif, nulle part

| Échantillon | T1 pente (bps par 100 bps de r3) | t | T2 nuit, tercile haut (bps) | t | T3 t | T4 t |
|---|---|---|---|---|---|---|
| NQ 2016-2026 (découverte) | −3,2 | −1,31 | −2,3 | −0,99 | −1,10 | +0,47 |
| **NQ 2010-2015** | −0,4 | −0,14 | **+3,4** | +1,95 | +0,18 | −0,76 |
| ES 2016-2026 | −3,8 | −1,23 | −1,4 | −0,73 | −1,30 | −0,37 |
| ES 2010-2015 | −0,4 | −0,13 | +1,5 | +0,80 | +0,59 | −1,49 |
| YM 2016-2026 | −2,1 | −0,67 | +0,6 | +0,33 | −0,66 | +0,04 |
| YM 2010-2015 | −1,0 | −0,37 | +1,9 | +1,24 | +0,34 | −0,38 |

**Aucun t ne dépasse 1,5 en valeur absolue dans le sens attendu, et la p de Holm vaut 1,0 pour les 24 tests.** Les pentes sont légèrement négatives sur 2016-2026, mais elles disparaissent après winsorisation à 1 % (corrélation de rang de Spearman ≈ 0 partout). Sur NQ, la pente n'est nette que sur 2025-2026 (t −2,65, 246 nuits), soit une seule sous-période. Sur 2010-2015, les nuits du tercile haut **montent** (+3,4 bps sur NQ). Plus r3 est haut, plus la nuit baisse : **c'est faux.**

## Ce que montrent les données : une asymétrie

| Décile de r3 (NQ 2016-2026) | D1 (≤ −61 bps) | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 (≥ +77 bps) |
|---|---|---|---|---|---|---|---|---|---|---|
| Nuit suivante (bps) | **+17,3** (t 3,7) | +3,5 | +5,7 | +4,1 | −0,9 | −1,2 | +1,2 | +1,4 | −4,7 | −0,6 |

- **Côté r3 > 0, le profil est plat.** La nuit vaut environ 0 bps, quelle que soit la hausse des 3 nuits : −1,2 bps en moyenne sur NQ 2016-2026 (t −1,05), +2,3 bps sur NQ 2010-2015. Après des nuits haussières, la [[wiki/concepts/prime-de-nuit|prime de nuit]] disparaît, mais la nuit ne s'inverse pas.
- **Côté r3 ≤ 0, c'est là que tout se passe.** Le décile le plus baissier (D1) donne la meilleure nuit dans **les 6 échantillons** : NQ +17,3 bps (t 3,7) et +6,8 (t 2,0) ; ES +15,9 (t 3,3) et +9,5 (t 3,0) ; YM +11,1 (t 2,5) et +8,7 (t 3,0). C'est le rebond après une forte baisse. Ce test n'était pas dans la famille prévue : il est trouvé en regardant les déciles, donc il est « à surveiller », pas confirmé.
- **Ce que capte le filtre 3n** (long si r3 ≤ 0) : il évite les nuits sans prime (r3 > 0) et prend les nuits de rebond (surtout D1). Il ne profite pas d'une baisse après les hausses, puisque cette baisse n'existe pas. Shorter les nuits à r3 très positif n'a donc pas de base. C'est cohérent avec le rapport d'origine, où le short des nuits sautées avait une espérance négative en R.

## Suite possible

Le rebond après une forte baisse (r3 dans le décile bas, environ ≤ −50 bps, ou z ≤ −1,5 σ) tient dans 6 échantillons sur 6, dont 3 jamais vus. C'est le candidat à pré-enregistrer sur le holdout postérieur au 2026-08-28, avec un seuil fixé à l'avance et comparé à un long de mêmes heures. Il est sans doute lié à la piste F2 du n° 13 (nuit précédente < 0).
