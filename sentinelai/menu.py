"""
SentinelAI v1.2 - Menü Motoru
Author:009
"""

from .utils import yaz, bolum, temizle, R
from .analyzer     import BlueTeam
from .scanner      import RedTeam
from .lynis_module import LynisDenetim
from .risk_engine  import RiskMotoru
from .ai_module    import AIModul
from .report       import RaporOlusturucu


class Menu:
    """
    İnteraktif ana menü.
    Kullanıcı yalnızca onay verir; geri kalanı script halleder.
    Author: Mehmed Gurbuz, Goksu Uludas, Bektas Ozkara
    """

    def __init__(self, mod, hedef, api_key=None):
        self.mod     = mod
        self.hedef   = hedef
        self.api_key = api_key
        self._son_bulgular = {}

    def baslat(self):
        while True:
            secim = self._ana_menu()
            if   secim == "1": self._blue()
            elif secim == "2": self._red()
            elif secim == "3": self._lynis()
            elif secim == "4": self._tam()
            elif secim == "5": self._ai()
            elif secim == "6": self._rapor()
            elif secim == "0": self._cikis()
            else:
                yaz("  Geçersiz seçim. 0-6 arası bir sayı girin.", R.SARI)
                import time; time.sleep(1)

    # ── Ana Menü ──────────────────────────────────────────────────────────────
    def _ana_menu(self):
        temizle()
        self._mini_baslik()
        yaz(f"\n  {R.KALIN}Ana Menü{R.SIFIRLA}\n")

        satirlar = [
            ("1", "🔵", "Blue Team Analizi",              "12 kontrol", R.MAVI),
            ("2", "🔴", "Red Team Taraması",              "7 tarama",   R.KIRMIZI),
            ("3", "🔬", "Lynis Sistem Denetimi",          "otomatik",   R.YESIL),
            ("4", "⚡", "Tam Analiz (Blue + Red + Lynis)","önerilir",   R.SARI),
            ("5", "🤖", "AI Güvenlik Yorumu",             "Gemini API", R.EFLATUN),
            ("6", "📄", "Rapor Oluştur / Görüntüle",      "MD + JSON",  R.CYAN),
        ]
        for no, ikon, etiket, rozet, renk in satirlar:
            print(
                f"  {renk}{R.KALIN}[{no}]{R.SIFIRLA}  {ikon}  "
                f"{R.BEYAZ}{etiket:<42}{R.SIFIRLA}  "
                f"{R.GRI}[{rozet}]{R.SIFIRLA}"
            )

        print(f"\n  {R.GRI}[0]{R.SIFIRLA}  🚪  {R.GRI}Çıkış{R.SIFIRLA}")
        print(f"\n  {R.GRI}Mod: {R.SARI}{self.mod.capitalize()}{R.GRI}  |  "
              f"Hedef: {R.BEYAZ}{self.hedef}{R.SIFIRLA}")
        print(f"\n  {R.GRI}Seçiminiz (0-6):{R.SIFIRLA} ", end="")
        return input().strip()

    # ── Onay ──────────────────────────────────────────────────────────────────
    def _onay(self, soru):
        yaz(f"\n  ❓ {soru}", R.SARI)
        print(f"\n     {R.YESIL}[E]{R.SIFIRLA} Evet    {R.KIRMIZI}[H]{R.SIFIRLA} Hayır\n")
        while True:
            s = input(f"  {R.GRI}Seçiminiz:{R.SIFIRLA} ").strip().lower()
            if s in ("e","evet","y","yes"): return True
            if s in ("h","hayir","hayır","n","no"): return False
            yaz("  [E] veya [H] girin.", R.SARI)

    def _devam(self):
        input(f"\n  {R.GRI}Devam için Enter'a basın...{R.SIFIRLA}")

    # ── Blue Team ─────────────────────────────────────────────────────────────
    def _blue(self):
        temizle()
        bolum("🔵 BLUE TEAM — Savunma Analizi", R.MAVI)
        if not self._onay("Blue Team analizi başlatılsın mı?"):
            return
        bolum("🔵 BLUE TEAM — Çalışıyor...", R.MAVI)
        bt = BlueTeam()
        sonuclar = bt.calistir()
        bt.yazdir(sonuclar)
        risk = RiskMotoru().hesapla({"blue_team": sonuclar})
        RiskMotoru().yazdir(risk)
        self._son_bulgular["blue_team"] = sonuclar
        self._son_bulgular["risk"]      = risk
        self._devam()

    # ── Red Team ──────────────────────────────────────────────────────────────
    def _red(self):
        temizle()
        bolum("🔴 RED TEAM — Saldırı Yüzeyi", R.KIRMIZI)
        yaz(f"  {R.SARI}⚠️  Gerçek saldırı yapılmaz — yalnızca analiz.{R.SIFIRLA}\n")
        if not self._onay("Red Team taraması başlatılsın mı?"):
            return
        bolum("🔴 RED TEAM — Çalışıyor...", R.KIRMIZI)
        rt = RedTeam(hedef=self.hedef)
        sonuclar = rt.calistir()
        rt.yazdir(sonuclar)
        self._son_bulgular["red_team"] = sonuclar
        self._devam()

    # ── Lynis ─────────────────────────────────────────────────────────────────
    def _lynis(self):
        temizle()
        bolum("🔬 LYNİS SİSTEM DENETİMİ", R.YESIL)
        yaz("  Lynis yüklü değilse otomatik kurulacak (sudo gerekli).\n", R.GRI)
        if not self._onay("Lynis denetimi başlatılsın mı?"):
            return
        bolum("🔬 LYNİS — Çalışıyor...", R.YESIL)
        ld = LynisDenetim()
        sonuc = ld.calistir()
        ld.yazdir(sonuc)
        self._son_bulgular["lynis"] = sonuc
        self._devam()

    # ── Tam Analiz ────────────────────────────────────────────────────────────
    def _tam(self):
        temizle()
        bolum("⚡ TAM ANALİZ — Blue + Red + Lynis", R.SARI)
        yaz("  Tahmini süre: ~10 dakika\n", R.GRI)
        if not self._onay("Tam analiz başlatılsın mı?"):
            return

        tum = {}

        bolum("🔵 BLUE TEAM", R.MAVI)
        bt = BlueTeam()
        blue = bt.calistir()
        bt.yazdir(blue)
        tum["blue_team"] = blue

        bolum("🔴 RED TEAM", R.KIRMIZI)
        rt = RedTeam(hedef=self.hedef)
        red = rt.calistir()
        rt.yazdir(red)
        tum["red_team"] = red

        bolum("🔬 LYNİS", R.YESIL)
        ld = LynisDenetim()
        lynis = ld.calistir()
        ld.yazdir(lynis)
        tum["lynis"] = lynis

        bolum("⚖️  RİSK DEĞERLENDİRMESİ", R.SARI)
        risk = RiskMotoru().hesapla(tum)
        RiskMotoru().yazdir(risk)
        tum["risk"] = risk

        self._son_bulgular = tum
        self._devam()

    # ── AI ────────────────────────────────────────────────────────────────────
    def _ai(self):
        temizle()
        bolum("🤖 AI GÜVENLİK YORUMU — Gemini", R.EFLATUN)

        if not self.api_key:
            yaz("  ⚠️  API anahtarı tanımlı değil.", R.SARI)
            key = input(f"  {R.EFLATUN}Gemini API Anahtarı:{R.SIFIRLA} ").strip()
            if not key:
                self._devam()
                return
            self.api_key = key

        if not self._son_bulgular:
            yaz("  ⚠️  Önce en az bir analiz çalıştırın.", R.SARI)
            self._devam()
            return

        if not self._onay("AI analizi başlatılsın mı?"):
            return

        bolum("🤖 AI — Çalışıyor...", R.EFLATUN)
        ai = AIModul(self.api_key)
        if not ai.baglanti_kontrol():
            yaz("  ❌ Gemini API'ye bağlanılamadı. API anahtarını kontrol edin.", R.KIRMIZI)
            self._devam()
            return

        sonuc = ai.analiz_et(self._son_bulgular)
        ai.yazdir(sonuc)
        self._son_bulgular["ai"] = sonuc
        self._devam()

    # ── Rapor ─────────────────────────────────────────────────────────────────
    def _rapor(self):
        temizle()
        bolum("📄 RAPOR OLUŞTUR / GÖRÜNTÜLE", R.CYAN)

        if not self._son_bulgular:
            yaz("  ⚠️  Önce en az bir analiz çalıştırın.", R.SARI)
            self._devam()
            return

        if not self._onay("Rapor oluşturulsun mu? (MD + JSON)"):
            return

        bolum("📄 RAPOR — Kaydediliyor...", R.CYAN)
        rapor = RaporOlusturucu()
        rapor.kaydet(self._son_bulgular)
        yaz("  ✅ Rapor kaydedildi.", R.YESIL)
        self._devam()

    # ── Çıkış ─────────────────────────────────────────────────────────────────
    def _cikis(self):
        temizle()
        yaz("\n  👋 SentinelAI kapatıldı. Güvende kalın.\n", R.CYAN)
        import sys; sys.exit(0)

    # ── Yardımcı ──────────────────────────────────────────────────────────────
    def _mini_baslik(self):
        yaz("  🛡️  SentinelAI v1.2", R.CYAN + R.KALIN)
        yaz(f"  {'─' * 40}", R.GRI)
