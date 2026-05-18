"""
SentinelAI v1.2 - Blue Team Analiz Modülü
"""

import re
import os
from dataclasses import dataclass, field
from .utils import komut, dosya_oku, root_mu, yaz, risk_rengi, R


@dataclass
class Bulgu:
    kategori: str
    baslik:   str
    detay:    str
    risk:     str
    oneri:    str = ""
    puan:     int = 0


@dataclass
class Sonuc:
    ad:      str
    bulgular: list = field(default_factory=list)
    ozet:    str = ""


class BlueTeam:
    """
    Blue Team — 11 savunma analizi.
    Yazar: BGT
    """

    def __init__(self, sessiz=False):
        self.sessiz = sessiz
        self._root  = root_mu()

    def calistir(self):
        analizler = [
            ("ssh",       "🔐 SSH",                    self._ssh),
            ("ufw",       "🧱 Güvenlik Duvarı (UFW)",  self._ufw),
            ("servis",    "⚙️  Aktif Servisler",         self._servis),
            ("kullanici", "👤 Kullanıcı Hesapları",     self._kullanici),
            ("cekirdek",  "🔧 Çekirdek Parametreleri",  self._cekirdek),
            ("dosya",     "📁 Dosya İzinleri",          self._dosya),
            ("paket",     "📦 Güvenlik Güncellemeleri", self._paket),
            ("audit",     "📜 Audit Log",               self._audit),
            ("syslog",    "🗂️  Syslog",                  self._syslog),
            ("giris",     "🚨 Başarısız Girişler",      self._giris),
            ("rootkit",   "🧬 Rootkit Kontrolü",        self._rootkit),
            ("wifi",      "📡 Kablosuz Ağ",             self._wifi),
        ]
        sonuclar = {}
        for anahtar, isim, fonk in analizler:
            if not self.sessiz:
                yaz(f"  ↳ {isim} kontrol ediliyor...", R.GRI)
            s = fonk()
            s.ad = isim
            sonuclar[anahtar] = s
        return sonuclar

    # ── SSH: yalnızca port 22 kontrolü ───────────────────────────────────────
    def _ssh(self):
        s = Sonuc(ad="SSH")
        icerik = dosya_oku("/etc/ssh/sshd_config")
        if icerik is None:
            s.ozet = "SSH yapılandırma dosyası bulunamadı."
            return s

        port_esles = re.search(r"^\s*Port\s+(\d+)", icerik, re.MULTILINE)
        port = int(port_esles.group(1)) if port_esles else 22

        if port == 22:
            s.bulgular.append(Bulgu(
                kategori="SSH",
                baslik="SSH varsayılan port 22 kullanıyor",
                detay="Otomatik tarayıcılar önce 22. portu hedef alır.",
                risk="DÜŞÜK",
                oneri="SSH portunu 1024+ arası standart dışı bir porta taşıyın.",
                puan=5,
            ))
        else:
            s.ozet = f"SSH port {port} — varsayılan değil, iyi."
        return s

    # ── UFW: yalnızca aktif/pasif ─────────────────────────────────────────────
    def _ufw(self):
        s = Sonuc(ad="UFW")
        ok, cikti = komut("ufw status 2>/dev/null")
        if not ok or not cikti:
            s.bulgular.append(Bulgu(
                kategori="UFW",
                baslik="UFW durumu alınamadı",
                detay="ufw komutu çalışmıyor veya yüklü değil.",
                risk="YÜKSEK",
                oneri="'sudo apt install ufw && sudo ufw enable' komutunu çalıştırın.",
                puan=30,
            ))
            return s

        if "inactive" in cikti.lower():
            s.bulgular.append(Bulgu(
                kategori="UFW",
                baslik="UFW güvenlik duvarı devre dışı",
                detay="Sistem gelen bağlantılara karşı korumasız.",
                risk="YÜKSEK",
                oneri="'sudo ufw enable' ile UFW'yi etkinleştirin.",
                puan=30,
            ))
        else:
            s.ozet = "UFW aktif."
        return s

    # ── Servisler ─────────────────────────────────────────────────────────────
    def _servis(self):
        s = Sonuc(ad="Servisler")
        _, cikti = komut(
            "systemctl list-units --type=service --state=running "
            "--no-pager --no-legend 2>/dev/null"
        )
        riskli = {
            "telnet": ("Telnet şifresiz protokol aktif",   "YÜKSEK", 25,
                       "sudo systemctl disable telnet --now"),
            "ftp":    ("FTP servisi çalışıyor",            "ORTA",   15,
                       "SFTP kullanın."),
            "rsh":    ("RSH uzak kabuk servisi aktif",     "KRİTİK", 35,
                       "sudo apt remove rsh-server"),
            "nfs":    ("NFS servisi aktif",                "ORTA",   15,
                       "Gereksizse NFS'yi kapatın."),
            "redis":  ("Redis servisi çalışıyor",          "ORTA",   15,
                       "Redis'e yalnızca yerel erişime izin verin."),
            "mongodb":("MongoDB servisi çalışıyor",        "ORTA",   15,
                       "Kimlik doğrulamayı etkinleştirin."),
        }
        c = cikti.lower()
        for ad, (baslik, risk, puan, oneri) in riskli.items():
            if ad in c:
                s.bulgular.append(Bulgu(
                    kategori="Servisler", baslik=baslik,
                    detay=f"'{ad}' servisi tespit edildi.",
                    risk=risk, oneri=oneri, puan=puan,
                ))
        if not s.bulgular:
            s.ozet = "Bilinen riskli servis tespit edilmedi."
        return s

    # ── Kullanıcılar ──────────────────────────────────────────────────────────
    def _kullanici(self):
        s = Sonuc(ad="Kullanıcılar")
        # NOPASSWD sudo
        sudoers = dosya_oku("/etc/sudoers")
        if sudoers:
            for satir in sudoers.splitlines():
                if "NOPASSWD" in satir and not satir.strip().startswith("#"):
                    s.bulgular.append(Bulgu(
                        kategori="Kullanıcılar",
                        baslik="NOPASSWD sudo kuralı mevcut",
                        detay=satir.strip(),
                        risk="YÜKSEK",
                        oneri="NOPASSWD kurallarını sudoers'dan kaldırın.",
                        puan=25,
                    ))
        # UID 0 olmayan root hesaplar
        passwd = dosya_oku("/etc/passwd")
        if passwd:
            for satir in passwd.splitlines():
                p = satir.split(":")
                if len(p) >= 4 and p[2] == "0" and p[0] != "root":
                    s.bulgular.append(Bulgu(
                        kategori="Kullanıcılar",
                        baslik=f"UID 0 yetkili hesap: {p[0]}",
                        detay="Root dışı hesap UID 0 ile tanımlanmış.",
                        risk="KRİTİK",
                        oneri=f"'{p[0]}' hesabının UID'sini değiştirin.",
                        puan=45,
                    ))
        if not s.bulgular:
            s.ozet = "Kritik kullanıcı sorunu tespit edilmedi."
        return s

    # ── Çekirdek ──────────────────────────────────────────────────────────────
    def _cekirdek(self):
        s = Sonuc(ad="Çekirdek")
        kontroller = [
            ("net.ipv4.ip_forward",               "1", "ORTA",   10,
             "sysctl -w net.ipv4.ip_forward=0"),
            ("net.ipv4.conf.all.accept_redirects", "1", "ORTA",   10,
             "sysctl -w net.ipv4.conf.all.accept_redirects=0"),
            ("kernel.randomize_va_space",          "0", "YÜKSEK", 20,
             "sysctl -w kernel.randomize_va_space=2"),
        ]
        for param, tehlikeli, risk, puan, oneri in kontroller:
            ok, cikti = komut(f"sysctl {param} 2>/dev/null")
            if ok and "=" in cikti:
                deger = cikti.split("=")[-1].strip()
                if deger == tehlikeli:
                    s.bulgular.append(Bulgu(
                        kategori="Çekirdek",
                        baslik=f"Riskli parametre: {param}={deger}",
                        detay="Bu değer sistem güvenliğini zayıflatıyor.",
                        risk=risk, oneri=oneri, puan=puan,
                    ))
        if not s.bulgular:
            s.ozet = "Çekirdek parametreleri makul."
        return s

    # ── Dosya İzinleri (SUID kaldırıldı) ─────────────────────────────────────
    def _dosya(self):
        s = Sonuc(ad="Dosya İzinleri")
        hedefler = {
            "/etc/passwd":  "644",
            "/etc/shadow":  "640",
            "/etc/sudoers": "440",
        }
        for dosya, beklenen in hedefler.items():
            if not os.path.exists(dosya):
                continue
            ok, cikti = komut(f"stat -c '%a' {dosya} 2>/dev/null")
            if ok and cikti.strip() != beklenen:
                s.bulgular.append(Bulgu(
                    kategori="Dosya",
                    baslik=f"{dosya} izni hatalı",
                    detay=f"Mevcut: {cikti.strip()}, Beklenen: {beklenen}",
                    risk="ORTA",
                    oneri=f"chmod {beklenen} {dosya}",
                    puan=10,
                ))
        if not s.bulgular:
            s.ozet = "Kritik dosya izinleri uygun."
        return s

    # ── Güvenlik Güncellemeleri ───────────────────────────────────────────────
    def _paket(self):
        s = Sonuc(ad="Güncellemeler")
        ok, cikti = komut(
            "apt list --upgradable 2>/dev/null | grep -i security | wc -l"
        )
        if ok:
            try:
                sayi = int(cikti.strip())
            except ValueError:
                sayi = 0
            if sayi > 0:
                risk = "KRİTİK" if sayi > 10 else "YÜKSEK" if sayi > 5 else "ORTA"
                s.bulgular.append(Bulgu(
                    kategori="Güncellemeler",
                    baslik=f"{sayi} güvenlik güncellemesi bekliyor",
                    detay="Yüklenmemiş güvenlik yamaları.",
                    risk=risk,
                    oneri="sudo apt upgrade -y",
                    puan=min(sayi * 3, 30),
                ))
            else:
                s.ozet = "Bekleyen güvenlik güncellemesi yok."
        return s

    # ── Audit ─────────────────────────────────────────────────────────────────
    def _audit(self):
        s = Sonuc(ad="Audit")
        ok, cikti = komut("systemctl is-active auditd 2>/dev/null")
        if not ok or cikti.strip() != "active":
            s.bulgular.append(Bulgu(
                kategori="Audit",
                baslik="auditd çalışmıyor",
                detay="Kritik sistem olayları loglanmıyor.",
                risk="YÜKSEK",
                oneri="sudo apt install auditd && sudo systemctl enable auditd --now",
                puan=20,
            ))
        else:
            # Kritik kural kontrolü
            ok2, kurallar = komut("auditctl -l 2>/dev/null")
            if ok2 and "-w /etc/passwd" not in kurallar:
                s.bulgular.append(Bulgu(
                    kategori="Audit",
                    baslik="Kritik dosya izleme kuralı eksik",
                    detay="/etc/passwd değişiklikleri izlenmiyor.",
                    risk="ORTA",
                    oneri="auditctl -w /etc/passwd -p wa -k passwd_degisiklik",
                    puan=10,
                ))
        if not s.bulgular:
            s.ozet = "auditd aktif ve kurallar yapılandırılmış."
        return s

    # ── Syslog ────────────────────────────────────────────────────────────────
    def _syslog(self):
        s = Sonuc(ad="Syslog")
        # rsyslog aktif mi?
        ok, cikti = komut("systemctl is-active rsyslog 2>/dev/null")
        if not ok or cikti.strip() != "active":
            s.bulgular.append(Bulgu(
                kategori="Syslog",
                baslik="rsyslog çalışmıyor",
                detay="Sistem logları toplanmıyor olabilir.",
                risk="YÜKSEK",
                oneri="sudo systemctl enable rsyslog --now",
                puan=20,
            ))
        # auth.log var mı?
        if not os.path.exists("/var/log/auth.log"):
            s.bulgular.append(Bulgu(
                kategori="Syslog",
                baslik="/var/log/auth.log bulunamadı",
                detay="Kimlik doğrulama logları eksik.",
                risk="ORTA",
                oneri="rsyslog yapılandırmasını kontrol edin.",
                puan=10,
            ))
        if not s.bulgular:
            s.ozet = "rsyslog aktif, log dosyaları mevcut."
        return s

    # ── Başarısız Girişler ────────────────────────────────────────────────────
    def _giris(self):
        s = Sonuc(ad="Başarısız Girişler")
        ok, cikti = komut(
            "grep 'Failed password' /var/log/auth.log 2>/dev/null | wc -l"
        )
        if not ok:
            ok, cikti = komut(
                "journalctl -n 5000 2>/dev/null | grep 'Failed password' | wc -l"
            )
        try:
            sayi = int(cikti.strip())
        except Exception:
            sayi = 0

        if sayi > 100:
            risk = "KRİTİK" if sayi > 500 else "YÜKSEK"
            s.bulgular.append(Bulgu(
                kategori="Girişler",
                baslik=f"Yüksek sayıda başarısız giriş: {sayi}",
                detay="Kaba kuvvet saldırısı olabilir.",
                risk=risk,
                oneri="fail2ban kurun: sudo apt install fail2ban",
                puan=min(sayi // 20, 30),
            ))
        else:
            s.ozet = f"Başarısız giriş sayısı normal: {sayi}"
        return s

    # ── Rootkit ───────────────────────────────────────────────────────────────
    def _rootkit(self):
        from .utils import arac_var
        s = Sonuc(ad="Rootkit")
        bulundu = False

        for arac, flag, anahtar in [
            ("rkhunter",   "--check --skip-keypress --quiet", "Warning"),
            ("chkrootkit", "",                                "INFECTED"),
        ]:
            if arac_var(arac):
                bulundu = True
                ok, cikti = komut(f"{arac} {flag} 2>/dev/null", zaman_asimi=120)
                for satir in cikti.splitlines():
                    if anahtar in satir:
                        s.bulgular.append(Bulgu(
                            kategori="Rootkit",
                            baslik=f"{arac} uyarısı",
                            detay=satir.strip(),
                            risk="KRİTİK",
                            oneri="Sistemi izole edin ve detaylı inceleme yapın.",
                            puan=50,
                        ))

        if not bulundu:
            s.bulgular.append(Bulgu(
                kategori="Rootkit",
                baslik="Rootkit tarayıcı yüklü değil",
                detay="rkhunter veya chkrootkit bulunamadı.",
                risk="BİLGİ",
                oneri="sudo apt install rkhunter chkrootkit",
                puan=0,
            ))
        elif not s.bulgular:
            s.ozet = "Rootkit taramasında sorun tespit edilmedi."
        return s

    # ── WiFi ──────────────────────────────────────────────────────────────────
    def _wifi(self):
        s = Sonuc(ad="WiFi")
        ok, cikti = komut("nmcli -t -f active,ssid,security dev wifi 2>/dev/null")
        if not ok or not cikti.strip():
            s.ozet = "Kablosuz ağ arayüzü tespit edilmedi."
            return s

        for satir in cikti.splitlines():
            if satir.startswith("yes:"):
                parcalar = satir.split(":")
                guvenlik = parcalar[2].strip() if len(parcalar) > 2 else ""
                ssid     = parcalar[1] if len(parcalar) > 1 else "?"
                if guvenlik in ("", "--", "Open"):
                    s.bulgular.append(Bulgu(
                        kategori="WiFi",
                        baslik=f"Açık WiFi ağına bağlı: {ssid}",
                        detay="Şifresiz ağ — trafik dinlenebilir.",
                        risk="YÜKSEK",
                        oneri="WPA2/WPA3 şifreli ağ kullanın.",
                        puan=20,
                    ))

        if not s.bulgular:
            s.ozet = "WiFi bağlantısı şifreli."
        return s

    # ── Çıktı ─────────────────────────────────────────────────────────────────
    def yazdir(self, sonuclar):
        toplam = 0
        for _, sonuc in sonuclar.items():
            print(f"\n  {R.KALIN}{sonuc.ad}{R.SIFIRLA}")
            if sonuc.ozet and not sonuc.bulgular:
                yaz(f"    ✅ {sonuc.ozet}", R.YESIL)
                continue
            for b in sonuc.bulgular:
                toplam += 1
                renk = risk_rengi(b.risk)
                print(f"    {renk}[{b.risk}]{R.SIFIRLA} {b.baslik}")
                yaz(f"           → {b.detay}", R.GRI)
                if b.oneri:
                    yaz(f"           💡 {b.oneri}", R.CYAN)
        print()
        yaz(f"  📊 Toplam {toplam} blue team bulgusu.", R.MAVI)
