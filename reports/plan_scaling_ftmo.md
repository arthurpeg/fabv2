# Plan de montée en taille FTMO 1-Step pour la règle NQ de nuit

*2026-10-31. Plan exploratoire, pas un résultat pré-enregistré. Chiffres : [run_propfirm_scaling.py](../run_propfirm_scaling.py) → `results/propfirm_scaling/sizes.csv` (trio de comptes 19:00 / 20:00 / 21:00, rendements par vectorbt, règles FTMO vérifiées, 662 fenêtres de 2 ans sur 2011-07 → 2026-08), et [[reports/prereg18_report]] (avenants C à E, exploratoires). Tous ces chiffres sont **optimistes** : la règle a été choisie sur 2016-2026, et il n'y a qu'un historique.*

## Règles FTMO qui cadrent le plan (lues sur ftmo.com le 2026-10-31)

- **Allocation maximale : 400 000 $ par trader ou par stratégie, tous comptes et produits confondus**, avant le Scaling Plan ; dépasser expose à la suspension des comptes. Pas de limite au nombre de comptes. Des trades identiques sur plusieurs comptes du même trader restent dans ce plafond.
- **Scaling Plan** (1-Step éligible) : +25 % de taille tous les 4 mois, jusqu'à 2 M$ au total, si le compte FTMO a ≥ 4 mois, ≥ 10 % de profit net sur les 4 derniers mois, ≥ 2 rewards sur la période, et un solde positif.
- Pas de hedge entre comptes : les trois heures prennent toujours le même sens (même signal de momentum), donc pas de conflit.

## Réglage de trading (inchangé à chaque palier)

Un compte par heure d'entrée (19:00, 20:00, 21:00 ET) ; éval : 2 % de risque, SL 2 ATR / TP 5 ATR ; financé : 1 % de risque, SL 2 ATR / TP 4 ATR (RR 2) ; sortie 9:30 ET ; une éval rachetée dès qu'un compte est raté ou perdu. **On ne change que la taille des comptes**, jamais le risque en %.

## Ce que donne un trio de comptes sur 2 ans, par taille

| Taille | Prix d'une éval | Gain net moyen du trio | 5e centile | Pire fenêtre | Frais moyens | Pire creux de trésorerie | Allocation |
|---|---|---|---|---|---|---|---|
| 10k | 87 $ | +12 811 $ | +6 227 $ | +3 813 $ | 1 722 $ | −1 738 $ | 30k |
| 25k | 219 $ | +31 994 $ | +15 527 $ | +9 483 $ | 4 337 $ | −4 378 $ | 75k |
| 50k | 351 $ | +65 709 $ | +33 225 $ | +21 573 $ | 6 952 $ | −7 018 $ | 150k |
| 100k | 549 $ | +134 448 $ | +69 779 $ | +47 732 $ | 10 875 $ | −10 978 $ | 300k |
| 200k | 1 099 $ | +268 875 $ | +139 535 $ | +95 431 $ | 21 772 $ | −21 978 $ | 600k (au-dessus du plafond) |

Valables à toutes les tailles : ~32 rewards en 2 ans pour le trio ; jusqu'à 7 évals ratées d'affilée sur un compte ; jusqu'à 151 nuits (~7 mois) sans aucun reward pour le trio. Les prix des tailles 25k, 50k et 200k n'ont pas été revérifiés.

## Le plan

**Règle de passage, la même à chaque palier :** on ne monte d'un cran que quand les rewards déjà encaissés couvrent le **pire creux historique du palier suivant** ; les comptes financés en cours continuent à leur taille ; à chaque compte perdu, on rachète l'éval à la nouvelle taille. Si la réserve retombe sous le pire creux du palier en cours, on redescend d'un cran.

| Palier | Comptes | Allocation | Réserve à avoir (pire creux) | On passe au suivant quand… |
|---|---|---|---|---|
| **0. Validation** | 3 × 10k (19h, 20h, 21h) | 30k | ~1 750 $ de ta poche | ≥ 3 mois en réel, ≥ 2 rewards versés, et les contrôles ci-dessous sont bons |
| 1 | 3 × 25k | 75k | 4 400 $ | rewards cumulés ≥ 7 000 $ |
| 2 | 3 × 50k | 150k | 7 000 $ | rewards cumulés ≥ 11 000 $ |
| 3 | 3 × 100k | 300k | 11 000 $ | rewards cumulés ≥ 15 000 $ |
| 4. Plafond | 4 × 100k (le 4e sur 20h, ou mieux sur une autre règle) | **400k** | ~15 000 $ | — |
| 5. Scaling Plan | comptes financés qui remplissent 4 mois / +10 % / 2 rewards | jusqu'à 2 M$ | — | au cas par cas |

