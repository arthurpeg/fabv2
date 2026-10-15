# La première heure FX après la reprise (Tolušić 2026), sur futures CME : rapport

*Exécuté le 2026-10-15 selon [PREREGISTRATION_6.md](../PREREGISTRATION_6.md) (commit `06ff89d`, antérieur à tout calcul de P&L). Papier : SSRN 7135159, [texte](../papers/ssrn_2026-10-13/c/ssrn-7135159.txt). Code : [fxreopen/](../fxreopen), [run_fx_reopen.py](../run_fx_reopen.py), tests : [tests/test_fx_reopen.py](../tests/test_fx_reopen.py). Sorties : [results/fx_reopen/](../results/fx_reopen) (`run.log`, `summary.csv`, `tests.csv`, `breakeven.csv`, `daily_net.parquet`, trades). **18 nouveaux essais, compteur global à 192.***

## Verdict

**Non. Le seuil de 5 pips ne survit ni à un spread réaliste ni à une entrée décalée. Il ne survit même pas à un coût de 2 pips.**

- **Configuration principale** (seuil de 5 pips, entrée à 18:01 ET, sortie à +60 min, 3 pips aller-retour) : perte de **−2,55 pips par trade**, PF de 0,52, perdante les 11 années sur 11 et sur chacune des 4 paires. Les 4 critères pré-enregistrés échouent (bootstrap p = 1,00, permutation p = 0,057, DSR = 0,000).
- **L'effet brut existe, mais il est 3 à 5 fois plus petit que dans le papier** : +1,10 pip par trade au seuil de 5 pips avec l'entrée du papier (open de 18:00), contre +3,82 pips nets annoncés.
- **Presque tout cet effet tient dans la première minute.** Entre l'open de 18:00 (prix de l'enchère) et l'open de 18:01, le prix revient déjà de **0,97 pip** dans le sens du fade, au seuil de 5 pips. Un trader qui entre une minute après avoir vu le gap ne récupère que +0,45 pip brut. En entrant à 18:05 ou 18:15, il en récupère environ +0,8.
- **Spread de point mort** : pour toutes les entrées exécutables, il est **< 1 pip aller-retour** (de 0,45 à 0,85 pip au seuil de 5 pips). C'est sous le coût minimal d'un aller-retour en futures (1 tick + commission, soit 0,9 à 2 pips), et très loin des 2 à 8 pips d'un spread au comptant au rollover.
- Le papier annonçait un PF de 4,69 au seuil de 5 pips : on mesure **1,31 en brut**, et **0,63 à 3 pips** de coût.

## 1. Ce qui a été testé

| | |
|---|---|
| Données | Futures CME 6E, 6B, 6A, 6J (Databento, 1 minute, **prix de transactions**), 2016-01-03 → 2026-08-28. 6J inversé en USDJPY. **USDCAD et USDCHF absents** (ni 6C ni 6S dans `Cotations`). Pas de FX au comptant dans le dépôt. |
| Reprise | Globex FX s'arrête de 17:00 à 18:00 ET. **La reprise est à 18:00 ET**, à la première barre dans [18:00, 18:05) après une pause d'au moins 60 minutes. Week-ends et fermetures anticipées des jours fériés sont inclus. Environ 2 730 reprises par paire. |
| Gap | open(barre de reprise) − close(dernière barre avant la pause), en pips |
| Fuseau | UTC → `America/New_York`. Reprise à 22:00 UTC l'été et 23:00 UTC l'hiver, testée sur les semaines où l'heure d'été américaine et l'européenne divergent (la règle HistData ne concerne pas ces fichiers) |
| Roulements | Le contrat continu bascule sur une barre de 00:00 UTC. Tous les sauts de plus de 0,15 % à 00:00 UTC tombent dans les fenêtres du 1er au 21 de mars, juin, septembre et décembre, **0 en dehors**. Tout gap ou trade qui traverse une telle barre est exclu. |
| Règles | Fade si \|gap\| ≥ 1, 2 ou 5 pips. Entrées : E0 (open de 18:00, la règle du papier), E1 (18:01), E5 (18:05), E15 (18:15). Sortie à l'entrée nominale + 60 min |
| Contrôles | (a) même fade aux 22 frontières horaires hors reprise, au coût standard (1 tick + 5 $). (b) entrée E0, détention jusqu'au close de 16:59 ET |
| Coûts | 0, 2, 3 (**principal**), 5 et 8 pips aller-retour |

