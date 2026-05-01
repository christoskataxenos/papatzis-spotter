import tree_sitter_language_pack
from tree_sitter import Tree, Query, QueryCursor
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding
from typing import List
import re

class SuspicionAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str):
        super().__init__(language_id)
        self.lang = tree_sitter_language_pack.get_language(language_id)
        
        if language_id == "python":
            self.ai_signature_query = Query(self.lang, "(function_definition) @func")
            self.class_query = Query(self.lang, "(class_definition) @class")
        else:
            self.ai_signature_query = None
            self.class_query = None

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        source_text = source_code.decode('utf8', errors='ignore')
        
        # 1. Boilerplate Density (Phase 2.1)
        # Ratio of Comments + Docstrings to actual Logic
        comment_chars = 0
        def find_docs(n):
            nonlocal comment_chars
            if n.type in ("comment", "string"):
                # If it's a string, check if it's used as a docstring
                is_doc = False
                if n.type == "string":
                    p = n.parent
                    if (p.type == "expression_statement" and p.parent.type == "block") or p.type == "block":
                        is_doc = True
                if n.type == "comment" or is_doc:
                    comment_chars += len(n.text)
            for c in n.children: find_docs(c)
        
        find_docs(tree.root_node)
        total_chars = len(source_text)
        code_chars = total_chars - comment_chars
        
        if total_chars > 200:
            ratio = comment_chars / max(1, code_chars)
            if ratio > 2.5: # 2.5x more comments than code is very "Slop-y"
                self.findings.append(Finding(
                    type="suspicion.boilerplate_density",
                    file=file_path,
                    line=1,
                    severity=2.0,
                    confidence=0.8,
                    message=f"Statistical Verbiage (Ratio: {ratio:.1f}x)",
                    human_alternative="Αφαίρεσε τα αυτονόητα σχόλια. Αν ο κώδικας είναι `x = 5`, δεν χρειάζεται docstring 10 γραμμών που να εξηγεί την έννοια της ανάθεσης τιμής.",
                    rationale="Τα AI μοντέλα 'πληρώνονται' (μεταφορικά) για να είναι ομιλητικά. Συχνά παράγουν τεράστιες επεξηγήσεις για πολύ απλό κώδικα, κάτι που ένας έμπειρος προγραμματιστής αποφεύγει για να μην 'θάψει' την ουσία."
                ))

        # 2. Architecture Overkill (Phase 2.2)
        # Looking for Factory/Manager/Protocol for trivial files
        enterprise_matches = re.findall(r"(manager|factory|protocol|strategy|orchestrator|protocol|synergistic)", source_text.lower())
        if len(enterprise_matches) >= 3 and total_chars < 1500:
            # Check if there's actually complex logic
            logical_ops = re.findall(r"(\+|\-|\*|\/|\%|==|!=|>|<|and|or|not|if|for|while)", source_text)
            if len(logical_ops) < 10:
                self.findings.append(Finding(
                    type="suspicion.architecture_overkill",
                    file=file_path,
                    line=1,
                    severity=2.5,
                    confidence=0.9,
                    message="Architecture Overkill (Logic 8/Boilerplate 147)",
                    human_alternative="Keep it Simple. Μην χτίζεις 'καθεδρικούς ναούς' (Managers, Factories) για να λύσεις ένα πρόβλημα που λύνεται με μια απλή συνάρτηση 5 γραμμών.",
                    rationale="Είναι το κλασικό φαινόμενο του AI: προσπαθεί να εντυπωσιάσει εφαρμόζοντας enterprise patterns (όπως το Factory Pattern) ακόμα και σε ένα απλό script, κάνοντας τον κώδικα δυσκίνητο και 'ρομποτικό'."
                ))

        # 3. AI Intro/Outro Filler
        intro_patterns = [
            r"as an ai language model",
            r"absolutely thrilled to provide",
            r"comprehensive.*solution",
            r"here is the.*robust",
            r"optimized for synergistic",
            r"in conclusion",
            r"hope this helps"
        ]
        for pat in intro_patterns:
            if re.search(pat, source_text.lower()):
                self.findings.append(Finding(
                    type="suspicion.ai_filler",
                    file=file_path,
                    line=1,
                    severity=3.0,
                    confidence=1.0,
                    message="AI Fingerprint Detected (Intro/Outro)",
                    human_alternative="Διέγραψε αμέσως αυτές τις φράσεις. Προδίδουν ότι ο κώδικας είναι copy-paste από chat και δεν έχει ελεγχθεί από άνθρωπο.",
                    rationale="Φράσεις όπως 'As an AI language model' ή 'Hope this helps' είναι η απόλυτη 'σφραγίδα' του AI. Η παρουσία τους στον κώδικα δείχνει έλλειψη προσοχής στη λεπτομέρεια."
                ))

        return self.findings
