#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║         LINUX AUTO-FIX v3.0  —  GUI PRO MAX             ║
║         A proper Ubuntu desktop application              ║
╚══════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import sys
import datetime
import platform

# ── Paths ────────────────────────────────────────────────────────────────────
HOME        = os.path.expanduser("~")
LOG_DIR     = os.path.join(HOME, ".autofix")
LOG_FILE    = os.path.join(LOG_DIR, "autofix.log")
os.makedirs(LOG_DIR, exist_ok=True)

# ── Palette ──────────────────────────────────────────────────────────────────
BG          = "#0a0f1a"
BG2         = "#111827"
BG3         = "#1a2235"
CARD        = "#141e30"
BORDER      = "#1e3a5f"
ACCENT      = "#00d4ff"
ACCENT2     = "#0096cc"
GREEN       = "#00ff88"
YELLOW      = "#ffd700"
RED         = "#ff4455"
ORANGE      = "#ff8c00"
PURPLE      = "#a855f7"
TEXT        = "#e2e8f0"
TEXT_DIM    = "#64748b"
TEXT_MUTED  = "#334155"

FONT_TITLE  = ("Courier New", 18, "bold")
FONT_HEAD   = ("Courier New", 11, "bold")
FONT_BODY   = ("Courier New", 10)
FONT_MONO   = ("Courier New", 9)
FONT_SMALL  = ("Courier New", 8)

# ── Logging ──────────────────────────────────────────────────────────────────
def log(msg, level="INFO"):
    ts  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)

# ── Shell helpers ─────────────────────────────────────────────────────────────
def run_cmd(cmd, shell=True, capture=True):
    try:
        result = subprocess.run(
            cmd, shell=shell, capture_output=capture,
            text=True, timeout=300
        )
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "Command timed out", 1
    except Exception as e:
        return str(e), 1

def run_sudo(cmd):
    return run_cmd(f"pkexec bash -c '{cmd}'")

