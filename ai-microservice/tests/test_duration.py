import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from esticrete_ai.data import load_projects
from esticrete_ai.duration.evaluate import area_bin_predictor, cross_validate, median_predictor
from esticrete_ai.duration.features import build_features
from esticrete_ai.duration.linear_gd import GradientDescentRegressor


def test_gradient_descent_matches_closed_form():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, 3))
    y = X @ np.array([2.0, -1.0, 0.5]) + 3.0 + rng.normal(scale=0.1, size=200)
    gd = GradientDescentRegressor(learning_rate=0.1, n_iter=5000).fit(X, y)
    ref = LinearRegression().fit(X, y)
    assert np.allclose(gd.coef_, ref.coef_, atol=1e-4)
    assert abs(gd.intercept_ - ref.intercept_) < 1e-4
    assert gd.loss_history_[-1] < gd.loss_history_[0]


def test_features_have_no_year_and_keep_missing(projects_csv):
    p = load_projects(projects_csv)
    amenities = pd.DataFrame({"project_id": [1, 1, 2], "feature": ["Yüzme Havuzu", "Jeneratör", "Fitness"]})
    x = build_features(p, amenities)
    assert not any("year" in c for c in x.columns)
    assert x["amenity_count"].tolist() == [2.0, 1.0, 0.0]
    assert x["has_Yüzme Havuzu"].tolist() == [1.0, 0.0, 0.0]
    assert np.isnan(x.loc[2, "log_land"])  # arsa 0 → bilinmiyor, doldurma hattın işi
    assert x.loc[1, "is_public"] == 1.0


def test_cross_validate_keeps_groups_apart_and_scores():
    rng = np.random.default_rng(1)
    n = 300
    x = pd.DataFrame({"log_area": rng.normal(8, 1, n)})
    y = pd.Series(np.clip(np.round(x["log_area"] - 2 + rng.normal(0, 0.5, n)), 1, None))
    groups = pd.Series(rng.integers(0, 20, n))
    base = cross_validate(median_predictor, x, y, groups)
    binned = cross_validate(area_bin_predictor(), x, y, groups)
    assert binned.mae < base.mae
    assert len(base.fold_mae) == 15
