"""Değerlendirme protokolü: il gruplu çapraz doğrulama, MAE (çeyrek) ana ölçüt."""

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import GroupKFold

Predictor = Callable[[pd.DataFrame, np.ndarray, pd.DataFrame], np.ndarray]


@dataclass(frozen=True)
class Scores:
    mae: float
    rmse: float
    r2: float
    within_1: float
    within_2: float
    fold_mae: tuple[float, ...]


def log_target_predictor(model) -> Predictor:
    """Modeli log(süre) üzerinde eğitir, tahmini çeyreğe geri çevirir."""

    def run(x_train, y_train, x_test):
        fitted = clone(model).fit(x_train, np.log(y_train))
        return np.exp(fitted.predict(x_test))

    return run


def median_predictor(x_train, y_train, x_test):
    return np.full(len(x_test), np.median(y_train))


def area_bin_predictor(n_bins: int = 5, column: str = "log_area") -> Predictor:
    """Referans: kapalı alanı eşit sayılı dilimlere böl, her dilimin medyan süresini ver."""

    def run(x_train, y_train, x_test):
        edges = np.quantile(x_train[column], np.linspace(0, 1, n_bins + 1))[1:-1]
        train_bin = np.digitize(x_train[column], edges)
        medians = pd.Series(y_train).groupby(train_bin).median()
        return medians.reindex(np.digitize(x_test[column], edges)).fillna(np.median(y_train)).to_numpy()

    return run


def cross_validate(
    predictor: Predictor,
    x: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series,
    n_splits: int = 5,
    repeats: int = 3,
    seed: int = 0,
) -> Scores:
    """Aynı ilin projeleri hem eğitimde hem testte olmaz. Ölçütler katlar üzerinden toplanmış tahminlerden."""
    y_arr = y.to_numpy(dtype=float)
    errors, fold_mae = [], []
    for r in range(repeats):
        splitter = GroupKFold(n_splits=n_splits, shuffle=True, random_state=seed + r)
        for train, test in splitter.split(x, y_arr, groups):
            pred = predictor(x.iloc[train], y_arr[train], x.iloc[test])
            err = pred - y_arr[test]
            errors.append(err)
            fold_mae.append(float(np.abs(err).mean()))
    e = np.concatenate(errors)
    total = np.tile(y_arr, repeats)
    return Scores(
        mae=float(np.abs(e).mean()),
        rmse=float(np.sqrt((e**2).mean())),
        r2=float(1 - (e**2).sum() / ((total - total.mean()) ** 2).sum()),
        within_1=float((np.abs(e) <= 1).mean()),
        within_2=float((np.abs(e) <= 2).mean()),
        fold_mae=tuple(fold_mae),
    )
