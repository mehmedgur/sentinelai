# sentinelai  {HALA DÜZENLEMELER, DEĞİŞİKLİKLER DEVAM EDİYOR}

sentinelai/
│
├── sentinelai_local.py       → Lokal kullanıcı için giriş noktası
├── sentinelai_server.py      → Sunucu kullanım giriş noktası
│
├── sentinelai/
│   ├── __init__.py
│   ├── menu.py               → İnteraktif menü motoru (ortak)
│   ├── onboarding.py         → İlk çalıştırma, ön bilgilendirme, API key kayıt
│   ├── analyzer.py           → Blue Team (12 analiz)
│   ├── scanner.py            → Red Team (10 tarama)
│   ├── lynis_module.py       → Lynis denetimi (ayrı modül)
│   ├── risk_engine.py        → Risk puanlama
│   ├── ai_module.py          → Claude API entegrasyonu **(Belli Değil)
│   ├── report.py             → Markdown + JSON rapor
│   └── utils.py              → Yardımcılar, renkler
│
├── config/
│   └── sentinelai.conf       → API key, kullanıcı tercihleri
│
├── setup.py
└── README.md

python sentinelai_local.py
        ↓
onboarding.py → ön bilgilendirme + API key
        ↓
menu.py → lokal menü (localhost sabit)
        ↓
ilgili modül çalışır, kullanıcı sadece onay verir

python sentinelai_server.py
        ↓
onboarding.py → ön bilgilendirme + API key + hedef IP sor
        ↓
menu.py → sunucu menüsü (hedef IP ile)
        ↓
ilgili modül çalışır, kullanıcı sadece onay verir

```text
🔵 Blue Team Modülü (11 Analiz)

1. SSH Güvenlik Analizi
   → SSH yapılandırması
   → Root login kontrolü
   → Zayıf ayar tespiti

2. Güvenlik Duvarı Analizi
   → UFW kontrolü
   → iptables kuralları
   → Açık port denetimi

3. Ağ ve Bağlantı Analizi
   → ss ile aktif bağlantılar
   → Dinleyen servisler
   → Şüpheli bağlantılar

4. Aktif Servis Analizi
   → systemctl servis kontrolü
   → Gereksiz servis tespiti
   → Kritik servis durumu

5. Kullanıcı ve Yetki Analizi
   → who / last kontrolü
   → Şüpheli kullanıcılar
   → Başarısız giriş denemeleri
   → sudo yetkileri

6. Kritik Dosya İzin Analizi
   → passwd/shadow kontrolü
   → chmod izin denetimi
   → SUID/SGID dosyaları

7. Kernel ve Sistem Parametreleri
   → sysctl kontrolü
   → Kernel hardening analizi
   → IPv4/IPv6 güvenlik ayarları

8. Güvenlik Güncelleme Analizi
   → Güncel olmayan paketler
   → Kritik güvenlik yamaları
   → Paket yöneticisi kontrolü

9. Audit ve Log Analizi
   → journalctl incelemesi
   → Syslog analizi
   → Kritik hata kayıtları

10. Rootkit ve Zararlı İmza Kontrolü
    → Rootkit taraması
    → Şüpheli process kontrolü
    → pspy süreç izleme

11. Kablosuz Ağ Güvenliği
    → Wi-Fi adaptör analizi
    → Açık ağ kontrolü
    → Şifreleme türü denetimi
```

 scanner.py — Red Team Modülü (10 Tarama)

1. Port Taraması
   → nmap
   → masscan
   → ss
   → Açık port analizi

2. NSE Güvenlik Açığı Scriptleri
   → nmap NSE scriptleri
   → Bilinen zafiyet kontrolleri
   → Servis bazlı güvenlik testi

3. Servis Tespiti
   → nmap servis/version detection
   → Banner bilgisi
   → Çalışan servis analizi


4. Temel Ağ Erişim Testi
   → ping
   → curl
   → Hedef erişilebilirlik kontrolü

5. Güvenlik Açığı Simülasyonu
   → Kontrollü zafiyet senaryoları
   → Eğitim amaçlı saldırı testi
   → Risk üretimi

6. Nikto Web Sunucu Taraması
   → Web sunucu açıkları
   → Yanlış yapılandırma kontrolü
   → Eski sürüm tespiti

7. WAF Tespiti
   → wafw00f
   → Web Application Firewall kontrolü

8. Ağ Keşfi
    → arp-scan(Yerel ağ cihaz keşfi)





-----------

SentinelAI modülleri:
Ana dosyalar:

main.py — CLI giriş noktası, argparse, mod yönetimi
utils.py — ANSI renkler, tablo, komut çalıştırıcı, yardımcılar

Blue Team (analyzer.py) — 12 analiz:

SSH Analizi:
SSH Portu varsayılan olarak 22 portumu bu bir dezavantajdır bunu değiştirmesi önerilecek veya ssh anahtarı ile giriş seçeneği değerlendirilecek.
Güvenlik Duvarı (UFW/iptables)
UFW veya iptables kullanılıyormu kontrol edecek evetse + değilse - puan alacak
Aktif Servisler
Kullanıcı manuel olarak kontrol edilmesini istiyormu istemiyormu ona bakılacak gereksiz önbelleği tutan servislerin temizlenmesini istiyormu istemiyormu kullanıcıya sorulacak.
Kullanıcı Hesapları
aktif olarak kullanıcıdan yetkisi olan kullanıcı hesaplarını listeleyecek
Çekirdek Parametreleri
bu parametreleri belirle
Kritik Dosya İzinleri(ÇIKARILDI)
Güvenlik Güncellemeleri
Güncellemeler kontrol edilecek değilse güncellenmesi istenecek veya otomatik güncellenecek
Audit / Kritik Log Olayları
Log olaylarında özellikle belirli parametreler mesela wifi veya ethernet sağlıklı çalışıyormu apache veri tabanı veya birkaç kritik linux uygulamasının çalılıp çalışmadığı status ile kontrol edilecek
Syslog & Log Yönetimi
aktifmi değişmi değilse açılacak
Başarısız Giriş Denemeleri
son 25 başarısız giriş denemesi ekranda gösterilecek ve hangi ip hangi tarihden yapıldığı gösterilebilecek
Rootkit İmza Kontrolü
Kablosuz Ağ Güvenliği
Wifi şifrelimi yoksa halka açık wifimi kontrol edilecek

Red Team (scanner.py) — 4 tarama:

Port Taraması (nmap / ss fallback)
Servis Tespiti (systemctl)
Yerel Bağlantılar (tüm arayüze açık dinleyiciler)
Güvenlik Açığı Simülasyonu (Docker soket, SUID, cron, /etc/passwd)








--------------------------
*****
-------------****
*****
--------------
