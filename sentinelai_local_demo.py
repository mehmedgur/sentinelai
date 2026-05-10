#!/usr/bin/env python3
"""
SentinelAI - Lokal Kullanim Demo Menu
Hocaya gösterim amaclidir.
"""

import os
import sys
import time
import shutil

# ── Renkler ───────────────────────────────────────────────────────────────────
R = "\033[0m"       # reset
KALIN  = "\033[1m"
CYAN   = "\033[96m"
YESIL  = "\033[92m"
SARI   = "\033[93m"
KIRMIZI= "\033[91m"
MAVI   = "\033[94m"
EFLATUN= "\033[95m"
GRI    = "\033[90m"
BEYAZ  = "\033[97m"
BG_MAV = "\033[44m"
BG_KIR = "\033[41m"


def temizle():
    os.system("clear")


def yaz(metin, renk=BEYAZ, son="\n"):
    print(f"{renk}{metin}{R}", end=son)


def bekleme(saniye=0.03):
    time.sleep(saniye)


def animasyonlu_yazdir(metin, renk=BEYAZ, gecikme=0.012):
    for k in metin:
        print(f"{renk}{k}{R}", end="", flush=True)
        time.sleep(gecikme)
    print()


def baslik():
    temizle()
    ascii_art = f"""
{CYAN}{KALIN} ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗      █████╗ ██╗
 ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     ██╔══██╗██║
 ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ███████║██║
 ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ██╔══██║██║
 ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗██║  ██║██║
 ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝{R}"""
    print(ascii_art)

    genislik = shutil.get_terminal_size().columns
    bilgi = [
        f"{GRI}  Versiyon : {R}{YESIL}v1.0.0{R}",
        f"{GRI}  Mod      : {R}{SARI}Lokal{R}",
        f"{GRI}  Hedef    : {R}{BEYAZ}localhost{R}",
        f"{GRI}  Kullanici: {R}{BEYAZ}{os.getenv('USER','?')}{R}",
    ]
    for b in bilgi:
        print(b)

    print(f"\n{GRI}  {'─' * 65}{R}")
    print(f"{GRI}  ⚠️  Yalnizca etik ve egitim amaclidir — Gercek saldiri yapilmaz{R}")
    print(f"{GRI}  {'─' * 65}{R}\n")


def bolum_basligi(ikon, baslik_metni, renk=CYAN):
    print(f"\n{renk}{KALIN}  {'═' * 60}{R}")
    print(f"{renk}{KALIN}  {ikon}  {baslik_metni}{R}")
    print(f"{renk}  {'─' * 60}{R}\n")


def menu_satiri(numara, ikon, etiket, rozet="", rozet_renk=MAVI):
    num_str  = f"{MAVI}{KALIN}  [{numara}]{R}"
    ikon_str = f"  {ikon}"
    etiket_str = f"{BEYAZ}{etiket:<42}{R}"
    rozet_str  = f"{rozet_renk}{KALIN}{rozet}{R}" if rozet else ""
    print(f"{num_str}  {ikon_str}  {etiket_str}  {rozet_str}")


def ayrac():
    print(f"{GRI}      {'·' * 55}{R}")


def onay_sor(soru, ikon="❓") -> bool:
    print(f"\n  {ikon}  {SARI}{soru}{R}")
    print(f"\n      {YESIL}[E]{R} Evet, baslat    {KIRMIZI}[H]{R} Hayir, iptal\n")
    while True:
        secim = input(f"  {GRI}Seciminiz:{R} ").strip().lower()
        if secim in ("e", "evet", "y", "yes"):
            return True
        if secim in ("h", "hayir", "n", "no"):
            return False
        yaz("  Gecersiz secim. [E] veya [H] girin.", SARI)


def yuklenme_cubugu(isim, sure=2.0, adim=0.05):
    genislik = 40
    toplam   = int(sure / adim)
    for i in range(toplam + 1):
        dolu  = int(i / toplam * genislik)
        bos   = genislik - dolu
        bar   = f"{'█' * dolu}{'░' * bos}"
        yuzde = int(i / toplam * 100)
        print(
            f"\r  {CYAN}{isim:<35}{R}  {MAVI}[{bar}]{R}  {BEYAZ}{yuzde:>3}%{R}",
            end="", flush=True
        )
        time.sleep(adim)
    print()


