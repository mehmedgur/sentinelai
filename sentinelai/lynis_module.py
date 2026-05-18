"""
SentinelAI v1.2 - Lynis Denetim Modülü
Yazar: BGT
"""

import re
from dataclasses import dataclass, field
from .utils import komut, arac_var, yaz, R


@dataclass
class LynisSonuc:
    hardening_index: int = 0
    uyarilar:        list = field(default_factory=list)
    oneriler:        list = field(default_factory=list)
    ozet:            str  = ""


class LynisDenetim:
    """
    Lynis sistem sertleştirme denetimi.
    Kurulu değilse otomatik kurar.
    Yazar: BGT
    """

    def calistir(self, sessiz=False):
        if not sessiz:
            yaz("  ↳ Lynis kurulum kontrol ediliyor...", R.GRI)

        if not arac_var("lynis"):
            if not sessiz:
                yaz("  ℹ️  Lynis yüklü değil — kuruluyor...", R.SARI)
            ok, _ = komut("sudo apt install -y lynis 2>/dev/null")
            if not ok:
                s = LynisSonuc()
                s.ozet = "Lynis kurulamadı."
                return s

        if not sessiz:
            yaz("  ↳ Lynis denetimi başlatılıyor (sudo gerekli)...", R.GRI)

        ok, cikti = komut(
            "sudo lynis audit system --quiet --no-colors 2>/dev/null",
            zaman_asimi=300,
        )

        return self._parse(cikti)

    def _parse(self, cikti):
        s = LynisSonuc()
        for satir in cikti.splitlines():
            m = re.search(r"Hardening index\s*:\s*(\d+)", satir)
            if m:
                s.hardening_index = int(m.group(1))
            if "Warning" in satir:
                s.uyarilar.append(satir.strip())
            if "Suggestion" in satir:
                s.oneriler.append(satir.strip())

        s.ozet = (
            f"Hardening Index: {s.hardening_index}/100 — "
            f"{len(s.uyarilar)} uyarı, {len(s.oneriler)} öneri."
        )
        return s

    def yazdir(self, sonuc):
        from .utils import cubuk
        renk = R.YESIL if sonuc.hardening_index >= 70 else (
               R.SARI  if sonuc.hardening_index >= 50 else R.KIRMIZI)

        print()
        yaz(f"  Hardening Index : {sonuc.hardening_index}/100", renk)
        yaz(f"  [{cubuk(sonuc.hardening_index)}]", renk)

        if sonuc.uyarilar:
            yaz(f"\n  ⚠️  Lynis Uyarıları ({len(sonuc.uyarilar)}):", R.SARI)
            for u in sonuc.uyarilar[:10]:
                yaz(f"    → {u}", R.GRI)

        yaz(f"\n  📝 {sonuc.ozet}", R.CYAN)
