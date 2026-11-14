---
type: hot
updated: 2026-11-14 14:08
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 742** (source : [[reports/inference_overnight_report]])
- Dernier pré-enregistrement : n° 26 ([[PREREGISTRATION_26]])
- Idées abandonnées au registre : 35 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-14

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |
| [[wiki/experiments/propfirm-ftmo-option\|Prop firm comme option : FTMO 1-Step avec des trades au hasard]] | active | EV positive sans edge (si les rewards sont versés) |

## Dernières entrées du journal (8)

- [2026-11-14] fix | Jours fériés et demi-séances du bot FTMO : rejeu des fêtes de fin 2025 (Thanksgiving, Noël, 1er janvier), horaires FTMO de Thanksgiving 2026 et FAQ « positions à travers une fermeture » relus ; mom ne rentre plus en financé une nuit qui enjambe un férié (live/bot.py ev_mom, test_book_A_jour_ferie) | M2 sort à 12:59:57 les demi-séances, pas de trade les soirs fermés, 3n sort à 03:00 : conformes ; écart corrigé : FTMO interdit en financé de garder une position à travers une fermeture > 2 h (permis en éval), ce que faisait mom (≈ 9 nuits par an, 148 / 3 981 de 2011 à 2026) ; coût non chiffré
- [2026-11-14] fix | Bascule automatique vers les vrais comptes FTMO (live/bascule.toml armé ; Bot.controle_compte : au 1er nouveau login MT5, archivage de la démo, relance et compte virtuel neuf en mode réel, une seule fois par book, en attente si une position est suivie ; test_bascule_vers_le_compte_reel) et calendrier live/annonces.csv complété jusqu'à fin 2027 (NFP / CPI bls.gov, FOMC federalreserve.gov relus ; minutes = décision + 21 j, PIB avancé 2027 supposés) | il ne reste qu'à acheter les 2 × 1-Step 10k et se connecter dans les deux terminaux, hors position ; ne plus connecter d'essai gratuit d'ici là ; achat suspendu à la réponse du support FTMO sur A + B long la même nuit
- [2026-11-13] query | Règles FTMO 1-Step 10k relues sur ftmo.com (Trading Objectives, page 1-Step, FAQ reward / annonces / stratégies / comptes / VPS, Forbidden Trading Practices), comparées à live/compte.py et au plan retenu | chiffres conformes (79 €, +10 %, 3 % jour, 10 % max fin de journée remis à zéro au nouveau compte, Consistency 50 % du gain total, reward au 14e jour, 90 %, 400 k$ max) ; annonces ±2 min en financé couvertes par les coupures 8:19 / 13:55 ; à vérifier : VPS hors US, et 3 points flous à poser au support (gap trading de mom en éval, exposition cumulée A + B long la même nuit, cible + attente) ; détail dans live/README.md
- [2026-11-13] fix | Passage aux vrais comptes FTMO préparé : drapeau de réinitialisation du compte virtuel (live/reinit.py, Bot.reinitialise_si_demande : archive live/etat/<book> dans live/etat/archive/ puis éval n° 1 à zéro, refusé si position suivie), journal vps-journal nettoyé des fichiers disparus, option objectif_essai_pct dans les configs, checklist « Passage aux vrais comptes FTMO » dans live/README.md | démo au 13/11 : A −5,46 % (7 trades), B financé virtuel +3,91 %, en attente du reward (24/11) ; rien de lancé en réel
- [2026-11-06] query | Inférence des chiffres overnight (run_inference_overnight.py, reports/inference_overnight_report.md, exploratoire, compteur inchangé) : t HAC Newey-West, bootstrap par blocs, Ljung-Box, ARCH-LM, N effectif (Li & Ji), DSR avec N brut et effectif | t HAC > t iid partout (ρ1 négatif ; NQ close-to-open 3,12 → 3,51) ; ARCH massif en bp, absent en R ; N effectif ≈ 610 / 1 742 ; DSR mom 0,005 et NQ CTO 0,016 avec N ≈ 610 (≤ 0,53 avec V = 1/T) : la preuve de mom reste le hors échantillon du n° 11
- [2026-11-06] query | Version anglaise du document overnight en PDF (reports/overnight_research_en.pdf, 5 pages, généré par reportlab depuis un script du scratchpad) | traduction fidèle du document Claude Docs, aucun nouveau calcul
- [2026-11-06] query | Document overnight : ajout d'une section « L'hypothèse : une prime pour porter le risque de la nuit » (mécanisme de risque d'inventaire de Boyarchenko-Larsen-Whelan, 6 prédictions confrontées à nos résultats) | P1, P2 cohérents ; P3, P5 à surveiller ; P4 non démontré (n° 16, approximation VWAP) ; aucun nouveau calcul
- [2026-11-06] query | Document de synthèse de la recherche overnight (Claude Docs « Recherche overnight : hypothèses, protocole et résultats », https://claude.ai/artifact/Rm8gtyyPCG6zuoVtsPtN2m) : cadre, protocole, hypothèses testées, phénomènes significatifs, échecs, suite | rédigé à partir du wiki, aucun nouveau calcul, hors compteur

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- **Passage aux vrais comptes FTMO** : bascule automatique armée (`live/bascule.toml`, 2026-11-14) ; attendre la réponse du support FTMO (A + B long la même nuit, voir [[live/README]]), puis acheter 2 × 1-Step 10k et se connecter dans les deux terminaux MT5, hors position. Ne plus connecter d'essai gratuit d'ici là.
- **Plan FTMO retenu (2026-11-04)** : compte A = mom, compte B = 3n + M2, règle des annonces + cible + attente, éval 2,5 % / financé 1 %, scaling 10k → 400k ; détail dans [[wiki/experiments/propfirm-ftmo-option]] (section « Plan retenu »).
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Holdout NQ : plan figé au n° 26 (mom, M2, 3n SL, rebond) ; fenêtre 2026-08-29 → 11-03 déjà vue (avenant A), holdout officiel à partir du 2026-11-04. Télécharger chaque mois (`uv run python fetch_lse.py NASDAQ100 NQ futures 2026-01-01 <date>`) sans rien calculer ; 1re lecture le 2028-02-29 (Databento acheté à cette date).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
