#!/usr/bin/env python3
"""
SentinelAI v1.2 —Giriş Noktası
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sentinelai.onboarding import baslat
from sentinelai.menu       import Menu


def main():
    try:
        mod, hedef, api_key = baslat()
        Menu(mod=mod, hedef=hedef, api_key=api_key).baslat()
    except KeyboardInterrupt:
        print("\n\n  \033[90mCtrl+C algılandı. Çıkılıyor...\033[0m\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
