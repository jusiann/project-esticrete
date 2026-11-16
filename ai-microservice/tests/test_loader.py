import pandas as pd
import pytest

from esticrete_ai.data import SchemaError, load_features, load_projects, training_window
from tests.conftest import HEADER, ROWS, write_csv


def test_residential_rows_are_kept_and_bad_rows_dropped(projects_csv):
    df = load_projects(projects_csv)
    assert df["project_id"].tolist() == [1, 2, 4]


def test_all_rows_when_not_residential_only(projects_csv):
    df = load_projects(projects_csv, residential_only=False)
    assert sorted(df["project_id"]) == [1, 2, 3, 4]
    assert not df.set_index("project_id").loc[3, "is_residential"]


def test_leakage_and_end_columns_are_not_returned(projects_csv):
    df = load_projects(projects_csv)
    for col in ("asama", "bedel_usd", "ihale_no", "kayit_tarihi", "end_year", "end_quarter"):
        assert col not in df.columns


def test_types_and_cleaning(projects_csv):
    df = load_projects(projects_csv).set_index("project_id")
    assert df.loc[2, "land_area_m2"] == 1250.5  # Türkçe virgül
    assert pd.isna(df.loc[4, "land_area_m2"])  # 0 → bilinmiyor
    assert pd.isna(df.loc[2, "floor_count"])
    assert df.loc[2, "ownership"] == "public" and df.loc[1, "ownership"] == "private"
    assert df.loc[2, "categories"] == ["Konut", "Cadde Dükkan"]
    assert df["duration_quarters"].dtype == "int64"


def test_missing_column_raises(tmp_path):
    header = HEADER.replace("sure_ceyrek", "sure")
    with pytest.raises(SchemaError, match="sure_ceyrek"):
        load_projects(write_csv(tmp_path / "p.csv", header=header))


def test_unknown_region_raises(tmp_path):
    rows = [ROWS[0].replace("Marmara", "Trakya")]
    with pytest.raises(SchemaError, match="bölge"):
        load_projects(write_csv(tmp_path / "p.csv", rows=rows))


def test_duplicate_project_id_raises(tmp_path):
    with pytest.raises(SchemaError, match="tekrar"):
        load_projects(write_csv(tmp_path / "p.csv", rows=[ROWS[0], ROWS[0]]))


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_projects(tmp_path / "yok.csv")


def test_training_window(projects_csv):
    df = load_projects(projects_csv)
    assert training_window(df)["project_id"].tolist() == [1, 2]
    assert training_window(df, (2022, 2022))["project_id"].tolist() == [4]


def test_load_features(tmp_path):
    p = tmp_path / "ozellikler.csv"
    p.write_text("proje_id;ozellik_adi\n1;Yüzme Havuzu\n1;Yüzme Havuzu\n2;Jeneratör\n", encoding="utf-8")
    df = load_features(p)
    assert df.to_dict("records") == [
        {"project_id": 1, "feature": "Yüzme Havuzu"},
        {"project_id": 2, "feature": "Jeneratör"},
    ]
