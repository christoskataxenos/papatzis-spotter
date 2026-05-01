import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QSplitter,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QFont
from gui.editor import CodeEditor
from gui.widgets import FindingCard, SummaryWidget
from gui.analysis_worker import AnalysisWorker

class TopNavBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setObjectName("TopNavBar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Logo / Title
        self.logo = QLabel("PAPATZIS SPOTTER V3")
        self.logo.setStyleSheet("font-weight: bold; font-size: 18px; color: #ff4d4d;")
        layout.addWidget(self.logo)
        
        layout.addStretch()
        
        # Nav Buttons
        self.btn_home = QPushButton("ΑΡΧΙΚΗ")
        self.btn_analyze = QPushButton("ΑΝΑΛΥΣΗ")
        self.btn_batch = QPushButton("BATCH")
        self.btn_settings = QPushButton("ΡΥΘΜΙΣΕΙΣ")
        
        for btn in [self.btn_home, self.btn_analyze, self.btn_batch, self.btn_settings]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)
            
        layout.addStretch()
        
        # Help Button
        self.btn_help = QPushButton("?")
        self.btn_help.setFixedSize(30, 30)
        layout.addWidget(self.btn_help)

class HomeView(QWidget):
    analyzeRequested = pyqtSignal(str) # Emits the code to analyze
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Welcome Header
        self.title = QLabel("DETECT THE SLOP")
        self.title.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: white; 
            letter-spacing: 2px;
            margin-bottom: 10px;
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)
        
        self.subtitle = QLabel("Η ψηφιακή ασπίδα κατά του AI-Generated κώδικα")
        self.subtitle.setStyleSheet("font-size: 14px; color: #888; margin-bottom: 30px;")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.subtitle)
        
        # Glassmorphic Input Area
        self.input_area = QFrame()
        self.input_area.setMinimumSize(800, 400)
        self.input_area.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 0.7);
                border: 1px solid #333;
                border-radius: 15px;
            }
        """)
        input_layout = QVBoxLayout(self.input_area)
        
        from PyQt6.QtWidgets import QTextEdit
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("Επικόλλησε τον κώδικα εδώ για ανάλυση...")
        self.code_input.setStyleSheet("""
            background: transparent;
            border: none;
            color: #50fa7b;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 14px;
            padding: 15px;
        """)
        input_layout.addWidget(self.code_input)
        layout.addWidget(self.input_area)
        
        layout.addSpacing(30)
        
        # Glowy Analyze Button
        self.btn_start = QPushButton("ΑΝΑΛΥΣΗ ΤΩΡΑ")
        self.btn_start.setFixedSize(250, 60)
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff4d4d, stop:1 #ff8080);
                color: white;
                border-radius: 30px;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff3333, stop:1 #ff6666);
                box-shadow: 0 0 20px rgba(255, 77, 77, 0.5);
            }
        """)
        self.btn_start.clicked.connect(self.on_analyze_clicked)
        layout.addWidget(self.btn_start, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()

    def on_analyze_clicked(self):
        code = self.code_input.toPlainText()
        if code:
            self.analyzeRequested.emit(code)

class AnalysisView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Use a Splitter for resizable panels
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 1. Left Panel (Control Center)
        self.left_panel = QFrame()
        self.left_panel.setMinimumWidth(300)
        self.left_panel.setObjectName("ControlCenter")
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        left_layout.addWidget(QLabel("CONTROL CENTER"))
        
        # Sensitivity Slider
        left_layout.addWidget(QLabel("SENSITIVITY"))
        from PyQt6.QtWidgets import QSlider
        self.sensitivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.sensitivity_slider.setRange(1, 100)
        self.sensitivity_slider.setValue(50)
        left_layout.addWidget(self.sensitivity_slider)
        
        left_layout.addSpacing(20)
        
        # Scan Button
        self.btn_scan = QPushButton("🚀 RUN SCAN")
        self.btn_scan.setObjectName("ScanButton")
        self.btn_scan.setMinimumHeight(50)
        self.btn_scan.setStyleSheet("""
            QPushButton#ScanButton {
                background-color: #ff4d4d;
                color: white;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton#ScanButton:hover {
                background-color: #ff3333;
            }
        """)
        self.btn_scan.clicked.connect(self.start_scan)
        left_layout.addWidget(self.btn_scan)
        
        left_layout.addStretch()
        
        # 2. Center Panel (Editor)
        self.center_panel = QFrame()
        self.center_panel.setMinimumWidth(500)
        self.center_panel.setObjectName("CodeEditorContainer")
        center_layout = QVBoxLayout(self.center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        self.editor = CodeEditor()
        center_layout.addWidget(self.editor)
        
        # 3. Right Panel (Audit Log)
        self.right_panel = QFrame()
        self.right_panel.setMinimumWidth(400) # Increased for stability
        self.right_panel.setObjectName("AuditLog")
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        right_layout.addWidget(QLabel("AUDIT LOG"))
        
        from PyQt6.QtWidgets import QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")
        
        self.findings_container = QWidget()
        self.findings_layout = QVBoxLayout(self.findings_container)
        self.findings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.findings_container)
        
        right_layout.addWidget(self.scroll_area)
        
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.center_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setStretchFactor(1, 2) 
        self.splitter.setCollapsible(0, False) # Don't collapse control center
        self.splitter.setCollapsible(1, False) # Don't collapse editor
        self.splitter.setCollapsible(2, False) # Don't collapse audit log
        
        layout.addWidget(self.splitter)

    def start_scan(self):
        content = self.editor.toPlainText()
        if not content: return
        
        self.btn_scan.setEnabled(False)
        self.btn_scan.setText("SCANNING...")
        
        # Clear previous findings
        while self.findings_layout.count():
            child = self.findings_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()
            
        self.worker = AnalysisWorker(
            content, 
            "auto", 
            "pasted_code.c", # Use .c as hint but auto will override
            settings={"sensitivity": self.sensitivity_slider.value()}
        )
        self.worker.finished.connect(self.on_scan_finished)
        self.worker.start()

    def on_scan_finished(self, result):
        self.btn_scan.setEnabled(True)
        self.btn_scan.setText("🚀 RUN SCAN")
        
        # Add Summary
        summary = SummaryWidget(result)
        self.findings_layout.addWidget(summary)
        
        # Add Finding Cards
        for pillar in result.pillars:
            for finding in pillar.findings:
                if finding.type == "humanity.shield": continue 
                card = FindingCard(finding)
                card.clicked.connect(self.on_finding_clicked)
                self.findings_layout.addWidget(card)

    def on_finding_clicked(self, finding):
        self.editor.goto_line(finding.line)
        
        # Show educational popup
        from gui.widgets import EducationalPopup
        if hasattr(self, 'current_popup'):
            self.current_popup.hide()
            
        self.current_popup = EducationalPopup(finding, self)
        
        # Smart Positioning Logic
        cursor_rect = self.editor.cursorRect()
        global_pos = self.editor.mapToGlobal(cursor_rect.bottomRight())
        
        # Get screen geometry to prevent clipping
        screen = self.screen().availableGeometry()
        popup_width = self.current_popup.width()
        popup_height = self.current_popup.sizeHint().height()
        
        # If too far right, shift left
        if global_pos.x() + popup_width > screen.right():
            global_pos.setX(screen.right() - popup_width - 20)
            
        # If too far down, show ABOVE the cursor
        if global_pos.y() + popup_height > screen.bottom():
            global_pos.setY(global_pos.y() - popup_height - cursor_rect.height() - 10)
            
        self.current_popup.move(global_pos)
        self.current_popup.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Papatzis Spotter V3 - The Slop Buster")
        self.setMinimumSize(1280, 720) # 720p Minimum as per brainstorming
        
        # Main Container
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Add Top Nav
        self.nav_bar = TopNavBar()
        self.main_layout.addWidget(self.nav_bar)
        
        # Add Stacked Widget for different views
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # Initialize Views
        self.home_view = HomeView()
        self.analysis_view = AnalysisView()
        
        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.analysis_view)
        
        # Connect Signals
        self.home_view.analyzeRequested.connect(self.start_global_analysis)
        self.nav_bar.btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.nav_bar.btn_analyze.clicked.connect(lambda: self.stack.setCurrentIndex(1))

    def start_global_analysis(self, code):
        # 1. Set code in editor
        self.analysis_view.editor.setPlainText(code)
        # 2. Switch to IDE view
        self.stack.setCurrentIndex(1)
        # 3. Trigger scan
        self.analysis_view.start_scan()
        
        # Style (Basic Dark Theme)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Segoe UI', sans-serif;
            }
            #TopNavBar {
                background-color: #1e1e1e;
                border-bottom: 1px solid #333;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                color: #b0b0b0;
            }
            QPushButton:hover {
                color: #ff4d4d;
            }
            QFrame#ControlCenter, QFrame#AuditLog {
                background-color: #181818;
                border: 1px solid #282828;
            }
            QFrame#CodeEditorContainer {
                background-color: #1e1e1e;
            }
            QLabel {
                font-weight: bold;
                padding: 10px;
            }
        """)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
