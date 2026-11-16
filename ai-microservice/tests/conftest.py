"""Testler gerçek veri yerine küçük, uydurma bir CSV kullanır (gerçek veri repoya girmez)."""

from pathlib import Path

import pytest

HEADER = (
    "proje_id;bolge;il;ilce;kategori;kamu_ozel;asama;baslangic_yil;baslangic_ceyrek;bitis_yil;bitis_ceyrek;"
    "sure_ceyrek;arsa_m2;kapali_alan_m2;blok_sayisi;kat_sayisi;daire_sayisi;bedel_usd;ihale_no;kayit_tarihi"
)
ROWS = [
    "1;Marmara;İstanbul;Kadıköy;Konut;Özel;Tamamlandı;2019;1;2020;3;6;1200;8000;2;10;80;100;;2019-01-01",
    # konut + ticaret, kamu, arsa Türkçe virgüllü, kat yok
    "2;Ege;İzmir;Bornova;Konut,Cadde Dükkan;Kamu;Tamamlandı;2021;2;2023;2;8;1250,5;12000;3;;96;100;;",
    "3;Akdeniz;Antalya;Muratpaşa;Sanayi Tesisi;Özel;Tamamlandı;2020;1;2021;1;4;5000;3000;1;1;;100;;",
    # arsa sıfır → bilinmiyor
    "4;İç Anadolu;Ankara;Çankaya;Konut;Özel;Tamamlandı;2022;4;2024;4;8;0;6000;1;8;40;100;;",
    # süre bitiş − başlangıç ile tutmuyor → atılır
    "5;Karadeniz;Trabzon;Ortahisar;Konut;Özel;Tamamlandı;2018;1;2019;1;9;900;4000;1;6;24;100;;",
    # kapalı alan boş (zorunlu) → atılır
    "6;Marmara;Bursa;Nilüfer;Konut;Özel;Tamamlandı;2017;3;2019;3;8;;;1;5;20;100;;",
]


def write_csv(path: Path, header: str = HEADER, rows: list[str] = ROWS) -> Path:
    # gerçek dosyalardaki gibi BOM ve CRLF
    path.write_bytes(("﻿" + "\r\n".join([header, *rows]) + "\r\n").encode("utf-8"))
    return path


@pytest.fixture
def projects_csv(tmp_path: Path) -> Path:
    return write_csv(tmp_path / "projeler.csv")