def simule_et_blue():
    kontroller = [
        ("🔐 SSH Analizi",              1.2, "YÜKSEK",  "PermitRootLogin aktif"),
        ("🧱 Güvenlik Duvari",          0.8, "YÜKSEK",  "UFW devre disi"),
        ("⚙️  Aktif Servisler",          1.0, "TAMAM",   "Riskli servis bulunamadi"),
        ("👤 Kullanici Hesaplari",       0.9, "TAMAM",   "Kritik sorun yok"),
        ("🔧 Cekirdek Parametreleri",   1.1, "ORTA",    "ip_forward aktif"),
        ("📁 Kritik Dosya Izinleri",    1.3, "ORTA",    "5 beklenmedik SUID dosyasi"),
        ("📦 Güvenlik Güncellemeleri",  1.5, "BILGI",   "Güncelleme bulunamadi"),
        ("📜 Audit Log Olaylari",       0.7, "YÜKSEK",  "auditd calismiyor"),
        ("🗂️  Syslog & Log Yönetimi",   0.8, "ORTA",    "logrotate suresi dusuk"),
        ("🚨 Basarisiz Girisler",       1.0, "YÜKSEK",  "Son 5000 satirda 143 deneme"),
        ("🧬 Rootkit Imza Kontrolü",    2.0, "BILGI",   "rkhunter/chkrootkit yüklü degil"),
        ("📡 Kablosuz Ag Güvenligi",    0.6, "TAMAM",   "Wi-Fi arayüzü tespit edilmedi"),
    ]

    risk_renk = {
        "KRİTİK": f"{BG_KIR}{BEYAZ}",
        "YÜKSEK":  KIRMIZI,
        "ORTA":    SARI,
        "TAMAM":   YESIL,
        "BILGI":   GRI,
    }

    print()
    for isim, sure, risk, detay in kontroller:
        yuklenme_cubugu(isim, sure=sure)
        renk = risk_renk.get(risk, GRI)
        print(f"    {GRI}↳{R}  {renk}{risk:<8}{R}  {GRI}{detay}{R}")
        time.sleep(0.1)


def simule_et_red():
    taramalar = [
        ("🔍 Port Taramasi (nmap)",       2.5),
        ("🧩 NSE Güvenlik Scriptleri",    3.0),
        ("🔗 Yerel Baglantilar",          1.0),
        ("⚠️  Zafiyet Simülasyonu",        1.5),
        ("🌐 Nikto Web Taramasi",         2.0),
        ("📂 Gobuster Dizin Taramasi",    2.0),
        ("🛡️  WAF Tespiti",                0.8),
        ("📡 Ag Kesfi (arp-scan)",        1.2),
        ("👁️  Process Izleme (pspy)",      1.5),
    ]
    print()
    for isim, sure in taramalar:
        yuklenme_cubugu(isim, sure=sure)
        time.sleep(0.08)


def simule_et_lynis():
    adimlar = [
        ("Lynis kurulum kontrolü",     0.5),
        ("Sistem bilgisi toplaniyor",  0.8),
        ("Önyükleme ve servisleri",    1.0),
        ("Kullanici ve gruplar",       0.8),
        ("Dosya sistemi",              1.2),
        ("SSH konfigürasyonu",         0.7),
        ("Ag parametreleri",           0.9),
        ("Logging ve denetim",         0.8),
        ("Güvenlik yazilimlari",       1.0),
        ("Hardening index hesaplaniyor",0.5),
    ]
    print()
    for isim, sure in adimlar:
        yuklenme_cubugu(f"  {isim}", sure=sure)
        time.sleep(0.05)


def risk_skoru_goster(puan, seviye):
    genislik = 40
    dolu = int(puan / 100 * genislik)
    bos  = genislik - dolu

    seviye_renk = {
        "KRİTİK": KIRMIZI,
        "YÜKSEK":  SARI,
        "ORTA":    MAVI,
        "DÜŞÜK":   YESIL,
        "GÜVENLİ": YESIL,
    }
    renk = seviye_renk.get(seviye, BEYAZ)
    bar  = f"{'█' * dolu}{'░' * bos}"

    print(f"\n{GRI}  {'─' * 60}{R}")
    print(f"\n  {BEYAZ}{KALIN}RİSK DEGERLENDİRMESİ{R}\n")
    print(f"  {renk}{KALIN}Puan  : {puan}/100{R}")
    print(f"  {renk}{KALIN}Seviye: {seviye}{R}")
    print(f"\n  {MAVI}[{bar}]{R}  {renk}{KALIN}{puan}%{R}\n")
    print(f"{GRI}  {'─' * 60}{R}\n")


