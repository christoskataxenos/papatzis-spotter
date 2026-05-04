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
        elif language_id == "python":
            self.lang = tree_sitter_language_pack.get_language(language_id)
            self.malloc_query = None
            self.struct_query = None
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
        
        content = source_code.decode('utf8', errors='ignore')
        
        if self.language == "python":
            self._analyze_python(tree.root_node, source_code, file_path)
            return self.findings

        if self.language != "c":
            return self.findings
            
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
                            
                            # Μειωμένη ποινή αν είναι τυπικό struct allocation (academic)
                            text = node.text.decode('utf8', errors='ignore')
                            # Handle sizeof(Type), sizeof(struct Type), and variants
                            is_academic_struct = "sizeof" in text and re.search(r'sizeof\s*\(?\s*(struct\s+|[A-Z][a-zA-Z0-9_]*|[a-z_]+_t)', text)
                            
                            if is_academic_struct:
                                continue # Honest Code: Standard pattern for data structures
                            
                            severity = 4.0
                            confidence = 0.85

                            malloc_found_lines.add(line)
                            from analyzer.i18n import translate
                            t_data = translate("logic.heap_abuse", ui_lang=self.ui_lang)
                            self.findings.append(Finding(
                                type="logic.heap_abuse",
                                file=file_path, line=line, severity=severity, confidence=confidence,
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

    def _analyze_python(self, root_node: Node, source_code: bytes, file_path: str):
        from analyzer.i18n import translate

        # Define expensive functions and redundant casts
        expensive_funcs = {"copy.deepcopy", "time.sleep", "requests.get", "requests.post", "requests.put", "urllib.request.urlopen"}
        redundant_casts = {"str", "list", "set", "int", "float", "bool", "dict", "tuple"}

        def get_text(node):
            if not node: return ""
            return source_code[node.start_byte:node.end_byte].decode('utf8', errors='ignore')

        def visit(node: Node, depth: int = 0, inside_loop: bool = False):
            current_inside_loop = inside_loop
            
            # 1. Check for Loop
            if node.type in ("for_statement", "while_statement"):
                current_inside_loop = True

            # 2. Check for "Arrow of Code" (Hadouken) -> Deep Nesting
            if node.type in ("if_statement", "for_statement", "while_statement", "try_statement"):
                # If depth > 3, it's Hadouken
                if depth > 3:
                    t_data = translate("structural.hadouken", ui_lang=self.ui_lang, depth=depth)
                    self.findings.append(Finding(
                        type="structural.hadouken",
                        file=file_path, line=node.start_point[0] + 1, severity=3.5, confidence=0.8,
                        **t_data
                    ))

            # 3. Check for God Functions
            if node.type == "function_definition":
                body = node.child_by_field_name('body')
                if body and body.type == "block":
                    statements = [c for c in body.children if c.is_named]
                    if len(statements) > 50:
                        t_data = translate("structural.god_function", ui_lang=self.ui_lang, statements=len(statements))
                        self.findings.append(Finding(
                            type="structural.god_function",
                            file=file_path, line=node.start_point[0] + 1, severity=3.0, confidence=0.85,
                            **t_data
                        ))

            # Checks only applicable inside loops
            if current_inside_loop:
                # 4. Expensive Function Calls and Redundant Casts
                if node.type == "call":
                    func_node = node.child_by_field_name('function')
                    if func_node:
                        func_name = get_text(func_node)
                        if func_name in expensive_funcs:
                            t_data = translate("logic.expensive_loop", ui_lang=self.ui_lang, call_name=func_name)
                            self.findings.append(Finding(
                                type="logic.expensive_loop",
                                file=file_path, line=node.start_point[0] + 1, severity=5.0, confidence=0.9,
                                **t_data
                            ))
                        elif func_name in redundant_casts:
                            t_data = translate("logic.redundant_cast", ui_lang=self.ui_lang, cast_type=func_name)
                            self.findings.append(Finding(
                                type="logic.redundant_cast",
                                file=file_path, line=node.start_point[0] + 1, severity=2.5, confidence=0.7,
                                **t_data
                            ))

                # 5. List Concatenation in Loop
                if node.type == "assignment":
                    right = node.child_by_field_name('right')
                    if right and right.type == "binary_operator":
                        operator = right.child_by_field_name('operator')
                        if operator and get_text(operator) == "+":
                            left_op = right.child_by_field_name('left')
                            right_op = right.child_by_field_name('right')
                            if (left_op and left_op.type == "list") or (right_op and right_op.type == "list"):
                                t_data = translate("logic.list_concat", ui_lang=self.ui_lang)
                                self.findings.append(Finding(
                                    type="logic.list_concat",
                                    file=file_path, line=node.start_point[0] + 1, severity=4.0, confidence=0.8,
                                    **t_data
                                ))

            # Recursively visit children
            next_depth = depth + 1 if node.type in ("if_statement", "for_statement", "while_statement", "try_statement") else depth
            for child in node.children:
                visit(child, next_depth, current_inside_loop)

        visit(root_node)

