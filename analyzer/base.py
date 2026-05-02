from abc import ABC, abstractmethod
from typing import List
from tree_sitter import Tree
from analyzer.models import Finding

class BaseAnalyzer(ABC):
    def __init__(self, language: str, ui_lang: str = "EN"):
        self.language = language
        self.ui_lang = ui_lang
        self.findings: List[Finding] = []

    @abstractmethod
    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        """
        Εκτελεί την ανάλυση στο AST και επιστρέφει λίστα με ευρήματα.
        """
        pass

    def clear(self):
        self.findings = []
