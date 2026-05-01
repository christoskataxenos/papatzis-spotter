import sys
import os
import json
import multiprocessing
import re
import math
import difflib
from abc import ABC, abstractmethod
from typing import List, Dict, Set, Tuple, Optional
import tree_sitter_language_pack
from tree_sitter import Tree, Parser, Query, Node, QueryCursor
from pydantic import BaseModel

from analyzer.models import Finding, PillarScore, AnalysisResult

# --- Engines ---

from analyzer.scoring_engine import ScoringEngine
from analyzer.suspicion_analyzer import SuspicionAnalyzer
from analyzer.naming_analyzer import NamingAnalyzer
from analyzer.similarity_analyzer import SimilarityAnalyzer
from analyzer.structural_analyzer import StructuralAnalyzer
from analyzer.comment_analyzer import CommentAnalyzer
from analyzer.redundancy_analyzer import RedundancyAnalyzer
from analyzer.logic_analyzer import LogicAnalyzer
from analyzer.statistical_analyzer import StatisticalAnalyzer
from analyzer.semantic_analyzer import SemanticAnalyzer
from analyzer.integrity_analyzer import IntegrityAnalyzer

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

    def detect_language(self, content: str, file_path: str = None) -> str:
        if file_path:
            ext = file_path.lower().split('.')[-1]
            if ext in ['c', 'h']: return 'c'
            if ext in ['cpp', 'cc', 'hpp']: return 'cpp'
            if ext == 'py': return 'python'

        scores = {"c": 0, "python": 0}
        c_strong = ["#include", "int main(", "printf(", "size_t", "malloc(", "free(", "struct ", "extern ", "typedef ", "#define "]
        c_weak = ["->", "//", "/*", "{", "};", "();", "bool ", "char "]
        
        for ind in c_strong:
            if ind in content: scores["c"] += 10
        for ind in c_weak:
            if ind in content: scores["c"] += 2
            
        if re.search(r"\bdef\s+", content): scores["python"] += 10
        if re.search(r"\bimport\s+", content): scores["python"] += 10
        if re.search(r"\bclass\s+", content): scores["python"] += 10
        
        py_weak = ["elif ", "lambda ", "if __name__ ==", "print(", "]:", "):\n", "    "]
        for ind in py_weak:
            if ind in content: scores["python"] += 2

        if scores["c"] > scores["python"]:
            return "c"
        elif scores["python"] > scores["c"]:
            return "python"
            
        return "python"

    def analyze(self, content: str, lang: str, file_path: str, settings: Dict = None, template_content: str = None) -> AnalysisResult:
        lang = lang.lower() if lang else "auto"
        if lang in ["auto", "unknown", "detect", "generic"]:
            lang = self.detect_language(content, file_path)
            
        try:
            findings = []
            findings.append(Finding(
                type="statistical.info",
                file=file_path,
                line=0,
                severity=0,
                confidence=1.0,
                message=f"Engine Mode: {lang.upper()}",
                human_alternative="",
                rationale=f"Analysis performed using {lang} specialized rules."
            ))

            # --- 0. Template Pass (Dynamic Whitelisting & Integrity) ---
            template_identifiers = set()
            if template_content:
                # 1. Dynamic Whitelisting
                template_identifiers = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', template_content))
                
                # 2. Integrity Check (difflib)
                import difflib
                t_lines = [line.strip() for line in template_content.splitlines() if line.strip() and "//" not in line and "/*" not in line]
                c_lines = [line.strip() for line in content.splitlines() if line.strip()]
                
                missing_essential = []
                for t_line in t_lines:
                    if t_line not in c_lines:
                        # Allow some flexibility for simple lines, but flag complex ones
                        if len(t_line) > 10 or "(" in t_line:
                            missing_essential.append(t_line)
                
                if missing_essential:
                    findings.append(Finding(
                        type="template.integrity",
                        file=file_path,
                        line=1,
                        severity=4.0, # High severity for template violation
                        confidence=1.0,
                        message=f"Template Integrity Violation: {len(missing_essential)} essential lines missing.",
                        human_alternative="Επαναφέρετε τη δομή του template που σας δόθηκε. Μην αλλάζετε τα ονόματα των συναρτήσεων ή τη δομή των structs.",
                        rationale=f"Ο καθηγητής έδωσε συγκεκριμένο template. Η αλλαγή του προδίδει προσπάθεια 'προσαρμογής' του κώδικα που παρήγαγε το AI στο δικό σας αρχείο, ή απλή αδιαφορία για τις οδηγίες."
                    ))

            # --- Template Processing & Line Mapping ---
            user_lines = set()
            if template_content:
                integrity = IntegrityAnalyzer(lang, template_content)
                template_identifiers = integrity.template_identifiers
                
                t_lines = template_content.splitlines()
                c_lines = content.splitlines()
                s = difflib.SequenceMatcher(None, t_lines, c_lines)
                for tag, i1, i2, j1, j2 in s.get_opcodes():
                    if tag in ('insert', 'replace'):
                        for line_idx in range(j1, j2):
                            user_lines.add(line_idx + 1)
                
                lang_pkg = tree_sitter_language_pack.get_language(lang)
                if lang not in self.parsers: self.parsers[lang] = Parser(lang_pkg)
                tree = self.parsers[lang].parse(content.encode('utf8', errors='replace'))
                findings.extend(integrity.analyze(tree, content.encode('utf8', errors='replace'), file_path))

            found_indicators = set() 
            sensitivity = settings.get("sensitivity", 50) if settings else 50
            humanity_shield = settings.get("humanity_shield", True) if settings else True
            
            self.scorer = ScoringEngine(sensitivity=sensitivity, humanity_shield=humanity_shield)

            # --- 1. Global Regex Pass ---
            for word in self.buzzwords:
                matches = re.finditer(re.escape(word), content, re.IGNORECASE)
                for m in matches:
                    if word not in found_indicators:
                        line_num = content.count('\n', 0, m.start()) + 1
                        if template_content and line_num not in user_lines:
                            continue

                        findings.append(Finding(
                            type="comments.ai_style", file=file_path, line=line_num, severity=2.5, confidence=1.0,
                            message=f"GPT Buzzword: '{word}'", 
                            human_alternative="Αφαίρεσε τους βαρύγδουπους όρους. Αντί για 'synergistic solution', πες 'data_merger'. Η ακρίβεια μετράει περισσότερο από το marketing.", 
                            rationale="Λέξεις όπως 'synergistic', 'comprehensive' ή 'holistic' χρησιμοποιούνται από το GPT για να 'γεμίσουν' το κείμενο και να ακούγονται εντυπωσιακά. Στον κώδικα όμως, θέλουμε ακρίβεια, όχι marketing."
                        ))
                        found_indicators.add(word)
            
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
                    if template_content and line_num not in user_lines: continue
                    findings.append(Finding(
                        type="statistical.fake_metric", file=file_path, line=line_num, severity=3.0, confidence=1.0,
                        message=f"Fake Metric Detected: '{metric_name}'", 
                        human_alternative="Αφαίρεσε τα ψεύτικα metrics. Αν χρειάζεσαι πραγματικό logging για το σύστημά σου, χρησιμοποίησε standard βιβλιοθήκες (όπως το logging της Python).", 
                        rationale="Το AI συχνά 'εφεύρει' μεταβλητές όπως `ai_confidence_score` ή `accuracy_metric` για να κάνει τον κώδικα να φαίνεται πιο 'έξυπνος' ή 'επιστημονικός', χωρίς αυτές να έχουν καμία πραγματική λειτουργία."
                    ))
                    found_indicators.add(metric_name)
            
            logic_match = self.stupid_logic_regex.search(content)
            if logic_match:
                findings.append(Finding(
                    type="statistical.stupid_logic", file=file_path, line=1, severity=3.5, confidence=1.0,
                    message="Anti-pattern Logic Detected", 
                    human_alternative="Χρησιμοποίησε τις σύγχρονες δυνατότητες της γλώσσας. Για παράδειγμα, αντί για `str(x)[-1]`, χρησιμοποίησε μαθηματικούς τελεστές ή built-in functions.", 
                    rationale="Το AI μερικές φορές προτείνει 'τεμπέλικες' λύσεις που φαίνονται σωστές αλλά είναι κακές προγραμματιστικά (π.χ. μετατροπή αριθμού σε string για να βρεις το τελευταίο ψηφίο). Ένας άνθρωπος προγραμματιστής ξέρει να χρησιμοποιεί τα σωστά εργαλεία."
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
            tree = self.parsers[lang].parse(content.encode('utf8', errors='replace'))
            
            analyzers = [
                NamingAnalyzer(lang, template_identifiers=template_identifiers),
                SimilarityAnalyzer(lang),
                SuspicionAnalyzer(lang),
                StructuralAnalyzer(lang),
                CommentAnalyzer(lang),
                RedundancyAnalyzer(lang),
                LogicAnalyzer(lang),
                StatisticalAnalyzer(lang),
                SemanticAnalyzer(lang)
            ]
            
            for analyzer in analyzers:
                try:
                    new_findings = analyzer.analyze(tree, content.encode('utf8', errors='replace'), file_path)
                    if template_content:
                        for f in new_findings:
                            if f.line > 0:
                                if f.line not in user_lines:
                                    f.severity *= 0.1
                                    f.confidence *= 0.5
                                else:
                                    f.severity *= 2.0
                    findings.extend(new_findings)
                except Exception as e:
                    findings.append(Finding(
                        type="statistical.error",
                        file=file_path,
                        line=0,
                        severity=0.5,
                        confidence=1.0,
                        message=f"Analyzer Error ({type(analyzer).__name__}): {str(e)}",
                        human_alternative="",
                        rationale=f"One of the specialized analyzers failed. The rest of the results are still valid."
                    ))

            return self.scorer.calculate(findings)
        except Exception as e:
            import traceback
            error_msg = f"Analysis Error: {str(e)}\n{traceback.format_exc()}"
            return self.scorer.calculate([Finding(
                type="statistical.error", 
                file=file_path, 
                line=1, 
                severity=5.0,
                confidence=1.0, 
                message=f"Critical Analysis Error: {str(e)}", 
                human_alternative="Διαπιστώθηκε εσωτερικό σφάλμα κατά την ανάλυση. Ελέγξτε αν ο κώδικας είναι έγκυρος για την επιλεγμένη γλώσσα.", 
                rationale=error_msg
            )])

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
                        settings=data.get("settings", {}),
                        template_content=data.get("template", None)
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
