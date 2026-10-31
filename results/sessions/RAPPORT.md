# Rendements par session — ES, NQ, YM (Databento 1 min, 2016-01-05 → 2026-08-28)

Script : `run_sessions.py` (rendements calculés par vectorbt, `Portfolio.from_orders`, long 100 % sur chaque session, sans frais).
Données : `D:\quant-data\Cotations\indices\{ES,NQ,YM}_v0_1m.parquet`, ajustées en ratio aux 42 roulements (liste : `rolls_<ACTIF>.csv`).

Sessions (jours = séances NYSE, calendrier XNYS) :
- **Asie** : clôture NYSE précédente (16:00 NY ; 13:00 en demi-séance) → 08:00 Londres
- **Europe** : 08:00 Londres → 09:30 NY
- **US** : 09:30 NY → clôture NYSE
- Asie + Europe = close-to-open ; US = open-to-close (composition vérifiée par assertion).

Prix à T = clôture de la dernière barre démarrant dans [T-5 min, T-1 min] ; jour exclu sinon.

## Résultats (rendements simples, bp par jour)

| Actif | Session | n | Moyenne | Médiane | t | % > 0 | Cumul log (bp) | Annualisé |
|---|---|---|---|---|---|---|---|---|
| ES | Asie | 2670 | 1.99 | 2.99 | 2.13 | 54.3 | 4 994 | 4.83 % |
| ES | Europe | 2670 | 1.48 | 2.64 | 1.69 | 53.3 | 3 671 | 3.53 % |
| ES | **Close-to-open** | 2670 | **3.45** | 5.89 | 2.80 | 55.5 | 8 665 | 8.52 % |
| ES | **US (open-to-close)** | 2670 | **2.11** | 5.59 | 1.31 | 54.0 | 4 716 | 4.55 % |
| NQ | Asie | 2671 | 4.35 | 5.48 | 3.66 | 55.5 | 11 104 | 11.05 % |
| NQ | Europe | 2671 | 0.49 | 1.28 | 0.46 | 51.5 | 904 | 0.86 % |
| NQ | **Close-to-open** | 2671 | **4.81** | 7.35 | 3.12 | 56.3 | 12 008 | 12.00 % |
| NQ | **US (open-to-close)** | 2671 | **3.02** | 7.92 | 1.42 | 54.3 | 6 465 | 6.29 % |
| YM | Asie | 2666 | 1.99 | 2.67 | 2.27 | 54.5 | 5 028 | 4.87 % |
| YM | Europe | 2666 | 1.30 | 2.23 | 1.51 | 53.4 | 3 212 | 3.08 % |
| YM | **Close-to-open** | 2666 | **3.28** | 4.25 | 2.74 | 54.2 | 8 240 | 8.10 % |
| YM | **US (open-to-close)** | 2666 | **1.92** | 3.93 | 1.26 | 53.5 | 4 296 | 4.14 % |

Jours exclus (prix manquant) : ES 8, NQ 7, YM 12 sur 2 678 séances.
Hors jours de roulement (41 par actif), close-to-open : ES 3.37 bp (t 2.71), NQ 4.78 (t 3.06), YM 3.35 (t 2.77).

Détail annuel : `by_year.csv` ; séries journalières : `sessions_<ACTIF>.csv`.

## Lecture

- Close-to-open positif et significatif sur les trois (t ≈ 2.7–3.1). L'essentiel vient de la session asiatique, surtout sur NQ (4.35 bp/jour contre 0.49 en Europe).
- La session US n'est **pas négative** sur 2016-2026 : +1.9 à +3.0 bp/jour, non significatif (t ≈ 1.3–1.4). L'affirmation « open-to-close négatif » ne se retrouve pas sur ces futures et cette période ; la décomposition donne plutôt « overnight fort et régulier, intraday positif mais bruité ».
- L'US est très instable d'une année à l'autre (ES : −1 864 bp en 2018, +1 829 bp en 2023), alors que le close-to-open n'est négatif qu'en 2016 (ES, faible), 2022 et 2023 (ES/YM, faible).
- Rendements de futures ajustés = rendement excédentaire (indice + dividendes − taux), pas le rendement prix de l'indice cash.
