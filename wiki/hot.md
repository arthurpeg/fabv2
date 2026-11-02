---
type: hot
updated: 2026-11-02 13:58
---

> **Généré automatiquement par `wiki/update_hot.py` (hook Stop). Ne pas éditer à la main**, sauf le bloc « Prochaines actions », conservé à chaque régénération.

# État courant

- Compteur global d'essais : **1 559** (source : [[reports/gc_sessions_report]])
- Dernier pré-enregistrement : n° 20 ([[PREREGISTRATION_20]])
- Idées abandonnées au registre : 29 ([[wiki/Failed Ideas/ledger]])
- Dernière activité : 2026-11-02

## Expériences ouvertes

| Expérience | Statut | Verdict |
|---|---|---|
| [[wiki/experiments/fade-gap-indices\|Fade de gap sur indices (\|z\| > 1, régime post-0DTE)]] | paper-trading | candidat (dépend du régime) |
| [[wiki/experiments/m2-bande-bruit-nq\|Bande de bruit M2 (« Beat the Market », Zarattini et al.) sur NQ]] | paper-trading | rejeté (DSR), surveillé |
| [[wiki/experiments/nq-nuit-momentum\|Règle NQ de nuit : momentum 12-1, entrée 20:00 ET]] | active | candidat |

## Dernières entrées du journal (8)

- [2026-11-02] query | Lecture détaillée de Fattinger-Ziegler « Risk and Return around the Clock » (SSRN 2606706, papiers overnight ssrn/ssrn-2606706.pdf ; résumé existant dans resumes_papiers_overnight_recolte1.md [20]) | papier descriptif, aucune stratégie ; utile pour nos travaux : inefficience de la découverte de prix des métaux pendant les 3-4 premières heures de Globex (≈ 18:00-22:00 NY), cohérente avec la reprise de l'or ; la « contribution au prix » (moyenne de r_i/r) ne mesure pas une dérive exploitable
- [2026-11-02] ingest | Papiers SSRN overnight sur FX majeurs, or et pétrole via Crossref (papiers_ssrn_overnight_fx_or_petrole_2026-11-02.md) | 17 papiers fournis, 5 doublons écartés, 2 sans résumé ; FX : nuit asiatique bruitée et suiveuse pour EUR/GBP, devise européenne en hausse après Londres ; or : découverte du prix partiellement en Asie depuis 2014 ; pétrole quasi vide ; hypothèses H12 à H15 à pré-enregistrer
- [2026-11-01] query | Règle matinée US NQ avec SL/TP ATR, performances en R (reports/nq_matin_sltp_report.md) | SL 2/TP 2 + |z| > 1 : +0,079 R/trade [+0,029 ; +0,128], +6,1 R/an, max DD −31 R, 56 % gagnants, 2010-2017 −0,011 R ; RR 1 : +0,039 R, +3,0 R/an ; règle de nuit pour mémoire +22 R/an, DD −25 R
- [2026-11-01] query | Anatomie de la reprise de l'or 17:00 NY → 9:00 Shanghai : jambes, jour de semaine, roulements, queues, conditionnement, volume (run_gc_reprise.py, exploratoire, compteur 1 577) | portée par le gap de l'arrêt 17:00 → 18:05 (+1,2 bp, t 3,6) et 19:00 → 20:00 NY (+1,0 bp, t 3,2) ; nulle le lundi, +2,5 bp hors lundis ; pas un artefact de roulement ni des queues ; aucun conditionnement utile ; volume 46 contrats/min contre 288 au COMEX, coût 1 tick probablement optimiste
- [2026-11-01] query | Règle matinée US sur NQ (9:30→11:30, |z| > 1, sortie 16:00) avec SL/TP 1/1 et 2/2 ATR M15 (run_nq_matin_sltp.py, exploratoire, compteur 1 559) | SL 1/TP 1 : +1,3 bp/trade net (t 1,6), 99 % sorties sur stop ; SL 2/TP 2 : +4,8 bp (t 3,3, Sharpe 0,83) contre +4,8 sans stop (t 2,0, Sharpe 0,49), DD divisé par ~2 ; 2010-2017 ≈ 0 partout ; règle toujours au registre (n° 20)
- [2026-11-01] abandon | Matinée US → reste de séance (règle n° 20) | rouverte seulement avec une donnée de gamma des options (OPRA)
- [2026-11-01] experiment | n° 20 sur ES et YM, 2010-2026 (run_prereg20.py) | ÉCHEC : ES +2,1 bp/trade net p Holm 0,35, YM −1,1 bp p 0,71 ; les deux négatifs sur 2010-2017 ; ES et YM portés par 2025
- [2026-11-01] prereg | n° 20 : matinée US 9:30→11:30 (|z| > 1) → position 11:30→16:00 sur ES et YM (PREREGISTRATION_20.md, commit 035a8bb) | compteur 1 553 → 1 555 (annoncé 1 520 → 1 522, essais de l'or comptés entre-temps)

## Prochaines actions

<!-- NEXT-ACTIONS:START -->
- Reprendre les n° 10 à 13 dans `RESULTS.md` (les rapports existent, la synthèse s'arrête au n° 9).
- Règle NQ de nuit : pré-enregistrer le test sur le holdout postérieur au 2026-08-28 (à ouvrir une seule fois).
- Or : fenêtre 16:00 → 19:00 NY autour de l'arrêt (+1,4 bp net, choisie après coup, nulle en 2016-19) : candidate au holdout, voir [[reports/gc_sessions_report]].
- Paper trading : fade de gap indices (avec interrupteur de régime) et M2 NQ.
<!-- NEXT-ACTIONS:END -->
