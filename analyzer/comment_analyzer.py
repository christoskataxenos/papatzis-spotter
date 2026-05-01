import tree_sitter_language_pack
from tree_sitter import Tree, Query, QueryCursor
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding
from typing import List
import re

class CommentAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str):
        super().__init__(language_id)
        self.lang = tree_sitter_language_pack.get_language(language_id)

        # Language specific queries
        if language_id == "python":
            self.comment_query = Query(self.lang, """
                (comment) @comment
                (string) @docstring
            """)
        else: # C
            self.comment_query = Query(self.lang, "(comment) @comment")
        
        self.comment_cursor = QueryCursor(self.comment_query)
        # AI-style phrases (GPT typical verbosity + Enterprise fluff)
        self.ai_phrases = [
            "this function", "in this code", "the purpose of",
            "this block", "firstly", "secondly", "overall",
            "in summary", "as we can see", "calculates the",
            "note that", "we are using", "this function processes",
            "the provided", "performing some", "basic filtering",
            "returns the result", "given the", "implementation of",
            "straightforward", "demonstrates how", "simple example",
            "handle the case", "associated with", "ensures that",
            "absolutely thrilled", "comprehensive solution", "robust solution",
            "enterprise-grade", "cloud-native", "synergistic", "paradigm",
            "delving into", "cosmic order", "space-time continuum",
            "in conclusion", "hope this helps", "on your coding journey",
            "modular approach", "best practices", "highly scalable",
            "cutting-edge", "optimized for", "as an ai language model"
        ]
        
        # Human-centric exclusions (Cursed but authentic!)
        self.human_exclusions = [
            "TODO", "FIXME", "NOTE", "wtf", "lol", "cursed",
            "achtung", "Προσοχή", "ρε φίλε", "τι φάση", "fix"
        ]

    def _get_sentence_count(self, text: str) -> int:
        return len(re.findall(r'[.!?](\s|$)', text))

    def _has_technical_terms(self, text: str) -> bool:
        return bool(re.search(r'([a-z]+[A-Z][a-z]+|[a-z]+_[a-z]+|\.[a-z]+)', text))

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        
        code_str = source_code.decode('utf8', errors='ignore')
        code_lines = code_str.splitlines()
        
        cursor = QueryCursor(self.comment_query)
        raw_captures = cursor.captures(tree.root_node)
        all_nodes = []
        seen_nodes = set()
        
        # Normalize captures
        if isinstance(raw_captures, list):
            captures = {}
            for node, tag in raw_captures:
                if tag not in captures: captures[tag] = []
                captures[tag].append(node)
        else:
            captures = raw_captures

        for tag, nodes in captures.items():
            if tag in ["comment", "docstring"]:
                for node in nodes:
                    if node.id not in seen_nodes:
                        all_nodes.append(node)
                        seen_nodes.add(node.id)
        
        for node in all_nodes:
            comment_raw = node.text.decode('utf8', errors='ignore').strip()
            comment_text = re.sub(r'^(\s*#|\s*//|\s*/\*|\s*\*/|\s*\*|\'\'\'|"""|\'|")', '', comment_raw)
            comment_text = re.sub(r'(\'\'\'|"""|\'|")$', '', comment_text).strip()
            
            comment_text_norm = " ".join(comment_text.split())
            
            if not comment_text_norm or len(comment_text_norm) < 5:
                continue

            if any(ex.lower() in comment_text_norm.lower() for ex in self.human_exclusions):
                continue

            # --- 1. AI Phrase Matching ---
            clean_lower = comment_text_norm.lower()
            found_phrase = None
            for phrase in self.ai_phrases:
                if phrase in clean_lower:
                    found_phrase = phrase
                    break
            
            if found_phrase:
                self.findings.append(Finding(
                    type="comments.ai_style",
                    file=file_path,
                    line=node.start_point[0] + 1,
                    severity=2.5,
                    confidence=0.9,
                    message=f"GPT-Style Παπατζιλίκι (Phrase: '{found_phrase}')",
                    human_alternative="Αφαίρεσε τις 'ευγενικές' εισαγωγές. Αντί για 'This function calculates...', πες απλά '# Υπολογισμός ΦΠΑ'. Ο κώδικας δεν είναι έκθεση ιδεών, είναι εργαλείο.",
                    rationale="Τα AI έχουν εκπαιδευτεί να είναι υπερβολικά ευγενικά και επεξηγηματικά. Φράσεις όπως 'This function handles...' ή 'The purpose of...' είναι κλασικά γεμίσματα (filler phrases) που ένας άνθρωπος σπάνια γράφει."
                ))
                continue

            # --- 2. Obviousness Heuristic ---
            comment_words = set(re.findall(r'\w+', clean_lower))
            end_line_idx = node.end_point[0]
            if end_line_idx + 1 < len(code_lines):
                next_code_line = ""
                for i in range(end_line_idx + 1, min(end_line_idx + 5, len(code_lines))):
                    line = code_lines[i].strip()
                    if line and not line.startswith(('#', '"""', "'''")):
                        next_code_line = line
                        break
                
                if next_code_line:
                    obvious_verbs = {"add", "adds", "increase", "loop", "check", "return", "call", "set", "calculates", "processes"}
                    code_operators = ["+=", "=", "while", "if", "for", "return"]
                    
                    if (comment_words & obvious_verbs) and any(op in next_code_line for op in code_operators):
                        if len(comment_words) < 20: 
                            self.findings.append(Finding(
                                type="comments.obvious",
                                file=file_path,
                                line=node.start_point[0] + 1,
                                severity=1.2,
                                confidence=0.8,
                                message="Syntax Translator (Obvious Comment)",
                                human_alternative="Μην εξηγείς τι κάνει η γλώσσα προγραμματισμού (π.χ. 'αυξάνει το x'). Εξήγησε το *γιατί* χρειάζεται αυτή η αύξηση στο συγκεκριμένο σενάριο.",
                                rationale="Είναι το κλασικό 'AI verbosity': το AI μεταφράζει κάθε γραμμή κώδικα σε απλά αγγλικά/ελληνικά. Ένας προγραμματιστής ξέρει τι κάνει το `x += 1`, δεν χρειάζεται να του το πεις."
                            ))
                            continue

            # --- 3. Wikipedia/Textbook-Style Verbosity ---
            word_count = len(comment_text.split())
            ai_connectives = {
                "fundamental", "approach", "science", "efficient", "traversal", 
                "structure", "typically", "generally", "essential", "crucial",
                "simulation", "controller", "redundancy", "complexity", "enhanced",
                "comprehensive", "robust", "scalable", "enterprise"
            }
            matches = [w for w in comment_words if w in ai_connectives]
            
            if (self._get_sentence_count(comment_text) >= 1 or word_count > 10) and len(matches) >= 1 and not self._has_technical_terms(comment_text):
                if ":" in comment_text[:20] and word_count > 5:
                    self.findings.append(Finding(
                        type="comments.textbook_style",
                        file=file_path,
                        line=node.start_point[0] + 1,
                        severity=1.8,
                        confidence=0.8,
                        message="Textbook Style: Το σχόλιο μοιάζει με ορισμό από εγχειρίδιο.",
                        human_alternative="Γράψτε πιο άμεσα σχόλια που αφορούν το συγκεκριμένο context του κώδικα.",
                        rationale="Σχόλια που ξεκινούν με ορισμούς χωρίς να αναφέρονται στην υλοποίηση είναι δείγμα AI Slop."
                    ))
                elif (self._get_sentence_count(comment_text) >= 2 or word_count > 15) and len(matches) >= 2:
                    self.findings.append(Finding(
                        type="comments.wikipedia_style",
                        file=file_path,
                        line=node.start_point[0] + 1,
                        severity=2.0,
                        confidence=0.7,
                        message="Wikipedia-Style Slop (Verbiage)",
                        human_alternative="Συνοψίστε τη θεωρία ή αφαίρεσέ την τελείως. Ο κώδικας πρέπει να είναι αυτο-επεξηγηματικός. Αν χρειάζεται Wikipedia για να τον καταλάβουμε, κάτι πάει λάθος.",
                        rationale="Τα LLMs συχνά κάνουν 'κήρυγμα' μέσα στα σχόλια, εξηγώντας ολόκληρες θεωρίες ή βέλτιστες πρακτικές. Αυτό ονομάζεται Statistical Verbiage και είναι σήμα κατατεθέν του AI Slop."
                    ))
                continue

        return self.findings
