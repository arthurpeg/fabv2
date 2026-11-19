# Correction des simulations FTMO : objectif d'éval ramené au reste à faire

*2026-11-04. **Exploratoire, hors compteur.** Ce rapport fait suite à une question de l'utilisateur sur [[reports/ftmo_septembre_report]].*

## Le défaut

Plusieurs simulations FTMO récentes rejouaient une **liste de trades** : mom, trio, 3n + M2, évals rapides et croisements éval / financé. Dans ces simulations, chaque trade gardait son **objectif fixe de 2 R, même en éval**. Or quand le compte est à +9,1 % et qu'il ne manque que +0,9 %, l'objectif doit être ramené à ce qui manque (et à la règle du meilleur jour). Le moteur du n° 18 le faisait en mode « jours », mais pas en mode « trades ».

## La correction

- **Le mouvement favorable maximal (MFE) de chaque trade avant sa sortie**, en R, est calculé en excluant la barre du stop, puisqu'on ne sait pas si le haut est venu avant le bas dans cette barre :
  - mom (TP 4 ATR) : [build_mfe_mom.py](../build_mfe_mom.py), barres 1 min → `cache/propfirm/nq_nuit_tp4_mfe.parquet` ;
  - 3n et M2 : `run_propfirm_combo.simule`, barres 5 min → colonne `MFE_R` de `results/propfirm_combo/trades_tp2.csv`.
- **Contrôle** : 100 % des trades sortis au TP ont un MFE ≥ 1,98 R.
- **En éval**, l'objectif d'un trade devient k = ce qui manque × (1 + c) / risque + c, quand k < 2 R. Il est atteint si le MFE ≥ k ; sinon le trade garde son issue d'origine. Le financé ne change pas : son objectif est fixe à 2 R par règle.
- **Moteurs corrigés** : [run_propfirm_trio.py](../run_propfirm_trio.py), [run_propfirm_mix.py](../run_propfirm_mix.py), [run_propfirm_eval_rapide.py](../run_propfirm_eval_rapide.py). Les anciennes sorties sont gardées (`*_objectif_fixe.*`).

## Avant → après

**Plans à 2,5 % en éval et 1 % en financé** ([[reports/propfirm_trio_report]]) :

| Période | Plan | Passage | Durée de l'éval | EV 10k | EV 100k | EV / mois 100k |
|---|---|---|---|---|---|---|
| 2016-2026 | Trio | 59,8 → **64,7 %** | 1,1 → 1,0 mois | +2 020 → **+2 193 $** | +20 519 → **+22 253 $** | +1 478 → +1 500 $ |
| | 3n + M2 (1 / jour) | 60,5 → **65,5 %** | 0,9 mois | +2 618 → **+2 880 $** | +26 500 → **+29 123 $** | +1 446 → +1 464 $ |
| | mom seul | 43,6 → **50,7 %** | 0,4 mois | +625 → **+729 $** | +6 572 → **+7 610 $** | +1 989 → **+2 061 $** |
| | Trio sans edge | 25,5 → 29,5 % | | −6 → +7 $ | | |
| 2011-2015 | Trio | 71,2 → 71,9 % | 1,1 → 1,0 mois | +3 362 → +3 430 $ | +33 942 → +34 617 $ | +1 616 → +1 623 $ |
| | 3n + M2 | 54,1 → 59,4 % | 1,1 → 1,0 mois | +879 → +960 $ | +9 113 → +9 923 $ | +948 → +972 $ |
| | mom seul | 56,1 → 61,4 % | 0,5 → 0,4 mois | +1 786 → +1 967 $ | +18 185 → +19 995 $ | +3 397 → +3 454 $ |

**Éval / financé** ([[reports/propfirm_mix_report]]), sur 2016-2026 :

| Plan | EV 10k avant | EV 10k après | EV / mois 100k avant | EV / mois 100k après |
|---|---|---|---|---|
| mom → mom | +617 $ | **+720 $** | +1 978 $ | **+2 055 $** |
| mom → trio | +1 451 $ | **+1 675 $** | +1 518 $ | +1 539 $ |
| trio → mom | +886 $ | +955 $ | +1 815 $ | +1 889 $ |
| trio → trio | +2 037 $ | **+2 187 $** | +1 476 $ | +1 498 $ |

Le passage de l'éval mom passe de 43,8 % à 50,2 % (2016-2026), celui de l'éval trio de 60,5 % à 64,8 %. Sur 2019-2026, mom → trio passe de +1 443 à +1 663 $.

**Évals rapides** ([[reports/propfirm_eval_rapide_report]]), vérification sur 2019-2026 :

| Réglage (3n / mom / M2) | Passage | Durée moyenne (séances) |
|---|---|---|
| mom seul 2,5 % | 42,4 → **49,1 %** | 9,5 → 8,6 |
| **Trio 2,5 / 1,25 / 1,25** | 58,2 → **61,2 %** | 21,2 → **19,4** |
| B : – / 2,0 / 0,5 (nouveau dans le top) | → **57,5 %** | → **15,0** |
| C : 0,5 / 2,0 / 0,5 (nouveau dans le top) | → 55,8 % | → 13,1 |
| A : 2,0 / 2,5 / – (nouveau dans le top) | → 50,2 % | → 12,0 |

## Lecture

1. **Le passage gagne 1 à 7 points.** Le gain est le plus fort pour mom seul (+7 points), dont les trades à 2,5 % approchent souvent la cible par un TP de 5 % qu'un objectif réduit permet d'encaisser plus tôt. Les évals sont aussi un peu plus courtes. L'EV par tentative augmente de 3 à 17 %.
2. **Les classements ne changent pas.**
   - Par tentative : 3n + M2 ≥ trio > mom → trio > mom seul.
   - Par mois d'emplacement : mom seul reste devant.
   - Le trio reste le plan d'éval le plus sûr sur 2019-2026 (61 %).
3. **Pour aller plus vite, il y a désormais un compromis un peu moins coûteux** : mom à 2 % plus M2 à 0,5 % donne 57,5 % de passage en 15 séances (environ 3 semaines), contre 61 % en 19 séances pour le trio.
4. **Ce qui n'est pas corrigé :**
   - les chiffres FTMO de [[reports/propfirm_combo_report]] (moteur `propfirm.ftmo`, financé arrêté à 500 trades). La version corrigée de « 3n + M2 » est dans le tableau ci-dessus ;
   - [[reports/propfirm_3n_vs_mom_report]] (3n sans TP, mom TP 5 ATR) ;
   - les avenants pré-enregistrés du n° 18, qui restent tels quels.

   Leurs taux de passage sont un peu pessimistes.
5. **Limite de la correction.** Le MFE est mesuré sur des barres de 5 min pour 3n et M2, et de 1 min pour mom, en excluant la barre du stop. C'est prudent : un objectif touché dans la barre du stop compte comme raté.
