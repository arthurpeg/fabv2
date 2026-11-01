# NQ : la matinée US prédit-elle l'après-midi ?

*2026-11-01. Exploratoire, non pré-enregistré, demandé en séance, suite de [[reports/nq_sessions_corr_report]]. Compteur global : 1 501 → 1 520 (12 couples matinée × cible + 7 règles « suivre le signe »). Code : [run_nq_matin_aprem.py](../run_nq_matin_aprem.py). Sorties : `results/nq_matin_aprem/` (run.log, grid.csv, by_period.csv, by_year.csv, magnitude.csv, regime.csv, follow.csv).*

Cadre : le momentum intraday sur indices (Gao : première demi-heure → dernière demi-heure ; Baltussen) est déjà au [[wiki/Failed Ideas/ledger|registre des échecs]]. Ce rapport décrit l'effet ; il ne rouvre pas de stratégie.

## Ce qui est mesuré

NQ 1 minute, 2010-06-08 → 2026-08-28, 4 048 séances pleines, mêmes prix et mêmes mesures que [[reports/nq_sessions_corr_report]]. Matinée X = 9:30 → h, avec h = 10:00, 10:30, 11:00, 11:30, 12:00 ou 13:00 NY. Deux cibles : le **reste de la séance** (h → 16:00) et la **dernière demi-heure** (15:30 → 16:00, cible de Gao).

## Résultats

### Toutes les fenêtres (2010-2026)

| Matinée | Cible | Pearson | t pente | Après-midi en hausse si matin + / − | Après-midi moyen si matin + / − (bp) |
|---|---|---|---|---|---|
| 9:30 → 10:00 | reste | +0,050 | 1,9 | 57,4 % / 52,6 % | +5,1 / −1,8 |
| 9:30 → 10:30 | reste | +0,044 | 2,0 | 57,7 % / 51,8 % | +4,5 / −1,3 |
| 9:30 → 11:00 | reste | +0,030 | 1,5 | 56,6 % / 54,7 % | +4,5 / +0,4 |
| 9:30 → 11:30 | reste | +0,054 | 2,3 | 57,8 % / 52,9 % | +4,5 / −1,8 |
| 9:30 → 12:00 | reste | +0,047 | 2,2 | 56,5 % / 52,9 % | +3,2 / −1,3 |
| 9:30 → 13:00 | reste | +0,070 | 2,9 | 55,6 % / 52,0 % | +2,3 / −0,7 |
| toutes | dernière 1/2 h | +0,006 à +0,054 | 0,3 à 2,1 | ≈ 50 % / 50 % | ±1 |

Source : `grid.csv`.

### Taille de la matinée (9:30 → 11:30), en écarts-types des 20 séances précédentes

| z matinée | ≤ −2 | −2 à −1 | −1 à −0,5 | −0,5 à 0 | 0 à 0,5 | 0,5 à 1 | 1 à 2 | > 2 |
|---|---|---|---|---|---|---|---|---|
| Jours | 152 | 456 | 474 | 783 | 826 | 644 | 520 | 100 |
| Reste de séance (bp) | −2,8 | −5,2 | −3,3 | +1,6 | +4,6 | +3,4 | +6,4 | +8,6 |
| % en hausse | 52 % | 49 % | 55 % | 55 % | 57 % | 57 % | 60 % | 63 % |

Source : `magnitude.csv`.

### Régime de volatilité (9:30 → 11:30)

Terciles de la volatilité réalisée sur 20 jours : vol basse r −0,01 (rien) ; vol moyenne r +0,08 (t 2,4) ; vol haute r +0,06 (t 1,7). Source : `regime.csv`.

### Contrôle tradable

Position = signe de la matinée, tenue de h à 16:00. Backtest vectorbt, net 1 tick + 5 $.

