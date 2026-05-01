import tree_sitter_language_pack
from tree_sitter import Tree, Query, QueryCursor, Node
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding
from typing import List, Dict
import math

class StructuralAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str):
        super().__init__(language_id)
        self.lang = tree_sitter_language_pack.get_language(language_id)
        
        # Redundant IF pattern
        if language_id == "python":
            self.redundant_if_query = Query(self.lang, """
                (if_statement
                  consequence: (block (return_statement))
                  alternative: (else_clause (block (return_statement)))
                ) @redundant_if
            """)
        else: # C
            self.redundant_if_query = Query(self.lang, """
                (if_statement
                  consequence: (compound_statement (return_statement))
                  alternative: (else_clause (compound_statement (return_statement)))
                ) @redundant_if
            """)
        self.redundant_if_cursor = QueryCursor(self.redundant_if_query)
        
        # Query for unnecessary function proxies (wrappers)
        if language_id == "python":
            self.unnecessary_wrapper_query = Query(self.lang, """
                (function_definition
                  body: (block
                          [
                            (expression_statement
                              (call
                                function: (identifier) @called_func
                              )
                            )
                            (return_statement
                              (call
                                function: (identifier) @called_func
                              )
                            )
                          ]
                        )
                ) @wrapper
            """)
            # AI-Style Error Handling (Python) - Robust query
            self.gpt_error_query = Query(self.lang, """
                (try_statement
                  (block)
                  (except_clause
                    (block
                      (expression_statement
                        (call
                          function: (identifier) @print_func
                        )
                      )
                    )
                  )
                ) @gpt_error
            """)
        else: # C
            self.unnecessary_wrapper_query = Query(self.lang, """
                (function_definition
                  body: (compound_statement
                          [
                            (expression_statement
                              (call_expression
                                function: (identifier) @called_func
                              )
                            )
                            (return_statement
                              (call_expression
                                function: (identifier) @called_func
                              )
                            )
                          ]
                        )
                ) @wrapper
            """)
            self.gpt_error_query = None # Θα μπορούσαμε να προσθέσουμε για C

        self.wrapper_cursor = QueryCursor(self.unnecessary_wrapper_query)
        if self.gpt_error_query:
            self.gpt_error_cursor = QueryCursor(self.gpt_error_query)

    def _get_node_depths(self, node: Node, depth: int = 0) -> List[int]:
        depths = [depth]
        for child in node.children:
            depths.extend(self._get_node_depths(child, depth + 1))
        return depths

    def _get_node_counts(self, node: Node, counts: Dict[str, int]) -> None:
        counts[node.type] = counts.get(node.type, 0) + 1
        for child in node.children:
            self._get_node_counts(child, counts)

    def _normalize_captures(self, raw_captures):
        if isinstance(raw_captures, list):
            captures = {}
            for node, tag in raw_captures:
                if tag not in captures: captures[tag] = []
                captures[tag].append(node)
            return captures
        return raw_captures

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        
        # 1. Detect Redundant If-Returns
        cursor = QueryCursor(self.redundant_if_query)
        captures = self._normalize_captures(cursor.captures(tree.root_node))
        for tag, nodes in captures.items():
            if tag == "redundant_if":
                for node in nodes:
                    self.findings.append(Finding(
                        type="structural.redundant_if",
                        file=file_path,
                        line=node.start_point[0] + 1,
                        severity=0.5,
                        confidence=1.0,
                        message="Redundant If-Return (Verbose Logic)",
                        human_alternative="Αντικατάστησε το if/else με ένα άμεσο `return condition`. Για παράδειγμα: `return x > 5` αντί για `if x > 5: return True else: return False`.",
                        rationale="Το AI έχει την τάση να είναι υπερβολικά αναλυτικό (verbose) για να φαίνεται επεξηγηματικό. Ένας έμπειρος προγραμματιστής προτιμά την κομψότητα και την αποφυγή περιττών διακλαδώσεων."
                    ))

        # 2. Detect Unnecessary Wrappers (Proxy functions)
        cursor = QueryCursor(self.unnecessary_wrapper_query)
        captures = self._normalize_captures(cursor.captures(tree.root_node))
        for tag, nodes in captures.items():
            if tag == "wrapper":
                for node in nodes:
                    # Verify it only has ONE statement in the body to avoid false positives
                    body_node = node.child_by_field_name('body')
                    if body_node:
                        # Count named children (actual statements)
                        statements = [c for c in body_node.children if c.is_named]
                        if len(statements) != 1:
                            continue
                            
                    self.findings.append(Finding(
                        type="structural.proxy_function",
                        file=file_path,
                        line=node.start_point[0] + 1,
                        severity=0.4,
                        confidence=0.7,
                        message="Empty Proxy Function (Wrapper Slop)",
                        human_alternative="Αν η συνάρτηση δεν προσθέτει κάποιο abstraction ή business logic, αφαίρεσέ την και κάλεσε απευθείας την εσωτερική συνάρτηση.",
                        rationale="Τα LLMs μερικές φορές δημιουργούν 'άδειες' συναρτήσεις-περιτυλίγματα που απλώς πασάρουν δεδομένα. Αυτό προσθέτει περιττή πολυπλοκότητα χωρίς κανένα όφελος."
                    ))

        # 3. GPT Error Handling Template Matching
        if self.gpt_error_query:
            cursor = QueryCursor(self.gpt_error_query)
            captures = self._normalize_captures(cursor.captures(tree.root_node))
            for tag, nodes in captures.items():
                if tag == "gpt_error":
                    for node in nodes:
                        self.findings.append(Finding(
                            type="structural.gpt_error_pattern",
                            file=file_path,
                            line=node.start_point[0] + 1,
                            severity=0.6,
                            confidence=0.8,
                            message="Standard AI Error Handling Template",
                            human_alternative="Μην μένεις στο `print(e)`. Χρησιμοποίησε ένα σωστό `logger`, σήκωσε ένα custom exception ή πρόσθεσε ουσιαστικό error recovery.",
                            rationale="Το `try: ... except Exception as e: print(e)` είναι η 'εύκολη λύση' που δίνει το AI αν δεν του δώσεις οδηγίες. Σε επαγγελματικό κώδικα, η διαχείριση σφαλμάτων πρέπει να είναι στοχευμένη."
                        ))

        # 4. Depth Variance Metric (1.2)
        depths = self._get_node_depths(tree.root_node)
        if depths:
            mean_depth = sum(depths) / len(depths)
            variance = sum((d - mean_depth) ** 2 for d in depths) / len(depths)
            std_dev = math.sqrt(variance)
            
            # Πολύ χαμηλή απόκλιση σε κώδικα με κάποιο βάθος είναι ύποπτη για AI "επιπεδότητα"
            if std_dev < 1.0 and mean_depth > 3:
                self.findings.append(Finding(
                    type="structural.low_depth_variance",
                    file=file_path,
                    line=1,
                    severity=0.4,
                    confidence=0.6,
                    message=f"Low Depth Variance ({std_dev:.2f}): Ο κώδικας έχει ασυνήθιστα ομοιόμορφο βάθος nesting.",
                    human_alternative="Ενισχύστε τη δομή του κώδικα με πιο φυσικές διακυμάνσεις στη λογική.",
                    rationale="Ο ανθρώπινος κώδικας τείνει να έχει 'κορυφές' και 'κοιλάδες' πολυπλοκότητας, ενώ το AI παράγει συχνά ομοιόμορφες δομές."
                ))

        # 5. Node Distribution & Entropy Analysis (Phase 1.1)
        node_counts = {}
        self._get_node_counts(tree.root_node, node_counts)
        
        # 5.1 Node Type Entropy (Shannon Entropy of AST nodes)
        total_nodes = sum(node_counts.values())
        if total_nodes > 10:
            entropy = 0.0
            for count in node_counts.values():
                p = count / total_nodes
                entropy -= p * math.log2(p)
            
            # Heuristic: AI code often has "low diversity" in node types (very balanced/flat)
            # Ή αντίθετα, αν είναι υπερβολικά "καθαρό" textbook, η εντροπία είναι χαμηλή
            if 1.0 < entropy < 2.5: # Εύρος που θυμίζει "υπερβολικά προβλέψιμο" κώδικα
                self.findings.append(Finding(
                    type="structural.low_node_entropy",
                    file=file_path,
                    line=1,
                    severity=0.5,
                    confidence=0.7,
                    message=f"Low Node Type Entropy ({entropy:.2f}): Χαμηλή ποικιλία δομικών στοιχείων.",
                    human_alternative="Εμπλουτίστε τον κώδικα με πιο φυσικές προγραμματιστικές δομές.",
                    rationale="Τα LLMs συχνά ανακυκλώνουν τις ίδιες δομικές μονάδες, οδηγώντας σε στατιστικά 'επίπεδο' κώδικα."
                ))

        # 5.2 Ratio Analysis (High Assignment-to-Loop)
        assignments = node_counts.get("assignment", 0) or node_counts.get("expression_statement", 0)
        loops = node_counts.get("for_statement", 0) + node_counts.get("while_statement", 0)
        
        if loops > 0 and (assignments / loops) > 12:
            self.findings.append(Finding(
                type="structural.high_assignment_ratio",
                file=file_path,
                line=1,
                severity=0.3,
                confidence=0.5,
                message="High Assignment-to-Loop Ratio: Πολύ μεγάλο ποσοστό αναθέσεων σε σχέση με loops.",
                human_alternative="Εμπλουτίστε τη λογική με δυναμικές δομές ελέγχου.",
                rationale="Το AI τείνει να 'ξεδιπλώνει' λογική σε πολλές μεμονωμένες αναθέσεις αντί για συμπαγή loops (verbosity)."
            ))

        return self.findings
