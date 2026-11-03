---
type: registry
updated: 2026-11-02
---

# Registre des phénomènes confirmés

> Le pendant du [[wiki/Failed Ideas/ledger|registre des échecs]]. **Chaque règle ou hypothèse (d'un papier ou à nous) qui se vérifie sur nos données y entre, même si elle n'est pas tradable seule.** Le but est d'amasser des briques (heures, actifs, conditions où quelque chose se passe vraiment) pour les combiner en stratégies.
>
> **Critère d'entrée** : significatif sur nos données après correction pour tests multiples dans sa famille (Holm ou BH ≤ 0,05), ou critère d'un pré-enregistrement rempli. On note la stabilité par sous-période et si l'effet survit aux coûts. Ce qui est significatif en brut mais pas après correction, ou porté par une seule sous-période, va dans « À surveiller ».
>
> Une ligne par phénomène, ajoutée le jour du test, jamais supprimée : si un test ultérieur le contredit, on ajoute « ⚠️ contredit le AAAA-MM-JJ, voir … » dans la colonne Stabilité. Les chiffres sont des repères : c'est le rapport lié qui fait foi.
>
> Avant de construire une stratégie à partir de plusieurs lignes : vérifier qu'elles ne sont pas le même effet compté deux fois (exemple : la [[wiki/concepts/prime-de-nuit|prime de nuit]] réapparaît sous beaucoup de noms), et pré-enregistrer la combinaison.

## Confirmés

Heures en New York (ET). « Net ? » : ✅ survit au coût standard, ❌ non, — sans objet (phénomène de volatilité ou de volume, pas un rendement).

| Date | Phénomène | Actif · fenêtre | Taille, statistique | Stabilité | Net ? | Origine | Rapport | Pistes de combinaison |
|---|---|---|---|---|---|---|---|---|
| 2026-10-31 | Prime de nuit : le rendement des indices se fait hors séance | NQ, clôture → ouverture | +4,8 pb/jour, t 3,1 (2016-2026) | Robuste ; base de la règle NQ de nuit | ✅ (via la règle NQ de nuit) | Littérature overnight (récolte 1) | [[wiki/concepts/prime-de-nuit]] | Toute règle de nuit : comparer à un long simple de mêmes heures |
| 2026-10-31 | Règle NQ de nuit (momentum 12-1, 20:00 → 9:30, SL 2 / TP 5 ATR) | NQ | +0,116 R/trade hors échantillon 2011-2015, p 0,0015 ; α +6,2 %/an | Validée hors échantillon (n° 11, 12) ; échoue sur ES et YM | ✅ | Récolte 1 | [[wiki/experiments/nq-nuit-momentum]] | Pondérer les nuits d'annonce (voir « À surveiller ») |
| 2026-10-14 | Le signe de la minute 08:55 → 09:00 du DAX (enchère Xetra) est prévisible | DAX, 08:55-09:00 Francfort | 55 % de bons signes, p 0,0008 (Bonferroni ≈ 0,012) | Stable avant et après 2023 | ❌ (Sharpe net 0,13) | De Gooijer et al. (n° 5) | [[reports/opening_gap_report]] | Exécution passive ou participation à l'enchère |
| 2026-11-01 | Reprise de l'or : hausse concentrée sur la reprise du soir | GC, 17:00 → 9:00 Shanghai | +2,0 bp brut/jour, t 3,5, Holm 0,003 ; +1,1 bp net | 3 sous-périodes positives ; nulle le lundi | ⚠️ +1,1 bp net, t 2,0 | Exploratoire (sessions de l'or) | [[reports/gc_sessions_report]] | Avec la continuation de nuit (à surveiller) ; avec un filtre de jour de semaine |
| 2026-11-02 | Pic de volatilité à 8:30 (annonces US), le plus gros intervalle de la journée | GC, SI | GC × 4,8, SI × 3,2 face aux voisins ; Holm 0,005 | GC et SI | — | Fattinger-Ziegler | [[reports/gc_fattinger_report]], [[reports/si_fattinger_report]] | Filtre d'annonces ; dimensionner les stops autour de 8:30 |
| 2026-11-02 | Le saut de 8:30 vient des jours d'annonce | GC, SI | 2,0 % (GC) / 1,15 % (SI) de toute la variance dans ce seul intervalle ; 91 % / 94 % les jours d'annonce | Rang 1 dans 100 % des tirages, toutes sous-périodes | — | Fattinger-Ziegler | idem | Calendrier macro comme variable d'état |
| 2026-11-02 | Pic de volatilité à 14:00 les jours FOMC | GC, SI | × 7,3 / × 6,4 ; Holm 0,005 | GC et SI | — | Fattinger-Ziegler | idem | Idem |
| 2026-11-02 | Pic de volatilité à l'ouverture de Tokyo (9:00 JST = 19:00 ou 20:00 NY) | GC, SI | × 2,0 / × 1,7 ; Holm 0,005 | GC et SI | — | Fattinger-Ziegler | idem | Coïncide avec la jambe 19:00 → 20:00 de la reprise de l'or |
| 2026-11-02 | Pics de volatilité à 10:00 et 8:20 NY | GC, SI | 10:00 × 1,9 / × 1,4 ; 8:20 × 1,9 / × 1,2 ; Holm ≤ 0,01 | GC et SI | — | Fattinger-Ziegler | idem | — |
| 2026-11-02 | Pic de volatilité à 13:30 (règlement COMEX) | GC seul | × 1,36, Holm 0,03 | Absent sur SI | — | Fattinger-Ziegler | [[reports/gc_fattinger_report]] | — |
| 2026-11-02 | Hausse de volatilité à l'ouverture européenne (3:00 NY) | GC | × 1,22, Holm 0,005 | Non significatif sur SI (× 1,19) | — | Fattinger-Ziegler | idem | — |
| 2026-11-02 | Pas de U en séance COMEX : volatilité de diffusion forte au début, faible en fin de séance | GC, SI | GC fin/milieu 0,55, début/milieu 1,23 ; SI 0,58 / 1,37 | GC et SI | — | Fattinger-Ziegler (contre la littérature actions US) | idem | Stops plus serrés l'après-midi |
| 2026-11-02 | Marché mince la nuit : part de volatilité > part de volume hors 8:20-13:30 | GC, SI | GC +15,5 pts, SI +21,0 pts ; Holm 0,004 | GC et SI | — | Fattinger-Ziegler | idem | Coût réel la nuit plus élevé que 1 tick ; ordres passifs |
| 2026-11-02 | Plus de prix par contrat la nuit (contribution au prix / part de volume) | GC, SI, 18:00 → 3:00 | × 1,29 / × 1,47 ; IC hors de 1 | GC et SI | — | Fattinger-Ziegler | idem | Flux de nuit informatif |
| 2026-11-02 | Un quart du prix du jour se fait avant 3:00 NY, autant que la part de variance | GC, SI, 17:00 → 3:00 | GC 26,5 %, SI 28,5 % (contribution pondérée) | Hausse en 2023-2026 (33 %) | — | Contredit Fattinger-Ziegler (≈ 0 en 2010-2013) | idem | Avec la reprise de l'or |
| 2026-11-02 | Sauts ≈ 7-9 % de la variance journalière | GC 9,0 %, SI 7,3 % | IC [7,8 ; 10,2] / [5,9 ; 9,1] | Toutes sous-périodes | — | Fattinger-Ziegler | idem | — |
| 2026-11-02 | Aux annonces (8:30, 10:00) et à 9:30, le volume monte plus que la volatilité | GC, SI | Excès de part de volume > 0, Holm 0,004 | GC et SI (8:20 et 13:30 : GC seul) | — | Fattinger-Ziegler | idem | Liquidité disponible au moment des annonces |

