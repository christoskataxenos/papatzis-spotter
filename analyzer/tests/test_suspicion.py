import pytest
import tree_sitter_language_pack
from tree_sitter import Parser
from suspicion_analyzer import SuspicionAnalyzer
import textwrap

@pytest.fixture
def parser():
    lang = tree_sitter_language_pack.get_language('python')
    return Parser(lang)

@pytest.fixture
def analyzer():
    return SuspicionAnalyzer('python')

def test_ai_signature(parser, analyzer):
    # Long docstring, tiny body
    code = textwrap.dedent('''
        def add(a, b):
            """
            This function takes two parameters, a and b, which should be numbers.
            It then performs an addition operation on these two numbers and returns
            the resulting sum to the caller of the function.
            """
            return a + b
    ''').strip().encode('utf8')
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert any("suspicion.boilerplate_density" in f.type for f in findings)

def test_ai_filler(parser, analyzer):
    code = b"# As an AI language model, here is the solution\ndef run(): pass"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert any("suspicion.ai_filler" in f.type for f in findings)

def test_clean_suspicion(parser, analyzer):
    code = b"def add(a, b):\n    return a + b\n\ndef sort_list(my_list):\n    my_list.sort()"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert len(findings) == 0
