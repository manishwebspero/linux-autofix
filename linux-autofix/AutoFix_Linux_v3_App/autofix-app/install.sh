#!/bin/bash
# ============================================================
#   LINUX AUTO-FIX v3.0 — INSTALLER
#   Run this once to install the app on your Ubuntu system
#   Usage: bash install.sh
# ============================================================

set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; WHITE='\033[1;37m'; NC='\033[0m'

APP_NAME="autofix"
APP_VERSION="3.0"
INSTALL_DIR="$HOME/.local/share/autofix"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

print_header() {
    echo -e "\n${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║   ⚡  Linux Auto-Fix v${APP_VERSION} — Installer          ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}\n"
}

print_ok()   { echo -e "${GREEN}  [✔]  $1${NC}"; }
print_info() { echo -e "${CYAN}  [•]  $1${NC}"; }
print_warn() { echo -e "${YELLOW}  [!]  $1${NC}"; }
print_err()  { echo -e "${RED}  [✘]  $1${NC}"; }
print_step() { echo -e "\n${WHITE}  ──  $1${NC}"; }

# ── Check not root ────────────────────────────────────────────────────────────
if [ "$EUID" -eq 0 ]; then
    print_err "Do NOT run the installer as root. Run as your normal user."
    print_info "Usage: bash install.sh"
    exit 1
fi

print_header

# ── Step 1: Check Ubuntu ──────────────────────────────────────────────────────
print_step "Checking system compatibility"
if ! command -v apt &>/dev/null; then
    print_err "This installer requires Ubuntu/Debian (apt not found)."
    exit 1
fi
print_ok "Ubuntu/Debian detected: $(lsb_release -ds 2>/dev/null || echo 'Linux')"

# ── Step 2: Install dependencies ──────────────────────────────────────────────
print_step "Installing required packages"
PKGS=("python3" "python3-tk" "policykit-1" "lm-sensors" "smartmontools" "ufw" "fail2ban")
MISSING=()
for pkg in "${PKGS[@]}"; do
    if ! dpkg -l "$pkg" &>/dev/null 2>&1; then
        MISSING+=("$pkg")
    fi
done

if [ "${#MISSING[@]}" -gt 0 ]; then
    print_info "Installing: ${MISSING[*]}"
    sudo apt-get update -qq
    sudo apt-get install -y "${MISSING[@]}"
    print_ok "Dependencies installed"
else
    print_ok "All dependencies already installed"
fi

# ── Step 3: Create directories ────────────────────────────────────────────────
print_step "Creating installation directories"
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"
mkdir -p "$HOME/.autofix"
print_ok "Directories created"

# ── Step 4: Copy app files ────────────────────────────────────────────────────
print_step "Installing application files"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/autofix_app.py" "$INSTALL_DIR/autofix_app.py"
chmod +x "$INSTALL_DIR/autofix_app.py"
print_ok "App files copied to $INSTALL_DIR"

# ── Step 5: Create launcher script ────────────────────────────────────────────
print_step "Creating launcher"
cat > "$BIN_DIR/autofix" <<EOF
#!/bin/bash
# Linux Auto-Fix v${APP_VERSION} Launcher
cd "$INSTALL_DIR"
python3 "$INSTALL_DIR/autofix_app.py" "\$@"
EOF
chmod +x "$BIN_DIR/autofix"
print_ok "Launcher created: $BIN_DIR/autofix"

# ── Step 6: Create SVG icon ───────────────────────────────────────────────────
print_step "Creating app icon"
cat > "$ICON_DIR/autofix.svg" <<'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect width="256" height="256" rx="40" fill="#0a0f1a"/>
  <polygon points="128,24 148,100 220,100 162,148 184,224 128,176 72,224 94,148 36,100 108,100"
           fill="none" stroke="#00d4ff" stroke-width="8"/>
  <text x="128" y="140" text-anchor="middle" font-family="monospace"
        font-size="52" font-weight="bold" fill="#00ff88">⚡</text>
</svg>
SVGEOF
print_ok "Icon created"

