---
type: concept
updated: 2026-10-31
---

# Fuseau horaire des fichiers HistData

**Définition** : les CSV HistData suivent un décalage avec les règles d'heure d'été **européennes** (heure brute + 7 h = heure d'Athènes), et non un EST fixe comme le dit leur FAQ.

**Autre piège** : le fichier DAX de HistData contient un autre indice de 2020-06 à 2023-12 (exclu par l'amendement du n° 5).

**Code** : `gap/` (chargeur HistData, alignement DST, tests). **Rapport** : [[reports/opening_gap_report]].
