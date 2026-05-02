import tree_sitter_language_pack
from tree_sitter import Tree, Query, QueryCursor, Node
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding
from typing import List
import re

class LogicAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str, ui_lang: str = "EN"):
        super().__init__(language_id, ui_lang=ui_lang)
        if language_id == "c":
            self.lang = tree_sitter_language_pack.get_language(language_id)
            
            try:
                # Capture the whole call expression for malloc
                self.malloc_query = Query(self.lang, """
                    (call_expression
                        function: (identifier) @f
                        (#eq? @f "malloc")
                    ) @malloc_call
                """)
            except:
                self.malloc_query = None

            try:
                # Capture struct declarations that look like Java entities
                self.struct_query = Query(self.lang, """
                    (struct_specifier
                        name: (type_identifier) @name
                    ) @struct
                """)
            except:
                self.struct_query = None

            try:
                # AST pattern for manual loops
                self.manual_loop_query = Query(self.lang, """
                    (while_statement
                        condition: (parenthesized_expression
                            (binary_expression
                                left: (subscript_expression)
                                right: [ (char_literal) (number_literal) ]
                            )
                        )
                    ) @manual_loop
                    (for_statement
                        condition: (binary_expression
                            left: (subscript_expression)
                            right: [ (char_literal) (number_literal) ]
                        )
                    ) @manual_loop
                """)
            except:
                self.manual_loop_query = None
        else:
            self.malloc_query = None
            self.struct_query = None
            self.manual_loop_query = None

    def _normalize_captures(self, raw_captures):
        if isinstance(raw_captures, dict):
            return raw_captures
        if isinstance(raw_captures, list):
            captures = {}
            for node, tag in raw_captures:
                if tag not in captures: captures[tag] = []
                captures[tag].append(node)
            return captures
        return {}

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        if self.language != "c":
            return self.findings
            
        content = source_code.decode('utf8', errors='ignore')
        ast_found_lines = set()

        # --- 1. Manual strlen loops ---
        # Try AST first
        if self.manual_loop_query:
            try:
                cursor = QueryCursor(self.manual_loop_query)
                captures = self._normalize_captures(cursor.captures(tree.root_node))
                for tag, nodes in captures.items():
                    if tag == "manual_loop":
                        for node in nodes:
                            text = node.text.decode('utf8', errors='ignore')
                            if "'\\0'" in text or "0" in text:
                                line = node.start_point[0] + 1
                                ast_found_lines.add(line)
                                from analyzer.i18n import translate
                                t_data = translate("logic.manual_strlen", ui_lang=self.ui_lang)
                                self.findings.append(Finding(
                                    type="logic.manual_strlen",
                                    file=file_path, line=line, severity=3.5, confidence=0.95,
                                    **t_data
                                ))
            except: pass

        # Regex Fallback for things AST might miss (very reliable)
        strlen_patterns = [
            r"while\s*\(\s*.*\[.*\]\s*!=\s*['\"]\\0['\"]\s*\)",
            r"while\s*\(\s*.*\[.*\]\s*!=\s*0\s*\)",
            r"while\s*\(\s*\*.*\+\+\s*\)"
        ]
        for pattern in strlen_patterns:
            for match in re.finditer(pattern, content):
                line_num = content.count('\n', 0, match.start()) + 1
                if line_num not in ast_found_lines:
                    from analyzer.i18n import translate
                    t_data = translate("logic.manual_strlen", ui_lang=self.ui_lang)
                    self.findings.append(Finding(
                        type="logic.manual_strlen",
                        file=file_path, line=line_num, severity=3.5, confidence=0.9,
                        **t_data
                    ))

        # --- 2. Malloc detection ---
        malloc_found_lines = set()
        if self.malloc_query:
            try:
                cursor = QueryCursor(self.malloc_query)
                captures = self._normalize_captures(cursor.captures(tree.root_node))
                for tag, nodes in captures.items():
                    if tag == "malloc_call":
                        for node in nodes:
                            line = node.start_point[0] + 1
                            malloc_found_lines.add(line)
                            from analyzer.i18n import translate
                            t_data = translate("logic.heap_abuse", ui_lang=self.ui_lang)
                            self.findings.append(Finding(
                                type="logic.heap_abuse",
                                file=file_path, line=line, severity=4.0, confidence=0.85,
                                **t_data
                            ))
            except: pass

        if not malloc_found_lines and "malloc(" in content:
            from analyzer.i18n import translate
            t_data = translate("logic.heap_abuse", ui_lang=self.ui_lang)
            self.findings.append(Finding(
                type="logic.heap_abuse",
                file=file_path, line=1, severity=3.0, confidence=0.6,
                **t_data
            ))

        # --- 3. Java-fication (Struct Naming) ---
        if self.struct_query:
            try:
                cursor = QueryCursor(self.struct_query)
                captures = self._normalize_captures(cursor.captures(tree.root_node))
                for tag, nodes in captures.items():
                    if tag == "struct":
                        for node in nodes:
                            text = node.text.decode('utf8', errors='ignore').lower()
                            if any(x in text for x in ["entity", "result", "status", "response", "data", "info"]):
                                from analyzer.i18n import translate
                                t_data = translate("logic.javafication", ui_lang=self.ui_lang)
                                self.findings.append(Finding(
                                    type="logic.javafication",
                                    file=file_path, line=node.start_point[0] + 1, severity=3.0, confidence=0.75,
                                    **t_data
                                ))
            except: pass

        return self.findings

