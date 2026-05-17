#!/bin/bash
# SentinelAI v1.5 Kurulum Betiği
# Yazar: Mehmed Gürbüz (s247003009)

R="\033[0m"
KALIN="\033[1m"
CYAN="\033[96m"
YESIL="\033[92m"
SARI="\033[93m"
KIRMIZI="\033[91m"
GRI="\033[90m"
BEYAZ="\033[97m"

clear
echo -e "${CYAN}${KALIN}"
cat << 'EOF'
 ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗      █████╗ ██╗
 ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     ██╔══██╗██║
 ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ███████║██║
 ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ██╔══██║██║
 ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗██║  ██║██║
 ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝
EOF
echo -e "${R}"
echo -e "  ${GRI}SentinelAI v1.5 Kurulum Betiği  |  Yazar: Mehmed Gürbüz (s247003009)${R}"
echo -e "  ${GRI}──────────────────────────────────────────────────────${R}\n"

KURULUM_DIR="$HOME/sentinelai"
VENV_DIR="$HOME/sentinelai-env"

# ── 1. Python kontrolü ───────────────────────────────────────
echo -e "  ${CYAN}[1/6] Python kontrol ediliyor...${R}"
PYTHON=""
for p in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$p" &>/dev/null; then
        MAJ=$($p -c "import sys; print(sys.version_info.major)" 2>/dev/null)
        MIN=$($p -c "import sys; print(sys.version_info.minor)" 2>/dev/null)
        if [ "$MAJ" -eq 3 ] && [ "$MIN" -ge 10 ]; then
            PYTHON="$p"
            echo -e "  ${YESIL}✅ $($p --version) bulundu.${R}"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "  ${SARI}⚠️  Python 3.10+ bulunamadı, kuruluyor...${R}"
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv python3-full
    PYTHON="python3"
fi

# ── 2. pip kontrolü ──────────────────────────────────────────
echo -e "\n  ${CYAN}[2/6] pip kontrol ediliyor...${R}"
if $PYTHON -m pip --version &>/dev/null; then
    echo -e "  ${YESIL}✅ pip kurulu: $($PYTHON -m pip --version | awk '{print $1, $2}')${R}"
else
    echo -e "  ${SARI}⚠️  pip bulunamadı, kuruluyor...${R}"
    sudo apt install -y python3-pip python3-venv python3-full
    if $PYTHON -m pip --version &>/dev/null; then
        echo -e "  ${YESIL}✅ pip kuruldu.${R}"
    else
        echo -e "  ${KIRMIZI}❌ pip kurulamadı, manuel kurulum gerekli.${R}"
    fi
fi

# ── 3. Google Generative AI (PEP 668 uyumlu) ─────────────────
echo -e "\n  ${CYAN}[3/6] Google Generative AI kütüphanesi...${R}"

if $PYTHON -c "import google.generativeai" &>/dev/null; then
    echo -e "  ${YESIL}✅ google-generativeai zaten kurulu.${R}"
else
    echo -e "  ${GRI}google-generativeai bulunamadı. Kurulum yöntemi seçin:${R}\n"
    echo -e "  ${CYAN}[1]${R} pipx ile kur  ${GRI}(önerilen, sistemi etkilemez)${R}"
    echo -e "  ${CYAN}[2]${R} venv oluştur  ${GRI}(izole sanal ortam)${R}"
    echo -e "  ${CYAN}[3]${R} Sistem geneli ${GRI}(--break-system-packages, riskli)${R}"
    echo -e "  ${CYAN}[4]${R} Atla         ${GRI}(AI modülü devre dışı kalır)${R}\n"
    read -p "$(echo -e "  ${SARI}Seçiminiz [1-4]: ${R}")" PIP_SEC

    case "$PIP_SEC" in
        1)
            if ! command -v pipx &>/dev/null; then
                echo -e "  ${GRI}pipx kuruluyor...${R}"
                sudo apt install -y pipx
                pipx ensurepath
            fi
            pipx install google-generativeai
            if [ $? -eq 0 ]; then
                echo -e "  ${YESIL}✅ pipx ile kuruldu. Yeni terminal açmanız gerekebilir.${R}"
            else
                echo -e "  ${KIRMIZI}❌ pipx kurulumu başarısız.${R}"
            fi
            ;;
        2)
            echo -e "  ${GRI}Sanal ortam oluşturuluyor: $VENV_DIR${R}"
            $PYTHON -m venv "$VENV_DIR"
            "$VENV_DIR/bin/pip" install google-generativeai
            if [ $? -eq 0 ]; then
                echo -e "  ${YESIL}✅ venv içine kuruldu.${R}"
                echo -e "  ${SARI}⚠️  SentinelAI bu venv içinden çalıştırılmalı:${R}"
                echo -e "  ${CYAN}    $VENV_DIR/bin/python $KURULUM_DIR/sentinelai.py${R}"
                PYTHON="$VENV_DIR/bin/python"
            else
                echo -e "  ${KIRMIZI}❌ venv kurulumu başarısız.${R}"
            fi
            ;;
        3)
            echo -e "  ${SARI}⚠️  --break-system-packages ile zorla kuruluyor...${R}"
            $PYTHON -m pip install --user --break-system-packages google-generativeai
            ;;
        4)
            echo -e "  ${GRI}⏭  Atlandı. AI modülü çalışmayacak.${R}"
            ;;
        *)
            echo -e "  ${SARI}Geçersiz seçim, atlandı.${R}"
            ;;
    esac
