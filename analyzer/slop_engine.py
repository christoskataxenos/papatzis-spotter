import sys
import os
import json
import multiprocessing
import re
import math
from abc import ABC, abstractmethod
from typing import List, Dict, Set, Tuple, Optional
import tree_sitter_language_pack
from tree_sitter import Tree, Parser, Query, Node, QueryCursor
from pydantic import BaseModel

# --- Models ---

class Finding(BaseModel):
    type: str
    file: str
    line: int
    severity: float
    confidence: float
    message: str
    human_alternative: str
    rationale: str

class PillarScore(BaseModel):
    pillar: str
    score: float
    findings: List[Finding]

class AnalysisResult(BaseModel):
    final_score: float
    confidence_score: float
    pillars: List[PillarScore]
    interpretation: str

# --- Engines ---

class ScoringEngine:
    def __init__(self, sensitivity=50, humanity_shield=True):
        self.sensitivity_multiplier = 0.5 + (sensitivity / 50.0) # 0.5 to 2.5
        self.humanity_shield = humanity_shield
        self.pillar_config = {
            "ast_uniformity": {"weight": 0.20, "desc": "Ρομποτική Ομοιομορφία"},
            "statistical": {"weight": 0.35, "desc": "Στατιστική Φλυαρία"},
            "naming": {"weight": 0.20, "desc": "Βαφτιστικό Slop"},
            "comments": {"weight": 0.25, "desc": "GPT-Style Παπατζιλίκι"}
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
            if p in pillars_map: pillars_map[p].append(f)
        
        total_score, p_scores = 0.0, []
        for pk, pf in pillars_map.items():
            raw_sum = sum(f.severity * f.confidence for f in pf) * self.sensitivity_multiplier
            # Apply humanity shield reduction to the raw sum before sigmoid
            if self.humanity_shield:
                raw_sum = max(0, raw_sum - human_reduction)

            s = 100 * (1 - math.exp(-0.45 * raw_sum))
            total_score += s * self.pillar_config[pk]["weight"]
            p_scores.append(PillarScore(pillar=self.pillar_config[pk]["desc"], score=round(s, 1), findings=pf))
        
        final_score = min(100.0, total_score)
        
        # --- Papatzis Hierarchy (v2.1) ---
        if final_score < 15: interp = "Τίμιος Κώδικας"
        elif final_score < 40: interp = "Ψιλικατζής"
        elif final_score < 75: interp = "Επαγγελματίας Παπατζής"
        else: interp = "Ερασιτέχνης (100% Slop)"
        
        return AnalysisResult(final_score=round(final_score, 1), confidence_score=0.9, pillars=p_scores, interpretation=interp)

class SuspicionAnalyzer:
    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        findings = []
        logic_nodes, boilerplate_nodes, max_depth = 0, 0, 0
        logic_types = (
            "binary_expression", "boolean_expression", "comparison_operator", 
            "augmented_assignment", "unary_operator"
        )
        boilerplate_types = (
            "assignment", "call", "try_statement", "except_clause", "finally_clause", 
            "function_definition", "class_definition", "if_statement", "while_statement", 
            "for_statement", "parameters", "block", "module", "comment", "string", 
            "pass_statement", "decorator", "expression_statement", "attribute"
        )
        def walk(n, depth=0):
            nonlocal logic_nodes, boilerplate_nodes, max_depth
            if depth > max_depth: max_depth = depth
            if n.type in logic_types: logic_nodes += 1
            elif n.type in boilerplate_types: boilerplate_nodes += 1
            if n.type == "call":
                t = n.text.decode('utf8', errors='ignore').lower()
                if t.startswith(("print", "log", "self.log", "logger")):
                    boilerplate_nodes += 3 
            inc = 1 if n.type in ("if_statement", "for_statement", "while_statement", "try_statement", "elif_clause", "with_statement") else 0
            for c in n.children: walk(c, depth + inc)
        
        walk(tree.root_node)
        if max_depth > 3:
            findings.append(Finding(type="statistical.hadouken_nesting", file=file_path, line=1, severity=2.5, confidence=1.0, message=f"Hadouken Code: Βάθος {max_depth}.", human_alternative="Flatten logic.", rationale="AI nesting."))
        if boilerplate_nodes > logic_nodes * 1.2 and len(source_code) > 200:
            findings.append(Finding(type="suspicion.architecture_overkill", file=file_path, line=1, severity=4.0, confidence=1.0, message=f"Architecture Overkill: Logic {logic_nodes}/Boilerplate {boilerplate_nodes}.", human_alternative="Simplify the structure.", rationale="Severe structural slop."))
        return findings

class NamingAnalyzer:
    def __init__(self, language_id: str):
        self.dummy_re = re.compile(r"^(num|val|result|temp|temp_val|i|j|k)[0-9]*$", re.IGNORECASE)
        self.generic_re = re.compile(r"^(data|output|info|value|item|stuff|var|processed|input|id|ptr|element)[0-9]*$", re.IGNORECASE)
        self.enterprise_terms = {"manager", "factory", "protocol", "entity", "strategy", "orchestrator", "synergistic", "robust", "enterprise", "paradigm", "scalability", "abstraction", "payload", "engine", "holistic", "matrix", "parity", "evaluation", "cache", "validator", "symmetrical"}
        self.safe_names = {"list", "int", "str", "dict", "set", "tuple", "float", "bool", "len", "sum", "range", "argc", "argv"}

    def analyze(self, tree: Tree, source_code: bytes, file_path: str) -> List[Finding]:
        findings, found_names = [], set() 
        def find_ids(n):
            if n.type == "identifier":
                name = n.text.decode("utf8", errors="ignore")
                if name not in self.safe_names and len(name) >= 2:
                    name_lower = name.lower()
                    is_definition = False
                    p = n.parent
                    while p:
                        if p.type in ("class_definition", "function_definition", "function_declarator", "class_specifier", "decorator"): is_definition = True; break
                        p = p.parent
                    ent_matches = [t for t in self.enterprise_terms if t in name_lower]
                    if (len(ent_matches) >= 2 or (len(ent_matches) == 1 and len(name) > 12)) or (is_definition and any(t in name_lower for t in ("manager", "factory", "protocol"))):
                        key = ("ent", name)
                        if key not in found_names:
                            findings.append(Finding(type="naming.enterprise_slop", file=file_path, line=n.start_point[0] + 1, severity=1.5, confidence=1.0, message=f"Enterprise Slop: '{name}'", human_alternative="Simplify naming.", rationale="Pretentious naming."))
                            found_names.add(key)
                    elif self.generic_re.match(name) and not is_definition:
                        key = ("gen", name)
                        if key not in found_names:
                            findings.append(Finding(type="naming.generic", file=file_path, line=n.start_point[0] + 1, severity=0.8, confidence=1.0, message=f"Generic όνομα: '{name}'", human_alternative="Be descriptive.", rationale="Generic var."))
                            found_names.add(key)
            for c in n.children: find_ids(c)
        find_ids(tree.root_node)
        return findings

class SlopEngine:
    def __init__(self):
        self.parsers = {}
        self.scorer = ScoringEngine()
        self.buzzwords = [
            "absolutely thrilled", "comprehensive solution", "robust solution", "enterprise-grade", "cloud-native",
            "synergistic", "cosmic order", "space-time continuum", "as an ai language model", "delving into",
            "holistic", "paradigm", "encapsulated payload", "computation matrix", "quantum compatibility",
            "cloud-first architecture", "numerical entity", "robustness", "efficiency", "the provided",
            "initialization_timestamp", "parity", "evaluation", "cache_matrix", "holistic", "ai-driven"
        ]
        self.human_markers = ["TODO", "FIXME", "HACK", "WTF", "XXX", "STUPID", "WORKAROUND", "MAGIC", "DARK ARTS"]
        self.metrics_regex = re.compile(r"[\"']?(ai_confidence|confidence_score|accuracy_metric|ai_score|confidence|ai_confidence_score)[\"']?[\w\s_]*[:=]\s*0\.[789]\d*", re.IGNORECASE)
        self.stupid_logic_regex = re.compile(r"str\(.*\[-1\]|type\(.*\)\s*[=!]=", re.IGNORECASE)
        self.async_slop_regex = re.compile(r"asyncio\.sleep\(0\.(000|00|0)\d+\)", re.IGNORECASE)

    def analyze(self, content: str, lang: str, file_path: str, settings: Dict = None) -> AnalysisResult:
        try:
            findings = []
            found_indicators = set() 
            
            # Update settings
            sensitivity = settings.get("sensitivity", 50) if settings else 50
            humanity_shield = settings.get("humanity_shield", True) if settings else True
            experimental = settings.get("experimental", False) if settings else False
            
            self.scorer = ScoringEngine(sensitivity=sensitivity, humanity_shield=humanity_shield)

            # --- 1. Global Regex Pass ---
            for word in self.buzzwords:
                matches = re.finditer(re.escape(word), content, re.IGNORECASE)
                for m in matches:
                    if word not in found_indicators:
                        line_num = content.count('\n', 0, m.start()) + 1
                        findings.append(Finding(
                            type="comments.ai_style", file=file_path, line=line_num, severity=2.5, confidence=1.0,
                            message=f"GPT Buzzword: '{word}'", human_alternative="Be direct.", rationale="AI-style framing."
                        ))
                        found_indicators.add(word)
            
            # Humanity Shield Check
            if humanity_shield:
                for marker in self.human_markers:
                    if marker in content:
                        findings.append(Finding(
                            type="humanity.shield", file=file_path, line=1, severity=1.5, confidence=1.0,
                            message=f"Human Marker: '{marker}'", human_alternative="", rationale="Evidence of human frustration/intent."
                        ))

            for m in self.metrics_regex.finditer(content):
                raw_match = m.group(0)
                metric_name = raw_match.split(":")[0].split("=")[0].replace("\"", "").replace("'", "").strip()
                if metric_name not in found_indicators:
                    line_num = content.count('\n', 0, m.start()) + 1
                    findings.append(Finding(
                        type="statistical.fake_metric", file=file_path, line=line_num, severity=3.0, confidence=1.0,
                        message=f"Fake Metric Detected: '{metric_name}'", human_alternative="Remove fakes.", rationale="AI placeholders."
                    ))
                    found_indicators.add(metric_name)
            
            logic_match = self.stupid_logic_regex.search(content)
            if logic_match:
                findings.append(Finding(
                    type="statistical.stupid_logic", file=file_path, line=1, severity=3.5, confidence=1.0,
                    message="Anti-pattern Logic Detected", human_alternative="Use modern primitives.", rationale="AI logic smell."
                ))

            async_match = self.async_slop_regex.search(content)
            if async_match:
                findings.append(Finding(
                    type="statistical.async_slop", file=file_path, line=1, severity=3.5, confidence=1.0,
                    message="Async Enterprise Slop", human_alternative="Remove fake delays.", rationale="AI boilerplate async logic."
                ))

            # --- 2. AST Pass ---
            lang_pkg = tree_sitter_language_pack.get_language(lang)
            if lang not in self.parsers: self.parsers[lang] = Parser(lang_pkg)
            tree = self.parsers[lang].parse(content.encode('utf8'))
            findings.extend(NamingAnalyzer(lang).analyze(tree, content.encode('utf8'), file_path))
            findings.extend(SuspicionAnalyzer().analyze(tree, content.encode('utf8'), file_path))

            # --- 3. Experimental (Deep Scan) Pass ---
            if experimental:
                try:
                    from statistical_analyzer import StatisticalAnalyzer
                    from semantic_analyzer import SemanticAnalyzer
                    findings.extend(StatisticalAnalyzer(lang).analyze(tree, content.encode('utf8'), file_path))
                    findings.extend(SemanticAnalyzer(lang).analyze(tree, content.encode('utf8'), file_path))
                except ImportError: pass
            
            return self.scorer.calculate(findings)
        except Exception as e:
            return self.scorer.calculate([Finding(type="error", file=file_path, line=1, severity=0, confidence=0, message=str(e), human_alternative="", rationale="")])

    def run(self):
        if len(sys.argv) > 1:
            target = sys.argv[1]
            if os.path.isfile(target): self._cli_analyze_file(target)
            return
        for line in sys.stdin:
            try:
                data = json.loads(line)
                if data.get("command") == "analyze":
                    res = self.analyze(
                        data.get("content", ""), 
                        data.get("language", "python"), 
                        data.get("file_path", "unknown"),
                        settings=data.get("settings", {})
                    )
                    print(json.dumps(res.model_dump()))
                elif data.get("command") == "ping": print(json.dumps({"status": "pong"}))
                sys.stdout.flush()
            except Exception: pass

    def _cli_analyze_file(self, path: str):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
            ext = os.path.splitext(path)[1].lower().strip(".")
            lang = "python" if ext == "py" else ("c" if ext in ["c", "h"] else "unknown")
            res = self.analyze(content, lang, path)
            print(json.dumps(res.model_dump(), indent=2))
        except Exception: pass

if __name__ == "__main__":
    multiprocessing.freeze_support()
    SlopEngine().run()
