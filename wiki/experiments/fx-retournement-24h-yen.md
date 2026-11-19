---
type: experiment
updated: 2026-11-19
status: planned
verdict: étape 1 figée (grille commitée), pas encore calculée
prereg: []
trials: 1798
---

# Retournement des rendements 24 h sur les paires yen (Piccotti)

**Une phrase** : chaque jour à une heure fixe, prendre la position inverse du rendement des 24 h écoulées sur USD/JPY (et peut-être AUD/JPY), puis la garder 24 h. Le papier trouve une autocorrélation d'ordre 1 négative de ces rendements. Pour l'instant, c'est une fiche d'idée (étape 0 de [[PROTOCOLE]]) : aucun rendement n'a été calculé.

## Origine

Le papier est Piccotti, « Pricing errors and the geography of trade in the FX market », SSRN 2446584. Le texte est dans `papers/txt/piccotti_pricing_errors.txt`, et la lecture est notée au journal du 2026-11-19. Les données du papier sont des cotations Gain Capital de 2007 à 2010, sur 14 paires, avec un rendement 24 h mesuré à chaque demi-heure.

Les chiffres suivants viennent du papier. Ils ne sont pas vérifiés chez nous.

| Mesure | Paire, heure ET | Valeur | Source |
|---|---|---|---|
| ρ(1) des rendements 24 h | USD/JPY, de 11:00 à 17:00 | −0,04 à −0,09, tous marqués * | Tableau 4 |
| ρ(1) des rendements 24 h | USD/JPY, 18:00 | −0,22 | Tableau 4 |
| ρ(1) des rendements 24 h | AUD/JPY, de 11:00 à 17:00 | −0,09 à −0,13 | Tableau 4 |
| ρ(1) des rendements 24 h | NZD/JPY, EUR/AUD | négatif à presque toutes les heures | Tableau 4 |
| ρ(1) des rendements 24 h | EUR/USD, GBP/USD, EUR/GBP | ≥ 0 à presque toutes les heures | Tableau 4 |
| Part de jours où le signe continue | USD/JPY, de 11:00 à 17:00 | 0,43 à 0,45, binomial * (ce sont donc 55 à 57 % de retournements) | Annexe, tableau B3 |

L'auteur ne chiffre aucun rendement de trading. Il voit dans le ρ négatif la marque d'erreurs de prix transitoires, sans lien avec l'information, et parle d'un « léger dépassement » du yen pendant la séance NY.

## Étape 0 : fiche

**1. Déjà vu ?**
- Registre des échecs : aucune ligne sur le retournement d'un jour sur l'autre en FX. Les lignes voisines portent sur d'autres objets :
  - Caporale-Plastun : contrarien sur l'or, signe inversé ;
  - Tolušić : fade de la première heure après 18:00, l'effet tient dans la minute de l'enchère ;
  - momentum intraday FX : objet opposé, intraday.
- Phénomènes : la ligne la plus proche est l'autocorrélation négative des sessions Asie et US, mais sur ES, NQ et YM, donc un autre actif.
- Risque de double comptage avec le n° 28 (le yen baisse en session US, une dérive constante). Une règle de retournement est en principe orthogonale à une dérive, mais il faut le vérifier : la référence triviale de l'étape 1 est justement « toujours short yen » sur les mêmes 24 h.
- → **B0 : l'idée est nouvelle.**

**2. Mécanisme** (celui du papier, non vérifié). Les demandeurs de liquidité poussent le prix au-delà de sa valeur. Les dealers absorbent l'inventaire et sont payés quand le prix revient. Le marché FX est à deux niveaux : les clients ne traitent qu'avec des dealers, ce qui empêche les traders informés d'absorber tout le flux non informé (section 3 du papier).
- Pourquoi ça ne s'arrête pas : le capital des teneurs de marché est limité.
- Point faible : l'échantillon de 2007 à 2010 couvre la crise et les débouclages de carry trade. L'annexe D montre que d'autres effets du papier sont concentrés dans la crise.

**3. Taille attendue face au coût.**
- Volatilité quotidienne de 6J sur 2016 à 2026-08 (données explorées) : 60 bp. C'est un écart type de rendements 24 h, pas une moyenne, mesuré le 2026-11-19 et non compté.
- Pour une règle de signe, l'espérance brute vaut |ρ| · σ · √(2/π) si les rendements sont gaussiens (approximation) :

| ρ supposé | Brut attendu | Net attendu (coût standard 6J ≈ 1,13 bp*) | Sharpe annuel brut / net |
|---|---|---|---|
| −0,05 | ≈ 2,4 bp | ≈ 1,3 bp | 0,63 / 0,33 |
| −0,09 | ≈ 4,3 bp | ≈ 3,2 bp | 1,14 / 0,84 |

*Coût en bp : écart brut − net du backtest du yen, voir [[reports/jpy_us_backtest_report]].

- 1,5 × coût ≈ 1,7 bp. Avec ρ = −0,05, l'effet attendu passe ce seuil, donc les parcours **stratégie** et **phénomène** restent ouverts. Le net serait toutefois mince : à ρ ≈ −0,03, seul le parcours phénomène resterait ouvert.

