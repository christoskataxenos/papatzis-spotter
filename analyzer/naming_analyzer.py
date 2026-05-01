from typing import List
import re
import tree_sitter_language_pack
from tree_sitter import Tree, Language, Query, QueryCursor
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding

class NamingAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str, template_identifiers: set = None):
        super().__init__(language_id)
        self.lang = tree_sitter_language_pack.get_language(language_id)
        
        # Target assignments, parameters, loops, AND class/function definitions
        if language_id == "python":
            query_str = """
                (assignment left: (identifier) @id)
                (parameters (identifier) @id)
                (for_statement left: (identifier) @id)
                (class_definition name: (identifier) @id)
                (function_definition name: (identifier) @id)
            """
        else: # C
            query_str = """
                (identifier) @id
                (field_identifier) @id
                (type_identifier) @id
            """
        
        self.naming_query = Query(self.lang, query_str)
        # Safe list to avoid false positives
        self.safe_names = {"list", "int", "str", "dict", "set", "tuple", "float", "bool", "len", "sum", "min", "max", "range", "enumerate", "zip", "map", "filter"}
        if template_identifiers:
            self.safe_names.update(template_identifiers)

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        
        # 1. Human-Authentic Dummy Names (Lower Severity)
        dummy_re = re.compile(r"^(num|val|result|temp|temp_val|i|j|k)[0-9]*$", re.IGNORECASE)
        
        # 2. Lazy Generic Names (Classic Slop)
        generic_re = re.compile(r"^(data|output|info|value|item|stuff|var|processed|input|id|ptr|element)[0-9]*$", re.IGNORECASE)
        
        # 3. Enterprise-High-Slop (High Severity)
        # Patterns like "RobustCalculatorManagerFactory" or "EnterpriseAdditionProtocol"
        enterprise_terms = {
            "manager", "factory", "protocol", "entity", "strategy", "orchestrator",
            "synergistic", "operational", "robust", "enterprise", "implementation",
            "paradigm", "context", "handler", "provider", "service", "utility"
        }

        seen_findings = set() # (type, line, name)
        
        cursor = QueryCursor(self.naming_query)
        raw_captures = cursor.captures(tree.root_node)
        
        # Normalize captures to dict for easier processing
        # Some versions return dict, others return list of (node, tag)
        if isinstance(raw_captures, list):
            captures = {}
            for node, tag in raw_captures:
                if tag not in captures: captures[tag] = []
                captures[tag].append(node)
        else:
            captures = raw_captures

        for tag, nodes in captures.items():
            for node in nodes:
                name = node.text.decode('utf8', errors='ignore')
                line = node.start_point[0] + 1
            
                if name in self.safe_names or len(name) < 2:
                    continue
                
                # --- Detection Logic ---
                name_lower = name.lower()
                
                # 1. Enterprise Over-engineering (High Severity)
                # Find names that combine multiple enterprise terms (e.g., ManagerFactory)
                # Ignore constants (all caps)
                if name.isupper() and len(name) > 2:
                    continue

                ent_matches = [term for term in enterprise_terms if term in name_lower]
                if len(ent_matches) >= 2 or (len(ent_matches) == 1 and len(name) > 20):
                    fid = ("naming.enterprise_slop", line, name)
                    if fid not in seen_findings:
                        seen_findings.add(fid)
                        self.findings.append(Finding(
                            type="naming.enterprise_slop",
                            file=file_path,
                            line=line,
                            severity=2.5,
                            confidence=0.9,
                            message=f"Enterprise Slop: '{name}'",
                            human_alternative="Αντικατάστησε το '{name}' με κάτι απλό. Η οικονομία λέξεων είναι δείγμα εμπειρίας. Για παράδειγμα, αν είναι validator, πες το 'TextValidator' και όχι 'SymmetricalTextualEntityValidatorFactory'.",
                            rationale="Τα AI μοντέλα 'εκπαιδεύονται' να είναι υπερ-επαγγελματικά, με αποτέλεσμα να χρησιμοποιούν τεράστια ονόματα (Factories, Entities, Managers) ακόμα και για απλές λειτουργίες. Ένας άνθρωπος γράφει κώδικα για να διαβάζεται, όχι για να εντυπωσιάζει."
                        ))
                    continue # Skip further checks if this is already a structural slop name
    
                # 2. Generic Names (Classic Slop)
                if generic_re.match(name):
                    fid = ("naming.generic", line, name)
                    if fid not in seen_findings:
                        seen_findings.add(fid)
                        self.findings.append(Finding(
                            type="naming.generic",
                            file=file_path,
                            line=line,
                            severity=1.2,
                            confidence=1.0,
                            message=f"Lazy AI Naming: '{name}'",
                            human_alternative="Γίνε πιο συγκεκριμένος. Τι ακριβώς περιέχει αυτό το '{name}'; Αν είναι λίστα χρηστών, ονόμασέ το 'users' ή 'user_list'.",
                            rationale="Το AI συχνά βαριέται να σκεφτεί το context και χρησιμοποιεί λέξεις-πασπαρτού όπως 'data', 'info' ή 'value'. Αυτό κάνει τον κώδικα δυσνόητο για άλλους ανθρώπους."
                        ))

                # 3. CamelCase Detection in C (Phase 2.4)
                if self.language == "c":
                    if re.search(r'[a-z][A-Z]', name) and not name.isupper():
                        fid = ("naming.camel_case_slop", line, name)
                        if fid not in seen_findings:
                            seen_findings.add(fid)
                            self.findings.append(Finding(
                                type="naming.camel_case_slop",
                                file=file_path,
                                line=line,
                                severity=2.0,
                                confidence=0.9,
                                message=f"CamelCase Variable '{name}': Μη-παραδοσιακό naming για C.",
                                human_alternative="Χρησιμοποίησε snake_case (π.χ. `validation_result`).",
                                rationale="Ο CamelCase στη C είναι ισχυρό αποτύπωμα LLM, καθώς τα μοντέλα τείνουν να μεταφέρουν συμβάσεις από άλλες γλώσσες (Java/JS)."
                            ))
    
                # 3. Dummy Names (Human-Authentic but lazy)
                if dummy_re.match(name):
                    fid = ("naming.dummy", line, name)
                    if fid not in seen_findings:
                        seen_findings.add(fid)
                        self.findings.append(Finding(
                            type="naming.dummy",
                            file=file_path,
                            line=line,
                            severity=0.4, # Very low severity - humans use these too!
                            confidence=0.5,
                            message=f"Τυπικό (dummy) όνομα: '{name}'",
                            human_alternative="Αν ο κώδικας είναι παραγωγής, δώστε πιο συγκεκριμένο όνομα.",
                            rationale="Αυτά τα ονόματα είναι κοινά σε ανθρώπινα dummy scripts αλλά και σε AI παραδείγματα. Χαμηλή βαρύτητα."
                        ))

        return self.findings