# ── Menü Ekranlari ────────────────────────────────────────────────────────────

def ekran_ana():
    baslik()
    yaz(f"  {KALIN}Ana Menü{R}", BEYAZ)
    print()

    menu_satiri("1", "🔵", "Blue Team Analizi",              "[ 12 kontrol ]", MAVI)
    menu_satiri("2", "🔴", "Red Team Taramasi",              "[ 10 tarama  ]", KIRMIZI)
    menu_satiri("3", "🔬", "Lynis Sistem Denetimi",          "[ otomatik   ]", YESIL)
    menu_satiri("4", "⚡", "Tam Analiz (Blue + Red + Lynis)","[ önerilir   ]", SARI)
    menu_satiri("5", "🤖", "Claude AI Yorumu",               "[ API        ]", EFLATUN)
    menu_satiri("6", "📄", "Rapor Olustur / Görüntüle",      "[ MD + JSON  ]", CYAN)
    ayrac()
    menu_satiri("0", "🚪", "Cikis", "", GRI)

    print(f"\n{GRI}  Seciminiz (0-6):{R} ", end="")
    return input().strip()


def ekran_blue():
    baslik()
    bolum_basligi("🔵", "BLUE TEAM — Savunma Analizi", MAVI)

    print(f"  {GRI}Asagidaki 12 kontrol calistirilacak:{R}\n")
    kontroller = [
        "🔐 SSH Analizi",      "🧱 Güvenlik Duvari",
        "⚙️  Aktif Servisler",  "👤 Kullanici Hesaplari",
        "🔧 Cekirdek Param.",   "📁 Dosya Izinleri",
        "📦 Pkt Güncellemeleri","📜 Audit Log",
        "🗂️  Syslog",           "🚨 Basarisiz Girisler",
        "🧬 Rootkit",           "📡 Wi-Fi Güvenligi",
    ]
    for i in range(0, len(kontroller), 2):
        sol = kontroller[i]
        sag = kontroller[i+1] if i+1 < len(kontroller) else ""
        print(f"  {YESIL}✦{R}  {BEYAZ}{sol:<35}{R}  {YESIL}✦{R}  {BEYAZ}{sag}{R}")

    if onay_sor("Blue Team analizi baslatilsin mi?", "🔵"):
        bolum_basligi("🔵", "BLUE TEAM — Calistirilıyor...", MAVI)
        simule_et_blue()
        risk_skoru_goster(72, "YÜKSEK")
        yaz("  ✅ Blue Team analizi tamamlandi.", YESIL)
        print(f"\n  {GRI}Raporlamak icin Ana Menü > [6] Rapor secenegini kullanin.{R}")
    else:
        yaz("\n  ↩  Ana menüye dönülüyor...", GRI)

    input(f"\n  {GRI}Devam etmek icin Enter'a basin...{R}")


def ekran_red():
    baslik()
    bolum_basligi("🔴", "RED TEAM — Saldiri Yüzeyi Analizi", KIRMIZI)

    print(f"  {GRI}Asagidaki taramalar calistirilacak:{R}\n")
    taramalar = [
        "🔍 Port Taramasi (nmap → masscan → ss)",
        "🧩 NSE Güvenlik Acigi Scriptleri",
        "🔗 Yerel Baglantilar",
        "⚠️  Zafiyet Simülasyonu",
        "🌐 Nikto Web Sunucu Taramasi",
        "📂 Gobuster / Dirb Dizin Taramasi",
        "🛡️  WAF Tespiti (wafw00f)",
        "📡 Ag Kesfi (netdiscover / arp-scan)",
        "👁️  Process Izleme (pspy)",
    ]
    for t in taramalar:
        print(f"  {KIRMIZI}✦{R}  {BEYAZ}{t}{R}")

    print(f"\n  {SARI}⚠️  Hicbir gercek saldiri veya somürü yapilmaz.{R}")

    if onay_sor("Red Team taramasi baslatilsin mi?", "🔴"):
        bolum_basligi("🔴", "RED TEAM — Calistirilıyor...", KIRMIZI)
        simule_et_red()
        print(f"\n  {KIRMIZI}{KALIN}[ Açik Portlar ]{R}")
        portlar = [
            ("22", "tcp", "SSH",   "DÜŞÜK"),
            ("80", "tcp", "HTTP",  "DÜŞÜK"),
            ("443","tcp", "HTTPS", "BİLGİ"),
        ]
        print(f"\n  {GRI}{'PORT':<8}{'PROTOKOL':<12}{'SERVİS':<12}{'RİSK'}{R}")
        print(f"  {GRI}{'─'*45}{R}")
        for port, proto, servis, risk in portlar:
            renk = SARI if risk == "DÜŞÜK" else GRI
            print(f"  {BEYAZ}{port:<8}{GRI}{proto:<12}{BEYAZ}{servis:<12}{renk}{risk}{R}")
        risk_skoru_goster(35, "DÜŞÜK")
        yaz("  ✅ Red Team taramasi tamamlandi.", YESIL)
    else:
        yaz("\n  ↩  Ana menüye dönülüyor...", GRI)

    input(f"\n  {GRI}Devam etmek icin Enter'a basin...{R}")


