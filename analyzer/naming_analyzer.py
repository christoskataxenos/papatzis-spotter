from typing import List
import re
import tree_sitter_language_pack
from tree_sitter import Tree, Language, Query, QueryCursor
from base import BaseAnalyzer
from models import Finding

class NamingAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str):
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
                (declaration 
                    declarator: [
                        (identifier) @id
                        (init_declarator declarator: (identifier) @id)
                        (pointer_declarator declarator: (identifier) @id)
                        (array_declarator declarator: (identifier) @id)
                    ]
                )
                (parameter_declaration 
                    declarator: [
                        (identifier) @id
                        (pointer_declarator declarator: (identifier) @id)
                        (array_declarator declarator: (identifier) @id)
                    ]
                )
                (function_definition declarator: (function_declarator declarator: (identifier) @id))
                (struct_specifier name: (identifier) @id)
            """
        
        self.naming_query = Query(self.lang, query_str)

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

        # Safe list to avoid false positives
        safe_names = {"list", "int", "str", "dict", "set", "tuple", "float", "bool", "len", "sum", "min", "max", "range", "enumerate", "zip", "map", "filter"}

        seen_findings = set() # (type, line, name)
        
        cursor = QueryCursor(self.naming_query)
        captures = cursor.captures(tree.root_node)
        
        for node, index in captures:
            tag = self.naming_query.capture_names[index]
            name = node.text.decode('utf8')
            line = node.start_point[0] + 1
            
            if name in safe_names or len(name) < 2:
                continue
            
            # --- Detection Logic ---
            name_lower = name.lower()
            
            # 1. Enterprise Over-engineering (High Severity)
            # Find names that combine multiple enterprise terms (e.g., ManagerFactory)
            ent_matches = [term for term in enterprise_terms if term in name_lower]
            if len(ent_matches) >= 2 or (len(ent_matches) == 1 and len(name) > 15):
                fid = ("naming.enterprise_slop", line, name)
                if fid not in seen_findings:
                    seen_findings.add(fid)
                    self.findings.append(Finding(
                        type="naming.enterprise_slop",
                        file=file_path,
                        line=line,
                        severity=2.5,
                        confidence=0.9,
                        message=f"Enterprise Over-engineering: '{name}'",
                        human_alternative="Απλοποιήστε την ονομασία. Αποφύγετε βαρύγδουπους όρους (Manager, Protocol, Factory) για απλή λειτουργικότητα.",
                        rationale="Τα LLMs συχνά επιλέγουν 'πλούσια' ονόματα που θυμίζουν enterprise-java logic για να φαίνονται πιο επαγγελματικά."
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
                        message=f"Generic όνομα: '{name}'",
                        human_alternative="Πιο περιγραφικό όνομα (π.χ. 'user_data' αντί για 'data').",
                        rationale="AI-style generic naming."
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
