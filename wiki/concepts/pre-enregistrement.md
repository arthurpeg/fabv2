---
type: concept
updated: 2026-10-31
---

# Pré-enregistrement

**Définition** : document `PREREGISTRATION_<n>.md` écrit et commité **avant** tout calcul de rendement ou de P&L. Il fige la règle, les paramètres, les données, les coûts et les critères de succès. Le hash du commit prouve l'antériorité.

**Dans ce dépôt** :
- Tout paramètre ajouté après coup est marqué « post-hoc » et compté dans le [[wiki/concepts/compteur-essais|compteur d'essais]].
- Les amendements sont permis seulement avant l'exécution, et commités à part (ex. n° 5, amendements 1 à 3).
- On ne déplace pas la barre après coup : un critère échoué = rejet, même si un autre test passe (cas de [[wiki/experiments/m2-bande-bruit-nq|M2 sur NQ]]).
- Les tests « descriptifs » (n° 12, robust13) sont annoncés comme tels et ne valident rien.

**Voir aussi** : [[wiki/concepts/is-oos]] · [[wiki/concepts/dsr]]