**4. Découpage des données** (règle 4 de `CLAUDE.md`, [[wiki/reserves]]).
- **Période du papier (2007-2010)** : nous ne l'avons pas. Pour faire la réplication de l'étape 1, il faudrait télécharger le spot Dukascopy de 2007 à 2009, à condition qu'il existe. Ce serait une tranche vierge à déclarer dans `reserves.md` comme « période du papier, explorable ».
- **Explorable** : USD/JPY spot de 2010 à 2015 (Dukascopy) et 6J de 2016 au 2026-08-28. Tout est déjà exploré, donc tout ce qu'on y trouvera est en échantillon. Pour AUD/JPY, il faudrait un cours synthétique (AUDUSD × USDJPY spot, ou 6A / 6J).
- **Réserve** : il n'en reste aucune. Le yen postérieur au 2026-08-28 est réservé au holdout du n° 28. On suivrait donc le parcours « étape 1 → étape 4 » : un nouveau pré-enregistrement, commité **avant la lecture L1 du 2028-02-29**, qui lit sur les mêmes dates (2028-02-29, 2029-08-31, 2031-08-29). Il faudrait déclarer dans `reserves.md` que la tranche sert aussi à cette famille. **Aucun calcul sur le yen après le 2026-08-28 d'ici là.**

**5. Puissance** (test unilatéral à 5 %, ≈ 252 jours par an). Durées jusqu'aux lectures : 380 jours (L1), 760 jours (L2), 1 260 jours (L3).

| ρ supposé | Puissance brut L1 / L2 / L3 | Puissance net L1 / L2 / L3 | Lecture intermédiaire z ≥ 3 (net) L1 / L2 |
|---|---|---|---|
| −0,05 | 19 % / 29 % / 41 % | 11 % / 14 % / 18 % | 0 % / 1 % |
| −0,09 | 40 % / 63 % / 82 % | 27 % / 43 % / 59 % | 2 % / 6 % |

→ **La puissance est faible.** Sauf si ρ est proche du haut de la fourchette du papier, le holdout ne pourra pas trancher sur le net avant 2031. C'est le même problème que pour le n° 28.

**B0** : l'idée n'est pas au registre, le découpage est écrit, la puissance est connue. **B0 est passée.**

## Étape 1 : grille figée le 2026-11-19 dans l'en-tête de [run_jpy_reversal24.py](../../run_jpy_reversal24.py), commitée avant tout calcul

L'en-tête du script fait foi. Il précise : spot USDJPY/AUDUSD Dukascopy 1 min 2012-01-11 → 2015 (le spot horaire 2010-2011 n'est pas utilisé), 6J/6A 2016 → 2026-08-28 ajustés en ratio ; entrées lundi-jeudi ; choix = plus grand Sharpe net ; compteur 1 798 → 1 804. Ci-dessous, la proposition de la fiche.

- **Règle** : à l'heure H, position = −signe(rendement de H la veille à H aujourd'hui), tenue jusqu'à H le lendemain. Coût standard. Les jours ouvrés seulement ; le lundi inclut le week-end, à traiter comme le papier (qui l'exclut) ou à part.
- **Grille minimale** :
  - paires : USD/JPY, AUD/JPY (synthétique) ;
  - heures H : 11:00, 15:00, 16:55 ET (cette dernière évite 17:00-18:00, les heures les plus chères du papier).
  - → **n_famille = 6**. Ajouter des heures ou des paires fait monter le DSR requis.
- **Référence triviale** : toujours short yen sur les mêmes 24 h (règle conditionnelle contre position sans condition). Elle mesure aussi le recouvrement avec le n° 28.
- **Données** : spot de 2010 à 2015 au bid/ask ; 6J de 2016 au 2026-08-28. Pour les rendements 24 h, les roulements doivent être traités : 6J v0 n'est pas ajusté (voir la mémoire « fab.core roll detection » et [[wiki/concepts/roulements]]).
- **Réplication d'abord**, si la période 2007-2010 est récupérable : signe et ordre de grandeur de ρ pour USD/JPY en séance NY.
- **Barrière** : B1 de [[PROTOCOLE]]. Si elle échoue, ligne au registre ; si le ρ est significatif en brut seulement, ligne « À surveiller » dans [[wiki/phenomenes]].

## Ouvert

- Le ρ de 2007 à 2010 survit-il hors crise ? Le papier ne le découpe pas (son annexe D ne porte pas sur ρ par paire).
- Le ρ de −0,22 à 18:00 ET est très probablement le bruit de la reprise (voir l'échec Tolušić). Il n'est pas captable et sort de la grille.

## Sources brutes

`papers/ssrn-2446584.pdf` · `papers/txt/piccotti_pricing_errors.txt` · [[papiers_ssrn_overnight_fx_or_petrole_2026-11-02]] (fiche corrigée le 2026-11-19) · [[PREREGISTRATION_28]] (réserve du yen)
