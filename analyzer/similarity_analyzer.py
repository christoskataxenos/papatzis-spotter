import tree_sitter_language_pack
from tree_sitter import Tree, Query, QueryCursor, Node
from analyzer.base import BaseAnalyzer
from analyzer.models import Finding
from typing import List, Set, Dict, Tuple
import re

class SimilarityAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str):
        super().__init__(language_id)
        self.lang = tree_sitter_language_pack.get_language(language_id)
        
        # Keywords to filter from content-aware tokens
        if language_id == "python":
            self.keywords = {
                "def", "class", "return", "if", "else", "elif", "for", "while", 
                "try", "except", "finally", "with", "as", "import", "from", 
                "None", "True", "False", "and", "or", "not", "is", "in", "lambda",
                "yield", "pass", "break", "continue", "raise", "assert", "global", "nonlocal"
            }
            # Query to find functions and classes
            self.block_query = Query(self.lang, """
                (function_definition) @block
                (class_definition) @block
            """)
        else: # C
            self.keywords = {
                "int", "char", "float", "double", "void", "struct", "enum", "union",
                "if", "else", "switch", "case", "default", "for", "while", "do",
                "return", "break", "continue", "goto", "sizeof", "typedef", "static",
                "extern", "const", "volatile", "unsigned", "signed", "long", "short"
            }
            self.block_query = Query(self.lang, """
                (function_definition) @block
                (struct_specifier) @block
            """)

    def _get_jaccard(self, set_a: Set, set_b: Set) -> float:
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return intersection / union if union > 0 else 0.0

    def _get_structural_set(self, node: Node) -> Set[str]:
        """Returns a set of structural node types in order-independent fashion (bag of types)"""
        types = []
        def traverse(n):
            types.append(n.type)
            for child in n.children:
                traverse(child)
        traverse(node)
        return set(types)

    def _get_naming_set(self, node: Node) -> Set[str]:
        """Returns a set of variable and function identifiers, excluding keywords"""
        names = []
        def traverse(n):
            if n.type == "identifier":
                name = n.text.decode('utf8')
                if name not in self.keywords and len(name) > 1:
                    names.append(name)
            for child in n.children:
                traverse(child)
        traverse(node)
        return set(names)

    def _get_comment_set(self, node: Node) -> Set[str]:
        """Returns a set of words from comments within the block"""
        words = []
        def traverse(n):
            if "comment" in n.type:
                text = n.text.decode('utf8')
                # Simple word extraction
                clean_text = re.sub(r'[^\w\s]', ' ', text)
                words.extend(clean_text.lower().split())
            for child in n.children:
                traverse(child)
        return set(word for word in words if len(word) > 2)

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        
        cursor = QueryCursor(self.block_query)
        captures = cursor.captures(tree.root_node)
        
        blocks = []
        for tag, nodes in captures.items():
            for node in nodes:
                # Complexity Filter: Ignore very small blocks (less than 5 lines)
                start_line = node.start_point[0]
                end_line = node.end_point[0]
                if (end_line - start_line) < 2:
                    continue
                    
                blocks.append({
                    "node": node,
                    "name": f"Block at L{start_line + 1}",
                    "lines": end_line - start_line + 1,
                    "structural": self._get_structural_set(node),
                    "naming": self._get_naming_set(node),
                    "comments": self._get_comment_set(node)
                })

        if len(blocks) < 2:
            return self.findings

        # Pairwise Jaccard Comparison
        high_sim_pairs = []
        all_jaccards = []
        
        for i in range(len(blocks)):
            for j in range(i + 1, len(blocks)):
                b1, b2 = blocks[i], blocks[j]
                
                # Calculate Jaccard for different aspects
                s_sim = self._get_jaccard(b1["structural"], b2["structural"])
                n_sim = self._get_jaccard(b1["naming"], b2["naming"])
                
                # Combined similarity (weighted)
                # Structure is more important for robotic consistency
                avg_sim = (s_sim * 0.7) + (n_sim * 0.3)
                all_jaccards.append(avg_sim)
                
                if avg_sim > 0.8:
                    high_sim_pairs.append((i, j, avg_sim))

        # Clustering (Simple union-find style)
        clusters = []
        if high_sim_pairs:
            membership = list(range(len(blocks)))
            def find(i):
                if membership[i] == i: return i
                membership[i] = find(membership[i])
                return membership[i]
            
            def union(i, j):
                root_i = find(i)
                root_j = find(j)
                if root_i != root_j:
                    membership[root_i] = root_j
            
            for i, j, sim in high_sim_pairs:
                union(i, j)
            
            cluster_map = {}
            for i in range(len(blocks)):
                root = find(i)
                if root not in cluster_map: cluster_map[root] = []
                cluster_map[root].append(i)
            
            clusters = [indices for indices in cluster_map.values() if len(indices) > 1]

        # Scoring & Findings
        total_source_lines = len(source_code.splitlines())
        if total_source_lines == 0: return self.findings

        slop_lines = 0
        for cluster in clusters:
            cluster_lines = sum(blocks[i]["lines"] for i in cluster)
            slop_lines += cluster_lines
            
            # Create a finding for each cluster
            rep_block = blocks[cluster[0]]
            self.findings.append(Finding(
                type="similarity.robotic_uniformity",
                file=file_path,
                line=rep_block["node"].start_point[0] + 1,
                severity=0.8,
                confidence=0.9,
                message=f"Robotic Uniformity: Εντοπίστηκε cluster {len(cluster)} συναρτήσεων με υπερβολική δομική ομοιότητα.",
                human_alternative="Ενισχύστε την ποικιλομορφία στον κώδικα. Αποφύγετε τα επαναλαμβανόμενα templates που παράγει το AI.",
                rationale=f"Η Jaccard ομοιότητα μεταξύ αυτών των blocks είναι > 80%, κάτι που σπάνια συμβαίνει σε ανθρώπινο κώδικα χωρίς copy-paste."
            ))

        # Global Entropy Check (Option 2)
        if all_jaccards:
            mean_jaccard = sum(all_jaccards) / len(all_jaccards)
            if mean_jaccard > 0.7:
                self.findings.append(Finding(
                    type="similarity.high_global_entropy",
                    file=file_path,
                    line=1,
                    severity=0.6,
                    confidence=0.7,
                    message=f"High Global Similarity ({mean_jaccard:.2f}): Το αρχείο παρουσιάζει ασυνήθιστη ομοιομορφία.",
                    human_alternative="Προσθέστε 'ανθρώπινο θόρυβο' και διαφοροποιήστε τις δομές των συναρτήσεων.",
                    rationale="Η μέση ομοιότητα μεταξύ όλων των blocks είναι πολύ υψηλή, υποδεικνύοντας ενιαίο generator (LLM)."
                ))

        return self.findings
