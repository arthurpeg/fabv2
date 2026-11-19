---
type: hot
updated: 2026-11-19 19:03
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 798** (source : [[reports/jpy_us_distribution_report]])
- Dernier pré-enregistrement : n° 28 ([[PREREGISTRATION_28]])
- Idées abandonnées au registre : 37 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-19

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/fx-retournement-24h-yen\|Retournement des rendements 24 h sur les paires yen (Piccotti)]] | planned | grille 24 h suspendue (contrainte intraday) ; version intraday sous le seuil de taille sauf hypothèse haute |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-19] decision | Retournement 24 h yen : grille 24 h de run_jpy_reversal24.py suspendue avant tout lancement (contrainte de l'utilisateur : intraday uniquement), version intraday (signal 24 h à H, sortie 16:55 ET le jour même) réévaluée à l'étape 0 | Parts de variance 6J (écarts types seuls) : 03:00 → 16:55 59 %, 08:00 41 %, 11:00 16 % ; sous l'hypothèse « retournement proportionnel à la variance », seule 03:00 → 16:55 avec ρ −0,09 dépasse 1,5 × coût (brut 2,5 bp, net +1,4), puissance net ≤ 29 % à L3 ; 11:00 → 16:55 exclue (brut < coût) ; compteur inchangé 1 798
- [2026-11-19] schema | Grille de l'étape 1 du retournement 24 h yen figée dans l'en-tête de run_jpy_reversal24.py et commitée avant calcul (wiki/experiments/fx-retournement-24h-yen.md) | 6 variantes (USDJPY, AUDJPY synthétique × 11:00, 15:00, 16:55 ET), spot 2012-01-11 → 2015 + 6J/6A 2016 → 2026-08-28, référence toujours short yen, choix au Sharpe net, B1 net et brut ; réplication 2007-2010 impossible (données absentes) ; rien calculé, compteur 1 798 (→ 1 804 au lancement)
- [2026-11-19] experiment | Fiche d'idée (étape 0) : retournement des rendements 24 h sur les paires yen (Piccotti, SSRN 2446584), wiki/experiments/fx-retournement-24h-yen.md | B0 passée (idée nouvelle) ; brut attendu 2,4-4,3 bp pour ρ −0,05 à −0,09 (σ quotidienne 6J 60 bp, écart type seul) contre ≈ 1,13 bp de coût ; aucune réserve (yen post-2026-08-28 = holdout n° 28) → étape 1 sur données explorées puis étape 4 aux dates de lecture du n° 28 ; puissance net 18-59 % à L3 ; grille proposée n_famille 6 (USD/JPY, AUD/JPY × 11:00, 15:00, 16:55), non commitée ; compteur inchangé 1 798
- [2026-11-19] query | Lecture intégrale de Piccotti, « Pricing errors and the geography of trade in the FX market » (SSRN 2446584, 68 p., papers/txt/piccotti_pricing_errors.txt) ; correction du résumé du 2026-11-02 dans papiers_ssrn_overnight_fx_or_petrole_2026-11-02.md | Papier de microstructure (variance des erreurs de prix, Gain Capital 2007-2010, 14 paires), aucune stratégie ni rendement ; H13 (fade du mouvement asiatique sur 6E) sans appui (ρ 24 h ≥ 0 sur EUR/USD, GBP/USD) ; piste : retournement des rendements 24 h sur les paires yen (USD/JPY ρ −0,04 à −0,09 en séance NY), à tester seulement sur données explorées (pas le yen après le 2026-08-28) ; aucun calcul, compteur inchangé
- [2026-11-19] query | Distribution du short yen 11:00 → 16:55 ET (6J 2016-2026-08 et spot 2012-2015, déjà vus) : 34 coupes figées avant calcul (run_jpy_us_distribution.py, reports/jpy_us_distribution_report.md, results/jpy_us_distribution/), compteur inchangé 1 798 | Effet constant : médiane +2,19 = moyenne +2,03, moyennes tronquées 1-25 % +2,05-2,11, profil (q(p)+q(1−p))/2 plat ≈ +2 bp, 10 meilleures et 10 pires séances s'annulent, 11 années positives sur 11, 36 trimestres sur 43, dispersion trimestrielle inférieure au hasard (χ² p 0,99) ; aucune coupe ex ante ne concentre l'effet ; nul quand ES baisse dans la fenêtre (+0,01) et dans le quintile de volatilité réalisée le plus haut (−1,20, Holm p 0,03), FOMC décision −4,4 (t −1,1) ; aucun filtre pour le n° 28
- [2026-11-19] schema | Protocole de validation standard pour toute idée : PROTOCOLE.md (étapes 0 fiche → 1 exploration B1 → 2 prereg → 3 confirmation C1-C4 → 4 forward F1-F3 → 5 réel K1-K2), modèle templates/preregistration.md, module fab/protocole.py (nw_t, holm, dsr, fiche, barrières) + tests/test_protocole.py, CLAUDE.md règle 5, concept wiki/concepts/protocole.md | Illustration sur le short yen 2016-2026 (explorée, hors compteur) : B1 passe 6/6 avec n_famille = 1, mais DSR 0,48 avec n_famille = 28 (cases du n° 27) → pas de réserve possible, d'où l'étape 4 directe (n° 28)
- [2026-11-19] query | Short yen 11:00 → 16:55 ET avec SL/TP RR 2 en ATR (M5, M15, H1 × k = 1-4), grille figée et commitée avant calcul, exploratoire sur 6J 2016-2026-08 déjà vu (run_jpy_us_sltp.py, reports/jpy_us_sltp_report.md, results/jpy_us_sltp/), compteur 1 786 → 1 798 | aucune des 12 ne bat la règle sans stop (+0,88 bp net, Sharpe 0,59) : stops serrés destructeurs (SL 1 ATR M5 −0,79 bp, Sharpe −1,35 ; SL 1 ATR M15 −0,37), stops larges = référence (SL 3-4 ATR H1 +0,81, 95-97 % de sorties à 16:55) ; espérance ≤ +0,02 R ; effet = dérive lente de 2 bp sous 24 bp de bruit, TP 2R rarement atteint ; n° 28 inchangé
- [2026-11-19] query | Journal VPS du 19/11 : éval réelle du compte A (511480419) perdue au 4e stop de mom (long 1,34 lot 18/11 20:00:02 ET à 27 487,58, risque réduit à 2,40 %, stop 176,3 pts, SL à 20:25:48, −241,54 $, −1,02 R) | solde 8 998,74 $ (−10,01 %, 1,26 $ sous le plancher à cause du glissement ; sans lui le compte était de toute façon perdu, risque restant < 0,05 %) ; compte virtuel passé à l'éval n° 2 (+0,00 %), FTMO a coupé le trading à 20:30 ; exécution conforme ; rachat d'un 1-Step 10k à connecter dans le terminal A (pas de nouvelle bascule : mode réel déjà marqué) ; mom live 12 trades, 2 gagnants, −7,35 R

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- **Vrais comptes FTMO en éval depuis le 2026-11-14** : A = compte 511480419 (FTMO-Server), B = 541521340 (FTMO-Server4), 10 000 $ chacun, bascule automatique faite (démo archivée dans `live/etat/archive/`). 1er trade réel : mom SL le 15/11 (A éval −2,50 %, B 0 %) ; relire le journal (`git fetch origin vps-journal`). Toujours en attente de la réponse du support FTMO (A + B long la même nuit, voir [[live/README]]).
- **Plan FTMO retenu (2026-11-04)** : compte A = mom, compte B = 3n + M2, règle des annonces + cible + attente, éval 2,5 % / financé 1 %, scaling 10k → 400k ; détail dans [[wiki/experiments/propfirm-ftmo-option]] (section « Plan retenu »).
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
- **N° 28 (short yen en session US)** : aucun calcul sur le yen après le 2026-08-28 avant la lecture L1 du 2028-02-29 (acheter alors 6J.v.0 Databento avec NQ), puis `uv run python run_prereg28.py --lecture 2028-02-29`.
<!-- NEXT-ACTIONS:END -->
