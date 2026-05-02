import math
from typing import List, Dict
from analyzer.models import Finding, PillarScore, AnalysisResult

class ScoringEngine:
    def __init__(self, sensitivity=50, humanity_shield=True, ui_lang="EN"):
        # Wider multiplier range: 0.2x to 3.2x
        self.sensitivity_multiplier = 0.2 + (sensitivity / 33.3) 
        self.humanity_shield = humanity_shield
        self.ui_lang = ui_lang.upper() if ui_lang else "EN"
        
        # Pillar display names (Internal keys for logic, display from i18n/FE)
        self.pillar_config = {
            "ast_uniformity": {"weight": 0.20},
            "statistical": {"weight": 0.20},
            "naming": {"weight": 0.15},
            "comments": {"weight": 0.10},
            "drift": {"weight": 0.15},
            "integrity": {"weight": 0.20}
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
            if p == "similarity": p = "statistical" # Jaccard/Entropy is statistical
            if p == "logic": p = "drift"            # Algorithmic anti-patterns
            if p == "naming": p = "naming"
            if p == "comments": p = "comments"
            if p == "statistical": p = "statistical"
            if p == "drift": p = "drift"
            if p == "integrity": p = "integrity"
            
            if p in pillars_map: pillars_map[p].append(f)
            else:
                # Fallback mapping
                if p == "redundancy": pillars_map["drift"].append(f)
                else: pillars_map["drift"].append(f) # Final fallback
        
        total_score, p_scores = 0.0, []
        for pk, pf in pillars_map.items():
            # Non-linear weighting: Serious issues should hit the score harder
            # severity^1.4 creates an exponential curve that penalizes high-severity slop
            raw_sum = sum((f.severity ** 1.4) * f.confidence for f in pf) * self.sensitivity_multiplier
            
            # Apply humanity shield reduction to the raw sum before sigmoid
            if self.humanity_shield:
                raw_sum = max(0, raw_sum - human_reduction)

            # Re-calibrated sigmoid: 0.15 instead of 0.45 to provide more headroom and sensitivity responsiveness
            s = 100 * (1 - math.exp(-0.15 * raw_sum))
            total_score += s * self.pillar_config[pk]["weight"]
            p_scores.append(PillarScore(pillar=pk, score=round(s, 1), findings=pf))
        
        final_score = min(100.0, total_score)
        
        # --- Papatzis Hierarchy (v3.0) - Localized ---
        from analyzer.i18n import translate
        if final_score < 10:
            tier_key = "scoring.honest_code"
        elif final_score < 30:
            tier_key = "scoring.petty_scammer"
        elif final_score < 60:
            tier_key = "scoring.professional_papatzis"
        else:
            tier_key = "scoring.amateur_slop"
            
        t_data = translate(tier_key, ui_lang=self.ui_lang)
        interp = t_data["message"]
        
        return AnalysisResult(
            final_score=round(final_score, 1), 
            confidence_score=0.9, 
            pillars=p_scores, 
            interpretation=interp
        )
