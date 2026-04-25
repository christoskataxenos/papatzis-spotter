import math
from typing import List, Dict
from models import Finding, PillarScore, AnalysisResult

class ScoringEngine:
    def __init__(self, sensitivity=50, humanity_shield=True):
        self.sensitivity_multiplier = 0.5 + (sensitivity / 50.0) # 0.5 to 2.5
        self.humanity_shield = humanity_shield
        self.pillar_config = {
            "ast_uniformity": {"weight": 0.25, "desc": "Ρομποτική Ομοιομορφία"},
            "statistical": {"weight": 0.20, "desc": "Στατιστική Φλυαρία"},
            "naming": {"weight": 0.20, "desc": "Βαφτιστικό Slop"},
            "comments": {"weight": 0.15, "desc": "GPT-Style Παπατζιλίκι"},
            "drift": {"weight": 0.20, "desc": "Ύποπτο Drift Κώδικα"}
        }

    def calculate(self, findings: List[Finding]) -> AnalysisResult:
        pillars_map = {p: [] for p in self.pillar_config.keys()}
        human_reduction = 0.0

        for f in findings:
            if f.type == "humanity.shield":
                human_reduction += f.severity # Gravity of "humanity proof"
                continue

            p = f.type.split(".")[0]
            if p == "suspicion": p = "ast_uniformity"
            if p == "structural": p = "ast_uniformity"
            if p == "naming": p = "naming"
            if p == "comments": p = "comments"
            if p == "statistical": p = "statistical"
            if p == "drift": p = "drift"
            
            if p in pillars_map: pillars_map[p].append(f)
            else:
                # Fallback mapping if type prefix doesn't match keys exactly
                # e.g. redundancy -> drift
                if p == "redundancy": pillars_map["drift"].append(f)
        
        total_score, p_scores = 0.0, []
        for pk, pf in pillars_map.items():
            raw_sum = sum(f.severity * f.confidence for f in pf) * self.sensitivity_multiplier
            # Apply humanity shield reduction to the raw sum before sigmoid
            if self.humanity_shield:
                raw_sum = max(0, raw_sum - human_reduction)

            # Σιγμοειδής συνάρτηση για την εξομάλυνση του σκορ
            s = 100 * (1 - math.exp(-0.45 * raw_sum))
            total_score += s * self.pillar_config[pk]["weight"]
            p_scores.append(PillarScore(pillar=self.pillar_config[pk]["desc"], score=round(s, 1), findings=pf))
        
        final_score = min(100.0, total_score)
        
        # --- Papatzis Hierarchy (v2.1) ---
        if final_score < 15: interp = "Τίμιος Κώδικας"
        elif final_score < 40: interp = "Ψιλικατζής"
        elif final_score < 75: interp = "Επαγγελματίας Παπατζής"
        else: interp = "Ερασιτέχνης (100% Slop)"
        
        return AnalysisResult(
            final_score=round(final_score, 1), 
            confidence_score=0.9, 
            pillars=p_scores, 
            interpretation=interp
        )
