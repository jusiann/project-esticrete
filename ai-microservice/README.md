# ai-microservice

Yapay zekâ servisi (Python, FastAPI). Sıfırdan yazılır; `server` (ASP.NET Core API) bu servisi HTTP üzerinden çağırır, sözleşme OpenAPI ile tanımlanır. Arayüz bu servise doğrudan bağlanmaz.

Kapsam:

- **NLP:** serbest metinden proje bilgisini çıkarma (il, kat, daire, alan, kalite …)
- **Tamamlama:** yazılmayan girdilerin (kat, daire, arsa, blok) tahmini
- **Süre:** bitiş süresi tahmini ve belirsizlik aralığı
- **Çizim:** DXF kat planı okuma ve kural tabanlı plan alternatifi üretme

## Klasörler

```
ai-microservice/
├── src/esticrete_ai/
│   ├── settings.py     yollar (ESTICRETE_DATA_DIR ile değiştirilebilir)
│   └── data/           şema ve yükleyici: ham CSV'yi okuyup temiz, tipli tabloya çevirir
├── tests/              pytest; uydurma CSV ile birim testleri, yerel veri varsa gerçek veri testleri
├── data/               eğitim ve çalışma verisi (repoya girmez; liste: data/README.md)
├── models/             eğitilmiş modeller (repoya girmez; liste: models/README.md)
└── pyproject.toml
```

## Çalıştırma

```bash
cd ai-microservice
uv sync                 # sanal ortam ve bağımlılıklar
uv run pytest           # testler (yerel veri yoksa gerçek veri testleri atlanır)
uv run ruff check .     # kod denetimi
```

Model eğitimi ve API (FastAPI) adım adım eklenecek.

## Veri kuralı

`data/` ve `models/` içindeki hiçbir dosya repoya girmez; yalnız iki README izlenir. Özel veri (YapıRadar) yalnız model eğitiminde kullanılır, arayüzde ya da API yanıtında gösterilmez.
