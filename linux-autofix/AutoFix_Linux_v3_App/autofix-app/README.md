# ⚡ Linux Auto-Fix v3.0 PRO MAX

A proper Ubuntu desktop application for one-click system repair,
optimization, deep cleaning, security scanning, and game boosting.

---

## 📦 WHAT'S INCLUDED

```
autofix-app/
├── autofix_app.py    ← Main GUI application (Python 3 + tkinter)
├── install.sh        ← One-click installer
└── README.md         ← This file
```

---

## 🚀 HOW TO INSTALL (One Command)

```bash
bash install.sh
```

That's it! The installer will:
- Check your Ubuntu version
- Install all required packages (python3-tk, lm-sensors, ufw, etc.)
- Copy the app to ~/.local/share/autofix/
- Create a launcher command: `autofix`
- Add an icon to your App Menu
- Create a Desktop shortcut

---

## ▶️ HOW TO LAUNCH

After installing, you can open it 3 ways:

| Method      | How                                |
|-------------|------------------------------------|
| Terminal    | Type: `autofix`                    |
| App Menu    | Search "Auto-Fix" or "Linux Fix"   |
| Desktop     | Double-click the ⚡ icon            |

---

## 🔧 FEATURES

### 🏠 Dashboard
- Live CPU, RAM, Disk and Uptime stats
- Quick action buttons for all features
- Recent activity log

### 🔧 Full Auto Fix
- apt update + upgrade
- Remove orphaned packages
- Clean APT cache
- Clear /tmp files
- Drop memory caches
- Restart NetworkManager
- Flush DNS cache
- Trim journal logs (7 days)
- Fix broken packages

### 🧹 Deep Clean
- /tmp directory
- Thumbnail cache
- Firefox, Chrome, Chromium caches
- APT package cache
- Old kernel packages
- Snap revision cache
- systemd journal (3 days)
- Orphaned dpkg config files
- Shows how much space was freed

### 🎮 Game Boost Mode
- CPU governor → performance
- Drops memory caches
- Sets vm.swappiness = 5
- Stops Bluetooth, CUPS, tracker, avahi
- One-click Restore Normal Mode

### 🔐 Security Scan
- UFW firewall check + auto-enable
- SSH root login check + auto-fix
- World-writable files in /etc + auto-fix
- Failed login attempts
- Listening ports audit
- SUID files check
- rkhunter rootkit scan (if installed)
- Pending security updates

### 📊 System Info
- OS, Kernel, Arch
- CPU model, cores, usage, governor
- RAM total/used/free, Swap
- Disk usage and type (HDD/SSD)
- Network interfaces and DNS
- GPU info + NVIDIA stats
- Top CPU processes
- Failed services

### 💽 Disk Tools
- SMART health check (all drives)
- SSD TRIM
- Disk usage (largest directories)
- Schedule fsck for next boot

### 📋 Fix Log
- Full timestamped log of every action
- Color-coded (green=fixed, yellow=skip, red=error)
- Clear log button

---

## 📋 REQUIREMENTS

| Requirement   | Version          |
|---------------|------------------|
| Ubuntu        | 20.04+ / 22.04+  |
| Python        | 3.8+             |
| python3-tk    | (auto-installed)  |

---

## 🔗 HOW TO SHARE

To share with a friend:

**Option A — ZIP and send:**
```bash
zip -r AutoFix_v3.zip autofix-app/
```
They just run: `bash install.sh`

**Option B — Send via any method:**
- WhatsApp / Telegram (as .zip)
- Google Drive / Dropbox link
- USB drive
- GitHub repo

---

## 🗑️ HOW TO UNINSTALL

```bash
bash ~/.local/share/autofix/uninstall.sh
```

---

## 📝 LOGS

All actions are logged to:
```
~/.autofix/autofix.log
```

---

Made with ❤ for Linux users