## 2. Anatomie du gap : elle se retrouve

| Paire | \|gap\| moyen à la reprise | médian | ≥ 1 pip | ≥ 5 pips | \|gap\| intrajournalier moyen* |
|---|---|---|---|---|---|
| EURUSD (6E) | 3,62 | 1,50 | 59 % | 14 % | 0,55 |
| GBPUSD (6B) | 5,82 | 3,00 | 68 % | 25 % | 1,09 |
| AUDUSD (6A) | 3,26 | 2,00 | 58 % | 17 % | 0,75 |
| USDJPY (6J) | 6,87 | 2,51 | 78 % | 29 % | 0,86 |

\* Sur les frontières dont le gap n'est pas nul. Avec un tick de 6B égal à 1 pip, tout gap non nul y fait au moins 1 pip.

Le papier annonce 4,8 pips et 74 % au-dessus de 1 pip au comptant. Le future à 18:00 ET donne le même ordre de grandeur, avec une heure de cotation au comptant de plus dans le gap. La reprise est bien un événement à part : son volume par minute est de 81 à 141 contrats à 18:00, contre 21 à 47 à 18:01. **C'est l'enchère d'ouverture de Globex.**

## 3. Résultats : fade de la reprise, sortie à +60 min

Gain moyen par trade en pips. « Brut » = coût de 0. PF à 3 pips.

| Seuil | Entrée | n | Brut 2016-18 | Brut 2019-26/01 | Brut 2026-02+ | PF brut | **Net à 3 pips** | PF à 3 pips | Années < 0 à 3 pips | p de permutation |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | E0 | 7 718 | +0,71 | +0,59 | −0,44 | 1,22 | −2,43 | 0,43 | 11/11 | 0,0000 |
| 1 | E1 | 7 690 | +0,44 | +0,02 | −0,58 | 1,05 | −2,88 | 0,35 | 11/11 | 0,17 |
| 1 | E5 | 7 653 | +0,46 | +0,21 | −0,18 | 1,11 | −2,73 | 0,36 | 11/11 | 0,005 |
| 1 | E15 | 7 638 | +0,67 | +0,23 | +0,34 | 1,15 | −2,63 | 0,39 | 11/11 | 0,002 |
| 2 | E0 | 5 472 | +0,82 | +0,79 | −0,32 | 1,27 | −2,25 | 0,49 | 11/11 | 0,0000 |
| 2 | E1 | 5 452 | +0,51 | +0,04 | −0,37 | 1,07 | −2,82 | 0,39 | 11/11 | 0,12 |
| 2 | E5 | 5 432 | +0,52 | +0,28 | +0,39 | 1,14 | −2,63 | 0,40 | 11/11 | 0,003 |
| 2 | E15 | 5 408 | +0,45 | +0,30 | +0,92 | 1,14 | −2,62 | 0,41 | 11/11 | 0,004 |
| 5 | E0 | 2 256 | +1,28 | +1,16 | −0,92 | 1,31 | −1,90 | 0,63 | 11/11 | 0,0000 |
| **5** | **E1** | **2 241** | **+0,89** | **+0,24** | **−0,79** | **1,13** | **−2,55** | **0,52** | **11/11** | **0,057** |
| 5 | E5 | 2 246 | +0,88 | +0,77 | +0,35 | 1,25 | −2,21 | 0,55 | 10/11 | 0,001 |
| 5 | E15 | 2 229 | +0,88 | +0,76 | +1,40 | 1,26 | −2,15 | 0,56 | 11/11 | 0,001 |

Au seuil de 5 pips, en E0 (le cas le plus favorable), le net vaut −0,84 pip à 2 pips de coût et −3,90 à 5 pips. Le détail par coût et par fenêtre est dans `results/fx_reopen/summary.csv`.

Le papier, lui, annonce au seuil de 5 pips sur 2019-2026 : PF de 4,69, 80 % de trades gagnants, +3,82 pips **nets**, aucune année perdante. Sur le future, même en brut et en E0 : PF de 1,29, 57,5 % de gagnants, +1,16 pip, une année perdante sur huit.

### Spread de point mort (aller-retour, en pips)

| Seuil | E0 | E1 | E5 | E15 |
|---|---|---|---|---|
| 1 | 0,57 | 0,12 | 0,27 | 0,37 |
| 2 | 0,75 | 0,18 | 0,37 | 0,38 |
| 5 | **1,10** | **0,45** | **0,79** | **0,85** |

