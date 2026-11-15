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
├── data/       eğitim ve çalışma verisi (repoya girmez; liste: data/README.md)
├── models/     eğitilmiş modeller (repoya girmez; liste: models/README.md)
└── .gitignore
```

Kaynak kod, eğitim ve test klasörleri bahar 2027'de açılır.

## Veri kuralı

`data/` ve `models/` içindeki hiçbir dosya repoya girmez; yalnız iki README izlenir. Özel veri (YapıRadar) yalnız model eğitiminde kullanılır, arayüzde ya da API yanıtında gösterilmez.
