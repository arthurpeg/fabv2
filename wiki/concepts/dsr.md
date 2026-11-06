---
type: concept
updated: 2026-10-31
---

# Deflated Sharpe Ratio (DSR)

**Définition** : probabilité que le vrai Sharpe soit > 0 après correction pour le nombre d'essais N, l'asymétrie et le kurtosis des rendements (Bailey & López de Prado). Seuil retenu dans ce dépôt : **DSR > 0,95**.

**Dans ce dépôt** : critère standard des pré-enregistrements, avec N = [[wiki/concepts/compteur-essais|compteur d'essais]] ou N = nombre de règles du lot. Il pénalise fortement les stratégies à gains de crise (M2 NQ : DSR 0,03 avec un Sharpe de 1,14).

**N effectif** (2026-11-06, [[reports/inference_overnight_report]]) : sur les 560 séries d'essais sauvegardées, Meff de Li & Ji = 196 (ratio 0,35), soit ≈ 610 essais effectifs sur 1 742. Ça abaisse SR0 d'environ 9 % seulement : ni mom ni la prime de nuit brute ne passent le DSR contre le compteur global (0,005 / 0,016 avec N ≈ 610 ; 0,42 / 0,53 même avec V = 1/T). Ce qui pèse est V, la dispersion des Sharpe entre essais. La preuve de mom repose sur le hors échantillon pré-enregistré (n° 11), pas sur le DSR global.

**À ne pas confondre avec** : [[wiki/concepts/reality-check|Reality Check de White]], qui teste si le meilleur d'un lot bat le hasard et peut passer quand le DSR échoue.

**Code** : `fab/` (recherche paramétrique avec DSR), `asym.backtest` (permutation).
