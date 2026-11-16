"""Süre modelinin özellik matrisi. Eğitim ve çıkarım aynı fonksiyonu kullanır."""

import numpy as np
import pandas as pd

from esticrete_ai.data import schema

TARGET = "duration_quarters"
GROUP = "province"

# Yeterince sık görülen ve süreyle ilişkisi keşifsel analizde görülen proje özellikleri
AMENITIES = (
    "Güvenlik Sistemleri",
    "Çocuk Oyun Alanları",
    "Spor Alanları",
    "Yüzme Havuzu",
    "Jeneratör",
    "Fitness",
    "Hamam / Spa / Sauna",
)
REGIONS = tuple(sorted(schema.REGIONS))


def build_features(projects: pd.DataFrame, amenities: pd.DataFrame | None = None) -> pd.DataFrame:
    """Sayısal özellik tablosu. Eksik değerler NaN kalır; doldurma model hattının işidir.

    Başlangıç yılı bilerek yoktur (sağdan kesilme). İl yalnız gruplama için kullanılır.
    """
    p = projects
    x = pd.DataFrame(index=p.index)
    x["log_area"] = np.log(p["gross_area_m2"])
    x["log_units"] = np.log(p["unit_count"])
    x["log_blocks"] = np.log(p["block_count"])
    x["log_land"] = np.log(p["land_area_m2"])
    x["log_units_per_block"] = x["log_units"] - x["log_blocks"]
    x["is_public"] = (p["ownership"] == "public").astype(float)
    for q in (2, 3, 4):
        x[f"start_q{q}"] = (p["start_quarter"] == q).astype(float)
    for region in REGIONS[1:]:
        x[f"region_{region}"] = (p["region"] == region).astype(float)

    if amenities is not None:
        own = amenities[amenities["project_id"].isin(p["project_id"])]
        counts = own.groupby("project_id").size()
        x["amenity_count"] = p["project_id"].map(counts).fillna(0).to_numpy(dtype=float)
        for name in AMENITIES:
            ids = set(own.loc[own["feature"] == name, "project_id"])
            x[f"has_{name}"] = p["project_id"].isin(ids).to_numpy(dtype=float)
    return x
