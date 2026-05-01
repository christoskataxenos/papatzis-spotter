import os
import multiprocessing
from PyQt6.QtCore import QThread, pyqtSignal
from analyzer.slop_engine import SlopEngine
from analyzer.models import AnalysisResult, Finding

class AnalysisWorker(QThread):
    finished = pyqtSignal(AnalysisResult)
    progress = pyqtSignal(int)
    
    def __init__(self, content, lang, file_path, settings=None):
        super().__init__()
        self.content = content
        self.lang = lang
        self.file_path = file_path
        self.settings = settings or {}

    def run(self):
        # Αρχικοποίηση της μηχανής ανάλυσης
        engine = SlopEngine()
        from analyzer.scoring_engine import ScoringEngine
        engine.scorer = ScoringEngine(
            sensitivity=self.settings.get("sensitivity", 50),
            humanity_shield=self.settings.get("humanity_shield", True)
        )
        
        # Εκτέλεση της ανάλυσης (Sequential but within the worker thread)
        # Χρησιμοποιούμε "auto" για την ανίχνευση γλώσσας αν δεν έχει οριστεί
        result = engine.analyze(self.content, self.lang, self.file_path, settings=self.settings)
        
        # Ενημέρωση του UI
        self.progress.emit(100)
        self.finished.emit(result)