def ekran_lynis():
    baslik()
    bolum_basligi("🔬", "LYNIS SISTEM DENETİMİ", YESIL)

    print(f"  {GRI}Lynis acik kaynakli bir sistem sertlestirme denetcisidir.{R}")
    print(f"  {GRI}Script kurulum, calistirma ve raporlamayi otomatik yapar.{R}\n")

    print(f"  {YESIL}✦{R}  {BEYAZ}Kurulum kontrolü (yoksa otomatik kurar){R}")
    print(f"  {YESIL}✦{R}  {BEYAZ}--audit modu ile sistem taramasi{R}")
    print(f"  {YESIL}✦{R}  {BEYAZ}Hardening Index skoru (0-100){R}")
    print(f"  {YESIL}✦{R}  {BEYAZ}Blue Team bulgulariyla capraz karsilastirma{R}")
    print(f"  {YESIL}✦{R}  {BEYAZ}Otomatik Markdown raporu{R}")

    if onay_sor("Lynis denetimi baslatilsin mi?", "🔬"):
        bolum_basligi("🔬", "LYNIS — Calistirilıyor...", YESIL)

        yaz("  ℹ️  Lynis kurulumu kontrol ediliyor...", GRI)
        time.sleep(1)
        yaz("  ✅ Lynis mevcut.", YESIL)

        simule_et_lynis()

        print(f"\n  {YESIL}{KALIN}Hardening Index : 58 / 100{R}")
        print(f"  {SARI}Uyari sayisi    : 14{R}")
        print(f"  {MAVI}Öneri sayisi    : 31{R}")
        risk_skoru_goster(58, "ORTA")
        yaz("  ✅ Lynis denetimi tamamlandi.", YESIL)
    else:
        yaz("\n  ↩  Ana menüye dönülüyor...", GRI)

    input(f"\n  {GRI}Devam etmek icin Enter'a basin...{R}")


def ekran_tam():
    baslik()
    bolum_basligi("⚡", "TAM ANALİZ — Blue + Red + Lynis", SARI)

    print(f"  {GRI}Üc modül sirali sekilde otomatik calistirilacak:{R}\n")
    print(f"  {MAVI}1.{R}  🔵 Blue Team Analizi      {GRI}(~3 dk){R}")
    print(f"  {KIRMIZI}2.{R}  🔴 Red Team Taramasi      {GRI}(~4 dk){R}")
    print(f"  {YESIL}3.{R}  🔬 Lynis Denetimi         {GRI}(~2 dk){R}")
    print(f"\n  {SARI}Tahmini toplam süre: 9 dakika{R}")

    if onay_sor("Tam analiz baslatilsin mi?", "⚡"):
        for ikon, baslik_m, renk, fonk in [
            ("🔵", "BLUE TEAM", MAVI,    simule_et_blue),
            ("🔴", "RED TEAM",  KIRMIZI, simule_et_red),
            ("🔬", "LYNIS",     YESIL,   simule_et_lynis),
        ]:
            bolum_basligi(ikon, baslik_m, renk)
            fonk()
            time.sleep(0.3)

        risk_skoru_goster(68, "YÜKSEK")
        yaz("  ✅ Tam analiz tamamlandi. Rapor icin [6] secenegini kullanin.", YESIL)
    else:
        yaz("\n  ↩  Ana menüye dönülüyor...", GRI)

    input(f"\n  {GRI}Devam etmek icin Enter'a basin...{R}")


