import math
import re
from typing import List, Dict, Set
from tree_sitter import Tree
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding

class SemanticAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str, ui_lang: str = "EN"):
        super().__init__(language_id, ui_lang=ui_lang)
        # Λέξεις που αγνοούμε στην ανάλυση ομοιότητας
        self.stop_words = {
            "def", "class", "return", "if", "else", "elif", "for", "while", "import", "from", "as", "try", "except", "finally", 
            "self", "this", "the", "of", "and", "or", "in", "is", "not", "with", "lambda", "yield", "pass", "None", "True", "False",
            "select", "insert", "update", "delete", "where", "from", "into", "values", "create", "table",
            "stdio", "stdlib", "math", "string", "malloc", "free", "strlen", "printf", "scanf",
            "os", "sys", "json", "re", "datetime", "append", "join", "split", "open"
        }

    def _get_word_freq(self, text: str) -> Dict[str, int]:
        # Χρήση regex για εξαγωγή λέξεων και split underscores για snake_case
        raw_words = re.findall(r'\w+', text)
        words = []
        for rw in raw_words:
            # Split snake_case
            parts = rw.split('_')
            for p in parts:
                if p.lower() not in self.stop_words and len(p) > 1:
                    words.append(p.lower())
        
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return freq

    def _cosine_similarity(self, freq1: Dict[str, int], freq2: Dict[str, int]) -> float:
        all_words = set(freq1.keys()).union(set(freq2.keys()))
        dot_product = sum(freq1.get(w, 0) * freq2.get(w, 0) for w in all_words)
        mag1 = math.sqrt(sum(v**2 for v in freq1.values()))
        mag2 = math.sqrt(sum(v**2 for v in freq2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0
        return dot_product / (mag1 * mag2)

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        
        # 3.1 Semantic Uniformity Check (Similarity between functions)
        functions_text = []
        
        # Traverse for function definitions
        def find_funcs(node):
            if node.type in ("function_definition", "function_declaration"):
                text = source_code[node.start_byte:node.end_byte].decode('utf-8', errors='ignore')
                functions_text.append(text)
            for child in node.children:
                find_funcs(child)
        
        find_funcs(tree.root_node)
        
        if len(functions_text) >= 2:
            similarities = []
            freqs = [self._get_word_freq(t) for t in functions_text]
            
            for i in range(len(freqs)):
                for j in range(i + 1, len(freqs)):
                    sim = self._cosine_similarity(freqs[i], freqs[j])
                    similarities.append(sim)
            
            if similarities:
                avg_sim = sum(similarities) / len(similarities)
                
                # Πολύ υψηλή ομοιότητα μεταξύ διαφορετικών functions
                if avg_sim > 0.55: # Μειώσαμε το threshold για μεγαλύτερη ευαισθησία (Ph5)
                    from analyzer.i18n import translate
                    t_data = translate("semantic.high_uniformity", ui_lang=self.ui_lang, avg_sim=f"{avg_sim:.2%}")
                    self.findings.append(Finding(
                        type="semantic.high_uniformity",
                        file=file_path,
                        line=0,
                        severity=0.7,
                        confidence=0.7,
                        **t_data
                    ))
                    
                # Ανίχνευση "Template Functions" (Ph5)
                # Αν πολλές συναρτήσεις έχουν ακριβώς το ίδιο πλήθος λέξεων/δομή
                if any(sim > 0.95 for sim in similarities):
                    from analyzer.i18n import translate
                    t_data = translate("semantic.template_functions", ui_lang=self.ui_lang)
                    self.findings.append(Finding(
                        type="semantic.template_functions",
                        file=file_path,
                        line=0,
                        severity=0.8,
                        confidence=0.9,
                        **t_data
                    ))

        return self.findings
