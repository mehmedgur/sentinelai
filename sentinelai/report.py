"""
SentinelAI v1.2 - Rapor Modülü
Yazar: BGT
"""

import os
import json
from datetime import datetime
from dataclasses import asdict, is_dataclass
from .utils import yaz, R


def _donustur(nesne):
    if is_dataclass(nesne) and not isinstance(nesne, type):
        return {k: _donustur(v) for k, v in asdict(nesne).items()}
    if isinstance(nesne, list):
        return [_donustur(i) for i in nesne]
    if isinstance(nesne, dict):
        return {k: _donustur(v) for k, v in nesne.items()}
    return nesne


class RaporOlusturucu:
    """Yazar: s247003009"""

    def __init__(self, dizin="./sentinelai_rapor"):
        self.dizin = dizin

    def kaydet(self, bulgular):
        os.makedirs(self.dizin, exist_ok=True)
        ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
        md_yol  = os.path.join(self.dizin, f"sentinelai_{ts}.md")
        json_yol= os.path.join(self.dizin, f"sentinelai_{ts}.json")

        self._json(bulgular, json_yol)
        self._markdown(bulgular, md_yol)

        yaz(f"  📝 Markdown : {md_yol}", R.GRI)
        yaz(f"  📦 JSON     : {json_yol}", R.GRI)
        return md_yol

    def _json(self, bulgular, yol):
        try:
            with open(yol, "w", encoding="utf-8") as f:
                json.dump(_donustur(bulgular), f, ensure_ascii=False, indent=2)
        except Exception as e:
            yaz(f"  ⚠️  JSON hatası: {e}", R.SARI)

    def _markdown(self, bulgular, yol):
        zaman = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        s = [
            "# 🛡️ SentinelAI v1.2 — Güvenlik Raporu",
            "",
            f"> **Tarih:** {zaman}  ",
            f"> **Yapımcı:** s247003009  ",
            f"> ⚠️ Yalnızca etik ve eğitim amaçlıdır.",
            "",
            "---",
            "",
        ]

        # Risk özeti
        risk = bulgular.get("risk")
        if risk:
            s += [
                "## ⚖️ Risk Özeti",
                "",
                f"| Puan | Seviye | Kritik | Yüksek | Orta | Düşük |",
                f"|------|--------|--------|--------|------|-------|",
                f"| {risk.puan}/100 | **{risk.seviye}** | "
                f"{risk.kritik} | {risk.yuksek} | {risk.orta} | {risk.dusuk} |",
                "",
                f"**{risk.ozet}**",
                "",
                "---",
                "",
            ]

        # Blue Team
        blue = bulgular.get("blue_team", {})
        if blue:
            s += ["## 🔵 Blue Team", ""]
            for _, bolum in blue.items():
                if not bolum.bulgular:
                    continue
                s.append(f"### {bolum.ad}")
                s.append("")
                s.append("| Risk | Başlık | Öneri |")
                s.append("|------|--------|-------|")
                for b in bolum.bulgular:
                    s.append(f"| `{b.risk}` | {b.baslik} | {b.oneri} |")
                s.append("")
            s += ["---", ""]

        # Red Team
        red = bulgular.get("red_team", {})
        if red:
            s += ["## 🔴 Red Team", ""]
            pt = red.get("port")
            if pt and pt.portlar:
                s.append("### Açık Portlar")
                s.append("")
                s.append("| Port | Servis | Risk | Not |")
                s.append("|------|--------|------|-----|")
                for p in pt.portlar:
                    s.append(f"| {p.port} | {p.servis} | `{p.risk}` | {p.not_ or '-'} |")
                s.append("")
            s += ["---", ""]

        # Lynis
        lynis = bulgular.get("lynis")
        if lynis:
            s += [
                "## 🔬 Lynis Denetimi",
                "",
                f"**Hardening Index:** {lynis.hardening_index}/100  ",
                f"**Uyarı:** {len(lynis.uyarilar)}  ",
                f"**Öneri:** {len(lynis.oneriler)}",
                "",
                "---",
                "",
            ]

        # AI yorumu
        ai = bulgular.get("ai")
        if ai and isinstance(ai, dict):
            s += ["## 🤖 AI Analizi", ""]
            for anahtar, baslik in [
                ("genel",    "Genel Yorum"),
                ("oneri",    "Öneriler"),
                ("saldirgan","Saldırgan Perspektifi"),
            ]:
                if ai.get(anahtar):
                    s += [f"### {baslik}", "", ai[anahtar], ""]
            s += ["---", ""]

        # Öncelikli öneriler
        if risk and risk.oneriler:
            s += ["## 💡 Öncelikli Öneriler", ""]
            for i, o in enumerate(risk.oneriler[:10], 1):
                s.append(
                    f"{i}. **[{o.get('risk','?')}]** {o.get('baslik','')}  \n"
                    f"   → {o.get('oneri','')}"
                )
            s.append("")

        # Yasal
        s += [
            "---",
            "",
            "## ⚠️ Yasal Uyarı",
            "",
            "Bu rapor yalnızca etik ve eğitim amaçlıdır. "
            "Yetkisiz sistemlerde kullanmak yasaktır.",
            "",
        ]

        try:
            with open(yol, "w", encoding="utf-8") as f:
                f.write("\n".join(s))
        except Exception as e:
            yaz(f"  ⚠️  Markdown hatası: {e}", R.SARI)
