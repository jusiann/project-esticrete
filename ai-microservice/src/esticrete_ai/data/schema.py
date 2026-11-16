"""Proje tablosunun şeması: kaynak sütun adları, servis içi adlar ve izin verilen değerler."""

PROJECT_COLUMNS: dict[str, str] = {
    "proje_id": "project_id",
    "bolge": "region",
    "il": "province",
    "ilce": "district",
    "kategori": "categories",
    "kamu_ozel": "ownership",
    "baslangic_yil": "start_year",
    "baslangic_ceyrek": "start_quarter",
    "bitis_yil": "end_year",
    "bitis_ceyrek": "end_quarter",
    "sure_ceyrek": "duration_quarters",
    "arsa_m2": "land_area_m2",
    "kapali_alan_m2": "gross_area_m2",
    "blok_sayisi": "block_count",
    "kat_sayisi": "floor_count",
    "daire_sayisi": "unit_count",
}

# Tahmin anında bilinmeyen ya da hedefi ele veren sütunlar. Yükleyici bunları hiç okumaz:
# asama (hepsi "Tamamlandı"), kayit_tarihi, bedel_usd (alan × birim bedel kestirimi), ihale_no.
# bitis_yil / bitis_ceyrek yalnız süre tutarlılığını sınamak için okunur, sonra atılır.
LEAKAGE_SOURCE_COLUMNS = ("asama", "kayit_tarihi", "bedel_usd", "ihale_no")
END_COLUMNS = ("end_year", "end_quarter")

REGIONS = frozenset(
    {"Marmara", "Ege", "Akdeniz", "İç Anadolu", "Karadeniz", "Doğu Anadolu", "Güneydoğu Anadolu"}
)
OWNERSHIP = {"Özel": "private", "Kamu": "public"}
RESIDENTIAL_CATEGORY = "Konut"

# Sıfır ya da negatif değer "bilinmiyor" sayılır
POSITIVE_COLUMNS = ("land_area_m2", "gross_area_m2", "block_count", "floor_count", "unit_count")
INTEGER_COLUMNS = (
    "project_id",
    "start_year",
    "start_quarter",
    "end_year",
    "end_quarter",
    "duration_quarters",
)
REQUIRED_VALUES = (
    "project_id",
    "region",
    "province",
    "start_year",
    "start_quarter",
    "duration_quarters",
    "gross_area_m2",
)

FEATURE_COLUMNS: dict[str, str] = {"proje_id": "project_id", "ozellik_adi": "feature"}

# Sağdan kesilmeye karşı: uzun sürelerin de gözlenebildiği başlangıç yılları
TRAINING_WINDOW = (2018, 2021)
