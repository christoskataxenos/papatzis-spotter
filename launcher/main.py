import sys
import os
import subprocess
import threading
import webbrowser
import re
import shutil
import multiprocessing
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTabWidget, QTextEdit, QLabel, QSystemTrayIcon, 
    QMenu, QAction, QFrame, QProgressBar, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QProcess, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QColor

# Υπολογισμός του root φακέλου για το project
def get_project_root():
    if getattr(sys, 'frozen', False):
        # Όταν τρέχουμε ως EXE, ο sys.executable είναι η διαδρομή του .exe
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        # 1. Έλεγχος αν ο analyzer είναι στον ίδιο φάκελο (flat structure)
        if os.path.exists(os.path.join(exe_dir, "analyzer")):
            return exe_dir
        # 2. Έλεγχος αν είμαστε στο launcher/dist (ανάπτυξη)
        parent = os.path.abspath(os.path.join(exe_dir, "..", ".."))
        if os.path.exists(os.path.join(parent, "analyzer")):
            return parent
        # 3. Fallback στο AppData αν πρόκειται για εγκατεστημένη εφαρμογή
        return exe_dir
    else:
        # Κανονική εκτέλεση από Python
        launcher_internal_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(launcher_internal_dir, ".."))

project_root = get_project_root()
launcher_dir = os.path.join(project_root, "launcher")
analyzer_dir = os.path.join(project_root, "analyzer")
venv_dir = os.path.join(analyzer_dir, "venv")
python_exec = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == "nt" else os.path.join(venv_dir, "bin", "python")

# --- Σύγχρονη Παλέτα Χρωμάτων (Papatzis Spotter) ---
THEME = {
    "bg": "#0a0a0a",
    "surface": "#111111",
    "accent": "#2F6FFF", # Electric Blue
    "accent_hover": "#38bdf8",
    "text": "#f8fafc",
    "text_dim": "#94a3b8",
    "success": "#2ECC71", # Emerald Green
    "danger": "#FF6F5E", # Muted Coral
    "warning": "#A259FF", # Electric Purple
}

class LogEmitter(QObject):
    log_received = pyqtSignal(str, str)

class PapatzisLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.log_emitter = LogEmitter()
        self.log_emitter.log_received.connect(self.append_log)
        self.running_procs = {}
        self.is_auto_building_analyzer = False
        
        self.setup_ui()
        self.setup_tray()
        
        # Ορισμός εικονιδίου
        if getattr(sys, 'frozen', False):
            # Στο frozen EXE, το icon.ico είναι συνήθως στο root του temp dir (_MEI)
            icon_path = os.path.join(sys._MEIPASS, "icon.ico") if hasattr(sys, '_MEIPASS') else "icon.ico"
        else:
            icon_path = os.path.join(launcher_dir, "icon.ico")
            
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Αρχικός έλεγχος περιβάλλοντος
        QTimer.singleShot(800, self.verify_env)

    def setup_ui(self):
        self.setWindowTitle("Papatzis Spotter - Orchestrator")
        self.resize(1150, 750)
        self.apply_theme()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- ARISTERO SIDEBAR ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(280)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)
        
        # Logo / Title Section
        logo_lbl = QLabel("PAPATZIS")
        logo_lbl.setStyleSheet(f"color: {THEME['accent']}; font-size: 26px; font-weight: 900; letter-spacing: 2px;")
        sidebar_layout.addWidget(logo_lbl)
        
        sub_lbl = QLabel("SPOTTER ORCHESTRATOR")
        sub_lbl.setStyleSheet(f"color: {THEME['text_dim']}; font-size: 10px; font-weight: bold; margin-bottom: 30px;")
        sidebar_layout.addWidget(sub_lbl)

        # Status Badges
        self.status_env = self.create_status_item("Environment", "Checking...")
        sidebar_layout.addWidget(self.status_env)
        
        self.status_venv = self.create_status_item("Python Venv", "Checking...")
        sidebar_layout.addWidget(self.status_venv)
        
        sidebar_layout.addSpacing(40)
        sidebar_layout.addWidget(QLabel("ACTIONS"))

        # Action Buttons
        btn_folder = self.create_side_btn("📁 Open Folder", self.open_project_folder)
        sidebar_layout.addWidget(btn_folder)
        
        btn_rebuild = self.create_side_btn("🔄 Rebuild Env", self.rebuild_environment)
        sidebar_layout.addWidget(btn_rebuild)
        
        btn_clear = self.create_side_btn("🧹 Clear Logs", self.clear_logs)
        sidebar_layout.addWidget(btn_clear)

        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(QLabel("ECOSYSTEM"))
        
        btn_cli = self.create_side_btn("💻 Install CLI", self.install_cli_global)
        sidebar_layout.addWidget(btn_cli)

        btn_skill = self.create_side_btn("🤖 Shield AI Agents", self.inject_papatzo_skill)
        sidebar_layout.addWidget(btn_skill)

        btn_bouncer = self.create_side_btn("🪝 Git Bouncer", self.install_git_bouncer)
        sidebar_layout.addWidget(btn_bouncer)

        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(QLabel("BUILD CENTER"))
        
        btn_build_cli = self.create_side_btn("🔨 Build Papatzis Engine", self.build_analyzer)
        sidebar_layout.addWidget(btn_build_cli)

        btn_build_gui = self.create_side_btn("🏠 Build Papatzis Spotter", self.build_launcher)
        sidebar_layout.addWidget(btn_build_gui)

        btn_build_release = self.create_side_btn("📦 Build Release EXE", self.build_release)
        btn_build_release.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #4f46e5);
                color: #ffffff;
                text-align: left;
                padding: 12px;
                border-radius: 8px;
                font-weight: 700;
                border: none;
            }}
            QPushButton:hover {{ background: #6d28d9; }}
        """)
        sidebar_layout.addWidget(btn_build_release)

        sidebar_layout.addStretch()
        
        # App Version
        ver_lbl = QLabel("v1.5.0-stable")
        ver_lbl.setStyleSheet(f"color: {THEME['text_dim']}; font-size: 10px;")
        ver_lbl.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(ver_lbl)

        main_layout.addWidget(sidebar)

        # --- ΚΕΝΤΡΙΚΟ ΠΕΡΙΕΧΟΜΕΝΟ ---
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top Header Control
        header_frame = QFrame()
        header_frame.setObjectName("HeaderFrame")
        h_layout = QHBoxLayout(header_frame)
        
        self.lbl_main_status = QLabel("System Ready")
        self.lbl_main_status.setFont(QFont("Segoe UI", 16, QFont.Bold))
        h_layout.addWidget(self.lbl_main_status)
        h_layout.addStretch()
        
        self.btn_launch = QPushButton("🚀 LAUNCH PROJECT")
        self.btn_launch.setObjectName("PrimaryBtn")
        self.btn_launch.setFixedSize(200, 45)
        self.btn_launch.clicked.connect(self.run_all)
        h_layout.addWidget(self.btn_launch)

        self.btn_stop = QPushButton("🛑 STOP")
        self.btn_stop.setObjectName("StopBtn")
        self.btn_stop.setFixedSize(100, 45)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.kill_all)
        h_layout.addWidget(self.btn_stop)
        
        content_layout.addWidget(header_frame)
        
        # Progress Bar (Subtle)
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setFixedHeight(3)
        self.progress.setTextVisible(False)
        content_layout.addWidget(self.progress)

        # Log Tabs
        self.tabs = QTabWidget()
        self.tabs.setObjectName("MainTabs")
        
        self.npm_out = QTextEdit()
        self.npm_out.setReadOnly(True)
        self.npm_out.setObjectName("Terminal")
        self.tabs.addTab(self.npm_out, "📦 TAURI ENGINE")
        
        self.py_out = QTextEdit()
        self.py_out.setReadOnly(True)
        self.py_out.setObjectName("Terminal")
        self.tabs.addTab(self.py_out, "🐍 ANALYZER ENGINE")
        
        self.build_out = QTextEdit()
        self.build_out.setReadOnly(True)
        self.build_out.setObjectName("Terminal")
        self.tabs.addTab(self.build_out, "🛠️ BUILD LOGS")
        
        content_layout.addWidget(self.tabs)
        
        main_layout.addWidget(content_area)

    def create_status_item(self, label, value):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 5, 0, 5)
        
        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {THEME['text_dim']}; font-size: 10px; text-transform: uppercase;")
        val = QLabel(value)
        val.setStyleSheet(f"color: {THEME['text']}; font-weight: bold; font-size: 12px;")
        val.setObjectName(f"StatusVal_{label.replace(' ', '')}")
        
        layout.addWidget(lbl)
        layout.addWidget(val)
        return frame

    def create_side_btn(self, text, callback):
        btn = QPushButton(text)
        btn.setObjectName("SidebarBtn")
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(callback)
        return btn

    def apply_theme(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {THEME['bg']}; }}
            
            #Sidebar {{ 
                background-color: {THEME['surface']}; 
                border-right: 1px solid #2d3748;
            }}
            
            #HeaderFrame {{ margin-bottom: 10px; }}
            
            QLabel {{ color: {THEME['text']}; font-family: 'Segoe UI', sans-serif; }}
            
            #SidebarBtn {{
                background-color: transparent;
                color: {THEME['text_dim']};
                text-align: left;
                padding: 12px;
                border-radius: 8px;
                font-weight: 500;
                border: none;
            }}
            #SidebarBtn:hover {{
                background-color: #2d3748;
                color: {THEME['text']};
            }}
            
            #PrimaryBtn {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {THEME['accent']}, stop:1 #2563eb);
                color: #ffffff;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }}
            #PrimaryBtn:hover {{ background: {THEME['accent_hover']}; }}
            #PrimaryBtn:disabled {{ background-color: #475569; color: #94a3b8; border: none; }}
            
            #StopBtn {{
                background-color: {THEME['danger']};
                color: #ffffff;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }}
            #StopBtn:hover {{ background-color: #dc2626; }}
            #StopBtn:disabled {{ background-color: #334155; color: #94a3b8; border: 1px solid #475569; }}
            
            QProgressBar {{ background-color: #1e293b; border: none; border-radius: 2px; }}
            QProgressBar::chunk {{ background-color: {THEME['accent']}; }}
            
            #MainTabs::pane {{ border: 1px solid #2d3748; border-radius: 12px; background: #000; top: -1px; }}
            QTabBar::tab {{
                background: transparent;
                color: {THEME['text_dim']};
                padding: 10px 30px;
                min-width: 140px;
                font-size: 10px;
                font-weight: bold;
                border-bottom: 2px solid transparent;
            }}
            QTabBar::tab:selected {{
                color: {THEME['accent']};
                border-bottom: 2px solid {THEME['accent']};
            }}
            
            #Terminal {{
                background-color: #050505;
                color: #e2e8f0;
                font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
                font-size: 13px;
                border: none;
                padding: 10px;
                line-height: 1.5;
            }}
        """)

    def setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "icon.ico") if hasattr(sys, '_MEIPASS') else "icon.ico"
        else:
            icon_path = os.path.join(launcher_dir, "icon.ico")
            
        if os.path.exists(icon_path):
            self.tray.setIcon(QIcon(icon_path))
        else:
            self.tray.setIcon(self.style().standardIcon(65))
        
        menu = QMenu()
        act_show = QAction("Άνοιγμα", self)
        act_show.triggered.connect(self.showNormal)
        act_exit = QAction("Έξοδος", self)
        act_exit.triggered.connect(self.full_exit)
        
        menu.addAction(act_show)
        menu.addSeparator()
        menu.addAction(act_exit)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.activated.connect(self.on_tray_click)

    def on_tray_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal() if not self.isVisible() else self.hide()

    # --- ACTIONS ---
    # --- ECOSYSTEM ACTIONS ---
    def install_cli_global(self):
        """Adds the Papatzis CLI to system PATH."""
        self.tabs.setCurrentIndex(2)
        self.append_log("build", "<b>[ECOSYSTEM] Initiating CLI system integration...</b>\n")
        
        # Determine paths
        dist_cli = os.path.join(project_root, "dist", "PapatzisEngine.exe")
        target_dir = os.path.join(os.environ.get("LOCALAPPDATA", ""), "PapatzisSpotter", "bin")
        target_exe = os.path.join(target_dir, "papatzis.exe")

        if not os.path.exists(dist_cli):
            self.append_log("build", "[FAILED] CLI binary not found in dist/. Build the Analyzer first.\n")
            return

        try:
            os.makedirs(target_dir, exist_ok=True)
            shutil.copy2(dist_cli, target_exe)
            
            # Logic to add to PATH (Windows)
            current_path = os.environ.get("PATH", "")
            if target_dir not in current_path:
                subprocess.run(['setx', 'PATH', f"{current_path};{target_dir}"], check=True, shell=True)
                self.append_log("build", f"[SUCCESS] CLI installed to {target_dir} and added to PATH.\n")
                self.append_log("build", "<b>Note:</b> Restart your terminal to use 'papatzis' command.\n")
            else:
                self.append_log("build", "[INFO] CLI already exists in PATH.\n")
        except Exception as e:
            self.append_log("build", f"[ERROR] Installation failed: {str(e)}\n")

    def inject_papatzo_skill(self):
        """Injects anti-slop rules into various AI Agent configurations."""
        self.tabs.setCurrentIndex(2)
        self.append_log("build", "<b>[ECOSYSTEM] Deploying PapatzoSkill to AI Agents...</b>\n")
        
        skill_source = os.path.join(project_root, "my-skills", "papatzis-spotter", "SKILL.md")
        if not os.path.exists(skill_source):
            self.append_log("build", "[FAILED] Skill source missing. Verify my-skills/papatzis-spotter/SKILL.md.\n")
            return

        with open(skill_source, "r", encoding="utf-8") as f:
            skill_content = f.read()

        targets = [
            # Cursor IDE
            (".cursorrules", "append"),
            # GitHub Copilot / Cline
            (".github/copilot-instructions.md", "overwrite"),
            # Local Antigravity/Gemini (if in root)
            (".gemini/my-skills/papatzis/SKILL.md", "overwrite")
        ]

        for rel_path, mode in targets:
            full_path = os.path.join(project_root, rel_path)
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                if mode == "append" and os.path.exists(full_path):
                    with open(full_path, "a", encoding="utf-8") as f:
                        f.write("\n\n" + skill_content)
                else:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(skill_content)
                self.append_log("build", f"[SUCCESS] Injected rules into {rel_path}\n")
            except Exception as e:
                self.append_log("build", f"[WARN] Could not write to {rel_path}: {str(e)}\n")

    def install_git_bouncer(self):
        """Installs a pre-commit hook to block slop commits."""
        self.tabs.setCurrentIndex(2)
        self.append_log("build", "<b>[ECOSYSTEM] Installing Git Bouncer (Pre-commit Hook)...</b>\n")
        
        hooks_dir = os.path.join(project_root, ".git", "hooks")
        if not os.path.exists(hooks_dir):
            self.append_log("build", "[FAILED] .git directory not found. Is this a repository?\n")
            return

        hook_script = f"""#!/bin/bash
# Papatzis Spotter Bouncer
echo "🔍 Scanning for slop before commit..."
papatzis check . --heat hot --exit-on-slop
if [ $? -ne 0 ]; then
    echo "🛑 STOP! Papatzis detected. Commit aborted."
    exit 1
fi
"""
        hook_path = os.path.join(hooks_dir, "pre-commit")
        try:
            with open(hook_path, "w", encoding="utf-8") as f:
                f.write(hook_script)
            # Make executable on Unix-like systems (or if running via git bash on windows)
            # Note: windows file permissions are tricky, but git uses the file content.
            self.append_log("build", "[SUCCESS] Git Bouncer active. No slop shall pass.\n")
        except Exception as e:
            self.append_log("build", f"[ERROR] Failed to install hook: {str(e)}\n")

    def open_project_folder(self):
        os.startfile(project_root)

    def clear_logs(self):
        self.npm_out.clear()
        self.py_out.clear()

    def rebuild_environment(self):
        if os.path.exists(venv_dir):
            try:
                shutil.rmtree(venv_dir)
                self.append_log("py", "[SYSTEM] Το venv διαγράφηκε. Ξεκινάει επαναδημιουργία...\n")
                self.verify_env()
            except Exception as e:
                self.append_log("py", f"[ERROR] Αδυναμία διαγραφής venv: {str(e)}\n")

    def verify_env(self):
        # Έλεγχος .env
        dot_env = os.path.join(project_root, ".env")
        status_env = self.findChild(QLabel, "StatusVal_Environment")
        if os.path.exists(dot_env):
            status_env.setText("✅ FOUND")
            status_env.setStyleSheet(f"color: {THEME['success']}; font-weight: bold;")
        else:
            with open(dot_env, "w") as f: f.write("DEBUG=True\n")
            status_env.setText("Created default")
            status_env.setStyleSheet(f"color: {THEME['warning']};")

        # Έλεγχος venv
        status_venv = self.findChild(QLabel, "StatusVal_PythonVenv")
        if not os.path.exists(venv_dir):
            status_venv.setText("⏳ BUILDING...")
            status_venv.setStyleSheet(f"color: {THEME['accent']}; font-weight: bold;")
            self.lbl_main_status.setText("Setting up environment...")
            self.progress.setVisible(True)
            self.progress.setRange(0, 0)
            threading.Thread(target=self.build_venv, daemon=True).start()
        else:
            status_venv.setText("✅ READY")
            status_venv.setStyleSheet(f"color: {THEME['success']}; font-weight: bold;")
            self.lbl_main_status.setText("Ready to Launch")

    def get_python_base(self):
        """Επιστρέφει την διαδρομή προς έναν κανονικό Python interpreter."""
        if not getattr(sys, 'frozen', False):
            # Καθαρισμός από εισαγωγικά και κενά
            exe = sys.executable.strip('"').strip("'").strip()
            # Προτιμούμε το python.exe για CLI tasks
            if exe.lower().endswith("pythonw.exe"):
                exe = exe[:exe.lower().rfind("pythonw.exe")] + "python.exe"
            elif exe.lower().endswith("pythonw"):
                exe = exe[:exe.lower().rfind("pythonw")] + "python"
            return exe
        
        # Αν είμαστε frozen, ο sys.executable είναι το EXE μας.
        # Πρέπει να βρούμε έναν πραγματικό Python στο σύστημα.
        system_python = shutil.which("python") or shutil.which("python3")
        if system_python:
            return system_python.strip('"').strip("'").strip()
            
        # Αν δεν βρεθεί, επιστρέφουμε την διαδρομή του venv αν υπάρχει
        if os.path.exists(python_exec):
            return python_exec.strip('"').strip("'").strip()
            
        return None

    def build_venv(self):
        try:
            base_py = self.get_python_base()
            if not base_py or base_py == sys.executable:
                if getattr(sys, 'frozen', False):
                    self.log_emitter.log_received.emit("py", "[ERROR] Δεν βρέθηκε Python στο σύστημα για την δημιουργία venv. Εγκαταστήστε την Python.\n")
                    return
            
            subprocess.run([base_py, "-m", "venv", venv_dir], check=True)
            reqs = os.path.join(analyzer_dir, "requirements.txt")
            if os.path.exists(reqs):
                clean_py_exec = python_exec.strip('"').strip("'").strip()
                subprocess.run([clean_py_exec, "-m", "pip", "install", "-r", reqs], check=True)
            self.log_emitter.log_received.emit("py", "[SUCCESS] Το περιβάλλον Python στήθηκε επιτυχώς.\n")
        except Exception as e:
            self.log_emitter.log_received.emit("py", f"[ERROR] Σφάλμα setup: {str(e)}\n")
        finally:
            self.progress.setVisible(False)
            QTimer.singleShot(0, self.verify_env)

    def run_all(self):
        self.btn_launch.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.lbl_main_status.setText("Orchestrator Running")
        
        # Εκκίνηση Tauri
        p = QProcess(self)
        p.setWorkingDirectory(project_root)
        p.setProcessChannelMode(QProcess.MergedChannels)
        p.readyRead.connect(lambda: self.stream_logs(p, "npm"))
        
        cmd = ["cmd", "/c", "npm run tauri dev"] if os.name == "nt" else ["npm", "run", "tauri", "dev"]
        p.start(cmd[0], cmd[1:])
        self.running_procs["npm"] = p

    def stream_logs(self, p, sid):
        msg = p.readAll().data().decode("utf8", errors="replace")
        self.log_emitter.log_received.emit(sid, msg)

    def append_log(self, sid, msg):
        if sid == "npm": box = self.npm_out
        elif sid == "py": box = self.py_out
        else: box = self.build_out
        
        # --- HTML HIGHLIGHTING ---
        color = "#e2e8f0"
        if "ERROR" in msg.upper() or "ERR!" in msg.upper() or "FAILED" in msg.upper():
            color = THEME['danger']
        elif "SUCCESS" in msg.upper() or "DONE" in msg.upper() or "✅" in msg:
            color = THEME['success']
        elif "WARN" in msg.upper():
            color = THEME['warning']
        elif "INFO" in msg.upper() or "SYSTEM" in msg.upper():
            color = THEME['accent']

        # Καθαρισμός ANSI χρωμάτων αν υπάρχουν (npm outputs)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_msg = ansi_escape.sub('', msg)
        
        formatted = f'<span style="color: {color};">{clean_msg}</span>'
        formatted = formatted.replace("\n", "<br>")
        
        box.moveCursor(QTextCursor.End)
        box.insertHtml(formatted)
        box.verticalScrollBar().setValue(box.verticalScrollBar().maximum())

    def kill_all(self):
        for p in self.running_procs.values():
            p.terminate()
            if not p.waitForFinished(1000): p.kill()
        self.running_procs.clear()
        self.btn_launch.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.lbl_main_status.setText("Stopped")

    def build_launcher(self):
        """Χτίζει το εκτελέσιμο του Orchestrator (self-packaging)"""
        self.tabs.setCurrentIndex(2) # Build Logs Tab
        self.append_log("build", "<b>[BUILD] Έναρξη δημιουργίας Papatzis Spotter...</b>\n")
        
        # Χρησιμοποιούμε την απόλυτη διαδρομή από τον launcher_dir του project
        spec_path = os.path.join(launcher_dir, "PapatzisSpotter.spec")
        
        p = QProcess(self)
        # Χρησιμοποιούμε τον πραγματικό φάκελο του launcher
        p.setWorkingDirectory(launcher_dir)
        p.setProcessChannelMode(QProcess.MergedChannels)
        p.readyRead.connect(lambda: self.stream_logs(p, "build"))
        
        # Εκτέλεση PyInstaller πάνω στο spec
        launcher_venv_py = self.get_python_base()
        if not launcher_venv_py:
            self.append_log("build", "[ERROR] Δεν βρέθηκε Python για το PyInstaller.\n")
            return
            
        args = ["-m", "PyInstaller", spec_path, "--noconfirm", "--clean"]
        self.append_log("build", f"[SYSTEM] Executing: {launcher_venv_py} {' '.join(args)} in {launcher_dir}\n")
        p.start(launcher_venv_py, args)

        self.running_procs["build_spotter"] = p
        p.finished.connect(lambda code, _: self.on_build_finished("Spotter", code))

    def build_analyzer(self):
        """Χτίζει το εκτελέσιμο του Papatzis Engine (CLI)"""
        self.tabs.setCurrentIndex(2)
        self.append_log("build", "<b>[BUILD] Έναρξη δημιουργίας Papatzis Engine...</b>\n")

        # Χρησιμοποιούμε το spec file από το project root
        spec_file = os.path.join(project_root, "PapatzisEngine.spec")

        p = QProcess(self)
        p.setWorkingDirectory(project_root)
        p.setProcessChannelMode(QProcess.MergedChannels)
        p.readyRead.connect(lambda: self.stream_logs(p, "build"))

        # Use the venv python if it exists, otherwise fallback to system python
        if os.path.exists(python_exec):
            launcher_venv_py = python_exec.strip('"').strip("'").strip()
        else:
            launcher_venv_py = self.get_python_base()

        if not launcher_venv_py:
            self.append_log("build", "[ERROR] Δεν βρέθηκε Python για το PyInstaller.\n")
            return

        # Προσθήκη --clean και αλλαγή distpath για να μην χτυπάει με το Vite dist/
        args = ["-m", "PyInstaller", spec_file, "--noconfirm", "--clean", "--distpath", "analyzer-dist"]
        self.append_log("build", f"[SYSTEM] Executing: {launcher_venv_py} {' '.join(args)} in {project_root}\n")
        p.start(launcher_venv_py, args)

        self.running_procs["build_engine"] = p
        p.finished.connect(lambda code, _: self.on_build_finished("Engine", code))

    def build_release(self):
        """Φτιάχνει το τελικό Standalone EXE μέσω Tauri build."""
        self.tabs.setCurrentIndex(2)
        self.append_log("build", "<b>[RELEASE] Ο τελικός είναι ένα standalone Windows EXE...</b>\n")

        # Βήμα 1: Αντιγραφή του PapatzisEngine.exe στον φάκελο src-tauri/binaries
        src_engine = os.path.join(project_root, "analyzer-dist", "PapatzisEngine.exe")
        dst_engine = os.path.join(project_root, "src-tauri", "binaries", "slop-engine-x86_64-pc-windows-msvc.exe")

        if not os.path.exists(src_engine):
            self.append_log("build", "[AUTO] Ο Papatzis Engine δεν βρέθηκε. Έναρξη αυτόματης δημιουργίας...\n")
            self.is_auto_building_analyzer = True
            self.build_analyzer()
            return

        try:
            # Διασφάλιση ότι ο φάκελος προορισμού υπάρχει
            os.makedirs(os.path.dirname(dst_engine), exist_ok=True)
            shutil.copy2(src_engine, dst_engine)
            self.append_log("build", f"[OK] PapatzisEngine.exe αντιγράφηκε στο src-tauri/\n")
        except Exception as e:
            self.append_log("build", f"[ERROR] Αδυναμία αντιγραφής: {e}\n")
            return

        # Βήμα 2: Tauri build (npm run tauri build)
        self.append_log("build", "[BUILD] Τρέχει 'npm run tauri build'... (Μπορεί να πάρει 3-10 λεπτά)\n")
        p = QProcess(self)
        p.setWorkingDirectory(project_root)
        p.setProcessChannelMode(QProcess.MergedChannels)
        p.readyRead.connect(lambda: self.stream_logs(p, "build"))
        p.finished.connect(lambda code, _: self._on_tauri_build_finished(code))
        p.start("cmd", ["/c", "npm run tauri build"])
        self.running_procs["tauri_build"] = p

    def _on_tauri_build_finished(self, exit_code: int):
        if exit_code != 0:
            self.append_log("build", "\n[ERROR] Το Tauri build απέτυχε. Ελέγξτε τα logs παραπάνω.\n")
            return

        self.append_log("build", "\n[OK] Tauri build ολοκληρώθηκε!\n")

        # Βήμα 3: Οργάνωση του Portable φακέλου
        tauri_exe_dir = os.path.join(project_root, "src-tauri", "target", "release")
        # Το Tauri παράγει το όνομα βάσει του productName (Papatzis Spotter)
        tauri_exe = os.path.join(tauri_exe_dir, "Papatzis Spotter.exe")
        if not os.path.exists(tauri_exe):
            tauri_exe = os.path.join(tauri_exe_dir, "papatzis-spotter.exe")
        if not os.path.exists(tauri_exe):
            # Αναζήτηση για οποιοδήποτε .exe στο release dir που δεν είναι ο engine
            exes = [f for f in os.listdir(tauri_exe_dir) if f.endswith(".exe") and "engine" not in f.lower() and "papatzis" in f.lower()]
            if not exes:
                exes = [f for f in os.listdir(tauri_exe_dir) if f.endswith(".exe") and "engine" not in f.lower()]
            tauri_exe = os.path.join(tauri_exe_dir, exes[0]) if exes else None

        if not tauri_exe or not os.path.exists(tauri_exe):
            self.append_log("build", "[ERROR] Δεν βρέθηκε το EXE στο src-tauri/target/release/.\n")
            return

        portable_dir = os.path.join(project_root, "Papatzis-Portable")
        os.makedirs(portable_dir, exist_ok=True)

        try:
            shutil.copy2(tauri_exe, os.path.join(portable_dir, os.path.basename(tauri_exe)))
            
            self.append_log("build", f"\n<b>✅ Παράδοτος αποθήκευση έτοιμη! Ολόκληρη η εφαρμογή είναι σε ένα μόνο .exe!</b>\n")
            self.append_log("build", f"Φάκελος: <b>{portable_dir}</b>\n")
            self.append_log("build", "Τρέξτε το EXE σε οποιονδήποτε υπολογιστή!\n")
            self.lbl_main_status.setText("Release Ready!")
            os.startfile(portable_dir)
        except Exception as e:
            self.append_log("build", f"[ERROR] Σφάλμα packaging: {e}\n")

    def on_build_finished(self, name, exit_code=0):
        if exit_code != 0:
            self.append_log("build", f"\n<b>❌ Το PyInstaller απέτυχε για το {name} (Exit Code: {exit_code})</b>\n")
            self.lbl_main_status.setText(f"{name} Failed!")
            return

        # Έλεγχος αν όντως δημιουργήθηκε το αρχείο
        dist_path = os.path.join(project_root, "analyzer-dist") if name == "Engine" else os.path.join(launcher_dir, "dist")
        exe_name = "PapatzisEngine.exe" if name == "Engine" else "PapatzisSpotter.exe"
        exe_path = os.path.join(dist_path, exe_name)

        if os.path.exists(exe_path):
            self.append_log("build", f"\n<b>✅ Η διαδικασία για το {name} ολοκληρώθηκε με επιτυχία!</b>\n")

            # Αυτόματη αντιγραφή στο root για ευκολία
            target_path = os.path.join(project_root, exe_name)
            try:
                shutil.copy2(exe_path, target_path)
                self.append_log("build", f"[SYSTEM] Το αρχείο αντιγράφηκε στο root: {target_path}\n")
            except Exception as e:
                self.append_log("build", f"[ERROR] Αδυναμία αντιγραφής στο root: {e}\n")

            self.lbl_main_status.setText(f"{name} Ready!")
        else:
            self.append_log("build", f"\n<b>❌ Σφάλμα: Η διαδικασία ολοκληρώθηκε αλλά το {exe_name} δεν βρέθηκε!</b>\n")
            self.append_log("build", f"Το PyInstaller ίσως απέτυχε χωρίς να επιστρέψει σφάλμα. Ελέγξτε τα build logs.\n")
            self.lbl_main_status.setText(f"{name} Failed!")

        if name == "Engine" and self.is_auto_building_analyzer:
            self.is_auto_building_analyzer = False
            if os.path.exists(exe_path):
                self.append_log("build", "\n[AUTO] Ο Papatzis Engine είναι έτοιμος. Συνέχεια στο Release build...\n")
                self.build_release()
            else:
                self.append_log("build", "\n[AUTO] Το release build σταμάτησε λόγω αποτυχίας του Engine.\n")
    def closeEvent(self, event):
        if self.tray.isVisible():
            self.hide()
            event.ignore()

    def full_exit(self):
        self.kill_all()
        QApplication.quit()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    ui = PapatzisLauncher()
    ui.show()
    sys.exit(app.exec_())
