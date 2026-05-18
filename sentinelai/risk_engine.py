"""
SentinelAI v1.2 - Risk Motoru
Yazar: BGT
"""

from dataclasses import dataclass, field
from .utils import yaz, cubuk, risk_rengi, R


@dataclass
class RiskSonuc:
    puan:       int  = 0
    seviye:     str  = "GÜVENLİ"
    kritik:     int  = 0
    yuksek:     int  = 0
    orta:       int  = 0
    dusuk:      int  = 0
    bilgi:      int  = 0
    oneriler:   list = field(default_factory=list)
    ozet:       str  = ""


ESIKLER = [(80,"KRİTİK"),(60,"YÜKSEK"),(40,"ORTA"),(20,"DÜŞÜK"),(0,"GÜVENLİ")]
PUAN_MAP = {"KRİTİK":40,"YÜKSEK":25,"ORTA":15,"DÜŞÜK":5,"BİLGİ":1}


class RiskMotoru:
    """Yazar: s247003009"""

    def hesapla(self, bulgular):
        s   = RiskSonuc()
        ham = 0

        # Blue Team
        for _, bolum in bulgular.get("blue_team", {}).items():
            for b in bolum.bulgular:
                ham += getattr(b, "puan", 0)
                self._say(s, getattr(b, "risk", "BİLGİ"))
                if b.risk in ("KRİTİK","YÜKSEK") and b.oneri:
                    s.oneriler.append({"kaynak":"Blue","baslik":b.baslik,
                                       "risk":b.risk,"oneri":b.oneri})

        # Red Team port
        red = bulgular.get("red_team", {})
        pt  = red.get("port")
        if pt:
            for p in getattr(pt, "portlar", []):
                ham += min(PUAN_MAP.get(p.risk, 1) // 3, 10)
                self._say(s, p.risk)

        # Red Team zafiyet
        zaf = red.get("zafiyet")
        if zaf:
            for b in getattr(zaf, "bulgular", []):
                ham += PUAN_MAP.get(b.get("risk","BİLGİ"), 1)
                self._say(s, b.get("risk","BİLGİ"))
                if b.get("risk") in ("KRİTİK","YÜKSEK"):
                    s.oneriler.append({"kaynak":"Red","baslik":b.get("baslik",""),
                                       "risk":b.get("risk",""),"oneri":b.get("oneri","")})

        # Lynis
        lynis = bulgular.get("lynis")
        if lynis:
            hi = getattr(lynis, "hardening_index", 100)
            ham += max(0, (100 - hi) // 5)

        s.puan = min(ham, 100)
        for esik, seviye in ESIKLER:
            if s.puan >= esik:
                s.seviye = seviye
                break

        oncelik = {"KRİTİK":0,"YÜKSEK":1,"ORTA":2,"DÜŞÜK":3,"BİLGİ":4}
        s.oneriler.sort(key=lambda x: oncelik.get(x.get("risk","BİLGİ"), 5))
        s.ozet = self._ozet(s)
        return s

    def _say(self, s, risk):
        if risk == "KRİTİK": s.kritik += 1
        elif risk == "YÜKSEK": s.yuksek += 1
        elif risk == "ORTA":   s.orta   += 1
        elif risk == "DÜŞÜK":  s.dusuk  += 1
        else:                  s.bilgi  += 1

    def _ozet(self, s):
        return {
            "KRİTİK":  "Sistem ciddi güvenlik açıkları barındırıyor. Acil müdahale gerekli.",
            "YÜKSEK":  "Önemli güvenlik zafiyetleri tespit edildi. En kısa sürede giderilmeli.",
            "ORTA":    "Orta düzeyde riskler var. Planlı iyileştirme başlatılmalı.",
            "DÜŞÜK":   "Düşük seviyeli riskler. İyi güvenlik duruşu; küçük iyileştirmeler yapılabilir.",
            "GÜVENLİ": "Sistem güvenli görünüyor. Periyodik denetimlere devam edin.",
        }.get(s.seviye, "")

    def yazdir(self, s):
        renk = risk_rengi(s.seviye)
        print()
        yaz(f"  Risk Puanı : {s.puan}/100  —  {s.seviye}", renk)
        yaz(f"  [{cubuk(s.puan)}]", renk)
        print()
        for ad, sayi, rk in [
            ("KRİTİK", s.kritik, R.KIRMIZI),
            ("YÜKSEK",  s.yuksek, R.SARI),
            ("ORTA",    s.orta,   R.MAVI),
            ("DÜŞÜK",   s.dusuk,  R.YESIL),
            ("BİLGİ",   s.bilgi,  R.GRI),
        ]:
            if sayi:
                print(f"  {rk}{ad:<10}{R.SIFIRLA}  {sayi:>3} bulgu  {rk}{'●'*min(sayi,10)}{R.SIFIRLA}")
        print()
        yaz(f"  📝 {s.ozet}", renk)
        if s.oneriler:
            yaz("\n  🔝 Öncelikli Öneriler:", R.KALIN)
            for i, o in enumerate(s.oneriler[:5], 1):
                renk2 = risk_rengi(o.get("risk","BİLGİ"))
                print(f"  {i}. {renk2}[{o.get('risk','?')}]{R.SIFIRLA} {o.get('baslik','')}")
                yaz(f"       💡 {o.get('oneri','')}", R.CYAN)
        print()
