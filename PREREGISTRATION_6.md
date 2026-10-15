# Pré-enregistrement n° 6 : la première heure FX après la reprise quotidienne (Tolušić 2026)

*2026-10-15, avant tout calcul de rendement ou de P&L. Papier : Tolušić (2026), « The First Hour: How Foreign Exchange Absorbs Its Daily Gap », SSRN 7135159, texte intégral : [papers/ssrn_2026-10-13/c/ssrn-7135159.txt](papers/ssrn_2026-10-13/c/ssrn-7135159.txt). Classé premier des 24 papiers de [papiers_ssrn_ohlcv_2026-10-13.md](papiers_ssrn_ohlcv_2026-10-13.md).*

## Ce que dit le papier

- Données : barres H1 d'un courtier, 6 paires USD (EURUSD, GBPUSD, AUDUSD, USDCAD, USDCHF, USDJPY), 2014-01 → 2026-01. Jour serveur aligné sur la clôture de New York : h0 = 17:00-18:00 ET.
- Règle : gap = open(h0) − close(barre précédente), en pips. Si |gap| ≥ seuil, on fade à l'open de h0 (vente sur gap haussier, achat sur gap baissier), sortie au close de h0. Les gaps du week-end sont inclus.
- Résultats annoncés, nets d'un **spread fixe de 0,6 à 1,4 pip** :
  - 2019-2026 : PF de 2,63 / 3,16 / 4,69 aux seuils de 1 / 2 / 5 pips, gain moyen de +1,92 / +2,40 / +3,82 pips par trade, aucune année perdante ;
  - 2014-2018 : PF de 1,25 / 1,47 / 1,73 ;
  - heures 1 à 23 : perdantes partout ;
  - sortie au close du jour : PF de 2,63 → 1,18 ;
  - Reality Check sur 18 règles : p < 0,0005.
- Limites reconnues par l'auteur : le spread est supposé fixe à l'instant précis où il s'élargit le plus, et l'exécutabilité de l'open d'archive n'est pas vérifiée. Le point mort annoncé est une dégradation d'exécution de 1,06 pip.

## Données : futures CME, pas le comptant

Le dépôt n'a **pas de FX au comptant** : HistData n'y contient que des CFD d'indices. Sur demande de l'utilisateur, on utilise les futures FX de `D:/quant-data/Cotations/forex` (Databento GLBX, 1 minute, prix de **transactions** réelles, 2016-01-03 → 2026-08-28, contrat continu `.v.0`).

| Paire du papier | Future | Pip | Traitement |
|---|---|---|---|
| EURUSD | 6E | 0,0001 | tel quel |
| GBPUSD | 6B | 0,0001 | tel quel |
| AUDUSD | 6A | 0,0001 | tel quel |
| USDJPY | 6J | 0,01 JPY | **prix inversé** (1/p, high et low permutés) pour travailler en USDJPY |
| USDCAD, USDCHF | — | — | **absents** (pas de 6C ni de 6S dans `Cotations`) |

**Conséquence de structure, à garder en tête dans toute la lecture.** Globex FX arrête de coter de 17:00 à 18:00 ET (16:00-17:00 CT) chaque jour. L'heure h0 du papier (17:00-18:00 ET, au comptant) tombe donc **entièrement dans la pause du future** : on ne peut pas la trader. La reprise du future, à **18:00 ET**, est une vraie enchère d'ouverture (phase de pré-ouverture puis appariement Globex). Son gap couvre la clôture de 16:59 ET, le rollover au comptant de 17:00 et l'heure fine de 17:00 à 18:00.

