import pytest
import tree_sitter_language_pack
from tree_sitter import Parser
from structural_analyzer import StructuralAnalyzer

@pytest.fixture
def parser():
    lang = tree_sitter_language_pack.get_language('python')
    return Parser(lang)

@pytest.fixture
def analyzer():
    return StructuralAnalyzer('python', ui_lang='EL')

def test_redundant_if(parser, analyzer):
    code = b"def is_positive(x):\n    if x > 0:\n        return True\n    else:\n        return False"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    print(f"Structural findings: {[f.type for f in findings]}")
    print(f"Structural messages: {[f.message for f in findings]}")
    assert any("Δομική Φλυαρία (Logic Verbosity)" in f.message for f in findings)

def test_proxy_function(parser, analyzer):
    code = b"def wrapper(x):\n    return some_other_function(x)"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert any("Άδεια Συνάρτηση (Wrapper Slop)" in f.message for f in findings)

def test_clean_structural(parser, analyzer):
    code = b"def is_positive(x):\n    return x > 0"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert len(findings) == 0
