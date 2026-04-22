import math
import re
from typing import List, Dict
from tree_sitter import Tree
from base import BaseAnalyzer
from models import Finding

class StatisticalAnalyzer(BaseAnalyzer):
    def __init__(self, language_id: str):
        super().__init__(language_id)

    def _calculate_entropy(self, text: str) -> float:
        """
        Υπολογίζει την Shannon Entropy σε επίπεδο χαρακτήρων.
        """
        if not text:
            return 0.0
        
        counts = {}
        for char in text:
            counts[char] = counts.get(char, 0) + 1
            
        entropy = 0.0
        total = len(text)
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def _calculate_token_entropy(self, tokens: List[str]) -> float:
        """
        Υπολογίζει την Shannon Entropy σε επίπεδο tokens.
        """
        if not tokens:
            return 0.0
            
        counts = {}
        for token in tokens:
            counts[token] = counts.get(token, 0) + 1
            
        entropy = 0.0
        total = len(tokens)
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        self.clear()
        
        source_text = source_code.decode('utf8', errors='ignore')
        lines = source_text.splitlines()
        
        # --- 1. Shannon Entropy Analysis (Phase 2.1) ---
        # Υπολογίζουμε την εντροπία ολόκληρου του αρχείου
        tokens = re.findall(r'\w+', source_text)
        token_entropy = self._calculate_token_entropy(tokens)
        
        # Heuristic: Τα LLMs παράγουν κώδικα με χαμηλή "εντροπία λεξιλογίου" 
        # (συχνή χρήση των ίδιων λέξεων/δομών).
        # Ο άνθρωπος έχει περισσότερο 'θόρυβο' και ποικιλία.
        if 2.5 < token_entropy < 5.2 and len(tokens) > 50:
            self.findings.append(Finding(
                type="statistical.low_entropy",
                file=file_path,
                line=1,
                severity=0.6,
                confidence=0.8,
                message=f"Low Token Entropy ({token_entropy:.2f}): Στατιστικά υπερβολικά προβλέψιμος κώδικας.",
                human_alternative="Ενισχύστε την ποικιλία στην ονοματολογία και στη δομή.",
                rationale="Η χαμηλή εντροπία σε μεγάλα αρχεία υποδηλώνει την ομοιόμορφη κατανομή tokens που χαρακτηρίζει τα LLMs."
            ))

        # --- 2. Burstiness & Variance Analysis (Phase 2.2) ---
        line_lengths = [len(l.strip()) for l in lines if l.strip()]
        if len(line_lengths) > 8:
            mean_len = sum(line_lengths) / len(line_lengths)
            variance = sum((l - mean_len) ** 2 for l in line_lengths) / len(line_lengths)
            std_dev = math.sqrt(variance)
            
            # Αν η τυπική απόκλιση στο μήκος των γραμμών είναι πολύ χαμηλή, 
            # ο κώδικας είναι "επίπεδος" (flat), σήμα AI.
            # Για C κώδικα, ο άνθρωπος έχει μεγάλη διακύμανση λόγω macros/headers.
            if std_dev < 12.0 and mean_len > 15:
                self.findings.append(Finding(
                    type="statistical.low_burstiness",
                    file=file_path,
                    line=1,
                    severity=0.6,
                    confidence=0.7,
                    message=f"Low Burstiness (StdDev: {std_dev:.2f}): Υπερβολικά σταθερός ρυθμός γραφής.",
                    human_alternative="Αποφύγετε την υπερβολική ομοιομορφία στο μήκος των εντολών.",
                    rationale="Ο 'μηχανικός' ρυθμός (παρόμοια μήκη γραμμών) είναι στατιστικό αποτύπωμα των LLMs."
                ))

        # --- 3. N-gram Repetition (Phase 2.3) ---
        # Αναζητούμε επαναλαμβανόμενες ακολουθίες 3 tokens
        if len(tokens) > 20:
            ngrams = {}
            for i in range(len(tokens) - 2):
                ngram = tuple(tokens[i:i+3])
                ngrams[ngram] = ngrams.get(ngram, 0) + 1
            
            # Αν κάποιο n-gram επαναλαμβάνεται υπερβολικά σε μικρά αρχεία
            top_repeats = [count for count in ngrams.values() if count > 4]
            if len(top_repeats) > 2:
                self.findings.append(Finding(
                    type="statistical.high_repetition",
                    file=file_path,
                    line=1,
                    severity=0.5,
                    confidence=0.6,
                    message="High N-gram Repetition: Εντοπίστηκαν επαναλαμβανόμενα λεκτικά μοτίβα.",
                    human_alternative="Αποφύγετε τις επαναλαμβανόμενες δομές ονοματολογίας.",
                    rationale="Τα LLMs συχνά εγκλωβίζονται σε συγκεκριμένες λεκτικές ακολουθίες κατά την παραγωγή."
                ))

        return self.findings
