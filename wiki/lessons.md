---
type: lessons
updated: 2026-10-31
---

# Leçons transversales

Synthèse de ce qui a été appris sur l'ensemble des expériences. Chaque leçon renvoie aux pages qui la fondent. À réviser quand une nouvelle expérience la confirme ou la contredit.

## Sur les effets publiés
1. **Effet réel ≠ effet tradable.** Avec la spécification exacte, la plupart des effets publiés se retrouvent en brut (Baltussen FX, Krohn, Breedon, Zarattini ORB), mais valent 0,5 à 3 ticks par trade pour 1,4 à 2 ticks de [[wiki/concepts/cout-standard|coût]]. → [[wiki/research/litterature-intraday]]
2. **Les effets s'affaiblissent après publication** : Krohn, ORB de Zarattini, Breedon sur EUR, M2 sur ES.
3. **La spécification exacte compte** : la mauvaise session FX donnait un M1 négatif même en brut. Lire le texte intégral avant de coder ([[PAPER_SPECS]]).
4. Les papiers sans coûts ou à coûts institutionnels surestiment ce qui est captable (Tolušić : ≈ ⅓ de l'effet annoncé ; l'effet tient dans la première minute).

## Sur la méthode
5. **Le multiple testing domine tout** : à N = 93, deux survivants sont compatibles avec le bruit ; à N ≈ 930 (récolte 1), ~23 IC positifs sont attendus au hasard. Toujours rapporter le [[wiki/concepts/compteur-essais|compteur]] et le [[wiki/concepts/dsr|DSR]].
6. **Vérifier que le filtre a réellement agi** : au n° 11, 100 % des trades étaient longs ; le test validait « long la nuit », pas le momentum.
7. **Toujours comparer à la référence triviale** : un long de mêmes heures, une entrée aléatoire, le contrarien ouverture → clôture (Valenti n'apportait rien, corrélation 0,90).
8. **Regarder 2020 à part** : plusieurs résultats (LETF ES, Valenti, nuits) viennent surtout de 2020.
9. Le DSR et le Reality Check peuvent diverger ; la règle fixée à l'avance tranche ([[wiki/concepts/pre-enregistrement]]).
10. Les SL/TP en ATR ne créent pas d'edge (contrôle pile ou face) ; ils changent la queue de distribution, pas le Sharpe.

## Sur les données
11. Pièges connus : fuseau HistData ([[wiki/concepts/histdata-fuseau]]), fichier DAX corrompu 2020-06 → 2023-12, roulements manqués par `fab.core.load` ([[wiki/concepts/roulements]]).

## Ce qui tient
La seule chose robuste trouvée à ce jour : la [[wiki/concepts/prime-de-nuit|prime de nuit]] de NQ ([[wiki/experiments/nq-nuit-momentum]]). Candidats secondaires : [[wiki/experiments/fade-gap-indices]] (régime 0DTE) et [[wiki/experiments/m2-bande-bruit-nq]] (rejeté, surveillé).
- Plusieurs comptes de prop firm sur la même règle ne se diversifient pas en les décalant dans le temps : ils meurent dans le même drawdown et se resynchronisent (corrélation 0,97). Il faut des flux différents : trois heures d'entrée de la même règle lissent les rentrées mensuelles (corrélation trimestrielle 0,56) mais pas le résultat sur deux ans, dominé par le régime de marché. ([[reports/prereg18_report]], 2026-10-31)
