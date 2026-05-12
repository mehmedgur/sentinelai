"""
SentinelAI v1.2 - AI Analiz Modülü (Gemini API)
Yazar: s247003009
"""

import json
import urllib.request
import urllib.error
from .utils import yaz, R

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-pro:generateContent?key={key}"
)


class AIModul:
    """
    Google Gemini API ile güvenlik bulgularını analiz eder.
    Yazar: s247003009
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def baglanti_kontrol(self):
        try:
            url = GEMINI_URL.format(key=self.api_key)
            veri = json.dumps({
                "contents": [{"parts": [{"text": "merhaba"}]}]
            }).encode()
            req = urllib.request.Request(
                url, data=veri,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=8)
            return True
        except urllib.error.HTTPError as e:
            return e.code != 400
        except Exception:
            return False

    def analiz_et(self, tum_bulgular):
        ozet = self._ozetle(tum_bulgular)
        sonuclar = {}
        for anahtar, istem in [
            ("genel",    self._istem_genel(ozet)),
            ("oneri",    self._istem_oneri(ozet)),
            ("saldirgan",self._istem_saldirgan(ozet)),
        ]:
            yaz(f"  ↳ Gemini {anahtar} analizi yapıyor...", R.GRI)
            sonuclar[anahtar] = self._gemini(istem)
        return sonuclar

    def _gemini(self, istem, zaman_asimi=60):
        try:
            url  = GEMINI_URL.format(key=self.api_key)
            veri = json.dumps({
                "contents": [{"parts": [{"text": istem}]}],
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 800},
            }).encode()
            req  = urllib.request.Request(
                url, data=veri,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            yanit = urllib.request.urlopen(req, timeout=zaman_asimi)
            data  = json.loads(yanit.read().decode())
            return (
                data["candidates"][0]["content"]["parts"][0]["text"].strip()
            )
        except Exception as e:
            return f"Gemini hatası: {e}"

    def _istem_genel(self, ozet):
        return (
            "Sen deneyimli bir siber güvenlik uzmanısın. "
            "Aşağıdaki Linux sistem güvenlik taraması sonuçlarını "
            "Türkçe, kısa ve anlaşılır biçimde yorumla. Maksimum 5 cümle.\n\n"
            f"TARAMA:\n{ozet}"
        )

    def _istem_oneri(self, ozet):
        return (
            "Sen bir Linux güvenlik danışmanısın. "
            "Aşağıdaki bulgulara göre en kritik 5 iyileştirme önerisini "
            "Türkçe, numaralı liste halinde yaz. Her öneri somut bir eylem içermeli.\n\n"
            f"BULGULAR:\n{ozet}"
        )

    def _istem_saldirgan(self, ozet):
        return (
            "Sen etik bir sızma testi uzmanısın. "
            "Aşağıdaki sistem bilgilerine göre bir saldırganın bu sisteme "
            "nasıl yaklaşabileceğini savunmacı farkındalık için Türkçe açıkla. "
            "Gerçek saldırı tekniği verme. Maksimum 4 cümle.\n\n"
            f"SİSTEM:\n{ozet}"
        )

    def _ozetle(self, tum_bulgular):
        satirlar = []

        blue = tum_bulgular.get("blue_team", {})
        if blue:
            satirlar.append("=== BLUE TEAM ===")
            for _, bolum in blue.items():
                for b in bolum.bulgular:
                    satirlar.append(f"[{b.risk}] {b.baslik}: {b.detay}")

        red = tum_bulgular.get("red_team", {})
        if red:
            satirlar.append("\n=== RED TEAM ===")
            pt = red.get("port")
            if pt and pt.portlar:
                satirlar.append(f"Toplam {len(pt.portlar)} açık port.")
                for p in [x for x in pt.portlar if x.risk in ("KRİTİK","YÜKSEK")][:5]:
                    satirlar.append(f"  Port {p.port} ({p.servis}): [{p.risk}] {p.not_}")

        risk = tum_bulgular.get("risk")
        if risk:
            satirlar.append(f"\n=== RİSK ===")
            satirlar.append(
                f"Puan: {risk.puan}/100, Seviye: {risk.seviye}, "
                f"Kritik: {risk.kritik}, Yüksek: {risk.yuksek}"
            )

        return "\n".join(satirlar)

    def yazdir(self, sonuclar):
        basliklar = {
            "genel":     ("📋 Genel Güvenlik Yorumu",           R.CYAN),
            "oneri":     ("💡 Öncelikli İyileştirme Önerileri", R.YESIL),
            "saldirgan": ("🎯 Saldırgan Perspektifi",           R.SARI),
        }
        for anahtar, (baslik, renk) in basliklar.items():
            metin = sonuclar.get(anahtar, "")
            if metin:
                print()
                yaz(f"  {R.KALIN}{baslik}{R.SIFIRLA}", renk)
                print(f"  {'─'*55}")
                for satir in metin.splitlines():
                    print(f"  {satir}")
        print()