**Contrôles du palier 0** (sinon on ne monte pas) : spread réel de l'US100 chez FTMO à 19:00, 20:00, 21:00 et 9:30 ET (le modèle suppose 1,5 point ; à 3 points l'EV baisse d'environ 30 %) ; écart d'exécution entre le CFD et le future NQ ; R moyen par trade réalisé, comparé au backtest ; premier reward accepté par la revue FTMO sans remarque.

**Durées indicatives** (débit moyen d'un trio, pas un chemin simulé) : 10k → ~530 $/mois en moyenne (~260 $/mois au 5e centile), donc ~8 à 17 mois pour réunir les 4 400 $ du palier 1 ; 25k → ~1 300 $/mois ; 50k → ~2 700 $/mois ; 100k → ~5 600 $/mois. Compter **1,5 à 3 ans** de 10k jusqu'à 300k.

**Au plafond** (4 × 100k) : de l'ordre de **+90 000 $ par an en moyenne** sur l'historique (trio 100k : +67 000 $/an, plus un quatrième compte), environ la moitié au 5e centile. Un quatrième compte sur une heure déjà prise ajoute du rendement mais ne lisse rien (voir l'exploratoire « un signal par compte » du rapport n° 18).

**Scaling Plan** : non simulé. Un compte financé vit en moyenne ~148 nuits (médiane 112, soit ~5 mois) avec ce réglage ; seule une partie atteindra 4 mois avec +10 % net et 2 rewards. C'est un bonus possible, pas une base du plan.

## Ce qui peut casser le plan

- **Le marché change** : la seule vraie phase baissière de l'historique (2022) a donné une année quasi nulle ; une phase plus longue ferait pire que les pires fenêtres ci-dessus.
- **Biais de sélection** : la règle a été choisie sur 2016-2026 ; le holdout (après le 2026-08-28) n'a pas encore été ouvert. Le test pré-enregistré sur ce holdout devrait précéder le palier 1.
- **FTMO** : revue des comptes avant chaque reward, interprétation de « trading identique » sur plusieurs comptes, changement des règles (prix, perte max, Scaling Plan).
- **Corrélation** : les comptes sautent ensemble les mauvaises semaines (6 financés perdus la même nuit le 2026-07-28 dans l'exploratoire 2026). La réserve sert à racheter sans s'arrêter.

## Mise à jour : paliers ou 100k directement ? (chemin complet simulé)

Code : [run_propfirm_paths.py](../run_propfirm_paths.py), sorties `results/propfirm_paths/`. Trio 19h/20h/21h, mêmes règles, départ avec 1 750 $, 612 départs de 2011-07 à 2023-08, horizon 3 ans. À chaque achat d'éval, la taille dépend de la trésorerie du moment ; un achat se fait toujours, quitte à demander un apport personnel. En % du capital, la vie d'un compte ne dépend pas de sa taille.

| Politique | 3 × 100k atteints en 3 ans | Délai médian (si atteint) | Gain net à 1 an (médiane / 5e centile) | À 3 ans (médiane / 5e centile / pire) | Apport en plus des 1 750 $ (pire) | Frais sur 3 ans (médiane) |
|---|---|---|---|---|---|---|
| Paliers (taille dont la réserve est couverte) | 80 % | ~27 mois | +5 020 $ / +958 $ | +66 734 $ / +26 625 $ / +19 172 $ | 0 $ | 8 915 $ |
| 10k puis 100k quand 10 978 $ sont couverts | 62 % | ~30 mois | +4 907 $ / +958 $ | +29 568 $ / +10 433 $ / +8 691 $ | 0 $ | 5 640 $ |
| **100k dès que l'éval (549 $) est payable, sinon 10k** | 100 % (dès le départ) | 0 | +29 378 $ / **−1 452 $** | **+147 908 $ / +65 627 $ / +40 415 $** | **1 374 $** (0 $ dans 40 % des départs) | 13 809 $ |

- **Passer de 10k à 100k avec la même règle de réserve est plus lent que les paliers** dans 100 % des départs, et rapporte moins à 3 ans dans 100 % des cas : il faut réunir 10 978 $ avec le seul débit des comptes 10k.
- **Commencer directement en 100k** (en retombant en 10k quand la trésorerie ne paie plus une éval 100k) rapporte plus que les paliers dans **97 %** des départs. Le prix : jusqu'à **3 124 $** de ta poche au total dans le pire départ historique (1 750 $ + 1 374 $), et un an sur vingt environ fini en perte (5e centile à 1 an : −1 452 $).
- La raison : le prix d'une éval croît moins vite que sa taille (100k coûte 6,3 fois un 10k pour 10 fois le capital) et le taux de passage ne dépend pas de la taille. La règle de réserve du plan initial (« pire creux du palier suivant ») était donc **trop prudente** : ce pire creux mesure une baisse après des gains, pas l'argent à engager au départ.
- Les mêmes réserves que plus haut s'appliquent (biais de sélection, holdout non ouvert, spread réel FTMO, revue des comptes). Commencer en 100k n'est raisonnable qu'après avoir vérifié l'exécution réelle, ce qui peut se faire sur un seul 10k quelques semaines.

### Ta règle : 10k, puis 100k dès que les 10k ont rapporté de quoi payer les évals 100k

Même simulation ([run_propfirm_paths.py](../run_propfirm_paths.py)) : trio en 10k au départ ; dès que le gain net des 10k atteint le seuil, **toutes les évals suivantes sont achetées en 100k** (sans 25k ni 50k, sans retour en 10k) ; les financés 10k déjà ouverts continuent jusqu'à leur perte.

| Seuil de bascule (gain des 10k) | Bascule (médiane) | 3 comptes en 100k (médiane ; % des départs en 3 ans) | Gain à 1 an (médiane / 5e centile / pire) | À 2 ans (médiane / 5e c.) | À 3 ans (médiane / 5e c. / pire) | Apport en plus des 1 750 $ (pire) |
|---|---|---|---|---|---|---|
| **1 trio d'évals 100k (1 647 $)** | **~10 mois** | ~15 mois ; 96 % | +7 395 $ / +23 $ / −1 615 $ | +52 149 $ / +13 191 $ | **+103 777 $ / +55 494 $ / +21 807 $** | 3 418 $ (0 $ dans 92 % des départs) |
| 2 trios (3 293 $) | ~13 mois | ~19 mois ; 95 % | +5 029 $ / +865 $ / −401 $ | +41 937 $ / +6 788 $ | +92 836 $ / +32 354 $ / +19 172 $ | 2 165 $ (0 $ dans 99 %) |
| 3 trios (4 940 $) | ~18 mois | ~22 mois ; 90 % | +4 627 $ / +786 $ / −2 163 $ | +22 225 $ / +5 347 $ | +78 088 $ / +20 674 $ / +12 916 $ | 413 $ (0 $ dans 98 %) |
| Rappel : paliers 25k / 50k | — | ~27 mois ; 80 % | +5 020 $ / +958 $ / −198 $ | +19 850 $ / +5 325 $ | +66 734 $ / +26 625 $ / +19 172 $ | 0 $ |
| Rappel : 100k dès le départ | — | 0 ; 100 % | +29 378 $ / −1 452 $ / −2 075 $ | +86 533 $ / +18 739 $ | +147 908 $ / +65 627 $ / +40 415 $ | 1 374 $ |

Face aux paliers, sur le même départ, la bascule à 1 trio atteint 3 × 100k plus tôt dans 76 % des cas et gagne plus à 3 ans dans 81 % ; à 2 trios : 70 % et 76 % ; à 3 trios : 54 % et 59 %. **Ta règle est donc plus rapide que les paliers**, et d'autant plus que le seuil est bas ; le seuil à 2 trios (3 293 $) garde presque toujours l'argent personnel à 1 750 $ (99 % des départs). Commencer directement en 100k reste le plus rapide, avec un peu plus d'apport et de risque la première année.
