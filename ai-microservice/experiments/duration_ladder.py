"""Süre modeli merdiveni: referanslar ve modeller aynı protokolle ölçülür.

Çalıştırma: uv run python experiments/duration_ladder.py [--out sonuc.md]
Yerel veri gerekir; çıktı yalnız toplu ölçütlerdir.
"""

import argparse
import warnings

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

from esticrete_ai.data import load_features, load_projects, training_window
from esticrete_ai.duration.evaluate import (
    area_bin_predictor,
    cross_validate,
    log_target_predictor,
    median_predictor,
)
from esticrete_ai.duration.features import GROUP, TARGET, build_features
from esticrete_ai.duration.linear_gd import GradientDescentRegressor

REFERENCE = "Alan dilimi medyanı"


def scaled(model):
    return make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler(), model)


def ladder():
    return {
        "Genel medyan": median_predictor,
        REFERENCE: area_bin_predictor(),
        "Doğrusal (sıfırdan GD)": log_target_predictor(scaled(GradientDescentRegressor())),
        "Doğrusal (sklearn)": log_target_predictor(scaled(LinearRegression())),
        "Ridge (L2)": log_target_predictor(scaled(Ridge(alpha=10.0))),
        "Lasso (L1)": log_target_predictor(scaled(Lasso(alpha=0.01))),
        "kNN (k=25)": log_target_predictor(scaled(KNeighborsRegressor(n_neighbors=25))),
        "Karar ağacı": log_target_predictor(
            scaled(DecisionTreeRegressor(max_depth=4, min_samples_leaf=20, random_state=0))
        ),
        "Random Forest": log_target_predictor(
            scaled(RandomForestRegressor(n_estimators=300, min_samples_leaf=10, random_state=0, n_jobs=-1))
        ),
        "SVR (RBF)": log_target_predictor(scaled(SVR(C=1.0, epsilon=0.1))),
        "Gradient boosting": log_target_predictor(
            HistGradientBoostingRegressor(max_iter=200, learning_rate=0.03, max_depth=3, random_state=0)
        ),
    }


def run(projects, amenities, title):
    x = build_features(projects, amenities)
    y, groups = projects[TARGET], projects[GROUP]
    results = {name: cross_validate(p, x, y, groups) for name, p in ladder().items()}
    ref = results[REFERENCE]
    lines = [
        f"### {title} (n = {len(projects)})",
        "",
        "| Model | MAE | RMSE | R² | ±1 çeyrek | ±2 çeyrek | Referansa göre | Kazandığı kat |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for name, s in results.items():
        gain = 100 * (ref.mae - s.mae) / ref.mae
        wins = int(np.sum(np.array(s.fold_mae) < np.array(ref.fold_mae)))
        lines.append(
            f"| {name} | {s.mae:.3f} | {s.rmse:.3f} | {s.r2:.3f} | {s.within_1:.1%} | {s.within_2:.1%} "
            f"| {gain:+.1f}% | {wins} / {len(s.fold_mae)} |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="sonuç tablosunun yazılacağı Markdown dosyası")
    args = parser.parse_args()
    warnings.filterwarnings("ignore")

    projects, amenities = load_projects(), load_features()
    text = "\n\n".join(
        [
            run(projects, amenities, "Bütün konut projeleri"),
            run(training_window(projects), amenities, "Eğitim penceresi 2018–2021"),
        ]
    )
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")


if __name__ == "__main__":
    main()
