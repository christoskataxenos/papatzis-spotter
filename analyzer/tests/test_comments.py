import pytest
import tree_sitter_language_pack
from tree_sitter import Parser
from comment_analyzer import CommentAnalyzer

@pytest.fixture
def parser():
    lang = tree_sitter_language_pack.get_language('python')
    return Parser(lang)

@pytest.fixture
def analyzer():
    return CommentAnalyzer('python')

def test_ai_style_phrases(parser, analyzer):
    code = b"# This function calculates the sum\ndef add(a, b): return a + b"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert any("GPT-Style Παπατζιλίκι" in f.message for f in findings)

def test_obvious_comments(parser, analyzer):
    code = b"def loop():\n    # loop 10 times\n    for i in range(10): pass"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert any("αυτονόητο syntax" in f.message for f in findings)

def test_wikipedia_style(parser, analyzer):
    code = b"# This algorithm is a fundamental approach in computer science that allows efficient traversal of data structures without local context."
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert any("Θεωρητική ανάλυση" in f.message for f in findings)

def test_human_exclusions(parser, analyzer):
    code = b"# TODO: fix this\n# wtf?\n# lol cursed code"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert len(findings) == 0

def test_multilingual_human(parser, analyzer):
    code = "# Achtung: Dieser Code ist kaputt.\n# Εδώ υπάρχει ένα θέμα.".encode('utf8')
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert len(findings) == 0
