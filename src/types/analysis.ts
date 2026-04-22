export interface Finding {
    type: string;
    file: string;
    line: number;
    severity: number;
    confidence: number;
    message: string;
    human_alternative: string;
    rationale: string;
}

export interface PillarScore {
    pillar: string;
    score: number;
    findings: Finding[];
}

export interface AnalysisResult {
    final_score: number;
    confidence_score: number;
    pillars: PillarScore[];
    interpretation: string;
}