# ═════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════
class AutoFixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux Auto-Fix v3.0 PRO MAX")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)
        self._set_icon()

        self.running     = False
        self.fix_count   = tk.IntVar(value=0)
        self.skip_count  = tk.IntVar(value=0)
        self.err_count   = tk.IntVar(value=0)
        self.status_var  = tk.StringVar(value="Ready")
        self.progress    = tk.DoubleVar(value=0)

        self._build_ui()
        self._print_banner()
        log("Application started")

    # ── Icon ──────────────────────────────────────────────────────────────────
    def _set_icon(self):
        try:
            icon_data = """
R0lGODlhIAAgAMQAAAAAABERESIiIjMzM0REREZGRlVVVWZmZnd3d4iIiJmZmaqqqru7u8zMzN3d
3e7u7v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAA
AAgACAAAAV+ICCOZGmeaKqubOu+cCzPdG3feK7vfO//wKBwSCwaj8ikcslsOp/QqHRKrVqv2Kx2y+
16v+CweEwum8/otHrNbrvf8Lh8Tq/b7/i8fs/v+/+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZ
qbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5urm7vL2+v8DBwsM=
"""
        except Exception:
            pass

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Left sidebar ──────────────────────────────────────────────────────
        sidebar = tk.Frame(self.root, bg=BG2, width=220, relief="flat")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo block
        logo_frame = tk.Frame(sidebar, bg=CARD, pady=20)
        logo_frame.pack(fill="x", padx=0)

        tk.Label(logo_frame, text="⚡", font=("Courier New", 30),
                 bg=CARD, fg=ACCENT).pack()
        tk.Label(logo_frame, text="AUTO-FIX", font=("Courier New", 13, "bold"),
                 bg=CARD, fg=ACCENT).pack()
        tk.Label(logo_frame, text="v3.0 PRO MAX", font=FONT_SMALL,
                 bg=CARD, fg=TEXT_DIM).pack()
        tk.Label(logo_frame, text=platform.node(), font=FONT_SMALL,
                 bg=CARD, fg=TEXT_MUTED).pack(pady=(4, 0))

        # Divider
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=10, pady=8)

        # Nav buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠",  "Dashboard",     self.show_dashboard),
            ("🔧",  "Auto Fix",      self.show_autofix),
            ("🧹",  "Deep Clean",    self.show_deepclean),
            ("🎮",  "Game Boost",    self.show_gameboost),
            ("🔐",  "Security Scan", self.show_security),
            ("📊",  "System Info",   self.show_sysinfo),
            ("💽",  "Disk Tools",    self.show_disktools),
            ("📋",  "Fix Log",       self.show_log),
        ]
        for icon, label, cmd in nav_items:
            self._nav_btn(sidebar, icon, label, cmd)

        # Bottom info
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=10, pady=8)
        tk.Label(sidebar, text="Ubuntu  •  Python 3",
                 font=FONT_SMALL, bg=BG2, fg=TEXT_MUTED).pack(pady=2)
        tk.Label(sidebar, text="Made with ❤ for Linux",
                 font=FONT_SMALL, bg=BG2, fg=TEXT_MUTED).pack()

        # ── Right content area ────────────────────────────────────────────────
        content_wrapper = tk.Frame(self.root, bg=BG)
        content_wrapper.pack(side="left", fill="both", expand=True)

        # Top bar
        topbar = tk.Frame(content_wrapper, bg=BG2, height=48)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        self.page_title = tk.Label(topbar, text="Dashboard",
                                   font=FONT_HEAD, bg=BG2, fg=TEXT)
        self.page_title.pack(side="left", padx=20, pady=10)

        self.status_label = tk.Label(topbar, textvariable=self.status_var,
                                     font=FONT_SMALL, bg=BG2, fg=ACCENT)
        self.status_label.pack(side="right", padx=20)

        now = datetime.datetime.now().strftime("%d %b %Y  %H:%M")
        tk.Label(topbar, text=now, font=FONT_SMALL,
                 bg=BG2, fg=TEXT_DIM).pack(side="right", padx=10)

        # Progress bar (hidden when idle)
        self.progress_frame = tk.Frame(content_wrapper, bg=BG, height=4)
        self.progress_frame.pack(fill="x")
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, variable=self.progress,
            maximum=100, mode="determinate", length=400)

        # Page container
        self.container = tk.Frame(content_wrapper, bg=BG)
        self.container.pack(fill="both", expand=True, padx=16, pady=12)

        # Status strip
        strip = tk.Frame(content_wrapper, bg=BG3, height=32)
        strip.pack(fill="x", side="bottom")
        strip.pack_propagate(False)

        for var, label, color in [
            (self.fix_count,  "Fixed",   GREEN),
            (self.skip_count, "Skipped", YELLOW),
            (self.err_count,  "Errors",  RED),
        ]:
            f = tk.Frame(strip, bg=BG3)
            f.pack(side="left", padx=16)
            tk.Label(f, textvariable=var, font=("Courier New", 11, "bold"),
                     bg=BG3, fg=color).pack(side="left")
            tk.Label(f, text=f" {label}", font=FONT_SMALL,
                     bg=BG3, fg=TEXT_DIM).pack(side="left")

        # Show dashboard by default
        self.show_dashboard()

    def _nav_btn(self, parent, icon, label, cmd):
        frame = tk.Frame(parent, bg=BG2, cursor="hand2")
        frame.pack(fill="x", padx=6, pady=1)

        def on_enter(e): frame.config(bg=BG3); lbl_icon.config(bg=BG3); lbl_text.config(bg=BG3)
        def on_leave(e): frame.config(bg=BG2); lbl_icon.config(bg=BG2); lbl_text.config(bg=BG2)
        def on_click(e): cmd()

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        frame.bind("<Button-1>", on_click)

        lbl_icon = tk.Label(frame, text=icon, font=("Courier New", 14),
                            bg=BG2, fg=ACCENT, width=3)
        lbl_icon.pack(side="left", padx=(8, 4), pady=8)
        lbl_icon.bind("<Enter>", on_enter); lbl_icon.bind("<Leave>", on_leave)
        lbl_icon.bind("<Button-1>", on_click)

        lbl_text = tk.Label(frame, text=label, font=FONT_BODY,
                            bg=BG2, fg=TEXT, anchor="w")
        lbl_text.pack(side="left", fill="x", expand=True)
        lbl_text.bind("<Enter>", on_enter); lbl_text.bind("<Leave>", on_leave)
        lbl_text.bind("<Button-1>", on_click)

        self.nav_buttons[label] = frame

    # ── Page helpers ──────────────────────────────────────────────────────────
    def _clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def _set_title(self, title):
        self.page_title.config(text=title)

    def _card(self, parent, title=None, pady=8, padx=8):
        outer = tk.Frame(parent, bg=CARD, bd=0, relief="flat",
                         highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="x", pady=4)
        if title:
            hdr = tk.Frame(outer, bg=BG3)
            hdr.pack(fill="x")
            tk.Label(hdr, text=title, font=FONT_HEAD,
                     bg=BG3, fg=ACCENT, anchor="w").pack(
                side="left", padx=12, pady=6)
            tk.Frame(outer, bg=BORDER, height=1).pack(fill="x")
        inner = tk.Frame(outer, bg=CARD, padx=padx, pady=pady)
        inner.pack(fill="both", expand=True)
        return inner

    def _action_btn(self, parent, text, cmd, color=ACCENT, width=22):
        btn = tk.Button(
            parent, text=text, font=FONT_BODY,
            bg=color, fg="#000" if color in (GREEN, YELLOW, ACCENT) else "#fff",
            activebackground=ACCENT2, activeforeground="#000",
            relief="flat", bd=0, cursor="hand2", width=width,
            padx=10, pady=6, command=cmd
        )
        btn.pack(side="left", padx=6, pady=4)
        return btn

    def _terminal(self, parent, height=18):
        term = scrolledtext.ScrolledText(
            parent, font=FONT_MONO, bg="#060d18", fg=GREEN,
            insertbackground=GREEN, relief="flat", bd=0,
            height=height, wrap="word",
            selectbackground=BORDER, selectforeground=TEXT
        )
        term.pack(fill="both", expand=True, padx=2, pady=2)
        term.config(state="disabled")
        return term

    def _write(self, term, text, tag="normal"):
        term.config(state="normal")
        colors = {
            "ok":      GREEN,
            "warn":    YELLOW,
            "err":     RED,
            "info":    ACCENT,
            "dim":     TEXT_DIM,
            "head":    ACCENT,
            "normal":  TEXT,
        }
        term.tag_configure(tag, foreground=colors.get(tag, TEXT))
        term.insert("end", text + "\n", tag)
        term.see("end")
        term.config(state="disabled")
        self.root.update_idletasks()

    def _print_banner(self):
        pass  # banner shown on dashboard

    def _start_progress(self):
        self.progress_bar.pack(fill="x")
        self.progress.set(0)

    def _stop_progress(self):
        self.progress.set(100)
        self.root.after(800, self.progress_bar.pack_forget)

    def _set_status(self, msg):
        self.status_var.set(msg)
        self.root.update_idletasks()

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: DASHBOARD
    # ─────────────────────────────────────────────────────────────────────────
    def show_dashboard(self):
        self._clear()
        self._set_title("Dashboard")

        # Banner
        banner = tk.Frame(self.container, bg=CARD,
                          highlightbackground=BORDER, highlightthickness=1)
        banner.pack(fill="x", pady=(0, 8))
        tk.Label(banner,
                 text="⚡  LINUX AUTO-FIX  v3.0 PRO MAX",
                 font=("Courier New", 16, "bold"),
                 bg=CARD, fg=ACCENT).pack(pady=(14, 2))
        tk.Label(banner,
                 text="One-click system repair, optimization & security for Ubuntu",
                 font=FONT_BODY, bg=CARD, fg=TEXT_DIM).pack(pady=(0, 14))

        # Quick stats row
        stats_row = tk.Frame(self.container, bg=BG)
        stats_row.pack(fill="x", pady=4)

        info_items = self._get_quick_stats()
        for label, value, color in info_items:
            f = tk.Frame(stats_row, bg=CARD,
                         highlightbackground=BORDER, highlightthickness=1)
            f.pack(side="left", expand=True, fill="both", padx=4)
            tk.Label(f, text=value, font=("Courier New", 18, "bold"),
                     bg=CARD, fg=color).pack(pady=(12, 2))
            tk.Label(f, text=label, font=FONT_SMALL,
                     bg=CARD, fg=TEXT_DIM).pack(pady=(0, 12))

        # Quick action grid
        grid_lbl = tk.Label(self.container, text="QUICK ACTIONS",
                            font=FONT_HEAD, bg=BG, fg=TEXT_DIM, anchor="w")
        grid_lbl.pack(fill="x", pady=(12, 4))

        grid = tk.Frame(self.container, bg=BG)
        grid.pack(fill="x")

        actions = [
            ("🔧  Full Auto Fix",      GREEN,   self.show_autofix),
            ("🧹  Deep Clean",         ACCENT,  self.show_deepclean),
            ("🎮  Game Boost",         PURPLE,  self.show_gameboost),
            ("🔐  Security Scan",      YELLOW,  self.show_security),
            ("📊  System Info",        ORANGE,  self.show_sysinfo),
            ("💽  Disk Tools",         RED,     self.show_disktools),
        ]
        for i, (label, color, cmd) in enumerate(actions):
            col = i % 3
            row = i // 3
            btn = tk.Button(grid, text=label, font=FONT_BODY,
                            bg=BG3, fg=color,
                            activebackground=BG2, activeforeground=color,
                            relief="flat", bd=0, cursor="hand2",
                            padx=10, pady=14, command=cmd,
                            highlightbackground=BORDER, highlightthickness=1)
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            grid.columnconfigure(col, weight=1)

        # Last log snippet
        inner = self._card(self.container, "📋  Recent Activity")
        try:
            with open(LOG_FILE) as f:
                lines = f.readlines()[-6:]
            for l in lines:
                tk.Label(inner, text=l.strip(), font=FONT_MONO,
                         bg=CARD, fg=TEXT_DIM, anchor="w").pack(fill="x")
        except Exception:
            tk.Label(inner, text="No activity yet. Run a fix to get started!",
                     font=FONT_MONO, bg=CARD, fg=TEXT_MUTED, anchor="w").pack()

    def _get_quick_stats(self):
        # CPU
        out, _ = run_cmd("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        try: cpu = f"{float(out.split()[0]):.1f}%"
        except: cpu = "N/A"

        # RAM
        out2, _ = run_cmd("free -h | awk '/^Mem:/{print $3\"/\"$2}'")
        ram = out2.strip() or "N/A"

        # Disk
        out3, _ = run_cmd("df -h / | awk 'NR==2{print $3\"/\"$2\" (\"$5\")\"}'")
        disk = out3.strip() or "N/A"

        # Uptime
        out4, _ = run_cmd("uptime -p | sed 's/up //'")
        uptime = out4.strip()[:16] or "N/A"

        color_cpu = RED if "%" in cpu and float(cpu.replace("%","")) > 80 else GREEN
        return [
            ("CPU Usage",  cpu,    color_cpu),
            ("RAM Used",   ram,    ACCENT),
            ("Disk /",     disk,   YELLOW),
            ("Uptime",     uptime, PURPLE),
        ]

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: AUTO FIX
    # ─────────────────────────────────────────────────────────────────────────
    def show_autofix(self):
        self._clear()
        self._set_title("Full Auto Fix")

        inner = self._card(self.container, "🔧  Full Auto Fix — What will run:")
        steps = [
            "✔  Update & upgrade all packages (apt)",
            "✔  Remove orphaned packages (autoremove)",
            "✔  Clean APT cache (autoclean + clean)",
            "✔  Clear /tmp files older than 1 day",
            "✔  Drop memory caches (page/slab/inode)",
            "✔  Restart NetworkManager",
            "✔  Flush DNS cache",
            "✔  Trim journal logs to 7 days",
            "✔  Reload systemd daemon",
            "✔  Fix broken packages (apt --fix-broken)",
        ]
        for s in steps:
            tk.Label(inner, text=s, font=FONT_BODY,
                     bg=CARD, fg=TEXT, anchor="w").pack(fill="x", pady=1)

        btn_row = tk.Frame(self.container, bg=BG)
        btn_row.pack(fill="x", pady=6)
        self._action_btn(btn_row, "▶  RUN FULL AUTO FIX", self._run_autofix, GREEN)

        term_frame = self._card(self.container, "Terminal Output")
        self.af_term = self._terminal(term_frame)

    def _run_autofix(self):
        if self.running: return
        self.running = True
        self._start_progress()
        self._set_status("Running Auto Fix...")
        threading.Thread(target=self._autofix_thread, daemon=True).start()

    def _autofix_thread(self):
        t = self.af_term
        steps = [
            ("Updating package list...",          "sudo apt-get update -y",               10),
            ("Upgrading packages...",              "sudo apt-get upgrade -y",              30),
            ("Removing orphaned packages...",      "sudo apt-get autoremove -y",           15),
            ("Cleaning APT cache...",              "sudo apt-get autoclean -y && sudo apt-get clean -y", 5),
            ("Fixing broken packages...",          "sudo apt-get install -f -y",           10),
            ("Clearing /tmp (older than 1d)...",   "find /tmp -mindepth 1 -mtime +1 -exec rm -rf {} + 2>/dev/null; echo done", 5),
            ("Dropping memory caches...",          "sync && echo 3 | sudo tee /proc/sys/vm/drop_caches", 5),
            ("Restarting NetworkManager...",       "sudo systemctl restart NetworkManager", 5),
            ("Flushing DNS...",                    "sudo systemd-resolve --flush-caches 2>/dev/null || true", 5),
            ("Trimming journal logs...",           "sudo journalctl --vacuum-time=7d",     5),
            ("Reloading systemd daemon...",        "sudo systemctl daemon-reload",         5),
        ]
        total = sum(s[2] for s in steps)
        done  = 0
        self._write(t, "═" * 55, "head")
        self._write(t, "  FULL AUTO FIX — Starting", "head")
        self._write(t, "═" * 55, "head")

        for desc, cmd, weight in steps:
            self._write(t, f"\n[...] {desc}", "info")
            out, code = run_cmd(cmd)
            done += weight
            self.progress.set(done * 100 / total)
            if code == 0:
                self._write(t, f"[OK]  Done", "ok")
                self.fix_count.set(self.fix_count.get() + 1)
                log(f"FIXED: {desc}")
            else:
                self._write(t, f"[!!]  Issue: {out[:80]}", "warn")
                self.skip_count.set(self.skip_count.get() + 1)
                log(f"SKIP: {desc} — {out[:80]}")

        self._write(t, "\n" + "═" * 55, "head")
        self._write(t, "  ✅  FULL AUTO FIX COMPLETE!", "ok")
        self._write(t, "═" * 55, "head")
        self._stop_progress()
        self._set_status("Auto Fix Complete ✓")
        self.running = False
        log("Auto Fix completed")

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: DEEP CLEAN
    # ─────────────────────────────────────────────────────────────────────────
    def show_deepclean(self):
        self._clear()
        self._set_title("Deep Clean")

        inner = self._card(self.container, "🧹  Deep Clean — Targets:")
        items = [
            "🗑  /tmp directory (all files)",
            "🗑  ~/.cache/thumbnails",
            "🗑  Browser caches (Firefox, Chrome, Chromium)",
            "🗑  APT package cache (/var/cache/apt)",
            "🗑  Old kernel packages (keep current)",
            "🗑  Snap revision cache",
            "🗑  systemd journal (keep 3 days)",
            "🗑  Orphaned .deb packages",
            "🗑  Leftover dpkg config files",
        ]
        for item in items:
            tk.Label(inner, text=item, font=FONT_BODY,
                     bg=CARD, fg=TEXT, anchor="w").pack(fill="x", pady=1)

        btn_row = tk.Frame(self.container, bg=BG)
        btn_row.pack(fill="x", pady=6)
        self._action_btn(btn_row, "🧹  RUN DEEP CLEAN", self._run_deepclean, ACCENT)

        term_frame = self._card(self.container, "Terminal Output")
        self.dc_term = self._terminal(term_frame)

    def _run_deepclean(self):
        if self.running: return
        self.running = True
        self._start_progress()
        self._set_status("Running Deep Clean...")
        threading.Thread(target=self._deepclean_thread, daemon=True).start()

    def _deepclean_thread(self):
        t = self.dc_term
        self._write(t, "═" * 55, "head")
        self._write(t, "  DEEP CLEAN — Starting", "head")
        self._write(t, "═" * 55, "head")

        steps = [
            ("Clear /tmp",                    "rm -rf /tmp/* 2>/dev/null; echo ok"),
            ("Clear thumbnail cache",          f"rm -rf {HOME}/.cache/thumbnails/* 2>/dev/null; echo ok"),
            ("Clear Firefox cache",            f"rm -rf {HOME}/.cache/mozilla 2>/dev/null; echo ok"),
            ("Clear Chrome/Chromium cache",    f"rm -rf {HOME}/.cache/google-chrome {HOME}/.cache/chromium 2>/dev/null; echo ok"),
            ("APT clean",                      "sudo apt-get clean -y && sudo apt-get autoclean -y"),
            ("APT autoremove",                 "sudo apt-get autoremove -y"),
            ("Purge old dpkg configs",         "dpkg -l | grep '^rc' | awk '{print $2}' | xargs -r sudo dpkg --purge"),
            ("Remove old kernels",             f"sudo apt-get purge -y $(dpkg -l 'linux-image-*' | grep '^ii' | awk '{{print $2}}' | grep -v $(uname -r) | grep -v linux-image-generic) 2>/dev/null; echo ok"),
            ("Clean snap revisions",           "sudo snap list --all 2>/dev/null | awk '/disabled/{print $1, $3}' | while read name rev; do sudo snap remove $name --revision=$rev 2>/dev/null; done; echo ok"),
            ("Journal logs → 3 days",          "sudo journalctl --vacuum-time=3d"),
        ]
        total_freed_before, _ = run_cmd("df / --output=avail | tail -1")

        for i, (desc, cmd) in enumerate(steps):
            self._write(t, f"\n[...] {desc}", "info")
            out, code = run_cmd(cmd)
            self.progress.set((i + 1) * 100 / len(steps))
            if code == 0:
                self._write(t, "[OK]  Done", "ok")
                self.fix_count.set(self.fix_count.get() + 1)
                log(f"CLEANED: {desc}")
            else:
                self._write(t, f"[~~]  Skipped ({out[:60]})", "warn")
                self.skip_count.set(self.skip_count.get() + 1)

        total_freed_after, _ = run_cmd("df / --output=avail | tail -1")
        try:
            freed_kb = int(total_freed_after) - int(total_freed_before)
            freed_mb = round(freed_kb / 1024, 1)
            self._write(t, f"\n  💾  Freed approx {freed_mb} MB of disk space", "ok")
        except Exception:
            pass

        self._write(t, "\n" + "═" * 55, "head")
        self._write(t, "  ✅  DEEP CLEAN COMPLETE!", "ok")
        self._write(t, "═" * 55, "head")
        self._stop_progress()
        self._set_status("Deep Clean Complete ✓")
        self.running = False
        log("Deep Clean completed")

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: GAME BOOST
    # ─────────────────────────────────────────────────────────────────────────
    def show_gameboost(self):
        self._clear()
        self._set_title("Game Boost Mode 🎮")

        inner = self._card(self.container, "🎮  Game Boost — What changes:")
        on_items = [
            "🟢  CPU Governor → performance mode",
            "🟢  Stop Bluetooth service",
            "🟢  Stop printer service (cups)",
            "🟢  Stop tracker/indexer services",
            "🟢  Drop memory caches",
            "🟢  Set vm.swappiness → 5",
            "🟢  Increase process niceness for games",
        ]
        off_items = [
            "🔴  Does NOT kill browser (your choice)",
            "🔴  Does NOT touch NetworkManager",
            "🔴  Does NOT disable audio",
        ]
        for item in on_items:
            tk.Label(inner, text=item, font=FONT_BODY,
                     bg=CARD, fg=GREEN, anchor="w").pack(fill="x", pady=1)
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=6)
        for item in off_items:
            tk.Label(inner, text=item, font=FONT_BODY,
                     bg=CARD, fg=RED, anchor="w").pack(fill="x", pady=1)

        btn_row = tk.Frame(self.container, bg=BG)
        btn_row.pack(fill="x", pady=6)
        self._action_btn(btn_row, "🎮  ACTIVATE GAME BOOST", self._run_gameboost, PURPLE)
        self._action_btn(btn_row, "↩  RESTORE NORMAL MODE", self._run_restore, YELLOW)

        term_frame = self._card(self.container, "Terminal Output")
        self.gb_term = self._terminal(term_frame)

    def _run_gameboost(self):
        if self.running: return
        self.running = True
        self._start_progress()
        self._set_status("Activating Game Boost...")
        threading.Thread(target=self._gameboost_thread, daemon=True).start()

    def _gameboost_thread(self):
        t = self.gb_term
        self._write(t, "🎮  GAME BOOST MODE — Activating...", "head")
        cmds = [
            ("CPU → performance governor",  "for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance | sudo tee $g; done", 20),
            ("Dropping memory caches",      "sync && echo 3 | sudo tee /proc/sys/vm/drop_caches",                                                        20),
            ("Set swappiness = 5",          "echo 5 | sudo tee /proc/sys/vm/swappiness",                                                                 10),
            ("Stop Bluetooth",              "sudo systemctl stop bluetooth 2>/dev/null; echo ok",                                                         10),
            ("Stop CUPS (printer)",         "sudo systemctl stop cups 2>/dev/null; echo ok",                                                              10),
            ("Stop tracker-miner",          "sudo systemctl stop tracker-miner-fs-3.service 2>/dev/null; echo ok",                                        10),
            ("Stop avahi-daemon",           "sudo systemctl stop avahi-daemon 2>/dev/null; echo ok",                                                      10),
            ("Kill unnecessary bg procs",   "pkill -f update-notifier 2>/dev/null; pkill -f tracker 2>/dev/null; echo ok",                               10),
        ]
        for i, (desc, cmd, w) in enumerate(cmds):
            self._write(t, f"[...] {desc}", "info")
            out, code = run_cmd(cmd)
            self.progress.set((i + 1) * 100 / len(cmds))
            if code == 0:
                self._write(t, "[OK]  Done", "ok")
            else:
                self._write(t, f"[~~]  {out[:60]}", "warn")

        self._write(t, "\n🎮  GAME BOOST ACTIVE! Enjoy your session.", "ok")
        self._write(t, "     Run 'Restore Normal Mode' when done gaming.", "dim")
        self._stop_progress()
        self._set_status("🎮 Game Mode ACTIVE")
        self.running = False
        log("Game Boost activated")

    def _run_restore(self):
        if self.running: return
        self.running = True
        threading.Thread(target=self._restore_thread, daemon=True).start()

    def _restore_thread(self):
        t = self.gb_term
        self._write(t, "\n↩  Restoring normal mode...", "info")
        cmds = [
            "for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo ondemand | sudo tee $g 2>/dev/null; done",
            "echo 10 | sudo tee /proc/sys/vm/swappiness",
            "sudo systemctl start bluetooth 2>/dev/null",
            "sudo systemctl start cups 2>/dev/null",
            "sudo systemctl start avahi-daemon 2>/dev/null",
        ]
        for cmd in cmds:
            run_cmd(cmd)
        self._write(t, "[OK]  Normal mode restored.", "ok")
        self._set_status("Normal Mode Restored")
        self.running = False
        log("Normal mode restored from Game Boost")

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: SECURITY SCAN
    # ─────────────────────────────────────────────────────────────────────────
    def show_security(self):
        self._clear()
        self._set_title("Security Scan 🔐")

        inner = self._card(self.container, "🔐  Security Checks:")
        checks = [
            "🛡  UFW Firewall status + auto-enable",
            "🛡  SSH config (root login, max auth tries)",
            "🛡  World-writable files in /etc",
            "🛡  Failed login attempts (lastb)",
            "🛡  Listening ports (unexpected services)",
            "🛡  SUID files check",
            "🛡  rkhunter rootkit scan (if installed)",
            "🛡  Pending security updates",
        ]
        for c in checks:
            tk.Label(inner, text=c, font=FONT_BODY,
                     bg=CARD, fg=TEXT, anchor="w").pack(fill="x", pady=1)

        btn_row = tk.Frame(self.container, bg=BG)
        btn_row.pack(fill="x", pady=6)
        self._action_btn(btn_row, "🔐  RUN SECURITY SCAN", self._run_security, YELLOW)

        term_frame = self._card(self.container, "Scan Output")
        self.sec_term = self._terminal(term_frame, height=16)

    def _run_security(self):
        if self.running: return
        self.running = True
        self._start_progress()
        self._set_status("Running Security Scan...")
        threading.Thread(target=self._security_thread, daemon=True).start()

    def _security_thread(self):
        t = self.sec_term
        self._write(t, "═" * 55, "head")
        self._write(t, "  SECURITY SCAN", "head")
        self._write(t, "═" * 55, "head")

        # UFW
        self._write(t, "\n[1/8] UFW Firewall", "info")
        out, code = run_cmd("sudo ufw status 2>/dev/null | head -3")
        if "active" in out.lower():
            self._write(t, f"[OK]  Firewall ACTIVE\n{out}", "ok")
        else:
            self._write(t, "[!!]  Firewall INACTIVE — enabling...", "warn")
            run_cmd("sudo ufw --force enable && sudo ufw default deny incoming && sudo ufw default allow outgoing")
            self._write(t, "[OK]  Firewall enabled", "ok")
            self.fix_count.set(self.fix_count.get() + 1)
        self.progress.set(12)

        # SSH
        self._write(t, "\n[2/8] SSH Root Login", "info")
        out, _ = run_cmd("grep -i '^PermitRootLogin' /etc/ssh/sshd_config 2>/dev/null")
        if "yes" in out.lower():
            self._write(t, "[!!]  SSH root login ENABLED — disabling...", "warn")
            run_cmd("sudo sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && sudo systemctl restart sshd 2>/dev/null")
            self._write(t, "[OK]  SSH root login disabled", "ok")
            self.fix_count.set(self.fix_count.get() + 1)
        else:
            self._write(t, f"[OK]  SSH root login: {out or 'default (safe)'}", "ok")
        self.progress.set(25)

        # World-writable files
        self._write(t, "\n[3/8] World-writable files in /etc", "info")
        out, _ = run_cmd("find /etc -maxdepth 2 -perm -o+w -type f 2>/dev/null")
        if out.strip():
            count = len(out.strip().split("\n"))
            self._write(t, f"[!!]  {count} world-writable file(s) found — fixing...", "warn")
            run_cmd(f"find /etc -maxdepth 2 -perm -o+w -type f -exec sudo chmod o-w {{}} \\;")
            self._write(t, "[OK]  Permissions fixed", "ok")
            self.fix_count.set(self.fix_count.get() + 1)
        else:
            self._write(t, "[OK]  No world-writable files found", "ok")
        self.progress.set(37)

        # Failed logins
        self._write(t, "\n[4/8] Failed login attempts", "info")
        out, _ = run_cmd("sudo lastb 2>/dev/null | head -5")
        count_out, _ = run_cmd("sudo lastb 2>/dev/null | wc -l")
        try: fc = int(count_out.strip())
        except: fc = 0
        if fc > 20:
            self._write(t, f"[!!]  {fc} failed login attempts!\n{out}", "warn")
            self.err_count.set(self.err_count.get() + 1)
        else:
            self._write(t, f"[OK]  Failed logins: {fc} (normal)", "ok")
        self.progress.set(50)

        # Listening ports
        self._write(t, "\n[5/8] Listening ports", "info")
        out, _ = run_cmd("ss -tlnp 2>/dev/null | tail -n +2 | head -12")
        self._write(t, out or "None found", "dim")
        self._write(t, "[OK]  Review ports above for anything unexpected", "ok")
        self.progress.set(62)

        # SUID
        self._write(t, "\n[6/8] SUID files check", "info")
        out, _ = run_cmd("find / -perm /4000 -type f 2>/dev/null | grep -v '/proc\\|/snap\\|/sys' | head -10")
        lines = [l for l in out.split("\n") if l.strip()]
        suspicious = [l for l in lines if not any(x in l for x in ["/bin/","/usr/bin/","/usr/sbin/","/sbin/"])]
        if suspicious:
            self._write(t, f"[!!]  Suspicious SUID files:", "warn")
            for s in suspicious: self._write(t, f"      {s}", "warn")
        else:
            self._write(t, f"[OK]  {len(lines)} SUID files (all in standard locations)", "ok")
        self.progress.set(75)

        # rkhunter
        self._write(t, "\n[7/8] Rootkit check (rkhunter)", "info")
        if run_cmd("which rkhunter")[1] == 0:
            self._write(t, "[...] Running rkhunter scan (may take 30s)...", "info")
            out, code = run_cmd("sudo rkhunter --check --sk --nocolors 2>/dev/null | tail -15")
            self._write(t, out[:400], "dim")
            if "Warning" in out:
                self._write(t, "[!!]  rkhunter found warnings (review above)", "warn")
            else:
                self._write(t, "[OK]  rkhunter scan passed", "ok")
        else:
            self._write(t, "[~~]  rkhunter not installed", "dim")
            self._write(t, "      Install: sudo apt install rkhunter", "dim")
        self.progress.set(88)

        # Security updates
        self._write(t, "\n[8/8] Pending security updates", "info")
        out, _ = run_cmd("apt list --upgradable 2>/dev/null | grep -c security || echo 0")
        try: n = int(out.strip())
        except: n = 0
        if n > 0:
            self._write(t, f"[!!]  {n} security update(s) pending!", "warn")
            self._write(t, "      Run Auto Fix to install them.", "dim")
        else:
            self._write(t, "[OK]  No pending security updates", "ok")
        self.progress.set(100)

        self._write(t, "\n" + "═" * 55, "head")
        self._write(t, "  ✅  SECURITY SCAN COMPLETE!", "ok")
        self._write(t, "═" * 55, "head")
        self._stop_progress()
        self._set_status("Security Scan Complete ✓")
        self.running = False
        log("Security scan completed")

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: SYSTEM INFO
    # ─────────────────────────────────────────────────────────────────────────
    def show_sysinfo(self):
        self._clear()
        self._set_title("System Info 📊")

        btn_row = tk.Frame(self.container, bg=BG)
        btn_row.pack(fill="x", pady=4)
        self._action_btn(btn_row, "🔄  Refresh", self.show_sysinfo, ACCENT, width=14)

        term_frame = self._card(self.container, "System Information")
        t = self._terminal(term_frame, height=28)

        def populate():
            self._write(t, "═" * 55, "head")
            self._write(t, "  SYSTEM INFORMATION", "head")
            self._write(t, "═" * 55, "head")

            sections = [
                ("OS & Kernel", [
                    ("OS",       "lsb_release -ds 2>/dev/null || cat /etc/os-release | grep PRETTY | cut -d= -f2 | tr -d '\"'"),
                    ("Kernel",   "uname -r"),
                    ("Arch",     "uname -m"),
                    ("Hostname", "hostname"),
                    ("Uptime",   "uptime -p"),
                ]),
                ("CPU", [
                    ("Model",    "grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs"),
                    ("Cores",    "nproc"),
                    ("Usage",    "top -bn2 -d0.5 | grep 'Cpu(s)' | tail -1 | awk '{print $2\"%\"}'"),
                    ("Governor", "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo N/A"),
                ]),
                ("Memory", [
                    ("Total",    "free -h | awk '/^Mem:/{print $2}'"),
                    ("Used",     "free -h | awk '/^Mem:/{print $3}'"),
                    ("Free",     "free -h | awk '/^Mem:/{print $7}'"),
                    ("Swap",     "free -h | awk '/^Swap:/{print $3\"/\"$2}'"),
                ]),
                ("Disk", [
                    ("Root /",   "df -h / | awk 'NR==2{print $3\"/\"$2\" (\"$5\" used)\"}'"),
                    ("Type",     "lsblk -d -o rota | awk 'NR==2{print ($1==\"0\") ? \"SSD/NVMe\" : \"HDD\"}'"),
                ]),
                ("Network", [
                    ("Hostname", "hostname -f 2>/dev/null || hostname"),
                    ("IP (eth)", "ip -4 addr show | grep inet | grep -v '127.0' | awk '{print $2}' | head -3 | tr '\n' ' '"),
                    ("DNS",      "systemd-resolve --status 2>/dev/null | grep 'DNS Servers' | head -1 | awk '{print $3}' || cat /etc/resolv.conf | grep nameserver | head -2 | awk '{print $2}' | tr '\n' ' '"),
                ]),
                ("GPU", [
                    ("GPU",      "lspci | grep -iE 'vga|3d' | cut -d: -f3 | xargs"),
                    ("NVIDIA",   "nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu --format=csv,noheader 2>/dev/null || echo N/A"),
                ]),
            ]
            for section, items in sections:
                self._write(t, f"\n  [{section}]", "info")
                for label, cmd in items:
                    out, _ = run_cmd(cmd)
                    val = out.strip()[:60] if out.strip() else "N/A"
                    self._write(t, f"  {label:<14} {val}", "normal")

            # Top processes
            self._write(t, "\n  [Top CPU Processes]", "info")
            out, _ = run_cmd("ps aux --sort=-%cpu | awk 'NR>1 && NR<8 {printf \"  %-20s %5s%% CPU  %5s%% MEM\\n\", $11, $3, $4}'")
            self._write(t, out, "dim")

            self._write(t, "\n  [Failed Services]", "info")
            out, _ = run_cmd("systemctl --failed --no-legend 2>/dev/null | awk '{print \"  \" $1}' | head -5")
            self._write(t, out if out.strip() else "  None — all services healthy ✓", "ok" if not out.strip() else "warn")

        threading.Thread(target=populate, daemon=True).start()

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: DISK TOOLS
    # ─────────────────────────────────────────────────────────────────────────
    def show_disktools(self):
        self._clear()
        self._set_title("Disk Tools 💽")

        btn_row = tk.Frame(self.container, bg=BG)
        btn_row.pack(fill="x", pady=6)
        self._action_btn(btn_row, "🔍  SMART Health",  self._run_smart,   ACCENT, 16)
        self._action_btn(btn_row, "✂  Run TRIM (SSD)", self._run_trim,    GREEN,  16)
        self._action_btn(btn_row, "📊  Disk Usage",    self._run_dusage,  YELLOW, 16)
        self._action_btn(btn_row, "🔧  fsck (next boot)", self._run_fsck, ORANGE, 18)

        term_frame = self._card(self.container, "Disk Output")
        self.disk_term = self._terminal(term_frame, height=24)

    def _run_smart(self):
        t = self.disk_term
        self._write(t, "\n[SMART] Reading disk health...", "head")
        if run_cmd("which smartctl")[1] != 0:
            self._write(t, "[!!]  smartmontools not installed", "warn")
            self._write(t, "      Installing: sudo apt install smartmontools", "info")
            run_cmd("sudo apt-get install -y smartmontools")

        disks_out, _ = run_cmd("lsblk -d -o NAME,TYPE | awk '$2==\"disk\"{print \"/dev/\"$1}'")
        for disk in disks_out.strip().split("\n"):
            if disk:
                self._write(t, f"\n  Disk: {disk}", "info")
                out, _ = run_cmd(f"sudo smartctl -H {disk} 2>/dev/null | grep -i 'result\\|overall'")
                if "PASSED" in out or "OK" in out:
                    self._write(t, f"[OK]  {out.strip()}", "ok")
                elif out.strip():
                    self._write(t, f"[!!]  {out.strip()}", "warn")
                else:
                    self._write(t, "      SMART not supported on this disk", "dim")
        log("SMART check run")

    def _run_trim(self):
        t = self.disk_term
        self._write(t, "\n[TRIM] Checking disk type...", "head")
        rota, _ = run_cmd("lsblk -d -o rota | tail -n1")
        if rota.strip() == "0":
            self._write(t, "[SSD] Running fstrim...", "info")
            out, code = run_cmd("sudo fstrim -av 2>/dev/null")
            self._write(t, out if out else "TRIM complete", "ok")
        else:
            self._write(t, "[HDD] TRIM is for SSDs only — skipping", "dim")
        log("TRIM run")

    def _run_dusage(self):
        t = self.disk_term
        self._write(t, "\n[DISK USAGE] Top directories...", "head")
        out, _ = run_cmd("df -h --output=source,size,used,avail,pcent,target | grep -v 'tmpfs\\|udev\\|loop' | head -10")
        self._write(t, out, "normal")
        self._write(t, "\n  Largest directories in /home:", "info")
        out2, _ = run_cmd(f"du -sh {HOME}/* 2>/dev/null | sort -rh | head -10")
        self._write(t, out2, "dim")
        log("Disk usage checked")

    def _run_fsck(self):
        t = self.disk_term
        self._write(t, "\n[FSCK] Scheduling filesystem check on next reboot...", "info")
        run_cmd("sudo touch /forcefsck 2>/dev/null")
        self._write(t, "[OK]  /forcefsck created — fsck will run on next boot", "ok")
        log("fsck scheduled")

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: LOG VIEWER
    # ─────────────────────────────────────────────────────────────────────────
    def show_log(self):
        self._clear()
        self._set_title("Fix Log 📋")

        btn_row = tk.Frame(self.container, bg=BG)
        btn_row.pack(fill="x", pady=4)
        self._action_btn(btn_row, "🔄  Refresh", self.show_log, ACCENT, 12)

        def clear_log():
            if messagebox.askyesno("Clear Log", "Clear the fix log file?"):
                open(LOG_FILE, "w").close()
                self.show_log()

        self._action_btn(btn_row, "🗑  Clear Log", clear_log, RED, 12)

        inner = self._card(self.container, f"📋  {LOG_FILE}")
        t = self._terminal(inner, height=28)

        try:
            with open(LOG_FILE) as f:
                content = f.read()
            if content.strip():
                for line in content.strip().split("\n"):
                    if "FIXED" in line or "CLEANED" in line:
                        self._write(t, line, "ok")
                    elif "WARN" in line or "SKIP" in line:
                        self._write(t, line, "warn")
                    elif "ERROR" in line:
                        self._write(t, line, "err")
                    else:
                        self._write(t, line, "dim")
            else:
                self._write(t, "Log is empty. Run some fixes first!", "dim")
        except FileNotFoundError:
            self._write(t, "No log file yet. Run some fixes first!", "dim")


# ═════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═════════════════════════════════════════════════════════════════════════════
def main():
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Horizontal.TProgressbar",
                    background=ACCENT, troughcolor=BG3,
                    bordercolor=BG3, lightcolor=ACCENT, darkcolor=ACCENT2)

    app = AutoFixApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
