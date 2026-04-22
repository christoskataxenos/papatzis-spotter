from typing import List, Dict
from models import Finding, PillarScore, AnalysisResult

class ScoringEngine:
    def __init__(self):
        # Ερμηνείες αποτελεσμάτων βάσει σκορ (v2.0 Scientific)
        self.ranges = [
            (15, "Καθαρός, ανθρώπινος κώδικας ✅"),
            (35, "Ήπια AI επιρροή (Αποδεκτό) 🧐"),
            (55, "Μέτρια AI slop (Χρειάζεται καθάρισμα) ⚠️"),
            (75, "Πολύ AI-generated (Ύποπτος κώδικας) 🤖"),
            (100, "Τσατπαπατζής Confirmed! 🚩")
        ]
        
        # Πυλώνες v2.0 και τα βάρη τους (Weights)
        self.pillar_config = {
            "ast_uniformity": {"weight": 0.25, "desc": "AST Uniformity"},
            "entropy_signals": {"weight": 0.20, "desc": "Entropy Signals"},
            "naming_ngrams": {"weight": 0.20, "desc": "Naming & N-grams"},
            "comment_patterns": {"weight": 0.15, "desc": "Comment Patterns"},
            "project_drift": {"weight": 0.20, "desc": "Project-Wide Drift"}
        }

        # Mapping των types των findings στους νέους πυλώνες
        self.type_to_pillar = {
            "structural": "ast_uniformity",
            "suspicion": "ast_uniformity",
            "statistical": "entropy_signals",
            "naming": "naming_ngrams",
            "comments": "comment_patterns",
            "redundancy": "project_drift", # Προσωρινό mapping μέχρι την πλήρη υλοποίηση του drift
            "drift": "project_drift"
        }

    def calculate(self, findings: List[Finding]) -> AnalysisResult:
        # Αρχικοποίηση των pillars βάσει του config
        pillars_map: Dict[str, List[Finding]] = {p: [] for p in self.pillar_config.keys()}
        
        all_confidences = [f.confidence for f in findings]
        avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 1.0
        
        for f in findings:
            prefix = f.type.split(".")[0]
            target_pillar = self.type_to_pillar.get(prefix, "project_drift")
            if target_pillar in pillars_map:
                pillars_map[target_pillar].append(f)
        
        pillar_scores = []
        total_final_score = 0.0
        active_pillars_count = sum(1 for p_findings in pillars_map.values() if p_findings)
        
        for p_key, p_findings in pillars_map.items():
            # Κάθε πυλώνας υπολογίζεται ανεξάρτητα (0-100) πριν εφαρμοστεί το βάρος
            # raw_sum: Το άθροισμα των προβλημάτων στον πυλώνα
            raw_sum = sum(f.severity * f.confidence for f in p_findings)
            
            # Υπολογίζουμε το score του πυλώνα (0-100)
            # Χαιδευτικά: αν έχεις 5-6 σοβαρά findings, ο πυλώνας τερματίζει
            p_score_raw = min(100.0, raw_sum * 25) 
            
            # Εφαρμόζουμε το βάρος (weight) για το τελικό σκορ
            weight = self.pillar_config[p_key]["weight"]
            total_final_score += p_score_raw * weight
            
            pillar_scores.append(PillarScore(
                pillar=self.pillar_config[p_key]["desc"],
                score=round(p_score_raw, 1),
                findings=p_findings
            ))
            
        # Confidence boost βασισμένο στο πλήθος των διαφορετικών σημάτων (Diversity)
        diversity_multiplier = 0.6 + (active_pillars_count * 0.1)
        final_confidence = min(1.0, avg_confidence * diversity_multiplier)

        # Επιλογή ερμηνείας
        total_final_score = min(100.0, total_final_score)
        interpretation = "Άγνωστο"
        for threshold, text in self.ranges:
            if total_final_score <= threshold:
                interpretation = text
                break
        else:
            interpretation = self.ranges[-1][1]

        return AnalysisResult(
            final_score=round(total_final_score, 1),
            confidence_score=round(final_confidence, 2),
            pillars=pillar_scores,
            interpretation=interpretation
        )