# ── Step 7: Create .desktop entry ────────────────────────────────────────────
print_step "Creating desktop entry"
cat > "$DESKTOP_DIR/autofix.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Linux Auto-Fix
GenericName=System Optimizer
Comment=One-click system repair, optimization and security for Ubuntu
Exec=$BIN_DIR/autofix
Icon=$ICON_DIR/autofix.svg
Terminal=false
Categories=System;Settings;Utility;
Keywords=fix;repair;optimize;clean;security;performance;
StartupNotify=true
StartupWMClass=autofix_app
EOF
chmod +x "$DESKTOP_DIR/autofix.desktop"

# Also put on Desktop if it exists
if [ -d "$HOME/Desktop" ]; then
    cp "$DESKTOP_DIR/autofix.desktop" "$HOME/Desktop/autofix.desktop"
    chmod +x "$HOME/Desktop/autofix.desktop"
    gio set "$HOME/Desktop/autofix.desktop" metadata::trusted true 2>/dev/null || true
    print_ok "Desktop shortcut created"
fi

# Update icon cache
gtk-update-icon-cache ~/.local/share/icons/hicolor 2>/dev/null || true
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
print_ok "Desktop entry installed"

# ── Step 8: Add to PATH ───────────────────────────────────────────────────────
print_step "Configuring PATH"
SHELL_RC=""
if [ -f "$HOME/.bashrc" ]; then SHELL_RC="$HOME/.bashrc"; fi
if [ -n "$ZSH_VERSION" ] && [ -f "$HOME/.zshrc" ]; then SHELL_RC="$HOME/.zshrc"; fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q 'autofix' "$SHELL_RC" 2>/dev/null; then
        echo -e '\n# Linux Auto-Fix' >> "$SHELL_RC"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        print_ok "Added ~/.local/bin to PATH in $SHELL_RC"
    else
        print_ok "PATH already configured"
    fi
fi

# Add to current session
export PATH="$HOME/.local/bin:$PATH"

# ── Step 9: Create uninstaller ────────────────────────────────────────────────
print_step "Creating uninstaller"
cat > "$INSTALL_DIR/uninstall.sh" <<EOF
#!/bin/bash
echo "Uninstalling Linux Auto-Fix v${APP_VERSION}..."
rm -rf "$INSTALL_DIR"
rm -f  "$BIN_DIR/autofix"
rm -f  "$DESKTOP_DIR/autofix.desktop"
rm -f  "$HOME/Desktop/autofix.desktop"
rm -f  "$ICON_DIR/autofix.svg"
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
echo "✔ Uninstalled. Log file kept at ~/.autofix/autofix.log"
echo "  To remove log: rm -rf ~/.autofix"
EOF
chmod +x "$INSTALL_DIR/uninstall.sh"
print_ok "Uninstaller: $INSTALL_DIR/uninstall.sh"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   ✅  INSTALLATION COMPLETE!                     ║${NC}"
echo -e "${CYAN}╠══════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║                                                  ║${NC}"
echo -e "${CYAN}║  Launch options:                                 ║${NC}"
echo -e "${CYAN}║${GREEN}  • Terminal  :  autofix                          ${CYAN}║${NC}"
echo -e "${CYAN}║${GREEN}  • App Menu  :  Search 'Auto-Fix'                ${CYAN}║${NC}"
echo -e "${CYAN}║${GREEN}  • Desktop   :  Double-click the icon            ${CYAN}║${NC}"
echo -e "${CYAN}║                                                  ║${NC}"
echo -e "${CYAN}║  To uninstall:                                   ║${NC}"
echo -e "${CYAN}║${YELLOW}  bash ~/.local/share/autofix/uninstall.sh       ${CYAN}║${NC}"
echo -e "${CYAN}║                                                  ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# Launch the app now?
read -rp "  Launch Auto-Fix now? (y/n): " LAUNCH
if [[ "$LAUNCH" =~ ^[Yy]$ ]]; then
    python3 "$INSTALL_DIR/autofix_app.py" &
fi
