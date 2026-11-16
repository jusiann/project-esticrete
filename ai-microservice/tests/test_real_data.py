"""Yerel gerçek veriyle sınama; veri yoksa atlanır. Yalnız toplu sayılar kontrol edilir."""

import pytest

from esticrete_ai.data import load_features, load_projects, training_window
from esticrete_ai.settings import get_settings

settings = get_settings()
pytestmark = [
    pytest.mark.real_data,
    pytest.mark.skipif(not settings.projects_csv.exists(), reason="yerel veri yok"),
]


def test_residential_count_matches_problem_card():
    df = load_projects()
    assert len(df) == 1569
    assert df["province"].nunique() == 77
    assert (df["ownership"] == "public").sum() == 42


def test_training_window_count_matches_problem_card():
    assert len(training_window(load_projects())) == 851


def test_no_rows_dropped_from_full_table():
    assert len(load_projects(residential_only=False)) == 2100


def test_features_load():
    df = load_features()
    assert df["project_id"].nunique() > 0