fi

# ── 4. Proje dosyaları ───────────────────────────────────────
echo -e "\n  ${CYAN}[4/6] Proje dosyaları indiriliyor...${R}"

if ! command -v git &>/dev/null; then
    sudo apt install -y git
fi

if [ -d "$KURULUM_DIR" ]; then
    echo -e "  ${GRI}Mevcut kurulum güncelleniyor...${R}"
    cd "$KURULUM_DIR" && git pull
else
    git clone https://github.com/mehmedgur/sentinelaiv1.5.git "$KURULUM_DIR"
    if [ $? -ne 0 ]; then
        echo -e "  ${KIRMIZI}❌ İndirme başarısız.${R}"
        exit 1
    fi
fi
echo -e "  ${YESIL}✅ Dosyalar hazır: $KURULUM_DIR${R}"

# ── 5. Güvenlik araçları ─────────────────────────────────────
echo -e "\n  ${CYAN}[5/6] Güvenlik Araçları${R}"

arac_kur() {
    local ARAC=$1
    local PAKET=$2
    local ACIKLAMA=$3

    if command -v "$ARAC" &>/dev/null; then
        echo -e "  ${YESIL}✅ $ARAC zaten kurulu.${R}"
        return
    fi

    echo -e "  ${BEYAZ}$ARAC — $ACIKLAMA${R}"
    read -p "$(echo -e "  ${SARI}Kurulsun mu? [E/H]: ${R}")" CEVAP
    if [[ "$CEVAP" =~ ^[Ee]$ ]]; then
        sudo apt install -y "$PAKET"
        if [ $? -ne 0 ]; then
            echo -e "  ${SARI}⚠️  $PAKET kurulamadı, atlanıyor.${R}"
        fi
    else
        echo -e "  ${GRI}⏭  Atlandı.${R}"
    fi
    echo
}

arac_kur "nmap"       "nmap"       "Port tarama"
arac_kur "nikto"      "nikto"      "Web tarayıcı"
arac_kur "lynis"      "lynis"      "Sistem denetçisi"
arac_kur "rkhunter"   "rkhunter"   "Rootkit tarayıcı"
arac_kur "chkrootkit" "chkrootkit" "Rootkit tarayıcı"
arac_kur "arp-scan"   "arp-scan"   "Ağ keşfi"
arac_kur "ufw"        "ufw"        "Güvenlik duvarı"
arac_kur "nft"        "nftables"   "Gelişmiş güvenlik duvarı"
arac_kur "rsyslog"    "rsyslog"    "Sistem loglama"

# ── 6. İzinler ───────────────────────────────────────────────
echo -e "  ${CYAN}[6/6] İzinler ve klasörler ayarlanıyor...${R}"

# Proje dizini ve dosyaları
sudo chmod -R 755 "$KURULUM_DIR"
find "$KURULUM_DIR" -name "*.py" -exec chmod 644 {} \;
chmod +x "$KURULUM_DIR/sentinelai.py"
echo -e "  ${YESIL}✅ Proje dosya izinleri ayarlandı.${R}"

# Log ve data dizinleri root korumalı
sudo mkdir -p /var/log/sentinelai
sudo mkdir -p /var/lib/sentinelai
sudo chown root:root /var/log/sentinelai
sudo chown root:root /var/lib/sentinelai
sudo chmod 700 /var/log/sentinelai
sudo chmod 700 /var/lib/sentinelai
echo -e "  ${YESIL}✅ /var/log/sentinelai ve /var/lib/sentinelai root korumalı.${R}"

# Config dosyası izni
if [ -f "$HOME/.sentinelai.conf" ]; then
    chmod 600 "$HOME/.sentinelai.conf"
    echo -e "  ${YESIL}✅ ~/.sentinelai.conf güvenliği sağlandı.${R}"
fi

# Alias
ALIAS_SATIR="alias sentinelai='$PYTHON $KURULUM_DIR/sentinelai.py'"
if ! grep -q "alias sentinelai=" "$HOME/.bashrc" 2>/dev/null; then
    echo "" >> "$HOME/.bashrc"
    echo "# SentinelAI v1.5" >> "$HOME/.bashrc"
    echo "$ALIAS_SATIR" >> "$HOME/.bashrc"
    echo -e "  ${YESIL}✅ 'sentinelai' komutu eklendi.${R}"
fi

# ── Özet ─────────────────────────────────────────────────────
echo
echo -e "  ${GRI}──────────────────────────────────────────────────────${R}"
echo -e "  ${YESIL}${KALIN}  Kurulum tamamlandı!${R}"
echo -e "  ${GRI}──────────────────────────────────────────────────────${R}"
echo
echo -e "  ${BEYAZ}Çalıştırmak için:${R}"
echo -e "  ${CYAN}${KALIN}  cd $KURULUM_DIR && $PYTHON sentinelai.py${R}"
echo -e "  ${GRI}  veya yeni terminal açıp: ${CYAN}sentinelai${R}"
echo
echo -e "  ${SARI}⚠️  Bazı analizler sudo gerektirebilir.${R}"
echo

read -p "$(echo -e "  ${CYAN}Şimdi başlatılsın mı? [E/H]: ${R}")" BASLAT
if [[ "$BASLAT" =~ ^[Ee]$ ]]; then
    cd "$KURULUM_DIR"
    exec "$PYTHON" sentinelai.py
fi