## À surveiller (significatif en brut, pas après correction, ou porté par une sous-période)

| Date | Phénomène | Actif · fenêtre | Chiffres | Pourquoi pas confirmé | Rapport |
|---|---|---|---|---|---|
| 2026-10-31 | Les nuits NFP/CPI sont les meilleures de la règle NQ de nuit | NQ, nuits d'annonce | +0,30 R contre +0,05 ; ≈ 40 % des R en 9 % des nuits | Trouvé en inversant l'hypothèse du n° 14 ; ne se généralise pas aux autres annonces | [[reports/prereg14_report]] |
| 2026-11-01 | Fenêtre 16:00 → 19:00 NY sur l'or | GC | +1,4 bp net, t 2,7 | Choisie après coup ; nulle en 2016-2019 | [[reports/gc_sessions_report]] |
| 2026-11-02 | Continuation : le mouvement 17:00 → 5:00 NY se prolonge le reste du jour | GC (b 1,13, Holm 0,02) ; SI (b ≈ 1,2, non significatif après Holm) | Pour 1 σ de nuit, ≈ +7 bp dans le même sens ensuite (GC) | Entièrement 2023-2026 ; trouvé parmi 23 coupures ; GC et SI très corrélés | [[reports/gc_fattinger_report]], [[reports/si_fattinger_report]] |
| 2026-11-03 | Retour à la moyenne des nuits NQ : après 3 nuits (20:05 → 03:00) de somme ≤ 0, la nuit suivante est meilleure | NQ, 20:05 → 03:00 | Long filtré +0,14 R/trade, t NW 3,9 (2016-2024) contre +0,04 R non filtré ; OOS 2025-26 t 2,1 | Filtre choisi parmi plusieurs par l'auteur, non corrigé ; nul en 2022-2024 (t 1,1) | [[reports/nq_nuit_3n_vbt_report]] |
