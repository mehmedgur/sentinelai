#!/bin/bash
# SentinelAI v1.2 Kurulum Betiği
# Yazar: s247003009

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
echo -e "  ${GRI}SentinelAI v1.2 Kurulum Betiği  |  Yazar: s247003009${R}"
echo -e "  ${GRI}──────────────────────────────────────────────────────${R}\n"

KURULUM_DIR="$HOME/sentinelai"

echo -e "  ${CYAN}[1/4] Python kontrol ediliyor...${R}"
PYTHON=""
for p in python3.12 python3.11 python3.10 python3; do
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
    sudo apt update -qq && sudo apt install -y python3 &>/dev/null
    PYTHON="python3"
    echo -e "  ${YESIL}✅ Python kuruldu.${R}"
fi

echo -e "\n  ${CYAN}[2/4] Proje dosyaları indiriliyor...${R}"

if ! command -v git &>/dev/null; then
    echo -e "  ${GRI}git bulunamadı, kuruluyor...${R}"
    sudo apt install -y git &>/dev/null
fi

if [ -d "$KURULUM_DIR" ]; then
    echo -e "  ${GRI}Mevcut kurulum güncelleniyor...${R}"
    cd "$KURULUM_DIR" && git pull -q
    echo -e "  ${YESIL}✅ Güncellendi.${R}"
else
    git clone -q https://github.com/mehmedgur/sentinelai.git "$KURULUM_DIR"
    if [ $? -eq 0 ]; then
        echo -e "  ${YESIL}✅ Dosyalar indirildi: $KURULUM_DIR${R}"
    else
        echo -e "  ${KIRMIZI}❌ İndirme başarısız. İnternet bağlantınızı kontrol edin.${R}"
        exit 1
    fi
fi

echo -e "\n  ${CYAN}[3/4] Güvenlik Araçları${R}"
echo -e "  ${GRI}Her araç için kurulsun mu diye sorulacak.${R}\n"

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
        echo -e "  ${GRI}Kuruluyor...${R}"
        sudo apt install -y "$PAKET" &>/dev/null
        if command -v "$ARAC" &>/dev/null; then
            echo -e "  ${YESIL}✅ $ARAC kuruldu.${R}"
        else
            echo -e "  ${SARI}⚠️  $ARAC kurulamadı, atlanıyor.${R}"
        fi
    else
        echo -e "  ${GRI}⏭  $ARAC atlandı.${R}"
    fi
    echo
}

arac_kur "nmap"       "nmap"       "Port tarama aracı"
arac_kur "nikto"      "nikto"      "Web sunucu güvenlik tarayıcısı"
arac_kur "lynis"      "lynis"      "Sistem sertleştirme denetçisi"
arac_kur "rkhunter"   "rkhunter"   "Rootkit tarayıcısı"
arac_kur "chkrootkit" "chkrootkit" "Rootkit tarayıcısı (alternatif)"
arac_kur "arp-scan"   "arp-scan"   "Yerel ağ cihaz keşfi"

echo -e "  ${CYAN}[4/4] Ayarlar yapılandırılıyor...${R}"

chmod +x "$KURULUM_DIR/sentinelai.py"
echo -e "  ${YESIL}✅ Çalıştırma izni verildi.${R}"

ALIAS_SATIR="alias sentinelai='$PYTHON $KURULUM_DIR/sentinelai.py'"
if ! grep -q "alias sentinelai=" "$HOME/.bashrc" 2>/dev/null; then
    echo "" >> "$HOME/.bashrc"
    echo "# SentinelAI" >> "$HOME/.bashrc"
    echo "$ALIAS_SATIR" >> "$HOME/.bashrc"
    echo -e "  ${YESIL}✅ 'sentinelai' komutu eklendi.${R}"
else
    echo -e "  ${YESIL}✅ Alias zaten mevcut.${R}"
fi

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
echo -e "  ${GRI}──────────────────────────────────────────────────────${R}"
echo

read -p "$(echo -e "  ${CYAN}Şimdi başlatılsın mı? [E/H]: ${R}")" BASLAT
if [[ "$BASLAT" =~ ^[Ee]$ ]]; then
    cd "$KURULUM_DIR"
    exec "$PYTHON" sentinelai.py
fi
