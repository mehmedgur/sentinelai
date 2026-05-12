"""
SentinelAI v1.2 - Red Team Tarama Modülü
Yazar: s247003009
⚠️  Gerçek saldırı yapılmaz — yalnızca analiz
"""

import re
import os
from dataclasses import dataclass, field
from .utils import komut, arac_var, yaz, risk_rengi, R

RISKLI_PORTLAR = {
    21:    ("FTP",          "ORTA",   "Şifresiz FTP — SFTP kullanın."),
    22:    ("SSH",          "DÜŞÜK",  "SSH aktif — anahtar doğrulaması kullanın."),
    23:    ("Telnet",       "YÜKSEK", "Şifresiz — SSH kullanın."),
    25:    ("SMTP",         "ORTA",   "Mail sunucu — gereksizse kapatın."),
    80:    ("HTTP",         "DÜŞÜK",  "HTTPS'ye yönlendirme ekleyin."),
    443:   ("HTTPS",        "BİLGİ",  "Sertifika geçerliliğini kontrol edin."),
    445:   ("SMB",          "YÜKSEK", "EternalBlue riski."),
    2375:  ("Docker API",   "KRİTİK", "Docker API şifresiz açık — kapatın!"),
    3306:  ("MySQL",        "YÜKSEK", "bind-address=127.0.0.1 yapın."),
    3389:  ("RDP",          "YÜKSEK", "NLA zorunlu tutun."),
    5432:  ("PostgreSQL",   "ORTA",   "Yerel erişimle kısıtlayın."),
    6379:  ("Redis",        "YÜKSEK", "Kimlik doğrulama ekleyin."),
    8080:  ("HTTP-Alt",     "DÜŞÜK",  "SSL ekleyin."),
    9200:  ("Elasticsearch","KRİTİK", "Kimlik doğrulamasız açık!"),
    27017: ("MongoDB",      "YÜKSEK", "Kimlik doğrulama etkinleştirin."),
}

WEB_PORTLAR = {80, 443, 8080, 8443, 8000, 3000}


@dataclass
class Port:
    port:     int
    protokol: str
    servis:   str
    versiyon: str = ""
    risk:     str = "BİLGİ"
    not_:     str = ""


@dataclass
class Sonuc:
    ad:       str
    bulgular: list = field(default_factory=list)
    portlar:  list = field(default_factory=list)
    ozet:     str = ""


