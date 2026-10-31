# Pré-enregistrement n° 19 — S1 + stop dur 1R hors échantillon (2010–2015) : échec

*2026-10-31. Protocole : [PREREGISTRATION_19.md](../PREREGISTRATION_19.md) (commit `99a4f5c`, avant calcul). Code : [run_prereg19.py](../run_prereg19.py), qui réutilise [run_s1_r_stop_vbt.py](../run_s1_r_stop_vbt.py). Résultats : [results/prereg19/](../results/prereg19/). Compteur global : 1 485.*

Trades du 2010-09-01 au 2015-12-31 (1 343 séances), NQ 1 contrat, 2,25 $ + 1 tick par côté. vectorbt et la boucle d'origine donnent les mêmes trades (écart total ≤ 0,06 $).

| Réglage | Trades | R net / trade [IC 95 %] | p unilatéral | R brut | 2010-09→2012 / 2013–2015 | Sharpe $ [IC 95 %] | $/an |
|---|---|---|---|---|---|---|---|
| **Principal : plancher 0,5 % + stop 1R** | 885 | +0,030 [−0,026 ; +0,090] | 0,154 | +0,079 | +0,005 / +0,052 | 0,57 [−0,19 ; 1,33] | +2 013 |
| S1 d'origine (sans stop) | 878 | n. s. (R sans plancher) | 0,55 | — | — | 0,55 [−0,21 ; 1,33] | +2 009 |
| Plancher 0,3 % + stop 1R | 899 | +0,052 [−0,035 ; +0,147] | 0,141 | +0,132 | +0,027 / +0,074 | 0,60 [−0,20 ; 1,39] | +2 093 |
| Principal au coût MNQ (0,60 $ + 1 tick) | 885 | +0,004 | 0,43 | +0,079 | −0,026 / +0,031 | 0,22 | +77 |

## Verdict pré-enregistré

**Échec** : R net positif mais p = 0,15 > 0,05. Les deux sous-périodes sont positives, mais la première l'est à peine (+0,005 R).

- Sur 2016–2026, la même règle faisait +0,106 R par trade (t 4,0) et un Sharpe en dollars de 1,12. Hors échantillon, il reste environ un tiers de l'effet en R. Le Sharpe en dollars tombe à 0,57, et son IC inclut zéro.
- Le stop dur n'apporte rien hors échantillon : Sharpe $ 0,57 contre 0,55 pour S1 d'origine, pour le même P&L (+10,7 k$).
- Les coûts pèsent : le brut fait +0,079 R, le net +0,030 R. Au coût MNQ, l'avantage disparaît (+0,004 R). Avec un NQ à 2 000 points, R ≈ 10 points, donc l'aller-retour coûte 0,05 à 0,11 R.
- DSR approché (N = 1 485) : 0,000 pour tous les réglages.
- Années : 2010 −15 R, 2011 −4, 2012 +21, 2013 +5, 2014 +7, 2015 +13.

Conséquence : la variante va au registre des échecs. La bande de bruit M2 sur NQ reste rejetée ; seul un test sur le holdout postérieur au 2026-08-28 pourrait la rouvrir.
