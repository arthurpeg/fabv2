# Asymétrie intraday ancrée sur l'ouverture (Valenti 2026, SSRN 6074846) : rapport

*Protocole : [PREREGISTRATION_8.md](../PREREGISTRATION_8.md), commit `3da7b75`, antérieur à tout calcul de P&L. Code : `asym/`, `run_asym.py`, tests `tests/test_asym.py` (commit `05bb9d5`). Sorties : `results/asym/` (`run.log`, `vbt_summary.csv`, `vbt_daily_net.parquet`, trades, `equity.png`). **7 nouveaux tests, compteur à 208.***

**Données.** ES (futures CME 1 minute, séance régulière 09:30-16:00 ET) comme proxy de SPY, 2016-01 → 2026-08. Réplication sur le DAX (CFD HistData, 09:00-17:30 Berlin). 2016-2025 recoupe l'échantillon du papier : c'est une réplication sur un autre instrument et un autre marché, pas un test hors échantillon dans le temps.

## Verdict : ❌ (rejeté), mais c'est le signal le plus solide des trois papiers testés

ES_asym (long si Asym_O < 0, short sinon, de l'ouverture à la clôture du lendemain), au coût de 1 tick + 5 $ :

| Critère | Résultat | |
|---|---|---|
| 1. Positif sur les deux moitiés | +3,98 pb/trade sur 2016-2020, +2,79 sur 2021-2026 (PF 1,16 / 1,10) | ✅ |
| 2. Bootstrap stationnaire | p = 0,021 | ✅ |
| 3. Permutation du sens | p = 0,005 | ✅ |
| 4. DSR, N = 7 | 0,58 (0,05 avec N = 208) | ❌ |
| 5. Apport par rapport au contrariant ouverture → clôture | b(Asym) = +0,006, t = +0,05 | ❌ |

**vectorbt (1×, cible ±100 %)** : +116 % sur 10,7 ans, soit +8,2 %/an, Sharpe 0,61, drawdown max −23 %. Brut : +10,7 %/an, Sharpe 0,80. L'avantage disparaît vers 4 à 5 pb de coût aller-retour (−1,6 %/an à 5 pb).

**Concentration.** Les gains viennent surtout de deux années de stress : **2020 (+54,6 %)** et **2025 (+24,6 %)**. Les 9 autres années donnent au total environ +14 % (2017 et 2018 négatives). C'est cohérent avec le papier (« la jambe courte paie en période de stress »), mais le résultat dépend donc de quelques épisodes.

## Pourquoi le rejet

1. **Multiplicité.** Avec N = 7 essais, le Sharpe de 0,61 n'est pas assez élevé pour le DSR (0,58). Le Reality Check sur les 7 règles donne p = 0,062.
2. **Asym n'apporte rien en plus du rendement ouverture → clôture du jour** :
   - dans la régression r_{t+1} = a + b·Asym + c·ln(C/O) avec erreurs de Newey-West, b = +0,006 (t = 0,05) et c = −0,111 (t = −0,92) ;
   - pris seuls, Asym (t = −1,80) et ln(C/O) (t = −2,22) portent la même information ;
   - corrélation des deux signaux : 0,90, signe identique 85 % des jours.

   Linéairement, le signal du papier est le retournement du jour, rien de plus. En règle de signe, Asym fait mieux que ln(C/O) (+3,35 contre +1,18 pb/trade). Mais cet écart entre deux versions d'un même signal ne repose sur aucun test d'apport significatif.
3. **Pas de réplication sur le DAX** : −0,82 pb/trade à 2 pb de coût. Légèrement positif sur 2016-2020 (+1,08), négatif sur 2021-2026 (−2,60). Bootstrap p = 0,67.

## Comparaison avec le papier (moyennes annualisées sur les seuls jours actifs, net)

| | Papier (SPY 2002-2025) | ES 2016-2026 |
|---|---|---|
| Long conditionnel (Asym < 0) | 16,9 % | 14,5 % |
| Short conditionnel (Asym > 0) | 8,9 % | 2,3 % |
| Combiné | 12,9 % | 8,4 % |
| Long inconditionnel, ouverture → clôture (brut) | 4,1 % | 6,1 % |
| Ancré sur la clôture de la veille | 4,6 % | 0,6 % |
| Ancré sur la clôture du jour | −9,5 % | −5,9 % |
| Contrariant ouverture → clôture | 11,0 % | 3,0 % |

Les trois prédictions de structure du papier sont vérifiées : jambe longue plus forte que la courte, ancrage sur la clôture du jour perdant, ancrage sur la clôture de la veille plus faible. La jambe courte est nettement plus faible que dans le papier : +0,9 pb/trade, et nulle sur 2021-2026.

**Jambe longue seule** (ES_asym_long) : +5,74 pb/trade, 1 année perdante sur 11, vectorbt +7,1 %/an, Sharpe 0,70, drawdown max −16 %, bootstrap p = 0,007.
- Elle bat le long inconditionnel ouverture → clôture, qui fait environ 2,4 pb/jour brut. Mais elle encaisse aussi la dérive haussière de l'indice, ce qui gonfle son Sharpe.
- Son DSR est de 0,69 (N = 7).
- La permutation du sens n'a pas de sens pour une jambe à sens unique (p = 1, sans valeur).
- Un test propre serait : jours Asym < 0 contre jours Asym > 0 en long. Il n'a pas été pré-enregistré.

**Exécutabilité** : entrer à 09:31 au lieu de 09:30 ne change rien (+3,37 contre +3,35 pb).

## Conclusion

- Sur ES 2016-2026, le signal de Valenti réplique dans le bon sens. Il passe les trois tests de significativité simples (deux moitiés positives, bootstrap, permutation), ce qu'aucun des deux tests précédents n'a fait.
- Mais il ne survit pas à la correction pour multiplicité (DSR). Surtout, il n'apporte rien de mesurable au simple retournement du rendement ouverture → clôture de la veille. Il ne réplique pas sur le DAX. Ses gains sont concentrés en 2020 et 2025.
- C'est un effet connu de retournement de court terme, coûteux à 5 pb, pas un nouvel edge.
- Piste restante, à pré-enregistrer à part si on veut la poursuivre : la jambe longue conditionnelle (long ouverture → clôture seulement après une séance tirée vers le bas), testée contre le long inconditionnel, sur des données nouvelles (2026-09+) ou sur un autre indice américain (NQ, YM).
