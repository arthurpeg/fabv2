# Fix de Londres à 16h en fin de mois (Melvin et Prins, SSRN 2019274) : rapport

*Protocole : [PREREGISTRATION_7.md](../PREREGISTRATION_7.md), commit `e2a4428`, antérieur à tout calcul de P&L. Code : `fxfix/`, `run_fx_fix.py`, tests `tests/test_fx_fix.py` (commit `4f1b080`). Sorties : `results/fx_fix/` (`run.log`, `vbt_summary.csv`, `vbt_daily_net.parquet`, trades, `equity.png`). **9 nouveaux tests, compteur à 201.***

**Données.** Futures CME 6E, 6B, 6A et 6J, 1 minute, 2016-01 → 2026-08. L'échantillon est entièrement postérieur à la réforme du fix de 2015. Les indices actions du résultat B sont l'ES ajusté des roulements (cache) et les CFD HistData du DAX, de l'ASX et du Nikkei. Il n'y a pas d'indice britannique : 6B est exclu de B.

## Verdict

| Configuration principale | Gain net moyen par trade | 2016-2020 / 2021-2026 | Bootstrap p | Permutation p | DSR (N = 9) | Verdict |
|---|---|---|---|---|---|---|
| **A\*** : retournement, fin de mois, entrée 16:05, sortie à 12:00 le lendemain | +2,41 pips (n = 502) | −2,39 / +6,60 | 0,28 | 0,16 | 0,09 | ❌ |
| **B\*** : flux de couverture, fin de mois, 13:00 → 16:00 | −3,08 pips (n = 373) | +0,82 / −6,55 | 0,93 | 0,92 | 0,00 | ❌ |

Les deux configurations échouent aux 4 critères. Le Reality Check sur les 9 règles donne p = 0,46.

## A : retournement après le fix

**La régression du papier, refaite sur 2016-2026** (n = 9 162 jours × paires, entrée à 16:00) :
- coefficient tous jours b = −0,000 (p = 0,996), contre −0,178 dans le papier ;
- coefficient additionnel de fin de mois c = −0,254 (p = 0,13), contre −0,518 ;
- R² = 0,10 %.

**Lecture.** Le retournement quotidien a disparu après 2015. En fin de mois, il en reste environ la moitié, sans significativité.

**Par trade, coût standard (1 tick + 5 $) :**

| Règle | n | Brut moyen | Net moyen | PF | 2016-2020 net | 2021-2026 net |
|---|---|---|---|---|---|---|
| Fin de mois, entrée E0 (16:00) | 502 | +4,98 | +3,70 | 1,21 | −0,81 | +7,64 |
| Fin de mois, entrée E1 (16:01) | 502 | +5,54 | +4,25 | 1,24 | −0,01 | +7,97 |
| **Fin de mois, entrée E5 (16:05)** | 502 | +3,70 | +2,41 | 1,13 | −2,39 | +6,60 |
| Autres jours, entrée E5 | 8 660 | +0,01 | −1,27 | 0,93 | −1,07 | −1,46 |

- Le contrôle est **confirmé** : le fade est nul les autres jours et positif en fin de mois (+3,70 contre +0,01 pip brut en E5). La structure prédite par le papier est donc là.
- Mais l'effet est trop petit pour le bruit. L'écart type d'un trade est d'environ 55 pips pour une détention d'environ 20 heures. Avec 502 trades, l'erreur type est d'environ 2,5 pips.
- L'effet est concentré sur **2021-2026** (aucune année perdante sur 6) et absent sur 2016-2020 (2 années perdantes sur 5).
- Par paire (E5) : GBP +4,4 et JPY +4,2 pips nets, EUR +1,6, AUD −0,6.
- Fins de trimestre seules : +2,0 pips nets (n = 165). Ce n'est pas plus fort que les autres fins de mois.

**Exécutabilité.** On perd environ 1,3 à 1,8 pip à attendre la fin de la fenêtre du fix : brut de +5,0 en E0, +5,5 en E1, +3,7 en E5.

**Backtest vectorbt au coût standard** (1/4 du capital par paire, sans levier) :
- A\* : +2,05 % sur 10,7 ans, soit +0,19 %/an, Sharpe 0,17, drawdown max −2,65 % ;
- variante E1 : +4,2 %, Sharpe 0,34.

La stratégie n'est exposée qu'un jour par mois : même si l'effet était réel, le rendement annuel resterait marginal sans fort levier.

## B : flux de couverture avant le fix

**Régression** r_devise(13:00 → 16:00) = a + b·x sur les jours de fin de mois, n = 373 : b = −0,0019 (p = 0,68), R² = 0,05 %. Le papier trouve b < 0 avec un R² de 2 %. Le signe est le bon, mais il n'y a aucun pouvoir explicatif.

**Par trade :**
- −1,97 pip brut, −3,08 pips net.
- Légèrement positif sur 2016-2020 (+0,82), clairement négatif sur 2021-2026 (−6,55, 5 années perdantes sur 6).
- Négatif sur EUR et JPY, nul sur AUD.
- Le contrôle hors fin de mois est à +0,28 pip brut, donc pas plus faible : la prédiction de structure n'est **pas** confirmée.

**vectorbt :** −2,26 %, Sharpe −0,44.

**Limites propres à B :**
- les indices sont des CFD HistData relevés à la clôture locale ;
- le DAX est remplacé par l'Euro Stoxx 50 du 2020-06 au 2023-12 ;
- il n'y a pas de couple GBP / FTSE ;
- on ne mesure que la performance relative contre les États-Unis, et non contre la moyenne transversale du G10 comme le papier.

L'échec de B est donc moins concluant que celui de A.

## Conclusion

- Après la réforme de 2015, sur futures CME, le flux directionnel avant le fix (B) n'est pas détectable.
- Le retournement quotidien (A) a disparu. Il ne reste qu'un retournement de fin de mois d'environ 4 pips brut, au bon signe et nul les autres jours, mais non significatif (p entre 0,16 et 0,28 selon le test) et absent sur 2016-2020.
- Rien de tradable au sens des critères. Si l'on veut y revenir, la seule piste est A en fin de mois, sur 2021+. Elle demanderait un nouveau pré-enregistrement et des données au comptant ou une autre source pour une vraie réplication. Avec environ 50 trades par an, il faudrait plusieurs années de données nouvelles pour trancher.
