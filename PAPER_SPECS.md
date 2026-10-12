# Fiches de spécification (lecture des textes intégraux)

*2026-10-12. Les PDF sont dans `papers/` (exclu du dépôt pour des raisons de droits d'auteur). Pour chaque papier : la source effectivement lue, les règles exactes, et l'écart avec mes premiers tests (M1-M5).*

## Ce qui a pu être lu

| Papier | Source lue | Statut |
|---|---|---|
| Gao, Han, Li, Zhou, *Market Intraday Momentum* | Working paper déc. 2015 (copie mql5 du WP des auteurs) | ✅ texte intégral |
| Baltussen, Da, Lammers, Martens, *Hedging Demand and Market Intraday Momentum* (JFE 2021) | Version publiée, page de Zhi Da (nd.edu) | ✅ texte intégral |
| Zarattini, Aziz, Barbon, *Beat the Market* | Dépôt de l'Université de Saint-Gall (version du 2025-02-03) | ✅ texte intégral |
| Zarattini & Aziz, *Can Day Trading Really Be Profitable?* | Copie tierce (wealth-lab), 18 pages, conforme à la description SSRN | ✅ texte intégral |
| Krohn, Mueller, Whelan, *FX Fixings and Returns Around the Clock* (JF 2023) | Manuscrit accepté (Warwick WRAP) | ✅ texte intégral |
| Breedon & Ranaldo, *Intraday Patterns in FX Returns and Order Flow* | WP Queen Mary n° 694 (2012) | ✅ texte intégral |
| Caporale & Plastun, *Gold and oil prices: abnormal returns…* (FMPM 2021) | Springer, accès libre | ✅ texte intégral (formules perdues à l'extraction) |
| Caporale, Gil-Alana, Plastun, *Short-Term Price Overreactions* | WP CESifo 5066 | ✅ texte intégral |
| Tsai et al., *Timely ORB on Index Futures* (IEEE Access 2019) | IEEE, accès libre | ✅ texte intégral |
| Bondarenko & Muravyev, *Market Return Around the Clock* | Résumé JFQA + résumé Alpha Architect (secondaire) | ⚠️ résumé seulement |
| Rosa 2022 ; Wen et al. 2022/23 (EIA) ; Elaut et al. ; Grant et al. ; Ladia, Fetna, Seeck, Paz, Delgado, Mesfin, Mahadzva 2026 | SSRN (bloqué par Cloudflare), Wiley/Elsevier payants ; le PDF d'Adelaide pour Wen renvoie une erreur 404 | ❌ non lus |

## Fiches

### Gao et al.: momentum intraday sur SPY
- r₁ = clôture J-1 → **10:00** ET ; r₁₂ = 15:00 → 15:30 ; r₁₃ = 15:30 → 16:00. SPY, 1993-2013, jours avec moins de 500 trades exclus.
- η(r₁) : long sur r₁₃ si r₁ > 0, short sinon. **Variante jointe η(r₁, r₁₂)** : long si les deux sont > 0, short si les deux sont ≤ 0, sinon pas de position.
- Coûts examinés seulement après la décimalisation (section 5.2).
- **Écart avec M1a** : aucun pour η(r₁). La variante jointe n'avait pas été testée.

### Baltussen et al.: momentum intraday sur plus de 60 futures
- r_ONFH = clôture J-1 → ouverture + 30 min ; **r_ROD = clôture J-1 → clôture − 30 min** ; r_LH = 30 dernières minutes. Seules les heures de la session « commune » sont gardées.
- Heures (Table 1) : ES/NQ/YM 9:30-16:00 ; **GC 8:20-13:30** ; **CL 9:00-14:30** ; **futures FX (EC, JY, BP, AD) 7:20-14:00 CT = 8:20-15:00 ET** (pics de volume de la criée des options, et 15:00 ET = fin de la période de settlement).
- η(r) = r_LH si r > 0, sinon −r_LH ; variante jointe η(r_ONFH, r_ROD). **Aucun coût** dans le papier. Les auteurs notent qu'à 1 tick sur ES, le Sharpe net reste positif sur 1974-2020.
- **Écart avec M1** : j'avais pris la session FX à 08:00-16:00 **heure de Londres**, au lieu de 8:20-15:00 ET. Variante jointe non testée.

### Zarattini, Aziz, Barbon, « Beat the Market »
- σ(HH:MM) = moyenne sur les **14 jours précédents** de |Close(HH:MM)/Open(9:30) − 1|. Bande haute = max(Open, Close J-1 16:00)·(1+σ), bande basse = min(…)·(1−σ).
- Décisions **seulement à HH:00 et HH:30**. Long au-dessus de la bande, short en dessous. Stop suiveur = max(bande haute, VWAP) pour une position longue, min(bande basse, VWAP) pour une courte, vérifié aux mêmes heures. Tout est fermé à 16:00. VWAP calculé sur les heures de marché. Exécution à l'Open de la minute HH:MM.
- Taille de base : 100 % des fonds (Sharpe 1,24). **Version finale : volatilité journalière cible σ_target = 2 %, avec σ = écart-type des 14 derniers rendements journaliers de SPY ; levier = min(4, 2 %/σ)** (Sharpe 1,33). Coûts : 0,0035 $/action + 0,001 $ de slippage.
- **Écart avec M2** : la version 100 % est fidèle. Il manque la **volatilité cible avec levier jusqu'à 4×**.

### Zarattini & Aziz : ORB 5 minutes sur QQQ
- **Ce n'est pas une cassure.** On prend le sens de la **1ʳᵉ bougie de 5 minutes** (long si close > open, short si close < open, rien si c'est un doji). Entrée à l'**open de la 2ᵉ bougie** (9:35). Stop au plus bas (long) ou au plus haut (short) de la 1ʳᵉ bougie. **Objectif à 10R**, sinon sortie à la clôture.
- Taille : on risque **1 % du capital** par trade (taille = 1 % × capital / R), avec un **levier plafonné à 4**. Commission de 0,0005 $/action, sans slippage. QQQ 2016-2023.
- **Écart avec M3b** : complet (j'avais testé une cassure du range de 5 minutes).

### Krohn, Mueller, Whelan : fixings FX
- Fenêtres en ET : pré-Tokyo 17:00 → 20:55 (Tokyo 9:55) ; post-Tokyo 20:55 → 2:00 ; pré-BCE 2:00 → 8:15 ; BCE-Londres 8:15 → 11:00 (exclue) ; post-Londres 11:00 → 17:00.
- Stratégie : **Tokyo** = long USD pré-Tokyo, puis short USD post-Tokyo. **Europe** = long USD pré-BCE, puis short USD post-Londres. Aucun coût. Rendements en baisse en fin d'échantillon (1999-2019).
- **Écart avec M5b/M5c** : complet. J'avais pris des fenêtres d'une heure autour des fixes, au lieu de fenêtres de 4 à 6 heures.

### Breedon & Ranaldo : la devise se déprécie pendant ses propres heures
- Sessions (heure de New York) : **EUR et GBP 2:00-8:00**, **USD 8:00-16:00**. Japon 8:00-15:00 et Australie 10:00-16:00 en heure locale.
- Stratégie : short la devise de base pendant sa session, long pendant la session de la contrepartie. Après coûts (bid/ask EBS), **seul EUR/USD est rentable** : Sharpe 1,3 sur le short du matin, 0,9 sur le long de l'après-midi.
- **Écart avec M5d** : il manquait la jambe longue pendant la session USD, et mes fenêtres européennes étaient fausses.

### Caporale & Plastun : jour anormal sur l'or et le pétrole
- Jour de 24 heures en **GMT+3**. R = Close/Open − 1, avec l'open du jour pour éviter les gaps. Jour anormal si R > moyenne + **k = 2** σ (et symétriquement à la baisse). La période n de calcul n'est pas précisée dans le texte extrait (formules perdues).
- **Stratégie 1** : dès que le seuil est franchi dans la journée, position dans le sens du mouvement jusqu'à la fin du jour (environ 70 % de trades gagnants dans le papier). **Stratégie 2** : le lendemain, en suivant le mouvement pour le pétrole (toute la journée) et en contrarien pour l'or (jusqu'à 6:00 GMT+3 après un jour positif, toute la journée après un jour négatif). Aucun coût. Période 2009 à 2020-03.
- **Écart avec M4** : M4a utilisait une fenêtre de 30 minutes à l'ouverture et un z sur 60 jours, sans détection en cours de séance sur le jour de 24 heures.

### Tsai et al.: Timely ORB
- La fenêtre de sondage est **optimisée** en échantillon (1 à 5 minutes pour les US). Ce n'est pas une règle fixe : **non répliqué**, car il faudrait refaire la recherche de paramètres.

### Bondarenko & Muravyev
- E-mini S&P, 2004-2018. Fenêtre « EU-open » **23:30 → 3:30 ET** selon le résumé d'Alpha Architect (source secondaire, non vérifiée dans le papier).
- **Écart avec M5a** : j'avais pris 01:00 → 05:00 ET.
