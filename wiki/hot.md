---
type: hot
updated: 2026-11-02 14:48
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 631** (source : [[reports/si_fattinger_report]])
- Dernier pré-enregistrement : n° 21 ([[PREREGISTRATION_21]])
- Idées abandonnées au registre : 30 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-02

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-02] schema | Nouvelle règle de projet : registre des phénomènes confirmés (wiki/phenomenes.md, CLAUDE.md règle 3, SCHEMA) | 17 phénomènes confirmés amorcés (or et argent Fattinger-Ziegler, prime de nuit, règle NQ de nuit, minute 08:55 du DAX, reprise de l'or) et 3 à surveiller
- [2026-11-02] query | Affirmations de Fattinger-Ziegler testées sur l'argent SI 5 min 2017-2026, données London Strategic Edge ajustées par nos soins (run_gc_fattinger.py SI, reports/si_fattinger_report.md, exploratoire, compteur 1 631 → 1 685, 54 tests ; SI ajouté à recolte1.engine avec détection des roulements par le volume) | même microstructure que l'or en plus bruyante : 8:30 × 3,2, Fed × 6,4, Tokyo × 1,7, sauts 7,3 % ; 28,5 % du prix avant 3:00 NY (contredit le papier) ; pas de pic à 13:30 ; début de Globex non bruité ; continuation de nuit b ≈ 1,2 non significative après Holm, portée par 2023-2026
- [2026-11-02] ingest | Argent (SI) 1 minute via l'API London Strategic Edge, plan gratuit, marché `futures` (fetch_lse.py → cache/lse/SI_lse_1m.parquet) | 3,02 M barres 2017-04-02 → 2026-08-28 ; rien avant 2017 ; GOLD de la même source = GC Databento à 1 tick près ; série front non ajustée qui roule au 1er jour du mois de livraison : 114 séances quasi vides (2-3 avant chaque roulement), à filtrer et ajuster avant usage ; contrats individuels (marché cme) payants
- [2026-11-02] query | Affirmations de Fattinger-Ziegler (SSRN 2606706) testées sur l'or GC 5 min 2016-2026 (run_gc_fattinger.py, reports/gc_fattinger_report.md, exploratoire, compteur 1 577 → 1 631, 54 tests) | microstructure reproduite (pic 8:30 × 4,8, Tokyo × 2, Fed × 7, sauts 9 % dont 8:30 = 2 %, pas de U, volume < volatilité la nuit, VWPC nuit 1,29) ; contredit : 26,5 % du prix avant 3:00 NY ; non confirmé : début de Globex bruité, chute d'efficience avant l'Europe ; continuation 17:00→5:00 (b 1,13) seulement 2023-2026
- [2026-11-02] query | Lecture détaillée de Fattinger-Ziegler « Risk and Return around the Clock » (SSRN 2606706, papiers overnight ssrn/ssrn-2606706.pdf ; résumé existant dans resumes_papiers_overnight_recolte1.md [20]) | papier descriptif, aucune stratégie ; utile pour nos travaux : inefficience de la découverte de prix des métaux pendant les 3-4 premières heures de Globex (≈ 18:00-22:00 NY), cohérente avec la reprise de l'or ; la « contribution au prix » (moyenne de r_i/r) ne mesure pas une dérive exploitable
- [2026-11-02] ingest | Papiers SSRN overnight sur FX majeurs, or et pétrole via Crossref (papiers_ssrn_overnight_fx_or_petrole_2026-11-02.md) | 17 papiers fournis, 5 doublons écartés, 2 sans résumé ; FX : nuit asiatique bruitée et suiveuse pour EUR/GBP, devise européenne en hausse après Londres ; or : découverte du prix partiellement en Asie depuis 2014 ; pétrole quasi vide ; hypothèses H12 à H15 à pré-enregistrer
- [2026-11-01] query | Règle matinée US NQ avec SL/TP ATR, performances en R (reports/nq_matin_sltp_report.md) | SL 2/TP 2 + |z| > 1 : +0,079 R/trade [+0,029 ; +0,128], +6,1 R/an, max DD −31 R, 56 % gagnants, 2010-2017 −0,011 R ; RR 1 : +0,039 R, +3,0 R/an ; règle de nuit pour mémoire +22 R/an, DD −25 R
- [2026-11-01] query | Anatomie de la reprise de l'or 17:00 NY → 9:00 Shanghai : jambes, jour de semaine, roulements, queues, conditionnement, volume (run_gc_reprise.py, exploratoire, compteur 1 577) | portée par le gap de l'arrêt 17:00 → 18:05 (+1,2 bp, t 3,6) et 19:00 → 20:00 NY (+1,0 bp, t 3,2) ; nulle le lundi, +2,5 bp hors lundis ; pas un artefact de roulement ni des queues ; aucun conditionnement utile ; volume 46 contrats/min contre 288 au COMEX, coût 1 tick probablement optimiste

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
- Or : continuation du mouvement 17:00 → 5:00 NY sur le reste du jour (pente 1,13, uniquement 2023-2026, trouvée parmi 23 coupures) : candidate au holdout, voir [[reports/gc_fattinger_report]].
<!-- NEXT-ACTIONS:END -->
