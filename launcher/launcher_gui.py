import sys
import multiprocessing
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    # Required for Windows multiprocessing when bundled
    multiprocessing.freeze_support()
    
    # Optional: Set app-wide styles or icons
    app = QApplication(sys.argv)
    app.setApplicationName("Papatzis Spotter V3")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
