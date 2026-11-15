# data

Bu klasördeki dosyaların **hiçbiri repoya girmez** (`ai-microservice/.gitignore`: `data/*`, yalnız bu README izlenir). Dosyalar yerelde, eski çalışma alanından (`documents/data/`) 15 Kasım 2026'da birebir kopyalandı; biçimleri değiştirilmedi.

```
data/
├── catalog/   hesap kuralları ve katalog (projenin kendi tabloları)
└── raw/       dışarıdan gelen, değiştirilmeyen veri (kaynak başına bir klasör)
```

## Gizlilik sınıfları

| Sınıf | Anlamı |
|---|---|
| **Hassas** | YapıRadar verisi. Yalnız model eğitiminde kullanılır; arayüzde, API yanıtında, sunumda gösterilmez, repoya girmez. |
| **Lisanslı** | Kaynağın kullanım koşulu var (ÇŞB listeleri). Repoya girmez. |
| **Açık** | Kamuya açık ya da projenin kendi tablosu. Yine de bu klasörde tutulur, repoya girmez. |

## catalog/

| Dosya | Amaç | Sınıf |
|---|---|---|
| `kalemler.csv` | 61 maliyet kalemi: ana başlık, birim, miktar formülü, eklenme koşulu, kaynak, güven, aralık, kalite tanımı | Açık |
| `parametreler.csv` | Formüllerin ve mevzuat eşiklerinin sayıları (kaynak ve madde numarasıyla) | Açık |
| `fiyat_modeli.csv` | Kalem × kalite birim fiyatı (tez + TÜİK endeksi, piyasa, ödenek) | Açık |
| `fiyat_modeli_A.csv`, `fiyat_modeli_B.csv` | Fiyat modelinin iki eski çalışma sürümü (belgelenmemiş; yeni serviste kullanılmadan önce incelenmeli) | Açık |
| `kalem_poz.csv` | Kalem → ÇŞB poz numarası eşlemesi | Açık |
| `kalem_akademik_esleme.csv` | Kalem → akademik kaynak eşlemesi | Açık |
| `alternatif_kurallari.csv` | Dokuz plan alternatifi (A–I): daire modülü ve katta daire sayısı | Açık |
| `oda_dizilim_kurallari.csv` | Oda dizilim kuralları D01–D10 (plan denetimi) | Açık |
| `cizim_sozluk.csv` | DXF okuyucunun katman ve mahal adı sözlüğü | Açık |
| `README.md`, `README_kalem_poz.md` | Katalog açıklamaları | Açık |

## raw/

| Klasör / dosya | Amaç | Sınıf |
|---|---|---|
| `yapiradar/projeler.csv` | Proje kayıtları (2.100): konum, alan, kat, daire, blok, başlangıç ve bitiş; süre ve tamamlama modellerinin eğitim verisi | **Hassas** |
| `yapiradar/ozellikler.csv` | Proje başına özellikler (havuz, otopark …); tamamlama ve kalem önerisi | **Hassas** |
| `yapiradar/talepler.csv` | Malzeme talepleri; kalem oranlarının (talep / alan) eğitim verisi | **Hassas** |
| `csb-prices/csb_2026_10.csv` | ÇŞB 2026 Ekim birim fiyat ve rayiç listelerinden ayrıştırılmış pozlar | Lisanslı |
| `csb-prices/csb_fiyat_listesi.csv` | Kalemlere eşlenmiş ÇŞB fiyat listesi | Lisanslı |
| `tuik/tuik-ime-aylik.csv` | TÜİK İnşaat Maliyet Endeksi, aylık 2015-01 → 2026-07; fiyatları tarihe taşıma | Açık |
| `tcmb/usd_try.csv` | TCMB USD/TL kuru; USD çıktısı | Açık |
| `geo/ilceler.csv` | İlçe → il listesi (Harita Genel Müdürlüğü); konum ayrıştırma | Açık |
| `literature/turkel2016_binalar.csv` | Tezden 65 binanın metraj ve maliyet tablosu; beton ve demir eğimi | Açık |
| `literature/mahal2026_oda_tablolari.csv` | Örnek konut planlarının oda alanları; plan ölçüleri | Açık |
| `market/piyasa_tarama_2026_10.csv` | Kamuya açık piyasa fiyatı gözlemleri (ana tarama) | Açık |
| `market/piyasa2026_kaynak_sicili.csv` | Piyasa gözlemlerinin kaynak siteleri | Açık |
| `market/ek_tur/piyasa_ek_gozlem_1–7.csv` | Ek piyasa turları (7 numaralı dosya yalnız başlık satırı, boş şablon) | Açık |

## Kopyalanmayanlar (yerelde, `documents/data/`)

| Ne | Neden |
|---|---|
| `input/swiss-dwellings/` (1,9 GB) | Çizim okuyucu ve plan denetimi için; büyük. Gerekirse buraya `raw/swiss-dwellings/` olarak kopyalanır (CC BY 4.0, Archilyse AG). |
| `input/csb-prices/csb_2026_10_pdf/` (91 MB) | ÇŞB'nin özgün PDF'leri; CSV'ler bunlardan ayrıştırıldı. |
| `output/` (türetilmiş dosyalar, sentetik veri, çizim setleri, TKGM önbelleği) | Betik çıktıları; yeni serviste yeniden üretilir. `output/synthetic/projeler_sentetik.csv` YapıRadar satırlarından türetildiği için hassas sayılır. |

## Bilinen biçim sorunları (yeni serviste yükleyici çözer)

- Ayraç çoğunlukla `;`, ama `tuik-ime-aylik.csv` `,`.
- `talepler.csv` UTF-8 BOM'lu; satır sonları CRLF ve LF karışık.
- Tırnaksız `;` yüzünden fazla sütun: `cizim_sozluk.csv` (6 satır), `alternatif_kurallari.csv` (5 satır), `piyasa_ek_gozlem_3.csv` (4 satır).
- Birim yazımları tutarsız (`m2` / `m²`, `adet` / `Ad`).
