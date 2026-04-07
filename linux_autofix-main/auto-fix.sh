#!/bin/bash

# ============================================================
#   LINUX AUTO-FIX v3.0 GUI PRO MAX
# ============================================================

# --- Check dependencies ---
for pkg in zenity lm-sensors; do
    if ! command -v $pkg &>/dev/null; then
        sudo apt install -y $pkg
    fi
done

LOG="$HOME/autofix_v3.log"

log() {
    echo "$(date '+%H:%M:%S') - $1" >> $LOG
}

# ============================================================
# FUNCTIONS
# ============================================================

auto_fix() {
    zenity --info --title="Auto Fix" --text="Running full system optimization..."

    sudo apt update -y && sudo apt upgrade -y
    sudo apt autoremove -y && sudo apt autoclean -y
    sudo systemctl restart NetworkManager

    sync; echo 3 | sudo tee /proc/sys/vm/drop_caches

    log "Auto Fix completed"
    zenity --info --text="✅ Auto Fix Completed!"
}

deep_clean() {
    zenity --info --text="Cleaning system..."

    sudo rm -rf /tmp/*
    journalctl --vacuum-time=3d

    log "Deep Clean done"
    zenity --info --text="🧹 Deep Clean Done!"
}

game_boost() {
    zenity --info --text="Activating Game Mode..."

    pkill -f chrome
    pkill -f firefox
    pkill -f snapd

    sudo systemctl stop bluetooth

    log "Game Boost activated"
    zenity --info --text="🎮 Game Mode ON!"
}

security_scan() {
    zenity --info --text="Running security scan..."

    sudo apt install -y rkhunter chkrootkit
    sudo rkhunter --check --sk

    log "Security scan complete"
    zenity --info --text="🔐 Scan Completed!"
}

system_monitor() {
    zenity --info --text="$(top -b -n1 | head -n 15)"
}

disk_optimize() {
    TYPE=$(lsblk -d -o rota | tail -n1)
    if [ "$TYPE" == "0" ]; then
        sudo fstrim -av
        zenity --info --text="SSD optimized (TRIM done)"
    else
        zenity --info --text="HDD detected - no TRIM needed"
    fi
}

show_menu() {
    while true; do
        choice=$(zenity --list \
        --title="🚀 Linux Auto-Fix v3 PRO MAX" \
        --column="Select Option" \
        "1. Full Auto Fix" \
        "2. Deep Clean" \
        "3. Game Boost Mode 🎮" \
        "4. Security Scan 🔐" \
        "5. System Monitor 📊" \
        "6. Disk Optimize 💽" \
        "7. Exit")

        case $choice in
            "1. Full Auto Fix") auto_fix ;;
            "2. Deep Clean") deep_clean ;;
            "3. Game Boost Mode 🎮") game_boost ;;
            "4. Security Scan 🔐") security_scan ;;
            "5. System Monitor 📊") system_monitor ;;
            "6. Disk Optimize 💽") disk_optimize ;;
            "7. Exit") exit ;;
        esac
    done
}

# ============================================================
# START
# ============================================================

show_menu
