import re
from typing import List
from analyzer.models import Finding

class GenericAnalyzer:
    """
    Αναλυτής για γλώσσες χωρίς AST υποστήριξη.
    Χρησιμοποιεί Regex για τον εντοπισμό σχολίων και patterns.
    """
    def __init__(self):
        self.findings: List[Finding] = []
        # GPT typical verbosity
        self.ai_phrases = [
            "this function", "in this code", "the purpose of",
            "this block", "firstly", "secondly", "overall",
            "in summary", "as we can see", "calculates the",
            "note that", "we are using", "this function processes",
            "the provided", "performing some", "basic filtering",
            "returns the result"
        ]

    def analyze(self, content: str, file_path: str) -> List[Finding]:
        self.findings = []
        lines = content.splitlines()
        
        # Εντοπισμός σχολίων (Generic: #, //, /* */)
        # Σημείωση: Πολύ απλοϊκό, μπορεί να πιάσει σχόλια μέσα σε strings
        for i, line in enumerate(lines):
            line_num = i + 1
            clean_line = line.strip()
            
            # AI Phrases check on the whole line
            lower_line = clean_line.lower()
            for phrase in self.ai_phrases:
                if phrase in lower_line:
                    self.findings.append(Finding(
                        type="comments.ai_style",
                        file=file_path,
                        line=line_num,
                        severity=2.0,
                        confidence=0.6,
                        message="Εντοπίστηκε πιθανό AI pattern σε αυτό το σημείο.",
                        human_alternative="Αποφύγετε τις τυπικές φράσεις εισαγωγής του ChatGPT.",
                        rationale=f"Η φράση '{phrase}' είναι πολύ συνηθισμένη σε αυτόματα παραγόμενο κώδικα."
                    ))

            # Generic Naming check
            # Ψάχνουμε για data1, val2 κλπ σε απλά assignments (id = val)
            names = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*[0-9]+)\b\s*=', clean_line)
            for name in names:
                self.findings.append(Finding(
                    type="naming.generic",
                    file=file_path,
                    line=line_num,
                    severity=1.2,
                    confidence=0.5,
                    message=f"Πιθανό σειριακό όνομα: '{name}'",
                    human_alternative="Δώστε πιο περιγραφικά ονόματα στις μεταβλητές σας.",
                    rationale="Η αρίθμηση μεταβλητών είναι ένδειξη slop."
                ))

        return self.findings
