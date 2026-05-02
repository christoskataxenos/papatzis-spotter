import tree_sitter_language_pack
from tree_sitter import Tree, Query, QueryCursor
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding
from typing import List
import re

class SuspicionAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str, ui_lang: str = "EN"):
        super().__init__(language_id, ui_lang=ui_lang)
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
                from analyzer.i18n import translate
                t_data = translate("suspicion.verbosity", ui_lang=self.ui_lang)
                self.findings.append(Finding(
                    type="suspicion.boilerplate_density",
                    file=file_path,
                    line=0,
                    severity=2.0,
                    confidence=0.8,
                    **t_data
                ))

        # 2. Architecture Overkill (Phase 2.2)
        # Looking for Factory/Manager/Protocol for trivial files
        enterprise_matches = re.findall(r"(manager|factory|protocol|strategy|orchestrator|protocol|synergistic)", source_text.lower())
        if len(enterprise_matches) >= 3 and total_chars < 1500:
            # Check if there's actually complex logic
            logical_ops = re.findall(r"(\+|\-|\*|\/|\%|==|!=|>|<|and|or|not|if|for|while)", source_text)
            if len(logical_ops) < 10:
                from analyzer.i18n import translate
                t_data = translate("suspicion.abstraction_slop", ui_lang=self.ui_lang)
                self.findings.append(Finding(
                    type="suspicion.architecture_overkill",
                    file=file_path,
                    line=0,
                    severity=2.5,
                    confidence=0.9,
                    **t_data
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
                from analyzer.i18n import translate
                t_data = translate("suspicion.chat_boilerplate", ui_lang=self.ui_lang)
                self.findings.append(Finding(
                    type="suspicion.ai_filler",
                    file=file_path,
                    line=0,
                    severity=3.0,
                    confidence=1.0,
                    **t_data
                ))

        return self.findings
