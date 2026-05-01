import tree_sitter_language_pack
from tree_sitter import Tree, Query, QueryCursor
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding
from typing import List

class RedundancyAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str):
        super().__init__(language_id)
        self.lang = tree_sitter_language_pack.get_language(language_id)
        
        # 1. Unreachable code after return (Python)
        if language_id == "python":
            self.unreachable_query = Query(self.lang, """
                (block
                  (return_statement)
                  .
                  (_) @unreachable
                )
            """)
        else: # C
            self.unreachable_query = Query(self.lang, """
                (compound_statement
                  (return_statement)
                  .
                  (_) @unreachable
                )
            """)
        self.unreachable_cursor = QueryCursor(self.unreachable_query)

        # 2. Over-abstraction: Single-method classes (Python)
        if language_id == "python":
            self.single_method_class_query = Query(self.lang, """
                (class_definition
                  body: (block
                    (function_definition) @method
                    (#not-match? @method "__init__")
                  ) @class_body
                ) @class_def
            """)
        else:
            self.single_method_class_query = None
        
        if self.single_method_class_query:
            self.single_method_class_cursor = QueryCursor(self.single_method_class_query)
        else:
            self.single_method_class_cursor = None

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        
        # 1. Ανίχνευση μη προσβάσιμου κώδικα (Unreachable Code)
        raw_captures = self.unreachable_cursor.captures(tree.root_node)
        if isinstance(raw_captures, list):
            captures = {"unreachable": [n for n, t in raw_captures if t == "unreachable"]}
        else:
            captures = raw_captures

        # Χρησιμοποιούμε set για να αποφύγουμε πολλαπλά findings για το ίδιο block
        unreachable_nodes = set()
        for node in captures.get("unreachable", []):
            if node.id not in unreachable_nodes:
                unreachable_nodes.add(node.id)
                self.findings.append(Finding(
                    type="redundancy.unreachable",
                    file=file_path,
                    line=node.start_point[0] + 1,
                    severity=2.0,
                    confidence=1.0,
                    message="Unreachable Code: Κώδικας μετά από return.",
                    human_alternative="Αφαιρέστε τον περιττό κώδικα ή ελέγξτε τη λογική ροή.",
                    rationale="Τα LLMs μερικές φορές αφήνουν boilerplate ή debug κώδικα μετά από return που δεν εκτελείται ποτέ."
                ))

        # 2. Ανίχνευση Over-abstraction (Single-method classes)
        if self.single_method_class_query:
            self.single_method_class_cursor = QueryCursor(self.single_method_class_query)
            raw_captures = self.single_method_class_cursor.captures(tree.root_node)
            if isinstance(raw_captures, list):
                captures = {"class_def": [n for n, t in raw_captures if t == "class_def"]}
            else:
                captures = raw_captures
            # Εδώ θέλουμε να δούμε αν η κλάση έχει ΜΟΝΟ μία μέθοδο (εκτός __init__)
            # Η tree-sitter Query API για "μόνο μία" είναι λίγο περιορισμένη, οπότε θα κάνουμε post-processing
            class_nodes = captures.get("class_def", [])
            for class_node in class_nodes:
                # Μετράμε πόσες μεθόδους έχει το block
                methods = [n for n in class_node.children if n.type == "block"]
                if not methods: continue
                
                all_defs = [n for n in methods[0].children if n.type == "function_definition"]
                # Αν έχει μόνο μία και δεν είναι η __init__
                if len(all_defs) == 1:
                    method_name_node = all_defs[0].child_by_field_name("name")
                    if method_name_node and method_name_node.text.decode('utf8') != "__init__":
                        self.findings.append(Finding(
                            type="redundancy.over_abstraction",
                            file=file_path,
                            line=class_node.start_point[0] + 1,
                            severity=1.2,
                            confidence=0.8,
                            message="Over-abstraction: Κλάση με μία μόνο μέθοδο.",
                            human_alternative="Εξετάστε αν η κλάση μπορεί να αντικατασταθεί από μια απλή συνάρτηση.",
                            rationale="Το AI τείνει να δημιουργεί κλάσεις για τα πάντα (Java-style), ακόμα και όταν μια συνάρτηση αρκεί."
                        ))

        return self.findings
