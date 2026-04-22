import pytest
import tree_sitter_language_pack
from tree_sitter import Parser
from redundancy_analyzer import RedundancyAnalyzer

@pytest.fixture
def parser():
    lang = tree_sitter_language_pack.get_language('python')
    return Parser(lang)

@pytest.fixture
def analyzer():
    return RedundancyAnalyzer('python')

def test_unreachable_code(parser, analyzer):
    code = b"def do_something():\n    return 10\n    print('This is unreachable')"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert any("Unreachable Code" in f.message for f in findings)

def test_over_abstraction_class(parser, analyzer):
    code = b"class Processor:\n    def process(self, x):\n        return x * 2"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert any("Over-abstraction" in f.message for f in findings)

def test_clean_redundancy(parser, analyzer):
    code = b"def process(x):\n    return x * 2\n\nclass MultiMethod:\n    def __init__(self, val):\n        self.val = val\n    def do(self):\n        return self.val"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert len(findings) == 0
