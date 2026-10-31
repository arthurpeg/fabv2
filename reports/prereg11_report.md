# Pré-enregistrement n° 11 — résultat : SUCCÈS (avec une réserve majeure)

*2026-10-30. Règle et critères : [PREREGISTRATION_11.md](../PREREGISTRATION_11.md). Code : [run_prereg11.py](../run_prereg11.py). Données : Databento `GLBX.MDP3` `ohlcv-1m` 2010-06 → 2015-12 (19,93 $), raboutées à la série 2016+ ; 23 roulements détectés par actif sur 2010–2015. Résultats : [results/prereg11/](../results/prereg11/). Compteur global : 1 459.*

Règle (inchangée depuis le n° 10) : NQ, momentum 12-1, entrée 20:00 ET, SL 2 ATR / TP 5 ATR (ATR 14 sur M15), sortie à 9:30 ET, coût 1 tick + 5 $. Période de test : nuits du 2011-07-01 au 2015-12-31, jamais vues auparavant.

## Test principal : NQ, compte 20:00

| | Trades | R/trade [IC 95 %] | p unilatéral | 2011-07 → 2013 | 2014 → 2015 | R/an 2012–2015 | Max DD |
|---|---|---|---|---|---|---|---|
| Net | 1 115 | **+0,116 [+0,037 ; +0,198]** | **0,0015** | +0,091 | +0,147 | +32,4 | −22 R |
| Brut | 1 115 | +0,188 [+0,110 ; +0,270] | — | +0,171 | +0,209 | +50,8 | −17 R |

Les trois critères sont remplis (R > 0, p < 0,05, les deux sous-périodes positives) : **verdict pré-enregistré, succès.** Sur 2016–2026, la même règle faisait +0,084 R/trade ; l'effet hors échantillon est du même ordre, un peu plus fort.

R par année (net) : 2011 (juillet → décembre) −1,0 ; 2012 +31,0 ; 2013 +26,3 ; 2014 +43,3 ; 2015 +29,1.

## Tests secondaires (rapportés tels quels)

| Test | R [IC 95 %] (net) | p | Brut |
|---|---|---|---|
| NQ bloc 19:00–21:00 (R/nuit) | +0,349 [+0,145 ; +0,562] | 0,003 | — |
| ES compte 20:00 | −0,012 [−0,089 ; +0,066] | 0,61 | +0,093 [+0,017 ; +0,170] |
| YM compte 20:00 | +0,058 [−0,019 ; +0,137] | 0,07 | +0,135 [+0,057 ; +0,214] |

## Réserve majeure : ce qui a été validé, exactement

- **Le momentum 12-1 a été positif tous les mois de 2011 à 2015** : 100 % des trades NQ sont longs. Le filtre de direction n'a jamais agi. Ce qui est validé hors échantillon, c'est « **long NQ à 20:00 ET, SL 2 ATR / TP 5 ATR, sortie 9:30** », pas la capacité du momentum à éviter les baisses.
- 2011–2015 est une forte période haussière pour le Nasdaq-100. Le résultat confirme la prime de nuit de NQ dans un marché haussier ; il ne dit rien du comportement en marché baissier prolongé (2018 T4, 2022), où la règle dépend du filtre.
- Sur ES, l'effet existe en brut mais disparaît après coût ; sur YM, il est positif mais non significatif après coût. Comme en 2016–2026, NQ ressort nettement plus fort que les deux autres indices.
- Coût fixe de 1 tick : les spreads de nuit étaient plus larges en 2011–2012, donc le net du début de période est probablement un peu optimiste (réserve écrite avant calcul).
- Databento signale 3 jours de qualité dégradée (11–13 juin 2014), gardés tels quels.
