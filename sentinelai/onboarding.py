"""
SentinelAI v1.2 - Karşılama ve Kurulum Ekranı
Yazar: s247003009
"""

import os
import sys
import time
import configparser
from .utils import yaz, temizle, R

CONF_YOL = os.path.expanduser("~/.sentinelai.conf")

BASLIK = f"""
{R.CYAN}{R.KALIN} ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗      █████╗ ██╗
 ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     ██╔══██╗██║
 ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ███████║██║
 ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ██╔══██║██║
 ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗██║  ██║██║
 ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝{R.SIFIRLA}"""

BILGILENDIRME = f"""
{R.GRI}  {'─' * 60}{R.SIFIRLA}
{R.BEYAZ}  SentinelAI — Linux Sistem Güvenlik Analiz Aracı{R.SIFIRLA}
{R.GRI}  Versiyon: {R.YESIL}v1.2{R.SIFIRLA}   {R.GRI}Yapımcı: {R.CYAN}s247003009{R.SIFIRLA}
{R.GRI}  {'─' * 60}{R.SIFIRLA}

{R.SARI}  ⚠️  YASAL UYARI{R.SIFIRLA}
{R.GRI}  Bu araç yalnızca etik ve eğitim amaçlıdır.
  Gerçek saldırı veya sömürü gerçekleştirmez.
  Yalnızca yetkili olduğunuz sistemlerde kullanın.
  Yetkisiz kullanımdan doğan sorumluluk kullanıcıya aittir.{R.SIFIRLA}

{R.GRI}  {'─' * 60}{R.SIFIRLA}
"""


def conf_oku():
    conf = configparser.ConfigParser()
    if os.path.exists(CONF_YOL):
        conf.read(CONF_YOL)
    return conf


def conf_kaydet(anahtar, deger, bolum="sentinelai"):
    conf = conf_oku()
    if bolum not in conf:
        conf[bolum] = {}
    conf[bolum][anahtar] = deger
    with open(CONF_YOL, "w") as f:
        conf.write(f)


def api_key_al():
    conf = conf_oku()
    kayitli = conf.get("sentinelai", "gemini_api_key", fallback=None)

    if kayitli:
        yaz(f"  ✅ Gemini API anahtarı kayıtlı.", R.YESIL)
        return kayitli

    yaz("\n  🔑 Gemini API Anahtarı", R.EFLATUN)
    yaz("  AI yorumu için Google AI Studio API anahtarı gerekli.", R.GRI)
    yaz("  Boş bırakırsanız AI analizi devre dışı kalır.\n", R.GRI)

    key = input(f"  {R.EFLATUN}API Anahtarı (opsiyonel):{R.SIFIRLA} ").strip()

    if key:
        kaydet = input(f"  {R.GRI}Kaydedilsin mi? [E/H]:{R.SIFIRLA} ").strip().lower()
        if kaydet in ("e", "evet"):
            conf_kaydet("gemini_api_key", key)
            yaz("  ✅ ~/.sentinelai.conf dosyasına kaydedildi.", R.YESIL)

    return key or None


def mod_sec():
    yaz("\n  Bu aracı nerede kullanacaksınız?\n", R.BEYAZ)
    yaz(f"  {R.MAVI}[1]{R.SIFIRLA}  💻  Kendi bilgisayarım  {R.GRI}(localhost){R.SIFIRLA}")
    yaz(f"  {R.MAVI}[2]{R.SIFIRLA}  🖥️   Sunucu              {R.GRI}(uzak hedef){R.SIFIRLA}")

    while True:
        secim = input(f"\n  {R.GRI}Seçiminiz [1/2]:{R.SIFIRLA} ").strip()
        if secim == "1":
            return "lokal", "localhost"
        if secim == "2":
            hedef = input(f"  {R.GRI}Hedef IP / hostname:{R.SIFIRLA} ").strip()
            if hedef:
                return "sunucu", hedef
            yaz("  Hedef boş bırakılamaz.", R.SARI)


def baslat():
    """
    Karşılama ekranını göster, mod ve API key al.
    Döndürür: (mod, hedef, api_key)
    """
    temizle()
    print(BASLIK)
    print(BILGILENDIRME)

    mod, hedef = mod_sec()
    api_key    = api_key_al()

    yaz(f"\n  {R.GRI}{'─' * 60}{R.SIFIRLA}")
    yaz(f"  Mod    : {R.SARI}{mod.capitalize()}{R.SIFIRLA}")
    yaz(f"  Hedef  : {R.BEYAZ}{hedef}{R.SIFIRLA}")
    yaz(f"  AI     : {R.YESIL if api_key else R.GRI}{'Aktif' if api_key else 'Devre Dışı'}{R.SIFIRLA}")
    yaz(f"  {R.GRI}{'─' * 60}{R.SIFIRLA}")

    input(f"\n  {R.GRI}Devam etmek için Enter'a basın...{R.SIFIRLA}")

    return mod, hedef, api_key
