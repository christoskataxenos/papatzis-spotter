from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

class FindingCard(QFrame):
    clicked = pyqtSignal(object) # Emits the Finding object
    
    def __init__(self, finding, parent=None):
        super().__init__(parent)
        self.finding = finding
        self.setObjectName("FindingCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Severity-based styling
        border_color = "#333"
        if finding.severity >= 2.5: border_color = "#ff4d4d" # Red
        elif finding.severity >= 1.5: border_color = "#ffa500" # Orange
        elif finding.severity >= 0.5: border_color = "#ffeb3b" # Yellow
        
        self.setStyleSheet(f"""
            QFrame#FindingCard {{
                background-color: #1a1a1a;
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 8px;
            }}
            QFrame#FindingCard:hover {{
                background-color: #252525;
                border: 2px solid {border_color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        # Header: Type & Line
        header = QHBoxLayout()
        type_lbl = QLabel(finding.type.upper())
        type_lbl.setStyleSheet("font-size: 10px; color: #888; font-weight: bold;")
        line_lbl = QLabel(f"LINE {finding.line}")
        line_lbl.setStyleSheet("font-size: 10px; color: #888;")
        
        header.addWidget(type_lbl)
        header.addStretch()
        header.addWidget(line_lbl)
        layout.addLayout(header)
        
        # Message
        msg_lbl = QLabel(finding.message)
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet("font-weight: bold; font-size: 13px; color: #fff;")
        layout.addWidget(msg_lbl)
        
        # Rationale (Brief)
        rat_lbl = QLabel(finding.rationale)
        rat_lbl.setWordWrap(True)
        rat_lbl.setStyleSheet("font-size: 11px; color: #aaa; font-style: italic;")
        layout.addWidget(rat_lbl)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.finding)
        super().mousePressEvent(event)

class SummaryWidget(QFrame):
    def __init__(self, result, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 10px;
                border: 1px solid #333;
            }
        """)
        layout = QVBoxLayout(self)
        
        score_lbl = QLabel(str(int(result.final_score)))
        score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_lbl.setStyleSheet(f"font-size: 48px; font-weight: bold; color: {self.get_score_color(result.final_score)};")
        layout.addWidget(score_lbl)
        
        title_lbl = QLabel("PAPATZIS SCORE")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setStyleSheet("font-size: 12px; color: #888; font-weight: bold;")
        layout.addWidget(title_lbl)
        
        rank_lbl = QLabel(result.interpretation.upper())
        rank_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rank_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #fff; margin-top: 10px;")
        layout.addWidget(rank_lbl)

    def get_score_color(self, score):
        if score >= 80: return "#ff4d4d"
        if score >= 50: return "#ffa500"
        return "#50fa7b"

class EducationalPopup(QFrame):
    def __init__(self, finding, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)
        self.setObjectName("EducationalPopup")
        
        self.setStyleSheet("""
            QFrame#EducationalPopup {
                background-color: #1e1e1e;
                border: 2px solid #ff4d4d;
                border-radius: 12px;
            }
            QLabel {
                background-color: transparent;
                color: #e0e0e0;
            }
            QLabel#PopupTitle {
                font-size: 18px;
                font-weight: bold;
                color: #ff4d4d;
                padding-bottom: 5px;
            }
            QLabel#PopupRationale {
                color: #b0b0b0;
                font-style: italic;
                font-size: 13px;
                line-height: 1.4;
            }
            QLabel#PopupAlternative {
                color: #50fa7b;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
                border-top: 1px solid #333;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel(f"🤖 {finding.type.split('.')[-1].replace('_', ' ').upper()}")
        title.setObjectName("PopupTitle")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.btn_x = QPushButton("✕") # Better X symbol
        self.btn_x.setFixedSize(24, 24)
        self.btn_x.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_x.setStyleSheet("""
            QPushButton {
                color: #ff4d4d;
                font-size: 16px;
                font-weight: bold;
                background-color: #2a2a2a;
                border: 1px solid #ff4d4d;
                border-radius: 12px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #ff4d4d;
                color: white;
            }
        """)
        self.btn_x.clicked.connect(self.hide)
        header_layout.addWidget(self.btn_x)
        layout.addLayout(header_layout)
        
        # Rationale
        rationale = QLabel(finding.rationale)
        rationale.setObjectName("PopupRationale")
        rationale.setWordWrap(True)
        layout.addWidget(rationale)
        
        layout.addSpacing(5)
        
        # Human Touch Section
        alt_header = QLabel("Η ΑΝΘΡΩΠΙΝΗ ΠΙΝΕΛΙΑ:")
        alt_header.setStyleSheet("color: #50fa7b; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(alt_header)
        
        alternative = QLabel(finding.human_alternative)
        alternative.setObjectName("PopupAlternative")
        alternative.setWordWrap(True)
        layout.addWidget(alternative)
        
        # Bottom Button
        self.btn_close = QPushButton("OK, ΤΟ ΕΠΙΑΣΑ!")
        self.btn_close.setMinimumHeight(35)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4d;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)
        self.btn_close.clicked.connect(self.hide)
        layout.addWidget(self.btn_close)
        
        self.setFixedWidth(450)
        self.adjustSize()
        
        # For Dragging
        self._drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