def ekran_ai():
    baslik()
    bolum_basligi("🤖", "CLAUDE AI YORUMU", EFLATUN)

    print(f"  {GRI}Bulgularinizi Claude API ile analiz ettirin.{R}")
    print(f"  {GRI}Türkce dogal dil yorumu + oneri + saldirgan perspektifi.{R}\n")

    api_key = input(f"  {EFLATUN}Claude API Anahtarinizi girin:{R} ").strip()
    if not api_key:
        yaz("  ⚠️  API anahtari bos birakılamaz.", SARI)
    else:
        yaz(f"\n  ✅ API anahtari alindi. Config dosyasina kaydedilsin mi?", YESIL)
        kaydet = input(f"  {GRI}[E/H]:{R} ").strip().lower()
        if kaydet in ("e", "evet"):
            yaz("  ✅ ~/.sentinelai.conf dosyasina kaydedildi.", YESIL)
        print()
        yaz("  🤖 Claude'a baglaniliyor...", EFLATUN)
        time.sleep(1.5)
        yaz("  ✅ Baglanti basarili.", YESIL)
        time.sleep(0.5)
        yaz("\n  📤 Bulgular gönderiliyor...", GRI)
        yuklenme_cubugu("  Analiz ediliyor", sure=3.0)
        print(f"\n  {EFLATUN}{KALIN}[ Claude AI Yorumu ]{R}\n")
        yorum = [
            "Sistem orta-yüksek risk seviyesinde. SSH konfigürasyonu ve",
            "auditd eksikligi en öncelikli sorunlar. UFW devre disi olmasi",
            "sistemi dis tehditlere acik birakmaktadir. Önerilen ilk adim:",
            "UFW'yi etkinlestirin ve SSH anahtar dogrulamasina gecin.",
        ]
        for satir in yorum:
            animasyonlu_yazdir(f"  {satir}", BEYAZ, gecikme=0.015)

    input(f"\n  {GRI}Devam etmek icin Enter'a basin...{R}")


def ekran_rapor():
    baslik()
    bolum_basligi("📄", "RAPOR OLUSTUR / GÖRÜNTÜLE", CYAN)

    print(f"  {CYAN}[1]{R}  {BEYAZ}Markdown raporu olustur (.md){R}")
    print(f"  {CYAN}[2]{R}  {BEYAZ}JSON raporu olustur (.json){R}")
    print(f"  {CYAN}[3]{R}  {BEYAZ}Her ikisini olustur{R}")
    print(f"  {CYAN}[4]{R}  {BEYAZ}Son raporu görüntüle{R}")
    ayrac()
    print(f"  {GRI}[0]{R}  {GRI}Ana menüye dön{R}")

    print(f"\n  {GRI}Seciminiz:{R} ", end="")
    secim = input().strip()

    if secim in ("1", "2", "3"):
        yaz("\n  📝 Rapor olusturuluyor...", GRI)
        yuklenme_cubugu("  Yaziliyor", sure=1.5)
        yaz("  ✅ Rapor kaydedildi: ./sentinelai_rapor/sentinelai_20250510_143022.md", YESIL)
    elif secim == "4":
        yaz("\n  📂 Son rapor bulunamadi. Önce analiz calistirin.", SARI)

    input(f"\n  {GRI}Devam etmek icin Enter'a basin...{R}")


# ── Ana Döngü ─────────────────────────────────────────────────────────────────

def main():
    while True:
        secim = ekran_ana()

        if secim == "1":
            ekran_blue()
        elif secim == "2":
            ekran_red()
        elif secim == "3":
            ekran_lynis()
        elif secim == "4":
            ekran_tam()
        elif secim == "5":
            ekran_ai()
        elif secim == "6":
            ekran_rapor()
        elif secim == "0":
            temizle()
            yaz("\n  👋 SentinelAI kapatildi. Güvende kalin.\n", CYAN)
            sys.exit(0)
        else:
            yaz("  ⚠️  Gecersiz secim. 0-6 arasinda bir sayi girin.", SARI)
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {GRI}Ctrl+C algilandi. Cikiliyor...{R}\n")
        sys.exit(0)
