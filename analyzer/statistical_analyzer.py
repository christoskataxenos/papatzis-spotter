import math
import re
from typing import List, Dict
from tree_sitter import Tree
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding

class StatisticalAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str, ui_lang: str = "EN"):
        super().__init__(language_id, ui_lang=ui_lang)

    def _calculate_entropy(self, text: str) -> float:
        """
        Υπολογίζει την Shannon Entropy σε επίπεδο χαρακτήρων.
        """
        if not text:
            return 0.0
        
        counts = {}
        for char in text:
            counts[char] = counts.get(char, 0) + 1
            
        entropy = 0.0
        total = len(text)
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def _calculate_token_entropy(self, tokens: List[str]) -> float:
        """
        Υπολογίζει την Shannon Entropy σε επίπεδο tokens.
        """
        if not tokens:
            return 0.0
            
        counts = {}
        for token in tokens:
            counts[token] = counts.get(token, 0) + 1
            
        entropy = 0.0
        total = len(tokens)
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        
        source_text = source_code.decode('utf8', errors='ignore')
        lines = source_text.splitlines()
        
        # Εξαιρούμε κοινές λέξεις-κλειδιά και built-ins για να μην επηρεάζουν τη στατιστική ανάλυση
        whitelists = {
            "c": {
                "include", "define", "ifdef", "ifndef", "endif", "int", "char", "float", "double", "void", "static", "const", "return", "if", "else", "for", "while", "do", "switch", "case", "break", "continue", "struct", "typedef", "sizeof", "printf", "scanf",
                "stdio", "stdlib", "math", "string", "time", "ctype", "stdbool", "stdint", "malloc", "free", "strlen", "strcpy", "strcmp", "sqrt", "pow", "memset", "memcpy"
            },
            "python": {
                "def", "class", "elif", "try", "except", "finally", "from", "as", "with", "lambda", "yield", "pass", "in", "is", "not", "and", "or", "none", "true", "false", "print", "self", "import", "list", "dict", "set", "tuple", "str", "range", "len", "type", "isinstance",
                "os", "sys", "json", "re", "math", "datetime", "time", "random", "pathlib", "logging", "append", "join", "split", "strip", "replace", "format", "open", "read", "write"
            },
            "generic": {
                # Master Whitelist for common keywords across languages (Web, Enterprise, Academic pseudocode)
                "if", "else", "for", "while", "return", "function", "var", "let", "const", "class", "async", "await", "import", "export", "from",
                "try", "catch", "finally", "throw", "new", "this", "super", "null", "undefined", "true", "false", "public", "private", "protected",
                "interface", "implements", "extends", "package", "namespace", "use", "using", "include", "require", "module", "static", "void",
                "int", "string", "bool", "boolean", "float", "double", "list", "map", "set", "print", "log", "console", "echo", "system", "out",
                "select", "insert", "update", "delete", "where", "into", "values", "create", "table", "null", "primary", "key"
            }
        }
        
        # Select the correct whitelist, falling back to "generic"
        current_whitelist = whitelists.get(self.language.lower(), whitelists["generic"])
        
        raw_tokens = re.findall(r'\w+', source_text)
        tokens = [t for t in raw_tokens if t.lower() not in current_whitelist and len(t) > 1]
        
        # --- 1. Shannon Entropy Analysis (Phase 2.1) ---
        # Υπολογίζουμε την εντροπία ολόκληρου του αρχείου
        token_entropy = self._calculate_token_entropy(tokens)
        
        # Heuristic: Τα LLMs παράγουν κώδικα με χαμηλή "εντροπία λεξιλογίου" 
        # (συχνή χρήση των ίδιων λέξεων/δομών).
        if 2.5 < token_entropy < 5.2 and len(tokens) > 50:
            from analyzer.i18n import translate
            t_data = translate("statistical.low_token_entropy", ui_lang=self.ui_lang, token_entropy=f"{token_entropy:.2f}")
            self.findings.append(Finding(
                type="statistical.low_entropy",
                file=file_path,
                line=0, # Global finding
                severity=0.6,
                confidence=0.8,
                **t_data
            ))

        # --- 2. Burstiness & Variance Analysis (Phase 2.2) ---
        line_lengths = [len(l.strip()) for l in lines if l.strip()]
        if len(line_lengths) > 8:
            mean_len = sum(line_lengths) / len(line_lengths)
            variance = sum((l - mean_len) ** 2 for l in line_lengths) / len(line_lengths)
            std_dev = math.sqrt(variance)
            
            # Αν η τυπική απόκλιση στο μήκος των γραμμών είναι πολύ χαμηλή, 
            # ο κώδικας είναι "επίπεδος" (flat), σήμα AI.
            if std_dev < 12.0 and mean_len > 15:
                from analyzer.i18n import translate
                t_data = translate("statistical.low_burstiness", ui_lang=self.ui_lang, std_dev=f"{std_dev:.2f}")
                self.findings.append(Finding(
                    type="statistical.low_burstiness",
                    file=file_path,
                    line=0, # Global finding
                    severity=0.6,
                    confidence=0.7,
                    **t_data
                ))

        # --- 3. N-gram Repetition (Phase 2.3) ---
        # Αναζητούμε επαναλαμβανόμενες ακολουθίες 3 tokens
        if len(tokens) > 20:
            ngrams = {}
            for i in range(len(tokens) - 2):
                ngram = tuple(tokens[i:i+3])
                ngrams[ngram] = ngrams.get(ngram, 0) + 1
            
            # Αν κάποιο n-gram επαναλαμβάνεται υπερβολικά σε μικρά αρχεία
            top_repeats = [count for count in ngrams.values() if count > 4]
            if len(top_repeats) > 2:
                from analyzer.i18n import translate
                t_data = translate("statistical.high_repetition", ui_lang=self.ui_lang)
                self.findings.append(Finding(
                    type="statistical.high_repetition",
                    file=file_path,
                    line=0, # Global finding
                    severity=0.5,
                    confidence=0.6,
                    **t_data
                ))

        return self.findings
