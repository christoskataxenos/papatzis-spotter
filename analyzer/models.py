from pydantic import BaseModel
from typing import List, Tuple, Optional

class Finding(BaseModel):
    type: str              # π.χ. naming.generic
    file: str
    line: int
    severity: float        # 0.0 - 1.0 (weight)
    confidence: float      # 0.0 - 1.0
    message: str
    human_alternative: str
    rationale: str

class PillarScore(BaseModel):
    pillar: str
    score: float
    findings: List[Finding]

class AnalysisResult(BaseModel):
    final_score: float
    confidence_score: float # 0.0 - 1.0 (v2.0)
    pillars: List[PillarScore]
    interpretation: str
