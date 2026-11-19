"""Validation glissante et audit anti-fuite.

À chaque réestimation r : entraînement sur les jours [0, r) (expansif) ou
[r − L, r) (glissant), prévision des jours [r, r + N). ACP, échelle, h, h_y,
coefficients et m_ref sont réajustés sur l'entraînement seulement.

L'audit vérifie, pour chaque prévision :
- que la dernière barre utilisée par les variables se termine au plus tard à
  t_decision (et a donc commencé strictement avant) ;
- que le dernier jour d'entraînement est strictement antérieur au jour prédit.
Le run échoue (`LeakError`) sinon.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from gap.data import Sample
from gap.features import FeatureBuilder
from gap.models import NPFDA, OLS


class LeakError(AssertionError):
    pass


def splits(n: int, initial: int, every: int, scheme: str = "expanding", window: int | None = None):
    for r in range(initial, n, every):
        lo = 0 if scheme == "expanding" else max(0, r - (window or initial))
        yield np.arange(lo, r), np.arange(r, min(r + every, n))


def audit(s: Sample, markets: list[str], train: np.ndarray, test: np.ndarray) -> pd.Timestamp:
    last = s.last_feature_end(markets)[test]
    if last.isna().any() or (last > s.t_decision[test]).any():
        raise LeakError("une variable utilise une barre terminée après t_decision")
    train_end = s.days[train].max()
    if not train_end < s.days[test].min():
        raise LeakError("la fenêtre d'entraînement chevauche le jour prédit")
    return train_end


def walk_forward(s: Sample, markets: list[str], targets: dict[str, np.ndarray], cfg: dict) -> dict[str, pd.DataFrame]:
    """Prévisions hors échantillon, une table par cible (index = jour prédit)."""
    wf, npc = cfg["walkforward"], cfg["npfda"]
    rows: dict[str, list[pd.DataFrame]] = {k: [] for k in targets}
    for train, test in splits(len(s), wf["initial_train"], wf["refit_every"], wf["scheme"], wf.get("rolling_train")):
        train_end = audit(s, markets, train, test)
        fb = FeatureBuilder(markets, cfg["features"]["n_pc"]).fit(s, train)
        Ztr, Zte = fb.scores(s, train), fb.scores(s, test)
        Xtr, Xte = fb.linear(s, train), fb.linear(s, test)
        Str, Ste = fb.subperiods(s, train), fb.subperiods(s, test)
        for name, y in targets.items():
            ok = np.isfinite(y[train])
            ytr = y[train][ok]
            np_ = NPFDA(npc["h_quantiles"], npc["mode_grid"], npc["cpi_level"]).fit(Ztr[ok], ytr)
            f = np_.predict(Zte)
            rows[name].append(pd.DataFrame({
                "y": y[test],
                "ols": OLS().fit(Xtr[ok], ytr).predict(Xte),
                "ols_sub": OLS().fit(Str[ok], ytr).predict(Ste),
                "np_mean": f.mean, "np_median": f.median, "np_mode": f.mode, "p_up": f.p_up,
                "lo": f.lo, "hi": f.hi, "no_signal": f.no_signal,
                "m_ref": np.median(np.abs(ytr)), "h": np_.h_, "n_train": ok.sum(),
                "train_end": train_end, "last_feature_end": s.last_feature_end(markets)[test],
                "t_decision": s.t_decision[test],
            }, index=s.days[test]))
    return {k: pd.concat(v) for k, v in rows.items()}
