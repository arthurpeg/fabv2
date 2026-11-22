---
type: research
updated: 2026-11-22
source: recherche_causalite_intraday.md, PAPER_SPECS.md
status: ingested
---

# Littérature intraday : mécanismes M1 à M5

**Ce que c'est** : la revue de départ ([[recherche_causalite_intraday]]) a classé les effets intraday en cinq mécanismes ; [[PAPER_SPECS]] fixe la spécification exacte des papiers lus en texte intégral.

| Mécanisme | Papiers | Ce qu'on a trouvé |
|---|---|---|
| M1 momentum intraday | Gao 2014, Baltussen, Rosa 2022 | Absent sur indices ; réel en brut sur FX avec la bonne session, < coût |
| M2 bande de bruit | Zarattini et al. 2024 | NQ fort mais rejeté par le DSR ; ES perd depuis la publication |
| M3 ORB | Zarattini ORB, Fetna, Tsai ; récolte ORB du 2026-11-22 ([[papiers_ssrn_orb_2026-11-22]]) | Tué par les coûts ; s'effondre après 2023. Non testés : filtre « vendredi sans annonce » (Subhani, 30 min) et sens de la 1ʳᵉ bougie de 5 min (Zarattini-Aziz, ≠ cassure) |
| M4 sur-réaction / reversal | Caporale-Plastun, Ladia 2026 | Fade de gap post-0DTE = seul candidat ; or : signe inverse |
| M5 horloge et fixings | Krohn 2023, Breedon-Ranaldo, Bondarenko | Effet réel, 1 à 2,5 ticks, < coût ; utile pour l'exécution |

**Contradictions avec les papiers** : Caporale (or contrarien) inversé ; Tolušić ≈ ⅓ de l'effet annoncé ; Melvin-Prins ≈ ½ après la réforme de 2015 ; NP-FDA ne bat pas le MCO (De Gooijer).

**Liens** : [[RESULTS]] · [[wiki/Failed Ideas/ledger]]
