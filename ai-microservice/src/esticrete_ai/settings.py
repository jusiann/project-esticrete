"""Servis ayarları: yollar tek yerde, ortam değişkeniyle değiştirilebilir."""

import os
from dataclasses import dataclass
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    data_dir: Path

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def catalog_dir(self) -> Path:
        return self.data_dir / "catalog"

    @property
    def projects_csv(self) -> Path:
        return self.raw_dir / "yapiradar" / "projeler.csv"

    @property
    def features_csv(self) -> Path:
        return self.raw_dir / "yapiradar" / "ozellikler.csv"


def get_settings() -> Settings:
    """`ESTICRETE_DATA_DIR` verilmişse onu, yoksa `ai-microservice/data` klasörünü kullanır."""
    data_dir = os.environ.get("ESTICRETE_DATA_DIR")
    return Settings(data_dir=Path(data_dir) if data_dir else SERVICE_ROOT / "data")
