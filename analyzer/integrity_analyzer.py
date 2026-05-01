from typing import List, Set
import tree_sitter_language_pack
from tree_sitter import Tree, Parser, Query, QueryCursor
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding

class IntegrityAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str, template_content: str = None):
        super().__init__(language_id)
        self.lang = tree_sitter_language_pack.get_language(language_id)
        self.template_content = template_content
        self.template_identifiers = self._extract_template_identifiers() if template_content else set()

    def _extract_template_identifiers(self) -> Set[str]:
        """Εξαγωγή κρίσιμων identifiers από το template (functions, structs, globals)."""
        parser = Parser(self.lang)
        tree = parser.parse(self.template_content.encode('utf8', errors='ignore'))
        
        if self.language == "python":
            query_str = """
                (function_definition name: (identifier) @id)
                (class_definition name: (identifier) @id)
            """
        else: # C
            query_str = """
                (function_declarator declarator: (identifier) @id)
                (function_declarator declarator: (pointer_declarator (identifier) @id))
                (struct_specifier name: (type_identifier) @id)
                (type_definition declarator: (type_identifier) @id)
                (declaration declarator: (identifier) @id)
                (declaration declarator: (pointer_declarator (identifier) @id))
                (preproc_include path: (string_literal) @id)
            """
        
        query = Query(self.lang, query_str)
        cursor = QueryCursor(query)
        raw_captures = cursor.captures(tree.root_node)
        
        nodes = []
        if isinstance(raw_captures, dict):
            for n_list in raw_captures.values():
                nodes.extend(n_list)
        elif isinstance(raw_captures, list):
            for item in raw_captures:
                if isinstance(item, (list, tuple)):
                    nodes.append(item[0])
                else:
                    nodes.append(item)
        
        identifiers = set()
        for node in nodes:
            try:
                # node.text is usually bytes in tree-sitter Python
                text_bytes = getattr(node, 'text', None)
                if text_bytes is not None:
                    if isinstance(text_bytes, bytes):
                        text = text_bytes.decode('utf8', errors='ignore').strip('"<>')
                    else:
                        text = str(text_bytes).strip('"<>')
                    if text:
                        identifiers.add(text)
            except Exception:
                continue
        
        return identifiers

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        if not self.template_content:
            return []

        # 1. Check if template identifiers still exist in the user AST
        # We look for any identifier or type_identifier node with the same text
        # that is NOT inside a comment.
        
        found_identifiers = set()
        
        def walk(node):
            if node.type == "comment":
                return
            
            if node.type in ("identifier", "type_identifier", "string_literal", "system_lib_string"):
                text_bytes = getattr(node, 'text', None)
                if text_bytes is not None:
                    if isinstance(text_bytes, bytes):
                        text = text_bytes.decode('utf8', errors='ignore').strip('"<>')
                    else:
                        text = str(text_bytes).strip('"<>')
                    
                    if text in self.template_identifiers:
                        found_identifiers.add(text)
            
            for child in node.children:
                walk(child)
        
        walk(tree.root_node)
        
        for identifier in self.template_identifiers:
            if identifier not in found_identifiers:
                self.findings.append(Finding(
                    type="integrity.violation",
                    file=file_path,
                    line=1,
                    severity=4.0,
                    confidence=1.0,
                    message=f"Template Violation: Missing '{identifier}'",
                    human_alternative=f"Μην διαγράφεις ή μετονομάζεις τα στοιχεία του template. Το '{identifier}' είναι απαραίτητο για την ορθή λειτουργία/βαθμολόγηση.",
                    rationale="Ο καθηγητής παρέχει ένα template για συγκεκριμένο λόγο. Η αλλοίωση της δομής του (π.χ. διαγραφή απαραίτητων headers ή συναρτήσεων) συχνά υποδηλώνει απρόσεκτη χρήση AI που 'ξαναέγραψε' όλο τον κώδικα από την αρχή."
                ))

        return self.findings
