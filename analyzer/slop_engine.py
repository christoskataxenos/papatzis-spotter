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

from models import Finding, PillarScore, AnalysisResult

# --- Engines ---

from scoring_engine import ScoringEngine
from suspicion_analyzer import SuspicionAnalyzer
from naming_analyzer import NamingAnalyzer

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
