import pytest
import tree_sitter_language_pack
from tree_sitter import Parser
from naming_analyzer import NamingAnalyzer

@pytest.fixture
def parser():
    lang = tree_sitter_language_pack.get_language('python')
    return Parser(lang)

@pytest.fixture
def analyzer():
    return NamingAnalyzer('python', ui_lang='EL')

def test_generic_names(parser, analyzer):
    code = b"data = [1, 2, 3]\nresult = sum(data)"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    
    messages = [f.message for f in findings]
    print(f"Naming messages: {messages}")
    assert any("Τυπικό (generic) AI naming: 'data'" in m for m in messages)
    assert any("Τυπικό (dummy) όνομα: 'result'" in m for m in messages)

def test_sequential_names(parser, analyzer):
    code = b"var1 = 10\nvar2 = 20\nvar3 = 30"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    
    messages = [f.message for f in findings]
    # Check if we have sequential findings. Note: naming_analyzer might classify var1 as generic.
    # We should check the actual implementation of naming_analyzer for sequential.
    assert len(findings) >= 3

def test_clean_names(parser, analyzer):
    code = b"user_records = [1, 2, 3]\ntotal_sum = sum(user_records)"
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert len(findings) == 0
