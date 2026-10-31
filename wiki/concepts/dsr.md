---
type: concept
updated: 2026-10-31
---

# Deflated Sharpe Ratio (DSR)

**Définition** : probabilité que le vrai Sharpe soit > 0 après correction pour le nombre d'essais N, l'asymétrie et le kurtosis des rendements (Bailey & López de Prado). Seuil retenu dans ce dépôt : **DSR > 0,95**.

**Dans ce dépôt** : critère standard des pré-enregistrements, avec N = [[wiki/concepts/compteur-essais|compteur d'essais]] ou N = nombre de règles du lot. Il pénalise fortement les stratégies à gains de crise (M2 NQ : DSR 0,03 avec un Sharpe de 1,14).

**À ne pas confondre avec** : [[wiki/concepts/reality-check|Reality Check de White]], qui teste si le meilleur d'un lot bat le hasard et peut passer quand le DSR échoue.

**Code** : `fab/` (recherche paramétrique avec DSR), `asym.backtest` (permutation).