Par paire, au seuil de 5 pips en E1 : AUDUSD +1,26, GBPUSD +0,66, EURUSD +0,48, USDJPY −0,31. Même la meilleure paire reste sous 1,5 pip.

### Où passe l'effet : la première minute

Mouvement moyen dans le sens du fade entre l'open de 18:00 et l'entrée décalée, en pips (gain brut E0 entre parenthèses) :

| Seuil | → 18:01 | → 18:05 | → 18:15 |
|---|---|---|---|
| 1 | 0,58 (0,57) | 0,58 | 0,48 |
| 2 | 0,73 (0,74) | 0,72 | 0,62 |
| 5 | 0,97 (1,08) | 0,98 | 0,82 |

**La correction est déjà faite à 18:01.** Le prix de l'enchère dépasse, puis revient en une minute. Pour les seuils de 1 et 2 pips, cette première minute représente **la totalité** du gain de l'heure. C'est exactement le risque d'exécutabilité soulevé dans la commande (cf. SSRN 5139307) : le gain du papier se trouve dans un prix qu'on ne peut pas obtenir une fois le gap connu. Pour l'obtenir, il faudrait participer à l'enchère, à l'aveugle ou au vu du prix indicatif d'ouverture, que ces données n'ont pas.

Après 18:01, il reste un retour à la moyenne **statistiquement réel** en E5 et E15 : p de permutation de 0,001 à 0,005, environ +0,8 pip au seuil de 5 pips, de signe stable sur les trois fenêtres. Il est cependant inférieur à un aller-retour même au coût d'un future en temps normal.

## 4. Contrôles

**(a) Heures intrajournalières (coût standard 1 tick + 5 $)** : la prédiction du papier est confirmée.

| Seuil | n | Brut | Net | PF net |
|---|---|---|---|---|
| 1 | 53 646 | +0,03 | −1,56 | 0,73 |
| 2 | 3 135 | −0,82 | −2,51 | 0,71 |
| 5 | 87 | −16,6 | −18,2 | 0,38 |

Aux autres heures, le gain brut est nul, voire négatif : les gros gaps intrajournaliers sont des sauts d'information, et ils continuent. **Le contraste entre la reprise et les autres heures existe**, mais seulement en brut, et sur un effet d'environ 1 pip, pas de 4.

**(b) Détention jusqu'au close de 16:59 ET (entrée E0)**

| Seuil | PF 1 h, brut | PF close, brut | Brut 1 h | Brut close | Net close à 3 pips (2016-18 / 2019-26) |
|---|---|---|---|---|---|
| 1 | 1,22 | 1,05 | +0,57 | +1,12 | −2,92 / −1,87 |
| 2 | 1,27 | 1,08 | +0,75 | +1,83 | −2,61 / −0,94 |
| 5 | 1,31 | 1,19 | +1,10 | +4,43 | +1,57 / −0,09 |

La prédiction du papier, un PF plus bas pour la détention jusqu'au close, est confirmée. Mais le gain moyen en pips est **plus grand** quand on garde la position jusqu'au close, parce que la variance d'une journée entière dilue le PF. Pour le close au seuil de 5 pips, le net à 3 pips est positif sur toute la période (+1,43 pip, permutation p = 0,007), mais nul sur 2019-2026 (−0,09), avec un bootstrap p de 0,12 et un DSR de 0. **Ce n'est pas un candidat.**

## 5. Tests et corrections pour tests multiples

| Test (configuration principale, 3 pips) | Résultat | Critère |
|---|---|---|
| 1. Net > 0 et PF > 1 sur 2016-2018 et sur 2019-2026-01 | −2,11 (PF 0,55) / −2,76 (PF 0,51) | ❌ |
| 2. Bootstrap stationnaire, moyenne journalière > 0 | p = 1,00 | ❌ |
| 3. Permutation du sens | p = 0,057 | ❌ |
| 4. DSR, N = 18 | 0,000 (N = 192 : 0,000) | ❌ |
| Scénarios défavorables à 5 et à 8 pips | −4,55 et −7,55 pips par trade | — |
| Reality Check de White sur les 18 règles | p = 0,72 (2019-2026 : p = 0,90), meilleure règle = close au seuil de 5 pips | papier : p < 0,0005 |

