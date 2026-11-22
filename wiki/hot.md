---
type: hot
updated: 2026-11-22 18:25
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **2 021** (source : [[reports/orb_bougie_indices_report]])
- Dernier pré-enregistrement : n° 29 ([[PREREGISTRATION_29]])
- Idées abandonnées au registre : 46 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-22

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/ml-anomalies\|Machine learning sur les anomalies que les filtres classiques n'ont pas améliorées]] | active | 1er essai (filtre binaire sur mom) rejeté ; autres candidates à faire |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-22] experiment | Suite de wiki/experiments/nq-orb-bougie-sorties : même grille sur ES et YM, stop 1 ATR / objectif 2-3 ATR sur les trois indices, détail stop 0,5 ATR / 2R et 3R ; réserve ES/YM 2021-10 → 2026-08 déclarée, grille commitée (40cfcc9), exploration 2010-06 → 2021-09, compteur 1 965 → 2 021 | ❌ B1 partout : ES V0 +0,68 pt (t 2,11, DSR 0,002), YM rien, NQ 0,5 ATR/2R +2,23 pts (t 2,17), NQ stop 1 ATR ≈ V0 ; DSR NQ 0,953 avec la famille NQ seule mais 0,02 avec la famille complète (81 variantes) ; réserve non lue
- [2026-11-22] experiment | Étape 0-1 de wiki/experiments/nq-orb-bougie-sorties : règle de la 1ʳᵉ bougie de Zarattini-Aziz sur NQ, sorties V0 (aucune) + 24 variantes stop k × ATR14 / objectif RR ; réserve 2021-10 → 2026-08 déclarée, grille commitée (a49ca1a), exploration 2010-06 → 2021-09, compteur 1 940 → 1 965 | ❌ B1 de justesse : meilleure variante (stop 0,05 ATR, clôture) +1,52 pt/trade, t 3,16, DSR 0,948 ; ≈ 0 avant 2016 ; V0 +2,83 pts/trade mais t 1,27 contre « toujours long » ; objectifs fixes moins bons ; ligne au registre ; réserve non lue
- [2026-11-22] research | Papier SSRN 6833239 (Levine, Day Trading: Adapting to Change) lu en entier (PDF fourni par l'utilisateur) : fiche [3] de papiers_ssrn_orb_2026-11-22.md corrigée | ORB = range 8:00-8:15 ET + entrée au retest, discrétionnaire, 61 trades sur 23 jours (oct.-déc. 2025) ; chiffres incohérents (53 % annoncé, 64 % dans le tableau) ; aucune valeur de preuve
- [2026-11-22] research | Recherche d'une autre copie du papier retiré SSRN 6355218 (Chuk, SPY 0DTE ORB) : OpenAlex, Crossref, arXiv, Wayback Machine, ORCID de l'auteur, web | introuvable ; l'ORCID de l'auteur ne le liste plus (retrait vraisemblablement volontaire)
- [2026-11-22] research | papiers_ssrn_orb_2026-11-22.md : papier [2] (Chuk, SPY 0DTE ORB, SSRN 6355218) marqué retiré de SSRN, signalé par l'utilisateur ; note ajoutée au registre local | à ne plus citer
- [2026-11-22] research | papiers_ssrn_orb_2026-11-22.md : section E ajoutée, les 16 papiers ORB déjà fournis (Schulmeister, Holmberg, Sönnert, Tsai, Xin, Zarattini ×3, Pineda, Subhani, Ladia, Fetna, Mesfin, Wijesinghe, Mahadzva, Howard) remis au format de récolte avec nos résultats en regard | aucun calcul ; Subhani (ORB 30 min, vendredis sans annonce) noté comme la piste ORB la plus sérieuse non testée
- [2026-11-22] research | Récolte SSRN sur l'opening range breakout (indices US, ranges 5/15/30 min) : papiers_ssrn_orb_2026-11-22.md, OpenAlex (429 fréquents) + Crossref, 57 requêtes, ~2 000 candidats | 8 papiers fournis (dont réplication de Zarattini-Aziz QQQ 5 min sur la seule période d'origine, bande de bruit NQ +10 $/jour 2 survivants sur 144 essais, ORB 15 min sur l'or nul), 8 écartés, carte des ORB déjà fournis par durée ; aucun calcul, compteur inchangé ; ORB toujours au registre sans condition de réouverture
- [2026-11-22] experiment | Étape 1 de wiki/experiments/fx-exportateur-importateur : grille figée avant calcul (run_fx_balance.py, commit 5f8afd2), 12 devises hors majeures téléchargées (fetch_fx_balance.py, Dukascopy 1 h), contrôle de qualité → 7 gardées (NOK, SEK, PLN, MXN, ZAR, SGD, TRY), solde commercial Banque mondiale de l'année précédente, exploration 2010-01 → 2021-08, compteur 1 937 → 1 940 | ❌ B1 : T1 exportateurs − importateurs −0,60 bp (t −0,72) ; T2 fuseau européen +2,71 bp (t 2,09, Holm 0,054, DSR 0,89, une seule devise importatrice : PLN 2010-2013) ; T3 t 0,49 ; à la place, session domestique négative toutes devises −1,38 bp (t −2,36, sens Zhang H1) → « À surveiller » ; ligne au registre ; réserve 2021-09 → 2026-08 non ouverte

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- **Vrais comptes FTMO en éval depuis le 2026-11-14** : A = compte 511480419 (FTMO-Server), B = 541521340 (FTMO-Server4), 10 000 $ chacun, bascule automatique faite (démo archivée dans `live/etat/archive/`). 1er trade réel : mom SL le 15/11 (A éval −2,50 %, B 0 %) ; relire le journal (`git fetch origin vps-journal`). Toujours en attente de la réponse du support FTMO (A + B long la même nuit, voir [[live/README]]).
- **Plan FTMO retenu (2026-11-04)** : compte A = mom, compte B = 3n + M2, règle des annonces + cible + attente, éval 2,5 % / financé 1 %, scaling 10k → 400k ; détail dans [[wiki/experiments/propfirm-ftmo-option]] (section « Plan retenu »).
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- ~~Or : continuation 17:00 → 5:00 NY sur le reste du jour~~ : ❌ échec du n° 21 le 2026-11-21 (or au comptant 2003-2015, pente nulle), voir [[reports/prereg21_report]].
- **N° 28 (short yen en session US)** : aucun calcul sur le yen après le 2026-08-28 avant la lecture L1 du 2028-02-29 (acheter alors 6J.v.0 Databento avec NQ), puis `uv run python run_prereg28.py --lecture 2028-02-29`.
- **N° 29 (R4 + SL 2 ATR H1 sur le short yen)** : télécharger les ticks USDJPY 2003-05 → 2009-12 (Dukascopy, barres 1 min bid/ask), contrôle de qualité sans moyenne de rendement, puis `uv run python -X utf8 run_prereg29.py --spot <fichier>` une seule fois ; forward aux dates du n° 28 (`--lecture`).
<!-- NEXT-ACTIONS:END -->