class RedTeam:
    """
    Red Team — 7 saldırı yüzeyi taraması.
    Yazar: s247003009
    """

    def __init__(self, hedef="localhost", sessiz=False):
        self.hedef  = hedef
        self.sessiz = sessiz
        self._web_portlar = []

    def calistir(self):
        taramalar = [
            ("port",    "🔍 Port Taraması",             self._port),
            ("nse",     "🧩 NSE Zafiyet Scriptleri",    self._nse),
            ("servis",  "🏷️  Servis Tespiti",             self._servis),
            ("zafiyet", "⚠️  Zafiyet Simülasyonu",        self._zafiyet),
            ("nikto",   "🌐 Nikto Web Taraması",         self._nikto),
            ("gobuster","📂 Gobuster Dizin Taraması",    self._gobuster),
            ("agkesif", "📡 Ağ Keşfi",                  self._agkesif),
            ("pspy",    "👁️  Process İzleme (pspy)",      self._pspy),
        ]
        sonuclar = {}
        for anahtar, isim, fonk in taramalar:
            if not self.sessiz:
                yaz(f"  ↳ {isim} çalışıyor...", R.GRI)
            s = fonk()
            s.ad = isim
            sonuclar[anahtar] = s
        return sonuclar

    # ── Port Taraması: nmap → masscan → ss ───────────────────────────────────
    def _port(self):
        s = Sonuc(ad="Port")
        if arac_var("nmap"):
            s.portlar = self._nmap()
        elif arac_var("masscan"):
            yaz("  ℹ️  nmap yok → masscan kullanılıyor...", R.GRI)
            s.portlar = self._masscan()
        else:
            yaz("  ℹ️  nmap/masscan yok → ss kullanılıyor...", R.GRI)
            s.portlar = self._ss()

        self._web_portlar = [p.port for p in s.portlar if p.port in WEB_PORTLAR]
        s.ozet = f"{len(s.portlar)} açık port."
        return s

    def _nmap(self):
        ok, cikti = komut(
            f"nmap -sV --open -T4 --top-ports 1000 {self.hedef} 2>/dev/null",
            zaman_asimi=120,
        )
        portlar = []
        if not ok:
            return portlar
        for satir in cikti.splitlines():
            m = re.match(r"(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)", satir.strip())
            if m:
                no = int(m.group(1))
                rb = RISKLI_PORTLAR.get(no, ("", "BİLGİ", ""))
                portlar.append(Port(
                    port=no, protokol=m.group(2),
                    servis=m.group(3), versiyon=m.group(4).strip(),
                    risk=rb[1], not_=rb[2],
                ))
        return portlar

    def _masscan(self):
        ok, cikti = komut(
            f"masscan {self.hedef} -p1-65535 --rate=1000 2>/dev/null",
            zaman_asimi=120,
        )
        portlar = []
        if not ok:
            return portlar
        for satir in cikti.splitlines():
            m = re.search(r"port (\d+)/(tcp|udp)", satir)
            if m:
                no = int(m.group(1))
                rb = RISKLI_PORTLAR.get(no, ("Bilinmiyor", "BİLGİ", ""))
                portlar.append(Port(
                    port=no, protokol=m.group(2),
                    servis=rb[0], risk=rb[1], not_=rb[2],
                ))
        return sorted(portlar, key=lambda p: p.port)

    def _ss(self):
        ok, cikti = komut("ss -tlnp 2>/dev/null")
        portlar = []
        gorulmus = set()
        for satir in cikti.splitlines():
            m = re.search(r":(\d{2,5})\s", satir)
            if m:
                no = int(m.group(1))
                if no in gorulmus or no > 65535:
                    continue
                gorulmus.add(no)
                rb = RISKLI_PORTLAR.get(no, ("Bilinmiyor", "BİLGİ", ""))
                portlar.append(Port(
                    port=no, protokol="tcp",
                    servis=rb[0], risk=rb[1], not_=rb[2],
                ))
        return sorted(portlar, key=lambda p: p.port)

    # ── NSE Zafiyet Scriptleri ────────────────────────────────────────────────
    def _nse(self):
        s = Sonuc(ad="NSE")
        if not arac_var("nmap"):
            s.ozet = "nmap yüklü değil — NSE taraması atlandı."
            return s

        ok, cikti = komut(
            f"nmap --script vuln --open -T4 {self.hedef} 2>/dev/null",
            zaman_asimi=180,
        )
        if not ok:
            s.ozet = "NSE taraması tamamlanamadı."
            return s

        for satir in cikti.splitlines():
            if "VULNERABLE" in satir or "CVE" in satir:
                s.bulgular.append({
                    "baslik": satir.strip(),
                    "risk":   "YÜKSEK",
                })

        if not s.bulgular:
            s.ozet = "NSE taramasında bilinen zafiyet tespit edilmedi."
        return s

    # ── Servis Tespiti ────────────────────────────────────────────────────────
    def _servis(self):
        s = Sonuc(ad="Servisler")
        ok, cikti = komut(
            "systemctl list-units --type=service --state=running "
            "--no-pager --no-legend 2>/dev/null"
        )
        if ok and cikti:
            for satir in cikti.splitlines():
                p = satir.split()
                if p:
                    s.bulgular.append({"servis": p[0]})
        s.ozet = f"{len(s.bulgular)} aktif servis."
        return s

    # ── Zafiyet Simülasyonu ───────────────────────────────────────────────────
    def _zafiyet(self):
        s = Sonuc(ad="Zafiyet Sim.")

        # Docker soketi
        for soket in ["/var/run/docker.sock", "/run/docker.sock"]:
            if os.path.exists(soket) and os.access(soket, os.W_OK):
                s.bulgular.append({
                    "baslik": "Docker soketi yazılabilir",
                    "detay":  f"{soket} — konteyner ayrıcalık yükseltmesi mümkün.",
                    "risk":   "KRİTİK",
                    "oneri":  "Docker grubundan gereksiz kullanıcıları çıkarın.",
                })

        # Yazılabilir /etc/passwd
        if os.path.exists("/etc/passwd") and os.access("/etc/passwd", os.W_OK):
            s.bulgular.append({
                "baslik": "/etc/passwd herkes tarafından yazılabilir",
                "detay":  "Saldırgan root hesabı ekleyebilir.",
                "risk":   "KRİTİK",
                "oneri":  "chmod 644 /etc/passwd",
            })

        if not s.bulgular:
            s.ozet = "Zafiyet simülasyonunda kritik sorun tespit edilmedi."
        return s

    # ── Nikto ─────────────────────────────────────────────────────────────────
    def _nikto(self):
        s = Sonuc(ad="Nikto")
        if not arac_var("nikto"):
            s.ozet = "nikto yüklü değil — 'sudo apt install nikto' ile kurabilirsiniz."
            return s
        if not self._web_portlar:
            s.ozet = "Açık web portu bulunamadı — Nikto atlandı."
            return s

        for port in self._web_portlar[:2]:
            ssl = "-ssl" if port in (443, 8443) else ""
            ok, cikti = komut(
                f"nikto -h {self.hedef} -p {port} {ssl} -maxtime 60 2>/dev/null",
                zaman_asimi=90,
            )
            if ok:
                for satir in cikti.splitlines():
                    if satir.startswith("+"):
                        s.bulgular.append({
                            "baslik": satir.strip(),
                            "port":   port,
                            "risk":   "ORTA",
                        })

        if not s.bulgular:
            s.ozet = "Nikto taramasında belirgin sorun tespit edilmedi."
        return s

    # ── Gobuster ──────────────────────────────────────────────────────────────
    def _gobuster(self):
        s = Sonuc(ad="Gobuster")
        arac = "gobuster" if arac_var("gobuster") else ("dirb" if arac_var("dirb") else None)

        if not arac:
            s.ozet = "gobuster/dirb yüklü değil."
            return s
        if not self._web_portlar:
            s.ozet = "Açık web portu yok — Gobuster atlandı."
            return s

        port = self._web_portlar[0]
        protokol = "https" if port in (443, 8443) else "http"
        url = f"{protokol}://{self.hedef}:{port}"

        if arac == "gobuster":
            ok, cikti = komut(
                f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt "
                f"-q -t 20 2>/dev/null",
                zaman_asimi=120,
            )
        else:
            ok, cikti = komut(
                f"dirb {url} /usr/share/wordlists/dirb/common.txt -S 2>/dev/null",
                zaman_asimi=120,
            )

        if ok:
            for satir in cikti.splitlines():
                if "200" in satir or "301" in satir or "+" in satir:
                    s.bulgular.append({"yol": satir.strip(), "risk": "BİLGİ"})

        s.ozet = f"{len(s.bulgular)} dizin/dosya bulundu."
        return s

    # ── Ağ Keşfi ─────────────────────────────────────────────────────────────
    def _agkesif(self):
        s = Sonuc(ad="Ağ Keşfi")
        if arac_var("arp-scan"):
            ok, cikti = komut("arp-scan --localnet 2>/dev/null", zaman_asimi=30)
        elif arac_var("netdiscover"):
            ok, cikti = komut("netdiscover -P -r 192.168.1.0/24 2>/dev/null",
                              zaman_asimi=30)
        else:
            s.ozet = "arp-scan/netdiscover yüklü değil."
            return s

        if ok and cikti:
            for satir in cikti.splitlines():
                m = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([\w:]+)", satir)
                if m:
                    s.bulgular.append({"ip": m.group(1), "mac": m.group(2)})

        s.ozet = f"{len(s.bulgular)} cihaz tespit edildi."
        return s

    # ── pspy ──────────────────────────────────────────────────────────────────
    def _pspy(self):
        s = Sonuc(ad="pspy")
        if not arac_var("pspy") and not arac_var("pspy64"):
            s.ozet = "pspy yüklü değil — https://github.com/DominicBreuker/pspy"
            return s

        arac = "pspy64" if arac_var("pspy64") else "pspy"
        ok, cikti = komut(f"{arac} -p -t 5000 2>/dev/null", zaman_asimi=15)

        if ok and cikti:
            for satir in cikti.splitlines():
                if "UID=0" in satir and "CMD" in satir:
                    s.bulgular.append({
                        "baslik": "Root process tespit edildi",
                        "detay":  satir.strip(),
                        "risk":   "BİLGİ",
                    })

        s.ozet = f"{len(s.bulgular)} root process tespit edildi."
        return s

    # ── Çıktı ─────────────────────────────────────────────────────────────────
    def yazdir(self, sonuclar):
        # Port tablosu
        port_s = sonuclar.get("port")
        if port_s and port_s.portlar:
            yaz("\n  📋 Açık Portlar:", R.KIRMIZI)
            print(f"\n  {'PORT':<8}{'PROTOKOL':<12}{'SERVİS':<14}{'RİSK':<10}{'NOT'}")
            print(f"  {'─'*70}")
            for p in port_s.portlar[:25]:
                renk = risk_rengi(p.risk)
                print(
                    f"  {R.BEYAZ}{p.port:<8}{R.GRI}{p.protokol:<12}"
                    f"{R.BEYAZ}{p.servis:<14}{renk}{p.risk:<10}{R.GRI}{p.not_[:30]}{R.SIFIRLA}"
                )

        # Zafiyet simülasyonu
        zaf = sonuclar.get("zafiyet")
        if zaf and zaf.bulgular:
            yaz("\n  ⚠️  Zafiyet Simülasyonu:", R.KIRMIZI)
            for b in zaf.bulgular:
                renk = risk_rengi(b.get("risk", "BİLGİ"))
                print(f"    {renk}[{b.get('risk','?')}]{R.SIFIRLA} {b.get('baslik','')}")
                yaz(f"           → {b.get('detay','')}", R.GRI)
                if b.get("oneri"):
                    yaz(f"           💡 {b['oneri']}", R.CYAN)

        toplam_port = len(port_s.portlar) if port_s else 0
        toplam_zaf  = len(zaf.bulgular) if zaf else 0
        print()
        yaz(
            f"  📊 Red Team: {toplam_port} açık port, "
            f"{toplam_zaf} simüle zafiyet.",
            R.KIRMIZI,
        )