| Matinée | Filtre | Jours | Net bp/jour (t) | 2016-26 | 2023-26 | Long seul, même fenêtre |
|---|---|---|---|---|---|---|
| 9:30 → 10:00 | — | 4 010 | +2,6 (1,8) | +2,8 | +1,7 | +0,9 |
| 9:30 → 11:30 | — | 4 022 | +2,3 (2,0) | +4,0 | +4,1 | +0,6 |
| 9:30 → 13:00 | — | 4 020 | +0,6 (0,7) | +1,6 | +2,3 | 0,0 |
| 9:30 → 11:30 | \|z\| > 1 | 1 215 | +5,8 (2,4) | +7,4 | +9,7 | −0,4 |

Source : `follow.csv` ; les 7 lignes sont dans `run.log`. Le « Sharpe 1,08 » de `follow.csv` pour \|z\| > 1 est annualisé avec √252, alors qu'il n'y a qu'environ 75 trades par an. Corrigé de la fréquence, il vaut environ 0,6.

## Lecture

1. **L'effet existe, il est petit et il est stable de signe.** Sur la cible « reste de séance », la corrélation est positive dans les 24 cases fenêtre × sous-période, de +0,003 à +0,10. Mais elle est faible : R² < 0,5 %, et t entre 0,1 et 2,1 par sous-période. Année par année, elle est négative 8 années sur 17. Elle tient sur la durée, pas d'une année à l'autre.
2. **La dernière demi-heure (Gao) ne marche pas** : ≈ 50 % de hausses quel que soit le signe de la matinée. C'est cohérent avec le registre. Ce qui se prolonge, c'est la tendance du milieu de journée, pas la fin de séance.
3. **C'est surtout une matinée baissière qui casse la dérive haussière.** Sans condition, l'après-midi (≈ 11:30 → 16:00) monte en moyenne de +1,6 bp (`results/nq_sessions_corr/run.log`, us_rest_B). Après une matinée en hausse, il fait +4,5 bp (+2,9 bp de plus) ; après une matinée en baisse, −1,8 bp (−3,4 bp de moins). En taille, c'est assez monotone : de −5 bp après une baisse de 1 à 2 σ à +6 / +9 bp après une hausse de plus de 1 σ.
4. **Rien en volatilité basse**, effet seulement en volatilité moyenne et haute. C'est compatible avec le mécanisme de couverture des vendeurs d'options (gamma négatif, Baltussen et al. 2021), qui achètent dans la hausse et vendent dans la baisse quand le marché bouge. Ce n'est qu'une compatibilité : le gamma n'a pas été mesuré.
5. **Tradable ?** Suivre la matinée 9:30 → 11:30 jusqu'à 16:00 rapporte +2,3 bp/jour net (t 2,0). Avec le seuil \|z\| > 1, c'est +5,8 bp/trade (t 2,4), et plus fort depuis 2016 (+7,4) et depuis 2023 (+9,7). Mais :
   - la fenêtre 11:30 vient du rapport précédent, et le seuil de 1 σ a été choisi ici : c'est de la sélection après coup ;
   - avec N = 1 520 essais, le meilleur t attendu par pur hasard est d'environ √(2 ln N) ≈ 3,8. Un t de 2,4 n'est pas une preuve ;
   - environ 75 trades par an, Sharpe ≈ 0,6.

## Conclusion

La matinée US a un pouvoir prédictif réel mais faible sur le reste de la séance NQ : même sens, corrélation ≈ +0,05, environ 5 points d'écart dans la probabilité de hausse de l'après-midi. Il est concentré sur les matinées marquées (\|z\| > 1) et sur les régimes de volatilité moyenne à haute, et il porte sur le reste de séance, pas sur la dernière demi-heure. Ce n'est pas une stratégie démontrée. Le seul test honnête serait une règle figée à l'avance (9:30 → 11:30, \|z\| > 1, sortie 16:00), pré-enregistrée et jouée une seule fois sur le holdout postérieur au 2026-08-28, qui doit d'abord s'allonger.
