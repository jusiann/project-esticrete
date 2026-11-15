# Esticrete

**Esticrete** (*estimate* + *concrete*): yapay zekâ destekli inşaat maliyet ve süre tahmin sistemi. BLG403 Uygulama Projesi (bitirme projesi), Güz 2026-2027.

Konut projeleri için serbest metinden proje bilgisini çıkarır, eksik girdileri tamamlar, kalem bazında yaklaşık doğrudan maliyet ve bitiş süresini belirsizlik aralığıyla hesaplar; DXF kat planı okuyup plan alternatifi üretir.

## Mimari

```
client (React) ──► server (ASP.NET Core API, C#) ──► ai-microservice (Python, FastAPI)
                          │
                          ▼
                      PostgreSQL
```

| Klasör | İçerik |
|---|---|
| `server/` | Asıl back-end: kullanıcı ve proje yönetimi, veritabanı, miktar motoru, fiyat ve maliyet |
| `client/` | Web arayüzü |
| `ai-microservice/` | NLP, tamamlama, süre ve çizim servisleri |

## Durum

Güz 2026: analiz ve tasarım (vize 6 Kasım, final 27 Aralık). Bahar 2027: kodlama ve test.

## Veri

Model eğitiminde kullanılan özel veri ve türetilmiş dosyalar repoda yoktur.
