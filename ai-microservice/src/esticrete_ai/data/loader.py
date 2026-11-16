"""Ham proje verisini okuyup şemaya göre temizler; ham dosya değiştirilmez."""

import logging
from pathlib import Path

import pandas as pd

from esticrete_ai.data import schema
from esticrete_ai.settings import get_settings

log = logging.getLogger(__name__)


class SchemaError(ValueError):
    """Ham dosya beklenen şemaya uymuyor."""


def _read_csv(path: Path, columns: dict[str, str]) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"veri dosyası yok: {path} (ai-microservice/data/README.md)")
    # utf-8-sig: kaynak dosyaların bir kısmı BOM'lu
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig", dtype=str, keep_default_na=False)
    df.columns = df.columns.str.strip()
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise SchemaError(f"{path.name}: eksik sütun(lar): {', '.join(missing)}")
    df = df[list(columns)].rename(columns=columns)
    return df.apply(lambda s: s.str.strip()).replace("", pd.NA)


def _to_number(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.str.replace(",", ".", regex=False), errors="coerce")


def load_projects(path: Path | None = None, residential_only: bool = True) -> pd.DataFrame:
    """Temiz ve tipli proje tablosu. Tutarsız süreli ya da zorunlu değeri boş satırlar uyarıyla atılır."""
    path = path or get_settings().projects_csv
    df = _read_csv(path, schema.PROJECT_COLUMNS)

    for col in schema.INTEGER_COLUMNS + schema.POSITIVE_COLUMNS:
        df[col] = _to_number(df[col])
    for col in schema.POSITIVE_COLUMNS:
        df[col] = df[col].where(df[col] > 0)

    unknown_regions = set(df["region"].dropna()) - schema.REGIONS
    if unknown_regions:
        raise SchemaError(f"bilinmeyen bölge(ler): {sorted(unknown_regions)}")
    unknown_ownership = set(df["ownership"].dropna()) - set(schema.OWNERSHIP)
    if unknown_ownership:
        raise SchemaError(f"bilinmeyen kamu / özel değeri: {sorted(unknown_ownership)}")
    df["ownership"] = df["ownership"].map(schema.OWNERSHIP)

    df["categories"] = (
        df["categories"].fillna("").map(lambda s: [c.strip() for c in s.split(",") if c.strip()])
    )
    df["is_residential"] = df["categories"].map(lambda c: schema.RESIDENTIAL_CATEGORY in c)

    n = len(df)
    df = df.dropna(subset=list(schema.REQUIRED_VALUES))
    if len(df) < n:
        log.warning("zorunlu değeri boş %d satır atıldı", n - len(df))

    quarters = (df["end_year"] * 4 + df["end_quarter"]) - (df["start_year"] * 4 + df["start_quarter"])
    bad = quarters != df["duration_quarters"]
    if bad.any():
        log.warning("süresi bitiş − başlangıç ile tutmayan %d satır atıldı", int(bad.sum()))
        df = df[~bad]
    if not df["start_quarter"].between(1, 4).all():
        raise SchemaError("başlangıç çeyreği 1–4 dışında")

    df = df.drop(columns=list(schema.END_COLUMNS))
    if residential_only:
        df = df[df["is_residential"]]

    int_cols = [c for c in schema.INTEGER_COLUMNS if c in df.columns]
    df[int_cols] = df[int_cols].astype("int64")
    if df["project_id"].duplicated().any():
        raise SchemaError("proje kimliği tekrarlıyor")
    return df.reset_index(drop=True)


def load_features(path: Path | None = None) -> pd.DataFrame:
    """Proje özelliklerini (havuz, otopark …) uzun biçimde döndürür: `project_id`, `feature`."""
    path = path or get_settings().features_csv
    df = _read_csv(path, schema.FEATURE_COLUMNS).dropna()
    df["project_id"] = _to_number(df["project_id"]).astype("int64")
    return df.drop_duplicates().reset_index(drop=True)


def training_window(df: pd.DataFrame, years: tuple[int, int] = schema.TRAINING_WINDOW) -> pd.DataFrame:
    """Sağdan kesilmeye karşı eğitim penceresi: başlangıç yılı `years` aralığında olan projeler."""
    first, last = years
    return df[df["start_year"].between(first, last)].reset_index(drop=True)