- **Entrées décalées (lecture secondaire)** : aucune des 6 variantes E5 et E15 ne reste positive à 3 pips sur l'une ou l'autre fenêtre.
- **Garde-fou (PF > 4, gagnants > 75 %, Sharpe journalier > 3)** : aucun déclenchement. Le contraste avec le papier, qui annonce un PF de 4,69 et 80 % de gagnants, est lui-même un signal.

## 6. Le coût réaliste à la reprise

L'estimateur d'Abdi et Ranaldo (2017) sur barres 1 minute donne un spread effectif de **0,56 à 0,84 pip à 18:00-18:04 ET**, contre 0,27 à 0,50 pip de 02:00 à 16:00 ET : le carnet est donc **1,5 à 2 fois plus large** à la reprise. Sur des barres 1 minute discrétisées au tick, cet estimateur est biaisé vers le bas (certaines années donnent 0). C'est un **plancher**.

En futures, un aller-retour réaliste comprend :
- un demi-spread de reprise à l'entrée (environ 0,3 à 0,4 pip) ;
- un demi-spread normal à la sortie (environ 0,15 à 0,25 pip) ;
- la commission (environ 0,4 pip pour 6E à 5 $).

Soit **environ 1 à 1,5 pip**. Le spread de point mort des entrées exécutables (de 0,45 à 0,85 pip) reste en dessous, même dans ce scénario de futures le plus favorable. Au comptant chez un courtier, le spread au rollover de 17:00 fait couramment plusieurs pips. Les coûts de 2 à 8 pips de la grille sont donc réalistes pour le comptant, et **tout est perdant dès 2 pips**.

## 7. Pourquoi le papier trouve 3 à 4 fois plus

Hypothèses, non testées ici faute de données au comptant :
1. **Barres de courtier au bid** (les archives MT4 sont en général des bid). À 17:00 NY, le spread du courtier s'élargit pendant quelques minutes : le bid baisse, puis revient. Ce mouvement crée mécaniquement un « gap » suivi d'un « retour », qu'aucun trader ne peut capter, puisqu'il achète au ask. Un spread fixe de 0,6 à 1,4 pip ne corrige pas cet effet. C'est cohérent avec les gaps de 4,8 pips en moyenne « au comptant », sur un marché qui ne ferme pas.
2. **Prix d'enchère non exécutable** : sur le future, où les prix sont des transactions, l'effet qui reste vient du premier prix, et il disparaît en une minute.
3. Le papier reconnaît lui-même que son point mort est une dégradation de 1,06 pip au seuil de 1 pip. Sur le future, la dégradation mesurée entre 18:00 et 18:01 vaut 0,58 pip au seuil de 1 pip, pour un gain brut total de 0,57 : il ne reste rien.

## 8. Limites

- **Ce n'est pas la règle au comptant.** L'heure h0 du papier (17:00-18:00 ET) tombe dans la pause du future. On teste ici la reprise du future, à 18:00 ET, que le papier invite lui-même à tester (« other conventions relocate the reopen »). Le test décisif de la règle au comptant demanderait des données bid **et** ask au comptant (ticks HistData, ou Dukascopy) autour de 17:00 NY, pour mesurer à la fois l'élargissement et le prix exécutable.
- 4 paires sur 6.
- Pas de 2014-2015 : la « pré-période » ne couvre que 2016-2018.
- Coûts fixes par scénario : le spread réel à la reprise varie d'un jour à l'autre, et plus encore les jours de gros gap.
- Le DSR utilise la variance des Sharpe des 18 essais. Le SR₀ obtenu (4,65) est gonflé par les variantes très négatives, mais tous les Sharpe sont de toute façon négatifs au coût principal, sauf celui du close au seuil de 5 pips (+0,30).
- Détail d'implémentation non précisé dans le pré-enregistrement : une entrée décalée ne réutilise jamais la barre de reprise (si le premier échange a lieu à 18:02, E1 entre sur la barre suivante). En hiver, E0 sort sur la barre de 00:00 UTC ; les séances d'hiver des fenêtres de roulement (du 1er au 21 décembre, début mars) sont donc exclues pour E0, comme le prévoit la règle des roulements.

## Reproduire

```bash
uv run pytest tests/test_fx_reopen.py
uv run python run_fx_reopen.py      # environ 10 min → results/fx_reopen/
```
