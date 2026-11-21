"""Short yen filtré R4, SL 2 ATR H1 avec TP 2R au lieu de 3R — 1 essai exploratoire, données déjà vues
(6J 2017-01-30 → 2026-08-28), figé avant calcul le 2026-11-21, compteur 1 826 → 1 827.
Même code et mêmes jours que run_prereg29.py --controle ; seul RR change (3 → 2). Le n° 29 reste figé (TP 3R).

uv run python -X utf8 run_jpy_us_r4_tp2.py   → results/prereg29/controle_tp2.txt
"""
import run_prereg29 as p

p.RR = 2.0
if __name__ == "__main__":
    import sys
    sys.argv = ["x", "--controle"]
    orig = p.imprimer
    p.imprimer = lambda res, tr, nom: orig(res, tr, "controle_tp2")
    p.main()
    tr = p.pd.read_csv("results/prereg29/controle_tp2_trades.csv")
    print("\nR par type de sortie :", tr.groupby("exit").R.agg(["count", "mean"]).round(3).to_dict())