C'est exactement le test que le papier réclame (« other conventions relocate the reopen and should reproduce the contrast at their own boundary »). Mais c'est un test du **mécanisme** (une enchère de liquidité quotidienne absorbée dans l'heure), pas de la règle au comptant. Un échec ici n'infirmerait pas la règle au comptant chez un courtier. Une réussite ne la validerait pas non plus.

**Avantage pour l'exécutabilité** : les prix sont des transactions avec volume. L'open de 18:00 est le prix de l'enchère, auquel des contrats ont réellement changé de main.

## Alignement temporel

- Horodatages Databento en UTC, convertis en `America/New_York` (la règle HistData d'heure d'été européenne ne s'applique pas ici). Le CME suit l'heure d'été américaine : la reprise est à 18:00 ET toute l'année, soit 22:00 UTC l'été et 23:00 UTC l'hiver. Tests unitaires sur les deux régimes et sur les semaines où les États-Unis et l'Europe ne sont pas à la même heure.
- **Événement de reprise** : la première barre dont l'horodatage est dans [18:00, 18:05) ET, et dont la barre précédente se termine au plus tard à 17:00 ET (pause d'au moins 60 minutes ; le week-end et les fermetures anticipées des jours fériés sont inclus). Sinon, pas d'événement ce jour-là.
- **Gap** = open(barre de reprise) − close(dernière barre avant la pause), en pips. Il est connu dès le premier échange de 18:00.
- **Roulements** : le contrat continu bascule sur une barre de 00:00 UTC, jamais entre 16:59 et 18:00 ET (vérifié sur les dates de 2023-2024 et contrôlé dans le code). On travaille en **prix bruts**. Tout trade, gap intrajournalier ou détention dont l'intervalle contient une barre de 00:00 UTC entre le 1er et le 21 de mars, juin, septembre ou décembre est **exclu**. Le code vérifie que chaque saut de plus de 0,15 % à 00:00 UTC tombe bien dans ces fenêtres.
- Prix d'exécution à l'instant T = open de la première barre dans [T, T + 5 min), sinon le trade est exclu. C'est la convention de `fab/core.py`.

## Règles testées

**Famille principale, la règle du papier transposée** : fade si |gap| ≥ s pips, avec s ∈ {1, 2, 5}.

| Entrée | Prix d'entrée | Sortie | Rôle |
|---|---|---|---|
| E0 | open de 18:00 (prix de l'enchère) | open de 19:00 | règle du papier |
| E1 | open de 18:01 | open de 19:01 | **première entrée réaliste** : on connaît le gap, puis on envoie un ordre au marché |
| E5 | open de 18:05 | open de 19:05 | entrée décalée |
| E15 | open de 18:15 | open de 19:15 | entrée décalée |

E0 suppose qu'on obtient le prix de l'enchère alors qu'on ne connaît le gap qu'une fois l'enchère faite. C'est possible seulement en plaçant l'ordre pendant la pré-ouverture, au vu du prix indicatif d'ouverture, qu'on n'a pas. **E0 est donc optimiste par construction.**

**Contrôles, prédictions du papier** (entrée E0, mêmes seuils) :
- (a) **heures intrajournalières** : même règle à chaque frontière HH:00 ET hors 18:00 (19:00 → 16:00, soit 22 frontières). Gap = open(barre de HH:00 exactement) − close(barre précédente, au plus 5 minutes avant), sortie à l'open de HH+1:00. Pour la frontière de 16:00, sortie au close de la dernière barre avant 17:00. Coût = coût standard du dépôt (1 tick + 5 $ aller-retour, converti en pips). **Le papier prédit PF < 1.**
- (b) **détention jusqu'au close du jour** : entrée E0, sortie au close de la dernière barre avant la pause de 17:00 ET. **Le papier prédit un PF nettement inférieur à celui de la sortie à une heure**.

## Coûts (aller-retour, en pips de la paire)

- Grille de sensibilité : **0** (brut), **2, 3, 5 et 8 pips**. Ce sont les mêmes positions : la grille ne compte pas comme des essais en plus.
- **Coût principal = 3 pips aller-retour.** Justification : en temps normal, un aller-retour coûte de 0,9 à 2 pips (1 tick + 5 $). L'entrée se fait à l'instant où le carnet est le plus mince, et la sortie une heure plus tard, en carnet normal.
- **Spread de point mort** par seuil et par entrée = gain brut moyen par trade, en pips (poolé, et par paire).
- Diagnostic, hors compteur : **spread effectif estimé** par l'estimateur d'Abdi et Ranaldo (2017) sur les barres 1 minute, pour les minutes 18:00-18:04 et pour la référence 02:00-16:00 ET. C'est pour calibrer ce qu'est un coût « réaliste » à la reprise.

## Mesure de la performance

- Par trade : P&L en pips (paire par paire, puis poolé), PF, taux de réussite, gain moyen, Sharpe « du papier » (moyenne / écart type × √(trades par an)).
- Portefeuille journalier : capital réparti à 1/4 par paire, 1× sans levier. Rendement du jour = moyenne sur les 4 paires de sens × (p_sortie / p_entrée − 1) − coût / p_entrée (0 si pas de trade). Sharpe annualisé avec √252.
- Fenêtres :
  - **2016-01 → 2018-12** (équivalent de la pré-période du papier, raccourcie : nos données commencent en 2016) ;
  - **2019-01 → 2026-01** (fenêtre d'analyse du papier) ;
  - **2026-02 → 2026-08** (postérieur aux données du papier : 7 mois, rapportés sans critère) ;
  - nombre d'années perdantes, par année civile.

## Essais : 18 (le compteur global passe de 174 à 192)

- Famille principale : 3 seuils × 4 entrées = 12
- Contrôle (a), heures intrajournalières : 3
- Contrôle (b), détention jusqu'au close du jour : 3

**Configuration principale, désignée à l'avance : s = 5 pips, entrée E1 (18:01), sortie +60 min, coût de 3 pips aller-retour.** C'est le seuil le plus robuste selon le papier, avec la première entrée réellement exécutable. Les 11 autres de la famille sont secondaires.

## Critères de décision (fixés avant exécution)

La configuration principale **survit** si elle vérifie **toutes** ces conditions :
1. gain moyen net > 0 et PF > 1 **à la fois** sur 2016-2018 et sur 2019-2026-01 ;
2. p < 0,05 pour la moyenne du rendement journalier net > 0, par bootstrap stationnaire (blocs de 10 jours en moyenne, 10 000 tirages, toute la période) ;
3. **p de permutation < 0,05** : 10 000 permutations aléatoires du sens (±1) entre les événements de la règle, avec les mêmes entrées et sorties ; statistique = gain moyen par trade. On teste ainsi si le fade bat un sens aléatoire sur les mêmes instants ;
4. **DSR > 0,95** avec N = 18 et la variance des Sharpe journaliers des 18 essais au coût principal (le DSR avec N = 192 est rapporté).

Lectures secondaires, fixées elles aussi à l'avance :
- **« Le seuil 5 pips survit à un spread réaliste »** : les critères 1 à 4 sont tenus pour s = 5 en E1 à 3 pips. Le résultat à **5 pips** de coût est rapporté comme scénario défavorable.
- **« Survit à une entrée décalée »** : en E5 et en E15, le gain moyen net à 3 pips reste > 0 sur les deux fenêtres, et la permutation donne p < 0,05.
- **Contrôles** : (a) est confirmé si le PF net est < 1 pour les 3 seuils. (b) est confirmé si le PF de la détention jusqu'au close est inférieur à celui de la sortie à une heure, pour les 3 seuils.
- **Reality Check de White** sur les 18 règles au coût principal (bootstrap stationnaire, blocs de 10 jours, 5 000 tirages) : rapporté, comme dans le papier.
- **Décomposition de l'exécutabilité** : quelle part du retour à la moyenne a lieu entre 18:00 et 18:01, en pips (open 18:01 − open 18:00, dans le sens du fade).

**Puissance (à lire avant les résultats).** Il y a environ 2 700 reprises par paire. Au seuil de 5 pips, on attend de quelques centaines à environ un millier d'événements par paire, selon la distribution des gaps du future, qu'on ne connaît pas encore. Avec un écart type par trade de l'ordre de 10 à 15 pips sur une heure, l'erreur type d'un gain moyen sur 2 000 trades poolés est d'environ 0,3 pip. Une différence de 1 pip est donc détectable, mais pas une de 0,3 pip.

**Garde-fou.** Si un résultat dépasse un PF de 4, un taux de réussite de 75 % ou un Sharpe journalier de 3, on cherche d'abord une fuite (roulement, horodatage, prix de la barre de signal réutilisé) avant de le présenter. Les chiffres du papier en E0 (PF jusqu'à 4,69, taux de réussite de 80 %) tombent dans cette zone : c'est attendu, et c'est justement ce que les entrées décalées doivent démêler.

## Rapport

[reports/fx_reopen_report.md](reports/fx_reopen_report.md) et une section dans [RESULTS.md](RESULTS.md) :
- anatomie du gap (taille moyenne et part supérieure à 1 pip, à la reprise et aux autres heures, à comparer aux 4,8 pips et 74 % du papier) ;
- tableaux des 18 règles par fenêtre et par coût, spreads de point mort, contrôles, résultats par paire et par année, critères, DSR, permutations, Reality Check ;
- verdict sur la question posée.
