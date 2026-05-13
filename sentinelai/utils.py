"""
SentinelAI v1.2 - Yardımcı Araçlar
Author: 009
"""

import os
import subprocess
import shutil


class R:
    SIFIRLA  = "\033[0m"
    KALIN    = "\033[1m"
    KIRMIZI  = "\033[91m"
    YESIL    = "\033[92m"
    SARI     = "\033[93m"
    MAVI     = "\033[94m"
    EFLATUN  = "\033[95m"
    CYAN     = "\033[96m"
    BEYAZ    = "\033[97m"
    GRI      = "\033[90m"
    BG_KIRMIZI = "\033[41m"


def yaz(metin, renk=R.BEYAZ, son="\n"):
    print(f"{renk}{metin}{R.SIFIRLA}", end=son)


def bolum(baslik, renk=R.CYAN):
    print(f"\n{renk}{R.KALIN}  {'═' * 58}{R.SIFIRLA}")
    print(f"{renk}{R.KALIN}  {baslik}{R.SIFIRLA}")
    print(f"{renk}  {'─' * 58}{R.SIFIRLA}\n")


def risk_rengi(seviye):
    return {
        "KRİTİK": R.BG_KIRMIZI + R.BEYAZ,
        "YÜKSEK": R.KIRMIZI,
        "ORTA":   R.SARI,
        "DÜŞÜK":  R.YESIL,
        "BİLGİ":  R.GRI,
        "TAMAM":  R.YESIL,
    }.get(seviye, R.BEYAZ)


def komut(cmd, zaman_asimi=60):
    try:
        s = subprocess.run(cmd, shell=True, capture_output=True,
                           text=True, timeout=zaman_asimi)
        return s.returncode == 0, (s.stdout + s.stderr).strip()
    except subprocess.TimeoutExpired:
        return False, "zaman aşımı"
    except Exception as e:
        return False, str(e)


def dosya_oku(yol):
    try:
        with open(yol, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return None


def arac_var(ad):
    return shutil.which(ad) is not None


def root_mu():
    return os.geteuid() == 0


def temizle():
    os.system("clear")


def cubuk(puan, genislik=38):
    dolu = int(puan / 100 * genislik)
    return "█" * dolu + "░" * (genislik - dolu)
