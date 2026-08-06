# SentinelAI

> **Linux Sistemleri İçin Yapay Zekâ Destekli Genel Güvenlik Analiz Aracı**

SentinelAI, Linux sistemlerinin güvenlik durumunu analiz etmek amacıyla geliştirilmiş açık kaynak kodlu bir **Blue Team** ve **Red Team** güvenlik aracıdır.

Proje; sistem güvenlik analizleri, zafiyet taramaları, risk puanlama sistemi ve **Google Gemini API** destekli yapay zekâ önerilerini tek bir terminal uygulamasında bir araya getirir.
Bu proje 2025-2026 Dönemi Ankara Bilim Üniversitesi Bilişim Güvenliği Teknolojisi olan 3 öğrencinin emekleriyle bir araya getirilip dönem projesi olarak sunulmuştur
Emeği Geçenler: Kod Tarafı: Mehmed Gürbüz
Görünüm Düzenleme: C. O., Göksu U.
Sunum: Bektaş C. O., Göksu U.


---

# 🚀 Özellikler

## 🔵 Blue Team Analizleri

SentinelAI sisteminizi aşağıdaki başlıklarda analiz eder.

* 🔐 SSH Güvenlik Analizi
* 🔥 Güvenlik Duvarı (UFW / iptables)
* 🌐 Ağ ve Aktif Bağlantılar
* ⚙️ Çalışan Servis Analizi
* 👤 Kullanıcı ve Yetki Analizi
* 🧠 Kernel (sysctl) Güvenlik Kontrolleri
* 📦 Güvenlik Güncellemeleri
* 📜 Audit ve Journal Log Analizi
* ❌ Başarısız Giriş Denemeleri
* ☠️ Rootkit İmza Kontrolü
* 📶 Kablosuz Ağ Güvenliği

Toplam **11 farklı güvenlik analizi** gerçekleştirilmektedir.

---

## 🔴 Red Team Taramaları

Blue Team analizlerinin yanında temel saldırı yüzeyi keşfi için aşağıdaki taramalar yapılabilir.

* Nmap Port Taraması
* Servis Tespiti
* NSE Güvenlik Scriptleri
* Ağ Keşfi
* Nikto Web Sunucusu Analizi
* Gobuster Dizin Taraması
* Process İzleme (pspy)
* Yerel Servis Analizi
* Temel Zafiyet Simülasyonu

Toplam **9 farklı Red Team taraması** bulunmaktadır.

---

# 🤖 Yapay Zekâ Desteği

SentinelAI, **Google Gemini API** kullanarak elde edilen analiz sonuçlarını yorumlar.

Yapay zekâ;

* Bulunan güvenlik açıklarını açıklar.
* Risk seviyesini yorumlar.
* Güvenlik sertleştirme (Hardening) önerileri sunar.
* Sistem yöneticileri için anlaşılır raporlar oluşturur.

---

# 📊 Risk Puanlama Sistemi

Her analiz sonucunda sistemin güvenlik seviyesi puanlanır.

| Puan   | Durum       |
| ------ | ----------- |
| 90-100 | Çok Güvenli |
| 70-89  | Güvenli     |
| 50-69  | Orta Risk   |
| 30-49  | Yüksek Risk |
| 0-29   | Kritik      |

---

# 📑 Oluşturulan Raporlar

Analiz sonunda otomatik olarak;

* Markdown (.md)
* JSON (.json)

formatlarında rapor oluşturulur.

Raporda;

* Tespit edilen güvenlik açıkları
* Risk puanı
* Yapay zekâ önerileri
* Alınması gereken aksiyonlar

yer almaktadır.

---

# 📂 Proje Yapısı

```text
sentinelai/
│
├── sentinelai_local.py      # Lokal kullanım
├── sentinelai_server.py     # Sunucu kullanımı
├── setup.py
│
└── sentinelai/
    ├── __init__.py
    ├── menu.py
    ├── onboarding.py
    ├── analyzer.py
    ├── scanner.py
    ├── lynis_module.py
    ├── risk_engine.py
    ├── ai_module.py
    ├── report.py
    └── utils.py
```

---

# 🔍 Blue Team Analizleri

✅ SSH yapılandırması

✅ Root Login kontrolü

✅ SSH Port analizi

✅ Güvenlik Duvarı denetimi

✅ UFW / iptables kontrolü

✅ Aktif bağlantılar

✅ Dinleyen servisler

✅ Servis durumları

✅ Kullanıcı hesapları

✅ sudo yetkileri

✅ Başarısız giriş denemeleri

✅ Kernel Hardening

✅ sysctl güvenlik parametreleri

✅ Güvenlik güncellemeleri

✅ Audit Log analizi

✅ Journal Log analizi

✅ Rootkit imza kontrolü

✅ Kablosuz ağ güvenliği

---

# ⚔️ Red Team Taramaları

* Port Taraması
* Servis Tespiti
* Ağ Keşfi
* NSE Script Analizi
* Nikto Web Taraması
* Gobuster Dizin Taraması
* Process İzleme (pspy)
* Yerel Ağ Analizi
* Temel Zafiyet Simülasyonu

---

# 🛠️ Kullanılan Teknolojiler

* Python 3
* Nmap
* UFW
* iptables
* systemctl
* journalctl
* ss
* Lynis
* Google Gemini API

---

# 🎯 Yol Haritası

* [x] Blue Team Analizleri
* [x] Red Team Taramaları
* [x] Risk Puanlama Sistemi
* [x] AI Destekli Güvenlik Önerileri
* [x] Markdown ve JSON Raporlama
* [ ] Bu özellik v1.5 sürümünde geliştirilmiştir.
* [ ] Bu özellik v1.5 sürümünde geliştirilmiştir.
* [ ] Bu özellik v1.5 sürümünde geliştirilmiştir.
* [ ] Bu özellik v1.5 sürümünde geliştirilmiştir.
* [ ] Bu özellik v1.5 sürümünde geliştirilmiştir.

---

# 🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyorum.

Yeni özellik ekleyebilir, hata bildirebilir veya Pull Request göndererek projeye katkıda bulunabilirsiniz.

---

# 📜 Lisans

Bu proje **MIT License** ile lisanslanacaktır.

---

# 👨‍💻 Geliştirici


3 Bilişim Güvenliği öğrencisi Dönem Projesi olarak yaptı.

⭐ Projeyi beğendiyseniz geri donut ve yıldız vermeyi unutmayın.
