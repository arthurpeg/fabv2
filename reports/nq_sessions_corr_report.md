# NQ : une session qui monte annonce-t-elle une hausse de la suivante ? (Asie → Europe → US)

*2026-11-01. Exploratoire, non pré-enregistré, demandé en séance. Compteur global : 1 493 → 1 501 (8 paires de sessions testées). Code : [run_nq_sessions_corr.py](../run_nq_sessions_corr.py). Sorties : `results/nq_sessions_corr/` (run.log, pairs.csv, by_period.csv, quintiles.csv, follow.csv, sessions.csv).*

## Ce qui est mesuré

NQ 1 minute Databento, 2010-06-08 → 2026-08-28 (holdout non touché), prix ajustés en ratio aux roulements (règle de `run_sessions.py`), 4 048 séances NYSE pleines (demi-séances exclues). Bornes en heure locale, heure d'été gérée :

| Borne | Heure |
|---|---|
| Clôture US de la veille | 16:00 NY |
| Ouverture Europe | 08:00 Londres |
| Clôture asiatique (Hong Kong, la dernière grande) | 16:00 HK = 08:00 UTC |
| Ouverture US | 09:30 NY |
| Clôture Europe (cash, 17:30 Paris) | 16:30 Londres = 11:30 NY (12:30 NY ~3 semaines par an) |
| Clôture US | 16:00 NY |

- **Variante A** : chaque session s'arrête quand la suivante ouvre. Asie = 16:00 NY → 08:00 Ldn, Europe = 08:00 Ldn → 9:30 NY, US = 9:30 → 16:00.
- **Variante B** : on attend la vraie clôture, et on regarde seulement ce qui reste de la session suivante. Asie jusqu'à 16:00 HK → reste de l'Europe jusqu'à 9:30 NY ; Europe jusqu'à 16:30 Ldn → reste de l'US 11:30 → 16:00 NY.
  - Pour l'Asie, la différence n'existe qu'en heure d'été britannique (60 % des jours, 1 h) : en hiver, HK ferme quand Londres ouvre.

Pour chaque paire X → Y : Pearson, Spearman, pente avec t robuste (White), P(Y > 0) selon le signe de X, moyenne de Y par quintile de X, sous-périodes, et un contrôle tradable (position sur Y = signe de X, backtest vectorbt, net 1 tick + 5 $).

## Résultats (toute la période)

| Paire | Var. | Pearson | t pente (HC) | P(Y>0 \| X>0) | P(Y>0 \| X<0) | Y si X>0 / X<0 (bp) | Suivre le signe, net (bp, t) |
|---|---|---|---|---|---|---|---|
| Asie → Europe | A | −0,052 | −2,0 | 50,5 % | 54,3 % | −0,3 / +2,9 | −2,4 (−2,9) |
| Asie → US | A | −0,003 | −0,1 | 54,7 % | 53,1 % | +4,5 / 0,0 | +1,6 (+1,0) |
| Asie → Europe + US | A | −0,006 | −0,2 | 54,5 % | 54,6 % | +4,4 / +2,4 | +0,5 (+0,3) |
| Asie (clôture HK) → reste Europe | B | −0,045 | −1,8 | 50,0 % | 55,4 % | −1,1 / +4,0 | −3,3 (−4,2) |
| Asie (clôture HK) → US | B | +0,003 | +0,1 | 55,5 % | 52,4 % | +5,8 / −1,2 | +2,9 (+1,8) |
| **Europe → US** | A | −0,003 | −0,1 | 53,6 % | 54,5 % | +3,4 / +1,5 | +0,1 (+0,1) |
| **Europe (clôture 16:30 Ldn) → reste US** | B | **+0,066** | **+2,7** | **57,3 %** | **52,9 %** | +4,0 / −1,1 | +1,7 (+1,4) |
| Nuit (Asie + Europe) → US | A | 0,000 | 0,0 | 53,5 % | 54,8 % | +3,1 / +2,3 | −0,2 (−0,1) |

Référence : l'US monte 54 % des jours sans condition ; le long seul sur l'US fait +1,6 bp net par jour. Source : `results/nq_sessions_corr/pairs.csv`, `follow.csv`, `run.log`.

## Lecture

1. **Variante A : l'Europe ne dit rien de l'US.** Corrélation −0,003 ; l'US monte 53,6 % des jours après une Europe positive contre 54,5 % après une Europe négative. Pareil pour l'Asie → US et pour toute la nuit → US (r = 0,000). Le signe de la matinée européenne n'apporte rien au-delà de la dérive haussière de NQ.
2. **Asie → Europe : léger retournement, pas une continuation.** r ≈ −0,05 (t −2) : après une Asie en hausse, l'Europe monte 50,5 % des jours contre 54,3 %. L'effet vient de 2016-2022 (r −0,07 à −0,11) et disparaît en 2023-2026 (r +0,01). Le fade net ne rapporte que ~+0,5 bp (le coût mange 0,9 bp) : rien de tradable.
3. **Variante B Europe → reste US : la seule corrélation positive stable** (r +0,066, positive dans les 4 sous-périodes, de +0,04 à +0,10). Mais la décomposition montre que **ce n'est pas l'Europe** : l'« Europe jusqu'à 16:30 Londres » contient les deux premières heures de l'US (9:30 → 11:30 NY). En régression multiple, la partie Europe pré-US a β +0,04 (t 1,2) et le début de l'US β +0,07 (t 3,0). C'est le **momentum intraday US** (la matinée prédit l'après-midi), même famille que Gao-Baltussen-Rosa, déjà au registre : net +1,7 bp/jour (t 1,4), Sharpe 0,36, à peine mieux que le long seul.
4. **Asie (clôture HK) → US** : écart de 7 bp selon le signe (t 2,2) mais corrélation nulle et négative en 2023-2026 (r −0,05) ; avec 8 paires testées, compatible avec le hasard.
5. **Quintiles** : aucune relation monotone sauf Europe B → reste US (Q1 −4,2 bp, Q5 +7,7 bp, 61 % de hausses dans Q5), expliquée au point 3.

## Conclusion

Sur NQ 2010-2026, **le sens d'une session ne prédit pas celui de la suivante** quand on coupe les sessions à l'ouverture de la suivante (variante A) : Europe → US et nuit → US ont une corrélation nulle. Attendre la vraie clôture européenne (variante B) fait apparaître une corrélation positive avec le reste de la séance US, mais elle vient des deux premières heures US incluses dans la fenêtre, pas de l'Europe. Le seul effet propre aux sessions est un léger retournement Asie → Europe, qui s'est éteint depuis 2023 et ne couvre pas les coûts. Aucune règle retenue ; ligne ajoutée à [[wiki/Failed Ideas/ledger]].
